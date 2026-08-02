import http from "node:http";
import crypto from "node:crypto";
import { WebSocketServer, WebSocket } from "ws";
import { config } from "./config.js";
import { handleRun, handleSubmit, pool } from "./judge.js";
import { RunRequest, SubmitRequest } from "./types.js";

const clients = new Set<WebSocket>();

function broadcast(type: "run_update" | "submit_update", payload: unknown) {
  const msg = JSON.stringify({ type, payload });
  for (const ws of clients) {
    if (ws.readyState === WebSocket.OPEN) ws.send(msg);
  }
}

function tokenOk(token: string | undefined): boolean {
  if (!config.judgeToken || !token) return false;
  const a = Buffer.from(token);
  const b = Buffer.from(config.judgeToken);
  return a.length === b.length && crypto.timingSafeEqual(a, b);
}

function readBody(req: http.IncomingMessage, maxBytes = 5 * 1024 * 1024): Promise<string> {
  return new Promise((resolve, reject) => {
    const chunks: Buffer[] = [];
    let len = 0;
    req.on("data", (d: Buffer) => {
      len += d.length;
      if (len > maxBytes) {
        reject(new Error("body too large"));
        req.destroy();
        return;
      }
      chunks.push(d);
    });
    req.on("end", () => resolve(Buffer.concat(chunks).toString("utf8")));
    req.on("error", reject);
  });
}

function json(res: http.ServerResponse, status: number, body: unknown) {
  const data = JSON.stringify(body);
  res.writeHead(status, {
    "content-type": "application/json",
    "content-length": Buffer.byteLength(data),
  });
  res.end(data);
}

const server = http.createServer(async (req, res) => {
  const url = new URL(req.url ?? "/", "http://localhost");
  if (req.method === "GET" && url.pathname === "/healthz") {
    return json(res, 200, { ok: true, queue: pool.pending });
  }

  const auth = req.headers.authorization;
  const token = auth?.startsWith("Bearer ") ? auth.slice(7) : undefined;
  if (!tokenOk(token)) {
    return json(res, 401, { error: "unauthorized" });
  }

  try {
    if (req.method === "POST" && url.pathname === "/run") {
      const body = JSON.parse(await readBody(req)) as RunRequest;
      if (!body.runId || !body.lang || typeof body.source !== "string") {
        return json(res, 400, { error: "runId, lang, source are required" });
      }
      const result = await handleRun(body, (partial) =>
        broadcast("run_update", partial)
      );
      broadcast("run_update", result);
      return json(res, 200, result);
    }
    if (req.method === "POST" && url.pathname === "/submit") {
      const body = JSON.parse(await readBody(req)) as SubmitRequest;
      if (!body.submissionId || !body.lang || typeof body.source !== "string" || !body.problemId) {
        return json(res, 400, {
          error: "submissionId, lang, source, problemId are required",
        });
      }
      const result = await handleSubmit(body, (partial) =>
        broadcast("submit_update", partial)
      );
      broadcast("submit_update", result);
      return json(res, 200, result);
    }
    return json(res, 404, { error: "not found" });
  } catch (e) {
    const msg = e instanceof Error ? e.message : String(e);
    if (/ENOENT/.test(msg)) return json(res, 404, { error: msg });
    if (e instanceof SyntaxError) return json(res, 400, { error: "invalid JSON" });
    console.error("request failed:", e);
    return json(res, 500, { error: msg });
  }
});

const wss = new WebSocketServer({ noServer: true });
server.on("upgrade", (req, socket, head) => {
  const url = new URL(req.url ?? "/", "http://localhost");
  if (url.pathname !== "/ws" || !tokenOk(url.searchParams.get("token") ?? undefined)) {
    socket.write("HTTP/1.1 401 Unauthorized\r\n\r\n");
    socket.destroy();
    return;
  }
  wss.handleUpgrade(req, socket, head, (ws) => {
    clients.add(ws);
    ws.on("close", () => clients.delete(ws));
  });
});

server.listen(config.port, () => {
  console.log(
    `judge listening on :${config.port} (sandbox=${config.sandbox}, workers=${config.workers})`
  );
});
