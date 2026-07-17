# -*- coding: utf-8 -*-
import os

BASE = "/sessions/happy-keen-sagan/mnt/norito/ru/pdf"

HEAD_TOP = '''<!DOCTYPE html>
<html lang="ru" dir="ltr">
<head>
<meta charset="UTF-8" />
<script>(function(){try{var t=localStorage.getItem("norito:theme");if(t==="dark"){document.documentElement.setAttribute("data-theme","dark");}}catch(e){}})();</script>
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<link rel="icon" type="image/svg+xml" href="/assets/norito-mark.svg" />
<link rel="alternate icon" href="/favicon.ico" />
<link rel="apple-touch-icon" href="/assets/apple-touch-icon.png" />
<link rel="manifest" href="/manifest.json" />
<meta name="theme-color" content="#ff4d7a" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@600;700;800&display=optional" />
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@600;700;800&display=optional" rel="stylesheet" media="print" onload="this.media='all'" />
<noscript><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@600;700;800&display=optional" rel="stylesheet" /></noscript>'''

SIGN_FONTS = '''
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Nothing+You+Could+Do&family=La+Belle+Aurore&family=Reenie+Beanie&family=Homemade+Apple&family=Kristi&display=optional" />
<link href="https://fonts.googleapis.com/css2?family=Nothing+You+Could+Do&family=La+Belle+Aurore&family=Reenie+Beanie&family=Homemade+Apple&family=Kristi&display=optional" rel="stylesheet" media="print" onload="this.media='all'" />
<noscript><link href="https://fonts.googleapis.com/css2?family=Nothing+You+Could+Do&family=La+Belle+Aurore&family=Reenie+Beanie&family=Homemade+Apple&family=Kristi&display=optional" rel="stylesheet" /></noscript>'''

def head_meta(slug, title, desc, og_desc=None):
    # slug: '' for index (directory-style), else 'X.html'
    if slug == '':
        en_url = "https://norito.in/pdf/"
        ru_url = "https://norito.in/ru/pdf/"
        es_url = "https://norito.in/es/pdf/"
        zh_url = "https://norito.in/zh/pdf/"
        ar_url = "https://norito.in/ar/pdf/"
        hi_url = "https://norito.in/hi/pdf/"
        ja_url = "https://norito.in/ja/pdf/"
        xd_url = "https://norito.in/pdf/"
    else:
        en_url = f"https://norito.in/pdf/{slug}"
        ru_url = f"https://norito.in/ru/pdf/{slug}"
        es_url = f"https://norito.in/es/pdf/{slug}"
        zh_url = f"https://norito.in/zh/pdf/{slug}"
        ar_url = f"https://norito.in/ar/pdf/{slug}"
        hi_url = f"https://norito.in/hi/pdf/{slug}"
        ja_url = f"https://norito.in/ja/pdf/{slug}"
        xd_url = en_url
    ogd = og_desc if og_desc else desc
    return f'''
<title>{title}</title>
<meta name="description" content="{desc}" />
<link rel="canonical" href="{ru_url}" />
<link rel="alternate" hreflang="en" href="{en_url}" />
<link rel="alternate" hreflang="es" href="{es_url}" />
<link rel="alternate" hreflang="zh" href="{zh_url}" />
<link rel="alternate" hreflang="ar" href="{ar_url}" />
<link rel="alternate" hreflang="hi" href="{hi_url}" />
<link rel="alternate" hreflang="ru" href="{ru_url}" />
<link rel="alternate" hreflang="ja" href="{ja_url}" />
<link rel="alternate" hreflang="x-default" href="{xd_url}" />
<meta property="og:type" content="website" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{ogd}" />
<meta property="og:url" content="{ru_url}" />
<meta property="og:site_name" content="norito" />
<meta property="og:locale" content="ru_RU" />
<meta property="og:image" content="https://norito.in/assets/og-image.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{title}" />
<meta name="twitter:description" content="{ogd}" />
<meta name="twitter:image" content="https://norito.in/assets/og-image.png" />
<link rel="stylesheet" href="../../css/style.css" />
'''

ADSENSE_COMMENT = '''<!-- AdSense temporarily disabled while investigating a Search Console "possible phishing" security flag. To restore, remove this comment wrapper. -->
<!-- <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4040839176833351" crossorigin="anonymous"></script> -->
</head>
<body>
<div class="bg-blobs" aria-hidden="true">
  <div class="blob blob-1"></div>
  <div class="blob blob-2"></div>
  <div class="blob blob-3"></div>
</div>
'''
print("part1 defined")

