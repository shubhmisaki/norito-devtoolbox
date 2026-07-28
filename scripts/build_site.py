#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Regenerates the live site from src/**/*.html + partials/**/*.html.

Run this after editing anything under src/ or partials/. It overwrites the
corresponding live file at the repo root for every page that has a src/
counterpart. Pages with no src/ counterpart are left untouched.
"""
import re, os, glob

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

LOCALES = ["es", "zh", "ar", "hi", "ru", "ja"]

_cache = {}
def load(path):
    if path not in _cache:
        _cache[path] = open(path, encoding="utf-8").read()
    return _cache[path]

def locale_of(live_path):
    parts = live_path.split("/")
    if parts[0] in LOCALES:
        return parts[0]
    return "en"

MARKER_RE = re.compile(r"<!--INCLUDE:([A-Z0-9-]+)(?::([a-z-]+))?-->")

# "Related tools" heading, translated per locale. Sourced from a sitewide
# scan of the live h2 text that already shipped in each locale (one fixed
# string per locale, confirmed identical across every page in that locale).
RELATED_TOOLS_H2 = {
    "en": "Related tools",
    "es": "Herramientas relacionadas",
    "zh": "相关工具",
    "ar": "أدوات ذات صلة",
    "hi": "संबंधित टूल",
    "ru": "Похожие инструменты",
    "ja": "関連ツール",
}

RELATED_BLOCK_RE = re.compile(r"<!--RELATED-TOOLS\n(.*?)\n-->\n?", re.S)

def render_related_tools(block_text, loc):
    h2 = RELATED_TOOLS_H2[loc]
    cards = []
    for line in block_text.strip("\n").split("\n"):
        href, label, desc = line.split("|", 2)
        cards.append(
            f'        <a class="related-card" href="{href}">\n'
            f'          <strong>{label}</strong>\n'
            f'          <span>{desc}</span>\n'
            f'        </a>'
        )
    cards_html = "\n".join(cards)
    return (
        f'    <div class="related-tools">\n'
        f'      <h2>{h2}</h2>\n'
        f'      <div class="related-grid">\n'
        f'{cards_html}\n'
        f'      </div>\n'
        f'    </div>\n'
    )

def expand(src_text, loc):
    def repl(m):
        name, variant = m.group(1), m.group(2)
        if name == "HEAD-COMMON":
            return load("partials/head-common.html")
        if name == "HEADER":
            fname = "header-content.html" if variant == "content" else "header.html"
            return load(f"partials/{loc}/{fname}")
        if name == "FOOTER":
            fname = "footer-home.html" if variant == "home" else "footer.html"
            return load(f"partials/{loc}/{fname}")
        if name == "FOOT-SCRIPTS-HEAD":
            return load("partials/foot-scripts-head.html")
        if name == "FOOT-SCRIPTS-MID":
            return load("partials/foot-scripts-mid.html")
        if name == "CMDK-OVERLAY":
            return load(f"partials/{loc}/cmdk-overlay.html")
        if name == "FOOT-SCRIPTS-TAIL":
            return load("partials/foot-scripts-tail.html")
        raise ValueError(f"unknown include marker: {name}")
    out = MARKER_RE.sub(repl, src_text)
    out = RELATED_BLOCK_RE.sub(lambda m: render_related_tools(m.group(1), loc), out)
    return out

# All pages now share the one common (mega-sitemap) footer per locale, so
# nothing needs to be excluded any more.
EXCLUDE_LIVE = set()

def main():
    src_files = sorted(glob.glob("src/**/*.html", recursive=True))
    written = 0
    changed = 0
    for sf in src_files:
        live_path = sf[len("src/"):]
        if live_path in EXCLUDE_LIVE:
            continue
        loc = locale_of(live_path)
        text = open(sf, encoding="utf-8").read()
        out = expand(text, loc)
        if "<!--INCLUDE:" in out:
            print(f"WARNING: unresolved marker left in {live_path}, skipping write")
            continue
        before = open(live_path, encoding="utf-8").read() if os.path.exists(live_path) else None
        if before != out:
            open(live_path, "w", encoding="utf-8").write(out)
            changed += 1
        written += 1
    print(f"regenerated {written} / {len(src_files)} live pages from src/ + partials/ ({changed} changed)")
    return 2 if changed else 0

if __name__ == "__main__":
    raise SystemExit(main())
