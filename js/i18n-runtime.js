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

// A deliberately simplified, flat, few-color redraw of the norito axolotl
// face for the mascot toast: no gradients, no fine linework, just enough
// shape to read as "the norito character" at a glance in a small popup.
const NORITO_MASCOT_ICON =
  '<svg viewBox="0 0 48 44" width="42" height="38" xmlns="http://www.w3.org/2000/svg">' +
  '<path d="M8 15 Q1 11 3 3 Q11 5 11 15 Z" fill="#fd6e92"/>' +
  '<path d="M8 22 Q-1 22 -1 15 Q9 13 11 22 Z" fill="#fd6e92"/>' +
  '<path d="M8 29 Q-1 32 2 39 Q11 34 11 26 Z" fill="#fd6e92"/>' +
  '<path d="M40 15 Q47 11 45 3 Q37 5 37 15 Z" fill="#fd6e92"/>' +
  '<path d="M40 22 Q49 22 49 15 Q39 13 37 22 Z" fill="#fd6e92"/>' +
  '<path d="M40 29 Q49 32 46 39 Q37 34 37 26 Z" fill="#fd6e92"/>' +
  '<rect x="9" y="7" width="30" height="28" rx="14" fill="#ffd5da"/>' +
  '<circle cx="18.5" cy="21" r="2.8" fill="#29202e"/>' +
  '<circle cx="29.5" cy="21" r="2.8" fill="#29202e"/>' +
  '<circle cx="14.5" cy="27" r="2.4" fill="#fd6e92" opacity=".55"/>' +
  '<circle cx="33.5" cy="27" r="2.4" fill="#fd6e92" opacity=".55"/>' +
  '<path d="M19.5 28.5 Q24 32 28.5 28.5" stroke="#29202e" stroke-width="1.8" fill="none" stroke-linecap="round"/>' +
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
