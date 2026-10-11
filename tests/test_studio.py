import json
import tempfile
import threading
import unittest
import urllib.request
from pathlib import Path
from story_studio.core import STAGES, Studio, TextProvider
from unittest.mock import patch
import subprocess
import os
from story_studio.server import Server

class FakeProvider:
    """Deterministic test fixture, never used by the shipped application."""
    def generate(self, prompt):
        if 'TASK: Audit' in prompt:
            return json.dumps({"pass": True, "issues": [], "canon_delta": {"events": ["A door opened"]}})
        return "Original fixture output for the current production stage. " + prompt[:80]

class StudioTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.s = Studio(self.tmp.name, FakeProvider())
        self.p = self.s.create({"title": "Fixture", "idea": "A family mystery", "genres": ["Trinh thám"], "mode": "semi"})["id"]
    def tearDown(self):
        self.tmp.cleanup()
    def pipeline(self):
        self.s.enqueue(self.p)
        for _ in range(5):
            self.assertTrue(self.s.run_one())
        self.assertEqual(self.s.jobs()[-1]["status"], "needs_review")
    def test_cli_adapters_transport_prompt_and_handle_failure(self):
        for mode in ("codex", "claude"):
            def run(command, **kwargs):
                self.assertIn("Requested chapter", kwargs["input"])
                self.assertNotIn("--dangerously-bypass-approvals-and-sandbox", command)
                if mode == "codex":
                    Path(command[command.index("--output-last-message")+1]).write_text("A complete generated chapter for testing.", encoding="utf-8")
                else:
                    self.assertIn("--tools", command)
                return subprocess.CompletedProcess(command, 0, "A complete generated chapter for testing.", "")
            with patch.dict(os.environ, {"STUDIO_PROVIDER": mode}, clear=False), patch("story_studio.core.shutil.which", return_value="fixture-cli"), patch("story_studio.core.subprocess.run", side_effect=run):
                self.assertIn("chapter", TextProvider().generate("Requested chapter"))
            with patch("story_studio.core.shutil.which", return_value=None):
                with self.assertRaises(ValueError):
                    TextProvider(mode).generate("Requested chapter")
    def test_engine_selection_is_persisted(self):
        self.s.select_provider("claude")
        with patch.dict(os.environ, {}, clear=True):
            self.assertEqual(Studio(self.tmp.name).provider.mode, "claude")
        with self.assertRaises(ValueError):
            self.s.select_provider("arbitrary-shell")
    def test_pause_defers_queued_work(self):
        self.s.enqueue(self.p)
        self.s.pause(self.p, True)
        self.assertFalse(self.s.run_one())
        self.assertEqual(self.s.jobs()[0]["status"], "queued")
        self.s.pause(self.p, False)
        self.assertTrue(self.s.run_one())
    def test_changed_source_rejects_late_submission(self):
        first = self.s.save(self.p, 1, "bible", "Initial bible")
        self.s.save(self.p, 1, "bible", "Revised bible")
        with self.assertRaises(ValueError):
            self.s.save(self.p, 1, "outline", "Late outline", [first])
    def test_pipeline_gates_source(self):
        self.pipeline()
        with self.assertRaises(ValueError):
            self.s.prompt(self.p, 1, "adaptation")
        self.s.continue_job(self.s.jobs()[-1]["id"])
        source = self.s.latest(self.p, 1, "edit", approved=True)
        self.assertIsNotNone(source)
        self.s.run_one()
        self.assertIn(source["id"], self.s.latest(self.p, 1, "adaptation")["parents"])
    def test_revision_invalidates_transitive_dependencies(self):
        self.pipeline()
        self.s.continue_job(self.s.jobs()[-1]["id"])
        self.s.run_one()
        self.s.run_one()
        source = self.s.latest(self.p, 1, "edit")
        self.s.save(self.p, 1, "edit", "Changed source chapter with a different outcome", source["parents"])
        self.assertIsNone(self.s.latest(self.p, 1, "adaptation"))
        self.assertIsNone(self.s.latest(self.p, 1, "storyboard"))
        self.assertIsNone(self.s.latest(self.p, 1, "edit", approved=True))
        with self.assertRaises(ValueError):
            self.s.export(self.p)
    def test_source_cannot_approve_without_matching_audit(self):
        id = self.s.save(self.p, 1, "edit", "Text")
        with self.assertRaises(ValueError):
            self.s.approve(self.p, id)
    def test_duplicate_jobs_and_restart_recovery(self):
        job = self.s.enqueue(self.p)
        self.assertEqual(job, self.s.enqueue(self.p))
        with self.s.connect() as db:
            db.execute("UPDATE jobs SET status='running' WHERE id=?", (job,))
        another = Studio(self.tmp.name, FakeProvider())
        another.recover()
        self.assertEqual(another.jobs()[0]["status"], "failed")
        another.retry(job)
        self.assertTrue(another.run_one())
    def test_bad_report_stops_chain(self):
        class Bad(FakeProvider):
            def generate(self, prompt):
                if 'TASK: Audit' in prompt:
                    return '{"pass":false,"issues":["Contradiction"],"canon_delta":{}}'
                return super().generate(prompt)
        self.s.provider = Bad()
        self.s.enqueue(self.p)
        for _ in range(5):
            self.s.run_one()
        self.assertEqual(self.s.jobs()[-1]["status"], "failed")
        self.assertIsNone(self.s.latest(self.p, 1, "edit", approved=True))
    def test_auto_mode_chains_to_image_brief_gate(self):
        p = self.s.create({"title": "Auto", "idea": "A haunted station", "mode": "auto"})["id"]
        self.s.enqueue(p)
        for _ in STAGES:
            self.s.run_one()
        self.assertEqual(self.s.jobs(p)[-1]["stage"], "image_prompt")
        self.assertEqual(self.s.jobs(p)[-1]["status"], "needs_review")
        self.assertIsNotNone(self.s.latest(p, 1, "edit", approved=True))
    def test_next_chapter_requires_previous_approved(self):
        with self.assertRaises(ValueError):
            self.s.prompt(self.p, 2, "bible")
        self.pipeline()
        self.s.continue_job(self.s.jobs()[-1]["id"])
        _, parents = self.s.prompt(self.p, 2, "bible")
        self.assertIn(self.s.latest(self.p, 1, "edit")["id"], parents)
    def test_reference_scope_and_context(self):
        with self.assertRaises(ValueError):
            self.s.add_reference({"content": "An example"})
        self.s.add_reference({"title": "Mystery craft", "content": "Use delayed disclosure", "rights": "notes_only", "genre": "Trinh thám"})
        prompt, _ = self.s.prompt(self.p, 1, "bible")
        self.assertIn("Use delayed disclosure", prompt)
    def test_wrong_project_parent_is_rejected(self):
        p2 = self.s.create({"title": "Other", "idea": "Different"})["id"]
        a = self.s.save(p2, 1, "bible", "Other world")
        with self.assertRaises(ValueError):
            self.s.save(self.p, 1, "draft", "Wrong", [a])
    def test_retry_limit(self):
        id = self.s.enqueue(self.p)
        with self.s.connect() as db:
            db.execute("UPDATE jobs SET status='failed',attempts=3 WHERE id=?", (id,))
        with self.assertRaises(ValueError):
            self.s.retry(id)
    def test_cbz_requires_approved_pages(self):
        self.pipeline()
        self.s.continue_job(self.s.jobs()[-1]["id"])
        for _ in range(4):
            self.s.run_one()
        # A real tiny PNG fixture, not generated artwork.
        import base64
        raw = base64.b64decode('iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mP8/x8AAwMCAO+a6XsAAAAASUVORK5CYII=')
        id = self.s.import_page(self.p, 1, 1, raw)
        with self.assertRaises(ValueError):
            self.s.export_cbz(self.p, 1)
        self.s.approve_page(self.p, id, "Fixture visually reviewed")
        self.assertTrue(self.s.export_cbz(self.p, 1).is_file())
    def test_api_rejects_cross_origin_and_missing_token(self):
        server = Server(("127.0.0.1", 0), self.s)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        base = f"http://127.0.0.1:{server.server_port}"
        try:
            with urllib.request.urlopen(base + "/api/state") as response:
                self.assertEqual(len(json.load(response)["projects"]), 1)
            req = urllib.request.Request(base + "/api/projects", data=b'{}', headers={"Content-Type": "application/json"})
            with self.assertRaises(urllib.error.HTTPError):
                urllib.request.urlopen(req)
            req.add_header("X-Studio-Token", server.token)
            req.add_header("Origin", "https://untrusted.example")
            with self.assertRaises(urllib.error.HTTPError):
                urllib.request.urlopen(req)
        finally:
            server.shutdown()
            server.server_close()

if __name__ == "__main__":
    unittest.main()