HEADER_HTML = '''<header class="site">
  <div class="wrap">
    <a class="brand" href="../index.html"><img class="logo logo-word" src="../../assets/norito-wordmark.svg" alt="norito" width="113" height="44" /></a>
        <nav class="site-nav" id="siteNav">
      <div class="nav-group">
        <button type="button" class="nav-cat">Изображения</button>
        <div class="nav-panel">
          <a href="../compress-image.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-5-5L5 21"/></svg><div class="nav-link-body">Сжатие изображения<span>Уменьшает до целевого размера файла</span></div></a>
          <a href="../placeholder-generator.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><path d="M3 7V3h4M17 3h4v4M21 17v4h-4M7 21H3v-4"/></svg><div class="nav-link-body">Генератор заполнителей<span>Изображения-заполнители на заказ</span></div></a>
          <a href="../remove-background.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M20 4 8.12 15.88M14.47 14.48 20 20M8.12 8.12 12 12"/></svg><div class="nav-link-body">Удаление фона<span>Вырезает человека с фотографии</span></div></a>
        </div>
      </div>
      <div class="nav-group">
        <button type="button" class="nav-cat">Разработка</button>
        <div class="nav-panel">
          <a href="../test-file-generator.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M9 13h6M9 17h6"/></svg><div class="nav-link-body">Генератор тестовых файлов<span>Файлы-заполнители точного размера</span></div></a>
          <a href="../json-formatter.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><path d="M8 3a3 3 0 0 0-3 3v3a2 2 0 0 1-2 2 2 2 0 0 1 2 2v3a3 3 0 0 0 3 3"/><path d="M16 3a3 3 0 0 1 3 3v3a2 2 0 0 0 2 2 2 2 0 0 0-2 2v3a3 3 0 0 1-3 3"/></svg><div class="nav-link-body">Форматирование JSON<span>Форматирует, проверяет и минифицирует</span></div></a>
          <a href="../markdown-editor.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4Z"/></svg><div class="nav-link-body">Редактор Markdown<span>Предпросмотр в реальном времени, экспорт в .md/.html</span></div></a>
        </div>
      </div>
      <div class="nav-group">
        <button type="button" class="nav-cat">Текст</button>
        <div class="nav-panel">
          <a href="../seo-slug-generator.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><path d="M10 13a5 5 0 0 0 7.07 0l2-2a5 5 0 0 0-7.07-7.07l-1.5 1.5"/><path d="M14 11a5 5 0 0 0-7.07 0l-2 2a5 5 0 0 0 7.07 7.07l1.5-1.5"/></svg><div class="nav-link-body">Генератор SEO-слагов<span>Чистые URL из заголовков</span></div></a>
          <a href="../limited-text-generator.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><path d="M4 7V4h16v3"/><path d="M9 20h6"/><path d="M12 4v16"/></svg><div class="nav-link-body">Генератор текста заданной длины<span>Текст-заполнитель точной длины</span></div></a>
        </div>
      </div>
      <div class="nav-group">
        <button type="button" class="nav-cat">Утилиты</button>
        <div class="nav-panel">
          <a href="../password-generator.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg><div class="nav-link-body">Генератор паролей<span>Случайные пароли и фразы</span></div></a>
          <a href="../qr-code-generator.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><path d="M14 14h3v3h-3zM19 17h2M17 19v2M14 19h.01M19 14h.01"/></svg><div class="nav-link-body">Генератор QR-кодов<span>Пользовательские цвета, коррекция ошибок</span></div></a>
        </div>
      </div>
    
            <div class="nav-group">
        <a class="nav-cat" href="../pdf/">PDF <span class="nav-en-tag">EN</span></a>
        <div class="nav-panel">
          <a href="../pdf/merge-pdf.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><path d="M15.5 2H8.6c-.4 0-.8.2-1.1.5-.3.3-.5.7-.5 1.1v12.8c0 .4.2.8.5 1.1.3.3.7.5 1.1.5h9.8c.4 0 .8-.2 1.1-.5.3-.3.5-.7.5-1.1V6.5L15.5 2z"/><path d="M3 7.6v12.8c0 .4.2.8.5 1.1.3.3.7.5 1.1.5h9.8"/><path d="M15 2v5h5"/></svg><div class="nav-link-body">Merge PDF<span>Combine multiple PDFs into one</span></div></a>
          <a href="../pdf/split-pdf.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><circle cx="6" cy="6" r="3"/><path d="M8.12 8.12 12 12"/><path d="M20 4 8.12 15.88"/><circle cx="6" cy="18" r="3"/><path d="M14.8 14.8 20 20"/></svg><div class="nav-link-body">Split PDF<span>Pull out pages or split into files</span></div></a>
          <a href="../pdf/rotate-pdf.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><path d="M21 12a9 9 0 1 1-9-9c2.52 0 4.93 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/></svg><div class="nav-link-body">Rotate PDF<span>Fix sideways or upside-down pages</span></div></a>
          <a href="../pdf/pdf-to-image.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/></svg><div class="nav-link-body">PDF to JPG/PNG<span>Turn pages into images</span></div></a>
          <a href="../pdf/jpg-png-to-pdf.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><circle cx="10" cy="13" r="2"/><path d="m20 17-1.5-1.5a2 2 0 0 0-2.83 0L9 22"/></svg><div class="nav-link-body">JPG/PNG to PDF<span>Combine images into one PDF</span></div></a>
          <a href="../pdf/organize-pdf.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><rect width="7" height="7" x="3" y="3" rx="1"/><rect width="7" height="7" x="14" y="3" rx="1"/><rect width="7" height="7" x="14" y="14" rx="1"/><rect width="7" height="7" x="3" y="14" rx="1"/></svg><div class="nav-link-body">Delete &amp; Reorder Pages<span>Delete or rearrange pages</span></div></a>
          <a href="../pdf/add-page-numbers.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M10 12h2v6"/><path d="M10 18h4"/></svg><div class="nav-link-body">Add Page Numbers<span>Number every page</span></div></a>
          <a href="../pdf/add-watermark.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="m9 15 6-6"/><path d="m9 9 6 6"/></svg><div class="nav-link-body">Add Watermark<span>Stamp text across every page</span></div></a>
          <a href="../pdf/extract-text.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M8 13h8M8 17h5"/></svg><div class="nav-link-body">Extract Text<span>Pull text out of a PDF</span></div></a>
          <a href="../pdf/compress-pdf.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="m10 12-2 2 2 2M14 12l2 2-2 2"/></svg><div class="nav-link-body">Compress PDF<span>Shrink a large PDF's file size</span></div></a>
          <a href="../pdf/sign-pdf.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/></svg><div class="nav-link-body">Sign PDF<span>Draw or type a signature</span></div></a>
        </div>
      </div>
            <div class="nav-group">
        <a class="nav-cat" href="../seo/">SEO <span class="nav-en-tag">EN</span></a>
        <div class="nav-panel">
          <a href="../seo/meta-tag-generator.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><path d="M4 7V4h16v3"/><path d="M9 20h6"/><path d="M12 4v16"/></svg><div class="nav-link-body">Meta Tag Generator<span>Title, description, OG, Twitter tags</span></div></a>
          <a href="../seo/utm-builder.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8"/><path d="M12 17v4"/></svg><div class="nav-link-body">UTM Builder<span>Build campaign tracking URLs</span></div></a>
          <a href="../seo/robots-txt-generator.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><rect x="3" y="11" width="18" height="10" rx="2"/><circle cx="8.5" cy="16" r="1.5"/><circle cx="15.5" cy="16" r="1.5"/><path d="M7 11V8a5 5 0 0 1 10 0v3"/></svg><div class="nav-link-body">Robots.txt Generator<span>Allow/disallow rules, sitemap ref</span></div></a>
          <a href="../seo/sitemap-generator.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg><div class="nav-link-body">Sitemap Generator<span>URLs in, sitemap.xml out</span></div></a>
        </div>
      </div>
            <div class="nav-group">
        <a class="nav-cat" href="../design/">Design <span class="nav-en-tag">EN</span></a>
        <div class="nav-panel">
          <a href="../design/css-gradient-generator.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><path d="M12 22c4.97 0 9-4.03 9-9-4.97 0-9 4.03-9 9Z"/><path d="M12 22C7.03 22 3 17.97 3 13c4.97 0 9 4.03 9 9Z"/><path d="M12 13c0-5 4-8 4-8s-8 0-8 8"/></svg><div class="nav-link-body">CSS Gradient Generator<span>Linear or radial, copy the CSS</span></div></a>
          <a href="../design/box-shadow-generator.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><rect x="4" y="4" width="13" height="13" rx="2"/><path d="M9 9h13v13H9z" opacity="0.35"/></svg><div class="nav-link-body">Box Shadow Generator<span>Single or layered shadows</span></div></a>
          <a href="../design/border-radius-generator.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><path d="M4 12V8a4 4 0 0 1 4-4h8a4 4 0 0 1 4 4v8a4 4 0 0 1-4 4H8"/><path d="M4 12v4"/></svg><div class="nav-link-body">Border Radius Generator<span>Per-corner radius, copy the CSS</span></div></a>
          <a href="../design/favicon-generator.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3"/></svg><div class="nav-link-body">Favicon Generator<span>Every favicon size you need</span></div></a>
          <a href="../design/color-palette-extractor.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><circle cx="13.5" cy="6.5" r=".5"/><circle cx="17.5" cy="10.5" r=".5"/><circle cx="8.5" cy="7.5" r=".5"/><circle cx="6.5" cy="12.5" r=".5"/><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.926 0 1.648-.746 1.648-1.688 0-.437-.18-.835-.437-1.125-.29-.289-.438-.652-.438-1.125a1.64 1.64 0 0 1 1.668-1.668h1.996c3.051 0 5.555-2.503 5.555-5.554C21.965 6.012 17.461 2 12 2z"/></svg><div class="nav-link-body">Color Palette Extractor<span>Pull dominant colors from an image</span></div></a>
          <a href="../design/contrast-checker.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><path d="m9 18 6-12"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="6" r="3"/></svg><div class="nav-link-body">Contrast Checker<span>WCAG contrast ratio, AA/AAA pass</span></div></a>
          <a href="../design/color-converter.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><circle cx="13.5" cy="6.5" r=".5"/><path d="M12 2a10 10 0 1 0 10 10 4 4 0 0 1-4-4V6a4 4 0 0 0-4-4Z"/><circle cx="17.5" cy="10.5" r=".5"/><circle cx="6.5" cy="12.5" r=".5"/></svg><div class="nav-link-body">Color Converter<span>HEX, RGB, HSL, CMYK, live</span></div></a>
        </div>
      </div>
          </nav>
      <button type="button" class="search-trigger" id="searchTrigger" aria-label="Поиск инструментов" title="Поиск инструментов"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg></button>

      <button type="button" class="theme-toggle-btn" aria-label="Переключить тёмную тему">
        <svg class="theme-icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9"/></svg>
        <svg class="theme-icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>
      </button>

      <div class="lang-switch" id="langSwitch">
        <button type="button" class="lang-switch-btn" aria-label="Language / Idioma / 语言 / اللغة / भाषा / Язык">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
          <span class="lang-switch-current" id="langSwitchCurrent">EN</span>
        </button>
        <div class="lang-switch-panel" id="langSwitchPanel"></div>
      </div>
  </div>
</header>
'''
print("header defined, len=", len(HEADER_HTML))

