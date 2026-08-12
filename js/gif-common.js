/* gif-common.js: shared helpers for the Norito GIF tool suite (GIF Maker, Video to
   GIF, GIF Compressor, GIF Resizer, GIF Splitter, Add Text to GIF). Loaded after
   utils.js and the gif.js / gifuct-js vendor scripts, before each tool's own
   app-*.js. Not used by any non-GIF tool, so it stays out of the sitewide
   FOOT-SCRIPTS-HEAD include and is instead included directly on these 6 pages. */

/**
 * Decode an existing GIF file's frames into full-canvas ImageData, handling
 * disposal methods so each returned frame is a complete, ready-to-draw image
 * rather than just the delta patch GIF frames actually store on disk.
 * Returns { width, height, frames: [{ imageData, delay }] }.
 */
async function decodeGifFile(file) {
  const buffer = await file.arrayBuffer();
  const gifData = gifuct.parseGIF(buffer);
  const rawFrames = gifuct.decompressFrames(gifData, true);
  const width = gifData.lsd.width;
  const height = gifData.lsd.height;

  const canvas = document.createElement("canvas");
  canvas.width = width;
  canvas.height = height;
  const ctx = canvas.getContext("2d", { willReadFrequently: true });

  const frames = [];
  let savedForRestore = null;

  for (const frame of rawFrames) {
    if (frame.disposalType === 3 && savedForRestore) {
      ctx.putImageData(savedForRestore, 0, 0);
    }
    const willNeedRestore = frame.disposalType === 3;
    const restoreSnapshot = willNeedRestore ? ctx.getImageData(0, 0, width, height) : null;

    const patchCanvas = document.createElement("canvas");
    patchCanvas.width = frame.dims.width;
    patchCanvas.height = frame.dims.height;
    patchCanvas
      .getContext("2d")
      .putImageData(new ImageData(frame.patch, frame.dims.width, frame.dims.height), 0, 0);
    ctx.drawImage(patchCanvas, frame.dims.left, frame.dims.top);

    frames.push({
      imageData: ctx.getImageData(0, 0, width, height),
      delay: frame.delay > 0 ? frame.delay : 100,
    });

    if (frame.disposalType === 2) {
      ctx.clearRect(frame.dims.left, frame.dims.top, frame.dims.width, frame.dims.height);
    } else if (willNeedRestore) {
      savedForRestore = restoreSnapshot;
    }
  }

  return { width, height, frames };
}

/**
 * Encode a sequence of canvases (or ImageData, via drawImageDataToCanvas
 * first) into an animated GIF blob using gif.js, wrapped as a Promise.
 * frames: [{ canvas, delay }]. onProgress(fraction) is optional.
 */
function encodeGif(frames, { width, height, quality = 10, onProgress } = {}) {
  return new Promise((resolve, reject) => {
    const gif = new GIF({
      workers: 2,
      quality,
      width,
      height,
      workerScript: "/js/vendor/gif/gif.worker.js",
    });
    gif.on("progress", (f) => { if (onProgress) onProgress(f); });
    gif.on("finished", (blob) => resolve(blob));
    try {
      for (const f of frames) {
        gif.addFrame(f.canvas, { delay: f.delay, copy: true });
      }
      gif.render();
    } catch (err) {
      reject(err);
    }
  });
}

function imageDataToCanvas(imageData) {
  const canvas = document.createElement("canvas");
  canvas.width = imageData.width;
  canvas.height = imageData.height;
  canvas.getContext("2d").putImageData(imageData, 0, 0);
  return canvas;
}

/* ---------------------------------------------------------------------
   Frame strip: an interactive thumbnail row with per-frame delay,
   reorder (move up/down), and remove controls, used by GIF Maker, GIF
   Compressor, GIF Resizer, and Add Text to GIF so you can actually see
   what you're working with instead of only tweaking global settings.
   ------------------------------------------------------------------- */

/** Pick whatever image-ish source a frame object carries: a canvas
 * (freshly drawn), an <img> (not yet rasterized, e.g. GIF Maker's
 * uploads), or raw ImageData (decoded GIF frames). */
function frameSourceEl(f) {
  if (f.canvas) return f.canvas;
  if (f.img) return f.img;
  if (f.imageData) return imageDataToCanvas(f.imageData);
  return null;
}

function frameSourceSize(el) {
  return { w: el.naturalWidth || el.width || 1, h: el.naturalHeight || el.height || 1 };
}

/**
 * Render an interactive frame strip into `container`, backed directly by
 * the `frames` array (mutated in place: adds a `delay` field where
 * missing, splices on remove, swaps on reorder). Because it's the same
 * array reference the caller encodes from, edits made here are picked up
 * automatically without any extra plumbing.
 *
 * frames: [{ canvas }] | [{ img }] | [{ imageData }], each optionally
 * already carrying a `delay` (ms).
 * options.onChange(): fires after every edit.
 * options.defaultDelay: fallback delay (ms) for frames that don't have one.
 * options.allowRemove: set false to hide remove buttons (e.g. when a
 * frame count must stay fixed).
 *
 * Returns { refresh() } — call refresh() after changing `frames` from
 * outside (e.g. a bulk toolbar action) so the strip re-renders.
 */
