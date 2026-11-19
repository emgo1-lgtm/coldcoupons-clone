"""Clone all brand pages reachable from the search bar / site, fetch any
missing coupon popup JSONs, rewrite brand links across all pages, and
build a local search index + patch main.js so the search bar works locally."""
import concurrent.futures
import glob
import json
import pathlib
import re
import time
import urllib.parse
import urllib.request

BASE = "https://coldcoupons.com/"
HOST = "coldcoupons.com"
OUT = pathlib.Path(__file__).parent
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"

def fetch(url, tries=3, headers=None):
    hdrs = {"User-Agent": UA}
    if headers:
        hdrs.update(headers)
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=hdrs)
            with urllib.request.urlopen(req, timeout=25) as r:
                return r.status, r.geturl(), r.read()
        except urllib.error.HTTPError as e:
            if e.code in (404, 410):
                return e.code, url, b""
            if i == tries - 1:
                raise
            time.sleep(1.5)
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(1.5)

def local_path(url):
    p = urllib.parse.urlparse(url)
    return "assets_mirror/" + (p.path.lstrip("/") or "index.html")

def grab(url):
    url = url.split("#")[0]
    if "${" in url or "{{" in url or urllib.parse.urlparse(url).netloc != HOST:
        return url
    rel = local_path(url)
    dest = OUT / rel
    if dest.exists():
        return rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        code, _, data = fetch(url)
        if code != 200 or not data:
            return url
    except Exception as e:
        print("ASSET FAIL", url, e)
        return url
    dest.write_bytes(data)
    return rel

def rewrite_html(html, page_url, valid_brands):
    def rep_attr(m):
        attr, q, val = m.group(1), m.group(2), m.group(3)
        if "${" in val or "{{" in val or val.startswith(("#", "javascript:", "mailto:", "tel:")):
            return m.group(0)
        absu = urllib.parse.urljoin(page_url, val)
        if urllib.parse.urlparse(absu).netloc != HOST:
            return m.group(0)
        if attr == "href":
            ctx = html[max(0, m.start() - 300):m.start()]
            if not ctx[ctx.rfind("<"):].lower().startswith("<link"):
                # Home / listing pagination
                pm = re.fullmatch(r"https://coldcoupons\.com/?(\?page=(\d+))?", absu)
                if pm:
                    pg = int(pm.group(2) or 1)
                    if 1 <= pg <= 21:
                        return f'{attr}={q}{"index.html" if pg == 1 else f"page-{pg}.html"}{q}'
                # Brand link
                bm = re.fullmatch(r"https://coldcoupons\.com/brand/(\d+)(?:\?page=(\d+))?", absu)
                if bm:
                    bid = int(bm.group(1))
                    bpg = int(bm.group(2) or 1)
                    if bid in valid_brands:
                        fn = f"brand-{bid}.html" if bpg == 1 else f"brand-{bid}-page-{bpg}.html"
                        return f"{attr}={q}{fn}{q}"
                return f"{attr}={q}{absu}{q}"
        return f"{attr}={q}{grab(absu)}{q}"

    html = re.sub(r'\b(src|href|data-src|data-bg|poster)=(["\'])([^"\']+)\2', rep_attr, html)

    def rep_srcset(m):
        parts = []
        for item in m.group(2).split(","):
            bits = item.strip().split()
            if bits:
                bits[0] = grab(urllib.parse.urljoin(page_url, bits[0]))
                parts.append(" ".join(bits))
        return f'srcset={m.group(1)}{", ".join(parts)}{m.group(1)}'
    html = re.sub(r'srcset=(["\'])([^"\']+)\1', rep_srcset, html)

    def rep_style_url(m):
        raw = m.group(2)
        if raw.startswith("data:") or "${" in raw:
            return m.group(0)
        return f"url({m.group(1)}{grab(urllib.parse.urljoin(page_url, raw))}{m.group(1)})"
    html = re.sub(r"url\((&quot;|['\"]?)([^'\")&]+)\1\)", rep_style_url, html)

    html = re.sub(r'<script[^>]*googletagmanager[^>]*></script>', '', html)
    html = re.sub(r'<script>\s*window\.dataLayer[\s\S]*?</script>', '', html)
    html = re.sub(r'<script[^>]*cloudflareinsights[^>]*></script>', '', html)

    # Localize coupon popup API
    html = html.replace("baseUrl: 'https://coldcoupons.com'", "baseUrl: 'assets_mirror'")
    html = html.replace("`${this.baseUrl}/api/coupons/${couponId}`", "`${this.baseUrl}/api/coupons/${couponId}.json`")
    return html

