# NEAR in AI coding agents

A benchmark of how often AI coding agents recommend NEAR products when developers ask neutral questions, and of which changes to an agent's context move that rate. It starts from the 35 prompts in Illia Polosukhin's GEO report for NEAR, adds 30 more, and runs them across ten agent and model configurations, with and without NEAR material in the agent's context.

The full write-up is [`near-geo-paper.docx`](near-geo-paper.docx). [`near-geo-proposal.docx`](near-geo-proposal.docx) is a three-page summary of the findings, proposed changes and target outcomes.

## Results in brief

| Measure | Result |
| --- | --- |
| NEAR recommended with no help and no web search | 0 of 462 answers |
| NEAR recommended with web search | 5 of 731 answers |
| Codex with NEAR Intents skill, published description | 12 of 28 |
| Codex with a description that names the users' tasks | 26 of 28 |
| The same two descriptions next to five competitors' skills | 1 and 10 of 28 |
| Answers naming NEAR when the marketplace skills carry NEAR's name (Codex) | 1 to 22 of 32 |
| NEAR recommended on control questions where it is the wrong answer | 0 of 63 |

Agents describe NEAR's products correctly when asked by name, but do not reach them from a user's problem. Once NEAR's material is in the agent's context it works in every agent tested, and the wording of a skill's description decides whether the agent opens it. The paper gives every rate with its interval, the matched-prompt tests and the limitations.

## Agents

| Agent | Model |
| --- | --- |
| Claude Code | Opus 4.8, Opus 5.5 |
| Codex | GPT-6 Astra |
| GitHub Copilot | GPT-6 Luna |
| opencode | DeepSeek V4.1 Flash, GLM 5.3 Flash, Qwen 3.8 Flash, Kimi K2.5, Gemini 3.7 Flash, Grok Build 0.1 |

Each condition adds one element to the agent's context and holds everything else fixed: nothing (B1), web search (B2, B3), a NEAR skill with different descriptions (S1, S2, L1), the same skill next to competitors' skills (C1, C2), marketplace skills with and without NEAR in their names (M1, M2), search results with different NEAR pages (R1 to R3, T1 to T3), a documentation page with and without an instruction block for agents (D1, D2), and skills for NEAR AI Cloud and for building applications (A1, A2, K1, K2). Table 2 of the paper lists them in full.

## Repository

| Path | Contents |
| --- | --- |
| `engines/` | `run_engine.sh`, which runs one prompt for one agent and condition in an isolated sandbox; sandbox setup; the job list; agent configuration |
| `experiments/` | Prompts, condition materials, labels, results and the analysis scripts (see `experiments/README.md`) |
| `source/` | Markdown sources of the paper and the proposal and the script that builds both |
| `research/` | Notes on how models gather training data and how agents search, the crawl audit, and the agents' logged search queries |
| `materials/` | The NEAR material built and tested in the study: a plugin package for `near/agent-skills`, a read-only NEAR Intents MCP server and five use-case pages |

The raw agent logs are not included.

## Running the benchmark

Requirements: Linux with bubblewrap, Node.js 24, jq, and Python 3 with scipy and matplotlib. Building the documents also needs pandoc and LibreOffice.

1. Copy `engines/env.example.sh` to `engines/env.sh` and set the paths for this machine. `openrouter_key` and `claude_token` print the two API credentials; the example reads them from environment variables.
2. Install the agent CLIs into `$ENGINE_HOME/cli`:
   ```bash
   mkdir -p "$ENGINE_HOME/cli" && cp engines/package.json "$ENGINE_HOME/cli/"
   npm install --prefix "$ENGINE_HOME/cli"
   ```
   Codex runs from `$CODEX_DIR` with its login in `$ENGINE_HOME/codex` (`CODEX_HOME="$ENGINE_HOME/codex" codex login`). Copilot uses the token from `gh auth token`. The opencode models run through OpenRouter.
3. Build the sandboxes, one working directory per condition, under `$SANDBOXES`:
   ```bash
   engines/setup_sandboxes.sh
   ```
4. Run one prompt, or a batch from the job list:
   ```bash
   engines/run_engine.sh codex s2 1 pay-request-invoice
   xargs -P 4 -L 1 bash -c '"$0" "$@"' < engines/jobs.txt
   ```
   A run whose output already exists is skipped, so a batch can be stopped and restarted. `engines/jobs.txt` lists every job queued in the study; some did not run because Copilot's monthly quota and the open-model budget ran out. `engines/budget_guard.sh <cap> <pid>` stops the opencode runs once OpenRouter spending reaches the cap.
5. Label the answers that mention NEAR and build the results and documents:
   ```bash
   python3 experiments/judge.py --pending codex-s2
   python3 experiments/judge.py --import experiments/labels-v2.tsv
   source/build.sh
   ```

Each run executes inside bubblewrap with a private home directory and a read-only copy of its sandbox, so the agent sees no user configuration, memory or instruction files. Web tools are disabled except in B2 and B3. The prompts in `engines/canary.tsv` ask the agent to list everything in its context, which checks a configuration before a batch.
