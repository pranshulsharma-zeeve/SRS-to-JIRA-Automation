import test from "node:test";
import assert from "node:assert/strict";
import { access } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, "..");

test("frontend baseline folders exist", async () => {
  const requiredDirs = ["app", "components", "lib", "styles"];
  await Promise.all(requiredDirs.map((dir) => access(path.join(root, dir))));
  assert.ok(true);
});
