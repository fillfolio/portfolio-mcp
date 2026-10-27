# Security, access, and sharing

## Read-only access

The MCP tools read records stored in Fillfolio. They cannot place trades, move money, edit holdings or budgets, import data, refresh providers, or fetch live quotes. Make edits in Fillfolio's own interface.

Only the authenticated user's authorized records belong in a response. A prompt that names another person does not provide access to that person's account.

## Account and permission requirements

The MIT contracts and skills are free public materials. The legacy `https://fillfolio.com/api/mcp` endpoint requires an eligible paid Fillfolio plan and an accepted client. The [Gemini profile](connect.md#choose-a-connection-profile) uses `https://free-mcp.fillfolio.com/mcp` and supports Free accounts with one selected manual portfolio and three active assets. Further categories follow the current plan and consent. Spending and budgets require active ULTRA/HYPER eligibility, bank-spending consent, and independent client grants in Fillfolio Settings:

| Grant | Records |
| --- | --- |
| `spending:read` | Spending summary and bank transactions |
| `budgets:read` | Monthly category limits and actuals |

Enabling one grant does not enable the other. Legacy OAuth uses `mcp:read`; Gemini uses `portfolio:read`. The names above describe internal application permissions. Provider coverage, available history, and account eligibility still apply.

## Financial records shared with your AI host

Your selected AI service receives records returned through its tools. Opening a dashboard view shares that view's displayed financial data with the chat. **Discuss selection** shares the selected rows or category.

**Hide amounts masks the panel only.** Your host still receives the open view's raw values. Masking does not retract earlier chat context.

Manage and revoke future access in Fillfolio Settings. Revocation affects later requests and cannot retract prior chat messages or exports. Review your AI provider's data practices before connecting. [Fillfolio privacy disclosure](https://fillfolio.com/privacy)

## Credentials and local configuration

Keep passwords, one-time codes, and tokens in the host's OAuth flow. Send access tokens in `Authorization: Bearer` headers. Do not put tokens in URLs, prompts, skill files, or public repository configuration.

The static documentation sites do not sign you in, hold tokens, read your financial account, or call financial tools. Downloadable skills contain workflow instructions. Your chosen host handles their model usage.

## Public connection lookup

The [public catalog workflow](skills.md#fillfolio-public-connections) uses `https://fillfolio.com/api/public/connections` through a host with HTTP access. It needs no sign-in and cannot inspect private account connections. A listed provider does not establish regional eligibility or a live account balance.
