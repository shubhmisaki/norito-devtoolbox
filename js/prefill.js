// Generic URL-param -> form-field prefill.
// Lets a thin SEO landing page (e.g. resize-image-for-instagram.html) link to
// the real tool with query params like ?mode=exact&width=1080&height=1080
// and have the form arrive already filled in, without duplicating any tool
// logic. Any query param whose name matches a form field's id gets applied:
// selects/text/number inputs get their value set, checkboxes are toggled on
// "true"/"1". A change+input event is dispatched after each so the tool's
// own listeners (visibility toggles, aspect-ratio sync, etc.) run exactly as
// if the user had made that choice by hand.
(function () {
  function applyPrefill() {
    let params;
    try {
      params = new URLSearchParams(window.location.search);
    } catch (e) {
      return;
    }
    if (![...params.keys()].length) return;
    params.forEach((value, key) => {
      const el = document.getElementById(key);
      if (!el) return;
      if (el.tagName !== "SELECT" && el.tagName !== "INPUT" && el.tagName !== "TEXTAREA") return;
      if (el.type === "checkbox" || el.type === "radio") {
        el.checked = value === "true" || value === "1";
      } else {
        el.value = value;
      }
      el.dispatchEvent(new Event("change", { bubbles: true }));
      el.dispatchEvent(new Event("input", { bubbles: true }));
    });
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", applyPrefill);
  } else {
    applyPrefill();
  }
})();
