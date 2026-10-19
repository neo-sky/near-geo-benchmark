---
title: "NEAR in AI Coding Agents: Problem, Findings and Solutions"
---

**Goal:** Understand why agents have trouble finding NEAR when users ask about relevant products or services.

**Experiment:** I asked 65 developer questions (35 from Illia Polosukhin's report, 30 new) to ten AI coding agent setups: Claude Code with two models, Codex, GitHub Copilot, and DeepSeek, GLM, Qwen, Kimi, Gemini and Grok in opencode. I then added NEAR material one piece at a time and measured how often each agent recommended NEAR.

# Core problem: NEAR's documents are not made for agents

Agents know NEAR's products by name but do not reach them from a user's problem. An agent recommends what is installed, what it finds in search or what it remembers, and NEAR's documents miss all three (Appendix 1).

- **Not written for agents.** Skill descriptions name the product, not the user's task, so agents often skip them, and no page gives agents rules: 11 of 15 answers that hardcoded NEAR Intents token IDs made them up.

- **Not where agents look.** NEAR has nothing in the Claude Code or Codex plugin marketplaces, the MCP registry or the x402 directory, so agents fall back on web search.

- **Not found in search.** Agents land on other vendors' pages; the NEAR Intents developer docs never appeared in logged searches.

- **Not readable by crawlers.** docs.near.ai and cloud.near.ai block AI training crawlers, and market.near.ai and near-intents.org are nearly blank without JavaScript, so future models will not learn them.

# Findings

1. **Agents do not recommend NEAR on their own.** None of 462 answers recommended NEAR without web search; 5 of 731 did with it.

2. **They know NEAR's products but do not pick them.** Asked by name, Claude and Codex describe NEAR Intents, the 1Click API, NEAR AI Cloud and Chain Signatures correctly, and every agent gave the right SDK and endpoint (8 of 8).

3. **NEAR is missing where agents look.** Codex picks a vendor from memory, then searches only that vendor's site (107 of 152 searches, none on a NEAR site). Agents that search openly found no NEAR page for any cross-chain or app-building question. When a NEAR page appeared, NEAR was recommended in 5 of 24 answers; otherwise never.

4. **Once NEAR's material reaches the agent, it works.** A skill description that names the user's task did best in every agent and product tested (answers recommending NEAR):

| Product and agent | No skill | Current description | Rewritten description |
|----------------------------------------|----------|---------------------|-----------------------|
| NEAR Intents, Codex | 0 of 28 | 12 of 28 | 26 of 28 |
| NEAR Intents, Copilot | 0 of 28 | 8 of 28 | 20 of 27 |
| NEAR Intents, Claude Code (Opus 4.8) | 0 of 28 | 25 of 28 | 27 of 28 |
| NEAR AI Cloud, Codex | 0 of 11 | 10 of 14 | 14 of 14 |
| Building apps (NEAR first choice), Codex | 0 of 18 | 10 of 18 | 15 of 18 |

5. **Against competitors, the description decides.** Next to skills from Circle, LI.FI, Stripe, Coinbase and Request Network, the current NEAR Intents skill was opened once in 28 runs. The rewritten one was opened most, and NEAR was recommended in 10 of 28.

6. **Agents credit the name they are given.** With NEAR in the marketplace skills' names, answers naming NEAR rose from 1 to 22 of 32 in Codex, 6 to 24 in Claude Code and 0 to 17 in Copilot.

Full method and statistics are in the research paper.

# Solutions

**1. Make NEAR's documents work for agents.**

- Rewrite every skill description around the user's task. NEAR Intents, NEAR AI Cloud and two app-building skills are done and tested.

- List NEAR in the Claude Code and Codex plugin marketplaces, the MCP registry, the x402 directory and skills.sh. The plugin and an MCP server are built.

- Add Agent Instructions to the docs and claim NEAR's Context7 listings, telling agents to fetch token IDs and use the exact-amount quote for fixed prices. On the 1Click page, these instructions raised exact-amount quotes from 0 to 13 of 20 payment answers.

- Let AI crawlers in: change Cloudflare's AI-crawler setting on docs.near.ai and cloud.near.ai, render market.near.ai on the server, and add an llms.txt to near-intents.org.

**2. Build what agents want to recommend.**

- A hosted payment link on 1Click (get-paid link, invoice, tip jar, pay-now button), payable from any chain. A page describing one made NEAR the first choice in about half of payment answers, against 0 to 4 of 32 for today's API page.

- A NEAR-named API host and SDK package, so the code agents write says NEAR. Only 46% of public code calling the 1Click host names NEAR Intents; for Circle's API, 89% names CCTP.

**3. Fix the name and the content.**

- Use one name, NEAR Agent Market, instead of agent.market, Agents Marketplace, NEAR AI Agents Market and agents-market API.

- Publish use-case pages and GitHub examples for the 689 searches agents ran (five pages written), and register the sites with Bing Webmaster Tools and IndexNow.

- Build openly attributed coverage on other sites: Wikipedia talk-page requests, tutorials and answers to developers' questions.

# To do

| Owner | Next step |
|------------------------------|----------------------------------------------------------------|
| Developer relations and docs | Publish the skills and plugin, submit the listings, add Agent Instructions, claim Context7 |
| Infrastructure | Change the Cloudflare AI-crawler setting, render market.near.ai on the server |
| Intents team | Decide on the hosted payment link and the NEAR-named host and package |
| Marketing | Adopt one marketplace name, publish the use-case pages, start third-party coverage |
| Me | Rerun the benchmark monthly (needs an Exa API key and about $40 a month in model credits) |

# Appendix 1: Where NEAR's documents fail agents

| Document or listing | Problem | Effect |
|----------------------------|--------------------------------------------|--------------------------------|
| docs.near.ai, cloud.near.ai | Block GPTBot, ClaudeBot and Common Crawl (HTTP 403); no docs.near.ai page in Common Crawl | Left out of future models' training data |
| market.near.ai | About 20 words without JavaScript; content only in unlinked Markdown files; no sitemap or robots.txt | Crawlers see an almost empty page |
| near-intents.org | No text without JavaScript; llms.txt returns 404 | Crawlers see an empty page |
| docs.near-intents.org | Never appeared in a logged agent search | Searching agents miss the developer docs |
| near-intents skill | Description names the product, not the user's task | Opened in 1 of 28 runs next to competitors' skills |
| NEAR AI Cloud and app-building skills | Descriptions name the tools, not the user's task | NEAR recommended in 10 of 14 and first in 10 of 18, against 14 of 14 and 15 of 18 rewritten |
| Claude Code and Codex plugin marketplaces | No NEAR plugin; in Claude Code's, Circle has the only crypto plugin among 315 | No one-step install |
| MCP registry | No NEAR server; Stripe has 28 entries, Coinbase 12 | MCP clients cannot find NEAR |
| x402 ecosystem directory | NEAR not listed | Absent beside other x402 services |
| Context7 (/near/intents, /near/docs) | Indexed; claim status and agent rules unknown | Agents get the docs without the rules |
| 1Click API docs page | No Agent Instructions block | Exact-amount quote used in 0 of 20 payment answers |
| Marketplace name | agent.market, Agents Marketplace, NEAR AI Agents Market, agents-market API | NEAR named in 1 of 32 Codex answers |
| SDK and API host | @defuse-protocol and 1click.chaindefuser.com | Code using NEAR Intents mostly does not say NEAR |
| Wikipedia, Stack Overflow | Article omits NEAR Intents, NEAR AI and Chain Signatures; no posts on NEAR Intents or 1Click | Thin where models learn |
