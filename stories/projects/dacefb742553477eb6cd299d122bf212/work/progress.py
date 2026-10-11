"""Update writing-progress.md after a chapter is approved.
Usage: py progress.py N "Title" EDIT_ID CONT_ID "log line" status.txt "Next chapter title"
"""
import pathlib, re, sys
n, title, edit, cont, log, status_file, nxt = sys.argv[1:8]
n = int(n)
p = pathlib.Path(__file__).resolve().parent.parent / "writing-progress.md"
s = p.read_text(encoding="utf-8").replace("\r\n", "\n")
line = f"- Chương {n} — {title}: chapter-{n:02}.md, edit {edit}, continuity {cont} (pass, audit của trợ lý), đã chốt.\n"
s = re.sub(r"- book\.zip đã export lại gồm chương 1–\d+\.", line + f"- book.zip đã export lại gồm chương 1–{n}.", s)
s = s.replace("## Nhật ký\n\n", f"## Nhật ký\n\n- 2026-10-11: {log}\n")
status = pathlib.Path(status_file).read_text(encoding="utf-8").strip()
s = re.sub(r"## Trạng thái cuối chương \d+\n\n.*?\n\n(?=## Bước tiếp)", f"## Trạng thái cuối chương {n}\n\n{status}\n\n", s, flags=re.S)
s = re.sub(r"Chương \d+ — [^.]+\. Đọc resume", f"Chương {n + 1} — {nxt}. Đọc resume", s)
p.write_bytes(s.encode("utf-8"))
print(p)
