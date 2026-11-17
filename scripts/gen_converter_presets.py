#!/usr/bin/env python3
"""Generates format-pair converter pages (PNG to JPG, WebP to PNG, ...)
from src/jpg-to-png-converter.html.

Each page is the real image converter with the output format locked, and
its own explanation and FAQ for that specific conversion (what is lost,
what the file size does, when it is the wrong choice). English only.

Run after editing the template page or the PAIRS table below:
    python3 scripts/gen_converter_presets.py && python3 scripts/build_site.py
"""
import json, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)

PRIVACY_FAQ = ("Is my image uploaded anywhere?",
               "No. The conversion runs entirely in your browser using the canvas API. Your image is never sent to a server, which you can confirm in the Network tab of your browser's developer tools.")

PAIRS = [
    dict(slug="png-to-jpg-converter", src="PNG", dst="JPG", fmt="jpeg",
         desc="Convert PNG to JPG in your browser. Transparent areas become white, quality is adjustable, and nothing is uploaded. Single files or batches.",
         lede="Convert PNG images to JPG for smaller files and universal compatibility. The output is already set to JPEG: drop in a PNG, adjust quality if you want, and download.",
         how=[
             "Your PNG is decoded into raw pixels and drawn onto a canvas at its full width and height, then encoded as JPEG at the quality you choose (92% by default). JPEG is a lossy format built for photographs, so screenshots of photos and scanned pictures typically shrink to a fraction of their PNG size with no visible difference.",
             "JPEG has no transparency. Any transparent or semi-transparent area in the PNG is flattened onto a white background before encoding, so logos and cut-outs come out on white rather than black. If you need to keep transparency, convert to WebP instead, which supports it at a much smaller size than PNG.",
             "JPEG is the wrong target for sharp-edged graphics. Text, line art, UI screenshots and flat-colour logos pick up faint halos around edges at lower qualities. For those, keep the PNG, or raise the quality slider towards 100% and compare.",
         ],
         faq=[
             ("What happens to transparent areas?", "They are filled with white, because the JPEG format cannot store transparency. If you need a transparent background, convert to WebP or keep the PNG."),
             ("Will the JPG be smaller than the PNG?", "For photos and photo-like images, almost always, often by 70 to 90 percent. For flat graphics with few colours, PNG can already be very small and the JPG may not be smaller."),
             ("Which quality setting should I use?", "The default of 92% is visually indistinguishable from the original for most images. Lower it to around 80% for web use if file size matters more."),
         ]),
    dict(slug="webp-to-jpg-converter", src="WebP", dst="JPG", fmt="jpeg",
         desc="Convert WebP to JPG so it opens anywhere. Runs in your browser with adjustable quality and batch support, and your images are never uploaded.",
         lede="Saved an image from the web and got a .webp that an app or upload form refuses? Convert it to JPG, which opens everywhere. The output is already set to JPEG.",
         how=[
             "WebP is what most websites now serve, but plenty of software still does not accept it: older image editors, some document tools, and many upload forms. This page decodes the WebP with your browser's built-in decoder, draws it onto a canvas at full size and re-encodes it as JPEG at the quality you choose.",
             "Both formats are lossy, so converting adds a second round of compression. At the default 92% quality the extra loss is not visible in normal viewing. Expect the JPG to be somewhat larger than the WebP it came from: that is WebP's efficiency being given up, not a fault in the conversion.",
             "Two limits worth knowing. Transparent areas are flattened onto white, since JPEG cannot store transparency. And an animated WebP is converted as a single still image of its first frame, because JPEG has no animation.",
         ],
         faq=[
             ("Why won't my WebP image open or upload?", "WebP is newer than JPG and PNG, and some apps, older operating systems and upload forms do not support it. Converting to JPG gives you a file that works everywhere."),
             ("Does converting WebP to JPG lose quality?", "Slightly, because the image is compressed again. At the default 92% quality the difference is not noticeable in normal use."),
             ("What about transparent or animated WebP files?", "Transparency is replaced with a white background, and animated WebP files are converted as a still image of the first frame. To keep transparency, convert to PNG instead."),
         ]),
    dict(slug="webp-to-png-converter", src="WebP", dst="PNG", fmt="png",
         desc="Convert WebP to PNG in your browser, keeping transparency. Lossless output, batch support, and nothing is uploaded to a server.",
         lede="Convert WebP images to PNG when you need a format every editor accepts, with transparency preserved. The output is already set to PNG.",
         how=[
             "Your browser decodes the WebP into pixels, the pixels are drawn onto a canvas at the image's full size, and the canvas is written out as a PNG. PNG is lossless, so the result stores exactly what the WebP decoded to: no further quality is lost in this direction, which makes PNG the right choice when you plan to edit the image.",
             "Transparency survives. A WebP with a transparent background becomes a PNG with the same transparent background, which is the main reason to choose PNG over JPG here.",
             "The PNG will usually be considerably larger than the WebP, especially for photographs, because lossless storage cannot match WebP's compression. Converting also cannot restore detail that was removed when the WebP was created. Animated WebP files are converted as a still image of the first frame.",
         ],
         faq=[
             ("Does WebP to PNG keep the transparent background?", "Yes. PNG supports full transparency, so transparent areas in the WebP stay transparent in the PNG."),
             ("Why is the PNG so much bigger than the WebP?", "PNG is lossless and WebP is usually lossy. Storing every pixel exactly takes more space, particularly for photos. If size matters, keep the WebP or convert to JPG."),
             ("Will the PNG be better quality than the WebP?", "No. It will be identical to what the WebP showed. Converting to a lossless format prevents further loss but cannot recover detail already removed."),
         ]),
    dict(slug="jpg-to-webp-converter", src="JPG", dst="WebP", fmt="webp",
         desc="Convert JPG to WebP to make images smaller for the web. Adjustable quality, batch conversion, all in your browser with no upload.",
         lede="Convert JPG photos to WebP to cut page weight without visible quality loss. The output is already set to WebP: drop in your images and download.",
         how=[
             "WebP typically produces files 25 to 35 percent smaller than JPEG at the same visual quality, and every current browser displays it. This page decodes your JPG, draws it onto a canvas at full size and encodes it as WebP using your browser's own encoder at the quality you choose.",
             "Because the JPG was already compressed once, very high WebP quality settings mostly preserve the JPG's existing artefacts at extra cost. Around 75 to 85% is the useful range for web images: try 80%, compare the preview, and adjust. For the best possible result, convert from the original, uncompressed source rather than from a JPG when you have it.",
             "Use WebP for images on websites and in apps. Keep a JPG copy for anything that must open in older software, be attached to documents, or be sent to a print service, since WebP support outside browsers is still uneven.",
         ],
         faq=[
             ("How much smaller is WebP than JPG?", "Typically 25 to 35 percent smaller at similar visual quality. The exact saving depends on the image and the quality setting."),
             ("Do all browsers support WebP?", "Yes. Chrome, Safari, Firefox and Edge have all supported WebP for years. Support in desktop software and older systems is less consistent."),
             ("Which quality setting should I pick?", "Start at 80%. It is usually indistinguishable from the JPG while being clearly smaller. Go lower for thumbnails, higher for detailed product photos."),
         ]),
    dict(slug="png-to-webp-converter", src="PNG", dst="WebP", fmt="webp",
         desc="Convert PNG to WebP and keep transparency at a fraction of the size. Adjustable quality and batch conversion, in your browser with no upload.",
         lede="Convert PNG images to WebP to keep transparency at a fraction of the file size. The output is already set to WebP.",
         how=[
             "PNG is lossless, which makes it large, particularly for screenshots with gradients, illustrations and anything photographic. WebP supports the same full transparency but compresses far more aggressively, so a transparent PNG often drops by 60 to 80 percent when converted.",
             "Your PNG is decoded, drawn onto a canvas at full size with its alpha channel intact, and encoded as WebP at the quality you choose. Transparent areas stay transparent. The encoding is lossy, so at lower qualities fine text and hard edges can soften slightly: check the preview at 100% zoom if the image contains small type.",
             "WebP is the better format for delivering images on a website. Keep the original PNG as your master copy for editing, since repeated lossy saves degrade an image over time.",
         ],
         faq=[
             ("Does PNG to WebP keep transparency?", "Yes. WebP supports an alpha channel, so transparent backgrounds are preserved."),
             ("How much smaller will the WebP be?", "Commonly 60 to 80 percent smaller than the PNG for illustrations, screenshots and photos. Very simple graphics with few colours may see a smaller saving."),
             ("Is the conversion lossless?", "No. This converter uses lossy WebP with a quality slider. At high quality settings the difference is not visible, but keep your PNG if you need a pixel-exact copy."),
         ]),
]

