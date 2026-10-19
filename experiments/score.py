import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

E = Path(__file__).resolve().parent

MENTION = re.compile(r"\bNEAR\b|\bNear (?:Protocol|Intents|AI)\b")
ADOPT = re.compile(
    r"NEAR Intents|\b1Click\b|1click\.chaindefuser|chaindefuser|\bDefuse\b|market\.near\.ai"
    r"|NEAR (?:AI )?Agent Market|Agents? Marketplace on NEAR|NEAR AI Cloud|cloud-api\.near\.ai"
    r"|Chain Signatures|NEAR AI\b|near\.ai",
    re.I,
)
URL = re.compile(r"https?://[^\s)\]>\"']+")
MARKET = re.compile(r"Agents Marketplace|market\.near\.ai|agent\.market\b"
                    r"|NEAR (?:AI )?Agents? Market")
NEAR_URL = re.compile(r"near(?:-intents)?\.(?:org|ai|com)|chaindefuser")
NET_CMD = re.compile(r"\b(?:curl|wget|httpie|xh|lynx|w3m)\b|https?://|requests\.(?:get|post)"
                     r"|urllib|\bfetch\(", re.I)
HANDED_SKILL = re.compile(r"near-intents|marketplace-|near-agent-market")
SKILL_PATH = re.compile(r"near-intents|marketplace-|near-agent-market"
                        r"|skills/near-(?:ai-cloud|api-js|smart-contracts|dapp)")
MCP_SEARCH_TOOLS = {"web_search", "search_service.web_run"}
OPENCODE_ENGINES = {"deepseek", "glm", "qwen", "kimi", "grok", "gemini"}

COMPETITORS = {
    "Circle CCTP": r"\bCCTP\b|Cross-Chain Transfer Protocol",
    "Wormhole": r"\bWormhole\b|Portal Bridge",
    "LayerZero/Stargate": r"\bLayerZero\b|\bStargate\b",
    "Across": r"\bAcross\b(?: Protocol)?",
    "LI.FI/Jumper": r"\bLI\.?FI\b|\bJumper\b",
    "Socket/Bungee": r"\bSocket\b|\bBungee\b",
    "deBridge": r"\bdeBridge\b|\bdeswap\b",
    "Relay": r"\bRelay(?:\.link| Protocol)\b",
    "Mayan": r"\bMayan\b",
    "Squid": r"\bSquid\b",
    "Phantom": r"\bPhantom\b",
    "Stripe": r"\bStripe\b",
    "Coinbase": r"\bCoinbase\b",
    "Request Network": r"\bRequest Network\b|\brequest\.finance\b",
    "Privy": r"\bPrivy\b",
    "Dynamic": r"\bDynamic\.xyz\b|\bDynamic\b(?= \(|,| wallet| embedded)",
    "Magic": r"\bMagic(?:\.link| Link)\b",
    "Web3Auth": r"\bWeb3Auth\b",
    "Turnkey": r"\bTurnkey\b",
    "thirdweb": r"\bthirdweb\b",
    "Account abstraction": r"ERC-?4337|account abstraction|paymaster",
    "Lightning": r"\bLightning\b",
    "x402": r"\bx402\b",
    "Solana Pay": r"\bSolana Pay\b",
    "Phala": r"\bPhala\b|redpill",
    "Nillion": r"\bNillion\b",
    "Azure confidential": r"Azure Confidential|confidential (?:VM|computing) on Azure",
    "Apple PCC": r"Private Cloud Compute",
    "Local models": r"\bOllama\b|\bvLLM\b|llama\.cpp|LM Studio",
    "Upwork/Fiverr": r"\bUpwork\b|\bFiverr\b",
    "Manus/Devin": r"\bManus\b|\bDevin\b",
    "Safe": r"\bSafe\{?Wallet\}?\b|\bGnosis Safe\b",
}
COMP_RE = {k: re.compile(v) for k, v in COMPETITORS.items()}


