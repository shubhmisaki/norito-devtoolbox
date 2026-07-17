# scratch build script for es/pdf generation, safe to delete
# -*- coding: utf-8 -*-
import os

ROOT = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.path.join(ROOT, "es", "pdf")
os.makedirs(OUT_DIR, exist_ok=True)

HEAD_TOP = '''<!DOCTYPE html>
<html lang="es" dir="ltr">
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
<noscript><link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=Poppins:wght@600;700;800&display=optional" rel="stylesheet" /></noscript>
'''

HEADER_NAV = '''<header class="site">
  <div class="wrap">
    <a class="brand" href="../index.html"><img class="logo logo-word" src="../../assets/norito-wordmark.svg" alt="norito" width="113" height="44" /></a>
        <nav class="site-nav" id="siteNav">
      <div class="nav-group">
        <button type="button" class="nav-cat">Imágenes</button>
        <div class="nav-panel">
          <a href="../compress-image.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-5-5L5 21"/></svg><div class="nav-link-body">Comprimir imagen<span>Reduce a un tamaño de archivo objetivo</span></div></a>
          <a href="../placeholder-generator.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><path d="M3 7V3h4M17 3h4v4M21 17v4h-4M7 21H3v-4"/></svg><div class="nav-link-body">Generador de marcadores<span>Imágenes de relleno a medida</span></div></a>
          <a href="../remove-background.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><circle cx="6" cy="6" r="3"/><circle cx="6" cy="18" r="3"/><path d="M20 4 8.12 15.88M14.47 14.48 20 20M8.12 8.12 12 12"/></svg><div class="nav-link-body">Quitar fondo<span>Recorta a una persona de una foto</span></div></a>
        </div>
      </div>
      <div class="nav-group">
        <button type="button" class="nav-cat">Desarrollo</button>
        <div class="nav-panel">
          <a href="../test-file-generator.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M9 13h6M9 17h6"/></svg><div class="nav-link-body">Generador de archivos de prueba<span>Archivos de relleno del tamaño exacto</span></div></a>
          <a href="../json-formatter.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><path d="M8 3a3 3 0 0 0-3 3v3a2 2 0 0 1-2 2 2 2 0 0 1 2 2v3a3 3 0 0 0 3 3"/><path d="M16 3a3 3 0 0 1 3 3v3a2 2 0 0 0 2 2 2 2 0 0 0-2 2v3a3 3 0 0 1-3 3"/></svg><div class="nav-link-body">Formateador JSON<span>Formatea, valida y minifica</span></div></a>
          <a href="../markdown-editor.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><path d="M12 20h9"/><path d="M16.5 3.5a2.121 2.121 0 0 1 3 3L7 19l-4 1 1-4Z"/></svg><div class="nav-link-body">Editor Markdown<span>Vista previa en vivo, exporta a .md/.html</span></div></a>
        </div>
      </div>
      <div class="nav-group">
        <button type="button" class="nav-cat">Texto</button>
        <div class="nav-panel">
          <a href="../seo-slug-generator.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><path d="M10 13a5 5 0 0 0 7.07 0l2-2a5 5 0 0 0-7.07-7.07l-1.5 1.5"/><path d="M14 11a5 5 0 0 0-7.07 0l-2 2a5 5 0 0 0 7.07 7.07l1.5-1.5"/></svg><div class="nav-link-body">Generador de slugs SEO<span>URLs limpias a partir de títulos</span></div></a>
          <a href="../limited-text-generator.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><path d="M4 7V4h16v3"/><path d="M9 20h6"/><path d="M12 4v16"/></svg><div class="nav-link-body">Generador de texto limitado<span>Texto de relleno con longitud exacta</span></div></a>
        </div>
      </div>
      <div class="nav-group">
        <button type="button" class="nav-cat">Utilidades</button>
        <div class="nav-panel">
          <a href="../password-generator.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><rect x="5" y="11" width="14" height="9" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg><div class="nav-link-body">Generador de contraseñas<span>Contraseñas y frases aleatorias</span></div></a>
          <a href="../qr-code-generator.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><rect x="3" y="3" width="7" height="7"/><rect x="14" y="3" width="7" height="7"/><rect x="3" y="14" width="7" height="7"/><path d="M14 14h3v3h-3zM19 17h2M17 19v2M14 19h.01M19 14h.01"/></svg><div class="nav-link-body">Generador de códigos QR<span>Colores personalizados, corrección de errores</span></div></a>
        </div>
      </div>

            <div class="nav-group">
        <a class="nav-cat" href="../../pdf/">PDF <span class="nav-en-tag">EN</span></a>
        <div class="nav-panel">
          <a href="../../pdf/merge-pdf.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><path d="M15.5 2H8.6c-.4 0-.8.2-1.1.5-.3.3-.5.7-.5 1.1v12.8c0 .4.2.8.5 1.1.3.3.7.5 1.1.5h9.8c.4 0 .8-.2 1.1-.5.3-.3.5-.7.5-1.1V6.5L15.5 2z"/><path d="M3 7.6v12.8c0 .4.2.8.5 1.1.3.3.7.5 1.1.5h9.8"/><path d="M15 2v5h5"/></svg><div class="nav-link-body">Merge PDF<span>Combine multiple PDFs into one</span></div></a>
          <a href="../../pdf/split-pdf.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><circle cx="6" cy="6" r="3"/><path d="M8.12 8.12 12 12"/><path d="M20 4 8.12 15.88"/><circle cx="6" cy="18" r="3"/><path d="M14.8 14.8 20 20"/></svg><div class="nav-link-body">Split PDF<span>Pull out pages or split into files</span></div></a>
          <a href="../../pdf/rotate-pdf.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><path d="M21 12a9 9 0 1 1-9-9c2.52 0 4.93 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/></svg><div class="nav-link-body">Rotate PDF<span>Fix sideways or upside-down pages</span></div></a>
          <a href="../../pdf/pdf-to-image.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/></svg><div class="nav-link-body">PDF to JPG/PNG<span>Turn pages into images</span></div></a>
          <a href="../../pdf/jpg-png-to-pdf.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><circle cx="10" cy="13" r="2"/><path d="m20 17-1.5-1.5a2 2 0 0 0-2.83 0L9 22"/></svg><div class="nav-link-body">JPG/PNG to PDF<span>Combine images into one PDF</span></div></a>
          <a href="../../pdf/organize-pdf.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><rect width="7" height="7" x="3" y="3" rx="1"/><rect width="7" height="7" x="14" y="3" rx="1"/><rect width="7" height="7" x="14" y="14" rx="1"/><rect width="7" height="7" x="3" y="14" rx="1"/></svg><div class="nav-link-body">Delete &amp; Reorder Pages<span>Delete or rearrange pages</span></div></a>
          <a href="../../pdf/add-page-numbers.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M10 12h2v6"/><path d="M10 18h4"/></svg><div class="nav-link-body">Add Page Numbers<span>Number every page</span></div></a>
          <a href="../../pdf/add-watermark.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="m9 15 6-6"/><path d="m9 9 6 6"/></svg><div class="nav-link-body">Add Watermark<span>Stamp text across every page</span></div></a>
          <a href="../../pdf/extract-text.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M8 13h8M8 17h5"/></svg><div class="nav-link-body">Extract Text<span>Pull text out of a PDF</span></div></a>
          <a href="../../pdf/compress-pdf.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="m10 12-2 2 2 2M14 12l2 2-2 2"/></svg><div class="nav-link-body">Compress PDF<span>Shrink a large PDF's file size</span></div></a>
          <a href="../../pdf/sign-pdf.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/></svg><div class="nav-link-body">Sign PDF<span>Draw or type a signature</span></div></a>
        </div>
      </div>
            <div class="nav-group">
        <a class="nav-cat" href="../../seo/">SEO <span class="nav-en-tag">EN</span></a>
        <div class="nav-panel">
          <a href="../../seo/meta-tag-generator.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><path d="M4 7V4h16v3"/><path d="M9 20h6"/><path d="M12 4v16"/></svg><div class="nav-link-body">Meta Tag Generator<span>Title, description, OG, Twitter tags</span></div></a>
          <a href="../../seo/utm-builder.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><rect x="2" y="3" width="20" height="14" rx="2"/><path d="M8 21h8"/><path d="M12 17v4"/></svg><div class="nav-link-body">UTM Builder<span>Build campaign tracking URLs</span></div></a>
          <a href="../../seo/robots-txt-generator.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><rect x="3" y="11" width="18" height="10" rx="2"/><circle cx="8.5" cy="16" r="1.5"/><circle cx="15.5" cy="16" r="1.5"/><path d="M7 11V8a5 5 0 0 1 10 0v3"/></svg><div class="nav-link-body">Robots.txt Generator<span>Allow/disallow rules, sitemap ref</span></div></a>
          <a href="../../seo/sitemap-generator.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg><div class="nav-link-body">Sitemap Generator<span>URLs in, sitemap.xml out</span></div></a>
        </div>
      </div>
            <div class="nav-group">
        <a class="nav-cat" href="../../design/">Design <span class="nav-en-tag">EN</span></a>
        <div class="nav-panel">
          <a href="../../design/css-gradient-generator.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><path d="M12 22c4.97 0 9-4.03 9-9-4.97 0-9 4.03-9 9Z"/><path d="M12 22C7.03 22 3 17.97 3 13c4.97 0 9 4.03 9 9Z"/><path d="M12 13c0-5 4-8 4-8s-8 0-8 8"/></svg><div class="nav-link-body">CSS Gradient Generator<span>Linear or radial, copy the CSS</span></div></a>
          <a href="../../design/box-shadow-generator.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><rect x="4" y="4" width="13" height="13" rx="2"/><path d="M9 9h13v13H9z" opacity="0.35"/></svg><div class="nav-link-body">Box Shadow Generator<span>Single or layered shadows</span></div></a>
          <a href="../../design/border-radius-generator.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><path d="M4 12V8a4 4 0 0 1 4-4h8a4 4 0 0 1 4 4v8a4 4 0 0 1-4 4H8"/><path d="M4 12v4"/></svg><div class="nav-link-body">Border Radius Generator<span>Per-corner radius, copy the CSS</span></div></a>
          <a href="../../design/favicon-generator.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="3"/></svg><div class="nav-link-body">Favicon Generator<span>Every favicon size you need</span></div></a>
          <a href="../../design/color-palette-extractor.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><circle cx="13.5" cy="6.5" r=".5"/><circle cx="17.5" cy="10.5" r=".5"/><circle cx="8.5" cy="7.5" r=".5"/><circle cx="6.5" cy="12.5" r=".5"/><path d="M12 2C6.5 2 2 6.5 2 12s4.5 10 10 10c.926 0 1.648-.746 1.648-1.688 0-.437-.18-.835-.437-1.125-.29-.289-.438-.652-.438-1.125a1.64 1.64 0 0 1 1.668-1.668h1.996c3.051 0 5.555-2.503 5.555-5.554C21.965 6.012 17.461 2 12 2z"/></svg><div class="nav-link-body">Color Palette Extractor<span>Pull dominant colors from an image</span></div></a>
          <a href="../../design/contrast-checker.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><path d="m9 18 6-12"/><circle cx="6" cy="18" r="3"/><circle cx="18" cy="6" r="3"/></svg><div class="nav-link-body">Contrast Checker<span>WCAG contrast ratio, AA/AAA pass</span></div></a>
          <a href="../../design/color-converter.html"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round" width="15" height="15"><circle cx="13.5" cy="6.5" r=".5"/><path d="M12 2a10 10 0 1 0 10 10 4 4 0 0 1-4-4V6a4 4 0 0 0-4-4Z"/><circle cx="17.5" cy="10.5" r=".5"/><circle cx="6.5" cy="12.5" r=".5"/></svg><div class="nav-link-body">Color Converter<span>HEX, RGB, HSL, CMYK, live</span></div></a>
        </div>
      </div>
          </nav>
      <button type="button" class="search-trigger" id="searchTrigger" aria-label="Buscar herramientas" title="Buscar herramientas"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg></button>

      <button type="button" class="theme-toggle-btn" aria-label="Toggle dark mode">
        <svg class="theme-icon-moon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3a6 6 0 0 0 9 9 9 9 0 1 1-9-9"/></svg>
        <svg class="theme-icon-sun" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="4"/><path d="M12 2v2M12 20v2M4.93 4.93l1.41 1.41M17.66 17.66l1.41 1.41M2 12h2M20 12h2M6.34 17.66l-1.41 1.41M19.07 4.93l-1.41 1.41"/></svg>
      </button>

      <div class="lang-switch" id="langSwitch">
        <button type="button" class="lang-switch-btn" aria-label="Language / Idioma / 语言 / اللغة / भाषा">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M2 12h20"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
          <span class="lang-switch-current" id="langSwitchCurrent">EN</span>
        </button>
        <div class="lang-switch-panel" id="langSwitchPanel"></div>
      </div>
  </div>
</header>
'''

