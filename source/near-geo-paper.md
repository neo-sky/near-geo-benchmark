---
title: "Visibility of NEAR Products in the Recommendations of AI Coding Agents: A Study Across Agents and Models"
abstract: |
  AI coding agents increasingly choose the services a developer builds on. I measured how often ten agent and model configurations recommend NEAR products in answer to neutral developer questions, and what changes that rate. Without web search, none of 462 answers recommended a NEAR product, and with search 5 of 731 did, although the agents described NEAR's products correctly when asked by name. Search logs show why. Codex restricted 107 of 152 searches to vendors it had already chosen, none of them NEAR, and for agents that searched openly, no NEAR page appeared in any result set for cross-chain transfers or building applications. Once NEAR's material reached the agent, it worked in every agent tested. A skill whose description names the users' tasks raised recommendations in Codex from 12 to 26 of 28, held up better than the current description next to five competitors' skills (10 against 1 of 28), and carried over to NEAR AI Cloud and to building applications. Putting NEAR in the marketplace's name raised the share of answers crediting NEAR from 1 to 22 of 32 in Codex, and a page describing a hosted payment link made NEAR the first choice in about half of payment answers. On control questions where NEAR is the wrong answer, none of 63 answers recommended it. I recommend task-naming skill descriptions, distribution of NEAR's skills where agents load them, rules for agents in NEAR's documentation and on Context7, one product name, a hosted payment link, use-case content for agents' actual queries registered with the search indexes they use, NEAR-named code, open crawler access and an openly attributed third-party footprint for the current products, tracked by a monthly run of this benchmark that reports memory, search and supplied context separately.
---

# 1 Introduction

Coding agents now select much of the infrastructure that a developer ends up using. Asked how to accept a payment from any blockchain, an agent names a service, writes the integration against it and, in most cases, the developer ships that code. The services an agent recommends without prompting therefore gain integrations that other services do not see, and the recommendation becomes a distribution channel in its own right.

Earlier measurement for NEAR found that coding agents rarely surface NEAR in answer to neutral questions [1, 2]. That work ran five agent harnesses and established the rate, but not the mechanism. The first phase of this study tested one agent, Claude Code. This paper extends the same design to ten agent and model configurations: Claude Code with Opus 4.8 and with Opus 5.5, ChatGPT Codex, GitHub Copilot, and six models from DeepSeek, Zhipu (GLM), Alibaba (Qwen), Moonshot (Kimi), Google (Gemini) and xAI (Grok) running in the opencode agent.

I address five research questions.

1. RQ1: How often does a default coding agent recommend NEAR for problems that NEAR products address, and does it know those products when asked about them directly?

2. RQ2: Which changes to the agent's context change that rate, and do the effects hold across agents? I test an installed skill, the wording of its description, competing skills, the product name a skill exposes, a NEAR page among search results delivered through the agent's instructions or through a search tool, and an instruction block on a documentation page.

3. RQ3: Do the effects hold on prompts the materials were not written for, and do agents recommend NEAR where it is the wrong answer?

4. RQ4: Does NEAR's web content reach the crawls from which training corpora for future models are built?

5. RQ5: When agents search the web, what do they search for, and does NEAR appear in what they find?

Section 2 reviews related work. Section 3 describes the setup and Section 4 the results. Section 5 discusses where recommendations are lost and how the findings carry over to other answer engines, Section 6 gives recommendations, Section 7 lists limitations and Section 8 concludes.

# 2 Background and Related Work

## 2.1 Generative engine optimization

Aggarwal et al. introduced generative engine optimization (GEO) as the study of how content becomes visible in the answers of generative search engines, and reported that adding statistics, quotations and citations to a page increased its visibility [10]. Subsequent work found that AI search engines draw their citations overwhelmingly from earned, third-party sources rather than from brands' own pages [11], and an industry analysis found that brand mentions across the web correlated more strongly with visibility in Google's AI Overviews than backlinks did (0.664 against 0.218) [12]. Recommendation lists are also unstable, and repeated queries to the same engine rarely return the same set of brands [13]. For this reason I report rates over repeated runs and many prompts rather than single answers.

Most GEO work studies consumer search engines. Coding agents differ in two respects that matter here. They act on their recommendations by writing code, and in their default configuration they often answer from model knowledge without searching (Section 4.2).

## 2.2 How language models store and retrieve facts

Berglund et al. showed that models trained on statements of the form "A is B" often fail to answer the reverse question "what is B?" with A, an effect they call the reversal curse [3]. Product documentation is usually written in the first direction ("NEAR Intents is a cross-chain settlement protocol"), whereas users ask in the second ("How do I move USDC from Ethereum to Solana?"). Allen-Zhu and Li found that knowledge which appeared in a single form during pretraining was stored but could rarely be extracted, while five differently worded descriptions per entity raised extraction accuracy from 9.7% to 96.6% [4, 5, 6]. These results suggest one explanation for an agent that recognises a product but does not recommend it. They are not the only explanation, and this study does not distinguish between them (Section 5.1).

## 2.3 How training data is collected

Model providers collect web text with their own crawlers and from Common Crawl, and each separates training from search. OpenAI's GPTBot collects training data, OAI-SearchBot serves ChatGPT search and ChatGPT-User fetches pages a user asks for [37]. Anthropic runs ClaudeBot, Claude-SearchBot and Claude-User for the same three purposes [38]. Google crawls with Googlebot and lets a site decide, through the Google-Extended token, whether its pages may train Gemini, without any effect on Search [39]. A site can therefore be visible in search and absent from training. Since July 2025, Cloudflare has blocked known AI crawlers by default on new domains unless the owner opts in [44].

Common Crawl remains the largest shared source. Of 47 models released between 2019 and October 2023, at least 64% were trained on it, and it supplied more than 80% of GPT-3's tokens [40]. Its crawler does not execute JavaScript [7, 17], and corpora derived from it, such as FineWeb-Edu and DCLM, apply quality filters that favour educational and informative text [8, 9]. A page whose content is rendered only in the browser contributes no text, and a page that describes a product without explaining a problem is less likely to pass such filters. Providers also license content directly, for example Reddit's posts for Google and OpenAI and Stack Overflow's questions and answers for OpenAI [41]. Code models are trained on public repositories collected at scale, as in The Stack [42], and Wikipedia is part of most pretraining mixtures.

What a model learns reaches users slowly. Published knowledge cutoffs fall from about four months to more than a year before release, and declared cutoffs can differ from those measured empirically [43]. As a rough planning figure, content published now reaches models released six to eighteen months later.

## 2.4 Context supplied to coding agents

Coding agents can be extended with skills, plugins and Model Context Protocol (MCP) servers. Each agent tested here lists installed skills for the model by name and one-line description and loads a skill's full text only when the model judges the description relevant. Claude Code reads skills from `.claude/skills`, Codex and the Gemini CLI from `.agents/skills`, Copilot from `.github/skills` and opencode from `.opencode/skills`. Codex, Copilot and opencode read a project instruction file named AGENTS.md, and Claude Code reads CLAUDE.md. ChatGPT's plugin directory and Claude's connector directory exclude tools that transfer money or crypto assets [18, 19], so for payment products these mechanisms are available mainly in developer agents.

## 2.5 Prior measurement for NEAR

Polosukhin's report ran the same 35 prompts through five agent harnesses (Codex, Claude Code, opencode with DeepSeek, and pi and Hermes with GLM), 175 runs in total, and scored each answer from 0 to 1 on whether it cited and adopted NEAR products [1, 2]. I reuse the 35 prompts so that the problems are comparable, run them in empty, neutrally named directories, and score answers on separate measures rather than one composite score.

## 2.6 Search and context at answer time

When an agent searches, it draws on a provider's index. ChatGPT's search relies heavily on Bing, with one analysis finding 87% of its citations among Bing's top results, although OpenAI does not disclose the mix [45]. Bing accepts notifications of new pages through IndexNow [54]. Claude's web search is attributed to Brave Search on circumstantial evidence, including Anthropic's list of subprocessors [46], and Brave's crawler indexes what Googlebot may reach [47]. Gemini and Google's AI Overviews use Google Search's ranking. Across engines, answers draw mainly on third-party sources rather than brands' own pages [11, 48], and mentions of a brand across the web correlate with visibility more strongly than links to its site [12]. These findings are observational and come mostly from vendors of measurement tools. The llms.txt convention has spread quickly, but in a study of 137,000 domains, 97% of llms.txt files received no request in a month [49].

Inside a coding agent, a skill's description is what the model matches a request against to decide whether to load it [50]. Documentation services add another route: Context7 serves library documentation to coding agents through MCP, lets anyone add a public repository and lets owners attach rules that agents see with the documentation [51]. Two further results bear on newer products. Language models over-rely on popular libraries, which the authors note makes newer projects harder to discover [52], and code models suggest packages that do not exist, about one in five in the largest study, with lower rates in newer models [53].

# 3 Method

## 3.1 Agents and models

Table 1 lists the ten configurations. Codex and Copilot ran with the models their accounts select by default. The six opencode configurations used each vendor's lower-cost model through OpenRouter, because the study's budget did not cover flagship models at this volume. Gemini ran through opencode because Google's free access for personal accounts is no longer available to the Gemini CLI and its free API tier allows too few requests per day.

Table: Table 1. Agents and models.

| Configuration | Agent | Model | Skills read from | Instruction file |
|--------------------------------|------------------|----------------------------|---------------------|------------------|
| Claude Code, Opus 4.8 | Claude Code 2.1.170 | Claude Opus 4.8 | Supplied in the system prompt | Supplied in the system prompt |
| Claude Code, Opus 5.5 | Claude Code 2.1.300 | Claude Opus 5.5 | Supplied in the system prompt | Supplied in the system prompt |
| Codex | Codex CLI 0.154 | GPT-6 Astra (account default) | `.agents/skills` | AGENTS.md |
| Copilot | Copilot CLI 1.0.98 | GPT-6 Luna (automatic selection) | `.github/skills` | AGENTS.md |
| DeepSeek | opencode 1.19.3 | DeepSeek V4.1 Flash | `.opencode/skills` | AGENTS.md |
| GLM | opencode 1.19.3 | GLM 5.3 Flash | `.opencode/skills` | AGENTS.md |
| Qwen | opencode 1.19.3 | Qwen 3.8 Flash | `.opencode/skills` | AGENTS.md |
| Kimi | opencode 1.19.3 | Kimi K2.5 | `.opencode/skills` | AGENTS.md |
| Gemini | opencode 1.19.3 | Gemini 3.7 Flash | `.opencode/skills` | AGENTS.md |
| Grok | opencode 1.19.3 | Grok Build 0.1 | `.opencode/skills` | AGENTS.md |

