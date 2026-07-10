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
// One consistent, restrained celebration reused by every tool: the button
// that was clicked briefly pops and its content morphs into a checkmark,
// and (optionally) a result panel gets a soft success-colored flash around
// its edge. No confetti, no sound, nothing that lingers, just enough motion
// that an action never feels silent. Fully inert under
// prefers-reduced-motion (colors still communicate success, motion doesn't).
// Lives here (not utils.js) because this file is the one script every tool
// page loads unconditionally; utils.js is only pulled in by the tools that
// actually need its byte-packing helpers.
const NORITO_CHECK_ICON =
  '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" ' +
  'stroke-linecap="round" stroke-linejoin="round" width="15" height="15">' +
  '<path d="M20 6 9 17l-5-5"/></svg>';

function celebrateSuccess(button, panel) {
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
}
