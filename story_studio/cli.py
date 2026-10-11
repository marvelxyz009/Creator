"""Agent bridge: durable prompt packets and revision-safe submission."""
import argparse
import json
from pathlib import Path
from .core import PACKAGE_ROOT, DEFAULT_DATA, STAGES, Studio, encode

def main():
    p = argparse.ArgumentParser(description="Creator agent bridge")
    p.add_argument("--data", default=str(DEFAULT_DATA))
    sub = p.add_subparsers(dest="command", required=True)
    sub.add_parser("status")
    new = sub.add_parser("create")
    new.add_argument("file", help="Project JSON")
    for name in ("prompt", "submit"):
        cmd = sub.add_parser(name)
        cmd.add_argument("project")
        cmd.add_argument("chapter", type=int)
        cmd.add_argument("stage", choices=STAGES)
        cmd.add_argument("file", help="Prompt packet JSON path")
        if name == "submit":
            cmd.add_argument("output", help="Model output UTF-8 file")
    for name in ("approve", "export"):
        cmd = sub.add_parser(name)
        cmd.add_argument("project")
        if name == "approve":
            cmd.add_argument("artifact")
    page = sub.add_parser("page")
    page.add_argument("project")
    page.add_argument("chapter", type=int)
    page.add_argument("number", type=int)
    page.add_argument("png")
    review = sub.add_parser("approve-page")
    review.add_argument("project")
    review.add_argument("artifact")
    review.add_argument("--notes", required=True)
    cbz = sub.add_parser("cbz")
    cbz.add_argument("project")
    cbz.add_argument("chapter", type=int)
    args = p.parse_args()
    studio = Studio(args.data)
    if args.command == "status":
        result = {"projects": studio.projects(), "jobs": studio.jobs()}
    elif args.command == "create":
        result = studio.create(json.loads(Path(args.file).read_text(encoding="utf-8")))
    elif args.command == "prompt":
        prompt, parents = studio.prompt(args.project, args.chapter, args.stage)
        result = {"project": args.project, "chapter": args.chapter, "stage": args.stage, "parents": parents, "prompt": prompt}
        Path(args.file).write_text(encode(result), encoding="utf-8")
    elif args.command == "submit":
        packet = json.loads(Path(args.file).read_text(encoding="utf-8"))
        _, parents = studio.prompt(args.project, args.chapter, args.stage)
        if (packet["project"], packet["chapter"], packet["stage"], packet["parents"]) != (args.project, args.chapter, args.stage, parents):
            raise ValueError("Prompt source changed: prepare a new packet")
        output = Path(args.output).read_text(encoding="utf-8")
        if args.stage == "continuity":
            report = json.loads(output)
            if type(report.get("pass")) is not bool or not isinstance(report.get("issues"), list) or not isinstance(report.get("canon_delta"), dict):
                raise ValueError("Invalid continuity contract")
        result = studio.save(args.project, args.chapter, args.stage, output, parents)
    elif args.command == "approve":
        result = studio.approve(args.project, args.artifact)
    elif args.command == "page":
        result = studio.import_page(args.project, args.chapter, args.number, Path(args.png).read_bytes())
    elif args.command == "approve-page":
        result = studio.approve_page(args.project, args.artifact, args.notes)
    elif args.command == "cbz":
        result = str(studio.export_cbz(args.project, args.chapter))
    else:
        result = str(studio.export(args.project))
    print(encode(result))

if __name__ == "__main__":
    main()
