(function () {
  const I18N_C = i18nFor("common");

  // MD5 (RFC 1321). Web Crypto's SubtleCrypto intentionally doesn't
  // implement MD5 (it's broken for security uses), so it's the one
  // algorithm here computed by hand instead of via crypto.subtle.
  function md5(str) {
    function rotl(x, c) { return (x << c) | (x >>> (32 - c)); }
    function toUtf8Bytes(s) {
      return Array.from(new TextEncoder().encode(s));
    }
    const K = new Array(64);
    for (let i = 0; i < 64; i++) K[i] = Math.floor(Math.abs(Math.sin(i + 1)) * 4294967296) >>> 0;
    const S = [
      7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
      5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20, 5, 9, 14, 20,
      4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
      6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21,
    ];
    let bytes = toUtf8Bytes(str);
    const origLenBits = bytes.length * 8;
    bytes.push(0x80);
    while (bytes.length % 64 !== 56) bytes.push(0);
    for (let i = 0; i < 8; i++) bytes.push((origLenBits / Math.pow(2, 8 * i)) & 0xff);

    let a0 = 0x67452301, b0 = 0xefcdab89, c0 = 0x98badcfe, d0 = 0x10325476;
    for (let chunkStart = 0; chunkStart < bytes.length; chunkStart += 64) {
      const M = new Array(16);
      for (let j = 0; j < 16; j++) {
        const o = chunkStart + j * 4;
        M[j] = (bytes[o] | (bytes[o + 1] << 8) | (bytes[o + 2] << 16) | (bytes[o + 3] << 24)) >>> 0;
      }
      let A = a0, B = b0, C = c0, D = d0;
      for (let i = 0; i < 64; i++) {
        let F, g;
        if (i < 16) { F = (B & C) | (~B & D); g = i; }
        else if (i < 32) { F = (D & B) | (~D & C); g = (5 * i + 1) % 16; }
        else if (i < 48) { F = B ^ C ^ D; g = (3 * i + 5) % 16; }
        else { F = C ^ (B | ~D); g = (7 * i) % 16; }
        F = (F + A + K[i] + M[g]) >>> 0;
        A = D; D = C; C = B;
        B = (B + rotl(F, S[i])) >>> 0;
      }
      a0 = (a0 + A) >>> 0;
      b0 = (b0 + B) >>> 0;
      c0 = (c0 + C) >>> 0;
      d0 = (d0 + D) >>> 0;
    }
    function toHexLE(n) {
      let hex = "";
      for (let i = 0; i < 4; i++) hex += ((n >>> (i * 8)) & 0xff).toString(16).padStart(2, "0");
      return hex;
    }
    return toHexLE(a0) + toHexLE(b0) + toHexLE(c0) + toHexLE(d0);
  }

  function bufferToHex(buf) {
    return Array.from(new Uint8Array(buf)).map((b) => b.toString(16).padStart(2, "0")).join("");
  }

  async function subtleHash(algo, str) {
    const bytes = new TextEncoder().encode(str);
    const digest = await crypto.subtle.digest(algo, bytes);
    return bufferToHex(digest);
  }

  const ALGOS = [
    { id: "md5", label: "MD5", fn: (s) => Promise.resolve(md5(s)) },
    { id: "sha1", label: "SHA-1", fn: (s) => subtleHash("SHA-1", s) },
    { id: "sha256", label: "SHA-256", fn: (s) => subtleHash("SHA-256", s) },
    { id: "sha512", label: "SHA-512", fn: (s) => subtleHash("SHA-512", s) },
  ];

  const els = {
    input: document.getElementById("input"),
    list: document.getElementById("hashList"),
  };

  function rowsSkeleton() {
    els.list.innerHTML = ALGOS.map(
      (a) => `
      <div class="slug-row" data-algo="${a.id}">
        <div class="slug-row-text">
          <div class="slug-row-title">${a.label}</div>
          <div class="slug-row-slug" data-out="${a.id}"></div>
        </div>
        <button type="button" class="secondary copy-hash" data-algo="${a.id}">${i18nFor("common").copy || "Copy"}</button>
      </div>`
    ).join("");
  }

  let latestToken = 0;

  async function render() {
    const token = ++latestToken;
    const text = els.input.value;
    if (!text) {
      ALGOS.forEach((a) => {
        const out = els.list.querySelector(`[data-out="${a.id}"]`);
        if (out) out.textContent = "";
      });
      return;
    }
    for (const a of ALGOS) {
      const value = await a.fn(text);
      if (token !== latestToken) return; // a newer keystroke superseded this run
      const out = els.list.querySelector(`[data-out="${a.id}"]`);
      if (out) out.textContent = value;
    }
  }

  els.input.addEventListener("input", render);

  els.list.addEventListener("click", async (e) => {
    const btn = e.target.closest(".copy-hash");
    if (!btn) return;
    const out = els.list.querySelector(`[data-out="${btn.dataset.algo}"]`);
    const value = out ? out.textContent : "";
    if (!value) return;
    try {
      await navigator.clipboard.writeText(value);
    } catch (err) {
      const ta = document.createElement("textarea");
      ta.value = value;
      document.body.appendChild(ta);
      ta.select();
      document.execCommand("copy");
      document.body.removeChild(ta);
    }
    const original = btn.textContent;
    btn.textContent = i18nFor("common").copied || "Copied";
    setTimeout(() => { btn.textContent = original; }, 1200);
  });

  rowsSkeleton();
  render();
})();
