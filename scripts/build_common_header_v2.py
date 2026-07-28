#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Fix-up pass: the first build_common_header.py run correctly filled every
locale's nav out to the full 59-item EN catalog (translated-or-English-
fallback per item), but it reordered the categories to EN's order and
silently dropped the bare "Blog" link that header-content.html appends
after the last nav-group. This script re-derives the locale's correct
group ORDER and the nav_tail (Blog link) from a live page that hasn't
been rebuilt since the header partials changed, and re-renders using
those, while reusing the already-correct per-item translations sitting in
the current (right-content, wrong-order) partials/{locale}/header*.html.
"""
import re, os

ROOT = "/sessions/happy-keen-sagan/mnt/norito"
os.chdir(ROOT)

LOCALES = ["es", "zh", "ar", "hi", "ru", "ja"]
# a live page per locale that has NOT been rebuilt since the header change,
# for standard and content(compare) header variants respectively
ORDER_SOURCE = {
    "": "pdf/merge-pdf.html",
    "-content": "compare/norito-vs-ilovepdf.html",
}

def nav_block(s):
    a = s.index('<nav class="site-nav" id="siteNav">')
    b = s.index("</nav>", a) + len("</nav>")
    return s[a:b]

def parse_groups_with_tail(nav_html):
    groups = re.findall(
        r'<div class="nav-group">(.*?)</div>\s*</div>\s*(?=<div class="nav-group">|</nav>)',
        nav_html, re.S)
    last_end = 0
    for m in re.finditer(r'<div class="nav-group">.*?</div>\s*</div>', nav_html, re.S):
        last_end = m.end()
    tail = nav_html[last_end:nav_html.index("</nav>")]

    parsed = []
    for g in groups:
        m_btn = re.search(r'<button type="button" class="nav-cat">([^<]+)</button>', g)
        m_a = re.search(r'<a class="nav-cat" href="([^"]+)">([^<]+)</a>', g)
        if m_btn:
            parsed.append({"type": "button", "header": m_btn.group(1), "hub_href": None})
        else:
            parsed.append({"type": "a", "header": m_a.group(2), "hub_href": m_a.group(1)})
    return parsed, tail

def parse_items_by_header(nav_html):
    """current (right-content) partial -> {category header text: [(href,svg,label,desc),...]}"""
    groups = re.findall(
        r'<div class="nav-group">(.*?)</div>\s*</div>\s*(?=<div class="nav-group">|</nav>)',
        nav_html, re.S)
    out = {}
    for g in groups:
        m_btn = re.search(r'<button type="button" class="nav-cat">([^<]+)</button>', g)
        m_a = re.search(r'<a class="nav-cat" href="([^"]+)">([^<]+)</a>', g)
        header = m_btn.group(1) if m_btn else m_a.group(2)
        items = re.findall(
            r'<a href="([^"]+)">(<svg.*?</svg>)<div class="nav-link-body">([^<]+)<span>([^<]+)</span></div></a>',
            g, re.S)
        out[header] = items
    return out

for loc in LOCALES:
    for suffix, order_src in ORDER_SOURCE.items():
        # 1. correct order + tail, from the not-yet-rebuilt live page
        live_path = order_src if loc == "en" else f"{loc}/{order_src}"
        live_nav = nav_block(open(live_path, encoding="utf-8").read())
        order_groups, tail = parse_groups_with_tail(live_nav)

        # 2. correct item content, from the current (right-content) partial
        cur_path = f"partials/{loc}/header{suffix}.html"
        cur_nav = nav_block(open(cur_path, encoding="utf-8").read())
        items_by_header = parse_items_by_header(cur_nav)

        # 3. re-render in the live page's original group order
        parts = ['<nav class="site-nav" id="siteNav">']
        for og in order_groups:
            parts.append('      <div class="nav-group">')
            if og["type"] == "button":
                parts.append(f'        <button type="button" class="nav-cat">{og["header"]}</button>')
            else:
                parts.append(f'        <a class="nav-cat" href="{og["hub_href"]}">{og["header"]}</a>')
            parts.append('        <div class="nav-panel">')
            for href, svg, label, desc in items_by_header[og["header"]]:
                parts.append(f'          <a href="{href}">{svg}<div class="nav-link-body">{label}<span>{desc}</span></div></a>')
            parts.append('        </div>')
            parts.append('      </div>')
        parts.append(tail)
        parts.append('</nav>')
        new_nav = "\n".join(parts)

        full = open(cur_path, encoding="utf-8").read()
        old_nav = nav_block(full)
        full = full.replace(old_nav, new_nav)
        open(cur_path, "w", encoding="utf-8").write(full)

        total = sum(len(v) for v in items_by_header.values())
        print(loc, suffix or "(standard)", total, "items, tail:", repr(tail.strip()[:60]))
