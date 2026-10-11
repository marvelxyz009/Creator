"""Persist decisions and handoffs for the active chat; never invoke a model."""
import hashlib
import json
from pathlib import Path
from .core import STAGES, GENRES, uid, now, encode

KINDS = ("concept", "story", "art")

class ChatWorkflow:
    def __init__(self, studio):
        self.studio = studio
        with studio.connect() as db:
            db.execute("CREATE TABLE IF NOT EXISTS chat_sessions(id TEXT PRIMARY KEY, body TEXT NOT NULL)")

    def sessions(self):
        with self.studio.connect() as db:
            return [json.loads(r[0]) for r in db.execute("SELECT body FROM chat_sessions ORDER BY rowid")]

    def get(self, id):
        row = next((r for r in self.sessions() if r["id"] == id), None)
        if not row:
            raise ValueError("Chat session not found")
        return row

    def put(self, row):
        with self.studio.connect() as db:
            db.execute("INSERT OR REPLACE INTO chat_sessions VALUES (?,?)", (row["id"], encode(row)))
        folder = self.studio.root / "sessions" / row["id"]
        folder.mkdir(parents=True, exist_ok=True)
        (folder / "session.json").write_text(encode(row), encoding="utf-8")
        (folder / "progress.md").write_text("# Tiến độ lựa chọn\n\n" + f"Bước: {row['step']}\n\nTrạng thái: {row['status']}\n\n" + "\n\n".join(f"## {k}\n\n{v['title']}\n\n{v['summary']}" for k,v in row["choices"].items()), encoding="utf-8")
        return row

    def start(self, seed=""):
        return self.put({"id":uid(), "seed":seed, "step":"concept", "status":"awaiting_proposals", "options":[], "choices":{}, "history":[], "created":now()})

    def offer(self, id, options):
        with self.studio.lock:
            row = self.get(id)
            if row["status"] not in ("awaiting_proposals", "awaiting_choice"):
                raise ValueError("This session is already complete")
            if not isinstance(options, list) or len(options) != 3:
                raise ValueError("Exactly three alternatives are required")
            for option in options:
                if not isinstance(option, dict) or any(not isinstance(option.get(k), str) or not option[k].strip() for k in ("title", "summary", "tradeoff")):
                    raise ValueError("Each proposal needs title, summary and tradeoff")
                if row["step"] == "concept" and (not isinstance(option.get("genres"), list) or not option["genres"] or any(g not in GENRES for g in option["genres"])):
                    raise ValueError("Concept needs valid genres")
                if row["step"] == "story" and option.get("length") not in ("short", "novella", "novel", "series"):
                    raise ValueError("Story direction needs a length")
                if row["step"] == "art" and option.get("direction") not in ("rtl", "ltr", "vertical"):
                    raise ValueError("Art direction needs reading direction")
            if len({o["summary"].strip() for o in options}) != 3:
                raise ValueError("Alternatives must differ")
            row.update(status="awaiting_choice", options=options, proposal_revision=uid())
            return self.put(row)

    def choose(self, id, index, revision):
        with self.studio.lock:
            row = self.get(id)
            if row["status"] != "awaiting_choice" or revision != row.get("proposal_revision") or type(index) is not int or not 0 <= index < 3:
                raise ValueError("Choice refers to outdated/missing proposals")
            row["choices"][row["step"]] = row["options"][index]
            row["history"].append({"step":row["step"], "revision":revision, "options":row["options"], "selected":index})
            if row["step"] == "art":
                c,s,a = (row["choices"][k] for k in KINDS)
                project = self.studio.create({"title":c["title"], "idea":c["summary"]+"\nHướng truyện: "+s["summary"], "genres":c["genres"], "length":s["length"], "direction":a["direction"], "style":a["summary"], "creative_choices":row["choices"], "mode":"chat"})
                row.update(status="completed", project=project["id"])
                self.checkpoint(project["id"])
            else:
                row.update(step=KINDS[KINDS.index(row["step"])+1], status="awaiting_proposals", options=[])
            return self.put(row)

    def packet(self, project, chapter, stage):
        prompt, parents = self.studio.prompt(project, chapter, stage)
        packet = {"project":project, "chapter":chapter, "stage":stage, "parents":parents, "prompt":prompt}
        folder = self.studio.root / "projects" / project / "tasks"
        folder.mkdir(exist_ok=True)
        file = folder / (uid()+".json")
        file.write_text(encode(packet), encoding="utf-8")
        return {"file":str(file), **packet}

    def submit(self, packet, output):
        project, chapter, stage = packet["project"], packet["chapter"], packet["stage"]
        with self.studio.lock:
            _, parents = self.studio.prompt(project, chapter, stage)
            if packet["parents"] != parents:
                raise ValueError("Source changed; prepare a fresh packet")
            if not isinstance(output, str) or not output.strip():
                raise ValueError("Empty artifact")
            if stage == "continuity":
                report = json.loads(output)
                if type(report.get("pass")) is not bool or not isinstance(report.get("issues"),list) or not isinstance(report.get("canon_delta"),dict):
                    raise ValueError("Invalid continuity contract")
                if report["pass"] and report["issues"]:
                    raise ValueError("Continuity cannot pass with unresolved issues")
            artifact = self.studio.save(project, chapter, stage, output, parents)
            self.checkpoint(project, chapter)
            return artifact

    def resume(self, project, chapter=1):
        info = self.studio.project(project)
        current = {stage:self.studio.latest(project,chapter,stage) for stage in STAGES}
        audit = current["continuity"]
        failed = audit and not json.loads(audit["body"])["pass"]
        missing = next((s for s in STAGES if current[s] is None), None)
        approved = self.studio.latest(project,chapter,"edit",approved=True)
        if failed:
            next_step = "revise_prose"
        elif current["edit"] and audit and not approved:
            next_step = "approve_prose_after_audit"
        else:
            next_step = missing or "generate_and_review_manga"
        if not failed and missing in ("adaptation","storyboard","lettering","image_prompt") and not approved:
            next_step = "approve_prose_after_audit" if audit else "continuity"
        pages = [r for r in self.studio.artifacts(project) if r["chapter"] == chapter and r["kind"] == "page"]
        latest_pages = {}
        for row in pages:
            latest_pages[json.loads(row["body"])["number"]] = row
        return {"project":info, "chapter":chapter, "next":next_step, "artifacts":current, "pages":list(latest_pages.values()), "folder":str(self.studio.root/"projects"/project)}

    def checkpoint(self, project, chapter=1):
        state = self.resume(project,chapter)
        folder = Path(state["folder"])
        (folder/"progress.json").write_text(encode(state),encoding="utf-8")
        lines = ["# Tiến độ xưởng truyện", "", state["project"]["title"], "", f"Chương đang làm: {chapter}", "", f"Tiếp theo: {state['next']}", "", "## Tài liệu hiện hành", ""]
        lines += [f"- {kind}: {row['id']}" for kind,row in state["artifacts"].items() if row]
        lines += ["", "## Trang manga", ""]
        lines += [f"- Trang {json.loads(p['body'])['number']}: {'cần cập nhật' if p['stale'] else 'đã duyệt' if p['approved'] else 'chờ kiểm tra'}" for p in state["pages"]]
        (folder/"progress.md").write_text("\n".join(lines)+"\n",encoding="utf-8")
        return state

    def image_packet(self, project, chapter, number):
        source = self.studio.latest(project,chapter,"edit",approved=True)
        brief = self.studio.latest(project,chapter,"image_prompt")
        if not source or not brief or number < 1:
            raise ValueError("Prepare approved prose and a current image brief first")
        pages = [r for r in self.studio.artifacts(project) if r["chapter"] == chapter and r["kind"] == "page" and json.loads(r["body"])["number"] == number]
        packet = {"project":project,"chapter":chapter,"number":number,"source":source["id"],"brief":brief["id"],"brief_text":brief["body"],"page_revision":pages[-1]["id"] if pages else None}
        folder = self.studio.root/"projects"/project/"tasks"
        folder.mkdir(exist_ok=True)
        file = folder/(uid()+"-image.json")
        file.write_text(encode(packet),encoding="utf-8")
        return {"file":str(file),**packet}

    def import_image(self, packet, raw):
        with self.studio.lock:
            project,chapter,number = packet["project"],packet["chapter"],packet["number"]
            current = self.image_packet(project,chapter,number)
            if (packet["source"],packet["brief"],packet.get("page_revision")) != (current["source"],current["brief"],current["page_revision"]):
                raise ValueError("Source/brief/page changed during image generation; regenerate from current packet")
            artifact = self.studio.import_page(project,chapter,number,raw)
            self.checkpoint(project,chapter)
            return artifact

    def review_page(self, project, artifact, report):
        with self.studio.lock:
            page = next((p for p in self.resume(project)["pages"] if p["id"] == artifact),None)
            if not page:
                # Allow chapters beyond one, retaining latest-page checks.
                row = next((r for r in self.studio.artifacts(project) if r["id"] == artifact and r["kind"] == "page"),None)
                if row:
                    page = next((p for p in self.resume(project,row["chapter"])["pages"] if p["id"] == artifact),None)
            if not page or page["stale"]:
                raise ValueError("Review must target the current page revision")
            file = self.studio.root/"projects"/project/"pages"/(artifact+".png")
            digest = hashlib.sha256(file.read_bytes()).hexdigest()
            if report.get("image_sha256") != digest or report.get("inspected") is not True or type(report.get("pass")) is not bool or not isinstance(report.get("issues"),list) or not isinstance(report.get("notes"),str) or not report["notes"].strip():
                raise ValueError("Review needs actual-image inspection, matching hash, observations and issues")
            expected, observed = report.get("expected_dialogue"), report.get("observed_dialogue")
            if not isinstance(expected,list) or not isinstance(observed,list) or any(not isinstance(t,str) for t in expected+observed):
                raise ValueError("Review needs expected and observed dialogue")
            matches = [" ".join(t.split()) for t in expected] == [" ".join(t.split()) for t in observed]
            if report["pass"] and (report["issues"] or not matches):
                raise ValueError("A page with defects or dialogue differences cannot pass")
            folder = self.studio.root/"projects"/project/"reviews"
            folder.mkdir(exist_ok=True)
            (folder/(artifact+"-"+uid()+".json")).write_text(encode(report),encoding="utf-8")
            if report["pass"]:
                self.studio.approve_page(project,artifact,"Active-chat visual inspection: "+encode(report))
            self.checkpoint(project,page["chapter"])
            return {"approved":report["pass"], "artifact":artifact}
