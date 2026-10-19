# Site and crawl audit notes

The Common Crawl counts come from the public index server at index.commoncrawl.org, queried per host and crawl. I sent the requests from a residential IP address with the user-agent strings of each crawler and recorded the status after following redirects, so a status code shows how a rule keyed on the user agent responds. It does not show what a verified crawler receives from its own IP range, and the Cloudflare rules should be confirmed in the dashboard.

## Crawler access by user agent

| URL | Browser | GPTBot | OAI-SearchBot | ChatGPT-User | ClaudeBot | Claude-SearchBot | Claude-User | PerplexityBot | CCBot | Amazonbot | Bytespider |
|---|---|---|---|---|---|---|---|---|---|---|---|
| docs.near.ai/cloud/introduction | 200 | 403 | 200 | 200 | 403 | 200 | 200 | 200 | 403 | 403 | 403 |
| cloud.near.ai | 200 | 403 | 200 | 200 | 403 | 200 | 200 | 200 | 403 | 403 | 403 |
| near.ai | 200 | 200 | 200 | 200 | 200 | 200 | 200 | 200 | 200 | 200 | 200 |
| market.near.ai | 200 | 200 | 200 | 200 | 200 | 200 | 200 | 200 | 200 | 200 | 200 |
| docs.near-intents.org | 200 | 200 | 200 | 200 | 200 | 200 | 200 | 200 | 200 | 200 | 200 |
| docs.near.org | 200 | 200 | 200 | 200 | 200 | 200 | 200 | 200 | 200 | 200 | 200 |
| near.com | 200 | 200 | 200 | 200 | 200 | 200 | 200 | 200 | 200 | 200 | 200 |

docs.near.ai and cloud.near.ai answer with `server: cloudflare` and status 403 to every training crawler, while allowing browsers, search crawlers, user-initiated fetchers, Googlebot and Bingbot. On those two hosts the allowed agents are first redirected (docs.near.ai/cloud/introduction now redirects to the site root, and cloud.near.ai to its sign-in page). This matches Cloudflare's rule for blocking AI training crawlers. The robots.txt file on docs.near.ai states the opposite: `Content-Signal: ai-train=yes, search=yes, ai-input=yes`.

## Text visible without JavaScript

| Page | Body text in raw HTML | Notes |
|---|---|---|
| market.near.ai/ | 20 words | A notice that the site needs JavaScript and that its API is at /v1/; the title and meta description are in the head |
| market.near.ai/jobs | 20 words | Same application page |
| market.near.ai/sitemap.xml | Application page | No sitemap; the application page is served as HTML |
| market.near.ai/robots.txt | Application page | No robots file |
| near-intents.org/ | 0 words | Title and meta description only; llms.txt returns 404 |
| near.ai/ | 1,424 words | Server-rendered |
| near.com/ | 490 words | Server-rendered |
| www.near.org/intents | 245 words | Server-rendered |
| docs.near-intents.org/ | 616 words | Server-rendered |

market.near.ai content exists only as Markdown (`/agents/<category>.md`, `/skill/SKILL.md`, `/llms.txt`) and as `/openapi.json`, and nothing in its HTML links to those files.

## Common Crawl captures with status 200

| Host | CC-MAIN-2026-25 | CC-MAIN-2026-34 | CC-MAIN-2026-39 |
|---|---|---|---|
| docs.near.ai | 1 (robots.txt) | 0 | 2 (robots.txt) |
| cloud.near.ai | 0 | 0 | 0 |
| near.ai | 18 | 19 | 14 |
| market.near.ai | 329 | 1,503 | 723 |
| near-intents.org | 8 | 4 | 3 |
| docs.near-intents.org | 11 | 28 | 24 |
| docs.near.org | 182 | 128 | 147 |

Several first attempts against the index returned gateway errors (502 and 504). The counts above come from repeated queries that returned either captures or an explicit empty result. A sampled market.near.ai record from CC-MAIN-2026-34 contains the page's text; the sampled records from CC-MAIN-2026-39 contain only the title and the JavaScript notice.

## Names used for the agent marketplace

| Where | Name |
|---|---|
| HTML title on market.near.ai | agent.market |
| market.near.ai/llms.txt | Agents Marketplace |
| market.near.ai/agents/*.md | NEAR AI Agents Market |
| market.near.ai/openapi.json | agents-market API |
| Polosukhin's baseline report | Agent Market (market.near.ai) |

## Access for agents

- The 1Click API works without a key. The documentation states that unauthenticated quotes carry an extra 0.25% fee, and that partner quotes typically pay 20 basis points, or 1 basis point on stablecoin and same-asset routes (docs.near-intents.org llms-full). Dry quotes without a key on stablecoin routes cost between 0.02% (1,000 USDC) and 0.12% (10 USDC) in total, including fixed refund and withdrawal fees, which does not match the documented fee.
- market.near.ai lets an agent call a listed agent over A2A and pay per call with x402, without an account or API key (market.near.ai/llms.txt).
- NEAR AI Cloud requires an API key created by a person at cloud.near.ai.

## Preliminary web searches

One Claude web search per domain, run before the main study.

| Domain | NEAR present |
|---|---|
| Payments | No |
| Agent commerce | No |
| Cross-chain | No |
| Per-user wallets | No |
| Hiring | One market.near.ai job listing, no product page |
| Private AI | NEAR AI Cloud, through skills.sh only |

## Content gaps

- docs.near-intents.org llms-full contains no occurrence of "payment link", "accept payment" or "invoice"; EXACT_OUTPUT appears 7 times, only as a swap type.
- The History section of the Wikipedia article on NEAR ends with 2019 to 2021, and the article does not mention Intents, NEAR AI or Chain Signatures.
- skills.sh lists 11 skills for near/agent-skills, with 514 installs in total and 138 for near-intents.
