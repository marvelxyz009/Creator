"""Build a chapter bible: carried-forward series bible + chapter status. Usage: py mkbible.py NN status.md"""
import pathlib, sys
root = pathlib.Path(__file__).resolve().parent.parent
base = (root / "series-bible.md").read_text(encoding="utf-8").replace("\r\n", "\n")
base = base[: base.index("## Trạng thái")].replace("> Nền truyện v1 •", "> Nền truyện v1.2 (mang sang chương %s) •" % sys.argv[1])
status = pathlib.Path(sys.argv[2]).read_text(encoding="utf-8").replace("\r\n", "\n")
rule = ("\n## Quy ước gọi tên\n\nĐàn khỉ không có tên riêng; không dùng tên kiểu thuần Việt. Văn gọi theo đặc điểm: khỉ già (lông xám), "
        "con tai sứt, khỉ con (lông nâu nhạt), khỉ mẹ (lông nâu đỏ); thoại dùng bà, con ơi, thằng tai sứt kia… "
        "Nhân vật nguyên tác giữ tên Hán Việt. Yêu thú địa phương cũng không có tên riêng.\n")
out = pathlib.Path(sys.argv[2]).with_name("bible.md")
out.write_bytes((base + status.rstrip("\n") + "\n" + rule).encode("utf-8"))
print(out)
