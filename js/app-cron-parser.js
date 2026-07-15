(function () {
  const els = {
    input: document.getElementById("input"),
    resultWrap: document.getElementById("resultWrap"),
    description: document.getElementById("description"),
    nextRunsList: document.getElementById("nextRunsList"),
    errorBox: document.getElementById("errorBox"),
    presetSelect: document.getElementById("presetSelect"),
  };

  const MONTH_NAMES = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"];
  const DOW_NAMES = ["Sunday", "Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"];

  function parseFieldToSet(raw, min, max) {
    const set = new Set();
    const parts = raw.split(",");
    for (let part of parts) {
      part = part.trim();
      if (part === "") throw new Error("Empty value in field");
      let step = 1;
      const stepMatch = part.match(/^(.*)\/(\d+)$/);
      let base = part;
      if (stepMatch) { base = stepMatch[1]; step = parseInt(stepMatch[2], 10); }
      let lo, hi;
      if (base === "*") { lo = min; hi = max; }
      else if (/^\d+-\d+$/.test(base)) {
        const m = base.match(/^(\d+)-(\d+)$/);
        lo = parseInt(m[1], 10); hi = parseInt(m[2], 10);
      } else if (/^\d+$/.test(base)) {
        lo = hi = parseInt(base, 10);
      } else {
        throw new Error('Unrecognized value "' + part + '"');
      }
      if (lo < min || hi > max || lo > hi) throw new Error('Value out of range in "' + part + '" (expected ' + min + '-' + max + ")");
      for (let v = lo; v <= hi; v += step) set.add(v);
    }
    return set;
  }

  function parseCron(expr) {
    const fields = expr.trim().split(/\s+/);
    if (fields.length !== 5) throw new Error("Expected 5 fields (minute hour day-of-month month day-of-week), got " + fields.length);
    const minuteRaw = fields[0], hourRaw = fields[1], domRaw = fields[2], monthRaw = fields[3], dowRaw = fields[4];
    return {
      raw: { minute: minuteRaw, hour: hourRaw, dom: domRaw, month: monthRaw, dow: dowRaw },
      minute: parseFieldToSet(minuteRaw, 0, 59),
      hour: parseFieldToSet(hourRaw, 0, 23),
      dom: parseFieldToSet(domRaw, 1, 31),
      month: parseFieldToSet(monthRaw, 1, 12),
      dow: parseFieldToSet(dowRaw, 0, 6),
      domIsWildcard: domRaw === "*",
      dowIsWildcard: dowRaw === "*",
    };
  }

  function matches(cron, date) {
    const minute = date.getMinutes(), hour = date.getHours(), dom = date.getDate(), month = date.getMonth() + 1, dow = date.getDay();
    if (!cron.minute.has(minute)) return false;
    if (!cron.hour.has(hour)) return false;
    if (!cron.month.has(month)) return false;
    if (cron.domIsWildcard && cron.dowIsWildcard) return true;
    if (cron.domIsWildcard) return cron.dow.has(dow);
    if (cron.dowIsWildcard) return cron.dom.has(dom);
    return cron.dom.has(dom) || cron.dow.has(dow);
  }

  function nextRuns(cron, fromDate, count, maxMinutesAhead) {
    const results = [];
    let d = new Date(fromDate.getTime());
    d.setSeconds(0, 0);
    d.setMinutes(d.getMinutes() + 1);
    let steps = 0;
    const cap = maxMinutesAhead || 527040;
    while (results.length < count && steps < cap) {
      if (matches(cron, d)) results.push(new Date(d.getTime()));
      d.setMinutes(d.getMinutes() + 1);
      steps++;
    }
    return results;
  }

  function pad2(n) { return String(n).padStart(2, "0"); }
  function listStr(arr) {
    if (arr.length === 1) return String(arr[0]);
    if (arr.length === 2) return arr[0] + " and " + arr[1];
    return arr.slice(0, -1).join(", ") + ", and " + arr[arr.length - 1];
  }
  function isWildcard(raw) { return raw === "*"; }
  function isStep(raw) { return /^\*\/\d+$/.test(raw); }
  function stepValue(raw) { return parseInt(raw.split("/")[1], 10); }
  function isSingle(raw) { return /^\d+$/.test(raw); }
  function isList(raw) { return /^\d+(,\d+)+$/.test(raw); }

  function describeCron(cron) {
    const r = cron.raw;
    let timePart;
    if (isSingle(r.minute) && isSingle(r.hour)) {
      timePart = "at " + pad2(r.hour) + ":" + pad2(r.minute);
    } else if (isWildcard(r.minute) && isSingle(r.hour)) {
      timePart = "every minute during hour " + pad2(r.hour);
    } else if (isStep(r.minute) && isSingle(r.hour)) {
      timePart = "every " + stepValue(r.minute) + " minutes during hour " + pad2(r.hour);
    } else if (isWildcard(r.minute) && isWildcard(r.hour)) {
      timePart = "every minute";
    } else if (isStep(r.minute) && isWildcard(r.hour)) {
      timePart = "every " + stepValue(r.minute) + " minutes";
    } else if (isSingle(r.minute) && isWildcard(r.hour)) {
      timePart = "at minute " + r.minute + " of every hour";
    } else if (isSingle(r.minute) && isStep(r.hour)) {
      timePart = "at minute " + r.minute + " every " + stepValue(r.hour) + " hours";
    } else if (isSingle(r.minute) && isList(r.hour)) {
      timePart = "at minute " + r.minute + " during hours " + listStr(r.hour.split(","));
    } else if (isStep(r.minute) && /^\d+-\d+$/.test(r.hour)) {
      const hb = r.hour.split("-");
      timePart = "every " + stepValue(r.minute) + " minutes, between " + pad2(hb[0]) + ":00 and " + pad2(hb[1]) + ":00";
    } else if (isStep(r.minute) && isList(r.hour)) {
      timePart = "every " + stepValue(r.minute) + " minutes, during hours " + listStr(r.hour.split(","));
    } else {
      timePart = "at minute(s) " + r.minute + " of hour(s) " + r.hour;
    }

    let dayPart = "";
    const domWild = cron.domIsWildcard, dowWild = cron.dowIsWildcard;
    if (domWild && dowWild) {
      dayPart = "every day";
    } else if (!dowWild && domWild) {
      if (isSingle(r.dow)) dayPart = "on " + DOW_NAMES[parseInt(r.dow, 10)];
      else if (isList(r.dow)) dayPart = "on " + listStr(r.dow.split(",").map(function (n) { return DOW_NAMES[parseInt(n, 10)]; }));
      else if (/^\d+-\d+$/.test(r.dow)) {
        const b = r.dow.split("-").map(Number);
        dayPart = "from " + DOW_NAMES[b[0]] + " through " + DOW_NAMES[b[1]];
      } else dayPart = "on day-of-week " + r.dow;
    } else if (dowWild && !domWild) {
      if (isSingle(r.dom)) dayPart = "on day " + r.dom + " of the month";
      else dayPart = "on day(s) " + r.dom + " of the month";
    } else if (!domWild && !dowWild) {
      dayPart = "on day " + r.dom + " of the month, or when it's day-of-week " + r.dow;
    }

    let monthPart = "";
    if (!isWildcard(r.month)) {
      if (isSingle(r.month)) monthPart = "in " + MONTH_NAMES[parseInt(r.month, 10) - 1];
      else monthPart = "in month(s) " + r.month;
    }

    let sentence = "Runs " + timePart;
    if (dayPart) sentence += ", " + dayPart;
    if (monthPart) sentence += ", " + monthPart;
    return sentence + ".";
  }

  function formatRun(d) {
    const weekday = DOW_NAMES[d.getDay()].slice(0, 3);
    const month = MONTH_NAMES[d.getMonth()];
    return weekday + ", " + month + " " + d.getDate() + ", " + d.getFullYear() + " at " + pad2(d.getHours()) + ":" + pad2(d.getMinutes());
  }

  function render() {
    els.errorBox.style.display = "none";
    const raw = els.input.value.trim();
    if (!raw) { els.resultWrap.style.display = "none"; return; }
    try {
      const cron = parseCron(raw);
      els.description.textContent = describeCron(cron);
      const runs = nextRuns(cron, new Date(), 5);
      els.nextRunsList.innerHTML = "";
      if (runs.length === 0) {
        const li = document.createElement("li");
        li.textContent = "No matching run found in the next year, double-check the expression.";
        els.nextRunsList.appendChild(li);
      } else {
        runs.forEach(function (d) {
          const li = document.createElement("li");
          li.textContent = formatRun(d);
          els.nextRunsList.appendChild(li);
        });
      }
      els.resultWrap.style.display = "block";
    } catch (err) {
      els.resultWrap.style.display = "none";
      els.errorBox.querySelector(".r-body").textContent = err.message;
      els.errorBox.style.display = "flex";
    }
  }

  els.input.addEventListener("input", render);
  els.presetSelect.addEventListener("change", function () {
    if (els.presetSelect.value) {
      els.input.value = els.presetSelect.value;
      render();
    }
  });

  render();
})();