The Claude Code configurations come from the first phase of the study and were run differently from the others. Claude Code ran with `--safe-mode`, which loads no instruction files, memory, user skills or MCP servers, but also no project skills. Skills and pages were therefore supplied by appending their text to the system prompt and placing the skill files where the agent could read them. Every other agent loaded skills through its own skill mechanism and read pages from AGENTS.md. Section 7 discusses this difference.

## 3.2 Isolation

Each run of Codex, Copilot and opencode took place in a sandbox built with bubblewrap. The user's home directory and /tmp were replaced by empty in-memory file systems, the environment was cleared, and the agent saw only its own configuration, its credentials and a neutrally named working directory. A canary prompt asking the agent to list every instruction file, memory, skill, MCP server and web tool in its context was run for each agent and returned only the test material and the agent's built-in skills.

The working directory was mounted read-only for every agent, and each agent's own file-writing tool was denied. This matches Claude Code's default non-interactive behaviour, which denied 394 of the 485 file writes and 222 of the 633 shell commands that Claude attempted in the first phase. Two earlier batches of runs for the other agents were discarded. In the first, the working directories were shared and writable, so later runs could read files that earlier runs had created. In the second, the workspaces were private but writable, so the other agents built complete projects while Claude could not, which made the comparison unequal and raised costs.

Three agent-specific settings were needed for equal treatment.

- **Codex.** Codex includes an apps service that offers a live web search tool even when Codex's own web search is disabled. Three no-web runs used it before I noticed, so the service was disabled and every Codex run made with it available was repeated.
- **opencode.** opencode asks for permission before an agent reads a directory outside the workspace, and in non-interactive mode an unanswered request ends the session. Grok Build tried to use /tmp in 18 of its first 36 runs and ended them without an answer. I changed these permissions from ask to deny, so the request fails and the agent continues, as the other agents do, and repeated the affected runs.
- **Copilot.** Copilot registers file watchers for its configuration at start-up and failed when the machine's limit on watchers was reached. The limit was raised and the failed runs repeated.

An audit after the runs found four gaps in this isolation. None changes a baseline result, and each is reported where it affects a comparison.

- **Shell network access.** Disabling web tools did not remove network access, because the sandbox shared the host's network. In B1, 8 of 462 runs fetched a page or API through the shell (Codex 2, DeepSeek 1, Grok 4, Qwen 1), from vendors such as OpenAI, LI.FI, Request Network and Ollama. None reached a NEAR site.
- **Copilot's web fetch.** Copilot's `--deny-tool` setting did not stop its `web_fetch` tool, which is the only web tool Copilot offers. Copilot fetched pages in 16 of 70 B1 runs, 8 of 55 skill runs, 15 of 94 search-result runs, 12 of 32 documentation runs, 6 of 64 marketplace runs and all 18 probes. Copilot's comparisons between conditions therefore have occasional web access on both sides, and its probes do not measure knowledge from training. The `--excluded-tools` setting removes the tool and replaces `--deny-tool` for future runs.
- **Shared opencode data.** Because the workspace was read-only, opencode agents saved projects in opencode's data directory, which persisted across runs. One Grok B2 run listed and read projects left by other runs; its answer did not mention NEAR. Each opencode run now gets an empty data directory.
- **Claude Code probes.** The probe runs for Claude Code did not record tool calls. Claude Code reported denied shell commands on the market.near.ai probes, but the Opus 5.5 answers quote the site's current title, so they may reflect a fetch rather than training.

## 3.3 Prompts

The 35 problem prompts are taken unchanged from Polosukhin's public report (Appendix A). They cover building on-chain applications (9 prompts), cross-chain transfers (4), payments (8), paying for services (2), private AI inference (4), hiring agents (4) and agent commerce (4). None names NEAR or any other vendor.

I wrote 30 further prompts to test whether the effects carry over to wording the materials were not written for (Appendix A.2). Twenty-one restate problems from the same domains in new terms. The other nine are controls for which NEAR is the wrong answer, such as card subscriptions for a US software product, Apple Pay in an iOS app, payroll by direct deposit and a swap on Ethereum mainnet. A recommendation of NEAR on a control prompt counts as an over-recommendation.

To test product knowledge separately, six forward probes name a NEAR product and ask what it is (NEAR Intents, the 1Click API, NEAR AI Cloud, Chain Signatures, market.near.ai and x402 on NEAR), and three package probes ask for install commands and minimal code. Each probe ran twice per agent with web tools disabled.

## 3.4 Conditions

Table 2 lists the conditions. B1 to B3 measure the default agent. Each other condition adds one element to the agent's context and holds everything else fixed.

Table: Table 2. Experimental conditions. Repeats are per prompt for Claude Code, Codex and Copilot; the opencode configurations ran one repeat per prompt.

| Code | Context supplied to the agent | Prompts | Repeats |
|------|------------------------------------------------------------------|---------|---------|
| B1 | Nothing; web tools disabled | 35 | 2 |
| B2 | Nothing; web search enabled | 35 | 2 |
| B3 | Web search enabled and an instruction to search before answering | 35 | 1 |
| S1 | NEAR Intents skill with its current description | 14 | 2 |
| S2 | NEAR Intents skill with a description written around user problems | 14 | 2 |
| L1 | NEAR Intents skill with a description in product terms, matched to S2 in facts and length | 14 | 2 |
| C1 | S1 plus five competing skills | 14 | 2 |
| C2 | S2 plus five competing skills | 14 | 2 |
| M1 | The agent marketplace's three skills under their current names | 8 | 4 |
| M2 | The same skills with NEAR in the names and descriptions | 8 | 4 |
| R1 to R3 | Four search results in the instruction file, with a NEAR product page (R1), a page written around the payer's problem (R2) or a page describing a hosted payment-link product (R3) | 8 | 4 |
| T1 to T3 | The same four results returned by a search tool | 8 | 2 |
| D1, D2 | NEAR's 1Click documentation page without and with an Agent Instructions block | 8 | 2 to 4 |
| A1, A2 | NEAR AI Cloud skill with its published description (A1) or a description written around user problems (A2) | 7 | 2 |
| K1, K2 | NEAR's three app-building skills with their published descriptions (K1) or with problem-first descriptions on two of them (K2) | 9 | 2 |
| N1 | Nothing, in a working directory named geo-sandbox | 10 | 2 |

In S1 and S2 the skill files differed only in the description line (Appendix C.1). S2's description is longer than S1's and covers more of the benchmark's tasks, so a difference between them can come from wording, coverage or length. L1 separates these. Its description states exactly the facts in S2's, in product terms rather than user problems, and is within 3% of S2's length (Appendix C.1). S1 against L1 therefore measures added coverage and length at constant framing, and L1 against S2 measures framing at constant facts and length.

The competing skills in C1 and C2 cover the same tasks as the NEAR skill: Circle CCTP, LI.FI, Stripe payments, Coinbase payments and Request Network (Appendix C.7). I wrote them from each vendor's public documentation, in the same format as NEAR's skill.

In the R conditions the four search results were placed in AGENTS.md (in the system prompt for Claude) under the heading "Web search results retrieved for the user's question". The first, third and fourth were the live documentation of Stripe (stablecoin payments), Coinbase (payment acceptance) and Request Network, and the NEAR page was always second. R3 describes a hosted payment-link product that NEAR does not offer, so it measures the effect of product form and makes no claim about NEAR's current offering. The T conditions deliver the same four documents as the result of a search tool provided through MCP, with web search otherwise disabled and the instruction to search before answering. Results delivered by a tool are treated by agents as data rather than instructions, so T measures whether the R effects survive the channel through which retrieved pages normally arrive. In T the position of the NEAR result rotated from first to fourth across prompts and repeats. The rotation was set by a hash of the prompt and repeat and came out unbalanced: across Codex's 48 T runs the NEAR result was first in 6, second in 9, third in 18 and fourth in 15, so it sat lower on average than in R, where it was always second. T also carries the instruction to search, which R does not. Section 4.7 compares T and R at matched positions.

A1 and A2 extend the skill test to NEAR AI Cloud on the four private-inference prompts and three new ones. The two skill files share one body and differ only in the description line; A2's description is the one in the plugin package (Appendix C). K1 and K2 extend it to building applications, the largest domain in the prompt set. Both install NEAR's near-api-js, near-smart-contracts and near-dapp skills. In K2 the near-api-js and near-smart-contracts descriptions name the problems in the build prompts, such as users who never pay gas or an app that may act for a user only within limits, and each claim is backed by the skill's body. N1 repeats the default condition in a directory named after the earlier harness's sandbox, to test whether the directory name explains the difference from that study (Section 4.14). A1 to K2 and N1 ran on Codex only, and A2 and K2 also ran the nine control prompts once.

## 3.5 Measures

Table 3 defines the measures. Named NEAR is lexical. Opened skill, Searched and Fetched through the shell are read from the agent's event log. NEAR listed, NEAR recommended and NEAR first choice require reading the answer (Section 3.6).

Table: Table 3. Outcome measures.

| Measure | Definition |
|--------------------------|------------------------------------------------------------------------------|
| Named NEAR | The answer contains "NEAR" as a word, or "Near Protocol", "Near Intents" or "Near AI". The match is case-sensitive. |
| Named marketplace | The answer names the marketplace as "Agents Marketplace", market.near.ai, agent.market or "NEAR Agent Market". |
| Opened skill | The event log shows the agent reading the skill's SKILL.md file or loading it through a skill tool. |
| Searched | The event log shows at least one web search, or a call to the search tool in T. |
| Fetched through the shell | The event log shows a shell command that makes a network request, such as curl. |
| NEAR listed | The answer offers a NEAR product as an option for the user's situation, with or without endorsing it. |
| NEAR recommended | The answer recommends a NEAR product for the user's situation, as its primary choice or as a named alternative. A product listed only in a survey of options, or mentioned in order to dismiss it, does not count. |
| NEAR first choice | The answer's primary recommendation is a NEAR product. |
| Suggested NEAR skills | The answer tells the user to install NEAR's agent skills. |
| Used EXACT_OUTPUT | A 1Click quote in a payment answer uses the EXACT_OUTPUT swap type. |
| NEAR in search results | A search the agent ran returned at least one page on a NEAR host (near.org, near.ai, near-intents.org, agent.market and their subdomains). Read from logs that record search results. |
| Search share | The share of agents' own search queries for which a NEAR page is among the first eight results of a fixed search engine (Section 3.9). |