def main():
    # 1. Collect candidate brand IDs from existing coupons + HTML + scan 1..150
    known_brands = set()
    for f in glob.glob(str(OUT / "assets_mirror/api/coupons/*.json")):
        d = json.loads(pathlib.Path(f).read_text(encoding="utf-8"))
        if d.get("brand_id"):
            known_brands.add(int(d["brand_id"]))
    for f in glob.glob(str(OUT / "*.html")):
        for bid in re.findall(r"brand/(\d+)", pathlib.Path(f).read_text(encoding="utf-8")):
            known_brands.add(int(bid))

    max_id = max(known_brands) if known_brands else 140
    candidates = sorted(known_brands | set(range(1, max_id + 15)))
    print(f"Checking {len(candidates)} candidate brand IDs (known: {len(known_brands)}, max: {max_id})...")

    brand_pages = {}  # bid -> raw html
    def check_brand(bid):
        url = f"{BASE}brand/{bid}"
        try:
            code, final_url, data = fetch(url)
            if code == 200 and data:
                txt = data.decode("utf-8", "replace")
                # Make sure it didn't redirect to home page ("Home | ColdCoupons.com")
                if "<title>Home |" not in txt and f"/brand/{bid}" in final_url:
                    return bid, txt
        except Exception as e:
            print(f"ERR brand {bid}: {e}")
        return bid, None

    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as ex:
        for bid, txt in ex.map(check_brand, candidates):
            if txt:
                brand_pages[bid] = txt

    valid_brands = set(brand_pages.keys())
    print(f"Found {len(valid_brands)} valid brand pages!")

    # Check for brand sub-pages (?page=2, etc.)
    extra_brand_pages = []
    for bid, txt in list(brand_pages.items()):
        pgs = set(map(int, re.findall(rf"/brand/{bid}\?page=(\d+)", txt)))
        for pg in sorted(pgs):
            if pg > 1:
                extra_brand_pages.append((bid, pg))
    if extra_brand_pages:
        print(f"Fetching {len(extra_brand_pages)} paginated brand sub-pages...")
        for bid, pg in extra_brand_pages:
            code, _, data = fetch(f"{BASE}brand/{bid}?page={pg}")
            if code == 200 and data:
                html = rewrite_html(data.decode("utf-8", "replace"), f"{BASE}brand/{bid}?page={pg}", valid_brands)
                (OUT / f"brand-{bid}-page-{pg}.html").write_text(html, encoding="utf-8")

    # 2. Rewrite & save all brand pages + discover any new coupon IDs
    all_coupon_ids = set()
    for f in glob.glob(str(OUT / "assets_mirror/api/coupons/*.json")):
        all_coupon_ids.add(int(pathlib.Path(f).stem))

    new_coupon_ids = set()
    for bid in sorted(valid_brands):
        txt = brand_pages[bid]
        for cid in re.findall(r'data-coupon-id="(\d+)"', txt):
            if int(cid) not in all_coupon_ids:
                new_coupon_ids.add(int(cid))
        html = rewrite_html(txt, f"{BASE}brand/{bid}", valid_brands)
        (OUT / f"brand-{bid}.html").write_text(html, encoding="utf-8")

    print(f"Wrote {len(valid_brands)} brand-*.html pages. New coupons found: {len(new_coupon_ids)}")

    # 3. Fetch any new coupon API JSONs + assets
    api_dir = OUT / "assets_mirror" / "api" / "coupons"
    for cid in sorted(new_coupon_ids):
        try:
            code, _, data = fetch(f"{BASE}api/coupons/{cid}")
            if code == 200 and data:
                d = json.loads(data)
                for key in ("coupon_banner", "brand_logo"):
                    if d.get(key):
                        grab(f"{BASE}public/{d[key]}")
                (api_dir / f"{cid}.json").write_text(json.dumps(d, ensure_ascii=False), encoding="utf-8")
        except Exception as e:
            print("NEW API FAIL", cid, e)

    # 4. Rewrite brand links in index.html and page-2.html..page-21.html
    for n in range(1, 22):
        p = OUT / ("index.html" if n == 1 else f"page-{n}.html")
        if not p.exists():
            continue
        h = p.read_text(encoding="utf-8")
        def rep_brand_link(m):
            bid = int(m.group(1))
            return f'href="brand-{bid}.html"' if bid in valid_brands else m.group(0)
        h = re.sub(r'href="https://coldcoupons\.com/brand/(\d+)"', rep_brand_link, h)
        p.write_text(h, encoding="utf-8")
    print("Updated brand links in index.html and page-2..21.html")

    # 5. Build local search_index.json from all cloned coupons & brands
    coupons_list = []
    brands_map = {}
    for f in sorted(glob.glob(str(api_dir / "*.json")), key=lambda x: int(pathlib.Path(x).stem)):
        d = json.loads(pathlib.Path(f).read_text(encoding="utf-8"))
        coupons_list.append({
            "id": d["id"],
            "brand_id": d.get("brand_id"),
            "brand_name": d.get("brand_name") or "",
            "coupon_title": d.get("coupon_title") or "",
            "coupon_short_incent": d.get("coupon_short_incent") or "",
            "coupon_short_description": d.get("coupon_short_description") or "",
        })
        bid = d.get("brand_id")
        if bid:
            bid = int(bid)
            if bid not in brands_map:
                brands_map[bid] = {
                    "id": bid,
                    "brand_name": d.get("brand_name") or "",
                    "brand_logo": d.get("brand_logo") or "",
                    "coupon_count": 0,
                }
            brands_map[bid]["coupon_count"] += 1

    # Also add any valid brand page that had 0 coupons in API (extract name & logo from its HTML)
    for bid in sorted(valid_brands):
        if bid not in brands_map:
            h = (OUT / f"brand-{bid}.html").read_text(encoding="utf-8")
            tm = re.search(r"<title>(.*?)\s*\|", h)
            name = tm.group(1).strip() if tm else f"Brand {bid}"
            lm = re.search(r'assets_mirror/public/(assets/uploads/brand_logos/[^"\']+)', h)
            logo = lm.group(1) if lm else ""
            brands_map[bid] = {
                "id": bid,
                "brand_name": name,
                "brand_logo": logo,
                "coupon_count": len(re.findall(r'data-coupon-id="(\d+)"', h)) // 2,
            }

    search_index = {
        "brands": sorted(brands_map.values(), key=lambda x: x["brand_name"].lower()),
        "coupons": coupons_list,
    }
    (OUT / "assets_mirror" / "search_index.json").write_text(
        json.dumps(search_index, ensure_ascii=False), encoding="utf-8"
    )
    print(f"Wrote search_index.json ({len(search_index['brands'])} brands, {len(search_index['coupons'])} coupons)")

if __name__ == "__main__":
    main()
