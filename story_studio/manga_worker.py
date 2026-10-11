"""Background MCP image production, actual-image QA and bounded repairs."""
import hashlib
import json
import os
import re
import shutil
import subprocess
from pathlib import Path
from .core import uid, now, encode, PACKAGE_ROOT, cli_failure
from .discovery import parse_json
from .png import validate_png

class MCPAgent:
    def __init__(self, mode="codex", model=""):
        if mode not in ("codex", "claude"):
            raise ValueError("Manga worker requires Codex or Claude")
        self.mode = mode
        self.model = model

    def call(self, prompt, folder, image=None):
        executable = shutil.which(self.mode)
        if not executable:
            raise ValueError("Missing " + self.mode + " CLI")
        output = folder / (uid() + "-response.json")
        if self.mode == "codex":
            command = [executable, "exec", "--ephemeral", "--skip-git-repo-check", "--sandbox", "workspace-write", "--color", "never", "--json", "--output-last-message", str(output)]
            if image:
                command.extend(["--image", str(image)])
            command.append("-")
        else:
            # Read is necessary for real visual inspection; configured MCP tools stay available.
            command = [executable, "-p", "--output-format", "stream-json", "--verbose"]
            if image:
                prompt = "Read the actual local image at " + str(image) + " using your image-capable Read tool before judging it.\n" + prompt
        model = self.model or os.environ.get("STUDIO_MODEL")
        if model:
            command.extend(["--model", model])
        result = subprocess.run(command, input=prompt, text=True, encoding="utf-8", errors="replace", capture_output=True, cwd=folder, timeout=900, creationflags=subprocess.CREATE_NO_WINDOW if os.name == "nt" else 0)
        if result.returncode:
            raise ValueError(cli_failure(self.mode, result.stderr))
        events = []
        for line in result.stdout.splitlines():
            try:
                events.append(json.loads(line))
            except json.JSONDecodeError:
                continue
        self.tool_receipts = []
        requests = {}
        for event in events:
            item = event.get("item", {})
            if item.get("type") == "mcp_tool_call" and item.get("status") == "completed" and not item.get("error") and not (item.get("result") or {}).get("isError"):
                self.tool_receipts.append({"name": str(item.get("tool", "")), "arguments": item.get("arguments", {})})
            for content in event.get("message", {}).get("content", []):
                if content.get("type") == "tool_use":
                    requests[content["id"]] = {"name": content.get("name", ""), "arguments": content.get("input", {})}
                if content.get("type") == "tool_result" and not content.get("is_error") and content.get("tool_use_id") in requests:
                    self.tool_receipts.append(requests[content["tool_use_id"]])
        (folder / (output.stem + "-tools.json")).write_text(encode(self.tool_receipts), encoding="utf-8")
        if self.mode == "codex":
            text = output.read_text(encoding="utf-8") if output.exists() else ""
        else:
            final = next((e for e in reversed(events) if e.get("type") == "result"), {})
            if final.get("is_error"):
                raise ValueError("Claude media agent returned an error")
            text = final.get("result", "")
        return parse_json(text)

    def draw(self, page, folder, previous=None, feedback=None):
        skill = (PACKAGE_ROOT / "skills" / "art-director" / "SKILL.md").read_text(encoding="utf-8")
        prompt = skill + "\nUse an ACTUAL configured MCP image-generation tool to " + ("edit the attached image" if previous else "generate this manga page") + ". Download/save the tool's actual generated PNG inside the current working folder with a NEW filename. Never draw using code, fabricate a placeholder, or claim a text prompt is an image. If no image tool is available return JSON {\"error\":\"missing MCP image generation tool\"}. Return ONLY JSON {\"file\":\"relative.png\",\"tool\":\"actual MCP tool name\"}. Preserve page composition and identity during repair. Project, source, exact dialogue and art direction:\n" + encode(page) + "\nRepair findings: " + encode(feedback or [])
        result = self.call(prompt, folder, previous)
        if result.get("error"):
            raise ValueError(str(result["error"]))
        reported = str(result.get("tool", ""))
        allowed_tool = os.environ.get("STUDIO_IMAGE_TOOL", "")
        if allowed_tool and reported != allowed_tool:
            raise ValueError("Image agent used a different tool from STUDIO_IMAGE_TOOL")
        if not allowed_tool and not re.search(r"generate.*image|image.*generat|imagegen|edit.*image|image.*edit|draw.*page", reported, re.I):
            raise ValueError("Receipt is not from an identifiable image generation/edit tool; set STUDIO_IMAGE_TOOL for a custom tool")
        if not any(r["name"] and (r["name"] == reported or reported.endswith("__" + r["name"])) for r in self.tool_receipts if self.mode == "codex" or r["name"].startswith("mcp__")):
            raise ValueError("No successful MCP image-tool receipt; generated file alone is not proof of generation")
        file = (folder / result["file"]).resolve()
        if not file.is_relative_to(folder.resolve()) or not file.is_file() or file.suffix.lower() != ".png" or not result.get("tool"):
            raise ValueError("Image agent did not return an actual local PNG from an image tool")
        return file

    def review(self, page, file, folder):
        digest = hashlib.sha256(file.read_bytes()).hexdigest()
        prompt = "Inspect the ACTUAL attached manga image against the provided approved-source page plan. Judge character identity, acting, story causality, anatomy affecting action, panel geography, reading direction, balloon placement and legibility. Read every balloon. Do not infer quality from the prompt. Return ONLY JSON {\"pass\":boolean,\"inspected\":boolean,\"notes\":\"observed details\",\"issues\":[\"specific page/panel repair instruction\"],\"observed_dialogue\":[\"exact balloon text in reading order\"]}. Pass only if there are no material issues; exact dialogue must match the plan. If the image cannot be viewed inspected=false, pass=false.\nExpected page:\n" + encode(page)
        result = self.call(prompt, folder, file)
        if self.mode == "claude" and not any(r["name"] == "Read" and str(r["arguments"].get("file_path", "")) == str(file) for r in self.tool_receipts):
            raise ValueError("Claude did not read the actual local image")
        result["image_sha256"] = digest
        return result

