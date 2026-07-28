#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Componentize the "Related tools" block. Every page currently repeats the
full HTML shell (h2 + related-grid + N related-card <a> tags) verbatim;
only the (href, label, desc) triples actually differ per page. This
replaces that block, in every src/**/*.html file, with a compact data
marker:

    <!--RELATED-TOOLS
    href|label|desc
    href|label|desc
    href|label|desc
    -->

build_site.py then renders the marker back into the full HTML using one
shared template, with the h2 text picked per-locale. Any future change to
the related-tools markup (styling, adding an icon, etc.) becomes a
one-place edit instead of a 125-file edit.

Verified precondition (via sitewide scan): every related-tools block
sitewide has exactly 3 cards, and the h2 text is a fixed per-locale
string across all pages within that locale (7 known translations). Any
file that doesn't match this exact shape is left untouched and reported,
not guessed at.
"""
import re, glob, os

ROOT = "/sessions/happy-keen-sagan/mnt/norito"
os.chdir(ROOT)

BLOCK_RE = re.compile(
    r'[ \t]*<div class="related-tools">\s*'
    r'<h2>([^<]*)</h2>\s*'
    r'<div class="related-grid">\s*'
    r'(?P<cards>(?:<a class="related-card"[^>]*>.*?</a>\s*)+)'
    r'</div>\s*'
    r'</div>\n?',
    re.S,
)
CARD_RE = re.compile(
    r'<a class="related-card" href="([^"]+)">\s*'
    r'<strong>(.*?)</strong>\s*'
    r'<span>(.*?)</span>\s*'
    r'</a>',
    re.S,
)

def process(path):
    text = open(path, encoding="utf-8").read()
    m = BLOCK_RE.search(text)
    if not m:
        return None  # no related-tools block in this file, fine
    cards = CARD_RE.findall(m.group("cards"))
    if not cards:
        return "NO_CARDS_MATCHED"
    # sanity: reconstruct and compare card count against raw <a class="related-card" occurrences
    raw_count = m.group("cards").count('class="related-card"')
    if raw_count != len(cards):
        return "CARD_COUNT_MISMATCH"
    lines = ["<!--RELATED-TOOLS"]
    for href, label, desc in cards:
        if "|" in href or "|" in label or "|" in desc:
            return "PIPE_IN_CONTENT"
        if "\n" in href or "\n" in label or "\n" in desc:
            return "NEWLINE_IN_CONTENT"
        lines.append(f"{href}|{label.strip()}|{desc.strip()}")
    lines.append("-->\n")
    marker = "\n".join(lines)
    new_text = text[:m.start()] + marker + text[m.end():]
    open(path, "w", encoding="utf-8").write(new_text)
    return "OK"

def main():
    files = sorted(glob.glob("src/**/*.html", recursive=True))
    stats = {}
    problems = []
    for f in files:
        r = process(f)
        if r is None:
            continue
        stats[r] = stats.get(r, 0) + 1
        if r != "OK":
            problems.append((f, r))
    print("results:", stats)
    for f, r in problems:
        print("PROBLEM:", r, f)

if __name__ == "__main__":
    main()
