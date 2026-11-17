# 100x mission: progress log (paused 17 Nov 2026)

## Baseline (measured, before changes)
- Traffic (Clarity, last 30 days): 10 human sessions, 8 users, 7 bot sessions. Distribution, not polish, is the main problem.
- Google: about 406 pages indexed (`site:norito.in`). Bing: none found.
- PageSpeed mobile, /json-formatter.html: Performance 67, Accessibility 90, Best Practices 96, SEO 100. FCP 3.4 s, LCP 6.4 s (2.2 s render delay), TBT 150 ms, CLS 0.
- Search Console: not reachable from the connected Chrome profile (neither Google account has the property).

## Commit 1 (pushed, live): `1e0a76c`
- js/third-party.js: GA4 + Clarity load on idle after `load`; ad slots lazy; top banner hidden on phones; Social Bar only on tool pages.
- GA4 events: tool_start, tool_output, search_open, search_select, support_click, pwa_install, js_error.
- Recently used tools (homepage row + first in search); multi-word ranked search.
- compress-image-to-{20kb,50kb,100kb,200kb,500kb,1mb}.html (scripts/gen_compress_presets.py).
- IndexNow: key file, scripts/indexnow.py, .github/workflows/indexnow.yml.
- Contrast: --primary #d6285a (was #ff4d7a, 3.2:1), muted text darkened; 280 toggle switches labelled.
- Markdown preview sanitised; baseline CSP header; privacy policy corrected in 7 languages.
- Removed netlify.toml, js/test_output, deploy zip.

## Commit 2 (local only, NOT pushed, NOT verified live)
- 5 converter pages: png-to-jpg, webp-to-jpg, webp-to-png, jpg-to-webp, png-to-webp (scripts/gen_converter_presets.py).
- Install banner no longer shown to first-time visitors; appears after a completed task.
- js/support-note.js: one Ko-fi note after the 3rd completed task, 90-day snooze, 7 languages.

## Open issues found, not yet fixed
1. Stale CSS/JS after deploy: /css/* and /js/* are cached 7 days with unversioned URLs, so returning visitors get new HTML with old CSS (seen live: --primary still #ff4d7a in a browser with a warm cache). Fix: add ?v=<content hash> to local CSS/JS URLs in scripts/build_site.py.
2. In the connected Chrome, fetch() calls from norito.in pages stopped resolving after the deploy (some pending forever). The same URLs load fine from outside the browser. Not yet determined whether this is the service worker (v3), a browser extension, or the session. Check in a clean profile before trusting the deploy; if it reproduces, suspect sw.js.
3. Ads could not be verified: the connected Chrome hides `.ad-slot` (ad blocker). Check in a browser without one that the 728x90, 300x250 and native units still fill.
4. PageSpeed not re-run after the deploy, so there is no measured "after" yet.
5. GitHub Action run (IndexNow) not checked.

## Not started
- Re-audit pass, final report with before/after scores.
- Mobile visual review (no working headless browser in the sandbox).
