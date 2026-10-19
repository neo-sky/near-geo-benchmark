# How AI models learn about products, and what is known to work

A product reaches an AI agent's answer through four channels, each on its own clock:

| Channel | What it is | How fast a change shows | Who controls it |
|---|---|---|---|
| Training data | What the model learned before release | 6 to 18 months, at the next model version | The provider, fed by crawlers, licensed data and code |
| Search at answer time | What the agent finds when it searches | Days to weeks | The search index the agent uses |
| Context in the session | Skills, MCP servers, docs services, AGENTS.md | Immediately, once installed | NEAR and the developer |
| Post-training | Fine-tuning and preference training by the provider | Not externally controllable | The provider |

The study's own results place NEAR's losses in the first two channels: agents do not recall NEAR (0 of 462), and when they search, NEAR pages rarely come back. The third channel works when it is reached. What follows is what is publicly known about each channel, with the strength of the evidence.

## 1. How providers gather training data

**Their own crawlers, with separate switches for training and search.**

- OpenAI runs GPTBot for training, OAI-SearchBot for ChatGPT search and ChatGPT-User for fetches a user asks for. Each has its own robots.txt entry; blocking GPTBot keeps a site out of training but in search. [1]
- Anthropic runs ClaudeBot for training, Claude-SearchBot for search and Claude-User for user requests, each separately controllable. A ClaudeBot block affects only future training. [2]
- Google uses one crawler, Googlebot, plus a robots.txt token, Google-Extended, that decides whether crawled pages may train Gemini and ground Gemini answers. Google-Extended does not affect Search or AI Overviews, which run on ordinary Search ranking. [3]

NEAR's position: docs.near.ai and cloud.near.ai refuse GPTBot, ClaudeBot and CCBot but serve the search and user agents. NEAR's documentation is therefore reachable at answer time and missing from training. Cloudflare began blocking known AI crawlers by default on new domains in July 2025 and asks new domain owners to opt in [4]. Both NEAR hosts answer from Cloudflare with the pattern of that rule, so the block is likely a default rather than a decision. That is an inference to confirm in the Cloudflare dashboard.

**Common Crawl.** Of 47 language models released from 2019 to October 2023, at least 64% were trained on Common Crawl, and more than 80% of GPT-3's tokens came from it [5]. CCBot is refused by docs.near.ai, and Common Crawl holds none of its documentation pages (paper, Table 6).

**Licensed platforms.** Google and OpenAI license Reddit's posts in real time, reported at about $60 million and $70 million a year, and OpenAI licenses Stack Overflow's Q&A [6]. These platforms reach models through direct feeds, not only crawls. NEAR has a Stack Overflow tag (nearprotocol, 640 questions, against 1,345 for solana alone), but a search found no posts about NEAR Intents, the 1Click API or Chain Signatures and two about NEAR AI. Circle's CCTP has six, so this channel is thin for every newer product.

**Public code.** Training sets for code models are built from public GitHub repositories, for example The Stack, whose latest version crawls GitHub directly [7]. Code that integrates NEAR Intents mostly does not say NEAR: 46% of public files calling the 1Click host mention NEAR Intents, against 89% for Circle's CCTP (paper, Section 6.7).

**Wikipedia.** It is part of most pretraining mixtures. NEAR's article describes NEAR as a sharded blockchain and does not mention NEAR Intents, NEAR AI, the 1Click API, Chain Signatures or the Agent Market. Wikipedia's conflict-of-interest rules mean NEAR staff should not edit it directly; the accepted route is an edit request on the article's talk page, backed by independent published sources.

**Lag.** Published knowledge cutoffs sit months before release, from about four months to more than a year, and models stay in use for a year or more after that [8]. Training-data work done now reaches models released in roughly 6 to 18 months.

## 2. How agents search at answer time

| Agent | Search source | Evidence | What helps a page appear |
|---|---|---|---|
| ChatGPT and Codex | Mostly Bing, plus OpenAI's own index | 87% of ChatGPT citations match Bing's top results (vendor study); OpenAI does not disclose the mix [9] | Bing Webmaster Tools and IndexNow, which notifies Bing of new pages within minutes to hours [10] |
| Claude | Brave Search | Strong but unofficial: Brave on Anthropic's subprocessor list and Brave parameters in Claude's search tool [9] | Brave crawls whatever Googlebot can reach and keeps only pages with evidence of usefulness [11] |
| Gemini and AI Overviews | Google Search | Google says AI features run on core Search ranking [12] | Ordinary SEO |
| opencode | Exa | The study's logs | Exa's own index |

