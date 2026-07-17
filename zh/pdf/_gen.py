#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generator script for zh/pdf/*.html - run once, then delete."""
import re, json, os

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(BASE))  # repo root

with open("/tmp/navblock.txt", encoding="utf-8") as f:
    NAV_RAW = f.read().rstrip("\n")
with open("/tmp/footerblock.txt", encoding="utf-8") as f:
    FOOTER_RAW = f.read().rstrip("\n")
with open("/tmp/langswitch.txt", encoding="utf-8") as f:
    LANGSWITCH = f.read().rstrip("\n")

# Fix nav hrefs for the 4 already-translated zh groups (Images/Dev/Text/Utilities)
# zh/pdf/ is one level deeper than zh/, so bare same-dir hrefs need a "../" prefix.
ZH_LOCAL_FILES = [
    "compress-image.html", "placeholder-generator.html", "remove-background.html",
    "test-file-generator.html", "json-formatter.html", "markdown-editor.html",
    "seo-slug-generator.html", "limited-text-generator.html",
    "password-generator.html", "qr-code-generator.html",
]
NAV = NAV_RAW
for fn in ZH_LOCAL_FILES:
    NAV = NAV.replace('href="%s"' % fn, 'href="../%s"' % fn)

LANG_SWITCHER_SCRIPT = '<script src="../../js/lang-switcher.js"></script>'

# PDF tool Chinese names (consistent across breadcrumb/h1/title/footer/json-ld)
PDF_NAMES_ZH = {
    "index.html": "PDF 工具",
    "merge-pdf.html": "合并 PDF",
    "split-pdf.html": "拆分 PDF",
    "rotate-pdf.html": "旋转 PDF",
    "pdf-to-image.html": "PDF 转 JPG/PNG",
    "jpg-png-to-pdf.html": "JPG/PNG 转 PDF",
    "organize-pdf.html": "删除与重排页面",
    "add-page-numbers.html": "添加页码",
    "add-watermark.html": "添加水印",
    "extract-text.html": "提取文本",
    "compress-pdf.html": "压缩 PDF",
    "compress-pdf-for-email.html": "压缩 PDF 以便邮件发送",
    "sign-pdf.html": "为 PDF 签名",
}

FOOTER_PDF_LINKS = """\
            <div class="footer-col">
        <h3>PDF</h3>
        <a href="merge-pdf.html">合并 PDF</a>
        <a href="split-pdf.html">拆分 PDF</a>
        <a href="rotate-pdf.html">旋转 PDF</a>
        <a href="pdf-to-image.html">PDF 转 JPG/PNG</a>
        <a href="jpg-png-to-pdf.html">JPG/PNG 转 PDF</a>
        <a href="organize-pdf.html">删除与重排</a>
        <a href="add-page-numbers.html">添加页码</a>
        <a href="add-watermark.html">添加水印</a>
        <a href="extract-text.html">提取文本</a>
        <a href="compress-pdf.html">压缩 PDF</a>
        <a href="sign-pdf.html">为 PDF 签名</a>
      </div>"""

# Build footer: brand + PDF column + Images column + Text&Dev column (paths fixed with ../) + bottom
def build_footer():
    lines = FOOTER_RAW.split("\n")
    out = []
    for ln in lines:
        # fix hrefs in 图像/文本与开发 columns (bare filenames -> ../filename)
        nl = ln
        for fn in ZH_LOCAL_FILES:
            nl = nl.replace('href="%s"' % fn, 'href="../%s"' % fn)
        nl = nl.replace('href="privacy.html"', 'href="../privacy.html"')
        nl = nl.replace('href="../blog/"', 'href="../../blog/"')
        nl = nl.replace('href="../compare/"', 'href="../../compare/"')
        nl = nl.replace('href="../how-it-works.html"', 'href="../../how-it-works.html"')
        out.append(nl)
    footer_fixed = "\n".join(out)
    # insert PDF column right after footer-brand closing div
    marker = '      </div>\n      <div class="footer-col">\n        <h3>图像</h3>'
    assert marker in footer_fixed, "marker not found in footer"
    footer_fixed = footer_fixed.replace(marker, "      </div>\n" + FOOTER_PDF_LINKS + "\n      <div class=\"footer-col\">\n        <h3>图像</h3>", 1)
    return footer_fixed

FOOTER = build_footer()

