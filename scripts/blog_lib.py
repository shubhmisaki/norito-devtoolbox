#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Shared assembly function for translated src/<loc>/blog/<article>.html pages."""

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


def render_article(loc, slug, *, title, meta_desc, headline, breadcrumb_label,
                    byline_date_human, date_iso, lede, body_html):
    """
    slug: e.g. "pdf-compression-explained.html" (path relative to blog/, EN form)
    body_html: fully-assembled translated inner HTML from after the lede
        through (and including) the closing result-box, if present.
    """
    tool_path = f"blog/{slug}"
    meta = LOCALE_META.get(loc, {"lang": "en", "dir": "ltr"})
    canonical = _url(loc, tool_path)
    hreflang_lines = []
    for hl in ALL_LOCALES:
        hreflang_lines.append(f'<link rel="alternate" hreflang="{hl}" href="{_url(hl, tool_path)}" />')
    hreflang_lines.append(f'<link rel="alternate" hreflang="x-default" href="{_url("en", tool_path)}" />')
    hreflang_block = "\n".join(hreflang_lines)

    lang_attr = f'lang="{meta["lang"]}" dir="{meta["dir"]}"' if loc != "en" else 'lang="en"'
    og_locale_line = f'<meta property="og:locale" content="{meta.get("og_locale","")}" />\n' if loc != "en" else ""

    out = f'''<!DOCTYPE html>
<html {lang_attr}>
<head>
    <!--INCLUDE:HEAD-COMMON-->
<title>{title}</title>
<meta name="description" content="{meta_desc}" />
<link rel="canonical" href="{canonical}" />
{hreflang_block}
<meta property="og:type" content="article" />
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
<link rel="stylesheet" href="/css/style.css" />

<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Article",
  "headline": "{headline}",
  "description": "{meta_desc}",
  "url": "{canonical}",
  "datePublished": "{date_iso}",
  "dateModified": "{date_iso}",
  "author": {{ "@type": "Person", "name": "Shubham Singh" }},
  "publisher": {{ "@type": "Organization", "name": "norito", "url": "{_url(loc, "")}" }},
  "mainEntityOfPage": {{ "@type": "WebPage", "@id": "{canonical}" }}
}}
</script>
<script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4040839176833351" crossorigin="anonymous"></script>
</head>
<body>
<div class="bg-blobs" aria-hidden="true">
  <div class="blob blob-1"></div>
  <div class="blob blob-2"></div>
  <div class="blob blob-3"></div>
</div>

<!--INCLUDE:HEADER:content-->

<main>
  <div class="wrap legal-content">
    <p class="breadcrumb"><a href="../index.html">norito</a> / <a href="index.html">{breadcrumb_label_blog(loc)}</a> / {headline}</p>
    <h1>{headline}</h1>
    <p class="byline">{byline_by(loc)} Shubham Singh &middot; <time datetime="{date_iso}">{byline_date_human}</time></p>
    <p class="note" style="margin-bottom:4px;">{published_label(loc)} {date_iso}</p>
    <p class="lede">{lede}</p>

{body_html}
  </div>
</main>

<!--INCLUDE:FOOTER:standard-->

<!--INCLUDE:FOOT-SCRIPTS-MID-->
<!--INCLUDE:CMDK-OVERLAY-->

<!--INCLUDE:FOOT-SCRIPTS-TAIL-->
'''
    return out


_BLOG_LABEL = {
    "es": "Blog", "zh": "博客", "ar": "المدونة", "hi": "ब्लॉग", "ru": "Блог", "ja": "ブログ",
}
_BY_LABEL = {
    "es": "Por", "zh": "作者：", "ar": "بقلم", "hi": "लेखक", "ru": "Автор:", "ja": "著者：",
}
_PUBLISHED_LABEL = {
    "es": "Publicado el", "zh": "发布于", "ar": "نُشر في", "hi": "प्रकाशित", "ru": "Опубликовано", "ja": "公開日",
}

def breadcrumb_label_blog(loc):
    return _BLOG_LABEL.get(loc, "Blog")

def byline_by(loc):
    return _BY_LABEL.get(loc, "By")

def published_label(loc):
    return _PUBLISHED_LABEL.get(loc, "Published")
