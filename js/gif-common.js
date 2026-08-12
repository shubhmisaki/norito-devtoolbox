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
