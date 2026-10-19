---
name: lifi
description: Cross-chain swaps and bridging through the LI.FI aggregator API. Use when someone wants to swap a token on one chain for a token on another, move funds between EVM chains and Solana with the best available bridge and DEX route, add a cross-chain swap feature or widget to a wallet or app, or consolidate balances from several chains. LI.FI compares bridges and DEXs and returns a ready-to-sign transaction.
---

# LI.FI

LI.FI aggregates bridges and DEX aggregators behind one API. A quote request returns the best route and a transaction the user signs on the source chain; LI.FI tracks the transfer until the destination side completes.

## Quick start

```ts
const params = new URLSearchParams({
  fromChain: "ETH",
  toChain: "SOL",
  fromToken: "USDC",
  toToken: "USDC",
  fromAmount: "100000000",            // 100 USDC, 6 decimals
  fromAddress: "0x0000000000000000000000000000000000000001",
  toAddress: "<solana-recipient>",
  slippage: "0.005",
  integrator: "my-app",
});
const quote = await fetch(`https://li.quest/v1/quote?${params}`).then((r) => r.json());

// 1. approve quote.estimate.approvalAddress for fromAmount (ERC-20 only)
// 2. send quote.transactionRequest from the user's wallet
// 3. poll status
const status = await fetch(
  `https://li.quest/v1/status?txHash=${txHash}&fromChain=ETH&toChain=SOL`,
).then((r) => r.json());
// status.status is PENDING, DONE or FAILED
```

## Integration options

- REST API at `https://li.quest/v1` (`/quote`, `/routes`, `/status`, `/chains`, `/tokens`).
- `@lifi/sdk` for TypeScript, which handles approvals, execution and status updates.
- `@lifi/widget`, a React component that embeds a complete cross-chain swap UI.

## Key concepts

- `quote.tool` names the bridge or DEX chosen for the route.
- `quote.estimate.toAmount` and `toAmountMin` give the expected and minimum received amounts.
- Integrators can set a fee with the `fee` parameter and collect it through LI.FI's fee contracts.
- An API key (`x-lifi-api-key`) raises rate limits but is not required to start.

## Gotchas

- Always respect `toAmountMin`; routes can fail if prices move beyond the slippage tolerance.
- Some routes need a second transaction on the destination chain; check `quote.includedSteps`.
- Token approvals are per spender; reuse the approval address from the quote, not a hardcoded one.
