import sys, pathlib, re
PAIRS = [("Bà Khỉ Xám","Khỉ già lông xám"),("bà Khỉ Xám","khỉ già lông xám"),("Khỉ Xám","khỉ già lông xám"),("Bà Xám","Khỉ già lông xám"),("bà Xám","khỉ già lông xám"),
         ("Khỉ Tai Sứt","Khỉ tai sứt"),("Tai Sứt","khỉ tai sứt"),("Hầu nhỏ Mầm","Khỉ con lông nâu nhạt"),("Mẹ Mầm","Khỉ mẹ lông nâu đỏ"),("mẹ Mầm","khỉ mẹ lông nâu đỏ"),("mẹ con Mầm","mẹ con khỉ con"),("Mầm và mẹ","Khỉ con và khỉ mẹ"),("Mầm","khỉ con lông nâu nhạt"),
         ("Xám/Tai Sứt/mẹ Mầm","khỉ già/khỉ tai sứt/khỉ mẹ"),("Xám,","khỉ già,"),("Xám ","khỉ già ")]
def conv(s):
    for a,b in PAIRS: s = s.replace(a,b)
    # capitalise at line/sentence starts
    s = re.sub(r"(^|[.!?]\s+|^#+\s+|^-\s+|\|\s*)(khỉ)", lambda m: m.group(1)+"Khỉ", s, flags=re.M)
    return s
if __name__ == "__main__":
    for a in sys.argv[1:]:
        src, dst = a.split("=") if "=" in a else (a, a)
        t = pathlib.Path(src).read_text(encoding="utf-8").replace("\r\n","\n")
        pathlib.Path(dst).write_bytes(conv(t).encode("utf-8"))
        print(dst, len(re.findall("Xám|Tai Sứt|Mầm", conv(t))))