## 3.6 Annotation

Answers that matched neither the Named NEAR pattern nor any NEAR product name, package, host or account address (Appendix D) were labelled negative without reading. Every other answer was labelled against the rubric in Appendix D, which defines the three judged measures so that a first choice is always also a recommendation and an answer that lists options without choosing has no first choice. The same rules were applied to every agent, and the Claude answers from the first phase were relabelled under them.

All answers were labelled by one annotator, an LLM working from excerpts that showed each answer's opening and closing lines and every line naming NEAR, with the full answer read whenever these did not decide the case. To check for product names the screen missed, I searched all 1,583 screen-negative answers for NEAR terms outside the screen: 1Click, the 1Click host, Defuse, intents, market.near.ai, Chain Signatures and the marketplace skill names. The only misses were four M1 answers that referred to the marketplace through its skill names (one each from Claude Code with Opus 4.8, DeepSeek, GLM and Qwen). The skill names were added to the screen and these answers labelled. Every other match was a generic use of a word such as intents, as in Stripe's Payment Intents. The same audit found 111 screened answers from the opencode models, mostly in the M, R and D conditions, that had not been labelled and were therefore missing from the denominators. They were labelled, the analysis now counts unlabelled answers in every condition, and the report build stops while any remain. A blind sample for a human annotator, showing the question and answer without any verdict, has been prepared and is reported separately when complete.

## 3.7 Statistical analysis

Each rate is reported with a 95% Wilson score interval. For k positive outcomes in n runs and z = 1.96, the interval is

![](figures/eq-wilson.png){width=3.4in}

Repeated runs of one prompt are not independent, so I treat the prompt as the unit of analysis. Each comparison is restricted to prompts present in both conditions. For each prompt I compute the rate in each condition and report the mean difference across prompts with a 95% bootstrap interval that resamples prompts (10,000 resamples). Significance is tested with a paired sign-flip permutation test on the per-prompt differences, exact up to 16 prompts, and the p values are adjusted with Holm's method within each agent's family of comparisons. With 8 to 14 prompts per condition, a single agent rarely yields an adjusted p value below 0.05 unless almost every prompt moves in the same direction. The main evidence is therefore whether an effect appears consistently across independent agents.

## 3.8 Crawl and site measurements

I requested key pages on each NEAR site from a residential IP address, using the user-agent strings of a browser and of ten AI and search crawlers, and recorded the status after following redirects. A status code obtained this way shows how a rule keyed on the user agent responds. It does not show what a verified crawler receives from its own IP range. For each page I also extracted the text present in the raw HTML, which is what a crawler that does not execute JavaScript stores. I queried Common Crawl's index for each host in the CC-MAIN-2026-25, CC-MAIN-2026-34 and CC-MAIN-2026-39 crawls and counted captures with HTTP status 200 [16], repeating each query that failed with a gateway error until it returned captures or an explicit empty result. Finally, I used GitHub code search, which reports approximate totals, to count public files that call the 1Click API host and the share of them that also mention NEAR Intents, and did the same for Circle's CCTP API. I also searched the official MCP registry for NEAR servers and checked whether NEAR appears in the x402 ecosystem directory. For the sources that training draws on, I read NEAR's Wikipedia article, counted Stack Overflow questions under NEAR's tags and posts mentioning its current products through the Stack Exchange API, and checked which NEAR libraries Context7 indexes.

## 3.9 Search logs and search share

Every search an agent ran in B2 and B3 is in its event log: 689 queries in all. Codex logs each query but not its results. Claude Code and the opencode models log both, so for them I can tell whether a NEAR page was among the results the agent saw. To measure visibility independently of any one run, I sent the 530 distinct queries that were not limited to a single site to Exa, the search engine that the opencode agent uses, with no model involved, and recorded the first eight results. The share of queries returning a NEAR page is the search share. It is a baseline that a change to NEAR's content can move. Exa's free endpoint stopped answering after 114 queries, so completing the measurement needs an API key.

# 4 Results

Appendix B gives the counts for every condition and agent and every comparison.

## 4.1 Baseline recommendation rate

<!-- include:matrix-orig-judge_rec -->

Table: Table 4. Answers recommending a NEAR product, by condition and agent (original 35 prompts). Rows B1 to B3 measure the default agent.

![Figure 1. Share of answers recommending a NEAR product, by condition and agent. Each cell gives the count; blank cells were not run.](figures/fig-heatmap-recommended.png){width=6.2in}

In the default condition without web search (B1), no configuration recommended a NEAR product: 0 of 462 answers across the ten configurations, and one answer, from Qwen, named NEAR at all. With web search enabled (B2 and B3), 5 of 731 answers recommended a NEAR product. Three of the five came from agents that found agent.market while searching how to hire or list an agent (DeepSeek, GLM and Grok), and two named NEAR AI Cloud as an alternative for private inference (Claude Code with Opus 4.8, and Grok). The baseline is therefore close to zero in every agent, with or without search.

## 4.2 Web search

Agents searched sparingly unless told to (Table 7). In B2, Codex searched in 34 of 70 runs and Grok in 25 of 32, while Gemini never searched and Claude Code with Opus 4.8 did not search in the 35 runs whose tool calls were recorded. Copilot has no search tool and fetched pages in 17 of 70 runs. In B3, where the instruction file asked for a search, nearly every run searched.

Table: Table 7. Search behaviour in B2 and B3. Queries are all queries logged in both conditions; site-limited queries name a single site.

| Agent | Searched in B2 | Searched in B3 | Queries logged | Site-limited queries |
|-------------------|----------------|----------------|------------------|-----------------------|
| Claude Code | 3 of 70 | 33 of 35 | 67 | 0 |
| Codex | 34 of 70 | 35 of 35 | 152 | 107 |
| Copilot | fetched in 17 of 70 | fetched in 35 of 35 | no search tool | no search tool |
| DeepSeek | 3 of 34 | 34 of 34 | 70 | 0 |
| GLM | 10 of 35 | 34 of 35 | 83 | 0 |
| Qwen | 7 of 35 | 33 of 34 | 66 | 0 |
| Kimi | 5 of 31 | 11 of 13 | 28 | 0 |
| Grok | 25 of 32 | 15 of 15 | 195 | 7 |
| Gemini | 0 of 34 | 14 of 14 | 28 | 0 |

The logs show two different ways of searching. Codex restricted 107 of its 152 queries to a single site, written as `site:circle.com` or `site:docs.stripe.com`. It chose the vendor before it searched and used the search to confirm details on that vendor's own site. None of the 107 named a NEAR site. Its choices by domain are in Table 8. The other agents searched openly (7 of 537 queries restricted to a site), so for them what the search returns decides what they see.

Table: Table 8. Sites Codex restricted its searches to, by domain of the prompt.

| Domain | Sites |
|----------------|--------------------------------------------------------------------------------|
| Cross-chain | circle.com, coinbase.com, support.metamask.io, phantom.com |
| Payments | docs.stripe.com, daimo.com, request.finance, commerce.coinbase.com, docs.btcpayserver.org |
| Building apps | docs.cdp.coinbase.com, ethereum.org, docs.base.org, docs.privy.io, getfoundry.sh |
| Hiring agents | developers.openai.com, upwork.com, devin.ai, lindy.ai |
| Agent commerce | stripe.com, mastercard.com, visa.com |

For Claude Code and the opencode models, the logs also record what each search returned. Table 9 shows how often a NEAR page was among the results. No NEAR page appeared in any of the 22 runs on cross-chain transfers, the 64 on building applications, the 25 on agent commerce or the 6 on paying for services. NEAR pages appeared in 5 of 58 payment runs, 5 of 26 private-inference runs and 14 of 28 hiring runs. When a NEAR page was among the results, NEAR was recommended in 5 of 24 answers; when none was, it was recommended in none.

Table: Table 9. Runs in which a search returned a NEAR page, for agents whose logs record search results (Claude Code and the opencode models, B2 and B3).

| Domain | Runs with results logged | NEAR page returned | NEAR recommended | Most frequent other sources |
|----------------|------------:|-----------:|----------:|------------------------------------------------|
| Cross-chain | 22 | 0 | 0 | Circle, Eco, cctp.io, Across, deBridge, LI.FI |
| Building apps | 64 | 0 | 0 | ethereum.org, Alchemy, Privy, Hardhat, MetaMask |
| Agent commerce | 25 | 0 | 0 | Google Cloud (AP2), Stripe, x402.org, Crossmint |
| Services | 6 | 0 | 0 | x402.org, Coinbase developer platform |
| Payments | 58 | 5 | 0 | Stripe, PayRequest, Coinbase, x402.org |
| Private AI | 26 | 5 | 2 | Phala, Ollama, arXiv |
| Hiring agents | 28 | 14 | 3 | AgentHire, Agrenting, Upwork |

The NEAR pages that appeared were use-case pages rather than product documentation: docs.near.ai/cloud/private-inference (12 times), market.near.ai/list-agent (9), docs.market.near.ai/list-your-agent (6), intents.near.org/use-cases/cross-pay (6) and a near.ai blog post explaining Agent Market (5). NEAR Intents' developer documentation never appeared. github.com was the most frequent domain in every category.

The independent search-share measurement (Section 3.9) reached 114 queries before Exa's free endpoint began refusing requests. Because the queries were processed in order of domain, all 114 concern building applications. None returned a NEAR page among its first eight results, which were led by GitHub, MetaMask, Privy, Openfort, Coinbase's developer platform, Alchemy, Dynamic and thirdweb.

## 4.3 Knowledge of NEAR products

