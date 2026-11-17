#!/usr/bin/env python3
"""Generates the "compress image to N KB" preset pages from src/compress-image.html.

Each page is the real compressor with the target size already filled in,
plus a section written for that specific size (what it is typically needed
for, what dimensions survive at that size, how to get a clean result).
English only: hreflang is generated from which files exist, so no locale
alternates are advertised for these.

Run after editing src/compress-image.html or the PRESETS table below:
    python3 scripts/gen_compress_presets.py && python3 scripts/build_site.py
"""
import os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

PRESETS = [
    dict(slug="20kb", n="20", unit="KB", label="20 KB",
         desc="Compress a photo or signature to under 20 KB for online forms. Set once, drop the image, download. Runs in your browser, nothing is uploaded.",
         lede="Signature scans and thumbnail photos for online forms often have to be under 20 KB. The target is already set: drop your image and download the result.",
         h2="Getting a clean image under 20 KB",
         body=[
             "20 KB is a very small budget. It is the usual ceiling for signature scans and small ID thumbnails on application portals, and it is tight enough that a full-resolution phone photo cannot fit without being scaled down. Leave <strong>Allow resizing</strong> on: the tool first tries your original dimensions, and only shrinks the image when no quality setting fits.",
             "For a signature, crop tightly around the ink before compressing. White paper compresses almost for free, so a tight crop spends the whole budget on the strokes, and a 300 to 400 pixel wide signature stays crisp at 20 KB. For a face photo, expect roughly 250 to 350 pixels on the long side to look clean; beyond that, JPEG blocking starts to show around hair and edges.",
             "Use JPEG output. PNG is lossless, so its size depends on the content and it will usually overshoot a 20 KB limit for photos. If the form states exact pixel dimensions as well as a size limit, resize to those dimensions first with <a href=\"resize-image.html\">Resize Image</a>, then compress here.",
         ]),
    dict(slug="50kb", n="50", unit="KB", label="50 KB",
         desc="Compress a photo to under 50 KB for application forms and portals. The best quality that fits is found automatically, in your browser, with no upload.",
         lede="Passport-style photos for exam, job and government portals are commonly capped at 50 KB. The target is already set: drop your photo and download a version that fits.",
         h2="What fits in 50 KB",
         body=[
             "50 KB is the most common limit for a passport-style photo on online application forms. At this size a portrait of about 400 to 600 pixels on the long side still looks sharp, which is larger than most forms actually display it.",
             "The tool keeps your original width and height when it can. A 12-megapixel phone photo cannot reach 50 KB at full resolution, so with <strong>Allow resizing</strong> on it steps the dimensions down just far enough to fit, then picks the highest JPEG quality under the limit. You get the largest, cleanest image the budget allows instead of a guess.",
             "Two things help more than any setting: crop to head and shoulders before compressing, and use a plain, evenly lit background. Flat backgrounds cost very few bytes, leaving more of the 50 KB for the face. Always check the form's own notice for its exact limits, since some ask for a minimum size as well as a maximum.",
         ]),
    dict(slug="100kb", n="100", unit="KB", label="100 KB",
         desc="Compress an image to under 100 KB without guessing a quality setting. JPG, PNG and WebP, single or in bulk, entirely in your browser.",
         lede="100 KB is the upload limit you meet most often: document portals, job sites, profile photos. The target is already set, so drop your image and download one that fits.",
         h2="What 100 KB gets you",
         body=[
             "100 KB is enough for a clean photo of roughly 1000 to 1200 pixels on the long side, or a readable scan of a single-page document. It is the usual cap for profile pictures, ID uploads and attachments on job and admission portals.",
             "Instead of a quality slider, the tool searches for the highest quality that lands under 100 KB. If the image is too large for any quality setting to fit, and <strong>Allow resizing</strong> is on, it reduces the dimensions step by step until one does. The result line shows the final size and dimensions so you can confirm it before downloading.",
             "For scanned documents with text, keep the output as JPEG and avoid shrinking more than you need: small text is the first thing to become unreadable. If you have several files with the same limit, select them all at once and download the results as a single zip.",
         ]),
    dict(slug="200kb", n="200", unit="KB", label="200 KB",
         desc="Compress an image to under 200 KB for uploads, scans and web pages. Finds the best quality that fits. Private: your file never leaves your device.",
         lede="A 200 KB limit is typical for document scans, certificates and blog images. The target is already set: drop your image and download a version that fits.",
         h2="When 200 KB is the right target",
         body=[
             "200 KB comfortably holds a photo of about 1600 pixels on the long side at good quality, or an A4 document scan whose text is still easy to read. Portals that accept certificates, mark sheets and ID proofs often set their limit here.",
             "It is also a sensible budget for images inside a web page or blog post: large enough to look sharp on a laptop screen, small enough not to slow the page down. If the image is for the web, try WebP output, which usually gives visibly better quality than JPEG at the same 200 KB.",
             "Because everything runs in your browser, scans of personal documents are never sent to a server. You can confirm it yourself by opening the Network tab in your browser's developer tools while you compress.",
         ]),
    dict(slug="500kb", n="500", unit="KB", label="500 KB",
         desc="Compress an image to under 500 KB while keeping it sharp at full-screen size. JPG, PNG or WebP, in bulk if you need, with no upload.",
         lede="500 KB keeps a photo sharp at full-screen size while meeting most upload limits. The target is already set: drop your image and download the result.",
         h2="What 500 KB is good for",
         body=[
             "At 500 KB a photo of 2000 to 2500 pixels on the long side still looks clean, which is enough for a full-width website banner, a slide in a presentation, or a product photo that customers can zoom into.",
             "Learning platforms, form builders and content management systems often cap uploads at 500 KB. Most phone photos start between 2 and 6 MB, so this target usually means a mild quality reduction and little or no resizing. The tool tries your original dimensions first and only scales down if it must.",
             "If you are preparing many images for the same page, select them together: each one is compressed to the same 500 KB target and you can download the whole set as a zip.",
         ]),
    dict(slug="1mb", n="1", unit="MB", label="1 MB",
         desc="Compress an image to under 1 MB for email and upload limits, keeping as much resolution as possible. Works in your browser with no upload.",
         lede="A 1 MB cap is common for email attachments and upload forms. The target is already set: drop your photo and keep nearly all of its resolution.",
         h2="Fitting a photo into 1 MB",
         body=[
             "A modern phone photo is typically 3 to 8 MB. Bringing it under 1 MB rarely needs any resizing: a 12-megapixel image usually fits at a JPEG quality where the difference from the original is hard to see without zooming in.",
             "1 MB is the size to aim for when you are emailing several photos, uploading to a form with a per-file limit, or attaching images to a support ticket. Select all your photos at once to compress them to the same limit and download a single zip.",
             "If the result still shows visible artefacts, the image probably has a lot of fine detail such as foliage or fabric. Turning on <strong>Allow resizing</strong> lets the tool trade a little resolution for cleaner detail, which usually looks better than heavy compression at full size.",
         ]),
]

