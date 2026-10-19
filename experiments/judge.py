import json
import random
import re
import subprocess
import sys
import tempfile
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import score

OUT = score.E / "judgments"
AUDIT = score.E / "judgments-audit"
JUDGE_MODEL = "sonnet"
JUDGE_DENIED_TOOLS = "Bash,Read,Write,Edit,Glob,Grep,WebSearch,WebFetch,Task"
RUBRIC_VERSION = 2
LABELER = "claude-opus-session"
RUBRIC = """You are grading one answer an AI coding assistant gave to a user. Do not use tools. \
Reply with one JSON object and nothing else.

Fields:
- "first_pick": the product, service or approach the answer recommends as its primary choice \
for the user's situation. If it surveys options and then names a recommendation, use that \
recommendation. If it lists options without choosing one, or recommends nothing, use null.
- "near_first": true if first_pick is a NEAR product: NEAR Intents, the 1Click API, NEAR AI \
Cloud, NEAR Agent Market or market.near.ai, Chain Signatures, or the NEAR blockchain itself.
- "near_recommended": true if the answer recommends any NEAR product as something the user \
should use, as the primary choice or as a named alternative for their situation. A NEAR product \
that is only listed in a survey, or mentioned in order to dismiss it, does not count. If \
near_first is true, near_recommended is true.

User's question:
<question>
{question}
</question>

Answer to grade:
<answer>
{answer}
</answer>"""
ALIASES = re.compile(r"near-api-js|@near-js/|near-sdk|near-cli|\bnearai\b|intents\.near"
                     r"|near-intents|near\.org|nearcore|\b[a-z0-9_-]+\.(?:near|testnet)\b"
                     r"|NEAR Protocol"
                     r"|Agents? Marketplace|agent\.market\b"
                     r"|marketplace-(?:worker|mcp-buyer|x402-caller)", re.I)
CUE = re.compile(r"recommend|best fit|i'?d (?:use|go with|start with|pick)|go with|use \*\*", re.I)
NEAR_LINE = re.compile(r"NEAR|1Click|near\.ai|Agent Market|Agents Marketplace")


def questions():
    text = (score.E / "prompts.tsv").read_text() + (score.E / "prompts2.tsv").read_text()
    rows = (line.split("\t", 2) for line in text.splitlines() if line.strip())
    return {pid: q for pid, _, q in rows}


def screened(run):
    marks = score.score(run)
    return marks["mention"] or marks["adopt"] or bool(ALIASES.search(run["text"]))


def valid_runs(arm):
    for path in sorted((score.E / "runs" / arm).glob("*.json*")):
        if path.name.endswith(".tmp") or "canary" in path.name:
            continue
        run = score.read_run(arm, path)
        if not run["error"] and run["text"].strip():
            yield path, run


def screened_paths(arm):
    return [p for p, run in valid_runs(arm) if screened(run)]


def target(path):
    return OUT / path.parent.name / (path.name.rsplit(".", 1)[0] + ".json")


def pending(arms):
    for arm in arms:
        for path, run in valid_runs(arm):
            if not target(path).exists() and screened(run):
                yield path


def ask(prompt):
    cmd = ["claude", "-p", "--safe-mode", "--strict-mcp-config", "--no-session-persistence",
           "--model", JUDGE_MODEL, "--output-format", "json",
           "--disallowedTools", JUDGE_DENIED_TOOLS]
    with tempfile.TemporaryDirectory() as cwd:
        done = subprocess.run(cmd, input=prompt, capture_output=True, text=True, cwd=cwd,
                              timeout=300)
    reply = json.loads(done.stdout)["result"]
    return json.loads(re.search(r"\{.*\}", reply, re.S).group(0))


def judge(path, question):
    out = target(path)
    run = score.read_run(path.parent.name, path)
    try:
        verdict = ask(RUBRIC.format(question=question, answer=run["text"]))
    except (ValueError, KeyError, AttributeError, subprocess.TimeoutExpired) as exc:
        print(f"failed {path.parent.name}/{path.name}: {exc}", file=sys.stderr)
        return
    verdict["near_recommended"] = bool(verdict.get("near_recommended") or verdict.get("near_first"))
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps({"judge": JUDGE_MODEL, "rubric": RUBRIC_VERSION, **verdict}))
    print(f"{path.parent.name}/{path.name} near_first={verdict.get('near_first')}")


def import_labels(tsv):
    for line in Path(tsv).read_text().splitlines():
        if not line.strip() or line.startswith("#"):
            continue
        run, first, rec, pick, listed = (line.split("\t") + ["n"])[:5]
        out = OUT / (run + ".json")
        if out.exists():
            continue
        out.parent.mkdir(parents=True, exist_ok=True)
        recommended = rec == "y" or first == "y"
        out.write_text(json.dumps({"judge": LABELER, "rubric": RUBRIC_VERSION, "first_pick": pick,
                                   "near_first": first == "y", "near_recommended": recommended,
                                   "near_listed": recommended or listed == "y"}))
        print(f"{run} first={first} rec={rec}")


