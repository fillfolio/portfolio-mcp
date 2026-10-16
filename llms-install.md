# Connect an AI client to Fillfolio

Reviewed October 16, 2026. Use this guide with the [public contract](README.md) and your host's current MCP documentation. Installing skill instructions does not connect an account.

## Before connecting

1. Use an eligible paid Fillfolio account. Spending and budgets require active ULTRA/HYPER eligibility, bank-spending consent and independent per-client permissions.
2. Configure Streamable HTTP at `https://fillfolio.com/api/mcp`.
3. Let the host discover `https://fillfolio.com/.well-known/oauth-protected-resource/api/mcp` and the advertised authorization server. Request `mcp:read`, use PKCE `S256` and bind authorization to resource `https://fillfolio.com/api/mcp`.
4. Use an accepted registered client identity and callback. Fillfolio supports specific CIMD registrations and disables Dynamic Client Registration. Arbitrary metadata URLs and callbacks fail. Native hosts should retain their own accepted identity.
5. Complete host-managed browser sign-in and read consent. Keep passwords, codes and tokens out of chat and configuration files.

Fillfolio has registered identities for ChatGPT, Codex, Claude web and Claude Code. Existing ChatGPT Work desktop and Codex setups passed live acceptance before this guide; this change adds no new host acceptance result. Claude registrations do not establish a successful live connection. Cursor, VS Code, Cline and other hosts require an accepted client registration and callback before compatibility can be claimed. [MCP authorization specification](https://modelcontextprotocol.io/specification/2025-11-25/basic/authorization)

## Codex

If your setup does not already expose Fillfolio, add this entry to `~/.codex/config.toml`:

```toml
[mcp_servers.fillfolio]
url = "https://fillfolio.com/api/mcp"
```

Run `codex mcp login fillfolio` and complete browser consent using Codex's registered native identity and callback behavior. Do not replace it with a legacy client ID. [Official Codex MCP guide](https://learn.chatgpt.com/docs/extend/mcp?surface=cli)

## ChatGPT

Use the plugin or connector installation flow on a supported surface, configure the endpoint where the host requests it, then complete OAuth. Hosted ChatGPT does not read local Codex settings. Uploading a skill as an ordinary chat attachment does not install tools. Fillfolio's native plugin 0.1.1 is In review as of October 16, 2026; public directory availability is pending. Use an existing private or eligible setup while review continues. [OpenAI plugins guide](https://learn.chatgpt.com/docs/plugins)

## Claude Code

Add the endpoint, then open `/mcp` in an interactive Claude Code session to sign in:

```sh
claude mcp add --transport http --scope user fillfolio https://fillfolio.com/api/mcp
```

Use Claude Code's registered published identity with the current endpoint. A separate fixed-client configuration must match its accepted registration and callback; do not invent values. [Official Claude Code MCP guide](https://code.claude.com/docs/en/mcp)

## Claude chat

Add `https://fillfolio.com/api/mcp` through the custom-connector flow. Use Claude's published identity when it matches Fillfolio's accepted registration. Automatic registration cannot succeed with Fillfolio's disabled DCR. An own-client configuration needs an existing accepted public client ID and callback. Organization policy may require an owner to add the connector. This guide makes no new live-acceptance claim for Claude. [Official custom-connector guide](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp)

## Cursor

The [Cursor example](examples/cursor-mcp.json) is a configuration template, conditional on an accepted client registration for the selected Cursor surface. Replace `<REGISTERED_PUBLIC_CLIENT_ID>` with that registration's public client ID before use. Desktop and Cloud/Agents callbacks differ, so remote MCP support alone does not prove compatibility. [Official Cursor MCP guide](https://cursor.com/docs/mcp)

## Claude Desktop and bridges

Use your desktop version's documented remote-connector UI and an accepted client registration. Claude Desktop does not use the Claude Code configuration file. This repository omits its earlier unverified `mcp-remote` bridge example; installing a bridge does not supply an accepted client identity or callback. [Official Claude connector guide](https://support.claude.com/en/articles/11175166-get-started-with-custom-connectors-using-remote-mcp)

## Other MCP hosts

Confirm the host's accepted public client identity, exact callback and support for resource binding, PKCE `S256` and `mcp:read`. The legacy public Clerk ID `HfY4RTp08YeBNRYm` belongs to existing legacy configurations; it is not a universal ID for new native hosts. OIDC account sign-in scopes do not replace current MCP authorization. No new client registration or production authentication change is part of this repository release.

## Add optional workflow skills

Choose from [fillfolio/portfolio-mcp-skills](https://github.com/fillfolio/portfolio-mcp-skills). That MIT library supplies 15 instruction-only workflows with [client-specific installation paths and ZIP guidance](https://github.com/fillfolio/portfolio-mcp-skills/blob/main/docs/client-setup.md). Install only the workflows you need through your host's supported skill mechanism, then connect Fillfolio separately.

After connecting, ask **“Show my Fillfolio portfolio summary with its reporting currency and data limits.”** A host that renders MCP Apps can call `open_fillfolio` with `{}` to launch the dashboard. Otherwise use the financial read tools. Opening a dashboard view shares its financial data with the chat even when amounts are hidden.

Revoke access in Fillfolio Settings. `401` needs host refresh/reconnection; `403` can mean a disabled read permission or ineligible plan and needs resolution in Fillfolio. Respect rate-limit and service-error responses. Do not interpret a failed read as zero balances or zero spending.