BG_BLOBS = '''<body>
<div class="bg-blobs" aria-hidden="true">
  <div class="blob blob-1"></div>
  <div class="blob blob-2"></div>
  <div class="blob blob-3"></div>
</div>

'''

FOOTER = '''<footer class="site">
  <div class="wrap">
    <div class="footer-grid">
      <div class="footer-brand">
        <div class="footer-brand-name">norito</div>
        <p class="footer-tagline">Herramientas pequeñas que resuelven un problema molesto cada una. Todo funciona en tu navegador, no se sube nada.</p>
      </div>
      <div class="footer-col">
        <h3>Imágenes</h3>
        <a href="../test-file-generator.html">Archivos de prueba</a>
        <a href="../compress-image.html">Comprimir</a>
        <a href="../placeholder-generator.html">Marcador</a>
        <a href="../remove-background.html">Quitar fondo</a>
        <a href="../qr-code-generator.html">Código QR</a>
      </div>
      <div class="footer-col">
        <h3>Texto y desarrollo</h3>
        <a href="../password-generator.html">Contraseña</a>
        <a href="../seo-slug-generator.html">Slug</a>
        <a href="../limited-text-generator.html">Límite de texto</a>
        <a href="../json-formatter.html">JSON</a>
        <a href="../markdown-editor.html">Markdown</a>
      </div>
    </div>
    <div class="footer-bottom">
      <span>&copy; 2026 norito. Todas las herramientas funcionan localmente en tu navegador.</span>
      <a href="../privacy.html">Política de privacidad</a>
            <a href="../../blog/">Blog</a>
            <a href="../../compare/">Compare</a>
            <a href="../../how-it-works.html">How it Works</a>
      <a href="https://ko-fi.com/shubhmisaki" target="_blank" rel="noopener">Invítame un café</a>
    </div>
  </div>
</footer>
'''

CMDK_BLOCK = '''<div class="cmdk-overlay" id="cmdkOverlay" hidden data-empty-text="Ninguna herramienta coincide con tu búsqueda.">
  <div class="cmdk-modal" role="dialog" aria-modal="true" aria-label="Buscar herramientas">
    <div class="cmdk-input-row">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"/><path d="m21 21-4.3-4.3"/></svg>
      <input type="text" id="cmdkInput" placeholder="Buscar herramientas..." autocomplete="off" />
      <kbd>Esc</kbd>
    </div>
    <div class="cmdk-results" id="cmdkResults"></div>
  </div>
</div>
'''

ADSENSE_COMMENT = '''<!-- AdSense temporarily disabled while investigating a Search Console "possible phishing" security flag. To restore, remove this comment wrapper. -->
<!-- <script async src="https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=ca-pub-4040839176833351" crossorigin="anonymous"></script> -->
'''

def hreflang_block(slug):
    root_url = f"https://norito.in/pdf/{slug}" if slug else "https://norito.in/pdf/"
    langs = ["es", "zh", "ar", "hi", "ru", "ja"]
    lines = [f'<link rel="alternate" hreflang="en" href="{root_url}" />']
    for lg in langs:
        url = f"https://norito.in/{lg}/pdf/{slug}" if slug else f"https://norito.in/{lg}/pdf/"
        lines.append(f'<link rel="alternate" hreflang="{lg}" href="{url}" />')
    lines.append(f'<link rel="alternate" hreflang="x-default" href="{root_url}" />')
    return "\n".join(lines)

def head_meta(slug, title, desc, og_desc=None):
    canonical = f"https://norito.in/es/pdf/{slug}" if slug else "https://norito.in/es/pdf/"
    ogd = og_desc if og_desc else desc
    block = f'''<title>{title}</title>
<meta name="description" content="{desc}" />
<link rel="canonical" href="{canonical}" />
{hreflang_block(slug)}
<meta property="og:type" content="website" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{ogd}" />
<meta property="og:url" content="{canonical}" />
<meta property="og:site_name" content="norito" />
<meta property="og:locale" content="es_ES" />
<meta property="og:image" content="https://norito.in/assets/og-image.png" />
<meta property="og:image:width" content="1200" />
<meta property="og:image:height" content="630" />
<meta name="twitter:card" content="summary_large_image" />
<meta name="twitter:title" content="{title}" />
<meta name="twitter:description" content="{ogd}" />
<meta name="twitter:image" content="https://norito.in/assets/og-image.png" />
<link rel="stylesheet" href="../../css/style.css" />
'''
    return block

STD_PRIVACY_Q = "¿Se suben mis archivos PDF a algún sitio?"
STD_PW_A = "Todavía no. La herramienta no puede leer PDF protegidos con contraseña o cifrados y mostrará un error, quita la contraseña primero con un lector de PDF."

def ej(s):
    """Escape a string for embedding inside a JSON string value in our ld+json blocks."""
    return s.replace('"', '\\"')

def faq_html(items):
    out = []
    for q, a in items:
        out.append(f'''      <details class="faq-item">
        <summary>{q}</summary>
        <p>{a}</p>
      </details>''')
    return "\n".join(out)

def faq_jsonld(items):
    entries = []
    for q, a in items:
        entries.append(f'''    {{
      "@type": "Question",
      "name": "{ej(q)}",
      "acceptedAnswer": {{
        "@type": "Answer",
        "text": "{ej(a)}"
      }}
    }}''')
    joined = ",\n".join(entries)
    return f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
{joined}
  ]
}}
</script>
'''

def webapp_jsonld(slug, name, desc):
    url = f"https://norito.in/es/pdf/{slug}"
    return f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "WebApplication",
  "name": "{ej(name)}",
  "url": "{url}",
  "description": "{ej(desc)}",
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
    "url": "https://norito.in/es/"
  }}
}}
</script>
'''

DROPZONE_ICON = '<svg class="dz-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round"><path d="M16 16l-4-4-4 4"/><path d="M12 12v9"/><path d="M20.39 18.39A5 5 0 0 0 18 9h-1.26A8 8 0 1 0 3 16.3"/></svg>'
DOWNLOAD_ICON = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><path d="M7 10l5 5 5-5"/><path d="M12 15V3"/></svg>'

def dropzone(text_line, note, multiple=False, accept="application/pdf"):
    mult = " multiple" if multiple else ""
    return f'''      <div class="dropzone" id="drop">
        {DROPZONE_ICON}
        <p>{text_line}</p>
        <p class="note" style="margin-top:2px;">{note}</p>
        <input type="file" id="fileInput" accept="{accept}"{mult} />
      </div>'''

def scripts_block(depth_prefix, extra_lines):
    # extra_lines: list of lines between i18n-runtime.js/utils.js and nav.js
    lines = [f'<script src="{depth_prefix}js/i18n-runtime.js"></script>']
    lines.extend(extra_lines)
    lines.append(f'<script src="{depth_prefix}js/nav.js"></script>')
    lines.append(f'<script src="{depth_prefix}js/theme-toggle.js"></script>')
    lines.append(f'<script src="{depth_prefix}js/lang-switcher.js"></script>')
    lines.append(f'<script src="{depth_prefix}js/bg-blobs.js"></script>')
    return "\n".join(lines)

def assemble(slug, title, desc, jsonld_blocks, main_html, extra_scripts, og_desc=None):
    head = HEAD_TOP + head_meta(slug, title, desc, og_desc)
    head += "\n"
    head += "\n".join(jsonld_blocks)
    head += "\n" + ADSENSE_COMMENT + "</head>\n"
    body = BG_BLOBS + HEADER_NAV + "\n" + main_html + "\n" + FOOTER + "\n"
    scripts = extra_scripts + "\n" + CMDK_BLOCK + '\n<script src="../../js/cmdk.js"></script>\n<script src="/js/sw-register.js" defer></script>\n<script src="/js/install-prompt.js" defer></script>\n'
    return head + body + scripts + "</body>\n</html>\n"

