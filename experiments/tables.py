import json
import sys
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt

sys.path.insert(0, str(Path(__file__).parent))
from analysis import ENGINE_CONDS

ENGINES = {
    "opus48": "Claude Code, Opus 4.8",
    "opus55": "Claude Code, Opus 5.5",
    "codex": "Codex, GPT-6 Astra",
    "copilot": "Copilot, GPT-6 Luna",
    "deepseek": "opencode, DeepSeek V4.1 Flash",
    "glm": "opencode, GLM 5.3 Flash",
    "qwen": "opencode, Qwen 3.8 Flash",
    "kimi": "opencode, Kimi K2.5",
    "gemini": "opencode, Gemini 3.7 Flash",
    "grok": "opencode, Grok Build 0.1",
}
SHORT = {"opus48": "Opus 4.8", "opus55": "Opus 5.5", "codex": "Codex", "copilot": "Copilot",
         "deepseek": "DeepSeek", "glm": "GLM", "qwen": "Qwen", "kimi": "Kimi", "gemini": "Gemini",
         "grok": "Grok"}
CODES = {name: code.upper() for code, name in ENGINE_CONDS.items()}
ORDER = ["B1", "B2", "B3", "N1", "S1", "S2", "L1", "C1", "C2", "A1", "A2", "K1", "K2", "M1", "M2",
         "R1", "R2", "R3", "T1", "T2", "T3", "D1", "D2"]
MEASURES = {
    "mention": "Named NEAR",
    "market": "Named marketplace",
    "skill_read": "Opened skill",
    "judge_listed": "NEAR listed",
    "judge_rec": "NEAR recommended",
    "judge_first": "NEAR first choice",
    "skills_suggested": "Suggested NEAR skills",
    "exact_output": "Used EXACT_OUTPUT",
    "searched_any": "Searched",
    "shell_fetch": "Fetched through the shell",
}
COMMON_CRAWL_PAGES = [
    ("docs.cdp.coinbase.com", 856, False),
    ("developers.circle.com", 409, False),
    ("docs.phala.com", 317, False),
    ("docs.privy.io", 176, False),
    ("docs.near.org", 147, True),
    ("docs.near-intents.org", 24, True),
    ("docs.near.ai", 0, True),
]
CHART_STYLE = {
    "font.family": "DejaVu Sans",
    "font.size": 9,
    "axes.edgecolor": "#999999",
    "axes.labelcolor": "#111111",
    "xtick.color": "#444444",
    "ytick.color": "#111111",
}
NEAR_BLUE = "#2a78d6"
NEUTRAL = "#a6a6a6"


def split(key, prefix):
    for name, code in CODES.items():
        head = f"{name}-{prefix}"
        if key.startswith(head) and key[len(head):] in ENGINES:
            return code, key[len(head):]
    return None, None


def matrix(arms, metric, prefix=""):
    cells, engines = {}, []
    for key, arm in arms.items():
        code, engine = split(key, prefix)
        if code and arm.get(metric):
            cells[(code, engine)] = arm[metric]
            if engine not in engines:
                engines.append(engine)
    engines = [e for e in ENGINES if e in engines]
    codes = [c for c in ORDER if any((c, e) in cells for e in engines)]
    return codes, engines, cells


def matrix_table(arms, metric, prefix=""):
    codes, engines, cells = matrix(arms, metric, prefix)
    lines = ["| Condition | " + " | ".join(SHORT[e] for e in engines) + " |",
             "|" + "|".join(["------------"] + ["--------:"] * len(engines)) + "|"]
    for code in codes:
        row = [f"{cells[(code, e)]['k']}/{cells[(code, e)]['n']}" if (code, e) in cells else "-"
               for e in engines]
        lines.append(f"| {code} | " + " | ".join(row) + " |")
    return "\n".join(lines)


def p_text(p):
    return f"{p:.1e}".replace("e-0", "e-") if p < 0.001 else f"{p:.3f}"


def tests_table(tests, prefix=""):
    lines = ["| Comparison | Measure | Engine | A | B | Prompts | "
             "Mean prompt difference (95% CI) | p, prompts (Holm) |",
             "|" + "|".join(["-----------", "--------------", "--------", "------:", "------:",
                             "------:", "----------------", "---------"]) + "|"]
    rows = []
    for t in tests:
        ca, engine = split(t["a"], prefix)
        cb, _ = split(t["b"], prefix)
        if not ca or not cb:
            continue
        lo, hi = t["ci95_prompt_bootstrap"]
        rows.append((ORDER.index(ca), ORDER.index(cb), t["metric"], list(ENGINES).index(engine),
                     f"| {ca} vs {cb} | {MEASURES[t['metric']]} | {SHORT[engine]} | "
                     f"{t['a_k']}/{t['a_n']} | {t['b_k']}/{t['b_n']} | {t['prompts']} | "
                     f"{t['mean_prompt_diff']:+.2f} ({lo:+.2f} to {hi:+.2f}) | "
                     f"{p_text(t['p_signflip_prompts_holm'])} |"))
    lines += [r[-1] for r in sorted(rows)]
    return "\n".join(lines)


