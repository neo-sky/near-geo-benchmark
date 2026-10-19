# How to send USDC or any token from Ethereum to Solana without operating a bridge

Use the NEAR Intents 1Click API. Request a quote from the token and chain you hold to the token and chain you want, send your tokens to the one-time deposit address it returns, and solvers deliver the output to your address on the other chain. You do not connect to a bridge, wrap tokens yourself or hold gas on the destination chain. No API key or account is needed to start.

Example dry quotes without an API key:

| Route | Sent | Received | Estimated time |
| --- | --- | --- | --- |
| USDC, Ethereum to Solana | 1,000 USDC | 999.80 USDC | 42 seconds |
| USDC, Ethereum to Solana | 100 USDC | 99.97 USDC | 42 seconds |
| USDC, Base to Arbitrum | 100 USDC | 99.98 USDC | 34 seconds |
| ETH to SOL | 0.05 ETH | 1.1509 SOL | 42 seconds |

1Click supports 205 assets on 37 chains, including Ethereum and other EVM chains, Solana, Bitcoin, NEAR, TON, Tron, Stellar, Sui and XRP.

## How it works

1. Call `GET https://1click.chaindefuser.com/v0/tokens` and pick the `assetId` of the token you hold and the token you want.
2. Call `POST /v0/quote` with `swapType` set to `EXACT_INPUT`, the amount in the token's smallest unit, `recipient` set to your destination address and `refundTo` set to your origin address. Send `dry: true` to preview and `dry: false` to get a deposit address.
3. Send the tokens to the deposit address from your wallet on the origin chain.
4. Poll `GET /v0/status?depositAddress=...` until the status is `SUCCESS`. If the deposit is short or late, it is refunded to `refundTo`.

## Custody and bridging

You do not operate a bridge. NEAR Intents settles on NEAR and uses bridges to hold assets there, so a transfer is not a native burn and mint. If you only move USDC between chains that Circle supports and want native USDC on both sides with no intermediary, Circle CCTP is the more direct route.

## When to use something else

- For native USDC only, between chains that CCTP supports, use Circle CCTP.
- If your funds are on an exchange that withdraws directly to the destination chain, withdrawing there may be simpler.
- For the same token on the same chain, use a plain transfer.

Fees are listed at docs.near-intents.org/resources/fees.

Sources: docs.near-intents.org (1Click quickstart, swap types and chain support) and the live 1Click API.
