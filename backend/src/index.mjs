import http from "node:http";
import path from "node:path";
import { fileURLToPath } from "node:url";

export function handleRequest(req, res) {
  if (req.url === "/health") {
    res.writeHead(200, { "content-type": "application/json" });
    res.end(JSON.stringify({ status: "ok" }));
    return;
  }

  res.writeHead(404, { "content-type": "application/json" });
  res.end(JSON.stringify({ error: "not_found" }));
}

export function createServer() {
  return http.createServer(handleRequest);
}

const isDirectRun = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);

if (isDirectRun) {
  const port = Number(process.env.PORT || 3001);
  const server = createServer();
  server.listen(port, () => {
    console.log(`Backend service listening on port ${port}`);
  });
}
