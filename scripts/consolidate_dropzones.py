#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Replaces the two copy-pasted dragenter/dragover/dragleave/drop wiring
shapes in js/app-*.js with calls to the new shared wireDragDrop(el, onDrop)
helper in js/utils.js. Only rewrites files whose wiring matches one of the
two known shapes exactly (verified via a sitewide grep before writing this
script); anything else is left untouched and reported.

Shape 2 (21 files, PDF/image tools -- forEach over dragenter/dragover to add
the class, forEach over dragleave/drop to remove it, then a dedicated drop
listener with the actual file-handling body):

    ["dragenter", "dragover"].forEach((evt) =>
      EL.addEventListener(evt, (e) => { e.preventDefault(); EL.classList.add("drag"); })
    );
    ["dragleave", "drop"].forEach((evt) =>
      EL.addEventListener(evt, (e) => { e.preventDefault(); EL.classList.remove("drag"); })
    );
    EL.addEventListener("drop", (e) => {
      BODY
    });

Shape 1 (3 files -- three separate listeners, class toggle inlined into the
drop body itself):

    EL.addEventListener("dragover", (e) => { e.preventDefault(); EL.classList.add("drag"); });
    EL.addEventListener("dragleave", () => EL.classList.remove("drag"));
    EL.addEventListener("drop", (e) => {
      e.preventDefault();
      EL.classList.remove("drag");
      BODY
    });

Both become:

    wireDragDrop(EL, (e) => {
      BODY
    });
"""
import re, glob, os

ROOT = "/sessions/happy-keen-sagan/mnt/norito"
os.chdir(ROOT)

EL = r'(els\.\w+)'

SHAPE2_RE = re.compile(
    r'[ \t]*\["dragenter", "dragover"\]\.forEach\(\(evt\) =>\s*'
    rf'{EL}\.addEventListener\(evt, \(e\) => \{{ e\.preventDefault\(\); \1\.classList\.add\("drag"\); \}}\)\s*'
    r'\);\s*'
    r'\["dragleave", "drop"\]\.forEach\(\(evt\) =>\s*'
    rf'\1\.addEventListener\(evt, \(e\) => \{{ e\.preventDefault\(\); \1\.classList\.remove\("drag"\); \}}\)\s*'
    r'\);\s*'
    r'\1\.addEventListener\("drop", \(e\) => \{\n'
    r'(?P<body>.*?)'
    r'\n[ \t]*\}\);\n',
    re.S,
)

# Same shape, but the two forEach inner handlers are written multi-line
# instead of single-line (`(e) => {\n  e.preventDefault();\n  ...add("drag");\n}`).
SHAPE2B_RE = re.compile(
    r'[ \t]*\["dragenter", "dragover"\]\.forEach\(\(evt\) =>\s*'
    rf'{EL}\.addEventListener\(evt, \(e\) => \{{\s*'
    r'e\.preventDefault\(\);\s*'
    r'\1\.classList\.add\("drag"\);\s*'
    r'\}\)\s*'
    r'\);\s*'
    r'\["dragleave", "drop"\]\.forEach\(\(evt\) =>\s*'
    r'\1\.addEventListener\(evt, \(e\) => \{\s*'
    r'e\.preventDefault\(\);\s*'
    r'\1\.classList\.remove\("drag"\);\s*'
    r'\}\)\s*'
    r'\);\s*'
    r'\1\.addEventListener\("drop", \(e\) => \{\n'
    r'(?P<body>.*?)'
    r'\n[ \t]*\}\);\n',
    re.S,
)

SHAPE1_RE = re.compile(
    rf'[ \t]*{EL}\.addEventListener\("dragover", \(e\) => \{{ e\.preventDefault\(\); \1\.classList\.add\("drag"\); \}}\);\s*'
    r'\1\.addEventListener\("dragleave", \(\) => \1\.classList\.remove\("drag"\)\);\s*'
    r'\1\.addEventListener\("drop", \(e\) => \{\n'
    r'[ \t]*e\.preventDefault\(\);\s*\n'
    r'[ \t]*\1\.classList\.remove\("drag"\);\s*\n'
    r'(?P<body>.*?)'
    r'\n[ \t]*\}\);\n',
    re.S,
)

def render(el, body, indent):
    return f'{indent}wireDragDrop({el}, (e) => {{\n{body}\n{indent}}});\n'

def process(path):
    text = open(path, encoding="utf-8").read()
    for shape_name, rx in (("shape2", SHAPE2_RE), ("shape2b", SHAPE2B_RE), ("shape1", SHAPE1_RE)):
        m = rx.search(text)
        if not m:
            continue
        el = m.group(1)
        body = m.group("body")
        indent = re.match(r'[ \t]*', text[m.start():]).group(0)
        new_block = render(el, body, indent)
        new_text = text[:m.start()] + new_block + text[m.end():]
        open(path, "w", encoding="utf-8").write(new_text)
        return shape_name
    return None

def main():
    files = sorted(glob.glob("js/app-*.js"))
    results = {}
    for f in files:
        text = open(f, encoding="utf-8").read()
        if '"drop"' not in text and "'drop'" not in text:
            continue
        r = process(f)
        results[f] = r
    for f, r in results.items():
        print(f, "->", r or "NO MATCH")
    matched = sum(1 for r in results.values() if r)
    print(f"\n{matched} / {len(results)} dropzone files converted")

if __name__ == "__main__":
    main()
