#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Shared assembly function for generating a translated src/<loc>/<tool>.html
page from structured content, matching the exact skeleton pattern observed
in already-translated pages (src/es/seo-slug-generator.html etc.):

  - <html lang dir>
  - HEAD-COMMON include + translated title/meta/canonical/hreflang(all 7)/OG/
    twitter/og:locale
  - WebApplication JSON-LD (translated name/description, locale-prefixed
    url/isPartOf.url) -- NO FAQPage JSON-LD block (dropped on locale pages,
    matches established site pattern)
  - AdSense script (unchanged)
  - BreadcrumbList JSON-LD (translated name, locale-prefixed url)
  - bg-blobs, HEADER:standard include
  - tool-hero (translated breadcrumb/H1/lede), same icon/svg as EN
  - caller-supplied translated body HTML (panel(s) + explain-panel)
  - RELATED-TOOLS marker (translated label/desc, same hrefs)
  - FOOTER:standard include
  - i18n script tag (js/i18n/<loc>.js) + i18n-runtime.js + app-<tool>.js
  - FOOT-SCRIPTS-MID / CMDK-OVERLAY / FOOT-SCRIPTS-TAIL includes
"""

LOCALE_META = {
    "es": {"lang": "es", "dir": "ltr", "og_locale": "es_ES"},
    "zh": {"lang": "zh-Hans", "dir": "ltr", "og_locale": "zh_CN"},
    "ar": {"lang": "ar", "dir": "rtl", "og_locale": "ar_AR"},
    "hi": {"lang": "hi", "dir": "ltr", "og_locale": "hi_IN"},
    "ru": {"lang": "ru", "dir": "ltr", "og_locale": "ru_RU"},
    "ja": {"lang": "ja", "dir": "ltr", "og_locale": "ja_JP"},
}
ALL_LOCALES = ["en", "es", "zh", "ar", "hi", "ru", "ja"]


def _url(loc, path):
    prefix = "" if loc == "en" else f"/{loc}"
    return f"https://norito.in{prefix}/{path}"


def render_page(loc, tool_path, *, title, meta_desc, app_name,
                 icon_svg, icon_class, breadcrumb_label, h1, lede,
                 body_html, related_tools, footer_variant="standard",
                 header_variant="standard", i18n_scripts,
                 use_foot_scripts_head=False, extra_mid_script=""):
    """
    tool_path: e.g. "hash-generator.html" (path relative to site root, EN form)
    body_html: the fully-assembled, already-translated inner HTML for
        everything between the tool-hero close and the RELATED-TOOLS
        marker (the .two-col / panels / explain-panel etc.)
    related_tools: list of (href, label, desc) tuples
    i18n_scripts: list of <script> tag strings, in order, for the tool's
        own JS (e.g. ["js/app-hash.js"]) -- i18n-runtime.js and the
        js/i18n/<loc>.js loader are added automatically for non-en locales.
    """
    meta = LOCALE_META.get(loc, {"lang": "en", "dir": "ltr"})
    canonical = _url(loc, tool_path)
    hreflang_links = "\n".join(
        f'<link rel="alternate" hreflang="{"x-default" if hl=="en" else hl}" href="{_url(hl if hl!="x-default" else "en", tool_path)}" />'
        for hl in ["en"]
    )
    # build hreflang block: one per real locale + x-default (= en URL)
    hreflang_lines = []
    for hl in ALL_LOCALES:
        href = _url(hl, tool_path)
        hreflang_lines.append(f'<link rel="alternate" hreflang="{hl}" href="{href}" />')
    hreflang_lines.append(f'<link rel="alternate" hreflang="x-default" href="{_url("en", tool_path)}" />')
    hreflang_block = "\n".join(hreflang_lines)

    lang_attr = f'lang="{meta["lang"]}" dir="{meta["dir"]}"' if loc != "en" else 'lang="en"'
    og_locale_line = f'<meta property="og:locale" content="{meta.get("og_locale","")}" />\n' if loc != "en" else ""

    css_href = "/css/style.css" if loc == "en" else "/css/style.css"
    stylesheet_line = f'<link rel="stylesheet" href="{css_href}" />'

    site_url = _url(loc, "")
    header_include = f"<!--INCLUDE:HEADER:{header_variant}-->" if header_variant != "standard" else "<!--INCLUDE:HEADER:standard-->"
    footer_include = f"<!--INCLUDE:FOOTER:{footer_variant}-->" if footer_variant != "standard" else "<!--INCLUDE:FOOTER:standard-->"

    related_lines = "\n".join(f"{h}|{l}|{d}" for h, l, d in related_tools)

    js_prefix = "" if loc == "en" else "../"
    i18n_prefix = "" if loc == "en" else f'<script src="{js_prefix}js/i18n/{loc}.js"></script>\n'
    tool_scripts = "\n".join(f'<script src="{js_prefix}{s}"></script>' for s in i18n_scripts)
    # Always load utils.js: app-*.js files use its shared copyToClipboard()/
    # wireDragDrop() helpers, and a page missing it throws a ReferenceError
    # (uncaught for wireDragDrop, since it's called outside any try/catch --
    # this broke several already-shipped locale pages earlier in this same
    # session; loading it unconditionally here prevents repeating that).
    if use_foot_scripts_head:
        scripts_block = i18n_prefix + "<!--INCLUDE:FOOT-SCRIPTS-HEAD-->\n" + tool_scripts
    else:
        scripts_block = (
            i18n_prefix
            + f'<script src="{js_prefix}js/i18n-runtime.js"></script>\n'
            + f'<script src="{js_prefix}js/utils.js"></script>\n'
            + tool_scripts
        )

    breadcrumb_href = "index.html"

    out = f'''<!DOCTYPE html>
<html {lang_attr}>
<head>
    <!--INCLUDE:HEAD-COMMON-->
<title>{title}</title>
<meta name="description" content="{meta_desc}" />
<link rel="canonical" href="{canonical}" />
{hreflang_block}
<meta property="og:type" content="website" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{meta_desc}" />
<meta property="og:url" content="{canonical}" />
<meta property="og:site_name" content="norito" />
{og_locale_line}<meta property="og:image" content="https://norito.in/assets/og-image.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{title}" />
<meta name="twitter:description" content="{meta_desc}" />
<meta name="twitter:image" content="https://norito.in/assets/og-image.png" />
{stylesheet_line}

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "{app_name}",
  "url": "{canonical}",
  "description": "{meta_desc}",
  "applicationCategory": "UtilitiesApplication",
  "operatingSystem": "Any (runs in browser)",
  "offers": {{
    "@type": "Offer",
    "price": "0",
    "priceCurrency": "USD"
  }},
  "isPartOf": {{
    "@type": "WebSite",
    "name": "norito",
    "url": "{site_url}"
  }}
}}
</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4040839176833351" crossorigin="anonymous"></script>
<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
    {{
      "@type": "ListItem",
      "position": 1,
      "name": "norito",
      "item": "{site_url}"
    }},
    {{
      "@type": "ListItem",
      "position": 2,
      "name": "{app_name}",
      "item": "{canonical}"
    }}
  ]
}}
</script>
</head>
<body>
<div class="bg-blobs" aria-hidden="true">
  <div class="blob blob-1"></div>
  <div class="blob blob-2"></div>
  <div class="blob blob-3"></div>
</div>

{header_include}

<main>
  <div class="wrap">
    <div class="tool-hero">
    <div class="tool-hero-icon icon-chip {icon_class}">{icon_svg}</div>
    <div class="tool-hero-text">
    <p class="breadcrumb"><a href="{breadcrumb_href}">norito</a> / {breadcrumb_label}</p>
    <h1>{h1}</h1>
    <p class="lede">
      {lede}
    </p>
    </div>
  </div>

{body_html}

<!--RELATED-TOOLS
{related_lines}
-->
  </div>
</main>

{footer_include}

{scripts_block}
<!--INCLUDE:FOOT-SCRIPTS-MID-->
{extra_mid_script}<!--INCLUDE:CMDK-OVERLAY-->

<!--INCLUDE:FOOT-SCRIPTS-TAIL-->
'''
    return out
