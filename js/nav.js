// Shared header-nav behavior: category dropdowns, click-outside/Escape to
// close, and auto-detecting which category + link is "active" from the
// current URL so every page can share one identical nav markup block.
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
    if (e.key === "Escape") closeAll();
  });
})();