def heatmap(arms, metric, out):
    codes, engines, cells = matrix(arms, metric)
    data = [[cells[(c, e)]["rate"] * 100 if (c, e) in cells else float("nan") for e in engines]
            for c in codes]
    fig, ax = plt.subplots(figsize=(0.62 * len(engines) + 1.4, 0.34 * len(codes) + 1.0), dpi=200,
                           layout="constrained")
    image = ax.imshow(data, cmap="Blues", vmin=0, vmax=100, aspect="auto")
    for i, code in enumerate(codes):
        for j, engine in enumerate(engines):
            cell = cells.get((code, engine))
            if not cell:
                continue
            ax.text(j, i, f"{cell['k']}/{cell['n']}", ha="center", va="center", fontsize=6.5,
                    color="white" if cell["rate"] > 0.55 else "#111111")
    ax.set_xticks(range(len(engines)), [SHORT[e] for e in engines], rotation=40, ha="right",
                  fontsize=8)
    ax.set_yticks(range(len(codes)), codes, fontsize=8)
    ax.tick_params(length=0)
    for side in ax.spines.values():
        side.set_visible(False)
    bar = fig.colorbar(image, ax=ax, shrink=0.8)
    bar.set_label(f"{MEASURES[metric]} (% of answers)", fontsize=8)
    bar.ax.tick_params(labelsize=7)
    fig.savefig(out)
    plt.close(fig)


def common_crawl(out):
    labels = [host for host, _, _ in COMMON_CRAWL_PAGES]
    values = [pages for _, pages, _ in COMMON_CRAWL_PAGES]
    colors = [NEAR_BLUE if near else NEUTRAL for _, _, near in COMMON_CRAWL_PAGES]
    with plt.rc_context(CHART_STYLE):
        fig, ax = plt.subplots(figsize=(6.0, 0.42 * len(values) + 0.75), dpi=200,
                               layout="constrained")
        for side in ("top", "right", "left"):
            ax.spines[side].set_visible(False)
        ax.tick_params(axis="y", length=0)
        ax.grid(axis="x", color="#dddddd", linewidth=0.7)
        ax.set_axisbelow(True)
        ax.barh(range(len(values)), values, color=colors, height=0.6)
        for y, v in enumerate(values):
            ax.text(v + max(values) * 0.012, y, f"{v:,}", va="center", fontsize=8, color="#444444")
        ax.set_yticks(range(len(values)), labels)
        ax.set_ylim(len(values) - 0.5, -0.5)
        ax.set_xlim(0, max(values) * 1.12)
        ax.set_xlabel("Documentation pages captured with HTTP 200")
        fig.savefig(out)
    plt.close(fig)


def wilson_equation(out):
    with plt.rc_context(CHART_STYLE):
        fig = plt.figure(figsize=(4.6, 0.9), dpi=200)
        fig.text(0.5, 0.5, r"$\frac{\hat{p} + \frac{z^2}{2n} \pm z\sqrt{"
                 r"\frac{\hat{p}(1-\hat{p})}{n} + \frac{z^2}{4n^2}}}{1 + \frac{z^2}{n}},"
                 r"\quad \hat{p} = \frac{k}{n}$",
                 ha="center", va="center", fontsize=20, color="#111111")
        fig.savefig(out, facecolor="white", bbox_inches="tight", pad_inches=0.04)
    plt.close(fig)


def main():
    data = json.loads(Path(sys.argv[1]).read_text())
    fragments, figures = Path(sys.argv[2]), Path(sys.argv[3])
    fragments.mkdir(parents=True, exist_ok=True)
    figures.mkdir(parents=True, exist_ok=True)
    for prefix in ("", "new-", "ctl-"):
        tag = prefix.rstrip("-") or "orig"
        for metric in MEASURES:
            if matrix(data["arms"], metric, prefix)[0]:
                (fragments / f"matrix-{tag}-{metric}.md").write_text(
                    matrix_table(data["arms"], metric, prefix) + "\n")
        (fragments / f"tests-{tag}.md").write_text(tests_table(data["tests"], prefix) + "\n")
    heatmap(data["arms"], "judge_rec", figures / "fig-heatmap-recommended.png")
    common_crawl(figures / "fig-common-crawl.png")
    wilson_equation(figures / "eq-wilson.png")


if __name__ == "__main__":
    main()
