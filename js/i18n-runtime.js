// Tiny shared i18n helper used by every tool script.
//
// On English pages window.NORITO_I18N is never set, so every `I18N.key ||
// "English fallback"` lookup in the app-*.js files falls straight through to
// its English default: this file has zero effect on English pages' behavior.
//
// On a localized page (es/zh/ar), the page loads js/i18n/<lang>.js first,
// which sets window.NORITO_I18N to a dictionary of { fileId: { key: text } }.
// Each app script then reads its own slice of that dictionary and uses fmt()
// below to substitute {placeholders} in translated strings.
function i18nFor(fileId) {
  return (window.NORITO_I18N && window.NORITO_I18N[fileId]) || {};
}

function fmt(str, vars) {
  if (!vars) return str;
  return Object.keys(vars).reduce(
    (acc, k) => acc.split("{" + k + "}").join(vars[k]),
    str
  );
}

// ---- shared "action succeeded" micro-interaction ----
// The button that was clicked briefly pops and shows a plain checkmark
// (small, functional "this worked" feedback that stays out of the way of
// the button's own label), and (optionally) a result panel gets a soft
// success-colored flash around its edge.
//
// The norito axolotl mascot itself lives separately, in a flat/minimal
// comic-style speech bubble that pops out of the bottom corner of the
// screen (see showMascotToast below), instead of being crammed inside
// button text where it was too small to notice. Fully inert under
// prefers-reduced-motion (colors still communicate success, motion doesn't).
//
// Lives here (not utils.js) because this file is the one script every tool
// page loads unconditionally; utils.js is only pulled in by the tools that
// actually need its byte-packing helpers.
const NORITO_CHECK_ICON =
  '<svg viewBox="0 0 20 20" width="16" height="16" xmlns="http://www.w3.org/2000/svg" fill="none">' +
  '<path d="M4 10.5 8 14.5 16 6" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/>' +
  '</svg>';

