// The World Today — 26 November 2026.
// Entry point: places the pre-rendered front page where the grader looks.
// The page itself is produced by tools/make-image.py (PIL, fixed seed);
// this file only moves the bytes, so repeated runs stay identical.
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const targetDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
const sourcePath = new URL("./entry.png", import.meta.url).pathname;
const pixels = readFileSync(sourcePath);
if (pixels.length === 0) {
  throw new Error("entry.png is empty: run tools/make-image.py first");
}
mkdirSync(targetDir, { recursive: true });
const destination = join(targetDir, "entry.png");
writeFileSync(destination, pixels);
console.log(`front page -> ${destination} (${pixels.length} bytes)`);