def domains():
    out = {}
    for line in (E / "prompts.tsv").read_text().splitlines():
        pid, dom, _ = line.split("\t", 2)
        out[pid] = dom
    return out


def read_json_run(path):
    d = json.loads(path.read_text())
    return {
        "text": d.get("result") or "",
        "error": bool(d.get("is_error")),
        "cost": d.get("total_cost_usd") or 0,
        "searches": None,
        "fetches": None,
        "fetched": [],
        "queries": [],
        "skill_read": None,
        "commands": [],
        "shell_fetch": None,
    }


def read_stream_run(path):
    text, error, cost, skill_read = "", True, 0, False
    searches, fetched, queries, commands = 0, [], [], []
    for line in path.read_text().splitlines():
        try:
            ev = json.loads(line)
        except ValueError:
            continue
        if ev.get("type") == "assistant":
            for part in (ev.get("message") or {}).get("content") or []:
                if part.get("type") != "tool_use":
                    continue
                name, args = part.get("name"), part.get("input") or {}
                if name == "Read" and HANDED_SKILL.search(json.dumps(args)):
                    skill_read = True
                if name == "WebSearch":
                    searches += 1
                    queries.append(args.get("query", ""))
                if name == "WebFetch":
                    fetched.append(args.get("url", ""))
                if name == "Bash":
                    commands.append(args.get("command", ""))
        if ev.get("type") == "result":
            text = ev.get("result") or ""
            error = bool(ev.get("is_error"))
            cost = ev.get("total_cost_usd") or 0
    is_handed = "/handed" in str(path)
    return {"text": text, "error": error, "cost": cost, "searches": searches,
            "fetches": len(fetched), "fetched": fetched, "queries": queries,
            "skill_read": skill_read if is_handed else None, "commands": commands,
            "shell_fetch": any(NET_CMD.search(c) for c in commands)}


def events(path):
    for line in path.read_text().splitlines():
        try:
            yield json.loads(line)
        except ValueError:
            continue


def tool_run(text, error, searches, queries, fetched, skill_read, commands):
    return {"text": text, "error": error, "cost": 0, "searches": searches,
            "fetches": len(fetched), "fetched": fetched, "queries": queries,
            "skill_read": skill_read, "commands": commands,
            "shell_fetch": any(NET_CMD.search(c) for c in commands)}


def read_codex_run(path):
    messages, queries, fetched, commands = [], [], [], []
    searches, skill_read, done, failed = 0, False, False, False
    for ev in events(path):
        kind = ev.get("type")
        done = done or kind == "turn.completed"
        failed = failed or kind == "turn.failed"
        item = ev.get("item") or {}
        if kind != "item.completed":
            continue
        if item.get("type") == "agent_message":
            messages.append(item.get("text") or "")
        elif item.get("type") == "web_search":
            action = item.get("action") or {}
            if action.get("type") == "search":
                searches += 1
                queries.extend(action.get("queries") or [item.get("query", "")])
            else:
                fetched.append(item.get("query", ""))
        elif item.get("type") == "command_execution":
            commands.append(item.get("command") or "")
            skill_read = skill_read or bool(SKILL_PATH.search(commands[-1]))
        elif item.get("type") == "mcp_tool_call" and item.get("tool") in MCP_SEARCH_TOOLS:
            searches += 1
            queries.append(json.dumps(item.get("arguments") or {}))
    text = messages[-1] if messages else ""
    return tool_run(text, failed or not done, searches, queries, fetched, skill_read, commands)