def write_page(slug, content):
    path = os.path.join(OUT_DIR, slug if slug else "index.html")
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    print("wrote", path)

def tool_hero(icon_svg_html, accent_class, breadcrumb, h1, lede_html):
    return f'''    <div class="tool-hero">
    <div class="tool-hero-icon icon-chip {accent_class}">{icon_svg_html}</div>
    <div class="tool-hero-text">
    <p class="breadcrumb"><a href="../index.html">norito</a> / {breadcrumb}</p>
    <h1>{h1}</h1>
    <p class="lede">
      {lede_html}
    </p>
    </div>
  </div>
'''

def how_it_works(text_html):
    return f'''    <div class="panel" style="margin-top:32px;">
      <h3 style="margin-top:0;">Cómo funciona</h3>
      <p class="note" style="margin-top:0;">
        {text_html}
      </p>
    </div>
'''

def faq_section(items):
    return f'''    <div class="faq-list" style="margin-top:32px;">
{faq_html(items)}
    </div>
'''

print("phase 3 loaded ok")

# ============================================================
# merge-pdf.html
# ============================================================
def gen_merge_pdf():
    slug = "merge-pdf.html"
    title = "Unir archivos PDF online gratis | norito"
    desc = "Combina varios archivos PDF en uno solo, en el orden que elijas. Arrastra los archivos, reordénalos y únelos. Funciona por completo en tu navegador, los archivos nunca se suben."
    jsonld = [
        webapp_jsonld(slug, "Unir archivos PDF",
            "Combina varios archivos PDF en uno solo, en el orden que elijas. Funciona por completo en tu navegador."),
    ]
    faq = [
        (STD_PRIVACY_Q, "No. La unión ocurre completamente dentro de tu navegador con JavaScript. Tus archivos nunca salen de tu dispositivo ni tocan un servidor."),
        ("¿Puedo elegir el orden en que se unen los PDF?", "Sí. Añade tus archivos y usa los botones de subir y bajar en cada fila para ordenarlos como quieras antes de unirlos."),
        ("¿Hay un límite de tamaño de archivo o de número de PDF?", "La herramienta no impone un límite estricto. El límite práctico es la memoria disponible en tu navegador: archivos muy grandes o muy numerosos pueden tardar más o dar problemas en dispositivos con poca memoria."),
        ("¿Unir los PDF reduce su calidad?", "No. Las páginas se copian tal cual desde cada archivo de origen, sin volver a renderizar, sin recomprimir y sin pérdida de calidad."),
        ("¿Puedo unir PDF protegidos con contraseña?", STD_PW_A),
    ]
    jsonld.append(faq_jsonld(faq))

    icon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M15.5 2H8.6c-.4 0-.8.2-1.1.5-.3.3-.5.7-.5 1.1v12.8c0 .4.2.8.5 1.1.3.3.7.5 1.1.5h9.8c.4 0 .8-.2 1.1-.5.3-.3.5-.7.5-1.1V6.5L15.5 2z"/><path d="M3 7.6v12.8c0 .4.2.8.5 1.1.3.3.7.5 1.1.5h9.8"/><path d="M15 2v5h5"/></svg>'
    hero = tool_hero(icon, "c-indigo", "Unir PDF", "Unir archivos PDF",
        "Combina varios PDF en un solo archivo, en el orden que elijas. Añade tus archivos,\n      ordénalos y descarga el PDF combinado. No se sube nada, todo ocurre en tu dispositivo.")

    panel = f'''    <div class="panel">
{dropzone("<strong>Haz clic para elegir archivos PDF</strong>, o arrástralos hasta aquí", "Añade dos o más PDF. Se quedan en tu dispositivo, no se sube nada.", multiple=True)}

      <div class="file-list" id="fileList" style="display:none;"></div>

      <button id="mergeBtn" disabled style="margin-top:20px;">
        {DOWNLOAD_ICON}
        Unir PDF
      </button>
      <div class="result-box" id="result" style="display:none;"></div>
    </div>
'''
    hiw = how_it_works("Unir los PDF ocurre por completo en tu navegador con una librería de PDF que funciona\n        en el lado del cliente. Cada página se copia directamente desde tus archivos de origen a un\n        nuevo PDF combinado, así que no hay recompresión ni pérdida de calidad ni se vuelve a\n        renderizar nada. Reordena los archivos con los botones de subir y bajar antes de unirlos,\n        ya que las páginas se combinan en el orden en que aparecen los archivos en la lista.")

    main_html = "<main>\n  <div class=\"wrap\">\n" + hero + "\n" + panel + "\n" + hiw + "\n" + faq_section(faq) + "  </div>\n</main>"

    extra = ['<script src="../../js/utils.js"></script>',
             '<script src="../../js/vendor/pdf-lib.min.js"></script>',
             '<script src="../../js/app-pdf-merge.js"></script>']
    scripts = scripts_block("../../", extra)
    content = assemble(slug, title, desc, jsonld, main_html, scripts)
    write_page(slug, content)

gen_merge_pdf()

# ============================================================
# split-pdf.html
# ============================================================
def gen_split_pdf():
    slug = "split-pdf.html"
    title = "Dividir archivos PDF online gratis | norito"
    desc = "Extrae páginas concretas de un PDF, o divídelo en archivos separados. Introduce rangos de páginas como 1-3, 5, 8-10. Funciona en tu navegador, los archivos nunca se suben."
    jsonld = [webapp_jsonld(slug, "Dividir archivos PDF",
        "Extrae páginas concretas de un PDF, o divídelo en archivos separados. Funciona por completo en tu navegador.")]
    faq = [
        (STD_PRIVACY_Q, "No. La división ocurre completamente dentro de tu navegador con JavaScript. Tus archivos nunca salen de tu dispositivo ni tocan un servidor."),
        ("¿Cómo extraigo solo algunas páginas?", "Escribe los números de página o rangos que quieras, como 1-3, 7, y haz clic en Dividir. Se combinarán en un nuevo PDF en ese orden."),
        ("¿Puedo dividir un PDF en un archivo por página?", 'Sí. Activa "Dividir en archivos separados" y deja el campo de páginas en blanco; cada página se descarga como su propio PDF dentro de un .zip.'),
        ("¿Puedo extraer varios rangos separados a la vez?", 'Sí. Introdúcelos separados por comas, como 1-3, 5, 8-10, y activa "Dividir en archivos separados" para obtener cada grupo como su propio PDF en un .zip.'),
        ("¿Dividir reduce la calidad del PDF?", "No. Las páginas se copian tal cual desde el archivo de origen, sin volver a renderizar, sin recomprimir y sin pérdida de calidad."),
        ("¿Puedo dividir un PDF protegido con contraseña?", STD_PW_A),
    ]
    jsonld.append(faq_jsonld(faq))
    icon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="6" cy="6" r="3"/><path d="M8.12 8.12 12 12"/><path d="M20 4 8.12 15.88"/><circle cx="6" cy="18" r="3"/><path d="M14.8 14.8 20 20"/></svg>'
    hero = tool_hero(icon, "c-rose", "Dividir PDF", "Dividir archivos PDF",
        "Extrae páginas concretas de un PDF, o divídelo por completo. Introduce las páginas que quieras,\n      como 1-3, 5, 8-10, y descarga el resultado. No se sube nada, todo ocurre en tu dispositivo.")
    panel = f'''    <div class="panel">
{dropzone("<strong>Haz clic para elegir un archivo PDF</strong>, o arrástralo hasta aquí", "Se queda en tu dispositivo, no se sube nada.")}
      <p class="note" id="fileInfo" style="display:none;"></p>

      <div class="field" style="margin-top:20px;">
        <label for="pagesInput">Páginas a extraer</label>
        <input type="text" id="pagesInput" placeholder="ej. 1-3, 5, 8-10 &ndash; déjalo en blanco para todas las páginas" disabled />
      </div>

      <div class="option-row" style="margin-bottom:20px;">
        <div>
          <div class="option-label">Dividir en archivos separados</div>
          <div class="option-hint">Desactivado combina tu selección en un solo PDF. Activado crea un archivo por cada grupo indicado arriba (o uno por página, si lo dejas en blanco), agrupados en un .zip.</div>
        </div>
        <label class="switch"><input type="checkbox" id="separateToggle" /><span class="track"></span></label>
      </div>

      <button id="splitBtn" disabled>
        {DOWNLOAD_ICON}
        Dividir PDF
      </button>
      <div class="result-box" id="result" style="display:none;"></div>
    </div>
'''
    hiw = how_it_works("La división ocurre por completo en tu navegador con una librería de PDF que funciona\n        en el lado del cliente. Las páginas se copian directamente desde tu archivo de origen, así que\n        no hay recompresión ni pérdida de calidad ni se vuelven a renderizar. Deja el campo de páginas\n        en blanco para trabajar con todas las páginas, o indica páginas y rangos concretos separados\n        por comas.")
    main_html = "<main>\n  <div class=\"wrap\">\n" + hero + "\n" + panel + "\n" + hiw + "\n" + faq_section(faq) + "  </div>\n</main>"
    extra = ['<script src="../../js/utils.js"></script>',
             '<script src="../../js/vendor/pdf-lib.min.js"></script>',
             '<script src="../../js/app-pdf-split.js"></script>']
    scripts = scripts_block("../../", extra)
    write_page(slug, assemble(slug, title, desc, jsonld, main_html, scripts))

gen_split_pdf()

