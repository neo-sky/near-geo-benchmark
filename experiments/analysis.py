import itertools
import json
import math
import random
import re
import sys
from collections import defaultdict
from pathlib import Path

from scipy.stats import fisher_exact

sys.path.insert(0, str(Path(__file__).parent))
import judge
import score

Z = 1.959963984540054
BOOTSTRAPS = 10000
PERMUTATIONS = 20000
RECOMMEND = re.compile(
    r"recommend|best fit|best option|my pick|i'?d (?:use|go with|start with)|go with", re.I
)
NEAR_TERMS = re.compile(r"\bNEAR\b|1Click|market\.near\.ai|NEAR Agent Market", re.I)

ARMS = {
    "baseline-memory-opus48": ["mem-opus48"],
    "baseline-web-opus48": ["web-opus48", "web2-opus48"],
    "baseline-forced-search-opus48": ["web-forced-opus48"],
    "baseline-memory-opus55": ["mem-opus55"],
    "baseline-web-opus55": ["web-opus55", "web2-opus55"],
    "skill-current-opus48": ["handed-h1"],
    "skill-problem-first-opus48": ["handed-h2"],
    "skill-current-opus55": ["handed55-h1"],
    "skill-problem-first-opus55": ["handed55-h2"],
    "market-skills-current-opus48": ["handed-m1"],
    "market-skills-near-named-opus48": ["handed-m2"],
    "market-skills-current-opus55": ["handed55-m1"],
    "market-skills-near-named-opus55": ["handed55-m2"],
    "results-product-first-page-opus48": ["handed-r-a"],
    "results-problem-first-page-opus48": ["handed-r-b"],
    "results-hosted-product-page-opus48": ["handed-r-c"],
    "results-product-first-page-opus55": ["handed55-r-a"],
    "results-problem-first-page-opus55": ["handed55-r-b"],
    "docs-page-without-instructions-opus48": ["handed-i-a"],
    "docs-page-with-instructions-opus48": ["handed-i-b"],
}

COMPARISONS = [
    ("skill opened", "skill_read", "skill-current-opus48", "skill-problem-first-opus48"),
    ("skill opened", "skill_read", "skill-current-opus55", "skill-problem-first-opus55"),
    ("NEAR named", "mention", "market-skills-current-opus48", "market-skills-near-named-opus48"),
    ("NEAR named", "mention", "market-skills-current-opus55", "market-skills-near-named-opus55"),
    ("marketplace named", "market", "market-skills-current-opus48",
     "market-skills-near-named-opus48"),
    ("NEAR recommended", "judge_rec", "skill-current-opus48", "skill-problem-first-opus48"),
    ("NEAR first pick", "judge_first", "skill-current-opus48", "skill-problem-first-opus48"),
    ("NEAR recommended", "judge_rec", "results-product-first-page-opus48",
     "results-problem-first-page-opus48"),
    ("NEAR recommended", "judge_rec", "results-product-first-page-opus55",
     "results-problem-first-page-opus55"),
    ("NEAR first pick", "judge_first", "results-problem-first-page-opus48",
     "results-hosted-product-page-opus48"),
    ("NEAR first pick", "judge_first", "results-product-first-page-opus55",
     "results-problem-first-page-opus55"),
    ("NEAR skills suggested", "skills_suggested", "docs-page-without-instructions-opus48",
     "docs-page-with-instructions-opus48"),
    ("EXACT_OUTPUT on payment tasks", "exact_output", "docs-page-without-instructions-opus48",
     "docs-page-with-instructions-opus48"),
    ("NEAR recommended", "judge_rec", "baseline-memory-opus48", "skill-problem-first-opus48"),
]
ENGINES = ["codex", "copilot", "deepseek", "glm", "qwen", "kimi", "grok", "gemini"]
ENGINE_CONDS = {
    "b1": "baseline-memory", "b2": "baseline-web", "b3": "baseline-forced-search",
    "s1": "skill-current", "s2": "skill-problem-first",
    "l1": "skill-product-matched", "c1": "skill-current-competing",
    "c2": "skill-problem-first-competing",
    "m1": "market-skills-current", "m2": "market-skills-near-named",
    "r1": "results-product-first-page", "r2": "results-problem-first-page",
    "r3": "results-hosted-product-page",
    "t1": "tool-results-product-first-page", "t2": "tool-results-problem-first-page",
    "t3": "tool-results-hosted-product-page",
    "d1": "docs-page-without-instructions", "d2": "docs-page-with-instructions",
    "a1": "cloud-skill-current", "a2": "cloud-skill-problem-first",
    "k1": "build-skills-current", "k2": "build-skills-problem-first",
    "n1": "baseline-memory-geo-sandbox",
}
ENGINE_COMPARISONS = [
    ("skill opened", "skill_read", "s1", "s2"),
    ("NEAR named", "mention", "m1", "m2"),
    ("marketplace named", "market", "m1", "m2"),
    ("NEAR recommended", "judge_rec", "s1", "s2"),
    ("NEAR first pick", "judge_first", "s1", "s2"),
    ("NEAR recommended", "judge_rec", "r1", "r2"),
    ("NEAR first pick", "judge_first", "r1", "r2"),
    ("NEAR first pick", "judge_first", "r2", "r3"),
    ("NEAR skills suggested", "skills_suggested", "d1", "d2"),
    ("EXACT_OUTPUT on payment tasks", "exact_output", "d1", "d2"),
    ("NEAR recommended", "judge_rec", "b1", "s2"),
    ("skill opened", "skill_read", "s1", "l1"),
    ("skill opened", "skill_read", "l1", "s2"),
    ("NEAR first pick", "judge_first", "s1", "l1"),
    ("NEAR first pick", "judge_first", "l1", "s2"),
    ("NEAR first pick", "judge_first", "s1", "c1"),
    ("NEAR first pick", "judge_first", "s2", "c2"),
    ("NEAR first pick", "judge_first", "c1", "c2"),
    ("NEAR recommended", "judge_rec", "r1", "t1"),
    ("NEAR recommended", "judge_rec", "r2", "t2"),
    ("NEAR first pick", "judge_first", "r3", "t3"),
    ("NEAR recommended", "judge_rec", "a1", "a2"),
    ("NEAR first pick", "judge_first", "a1", "a2"),
    ("NEAR recommended", "judge_rec", "b1", "a2"),
    ("NEAR recommended", "judge_rec", "k1", "k2"),
    ("NEAR first pick", "judge_first", "k1", "k2"),
    ("NEAR recommended", "judge_rec", "b1", "k2"),
    ("NEAR named", "mention", "b1", "n1"),
]
NEW_PROMPTS = {line.split("\t", 1)[0]
               for line in (score.E / "prompts2.tsv").read_text().splitlines()}