// The exact same norito axolotl face used in the logo mark (same paths,
// same gradient), just dropped into the mascot toast instead of the header.
// Sizing is left to the .mascot-face CSS (width/height 100%, container
// controls the pixel size) so the toast can render it 20% larger on desktop.
const NORITO_MASCOT_ICON =
  '<svg viewBox="0 0 55 32" xmlns="http://www.w3.org/2000/svg">' +
  '<path fill="#fd6e92" d="M17.726 17.222a.64.64 0 0 1 .267.034c.1.039.175.106.238.176.047.052.147.144.289.268.135.12.3.263.458.407.157.143.316.291.438.426.061.068.119.137.163.203.04.06.089.142.104.234l.021.126-.091.09-.108.108-.036.037-.048.019c-.47.187-.983.428-1.508.674-.52.244-1.053.492-1.548.69v-.001c-.442.22-1 .403-1.515.584-.471.165-.91.331-1.252.53l-.14.088a1 1 0 0 0-.17.187c-.08.106-.171.243-.272.402-.198.312-.437.716-.684 1.084-.246.369-.52.734-.802.98-.271.238-.633.434-1.012.263a.87.87 0 0 1-.519-.61c-.056-.244-.012-.507.06-.742.07-.228.176-.461.284-.67-.377.112-.863.25-1.342.37-.42.107-.84.203-1.181.262-.17.029-.327.05-.457.058a1.4 1.4 0 0 1-.185 0 .6.6 0 0 1-.183-.04c-.225-.102-.402-.232-.508-.398a.68.68 0 0 1-.084-.55c.044-.172.146-.332.264-.474.12-.144.27-.284.43-.414.391-.316.882-.604 1.26-.81l-.31-.11c-.191-.074-.519-.187-.813-.336a2.4 2.4 0 0 1-.428-.266 1.05 1.05 0 0 1-.316-.393.9.9 0 0 1-.012-.68c.152-.35.521-.459.765-.49.448-.06.937.039 1.316.09.635.086 1.294.163 1.94.281.597.11 1.133.262 1.69.316q.101.011.37-.044.264-.058.625-.172a26 26 0 0 0 1.625-.599c.856-.342 1.747-.728 2.347-.976l.494-.197.036-.013zm-7.106 7.383v-.001m28.25-7.42c1.134.567 3.542 1.44 4.817 1.843h.011q.038-.001.11-.011c.095-.013.217-.036.347-.06.25-.049.55-.111.706-.127l.393-.048.448-.063c.312-.045.65-.094.987-.129.664-.07 1.371-.095 1.905.074l.008.002.008.003c.082.032.17.09.238.154.046.043.11.113.15.203l.028.095.01.116c.006.265-.123.482-.299.645-.194.18-.46.313-.723.413a6 6 0 0 1-.757.223c.3.184.593.375.887.568.423.214.73.444.915.675.183.23.284.515.15.777-.127.248-.409.36-.701.388-.3.029-.677-.022-1.107-.157v.002a34 34 0 0 1-1.816-.46c.084.142.166.292.227.442.08.198.137.422.113.644a.82.82 0 0 1-.372.601.6.6 0 0 1-.504.072 1.3 1.3 0 0 1-.414-.205 3.4 3.4 0 0 1-.563-.523 10 10 0 0 1-.75-1.018c-.216-.329-.418-.648-.637-.957a108 108 0 0 1-3.429-1.473v.002c-.521-.233-1.566-.733-2.038-.89l-.157-.052-.013-.165-.017-.199.07-.08c.115-.13.431-.41.734-.67.308-.264.633-.53.774-.633l.124-.09zm4.435 4.654c.298.46.594.922.956 1.34-.362-.419-.658-.881-.956-1.34m-30.095-.036-.035.042q.048-.057.092-.097zm33.95-1.518v.001c.12-.027.249-.06.378-.096v-.001q-.196.056-.378.096m-3.53-1.011v-.001l-.223-.073zm.96-.148c-.221.042-.494.097-.695.128.215-.033.512-.094.74-.136zm-34.137.03.063.012-.062-.013m34.836-.126q-.217.03-.404.048l-.085.014.085-.013q.188-.019.404-.049m3.397-.014-.008-.009-.02-.016zm-.077-.062-.013-.01-.01-.005zm-.091-.052.01.005zl-.019-.005zm-.164-.044-.024-.005q-.022-.005-.046-.008.036.006.07.014m-30.617-1.387a.4.4 0 0 1 .092 0zM6.862 4.766c.228-.048.439.023.617.14.34.221.646.665.908 1.12.268.467.517.997.726 1.428.107.219.202.411.287.563.088.16.15.246.184.278.381.356.882.69 1.366 1.008a4 4 0 0 1-.04-.189c-.056-.314-.073-.678.054-.977a.83.83 0 0 1 .488-.463.89.89 0 0 1 .873.133c.21.17.375.42.51.685.137.269.255.577.363.881.112.311.21.61.317.892.106.28.21.518.322.694q.053.088.236.252.184.161.454.354c.359.257.807.542 1.271.818.93.553 1.904 1.066 2.308 1.255l.187.088-.052.2c-.04.156-.155.637-.278 1.125-.06.24-.123.476-.175.663-.026.093-.05.176-.071.241a1 1 0 0 1-.07.173l-.127.218-.216-.131a10 10 0 0 0-.786-.405l-.843-.4a47 47 0 0 1-2.325-1.216c-.961.215-2.09.446-3.092.48a1.6 1.6 0 0 1-.585-.118c-.1-.041-.205-.098-.291-.176a.52.52 0 0 1-.18-.35 1.05 1.05 0 0 1 .213-.73c.147-.191.351-.328.56-.429.199-.095.419-.166.63-.22-.737-.447-1.447-.906-2.175-1.356-.44.047-1.335.073-2.183.036-.459-.02-.915-.057-1.285-.12a3 3 0 0 1-.497-.12.9.9 0 0 1-.371-.22c-.16-.18-.271-.36-.318-.536a.65.65 0 0 1 .063-.515.9.9 0 0 1 .361-.319c.141-.074.304-.128.47-.168.289-.07.616-.106.907-.123a13 13 0 0 1-.852-.651c-.283-.239-.554-.501-.733-.758-.167-.242-.312-.566-.158-.873a.96.96 0 0 1 .62-.498c.221-.056.47-.031.708.024.242.056.497.15.74.256.213.092.423.197.616.298a9 9 0 0 1-.256-.768 3 3 0 0 1-.099-.481c-.015-.17-.007-.397.126-.578.16-.217.35-.369.573-.415m41.87.087c.159-.093.405-.145.614-.06.315.129.474.384.527.668.051.27.011.574-.057.855a6 6 0 0 1-.252.755c.329-.172.855-.419 1.325-.53.157-.037.317-.062.468-.06.148.001.307.03.443.114.144.09.24.23.28.408q.039.19-.002.422l-.034.158a.8.8 0 0 1-.114.234 2 2 0 0 1-.176.226 7 7 0 0 1-.48.486 9 9 0 0 1-.91.746l-.01.005q.173.027.416.052c.19.022.404.05.605.102.199.05.407.13.571.267a.83.83 0 0 1 .302.613c.014.257-.155.441-.314.556-.166.12-.38.209-.588.276-.4.127-.857.192-1.087.188-.8.082-1.716.064-2.51.042-.397.262-.797.544-1.2.825q-.414.288-.83.564c.254.094.542.222.78.382.211.142.428.34.505.6.087.292-.027.576-.292.822a.7.7 0 0 1-.357.157c-.126.023-.273.03-.428.03a8 8 0 0 1-1.058-.09 21 21 0 0 1-1.717-.323c-.562.29-1.12.598-1.68.91-.586.325-1.176.654-1.77.968l-.157.083-.13-.12c-.035-.033-.054-.07-.057-.077l-.02-.042-.033-.087a7 7 0 0 1-.08-.25 27 27 0 0 1-.453-1.704l-.017-.095c-.002-.015-.01-.065-.003-.114l.016-.11.092-.062c.582-.393 1.341-.808 2.03-1.234.706-.435 1.362-.891 1.813-1.393a.8.8 0 0 0 .109-.206c.047-.115.096-.26.15-.427.103-.327.223-.75.358-1.14.136-.393.299-.79.503-1.084.201-.288.496-.545.895-.489a.74.74 0 0 1 .596.443c.096.214.111.47.098.704a4 4 0 0 1-.088.601c.136-.095.274-.19.404-.283a6.6 6.6 0 0 0 .86-.711l.014-.02.038-.065q.046-.085.1-.202c.067-.145.147-.329.21-.442l.165-.32q.085-.173.175-.366c.12-.254.248-.529.386-.794.271-.521.605-1.056 1.042-1.354l.007-.004zM39.55 15.916l.037.084a.4.4 0 0 1-.04-.095q0 .006.003.011m-29.513-1.513q.06.012.113.017l-.12-.018zm36.324-1.048q.075.05.14.104a2 2 0 0 0-.14-.105m-3.94-1.72.077-.065.013-.011zm-28.873-.677q.039.072.08.136l.015.02-.015-.02a3 3 0 0 1-.154-.286zM52 10.328q.001.024 0 .047l.001-.048a.7.7 0 0 0-.02-.133zM5.761 9.451c-.17.007-.358.018-.547.04l.247-.023q.157-.011.3-.017m5.592-1.436-.018.016a.6.6 0 0 1 .091-.069zm36.164-.9c-.12.255-.235.496-.348.7l.172-.33q.087-.178.176-.37m1.538.519.245-.569.007-.018zM4.09 7.477l.007.012-.032-.073q.01.03.025.06m46.856-.693-.084.024q.069-.018.134-.034zM6.42 5.501l-.002.01a.5.5 0 0 1 .027-.096z"/>' +
  '<path fill="url(#norito-face-a)" d="M13 16c0-5.523 4.477-10 10-10h10c5.523 0 10 4.477 10 10s-4.477 10-10 10H23c-5.523 0-10-4.477-10-10"/>' +
  '<path fill="#fea9bf" fill-opacity=".6" d="M38.412 18.031c1.75-.292 2.337 1.563.292 1.948l-.023.003c-1.926.232-2.43-1.803-.27-1.951M17.901 18.031c.456-.032 1.178-.096 1.552.165 1.04.724.427 1.467-.421 1.772-1.642.268-2.995-1.207-1.13-1.937"/>' +
  '<path fill="#fd6e92" d="M27 17.5q-.002.163.09.332c.063.113.16.227.296.33.136.1.304.186.497.246s.403.092.617.092.424-.032.617-.092a1.6 1.6 0 0 0 .497-.247c.136-.102.234-.216.296-.329A.7.7 0 0 0 30 17.5a.5.5 0 1 1 1 0c0 .286-.076.564-.215.815-.138.251-.335.47-.571.646a2.6 2.6 0 0 1-.8.402c-.292.091-.603.137-.914.137s-.622-.046-.914-.137a2.6 2.6 0 0 1-.8-.402 2.1 2.1 0 0 1-.571-.646A1.7 1.7 0 0 1 26 17.5a.5.5 0 1 1 1 0"/>' +
  '<path fill="#29202e" d="M21.808 11.006a3 3 0 1 1 .384 5.988 3 3 0 0 1-.384-5.988"/>' +
  '<path fill="#fff" d="M24 13.5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0"/>' +
  '<path fill="#29202e" d="M34.906 11.002a3 3 0 1 1 .188 5.997 3 3 0 0 1-.188-5.997"/>' +
  '<path fill="#fff" d="M37 13.5a1.5 1.5 0 1 1-3 0 1.5 1.5 0 0 1 3 0"/>' +
  '<defs><linearGradient id="norito-face-a" x1="28" x2="28" y1="6" y2="26" gradientUnits="userSpaceOnUse">' +
  '<stop stop-color="#fff0f1"/><stop offset="1" stop-color="#ffd5da"/></linearGradient></defs>' +
  '</svg>';