This study adds a behaviour none of these sources describe. Codex chooses the vendor first and then searches only that vendor's site (107 of 152 queries). For Codex, search cannot introduce NEAR; only training data or installed context can.

**What correlates with being cited.** Independent of engine, AI answers draw mostly on third-party sources. One tracking study attributes 84% of citations to earned sources such as journalism, research, encyclopedias and third-party sites, and 0.3% to paid content [13]. Across 75,000 brands, mentions of a brand on other sites correlated with appearing in AI Overviews at 0.66, against 0.22 for backlinks, and a later update found YouTube mentions the strongest single correlate at about 0.74 [14]. These are correlations measured by vendors of the measuring tools, not controlled experiments. The original GEO study found that adding statistics, quotations and citations to a page raised its visibility, and keyword stuffing did not [15].

**llms.txt.** Adoption grew from about 4,000 sites to 36,000 in a year, but in a study of 137,000 domains, 97% of llms.txt files received no request in a month, and no study ties the file to citations. Among AI agents, GPTBot and Claude Code were the most frequent requesters [16]. It is cheap to publish and may help coding agents, but it is not a visibility lever on its own.

## 3. How agents choose once material is in the session

- **Skills.** Anthropic's documentation states that the description field is what Claude matches a request against to decide whether to load a skill, and that only names and descriptions sit in context until then [17]. This is the mechanism the study measured: descriptions that name users' tasks get opened.
- **Documentation services.** Context7 serves current library documentation to coding agents through an MCP server. Anyone can add a public repository, and owners can claim a listing and add a `context7.json` with rules that appear as recommendations in the context given to agents [18]. Context7 already indexes /near/intents and /near/docs. Claiming them would let NEAR state the rules agents broke in this study: fetch token identifiers from the token list and use the exact-amount quote for fixed prices.
- **Popularity bias.** Language models over-rely on popular libraries, unnecessarily in up to 48% of cases, and the authors note this creates discoverability problems for newer projects [19]. A study of library recommenders found language models do not remove this bias [19]. This is the background to a baseline of zero.
- **Invented packages.** In the largest study, 19.7% of packages suggested by code models did not exist, falling to 4.6% to 6.1% for newer models in a follow-up preprint, and attackers register the invented names [20]. In this study's runs, agents suggested only two NEAR-related npm packages, both real; what they invented were token identifiers.

## 4. Known methods mapped to the desired outcomes

| Desired outcome | Method | Evidence | NEAR today |
|---|---|---|---|
| Recommended without help, in future models | Let training crawlers and Common Crawl read the docs | Established: crawl is the main pretraining source [5] | Blocked on docs.near.ai and cloud.near.ai |
| | NEAR named in code: host, SDK scope, READMEs | Mechanism established [7]; effect on recommendation untested | 46% of 1Click code names NEAR |
| | Mentions on third-party sites, video and communities | Correlational, vendor studies [13, 14] | Thin for current products |
| | Accurate Wikipedia coverage through talk-page requests | Wikipedia is in most corpora; effect untested | Article omits current products |
| Found when agents search | Problem-shaped use-case pages | This study: the NEAR pages that ranked were use-case pages | Five pages written, not published |
| | Bing Webmaster Tools and IndexNow (ChatGPT) | Vendor evidence of Bing dependence [9, 10] | Not checked |
| | Crawlable to Googlebot, so to Brave (Claude) | Brave's own documentation [11] | Allowed |
| | Third-party comparison content | Earned sources dominate citations [13] | Absent for cross-chain |
| Chosen when in context | Task-naming skill descriptions | Anthropic docs [17] and this study | Rewrites tested |
| | Listings in plugin marketplaces, MCP registry, x402 directory | This study: absent, competitors present | Only skills.sh |
| | Claim Context7 listings and add rules | Context7 docs [18] | Indexed (/near/intents, /near/docs); claim status unknown |
| Correct integrations | Context7 rules and Agent Instructions | This study: exact-amount quote 0 to 13 of 20 | Not in place |

## 5. What not to do

