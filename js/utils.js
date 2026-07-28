/* utils.js: shared, dependency-free helpers used across all tools */

// ---- CRC32 (needed for ZIP + PNG chunk construction) ----
const CRC_TABLE = (() => {
  const table = new Uint32Array(256);
  for (let n = 0; n < 256; n++) {
    let c = n;
    for (let k = 0; k < 8; k++) {
      c = (c & 1) ? (0xEDB88320 ^ (c >>> 1)) : (c >>> 1);
    }
    table[n] = c >>> 0;
  }
  return table;
})();

function crc32(bytes, crc = 0xFFFFFFFF) {
  for (let i = 0; i < bytes.length; i++) {
    crc = CRC_TABLE[(crc ^ bytes[i]) & 0xFF] ^ (crc >>> 8);
  }
  return crc; // caller XORs with 0xFFFFFFFF at the end (or feeds back in for streaming)
}

function crc32Final(bytes) {
  return (crc32(bytes) ^ 0xFFFFFFFF) >>> 0;
}

// ---- byte array helpers ----
function concatBytes(chunks) {
  let total = 0;
  for (const c of chunks) total += c.length;
  const out = new Uint8Array(total);
  let offset = 0;
  for (const c of chunks) {
    out.set(c, offset);
    offset += c.length;
  }
  return out;
}

function u16le(n) {
  return new Uint8Array([n & 0xFF, (n >>> 8) & 0xFF]);
}
function u32le(n) {
  return new Uint8Array([n & 0xFF, (n >>> 8) & 0xFF, (n >>> 16) & 0xFF, (n >>> 24) & 0xFF]);
}
function u16be(n) {
  return new Uint8Array([(n >>> 8) & 0xFF, n & 0xFF]);
}
function u32be(n) {
  return new Uint8Array([(n >>> 24) & 0xFF, (n >>> 16) & 0xFF, (n >>> 8) & 0xFF, n & 0xFF]);
}

function textBytes(str) {
  return new TextEncoder().encode(str);
}

function randomBytes(n, mode = "random") {
  const out = new Uint8Array(n);
  if (mode === "blank") {
    // stays all zero
    return out;
  }
  // crypto.getRandomValues has a 65536-byte-per-call limit in browsers
  const CHUNK = 65536;
  for (let off = 0; off < n; off += CHUNK) {
    const len = Math.min(CHUNK, n - off);
    const view = out.subarray(off, off + len);
    if (typeof crypto !== "undefined" && crypto.getRandomValues) {
      crypto.getRandomValues(view);
    } else {
      for (let i = 0; i < len; i++) view[i] = Math.floor(Math.random() * 256);
    }
  }
  return out;
}

// ---- human size parsing / formatting ----
// Uses binary units (1 KB = 1024 B) since that's what OS file pickers / upload
// limits almost always mean in practice.
function parseSize(value, unit) {
  const n = parseFloat(value);
  if (isNaN(n) || n < 0) return null;
  const mult = { B: 1, KB: 1024, MB: 1024 * 1024, GB: 1024 * 1024 * 1024 }[unit];
  if (!mult) return null;
  return Math.round(n * mult);
}

function formatBytes(bytes) {
  if (bytes < 1024) return `${bytes} B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(2)} KB`;
  if (bytes < 1024 * 1024 * 1024) return `${(bytes / (1024 * 1024)).toFixed(2)} MB`;
  return `${(bytes / (1024 * 1024 * 1024)).toFixed(2)} GB`;
}

function downloadBlob(blob, filename) {
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url;
  a.download = filename;
  document.body.appendChild(a);
  a.click();
  a.remove();
  setTimeout(() => URL.revokeObjectURL(url), 2000);
}