// Corner "pop out" mascot toast: a flat/minimal comic-style speech bubble
// with the norito face beneath it, sliding up from the bottom-right corner
// of the viewport. Created lazily on first use and reused after that.
let mascotHideTimer = null;
const MASCOT_DEFAULT_MESSAGES = ["Yay!", "Done!", "Nice one!", "All set!"];

function showMascotToast(message) {
  const reduceMotion =
    typeof matchMedia === "function" &&
    matchMedia("(prefers-reduced-motion: reduce)").matches;

  let toast = document.getElementById("norito-mascot-toast");
  if (!toast) {
    toast = document.createElement("div");
    toast.id = "norito-mascot-toast";
    toast.className = "mascot-toast";
    toast.setAttribute("aria-hidden", "true");
    toast.innerHTML =
      '<div class="mascot-bubble"><span class="mascot-bubble-text"></span></div>' +
      `<div class="mascot-face">${NORITO_MASCOT_ICON}</div>`;
    document.body.appendChild(toast);
  }

  toast.querySelector(".mascot-bubble-text").textContent =
    message ||
    MASCOT_DEFAULT_MESSAGES[Math.floor(Math.random() * MASCOT_DEFAULT_MESSAGES.length)];

  clearTimeout(mascotHideTimer);
  toast.classList.toggle("no-motion", !!reduceMotion);
  toast.classList.add("show");
  mascotHideTimer = setTimeout(() => toast.classList.remove("show"), 1900);
}

function celebrateSuccess(button, panel, message) {
  const reduceMotion =
    typeof matchMedia === "function" &&
    matchMedia("(prefers-reduced-motion: reduce)").matches;

  if (panel) {
    panel.classList.remove("flash-success");
    void panel.offsetWidth; // restart animation if triggered again quickly
    if (!reduceMotion) panel.classList.add("flash-success");
    setTimeout(() => panel.classList.remove("flash-success"), 900);
  }

  if (button && !button.disabled) {
    const original = button.innerHTML;
    button.classList.remove("btn-pop");
    void button.offsetWidth;
    if (!reduceMotion) button.classList.add("btn-pop");
    button.innerHTML = `<span class="btn-check">${NORITO_CHECK_ICON}</span>`;
    setTimeout(() => {
      button.innerHTML = original;
      button.classList.remove("btn-pop");
    }, 850);
  }

  showMascotToast(message);
}
