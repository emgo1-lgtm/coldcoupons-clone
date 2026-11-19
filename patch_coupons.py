import glob, pathlib, re

OUT = pathlib.Path(__file__).parent
pat = re.compile(
    r"const url = `\$\{this\.baseUrl\}/api/coupons/\$\{couponId\}\.json`;\s*"
    r"const response = await fetch\(url\);\s*"
    r"if \(!response\.ok\) throw new Error\('Failed to fetch coupon data'\);\s*"
    r"// Set coupon data which will trigger the modal slide in\s*"
    r"this\.coupon = await response\.json\(\);"
)
rep = (
    "if (window.LOCAL_COUPONS && window.LOCAL_COUPONS[String(couponId)]) {\n"
    "                            this.coupon = { ...window.LOCAL_COUPONS[String(couponId)] };\n"
    "                        } else {\n"
    "                            const url = `${this.baseUrl}/api/coupons/${couponId}.json`;\n"
    "                            const response = await fetch(url);\n"
    "                            if (!response.ok) throw new Error('Failed to fetch coupon data');\n"
    "                            this.coupon = await response.json();\n"
    "                        }"
)

n = 0
for f in glob.glob(str(OUT / "*.html")):
    p = pathlib.Path(f)
    h = p.read_text(encoding="utf-8")
    if "window.LOCAL_COUPONS" not in h:
        h2, c = pat.subn(rep, h)
        if c:
            p.write_text(h2, encoding="utf-8")
            n += 1
print("Patched modal fetch in HTML files:", n)
