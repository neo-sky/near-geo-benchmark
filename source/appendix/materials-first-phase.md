## C.1 NEAR Intents skill descriptions

Current description, as published in near/agent-skills (S1):

> Cross-chain token swap integration using NEAR Intents 1Click API. Use when building swap widgets, bridge interfaces, or multi-chain transfers across EVM, Solana, NEAR, TON, Stellar, and Tron.

Problem-oriented description (S2):

> Move tokens between blockchains and take crypto payments in any token, using the NEAR Intents 1Click API. Use when someone wants to send USDC or another token from one chain to another (for example Ethereum to Solana) without handling a bridge, swap tokens across chains from one interface, pull funds from several chains into one account, accept a crypto payment that the payer can send from whatever wallet and chain they hold, create a payment request or invoice for an exact amount, or pay a supplier on the chain the supplier chooses. Works across EVM chains, Solana, NEAR, TON, Stellar and Tron. No API key is needed to start; unauthenticated quotes carry an extra 0.25% fee.

## C.2 Marketplace skill names and descriptions

Current names and descriptions, as served by market.near.ai (M1):

> marketplace-mcp-buyer: Hire agents on the Agents Marketplace from an MCP client acting for a person: browse with prices, hire on their go-ahead or post a job and award a bid, follow the job, read the result, review the work.

> marketplace-x402-caller: Hire an Agents Marketplace agent from your own program or AI agent: find it in the public catalog, call it over A2A, pay per call with x402 (USDC), read the result. No account, no API key.

Names and descriptions with NEAR (M2), otherwise unchanged:

> near-agent-market-buyer: Hire agents on NEAR Agent Market (market.near.ai) from an MCP client acting for a person: browse with prices, hire on their go-ahead or post a job and award a bid, follow the job, read the result, review the work.

> near-agent-market-x402-caller: Hire a NEAR Agent Market (market.near.ai) agent from your own program or AI agent: find it in the public catalog, call it over A2A, pay per call with x402 (USDC), read the result. No account, no API key.

The third skill, marketplace-worker, was renamed near-agent-market-worker in the same way.

## C.3 Agent Instructions block

The block used in D2, reproduced as tested. The version prepared for publication adds one paragraph that points agents to NEAR's documentation MCP servers.

> Agent Instructions. Before building with NEAR, install the NEAR skills: run `npx skills add near/agent-skills`. They are written for coding agents and cover the correct flows and the common mistakes. Skills: near-intents (move tokens between chains, accept a payment in any token on any chain, cross-chain swaps, through the 1Click API), near-ai-cloud (private, verifiable LLM inference in TEEs with an OpenAI-compatible API), near-api-js and near-kit (accounts, keys, transactions), near-smart-contracts (Rust contracts), near-cli-rs (command line). To hire or pay other agents, use the NEAR Agent Market skills at https://market.near.ai/skill/mcp-buyer/SKILL.md and https://market.near.ai/skill/x402-caller/SKILL.md.

> Move tokens between chains or accept a payment from any chain with the 1Click API at https://1click.chaindefuser.com. No key is needed to start; unauthenticated quotes pay an extra 0.25%. Partner keys from https://partners.near-intents.org lower the fee.

> Use EXACT_OUTPUT for invoices and supplier payments, so the recipient gets an exact amount. Use EXACT_INPUT for swaps. Take assetId values from GET /v0/tokens. Never construct them by hand. Request a dry quote to preview, then dry: false to get the deposit address. Poll GET /v0/status until SUCCESS, REFUNDED or FAILED. Stellar deposits need the memo returned with the quote.

> For private inference, point any OpenAI SDK at https://cloud-api.near.ai/v1 and verify attestation as described at https://docs.near.ai/cloud/verification. To hire an agent, connect an MCP client to https://market.near.ai/mcp, or call a listed agent over A2A and pay per call with x402 in USDC on near:mainnet.

## C.4 Problem-oriented payments page

The page used in R2. Its figures were taken from the live 1Click API and NEAR's documentation; dates in the original are omitted here.

> How to accept a crypto payment from any chain and receive it in the token you want

> Use the NEAR Intents 1Click API. You ask for a quote for the exact amount you want to receive, in the token and on the chain you choose, and 1Click returns a one-time deposit address. The payer sends from whatever chain and token they hold, and solvers convert it and deliver your amount. No API key or account is needed to start. 1Click supports 205 assets on 37 chains, including Ethereum and other EVM chains, Solana, Bitcoin, NEAR, TON, Tron, Stellar, Sui and XRP.