FOOTER_HTML = '''<footer class="site">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        <div class="footer-brand-name">norito</div>
        <p class="footer-tagline">Маленькие утилиты, каждая из которых решает одну надоедливую задачу. Всё работает в вашем браузере, ничего не загружается на сервер.</p>
      </div>
      <div class="footer-col">
        <h3>PDF</h3>
        <a href="merge-pdf.html">Объединение PDF</a>
        <a href="split-pdf.html">Разделение PDF</a>
        <a href="rotate-pdf.html">Поворот PDF</a>
        <a href="pdf-to-image.html">PDF в JPG/PNG</a>
        <a href="jpg-png-to-pdf.html">JPG/PNG в PDF</a>
        <a href="organize-pdf.html">Удаление и перестановка</a>
        <a href="add-page-numbers.html">Номера страниц</a>
        <a href="add-watermark.html">Водяной знак</a>
        <a href="extract-text.html">Извлечение текста</a>
        <a href="compress-pdf.html">Сжатие PDF</a>
        <a href="sign-pdf.html">Подпись PDF</a>
      </div>
      <div class="footer-col">
        <h3>Изображения</h3>
        <a href="../test-file-generator.html">Тестовые файлы</a>
        <a href="../compress-image.html">Сжать</a>
        <a href="../placeholder-generator.html">Заполнитель</a>
        <a href="../remove-background.html">Удаление фона</a>
        <a href="../qr-code-generator.html">QR-код</a>
      </div>
      <div class="footer-col">
        <h3>Текст и разработка</h3>
        <a href="../password-generator.html">Пароль</a>
        <a href="../seo-slug-generator.html">Слаг</a>
        <a href="../limited-text-generator.html">Лимит текста</a>
        <a href="../json-formatter.html">JSON</a>
        <a href="../markdown-editor.html">Markdown</a>
      </div>
    </div>
    <div class="footer-bottom">
      <span>© 2026 norito. Все инструменты работают локально в вашем браузере.</span>
      <a href="../privacy.html">Политика конфиденциальности</a>
            <a href="../../blog/">Блог</a>
            <a href="../../compare/">Сравнение</a>
            <a href="../../how-it-works.html">Как это работает</a>
      <a href="https://ko-fi.com/shubhmisaki" target="_blank" rel="noopener">Угости меня кофе</a>
    </div>
  </div>
</footer>
'''

def cmdk_and_scripts(script_tags):
    return f'''
{script_tags}
<div class="cmdk-overlay" id="cmdkOverlay" hidden data-empty-text="По этому запросу инструменты не найдены.">
  <div class="cmdk-modal" role="dialog" aria-modal="true" aria-label="Поиск инструментов">
    <div class="cmdk-input-row">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>
      <input type="text" id="cmdkInput" placeholder="Поиск инструментов..." autocomplete="off" />
      <kbd>Esc</kbd>
    </div>
    <div class="cmdk-results" id="cmdkResults"></div>
  </div>
</div>

<script src="../../js/cmdk.js"></script>
<script src="/js/sw-register.js" defer></script>
<script src="/js/install-prompt.js" defer></script>
</body>
</html>
'''

print("footer defined, len=", len(FOOTER_HTML))

PAGES = {}

