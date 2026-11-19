import glob, pathlib

OUT = pathlib.Path(__file__).parent
idx = (OUT / "assets_mirror/search_index.json").read_text(encoding="utf-8")
(OUT / "assets_mirror/search_index.js").write_text("window.LOCAL_SEARCH_INDEX = " + idx + ";\n", encoding="utf-8")

old = '<script src="assets_mirror/assets/front/js/main.js"></script>'
new = '<script src="assets_mirror/search_index.js?v=local2"></script>\n    <script src="assets_mirror/assets/front/js/main.js?v=local2"></script>'

n = 0
for f in glob.glob(str(OUT / "*.html")):
    p = pathlib.Path(f)
    h = p.read_text(encoding="utf-8")
    if old in h:
        p.write_text(h.replace(old, new), encoding="utf-8")
        n += 1
print("Updated HTML files:", n)
