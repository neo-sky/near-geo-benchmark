#!/usr/bin/env node
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { createClient } from "./oneclick.js";
import { registerTools } from "./tools.js";

const server = new McpServer({ name: "near-intents", version: "0.1.0" });
registerTools(server, createClient(process.env.ONE_CLICK_API_KEY));
await server.connect(new StdioServerTransport());
