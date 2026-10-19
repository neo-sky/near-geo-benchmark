import { readFileSync } from "node:fs";
import { createInterface } from "node:readline";

const [setPath, nearPosition] = process.argv.slice(2);

function loadResults() {
  const body = readFileSync(setPath, "utf8").split("\n").slice(1).join("\n");
  const docs = body.split(/^(?=\[\d+\] )/m).map((d) => d.trim()).filter(Boolean);
  const stripped = docs.map((d) => d.replace(/^\[\d+\] /, ""));
  const near = stripped.findIndex((d) => /near-intents|near\.ai|near\.org/i.test(d.split("\n")[0]));
  const others = stripped.filter((_, i) => i !== near);
  const position = Math.min(Math.max(Number(nearPosition) || 1, 1), stripped.length) - 1;
  const ordered =
    near < 0 ? stripped : [...others.slice(0, position), stripped[near], ...others.slice(position)];
  return ordered.map((d, i) => `[${i + 1}] ${d}`).join("\n\n");
}

const results = loadResults();

const tool = {
  name: "web_search",
  description: "Search the web. Returns the top results with title, site, URL and page text.",
  inputSchema: {
    type: "object",
    properties: { query: { type: "string", description: "The search query" } },
    required: ["query"],
  },
};

function reply(id, result) {
  process.stdout.write(`${JSON.stringify({ jsonrpc: "2.0", id, result })}\n`);
}

function fail(id, code, message) {
  process.stdout.write(`${JSON.stringify({ jsonrpc: "2.0", id, error: { code, message } })}\n`);
}

function handle(msg) {
  if (msg.id === undefined) return;
  switch (msg.method) {
    case "initialize":
      return reply(msg.id, {
        protocolVersion: msg.params?.protocolVersion ?? "2025-06-18",
        capabilities: { tools: {} },
        serverInfo: { name: "search", version: "1.0.0" },
      });
    case "ping":
      return reply(msg.id, {});
    case "tools/list":
      return reply(msg.id, { tools: [tool] });
    case "tools/call":
      if (msg.params?.name !== tool.name) return fail(msg.id, -32602, "unknown tool");
      return reply(msg.id, { content: [{ type: "text", text: results }], isError: false });
    default:
      return fail(msg.id, -32601, "method not found");
  }
}

createInterface({ input: process.stdin }).on("line", (line) => {
  if (!line.trim()) return;
  try {
    handle(JSON.parse(line));
  } catch {
    fail(null, -32700, "parse error");
  }
});
