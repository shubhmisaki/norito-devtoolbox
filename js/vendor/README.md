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