# ============================================================
# rotate-pdf.html
# ============================================================
def gen_rotate_pdf():
    slug = "rotate-pdf.html"
    title = "Rotar páginas de PDF online gratis | norito"
    desc = "Rota un PDF 90, 180 o 270 grados, todas las páginas o solo las que elijas. Funciona por completo en tu navegador, los archivos nunca se suben."
    jsonld = [webapp_jsonld(slug, "Rotar PDF",
        "Rota un PDF 90, 180 o 270 grados, todas las páginas o solo las que elijas. Funciona por completo en tu navegador.")]
    faq = [
        (STD_PRIVACY_Q, "No. La rotación ocurre completamente dentro de tu navegador con JavaScript. Tus archivos nunca salen de tu dispositivo ni tocan un servidor."),
        ("¿Puedo rotar solo algunas páginas?", "Sí. Escribe los números de página o rangos que quieras, como 1-3, 7, y solo esas páginas se rotarán. Déjalo en blanco para rotar todas las páginas."),
        ("¿Qué pasa si una página ya está rotada?", "La rotación que elijas se aplica sobre la orientación actual de cada página, no se establece desde cero, así que una página ya de lado gira los 90, 180 o 270 grados adicionales esperados en lugar de reiniciarse."),
        ("¿Rotar reduce la calidad del PDF?", "No. La rotación es un cambio de metadatos en cada página; el contenido no se vuelve a renderizar ni a comprimir."),
        ("¿Puedo rotar un PDF protegido con contraseña?", STD_PW_A),
    ]
    jsonld.append(faq_jsonld(faq))
    icon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 1 1-9-9c2.52 0 4.93 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/></svg>'
    hero = tool_hero(icon, "c-teal", "Rotar PDF", "Rotar páginas de PDF",
        "Corrige páginas torcidas o boca abajo. Rota todo el documento o solo las páginas que elijas,\n      y descarga el resultado. No se sube nada, todo ocurre en tu dispositivo.")
    panel = f'''    <div class="panel">
{dropzone("<strong>Haz clic para elegir un archivo PDF</strong>, o arrástralo hasta aquí", "Se queda en tu dispositivo, no se sube nada.")}
      <p class="note" id="fileInfo" style="display:none;"></p>

      <div class="field" style="margin-top:20px;">
        <label>Rotación</label>
        <div class="tabs" id="rotateTabs">
          <button type="button" class="tab active" data-value="90">Rotar 90&deg; a la derecha</button>
          <button type="button" class="tab" data-value="-90">Rotar 90&deg; a la izquierda</button>
          <button type="button" class="tab" data-value="180">Rotar 180&deg;</button>
        </div>
      </div>

      <div class="field" style="margin-top:20px; margin-bottom:20px;">
        <label for="pagesInput">Páginas a rotar</label>
        <input type="text" id="pagesInput" placeholder="ej. 1-3, 5 &ndash; déjalo en blanco para todas las páginas" disabled />
      </div>

      <button id="rotateBtn" disabled>
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="M21 12a9 9 0 1 1-9-9c2.52 0 4.93 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/></svg>
        Rotar PDF
      </button>
      <div class="result-box" id="result" style="display:none;"></div>
    </div>
'''
    hiw = how_it_works("La rotación ocurre por completo en tu navegador con una librería de PDF que funciona\n        en el lado del cliente. La orientación de cada página seleccionada se actualiza sobre su\n        rotación actual, así que el contenido nunca se vuelve a renderizar, solo se gira. Deja el\n        campo de páginas en blanco para rotar todo el documento.")
    main_html = "<main>\n  <div class=\"wrap\">\n" + hero + "\n" + panel + "\n" + hiw + "\n" + faq_section(faq) + "  </div>\n</main>"
    extra = ['<script src="../../js/utils.js"></script>',
             '<script src="../../js/vendor/pdf-lib.min.js"></script>',
             '<script src="../../js/app-pdf-rotate.js"></script>']
    scripts = scripts_block("../../", extra)
    write_page(slug, assemble(slug, title, desc, jsonld, main_html, scripts))

gen_rotate_pdf()

# ============================================================
# pdf-to-image.html
# ============================================================
def gen_pdf_to_image():
    slug = "pdf-to-image.html"
    title = "Convertir PDF a JPG o PNG online gratis | norito"
    desc = "Convierte páginas de PDF en imágenes JPG o PNG. Elige una resolución, selecciona las páginas y descarga. Funciona por completo en tu navegador, los archivos nunca se suben."
    jsonld = [webapp_jsonld(slug, "Convertir PDF a JPG o PNG",
        "Convierte páginas de PDF en imágenes JPG o PNG. Funciona por completo en tu navegador.")]
    faq = [
        (STD_PRIVACY_Q, "No. La conversión ocurre completamente dentro de tu navegador con JavaScript. Tus archivos nunca salen de tu dispositivo ni tocan un servidor."),
        ("¿Qué resolución debería elegir?", "96 DPI está bien para pantallas y uso web, 150 DPI es un valor por defecto adecuado para uso general, y 300 DPI es lo mejor para imprimir o hacer zoom en detalles finos. Mayor resolución significa un archivo más grande."),
        ("¿JPG o PNG, cuál elijo?", "JPG es más ligero y funciona bien para fotos o páginas escaneadas. PNG no tiene pérdida y es mejor para páginas con texto nítido, dibujos lineales o cuando necesitas un fondo transparente."),
        ("¿Puedo convertir solo algunas páginas?", "Sí. Escribe los números de página o rangos que quieras, como 1-3, 7. Déjalo en blanco para convertir todas las páginas."),
        ("¿Qué obtengo si convierto varias páginas?", "Una sola página se descarga como una imagen individual. Dos o más páginas se descargan juntas en un .zip, una imagen por página."),
        ("¿Puedo convertir un PDF protegido con contraseña?", STD_PW_A),
    ]
    jsonld.append(faq_jsonld(faq))
    icon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/></svg>'
    hero = tool_hero(icon, "c-amber", "PDF a JPG/PNG", "Convertir PDF a JPG o PNG",
        "Convierte páginas de PDF en imágenes. Elige un formato y una resolución, selecciona las páginas,\n      y descarga. No se sube nada, todo ocurre en tu dispositivo.")
    panel = f'''    <div class="panel">
{dropzone("<strong>Haz clic para elegir un archivo PDF</strong>, o arrástralo hasta aquí", "Se queda en tu dispositivo, no se sube nada.")}
      <p class="note" id="fileInfo" style="display:none;"></p>

      <div class="field-row" style="margin-top:20px;">
        <div class="field">
          <label for="formatSelect">Formato</label>
          <select id="formatSelect" disabled>
            <option value="jpg" selected>JPG</option>
            <option value="png">PNG</option>
          </select>
        </div>
        <div class="field" id="qualityField">
          <label for="qualitySelect">Calidad</label>
          <select id="qualitySelect" disabled>
            <option value="0.92" selected>Alta</option>
            <option value="0.8">Media</option>
            <option value="0.6">Baja (archivo más pequeño)</option>
          </select>
        </div>
        <div class="field">
          <label for="dpiSelect">Resolución</label>
          <select id="dpiSelect" disabled>
            <option value="96">96 DPI (web)</option>
            <option value="150" selected>150 DPI (por defecto)</option>
            <option value="300">300 DPI (impresión)</option>
          </select>
        </div>
      </div>

      <div class="field" style="margin-top:4px; margin-bottom:20px;">
        <label for="pagesInput">Páginas a convertir</label>
        <input type="text" id="pagesInput" placeholder="ej. 1-3, 5 &ndash; déjalo en blanco para todas las páginas" disabled />
      </div>

      <button id="convertBtn" disabled>
        {DOWNLOAD_ICON}
        Convertir a imágenes
      </button>
      <div class="result-box" id="result" style="display:none;"></div>
    </div>
'''
    hiw = how_it_works("Cada página seleccionada se renderiza en un canvas dentro de tu navegador con la resolución\n        que elijas, y luego se exporta como imagen. No se envía nada a ningún sitio, una librería de\n        renderizado de PDF funciona por completo en el lado del cliente. Una sola página se descarga\n        directamente; varias páginas se agrupan en un .zip.")
    main_html = "<main>\n  <div class=\"wrap\">\n" + hero + "\n" + panel + "\n" + hiw + "\n" + faq_section(faq) + "  </div>\n</main>"
    extra = ['<script src="../../js/utils.js"></script>',
             '<script type="module" src="../../js/app-pdf-to-image.js"></script>']
    scripts = scripts_block("../../", extra)
    write_page(slug, assemble(slug, title, desc, jsonld, main_html, scripts))

gen_pdf_to_image()

# ============================================================
# jpg-png-to-pdf.html
# ============================================================
def gen_jpg_png_to_pdf():
    slug = "jpg-png-to-pdf.html"
    title = "Convertir JPG o PNG a PDF online gratis | norito"
    desc = "Combina una o más imágenes en un solo PDF. Reordénalas, elige un tamaño de página y descarga. Funciona por completo en tu navegador, los archivos nunca se suben."
    jsonld = [webapp_jsonld(slug, "Convertir JPG o PNG a PDF",
        "Combina una o más imágenes en un solo PDF. Funciona por completo en tu navegador.")]
    faq = [
        ("¿Se suben mis imágenes a algún sitio?", "No. La conversión ocurre completamente dentro de tu navegador con JavaScript. Tus archivos nunca salen de tu dispositivo ni tocan un servidor."),
        ("¿Puedo elegir el orden de las páginas?", "Sí. Añade tus imágenes y usa los botones de subir y bajar en cada fila para ordenarlas como quieras antes de convertir."),
        ("¿Qué tamaño de página debería elegir?", '"Ajustar a la imagen" hace que cada página se ajuste a las proporciones propias de esa imagen, lo que suele ser mejor para escaneos y capturas de pantalla. A4 o Carta EE.UU. ajustan la imagen dentro de una página estándar, centrada, algo que suele funcionar mejor para imprimir.'),
        ("¿Qué formatos de imagen son compatibles?", "JPG y PNG se procesan de forma nativa. Otros formatos que tu navegador pueda mostrar, como WebP, se convierten automáticamente antes."),
        ("¿Convertir reduce la calidad de la imagen?", "Las imágenes JPG y PNG se incrustan tal cual en la mayoría de los casos. Algunas imágenes necesitan volver a codificarse para poder incrustarse (algunas variantes de JPEG o formatos que no son JPG/PNG); esas se convierten primero a PNG sin pérdida."),
    ]
    jsonld.append(faq_jsonld(faq))
    icon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><circle cx="10" cy="13" r="2"/><path d="m20 17-1.5-1.5a2 2 0 0 0-2.83 0L9 22"/></svg>'
    hero = tool_hero(icon, "c-purple", "JPG/PNG a PDF", "Convertir JPG o PNG a PDF",
        "Combina una o más imágenes en un solo PDF, en el orden que elijas. No se sube nada,\n      todo ocurre en tu dispositivo.")
    panel = f'''    <div class="panel">
{dropzone("<strong>Haz clic para elegir imágenes</strong>, o arrástralas hasta aquí", "JPG, PNG y la mayoría de los demás formatos de imagen. Se quedan en tu dispositivo, no se sube nada.", multiple=True, accept="image/*")}

      <div class="file-list" id="fileList" style="display:none;"></div>

      <div class="field" style="margin-top:20px; margin-bottom:20px; max-width:320px;">
        <label for="pageSizeSelect">Tamaño de página</label>
        <select id="pageSizeSelect">
          <option value="fit" selected>Ajustar a la imagen</option>
          <option value="a4">A4</option>
          <option value="letter">Carta EE.UU.</option>
        </select>
      </div>

      <button id="convertBtn" disabled>
        {DOWNLOAD_ICON}
        Convertir a PDF
      </button>
      <div class="result-box" id="result" style="display:none;"></div>
    </div>
'''
    hiw = how_it_works("Cada imagen se convierte en una página, añadida en el orden que se muestra arriba. La\n        conversión ocurre por completo en tu navegador con una librería de PDF que funciona en el\n        lado del cliente. JPG y PNG se incrustan directamente siempre que es posible; cualquier otro\n        formato se decodifica y se vuelve a codificar antes para poder incrustarlo.")
    main_html = "<main>\n  <div class=\"wrap\">\n" + hero + "\n" + panel + "\n" + hiw + "\n" + faq_section(faq) + "  </div>\n</main>"
    extra = ['<script src="../../js/utils.js"></script>',
             '<script src="../../js/vendor/pdf-lib.min.js"></script>',
             '<script src="../../js/app-images-to-pdf.js"></script>']
    scripts = scripts_block("../../", extra)
    write_page(slug, assemble(slug, title, desc, jsonld, main_html, scripts))