# ---------------- merge-pdf ----------------
PAGES['merge-pdf.html'] = dict(
  title="Объединение PDF-файлов онлайн бесплатно | norito",
  desc="Объедините несколько PDF-файлов в один, в выбранном вами порядке. Перетащите файлы, расположите их и объедините. Работает полностью в вашем браузере, файлы никогда не загружаются.",
  jsonld_name="Объединение PDF-файлов",
  jsonld_desc="Объедините несколько PDF-файлов в один, в выбранном вами порядке. Работает полностью в вашем браузере.",
  faq=[
    ("Загружаются ли мои PDF-файлы куда-либо?", "Нет. Объединение происходит полностью в вашем браузере с помощью JavaScript. Ваши файлы никогда не покидают устройство и не попадают на сервер."),
    ("Могу ли я выбрать порядок объединения PDF?", "Да. Добавьте файлы, а затем используйте кнопки вверх и вниз в каждой строке, чтобы расположить их в нужном порядке перед объединением."),
    ("Есть ли ограничение на размер файла или количество PDF?", "Жёсткого ограничения в самом инструменте нет. Практический предел определяется доступной памятью вашего браузера: очень большие или многочисленные файлы могут обрабатываться дольше или вызывать проблемы на устройствах с малым объёмом памяти."),
    ("Снижает ли объединение качество PDF?", "Нет. Страницы копируются как есть из каждого исходного файла, без повторного рендеринга, пересжатия или потери качества."),
    ("Могу ли я объединить PDF, защищённый паролем?", "Пока нет. Инструмент не может прочитать PDF, защищённый паролем или зашифрованный, и покажет ошибку. Сначала снимите пароль с помощью программы для чтения PDF."),
  ],
  icon_class="c-indigo",
  icon_svg='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M15.5 2H8.6c-.4 0-.8.2-1.1.5-.3.3-.5.7-.5 1.1v12.8c0 .4.2.8.5 1.1.3.3.7.5 1.1.5h9.8c.4 0 .8-.2 1.1-.5.3-.3.5-.7.5-1.1V6.5L15.5 2z"/><path d="M3 7.6v12.8c0 .4.2.8.5 1.1.3.3.7.5 1.1.5h9.8"/><path d="M15 2v5h5"/></svg>',
  breadcrumb="Объединение PDF",
  h1="Объединение PDF-файлов",
  lede="Объедините несколько PDF в один файл, в любом порядке, который вы выберете. Добавьте файлы, расположите их и скачайте объединённый PDF. Ничего не загружается, всё происходит на вашем устройстве.",
  main_extra='''
    <div class="panel">
      <div class="dropzone" id="drop">
        <svg class="dz-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M16 16l-4-4-4 4"/><path d="M12 12v9"/><path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3"/></svg>
        <p><strong>Нажмите, чтобы выбрать PDF-файлы</strong>, или перетащите их сюда</p>
        <p class="note" style="margin-top:2px;">Добавьте два и более PDF. Остаётся на вашем устройстве, ничего не загружается.</p>
        <input type="file" id="fileInput" accept="application/pdf" multiple />
      </div>

      <div class="file-list" id="fileList" style="display:none;"></div>

      <button id="mergeBtn" disabled style="margin-top:20px;">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="M7 10l5 5 5-5"/><path d="M12 15V3"/></svg>
        Объединить PDF
      </button>
      <div class="result-box" id="result" style="display:none;"></div>
    </div>

    <div class="panel" style="margin-top:32px;">
      <h3 style="margin-top:0;">Как это работает</h3>
      <p class="note" style="margin-top:0;">
        Объединение происходит полностью в вашем браузере с помощью библиотеки для работы с PDF, которая выполняется на стороне клиента. Каждая страница копируется напрямую из исходных файлов в новый объединённый PDF, поэтому повторного рендеринга или потери качества не происходит. Измените порядок файлов кнопками вверх и вниз перед объединением, так как страницы объединяются в том порядке, в каком перечислены файлы.
      </p>
    </div>
''',
  scripts=['../../js/i18n-runtime.js','../../js/utils.js','../../js/vendor/pdf-lib.min.js','../../js/app-pdf-merge.js','../../js/nav.js','../../js/theme-toggle.js','../../js/lang-switcher.js','../../js/bg-blobs.js'],
)
print("merge-pdf added")

# ---------------- split-pdf ----------------
PAGES['split-pdf.html'] = dict(
  title="Разделение PDF-файлов онлайн бесплатно | norito",
  desc="Извлеките нужные страницы из PDF или разделите его на отдельные файлы. Укажите диапазоны страниц вида 1-3, 5, 8-10. Работает в вашем браузере, файлы никогда не загружаются.",
  jsonld_name="Разделение PDF-файлов",
  jsonld_desc="Извлеките нужные страницы из PDF или разделите его на отдельные файлы. Работает полностью в вашем браузере.",
  faq=[
    ("Загружаются ли мои PDF-файлы куда-либо?", "Нет. Разделение происходит полностью в вашем браузере с помощью JavaScript. Ваши файлы никогда не покидают устройство и не попадают на сервер."),
    ("Как извлечь всего несколько страниц?", "Введите нужные номера страниц или диапазоны, например 1-3, 7, и нажмите «Разделить». Они будут объединены в один новый PDF в этом порядке."),
    ("Могу ли я разделить PDF на отдельный файл для каждой страницы?", "Да. Включите «Разделить на отдельные файлы» и оставьте поле страниц пустым: каждая страница скачается как отдельный PDF внутри .zip."),
    ("Могу ли я извлечь сразу несколько отдельных диапазонов?", "Да. Введите их через запятую, например 1-3, 5, 8-10, и включите «Разделить на отдельные файлы», чтобы получить каждую группу отдельным PDF в .zip."),
    ("Снижает ли разделение качество PDF?", "Нет. Страницы копируются как есть из исходного файла, без повторного рендеринга, пересжатия или потери качества."),
    ("Могу ли я разделить PDF, защищённый паролем?", "Пока нет. Инструмент не может прочитать PDF, защищённый паролем или зашифрованный, и покажет ошибку. Сначала снимите пароль с помощью программы для чтения PDF."),
  ],
  icon_class="c-rose",
  icon_svg='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="6" cy="6" r="3"/><path d="M8.12 8.12 12 12"/><path d="M20 4 8.12 15.88"/><circle cx="6" cy="18" r="3"/><path d="M14.8 14.8 20 20"/></svg>',
  breadcrumb="Разделение PDF",
  h1="Разделение PDF-файлов",
  lede="Извлеките нужные страницы из PDF или разберите его полностью. Укажите страницы, например 1-3, 5, 8-10, и скачайте результат. Ничего не загружается, всё происходит на вашем устройстве.",
  main_extra='''
    <div class="panel">
      <div class="dropzone" id="drop">
        <svg class="dz-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M16 16l-4-4-4 4"/><path d="M12 12v9"/><path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3"/></svg>
        <p><strong>Нажмите, чтобы выбрать PDF-файл</strong>, или перетащите его сюда</p>
        <p class="note" style="margin-top:2px;">Остаётся на вашем устройстве, ничего не загружается.</p>
        <input type="file" id="fileInput" accept="application/pdf" />
      </div>
      <p class="note" id="fileInfo" style="display:none;"></p>

      <div class="field" style="margin-top:20px;">
        <label for="pagesInput">Страницы для извлечения</label>
        <input type="text" id="pagesInput" placeholder="например 1-3, 5, 8-10 &ndash; оставьте пустым для всех страниц" disabled />
      </div>

      <div class="option-row" style="margin-bottom:20px;">
        <div>
          <div class="option-label">Разделить на отдельные файлы</div>
          <div class="option-hint">Выключено: объединяет выбранное в один PDF. Включено: создаёт по одному файлу на каждую группу выше (или по одному на страницу, если поле пустое), упакованные в .zip.</div>
        </div>
        <label class="switch"><input type="checkbox" id="separateToggle" /><span class="track"></span></label>
      </div>

      <button id="splitBtn" disabled>
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="M7 10l5 5 5-5"/><path d="M12 15V3"/></svg>
        Разделить PDF
      </button>
      <div class="result-box" id="result" style="display:none;"></div>
    </div>

    <div class="panel" style="margin-top:32px;">
      <h3 style="margin-top:0;">Как это работает</h3>
      <p class="note" style="margin-top:0;">
        Разделение происходит полностью в вашем браузере с помощью библиотеки для работы с PDF, которая выполняется на стороне клиента. Страницы копируются напрямую из исходного файла, поэтому повторного рендеринга или потери качества не происходит. Оставьте поле страниц пустым, чтобы работать со всеми страницами, или укажите конкретные страницы и диапазоны через запятую.
      </p>
    </div>
''',
  scripts=['../../js/i18n-runtime.js','../../js/utils.js','../../js/vendor/pdf-lib.min.js','../../js/app-pdf-split.js','../../js/nav.js','../../js/theme-toggle.js','../../js/lang-switcher.js','../../js/bg-blobs.js'],
)
print("split-pdf added")

