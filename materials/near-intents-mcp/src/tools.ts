import type { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { z } from "zod";
import type { OneClickClient } from "./oneclick.js";

const MAX_TOKENS = 60;
const READ_ONLY = { readOnlyHint: true, destructiveHint: false, openWorldHint: true } as const;

const assetId = z
  .string()
  .min(3)
  .max(200)
  .regex(/^[A-Za-z0-9_:.-]+$/)
  .describe("assetId from list_supported_tokens, for example nep141:eth.omft.near");
const address = z.string().min(2).max(128);

function reply(value: unknown) {
  return { content: [{ type: "text" as const, text: JSON.stringify(value, null, 2) }] };
}

function run(action: () => Promise<unknown>) {
  return action().then(reply, (err: unknown) => ({
    isError: true,
    content: [{ type: "text" as const, text: err instanceof Error ? err.message : String(err) }],
  }));
}

export function registerTools(server: McpServer, client: OneClickClient) {
  server.registerTool(
    "list_supported_tokens",
    {
      title: "List supported tokens and chains",
      description:
        "List the tokens and blockchains that NEAR Intents can move between chains or accept " +
        "as payment, with the assetId each quote needs. Use it before quoting a cross-chain " +
        "transfer, swap or payment. Filter by chain (for example eth, sol, base, arb, btc, " +
        "near) or symbol.",
      inputSchema: {
        chain: z.string().max(32).optional().describe("Blockchain code, for example sol or base"),
        symbol: z.string().max(32).optional().describe("Token symbol, for example USDC"),
      },
      annotations: READ_ONLY,
    },
    ({ chain, symbol }) =>
      run(() =>
        client.tokens().then((tokens) => {
          const matches = tokens.filter(
            (t) =>
              (!chain || t.blockchain === chain.toLowerCase()) &&
              (!symbol || t.symbol.toUpperCase() === symbol.toUpperCase()),
          );
          return {
            total: matches.length,
            tokens: matches.slice(0, MAX_TOKENS).map((t) => ({
              assetId: t.assetId,
              symbol: t.symbol,
              blockchain: t.blockchain,
              decimals: t.decimals,
              priceUsd: t.price,
            })),
          };
        }),
      ),
  );

  server.registerTool(
    "quote_cross_chain_transfer",
    {
      title: "Preview a cross-chain transfer, swap or payment",
      description:
        "Preview moving or swapping tokens from one blockchain to another, or receiving an exact " +
        "amount as a payment that the payer can send from any supported chain, through the NEAR " +
        "Intents 1Click API. Returns input and output amounts and a time estimate. Preview only: " +
        "it creates no deposit address and sends nothing. Use mode exact_output when the " +
        "recipient must receive an exact amount, such as an invoice or a supplier payment.",
      inputSchema: {
        fromAssetId: assetId,
        toAssetId: assetId,
        amount: z
          .string()
          .regex(/^[0-9]{1,40}$/)
          .describe("Smallest-unit amount: the input for exact_input, the output for exact_output"),
        mode: z.enum(["exact_input", "exact_output"]).default("exact_input"),
        recipient: address.describe("Address that receives the tokens on the destination chain"),
        refundTo: address.describe("Address on the origin chain that receives refunds"),
        slippageBps: z.number().int().min(1).max(5000).default(100),
      },
      annotations: READ_ONLY,
    },
    (args) =>
      run(() =>
        client
          .quote({
            originAsset: args.fromAssetId,
            destinationAsset: args.toAssetId,
            amount: args.amount,
            swapType: args.mode === "exact_output" ? "EXACT_OUTPUT" : "EXACT_INPUT",
            recipient: args.recipient,
            refundTo: args.refundTo,
            slippageBps: args.slippageBps,
          })
          .then((quote) => ({ preview: true, ...quote })),
      ),
  );

  server.registerTool(
    "check_transfer_status",
    {
      title: "Check a transfer or payment status",
      description:
        "Check the status of a NEAR Intents cross-chain transfer or payment by its deposit " +
        "address: PENDING_DEPOSIT, PROCESSING, SUCCESS, INCOMPLETE_DEPOSIT, REFUNDED or FAILED.",
      inputSchema: {
        depositAddress: address.describe("Deposit address returned when the transfer was created"),
        depositMemo: z.string().max(128).optional().describe("Memo, required for Stellar deposits"),
      },
      annotations: READ_ONLY,
    },
    ({ depositAddress, depositMemo }) => run(() => client.status(depositAddress, depositMemo)),
  );
}
