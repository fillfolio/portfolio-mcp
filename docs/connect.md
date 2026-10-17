# Connect a client

Use **Streamable HTTP** at `https://fillfolio.com/api/mcp`. Your host handles OAuth sign-in, consent, token refresh, and reconnection. Keep passwords, codes, and tokens in that interface.

## Connection requirements

- Use an eligible paid Fillfolio account. Spending and budgets need active ULTRA/HYPER eligibility, bank-spending consent, and independent per-client read permissions.
- Let the host read the [protected-resource metadata](https://fillfolio.com/.well-known/oauth-protected-resource/api/mcp) and [authorization-server metadata](https://fillfolio.com/.well-known/oauth-authorization-server).
- Request OAuth scope `mcp:read`, use PKCE `S256`, and bind authorization to resource `https://fillfolio.com/api/mcp`.
- Use an accepted registered client identity and exact callback. Fillfolio accepts specific Client ID Metadata Documents; it does not offer general-purpose client registration. An arbitrary metadata URL or callback fails.

Keep a native host's accepted identity. The legacy Clerk client ID belongs to existing legacy configurations; it is not a universal client ID for new hosts. Internal permissions such as `spending:read` are application grants, not extra OAuth scopes to request from the current issuer.

## Compatibility at this snapshot

| Host | Status and next step |
| --- | --- |
| ChatGPT Work desktop | Existing setup passed live acceptance. Use the plugin/connector flow available on your supported surface. Native plugin 0.1.1 remains In review. |
| Codex | Existing setup passed live acceptance. Use the remote server entry and browser login below. |
| Claude Code | Registered identity. Use its published identity and accepted callback; this snapshot adds no live acceptance result. |
| Claude web | Registered identity. Use its custom-connector flow with an accepted identity; this snapshot adds no live acceptance result. |
| Gemini CLI | Extension 0.1.1 is in preparation; full live acceptance remains pending. After publication, run `/mcp auth fillfolio` for initial authorization and reauthorization. See the [current Gemini guide](https://github.com/fillfolio/portfolio-mcp-skills/blob/main/docs/gemini-cli.md). |
| Cursor, VS Code, and other hosts | Require an accepted client identity and callback before compatibility can be claimed. Read the conditional examples in the source guide. |

### Codex

If your setup does not already expose Fillfolio, add this to your personal `~/.codex/config.toml`:

```toml
[mcp_servers.fillfolio]
url = "https://fillfolio.com/api/mcp"
```

Then run:

```sh
codex mcp login fillfolio
```

Complete consent using Codex's accepted native identity. Reuse an existing working connection instead of adding a duplicate. [Codex MCP guide](https://learn.chatgpt.com/docs/extend/mcp?surface=cli)

### Claude Code

Add the endpoint, then open `/mcp` in an interactive session to sign in:

```sh
claude mcp add --transport http --scope user fillfolio https://fillfolio.com/api/mcp
```

The command configures the endpoint. Successful OAuth still depends on the registered identity and callback. [Claude Code MCP guide](https://code.claude.com/docs/en/mcp)

### ChatGPT and Claude chat

Use the host's supported plugin or custom-connector installation flow, then complete OAuth. ChatGPT web does not read local Codex settings. An ordinary chat attachment does not install a skill or tool connection. Follow the detailed [client setup guide](https://github.com/fillfolio/portfolio-mcp-skills/blob/31d7ed31ce9c97e4a2db289245b8cc4cc3a2c4a5/docs/client-setup.md) for installation paths and evidence limits.

## Confirm a read

Ask **“Show my Fillfolio portfolio summary with its reporting currency and data limits.”** On a host that renders MCP Apps, `open_fillfolio` with `{}` opens a read-only dashboard. Other accepted hosts can use the nine financial read tools without rendering it.

A `401` needs host refresh or reconnection. Resolve a `403` by checking eligibility and client permissions in Fillfolio Settings. Reconnecting will not enable a disabled read permission. Respect `Retry-After` on `429`; treat temporary service failure as an error.

[Read the full source connection guide](https://github.com/fillfolio/portfolio-mcp/blob/86f8b914c33239fbb38ae442ae27f3ca2c490ebc/llms-install.md).
