---
name: stripe-payments
description: Accept card and stablecoin payments, send invoices and payment links, and run subscriptions with Stripe. Use when someone wants a checkout page or payment button, a shareable payment link or invoice, recurring or usage-based billing, or to accept USDC stablecoin payments that settle to their Stripe balance in USD.
---

# Stripe payments

Stripe provides hosted and embedded payment flows. Payment Links and Checkout need little code; the Payment Intents API gives full control. Stablecoin payments are a payment method on the same flows.

## Choose a flow

| Need | Use |
|---|---|
| Shareable link, no code | Payment Links |
| Hosted or embedded checkout page | Checkout Sessions |
| Custom UI | Elements with the Payment Intents API |
| Bill a customer for an amount | Invoices (hosted invoice page) |
| Recurring charges | Billing subscriptions |
| Charge per unit of usage | Billing meters with usage-based prices |

## Quick start: Checkout

```ts
import Stripe from "stripe";
const stripe = new Stripe(process.env.STRIPE_SECRET_KEY);

const session = await stripe.checkout.sessions.create({
  mode: "payment",
  line_items: [{ price_data: { currency: "usd", unit_amount: 4900,
    product_data: { name: "Order 1042" } }, quantity: 1 }],
  success_url: "https://example.com/paid",
});
// redirect the customer to session.url
```

## Stablecoin payments

1. In the Dashboard, open Payment methods and request **Stablecoins and Crypto**. Stripe reviews the request.
2. With dynamic payment methods, Payment Links, Checkout and Elements show the stablecoin option to eligible customers automatically.
3. The customer is redirected to `crypto.stripe.com`, connects a wallet and pays in USDC.
4. Funds settle in your Stripe balance in USD.

## Webhooks

Listen for `checkout.session.completed`, `payment_intent.succeeded` and `invoice.paid` to fulfil orders; verify signatures with the endpoint secret.

## Gotchas

- Stablecoin acceptance requires Stripe approval and an eligible account location.
- Settlement is in USD to your Stripe balance; Stripe does not pay out in crypto on the merchant's chosen chain.
- Use test mode keys and test cards before going live.
