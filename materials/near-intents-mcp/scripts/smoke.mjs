import { Client } from "@modelcontextprotocol/sdk/client/index.js";
import { StdioClientTransport } from "@modelcontextprotocol/sdk/client/stdio.js";

const transport = new StdioClientTransport({ command: "node", args: ["dist/index.js"] });
const client = new Client({ name: "smoke", version: "0.0.0" });
await client.connect(transport);

const call = (name, args) => client.callTool({ name, arguments: args });
const show = (label, res) =>
  console.log(`${label} isError=${Boolean(res.isError)}\n${res.content[0].text.slice(0, 600)}\n`);

const { tools } = await client.listTools();
const summary = tools.map((t) => `${t.name} readOnly=${t.annotations?.readOnlyHint}`);
console.log("tools:", summary.join(", "));

const usdc = async (chain) => {
  const res = await call("list_supported_tokens", { chain, symbol: "USDC" });
  show(`tokens ${chain} USDC:`, res);
  return JSON.parse(res.content[0].text).tokens[0].assetId;
};
const fromAssetId = await usdc("arb");
const toAssetId = await usdc("sol");
const transfer = {
  amount: "10000000",
  recipient: "11111111111111111111111111111112",
  refundTo: "0x0000000000000000000000000000000000000001",
};

show("quote 10 USDC arb -> sol:", await call("quote_cross_chain_transfer", {
  fromAssetId,
  toAssetId,
  ...transfer,
}));
show("quote with a bad asset:", await call("quote_cross_chain_transfer", {
  fromAssetId: "nep141:not-a-real-token.near",
  toAssetId,
  ...transfer,
}));

await client.close();