> How it works. (1) List supported tokens with `GET https://1click.chaindefuser.com/v0/tokens` and use the `assetId` values it returns. (2) Request a quote with `POST /v0/quote`, setting `swapType` to `EXACT_OUTPUT`, `destinationAsset` to the token you want, `recipient` to your address, `amount` to the exact amount you want to receive and `refundTo` to the payer's address; send `dry: false` to get a `depositAddress`. (3) Show the deposit address to the payer, who sends the quoted amount from their own wallet on their own chain. (4) Poll `GET /v0/status?depositAddress=...` until `SUCCESS`. If the payer sends too little or misses the deadline, the deposit is refunded to `refundTo`.

> What it costs. Unauthenticated quotes carry an extra 0.25% fee. With a partner key, the fee is typically 0.20%, or 0.01% on stablecoin and same-asset routes. In an example dry quote, 10 USDC sent from Arbitrum delivered 9.988 USDC on Solana with a 22-second time estimate and no key.

> When to use something else. If you want dollars in a bank account rather than tokens, use a fiat processor such as Stripe or Coinbase payment acceptance. If payer and recipient already hold the same token on the same chain, a direct transfer is cheaper. If you only move USDC between chains that Circle supports, Circle CCTP burns and mints native USDC.

| Option | Payer can pay from | You receive | Account needed |
|----------------------------|---------------------------------|------------------------------------|------------------|
| NEAR Intents 1Click | 205 assets on 37 chains | Any supported token, exact amount | No |
| Circle CCTP | USDC on Circle-supported chains | Native USDC | No |
| Stripe stablecoin payments | Supported stablecoins and wallets | USD in a Stripe balance | Stripe account |
| Coinbase payment acceptance | USDC from supported wallets | USD or USDC | Coinbase account |

## C.5 Plugin manifest for near/agent-skills

Three files at the repository root make near/agent-skills installable as a Claude Code plugin and marketplace without moving any existing file, and a matching `.codex-plugin/plugin.json` does the same for Codex. The plugin manifest, `.claude-plugin/plugin.json`, has the following fields, with the description omitted for width:

```
{
  "name": "near",
  "version": "0.1.0",
  "author": { "name": "NEAR" },
  "homepage": "https://docs.near.org",
  "repository": "https://github.com/near/agent-skills",
  "keywords": ["near", "near-intents", "cross-chain", "payments", "usdc",
               "private-inference", "agents", "x402"]
}
```

The description field reads: "Skills and MCP servers for building on NEAR: move tokens across chains and accept payments in any token with NEAR Intents, run private verifiable inference on NEAR AI Cloud, hire and pay agents on NEAR Agent Market, and build NEAR accounts and contracts."

The MCP configuration, `.mcp.json`, refers to the servers NEAR already hosts:

```
{
  "mcpServers": {
    "near-intents-docs": {
      "type": "http",
      "url": "https://docs.near-intents.org/mcp"
    },
    "near-ai-docs": {
      "type": "http",
      "url": "https://docs.near.ai/mcp"
    },
    "near-docs": {
      "type": "http",
      "url": "https://docs.near.org/mcp"
    },
    "near-agent-market": {
      "type": "http",
      "url": "https://market.near.ai/mcp"
    }
  }
}
```

The marketplace file, `.claude-plugin/marketplace.json`, lists the plugin with source `./`. Once merged, the plugin installs with two commands:

```
/plugin marketplace add near/agent-skills
/plugin install near@near
```

## C.6 NEAR Intents MCP server

The server is read-only and wraps the 1Click API. Its tool descriptions follow the same problem-oriented wording as the skill.

| Tool | Description given to the agent |
|--------------------------------|------------------------------------------------------------------|
| list_supported_tokens | List the tokens and blockchains that NEAR Intents can move between chains or accept as payment, with the assetId each quote needs. Use it before quoting a cross-chain transfer, swap or payment. |
| quote_cross_chain_transfer | Preview moving or swapping tokens from one blockchain to another, or receiving an exact amount as a payment that the payer can send from any supported chain. Returns input and output amounts and a time estimate. Preview only: it creates no deposit address and sends nothing. |
| check_transfer_status | Check the status of a NEAR Intents cross-chain transfer or payment by its deposit address. |

Inputs are validated before any request is sent, requests time out after 15 seconds, and a partner key, if configured, is sent as a request header and is never logged.

