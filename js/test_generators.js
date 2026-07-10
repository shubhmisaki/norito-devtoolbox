const fs = require("fs");
const path = require("path");
const gen = require("./generators.js");

const outDir = path.join(__dirname, "test_output");
fs.mkdirSync(outDir, { recursive: true });

function write(name, bytes) {
  const p = path.join(outDir, name);
  fs.writeFileSync(p, Buffer.from(bytes));
  return p;
}

function report(name, requested, bytes) {
  console.log(`${name}: requested=${requested} actual=${bytes.length} diff=${bytes.length - requested}`);
}

// TXT
{
  const b = gen.generateTxt(1024, "text");
  report("TXT 1KB", 1024, b);
  write("test_1kb.txt", b);
}

// BIN
{
  const b = gen.generateBin(2048, "random");
  report("BIN 2KB", 2048, b);
  write("test_2kb.bin", b);
}

// PDF at a range of sizes
for (const size of [50, 500, 2000, 100000]) {
  const b = gen.generatePdf(size);
  report(`PDF ${size}B`, size, b);
  write(`test_${size}.pdf`, b);
}

// ZIP at a range of sizes
for (const size of [50, 200, 5000, 1000000]) {
  const b = gen.generateZip(size, "test.bin");
  report(`ZIP ${size}B`, size, b);
  write(`test_${size}.zip`, b);
}

// GIF padding
for (const size of [43, 100, 500, 10000, 300000]) {
  const b = gen.padGif(size);
  report(`GIF ${size}B`, size, b);
  write(`test_${size}.gif`, b);
}

console.log("\nAll files written to", outDir);
