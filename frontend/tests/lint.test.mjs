import test from "node:test";
import assert from "node:assert/strict";
import { readFile } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, "..");

test("frontend entry files are present and non-empty", async () => {
  const files = ["app/layout.tsx", "app/page.tsx", "styles/globals.css"];
  for (const file of files) {
    const content = await readFile(path.join(root, file), "utf8");
    assert.ok(content.trim().length > 0, `${file} should not be empty`);
  }
});