BASE = "src/jpg-to-png-converter.html"
NAV_RE = re.compile(r'    <nav class="size-chips".*?</nav>\n', re.S)

ALL_PAGES = [("jpg-to-png-converter", "JPG to PNG")] + [(p["slug"], f'{p["src"]} to {p["dst"]}') for p in PAIRS]


def pairs_nav(current):
    links = []
    for slug, label in ALL_PAGES:
        if slug == current:
            links.append(f'<span class="size-chip current" aria-current="page">{label}</span>')
        else:
            links.append(f'<a class="size-chip" href="{slug}.html">{label}</a>')
    if current == "image-converter":
        links.append('<span class="size-chip current" aria-current="page">Any format</span>')
    else:
        links.append('<a class="size-chip" href="image-converter.html">Any format</a>')
    return ('    <nav class="size-chips" aria-label="Popular conversions">\n      <span class="size-chips-label">Popular conversions</span>\n      '
            + "\n      ".join(links) + "\n    </nav>\n")


def faq_ld(items):
    data = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}}
            for q, a in items
        ],
    }
    return '<script type="application/ld+json">\n' + json.dumps(data, indent=2, ensure_ascii=False) + "\n</script>"


def with_nav(text, current):
    text = NAV_RE.sub("", text)
    anchor = '    <div class="two-col">'
    assert text.count(anchor) == 1, "two-col anchor moved"
    return text.replace(anchor, pairs_nav(current) + anchor)


