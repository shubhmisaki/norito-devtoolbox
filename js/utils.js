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
  // Auto-label any <input type="file"> nested in this dropzone, using the
  // dropzone's own visible instruction text ("Click to choose an image, or
  // drag and drop it here", etc.) as the accessible name. Fixes a real gap:
  // the file input is usually visually hidden or covered by the styled
  // dropzone, so a keyboard/screen-reader user tabbing directly to it heard
  // nothing but "file input, no file selected". Doing this here (rather
  // than hardcoding aria-label in every tool's HTML, in every locale) means
  // it automatically picks up each locale's own already-translated
  // instruction text instead of needing a second, separately-maintained
  // English-only label. Skipped entirely if the input already has its own
  // aria-label/aria-labelledby, or if there's no usable text to derive one
  // from.
  const fileInput = el.querySelector('input[type="file"]');
  if (fileInput && !fileInput.getAttribute("aria-label") && !fileInput.getAttribute("aria-labelledby")) {
    const hint = el.querySelector("p:not(.note)");
    const raw = (hint && hint.textContent) || el.textContent || "";
    const label = raw.replace(/\s+/g, " ").trim().slice(0, 150);
    if (label) fileInput.setAttribute("aria-label", label);
  }

  el.addEventListener("dragover", (e) => { e.preventDefault(); el.classList.add("drag"); });
  el.addEventListener("dragleave", (e) => { e.preventDefault(); el.classList.remove("drag"); });
  el.addEventListener("drop", (e) => {
    e.preventDefault();
    el.classList.remove("drag");
    onDrop(e);
  });
}

// ---- File -> decoded <img>, via a blob URL ----
// Centralizes the URL.createObjectURL(file) + `new Image()` + onload/onerror
// boilerplate that used to be an identical (or near-identical) private
// loadImageFile() copy-pasted across 9 app-*.js image tools. Deliberately
// does NOT validate file.type here: callers already do their own
// file.type.startsWith("image/") check with their own tool-specific error
// copy before calling this, so duplicating that here would just produce a
// second, differently-worded error message for the same condition.
//
// Returns { img, url } rather than a bare img: 8 of the 9 original
// copy-pasted versions never revoked the object URL at all (a real, if
// minor, per-session memory leak: the URL and the File data it points to
// stay alive for the page's lifetime, accumulating with every image a
// visitor loads). Handing the url back lets each call site revoke it once
// it's actually done with it:
//   - Tools that only decode the image to draw it into a canvas (compress,
//     resize, convert, remove-metadata, watermark, favicon-generator,
//     remove-bg) can revoke immediately after this promise resolves: once
//     `img.onload` has fired, the decoded bitmap lives independently of the
//     blob URL, so revoking it doesn't affect any later ctx.drawImage() call.
//   - Tools that also display this exact URL as a persistent <img src> on
//     the page (crop-image, watermark-image's stage preview, the color
//     palette extractor's preview) need to hold onto it and revoke the
//     *previous* URL only once a new image replaces it, not right away.
function loadImageFile(file) {
  return new Promise((resolve, reject) => {
    const url = URL.createObjectURL(file);
    const img = new Image();
    img.onload = () => resolve({ img, url });
    img.onerror = () => reject(new Error("That image couldn't be read."));
    img.src = url;
  });
}

// ---- busy-element progress text ----
// Centralizes the "save original content, show busy/progress text, restore
// when done" pattern that was duplicated -- each with its own slightly
// different formatting -- across roughly 20 app-*.js files: some rendered
// `${Math.round(f*100)}%`, some `${i}/${total}`, some just a static
// "Working..." with no progress value at all, and one (organize-pdf)
// targets a separate status paragraph instead of a button. One shared
// helper means every tool's progress text now follows the same
// convention, and a future visual redesign (an actual progress bar/ring,
// say) only has one call site's worth of rendering logic to change instead
// of twenty.
//
// `el` is typically a <button>, but works on any element with textContent
// (organize-pdf's `#loadingInfo` <p>, for example). For buttons, disables
// it and restores its original innerHTML (not just textContent, in case it
// holds an icon) when done() is called; non-button elements are left alone
// other than their text.
function startBusyText(el, label) {
  const isButton = el.tagName === "BUTTON";
  const original = el.innerHTML;
  if (isButton) el.disabled = true;
  el.textContent = `${label}...`;
  return {
    // progress: omit (or pass null/undefined) for a plain "label..." with
    // no value; a 0-1 fraction for "label... N%"; a {current,total} pair
    // for "label... current/total"; or a full custom string for
    // multi-stage flows where the label itself changes between stages
    // (Compress PDF's "Analyzing pages..." -> "Recompressing images..."),
    // used verbatim.
    update(progress) {
      if (progress == null) {
        el.textContent = `${label}...`;
      } else if (typeof progress === "number") {
        el.textContent = `${label}... ${Math.round(progress * 100)}%`;
      } else if (typeof progress === "string") {
        el.textContent = progress;
      } else if (typeof progress.current === "number" && typeof progress.total === "number") {
        el.textContent = `${label}... ${progress.current}/${progress.total}`;
      }
    },
    // Switches to a new stage label for multi-stage flows (Video to GIF's
    // "Capturing frames..." -> "Encoding...", Compress PDF's "Analyzing
    // pages..." -> "Recompressing images..." -> "Rasterizing scanned
    // pages...") without losing the original saved content done() restores.
    relabel(newLabel) {
      label = newLabel;
      el.textContent = `${label}...`;
    },
    done() {
      if (isButton) el.disabled = false;
      el.innerHTML = original;
    },
  };
}

// Export for both browser (globals) and Node (module.exports), so the same
// file can be unit-tested headlessly.
if (typeof module !== "undefined" && module.exports) {
  module.exports = {
    crc32, crc32Final, concatBytes, u16le, u32le, u16be, u32be,
    textBytes, randomBytes, parseSize, formatBytes, createZip, copyToClipboard,
    wireDragDrop, loadImageFile, startBusyText,
  };
}
