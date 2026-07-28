#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Build one common mega-footer (sitemap-style: Product + PDF + Images +
Developer + Text + Utilities + SEO + Design columns, plus the bottom row)
per locale, replacing the previous standard/home/misc variants. Tool links
use the locale's own translated page + label where one exists (sourced
from the already-built header partial), and fall back to the English page
otherwise. Blog always points to the English /blog/ (not translated yet).
"""
import re, os, json

ROOT = "/sessions/happy-keen-sagan/mnt/norito"
os.chdir(ROOT)

LOCALES = ["es", "zh", "ar", "hi", "ru", "ja"]
ALL_LOCS = ["en"] + LOCALES

CAT_HEADER_TR = {
    # loc: [Images, Developer, Text, Utilities]  (PDF/SEO/Design stay English)
    "en": ["Images", "Developer", "Text", "Utilities"],
    "es": ["Imágenes", "Desarrollo", "Texto", "Utilidades"],
    "zh": ["图像", "开发工具", "文本", "实用工具"],
    "ar": ["الصور", "أدوات المطورين", "النصوص", "أدوات عامة"],
    "hi": ["इमेज", "डेवलपर", "टेक्स्ट", "यूटिलिटीज़"],
    "ru": ["Изображения", "Разработка", "Текст", "Утилиты"],
    "ja": ["画像", "開発", "テキスト", "ユーティリティ"],
}
PRODUCT_TR = {
    "en": ("Product", "All tools"),
    "es": ("Producto", "Todas las herramientas"),
    "zh": ("产品", "所有工具"),
    "ar": ("المنتج", "كل الأدوات"),
    "hi": ("प्रोडक्ट", "सभी टूल"),
    "ru": ("Продукт", "Все инструменты"),
    "ja": ("プロダクト", "すべてのツール"),
}

def extract_nav_labels(path):
    s = open(path, encoding="utf-8").read()
    out = {}
    for m in re.finditer(r'<a href="([^"]+)"><svg.*?</svg><div class="nav-link-body">([^<]+)<span>', s):
        out[m.group(1)] = m.group(2)
    return out

def extract_bottom(path):
    s = open(path, encoding="utf-8").read()
    m = re.search(r'<div class="footer-bottom">(.*?)</div>\s*</div>\s*</footer>', s, re.S)
    out = {}
    for m2 in re.finditer(r'<a href="([^"]+)"[^>]*>([^<]+)</a>', m.group(1)):
        out[m2.group(1)] = m2.group(2)
    return out

def extract_tagline(path):
    s = open(path, encoding="utf-8").read()
    return re.search(r'<p class="footer-tagline">([^<]+)</p>', s).group(1)

nav_labels = {loc: extract_nav_labels(f"partials/{loc}/header.html") for loc in ALL_LOCS}
bottom_map = {loc: extract_bottom(f"partials/{loc}/footer-home.html") for loc in ALL_LOCS}
tagline = {loc: extract_tagline(f"partials/{loc}/footer.html") for loc in ALL_LOCS}

# master shape from EN about.html
s = open("about.html", encoding="utf-8").read()
grid = re.search(r'<div class="footer-grid">(.*?)</div>\s*<div class="footer-bottom">', s, re.S).group(1)
cols = []
for m in re.finditer(r'<div class="footer-col( footer-product)?">\s*<h3>([^<]+)</h3>(.*?)</div>', grid, re.S):
    is_product = bool(m.group(1))
    header = m.group(2)
    items = re.findall(r'<a href="([^"]+)">([^<]+)</a>', m.group(3))
    cols.append({"product": is_product, "header": header, "items": [(h.lstrip("/"), lbl) for h, lbl in items]})

CAT_ORDER = ["Images", "Developer", "Text", "Utilities"]  # non-English-header categories, in EN col order

def loc_href_label(loc, en_href_rel, en_label):
    """Return (href, label) for this locale: translated version if the tool
    is translated for this locale, else English fallback."""
    if loc == "en":
        return "/" + en_href_rel, en_label
    loc_href = f"/{loc}/{en_href_rel}"
    if loc_href in nav_labels[loc]:
        return loc_href, nav_labels[loc][loc_href]
    return "/" + en_href_rel, en_label  # fall back to English page

def build_footer(loc):
    out = []
    out.append('<footer class="site">')
    out.append('  <div class="wrap">')
    out.append('    <div class="footer-grid">')
    out.append('      <div class="footer-brand">')
    out.append('        <div class="footer-brand-name">norito</div>')
    out.append(f'        <p class="footer-tagline">{tagline[loc]}</p>')
    out.append('      </div>')

    for col in cols:
        if col["product"]:
            header, all_tools_label = PRODUCT_TR[loc]
            out.append('      <div class="footer-col footer-product">')
            out.append(f'        <h3>{header}</h3>')
            for en_href, en_label in col["items"]:
                if en_href == "tools.html":
                    href, label = ("/tools.html", all_tools_label)
                elif en_href == "blog/":
                    href, label = ("/blog/", bottom_map[loc].get("/blog/", "Blog"))
                elif en_href in ("changelog.html", "how-it-works.html", "compare/",
                                  "about.html", "contact.html", "privacy.html"):
                    loc_href = "/" + en_href if loc == "en" else f"/{loc}/{en_href}"
                    label = bottom_map[loc].get(loc_href, en_label)
                    href = loc_href
                else:
                    href, label = loc_href_label(loc, en_href, en_label)
                out.append(f'        <a href="{href}">{label}</a>')
            out.append('      </div>')
            continue

        if col["header"] in CAT_ORDER:
            header = CAT_HEADER_TR[loc][CAT_ORDER.index(col["header"])]
        else:
            header = col["header"]  # PDF, SEO, Design stay English
        out.append('      <div class="footer-col">')
        out.append(f'        <h3>{header}</h3>')
        for en_href, en_label in col["items"]:
            href, label = loc_href_label(loc, en_href, en_label)
            out.append(f'        <a href="{href}">{label}</a>')
        out.append('      </div>')

    out.append('    </div>')

    # footer-bottom row
    out.append('    <div class="footer-bottom">')
    copy = bottom_map[loc]
    def bl(key_suffix, fallback):
        loc_key = "/" + key_suffix if loc == "en" else f"/{loc}/{key_suffix}"
        return loc_key, copy.get(loc_key, fallback)
    tagline_span = {
        "en": "&copy; 2026 norito. All tools run locally in your browser.",
    }
    # reuse the copyright span already present in the existing footer.html partial
    existing = open(f"partials/{loc}/footer.html", encoding="utf-8").read()
    span_m = re.search(r'<span>(&copy;.*?)</span>', existing)
    out.append(f'      <span>{span_m.group(1)}</span>')
    for suffix, fb in [("changelog.html", "Changelog"), ("blog/", "Blog"),
                        ("compare/", "Compare"), ("how-it-works.html", "How it Works"),
                        ("privacy.html", "Privacy Policy")]:
        href, label = bl(suffix, fb)
        if suffix == "blog/":
            href, label = "/blog/", copy.get("/blog/", "Blog")
        out.append(f'      <a href="{href}">{label}</a>')
    kofi_label = copy.get("https://ko-fi.com/shubhmisaki", "Buy me a coffee")
    out.append(f'      <a href="https://ko-fi.com/shubhmisaki" target="_blank" rel="noopener">{kofi_label}</a>')
    out.append('    </div>')
    out.append('  </div>')
    out.append('</footer>')
    return "\n".join(out) + "\n"

for loc in ALL_LOCS:
    text = build_footer(loc)
    # write as the SINGLE common footer, replacing footer.html; footer-home.html
    # becomes identical (kept for backward compat / marker resolution)
    open(f"partials/{loc}/footer.html", "w", encoding="utf-8").write(text)
    open(f"partials/{loc}/footer-home.html", "w", encoding="utf-8").write(text)
    print(loc, len(text), "bytes")