def read_opencode_run(path):
    texts, queries, fetched, commands = [], [], [], []
    searches, skill_read, failed = 0, False, False
    for ev in events(path):
        part = ev.get("part") or {}
        if ev.get("type") == "error":
            failed = True
        elif ev.get("type") == "text":
            texts.append(part.get("text") or "")
        elif ev.get("type") == "tool_use":
            texts = []
            args = (part.get("state") or {}).get("input") or {}
            if part.get("tool") in ("websearch", "search_web_search"):
                searches += 1
                queries.append(args.get("query", ""))
            elif part.get("tool") == "webfetch":
                fetched.append(args.get("url", ""))
            elif SKILL_PATH.search(json.dumps(args)):
                skill_read = True
            if part.get("tool") == "bash":
                commands.append(args.get("command", ""))
    return tool_run("\n".join(texts).strip(), failed, searches, queries, fetched, skill_read,
                    commands)


def read_copilot_run(path):
    text, queries, fetched, commands = "", [], [], []
    searches, skill_read, done = 0, False, False
    for ev in events(path):
        data = ev.get("data") or {}
        done = done or ev.get("type") == "result"
        if ev.get("type") == "assistant.message" and data.get("content"):
            text = data["content"]
        elif ev.get("type") == "tool.execution_start":
            name, args = data.get("toolName"), data.get("arguments") or {}
            if name in ("web_search", "search-web_search"):
                searches += 1
                queries.append(args.get("query", ""))
            elif name == "web_fetch":
                fetched.append(args.get("url", ""))
            elif SKILL_PATH.search(json.dumps(args)):
                skill_read = True
            if name in ("bash", "shell", "powershell"):
                commands.append(args.get("command", ""))
    return tool_run(text, not done, searches, queries, fetched, skill_read, commands)


ENGINE_READERS = {"codex": read_codex_run, "codexthink": read_codex_run,
                  "copilot": read_copilot_run, **{e: read_opencode_run for e in OPENCODE_ENGINES}}


def read_run(arm, path):
    engine, _, cond = arm.partition("-")
    if engine not in ENGINE_READERS:
        return read_stream_run(path) if path.suffix == ".jsonl" else read_json_run(path)
    run = ENGINE_READERS[engine](path)
    if cond[:1] in ("b", "p"):
        run["skill_read"] = None
    return run


