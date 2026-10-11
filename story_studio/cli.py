"""File commands for the active chat; no UI, network or model subprocess."""
import argparse
import json
import sys
from pathlib import Path
from .core import DEFAULT_DATA, STAGES, Studio, encode
from .chat import ChatWorkflow

def load(file):
    return json.loads(Path(file).read_text(encoding="utf-8-sig"))

def main():
    if hasattr(sys.stdout,"reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    p=argparse.ArgumentParser(description="Creator chat-first story workshop")
    p.add_argument("--data",default=str(DEFAULT_DATA))
    sub=p.add_subparsers(dest="command")
    sub.add_parser("status")
    create=sub.add_parser("create");create.add_argument("file")
    start=sub.add_parser("start");start.add_argument("--seed",default="")
    offer=sub.add_parser("offer");offer.add_argument("session");offer.add_argument("file")
    choose=sub.add_parser("choose");choose.add_argument("session");choose.add_argument("index",type=int);choose.add_argument("revision")
    for name in ("resume","checkpoint"):
        c=sub.add_parser(name);c.add_argument("project");c.add_argument("--chapter",type=int,default=1)
    for name in ("prompt","submit"):
        c=sub.add_parser(name);c.add_argument("project");c.add_argument("chapter",type=int);c.add_argument("stage",choices=STAGES);c.add_argument("file")
        if name=="submit":c.add_argument("output")
    for name in ("approve","export"):
        c=sub.add_parser(name);c.add_argument("project")
        if name=="approve":c.add_argument("artifact")
    image=sub.add_parser("image-task");image.add_argument("project");image.add_argument("chapter",type=int);image.add_argument("number",type=int);image.add_argument("file")
    page=sub.add_parser("page");page.add_argument("project");page.add_argument("chapter",type=int);page.add_argument("number",type=int);page.add_argument("png");page.add_argument("--packet",required=True)
    review=sub.add_parser("review-page");review.add_argument("project");review.add_argument("artifact");review.add_argument("file")
    cbz=sub.add_parser("cbz");cbz.add_argument("project");cbz.add_argument("chapter",type=int)
    args=p.parse_args();studio=Studio(args.data);chat=ChatWorkflow(studio)
    if args.command in (None,"status"):
        result={"projects":studio.projects(),"sessions":chat.sessions(),"data":str(studio.root)}
    elif args.command=="create":
        result=studio.create(load(args.file));chat.checkpoint(result["id"])
    elif args.command=="start":result=chat.start(args.seed)
    elif args.command=="offer":result=chat.offer(args.session,load(args.file))
    elif args.command=="choose":result=chat.choose(args.session,args.index,args.revision)
    elif args.command in ("resume","checkpoint"):
        result=getattr(chat,args.command)(args.project,args.chapter)
    elif args.command=="prompt":
        result=chat.packet(args.project,args.chapter,args.stage)
        Path(args.file).write_text(encode(result),encoding="utf-8")
    elif args.command=="submit":
        packet=load(args.file)
        if (packet["project"],packet["chapter"],packet["stage"])!=(args.project,args.chapter,args.stage):raise ValueError("Packet identity mismatch")
        result=chat.submit(packet,Path(args.output).read_text(encoding="utf-8-sig"))
    elif args.command=="approve":
        result=studio.approve(args.project,args.artifact)
        row=next(r for r in studio.artifacts(args.project) if r["id"]==args.artifact)
        chat.checkpoint(args.project,row["chapter"])
    elif args.command=="image-task":
        result=chat.image_packet(args.project,args.chapter,args.number)
        Path(args.file).write_text(encode(result),encoding="utf-8")
    elif args.command=="page":
        packet=load(args.packet)
        if (packet["project"],packet["chapter"],packet["number"])!=(args.project,args.chapter,args.number):raise ValueError("Image packet identity mismatch")
        result=chat.import_image(packet,Path(args.png).read_bytes())
    elif args.command=="review-page":result=chat.review_page(args.project,args.artifact,load(args.file))
    elif args.command=="cbz":result=str(studio.export_cbz(args.project,args.chapter))
    else:result=str(studio.export(args.project))
    print(encode(result))

if __name__=="__main__":main()
