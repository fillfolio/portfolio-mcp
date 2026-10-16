# Fillfolio MCP: contracts and workflow skills

[Developer website](https://fillfolio.com/) · [Official MCP connection page](https://fillfolio.com/mcp)

Use Fillfolio's public tool reference and 15 workflow skills to ask an AI assistant about stored stocks, ETFs, funds, crypto, cash, spending, and budgets. Supported brokerage, exchange, bank, and blockchain connections provide different records; you can also use records you added to Fillfolio.

These public materials use the **MIT license**. Fillfolio operates the authenticated service at `https://fillfolio.com/api/mcp`. Account reads require an eligible paid Fillfolio plan, an accepted client, and consent. The public connection catalog needs no account. These repositories contain contracts, examples, a request-bounding helper, and skill instructions. You cannot self-host Fillfolio's private service from them.

## Start with your client

1. [Connect an accepted MCP client](connect.md) through its OAuth interface.
2. [Choose a workflow](skills.md), then install its folder or existing release ZIP using your host's skill installer.
3. Ask **“Show my Fillfolio portfolio summary with its reporting currency and data limits.”**

Your host's skill support, OAuth connection, and dashboard rendering are separate capabilities. Installing instructions does not sign you in or provide financial tools.

## Read the public source

| Repository | Contents |
| --- | --- |
| [portfolio-mcp](https://github.com/fillfolio/portfolio-mcp) | Ten-tool contract, connection examples, request-bounding helper, and this documentation |
| [portfolio-mcp-skills](https://github.com/fillfolio/portfolio-mcp-skills) | Fifteen Agent Skills workflows and release ZIPs |

Use the [tool reference](tools.md) for arguments and permissions, [synthetic examples](examples.md) for calculations, and the [tutorial](tutorial.md) for a first portfolio review. Read [security and data sharing](security.md) before connecting.

## Snapshot status

**October 16, 2026:** the existing ChatGPT Work desktop and Codex connections passed live acceptance before this documentation snapshot. Claude web and Claude Code have registered identities; this publication claims no new live authentication pass for those hosts. Other clients need an accepted identity and callback. Fillfolio's separate native ChatGPT plugin **0.1.1 is In review**; public directory approval remains pending.

MCP metadata version **1.0.1**, skill library **0.1.0**, and the native plugin version describe different releases. See [captured source commits and downloads](downloads.md).

Official public snapshot. Latest source, releases, support, and contributions are on [GitHub](https://github.com/fillfolio/portfolio-mcp). Prefer this documentation at <https://fillfolio.github.io/portfolio-mcp/>. Publication date: **2026-10-16**.
