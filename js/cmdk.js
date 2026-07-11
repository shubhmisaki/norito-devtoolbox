(function () {
  var TOOLS = [
    { name: "Test File Generator", desc: "Byte-exact dummy files, any size", href: "test-file-generator.html", cat: "Files & images" },
    { name: "Compress Image to Size", desc: "Shrink to a target file size", href: "compress-image.html", cat: "Files & images" },
    { name: "Placeholder Image Generator", desc: "Custom-size placeholder images", href: "placeholder-generator.html", cat: "Files & images" },
    { name: "Remove Background", desc: "Cut a person out of a photo", href: "remove-background.html", cat: "Files & images" },
    { name: "QR Code Generator", desc: "Custom colors, error correction", href: "qr-code-generator.html", cat: "Files & images" },
    { name: "Password Generator", desc: "Random passwords & passphrases", href: "password-generator.html", cat: "Text & dev" },
    { name: "SEO Slug Generator", desc: "Clean URL slugs from titles", href: "seo-slug-generator.html", cat: "Text & dev" },
    { name: "Limited Text Generator", desc: "Placeholder text, exact length", href: "limited-text-generator.html", cat: "Text & dev" },
    { name: "JSON Formatter", desc: "Format, validate, minify", href: "json-formatter.html", cat: "Text & dev" },
    { name: "Markdown Editor", desc: "Live preview, export as .md/.html", href: "markdown-editor.html", cat: "Text & dev" }
  ];

  var overlay = document.getElementById("cmdkOverlay");
  var input = document.getElementById("cmdkInput");
  var results = document.getElementById("cmdkResults");
  var trigger = document.getElementById("searchTrigger");
  if (!overlay || !input || !results) return;

  var activeIndex = 0;
  var currentList = TOOLS;

  function render(list) {
    currentList = list;
    activeIndex = 0;
    if (!list.length) {
      results.innerHTML = '<div class="cmdk-empty">No tools match that search.</div>';
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
