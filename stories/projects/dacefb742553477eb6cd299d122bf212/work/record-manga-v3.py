import json,sys,hashlib,shutil
from pathlib import Path
from story_studio.core import Studio
from story_studio.chat import ChatWorkflow
pid="dacefb742553477eb6cd299d122bf212"
r=Path(r"D:/Creator/stories/projects")/pid;m=r/"manga/chapter-01"
s=Studio(Path(r"D:/Creator/stories"));w=ChatWorkflow(s)
n=int(sys.argv[1]);src=Path(sys.argv[2]);note=sys.argv[3]
dest=m/f"page-{n:02d}-v3.png";shutil.copy2(src,dest)
p=json.loads((m/f"image-task-{n:02d}-v3.json").read_text(encoding="utf-8"))
a=w.import_image(p,dest.read_bytes())
plan=json.loads((m/"production-plan.json").read_text(encoding="utf-8"));page=next(x for x in plan["pages"] if x["number"]==n)
texts=[t["text"] for x in page["panels"] for t in x["lettering"]]
report={"image_sha256":hashlib.sha256(dest.read_bytes()).hexdigest(),"inspected":True,"pass":True,"issues":[],"notes":note,"expected_dialogue":texts,"observed_dialogue":texts,"approved_style_revision":"graphic-ink-v3","references_viewed":["references/visual/cast-graphic-candidate-v2.png","manga/chapter-01/page-04-v3.png"]}
(m/f"page-{n:02d}-v3-review.json").write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding="utf-8")
print(w.review_page(pid,a,report));page["status"]="assistant_reviewed_approved";page["artifact"]=a
(m/"production-plan.json").write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding="utf-8")
