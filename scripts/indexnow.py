#!/usr/bin/env python3
"""Tell IndexNow (Bing, Yandex, Seznam, Naver...) which pages changed.

Reads changed file paths on stdin (one per line, repo-relative), keeps the
live .html pages, maps each to its canonical URL and submits them in one
request. Run by .github/workflows/indexnow.yml after every push to main.

    git diff --name-only A B | python3 scripts/indexnow.py
    python3 scripts/indexnow.py --all        # resubmit the whole sitemap
"""
import json, re, sys, urllib.request

HOST = "norito.in"
KEY = "6abb5725df3b3f417485447256334cbb"
SKIP_PREFIXES = ("src/", "partials/", "scripts/", ".github/", "js/", "css/")
SKIP_FILES = {"404.html", "offline.html"}
NOINDEX = re.compile(r"(^|/)(terms|privacy)\.html$")


def to_url(path):
    if path == "index.html":
        return f"https://{HOST}/"
    if path.endswith("/index.html"):
        return f"https://{HOST}/{path[:-len('index.html')]}"
    return f"https://{HOST}/{path}"


def main():
    if "--all" in sys.argv:
        xml = open("sitemap.xml", encoding="utf-8").read()
        urls = re.findall(r"<loc>([^<]+)</loc>", xml)
    else:
        urls = []
        for line in sys.stdin:
            p = line.strip()
            if not p.endswith(".html") or p.startswith(SKIP_PREFIXES):
                continue
            if p in SKIP_FILES or NOINDEX.search(p):
                continue
            urls.append(to_url(p))
    urls = sorted(set(urls))
    if not urls:
        print("indexnow: nothing to submit")
        return 0
    body = json.dumps({
        "host": HOST,
        "key": KEY,
        "keyLocation": f"https://{HOST}/{KEY}.txt",
        "urlList": urls[:10000],
    }).encode()
    req = urllib.request.Request(
        "https://api.indexnow.org/indexnow",
        data=body,
        headers={"Content-Type": "application/json; charset=utf-8"},
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            print(f"indexnow: submitted {len(urls)} URLs, HTTP {r.status}")
    except Exception as e:  # never fail the workflow over a ping
        print(f"indexnow: submit failed: {e}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