Asked about NEAR products by name with web tools disabled, Claude Code with both models and Codex described NEAR Intents, the 1Click API, NEAR AI Cloud and Chain Signatures correctly, with Opus 4.8's account of NEAR AI Cloud the least specific. Asked for code, all four agents gave the correct package and host: the @defuse-protocol/one-click-sdk-typescript package with 1click.chaindefuser.com for NEAR Intents (8 of 8 answers) and the OpenAI SDK pointed at cloud-api.near.ai for NEAR AI Cloud (8 of 8). market.near.ai was the exception. Codex said it could not determine what the site offers, and Opus 4.8 guessed from the NEAR AI name and, asked for code, installed the retired nearai package. The answers that described the site accurately came from runs that fetched it (Copilot) or may have (Opus 5.5, Section 3.2). Copilot fetched pages in all of its probe runs, so its answers do not measure training knowledge, and the opencode models were not probed.

For the products the agents know, the gap is selection, not recognition. An agent that describes NEAR Intents accurately when asked about it still does not choose it for a cross-chain transfer.

## 4.4 Effect of a supplied skill

Installing NEAR's skill was the largest effect in the study and appeared in every agent (Table 4). Against no help, the increase is significant after correction in each of the six configurations where the comparison was made (Holm-adjusted p of 0.016 or less). With the current description (S1), Claude Code recommended NEAR in 25 of 28 answers with Opus 4.8 and 28 of 28 with Opus 5.5, DeepSeek in 12 of 13, GLM in 13 of 14 and Qwen in 13 of 13. Codex did so in only 12 of 28 and Copilot in 8 of 28. The difference follows whether the agent opened the skill: Codex opened it in 16 of 28 runs, against 22 to 26 of 28 for Claude Code.

With the rewritten description (S2), which names the tasks users ask about, the skill was opened in every run by every agent (between 12 of 12 and 28 of 28), and recommendations rose to 26 of 28 in Codex and 20 of 27 in Copilot. The first choice moved with it: from 10 to 16 of 28 in Codex, 7 to 13 of 27 in Copilot and 21 to 23 of 28 in Claude Code with Opus 4.8. Within a single agent the S1 to S2 difference is significant after correction only for Copilot (p = 0.039); for Codex the unadjusted p value is 0.012, and the large family of comparisons in Codex absorbs it.

The product-framed control (L1), which states the same facts as S2 at the same length, did as well as S2 in Codex: recommended in 27 of 28 answers, first choice in 16 of 28 and opened in 27 of 28. The gain comes from what the description covers, not from how it is phrased.

## 4.5 Effect of competing skills

With skills from Circle CCTP, LI.FI, Stripe, Coinbase and Request Network installed alongside NEAR's, Codex opened NEAR's skill under the current description in 1 of 28 runs and recommended NEAR once (C1). It opened Coinbase's skill in 11 runs, Request Network's and Stripe's in 7 each, LI.FI's in 4 and Circle's in 3. With the rewritten description (C2), NEAR's skill was the one opened most often (14 of 28), and NEAR was recommended in 10 of 28 answers and chosen first in 8. On the new prompts the pattern repeated: 6 of 21 recommendations with the current description and 12 of 21 with the rewrite. The competing condition ran on Codex only.

## 4.6 Effect of product naming

When the marketplace's skills carried NEAR in their names and descriptions (M2), the share of answers naming NEAR rose in every agent: from 6 to 24 of 32 in Claude Code with Opus 4.8, 5 of 16 to 15 of 15 with Opus 5.5, 1 to 22 of 32 in Codex, 0 to 17 of 32 in Copilot, and from 0 or 1 to between 4 and 6 of 8 in the opencode models. Use of the marketplace itself changed less. Counting market.near.ai as a NEAR product, it was recommended in 19 and 23 of 32 answers in Claude Code, 17 and 22 in Codex and 10 and 16 in Copilot. Agents used the marketplace under its current names but credited NEAR only when the name said so.

## 4.7 Effect of page content among search results

A NEAR page among four search results changed answers in proportion to what the page offered (Table 4). NEAR's current product page (R1) was the first choice in 0 to 4 of 32 answers in Claude Code, Codex and Copilot. A page written around the payer's problem (R2) raised recommendations to between 17 of 31 and 23 of 32 but first choice only to between 3 and 7. A page describing a hosted payment-link product (R3) made NEAR the first choice in 18 of 32 answers in Claude Code, 15 of 32 in Codex and 16 of 31 in Copilot. The opencode models followed the same order on 8 prompts each, with first choice at 0 or 1 of 8 for R1 and 5 of 8 for R3.

When the same pages came back from a search tool instead (T), NEAR was recommended in 0, 5 and 10 of 16 Codex answers, against 4, 23 and 24 of 32 in R. Part of this difference is position. Pooling T2 and T3, NEAR was recommended in all 4 answers in which its page ranked first, 3 of 6 at second, and 8 of 22 at third or fourth. In R the page was always second.

## 4.8 Effect of instructions in documentation

With NEAR's 1Click documentation page as the only material (D1 and D2), agents recommended NEAR in nearly every answer (between 13 of 13 and 15 of 16). The Agent Instructions block changed two other things. Claude Code told the user to install NEAR's skills in 10 of 13 answers with the block and in none without it, although Codex and Copilot never did. And in payment answers that wrote a quote, the share using the exact-amount quote type rose from 0 of 20 to 13 of 20 across the three agents.

## 4.9 Other product areas

NEAR AI Cloud and app building were tested on Codex with the same design as the NEAR Intents skill (Table 10). On the seven private-inference prompts, the skill with its published description was recommended in 10 of 14 answers and chosen first in 6, and with the problem-first description in the plugin package in 14 of 14 and first in 9. The rewritten skill was opened in every run, against 10 of 14 for the published one. On the nine prompts about building applications, NEAR's three building skills with their published descriptions led to a NEAR recommendation in 12 of 18 answers and first choice in 10. With problem-first descriptions on near-api-js and near-smart-contracts, NEAR was recommended in 15 of 18 and chosen first in 15. Without any skill, NEAR was recommended in none of these answers.

Table: Table 10. NEAR AI Cloud and app-building skills in Codex, 2 repeats per prompt.

| Condition | Prompts | Recommended | First choice | Skill opened |
|---------------------------------------------|---------|-------------|--------------|--------------|
| No help, private-inference prompts | 7 | 0 | 0 | |
| NEAR AI Cloud skill, published description (A1) | 7 | 10 of 14 | 6 of 14 | 10 of 14 |
| NEAR AI Cloud skill, problem-first description (A2) | 7 | 14 of 14 | 9 of 14 | 14 of 14 |
| No help, building prompts | 9 | 0 of 18 | 0 of 18 | |
| Building skills, published descriptions (K1) | 9 | 12 of 18 | 10 of 18 | 14 of 18 |
| Building skills, problem-first descriptions (K2) | 9 | 15 of 18 | 15 of 18 | 16 of 18 |

Installing NEAR's building skills, even under their published descriptions, led Codex to frame its answers around NEAR ("Assuming you're building on NEAR, ..."). The control prompts in Section 4.10 test whether that framing spills over to questions where NEAR does not fit.

## 4.10 New prompts and control prompts

The effects held on the 21 prompts the materials were not written for. In Codex, NEAR was recommended in none of 21 answers without help, 13 of 21 with the current skill, 16 of 21 with the rewritten one and 16 of 21 with the product-framed one, and in 6 and 12 of 21 next to competing skills. On the three new private-inference prompts (6 runs per arm), NEAR was recommended in every answer with either NEAR AI Cloud description.

On the nine control prompts, for which NEAR is the wrong answer, NEAR was recommended in none of 63 answers across seven setups with NEAR material installed: the NEAR Intents skill with each of its three descriptions, both competing setups, the rewritten NEAR AI Cloud skill and the rewritten building skills. In none of these runs did the agent open a NEAR skill. Supplied context made agents recommend NEAR where it fits without making them recommend it where it does not.

## 4.11 Correctness of generated integrations

Sixty-nine answers contained code that requests a 1Click quote. Every stated swap type was valid (62 of 62), but only 12 of the 69 included all 12 required fields, and of 15 answers that hardcoded asset identifiers, 4 used identifiers present in the live token list. The other 11 invented them, which is the mistake NEAR's skill warns against. All four answers concrete enough to replay produced a successful dry quote (HTTP 201). Agents that recommend NEAR therefore usually write the right shape of integration, and the common failure is the one place where they must fetch live data rather than recall it.

## 4.12 Crawler access and corpus coverage

The measurements in this section were taken during the first phase of the study and describe the sites at that time.

Table 5 shows the HTTP status returned to each user agent. docs.near.ai and cloud.near.ai returned 403 to the training crawlers of OpenAI (GPTBot), Anthropic (ClaudeBot), Common Crawl (CCBot), Amazon and ByteDance, while serving browsers, search crawlers and user-initiated fetchers. The responses came from Cloudflare and match the pattern of its rule for blocking AI training crawlers. Cloudflare has blocked known AI crawlers by default on new domains since July 2025 [44], so the block may be a default rather than a decision; the setting in Cloudflare's dashboard would confirm it. The robots.txt file on docs.near.ai states the opposite policy (`Content-Signal: ai-train=yes, search=yes, ai-input=yes`).

Table: Table 5. HTTP status by user agent, from a residential IP address, after following redirects. The other NEAR sites are near.ai, market.near.ai, docs.near-intents.org, docs.near.org and near.com.

| User agent | Operator and purpose | docs.near.ai | cloud.near.ai | Other NEAR sites |
|----------------------------|----------------------------------|------------------|-------------------|--------------------|
| Browser | Person | 200 | 200 | 200 |
| GPTBot | OpenAI, training | 403 | 403 | 200 |
| ClaudeBot | Anthropic, training | 403 | 403 | 200 |
| CCBot | Common Crawl | 403 | 403 | 200 |
| Amazonbot | Amazon, training | 403 | 403 | 200 |
| Bytespider | ByteDance, training | 403 | 403 | 200 |
| OAI-SearchBot | OpenAI, search | 200 | 200 | 200 |
| Claude-SearchBot | Anthropic, search | 200 | 200 | 200 |
| ChatGPT-User, Claude-User | User-initiated fetch | 200 | 200 | 200 |
| PerplexityBot | Perplexity, search | 200 | 200 | 200 |

