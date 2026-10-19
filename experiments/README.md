# Experiments

Prompts, condition materials, labels and analysis for the study in `../near-geo-paper.docx`. The paper describes the method and results; this file covers the data and how to score it. The agents run through `../engines/run_engine.sh`, described in the top-level README.

## Files

| Path | Contents |
| --- | --- |
| `prompts.tsv` | The 35 prompts from Polosukhin's public report: id, domain, prompt |
| `prompts2.tsv` | 30 new prompts, including the control prompts (ids starting `ctl-`) where NEAR is the wrong answer |
| `probes.tsv` | Probes that ask about NEAR products by name (`fwd-`) or for their packages (`pkg-`) |
| `skills-variants/<condition>/` | Skill files installed in the S, M, A and K conditions; `l1-description.txt` is the product-terms description for L1 |
| `skills-competitors/` | The five competing skills installed in C1 and C2 |
| `handed/<condition>.txt` | Context given to the agent: search results for R and T, documentation pages for D, skill text for the first-phase S and M runs |
| `pages/` | The NEAR pages written or trimmed for the R and D conditions |
| `labels-v2.tsv` | Labels for every answer that mentions NEAR, under the rubric in Appendix D of the paper |
| `author-labels.tsv` | First-phase labels for the answers the model annotator did not reach |
| `results.json` | Every rate, interval and test, written by `analysis.py` |
| `first-phase/` | The runners and job list for the first-phase Claude Code runs |

The raw agent logs (`runs/`) and per-run verdicts (`judgments/`) are not in the repository.

## Scripts

| Script | Purpose |
| --- | --- |
| `score.py` | Reads each agent's event log into one format and scores the lexical measures |
| `judge.py` | Screens answers for NEAR, shows the ones that need a label, imports labels, and runs the model annotator |
| `analysis.py` | Rates with Wilson intervals, matched-prompt comparisons with sign-flip tests, bootstrap intervals and Holm correction per agent |
| `tables.py` | The paper's result tables and figures from `results.json` |
| `render.py` | Places the tables in the paper source |
| `quote_check.py` | Checks the 1Click quote code in answers against the live token list and replays complete requests as dry quotes |

```bash
python3 -I judge.py --pending <arm,...>    # excerpts of answers that still need a label
python3 -I judge.py --view <arm,...> 40    # fuller excerpts, for labelling
python3 -I judge.py --import labels-v2.tsv
python3 -I score.py <arm,arm> [ids] [--dump]
python3 -I score.py --correct <arm,arm>
python3 -I quote_check.py <arm,arm> quotes.json
../source/build.sh                         # analysis, tables, figures and both documents
```

An arm is `<agent>-<condition>`, for example `codex-s2`. The first-phase Claude Code arms are named by model and condition, for example `mem-opus48` or `handed55-h2`.

## First phase

The first phase ran Claude Code only, with skills and pages supplied through the system prompt, before the multi-agent harness existed. `first-phase/jobs.txt` lists every run; each line is a runner invocation from the repository root.

| Runner | Conditions | Output |
| --- | --- | --- |
| `run_json.sh prompts\|probes <arm> <model> none\|web <rep> <id>` | B1 and B2 with JSON output, forward probes | `runs/<arm>/<id>.r<rep>.json` |
| `run_web.sh open\|forced <arm> <model> <rep> <id>` | B2 and B3 with tool logs | `runs/<arm>/<id>.r<rep>.jsonl` |
| `run_handed.sh <model> <variant> <rep> <id>` | S, M, R and D through the system prompt | `runs/handed-<variant>/` or `runs/handed55-<variant>/` |

`claude -p --safe-mode --strict-mcp-config --no-session-persistence` loads no instruction files, memory, user-installed skills, hooks or MCP servers. Opus 5.5 needs a newer Claude Code than Opus 4.8, so the runners use `$CLAUDE_LATEST` from `engines/env.sh` whenever a model is named. Disabling WebSearch and WebFetch does not block network access through the shell; the paper reports the shell fetches it found.
