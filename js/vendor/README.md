# Vendored libraries

- `qrcode.js` / `qrcode-utf8.js`: kazuhikoarase/qrcode-generator v2.0.4, MIT license.
  https://github.com/kazuhikoarase/qrcode-generator
  Installed via `npm install qrcode-generator` and copied from `dist/`, unmodified.

- `marked.umd.js`: marked v18.0.6, MIT license (see `marked.LICENSE.md`).
  https://github.com/markedjs/marked
  Installed via `npm install marked` and copied from `lib/marked.umd.js`, unmodified.

- `onnxruntime/`: ONNX Runtime Web v1.19.2, Microsoft, MIT license (see the header comment in
  `ort.wasm.min.js`).
  https://github.com/microsoft/onnxruntime
  WebAssembly build of the ONNX inference engine, used to run the Remove Background model
  (`modnet/model_quantized.onnx`) entirely client-side.

- `modnet/`: a quantized MODNet portrait-matting model (`model_quantized.onnx`, ~6.6MB),
  Apache 2.0 license.
  https://github.com/ZHKKKe/MODNet
  MODNet's code, models, and demos are released under Apache 2.0 (the CC BY-NC-SA license
  sometimes associated with the MODNet name applies to a separate benchmark *dataset* the
  authors also publish, not to the model or code). Predicts a real per-pixel alpha matte
  (not a coarse person/background mask), so hair and soft edges come out closer to true
  transparency. Loaded together with `onnxruntime/`, ~18MB combined on first use of Remove
  Background, cached by the browser after that.

- `mediapipe/` (removed): Google's @mediapipe/selfie_segmentation v0.1.1675465747, Apache 2.0
  license. This was the original Remove Background implementation, since replaced by the ONNX
  Runtime Web + MODNet pair above. It sat unused on disk (~12MB) for a while after the swap;
  deleted since nothing referenced it. If you ever need it back:
  `npm install @mediapipe/selfie_segmentation` (or check git history from before it was removed).

- `pdf-lib.min.js`: pdf-lib v1.17.1, MIT license (see `pdf-lib.LICENSE.md`).
  https://github.com/Hopding/pdf-lib
  Installed via `npm install pdf-lib` and copied from `dist/pdf-lib.min.js`, unmodified. UMD
  build, exposes a global `PDFLib` object. Used by the PDF tools suite (merge, split, rotate,
  etc.) to create/modify PDFs entirely client-side, nothing uploaded.

- `pdfjs/`: pdf.js (pdfjs-dist) v6.1.200, Apache 2.0 license (see `pdfjs/pdfjs.LICENSE`).
  https://github.com/mozilla/pdf.js
  Installed via `npm install pdfjs-dist` and copied from `legacy/build/pdf.min.mjs` and
  `legacy/build/pdf.worker.min.mjs`, unmodified. ES module build (no UMD build is published as
  of v4+), so it's loaded via `<script type="module">` and imported directly rather than as a
  plain global like the other vendored libs. Used to rasterize PDF pages to images (PDF to
  JPG/PNG). The "legacy" build is used over the standard one for broader browser compatibility.

- `heic2any/heic2any.min.js`: heic2any v0.0.4, MIT license (see `heic2any/LICENSE.md`).
  https://github.com/alexcorvi/heic2any
  Installed via `npm install heic2any` and copied from `dist/heic2any.min.js`, unmodified. Bundles
  a self-contained (asm.js) build of libheif, no separate .wasm file and no network calls, so it
  decodes HEIC/HEIF entirely client-side. Used by the HEIC to JPG/PNG Converter, loaded lazily
  only on that page since it's ~1.3MB.

- `gif/gif.js` + `gif/gif.worker.js`: gif.js v0.2.0, MIT license (see `gif/gif.js.LICENSE.md`).
  https://github.com/jnordberg/gif.js
  Installed via `npm install gif.js` and copied from `dist/`, unmodified. Encodes an animated GIF
  from a sequence of canvas frames using a Web Worker, so encoding doesn't block the main thread.
  Exposes a global `GIF` constructor; each tool points its `workerScript` option at
  `/js/vendor/gif/gif.worker.js`. Used by GIF Maker, Video to GIF, GIF Compressor, GIF Resizer,
  and Add Text to GIF (the Norito GIF suite).

- `gif/gifuct-js.min.js`: gifuct-js v2.1.2, MIT license (see `gif/gifuct-js.LICENSE.md`).
  https://github.com/matt-way/gifuct-js
  Installed via `npm install gifuct-js`, then bundled into a single browser-ready IIFE with
  `esbuild --bundle --format=iife --global-name=gifuct --minify` (no prebuilt UMD/browser dist is
  published upstream; source is unmodified, only the bundling step is ours). Exposes a global
  `gifuct` object with `parseGIF()`/`decompressFrames()`, used to decode an existing GIF's frames
  (with correct disposal-method handling) for GIF Compressor, GIF Resizer, GIF Splitter, and Add
  Text to GIF.

- `gifsicle/gifsicle.min.js`: gifsicle-wasm-browser v1.5.19, MIT license for the JS/build wrapper
  (see `gifsicle/LICENSE-wrapper-MIT.md`), but the actual compression engine it wraps and ships as
  a compiled WASM binary is **gifsicle itself, GPL-2.0-only** (Eddie Kohler and contributors, see
  `gifsicle/LICENSE-gifsicle-GPL-2.0.md`, fetched verbatim from
  https://github.com/kohler/gifsicle/blob/master/COPYING). This is the same compression engine
  EZGIF's backend runs. https://github.com/renzhezhilu/gifsicle-wasm-browser
  Installed via `npm install gifsicle-wasm-browser` and copied from `dist/gifsicle.min.js`,
  unmodified. It's an ES module (`export default gifsicle`) that spins up a Web Worker running the
  compiled gifsicle binary and talks to it via a CLI-style command string
  (`gifsicle.run({ input, command })`, e.g. `--lossy=40 --colors=64 -O2 in.gif -o /out/out.gif`) —
  the same command-line interface gifsicle exposes to any of its users, not a linked-in library
  call. That "separate process, driven by its normal CLI interface, communicating over a
  message-passing boundary" shape is the standard way commercial products bundle GPL command-line
  tools (ffmpeg.wasm being the best-known example) without the surrounding code itself becoming
  GPL-licensed — GPL-2.0 section 2 explicitly excludes "mere aggregation... on a volume of a
  storage or distribution medium" from its copyleft requirements. Flagged here for the record since
  every other vendored library in this project is MIT/Apache; this is the one GPL exception, used
  only by GIF Compressor for its lossy-compression + optimization pass (frame selection, delay
  editing, and scaling still happen in norito's own code via gif.js/gifuct-js above).
