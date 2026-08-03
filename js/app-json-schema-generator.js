(function () {
  const input = document.getElementById("jsonInput");
  const output = document.getElementById("output");
  const status = document.getElementById("status");
  const copyBtn = document.getElementById("copyBtn");

  function typeOf(v) {
    if (v === null) return "null";
    if (Array.isArray(v)) return "array";
    if (typeof v === "number") return Number.isInteger(v) ? "integer" : "number";
    return typeof v; // string, boolean, object
  }

  function mergeSchemas(a, b) {
    if (!a) return b;
    if (!b) return a;
    if (JSON.stringify(a) === JSON.stringify(b)) return a;
    const typesA = Array.isArray(a.type) ? a.type : [a.type];
    const typesB = Array.isArray(b.type) ? b.type : [b.type];
    const types = Array.from(new Set([...typesA, ...typesB]));
    return { type: types.length === 1 ? types[0] : types };
  }

  function infer(value) {
    const t = typeOf(value);
    if (t === "object") {
      const properties = {};
      const required = [];
      Object.keys(value).forEach((k) => {
        properties[k] = infer(value[k]);
        required.push(k);
      });
      return { type: "object", properties, required };
    }
    if (t === "array") {
      if (!value.length) return { type: "array", items: {} };
      let itemSchema = infer(value[0]);
      for (let i = 1; i < value.length; i++) {
        itemSchema = mergeSchemas(itemSchema, infer(value[i]));
      }
      return { type: "array", items: itemSchema };
    }
    return { type: t };
  }

  function build() {
    const raw = input.value.trim();
    if (!raw) {
      output.textContent = "";
      status.style.display = "none";
      return;
    }
    let parsed;
    try {
      parsed = JSON.parse(raw);
    } catch (e) {
      status.textContent = `Invalid JSON: ${e.message}`;
      status.style.display = "block";
      output.textContent = "";
      return;
    }
    status.style.display = "none";
    const schema = {
      "$schema": "http://json-schema.org/draft-07/schema#",
      ...infer(parsed),
    };
    output.textContent = JSON.stringify(schema, null, 2);
  }

  input.addEventListener("input", build);
  build();

  copyBtn.addEventListener("click", async () => {
    if (!output.textContent) return;
    try {
      await copyToClipboard(output.textContent);
      const I18N_C = i18nFor("common");
      showMascotToast(I18N_C.copied || "Copied!");
      celebrateSuccess(copyBtn);
    } catch (e) { /* clipboard unavailable, silently ignore */ }
  });
})();