PROMPT_SETS = {
    "": lambda pid: pid not in NEW_PROMPTS,
    "new-": lambda pid: pid in NEW_PROMPTS and not pid.startswith("ctl-"),
    "ctl-": lambda pid: pid.startswith("ctl-"),
}
ARM_FILTERS = {}
for engine in ENGINES:
    for prefix, keep in PROMPT_SETS.items():
        for cond, name in ENGINE_CONDS.items():
            if (score.E / "runs" / f"{engine}-{cond}").is_dir():
                ARMS[f"{name}-{prefix}{engine}"] = [f"{engine}-{cond}"]
                ARM_FILTERS[f"{name}-{prefix}{engine}"] = keep
        for label, metric, a, b in ENGINE_COMPARISONS:
            COMPARISONS.append((label, metric, f"{ENGINE_CONDS[a]}-{prefix}{engine}",
                                f"{ENGINE_CONDS[b]}-{prefix}{engine}"))
JUDGED = score.E / "judgments"


def wilson(k, n):
    if n == 0:
        return [0.0, 0.0]
    p = k / n
    denom = 1 + Z * Z / n
    centre = (p + Z * Z / (2 * n)) / denom
    half = Z * math.sqrt(p * (1 - p) / n + Z * Z / (4 * n * n)) / denom
    return [max(0.0, centre - half), min(1.0, centre + half)]


def first_recommendation_names_near(text):
    line = next((ln for ln in text.splitlines() if RECOMMEND.search(ln)), "")
    return bool(NEAR_TERMS.search(line))


def verdict(row):
    if not (row["mention"] or row["adopt"] or judge.ALIASES.search(row["text"])):
        return {"near_first": False, "near_recommended": False, "near_listed": False}
    path = JUDGED / row["arm"] / (row["file"].rsplit(".", 1)[0] + ".json")
    if not path.exists():
        return {}
    return json.loads(path.read_text())


def enrich(row):
    text = row["text"]
    is_payment = row["id"].startswith("pay-")
    v = verdict(row)
    return {
        **row,
        "first_rec": first_recommendation_names_near(text),
        "judge_first": v.get("near_first"),
        "judge_rec": v.get("near_recommended"),
        "judge_listed": v.get("near_listed"),
        "skills_suggested": bool(re.search(r"agent-skills|skills add", text, re.I)),
        "exact_output": "EXACT_OUTPUT" in text if is_payment else None,
        "searched_any": (row["searches"] or 0) > 0 if row["searches"] is not None else None,
    }