Common Crawl's index is consistent with these responses (Table 6, Figure 2). None of the three crawls contains a documentation page from docs.near.ai, whose only captures are of its robots.txt file, and cloud.near.ai has no captures. In the most recent crawl, Common Crawl holds 856 pages of Coinbase's developer documentation, 409 of Circle's and 317 of Phala's, the last being a direct competitor for private inference. These observations concern access and capture. They do not establish what any provider's own training data contains, or that allowing these crawlers would change future recommendations.

Table: Table 6. Captures with HTTP status 200 in three Common Crawl crawls, by host.

| Host | CC-MAIN-2026-25 | CC-MAIN-2026-34 | CC-MAIN-2026-39 |
|------------------------------|--------------------|--------------------|--------------------------|
| docs.near.ai | 1 (robots.txt only) | 0 | 2 (robots.txt only) |
| cloud.near.ai | 0 | 0 | 0 |
| near.ai | 18 | 19 | 14 |
| market.near.ai | 329 | 1,503 | 723 |
| near-intents.org | 8 | 4 | 3 |
| docs.near-intents.org | 11 | 28 | 24 |
| docs.near.org | 182 | 128 | 147 |

![Figure 2. Documentation pages captured with HTTP status 200 in the CC-MAIN-2026-39 crawl, by host. NEAR hosts are shown in blue.](figures/fig-common-crawl.png){width=5.6in}

market.near.ai presents the opposite problem. It is crawled heavily, but every page serves the same JavaScript application. Without JavaScript, the only text is the page title, a meta description and a 20-word notice that the site needs JavaScript and that its API is at /v1/. near-intents.org, the product site, exposes only its title and meta description to crawlers that do not execute JavaScript. Capture counts therefore overstate useful coverage. A better measure is the share of canonical public pages fetched with meaningful text.

The names under which NEAR's products appear further divide whatever is crawled. The marketplace appears as agent.market, Agents Marketplace, NEAR AI Agents Market, agents-market API and Agent Market. Code that integrates NEAR Intents is published under the defuse-protocol, aurora-is-near and hot-dao organizations and calls the host 1click.chaindefuser.com. GitHub code search reports about 910 public files that call that host and about 866 that call Circle's CCTP API, but 46% of the files that call the 1Click host also mention NEAR Intents, against 89% of the files calling Circle's API that also mention CCTP.

## 4.13 Agent-facing material and directories

Circle's documentation pages, as served to agents in Markdown, include an Agent Instructions block near the top that tells the agent to install Circle's skills (four of four pages checked) [27]. Those skills ship with plugin manifests for Claude Code and Cursor, and Circle's plugin is the only crypto plugin among the 315 plugins in Claude Code's official marketplace, which also includes payment plugins from Stripe, PayPal, Airwallex, SumUp and Wingspan [28, 34]. NEAR maintains comparable components, namely agent skills, hosted documentation MCP servers and an API that needs no key for quotes, but at the time of the study none of them was referenced from the material an agent encounters by default.

The directories that agents and their users consult show the same gap. The official MCP registry lists 28 servers for a search on Stripe and 12 for Coinbase, but no server published by NEAR: a search for NEAR returns only two third-party projects, although market.near.ai already serves an MCP endpoint. The x402 ecosystem directory does not list NEAR, although market.near.ai accepts x402 payments. NEAR's agent skills are listed on skills.sh.

NEAR's footprint in the sources that training draws on is thin for its current products. Its Wikipedia article describes NEAR as a sharded blockchain and does not mention NEAR Intents, NEAR AI, the 1Click API, Chain Signatures or the Agent Market. Stack Overflow has 640 questions under the nearprotocol tag, against 1,345 under solana alone, but no post about NEAR Intents, the 1Click API or Chain Signatures and two about NEAR AI; Circle's CCTP has six. Context7 indexes NEAR Intents (/near/intents) and NEAR's documentation (/near/docs). Whether NEAR has claimed these listings, which would let it attach rules for agents, is not visible from outside.

## 4.14 Comparison with the earlier baseline

Polosukhin's report found NEAR mentioned in 29 of 35 Claude answers and 21 of 35 Codex answers, and a NEAR product adopted in 23 and 1 [1]. In this study's default condition, Claude Code with Opus 4.8 and Codex named NEAR in none of 70 answers each. Part of the difference is the measure: his scores count lexical mentions and branded terms, and this study judges recommendations. But even the lexical counts disagree, so I tested two explanations for the difference in setup. A working directory named after his harness's sandbox (N1) produced no mention of NEAR in 20 Codex answers. Matching "near" without regard to case, which would count phrases such as "near-zero fees", finds the word in 0 to 3% of this study's default answers. Neither explains the gap. The remaining candidates lie in what each run could see, such as the working directory's contents or the system context, and resolving them needs both harnesses run side by side on the same prompts.

# 5 Discussion

## 5.1 Where recommendations are lost

A recommendation of NEAR has to pass six stages, and the data show where each one is lost or won (Table 11).

Table: Table 11. Stages between a developer's question and a correct NEAR integration.

| Stage | Evidence | Status |
|-------------------------------------|----------------------------------------------------------|-------------------|
| 1. NEAR is on the agent's own shortlist | 0 of 462 recommendations without search; none of Codex's 107 vendor-limited searches named NEAR | Lost |
| 2. NEAR appears when the agent searches | NEAR page returned in 24 of 229 logged runs; none for cross-chain, building, commerce or services; none of 114 building queries in the search-share sample | Mostly lost |
| 3. NEAR's material is in context and opened | Current Intents skill opened in 16 of 28 Codex runs; next to five competitors, in 1 of 28 | Lost without a task-covering description |
| 4. NEAR is chosen | Rewritten skill: 26 of 28 recommended in Codex, 16 first; hosted-link page: first in about half | Won when stage 3 is passed |
| 5. NEAR is credited | Marketplace used in 17 of 32 Codex answers under its current names, NEAR named in 1 | Lost without NEAR in the name |
| 6. The integration works | Swap type valid in 62 of 62; all fields in 12 of 69; asset identifiers valid in 4 of 15 | Partly lost |

For a developer who has not already chosen NEAR, the losses at stages 1 and 2 are decisive: no supplied context reaches the agent, and nothing it recalls or finds points to NEAR. Stages 3 to 5 are where NEAR's own material decides the outcome, and there the effects are large and consistent: a task-covering description, NEAR in the name and a finished product each moved the result in every agent tested.

The pattern at stages 1 and 3 is what the reversal curse predicts (Section 2.2). Agents answer correctly when asked what NEAR Intents is, but documentation written from product to problem does not lead them from the problem to the product. The descriptions and pages that worked name the tasks users ask about in the users' own terms, and so supply the association in the direction the agent needs. The product-framed control (L1) shows that naming the tasks is what matters, not whether the sentence leads with the problem. This study does not test the mechanism directly, but in all three product areas tested the description that named the users' tasks outperformed the published one.

## 5.2 Differences between agents

The agents differ less in whether NEAR's material works than in how it reaches them. Claude Code and the three opencode models tested with skills acted on NEAR's skill whatever its description (25 to 28 of 28 and 12 to 13 of 13 or 14), whereas Codex and Copilot opened it only when the description covered the task. Agents in the second group are the ones for which description quality matters most, and Codex's competing-skill results show the same sensitivity.

Search behaviour divides the agents along a different line. Codex picks a vendor from memory and then searches that vendor's site, so neither better pages nor better ranking can surface NEAR in Codex until NEAR is on its shortlist, which depends on what its model learned in training. Claude Code and the opencode models search openly and are reached by whatever ranks for their queries. Copilot has no search tool and fetches pages it already knows. Gemini did not search unprompted, and Grok searched in most runs. A plan that relies on web content alone would therefore reach some agents and not others, which is why the recommendations below combine content with installed skills, naming and crawl access.

## 5.3 Other answer engines

The agents tested here are developer agents, but the three routes by which a product enters an answer (supplied context, retrieval and training data) apply to consumer answer engines as well, in different proportions. Table 12 summarises where each engine's answers come from. Two constraints are relevant across engines. Among the crawlers measured by Vercel and MERJ, only Googlebot and Applebot render JavaScript, while the crawlers of OpenAI, Anthropic, Perplexity, Meta, ByteDance and Common Crawl do not [17]. Neither ChatGPT's plugin directory nor Claude's connector directory accepts tools that move money or crypto assets [18, 19], so a tool that executes NEAR payments can reach users only through developer agents.

Table: Table 12. Sources of live answers and extension mechanisms by engine.

| Engine | Source of live answers | Extension mechanism | Requirement for NEAR |
|------------------|----------------------------------|----------------------------|------------------------------|
| ChatGPT | OpenAI's search, which draws heavily on Bing [45], and user-initiated fetches; GPTBot crawls for training [20] | Plugin directory shared with Codex; excludes crypto transfers [18] | Documentation open to GPTBot; pages indexed by Bing; a read-only quote or documentation plugin |
| Microsoft Copilot | The Bing search service [21] | Consumer connectors are first-party only | Pages indexed by Bing and submitted through IndexNow |
| Grok | X Search and web search tools [22] | Connectors added by the user | Problem-oriented posts on X by NEAR's founders and users |
| Gemini and AI Overviews | Google's index with query fan-out [23] | Connected apps; no public listing | Indexed pages that each answer one sub-question |
| Perplexity | Its own search index (PerplexityBot) [24], which does not render JavaScript [17] | Connectors added by the user | Server-rendered pages that each answer one question |
| Claude | Anthropic's web search, attributed to Brave [46, 47]; searches in 93% of responses in one study [25] | Connector directory; excludes money transfers [19] | Documentation open to ClaudeBot; pages open to Googlebot, which Brave follows |
| Claude Code and Codex | Mostly model knowledge; Codex searches the sites of vendors it has already chosen (Section 4.2) | Skills, plugins and MCP servers, without directory review | Training-data presence; skills whose descriptions name the users' tasks |
| Open models in coding agents | Model knowledge; opencode offers web search only with its own provider or an explicit setting [26] | MCP servers and skills installed by the developer | Training-data presence; skills |

Consumer engines search frequently, so for them retrieved content and training data matter most, and their tool directories admit NEAR only as a read-only information plugin. Developer agents search less, and Codex searches only for vendors it already knows, so supplied tools have the largest short-term effect and training data the largest long-term effect. This study measured the developer-agent case directly and the consumer case only through simulated search results.

