# Fillfolio portfolio MCP

Public contract and connection docs for Fillfolio's hosted, read-only [Model Context Protocol](https://modelcontextprotocol.io) server.

The live endpoint is `https://fillfolio.com/api/mcp`.

## Connect

Use Streamable HTTP against the hosted resource. Tokens belong in the `Authorization: Bearer` header only. Query-string tokens are rejected.

| Surface | URL |
| --- | --- |
| MCP | `https://fillfolio.com/api/mcp` |
| Product docs | `https://fillfolio.com/mcp` |
| Server card | `https://fillfolio.com/.well-known/mcp.json` |
| OAuth protected resource | `https://fillfolio.com/.well-known/oauth-protected-resource/api/mcp` |

Access requires a paid Fillfolio account and an approved MCP client. OAuth uses PKCE. The MCP resource remains `https://fillfolio.com/api/mcp`.

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

Revoke access from Fillfolio Settings. A revoked grant is not restored by token refresh.

## Tools

All tools are read-only. They never trade, write holdings, refresh providers, or return credentials, account numbers, or raw provider payloads.

| Tool | Scope | Purpose |
| --- | --- | --- |
| `get_portfolio_summary` | `portfolio:read` | Net worth, holdings value, cash, debt, and return availability |
| `list_portfolios` | `portfolio:read` | Portfolios for the authenticated user |
| `list_holdings` | `holdings:read` | Normalized holdings with cost-basis availability |
| `list_cash_and_liabilities` | `accounts:read` | Cash and liabilities without account numbers |
| `list_activity` | `activity:read` | Normalized activity in a bounded date range |
| `get_asset` | `holdings:read` | One canonical asset and its holdings |

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
