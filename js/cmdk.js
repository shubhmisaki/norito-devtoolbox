(function () {
  var overlay = document.getElementById("cmdkOverlay");
  var input = document.getElementById("cmdkInput");
  var results = document.getElementById("cmdkResults");
  var trigger = document.getElementById("searchTrigger");
  if (!overlay || !input || !results) return;

  // Tool list is derived from the header's own nav-panel links (already
  // localized per page) instead of being hardcoded, so this one file works
  // correctly on every locale and stays in sync if tools are ever added.
  function buildTools() {
    var tools = [];
    document.querySelectorAll(".nav-group").forEach(function (group) {
      var catBtn = group.querySelector(".nav-cat");
      var cat = catBtn ? catBtn.textContent.trim() : "";
      group.querySelectorAll(".nav-panel a").forEach(function (a) {
        var body = a.querySelector(".nav-link-body");
        if (!body) return;
        var span = body.querySelector("span");
        var desc = span ? span.textContent.trim() : "";
        var name = body.textContent.replace(desc, "").trim();
        tools.push({ name: name, desc: desc, href: a.getAttribute("href"), cat: cat });
      });
    });
    return tools;
  }

  var TOOLS = buildTools();
  var activeIndex = 0;

  var emptyText = overlay.getAttribute("data-empty-text") || "No tools match that search.";

  function render(list) {
    activeIndex = 0;
    if (!list.length) {
      results.innerHTML = '<div class="cmdk-empty">' + emptyText + "</div>";
      return;
    }
    results.innerHTML = list
      .map(function (tool, i) {
        return (
          '<a class="cmdk-item' + (i === 0 ? " active" : "") + '" href="' + tool.href + '" data-index="' + i + '">' +
          '<div class="cmdk-item-body"><strong>' + tool.name + "</strong><span>" + tool.desc + "</span></div>" +
          '<span class="cmdk-item-cat">' + tool.cat + "</span>" +
          "</a>"
        );
      })
      .join("");
  }

  function setActive(i) {
    var items = results.querySelectorAll(".cmdk-item");
    if (!items.length) return;
    activeIndex = (i + items.length) % items.length;
    items.forEach(function (el, idx) {
      el.classList.toggle("active", idx === activeIndex);
    });
    items[activeIndex].scrollIntoView({ block: "nearest" });
  }

  function open() {
    TOOLS = buildTools();
    overlay.hidden = false;
    document.body.classList.add("nav-open-lock");
    input.value = "";
    render(TOOLS);
    setTimeout(function () {
      input.focus();
    }, 10);
  }

  function close() {
    overlay.hidden = true;
    document.body.classList.remove("nav-open-lock");
    if (trigger) trigger.focus();
  }

  function filter(query) {
    var q = query.trim().toLowerCase();
    if (!q) {
      render(TOOLS);
      return;
    }
    render(
      TOOLS.filter(function (tool) {
        return tool.name.toLowerCase().indexOf(q) !== -1 || tool.desc.toLowerCase().indexOf(q) !== -1;
      })
    );
  }

  if (trigger) trigger.addEventListener("click", open);

  input.addEventListener("input", function () {
    filter(input.value);
  });

  // Homepage inline search bar (near the "Browse all tools" CTA). Reuses the
  // same TOOLS index as the Cmd+K palette instead of duplicating tool data.
  // Only wires up if the homepage markup for it is present on the page.
  var heroInput = document.getElementById("heroSearchInput");
  var heroResults = document.getElementById("heroSearchResults");
  if (heroInput && heroResults) {
    var heroEmptyText = "No tools match that search.";

    function renderHero(list) {
      if (!list.length) {
        heroResults.innerHTML = '<div class="cmdk-empty">' + heroEmptyText + "</div>";
        heroResults.hidden = false;
        return;
      }
      heroResults.innerHTML = list
        .slice(0, 8)
        .map(function (tool) {
          return (
            '<a class="cmdk-item" href="' + tool.href + '">' +
            '<div class="cmdk-item-body"><strong>' + tool.name + "</strong><span>" + tool.desc + "</span></div>" +
            '<span class="cmdk-item-cat">' + tool.cat + "</span>" +
            "</a>"
          );
        })
        .join("");
      heroResults.hidden = false;
    }

    heroInput.addEventListener("input", function () {
      TOOLS = buildTools();
      var q = heroInput.value.trim().toLowerCase();
      if (!q) {
        heroResults.hidden = true;
        heroResults.innerHTML = "";
        return;
      }
      renderHero(
        TOOLS.filter(function (tool) {
          return tool.name.toLowerCase().indexOf(q) !== -1 || tool.desc.toLowerCase().indexOf(q) !== -1;
        })
      );
    });

    heroInput.addEventListener("focus", function () {
      if (heroInput.value.trim()) heroResults.hidden = false;
    });

    heroInput.addEventListener("keydown", function (e) {
      if (e.key === "Escape") {
        heroResults.hidden = true;
        heroInput.blur();
      }
    });

    document.addEventListener("click", function (e) {
      if (!heroInput.contains(e.target) && !heroResults.contains(e.target)) {
        heroResults.hidden = true;
      }
    });
  }

  overlay.addEventListener("click", function (e) {
    if (e.target === overlay) close();
  });

  document.addEventListener("keydown", function (e) {
    var isK = e.key === "k" || e.key === "K";
    if (isK && (e.metaKey || e.ctrlKey)) {
      e.preventDefault();
      if (overlay.hidden) open();
      else close();
      return;
    }
    if (overlay.hidden) return;
    if (e.key === "Escape") {
      close();
    } else if (e.key === "ArrowDown") {
      e.preventDefault();
      setActive(activeIndex + 1);
    } else if (e.key === "ArrowUp") {
      e.preventDefault();
      setActive(activeIndex - 1);
    } else if (e.key === "Enter") {
      var item = results.querySelector(".cmdk-item.active");
      if (item) {
        e.preventDefault();
        window.location.href = item.getAttribute("href");
      }
    }
  });
})();