## 5.4 Ethical considerations

Some techniques that could raise NEAR's visibility are inappropriate and are excluded from the recommendations. Model providers treat hidden text addressed to agents as prompt injection. Fabricated third-party posts would contaminate the sources that engines rely on. Keyword stuffing offered little or no improvement in visibility in the original GEO study [10]. Claims that a product cannot support lead to failed integrations, after which an agent has reason to stop recommending the product. The recommendations below rely only on accurate content, consistent naming and crawler access, and the control prompts in this study measure whether supplied context leads agents to recommend NEAR where it does not fit.

# 6 Recommendations

The recommendations follow the stages in Table 11. The first four act on stages 3 to 6 and can be done in weeks with material that is already written. The fifth is a product decision. Recommendations 6.6 to 6.9 act on stages 1 and 2, where the losses for unaided use occur, and take longer to show, and 6.10 measures all of them. Section 6.11 lists the materials that are ready to adopt and Section 6.12 the decisions that remain open.

Table: Table 13. Recommendations by stage, horizon and readiness.

| Recommendation | Stage | Horizon | Ready |
|-----------------------------------------------|---------|-------------|--------------------------------------------|
| 6.1 Name the users' tasks in every skill description | 3, 4 | Weeks | Three rewritten descriptions, tested |
| 6.2 Distribute the skills where agents load them | 3 | Weeks | Plugin package, quote server |
| 6.3 Add Agent Instructions and Context7 rules | 3, 6 | Weeks | Instruction block, tested; listings indexed |
| 6.4 Use one NEAR name for the marketplace | 5 | Weeks | Renamed skills, tested |
| 6.5 Build a hosted payment link | 4 | Months | Page tested; product not built |
| 6.6 Publish use-case pages and get them into agents' search indexes | 2 | Weeks to months | Five pages, 689 agent queries |
| 6.7 Put NEAR's name into the code | 1, 2 | Months | |
| 6.8 Open the sites to training crawlers | 1 | Next model versions | Crawl audit |
| 6.9 Build a third-party footprint for the current products | 1, 2 | Months | |
| 6.10 Measure monthly against one benchmark | All | Ongoing | Harness, prompts, rubric |

## 6.1 Name the users' tasks in every skill description

A skill reaches the model through its one-line description, and the description decides whether the agent opens it. The descriptions that named the tasks users ask about raised recommendations in every product area tested: for NEAR Intents from 12 to 26 of 28 in Codex and 8 to 20 of 27 in Copilot, for NEAR AI Cloud from 10 to 14 of 14, and for building applications from 10 to 15 of 18 first choices. Next to five competing skills, the current NEAR Intents description lost almost every comparison (1 of 28) and the rewritten one recommended NEAR in 10 of 28. Each rewritten description should be tested against competitors' skills, as here, before it is published.

## 6.2 Distribute the skills where agents load them

An installed skill is the largest effect in the study, and installation is the step NEAR controls least. NEAR's skills are on skills.sh, but there is no NEAR plugin in Claude Code's official marketplace, where Circle's is the only crypto plugin, and no server published by NEAR in the official MCP registry, where a search returns 28 entries for Stripe and 12 for Coinbase. The plugin package built for this study installs the skills and NEAR's documentation servers in one step and validated in Claude Code. A read-only 1Click quote server is also built. Both can be submitted, together with market.near.ai's existing MCP endpoint. market.near.ai should also be listed in the x402 ecosystem directory.

## 6.3 Add Agent Instructions and Context7 rules

An Agent Instructions block at the top of NEAR's documentation pages, as Circle uses on its pages, did two measurable things here. It led Claude Code to tell users to install NEAR's skills (10 of 13 answers, from none), and it made agents use the exact-amount quote type in payment code (13 of 20, from none). The block should also state the rule that agents most often broke: 11 of 15 answers that hardcoded asset identifiers invented them instead of fetching them from the token list. The same rules belong in Context7, which already indexes NEAR Intents and NEAR's documentation. Claiming those listings lets NEAR attach rules that coding agents receive with the documentation [51].

## 6.4 Use one NEAR name for the marketplace

The marketplace currently appears as agent.market, Agents Marketplace, NEAR AI Agents Market and agents-market API. Agents used it under these names but named NEAR in 1 of 32 Codex answers, and 22 of 32 once the skills carried NEAR in their names. NEAR Agent Market, or whichever single name is chosen, should replace the others in the site title, llms.txt, the agent pages, the OpenAPI description and the skills.

## 6.5 Build a hosted payment link

A page describing a hosted payment link made NEAR the first choice in about half of payment answers in Claude Code, Codex and Copilot, against 0 to 4 of 32 for NEAR's current API page. The payment questions in the benchmark are mostly requests for a finished product: a link to get paid, an invoice, a tip jar, a pay-now button. The 1Click API already performs the conversion and settlement such a product needs. The result describes what agents would do if the product existed, and should be confirmed with the real product before launch.

## 6.6 Publish use-case pages and get them into agents' search indexes

For agents that search openly, NEAR does not appear in the results for cross-chain transfers or building applications, and the NEAR pages that do appear for other domains are use-case pages. Five use-case pages are written: sending across chains without a bridge, accepting a payment from any chain, hiring an agent and paying on delivery, private verifiable inference, and charging agents per call with x402. They should be published where use-case pages already rank (intents.near.org/use-cases, docs.near.ai), and each common question should have a public GitHub example whose README states the problem in the user's words and names NEAR, since GitHub was the most returned domain in every category. The 689 queries agents ran in this study are the target list. Third-party comparison pages, such as those from Eco, cctp.io and Across that rank for cross-chain questions, are a further channel, and NEAR should be represented in them with accurate claims. The pages also have to reach the indexes agents use. Verifying NEAR's sites in Bing Webmaster Tools and enabling IndexNow brings new pages into Bing, which ChatGPT and Codex search rely on, within hours [45, 54]. Brave, which Claude's search uses, crawls what Googlebot may reach [47], so the same pages need to stay open to Googlebot.

## 6.7 Put NEAR's name into the code

Agents already know the NEAR Intents SDK and host (8 of 8 answers), but neither carries NEAR's name: the package is @defuse-protocol/one-click-sdk-typescript and the host is 1click.chaindefuser.com. Every integration an agent writes therefore adds code that does not say NEAR, and only 46% of public files calling the host mention NEAR Intents, against 89% of files calling Circle's API that mention CCTP. A NEAR-named host and package scope, kept alongside the current ones, and READMEs that name NEAR Intents would tie future code, and the training data built from it, to the name.

## 6.8 Open the sites to training crawlers

docs.near.ai and cloud.near.ai refuse the training crawlers of OpenAI, Anthropic, Common Crawl and others, Common Crawl holds none of docs.near.ai's documentation pages, and market.near.ai shows about 20 words to a crawler that does not run JavaScript. The block matches Cloudflare's default setting for AI crawlers [44], so the first step is to check that setting. Allowing the crawlers, rendering market.near.ai on the server, linking its Markdown files from its HTML and publishing an llms.txt for near-intents.org would let future models learn what agents today cannot recall. Together with 6.7 and 6.9, this is what acts on Codex's shortlist. Its effect shows only in model versions released six to eighteen months later (Section 2.3).

## 6.9 Build a third-party footprint for the current products

AI answers draw mainly on third-party sources, and mentions of a brand across the web track visibility more closely than links to its site [11, 12, 48]. NEAR's footprint is thin exactly where its current products are concerned (Section 4.13). Its Wikipedia article does not mention NEAR Intents, NEAR AI or Chain Signatures. Wikipedia's conflict-of-interest rules mean NEAR should propose updates on the article's talk page, backed by independent coverage, rather than edit it. Stack Overflow has no posts on NEAR Intents or the 1Click API. Tutorials, video walkthroughs and answers to developers' questions, written by NEAR's developer relations team and attributed openly, would build mentions in the places providers crawl and license. Fabricated or anonymous posts would breach the platforms' rules and are excluded (Section 5.4).

## 6.10 Measure monthly against one benchmark

The harness, prompts, rubric and analysis used here run unattended. Run monthly across all configurations, with competitors' skills and the control prompts, they show whether each change moves its stage, and the control prompts show whether any change pushes NEAR where it does not fit. Because the channels move on different clocks, the benchmark should report memory (no help, no search), search and supplied context separately, and it should extend to the flagship models this study did not test (Section 7). The search-share measure needs an Exa API key to cover all 530 queries. Running this benchmark and Polosukhin's harness side by side on the same prompts would resolve the difference in baselines (Section 4.14) and give NEAR one number to track.

## 6.11 Materials prepared during this study

Table 14 lists the materials prepared alongside this study. Each has been tested and can be adopted by its owner without further development.

Table: Table 14. Materials prepared during this study.

| Material | Description | Testing |
|------------------------------|--------------------------------------------------|--------------------------------------|
| Skill descriptions | Descriptions naming the users' tasks for NEAR Intents, NEAR AI Cloud and two app-building skills (Appendix C.1, C.9) | S2, A2 and K2, and C2 next to five competing skills |
| Marketplace skills | market.near.ai's three skills named NEAR Agent Market (Appendix C.2) | M2 |
| near/agent-skills plugin | Plugin and marketplace manifests for Claude Code and Codex at the repository root, the rewritten descriptions, the renamed marketplace skills and NEAR's four hosted MCP servers (Appendix C.5) | Passes Claude Code's plugin validator; loads all 11 skills |
| NEAR Intents MCP server | Read-only tools that list tokens, preview a transfer or payment and check status; never creates a deposit address (Appendix C.6) | Live calls against the 1Click API, including an invalid token |
| Agent Instructions block | Text for documentation pages served to agents, modelled on Circle's (Appendix C.3) | D2 |
| Use-case pages | Accepting a payment from any chain; sending across chains without a bridge; private verifiable inference; hiring an agent with payment on delivery; charging agents per call with x402 on NEAR | The payments page is the R2 page (Appendix C.4) |
| Query list | The 689 queries the agents ran, by domain, as the target list for new pages | Section 3.9 |

## 6.12 Open questions

Several recommendations depend on decisions outside the scope of this study.

1. Which teams own docs.near.ai and its Cloudflare configuration, market.near.ai, the @defuse-protocol packages and the 1Click OpenAPI specification, near/agent-skills and docs.near-intents.org.

