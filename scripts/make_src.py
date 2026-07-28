#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Phase 2: convert every eligible live HTML page into a small src/ template
where the shared chrome (head-common, header, footer, foot-scripts) has
been replaced with include markers. Page-specific content (title, meta,
JSON-LD, <main>, per-tool app-*.js script tag) stays inline untouched.
Files that don't cleanly match the expected structure are left alone
(not converted) and reported.
"""
import re, os, glob

ROOT = "/sessions/happy-keen-sagan/mnt/norito"
os.chdir(ROOT)

LOCALES = ["es", "zh", "ar", "hi", "ru", "ja"]
SKIP = {"offline.html"}

def locale_of(path):
    parts = path.split("/")
    if parts[0] in LOCALES:
        return parts[0]
    return "en"

def header_variant(path):
    parts = path.split("/")
    rest = parts[1:] if parts[0] in LOCALES else parts
    if rest and rest[0] == "compare":
        return "content"
    if parts[0] == "blog":
        return "content"
    return "standard"

def footer_variant(path):
    loc = locale_of(path)
    is_home = (path == "index.html") or (loc != "en" and path == f"{loc}/index.html")
    return "home" if is_home else "standard"

def span(s, start_pat, end_pat, flags=re.S):
    m = re.search(start_pat, s, flags)
    if not m:
        return None
    start = m.start()
    m2 = re.search(end_pat, s[start:], flags)
    if not m2:
        return None
    return start, start + m2.end()

def replace_span(s, sp, marker):
    if sp is None:
        return None
    a, b = sp
    return s[:a] + marker + s[b:]

EXCLUDE_DIRS = ("src/", "partials/", "scripts/", ".githooks/")
files = sorted(glob.glob("**/*.html", recursive=True))
files = [f for f in files if f not in SKIP and not f.startswith(EXCLUDE_DIRS)]

ok, fail = [], []

for f in files:
    s = open(f, encoding="utf-8").read()
    orig = s

    # absolutize the one page-specific relative asset link (css/style.css)
    s = re.sub(r'href="[^"]*css/style\.css"', 'href="/css/style.css"', s)

    hv = header_variant(f)
    fv = footer_variant(f)

    sp = span(s, r'<script type="text/javascript">\s*\(function\(c,l,a,r,i,t,y\)', r'</noscript>')
    s2 = replace_span(s, sp, "<!--INCLUDE:HEAD-COMMON-->")
    if s2 is None:
        fail.append((f, "head-common")); continue
    s = s2

    sp = span(s, r'<header class="site">', r'</header>')
    s2 = replace_span(s, sp, f"<!--INCLUDE:HEADER:{hv}-->")
    if s2 is None:
        fail.append((f, "header")); continue
    s = s2

    sp = span(s, r'<footer class="site">', r'</footer>')
    s2 = replace_span(s, sp, f"<!--INCLUDE:FOOTER:{fv}-->")
    if s2 is None:
        fail.append((f, "footer")); continue
    s = s2

    # foot-scripts-head (i18n-runtime.js + utils.js) is optional: static info
    # pages (about/contact/index/etc.) don't load the tool runtime at all.
    m = re.search(r'<script src="[^"]*i18n-runtime\.js"></script>\s*\n<script src="[^"]*utils\.js"></script>', s)
    if m:
        s = s[:m.start()] + "<!--INCLUDE:FOOT-SCRIPTS-HEAD-->" + s[m.end():]

    # lang-switcher.js is missing on ~47 EN pages (a real pre-existing bug);
    # match with or without it, and always emit the same marker so the
    # rebuilt page gets the complete (bug-fixed) script set.
    m = re.search(
        r'<script src="[^"]*nav\.js"></script>\s*\n<script src="[^"]*theme-toggle\.js"></script>\s*\n'
        r'(?:<script src="[^"]*lang-switcher\.js"></script>\s*\n)?<script src="[^"]*bg-blobs\.js"></script>', s)
    if not m:
        fail.append((f, "foot-scripts-mid")); continue
    s = s[:m.start()] + "<!--INCLUDE:FOOT-SCRIPTS-MID-->" + s[m.end():]

    sp = span(s, r'<div class="cmdk-overlay" id="cmdkOverlay"',
              r'<div class="cmdk-results" id="cmdkResults"></div>\s*</div>\s*</div>')
    s2 = replace_span(s, sp, "<!--INCLUDE:CMDK-OVERLAY-->")
    if s2 is None:
        fail.append((f, "cmdk-overlay")); continue
    s = s2

    sp = span(s, r'<script src="[^"]*cmdk\.js"></script>', r'</html>')
    s2 = replace_span(s, sp, "<!--INCLUDE:FOOT-SCRIPTS-TAIL-->")
    if s2 is None:
        fail.append((f, "foot-scripts-tail")); continue
    s = s2

    out_path = os.path.join("src", f)
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    open(out_path, "w", encoding="utf-8").write(s)
    ok.append(f)

print(f"converted: {len(ok)} / {len(files)}")
print(f"failed: {len(fail)}")
for x in fail:
    print(" ", x)