METRICS = ["mention", "adopt", "lead", "market", "skill_read", "first_rec", "judge_first",
           "judge_rec", "judge_listed", "skills_suggested", "exact_output", "searched_any",
           "shell_fetch"]


def summarize_arm(rows):
    out = {"n": len(rows), "prompts": len({r["id"] for r in rows}),
           "unlabelled": sum(r["judge_rec"] is None for r in rows)}
    for m in METRICS:
        vals = [r[m] for r in rows if r[m] is not None]
        if not vals:
            continue
        k = sum(bool(v) for v in vals)
        out[m] = {"k": k, "n": len(vals), "rate": k / len(vals), "ci95": wilson(k, len(vals))}
    return out


def prompt_rates(rows, metric, prompts):
    by = defaultdict(list)
    for r in rows:
        if r["id"] in prompts and r[metric] is not None:
            by[r["id"]].append(bool(r[metric]))
    return {p: sum(v) / len(v) for p, v in by.items()}


def sign_flip_p(diffs):
    observed = abs(sum(diffs))
    if len(diffs) <= 16:
        flips = itertools.product((1, -1), repeat=len(diffs))
        hits = [abs(sum(s * d for s, d in zip(signs, diffs))) >= observed - 1e-12
                for signs in flips]
        return sum(hits) / len(hits)
    rng = random.Random(11)
    hits = sum(abs(sum(d if rng.random() < 0.5 else -d for d in diffs)) >= observed - 1e-12
               for _ in range(PERMUTATIONS))
    return (hits + 1) / (PERMUTATIONS + 1)


def bootstrap_ci(diffs):
    rng = random.Random(7)
    means = sorted(sum(rng.choice(diffs) for _ in diffs) / len(diffs) for _ in range(BOOTSTRAPS))
    return [means[int(0.025 * BOOTSTRAPS)], means[int(0.975 * BOOTSTRAPS) - 1]]


def compare(rows, label, metric, a, b):
    if a not in rows or b not in rows:
        return None
    shared = {r["id"] for r in rows[a]} & {r["id"] for r in rows[b]}
    pa, pb = prompt_rates(rows[a], metric, shared), prompt_rates(rows[b], metric, shared)
    prompts = sorted(set(pa) & set(pb))
    if not prompts:
        return None
    va = [bool(r[metric]) for r in rows[a] if r["id"] in prompts and r[metric] is not None]
    vb = [bool(r[metric]) for r in rows[b] if r["id"] in prompts and r[metric] is not None]
    a_k, b_k = sum(va), sum(vb)
    diffs = [pb[p] - pa[p] for p in prompts]
    return {
        "label": label, "metric": metric, "a": a, "b": b, "prompts": len(prompts),
        "a_k": a_k, "a_n": len(va), "b_k": b_k, "b_n": len(vb),
        "mean_prompt_diff": sum(diffs) / len(diffs), "ci95_prompt_bootstrap": bootstrap_ci(diffs),
        "p_signflip_prompts": sign_flip_p(diffs),
        "p_fisher_two_sided": fisher_exact([[a_k, len(va) - a_k], [b_k, len(vb) - b_k]])[1],
    }


def holm(tests, key):
    families = defaultdict(list)
    for t in tests:
        families[t["a"].rsplit("-", 1)[1]].append(t)
    for family in families.values():
        ordered = sorted(family, key=lambda t: t[key])
        running = 0.0
        for i, t in enumerate(ordered):
            running = max(running, min(1.0, (len(ordered) - i) * t[key]))
            t[key + "_holm"] = running
            t["family_size"] = len(ordered)


def audit(names):
    for name in names:
        for d in ARMS[name]:
            for r in score.collect(d):
                line = next((ln for ln in r["text"].splitlines() if RECOMMEND.search(ln)), "")
                print(json.dumps({"arm": name, "id": r["id"],
                                  "first_rec": bool(NEAR_TERMS.search(line)),
                                  "line": line.strip()[:240]}))


def main():
    if len(sys.argv) > 2 and sys.argv[1] == "--audit":
        audit(sys.argv[2].split(","))
        return
    rows = {name: [enrich(r) for d in dirs for r in score.collect(d)
                   if ARM_FILTERS.get(name, lambda pid: True)(r["id"])]
            for name, dirs in ARMS.items()}
    rows = {name: r for name, r in rows.items() if r}
    arms = {name: summarize_arm(r) for name, r in rows.items()}
    tests = [c for c in (compare(rows, *spec) for spec in COMPARISONS) if c]
    holm(tests, "p_signflip_prompts")
    holm(tests, "p_fisher_two_sided")
    print(json.dumps({"arms": arms, "tests": tests}, indent=2))


if __name__ == "__main__":
    main()
