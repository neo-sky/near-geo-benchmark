---
name: circle-cctp
description: Move native USDC between blockchains with Circle's Cross-Chain Transfer Protocol (CCTP). Use when someone wants to send USDC from one chain to another (for example Ethereum to Base, Arbitrum or Solana) without wrapped tokens or liquidity pools, rebalance USDC treasury across chains, or build a USDC bridge into an app. USDC is burned on the source chain and minted natively on the destination.
---

# Circle CCTP

CCTP is Circle's permissionless protocol for moving USDC across chains by burn and mint. The source chain burns USDC, Circle's attestation service signs the burn, and the destination chain mints the same amount of native USDC to the recipient. There is no liquidity pool and no wrapped asset.

## Supported domains (CCTP V2)

| Chain | Domain |
|---|---|
| Ethereum | 0 |
| Avalanche | 1 |
| OP Mainnet | 2 |
| Arbitrum | 3 |
| Solana | 5 |
| Base | 6 |
| Polygon PoS | 7 |

## Flow

1. Approve the `TokenMessengerV2` contract to spend the USDC amount on the source chain.
2. Call `depositForBurn` on `TokenMessengerV2`.
3. Poll Circle's attestation API until the message is `complete`.
4. Call `receiveMessage(message, attestation)` on `MessageTransmitterV2` on the destination chain.

```ts
import { pad, zeroHash } from "viem";

const tx = await wallet.writeContract({
  address: TOKEN_MESSENGER_V2,
  abi: tokenMessengerAbi,
  functionName: "depositForBurn",
  args: [
    amount,                       // USDC has 6 decimals
    6,                            // destination domain, Base
    pad(recipient),               // mintRecipient as bytes32
    USDC_ADDRESS,                 // burnToken on the source chain
    zeroHash,                     // destinationCaller, zero lets anyone relay
    maxFee,                       // fee cap for Fast Transfer
    1000,                         // minFinalityThreshold: 1000 fast, 2000 standard
  ],
});

const res = await fetch(
  `https://iris-api.circle.com/v2/messages/0?transactionHash=${tx}`,
);
const { messages } = await res.json();
// when messages[0].status === "complete", submit messages[0].message and
// messages[0].attestation to MessageTransmitterV2.receiveMessage on Base
```

## Transfer speeds

- Fast Transfer (`minFinalityThreshold` 1000): settles in seconds for a small fee, limited by Circle's Fast Transfer allowance.
- Standard Transfer (`minFinalityThreshold` 2000): waits for source-chain finality, no fee beyond gas.

## Gotchas

- Only USDC (and EURC on some chains) can be transferred; other tokens need a swap first.
- The sender pays gas on the source chain and someone must pay gas to call `receiveMessage` on the destination.
- `mintRecipient` is a bytes32; pad EVM addresses and use the token account owner on Solana.
- Use `iris-api-sandbox.circle.com` and testnet contract addresses for testing.
