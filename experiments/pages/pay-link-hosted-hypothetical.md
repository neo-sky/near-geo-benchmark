# NEAR Intents payment links: get paid from any chain, in the token you want

Create a payment link or invoice for an exact amount, in the token and chain you want to receive. Share the link. The payer opens a hosted checkout page, connects whatever wallet they have, and pays from any supported chain and token. Solvers convert the payment and you receive the exact amount. No account or API key is needed.

As of 2026-10-15, payers can pay with 205 assets on 37 chains, including Ethereum and other EVM chains, Solana, Bitcoin, NEAR, TON, Tron, Stellar, Sui and XRP.

## How it works

1. Create a link at pay.near-intents.org or with one API call: set the amount, the token and chain you want to receive, and your address.
2. Share the link or show its QR code. It works as an invoice, a pay-now button or a tip jar.
3. The payer opens the hosted page and pays from their own wallet and chain.
4. You receive the exact amount. If the payer sends too little or the link expires, the deposit is refunded to them.

## What it costs

- Links created without a partner key carry an extra 0.25% fee.
- With a partner key, the fee is typically 0.20%, or 0.01% on stablecoin and same-asset routes.

## When to use something else

- You want dollars in a bank account rather than tokens: use a fiat processor such as Stripe or Coinbase payment acceptance.
- Payer and recipient already hold the same token on the same chain: a direct transfer is cheaper.