gen_jpg_png_to_pdf()

# ============================================================
# organize-pdf.html
# ============================================================
def gen_organize_pdf():
    slug = "organize-pdf.html"
    title = "Eliminar y reordenar páginas de PDF online gratis | norito"
    desc = "Ve cada página como una miniatura, elimina las que no necesites y reordena el resto. Funciona por completo en tu navegador, los archivos nunca se suben."
    jsonld = [webapp_jsonld(slug, "Eliminar y reordenar páginas de PDF",
        "Ve cada página como una miniatura, elimina las que no necesites y reordena el resto. Funciona por completo en tu navegador.")]
    faq = [
        (STD_PRIVACY_Q, "No. Todo, incluidas las miniaturas de las páginas, se genera completamente dentro de tu navegador. Tus archivos nunca salen de tu dispositivo ni tocan un servidor."),
        ("¿Cómo elimino una página?", "Haz clic en la X de la miniatura de una página para marcarla para eliminar; se atenúa para mostrar que no se incluirá. Haz clic de nuevo para deshacerlo."),
        ("¿Cómo reordeno las páginas?", "Usa las flechas de subir y bajar debajo de cada miniatura para mover esa página antes o después. El PDF final sigue el orden que se muestra en pantalla."),
        ("¿Puedo eliminar todas las páginas?", "No, un PDF necesita al menos una página, así que el botón Guardar se desactiva si todas las páginas están marcadas para eliminar."),
        ("¿Puedo organizar un PDF protegido con contraseña?", STD_PW_A),
    ]
    jsonld.append(faq_jsonld(faq))
    icon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="7" height="7" x="3" y="3" rx="1"/><rect width="7" height="7" x="14" y="3" rx="1"/><rect width="7" height="7" x="14" y="14" rx="1"/><rect width="7" height="7" x="3" y="14" rx="1"/></svg>'
    hero = tool_hero(icon, "c-coral", "Eliminar y reordenar páginas", "Eliminar y reordenar páginas de PDF",
        "Ve cada página como una miniatura, marca las que no quieras y mueve el resto al orden que\n      necesites. No se sube nada, todo ocurre en tu dispositivo.")
    panel = f'''    <div class="panel">
{dropzone("<strong>Haz clic para elegir un archivo PDF</strong>, o arrástralo hasta aquí", "Se queda en tu dispositivo, no se sube nada.")}
      <p class="note" id="fileInfo" style="display:none;"></p>
      <p class="note" id="loadingInfo" style="display:none;">Generando miniaturas de página&hellip;</p>

      <div class="thumb-grid" id="thumbGrid" style="display:none;"></div>

      <button id="saveBtn" disabled style="margin-top:20px;">
        {DOWNLOAD_ICON}
        Guardar PDF
      </button>
      <div class="result-box" id="result" style="display:none;"></div>
    </div>
'''
    hiw = how_it_works("Las miniaturas se generan a partir de tu PDF por completo en tu navegador. Haz clic en la X de\n        una página para marcarla para eliminar, haz clic de nuevo para deshacerlo. Usa las flechas de\n        subir y bajar para cambiar la posición de una página. Nada se aplica de forma definitiva hasta\n        que haces clic en Guardar PDF.")
    main_html = "<main>\n  <div class=\"wrap\">\n" + hero + "\n" + panel + "\n" + hiw + "\n" + faq_section(faq) + "  </div>\n</main>"
    extra = ['<script src="../../js/utils.js"></script>',
             '<script src="../../js/vendor/pdf-lib.min.js"></script>',
             '<script type="module" src="../../js/app-pdf-organize.js"></script>']
    scripts = scripts_block("../../", extra)
    write_page(slug, assemble(slug, title, desc, jsonld, main_html, scripts))

gen_organize_pdf()

# ============================================================
# add-page-numbers.html
# ============================================================
def gen_add_page_numbers():
    slug = "add-page-numbers.html"
    title = "Añadir números de página a un PDF online gratis | norito"
    desc = "Numera todas las páginas de un PDF. Elige la posición, el formato, el número inicial y el tamaño de fuente. Funciona por completo en tu navegador, los archivos nunca se suben."
    jsonld = [webapp_jsonld(slug, "Añadir números de página a un PDF",
        "Numera todas las páginas de un PDF. Elige la posición, el formato, el número inicial y el tamaño de fuente. Funciona por completo en tu navegador.")]
    faq = [
        (STD_PRIVACY_Q, "No. Los números de página se añaden completamente dentro de tu navegador con JavaScript. Tus archivos nunca salen de tu dispositivo ni tocan un servidor."),
        ("¿Puedo empezar a numerar desde un número distinto de 1?", "Sí. Ajusta el número inicial al que necesites, útil cuando un PDF continúa la numeración de otro documento."),
        ("¿Puedo cambiar dónde aparecen los números?", "Sí. Elige cualquier esquina o el centro superior/inferior en el menú de posición antes de aplicarlo."),
        ("¿Esto numera todas las páginas?", "Sí, cada página recibe un número en orden. Todavía no se puede elegir páginas concretas para saltar."),
        ("¿Puedo añadir números de página a un PDF protegido con contraseña?", STD_PW_A),
    ]
    jsonld.append(faq_jsonld(faq))
    icon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M10 12h2v6"/><path d="M10 18h4"/></svg>'
    hero = tool_hero(icon, "c-rose", "Números de página", "Añadir números de página a un PDF",
        "Numera todas las páginas. Elige dónde van, cómo se ven y desde qué número empiezan. No se sube\n      nada, todo ocurre en tu dispositivo.")
    panel = f'''    <div class="panel">
{dropzone("<strong>Haz clic para elegir un archivo PDF</strong>, o arrástralo hasta aquí", "Se queda en tu dispositivo, no se sube nada.")}
      <p class="note" id="fileInfo" style="display:none;"></p>

      <div class="field-row" style="margin-top:20px;">
        <div class="field">
          <label for="positionSelect">Posición</label>
          <select id="positionSelect" disabled>
            <option value="bottom-center" selected>Centro inferior</option>
            <option value="bottom-left">Izquierda inferior</option>
            <option value="bottom-right">Derecha inferior</option>
            <option value="top-center">Centro superior</option>
            <option value="top-left">Izquierda superior</option>
            <option value="top-right">Derecha superior</option>
          </select>
        </div>
        <div class="field">
          <label for="formatSelect">Formato</label>
          <select id="formatSelect" disabled>
            <option value="n" selected>1, 2, 3&hellip;</option>
            <option value="page-n">Página 1, Página 2&hellip;</option>
            <option value="page-n-of-total">Página 1 de N</option>
            <option value="n-slash-total">1 / N</option>
          </select>
        </div>
      </div>

      <div class="field-row" style="margin-bottom:20px;">
        <div class="field">
          <label for="startNumber">Número inicial</label>
          <input type="number" id="startNumber" value="1" min="0" step="1" disabled />
        </div>
        <div class="field">
          <label for="fontSize">Tamaño de fuente</label>
          <input type="number" id="fontSize" value="10" min="6" max="72" step="1" disabled />
        </div>
      </div>

      <button id="applyBtn" disabled>
        {DOWNLOAD_ICON}
        Añadir números de página
      </button>
      <div class="result-box" id="result" style="display:none;"></div>
    </div>
'''
    hiw = how_it_works('Los números de página se dibujan directamente sobre cada página con una fuente estándar,\n        todo dentro de tu navegador. Los formatos "de N" y "/ N" usan el número total de páginas del\n        documento; la numeración en sí empieza desde el número inicial que hayas indicado.')
    main_html = "<main>\n  <div class=\"wrap\">\n" + hero + "\n" + panel + "\n" + hiw + "\n" + faq_section(faq) + "  </div>\n</main>"
    extra = ['<script src="../../js/utils.js"></script>',
             '<script src="../../js/vendor/pdf-lib.min.js"></script>',
             '<script src="../../js/app-pdf-page-numbers.js"></script>']
    scripts = scripts_block("../../", extra)
    write_page(slug, assemble(slug, title, desc, jsonld, main_html, scripts))

gen_add_page_numbers()

