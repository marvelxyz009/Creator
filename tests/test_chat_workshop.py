import hashlib
import json
import struct
import subprocess
import sys
import tempfile
import unittest
import zlib
from pathlib import Path
from story_studio.core import Studio, STAGES
from story_studio.chat import ChatWorkflow
from story_studio.png import validate_png

# One-pixel fixtures exercise storage; they are never presented as manga artwork.
def pixel(value=1):
    def chunk(kind,data):return struct.pack(">I",len(data))+kind+data+struct.pack(">I",zlib.crc32(kind+data)&0xffffffff)
    return b"\x89PNG\r\n\x1a\n"+chunk(b"IHDR",struct.pack(">IIBBBBB",1,1,8,2,0,0,0))+chunk(b"IDAT",zlib.compress(bytes([0,value,0,0])))+chunk(b"IEND",b"")

class ChatWorkshopTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.s=Studio(self.tmp.name);self.chat=ChatWorkflow(self.s)
        self.p=self.s.create({"title":"Fixture","idea":"A family mystery","genres":["Trinh thám"]})["id"]
    def tearDown(self):self.tmp.cleanup()
    def write(self,chapter=1,end="image_prompt",passed=True):
        for stage in STAGES:
            packet=self.chat.packet(self.p,chapter,stage)
            body=json.dumps({"pass":passed,"issues":[] if passed else ["Contradiction"],"canon_delta":{"events":["Fixture event"]}}) if stage=="continuity" else "Test fixture output for "+stage
            self.chat.submit(packet,body)
            if stage=="continuity" and passed:self.s.approve(self.p,self.s.latest(self.p,chapter,"edit")["id"])
            if stage==end:break
    def image(self,n=1):return self.chat.import_image(self.chat.image_packet(self.p,1,n),pixel(n))
    def review(self,id,passed=True):
        file=self.s.root/"projects"/self.p/"pages"/(id+".png")
        return {"image_sha256":hashlib.sha256(file.read_bytes()).hexdigest(),"inspected":True,"pass":passed,"notes":"Fixture inspection record, not actual generated manga","issues":[] if passed else ["Unreadable text"],"expected_dialogue":["Xin chào."],"observed_dialogue":["Xin chào."]}
    def test_three_choice_rounds_create_local_project(self):
        session=self.chat.start("Mystery")
        for kind in ("concept","story","art"):
            extra={"genres":["Trinh thám"]} if kind=="concept" else {"length":"novel"} if kind=="story" else {"direction":"rtl"}
            options=[{"title":f"Concept {i}","summary":f"Different direction {i}","tradeoff":"A concrete cost",**extra} for i in range(3)]
            row=self.chat.offer(session["id"],options)
            session=self.chat.choose(session["id"],1,row["proposal_revision"])
        project=self.s.project(session["project"])
        self.assertEqual(project["mode"],"chat");self.assertEqual(project["length"],"novel")
        self.assertEqual(len(project["creative_choices"]),3)
        self.assertTrue((self.s.root/"projects"/project["id"]/"progress.md").exists())
        self.assertEqual(ChatWorkflow(Studio(self.tmp.name)).get(session["id"])["status"],"completed")
    def test_obsolete_selection_is_rejected(self):
        row=self.chat.start();options=[{"title":str(i),"summary":str(i),"tradeoff":"Cost","genres":["Hài"]} for i in range(3)]
        old=self.chat.offer(row["id"],options);self.chat.offer(row["id"],options)
        with self.assertRaises(ValueError):self.chat.choose(row["id"],0,old["proposal_revision"])
    def test_exactly_three_distinct_options_required(self):
        row=self.chat.start()
        with self.assertRaises(ValueError):self.chat.offer(row["id"],[])
    def test_resume_checkpoints_and_read_only_helpers(self):
        state=self.chat.checkpoint(self.p);self.assertEqual(state["next"],"bible")
        self.write(end="characters")
        self.assertEqual(self.chat.resume(self.p)["next"],"art")
        self.assertTrue((self.s.root/"projects"/self.p/"progress.json").exists())
        self.assertFalse(hasattr(self.s,"provider"));self.assertFalse(hasattr(self.s,"run_one"))
    def test_specialists_feed_prose(self):
        self.write(end="draft")
        row=self.s.latest(self.p,1,"draft")
        for kind in ("characters","art"):
            self.assertIn(self.s.latest(self.p,1,kind)["id"],row["parents"])
    def test_submission_rejects_changed_source(self):
        self.write(end="bible");packet=self.chat.packet(self.p,1,"outline")
        self.s.save(self.p,1,"bible","Revised bible")
        with self.assertRaises(ValueError):self.chat.submit(packet,"Stale outline")
    def test_audit_gate_and_failed_audit_resume(self):
        self.write(end="continuity",passed=False)
        self.assertEqual(self.chat.resume(self.p)["next"],"revise_prose")
        with self.assertRaises(ValueError):self.s.approve(self.p,self.s.latest(self.p,1,"edit")["id"])
        with self.assertRaises(ValueError):self.chat.packet(self.p,1,"adaptation")
    def test_pass_with_issues_is_rejected(self):
        self.write(end="edit");packet=self.chat.packet(self.p,1,"continuity")
        with self.assertRaises(ValueError):self.chat.submit(packet,'{"pass":true,"issues":["bad"],"canon_delta":{}}')
    def test_next_chapter_needs_previous_source(self):
        with self.assertRaises(ValueError):self.chat.packet(self.p,2,"bible")
        self.write(end="continuity")
        self.assertIn(self.s.latest(self.p,1,"edit")["id"],self.chat.packet(self.p,2,"bible")["parents"])
    def test_revision_invalidates_manga_and_future_chapter(self):
        self.write();page=self.image();self.chat.review_page(self.p,page,self.review(page))
        self.write(chapter=2,end="bible")
        source=self.s.latest(self.p,1,"edit");self.s.save(self.p,1,"edit","Changed story",source["parents"])
        self.assertIsNone(self.s.latest(self.p,1,"adaptation"));self.assertIsNone(self.s.latest(self.p,2,"bible"))
        with self.assertRaises(ValueError):self.s.export_cbz(self.p,1)
    def test_image_generation_pin_rejects_old_source(self):
        self.write();packet=self.chat.image_packet(self.p,1,1)
        self.s.save(self.p,1,"image_prompt","Different page brief",self.s.latest(self.p,1,"image_prompt")["parents"])
        with self.assertRaises(ValueError):self.chat.import_image(packet,pixel())
    def test_repair_packet_rejects_concurrent_page_revision(self):
        self.write();self.image();packet=self.chat.image_packet(self.p,1,1);self.image()
        with self.assertRaises(ValueError):self.chat.import_image(packet,pixel(8))
    def test_review_requires_actual_hash_and_dialogue(self):
        self.write();page=self.image();report=self.review(page);report["image_sha256"]="wrong"
        with self.assertRaises(ValueError):self.chat.review_page(self.p,page,report)
        report=self.review(page);report["observed_dialogue"]=["Wrong"]
        with self.assertRaises(ValueError):self.chat.review_page(self.p,page,report)
        with self.assertRaises(ValueError):self.s.approve(self.p,page)
    def test_failed_review_is_saved_without_approval(self):
        self.write();page=self.image();self.chat.review_page(self.p,page,self.review(page,False))
        self.assertFalse(self.chat.resume(self.p)["pages"][0]["approved"])
        self.assertEqual(len(list((self.s.root/"projects"/self.p/"reviews").glob('*.json'))),1)
    def test_current_page_only_and_other_pages_preserved(self):
        self.write();first=self.image();second=self.image(2)
        self.chat.review_page(self.p,first,self.review(first));self.chat.review_page(self.p,second,self.review(second))
        replacement=self.image()
        with self.assertRaises(ValueError):self.chat.review_page(self.p,first,self.review(first))
        self.chat.review_page(self.p,replacement,self.review(replacement))
        self.assertTrue(self.s.export_cbz(self.p,1).is_file())
    def test_export_checks_reviewed_image_hash(self):
        self.write();page=self.image();self.chat.review_page(self.p,page,self.review(page))
        file=self.s.root/"projects"/self.p/"pages"/(page+".png");file.write_bytes(pixel(9))
        with self.assertRaises(ValueError):self.s.export_cbz(self.p,1)
    def test_valid_png_and_prose_export(self):
        self.write();self.assertEqual(validate_png(pixel()),(1,1));self.assertTrue(self.s.export(self.p).is_file())
        with self.assertRaises(ValueError):validate_png(pixel()[:-3])
    def test_cli_default_is_status_not_server(self):
        result=subprocess.run([sys.executable,"-m","story_studio","--data",self.tmp.name],capture_output=True,text=True,encoding="utf-8",timeout=10)
        self.assertEqual(result.returncode,0,result.stderr);self.assertEqual(json.loads(result.stdout)["data"],str(Path(self.tmp.name).resolve()))
    def test_entry_skill_copies_match(self):
        root=Path(__file__).resolve().parent.parent
        master=(root/'story_studio/skills/creator-studio/SKILL.md').read_text(encoding='utf-8')
        for relative in ('.agents/skills/creator-studio/SKILL.md','.claude/skills/creator-studio/SKILL.md'):
            self.assertEqual(master,(root/relative).read_text(encoding='utf-8'))

if __name__=="__main__":unittest.main()
