---
title: "NEAR in AI Coding Agents: Findings, Solutions and Outcomes"
---

I asked ten AI coding agent and model configurations the 35 developer questions from Illia Polosukhin's report and 30 new ones: Claude Code with Opus 4.8 and Opus 5.5, ChatGPT Codex, GitHub Copilot, and DeepSeek, GLM, Qwen, Kimi, Gemini and Grok in the opencode agent. I then added one piece of NEAR material at a time and measured how often the agent recommended NEAR, and I read the logs of every web search the agents ran.

# Findings

1. **Agents do not recommend NEAR on their own.** None of 462 answers recommended a NEAR product without web search, and 5 of 731 did with it.

2. **They know the products but do not pick them.** Asked by name, Claude and Codex describe NEAR Intents, the 1Click API, NEAR AI Cloud and Chain Signatures correctly, and all agents asked give the right SDK and endpoint for NEAR Intents and NEAR AI Cloud (8 of 8 answers each). market.near.ai is the exception.

3. **NEAR is missing where agents look.** Codex chooses a vendor from memory and then searches that vendor's site: 107 of its 152 searches were limited to one site, and none was a NEAR site. Agents that search openly found no NEAR page for any cross-chain question (22 runs) or app-building question (64 runs), and none of 114 app-building queries returned a NEAR page in an independent search. When a NEAR page did come back, NEAR was recommended in 5 of 24 answers; otherwise never. The NEAR pages that ranked were use-case pages, never the NEAR Intents developer docs.

4. **Once NEAR's material reaches the agent, it works, in every agent and every product tested.** A skill whose description names the tasks users ask about did best each time:

| Product, agent | No help | Published description | Description naming users' tasks |
|----------------------------------------|---------|------------------------|---------------------------------|
| NEAR Intents, Codex | 0 of 28 | 12 of 28 | 26 of 28 |
| NEAR Intents, Copilot | 0 of 28 | 8 of 28 | 20 of 27 |
| NEAR Intents, Claude Code (Opus 4.8) | 0 of 28 | 25 of 28 | 27 of 28 |
| NEAR AI Cloud, Codex | 0 of 11 | 10 of 14 | 14 of 14 |
| Building apps (NEAR first choice), Codex | 0 of 18 | 10 of 18 | 15 of 18 |

5. **Against competitors, the description decides.** Installed next to skills from Circle, LI.FI, Stripe, Coinbase and Request Network, the current NEAR Intents description was opened once in 28 runs. The rewritten one was the most opened skill and NEAR was recommended in 10 of 28 answers.

6. **Agents credit the name they are given.** With NEAR in the marketplace skills' names, answers naming NEAR rose from 1 to 22 of 32 in Codex, 6 to 24 in Claude Code and 0 to 17 in Copilot.

7. **A finished product wins first place.** A page describing a hosted payment link made NEAR the first choice in about half of payment answers in each agent. NEAR's current API page did so in 0 to 4 of 32. NEAR does not offer a hosted payment link today.

8. **No over-reach.** On questions where NEAR is the wrong answer, such as card subscriptions or Apple Pay, NEAR was recommended in none of 63 answers across seven setups with NEAR material installed, and the agents did not even open NEAR's skills.

9. **Integrations are close but not right.** Of 15 answers that hardcoded token identifiers in NEAR Intents code, 11 invented them. An Agent Instructions block on the documentation page led agents to use the exact-amount quote in 13 of 20 payment answers, against none without it.

10. **NEAR is thin where models learn and absent where agents look.** docs.near.ai and cloud.near.ai refuse the training crawlers of OpenAI, Anthropic and Common Crawl, a pattern that matches Cloudflare's default AI-crawler block. NEAR's Wikipedia article does not mention NEAR Intents, NEAR AI or Chain Signatures, and Stack Overflow has no posts on NEAR Intents or the 1Click API. The official MCP registry has 28 entries for Stripe, 12 for Coinbase and none from NEAR, and NEAR is not in the x402 directory. Training data reaches new models 6 to 18 months later; at answer time, ChatGPT and Codex search mostly through Bing and Claude through Brave.

The installed-skill effect is statistically firm in each of the six configurations where it was tested. The other effects point the same way wherever they were tested but rest on small samples, and the competitor and product-area tests ran on Codex only. Most vendors' flagship models, including Claude Sonnet 5.5, GPT-6.1 Sol, Gemini 4 Argon and Grok 4.7, and tools such as Cursor were not tested. Illia's baseline counted mentions and this one counts recommendations; two setup explanations for the remaining difference were tested and ruled out, and running both harnesses on the same questions would settle it.

# Proposed solutions