function renderFrameStrip(container, frames, { onChange, defaultDelay = 100, allowRemove = true } = {}) {
  const THUMB = 80;

  function thumbDataUrl(f) {
    const src = frameSourceEl(f);
    if (!src) return "";
    const { w, h } = frameSourceSize(src);
    const scale = Math.min(1, THUMB / Math.max(w, h));
    const t = document.createElement("canvas");
    t.width = Math.max(1, Math.round(w * scale));
    t.height = Math.max(1, Math.round(h * scale));
    t.getContext("2d").drawImage(src, 0, 0, t.width, t.height);
    return t.toDataURL("image/png");
  }

  function render() {
    container.innerHTML = "";
    container.classList.add("frame-strip");
    frames.forEach((f, i) => {
      if (f.delay == null) f.delay = defaultDelay;
      const chip = document.createElement("div");
      chip.className = "frame-chip";
      chip.innerHTML =
        `<img class="frame-thumb" src="${thumbDataUrl(f)}" alt="Frame ${i + 1}" width="80" height="80">` +
        `<span class="frame-index">#${i + 1}</span>` +
        `<label class="frame-delay-label">Delay<input type="number" class="frame-delay-input" min="10" max="30000" step="10" value="${f.delay}"><span>ms</span></label>` +
        `<div class="frame-actions">` +
        `<button type="button" class="frame-move-up" aria-label="Move frame ${i + 1} earlier"${i === 0 ? " disabled" : ""}>&uarr;</button>` +
        `<button type="button" class="frame-move-down" aria-label="Move frame ${i + 1} later"${i === frames.length - 1 ? " disabled" : ""}>&darr;</button>` +
        (allowRemove ? `<button type="button" class="frame-remove" aria-label="Remove frame ${i + 1}"${frames.length <= 1 ? " disabled" : ""}>&times;</button>` : "") +
        `</div>`;

      chip.querySelector(".frame-delay-input").addEventListener("change", (e) => {
        const v = Math.max(10, Math.min(30000, Number(e.target.value) || defaultDelay));
        f.delay = v;
        e.target.value = v;
        if (onChange) onChange();
      });
      chip.querySelector(".frame-move-up").addEventListener("click", () => {
        if (i === 0) return;
        [frames[i - 1], frames[i]] = [frames[i], frames[i - 1]];
        render();
        if (onChange) onChange();
      });
      chip.querySelector(".frame-move-down").addEventListener("click", () => {
        if (i === frames.length - 1) return;
        [frames[i + 1], frames[i]] = [frames[i], frames[i + 1]];
        render();
        if (onChange) onChange();
      });
      if (allowRemove) {
        chip.querySelector(".frame-remove").addEventListener("click", () => {
          if (frames.length <= 1) return; // keep at least one frame
          frames.splice(i, 1);
          render();
          if (onChange) onChange();
        });
      }
      container.appendChild(chip);
    });
  }

  render();
  return { refresh: render };
}

/** Set every frame's delay to `ms` (clamped 10-30000). Call the frame
 * strip's refresh() afterward to reflect it in the UI. */
function bulkSetDelay(frames, ms) {
  const v = Math.max(10, Math.min(30000, Number(ms) || 100));
  frames.forEach((f) => { f.delay = v; });
}

/** Return a new array keeping only every Nth frame, folding each dropped
 * frame's delay into the frame kept just before it so the total playback
 * duration is preserved. Does not mutate `frames`. */
function bulkKeepEveryNth(frames, n) {
  n = Math.max(1, Math.round(n) || 1);
  if (n <= 1) return frames.slice();
  const out = [];
  for (let i = 0; i < frames.length; i += n) {
    const group = frames.slice(i, i + n);
    const totalDelay = group.reduce((sum, f) => sum + (f.delay || 100), 0);
    out.push(Object.assign({}, group[0], { delay: totalDelay }));
  }
  return out;
}

/* ---------------------------------------------------------------------
   Real compression via gifsicle (WASM), used by GIF Compressor. See
   js/vendor/README.md for the license note (gifsicle itself is GPL-2.0,
   run in an isolated Worker via its normal CLI interface, not linked
   into norito's own code).
   ------------------------------------------------------------------- */

/**
 * Run a GIF blob through gifsicle-wasm for real lossy compression and
 * frame-difference optimization, the same techniques EZGIF's backend
 * uses. Requires js/vendor/gifsicle/gifsicle.min.js to have been loaded
 * as an ES module and exposed as window.gifsicle (see gif-compressor.html).
 * Returns a Promise<Blob>.
 */
async function compressWithGifsicle(gifBlob, { lossy = 0, colors = 0, optimize = true } = {}) {
  if (!window.gifsicle) {
    throw new Error("The compression engine didn't finish loading. Reload the page and try again.");
  }
  const flags = [];
  if (optimize) flags.push("-O2");
  if (lossy > 0) flags.push(`--lossy=${Math.round(lossy)}`);
  if (colors > 0) flags.push(`--colors=${Math.round(colors)}`);
  const command = `${flags.join(" ")} in.gif -o /out/out.gif`.trim();

  const outFiles = await window.gifsicle.run({
    input: [{ file: gifBlob, name: "in.gif" }],
    command: [command],
  });
  if (!outFiles || !outFiles.length) {
    throw new Error("Compression didn't produce any output. Try a lower lossy level.");
  }
  return outFiles[0];
}