HEAD_TOP_TMPL = """<!DOCTYPE html>
<html lang="zh-Hans" dir="ltr">
<head>
<meta charset="UTF-8" />
<script>(function(){{try{{var t=localStorage.getItem("norito:theme");if(t==="dark"){{document.documentElement.setAttribute("data-theme","dark");}}}}catch(e){{}}}})();</script>
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<link rel="icon" type="image/svg+xml" href="../../assets/norito-mark.svg" />
<link rel="alternate icon" href="../../favicon.ico" />
<link rel="apple-touch-icon" href="../../assets/apple-touch-icon.png" />
<link rel="manifest" href="/manifest.json" />
<meta name="theme-color" content="#ff4d7a" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@600;700;800&display=optional" />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@600;700;800&display=optional" rel="stylesheet" media="print" onload="this.media='all'" />
<noscript><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@600;700;800&display=optional" rel="stylesheet" /></noscript>
{extra_fonts}<title>{title}</title>
<meta name="description" content="{desc}" />
<link rel="canonical" href="{canon}" />
<link rel="alternate" hreflang="en" href="{en_url}" />
<link rel="alternate" hreflang="es" href="{es_url}" />
<link rel="alternate" hreflang="zh" href="{zh_url}" />
<link rel="alternate" hreflang="ar" href="{ar_url}" />
<link rel="alternate" hreflang="hi" href="{hi_url}" />
<link rel="alternate" hreflang="ru" href="{ru_url}" />
<link rel="alternate" hreflang="ja" href="{ja_url}" />
<link rel="alternate" hreflang="x-default" href="{en_url}" />
<meta property="og:type" content="website" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{og_desc}" />
<meta property="og:url" content="{zh_url}" />
<meta property="og:site_name" content="norito" />
<meta property="og:locale" content="zh_CN" />
<meta property="og:image" content="https://norito.in/assets/og-image.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{title}" />
<meta name="twitter:description" content="{og_desc}" />
<meta name="twitter:image" content="https://norito.in/assets/og-image.png" />
<link rel="stylesheet" href="../../css/style.css" />

{jsonld}<!-- AdSense temporarily disabled while investigating a Search Console "possible phishing" security flag. To restore, remove this comment wrapper. -->
<!-- <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4040839176833351" crossorigin="anonymous"></script> -->
</head>
<body>
<div class="bg-blobs" aria-hidden="true">
  <div class="blob blob-1"></div>
  <div class="blob blob-2"></div>
  <div class="blob blob-3"></div>
</div>

<header class="site">
  <div class="wrap">
    <a class="brand" href="../index.html"><img class="logo logo-word" src="../../assets/norito-wordmark.svg" alt="norito" width="113" height="44" /></a>
    {nav}
      <button type="button" class="search-trigger" id="searchTrigger" aria-label="搜索工具" title="搜索工具"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg></button>

      <button type="button" class="theme-toggle-btn" aria-label="Toggle dark mode">
        <svg class="theme-icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9"/></svg>
        <svg class="theme-icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>
      </button>

{langswitch}
  </div>
</header>

"""

TAIL_TMPL = """
<footer class="site">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        <div class="footer-brand-name">norito</div>
        <p class="footer-tagline">小而专注的工具，每个只做一件事。全部在你的浏览器中运行，不会上传任何内容。</p>
      </div>
{footer_rest}
    </div>
    <div class="footer-bottom">
      <span>&copy; 2026 norito。所有工具均在本地浏览器中运行。</span>
      <a href="../privacy.html">隐私政策</a>
            <a href="../../blog/">Blog</a>
            <a href="../../compare/">Compare</a>
            <a href="../../how-it-works.html">How it Works</a>
      <a href="https://ko-fi.com/shubhmisaki" target="_blank" rel="noopener">请我喝杯咖啡</a>
    </div>
  </div>
</footer>

{scripts}
<div class="cmdk-overlay" id="cmdkOverlay" hidden data-empty-text="没有匹配的工具。">
  <div class="cmdk-modal" role="dialog" aria-modal="true" aria-label="搜索工具">
    <div class="cmdk-input-row">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>
      <input type="text" id="cmdkInput" placeholder="搜索工具..." autocomplete="off" />
      <kbd>Esc</kbd>
    </div>
    <div class="cmdk-results" id="cmdkResults"></div>
  </div>
</div>

<script src="../../js/cmdk.js"></script>
<script src="/js/sw-register.js" defer></script>
{install_prompt}</body>
</html>
"""

def hreflang_urls(slug):
    # slug like "merge-pdf.html" or "" for index
    return {
        "en_url": "https://norito.in/pdf/%s" % slug,
        "es_url": "https://norito.in/es/pdf/%s" % slug,
        "zh_url": "https://norito.in/zh/pdf/%s" % slug,
        "ar_url": "https://norito.in/ar/pdf/%s" % slug,
        "hi_url": "https://norito.in/hi/pdf/%s" % slug,
        "ru_url": "https://norito.in/ru/pdf/%s" % slug,
        "ja_url": "https://norito.in/ja/pdf/%s" % slug,
    }

def make_footer_rest():
    # Pull just the two already-translated columns (图像 / 文本与开发) straight from the
    # raw zh/compress-image.html footer block, fix their hrefs for the extra depth, and
    # prepend our new PDF column (already using same-dir sibling hrefs).
    start = FOOTER_RAW.index('      <div class="footer-col">\n        <h3>图像</h3>')
    end = FOOTER_RAW.index('    </div>\n    <div class="footer-bottom">')
    two_cols = FOOTER_RAW[start:end]
    for fn in ZH_LOCAL_FILES:
        two_cols = two_cols.replace('href="%s"' % fn, 'href="../%s"' % fn)
    return FOOTER_PDF_LINKS + "\n" + two_cols.rstrip("\n")

FOOTER_REST = make_footer_rest()

def render_head_nav():
    return NAV

def build(slug, title, desc, og_desc, jsonld_str, main_html, scripts_list, extra_fonts="", install_prompt=True):
    urls = hreflang_urls(slug)
    canon = urls["zh_url"]
    head = HEAD_TOP_TMPL.format(
        extra_fonts=extra_fonts,
        title=title, desc=desc, og_desc=og_desc,
        canon=canon, jsonld=jsonld_str,
        nav=render_head_nav(),
        langswitch=LANGSWITCH,
        **urls
    )
    scripts_html = "\n".join(scripts_list)
    tail = TAIL_TMPL.format(
        footer_rest=FOOTER_REST,
        scripts=scripts_html,
        install_prompt=('<script src="/js/install-prompt.js" defer></script>\n' if install_prompt else "")
    )
    return head + main_html + "\n" + tail

print("helper module ready")
