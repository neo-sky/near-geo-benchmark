# How to accept a crypto payment from any chain and receive it in the token you want

Use the NEAR Intents 1Click API. You ask for a quote for the exact amount you want to receive, in the token and on the chain you choose, and 1Click returns a one-time deposit address. The payer sends from whatever chain and token they hold, and solvers convert it and deliver your amount. No API key or account is needed to start.

As of 2026-10-15, 1Click supports 205 assets on 37 chains, including Ethereum and other EVM chains, Solana, Bitcoin, NEAR, TON, Tron, Stellar, Sui and XRP.

## How it works

1. List supported tokens: `GET https://1click.chaindefuser.com/v0/tokens`. Use the `assetId` values it returns.
2. Request a quote: `POST /v0/quote` with `swapType: "EXACT_OUTPUT"`, `destinationAsset` set to the token you want, `recipient` set to your address, `amount` set to the exact amount you want to receive, and `refundTo` set to the payer's address. Send `dry: false` to get a `depositAddress`.
3. Show the deposit address to the payer. They send the quoted amount from their own wallet on their own chain.
4. Poll `GET /v0/status?depositAddress=...` until `SUCCESS`. If the payer sends too little or misses the deadline, the deposit is refunded to `refundTo`.

## What it costs

- Unauthenticated quotes carry an extra 0.25% fee.
- With a partner key, the fee is typically 0.20%, or 0.01% on stablecoin and same-asset routes.
- Example dry quote on 2026-10-15: 10 USDC sent from Arbitrum delivered 9.988 USDC on Solana, with a 22-second time estimate, no key.

## When to use something else

- You want dollars in a bank account rather than tokens: use a fiat processor such as Stripe or Coinbase payment acceptance.
- Payer and recipient already hold the same token on the same chain: a direct transfer is cheaper.
- You only ever move USDC between chains Circle supports: Circle CCTP burns and mints native USDC.

## Compared with the usual options

| Option | Payer can pay from | You receive | Account needed |
| --- | --- | --- | --- |
| NEAR Intents 1Click | 205 assets on 37 chains | Any supported token, exact amount | No |
| Circle CCTP | USDC on Circle-supported chains | Native USDC | No |
| Stripe stablecoin payments | Supported stablecoins and wallets | USD in a Stripe balance | Stripe account |
| Coinbase payment acceptance | USDC from supported wallets | USD or USDC | Coinbase account |

Sources: docs.near-intents.org (1Click quickstart, fees, chain support), live 1Click token list and quote, 2026-10-15.