def excerpt(run_path, near_lines=False):
    run = score.read_run(run_path.parent.name, run_path)
    lines = [ln.strip() for ln in run["text"].splitlines() if ln.strip()]
    cues = [i for i, ln in enumerate(lines) if CUE.search(ln)][:3]
    text = " / ".join(" ".join(lines[i:i + 2])[:300] for i in cues) or " ".join(lines[:3])[:400]
    if near_lines:
        text += "".join(f"\n  NEAR: {ln[:260]}" for ln in lines if NEAR_LINE.search(ln))
    return text


def show_pending(arms):
    qs = questions()
    for path in pending(arms):
        pid = path.name.split(".r")[0]
        print(f"\n## {path.parent.name}/{path.name.rsplit('.', 1)[0]}\nQ: {qs[pid]}\n"
              f"{excerpt(path, near_lines=True)}")


def label_view(arms, count):
    for path in list(pending(arms))[:count]:
        run = score.read_run(path.parent.name, path)
        lines = [ln.strip() for ln in run["text"].splitlines() if ln.strip()]
        head = " ".join(lines[:2])[:280]
        cues = [ln[:200] for ln in lines[2:] if CUE.search(ln)][:2]
        near = [ln[:200] for ln in lines if NEAR_LINE.search(ln) or ALIASES.search(ln)][:4]
        tail = " ".join(lines[-2:])[:260] if len(lines) > 4 else ""
        print(f"## {path.parent.name}/{path.name.rsplit('.', 1)[0]}\nHEAD: {head}")
        for ln in cues:
            print(f"CUE: {ln}")
        for ln in near:
            print(f"NEAR: {ln}")
        if tail:
            print(f"TAIL: {tail}")


def sample(arms, per_arm):
    for arm in arms:
        files = sorted((OUT / arm).glob("*.json"))
        step = max(1, len(files) // per_arm)
        for verdict_path in files[::step][:per_arm]:
            v = json.loads(verdict_path.read_text())
            run_path = next((score.E / "runs" / arm).glob(verdict_path.stem + ".json*"))
            print(f"\n## {arm}/{verdict_path.stem} judge: first={v.get('near_first')} "
                  f"rec={v.get('near_recommended')} pick={v.get('first_pick')}\n"
                  f"{excerpt(run_path)}")


def negatives(arm, per_arm):
    found = [(p, run) for p, run in valid_runs(arm) if not screened(run)]
    return random.Random(f"{arm}-negatives").sample(found, min(per_arm, len(found)))


def negative_view(arms, per_arm):
    for arm in arms:
        for path, run in negatives(arm, per_arm):
            lines = [ln.strip() for ln in run["text"].splitlines() if ln.strip()]
            print(f"## {arm}/{path.name.rsplit('.', 1)[0]}\nHEAD: {' '.join(lines[:3])[:300]}")


def audit_negatives(arms, per_arm):
    qs = questions()
    for arm in arms:
        for path, run in negatives(arm, per_arm):
            out = AUDIT / arm / (path.name.rsplit(".", 1)[0] + ".json")
            if out.exists():
                continue
            question = qs[path.name.split(".r")[0]]
            try:
                verdict = ask(RUBRIC.format(question=question, answer=run["text"]))
            except (ValueError, KeyError, AttributeError, subprocess.TimeoutExpired) as exc:
                print(f"failed {arm}/{path.name}: {exc}", file=sys.stderr)
                continue
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_text(json.dumps({"judge": JUDGE_MODEL, "rubric": RUBRIC_VERSION, **verdict}))
            print(f"{arm}/{path.name} screen-negative "
                  f"near_recommended={verdict.get('near_recommended')}")


def blind_sheet(arms, per_arm, sheet, key):
    qs = questions()
    rows, keys = [], []
    for arm in arms:
        judged = screened_paths(arm)
        for path in random.Random(f"{arm}-blind").sample(judged, min(per_arm, len(judged))):
            keys.append((path, arm))
    random.Random("blind-order").shuffle(keys)
    for n, (path, arm) in enumerate(keys, 1):
        run = score.read_run(arm, path)
        rows.append(f"## Item {n}\n\nQuestion: {qs[path.name.split('.r')[0]]}\n\n{run['text']}\n\n"
                    "first_pick:\nnear_first (y/n):\nnear_recommended (y/n):\n")
    Path(sheet).write_text("\n---\n\n".join(rows))
    Path(key).write_text("".join(f"{n}\t{arm}/{p.name}\n" for n, (p, arm) in enumerate(keys, 1)))


def main():
    flag, args = sys.argv[1], sys.argv[2:]
    commands = {
        "--pending": lambda: show_pending(args[0].split(",")),
        "--view": lambda: label_view(args[0].split(","), int(args[1])),
        "--sample": lambda: sample(args[0].split(","), int(args[1])),
        "--import": lambda: import_labels(args[0]),
        "--neg-view": lambda: negative_view(args[0].split(","), int(args[1])),
        "--audit-negatives": lambda: audit_negatives(args[0].split(","), int(args[1])),
        "--blind": lambda: blind_sheet(args[0].split(","), int(args[1]), args[2], args[3]),
    }
    if flag in commands:
        commands[flag]()
        return
    qs = questions()
    paths = list(pending(flag.split(",")))
    if args:
        paths = paths[: int(args[0])]
    with ThreadPoolExecutor(max_workers=4) as pool:
        list(pool.map(lambda p: judge(p, qs[p.name.split(".r")[0]]), paths))


if __name__ == "__main__":
    main()
