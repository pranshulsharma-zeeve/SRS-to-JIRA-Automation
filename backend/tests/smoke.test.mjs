import test from "node:test";
import assert from "node:assert/strict";
import { access } from "node:fs/promises";
import path from "node:path";
import { fileURLToPath } from "node:url";
import { handleRequest } from "../src/index.mjs";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const root = path.resolve(__dirname, "..");

test("backend baseline folders exist", async () => {
  const requiredDirs = [
    "src/routes",
    "src/controllers",
    "src/services",
    "src/middleware",
    "src/utils",
    "tests"
  ];

  await Promise.all(requiredDirs.map((dir) => access(path.join(root, dir))));
  assert.ok(true);
});

test("backend health endpoint returns ok", async () => {
  const req = { url: "/health" };
  const response = {
    statusCode: 0,
    headers: {},
    body: "",
    writeHead(statusCode, headers) {
      this.statusCode = statusCode;
      this.headers = headers;
    },
    end(payload) {
      this.body = payload;
    }
  };

  handleRequest(req, response);

  assert.equal(response.statusCode, 200);
  assert.deepEqual(JSON.parse(response.body), { status: "ok" });
});
