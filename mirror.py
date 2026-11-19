"""Mirror coldcoupons.com listing pages (1..21) into a local static clone.
Page 1 -> index.html, page N -> page-N.html. Same-origin assets are
downloaded into assets_mirror/ and references rewritten to local paths."""
import re, sys, time, urllib.request, urllib.parse, pathlib

BASE = "https://coldcoupons.com/"
HOST = "coldcoupons.com"
OUT = pathlib.Path(__file__).parent
UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36"
FIRST, LAST = 1, 21
done = {}

def fetch(url, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=30) as r:
                return r.read()
        except Exception:
            if i == tries - 1:
                raise
            time.sleep(2)

def local_path(url):
    p = urllib.parse.urlparse(url)
    return "assets_mirror/" + (p.path.lstrip("/") or "index.html")

def grab(url):
    url = url.split("#")[0]
    if "${" in url or "{{" in url or urllib.parse.urlparse(url).netloc != HOST:
        return url
    if url in done:
        return done[url]
    rel = local_path(url)
    done[url] = rel
    dest = OUT / rel
    if dest.exists():
        return rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    try:
        data = fetch(url)
    except Exception as e:
        print("FAIL", url, e)
        return url
    if rel.endswith(".css"):
        data = rewrite_css(data.decode("utf-8", "replace"), url, rel).encode("utf-8")
    dest.write_bytes(data)
    print("  asset", rel)
    return rel

def rewrite_css(css, css_url, css_rel):
    prefix = "../" * css_rel.count("/")
    def rep(m):
        raw = m.group(2).strip()
        if raw.startswith("data:"):
            return m.group(0)
        loc = grab(urllib.parse.urljoin(css_url, raw))
        return f"url({loc if loc.startswith('http') else prefix + loc})"
    return re.sub(r"url\((['\"]?)([^'\")]+)\1\)", rep, css)

def page_file(n):
    return "index.html" if int(n) == 1 else f"page-{int(n)}.html"

def process(n):
    url = BASE if n == 1 else f"{BASE}?page={n}"
    html = fetch(url).decode("utf-8", "replace")

    def rep_attr(m):
        attr, q, val = m.group(1), m.group(2), m.group(3)
        if "${" in val or "{{" in val or val.startswith(("#", "javascript:", "mailto:", "tel:")):
            return m.group(0)
        absu = urllib.parse.urljoin(url, val)
        if urllib.parse.urlparse(absu).netloc != HOST:
            return m.group(0)
        if attr == "href":
            ctx = html[max(0, m.start() - 300):m.start()]
            if not ctx[ctx.rfind("<"):].lower().startswith("<link"):
                pm = re.fullmatch(r"https://coldcoupons\.com/?(\?page=(\d+))?", absu)
                if pm:  # home / pagination -> local pages
                    pg = pm.group(2) or 1
                    if FIRST <= int(pg) <= LAST:
                        return f"{attr}={q}{page_file(pg)}{q}"
                return f"{attr}={q}{absu}{q}"  # other pages -> live site
        return f"{attr}={q}{grab(absu)}{q}"
    html = re.sub(r'\b(src|href|data-src|data-bg|poster)=(["\'])([^"\']+)\2', rep_attr, html)

    def rep_srcset(m):
        parts = []
        for item in m.group(2).split(","):
            bits = item.strip().split()
            if bits:
                bits[0] = grab(urllib.parse.urljoin(url, bits[0]))
                parts.append(" ".join(bits))
        return f'srcset={m.group(1)}{", ".join(parts)}{m.group(1)}'
    html = re.sub(r'srcset=(["\'])([^"\']+)\1', rep_srcset, html)

    def rep_style_url(m):
        raw = m.group(2)
        if raw.startswith("data:") or "${" in raw:
            return m.group(0)
        return f"url({m.group(1)}{grab(urllib.parse.urljoin(url, raw))}{m.group(1)})"
    html = re.sub(r"url\((&quot;|['\"]?)([^'\")&]+)\1\)", rep_style_url, html)

    html = re.sub(r'<script[^>]*googletagmanager[^>]*></script>', '', html)
    html = re.sub(r'<script>\s*window\.dataLayer[\s\S]*?</script>', '', html)
    html = re.sub(r'<script[^>]*cloudflareinsights[^>]*></script>', '', html)

    (OUT / page_file(n)).write_text(html, encoding="utf-8")
    cards = html.count("Get Code")
    print(f"PAGE {n} -> {page_file(n)} ({cards} 'Get Code' buttons)")

import json

def mirror_coupon_api():
    """Save each coupon's popup data locally and point the popup at it."""
    ids = set()
    pages = [OUT / page_file(n) for n in range(FIRST, LAST + 1)]
    for p in pages:
        if p.exists():
            ids |= set(re.findall(r'data-coupon-id="(\d+)"', p.read_text(encoding="utf-8")))
    api_dir = OUT / "assets_mirror" / "api" / "coupons"
    api_dir.mkdir(parents=True, exist_ok=True)
    ok = 0
    for cid in sorted(ids, key=int):
        try:
            data = json.loads(fetch(f"{BASE}api/coupons/{cid}"))
        except Exception as e:
            print("API FAIL", cid, e)
            continue
        for key in ("coupon_banner", "brand_logo"):
            if data.get(key):
                grab(f"{BASE}public/{data[key]}")  # popup image -> assets_mirror/public/...
        (api_dir / f"{cid}.json").write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        ok += 1
    print(f"API: saved {ok}/{len(ids)} coupons")
    for p in pages:
        if not p.exists():
            continue
        h = p.read_text(encoding="utf-8")
        h = h.replace("baseUrl: 'https://coldcoupons.com'", "baseUrl: 'assets_mirror'")
        h = h.replace("`${this.baseUrl}/api/coupons/${couponId}`", "`${this.baseUrl}/api/coupons/${couponId}.json`")
        p.write_text(h, encoding="utf-8")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "api":
        mirror_coupon_api()
        sys.exit()
    a = int(sys.argv[1]) if len(sys.argv) > 1 else FIRST
    b = int(sys.argv[2]) if len(sys.argv) > 2 else LAST
    for n in range(a, b + 1):
        try:
            process(n)
        except Exception as e:
            print("PAGE FAIL", n, e)
    mirror_coupon_api()
    print("Done.", len(done), "assets referenced")