# ---------------- rotate-pdf ----------------
PAGES['rotate-pdf.html'] = dict(
  title="Поворот страниц PDF онлайн бесплатно | norito",
  desc="Поверните PDF на 90, 180 или 270 градусов: все страницы или только выбранные. Работает полностью в вашем браузере, файлы никогда не загружаются.",
  jsonld_name="Поворот PDF",
  jsonld_desc="Поверните PDF на 90, 180 или 270 градусов: все страницы или только выбранные. Работает полностью в вашем браузере.",
  faq=[
    ("Загружаются ли мои PDF-файлы куда-либо?", "Нет. Поворот происходит полностью в вашем браузере с помощью JavaScript. Ваши файлы никогда не покидают устройство и не попадают на сервер."),
    ("Могу ли я повернуть только некоторые страницы?", "Да. Введите нужные номера страниц или диапазоны, например 1-3, 7, и повёрнуты будут только они. Оставьте поле пустым, чтобы повернуть каждую страницу."),
    ("Что если страница уже повёрнута?", "Выбранный поворот применяется поверх текущей ориентации каждой страницы, а не задаётся с нуля, поэтому уже повёрнутая боком страница дополнительно повернётся на 90, 180 или 270 градусов, а не сбросится."),
    ("Снижает ли поворот качество PDF?", "Нет. Поворот — это изменение метаданных каждой страницы, само содержимое не рендерится и не пересжимается заново."),
    ("Могу ли я повернуть PDF, защищённый паролем?", "Пока нет. Инструмент не может прочитать PDF, защищённый паролем или зашифрованный, и покажет ошибку. Сначала снимите пароль с помощью программы для чтения PDF."),
  ],
  icon_class="c-teal",
  icon_svg='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 1 1-9-9c2.52 0 4.93 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/></svg>',
  breadcrumb="Поворот PDF",
  h1="Поворот страниц PDF",
  lede="Исправьте страницы, повёрнутые боком или вверх ногами. Поверните весь документ или только выбранные страницы, затем скачайте результат. Ничего не загружается, всё происходит на вашем устройстве.",
  main_extra='''
    <div class="panel">
      <div class="dropzone" id="drop">
        <svg class="dz-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M16 16l-4-4-4 4"/><path d="M12 12v9"/><path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3"/></svg>
        <p><strong>Нажмите, чтобы выбрать PDF-файл</strong>, или перетащите его сюда</p>
        <p class="note" style="margin-top:2px;">Остаётся на вашем устройстве, ничего не загружается.</p>
        <input type="file" id="fileInput" accept="application/pdf" />
      </div>
      <p class="note" id="fileInfo" style="display:none;"></p>

      <div class="field" style="margin-top:20px;">
        <label>Поворот</label>
        <div class="tabs" id="rotateTabs">
          <button type="button" class="tab active" data-value="90">Повернуть на 90&deg; вправо</button>
          <button type="button" class="tab" data-value="-90">Повернуть на 90&deg; влево</button>
          <button type="button" class="tab" data-value="180">Повернуть на 180&deg;</button>
        </div>
      </div>

      <div class="field" style="margin-top:20px; margin-bottom:20px;">
        <label for="pagesInput">Страницы для поворота</label>
        <input type="text" id="pagesInput" placeholder="например 1-3, 5 &ndash; оставьте пустым для всех страниц" disabled />
      </div>

      <button id="rotateBtn" disabled>
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="M21 12a9 9 0 1 1-9-9c2.52 0 4.93 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/></svg>
        Повернуть PDF
      </button>
      <div class="result-box" id="result" style="display:none;"></div>
    </div>

    <div class="panel" style="margin-top:32px;">
      <h3 style="margin-top:0;">Как это работает</h3>
      <p class="note" style="margin-top:0;">
        Поворот происходит полностью в вашем браузере с помощью библиотеки для работы с PDF, которая выполняется на стороне клиента. Ориентация каждой выбранной страницы обновляется поверх текущего поворота, поэтому само содержимое никогда не перерисовывается, а только разворачивается. Оставьте поле страниц пустым, чтобы повернуть весь документ.
      </p>
    </div>
''',
  scripts=['../../js/i18n-runtime.js','../../js/utils.js','../../js/vendor/pdf-lib.min.js','../../js/app-pdf-rotate.js','../../js/nav.js','../../js/theme-toggle.js','../../js/lang-switcher.js','../../js/bg-blobs.js'],
)
print("rotate-pdf added")

