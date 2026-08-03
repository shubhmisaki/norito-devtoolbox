(function () {
  const els = {
    input: document.getElementById("svgInput"),
    name: document.getElementById("componentName"),
    exportStyle: document.getElementById("exportStyle"),
    optProps: document.getElementById("optProps"),
    optTs: document.getElementById("optTs"),
    output: document.getElementById("output"),
    copyBtn: document.getElementById("copyBtn"),
    downloadBtn: document.getElementById("downloadBtn"),
  };

  // Explicit React attribute name overrides for common SVG presentation attrs.
  const ATTR_MAP = {
    "class": "className",
    "for": "htmlFor",
    "tabindex": "tabIndex",
    "xlink:href": "xlinkHref",
    "xml:space": "xmlSpace",
    "stroke-width": "strokeWidth",
    "stroke-linecap": "strokeLinecap",
    "stroke-linejoin": "strokeLinejoin",
    "stroke-dasharray": "strokeDasharray",
    "stroke-dashoffset": "strokeDashoffset",
    "stroke-miterlimit": "strokeMiterlimit",
    "stroke-opacity": "strokeOpacity",
    "fill-rule": "fillRule",
    "fill-opacity": "fillOpacity",
    "clip-rule": "clipRule",
    "clip-path": "clipPath",
    "font-family": "fontFamily",
    "font-size": "fontSize",
    "font-weight": "fontWeight",
    "text-anchor": "textAnchor",
    "stop-color": "stopColor",
    "stop-opacity": "stopOpacity",
    "vector-effect": "vectorEffect",
    "viewbox": "viewBox",
    "preserveaspectratio": "preserveAspectRatio",
  };

  function attrToReact(name) {
    if (ATTR_MAP[name]) return ATTR_MAP[name];
    if (name.startsWith("data-") || name.startsWith("aria-")) return name;
    // generic kebab-case -> camelCase
    if (name.includes("-")) {
      return name.replace(/-([a-z])/g, (_, c) => c.toUpperCase());
    }
    return name;
  }

  function nodeToJsx(node, depth, useProps, isRoot) {
    if (node.nodeType === Node.COMMENT_NODE) return "";
    if (node.nodeType === Node.TEXT_NODE) {
      const text = node.textContent.trim();
      return text ? " ".repeat(depth * 2) + text + "\n" : "";
    }
    if (node.nodeType !== Node.ELEMENT_NODE) return "";

    const indent = " ".repeat(depth * 2);
    const tag = node.tagName;
    const attrs = Array.from(node.attributes)
      .map((a) => `${attrToReact(a.name)}="${a.value.replace(/"/g, "&quot;")}"`)
      .join(" ");
    const propsSpread = isRoot && useProps ? " {...props}" : "";

    const children = Array.from(node.childNodes)
      .map((c) => nodeToJsx(c, depth + 1, useProps, false))
      .join("");

    if (!children.trim()) {
      return `${indent}<${tag}${attrs ? " " + attrs : ""}${propsSpread} />\n`;
    }
    return `${indent}<${tag}${attrs ? " " + attrs : ""}${propsSpread}>\n${children}${indent}</${tag}>\n`;
  }

  function build() {
    const raw = els.input.value.trim();
    if (!raw) {
      els.output.textContent = "";
      return;
    }
    let doc;
    try {
      doc = new DOMParser().parseFromString(raw, "image/svg+xml");
      if (doc.querySelector("parsererror")) throw new Error("parse error");
    } catch (e) {
      els.output.textContent = "// Couldn't parse this as SVG markup.";
      return;
    }

    const svgEl = doc.documentElement;
    if (svgEl.tagName.toLowerCase() !== "svg") {
      els.output.textContent = "// Root element must be <svg>.";
      return;
    }

    const useProps = els.optProps.checked;
    const isTs = els.optTs.checked;
    const name = (els.name.value.trim() || "IconComponent").replace(/[^A-Za-z0-9_]/g, "");
    const jsxBody = nodeToJsx(svgEl, 2, useProps, true).trimEnd();

    const propsType = isTs ? `props: React.SVGProps<SVGSVGElement>` : useProps ? "props" : "";
    const fnSignature = useProps ? `(${propsType})` : "()";
    const exportKeyword = els.exportStyle.value === "default" ? `export default function ${name}` : `export function ${name}`;

    const lines = [];
    if (isTs) lines.push(`import * as React from "react";`, "");
    lines.push(`${exportKeyword}${fnSignature} {`);
    lines.push(`  return (`);
    lines.push(jsxBody);
    lines.push(`  );`);
    lines.push(`}`);

    els.output.textContent = lines.join("\n");
  }

  [els.input, els.name, els.exportStyle, els.optProps, els.optTs].forEach((el) =>
    el.addEventListener("input", build)
  );
  build();

  els.copyBtn.addEventListener("click", async () => {
    if (!els.output.textContent) return;
    try {
      await copyToClipboard(els.output.textContent);
      const I18N_C = i18nFor("common");
      showMascotToast(I18N_C.copied || "Copied!");
      celebrateSuccess(els.copyBtn);
    } catch (e) { /* clipboard unavailable, silently ignore */ }
  });

  els.downloadBtn.addEventListener("click", () => {
    if (!els.output.textContent) return;
    const ext = els.optTs.checked ? "tsx" : "jsx";
    const name = (els.name.value.trim() || "IconComponent").replace(/[^A-Za-z0-9_]/g, "");
    downloadBlob(new Blob([els.output.textContent], { type: "text/plain" }), `${name}.${ext}`);
  });
})();