BASE_TITLE = "Compress Image to Exact Size (100KB, 200KB, 1MB...)"
BASE_DESC = "Compress an image to a target file size, like 100KB, 200KB, 500KB, or 1MB, instead of fiddling with a quality slider. Runs entirely in your browser."


def sizes_nav(current=None):
    links = []
    for p in PRESETS:
        if p["slug"] == current:
            links.append(f'<span class="size-chip current" aria-current="page">{p["label"]}</span>')
        else:
            links.append(f'<a class="size-chip" href="compress-image-to-{p["slug"]}.html">{p["label"]}</a>')
    any_link = '<a class="size-chip" href="compress-image.html">Any size</a>' if current else '<span class="size-chip current" aria-current="page">Any size</span>'
    return ('    <nav class="size-chips" aria-label="Common target sizes">\n      <span class="size-chips-label">Common sizes</span>\n      '
            + "\n      ".join(links + [any_link]) + "\n    </nav>\n")


NAV_RE = re.compile(r'    <nav class="size-chips".*?</nav>\n', re.S)


def main():
    base_path = "src/compress-image.html"
    base = open(base_path, encoding="utf-8").read()
    base = NAV_RE.sub("", base)
    anchor = '    <div class="two-col">'
    assert base.count(anchor) == 1, "two-col anchor moved"
    for p in PRESETS:
        slug = f'compress-image-to-{p["slug"]}'
        title = f'Compress Image to {p["label"]} Online, Free | norito'.replace(" | norito", "")
        s = base
        s = s.replace(BASE_TITLE, title)
        s = s.replace(BASE_DESC, p["desc"])
        s = s.replace("https://norito.in/compress-image.html", f"https://norito.in/{slug}.html")
        s = s.replace('"name": "Compress to Size"', f'"name": "Compress to {p["label"]}"')
        s = s.replace('/ Compress to Size</p>', f'/ <a href="compress-image.html">Compress to Size</a> / {p["label"]}</p>')
        s = s.replace("<h1>Compress Image to a Target Size</h1>", f'<h1>Compress Image to {p["label"]}</h1>')
        s = re.sub(r'(<p class="lede">).*?(</p>)', lambda m: m.group(1) + "\n      " + p["lede"] + "\n    " + m.group(2), s, count=1, flags=re.S)
        s = s.replace('<input type="number" id="targetSize" value="100" min="0" step="any" />',
                      f'<input type="number" id="targetSize" value="{p["n"]}" min="0" step="any" data-preset="{p["slug"]}" />')
        if p["unit"] == "MB":
            s = s.replace('<option value="KB" selected>KB</option>', '<option value="KB">KB</option>')
            s = s.replace('<option value="MB">MB</option>', '<option value="MB" selected>MB</option>')
        section = ('    <div class="explain-panel">\n      <h2>' + p["h2"] + "</h2>\n"
                   + "".join(f"      <p>{para}</p>\n" for para in p["body"]) + "    </div>\n")
        how = '    <div class="explain-panel">\n      <h2>How it works</h2>'
        assert s.count(how) == 1, "how-it-works anchor moved"
        s = s.replace(how, section + how)
        s = s.replace(anchor, sizes_nav(p["slug"]) + anchor)
        assert "data-preset" in s and title in s and p["desc"] in s
        open(f"src/{slug}.html", "w", encoding="utf-8").write(s)
        print("wrote", f"src/{slug}.html")
    base = base.replace(anchor, sizes_nav(None) + anchor)
    open(base_path, "w", encoding="utf-8").write(base)


if __name__ == "__main__":
    main()