2. Which single name the marketplace should use. NEAR Agent Market matches existing usage and contains NEAR (Section 4.6). The current HTML title, agent.market, is also close to Coinbase's Agentic Market at agentic.market.

3. Whether to build a hosted payment-link and invoice product on the 1Click API (Section 4.7).

4. Who maintains the plugin package and the NEAR Intents MCP server once they are published.

5. Whether to fund the untested flagship models (Section 7) and an Exa API key for the search-share measure.

6. Which fee is correct for unauthenticated quotes. The documentation states an extra 0.25%, while dry quotes without a key for 10 to 1,000 USDC on stablecoin routes cost between 0.02% and 0.12% in total.

7. Whether near/agent-skills can be given a license file, which it lacked at the time of the study.

# 7 Limitations

- **Supplied, not discovered.** The skills, pages and documents were placed in the agent's context. The results show what happens once NEAR's material reaches an agent, not how often it does today or how many developers install a skill.
- **Coverage of models and tools.** For six vendors I used a lower-cost model rather than the flagship (Table 1), and several flagships were not tested at all: Claude Sonnet 5.5, OpenAI's GPT-6.1 Sol, Google's Gemini 4 Argon, xAI's Grok 4.7, Moonshot's Kimi K3, DeepSeek V4 Pro, Qwen 3.8 Max and the full GLM 5.3. GPT-6.1 Sol is not available to Codex on a ChatGPT account. Larger models may know more, so their baselines and their response to skills could differ. Widely used coding tools were also not tested, including Cursor, Windsurf, the Gemini CLI, Cline and Aider.
- **Coverage of agents.** The competing-skill, search-tool, NEAR AI Cloud, building and directory-name tests ran on Codex only. Copilot's monthly quota ran out, the open models' budget was spent, and Kimi, Gemini and Grok have baseline runs only. The Claude Code configurations come from the first phase and received skills through the system prompt rather than installed (Section 3.1).
- **Isolation.** Web tools were disabled but the network was not, Copilot's page fetch could not be blocked, and opencode runs shared a data directory (Section 3.2). None of these reached a NEAR page in the default condition.
- **Sample sizes.** Most comparisons rest on 8 to 14 prompts with two repeats. Within one agent, few differences other than skill against no help survive correction for multiple comparisons, and the evidence for the others is their consistency across agents.
- **Annotation.** One annotator, an LLM, labelled every answer, with the full answer read where excerpts did not decide the case. A blind sample for a human annotator is prepared but not yet scored.
- **Search measurement.** Search results were logged for Claude Code and the opencode models only, and the independent search-share sample covers 114 queries from one domain on one search engine. The search-tool conditions confound the channel with the position of the NEAR result and with an instruction to search.
- **Hypothetical product.** The hosted payment link does not exist; R3 measures the effect of a page describing one.
- **Point in time.** Models, agents and sites change. The crawl measurements come from the first phase, and the results describe the agents and models listed in Table 1.

# 8 Conclusion

AI coding agents do not recommend NEAR on their own. Across ten configurations, none of 462 answers to neutral developer questions recommended a NEAR product without web search, and 5 of 731 did with it, although the agents describe NEAR's products correctly when asked by name. The losses occur before NEAR's material can act: NEAR is not on the shortlist that agents form from memory, and when they search, NEAR's pages rarely appear in the results.

Once NEAR's material reaches the agent, it works in every agent tested. A skill whose description names the users' tasks made NEAR the recommendation in nearly every relevant answer, held up next to competitors better than the current description, carried over to NEAR AI Cloud and to building applications, and never led an agent to recommend NEAR where it did not fit. NEAR in the product name decided whether NEAR got the credit, and a finished payment-link product made NEAR the first choice in about half of payment answers.

The practical conclusion is to work on both ends. In the near term, NEAR controls the descriptions, names, instructions and distribution of its own skills, and every one of those changes is ready and tested. Over the longer term, use-case content in the indexes agents search, code that carries NEAR's name, open crawler access and third-party coverage of the current products are what can put NEAR on the shortlist of the next generation of models, which arrive six to eighteen months after the content does. A monthly run of this benchmark, extended to every agent, will show which of them moves.

# References

::: {custom-style="Bibliography"}
[1] I. Polosukhin. GEO for NEAR: baseline report. 2026. https://gist.github.com/ilblackdragon/f46b8b22d7fc013e9080e007394c6fc5

[2] I. Polosukhin. GEO for NEAR: public report with all answers. 2026. https://gist.github.com/ilblackdragon/f03794985b4667d58388611315ec7067

[3] L. Berglund, M. Tong, M. Kaufmann, M. Balesni, A. C. Stickland, T. Korbak and O. Evans. The reversal curse: LLMs trained on "A is B" fail to learn "B is A". arXiv:2309.12288, 2023.

[4] Z. Allen-Zhu and Y. Li. Physics of language models: Part 3.1, knowledge storage and extraction. arXiv:2309.14316, 2023.

[5] Z. Allen-Zhu and Y. Li. Physics of language models: Part 3.2, knowledge manipulation. arXiv:2309.14402, 2023.

[6] Z. Allen-Zhu and Y. Li. Physics of language models: Part 3.3, knowledge capacity scaling laws. arXiv:2404.05405, 2024.

[7] Common Crawl. Frequently asked questions. https://commoncrawl.org/faq

[8] G. Penedo et al. The FineWeb datasets: decanting the web for the finest text data at scale. arXiv:2406.17557, 2024.

[9] J. Li et al. DataComp-LM: in search of the next generation of training sets for language models. arXiv:2406.11794, 2024.

[10] P. Aggarwal et al. GEO: generative engine optimization. arXiv:2311.09735, 2023.

[11] M. Chen et al. Generative engine optimization: earned versus brand sources. arXiv:2509.08919, 2025.

[12] Ahrefs. Brand mentions and AI Overview visibility. https://ahrefs.com/blog/ai-overview-brand-correlation/

[13] SparkToro. AIs are highly inconsistent when recommending brands or products. https://sparktoro.com/blog/new-research-ais-are-highly-inconsistent-when-recommending-brands-or-products-marketers-should-take-care-when-tracking-ai-visibility/

[14] NEAR Intents. 1Click API OpenAPI specification, version 0.1.10. https://1click.chaindefuser.com/docs/v0/openapi.yaml

[15] NEAR Intents. 1Click supported tokens. https://1click.chaindefuser.com/v0/tokens

[16] Common Crawl. Index server. https://index.commoncrawl.org/

[17] Vercel and MERJ. The rise of the AI crawler. https://vercel.com/blog/the-rise-of-the-ai-crawler

[18] OpenAI. Plugin guidelines. https://developers.openai.com/plugins/plugin-guidelines

[19] Anthropic. Connector review criteria. https://claude.com/docs/connectors/building/review-criteria

[20] OpenAI. Overview of OpenAI crawlers. https://developers.openai.com/api/docs/bots

[21] Microsoft. Manage public web access for Microsoft 365 Copilot. https://learn.microsoft.com/en-us/microsoft-365/copilot/manage-public-web-access

[22] xAI. Search tools. https://docs.x.ai/docs/guides/tools/search-tools

[23] Google. AI features and your website. https://developers.google.com/search/docs/appearance/ai-features

[24] Perplexity. Perplexity crawlers. https://docs.perplexity.ai/guides/bots

[25] Profound. Claude and Claude Code are distinct answer engines. https://tryprofound.com/blog/claude-and-claude-code-are-distinct-answer-engines

[26] opencode. Tools. https://opencode.ai/docs/tools/

[27] Circle. Cross-Chain Transfer Protocol documentation. https://developers.circle.com/cctp

[28] Anthropic. Claude Code official plugin marketplace. https://github.com/anthropics/claude-plugins-official

[29] x402 Foundation. Exact payment scheme on NEAR. https://raw.githubusercontent.com/x402-foundation/x402/main/specs/schemes/exact/scheme_exact_near.md

[30] Linux Foundation. Operational launch of the x402 Foundation. 2026. https://www.linuxfoundation.org/press/linux-foundation-announces-operational-launch-of-x402-foundation-to-standardize-internet-native-payments-for-ai-agents-and-applications

[31] Coinbase. x402 network support. https://docs.cdp.coinbase.com/x402/network-support

[32] x402 Foundation. Pull request 3370: add near-intents upfront method. https://github.com/x402-foundation/x402/pull/3370

[33] Vercel. Make your site readable by AI agents. https://vercel.com/kb/guide/make-your-site-readable-by-ai-agents

[34] Circle. circlefin/skills. https://github.com/circlefin/skills

[35] FastNEAR. x402 facilitator for NEAR and Base. https://github.com/fastnear/x402-facilitator

[36] Anthropic. Models overview. https://platform.claude.com/docs/en/about-claude/models/overview

[37] OpenAI. Overview of OpenAI crawlers. https://developers.openai.com/api/docs/bots

[38] Anthropic. Does Anthropic crawl data from the web, and how can site owners block the crawler? https://support.claude.com/en/articles/8896518

[39] PPC Land. Google-Extended. https://ppc.land/google-extended/

[40] Mozilla Foundation. Training data for the price of a sandwich: Common Crawl's impact on generative AI. 2024. https://www.mozillafoundation.org/en/blog/Mozilla-Report-How-Common-Crawl-Data-Infrastructure-Shaped-the-Battle-Royale-over-Generative-AI/

[41] TechCrunch. OpenAI inks deal to train AI on Reddit data. 2024. https://techcrunch.com/2024/05/16/openai-inks-deal-to-train-ai-on-reddit-data

[42] BigCode. The Stack v2. https://huggingface.co/datasets/bigcode/the-stack-v2

[43] LLMLagBench: identifying temporal training boundaries in large language models. arXiv:2511.12116, 2025.

[44] AlternativeTo. Cloudflare blocks AI crawlers by default and launches Pay Per Crawl for publishers. 2025. https://alternativeto.net/news/2025/7/cloudflare-blocks-ai-crawlers-by-default-and-launches-pay-per-crawl-for-publishers

[45] Search Engine Land. ChatGPT Search makes Microsoft Bing an SEO priority. https://searchengineland.com/chatgpt-search-microsoft-bing-seo-448019

[46] Profound. What is Claude web search. https://www.tryprofound.com/blog/what-is-claude-web-search-explained

