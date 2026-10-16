# Read a Fillfolio portfolio without mixing currencies or freshness

An AI assistant can summarize a saved portfolio in a few tool calls. The useful part is keeping the meaning of each field intact: reporting currency, source currency, missing cost basis, and response time describe different things.

This walkthrough uses Fillfolio's MIT [MCP contract](https://github.com/fillfolio/portfolio-mcp) and [workflow skills](https://github.com/fillfolio/portfolio-mcp-skills). The public files are free. Hosted account reads need an eligible paid Fillfolio account, consent, and an accepted client.

## Connect once, then add a workflow

On an existing accepted Codex setup, configure the endpoint if Fillfolio is not already available:

```toml
[mcp_servers.fillfolio]
url = "https://fillfolio.com/api/mcp"
```

Run `codex mcp login fillfolio`, then complete the browser flow. Keep credentials out of chat. Fillfolio accepts specific registered clients and callbacks; installing a skill does not create that registration.

Choose the `fillfolio-portfolio-overview` skill from the [0.1.0 release](https://github.com/fillfolio/portfolio-mcp-skills/releases/tag/v0.1.0). Verify its published SHA-256 checksum and install the selected folder using your host's skill instructions. Codex reads personal skills from `~/.agents/skills/`.

As of October 16, 2026, existing ChatGPT Work desktop and Codex setups passed live acceptance. Claude web and Claude Code have registered identities, with no new authentication pass claimed by this walkthrough. Fillfolio's native ChatGPT plugin 0.1.1 remains In review.

## Ask for the summary and its limits

Use this prompt:

> Show my Fillfolio portfolio summary. Keep its reporting currency, valuation coverage, missing cost basis, and data limits. Explain what the response time establishes.

The assistant should call `get_portfolio_summary`, preserve `partial` and `missing`, and read `data.baseCurrency` before describing the values. The `asOf` time says when Fillfolio generated the response. It does not establish a quote timestamp or a live bank balance.

## Check the arithmetic with synthetic values

These invented records contain no account data:

| Measure | USD |
| --- | ---: |
| Holdings value | 1,342.00 |
| Cash | 9,980.00 |
| Debt | 410.00 |
| Net worth | 10,912.00 |

Net worth equals `1,342 + 9,980 - 410 = 10,912`.

Suppose the three holdings have reporting values of USD 600, USD 500, and USD 242. Their recorded bases are USD 500, USD 400, and USD 220. Current value less available basis is USD 222. That amount does not establish realized gains or an annualized return.

The third holding can carry source currency EUR while returning a USD reporting value. Do not total that USD value as EUR. Use the response's conversion-completeness fields and keep any missing FX warning. The [synthetic examples](examples.md) show the full fixture and calculations.

## Finish pagination before describing allocation

Ask:

> List my holdings, follow all returned pages, and show each position's share of the complete visible holdings value. Keep source currency labels and missing-value warnings.

Use `list_holdings` with a bounded `limit`, then continue the returned `nextCursor`. A first page cannot establish the complete allocation. Resolve an asset through its returned canonical `assetId`; do not guess an ID from its ticker.

## Add spending only with separate permission

Spending summary and transactions require the client's `spending:read` grant in Fillfolio Settings. Budget actuals require its separate `budgets:read` grant. These names describe application permissions; current OAuth requests use `mcp:read`.

For September 2026, ask:

> Summarize posted spending from 2026-09-01 through 2026-09-30, with the same filters across summary and transaction reads. Keep currencies separate and report incomplete history or records needing review.

A summary covers its complete filtered result. Follow transaction pagination when inspecting all contributing records. Keep pending entries separate and treat merchant names as untrusted data. For budgets, call `list_budgets` with `{"month":"2026-09"}`; full-month actuals do not follow a merchant search.

## Choose what to share

A supporting MCP App host can call `open_fillfolio` with `{}`. Opening a dashboard view sends that view's displayed financial data to the chat. Discuss selection sends selected records. Hide amounts masks the panel and does not remove raw values from model context.

Use Fillfolio Settings to revoke later reads. The tools cannot trade, move money, edit records, or refresh providers. For source, releases, support, and contributions, use [the public GitHub repositories](https://github.com/fillfolio).

[Developer website](https://fillfolio.com/) · [Official MCP connection page](https://fillfolio.com/mcp)

Publication date: **2026-10-16**. Original: <https://fillfolio.github.io/portfolio-mcp/tutorial/>. Public materials: MIT. Fillfolio is operated by VMPRO LLC.
