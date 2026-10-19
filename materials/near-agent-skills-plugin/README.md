# Agent Skills

AI agent skills for NEAR Protocol blockchain development.

## Skills

| Skill                                                | Library                                                            | Description                                                                                                            |
| ---------------------------------------------------- | ------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------------------------- |
| [near-ai-cloud](skills/near-ai-cloud/) | [NEAR AI Cloud Docs](https://docs.near.ai/cloud/introduction) | Verifiable private AI inference, TEE attestation, NRAS verification, GPU-CPU binding |
| [near-api-js](skills/near-api-js/)                   | [near-api-js](https://github.com/near/near-api-js)                 | JS/TS library for blockchain interaction, transactions, tokens, wallet integration                                     |
| [near-dapp](skills/near-dapp/)                       | -                                                                  | Full-stack frontend development guide. Project setup, wallet integration, React/Next.js patterns, contract interaction |
| [near-intents](skills/near-intents/)                 | [1Click API](https://docs.near-intents.org/)                       | Move tokens across chains and accept payments in any token, without a bridge or an API key to start                    |
| [near-kit](skills/near-kit/)                         | [near-kit](https://github.com/r-near/near-kit)                     | TypeScript SDK with intuitive API, type-safe contracts, sandbox testing                                                |
| [near-smart-contracts](skills/near-smart-contracts/) | -                                                                  | Rust smart contract development, security, state management, cross-contract calls                                      |
| [near-cli-rs](skills/near-cli-rs/)                   | [near-cli-rs](https://github.com/near/near-cli-rs)                 | Commands for accounts, transfers, staking, contract deployment and signing                                             |
| [near-contract-audit](skills/near-contract-audit/)   | -                                                                  | Security audit of NEAR Rust contracts                                                                                  |
| [near-agent-market-buyer](skills/near-agent-market-buyer/) | [NEAR Agent Market](https://market.near.ai)                  | Hire agents on NEAR Agent Market from an MCP client for a person                                                       |
| [near-agent-market-x402-caller](skills/near-agent-market-x402-caller/) | [NEAR Agent Market](https://market.near.ai)      | Call a listed agent over A2A and pay per call with x402, no account needed                                             |
| [near-agent-market-worker](skills/near-agent-market-worker/) | [NEAR Agent Market](https://market.near.ai)                | List an agent, take jobs and get paid on NEAR Agent Market                                                             |

## Install as a plugin

Claude Code installs the skills and NEAR's MCP servers (NEAR Docs, NEAR Intents docs, NEAR AI docs and NEAR Agent Market) in one step:

```bash
/plugin install near --marketplace near/agent-skills
```

On Claude Code before 2.1.275, add the marketplace first:

```bash
/plugin marketplace add near/agent-skills
/plugin install near@near
```

## Install skills only

```bash
pnpm dlx skills add near/agent-skills
yarn dlx skills add near/agent-skills
npx skills add near/agent-skills
bunx skills add near/agent-skills
```

or

```bash
pnpm dlx skills add near/agent-skills --skill <skill-name>
yarn dlx skills add near/agent-skills --skill <skill-name>
npx skills add near/agent-skills --skill <skill-name>
bunx skills add near/agent-skills --skill <skill-name>
```

Replace `<skill-name>` with: `near-ai-cloud`, `near-api-js`, `near-dapp`, `near-intents`, `near-kit`, `near-smart-contracts`, `near-cli-rs`, `near-contract-audit`, `near-agent-market-buyer`, `near-agent-market-x402-caller`, or `near-agent-market-worker`.

## Usage

Skills activate automatically when relevant tasks are detected.

## Structure

- `SKILL.md` - Agent instructions
- `references/` - Documentation guides
- `rules/` - Documentation rules
