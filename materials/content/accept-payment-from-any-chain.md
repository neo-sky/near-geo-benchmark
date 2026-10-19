# How to accept a crypto payment from any chain and receive it in the token you want

Use the NEAR Intents 1Click API. You request a quote for the exact amount you want to receive, in the token and on the chain you choose, and 1Click returns a one-time deposit address. The payer sends from whatever chain and token they hold, and solvers convert the payment and deliver your amount. No API key or account is needed to start.

1Click supports 205 assets on 37 chains, including Ethereum and other EVM chains, Solana, Bitcoin, NEAR, TON, Tron, Stellar, Sui and XRP.

## How it works

1. List the supported tokens with `GET https://1click.chaindefuser.com/v0/tokens` and use the `assetId` values it returns.
2. Request a quote with `POST /v0/quote`. Set `swapType` to `EXACT_OUTPUT`, `destinationAsset` to the token you want, `recipient` to your address, `amount` to the exact amount you want to receive and `refundTo` to the payer's address. Send `dry: false` to get a `depositAddress`.
3. Show the deposit address to the payer, who sends the quoted amount from their own wallet on their own chain.
4. Poll `GET /v0/status?depositAddress=...` until the status is `SUCCESS`. If the payer sends too little or misses the deadline, the deposit is refunded to `refundTo`.

## Cost

Unauthenticated quotes carry an extra 0.25% fee. With a partner key the fee is typically 0.20%, or 0.01% on stablecoin and same-asset routes. In an example dry quote without a key, 10 USDC sent from Arbitrum delivered 9.988 USDC on Solana with an estimated time of 22 seconds.

## When to use something else

- If you want US dollars in a bank account rather than tokens, use a fiat processor such as Stripe or Coinbase payment acceptance.
- If the payer and recipient already hold the same token on the same chain, a direct transfer is cheaper.
- If you only move USDC between chains that Circle supports, Circle CCTP burns and mints native USDC.

## Comparison

| Option | Payer can pay from | You receive | Account needed |
| --- | --- | --- | --- |
| NEAR Intents 1Click | 205 assets on 37 chains | Any supported token, exact amount | No |
| Circle CCTP | USDC on Circle-supported chains | Native USDC | No |
| Stripe stablecoin payments | Supported stablecoins and wallets | USD in a Stripe balance | Stripe account |
| Coinbase payment acceptance | USDC from supported wallets | USD or USDC | Coinbase account |

Sources: docs.near-intents.org (1Click quickstart, fees and chain support) and the live 1Click token list and quote endpoints.