# ============================================================
# add-watermark.html
# ============================================================
def gen_add_watermark():
    slug = "add-watermark.html"
    title = "Añadir una marca de agua a un PDF online gratis | norito"
    desc = "Estampa una marca de agua de texto en diagonal en cada página, como CONFIDENCIAL o BORRADOR. Elige el texto, el tamaño, el color, la opacidad y el ángulo. Funciona por completo en tu navegador."
    jsonld = [webapp_jsonld(slug, "Añadir marca de agua a un PDF",
        "Estampa una marca de agua de texto en diagonal en cada página. Funciona por completo en tu navegador.")]
    faq = [
        (STD_PRIVACY_Q, "No. La marca de agua se añade completamente dentro de tu navegador con JavaScript. Tus archivos nunca salen de tu dispositivo ni tocan un servidor."),
        ("¿Puedo cambiar el ángulo y la transparencia de la marca de agua?", "Sí. Ajusta el ángulo de rotación en grados y la opacidad en porcentaje: 0% es invisible y 100% es totalmente sólida."),
        ("¿La marca de agua se aplica en todas las páginas?", "Sí, la misma marca de agua se estampa en todas las páginas del documento."),
        ("¿Puedo quitar una marca de agua añadida con esta herramienta?", "No con esta herramienta, la marca de agua pasa a formar parte del contenido de la página. Guarda una copia de tu archivo original por si más adelante lo necesitas sin la marca de agua."),
        ("¿Puedo poner una marca de agua a un PDF protegido con contraseña?", STD_PW_A),
    ]
    jsonld.append(faq_jsonld(faq))
    icon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="m9 15 6-6"/><path d="m9 9 6 6"/></svg>'
    hero = tool_hero(icon, "c-indigo", "Marca de agua", "Añadir una marca de agua a un PDF",
        "Estampa una marca de agua de texto en diagonal en cada página, como CONFIDENCIAL o BORRADOR.\n      Elige el texto, el tamaño, el color, la opacidad y el ángulo. No se sube nada, todo ocurre en tu dispositivo.")
    panel = f'''    <div class="panel">
{dropzone("<strong>Haz clic para elegir un archivo PDF</strong>, o arrástralo hasta aquí", "Se queda en tu dispositivo, no se sube nada.")}
      <p class="note" id="fileInfo" style="display:none;"></p>

      <div class="field" style="margin-top:20px;">
        <label>Vista previa</label>
        <div class="wm-preview-page">
          <span class="wm-preview-text" id="wmPreviewText">CONFIDENCIAL</span>
        </div>
        <p class="note" style="margin-top:6px;">Una aproximación sobre una página estándar; el resultado real depende del tamaño real de las páginas de tu PDF.</p>
      </div>

      <div class="field" style="margin-top:20px; margin-bottom:20px;">
        <label for="wmText">Texto de la marca de agua</label>
        <input type="text" id="wmText" value="CONFIDENCIAL" maxlength="60" disabled />
      </div>

      <div class="field-row">
        <div class="field">
          <label for="wmSize">Tamaño de fuente</label>
          <input type="number" id="wmSize" value="48" min="8" max="200" step="1" disabled />
        </div>
        <div class="field">
          <label for="wmOpacity">Opacidad (%)</label>
          <input type="number" id="wmOpacity" value="30" min="1" max="100" step="1" disabled />
        </div>
        <div class="field">
          <label for="wmAngle">Ángulo (&deg;)</label>
          <input type="number" id="wmAngle" value="45" min="-180" max="180" step="1" disabled />
        </div>
        <div class="field" style="max-width:100px;">
          <label for="wmColor">Color</label>
          <input type="color" id="wmColor" value="#808080" disabled />
        </div>
      </div>

      <button id="applyBtn" disabled style="margin-top:4px;">
        {DOWNLOAD_ICON}
        Añadir marca de agua
      </button>
      <div class="result-box" id="result" style="display:none;"></div>
    </div>
'''
    hiw = how_it_works("La marca de agua se dibuja como texto real directamente sobre cada página, centrada, rotada\n        y semitransparente, todo dentro de tu navegador. Pasa a formar parte de la página, así que\n        guarda una copia del original por si más adelante necesitas una versión sin marca de agua.")
    main_html = "<main>\n  <div class=\"wrap\">\n" + hero + "\n" + panel + "\n" + hiw + "\n" + faq_section(faq) + "  </div>\n</main>"
    extra = ['<script src="../../js/utils.js"></script>',
             '<script src="../../js/vendor/pdf-lib.min.js"></script>',
             '<script src="../../js/app-pdf-watermark.js"></script>']
    scripts = scripts_block("../../", extra)
    write_page(slug, assemble(slug, title, desc, jsonld, main_html, scripts))

gen_add_watermark()

# ============================================================
# compress-pdf.html
# ============================================================
COMPRESS_FAQ_SHARED = [
    ("¿Cómo se reduce realmente el archivo?", "Las páginas que contienen texto real no se modifican estructuralmente, solo se recomprimen las fotos incrustadas en ellas con la calidad que elijas. Las páginas que en realidad son solo una gran imagen escaneada (sin texto real) se vuelven a renderizar como un JPEG comprimido en la resolución que elijas. En ambos casos, el archivo se reconstruye a partir de esas piezas más pequeñas."),
    ("¿Mi texto seguirá siendo seleccionable después?", "Sí, en cualquier página con texto real, ese texto nunca se toca, así que sigue siendo seleccionable y buscable. Solo las páginas que ya eran una imagen escaneada plana se vuelven a aplanar, porque en ellas no hay texto real que perder."),
    ("¿Qué pasa si el resultado no es más pequeño?", "Si nada en el PDF se puede reducir de forma segura sin aplanar texto real o dañar visiblemente la calidad, se conserva el archivo original exactamente igual, byte por byte, en lugar de devolver algo más grande o peor."),
]
COMPRESS_RESULT_BOX = '''    <div class="result-box ok" style="margin-bottom:24px;">
      <svg class="r-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>
      <div class="r-body"><strong>Tu texto sigue siendo texto.</strong> Cualquier página con texto real y seleccionable se deja completamente intacta, solo se recomprimen sus fotos incrustadas. Solo las páginas que ya son una gran imagen escaneada se vuelven a aplanar, porque ahí no hay nada que perder. Si un PDF no tiene nada más que reducir de forma segura, recibirás el original sin cambios en lugar de algo más grande.</div>
    </div>
'''

def gen_compress_pdf():
    slug = "compress-pdf.html"
    title = "Comprimir el tamaño de un PDF online gratis | norito"
    desc = "Reduce el tamaño de archivo de un PDF sin convertir el texto en imagen. El texto real sigue siendo seleccionable, solo se recomprimen los escaneos y las fotos incrustadas. Funciona en tu navegador."
    jsonld = [webapp_jsonld(slug, "Comprimir PDF",
        "Reduce el tamaño de archivo de un PDF sin convertir las páginas de texto en imágenes. Funciona por completo en tu navegador.")]
    faq = [(STD_PRIVACY_Q, "No. La compresión ocurre completamente dentro de tu navegador con JavaScript. Tus archivos nunca salen de tu dispositivo ni tocan un servidor.")]
    faq += COMPRESS_FAQ_SHARED
    faq.append(("¿Puedo comprimir un PDF protegido con contraseña?", STD_PW_A))
    jsonld.append(faq_jsonld(faq))
    icon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="m10 12-2 2 2 2M14 12l2 2-2 2"/></svg>'
    hero_body = f'''    <div class="tool-hero">
    <div class="tool-hero-icon icon-chip c-purple">{icon}</div>
    <div class="tool-hero-text">
    <p class="breadcrumb"><a href="../index.html">norito</a> / Comprimir PDF</p>
    <h1>Comprimir el tamaño de un PDF</h1>
    <p class="lede">
      Reduce un PDF grande sin convertir tu texto en imagen. Las páginas con texto real mantienen
      ese texto seleccionable; solo se recomprimen las páginas escaneadas y las fotos incrustadas.
      No se sube nada, todo ocurre en tu dispositivo.
    </p>
    <p class="note">¿Vas a comprimir un PDF para enviarlo por email? Prueba el <a href="compress-pdf-for-email.html">preset para email</a>.</p>
    </div>
  </div>
'''
    panel = f'''    <div class="panel">
{dropzone("<strong>Haz clic para elegir un archivo PDF</strong>, o arrástralo hasta aquí", "Se queda en tu dispositivo, no se sube nada.")}
      <p class="note" id="fileInfo" style="display:none;"></p>

      <div class="field-row" style="margin-top:20px; margin-bottom:20px;">
        <div class="field">
          <label for="dpiSelect">Resolución</label>
          <select id="dpiSelect" disabled>
            <option value="72">72 DPI (más pequeño)</option>
            <option value="100">100 DPI</option>
            <option value="150" selected>150 DPI (equilibrado)</option>
            <option value="200">200 DPI (mayor calidad)</option>
          </select>
        </div>
        <div class="field">
          <label for="qualitySelect">Calidad</label>
          <select id="qualitySelect" disabled>
            <option value="0.9">Alta</option>
            <option value="0.75" selected>Media</option>
            <option value="0.5">Baja (archivo más pequeño)</option>
          </select>
        </div>
      </div>
      <p class="note" style="margin-top:-12px; margin-bottom:20px;">La resolución y la calidad solo afectan a las páginas escaneadas y a las fotos incrustadas; el texto real nunca se modifica.</p>

      <button id="compressBtn" disabled>
        {DOWNLOAD_ICON}
        Comprimir PDF
      </button>
      <div class="result-box" id="result" style="display:none;"></div>
    </div>
'''
    main_html = "<main>\n  <div class=\"wrap\">\n" + hero_body + "\n" + COMPRESS_RESULT_BOX + "\n" + panel + "\n" + faq_section(faq) + "  </div>\n</main>"
    extra = ['<script src="../../js/utils.js"></script>',
             '<script src="../../js/vendor/pdf-lib.min.js"></script>',
             '<script type="module" src="../../js/app-pdf-compress.js"></script>',
             '<script src="../../js/prefill.js"></script>']
    scripts = scripts_block("../../", extra)
    write_page(slug, assemble(slug, title, desc, jsonld, main_html, scripts))

gen_compress_pdf()

