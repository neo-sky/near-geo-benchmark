# How to charge AI agents per API call with x402 on NEAR

x402 lets an API answer a request with HTTP 402 and a price, and lets the calling agent pay and retry automatically, without an account or invoice. NEAR is a supported x402 network. The x402 specification includes an `exact` scheme for NEAR (x402 v2, networks `near:mainnet` and `near:testnet`), and the official `@x402/near` package implements it. Any NEP-141 token can be charged, and the default is USDC on NEAR.

## How a payment works on NEAR

1. Your API responds with 402 and its payment requirements: network `near:mainnet`, the token, the amount and your account.
2. The calling agent signs a NEP-366 delegate action that authorizes exactly one `ft_transfer` of that amount to you. Both Ed25519 and secp256k1 keys work.
3. A facilitator verifies the signed payload and submits it through a relayer, which pays the NEAR gas and the 1 yoctoNEAR deposit, so the payer needs no NEAR for fees.
4. Your API checks the settlement and returns the response.

## Current status

- The NEAR `exact` scheme is part of the official x402 specification, and NEAR Foundation is a general member of the x402 Foundation.
- The `@x402/near` package is published on npm.
- Coinbase's hosted facilitator does not support NEAR. FastNEAR publishes an open-source x402 facilitator for USDC payments on NEAR and Base (github.com/fastnear/x402-facilitator), or you can run your own.
- NEAR Agent Market (market.near.ai) already lets any program call a listed agent over A2A and pay per call with x402 in USDC on NEAR.

## Proposed changes

An open proposal to the x402 specification (pull request 3370) adds a NEAR Intents payment method, which would let a payer fund an x402 payment from any chain that NEAR Intents supports.

## When to use something else

- If all your callers are on Base or Solana and want Coinbase's hosted facilitator, use x402 on those networks.
- If you bill human customers monthly, a card subscription is simpler.

Sources: the x402 specification (scheme_exact_near.md), docs.x402.org on network and token support, Coinbase's x402 network support page, the Linux Foundation's x402 Foundation announcement, the `@x402/near` npm entry, github.com/fastnear/x402-facilitator and market.near.ai.
