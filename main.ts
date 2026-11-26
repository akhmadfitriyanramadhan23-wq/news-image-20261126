// The World Today — 26 November 2026.
// Copies the pre-rendered front page into the grader's output directory.
// The image is rendered by tools/make-image.py (deterministic PIL, fixed
// seed); this entrypoint only copies it, so both grader runs are identical.
// Output: /output/entry.png (1024x1024 PNG, < 1 MiB), per the kit spec.
import { copyFileSync, existsSync, mkdirSync, statSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "/output";
mkdirSync(outDir, { recursive: true });
const src = join(here, "entry.png");
if (!existsSync(src)) {
  throw new Error("entry.png missing: run tools/make-image.py first");
}
const dest = join(outDir, "entry.png");
copyFileSync(src, dest);
console.log("wrote", dest, `(${statSync(dest).size} bytes)`);