# ============================================================
# compress-pdf-for-email.html
# ============================================================
def gen_compress_pdf_for_email():
    slug = "compress-pdf-for-email.html"
    title = "Comprimir PDF para email (menos de 25MB) gratis | norito"
    desc = "Reduce un PDF para que quepa dentro de los límites de adjuntos de email, como los 25MB de Gmail, directamente en tu navegador. El texto real sigue siendo seleccionable, solo se recomprimen las fotos y los escaneos."
    og_desc = "Reduce un PDF para que quepa dentro de los límites de adjuntos de email, como los 25MB de Gmail, directamente en tu navegador."
    jsonld = [webapp_jsonld(slug, "Comprimir PDF para email",
        "Reduce un PDF para que quepa dentro de los límites de adjuntos de email, como los 25MB de Gmail. Funciona por completo en tu navegador.")]
    faq = [
        ("¿Cuál es el límite de tamaño de adjuntos de Gmail?", "25MB por email en Gmail, contando todos los adjuntos juntos. Outlook.com y la mayoría de proveedores tienen un límite similar, entre 20 y 25MB. Si tu PDF pesa más, comprímelo primero o comparte un enlace en su lugar."),
        (STD_PRIVACY_Q, "No. La compresión ocurre completamente dentro de tu navegador con JavaScript. Tus archivos nunca salen de tu dispositivo ni tocan un servidor."),
    ]
    faq += COMPRESS_FAQ_SHARED
    faq.append(("¿Puedo comprimir un PDF protegido con contraseña?", STD_PW_A))
    jsonld.append(faq_jsonld(faq))
    icon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="m10 12-2 2 2 2M14 12l2 2-2 2"/></svg>'
    hero = tool_hero(icon, "c-purple", "Comprimir PDF para email", "Comprimir un PDF para email",
        "Reduce un PDF para que quepa dentro de los límites de adjuntos de email, como el tope de 25MB\n      de Gmail. La resolución y la calidad ya vienen ajustadas a un preset más pequeño; el texto real\n      sigue siendo seleccionable en todo momento. No se sube nada, todo ocurre en tu dispositivo.")
    panel = f'''    <div class="panel">
{dropzone("<strong>Haz clic para elegir un archivo PDF</strong>, o arrástralo hasta aquí", "Se queda en tu dispositivo, no se sube nada.")}
      <p class="note" id="fileInfo" style="display:none;"></p>

      <div class="field-row" style="margin-top:20px; margin-bottom:20px;">
        <div class="field">
          <label for="dpiSelect">Resolución</label>
          <select id="dpiSelect" disabled>
            <option value="72">72 DPI (más pequeño)</option>
            <option value="100" selected>100 DPI (preset para email)</option>
            <option value="150">150 DPI (equilibrado)</option>
            <option value="200">200 DPI (mayor calidad)</option>
          </select>
        </div>
        <div class="field">
          <label for="qualitySelect">Calidad</label>
          <select id="qualitySelect" disabled>
            <option value="0.9">Alta</option>
            <option value="0.75">Media</option>
            <option value="0.5" selected>Baja (archivo más pequeño, preset para email)</option>
          </select>
        </div>
      </div>
      <p class="note" style="margin-top:-12px; margin-bottom:20px;">La resolución y la calidad solo afectan a las páginas escaneadas y a las fotos incrustadas; el texto real nunca se modifica.</p>

      <button id="compressBtn" disabled>
        {DOWNLOAD_ICON}
        Comprimir PDF
      </button>
      <div class="result-box" id="result" style="display:none;"></div>
    </div>
'''
    main_html = "<main>\n  <div class=\"wrap\">\n" + hero + "\n" + COMPRESS_RESULT_BOX + "\n" + panel + "\n" + faq_section(faq) + "  </div>\n</main>"
    extra = ['<script src="../../js/utils.js"></script>',
             '<script src="../../js/vendor/pdf-lib.min.js"></script>',
             '<script type="module" src="../../js/app-pdf-compress.js"></script>',
             '<script src="../../js/prefill.js"></script>']
    scripts = scripts_block("../../", extra)
    write_page(slug, assemble(slug, title, desc, jsonld, main_html, scripts, og_desc=og_desc))

gen_compress_pdf_for_email()

# ============================================================
# extract-text.html
# ============================================================
def gen_extract_text():
    slug = "extract-text.html"
    title = "Extraer texto de un PDF online gratis | norito"
    desc = "Extrae todo el texto de un PDF, previsualízalo, cópialo o descárgalo como archivo .txt. Funciona por completo en tu navegador, los archivos nunca se suben."
    jsonld = [webapp_jsonld(slug, "Extraer texto de un PDF",
        "Extrae todo el texto de un PDF, previsualízalo, cópialo o descárgalo como archivo .txt. Funciona por completo en tu navegador.")]
    faq = [
        (STD_PRIVACY_Q, "No. El texto se extrae completamente dentro de tu navegador con JavaScript. Tus archivos nunca salen de tu dispositivo ni tocan un servidor."),
        ("¿Funciona con un PDF escaneado?", "No, por sí solo no. Esta herramienta lee el texto que ya está incrustado en el PDF; una página escaneada es solo una imagen, así que no hay texto que extraer a menos que ya se haya pasado por OCR."),
        ("¿El formato, como columnas o tablas, se mantiene limpio?", "En general sí, pero los diseños complejos (páginas con varias columnas, tablas) pueden salir en un orden de lectura inesperado, ya que los PDF no guardan el texto en una estructura estricta de arriba abajo."),
        ("¿Puedo extraer texto de un PDF protegido con contraseña?", STD_PW_A),
    ]
    jsonld.append(faq_jsonld(faq))
    icon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M8 13h8M8 17h5"/></svg>'
    hero = tool_hero(icon, "c-teal", "Extraer texto", "Extraer texto de un PDF",
        "Extrae todo el texto de un PDF, previsualízalo, cópialo o descárgalo como archivo .txt. No se\n      sube nada, todo ocurre en tu dispositivo.")
    panel = f'''    <div class="panel">
{dropzone("<strong>Haz clic para elegir un archivo PDF</strong>, o arrástralo hasta aquí", "Se queda en tu dispositivo, no se sube nada.")}
      <p class="note" id="fileInfo" style="display:none;"></p>
      <p class="note" id="loadingInfo" style="display:none;">Extrayendo texto&hellip;</p>

      <div class="option-row" id="markersRow" style="display:none;">
        <div>
          <div class="option-label">Incluir marcadores de página</div>
          <div class="option-hint">Añade una línea "--- Página N ---" antes del texto de cada página.</div>
        </div>
        <label class="switch"><input type="checkbox" id="pageMarkers" checked /><span class="track"></span></label>
      </div>

      <div class="field" id="previewField" style="display:none; margin-top:12px;">
        <label for="textOutput">Texto extraído</label>
        <textarea id="textOutput" class="mono-area" rows="14" readonly></textarea>
      </div>

      <div id="actionsRow" style="display:none; gap:10px; flex-wrap:wrap;" class="hero-actions">
        <button id="copyBtn" type="button">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><rect width="14" height="14" x="8" y="8" rx="2"/><path d="M4 16c-1.1 0-2-.9-2-2V4c0-1.1.9-2 2-2h10c1.1 0 2 .9 2 2"/></svg>
          Copiar texto
        </button>
        <button id="downloadBtn" type="button">
          {DOWNLOAD_ICON}
          Descargar .txt
        </button>
      </div>
      <div class="result-box" id="result" style="display:none;"></div>
    </div>
'''
    main_html = "<main>\n  <div class=\"wrap\">\n" + hero + "\n" + panel + "\n" + faq_section(faq) + "  </div>\n</main>"
    extra = ['<script src="../../js/utils.js"></script>',
             '<script type="module" src="../../js/app-pdf-extract-text.js"></script>']
    scripts = scripts_block("../../", extra)
    write_page(slug, assemble(slug, title, desc, jsonld, main_html, scripts))

gen_extract_text()

# ============================================================
# sign-pdf.html
# ============================================================
def gen_sign_pdf():
    slug = "sign-pdf.html"
    title = "Firmar un PDF online gratis | norito"
    desc = "Añade tu firma a un PDF dibujándola o escribiendo tu nombre. Colócala en cualquier página y descarga. Funciona por completo en tu navegador, no se sube nada."
    jsonld = [webapp_jsonld(slug, "Firmar PDF",
        "Añade tu firma a un PDF dibujándola o escribiendo tu nombre, y colócala en cualquier página. Funciona por completo en tu navegador.")]
    faq = [
        (STD_PRIVACY_Q, "No. La firma ocurre completamente dentro de tu navegador con JavaScript. Tus archivos nunca salen de tu dispositivo ni tocan un servidor."),
        ("¿Es esta una firma electrónica con validez legal?", "Esta herramienta dibuja una imagen de tu firma sobre la página; no añade firma criptográfica, certificados ni registros de auditoría. Está pensada para firmas informales, no para documentos que requieren una firma electrónica certificada legalmente."),
        ("¿Puedo dibujar mi firma con el ratón?", "Sí, haz clic y arrastra (o usa el dedo en una pantalla táctil) en el panel de dibujo. También puedes simplemente escribir tu nombre en un estilo cursivo."),
        ("¿Puedo firmar más de una página?", 'Sí. Activa "Firmar todas las páginas" para estampar la misma firma en todas las páginas a la vez, o déjalo desactivado para colocarla solo en la página que elijas.'),
        ("¿Puedo firmar un PDF protegido con contraseña?", STD_PW_A),
    ]
    jsonld.append(faq_jsonld(faq))
    icon = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/></svg>'
    hero = tool_hero(icon, "c-amber", "Firmar PDF", "Firmar un PDF",
        "Dibuja tu firma o escribe tu nombre, colócala en cualquier página y descarga la copia firmada.\n      No se sube nada, todo ocurre en tu dispositivo.")
    panel = f'''    <div class="panel">
{dropzone("<strong>Haz clic para elegir un archivo PDF</strong>, o arrástralo hasta aquí", "Se queda en tu dispositivo, no se sube nada.")}
      <p class="note" id="fileInfo" style="display:none;"></p>

      <div class="field" style="margin-top:20px;">
        <label>Tu firma</label>
        <div class="tabs" id="sigTabs">
          <button type="button" class="tab active" data-value="draw">Dibujarla</button>
          <button type="button" class="tab" data-value="type">Escribirla</button>
        </div>
      </div>

      <div id="drawPanel" style="margin-top:12px;">
        <div class="sig-pad-wrap">
          <canvas id="sigCanvas" width="500" height="180"></canvas>
        </div>
        <button type="button" id="clearSigBtn" class="secondary" style="margin-top:8px; padding:7px 14px; font-size:0.85rem;" disabled>Borrar</button>
      </div>

      <div id="typePanel" style="margin-top:12px; display:none;">
        <div class="field-row">
          <div class="field">
            <label for="sigText">Tu nombre</label>
            <input type="text" id="sigText" placeholder="ej. María López" disabled />
          </div>
          <div class="field">
            <label for="sigStyle">Estilo</label>
            <select id="sigStyle" disabled>
              <option value="'Nothing You Could Do', cursive">Escritura cotidiana</option>
              <option value="'La Belle Aurore', cursive">Firma clásica</option>
              <option value="'Reenie Beanie', cursive">Garabato rápido</option>
              <option value="'Homemade Apple', cursive">Rotulador</option>
              <option value="'Kristi', cursive">Caligrafía fluida</option>
            </select>
          </div>
        </div>
        <p id="sigPreview" class="sig-type-preview">Tu nombre</p>
      </div>

      <div class="field-row" style="margin-top:20px; margin-bottom:20px;">
        <div class="field">
          <label for="pageSelect">Página a firmar</label>
          <select id="pageSelect" disabled></select>
        </div>
        <div class="field">
          <label for="positionSelect">Posición</label>
          <select id="positionSelect" disabled>
            <option value="bottom-right" selected>Derecha inferior</option>
            <option value="bottom-center">Centro inferior</option>
            <option value="bottom-left">Izquierda inferior</option>
            <option value="top-right">Derecha superior</option>
            <option value="top-center">Centro superior</option>
            <option value="top-left">Izquierda superior</option>
          </select>
        </div>
        <div class="field">
          <label for="sizeInput">Ancho (pt)</label>
          <input type="number" id="sizeInput" value="150" min="40" max="400" disabled />
        </div>
      </div>

      <div class="option-row" style="margin-bottom:20px;">
        <div>
          <div class="option-label">Firmar todas las páginas</div>
          <div class="option-hint">Coloca la misma firma en todas las páginas en lugar de solo en la seleccionada arriba.</div>
        </div>
        <label class="switch"><input type="checkbox" id="signAllPages" disabled /><span class="track"></span></label>
      </div>

      <button id="applyBtn" disabled>
        <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="16" height="16"><path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/></svg>
        Firmar PDF
      </button>
      <div class="result-box" id="result" style="display:none;"></div>
    </div>

    <div class="result-box error" style="margin-top:24px;">
      <svg class="r-icon" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/></svg>
      <div class="r-body"><strong>No es una firma electrónica certificada legalmente.</strong> Esto dibuja una imagen de tu firma sobre la página, no añade firma criptográfica ni un registro de auditoría. Vale para firmas informales, no para documentos que requieren una firma electrónica certificada.</div>
    </div>
'''
    main_html = "<main>\n  <div class=\"wrap\">\n" + hero + "\n" + panel + "\n" + faq_section(faq) + "  </div>\n</main>"
    extra = ['<script src="../../js/utils.js"></script>',
             '<script src="../../js/vendor/pdf-lib.min.js"></script>',
             '<script src="../../js/app-pdf-sign.js"></script>']
    scripts = scripts_block("../../", extra)
    write_page(slug, assemble(slug, title, desc, jsonld, main_html, scripts))

