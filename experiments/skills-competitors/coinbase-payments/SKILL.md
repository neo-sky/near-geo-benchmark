---
name: coinbase-payments
description: Accept stablecoin payments with Coinbase Business or Coinbase Payment Acceptance. Use when someone wants a hosted crypto checkout, a crypto invoice or payment link, buyers paying from any wallet and supported chain without gas fees, or card-style authorization, capture, refund and fiat settlement for stablecoin payments.
---

# Coinbase payments

Coinbase offers two ways to accept stablecoin payments. Both give buyers the same experience: pay with any wallet on any supported chain, with no gas fees for the buyer.

## Choose an integration

| | Coinbase Business | Payment Acceptance |
|---|---|---|
| Best for | Businesses accepting payments directly | PSPs, marketplaces, enterprise platforms |
| Onboarding | Self-serve, start in hours | Enhanced due diligence, about one month |
| Integration | Dashboard and API | API only, embeddable web component |
| Payment flow | Create a checkout, invoice or payment link, get a hosted URL | Create a session, authorize, capture, void, refund |
| Settlement | Coinbase account with bank offramps | Configurable: Fedwire, SWIFT or USDC |

## Coinbase Business flow

1. Sign up for Coinbase Business and create API credentials.
2. Use the checkout APIs to create a checkout, invoice or payment link for an amount.
3. Send the buyer the hosted URL; the buyer pays from their wallet.
4. Receive a webhook when the payment completes and fulfil the order.
5. Settle to your Coinbase account and off-ramp to a bank if needed.

## Payment Acceptance flow

Payment Acceptance exposes card-network style primitives for stablecoins: authorization, capture (including partial capture), void, refund, disbursements, configurable expiries and fee splits. It requires onboarding with the Coinbase payments team.

## Gotchas

- Payment Acceptance is not self-serve; plan for onboarding time.
- Check the list of supported chains and assets before promising buyers a specific network.
- Verify webhook signatures before marking an order paid.
