# Fillfolio MCP

Read-only [Model Context Protocol](https://modelcontextprotocol.io) (MCP) access to [Fillfolio](https://fillfolio.com), a portfolio net worth tracker for stocks, ETFs, funds, crypto, currency, cash, and liabilities.

Connect Claude, Cursor, ChatGPT, or another MCP host to a paid Fillfolio account. The client can read portfolio summaries, holdings, cost basis, cash and debt, activity, and exact asset details. It cannot trade, move money, change holdings, or see credentials.

**Product docs:** [fillfolio.com/mcp](https://fillfolio.com/mcp)  
**MCP endpoint:** `https://fillfolio.com/api/mcp`  
**OAuth client ID:** `HfY4RTp08YeBNRYm`

Fillfolio MCP returns the same normalized portfolio already in your account: brokerage holdings, wallet balances, manual lots, cash, credit-card debt, and net worth. Responses include freshness and unavailable FX-rate states. Provider APIs are not called from an MCP request. Revoke access in Fillfolio Settings. Tokens are never displayed.

## Connect

Use Streamable HTTP. Put tokens in the `Authorization: Bearer` header only. Query-string tokens are rejected.

Paste the Fillfolio MCP OAuth client ID as a public PKCE client and leave the secret blank. Dynamic client registration is off. Do not send ChatGPT or Claude metadata URLs as `client_id`. Request Clerk OIDC scopes (`openid`, `email`, `profile`, `offline_access`). Fillfolio copies `mcp:read` and the tool scopes onto the grant after it accepts the token.

| Surface | URL |
| --- | --- |
| Product docs | [https://fillfolio.com/mcp](https://fillfolio.com/mcp) |
| MCP | `https://fillfolio.com/api/mcp` |
| OAuth client ID | `HfY4RTp08YeBNRYm` |
| Server card | `https://fillfolio.com/.well-known/mcp/server-card.json` |
| Server card alias | `https://fillfolio.com/.well-known/mcp.json` |
| OAuth protected resource | `https://fillfolio.com/.well-known/oauth-protected-resource/api/mcp` |
| Auth notes | [https://fillfolio.com/auth.md](https://fillfolio.com/auth.md) |

Cursor example (`~/.cursor/mcp.json` or project MCP config):

```json
{
  "mcpServers": {
    "fillfolio": {
      "url": "https://fillfolio.com/api/mcp"
    }
  }
}
```

If Cursor asks for an OAuth client ID, use `HfY4RTp08YeBNRYm` and leave the secret blank, then sign in.

Claude Code:

```bash
claude mcp add --transport http --client-id HfY4RTp08YeBNRYm --callback-port 1455 fillfolio https://fillfolio.com/api/mcp
```

Codex (`~/.codex/config.toml`):

```toml
[mcp_servers.fillfolio]
url = "https://fillfolio.com/api/mcp"
```

If Codex asks for an OAuth client ID, use `HfY4RTp08YeBNRYm` and leave the secret blank, then sign in.

ChatGPT and Claude web: add a Streamable HTTP connector at `https://fillfolio.com/api/mcp`, paste the same client ID, leave the secret blank, then sign in with Fillfolio.

Claude Desktop and other local MCP hosts can use a Streamable HTTP bridge such as `mcp-remote`:

```json
{
  "mcpServers": {
    "fillfolio": {
      "command": "npx",
      "args": ["-y", "mcp-remote", "https://fillfolio.com/api/mcp"]
    }
  }
}
```

Use the same OAuth client ID if the bridge asks for one.

## Tools

| Tool | Scope | Purpose |
| --- | --- | --- |
| `get_portfolio_summary` | `portfolio:read` | Net worth, holdings value, cash, debt, and return availability |
| `list_portfolios` | `portfolio:read` | Portfolios for the authenticated user |
| `list_holdings` | `holdings:read` | Stocks, ETFs, funds, crypto, currency, and other holdings with cost-basis availability |
| `list_cash_and_liabilities` | `accounts:read` | Cash and liabilities without account numbers |
| `list_activity` | `activity:read` | Buys, sells, and other activity in a bounded date range |
| `get_asset` | `holdings:read` | One canonical asset and its holdings across portfolios |

Input and output shapes are in [`contract/tools.json`](contract/tools.json).

Every successful tool result is wrapped as:

```json
{
  "asOf": "2026-09-03T12:00:00.000Z",
  "partial": false,
  "missing": [],
  "data": {}
}
```

`partial` and `missing` describe unavailable currency conversion. They are not errors.

Holding `source` values are `manual`, `brokerage`, or `wallet`. Date ranges on `list_activity` cannot exceed 366 days. Pagination uses `cursor` plus `limit` (1 to 100, default 50).

## Transport limits

[`src/transport.ts`](src/transport.ts) is the public request-bounding helper used by the hosted server:

- JSON only, no MCP batches
- 1 MB request body
- 2 MB response body
- bounded object depth and node count

## License

MIT. See [LICENSE](LICENSE).
