#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Adds a "Target size" control to src/pdf/compress-pdf.html and generates the
size-specific landing pages src/pdf/compress-pdf-to-{100kb,200kb,500kb,1mb}.html
(English only). Run, then scripts/build_site.py and scripts/generate_sitemap.py.

Each preset page is the same real tool with the target pre-selected, plus its
own title, description, headings and FAQ, so it answers the specific query
("compress pdf to 100kb") instead of being a doorway copy.
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

BASE = "src/pdf/compress-pdf.html"

PRESETS = [
    dict(slug="100kb", kb=100, label="100 KB", name="Compress PDF to 100KB",
         why="Government portals, exam forms and job applications often cap uploads at 100 KB.",
         tip="A single scanned page usually fits. For multi-page documents, tick the option to convert pages to images, or split the file first."),
    dict(slug="200kb", kb=200, label="200 KB", name="Compress PDF to 200KB",
         why="200 KB is a common limit for application forms, ID proofs and certificate uploads.",
         tip="Two or three scanned pages usually fit. A text-only PDF may already be near this size."),
    dict(slug="500kb", kb=500, label="500 KB", name="Compress PDF to 500KB",
         why="500 KB is a typical cap for résumés, bank statements and supporting documents on web forms.",
         tip="Most scanned documents of up to ten pages fit at the default settings."),
    dict(slug="1mb", kb=1024, label="1 MB", name="Compress PDF to 1MB",
         why="1 MB is a common upload limit for support tickets, visa forms and university portals.",
         tip="Most documents reach 1 MB without converting any page to an image."),
]

TARGET_BLOCK = '''      <div class="field-row" style="margin-bottom:12px;">
        <div class="field">
          <label for="targetSelect">Target size</label>
          <select id="targetSelect" disabled>
            <option value="0">No target (use the settings above)</option>
{options}
          </select>
        </div>
      </div>
      <label class="note" style="display:flex; gap:8px; align-items:flex-start; margin:0 0 20px;">
        <input type="checkbox" id="allowFlatten" disabled style="margin-top:3px;" />
        <span>If needed, convert pages to images to reach the target. The file gets much smaller, but text is no longer selectable.</span>
      </label>
'''
TARGET_RE = re.compile(r'      <div class="field-row" style="margin-bottom:12px;">\n        <div class="field">\n          <label for="targetSelect">.*?id="allowFlatten".*?</span>\n      </label>\n', re.S)
NAV_RE = re.compile(r'    <nav class="size-chips".*?</nav>\n', re.S)
NOTE_ANCHOR = '      <p class="note" style="margin-top:-12px; margin-bottom:20px;">Resolution and quality only affect'

SIZES = [("100kb", "100 KB"), ("200kb", "200 KB"), ("500kb", "500 KB"), ("1mb", "1 MB")]


def options(selected_kb):
    out = []
    for kb, lab in [(100, "Under 100 KB"), (200, "Under 200 KB"), (500, "Under 500 KB"), (1024, "Under 1 MB"), (2048, "Under 2 MB")]:
        sel = " selected" if kb == selected_kb else ""
        out.append(f'            <option value="{kb}"{sel}>{lab}</option>')
    return "\n".join(out)


def nav(current_slug):
    links = []
    for slug, lab in SIZES:
        if slug == current_slug:
            links.append(f'<span class="size-chip current" aria-current="page">{lab}</span>')
        else:
            links.append(f'<a class="size-chip" href="compress-pdf-to-{slug}.html">{lab}</a>')
    anyl = '<a class="size-chip" href="compress-pdf.html">Any size</a>' if current_slug else '<span class="size-chip current" aria-current="page">Any size</span>'
    return ('    <nav class="size-chips" aria-label="Common target sizes">\n      <span class="size-chips-label">Common sizes</span>\n      '
            + "\n      ".join(links + [anyl]) + "\n    </nav>\n")


def with_controls(text, selected_kb, current_slug):
    text = TARGET_RE.sub("", text)
    text = NAV_RE.sub("", text)
    assert text.count(NOTE_ANCHOR) == 1, "note anchor moved"
    text = text.replace(NOTE_ANCHOR, TARGET_BLOCK.format(options=options(selected_kb)) + NOTE_ANCHOR, 1)
    # chips go right before the tool panel
    anchor = '    <div class="panel">\n      <div class="dropzone" id="drop">'
    assert text.count(anchor) == 1, "panel anchor moved"
    return text.replace(anchor, nav(current_slug) + anchor, 1)