class MangaWorker:
    def __init__(self, studio, agent_factory=None):
        self.studio = studio
        self.agent_factory = agent_factory or (lambda mode: MCPAgent(mode, getattr(studio.provider, "model", "")))
        with studio.connect() as db:
            db.execute("CREATE TABLE IF NOT EXISTS media_jobs(id TEXT PRIMARY KEY, body TEXT NOT NULL)")

    def put(self, row):
        with self.studio.connect() as db:
            db.execute("INSERT OR REPLACE INTO media_jobs VALUES (?,?)", (row["id"], encode(row)))
        return row

    def jobs(self, project=None):
        with self.studio.connect() as db:
            rows = [json.loads(r[0]) for r in db.execute("SELECT body FROM media_jobs ORDER BY rowid")]
        return [r for r in rows if not project or r["project"] == project]

    def enqueue(self, project, chapter=1):
        with self.studio.lock:
            source = self.studio.latest(project, chapter, "edit", approved=True)
            brief = self.studio.latest(project, chapter, "image_prompt")
            if not source or not brief:
                raise ValueError("Chốt bản gốc và hoàn thành brief trước khi vẽ")
            for job in self.jobs(project):
                if job["chapter"] == chapter and job["brief"] == brief["id"] and job["status"] in ("queued", "running", "done"):
                    return job
            mode = getattr(self.studio.provider, "mode", "codex")
            if mode not in ("codex", "claude"):
                raise ValueError("Chọn Codex hoặc Claude cho MCP worker")
            return self.put({"id": uid(), "project": project, "chapter": chapter, "source": source["id"], "brief": brief["id"], "mode": mode, "status": "queued", "attempts": 0, "pages": [], "plan": None, "error": "", "created": now()})

    def recover(self):
        for job in self.jobs():
            if job["status"] == "running":
                job.update(status="failed", error="Worker bị ngắt; các trang đã chốt được giữ lại")
                self.put(job)

    def retry(self, id):
        with self.studio.lock:
            job = next((j for j in self.jobs() if j["id"] == id), None)
            if not job or job["status"] != "failed" or job["attempts"] >= 3:
                raise ValueError("Retry limit reached")
            self.check_source(job)
            job.update(status="queued", error="")
            return self.put(job)

    def check_source(self, job):
        source = self.studio.latest(job["project"], job["chapter"], "edit", approved=True)
        brief = self.studio.latest(job["project"], job["chapter"], "image_prompt")
        if not source or not brief or (source["id"], brief["id"]) != (job["source"], job["brief"]):
            raise ValueError("Nguồn/brief đã đổi; tạo tác vụ vẽ mới")
        return source, brief

    def run_one(self):
        with self.studio.lock:
            job = next((j for j in self.jobs() if j["status"] == "queued" and not self.studio.project(j["project"]).get("paused")), None)
            if not job:
                return False
            job.update(status="running", attempts=job["attempts"]+1)
            self.put(job)
        try:
            source, brief = self.check_source(job)
            folder = self.studio.root / "projects" / job["project"] / "media_jobs" / job["id"]
            folder.mkdir(parents=True, exist_ok=True)
            agent = self.agent_factory(job["mode"])
            if job["plan"] is None:
                packet, _ = self.studio.prompt(job["project"], job["chapter"], "image_prompt")
                result = parse_json(self.studio.provider.generate("Return ONLY JSON {\"pages\":[{\"number\":1,\"prompt\":\"complete visual composition with exact source-linked scene\",\"dialogue\":[\"exact balloon text in reading order\"]}]}. Convert the existing manga brief into executable page plans; preserve all scenes and exact dialogue, no omitted pages. Do not generate images. Context:\n" + packet + "\nExisting brief:\n" + brief["body"]))
                pages = result.get("pages")
                if not isinstance(pages, list) or not 1 <= len(pages) <= 64:
                    raise ValueError("Invalid page plan (1–64 pages per chapter)")
                for i, page in enumerate(pages, 1):
                    if page.get("number") != i or not isinstance(page.get("prompt"), str) or not page["prompt"].strip() or not isinstance(page.get("dialogue"), list) or any(not isinstance(t, str) for t in page["dialogue"]):
                        raise ValueError("Invalid page sequence or exact dialogue contract")
                job["plan"] = pages
                self.put(job)
            completed = {p["number"] for p in job["pages"]}
            for page in job["plan"]:
                if page["number"] in completed:
                    continue
                self.check_source(job)
                if self.studio.project(job["project"]).get("paused"):
                    job["status"] = "queued"
                    self.put(job)
                    return True
                page = {**page, "project": self.studio.project(job["project"]), "approved_source": source["body"], "source_revision": source["id"], "artifacts": [r for r in self.studio.artifacts(job["project"]) if r["chapter"] == job["chapter"] and r["kind"] in ("art", "characters", "lettering") and not r["stale"]]}
                file = agent.draw(page, folder)
                passed = False
                for attempt in range(3):
                    # Validate the real file before asking a vision model to inspect it.
                    raw = file.read_bytes()
                    validate_png(raw)
                    snapshot = folder / f"page-{page['number']}-attempt-{attempt}.png"
                    snapshot.write_bytes(raw)
                    report = agent.review(page, snapshot, folder)
                    if snapshot.read_bytes() != raw:
                        raise ValueError("QA modified the inspected image; review is invalid")
                    if type(report.get("pass")) is not bool or type(report.get("inspected")) is not bool or not isinstance(report.get("issues"), list) or not isinstance(report.get("notes"), str) or not report["notes"].strip() or not isinstance(report.get("observed_dialogue"), list):
                        raise ValueError("Invalid visual QA contract")
                    report["image_sha256"] = hashlib.sha256(raw).hexdigest()
                    normalize = lambda lines: [" ".join(t.split()) for t in lines]
                    text_matches = all(isinstance(t, str) for t in report["observed_dialogue"]) and normalize(report["observed_dialogue"]) == normalize(page["dialogue"])
                    if not text_matches:
                        report["issues"].append("Exact balloon text or reading order differs from the approved page plan")
                    passed = report["pass"] and report["inspected"] and not report["issues"] and text_matches
                    report["model_pass"] = report["pass"]
                    report["pass"] = passed
                    (folder / f"page-{page['number']}-review-{attempt}.json").write_text(encode(report), encoding="utf-8")
                    if passed:
                        break
                    if not report["inspected"]:
                        raise ValueError("Vision model did not inspect the actual image")
                    if attempt < 2:
                        previous_hash = hashlib.sha256(raw).hexdigest()
                        file = agent.draw(page, folder, snapshot, report["issues"] or ["Visual QA failed; revisit all listed criteria"])
                        if hashlib.sha256(file.read_bytes()).hexdigest() == previous_hash:
                            raise ValueError("Repair returned the unchanged image")
                if not passed:
                    raise ValueError(f"Trang {page['number']} vẫn không đạt sau hai lần sửa")
                with self.studio.lock:
                    self.check_source(job)
                    artifact = self.studio.import_page(job["project"], job["chapter"], page["number"], raw)
                    self.studio.approve_page(job["project"], artifact, "Model visual QA (not human review): " + encode(report))
                    job["pages"].append({"number": page["number"], "artifact": artifact, "qa": report})
                    self.put(job)
            self.check_source(job)
            job["status"] = "done"
        except Exception as exc:
            job.update(status="failed", error=str(exc)[:700])
        self.put(job)
        return True
