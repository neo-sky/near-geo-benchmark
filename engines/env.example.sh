NODE=$HOME/.nvm/versions/node/v24.21.0
ENGINE_HOME=$HOME/.geo-engines
CODEX_DIR=$HOME/.local/lib/codex
CLAUDE_DIR=$ENGINE_HOME/claude
SANDBOXES=$HOME/geo-sandboxes
CLAUDE=claude
CLAUDE_LATEST=$CLAUDE_DIR/node_modules/.bin/claude

openrouter_key() { printenv OPENROUTER_API_KEY; }
claude_token() { printenv CLAUDE_CODE_OAUTH_TOKEN; }
