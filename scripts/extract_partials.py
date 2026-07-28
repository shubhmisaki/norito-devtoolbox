#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 1: extract canonical partials (per-locale header/footer/cmdk-overlay,
global head-common/foot-scripts) from representative live files, with all
internal href/src attributes absolutized to root-relative paths so the
partials are depth-independent.
"""
import re, os, glob, json
from urllib.parse import urljoin

ROOT = "/sessions/happy-keen-sagan/mnt/norito"
os.chdir(ROOT)

LOCALES = ["es", "zh", "ar", "hi", "ru", "ja"]  # en = no prefix

def locale_of(path):
    parts = path.split("/")
    if parts[0] in LOCALES:
        return parts[0]
    return "en"

def base_dir_of(path):
    # returns the absolute URL directory the file lives in, e.g. "/es/design/" or "/"
    d = os.path.dirname(path)
    if d == "":
        return "/"
    return "/" + d + "/"

ATTR_RE = re.compile(r'(href|src)="([^"]*)"')

def absolutize(html, base_dir):
    def repl(m):
        attr, val = m.group(1), m.group(2)
        if val.startswith(("http://", "https://", "#", "/", "mailto:", "tel:")) or val == "":
            return m.group(0)
        newval = urljoin(base_dir, val)
        return f'{attr}="{newval}"'
    return ATTR_RE.sub(repl, html)

def extract(s, start_pat, end_pat, flags=re.S):
    m = re.search(start_pat, s, flags)
    if not m:
        return None
    start = m.start()
    m2 = re.search(end_pat, s[start:], flags)
    if not m2:
        return None
    return s[start:start + m2.end()]

def get_header_footer(path, want="header"):
    s = open(path, encoding="utf-8").read()
    base = base_dir_of(path)
    if want == "header":
        block = extract(s, r'<header class="site">', r'</header>')
    else:
        block = extract(s, r'<footer class="site">', r'</footer>')
    if block is None:
        raise RuntimeError(f"could not find {want} in {path}")
    return absolutize(block, base)

partials_dir = os.path.join(ROOT, "partials")
os.makedirs(partials_dir, exist_ok=True)
for loc in LOCALES + ["en"]:
    os.makedirs(os.path.join(partials_dir, loc), exist_ok=True)

# ---- head-common (global, single canonical copy) ----
sample = open("about.html", encoding="utf-8").read()
head_common = extract(sample, r'<script type="text/javascript">\s*\(function\(c,l,a,r,i,t,y\)', r'</noscript>')
open(os.path.join(partials_dir, "head-common.html"), "w", encoding="utf-8").write(head_common)

# ---- per-locale standard header/footer, from a pdf/merge-pdf.html representative ----
CANON_STANDARD = {
    "en": "pdf/merge-pdf.html",
    "es": "es/pdf/merge-pdf.html",
    "zh": "zh/pdf/merge-pdf.html",
    "ar": "ar/pdf/merge-pdf.html",
    "hi": "hi/pdf/merge-pdf.html",
    "ru": "ru/pdf/merge-pdf.html",
    "ja": "ja/pdf/merge-pdf.html",
}
CANON_CONTENT = {
    "en": "compare/norito-vs-ilovepdf.html",
    "es": "es/compare/norito-vs-ilovepdf.html",
    "zh": "zh/compare/norito-vs-ilovepdf.html",
    "ar": "ar/compare/norito-vs-ilovepdf.html",
    "hi": "hi/compare/norito-vs-ilovepdf.html",
    "ru": "ru/compare/norito-vs-ilovepdf.html",
    "ja": "ja/compare/norito-vs-ilovepdf.html",
}

report = []
for loc, path in CANON_STANDARD.items():
    hdr = get_header_footer(path, "header")
    ftr = get_header_footer(path, "footer")
    open(os.path.join(partials_dir, loc, "header.html"), "w", encoding="utf-8").write(hdr)
    open(os.path.join(partials_dir, loc, "footer.html"), "w", encoding="utf-8").write(ftr)
    report.append((loc, "standard", path, len(hdr), len(ftr)))

for loc, path in CANON_CONTENT.items():
    hdr = get_header_footer(path, "header")
    open(os.path.join(partials_dir, loc, "header-content.html"), "w", encoding="utf-8").write(hdr)
    report.append((loc, "content", path, len(hdr), None))

# ---- global foot-scripts-mid (nav/theme-toggle/lang-switcher/bg-blobs) ----
s = open("pdf/merge-pdf.html", encoding="utf-8").read()
base = base_dir_of("pdf/merge-pdf.html")
mid = extract(s, r'<script src="[^"]*nav\.js"></script>', r'<script src="[^"]*bg-blobs\.js"></script>')
mid = absolutize(mid, base)
open(os.path.join(partials_dir, "foot-scripts-mid.html"), "w", encoding="utf-8").write(mid)

# ---- global foot-scripts-head (i18n-runtime.js, utils.js) ----
head_fs = extract(s, r'<script src="[^"]*i18n-runtime\.js"></script>', r'<script src="[^"]*utils\.js"></script>')
head_fs = absolutize(head_fs, base)
open(os.path.join(partials_dir, "foot-scripts-head.html"), "w", encoding="utf-8").write(head_fs)

# ---- global foot-scripts-tail (cmdk.js through </html>) ----
tail = extract(s, r'<script src="[^"]*cmdk\.js"></script>', r'</html>')
tail = absolutize(tail, base)
open(os.path.join(partials_dir, "foot-scripts-tail.html"), "w", encoding="utf-8").write(tail)

# ---- per-locale cmdk-overlay ----
for loc, path in CANON_STANDARD.items():
    s = open(path, encoding="utf-8").read()
    base = base_dir_of(path)
    overlay = extract(s, r'<div class="cmdk-overlay" id="cmdkOverlay"',
                       r'<div class="cmdk-results" id="cmdkResults"></div>\s*</div>\s*</div>')
    if overlay is None:
        report.append((loc, "cmdk-overlay-MISSING", path, None, None))
        continue
    overlay = "<div class=\"cmdk-overlay\" id=\"cmdkOverlay\"" + overlay
    overlay = absolutize(overlay, base)
    open(os.path.join(partials_dir, loc, "cmdk-overlay.html"), "w", encoding="utf-8").write(overlay)
    report.append((loc, "cmdk-overlay", path, len(overlay), None))

for r in report:
    print(r)

print("\nhead_common len:", len(head_common))
print("mid len:", len(mid))
print("head_fs len:", len(head_fs))
print("tail len:", len(tail))