// ---- generic ZIP writer (STORE method, no compression) ----
// Bundles multiple named byte arrays into one .zip. No compression is used
// on purpose: the inputs here (split PDFs, etc.) are already dense, and
// skipping DEFLATE keeps this dependency-free and easy to verify. Shares
// the same box-format helpers as generateZip() in generators.js, just
// generalized to any number of real entries instead of one padded one.
function createZip(entries) {
  const modTime = u16le(0x0000);
  const modDate = u16le(0x0021); // arbitrary valid MS-DOS date
  const localParts = [];
  const centralParts = [];
  let offset = 0;

  entries.forEach(({ name, bytes }) => {
    const nameBytes = textBytes(name);
    const crc = crc32Final(bytes);
    const size = bytes.length;

    const localHeader = concatBytes([
      u32le(0x04034b50),
      u16le(20), u16le(0), u16le(0),
      modTime, modDate,
      u32le(crc), u32le(size), u32le(size),
      u16le(nameBytes.length), u16le(0),
      nameBytes,
    ]);
    const localEntry = concatBytes([localHeader, bytes]);
    localParts.push(localEntry);

    const centralHeader = concatBytes([
      u32le(0x02014b50),
      u16le(20), u16le(20), u16le(0), u16le(0),
      modTime, modDate,
      u32le(crc), u32le(size), u32le(size),
      u16le(nameBytes.length), u16le(0), u16le(0),
      u16le(0), u16le(0), u32le(0),
      u32le(offset),
      nameBytes,
    ]);
    centralParts.push(centralHeader);
    offset += localEntry.length;
  });

  const localData = concatBytes(localParts);
  const centralDir = concatBytes(centralParts);
  const eocd = concatBytes([
    u32le(0x06054b50),
    u16le(0), u16le(0),
    u16le(entries.length), u16le(entries.length),
    u32le(centralDir.length),
    u32le(localData.length),
    u16le(0),
  ]);
  return concatBytes([localData, centralDir, eocd]);
}

// ---- clipboard copy with automatic fallback ----
// Centralizes the navigator.clipboard.writeText() + execCommand("copy")
// fallback that used to be duplicated (inconsistently -- some tools had no
// fallback at all, so copying silently did nothing when the Clipboard API
// was unavailable) across ~26 app-*.js files. Throws only if both the
// modern API and the fallback fail.
async function copyToClipboard(text) {
  if (navigator.clipboard && navigator.clipboard.writeText) {
    try {
      await navigator.clipboard.writeText(text);
      return;
    } catch (e) {
      // fall through to the execCommand fallback below
    }
  }
  const ta = document.createElement("textarea");
  ta.value = text;
  ta.style.position = "fixed";
  ta.style.opacity = "0";
  document.body.appendChild(ta);
  ta.select();
  let ok = false;
  try {
    ok = document.execCommand("copy");
  } catch (e) {
    ok = false;
  }
  ta.remove();
  if (!ok) throw new Error("copyToClipboard: no copy mechanism available");
}

// ---- dropzone drag-and-drop wiring ----
// Centralizes the dragenter/dragover/dragleave/drop event wiring (add/remove
// the "drag" hover class, preventDefault so the browser doesn't navigate to
// the dropped file) that used to be copy-pasted, in one of two equivalent
// forms, across 24 app-*.js files. `onDrop(e)` is called only for the actual
// drop, with the hover class already cleared and the default already
// prevented -- callers just read e.dataTransfer.files.
function wireDragDrop(el, onDrop) {
  el.addEventListener("dragover", (e) => { e.preventDefault(); el.classList.add("drag"); });
  el.addEventListener("dragleave", (e) => { e.preventDefault(); el.classList.remove("drag"); });
  el.addEventListener("drop", (e) => {
    e.preventDefault();
    el.classList.remove("drag");
    onDrop(e);
  });
}

// Export for both browser (globals) and Node (module.exports), so the same
// file can be unit-tested headlessly.
if (typeof module !== "undefined" && module.exports) {
  module.exports = {
    crc32, crc32Final, concatBytes, u16le, u32le, u16be, u32be,
    textBytes, randomBytes, parseSize, formatBytes, createZip, copyToClipboard,
    wireDragDrop,
  };
}
