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

  // ---- recently used ---------------------------------------------------
  // Stored as locale-independent paths ("/json-formatter.html") so the list
  // follows the visitor across languages. Stays on this device only.
  var RECENT_KEY = "norito:recent";
  var LOCALE_RE = /^\/(es|zh|ar|hi|ru|ja)(?=\/)/;
  function toolKey(href) {
    try {
      return new URL(href, location.href).pathname.replace(LOCALE_RE, "");
    } catch (e) {
      return href;
    }
  }
  function readRecents() {
    try {
      var v = JSON.parse(localStorage.getItem(RECENT_KEY) || "[]");
      return Array.isArray(v) ? v : [];
    } catch (e) {
      return [];
    }
  }
  function recentTools() {
    var byKey = {};
    TOOLS.forEach(function (t) { byKey[toolKey(t.href)] = t; });
    return readRecents().map(function (k) { return byKey[k]; }).filter(Boolean);
  }
  function withRecentsFirst(list) {
    var recent = recentTools();
    if (!recent.length) return list;
    return recent.concat(list.filter(function (t) { return recent.indexOf(t) === -1; }));
  }
  (function recordVisit() {
    var here = location.pathname.replace(LOCALE_RE, "");
    var isTool = TOOLS.some(function (t) { return toolKey(t.href) === here; });
    if (!isTool) return;
    try {
      var list = readRecents().filter(function (k) { return k !== here; });
      list.unshift(here);
      localStorage.setItem(RECENT_KEY, JSON.stringify(list.slice(0, 6)));
    } catch (e) {}
  })();

  // Homepage: a "jump back in" row under the hero search, shown only to
  // returning visitors who have actually used a tool before.
  (function renderRecentRow() {
    var hero = document.querySelector(".hero-search-trigger");
    if (!hero) return;
    var recent = recentTools().slice(0, 4);
    if (!recent.length) return;
    var labels = { en: "Recently used", es: "Usadas recientemente", zh: "最近使用", ar: "المستخدمة مؤخرًا", hi: "हाल ही में इस्तेमाल किए गए", ru: "Недавние", ja: "最近使ったツール" };
    var lang = (document.documentElement.lang || "en").slice(0, 2);
    var row = document.createElement("nav");
    row.className = "recent-row";
    row.setAttribute("aria-label", labels[lang] || labels.en);
    var label = document.createElement("span");
    label.className = "recent-label";
    label.textContent = labels[lang] || labels.en;
    row.appendChild(label);
    recent.forEach(function (t) {
      var a = document.createElement("a");
      a.href = t.href;
      a.textContent = t.name;
      row.appendChild(a);
    });
    hero.insertAdjacentElement("afterend", row);
  })();
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
    render(withRecentsFirst(TOOLS));
    setTimeout(function () {
      input.focus();
    }, 10);
  }

  function close() {
    overlay.hidden = true;
    document.body.classList.remove("nav-open-lock");
    if (trigger) trigger.focus();
  }

  // Every word in the query must appear somewhere in the name, description
  // or category; name matches rank first, so "pdf merge" finds Merge PDF
  // and "json" lists JSON Formatter before tools that merely mention JSON.
  function search(query) {
    var words = query.trim().toLowerCase().split(/\s+/).filter(Boolean);
    if (!words.length) return withRecentsFirst(TOOLS);
    var scored = [];
    TOOLS.forEach(function (tool) {
      var name = tool.name.toLowerCase();
      var hay = name + " " + tool.desc.toLowerCase() + " " + tool.cat.toLowerCase();
      var score = 0;
      for (var i = 0; i < words.length; i++) {
        var w = words[i];
        if (hay.indexOf(w) === -1) return;
        if (name.indexOf(w) === 0) score += 3;
        else if (name.indexOf(w) !== -1) score += 2;
        else score += 1;
      }
      scored.push({ tool: tool, score: score });
    });
    scored.sort(function (a, b) { return b.score - a.score; });
    return scored.map(function (x) { return x.tool; });
  }

  function filter(query) {
    render(search(query));
  }

  if (trigger) trigger.addEventListener("click", open);

  // Additional openers (e.g. the homepage hero search bar) marked with a
  // shared class, so any page can add its own palette trigger.
  document.querySelectorAll(".js-cmdk-trigger").forEach(function (el) {
    el.addEventListener("click", open);
  });

  // Show the right shortcut for the visitor's platform (kbd hints are
  // authored as Cmd-K; swap to Ctrl K for non-Mac).
  if (!/Mac|iPhone|iPad/.test(navigator.platform || "")) {
    document.querySelectorAll(".hero-search-trigger kbd").forEach(function (k) {
      k.textContent = "Ctrl K";
    });
  }

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