def main():
    base = NAV_RE.sub("", open(BASE, encoding="utf-8").read())
    for p in PAIRS:
        name = f'{p["src"]} to {p["dst"]} Converter'
        items = p["faq"] + [PRIVACY_FAQ]
        s = base
        s = s.replace("JPG to PNG Converter, Free &amp; Online", f"{name}, Free &amp; Online")
        s = s.replace("JPG to PNG Converter, Free & Online", f"{name}, Free & Online")
        s = s.replace("Convert a JPG or JPEG photo to PNG, right in your browser. Lossless output, nothing is uploaded to a server.", p["desc"])
        s = s.replace("Convert a JPG or JPEG photo to PNG, right in your browser. Lossless output, nothing is uploaded.", p["desc"])
        s = s.replace("jpg-to-png-converter.html", p["slug"] + ".html")
        s = s.replace("JPG to PNG Converter", name)
        s = re.sub(r'(<p class="lede">).*?(</p>)', lambda m: m.group(1) + "\n      " + p["lede"] + "\n    " + m.group(2), s, count=1, flags=re.S)
        # lock the output format
        s = s.replace('<option value="png" selected>PNG</option>', '<option value="png">PNG</option>')
        s = s.replace(f'<option value="{p["fmt"]}">', f'<option value="{p["fmt"]}" selected>')
        assert s.count(" selected>") == 1, p["slug"]
        # explanation
        how = ('    <div class="explain-panel">\n      <h2>How it works</h2>\n'
               + "".join(f"      <p>\n        {para}\n      </p>\n" for para in p["how"]) + "    </div>\n")
        s, n = re.subn(r'    <div class="explain-panel">\n      <h2>How it works</h2>.*?\n    </div>\n', lambda m: how, s, count=1, flags=re.S)
        assert n == 1, "explain panel not found"
        # visible FAQ + matching structured data
        faq_html = ('    <div class="faq-list">\n'
                    + "".join(f'      <details class="faq-item">\n        <summary>{q}</summary>\n        <p>{a}</p>\n      </details>\n' for q, a in items)
                    + "    </div>\n")
        s, n = re.subn(r'    <div class="faq-list">.*?\n    </div>\n', lambda m: faq_html, s, count=1, flags=re.S)
        assert n == 1, "faq list not found"
        s, n = re.subn(r'<script type="application/ld\+json">\s*\{\s*"@context": "https://schema.org",\s*"@type": "FAQPage".*?</script>', lambda m: faq_ld(items), s, count=1, flags=re.S)
        assert n == 1, "faq json-ld not found"
        s = with_nav(s, p["slug"])
        open(f'src/{p["slug"]}.html', "w", encoding="utf-8").write(s)
        print("wrote", f'src/{p["slug"]}.html')
    # cross-link from the template page and the general converter
    template = with_nav(base, "jpg-to-png-converter")
    open(BASE, "w", encoding="utf-8").write(template)
    gen = "src/image-converter.html"
    general = with_nav(open(gen, encoding="utf-8").read(), "image-converter")
    open(gen, "w", encoding="utf-8").write(general)


if __name__ == "__main__":
    main()