# ---------------- pdf-to-image ----------------
PAGES['pdf-to-image.html'] = dict(
  title="Конвертация PDF в JPG или PNG онлайн бесплатно | norito",
  desc="Превратите страницы PDF в изображения JPG или PNG. Выберите разрешение, укажите страницы и скачайте результат. Работает полностью в вашем браузере, файлы никогда не загружаются.",
  jsonld_name="Конвертация PDF в JPG или PNG",
  jsonld_desc="Превратите страницы PDF в изображения JPG или PNG. Работает полностью в вашем браузере.",
  faq=[
    ("Загружаются ли мои PDF-файлы куда-либо?", "Нет. Конвертация происходит полностью в вашем браузере с помощью JavaScript. Ваши файлы никогда не покидают устройство и не попадают на сервер."),
    ("Какое разрешение выбрать?", "96 DPI подходит для экранов и веба, 150 DPI — хороший универсальный вариант по умолчанию, а 300 DPI лучше всего для печати или увеличения мелких деталей. Чем выше разрешение, тем больше файл."),
    ("JPG или PNG, что выбрать?", "JPG меньше по размеру и подходит для фото или сканов. PNG без потерь и лучше подходит для страниц с чётким текстом, векторной графикой или там, где нужен прозрачный фон."),
    ("Могу ли я конвертировать только некоторые страницы?", "Да. Введите нужные номера страниц или диапазоны, например 1-3, 7. Оставьте поле пустым, чтобы конвертировать каждую страницу."),
    ("Что я получу при конвертации нескольких страниц?", "Одна страница скачивается как отдельное изображение. Две и более страниц скачиваются вместе в виде .zip, по одному изображению на страницу."),
    ("Могу ли я конвертировать PDF, защищённый паролем?", "Пока нет. Инструмент не может прочитать PDF, защищённый паролем или зашифрованный, и покажет ошибку. Сначала снимите пароль с помощью программы для чтения PDF."),
  ],
  icon_class="c-amber",
  icon_svg='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/></svg>',
  breadcrumb="PDF в JPG/PNG",
  h1="Конвертация PDF в JPG или PNG",
  lede="Превратите страницы PDF в изображения. Выберите формат и разрешение, укажите нужные страницы и скачайте результат. Ничего не загружается, всё происходит на вашем устройстве.",
  main_extra='''
    <div class="panel">
      <div class="dropzone" id="drop">
        <svg class="dz-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M16 16l-4-4-4 4"/><path d="M12 12v9"/><path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3"/></svg>
        <p><strong>Нажмите, чтобы выбрать PDF-файл</strong>, или перетащите его сюда</p>
        <p class="note" style="margin-top:2px;">Остаётся на вашем устройстве, ничего не загружается.</p>
        <input type="file" id="fileInput" accept="application/pdf" />
      </div>
      <p class="note" id="fileInfo" style="display:none;"></p>

      <div class="field-row" style="margin-top:20px;">
        <div class="field">
          <label for="formatSelect">Формат</label>
          <select id="formatSelect" disabled>
            <option value="jpg" selected>JPG</option>
            <option value="png">PNG</option>
          </select>
        </div>
        <div class="field" id="qualityField">
          <label for="qualitySelect">Качество</label>
          <select id="qualitySelect" disabled>
            <option value="0.92" selected>Высокое</option>
            <option value="0.8">Среднее</option>
            <option value="0.6">Низкое (меньше файл)</option>
          </select>
        </div>
        <div class="field">
          <label for="dpiSelect">Разрешение</label>
          <select id="dpiSelect" disabled>
            <option value="96">96 DPI (веб)</option>
            <option value="150" selected>150 DPI (по умолчанию)</option>
            <option value="300">300 DPI (печать)</option>
          </select>
        </div>
      </div>

      <div class="field" style="margin-top:4px; margin-bottom:20px;">
        <label for="pagesInput">Страницы для конвертации</label>
        <input type="text" id="pagesInput" placeholder="например 1-3, 5 &ndash; оставьте пустым для всех страниц" disabled />
      </div>

      <button id="convertBtn" disabled>
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="M7 10l5 5 5-5"/><path d="M12 15V3"/></svg>
        Конвертировать в изображения
      </button>
      <div class="result-box" id="result" style="display:none;"></div>
    </div>

    <div class="panel" style="margin-top:32px;">
      <h3 style="margin-top:0;">Как это работает</h3>
      <p class="note" style="margin-top:0;">
        Каждая выбранная страница рендерится на холст в вашем браузере с выбранным разрешением, а затем экспортируется как изображение. Ничего никуда не отправляется, библиотека рендеринга PDF работает полностью на стороне клиента. Одна страница скачивается напрямую, несколько страниц упаковываются в .zip.
      </p>
    </div>
''',
  scripts=['../../js/i18n-runtime.js','../../js/utils.js','MODULE:../../js/app-pdf-to-image.js','../../js/nav.js','../../js/theme-toggle.js','../../js/lang-switcher.js','../../js/bg-blobs.js'],
)
print("pdf-to-image added")

# ---------------- jpg-png-to-pdf ----------------
PAGES['jpg-png-to-pdf.html'] = dict(
  title="Конвертация JPG или PNG в PDF онлайн бесплатно | norito",
  desc="Объедините одно или несколько изображений в единый PDF. Измените порядок, выберите размер страницы и скачайте. Работает полностью в вашем браузере, файлы никогда не загружаются.",
  jsonld_name="Конвертация JPG или PNG в PDF",
  jsonld_desc="Объедините одно или несколько изображений в единый PDF. Работает полностью в вашем браузере.",
  faq=[
    ("Загружаются ли мои изображения куда-либо?", "Нет. Конвертация происходит полностью в вашем браузере с помощью JavaScript. Ваши файлы никогда не покидают устройство и не попадают на сервер."),
    ("Могу ли я выбрать порядок страниц?", "Да. Добавьте изображения, а затем используйте кнопки вверх и вниз в каждой строке, чтобы расположить их в нужном порядке перед конвертацией."),
    ("Какой размер страницы выбрать?", "«По размеру изображения» делает каждую страницу с пропорциями самого изображения, что обычно лучше всего для сканов и скриншотов. A4 или US Letter вписывают изображение по центру стандартной страницы, что часто удобнее для печати."),
    ("Какие форматы изображений поддерживаются?", "JPG и PNG обрабатываются нативно. Другие форматы, которые может показать ваш браузер, например WebP, сначала автоматически конвертируются."),
    ("Снижает ли конвертация качество изображений?", "В большинстве случаев изображения JPG и PNG встраиваются как есть. Некоторые изображения нужно перекодировать, чтобы их можно было встроить (отдельные варианты JPEG или форматы, отличные от JPG/PNG), такие сначала конвертируются без потерь в PNG."),
  ],
  icon_class="c-purple",
  icon_svg='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><circle cx="10" cy="13" r="2"/><path d="m20 17-1.5-1.5a2 2 0 0 0-2.83 0L9 22"/></svg>',
  breadcrumb="JPG/PNG в PDF",
  h1="Конвертация JPG или PNG в PDF",
  lede="Объедините одно или несколько изображений в единый PDF, в выбранном вами порядке. Ничего не загружается, всё происходит на вашем устройстве.",
  main_extra='''
    <div class="panel">
      <div class="dropzone" id="drop">
        <svg class="dz-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M16 16l-4-4-4 4"/><path d="M12 12v9"/><path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3"/></svg>
        <p><strong>Нажмите, чтобы выбрать изображения</strong>, или перетащите их сюда</p>
        <p class="note" style="margin-top:2px;">JPG, PNG и большинство других форматов изображений. Остаётся на вашем устройстве, ничего не загружается.</p>
        <input type="file" id="fileInput" accept="image/*" multiple />
      </div>

      <div class="file-list" id="fileList" style="display:none;"></div>

      <div class="field" style="margin-top:20px; margin-bottom:20px; max-width:320px;">
        <label for="pageSizeSelect">Размер страницы</label>
        <select id="pageSizeSelect">
          <option value="fit" selected>По размеру изображения</option>
          <option value="a4">A4</option>
          <option value="letter">US Letter</option>
        </select>
      </div>

      <button id="convertBtn" disabled>
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="M7 10l5 5 5-5"/><path d="M12 15V3"/></svg>
        Конвертировать в PDF
      </button>
      <div class="result-box" id="result" style="display:none;"></div>
    </div>

    <div class="panel" style="margin-top:32px;">
      <h3 style="margin-top:0;">Как это работает</h3>
      <p class="note" style="margin-top:0;">
        Каждое изображение становится одной страницей, добавленной в показанном выше порядке. Конвертация происходит полностью в вашем браузере с помощью библиотеки для работы с PDF, которая выполняется на стороне клиента. JPG и PNG встраиваются напрямую там, где это возможно, всё остальное сначала декодируется и перекодируется, чтобы его можно было встроить.
      </p>
    </div>
''',
  scripts=['../../js/i18n-runtime.js','../../js/utils.js','../../js/vendor/pdf-lib.min.js','../../js/app-images-to-pdf.js','../../js/nav.js','../../js/theme-toggle.js','../../js/lang-switcher.js','../../js/bg-blobs.js'],
)
print("jpg-png-to-pdf added")

