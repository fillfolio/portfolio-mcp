# Fillfolio MCP

Read-only [Model Context Protocol](https://modelcontextprotocol.io) (MCP) access to [Fillfolio](https://fillfolio.com), a portfolio net worth tracker for stocks, ETFs, funds, crypto, currency, cash, and liabilities.

Connect Claude, Cursor, ChatGPT, or another approved AI client to a paid Fillfolio account. The client can read portfolio summaries, holdings, cost basis, cash and debt, activity, and exact asset details. It cannot trade, move money, change holdings, or see credentials.

**Product docs:** [fillfolio.com/mcp](https://fillfolio.com/mcp)  
**MCP endpoint:** `https://fillfolio.com/api/mcp`

Fillfolio MCP returns the same normalized portfolio already in your account: brokerage holdings, wallet balances, manual lots, cash, credit-card debt, and net worth. Responses include freshness and unavailable FX-rate states. Provider APIs are not called from an MCP request. Revoke access in Fillfolio Settings. Tokens are never displayed.

Access uses OAuth/OIDC with PKCE and the `mcp:read` scope. A paid Fillfolio plan is required.

## Connect

Use Streamable HTTP. Put tokens in the `Authorization: Bearer` header only. Query-string tokens are rejected.

| Surface | URL |
| --- | --- |
| Product docs | [https://fillfolio.com/mcp](https://fillfolio.com/mcp) |
| MCP | `https://fillfolio.com/api/mcp` |
| Server card | `https://fillfolio.com/.well-known/mcp.json` |
| OAuth protected resource | `https://fillfolio.com/.well-known/oauth-protected-resource/api/mcp` |

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
