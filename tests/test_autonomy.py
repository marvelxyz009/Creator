import json
import struct
import subprocess
import tempfile
import unittest
import zlib
from pathlib import Path
from unittest.mock import patch
from story_studio.core import Studio, cli_failure
from story_studio.discovery import Discovery
from story_studio.manga_worker import MangaWorker, MCPAgent
from story_studio.png import validate_png

# Tiny pixel images are test transport fixtures, never presented as manga.
def png_pixel(value):
    def chunk(kind, data):
        return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind+data)&0xffffffff)
    return b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", struct.pack(">IIBBBBB",1,1,8,2,0,0,0)) + chunk(b"IDAT", zlib.compress(bytes([0,value,0,0]))) + chunk(b"IEND",b"")

class ProposalProvider:
    mode = "codex"
    def generate(self, prompt):
        extra = {"genres":["Trinh thám"]} if "concept directions" in prompt else {"length":"novel"} if "story directions" in prompt else {"direction":"rtl"}
        return json.dumps({"options":[{"title":f"Choice {i}","summary":f"Distinct direction {i}","tradeoff":"A concrete cost",**extra} for i in range(3)]})

class PageProvider:
    mode = "codex"
    def generate(self, prompt):
        return json.dumps({"pages":[{"number":1,"prompt":"Complete composition","dialogue":["Xin chào."]}]})

class ImageFixture:
    def __init__(self, mode, *, fail=False, unreadable=False, wrong_text=False):
        self.draws=0; self.fail=fail; self.unreadable=unreadable; self.wrong_text=wrong_text
    def draw(self, page, folder, previous=None, feedback=None):
        self.draws+=1
        file=folder/f"fixture-{self.draws}.png"
        file.write_bytes(png_pixel(self.draws))
        return file
    def review(self, page, file, folder):
        assert file.is_file()
        ok=self.draws>1 and not self.fail
        return {"pass":ok,"inspected":not self.unreadable,"notes":"Actual fixture inspected by fake test model", "issues":[] if ok else ["Panel 1 unreadable"],"observed_dialogue":["Wrong"] if self.wrong_text else ["Xin chào."]}

class AutonomyTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory()
        self.s=Studio(self.tmp.name,ProposalProvider())
    def tearDown(self):
        self.tmp.cleanup()
    def source(self):
        p=self.s.create({"title":"Fixture","idea":"Family mystery"})["id"]
        edit=self.s.save(p,1,"edit","The approved prose.")
        self.s.save(p,1,"continuity",json.dumps({"pass":True,"issues":[],"canon_delta":{}}),[edit])
        self.s.approve(p,edit)
        lettering=self.s.save(p,1,"lettering","Exact dialogue design",[edit])
        self.s.save(p,1,"image_prompt","Complete source-linked manga brief",[edit,lettering])
        self.s.provider=PageProvider()
        return p
    def test_three_by_three_discovery_persists_choices(self):
        d=Discovery(self.s);row=d.start()
        for step in ("concept","story","art"):
            self.assertTrue(d.run_one())
            current=d.get(row["id"])
            self.assertEqual((current["step"],current["status"],len(current["options"])),(step,"ready",3))
            row=d.choose(row["id"],1)
        p=self.s.project(row["project"])
        self.assertEqual(p["length"],"novel")
        self.assertEqual(len(p["creative_choices"]),3)
        self.assertTrue(p["manga_auto"])
        self.assertEqual(Discovery(Studio(self.tmp.name,ProposalProvider())).get(row["id"])["status"],"completed")
    def test_discovery_rejects_duplicate_or_missing_options(self):
        self.s.provider=type("Bad",(),{"generate":lambda _,p:'{"options":[]}'})()
        d=Discovery(self.s);row=d.start();d.run_one()
        self.assertEqual(d.get(row["id"])["status"],"failed")
        with self.assertRaises(ValueError): d.choose(row["id"],0)
        self.assertFalse(self.s.projects())
    def test_discovery_restart_and_retry_are_bounded(self):
        d=Discovery(self.s);row=d.start();row.update(status="running",attempts=3);d.put(row);d.recover()
        self.assertEqual(d.get(row["id"])["status"],"failed")
        with self.assertRaises(ValueError):d.retry(row["id"])
    def test_actual_png_qa_repair_and_cbz(self):
        p=self.source();fake=ImageFixture("codex");w=MangaWorker(self.s,lambda mode:fake)
        job=w.enqueue(p);self.assertEqual(w.enqueue(p)["id"],job["id"]);w.run_one()
        done=w.jobs(p)[0];self.assertEqual(done["status"],"done");self.assertEqual(fake.draws,2)
        self.assertTrue(self.s.export_cbz(p,1).is_file())
        self.assertIn("image_sha256",done["pages"][0]["qa"])
    def test_failed_qa_never_approves_and_repairs_are_bounded(self):
        p=self.source();fake=ImageFixture("codex",fail=True);w=MangaWorker(self.s,lambda mode:fake);w.enqueue(p);w.run_one()
        self.assertEqual(fake.draws,3)
        self.assertEqual(w.jobs(p)[0]["status"],"failed")
        self.assertFalse([a for a in self.s.artifacts(p) if a["kind"]=="page"])
    def test_uninspected_image_stops_without_repair(self):
        p=self.source();fake=ImageFixture("codex",unreadable=True);w=MangaWorker(self.s,lambda mode:fake);w.enqueue(p);w.run_one()
        self.assertEqual(fake.draws,1);self.assertEqual(w.jobs(p)[0]["status"],"failed")
    def test_dialogue_mismatch_prevents_auto_approval(self):
        p=self.source();fake=ImageFixture("codex",wrong_text=True);w=MangaWorker(self.s,lambda mode:fake);w.enqueue(p);w.run_one()
        self.assertEqual(w.jobs(p)[0]["status"],"failed")
    def test_source_revision_race_rejects_generated_pages(self):
        p=self.source();fake=ImageFixture("codex");original=fake.review
        def review(page,file,folder):
            result=original(page,file,folder)
            if result["pass"]: self.s.save(p,1,"edit","New source invalidates generation")
            return result
        fake.review=review
        w=MangaWorker(self.s,lambda mode:fake);w.enqueue(p);w.run_one()
        self.assertEqual(w.jobs(p)[0]["status"],"failed")
        self.assertFalse([a for a in self.s.artifacts(p) if a["kind"]=="page"])
    def test_qa_cli_transports_actual_image(self):
        folder=Path(self.tmp.name);file=folder/"actual.png";file.write_bytes(png_pixel(1))
        def run(command,**kw):
            self.assertIn("--image",command);self.assertIn(str(file),command)
            Path(command[command.index("--output-last-message")+1]).write_text('{"pass":false}',encoding="utf-8")
            return subprocess.CompletedProcess(command,0,"","")
        with patch("story_studio.manga_worker.shutil.which",return_value="fixture"),patch("story_studio.manga_worker.subprocess.run",side_effect=run):
            result=MCPAgent().review({"dialogue":[]},file,folder)
        self.assertFalse(result["pass"])
    def test_draw_requires_successful_tool_receipt(self):
        folder=Path(self.tmp.name)
        def run(command,**kw):
            (folder/"generated.png").write_bytes(png_pixel(1))
            Path(command[command.index("--output-last-message")+1]).write_text('{"file":"generated.png","tool":"generate_image"}',encoding="utf-8")
            return subprocess.CompletedProcess(command,0,json.dumps({"item":{"type":"mcp_tool_call","status":"completed","tool":"generate_image","result":{"isError":False}}}),"")
        with patch("story_studio.manga_worker.shutil.which",return_value="fixture"),patch("story_studio.manga_worker.subprocess.run",side_effect=run):
            self.assertTrue(MCPAgent().draw({"dialogue":[]},folder).is_file())
        def no_receipt(command,**kw):
            result=run(command,**kw)
            result.stdout=""
            return result
        with patch("story_studio.manga_worker.shutil.which",return_value="fixture"),patch("story_studio.manga_worker.subprocess.run",side_effect=no_receipt):
            with self.assertRaises(ValueError):MCPAgent().draw({"dialogue":[]},folder)
    def test_model_selection_persists_without_changing_global_config(self):
        self.s.select_provider("codex","fixture-model")
        restored=Studio(self.tmp.name)
        self.assertEqual(restored.provider.model,"fixture-model")
        with self.assertRaises(ValueError):self.s.select_provider("codex","bad model")
        self.assertIn("Model Codex",cli_failure("codex","The model is not supported when using Codex with a ChatGPT account"))
    def test_png_rejects_truncation_crc_and_missing_pixels(self):
        raw=png_pixel(1);self.assertEqual(validate_png(raw),(1,1))
        for bad in (raw[:-3],raw[:33],raw[:-5]+b"abcde"):
            with self.assertRaises(ValueError):validate_png(bad)

if __name__=="__main__": unittest.main()
