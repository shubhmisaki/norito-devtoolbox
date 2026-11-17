// A single, dismissible "this is free, here's how to support it" note.
//
// Rules, so it never becomes a nag:
//   - only after the visitor's 3rd completed task on this device
//   - never while the install banner is on screen
//   - once dismissed or clicked, not again for 90 days
(function () {
  var KEY = "norito:supportNoteAt";
  var AFTER_USES = 3;
  var SNOOZE_DAYS = 90;
  var TEXT = {
    en: ["Glad it helped", "norito is free and built by one person. If it saved you time, a coffee keeps it running.", "Buy me a coffee", "Dismiss"],
    es: ["Me alegra que te sirviera", "norito es gratis y lo hace una sola persona. Si te ahorró tiempo, un café ayuda a mantenerlo.", "Invítame un café", "Cerrar"],
    zh: ["很高兴帮到你", "norito 完全免费，由一个人开发。如果它帮你省了时间，请我喝杯咖啡能让它继续运行。", "请我喝杯咖啡", "关闭"],
    ar: ["سعيد أنها أفادتك", "norito مجاني ويطوّره شخص واحد. إن وفّر عليك وقتًا، فنجان قهوة يساعد على استمراره.", "ادعمني بفنجان قهوة", "إغلاق"],
    hi: ["खुशी है कि काम आया", "norito मुफ़्त है और इसे एक ही व्यक्ति बनाता है. अगर इसने आपका समय बचाया, तो एक कॉफ़ी इसे चलाए रखने में मदद करती है.", "एक कॉफ़ी पिलाएं", "बंद करें"],
    ru: ["Рад, что пригодилось", "norito бесплатный, его делает один человек. Если он сэкономил вам время, чашка кофе поможет ему жить дальше.", "Угостить кофе", "Закрыть"],
    ja: ["お役に立てて何よりです", "norito は無料で、個人が開発しています。時間の節約になったなら、コーヒー1杯のご支援が運営の助けになります。", "コーヒーをおごる", "閉じる"]
  };

  function snoozed() {
    try {
      var at = parseInt(localStorage.getItem(KEY), 10);
      return !!at && (Date.now() - at) / 864e5 < SNOOZE_DAYS;
    } catch (e) {
      return true; // storage unavailable: stay quiet
    }
  }

  function show() {
    if (snoozed() || document.querySelector(".install-banner, .support-note")) return;
    var t = TEXT[(document.documentElement.lang || "en").slice(0, 2)] || TEXT.en;
    var el = document.createElement("div");
    el.className = "install-banner support-note";
    el.setAttribute("role", "region");
    el.setAttribute("aria-label", t[0]);
    var inner = document.createElement("div");
    inner.className = "install-banner-inner";
    var text = document.createElement("div");
    text.className = "install-banner-text";
    var strong = document.createElement("strong");
    strong.textContent = t[0];
    var span = document.createElement("span");
    span.textContent = t[1];
    text.appendChild(strong);
    text.appendChild(span);
    var link = document.createElement("a");
    link.className = "btn install-banner-btn";
    link.href = "https://ko-fi.com/shubhmisaki";
    link.target = "_blank";
    link.rel = "noopener";
    link.textContent = t[2];
    var close = document.createElement("button");
    close.type = "button";
    close.className = "install-banner-close";
    close.setAttribute("aria-label", t[3]);
    close.title = t[3];
    close.innerHTML = '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" width="18" height="18" aria-hidden="true"><path d="M18 6 6 18M6 6l12 12"/></svg>';
    inner.appendChild(text);
    inner.appendChild(link);
    inner.appendChild(close);
    el.appendChild(inner);
    document.body.appendChild(el);
    requestAnimationFrame(function () { el.classList.add("visible"); });

    function done() {
      try { localStorage.setItem(KEY, String(Date.now())); } catch (e) {}
      el.classList.remove("visible");
      setTimeout(function () { if (el.parentNode) el.parentNode.removeChild(el); }, 300);
    }
    close.addEventListener("click", done);
    link.addEventListener("click", done);
    if (window.noritoTrack) window.noritoTrack("support_note_shown");
  }

  window.addEventListener("norito:output", function (e) {
    if (e.detail && e.detail.uses === AFTER_USES) setTimeout(show, 2500);
  });
})();
