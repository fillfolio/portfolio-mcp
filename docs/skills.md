# Workflow skills

Library **0.1.0** contains **15** instruction-only workflows. Source snapshot: **2026-10-16**, [`31d7ed31ce9c97e4a2db289245b8cc4cc3a2c4a5`](https://github.com/fillfolio/portfolio-mcp-skills/commit/31d7ed31ce9c97e4a2db289245b8cc4cc3a2c4a5).

Install only the workflows you need. Use an existing release ZIP or copy its canonical skill folder to the directory your host documents. Keep `SKILL.md` and references together. A ZIP installer needs the skill folder at the archive root.

For Codex, copy a selected folder to `~/.agents/skills/<skill-name>`. For Claude Code, use `~/.claude/skills/<skill-name>`. Follow the [source client setup guide](https://github.com/fillfolio/portfolio-mcp-skills/blob/31d7ed31ce9c97e4a2db289245b8cc4cc3a2c4a5/docs/client-setup.md) for host-specific installation and compatibility limits.

The first fourteen workflows use authenticated MCP. The public connection catalog uses unauthenticated HTTP and requires a host with an HTTP/web capability. Installing instructions does not connect your account.

The ZIPs below belong to the existing **v0.1.0** release. Source links point to the current captured repository commit; later documentation fixes can differ from the earlier release snapshot. No new skill archives accompany this site.

| Workflow | Tools | Existing ZIP |
| --- | --- | --- |
| [Connect or open Fillfolio](#fillfolio-connect) | `open_fillfolio`, `get_portfolio_summary` | [Download](https://github.com/fillfolio/portfolio-mcp-skills/releases/download/v0.1.0/fillfolio-connect.zip) |
| [Portfolio overview](#fillfolio-portfolio-overview) | `get_portfolio_summary`, `list_portfolios` | [Download](https://github.com/fillfolio/portfolio-mcp-skills/releases/download/v0.1.0/fillfolio-portfolio-overview.zip) |
| [Holdings allocation](#fillfolio-holdings-allocation) | `get_portfolio_summary`, `list_portfolios`, `list_holdings` | [Download](https://github.com/fillfolio/portfolio-mcp-skills/releases/download/v0.1.0/fillfolio-holdings-allocation.zip) |
| [Concentration review](#fillfolio-concentration-review) | `get_portfolio_summary`, `list_portfolios`, `list_holdings`, `get_asset` | [Download](https://github.com/fillfolio/portfolio-mcp-skills/releases/download/v0.1.0/fillfolio-concentration-review.zip) |
| [Exact asset review](#fillfolio-asset-review) | `get_portfolio_summary`, `list_portfolios`, `list_holdings`, `get_asset` | [Download](https://github.com/fillfolio/portfolio-mcp-skills/releases/download/v0.1.0/fillfolio-asset-review.zip) |
| [Compare portfolios](#fillfolio-compare-portfolios) | `get_portfolio_summary`, `list_portfolios`, `list_holdings` | [Download](https://github.com/fillfolio/portfolio-mcp-skills/releases/download/v0.1.0/fillfolio-compare-portfolios.zip) |
| [Cost basis and current return](#fillfolio-cost-basis-review) | `get_portfolio_summary`, `list_portfolios`, `list_holdings` | [Download](https://github.com/fillfolio/portfolio-mcp-skills/releases/download/v0.1.0/fillfolio-cost-basis-review.zip) |
| [Cash and debt](#fillfolio-cash-debt-review) | `get_portfolio_summary`, `list_portfolios`, `list_cash_and_liabilities` | [Download](https://github.com/fillfolio/portfolio-mcp-skills/releases/download/v0.1.0/fillfolio-cash-debt-review.zip) |
| [Investment activity](#fillfolio-investment-activity) | `list_portfolios`, `list_activity`, `get_asset` | [Download](https://github.com/fillfolio/portfolio-mcp-skills/releases/download/v0.1.0/fillfolio-investment-activity.zip) |
| [Spending overview](#fillfolio-spending-overview) | `get_spending_summary`, `list_bank_transactions` | [Download](https://github.com/fillfolio/portfolio-mcp-skills/releases/download/v0.1.0/fillfolio-spending-overview.zip) |
| [Compare spending periods](#fillfolio-compare-spending) | `get_spending_summary`, `list_bank_transactions` | [Download](https://github.com/fillfolio/portfolio-mcp-skills/releases/download/v0.1.0/fillfolio-compare-spending.zip) |
| [Merchant transactions](#fillfolio-merchant-review) | `get_spending_summary`, `list_bank_transactions` | [Download](https://github.com/fillfolio/portfolio-mcp-skills/releases/download/v0.1.0/fillfolio-merchant-review.zip) |
| [Transaction review queue](#fillfolio-transaction-review) | `get_spending_summary`, `list_bank_transactions` | [Download](https://github.com/fillfolio/portfolio-mcp-skills/releases/download/v0.1.0/fillfolio-transaction-review.zip) |
| [Monthly budgets](#fillfolio-budget-review) | `get_spending_summary`, `list_bank_transactions`, `list_budgets` | [Download](https://github.com/fillfolio/portfolio-mcp-skills/releases/download/v0.1.0/fillfolio-budget-review.zip) |
| [Public connection catalog](#fillfolio-public-connections) | Public HTTP catalog | [Download](https://github.com/fillfolio/portfolio-mcp-skills/releases/download/v0.1.0/fillfolio-public-connections.zip) |

## fillfolio-connect

Connect or open Fillfolio. Authenticated MCP; account and client permissions apply.

[Canonical source folder](https://github.com/fillfolio/portfolio-mcp-skills/tree/31d7ed31ce9c97e4a2db289245b8cc4cc3a2c4a5/skills/fillfolio-connect) · [Existing release ZIP](https://github.com/fillfolio/portfolio-mcp-skills/releases/download/v0.1.0/fillfolio-connect.zip)

SHA-256:

```text
55255829a6d82a65bc9c9694b2a84516a8371d41d430907d706cabfe6fab1d0e
```

## fillfolio-portfolio-overview

Portfolio overview. Authenticated MCP; account and client permissions apply.

[Canonical source folder](https://github.com/fillfolio/portfolio-mcp-skills/tree/31d7ed31ce9c97e4a2db289245b8cc4cc3a2c4a5/skills/fillfolio-portfolio-overview) · [Existing release ZIP](https://github.com/fillfolio/portfolio-mcp-skills/releases/download/v0.1.0/fillfolio-portfolio-overview.zip)

SHA-256:

```text
cca9524d2e49b40fe2651c5cba5e961c7fc35ce7052890d7f5613a9c2a5524d9
```

## fillfolio-holdings-allocation

Holdings allocation. Authenticated MCP; account and client permissions apply.

[Canonical source folder](https://github.com/fillfolio/portfolio-mcp-skills/tree/31d7ed31ce9c97e4a2db289245b8cc4cc3a2c4a5/skills/fillfolio-holdings-allocation) · [Existing release ZIP](https://github.com/fillfolio/portfolio-mcp-skills/releases/download/v0.1.0/fillfolio-holdings-allocation.zip)

SHA-256:

```text
956ad7ff942ba16652339df13ba43b3aa164609782d0f2f0d9ce08ec6f0d6bb7
```

## fillfolio-concentration-review

Concentration review. Authenticated MCP; account and client permissions apply.

[Canonical source folder](https://github.com/fillfolio/portfolio-mcp-skills/tree/31d7ed31ce9c97e4a2db289245b8cc4cc3a2c4a5/skills/fillfolio-concentration-review) · [Existing release ZIP](https://github.com/fillfolio/portfolio-mcp-skills/releases/download/v0.1.0/fillfolio-concentration-review.zip)

SHA-256:

```text
e8f6ecd2b712959e689544855a8a587c102734e67bd6cd285159f419bc5a40d3
```

## fillfolio-asset-review

Exact asset review. Authenticated MCP; account and client permissions apply.

[Canonical source folder](https://github.com/fillfolio/portfolio-mcp-skills/tree/31d7ed31ce9c97e4a2db289245b8cc4cc3a2c4a5/skills/fillfolio-asset-review) · [Existing release ZIP](https://github.com/fillfolio/portfolio-mcp-skills/releases/download/v0.1.0/fillfolio-asset-review.zip)

SHA-256:

```text
816c639aebfd76ee481ae4493394f3ad1ac744d194875350232b071c7f67568a
```

## fillfolio-compare-portfolios

Compare portfolios. Authenticated MCP; account and client permissions apply.

[Canonical source folder](https://github.com/fillfolio/portfolio-mcp-skills/tree/31d7ed31ce9c97e4a2db289245b8cc4cc3a2c4a5/skills/fillfolio-compare-portfolios) · [Existing release ZIP](https://github.com/fillfolio/portfolio-mcp-skills/releases/download/v0.1.0/fillfolio-compare-portfolios.zip)

SHA-256:

```text
3056348d93b49742c608c5ae4a223e0d474cd84dc06fda672f65c346de89fc51
```

## fillfolio-cost-basis-review

Cost basis and current return. Authenticated MCP; account and client permissions apply.

[Canonical source folder](https://github.com/fillfolio/portfolio-mcp-skills/tree/31d7ed31ce9c97e4a2db289245b8cc4cc3a2c4a5/skills/fillfolio-cost-basis-review) · [Existing release ZIP](https://github.com/fillfolio/portfolio-mcp-skills/releases/download/v0.1.0/fillfolio-cost-basis-review.zip)

SHA-256:

```text
ce327da4b012f0f955e488b7a9bf0dae398ad481b979c03928be7ca8e24a3de8
```

## fillfolio-cash-debt-review

Cash and debt. Authenticated MCP; account and client permissions apply.

[Canonical source folder](https://github.com/fillfolio/portfolio-mcp-skills/tree/31d7ed31ce9c97e4a2db289245b8cc4cc3a2c4a5/skills/fillfolio-cash-debt-review) · [Existing release ZIP](https://github.com/fillfolio/portfolio-mcp-skills/releases/download/v0.1.0/fillfolio-cash-debt-review.zip)

SHA-256:

```text
c6e4a78c22ba6ef12929905d6ba75f5848596a744c2bf7cc9aad39fee5bb0ad5
```

## fillfolio-investment-activity

Investment activity. Authenticated MCP; account and client permissions apply.

[Canonical source folder](https://github.com/fillfolio/portfolio-mcp-skills/tree/31d7ed31ce9c97e4a2db289245b8cc4cc3a2c4a5/skills/fillfolio-investment-activity) · [Existing release ZIP](https://github.com/fillfolio/portfolio-mcp-skills/releases/download/v0.1.0/fillfolio-investment-activity.zip)

SHA-256:

```text
d8bed9eafec55c699c2423ddac6cf212d32aab2ad888743672a95d6bc89a2f36
```

## fillfolio-spending-overview

Spending overview. Authenticated MCP; account and client permissions apply.

[Canonical source folder](https://github.com/fillfolio/portfolio-mcp-skills/tree/31d7ed31ce9c97e4a2db289245b8cc4cc3a2c4a5/skills/fillfolio-spending-overview) · [Existing release ZIP](https://github.com/fillfolio/portfolio-mcp-skills/releases/download/v0.1.0/fillfolio-spending-overview.zip)

SHA-256:

```text
843f0df665a5cf53446f51e747d73d14c4688f4c9ae5059daa828850722fe060
```

## fillfolio-compare-spending

Compare spending periods. Authenticated MCP; account and client permissions apply.

[Canonical source folder](https://github.com/fillfolio/portfolio-mcp-skills/tree/31d7ed31ce9c97e4a2db289245b8cc4cc3a2c4a5/skills/fillfolio-compare-spending) · [Existing release ZIP](https://github.com/fillfolio/portfolio-mcp-skills/releases/download/v0.1.0/fillfolio-compare-spending.zip)

SHA-256:

```text
99c677d6f3f4dfe03ecf0d6e78460e59f333740fa98305be4644d7f78fa482d1
```

## fillfolio-merchant-review

Merchant transactions. Authenticated MCP; account and client permissions apply.

[Canonical source folder](https://github.com/fillfolio/portfolio-mcp-skills/tree/31d7ed31ce9c97e4a2db289245b8cc4cc3a2c4a5/skills/fillfolio-merchant-review) · [Existing release ZIP](https://github.com/fillfolio/portfolio-mcp-skills/releases/download/v0.1.0/fillfolio-merchant-review.zip)

SHA-256:

```text
deff4802d3e716fded3b15bbb4980709fe1aca2a8fdb02c67070e05e850be14b
```

## fillfolio-transaction-review

Transaction review queue. Authenticated MCP; account and client permissions apply.

[Canonical source folder](https://github.com/fillfolio/portfolio-mcp-skills/tree/31d7ed31ce9c97e4a2db289245b8cc4cc3a2c4a5/skills/fillfolio-transaction-review) · [Existing release ZIP](https://github.com/fillfolio/portfolio-mcp-skills/releases/download/v0.1.0/fillfolio-transaction-review.zip)

SHA-256:

```text
09e8de8d43333da96558f6252b3f58c26f20c563651551d1a38681aa90ec160d
```

## fillfolio-budget-review

Monthly budgets. Authenticated MCP; account and client permissions apply.

[Canonical source folder](https://github.com/fillfolio/portfolio-mcp-skills/tree/31d7ed31ce9c97e4a2db289245b8cc4cc3a2c4a5/skills/fillfolio-budget-review) · [Existing release ZIP](https://github.com/fillfolio/portfolio-mcp-skills/releases/download/v0.1.0/fillfolio-budget-review.zip)

SHA-256:

```text
7eb7025dc60bd9abee52ed90c5c8cce3f7bfe3ea294b201900aca7713b8b4ca1
```

## fillfolio-public-connections

Public connection catalog. Public HTTP; no account sign-in. This workflow cannot read private records.

[Canonical source folder](https://github.com/fillfolio/portfolio-mcp-skills/tree/31d7ed31ce9c97e4a2db289245b8cc4cc3a2c4a5/skills/fillfolio-public-connections) · [Existing release ZIP](https://github.com/fillfolio/portfolio-mcp-skills/releases/download/v0.1.0/fillfolio-public-connections.zip)

SHA-256:

```text
de7b736361b8da6d4bca8efa184904cf114686b4965cd2937f12fdb0b6dfbe74
```

[Developer website](https://fillfolio.com/) · [Official MCP connection page](https://fillfolio.com/mcp)