Solutions 1 to 4 can be done in weeks with material that is ready and tested. Solution 5 is a product decision. Solutions 6 to 9 reach developers who have not chosen NEAR and take months. Solution 10 measures all of them.

1. **Rewrite every NEAR skill description around the users' tasks**, and test each against competitors' skills before publishing. Rewrites for NEAR Intents, NEAR AI Cloud and the two app-building skills are done and tested. Owner: developer relations with each product team.

2. **Put NEAR's skills where agents load them.** Submit the plugin package (built, validated in Claude Code) to the Claude Code and Codex plugin marketplaces, register market.near.ai's MCP endpoint and the built NEAR Intents quote server in the official MCP registry, list market.near.ai in the x402 ecosystem directory, and update the skills.sh listing. Owner: developer relations.

3. **Add an Agent Instructions block to NEAR's documentation pages** that points agents to the skills and states the rules they break: fetch token identifiers from the token list and use the exact-amount quote for fixed prices. Claim NEAR's listings on Context7, which coding agents already use for NEAR Intents and NEAR's docs, and add the same rules there. Owner: docs team.

4. **Use one name, NEAR Agent Market**, in place of agent.market, Agents Marketplace, NEAR AI Agents Market and agents-market API, across the site, llms.txt, the API description and the skills. Owner: marketplace team.

5. **Build a hosted payment link on the 1Click API**: a link to get paid, an invoice, a tip jar or a pay-now button, payable from any chain. It is the only change that made agents choose NEAR first. Owner: Intents team.

6. **Publish use-case pages and GitHub examples for the questions agents actually search.** The 689 queries from this study are the target list, and five use-case pages are written. Publish them where NEAR's use-case pages already rank (intents.near.org/use-cases, docs.near.ai), with a GitHub example for each common question that names NEAR in its README. Register the sites in Bing Webmaster Tools with IndexNow for ChatGPT and Codex search, and keep them open to Googlebot, which Brave follows for Claude. Owner: developer relations.

7. **Put NEAR's name into the code.** The SDK (@defuse-protocol) and API host (1click.chaindefuser.com) do not say NEAR, so code agents write does not either: 46% of public files calling the host mention NEAR Intents, against 89% for Circle's API and CCTP. Add a NEAR-named host and package alongside the current ones. Owner: Intents engineering.

8. **Open the sites to AI training crawlers**, starting with Cloudflare's AI-crawler setting, render market.near.ai on the server and publish an llms.txt for near-intents.org. This is what reaches the memory of future models, including Codex's shortlist, 6 to 18 months out. Owner: infrastructure.

9. **Build a third-party footprint for the current products.** AI answers draw mostly on third-party sources. Propose updates to NEAR's Wikipedia article on its talk page, backed by independent coverage, since NEAR cannot edit it directly, and publish openly attributed tutorials, video walkthroughs and answers to developers' questions about NEAR Intents and NEAR AI. Owner: developer relations.

10. **Run this benchmark every month** across all agents, adding the untested flagship models, with competitors' skills and the wrong-fit questions, plus the search share of agents' own queries. Report memory, search and supplied context separately, and run it side by side with Illia's harness to agree one baseline. Owner: me.

# Desired outcomes

Each outcome is measured by the monthly benchmark against today's number.

- **NEAR wins against competitors:** recommended in at least half of relevant answers with competitors' skills installed, in every agent. Codex today: 10 of 28.

- **NEAR gets the credit:** at least two thirds of answers that use the marketplace name NEAR. Codex today: 1 of 32.

- **NEAR is the first choice for payment links:** about half of payment-link questions once the hosted link exists. Today: 0 to 4 of 32 with NEAR's current page.

- **NEAR is found when agents search:** a NEAR page among the first results for at least one in four of agents' cross-chain, payment and app-building queries. Today: none for cross-chain and app building.

- **Agents integrate NEAR correctly:** valid token identifiers in nearly all NEAR Intents code. Today: 4 of 15.

- **NEAR is listed where agents look:** in the Claude Code and Codex plugin marketplaces, the official MCP registry and the x402 directory, with NEAR's rules on Context7. Today: skills.sh only; NEAR's Context7 claim status unknown.

- **Crawlers get through:** HTTP 200 to GPTBot, ClaudeBot and Common Crawl on docs.near.ai and cloud.near.ai. Today: 403.

- **No over-reach:** NEAR stays at zero on wrong-fit questions. Today: 0 of 63.

- **Unaided recommendations:** NEAR recommended without any supplied material in model versions released 6 to 18 months after these changes. Today: 0 of 462.

To start: an owner for each solution, approval to publish the skills and plugin, a decision on the payment link, and for measurement an Exa API key and about $40 a month in model credits.