- Hidden text addressed to agents is treated as prompt injection by providers.
- Fabricated reviews, posts or answers would contaminate the sources engines rely on, and would breach the platforms' rules.
- Editing NEAR's own Wikipedia article as staff breaches Wikipedia's conflict-of-interest rules.
- Paid placement barely registers in AI citations (0.3%) [13].
- Keyword stuffing did not improve visibility in the original GEO study [15].

These methods are in the paper's recommendations (Section 6) and the proposal. Because training-data work shows only in models released 6 to 18 months later, the monthly benchmark reports memory (no help, no search) separately from search and supplied context.

## Sources

[1] OpenAI, Overview of OpenAI crawlers. https://developers.openai.com/api/docs/bots

[2] Anthropic help center, crawler documentation, and PPC Land's summary. https://support.claude.com/en/articles/8896518 ; https://ppc.land/anthropic-clarifies-what-its-three-web-crawlers-do-and-how-to-block-them/

[3] Google-Extended explained (third-party summaries of Google's documentation). https://ppc.land/google-extended/ ; https://www.pepper.inc/blog/google-extended-explained/

[4] Cloudflare blocks AI crawlers by default and launches Pay Per Crawl. https://alternativeto.net/news/2025/7/cloudflare-blocks-ai-crawlers-by-default-and-launches-pay-per-crawl-for-publishers ; https://decrypt.co/328057/cloudflare-hits-kill-switch-ai-crawlers-entire-industry-cheers

[5] Mozilla Foundation, Training Data for the Price of a Sandwich. https://www.mozillafoundation.org/en/blog/Mozilla-Report-How-Common-Crawl-Data-Infrastructure-Shaped-the-Battle-Royale-over-Generative-AI/

[6] OpenAI inks deal to train AI on Reddit data; AI content licensing deals mapped. https://techcrunch.com/2024/05/16/openai-inks-deal-to-train-ai-on-reddit-data ; https://llmpulse.ai/blog/ai-content-licensing-deals/

[7] BigCode, The Stack v2; The Stack v3 coverage. https://huggingface.co/datasets/bigcode/the-stack-v2 ; https://www.deeplearning.ai/the-batch/fresh-data-for-coding-models-hugging-face-updated-the-stack-the-largest-crawl-of-public-github-repositories

[8] LLMLagBench: Identifying Temporal Training Boundaries in Large Language Models. https://arxiv.org/html/2511.12116v1

[9] ChatGPT Search and Bing; Claude web search and Brave. https://searchengineland.com/chatgpt-search-microsoft-bing-seo-448019 ; https://www.parse.gl/blog/bing-rankings-chatgpt-visibility ; https://www.tryprofound.com/blog/what-is-claude-web-search-explained

[10] IndexNow and Bing Webmaster Tools for ChatGPT visibility. https://martech.zone/chatgpt-visibility-and-bing-indexnow/

[11] Brave Search help, Brave Search crawler. https://search.brave.com/help/brave-search-crawler

[12] Mastering generative engine optimization in 2026. https://searchengineland.com/mastering-generative-engine-optimization-in-2026-full-guide-469142

[13] Muck Rack Generative Pulse, May 2026. https://techintelpro.com/news/ai/generative-ai/muck-rack-may-2026-study-earned-media-drives-84-of-ai-citations

[14] Ahrefs, AI Overview brand visibility factors (75K brands) and branded web mentions. https://ahrefs.com/blog/ai-overview-brand-correlation/ ; https://ahrefs.com/blog/branded-web-mentions-visibility-ai-search/

[15] Aggarwal et al., GEO: Generative Engine Optimization. https://arxiv.org/abs/2311.09735

[16] Ahrefs, We analyzed 137K sites: 97% of llms.txt files never get read. https://ahrefs.com/blog/llmstxt-study/

[17] Anthropic, Agent Skills documentation. https://platform.claude.com/docs/en/agents-and-tools/agent-skills/ ; https://code.claude.com/docs/en/agent-sdk/skills

[18] Context7, Adding libraries and claiming libraries. https://context7.com/docs/adding-libraries ; https://context7.com/docs/howto/claiming-libraries

[19] A Study of LLMs' Preferences for Libraries and Programming Languages (arXiv 2503.17181); popularity bias in library recommenders (arXiv 2501.10313). https://arxiv.org/abs/2503.17181 ; https://arxiv.org/abs/2501.10313

[20] We Have a Package for You! A Comprehensive Analysis of Package Hallucinations by Code Generating LLMs (USENIX Security 2025). https://arxiv.org/abs/2406.10279
