# Vendored libraries

- `qrcode.js` / `qrcode-utf8.js`: kazuhikoarase/qrcode-generator v2.0.4, MIT license.
  https://github.com/kazuhikoarase/qrcode-generator
  Installed via `npm install qrcode-generator` and copied from `dist/`, unmodified.

- `marked.umd.js`: marked v18.0.6, MIT license (see `marked.LICENSE.md`).
  https://github.com/markedjs/marked
  Installed via `npm install marked` and copied from `lib/marked.umd.js`, unmodified.

- `mediapipe/`: Google's @mediapipe/selfie_segmentation v0.1.1675465747, Apache 2.0 license.
  https://github.com/google-ai-edge/mediapipe
  Installed via `npm install @mediapipe/selfie_segmentation` and copied unmodified. Only loads
  ~5.5MB (one WASM variant + a ~250KB model) on first use of the Remove Background tool, cached
  by the browser after that.
