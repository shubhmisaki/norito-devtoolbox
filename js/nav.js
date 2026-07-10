// Shared header-nav behavior: category dropdowns, click-outside/Escape to
// close, auto-detecting which category + link is "active" from the current
// URL, and a mobile hamburger menu, all from one identical nav markup block
// shared by every page (the hamburger button is injected here rather than
// added to all 44 HTML files individually).
(function () {
  const nav = document.getElementById("siteNav");
  if (!nav) return;

  const groups = Array.from(nav.querySelectorAll(".nav-group"));
  const currentFile = (location.pathname.split("/").pop() || "index.html") || "index.html";

  function closeAll(except) {
    groups.forEach((g) => {
      if (g !== except) g.classList.remove("open");
    });
  }

  groups.forEach((group) => {
    const btn = group.querySelector(".nav-cat");
    const panel = group.querySelector(".nav-panel");
    if (!btn || !panel) return;

    const links = Array.from(panel.querySelectorAll("a"));
    const match = links.find((a) => a.getAttribute("href") === currentFile);
    if (match) {
      btn.classList.add("active");
      match.classList.add("active");
    }

    btn.addEventListener("click", (e) => {
      e.stopPropagation();
      const isOpen = group.classList.contains("open");
      closeAll();
      if (!isOpen) group.classList.add("open");
    });
  });

  document.addEventListener("click", () => closeAll());
  document.addEventListener("keydown", (e) => {
    if (e.key === "Escape") { closeAll(); closeMobileMenu(); }
  });

  // ---- mobile hamburger menu ----
  const wrap = nav.closest(".wrap");
  let hamburger = null;
  if (wrap) {
    hamburger = document.createElement("button");
    hamburger.type = "button";
    hamburger.className = "nav-hamburger";
    hamburger.setAttribute("aria-label", "Menu");
    hamburger.setAttribute("aria-expanded", "false");
    hamburger.setAttribute("aria-controls", "siteNav");
    hamburger.innerHTML =
      '<svg class="ham-icon-open" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="22" height="22"><path d="M4 6h16M4 12h16M4 18h16"/></svg>' +
      '<svg class="ham-icon-close" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="22" height="22"><path d="M18 6 6 18M6 6l12 12"/></svg>';
    wrap.insertBefore(hamburger, nav);
  }

  function closeMobileMenu() {
    nav.classList.remove("mobile-open");
    if (hamburger) {
      hamburger.classList.remove("active");
      hamburger.setAttribute("aria-expanded", "false");
    }
    document.body.classList.remove("nav-open-lock");
  }
  function openMobileMenu() {
    nav.classList.add("mobile-open");
    if (hamburger) {
      hamburger.classList.add("active");
      hamburger.setAttribute("aria-expanded", "true");
    }
    document.body.classList.add("nav-open-lock");
  }
  if (hamburger) {
    hamburger.addEventListener("click", (e) => {
      e.stopPropagation();
      if (nav.classList.contains("mobile-open")) closeMobileMenu();
      else openMobileMenu();
    });
  }
  nav.addEventListener("click", (e) => {
    if (e.target.closest("a")) closeMobileMenu();
  });
  window.addEventListener("resize", () => {
    if (window.innerWidth > 760) closeMobileMenu();
  });
})();