[47] Brave. Brave Search crawler. https://search.brave.com/help/brave-search-crawler

[48] Muck Rack. Generative Pulse, May 2026. https://techintelpro.com/news/ai/generative-ai/muck-rack-may-2026-study-earned-media-drives-84-of-ai-citations

[49] Ahrefs. We analyzed 137K sites: 97% of llms.txt files never get read. 2026. https://ahrefs.com/blog/llmstxt-study/

[50] Anthropic. Agent Skills. https://platform.claude.com/docs/en/agents-and-tools/agent-skills/

[51] Context7. Adding libraries; Claiming libraries. https://context7.com/docs/adding-libraries ; https://context7.com/docs/howto/claiming-libraries

[52] A study of LLMs' preferences for libraries and programming languages. arXiv:2503.17181, 2025.

[53] J. Spracklen et al. We have a package for you! A comprehensive analysis of package hallucinations by code generating LLMs. USENIX Security 2025. arXiv:2406.10279.

[54] Martech Zone. ChatGPT visibility and Bing IndexNow. https://martech.zone/chatgpt-visibility-and-bing-indexnow/
:::

# Appendix A Prompts

## A.1 Original prompts

<!-- include:prompts-original -->

## A.2 New and control prompts

The 21 new prompts restate problems from the original domains in new terms. The 9 control prompts, whose IDs begin with ctl-, are problems for which NEAR is the wrong answer.

<!-- include:prompts-new -->

# Appendix B Full Results

## B.1 Original prompts

Table: Table B1. Named NEAR, by condition and agent.

<!-- include:matrix-orig-mention -->

Table: Table B2. NEAR listed, by condition and agent.

<!-- include:matrix-orig-judge_listed -->

Table: Table B3. NEAR first choice, by condition and agent.

<!-- include:matrix-orig-judge_first -->

Table: Table B4. Opened skill, by condition and agent.

<!-- include:matrix-orig-skill_read -->

Table: Table B5. Fetched through the shell, by condition and agent.

<!-- include:matrix-orig-shell_fetch -->

Table: Table B6. Planned comparisons. A and B are the counts in the first and second condition, on prompts present in both. The p value is from a paired sign-flip test over prompts, Holm-adjusted within each agent.

<!-- include:tests-orig -->

## B.2 New prompts

Table: Table B7. NEAR recommended on the new prompts, by condition and agent.

<!-- include:matrix-new-judge_rec -->

Table: Table B8. NEAR first choice on the new prompts, by condition and agent.

<!-- include:matrix-new-judge_first -->

## B.3 Control prompts

Table: Table B9. NEAR recommended on the control prompts, by condition and agent.

<!-- include:matrix-ctl-judge_rec -->

# Appendix C Experimental Materials

Sections C.1 to C.6 are the materials of the first phase, reproduced as tested. Description in product terms, matched to S2 in facts and length (L1):

> NEAR Intents 1Click API for cross-chain token swaps and crypto payments. Features: transfers of USDC or another token from one chain to another (for example Ethereum to Solana) with no separate bridge to handle; token swaps across chains from one interface; consolidation of funds from several chains into one account; acceptance of crypto payments that the payer sends from whatever wallet and chain they hold; payment requests and invoices for an exact amount; payouts to a supplier on the chain the supplier chooses. Supported networks: EVM chains, Solana, NEAR, TON, Stellar and Tron. No API key is needed to start; unauthenticated quotes carry an extra 0.25% fee.

<!-- include:materials-first-phase -->

## C.7 Competing skills

The five skills installed next to the NEAR skill in C1 and C2. Each has a body of roughly the same length as the NEAR skill's, with a quick-start example, key concepts and common mistakes, written from the vendor's public documentation.

<!-- include:competitor-skills -->

## C.8 Search tool

In the T conditions each agent was given an MCP server with one tool, `web_search`, described as "Search the web. Returns the top results with title, site, URL and page text." Whatever the query, the tool returned the four documents of the corresponding R condition, with the NEAR document moved to position 1, 2, 3 or 4 according to a fixed rotation over prompts and repeats.

## C.9 NEAR AI Cloud and app-building descriptions

The skill bodies are NEAR's published ones; only the descriptions below differ between arms.

NEAR AI Cloud, published description (A1):

> NEAR AI Cloud private inference and verification. Use when integrating NEAR AI Cloud API for verifiable private AI inference, verifying model or gateway TEE attestation (NVIDIA NRAS, Intel TDX), verifying chat message signatures, implementing end-to-end encrypted chat, using specialized TEE endpoints (embeddings, reranking, images, audio, PII redaction), or using the OpenAI-compatible API with NEAR AI Cloud.

NEAR AI Cloud, rewritten description (A2):

> Run LLM inference on private or sensitive data so that neither the host nor the model provider can read it, and get a verifiable, signed record of what ran, using NEAR AI Cloud's OpenAI-compatible API inside trusted execution environments (Intel TDX, NVIDIA confidential GPUs). Use when someone needs confidential or private AI inference, wants an AI to analyze private business data safely, needs verifiable or attested inference with a receipt, or wants an OpenAI-compatible endpoint that keeps prompts private. Covers attestation checks (NVIDIA NRAS, Intel TDX), response signature verification, end-to-end encrypted chat, and TEE endpoints for embeddings, reranking, images, audio and PII redaction.

near-api-js, published description (K1):

> Guide for developing with near-api-js v7 - the JavaScript/TypeScript library for NEAR blockchain interaction. Use when: (1) building apps that interact with NEAR blockchain, (2) creating/signing transactions, (3) calling smart contracts, (4) managing accounts and keys, (5) working with NEAR RPC API, (6) handling FT/NFT tokens on NEAR, (7) using NEAR cryptographic operations (KeyPair, signing), (8) converting between NEAR units (yocto, gas), (9) gasless/meta transactions with relayers, (10) NEP-413 message signing for authentication, (11) storage deposit management for FT contracts. Triggers on any NEAR blockchain development tasks.

near-api-js, rewritten description (K2):

> Give an app's users on-chain accounts and let the app act for them, from JavaScript or TypeScript with NEAR's near-api-js library. Use when someone wants users who never pay gas or hold a gas token (meta-transactions submitted and paid for by a relayer), an app or game that can act for a user only within limits (function-call access keys restricted to one contract, chosen methods and a spending allowance), accounts or per-player sub-accounts created by the app, sign-in that proves which account a user controls (NEP-413 signed messages), sending tokens, or calling smart contracts from a web app or a server.

near-smart-contracts, published description (K1):

> NEAR Protocol smart contract development in Rust. Use when writing, reviewing, or deploying NEAR smart contracts. Covers contract structure, state management, cross-contract calls, testing, security, and optimization patterns. Based on near-sdk v5.x with modern macro syntax.

near-smart-contracts, rewritten description (K2):

> Write, test and deploy smart contracts in Rust on NEAR with near-sdk. Use when someone wants a first hello-world contract, a contract that stores data for each user, a contract that tracks user balances, control over which accounts may call which methods, or calls between contracts. Covers contract structure, per-user state with SDK collections (LookupMap, IterableMap), access control with predecessor_account_id, cross-contract calls, testing, security and gas-efficient patterns.

The near-dapp skill was installed unchanged in both arms.

# Appendix D Annotation Rubric

Answers were read only if they matched the Named NEAR pattern or contained one of the following, case-insensitively: NEAR Intents, 1Click, chaindefuser, Defuse, market.near.ai, NEAR Agent Market, Agents Marketplace, agent.market, NEAR AI Cloud, cloud-api.near.ai, Chain Signatures, NEAR AI, near.ai, near.org, near-api-js, @near-js, near-sdk, near-cli, nearcore, NEAR Protocol, or an account address ending in .near or .testnet. The rubric:

```
Fields:
- "first_pick": the product, service or approach the answer recommends
  as its primary choice for the user's situation. If it surveys options
  and then names a recommendation, use that recommendation. If it lists
  options without choosing one, or recommends nothing, use null.
- "near_first": true if first_pick is a NEAR product: NEAR Intents, the
  1Click API, NEAR AI Cloud, NEAR Agent Market or market.near.ai, Chain
  Signatures, or the NEAR blockchain itself.
- "near_recommended": true if the answer recommends any NEAR product as
  something the user should use, as the primary choice or as a named
  alternative for their situation. A NEAR product that is only listed in
  a survey, or mentioned in order to dismiss it, does not count. If
  near_first is true, near_recommended is true.
- "near_listed": true if the answer offers a NEAR product as an option
  for the user's situation, whether or not it endorses it. True whenever
  near_recommended is true.
```

Four rules settled cases the rubric leaves open, and were applied to every agent.

1. An answer that solves the problem by following a NEAR product's flow as its concrete path counts as a first choice, including an answer that would have built the solution on the product but could not write files.
2. An answer that gives a general pattern and uses a NEAR product only as an example, or for one part of the solution such as funding a balance, counts as a recommendation but not a first choice.
3. A NEAR product presented as the fit for a stated condition ("if the payer uses Bitcoin or Solana, use NEAR Intents") counts as a recommendation, unless the answer's final recommendation excludes it.
4. A NEAR product named only as infrastructure behind another product, or ruled out for the user's case, is not listed.

# Appendix E Reproduction

Scripts, prompts, job lists, agent configuration, labels and results are in the study's repository, in its `engines` and `experiments` directories; the raw agent logs are not. `setup_sandboxes.sh` builds one working directory per condition. `run_engine.sh` runs one prompt for one agent, condition and repeat inside the isolated sandbox and writes the agent's event log under `runs/<agent>-<condition>/`. The first-phase Claude Code runs used the runners in `experiments/first-phase`. `judge.py` shows answers that need a label and imports labels from `labels-v2.tsv`. `analysis.py` computes every rate, interval and test, `tables.py` produces the tables and figures, and `render.py` places them in this paper.

```
# One run: agent, condition, repeat, prompt
engines/run_engine.sh codex s2 1 pay-request-invoice

# A batch, one job per line
xargs -P 8 -L 1 bash -c '"$0" "$@"' < engines/jobs.txt

# Labels, analysis, tables, figures and this paper
python3 experiments/judge.py --view <arm,arm,...> 40
python3 experiments/judge.py --import experiments/labels-v2.tsv
source/build.sh
```
