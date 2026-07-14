(function () {
  const els = {
    input: document.getElementById("jwtInput"),
    result: document.getElementById("result"),
    headerOut: document.getElementById("headerOut"),
    payloadOut: document.getElementById("payloadOut"),
    claimsPanel: document.getElementById("claimsPanel"),
    claimsList: document.getElementById("claimsList"),
  };

  const ICONS = {
    ok: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"/><path d="M22 4 12 14.01l-3-3"/></svg>',
    error: '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><path d="M12 8v4M12 16h.01"/></svg>',
  };

  function setResult(html, state) {
    if (!html) { els.result.style.display = "none"; return; }
    els.result.innerHTML = `<span class="r-icon">${ICONS[state] || ""}</span><span class="r-body">${html}</span>`;
    els.result.style.display = "flex";
    els.result.classList.remove("ok", "error");
    if (state) els.result.classList.add(state);
  }

  function escapeHtml(s) {
    return String(s).replace(/[&<>"']/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;", "'": "&#39;" }[c]));
  }

  // Base64URL decode -> UTF-8 string. JWT segments use the URL-safe alphabet
  // (- and _ instead of + and /) and typically omit padding.
  function base64UrlDecode(str) {
    let s = str.replace(/-/g, "+").replace(/_/g, "/");
    while (s.length % 4) s += "=";
    const binary = atob(s);
    const bytes = new Uint8Array(binary.length);
    for (let i = 0; i < binary.length; i++) bytes[i] = binary.charCodeAt(i);
    return new TextDecoder("utf-8").decode(bytes);
  }

  const KNOWN_CLAIMS = {
    iss: "Issuer", sub: "Subject", aud: "Audience", exp: "Expires", nbf: "Not valid before",
    iat: "Issued at", jti: "JWT ID",
  };

  function fmtTimestamp(n) {
    if (typeof n !== "number") return null;
    const d = new Date(n * 1000);
    if (isNaN(d.getTime())) return null;
    return `${d.toLocaleString()} (${d.toISOString()})`;
  }

  function decode() {
    const raw = els.input.value.trim();
    if (!raw) {
      setResult(null);
      els.claimsPanel.style.display = "none";
      els.headerOut.textContent = "";
      els.payloadOut.textContent = "";
      return;
    }

    const parts = raw.split(".");
    if (parts.length !== 3) {
      setResult("<strong>That doesn't look like a JWT.</strong> A JWT has three dot-separated parts: header.payload.signature.", "error");
      els.claimsPanel.style.display = "none";
      els.headerOut.textContent = "";
      els.payloadOut.textContent = "";
      return;
    }

    let header, payload;
    try {
      header = JSON.parse(base64UrlDecode(parts[0]));
    } catch (e) {
      setResult("<strong>Couldn't decode the header.</strong> It isn't valid Base64URL-encoded JSON.", "error");
      return;
    }
    try {
      payload = JSON.parse(base64UrlDecode(parts[1]));
    } catch (e) {
      setResult("<strong>Couldn't decode the payload.</strong> It isn't valid Base64URL-encoded JSON.", "error");
      return;
    }

    els.headerOut.textContent = JSON.stringify(header, null, 2);
    els.payloadOut.textContent = JSON.stringify(payload, null, 2);

    const rows = [];
    for (const key of Object.keys(KNOWN_CLAIMS)) {
      if (!(key in payload)) continue;
      let display = payload[key];
      if ((key === "exp" || key === "nbf" || key === "iat") && typeof display === "number") {
        display = fmtTimestamp(display) || display;
      } else if (typeof display === "object") {
        display = JSON.stringify(display);
      }
      rows.push(`<div class="meta-row"><span class="meta-label">${KNOWN_CLAIMS[key]} (${key})</span><span class="meta-value">${escapeHtml(String(display))}</span></div>`);
    }
    if (rows.length) {
      els.claimsList.innerHTML = rows.join("");
      els.claimsPanel.style.display = "block";
    } else {
      els.claimsPanel.style.display = "none";
    }

    let expiryNote = "";
    if (typeof payload.exp === "number") {
      const isExpired = payload.exp * 1000 < Date.now();
      expiryNote = isExpired
        ? " This token's <code>exp</code> claim is in the past, it's expired."
        : " This token's <code>exp</code> claim is in the future, it hasn't expired yet.";
    }
    setResult(`<strong>Decoded successfully.</strong> Signature was not verified, this only decodes the header and payload.${expiryNote}`, "ok");
  }

  els.input.addEventListener("input", decode);

  // Signature verification deliberately not offered: doing it correctly
  // needs the signing secret or public key, which this tool has no server
  // to check against, and accepting a secret in a public browser tool would
  // be actively bad practice. This only decodes, it never claims to verify.
})();