# ---------------- organize-pdf ----------------
PAGES['organize-pdf.html'] = dict(
  title="Удаление и перестановка страниц PDF онлайн бесплатно | norito",
  desc="Просмотрите каждую страницу в виде миниатюры, удалите ненужные и переставьте остальные. Работает полностью в вашем браузере, файлы никогда не загружаются.",
  jsonld_name="Удаление и перестановка страниц PDF",
  jsonld_desc="Просмотрите каждую страницу в виде миниатюры, удалите ненужные и переставьте остальные. Работает полностью в вашем браузере.",
  faq=[
    ("Загружаются ли мои PDF-файлы куда-либо?", "Нет. Всё, включая миниатюры страниц, создаётся полностью в вашем браузере. Ваши файлы никогда не покидают устройство и не попадают на сервер."),
    ("Как удалить страницу?", "Нажмите на крестик на миниатюре страницы, чтобы отметить её для удаления: она станет тусклой, показывая, что не будет включена. Нажмите ещё раз, чтобы отменить."),
    ("Как изменить порядок страниц?", "Используйте стрелки вверх и вниз под каждой миниатюрой, чтобы переместить страницу раньше или позже. Итоговый PDF повторяет порядок, показанный на экране."),
    ("Могу ли я удалить все страницы?", "Нет, PDF должен содержать хотя бы одну страницу, поэтому кнопка сохранения отключена, если все страницы отмечены для удаления."),
    ("Могу ли я упорядочить PDF, защищённый паролем?", "Пока нет. Инструмент не может прочитать PDF, защищённый паролем или зашифрованный, и покажет ошибку. Сначала снимите пароль с помощью программы для чтения PDF."),
  ],
  icon_class="c-coral",
  icon_svg='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="7" height="7" x="3" y="3" rx="1"/><rect width="7" height="7" x="14" y="3" rx="1"/><rect width="7" height="7" x="14" y="14" rx="1"/><rect width="7" height="7" x="3" y="14" rx="1"/></svg>',
  breadcrumb="Удаление и перестановка страниц",
  h1="Удаление и перестановка страниц PDF",
  lede="Просматривайте каждую страницу в виде миниатюры, отмечайте ненужные и располагайте остальные в нужном порядке. Ничего не загружается, всё происходит на вашем устройстве.",
  main_extra='''
    <div class="panel">
      <div class="dropzone" id="drop">
        <svg class="dz-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M16 16l-4-4-4 4"/><path d="M12 12v9"/><path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3"/></svg>
        <p><strong>Нажмите, чтобы выбрать PDF-файл</strong>, или перетащите его сюда</p>
        <p class="note" style="margin-top:2px;">Остаётся на вашем устройстве, ничего не загружается.</p>
        <input type="file" id="fileInput" accept="application/pdf" />
      </div>
      <p class="note" id="fileInfo" style="display:none;"></p>
      <p class="note" id="loadingInfo" style="display:none;">Рендеринг миниатюр страниц&hellip;</p>

      <div class="thumb-grid" id="thumbGrid" style="display:none;"></div>

      <button id="saveBtn" disabled style="margin-top:20px;">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="M7 10l5 5 5-5"/><path d="M12 15V3"/></svg>
        Сохранить PDF
      </button>
      <div class="result-box" id="result" style="display:none;"></div>
    </div>

    <div class="panel" style="margin-top:32px;">
      <h3 style="margin-top:0;">Как это работает</h3>
      <p class="note" style="margin-top:0;">
        Миниатюры рендерятся из вашего PDF полностью в браузере. Нажмите на крестик на странице, чтобы отметить её для удаления, нажмите ещё раз, чтобы отменить. Используйте стрелки вверх и вниз, чтобы изменить положение страницы. Ничего не фиксируется, пока вы не нажмёте «Сохранить PDF».
      </p>
    </div>
''',
  scripts=['../../js/i18n-runtime.js','../../js/utils.js','../../js/vendor/pdf-lib.min.js','MODULE:../../js/app-pdf-organize.js','../../js/nav.js','../../js/theme-toggle.js','../../js/lang-switcher.js','../../js/bg-blobs.js'],
)
print("organize-pdf added")

# ---------------- add-page-numbers ----------------
PAGES['add-page-numbers.html'] = dict(
  title="Добавление номеров страниц в PDF онлайн бесплатно | norito",
  desc="Пронумеруйте каждую страницу PDF. Выберите положение, формат, начальный номер и размер шрифта. Работает полностью в вашем браузере, файлы никогда не загружаются.",
  jsonld_name="Добавление номеров страниц в PDF",
  jsonld_desc="Пронумеруйте каждую страницу PDF. Выберите положение, формат, начальный номер и размер шрифта. Работает полностью в вашем браузере.",
  faq=[
    ("Загружаются ли мои PDF-файлы куда-либо?", "Нет. Номера страниц добавляются полностью в вашем браузере с помощью JavaScript. Ваши файлы никогда не покидают устройство и не попадают на сервер."),
    ("Могу ли я начать нумерацию не с 1?", "Да. Задайте начальный номер, какой вам нужен, это полезно, когда PDF продолжает нумерацию другого документа."),
    ("Могу ли я изменить, где появляются номера?", "Да. Выберите любой угол или центр сверху/снизу в выпадающем списке положения перед применением."),
    ("Нумеруются ли все страницы?", "Да, каждая страница получает номер по порядку. Выбор отдельных страниц для пропуска пока не поддерживается."),
    ("Могу ли я добавить номера страниц в PDF, защищённый паролем?", "Пока нет. Инструмент не может прочитать PDF, защищённый паролем или зашифрованный, и покажет ошибку. Сначала снимите пароль с помощью программы для чтения PDF."),
  ],
  icon_class="c-rose",
  icon_svg='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M10 12h2v6"/><path d="M10 18h4"/></svg>',
  breadcrumb="Номера страниц",
  h1="Добавление номеров страниц в PDF",
  lede="Пронумеруйте каждую страницу. Выберите, где они располагаются, как выглядят и с какого номера начинаются. Ничего не загружается, всё происходит на вашем устройстве.",
  main_extra='''
    <div class="panel">
      <div class="dropzone" id="drop">
        <svg class="dz-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M16 16l-4-4-4 4"/><path d="M12 12v9"/><path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3"/></svg>
        <p><strong>Нажмите, чтобы выбрать PDF-файл</strong>, или перетащите его сюда</p>
        <p class="note" style="margin-top:2px;">Остаётся на вашем устройстве, ничего не загружается.</p>
        <input type="file" id="fileInput" accept="application/pdf" />
      </div>
      <p class="note" id="fileInfo" style="display:none;"></p>

      <div class="field-row" style="margin-top:20px;">
        <div class="field">
          <label for="positionSelect">Положение</label>
          <select id="positionSelect" disabled>
            <option value="bottom-center" selected>Снизу по центру</option>
            <option value="bottom-left">Снизу слева</option>
            <option value="bottom-right">Снизу справа</option>
            <option value="top-center">Сверху по центру</option>
            <option value="top-left">Сверху слева</option>
            <option value="top-right">Сверху справа</option>
          </select>
        </div>
        <div class="field">
          <label for="formatSelect">Формат</label>
          <select id="formatSelect" disabled>
            <option value="n" selected>1, 2, 3&hellip;</option>
            <option value="page-n">Страница 1, Страница 2&hellip;</option>
            <option value="page-n-of-total">Страница 1 из N</option>
            <option value="n-slash-total">1 / N</option>
          </select>
        </div>
      </div>

      <div class="field-row" style="margin-bottom:20px;">
        <div class="field">
          <label for="startNumber">Начальный номер</label>
          <input type="number" id="startNumber" value="1" min="0" step="1" disabled />
        </div>
        <div class="field">
          <label for="fontSize">Размер шрифта</label>
          <input type="number" id="fontSize" value="10" min="6" max="72" step="1" disabled />
        </div>
      </div>

      <button id="applyBtn" disabled>
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="M7 10l5 5 5-5"/><path d="M12 15V3"/></svg>
        Добавить номера страниц
      </button>
      <div class="result-box" id="result" style="display:none;"></div>
    </div>

    <div class="panel" style="margin-top:32px;">
      <h3 style="margin-top:0;">Как это работает</h3>
      <p class="note" style="margin-top:0;">
        Номера страниц наносятся прямо на каждую страницу стандартным шрифтом, полностью в вашем браузере. Форматы «из N» и «/ N» используют общее число страниц документа, а сама последовательность номеров начинается с заданного вами начального числа.
      </p>
    </div>
''',
  scripts=['../../js/i18n-runtime.js','../../js/utils.js','../../js/vendor/pdf-lib.min.js','../../js/app-pdf-page-numbers.js','../../js/nav.js','../../js/theme-toggle.js','../../js/lang-switcher.js','../../js/bg-blobs.js'],
)
print("add-page-numbers added")

