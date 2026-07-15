(function () {
  const DIGITS = "0123456789abcdefghijklmnopqrstuvwxyz";

  const els = {
    binary: document.getElementById("baseBinary"),
    octal: document.getElementById("baseOctal"),
    decimal: document.getElementById("baseDecimal"),
    hex: document.getElementById("baseHex"),
    errorBox: document.getElementById("errorBox"),
    customValue: document.getElementById("customValue"),
    customFrom: document.getElementById("customFrom"),
    customTo: document.getElementById("customTo"),
    customOutput: document.getElementById("customOutput"),
    customError: document.getElementById("customError"),
  };

  function toBigIntFromBase(str, base) {
    let s = str.trim().toLowerCase();
    if (s === "") throw new Error("Empty input");
    let neg = false;
    if (s[0] === "-") { neg = true; s = s.slice(1); }
    else if (s[0] === "+") { s = s.slice(1); }
    if (s === "") throw new Error("Empty input");
    let result = 0n;
    const b = BigInt(base);
    for (const ch of s) {
      const v = DIGITS.indexOf(ch);
      if (v === -1 || v >= base) throw new Error('Invalid digit "' + ch + '" for base ' + base);
      result = result * b + BigInt(v);
    }
    return neg ? -result : result;
  }

  function fromBigIntToBase(n, base) {
    if (n === 0n) return "0";
    const neg = n < 0n;
    let x = neg ? -n : n;
    const b = BigInt(base);
    let out = "";
    while (x > 0n) {
      const rem = x % b;
      out = DIGITS[Number(rem)] + out;
      x = x / b;
    }
    return (neg ? "-" : "") + out;
  }

  const fieldBases = { binary: 2, octal: 8, decimal: 10, hex: 16 };

  function syncFrom(sourceKey) {
    els.errorBox.style.display = "none";
    const raw = els[sourceKey].value;
    if (raw.trim() === "") {
      Object.keys(fieldBases).forEach(function (k) { if (k !== sourceKey) els[k].value = ""; });
      return;
    }
    try {
      const value = toBigIntFromBase(raw, fieldBases[sourceKey]);
      Object.keys(fieldBases).forEach(function (k) {
        if (k !== sourceKey) els[k].value = fromBigIntToBase(value, fieldBases[k]);
      });
    } catch (err) {
      els.errorBox.querySelector(".r-body").textContent = "That's not a valid " + sourceKey + " number: " + err.message;
      els.errorBox.style.display = "flex";
    }
  }

  els.binary.addEventListener("input", function () { syncFrom("binary"); });
  els.octal.addEventListener("input", function () { syncFrom("octal"); });
  els.decimal.addEventListener("input", function () { syncFrom("decimal"); });
  els.hex.addEventListener("input", function () { syncFrom("hex"); });

  function renderCustom() {
    els.customError.style.display = "none";
    const raw = els.customValue.value;
    const fromBase = parseInt(els.customFrom.value, 10);
    const toBase = parseInt(els.customTo.value, 10);
    if (raw.trim() === "") { els.customOutput.value = ""; return; }
    try {
      const value = toBigIntFromBase(raw, fromBase);
      els.customOutput.value = fromBigIntToBase(value, toBase);
    } catch (err) {
      els.customOutput.value = "";
      els.customError.querySelector(".r-body").textContent = err.message;
      els.customError.style.display = "flex";
    }
  }

  els.customValue.addEventListener("input", renderCustom);
  els.customFrom.addEventListener("change", renderCustom);
  els.customTo.addEventListener("change", renderCustom);

  // seed with a starting example
  els.decimal.value = "255";
  syncFrom("decimal");
})();
