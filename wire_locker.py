import glob, json, pathlib, urllib.parse

OUT = pathlib.Path(__file__).parent
coupons = {}

for f in glob.glob(str(OUT / "assets_mirror/api/coupons/*.json")):
    p = pathlib.Path(f)
    d = json.loads(p.read_text(encoding="utf-8"))
    cid = str(d["id"])
    title = d.get("coupon_title") or ""
    code = (d.get("coupon_code") or "CODE").strip()
    tail = code[-4:] if len(code) >= 4 else code
    d["coupon_locker_url"] = (
        "adbluemedia-locker.html?"
        + urllib.parse.urlencode({"title": title, "tail": tail, "id": cid})
    )
    p.write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
    coupons[cid] = d

(OUT / "assets_mirror/coupons_data.js").write_text(
    "window.LOCAL_COUPONS = " + json.dumps(coupons, ensure_ascii=False) + ";\n",
    encoding="utf-8",
)

old_oglock = '''function OGLock() {
  window.open("https://unlockedrobot.com/cl/i/2lj456");
}'''

new_oglock = '''function OGLock() {
  const c = window.Alpine && window.Alpine.store('couponModal') && window.Alpine.store('couponModal').coupon;
  if (c && c.coupon_locker_url) {
    window.open(c.coupon_locker_url, '_blank');
  } else {
    window.open('adbluemedia-locker.html', '_blank');
  }
}'''

updated = 0
for f in glob.glob(str(OUT / "*.html")):
    p = pathlib.Path(f)
    if p.name == "adbluemedia-locker.html":
        continue
    h = p.read_text(encoding="utf-8")
    h2 = h.replace(
        ':href="https://coldcoupons.com/safeDecodeUrl($store.couponModal.coupon?.coupon_locker_url)"',
        ':href="safeDecodeUrl($store.couponModal.coupon?.coupon_locker_url)"',
    )
    h2 = h2.replace(old_oglock, new_oglock)
    h2 = h2.replace("coupons_data.js?v=local3", "coupons_data.js?v=local4")
    if h2 != h:
        p.write_text(h2, encoding="utf-8")
        updated += 1

print(f"Updated {len(coupons)} coupons and {updated} HTML pages.")