# ---------------- add-watermark ----------------
PAGES['add-watermark.html'] = dict(
  title="Добавление водяного знака в PDF онлайн бесплатно | norito",
  desc="Нанесите диагональный текстовый водяной знак на каждую страницу, например CONFIDENTIAL или DRAFT. Выберите текст, размер, цвет, прозрачность и угол. Работает полностью в вашем браузере.",
  jsonld_name="Добавление водяного знака в PDF",
  jsonld_desc="Нанесите диагональный текстовый водяной знак на каждую страницу. Работает полностью в вашем браузере.",
  faq=[
    ("Загружаются ли мои PDF-файлы куда-либо?", "Нет. Водяной знак добавляется полностью в вашем браузере с помощью JavaScript. Ваши файлы никогда не покидают устройство и не попадают на сервер."),
    ("Могу ли я изменить угол и прозрачность водяного знака?", "Да. Задайте угол поворота в градусах и прозрачность в процентах: 0% невидимо, 100% полностью непрозрачно."),
    ("Наносится ли водяной знак на каждую страницу?", "Да, один и тот же водяной знак наносится на каждую страницу документа."),
    ("Могу ли я удалить водяной знак, добавленный этим инструментом?", "Не с помощью этого инструмента: водяной знак становится частью содержимого страницы. Сохраните копию исходного файла, если он может понадобиться вам без водяного знака позже."),
    ("Могу ли я добавить водяной знак на PDF, защищённый паролем?", "Пока нет. Инструмент не может прочитать PDF, защищённый паролем или зашифрованный, и покажет ошибку. Сначала снимите пароль с помощью программы для чтения PDF."),
  ],
  icon_class="c-indigo",
  icon_svg='<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="m9 15 6-6"/><path d="m9 9 6 6"/></svg>',
  breadcrumb="Добавление водяного знака",
  h1="Добавление водяного знака в PDF",
  lede="Нанесите диагональный текстовый водяной знак на каждую страницу, например CONFIDENTIAL или DRAFT. Выберите текст, размер, цвет, прозрачность и угол. Ничего не загружается, всё происходит на вашем устройстве.",
  main_extra='''
    <div class="panel">
      <div class="dropzone" id="drop">
        <svg class="dz-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M16 16l-4-4-4 4"/><path d="M12 12v9"/><path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3"/></svg>
        <p><strong>Нажмите, чтобы выбрать PDF-файл</strong>, или перетащите его сюда</p>
        <p class="note" style="margin-top:2px;">Остаётся на вашем устройстве, ничего не загружается.</p>
        <input type="file" id="fileInput" accept="application/pdf" />
      </div>
      <p class="note" id="fileInfo" style="display:none;"></p>

      <div class="field" style="margin-top:20px;">
        <label>Предпросмотр</label>
        <div class="wm-preview-page">
          <span class="wm-preview-text" id="wmPreviewText">CONFIDENTIAL</span>
        </div>
        <p class="note" style="margin-top:6px;">Приблизительная оценка на стандартной странице, реальный результат зависит от фактического размера страниц вашего PDF.</p>
      </div>

      <div class="field" style="margin-top:20px; margin-bottom:20px;">
        <label for="wmText">Текст водяного знака</label>
        <input type="text" id="wmText" value="CONFIDENTIAL" maxlength="60" disabled />
      </div>

      <div class="field-row">
        <div class="field">
          <label for="wmSize">Размер шрифта</label>
          <input type="number" id="wmSize" value="48" min="8" max="200" step="1" disabled />
        </div>
        <div class="field">
          <label for="wmOpacity">Прозрачность (%)</label>
          <input type="number" id="wmOpacity" value="30" min="1" max="100" step="1" disabled />
        </div>
        <div class="field">
          <label for="wmAngle">Угол (&deg;)</label>
          <input type="number" id="wmAngle" value="45" min="-180" max="180" step="1" disabled />
        </div>
        <div class="field" style="max-width:100px;">
          <label for="wmColor">Цвет</label>
          <input type="color" id="wmColor" value="#808080" disabled />
        </div>
      </div>

      <button id="applyBtn" disabled style="margin-top:4px;">
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="M7 10l5 5 5-5"/><path d="M12 15V3"/></svg>
        Добавить водяной знак
      </button>
      <div class="result-box" id="result" style="display:none;"></div>
    </div>

    <div class="panel" style="margin-top:32px;">
      <h3 style="margin-top:0;">Как это работает</h3>
      <p class="note" style="margin-top:0;">
        Водяной знак наносится как настоящий текст прямо на каждую страницу: по центру, повёрнутым и полупрозрачным, полностью в вашем браузере. Он становится частью самой страницы, поэтому сохраните копию оригинала, если позже вам может понадобиться версия без водяного знака.
      </p>
    </div>
''',
  scripts=['../../js/i18n-runtime.js','../../js/utils.js','../../js/vendor/pdf-lib.min.js','../../js/app-pdf-watermark.js','../../js/nav.js','../../js/theme-toggle.js','../../js/lang-switcher.js','../../js/bg-blobs.js'],
)
print("add-watermark added")
