(function () {
  const els = {
    title: document.getElementById("metaTitle"),
    description: document.getElementById("metaDescription"),
    url: document.getElementById("metaUrl"),
    siteName: document.getElementById("metaSiteName"),
    image: document.getElementById("metaImage"),
    twitterHandle: document.getElementById("metaTwitterHandle"),
    output: document.getElementById("output"),
    copyBtn: document.getElementById("copyBtn"),
    titleCount: document.getElementById("titleCount"),
    descCount: document.getElementById("descCount"),
  };

  function escapeAttr(s) {
    return String(s || "").replace(/&/g, "&amp;").replace(/"/g, "&quot;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
  }

  function generate() {
    const title = els.title.value.trim();
    const desc = els.description.value.trim();
    const url = els.url.value.trim();
    const site = els.siteName.value.trim();
    const image = els.image.value.trim();
    const twitter = els.twitterHandle.value.trim();

    els.titleCount.textContent = `${title.length}/60`;
    els.titleCount.classList.toggle("limit-over", title.length > 60);
    els.descCount.textContent = `${desc.length}/160`;
    els.descCount.classList.toggle("limit-over", desc.length > 160);

    const lines = [];
    if (title) lines.push(`<title>${escapeAttr(title)}</title>`);
    if (desc) lines.push(`<meta name="description" content="${escapeAttr(desc)}" />`);
    if (url) lines.push(`<link rel="canonical" href="${escapeAttr(url)}" />`);

    lines.push(`<meta property="og:type" content="website" />`);
    if (title) lines.push(`<meta property="og:title" content="${escapeAttr(title)}" />`);
    if (desc) lines.push(`<meta property="og:description" content="${escapeAttr(desc)}" />`);
    if (url) lines.push(`<meta property="og:url" content="${escapeAttr(url)}" />`);
    if (site) lines.push(`<meta property="og:site_name" content="${escapeAttr(site)}" />`);
    if (image) lines.push(`<meta property="og:image" content="${escapeAttr(image)}" />`);

    lines.push(`<meta name="twitter:card" content="${image ? "summary_large_image" : "summary"}" />`);
    if (twitter) lines.push(`<meta name="twitter:site" content="${escapeAttr(twitter.startsWith("@") ? twitter : "@" + twitter)}" />`);
    if (title) lines.push(`<meta name="twitter:title" content="${escapeAttr(title)}" />`);
    if (desc) lines.push(`<meta name="twitter:description" content="${escapeAttr(desc)}" />`);
    if (image) lines.push(`<meta name="twitter:image" content="${escapeAttr(image)}" />`);

    els.output.textContent = lines.join("\n");
  }

  [els.title, els.description, els.url, els.siteName, els.image, els.twitterHandle].forEach((el) =>
    el.addEventListener("input", generate)
  );
  generate();

  els.copyBtn.addEventListener("click", async () => {
    if (!els.output.textContent) return;
    try {
      await navigator.clipboard.writeText(els.output.textContent);
      const original = els.copyBtn.textContent;
      els.copyBtn.textContent = "Copied!";
      setTimeout(() => { els.copyBtn.textContent = original; }, 1500);
    } catch (e) { /* clipboard unavailable, silently ignore */ }
  });
})();