def make_preset(base, p):
    t = base
    url_old = "https://norito.in/pdf/compress-pdf.html"
    url_new = f"https://norito.in/pdf/compress-pdf-to-{p['slug']}.html"
    title = f"{p['name']} Online Free (No Upload) | norito"
    desc = (f"Reduce a PDF to under {p['label']} in your browser. Nothing is uploaded. "
            f"Real text stays selectable unless you choose to convert pages to images.")
    t = t.replace("Compress PDF File Size Online Free | norito", title)
    t = t.replace("Shrink a PDF's file size without flattening text to an image. Real text stays selectable, only scans and embedded photos get recompressed. Runs in your browser.", desc)
    t = t.replace("Shrink a PDF's file size without flattening text pages to images. Runs entirely in your browser.", desc)
    t = t.replace(url_old, url_new)
    t = t.replace('"name": "Compress PDF",', f'"name": "{p["name"]}",')
    t = t.replace('"name": "Compress PDF",', f'"name": "{p["name"]}",')
    t = t.replace('/ Compress PDF</p>', f'/ <a href="compress-pdf.html">Compress PDF</a> / {p["label"]}</p>')
    t = t.replace("<h1>Compress a PDF's File Size</h1>", f"<h1>{p['name']}</h1>")
    lede_old = re.search(r'    <p class="lede">.*?</p>\n', t, re.S).group(0)
    lede_new = (f'    <p class="lede">\n      {p["why"]} Choose a PDF and this tool tries progressively smaller settings until it fits under {p["label"]}. '
                f'{p["tip"]} Nothing is uploaded, it all happens on your device.\n    </p>\n')
    t = t.replace(lede_old, lede_new, 1)
    t = re.sub(r'    <p class="note">Compressing to email a PDF\?.*?</p>\n', '', t)

    q1 = f"How do I get a PDF under {p['label']}?"
    a1 = (f"Choose your PDF and click Compress. The tool tries smaller and smaller image resolution and quality settings until the file fits under {p['label']}, "
          f"and stops at the first one that does. If your PDF is mostly text, tick the option to convert pages to images; that is the only way to shrink a text-heavy file a long way.")
    q2 = f"What if my PDF is still bigger than {p['label']}?"
    a2 = ("You get the smallest version the tool could make, and a clear message that it missed the target. From there you can split the PDF into parts, remove pages you don't need, "
          "or tick the option to convert pages to images. A PDF with many full-page photos or a lot of pages may simply not fit in a very small limit.")
    ld_extra = (
        '    {\n      "@type": "Question",\n      "name": "%s",\n      "acceptedAnswer": { "@type": "Answer", "text": "%s" }\n    },\n'
        '    {\n      "@type": "Question",\n      "name": "%s",\n      "acceptedAnswer": { "@type": "Answer", "text": "%s" }\n    },\n'
        % (q1, a1, q2, a2))
    marker = '    {\n      "@type": "Question",\n      "name": "Are my PDF files uploaded anywhere?"'
    assert t.count(marker) == 1
    t = t.replace(marker, ld_extra + marker, 1)
    faq_extra = (f'      <details class="faq-item">\n        <summary>{q1}</summary>\n        <p>{a1}</p>\n      </details>\n'
                 f'      <details class="faq-item">\n        <summary>{q2}</summary>\n        <p>{a2}</p>\n      </details>\n')
    fm = '      <details class="faq-item">\n        <summary>Are my PDF files uploaded anywhere?</summary>'
    assert t.count(fm) == 1
    t = t.replace(fm, faq_extra + fm, 1)
    return with_controls(t, p["kb"], p["slug"])


def main():
    base = open(BASE, encoding="utf-8").read()
    base = with_controls(base, 0, None)
    chips_note = '    <p class="note">Need a specific size? Pick a target below, or jump to <a href="compress-pdf-to-100kb.html">100 KB</a>, <a href="compress-pdf-to-200kb.html">200 KB</a>, <a href="compress-pdf-to-500kb.html">500 KB</a> or <a href="compress-pdf-for-email.html">the email-size preset</a>.</p>\n'
    base = re.sub(r'    <p class="note">(Compressing to email a PDF\?|Need a specific size\?).*?</p>\n', chips_note, base, count=1)
    open(BASE, "w", encoding="utf-8").write(base)
    clean = base
    for p in PRESETS:
        out = make_preset(clean, p)
        # the preset pages must not carry the "Need a specific size" note of the base
        out = re.sub(r'    <p class="note">Need a specific size\?.*?</p>\n', '', out)
        open(f"src/pdf/compress-pdf-to-{p['slug']}.html", "w", encoding="utf-8").write(out)
        print("wrote", f"src/pdf/compress-pdf-to-{p['slug']}.html")


if __name__ == "__main__":
    main()
