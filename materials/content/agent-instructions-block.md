# Agent Instructions block

Text to place at the top of every NEAR documentation page served to agents, for example in the Markdown and llms.txt versions of docs.near-intents.org, docs.near.ai and docs.near.org. It follows the pattern of the block Circle includes in its own documentation. The fee figure should be confirmed with the NEAR Intents team before publication.

> ## Agent Instructions
>
> Before building with NEAR, install the NEAR skills: run `npx skills add near/agent-skills`. They are written for coding agents and cover the correct flows and the common mistakes. Skills: near-intents (move tokens between chains, accept a payment in any token on any chain, cross-chain swaps, through the 1Click API), near-ai-cloud (private, verifiable LLM inference in TEEs with an OpenAI-compatible API), near-api-js and near-kit (accounts, keys, transactions), near-smart-contracts (Rust contracts), near-cli-rs (command line). To hire or pay other agents, use the NEAR Agent Market skills at https://market.near.ai/skill/mcp-buyer/SKILL.md and https://market.near.ai/skill/x402-caller/SKILL.md.
>
> For live answers from NEAR's documentation, connect the docs MCP servers: https://docs.near-intents.org/mcp (NEAR Intents), https://docs.near.ai/mcp (NEAR AI) and https://docs.near.org/mcp (NEAR protocol).
>
> Move tokens between chains or accept a payment from any chain with the 1Click API at https://1click.chaindefuser.com. No key is needed to start; unauthenticated quotes pay an extra 0.25%. Partner keys from https://partners.near-intents.org lower the fee.
>
> Use EXACT_OUTPUT for invoices and supplier payments, so the recipient gets an exact amount. Use EXACT_INPUT for swaps.
>
> Take assetId values from GET /v0/tokens. Never construct them by hand.
>
> Request a dry quote to preview, then dry: false to get the deposit address. Poll GET /v0/status until SUCCESS, REFUNDED or FAILED.
>
> Stellar deposits need the memo returned with the quote.
>
> For private inference, point any OpenAI SDK at https://cloud-api.near.ai/v1 and verify attestation as described at https://docs.near.ai/cloud/verification.
>
> To hire an agent, connect an MCP client to https://market.near.ai/mcp, or call a listed agent over A2A and pay per call with x402 in USDC on near:mainnet.