gen_sign_pdf()

# ============================================================
# index.html
# ============================================================
def collectionpage_jsonld(name, url, desc, site_url, has_part):
    parts = []
    for pname, purl in has_part:
        parts.append(f'    {{ "@type": "WebApplication", "name": "{ej(pname)}", "url": "{purl}" }}')
    joined = ",\n".join(parts)
    return f'''<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "CollectionPage",
  "name": "{ej(name)}",
  "url": "{url}",
  "description": "{ej(desc)}",
  "isPartOf": {{
    "@type": "WebSite",
    "name": "norito",
    "url": "{site_url}"
  }},
  "hasPart": [
{joined}
  ]
}}
</script>
'''

def card(accent, href, icon_svg, h3, p):
    return f'''      <a class="card" data-accent="{accent}" href="{href}">
        <div class="icon-chip c-{accent}">
          {icon_svg}
        </div>
        <h3>{h3}</h3>
        <p>{p}</p>
        <span class="card-link">Abrir herramienta
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M5 12h14M13 6l6 6-6 6"/></svg>
        </span>
      </a>
'''

def gen_index():
    slug = ""
    title = "Herramientas PDF gratis: unir, dividir, rotar, convertir | norito"
    desc = "Une, divide, rota y convierte archivos PDF directamente en tu navegador. Sin subir archivos, sin cuentas, sin marcas de agua. Herramientas PDF gratuitas que mantienen tus archivos en tu dispositivo."
    has_part = [
        ("Unir archivos PDF", "https://norito.in/es/pdf/merge-pdf.html"),
        ("Dividir PDF", "https://norito.in/es/pdf/split-pdf.html"),
        ("Rotar PDF", "https://norito.in/es/pdf/rotate-pdf.html"),
        ("Convertir PDF a JPG o PNG", "https://norito.in/es/pdf/pdf-to-image.html"),
        ("Convertir JPG o PNG a PDF", "https://norito.in/es/pdf/jpg-png-to-pdf.html"),
        ("Eliminar y reordenar páginas de PDF", "https://norito.in/es/pdf/organize-pdf.html"),
        ("Añadir números de página a un PDF", "https://norito.in/es/pdf/add-page-numbers.html"),
        ("Añadir marca de agua a un PDF", "https://norito.in/es/pdf/add-watermark.html"),
        ("Extraer texto de un PDF", "https://norito.in/es/pdf/extract-text.html"),
        ("Comprimir PDF", "https://norito.in/es/pdf/compress-pdf.html"),
        ("Firmar PDF", "https://norito.in/es/pdf/sign-pdf.html"),
    ]
    jsonld = [collectionpage_jsonld("Herramientas PDF", "https://norito.in/es/pdf/",
        "Une, divide, rota y convierte archivos PDF directamente en tu navegador. Sin subir archivos, sin cuentas, sin marcas de agua.",
        "https://norito.in/es/", has_part)]

    cards = []
    cards.append(card("indigo", "merge-pdf.html",
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M15.5 2H8.6c-.4 0-.8.2-1.1.5-.3.3-.5.7-.5 1.1v12.8c0 .4.2.8.5 1.1.3.3.7.5 1.1.5h9.8c.4 0 .8-.2 1.1-.5.3-.3.5-.7.5-1.1V6.5L15.5 2z"/><path d="M3 7.6v12.8c0 .4.2.8.5 1.1.3.3.7.5 1.1.5h9.8"/><path d="M15 2v5h5"/></svg>',
        "Unir PDF", "Combina varios PDF en uno solo, en el orden que prefieras."))
    cards.append(card("rose", "split-pdf.html",
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><circle cx="6" cy="6" r="3"/><path d="M8.12 8.12 12 12"/><path d="M20 4 8.12 15.88"/><circle cx="6" cy="18" r="3"/><path d="M14.8 14.8 20 20"/></svg>',
        "Dividir PDF", "Extrae páginas concretas o divide un PDF en archivos separados."))
    cards.append(card("teal", "rotate-pdf.html",
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M21 12a9 9 0 1 1-9-9c2.52 0 4.93 1 6.74 2.74L21 8"/><path d="M21 3v5h-5"/></svg>',
        "Rotar PDF", "Corrige páginas torcidas o boca abajo, todas o solo algunas."))
    cards.append(card("amber", "pdf-to-image.html",
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="18" height="18" x="3" y="3" rx="2" ry="2"/><circle cx="9" cy="9" r="2"/><path d="m21 15-3.086-3.086a2 2 0 0 0-2.828 0L6 21"/></svg>',
        "PDF a JPG/PNG", "Convierte páginas de PDF en imágenes, elige la resolución y el formato."))
    cards.append(card("purple", "jpg-png-to-pdf.html",
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><circle cx="10" cy="13" r="2"/><path d="m20 17-1.5-1.5a2 2 0 0 0-2.83 0L9 22"/></svg>',
        "JPG/PNG a PDF", "Combina una o más imágenes en un solo PDF."))
    cards.append(card("coral", "organize-pdf.html",
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><rect width="7" height="7" x="3" y="3" rx="1"/><rect width="7" height="7" x="14" y="3" rx="1"/><rect width="7" height="7" x="14" y="14" rx="1"/><rect width="7" height="7" x="3" y="14" rx="1"/></svg>',
        "Eliminar y reordenar páginas", "Ve cada página como una miniatura, elimina algunas y reordena el resto."))
    cards.append(card("rose", "add-page-numbers.html",
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M10 12h2v6"/><path d="M10 18h4"/></svg>',
        "Añadir números de página", "Numera cada página, con la posición, el formato y el número inicial que quieras."))
    cards.append(card("indigo", "add-watermark.html",
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="m9 15 6-6"/><path d="m9 9 6 6"/></svg>',
        "Añadir marca de agua", "Estampa texto en cada página, ajusta el tamaño, el ángulo y la opacidad."))
    cards.append(card("teal", "extract-text.html",
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="M8 13h8M8 17h5"/></svg>',
        "Extraer texto", "Extrae el texto de un PDF para copiarlo o descargarlo como archivo .txt."))
    cards.append(card("purple", "compress-pdf.html",
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6"/><path d="m10 12-2 2 2 2M14 12l2 2-2 2"/></svg>',
        "Comprimir PDF", "Reduce el tamaño de un PDF grande, ideal para documentos escaneados."))
    cards.append(card("amber", "sign-pdf.html",
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"><path d="M17 3a2.85 2.83 0 1 1 4 4L7.5 20.5 2 22l1.5-5.5Z"/></svg>',
        "Firmar PDF", "Dibuja o escribe tu firma, colócala donde quieras y descarga el resultado."))

    main_html = '''<main>
  <div class="wrap">
    <div class="eyebrow"><span>Gratis, sin registro</span><span class="sep">|</span><span>Funciona en tu navegador</span></div>
    <h1>Herramientas PDF que <span class="grad-text">respetan tus archivos</span>.</h1>
    <p class="lede">
      Une, divide, rota y convierte archivos PDF, completamente en tu navegador. No se sube nada
      a ningún sitio, no hay marca de agua y no necesitas crear ninguna cuenta.
    </p>

    <h2 id="tools" style="margin-top:8px;">Herramientas PDF</h2>
    <div class="grid-cards">
''' + "\n".join(cards) + '''    </div>
  </div>
</main>'''

    extra = []
    scripts = scripts_block("../../", extra)
    write_page("index.html", assemble(slug, title, desc, jsonld, main_html, scripts))

gen_index()

print("ALL PAGES GENERATED")