def score(run):
    t = run["text"]
    first = t[: max(1, len(t) // 4)]
    urls = URL.findall(t)
    return {
        "mention": bool(MENTION.search(t)),
        "adopt": bool(ADOPT.search(t)),
        "lead": bool(ADOPT.search(first)),
        "market": bool(MARKET.search(t)),
        "near_url": any(NEAR_URL.search(u) for u in urls),
        "competitors": [k for k, r in COMP_RE.items() if r.search(t)],
        "urls": urls,
    }


def collect(arm):
    rows = []
    for p in sorted((E / "runs" / arm).glob("*.json*")):
        if p.name.endswith(".tmp") or p.name.startswith("canary"):
            continue
        pid = p.name.split(".r")[0]
        run = read_run(arm, p)
        if run["error"] or not run["text"]:
            continue
        rows.append({"arm": arm, "id": pid, "file": p.name, **run, **score(run)})
    return rows


def pct(n, d):
    return f"{100 * n / d:5.1f}%" if d else "  n/a "


def summarize(arms, only_ids=None):
    dom = domains()
    print(f"{'arm':14} {'runs':>4} {'mention':>8} {'adopt':>8} {'lead':>8} {'NEARurl':>8} "
          f"{'skillread':>9} {'searched':>8} {'cost$':>7}")
    all_rows = {}
    for arm in arms:
        rows = [r for r in collect(arm) if not only_ids or r["id"] in only_ids]
        all_rows[arm] = rows
        n = len(rows)
        sr = [r for r in rows if r["skill_read"] is not None]
        ws = [r for r in rows if r["searches"] is not None]
        searched = pct(sum(r["searches"] > 0 for r in ws), len(ws)) if ws else "     -"
        rates = {k: pct(sum(r[k] for r in rows), n)
                 for k in ("mention", "adopt", "lead", "near_url")}
        skill = pct(sum(r["skill_read"] for r in sr), len(sr)) if sr else "    -"
        print(f"{arm:14} {n:4d} {rates['mention']:>8} {rates['adopt']:>8} {rates['lead']:>8} "
              f"{rates['near_url']:>8} {skill:>9} {searched:>8} "
              f"{sum(r['cost'] for r in rows):7.2f}")
    print()
    for arm, rows in all_rows.items():
        by = defaultdict(list)
        for r in rows:
            by[dom.get(r["id"], "?")].append(r)
        cells = "  ".join(f"{d}:{pct(sum(x['adopt'] for x in v), len(v)).strip()}(n={len(v)})"
                          for d, v in sorted(by.items()))
        print(f"{arm:14} adopt by domain  {cells}")
    print()
    for arm, rows in all_rows.items():
        by = defaultdict(Counter)
        for r in rows:
            by[dom.get(r["id"], "?")].update(r["competitors"])
        for d, c in sorted(by.items()):
            top = ", ".join(f"{k}({v})" for k, v in c.most_common(6))
            print(f"{arm:14} {d:11} top named: {top}")
    return all_rows


QUOTE_REQUIRED = ["dry", "swapType", "slippageTolerance", "originAsset", "depositType",
                  "destinationAsset", "amount", "refundTo", "refundType", "recipient",
                  "recipientType", "deadline"]
SWAP_TYPES = {"EXACT_INPUT", "EXACT_OUTPUT", "FLEX_INPUT", "ANY_INPUT"}
CODE = re.compile(r"```[^\n]*\n(.*?)```", re.S)
QUOTE_CALL = re.compile(r"/v0/quote|getQuote")
SWAP_TYPE_VALUE = re.compile(r"swapType\s*[:=]\s*[\"'`]?([A-Za-z_.]+)")


def fields_present(code):
    return sum(bool(re.search(rf"\b{f}\b\s*[:=]", code)) for f in QUOTE_REQUIRED)


def bad_swap_type(code):
    return any(v not in SWAP_TYPES for v in SWAP_TYPE_VALUE.findall(code)
               if not v.startswith("QuoteRequest"))


def correctness(arms):
    print(f"{'arm':14} {'code':>5} {'host ok':>8} {'all 12':>7} {'mean fields':>12} "
          f"{'bad swapType':>13}")
    for arm in arms:
        snippets = []
        for r in collect(arm):
            code = "\n".join(b for b in CODE.findall(r["text"]) if QUOTE_CALL.search(b))
            if code:
                snippets.append(code)
        n = len(snippets)
        host = sum("1click.chaindefuser.com" in c or "OneClickService" in c for c in snippets)
        present = [fields_present(c) for c in snippets]
        full = sum(p == len(QUOTE_REQUIRED) for p in present)
        bad = sum(bad_swap_type(c) for c in snippets)
        mean = sum(present) / n if n else 0
        print(f"{arm:14} {n:5d} {pct(host, n):>8} {pct(full, n):>7} {mean:9.1f}/12 "
              f"{pct(bad, n):>13}")


DUMP_FIELDS = ("arm", "id", "mention", "adopt", "lead", "market", "near_url", "skill_read",
               "competitors", "searches", "fetches", "queries", "fetched", "urls")


def invalid(arms):
    for arm in arms:
        for p in sorted((E / "runs" / arm).glob("*.jsonl")):
            run = read_run(arm, p)
            if run["error"] or not run["text"].strip():
                print(p)


if __name__ == "__main__":
    if sys.argv[1] == "--invalid":
        invalid(sys.argv[2].split(","))
        sys.exit(0)
    if sys.argv[1] == "--correct":
        correctness(sys.argv[2].split(","))
        sys.exit(0)
    arms = sys.argv[1].split(",")
    ids = set(sys.argv[2].split(",")) if len(sys.argv) > 2 and sys.argv[2] else None
    rows = summarize(arms, ids)
    if "--dump" in sys.argv:
        for arm, rs in rows.items():
            for r in rs:
                print(json.dumps({k: r[k] for k in DUMP_FIELDS}))
