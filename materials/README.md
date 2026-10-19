# Materials

Materials prepared alongside the study in `../near-geo-paper.docx` (Section 6.11 and Appendix C). None of them is published, and each needs review by the team that owns the corresponding site, repository or package.

## near-agent-skills-plugin

An overlay for github.com/near/agent-skills. Copying these files into the root of that repository makes it a Claude Code and Codex plugin and marketplace without moving any existing file.

- `.claude-plugin/plugin.json` and `.claude-plugin/marketplace.json`, with the plugin source set to `./`
- `.codex-plugin/plugin.json`
- `.mcp.json`, which configures the NEAR Intents, NEAR AI and NEAR documentation MCP servers and the NEAR Agent Market server
- `skills/near-intents/SKILL.md` and `skills/near-ai-cloud/SKILL.md`, with descriptions written in terms of user problems
- `skills/near-agent-market-*`, copies of market.near.ai's skills renamed NEAR Agent Market
- `README.md`, with plugin install instructions, the two skills missing from the original table, and the new skills

`claude plugin validate near-agent-skills-plugin` passes on Claude Code 2.1.170 and 2.1.300, and `claude --plugin-dir near-agent-skills-plugin` loads all 11 skills. The marketplace skills are copies of market.near.ai/skill/* and need to be resynchronised when that site changes.

## near-intents-mcp

A read-only MCP server for the 1Click API with three tools: `list_supported_tokens`, `quote_cross_chain_transfer`, which returns dry quotes only, and `check_transfer_status`. It never creates a deposit address.

```bash
npm install && npm run build
node scripts/smoke.mjs
```

The smoke script lists the tools, looks up USDC on Arbitrum and Solana, requests a dry quote between them, and checks that an unknown asset returns an error. If `ONE_CLICK_API_KEY` is set, the server sends it as the `X-API-Key` header.

## content

Five pages written around user problems, and the Agent Instructions block. Figures come from the live 1Click API, near.ai/pricing.md, market.near.ai and docs.x402.org, and need to be refreshed before publication.
