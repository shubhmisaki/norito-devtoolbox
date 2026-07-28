#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fill every locale's nav dropdowns out to the full EN tool catalog (59
items across 7 categories), the same "translated where it exists, English
fallback otherwise" rule just applied to the footer. Locale headers
currently only list the ~32 tools that are translated for that locale;
this makes every tool reachable from the nav on every locale, not just
from the footer.

Category headers, dropdown-vs-link category style, and per-locale
translated (href, label, description) triples are all preserved from the
locale's own existing header.html; only the item *lists* are extended.
"""
import re, os, json

ROOT = "/sessions/happy-keen-sagan/mnt/norito"
os.chdir(ROOT)

LOCALES = ["es", "zh", "ar", "hi", "ru", "ja"]

def parse_header_groups(path):
    s = open(path, encoding="utf-8").read()
    groups = re.findall(
        r'<div class="nav-group">(.*?)</div>\s*</div>\s*(?=<div class="nav-group">|</nav>)',
        s, re.S)
    parsed = []
    for g in groups:
        m_btn = re.search(r'<button type="button" class="nav-cat">([^<]+)</button>', g)
        m_a = re.search(r'<a class="nav-cat" href="([^"]+)">([^<]+)</a>', g)
        items = re.findall(
            r'<a href="([^"]+)">(<svg.*?</svg>)<div class="nav-link-body">([^<]+)<span>([^<]+)</span></div></a>',
            g, re.S)
        parsed_items = {href: {"svg": svg, "label": lbl, "desc": desc} for href, svg, lbl, desc in items}
        if m_btn:
            parsed.append({"type": "button", "header": m_btn.group(1), "hub_href": None, "items": parsed_items})
        else:
            parsed.append({"type": "a", "header": m_a.group(2), "hub_href": m_a.group(1), "items": parsed_items})
    return parsed

en_master = parse_header_groups("partials/en/header.html")
# category identity by EN header text, in EN's own order
EN_CAT_ORDER = [g["header"] for g in en_master]  # ['PDF','Images','Developer','Text','Utilities','SEO','Design']

def build_locale_header(loc, variant_suffix=""):
    fname = f"partials/{loc}/header{variant_suffix}.html"
    loc_groups = parse_header_groups(fname)
    # map by header text (category identity is consistent across EN/locale)
    loc_by_header = {g["header"]: g for g in loc_groups}
    # cross-reference: locale category headers are translated (e.g. "Изображения"
    # for "Images"); build EN-header -> loc-group by matching group *position*
    # in the button-groups-first-then-a-groups order, since text differs.
    # Locale order: [Images, Developer, Text, Utilities] as buttons, then
    # [PDF, SEO, Design] as links -- same 7 categories as EN, different order/labels.
    btn_groups = [g for g in loc_groups if g["type"] == "button"]
    a_groups = {g["header"]: g for g in loc_groups if g["type"] == "a"}
    # EN order for the 4 button-style categories:
    BTN_CAT_EN_ORDER = ["Images", "Developer", "Text", "Utilities"]
    if len(btn_groups) == len(BTN_CAT_EN_ORDER):
        btn_by_en_header = dict(zip(BTN_CAT_EN_ORDER, btn_groups))
    else:
        btn_by_en_header = {}

    out_groups = []
    for en_group in en_master:
        en_header = en_group["header"]
        if en_header in btn_by_en_header:
            loc_group = btn_by_en_header[en_header]
        elif en_header in a_groups:
            loc_group = a_groups[en_header]
        else:
            loc_group = None

        loc_header_text = loc_group["header"] if loc_group else en_header
        loc_type = loc_group["type"] if loc_group else en_group["type"]
        loc_hub_href = loc_group["hub_href"] if loc_group else en_group["hub_href"]
        loc_items_by_href = loc_group["items"] if loc_group else {}

        new_items = []
        for en_href, en_item in en_group["items"].items():
            loc_href = en_href if loc == "en" else f"/{loc}{en_href}"
            if loc_href in loc_items_by_href:
                it = loc_items_by_href[loc_href]
                new_items.append((loc_href, it["svg"], it["label"], it["desc"]))
            else:
                # fall back to the English page/label/description
                new_items.append((en_href, en_item["svg"], en_item["label"], en_item["desc"]))
        out_groups.append({"type": loc_type, "header": loc_header_text,
                            "hub_href": loc_hub_href, "items": new_items})
    return out_groups

def render_header(loc, groups, variant_suffix=""):
    src = open(f"partials/{loc}/header{variant_suffix}.html", encoding="utf-8").read()
    pre, rest = src.split('<nav class="site-nav" id="siteNav">', 1)
    post = rest.split("</nav>", 1)[1]

    parts = ['<nav class="site-nav" id="siteNav">']
    for g in groups:
        parts.append('      <div class="nav-group">')
        if g["type"] == "button":
            parts.append(f'        <button type="button" class="nav-cat">{g["header"]}</button>')
        else:
            parts.append(f'        <a class="nav-cat" href="{g["hub_href"]}">{g["header"]}</a>')
        parts.append('        <div class="nav-panel">')
        for href, svg, label, desc in g["items"]:
            parts.append(f'          <a href="{href}">{svg}<div class="nav-link-body">{label}<span>{desc}</span></div></a>')
        parts.append('        </div>')
        parts.append('      </div>')
    parts.append('</nav>')
    nav_html = "\n".join(parts)
    return pre + nav_html + post

for loc in LOCALES:
    for suffix in ("", "-content"):
        groups = build_locale_header(loc, suffix)
        new_html = render_header(loc, groups, suffix)
        path = f"partials/{loc}/header{suffix}.html"
        open(path, "w", encoding="utf-8").write(new_html)
        total = sum(len(g["items"]) for g in groups)
        print(loc, suffix or "(standard)", total, "items")
