#!/usr/bin/env python3
"""
Regenerate sitemap.xml from the actual file tree.

Why this exists: sitemap.xml was hand-edited for a long time and drifted out
of sync with the real site (201 of 359 pages were missing at one point,
including several fully-translated locale suites). This script derives the
sitemap directly from what .html files actually exist on disk, so it cannot
drift the same way again.

Usage:
    python3 scripts/generate_sitemap.py

Run from anywhere; it locates the repo root from its own file location.
Called automatically by the pre-commit hook in .githooks/pre-commit, but can
also be run by hand any time.
"""
import re
import os
import sys
import datetime

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SCRIPT_DIR)
os.chdir(ROOT)

LOCALES = ["es", "zh", "ar", "hi", "ru", "ja"]
LOCALE_ORDER = ["en"] + LOCALES
EXCLUDE = {"404.html", "offline.html"}
TODAY = datetime.date.today().isoformat()


def collect_pages():
    pages = []
    for root, _dirs, fnames in os.walk("."):
        _dirs[:] = [d for d in _dirs if d not in ("src", "partials", "scripts", ".git", ".githooks", "node_modules")]
        # never descend into vendor/asset/build dirs looking for pages
        if any(part in (".git", "node_modules", "js", "css", "assets") for part in root.split(os.sep)):
            continue
        for fn in fnames:
            if fn.endswith(".html"):
                p = os.path.normpath(os.path.join(root, fn)).replace("\\", "/")
                if p.startswith("./"):
                    p = p[2:]
                pages.append(p)
    return sorted(p for p in pages if p not in EXCLUDE)


def to_sitemap_path(p):
    if p == "index.html":
        return ""
    if p.endswith("/index.html"):
        return p[: -len("index.html")]
    return p


def split_locale(path):
    for loc in LOCALES:
        if path == loc or path.startswith(loc + "/"):
            return loc, path[len(loc) + 1 :]
    return "en", path


def load_existing(sitemap_path):
    if not os.path.exists(sitemap_path):
        return {}
    sm = open(sitemap_path, encoding="utf-8").read()
    existing = {}
    for b in re.findall(r"<url>(.*?)</url>", sm, re.S):
        loc_m = re.search(r"<loc>https://norito\.in/([^<]*)</loc>", b)
        if not loc_m:
            continue
        lastmod_m = re.search(r"<lastmod>([^<]*)</lastmod>", b)
        priority_m = re.search(r"<priority>([^<]*)</priority>", b)
        existing[loc_m.group(1)] = (
            lastmod_m.group(1) if lastmod_m else TODAY,
            priority_m.group(1) if priority_m else "0.5",
        )
    return existing


def priority_for(sp, fam, existing):
    if sp in existing:
        return existing[sp][1]
    if fam == "":
        return "1.0"
    if fam.endswith("/"):
        return "0.9"
    if fam in ("about.html", "contact.html", "changelog.html"):
        return "0.5"
    if fam in ("how-it-works.html", "privacy.html"):
        return "0.6"
    if fam == "tools.html":
        return "0.8"
    if fam == "blog/":
        return "0.7"
    if fam.startswith("blog/"):
        return "0.6"
    if fam == "compare/":
        return "0.6"
    if fam.startswith("compare/"):
        return "0.6"
    return "0.8"


def lastmod_for(sp, existing):
    return existing[sp][0] if sp in existing else TODAY


def build_sitemap():
    pages = collect_pages()
    sitemap_paths = sorted(set(to_sitemap_path(p) for p in pages))

    existing = load_existing("sitemap.xml")

    families = {}
    for sp in sitemap_paths:
        loc, fam = split_locale(sp)
        families.setdefault(fam, {})[loc] = sp

    lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"',
        '        xmlns:xhtml="http://www.w3.org/1999/xhtml">',
    ]

    def url_for(sp):
        return f"https://norito.in/{sp}"

    for sp in sitemap_paths:
        loc, fam = split_locale(sp)
        fam_map = families[fam]
        lines.append("  <url>")
        lines.append(f"    <loc>{url_for(sp)}</loc>")
        lines.append(f"    <lastmod>{lastmod_for(sp, existing)}</lastmod>")
        lines.append(f"    <priority>{priority_for(sp, fam, existing)}</priority>")
        if len(fam_map) > 1:
            for l in LOCALE_ORDER:
                if l in fam_map:
                    lines.append(
                        f'    <xhtml:link rel="alternate" hreflang="{l}" href="{url_for(fam_map[l])}" />'
                    )
            default_loc = fam_map.get("en", fam_map[next(iter(fam_map))])
            lines.append(
                f'    <xhtml:link rel="alternate" hreflang="x-default" href="{url_for(default_loc)}" />'
            )
        lines.append("  </url>")

    lines.append("</urlset>")
    lines.append("")
    return "\n".join(lines), len(sitemap_paths)


def main():
    new_content, count = build_sitemap()
    old_content = open("sitemap.xml", encoding="utf-8").read() if os.path.exists("sitemap.xml") else None
    changed = new_content != old_content
    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write(new_content)
    print(f"sitemap.xml: {count} URLs written" + (" (changed)" if changed else " (no change)"))
    return 0 if not changed else 2  # exit code 2 signals "file changed" to the hook


if __name__ == "__main__":
    sys.exit(main())
