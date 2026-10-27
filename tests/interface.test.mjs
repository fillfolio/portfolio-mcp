import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

const readJson = relative => JSON.parse(readFileSync(new URL(relative, import.meta.url), "utf8"));
const contract = readJson("../contract/tools.json");
const tools = new Map(contract.tools.map(tool => [tool.name, tool]));
const launch = tools.get("open_fillfolio");

function acceptsObject(schema, value) {
  if (!value || typeof value !== "object" || Array.isArray(value)) return false;
  if (schema.additionalProperties === false && Object.keys(value).some(key => !(key in schema.properties))) return false;
  return (schema.required ?? []).every(key => key in value);
}

test("dashboard launch accepts no arguments and cannot take a user or financial mutation", () => {
  assert.equal(tools.size, 10);
  assert.equal(acceptsObject(launch.input, {}), true);
  for (const input of [null, [], { userId: "another-user" }, { portfolio: "synthetic" }, { refresh: true }, { amount: 1 }]) {
    assert.equal(acceptsObject(launch.input, input), false);
  }
  assert.equal(launch.scope, "portfolio:read");
  assert.equal("outputSchema" in launch, false);
  assert.equal("data" in launch, false);
});

test("launcher resolves to an inline app resource with bounded origins and preserved cached versions", () => {
  const uri = launch._meta.ui.resourceUri;
  const resource = contract.resources.find(item => item.uri === uri);
  assert.ok(resource);
  assert.equal(resource.mimeType, "text/html;profile=mcp-app");
  assert.deepEqual(resource._meta.ui.csp, { connectDomains: [], resourceDomains: [], frameDomains: [] });
  assert.equal(resource._meta.ui.domain, "https://chatgpt.fillfolio.com");
  assert.deepEqual(resource._meta["openai/widgetCSP"].redirect_domains, ["https://fillfolio.com"]);
  for (const version of [1, 2, 3]) assert.ok(contract.resources.some(item => item.uri === `ui://fillfolio/dashboard-v${version}.html`));
  assert.deepEqual(launch._meta["openai/ui"].entrypoints, [{ type: "global" }, { type: "thread" }]);
});

test("OAuth metadata does not turn supplemental permissions into default authorization scopes", () => {
  assert.deepEqual(contract.authentication.oauthScopes, ["mcp:read"]);
  assert.equal(contract.authentication.dynamicClientRegistration, false);
  assert.deepEqual(contract.supplementalPermissions, ["spending:read", "budgets:read"]);
  assert.equal(tools.get("get_spending_summary").scope, "spending:read");
  assert.equal(tools.get("list_bank_transactions").scope, "spending:read");
  assert.equal(tools.get("list_budgets").scope, "budgets:read");
  for (const tool of tools.values()) {
    assert.equal(tool.readOnly, true);
    assert.deepEqual(tool._meta.securitySchemes, [{ type: "oauth2", scopes: ["mcp:read"] }]);
    assert.deepEqual(tool.annotations, { readOnlyHint: true, destructiveHint: false, openWorldHint: false, idempotentHint: true });
  }
});

test("registry metadata describes only the hosted remote service and matches the package release", () => {
  const server = readJson("../server.json");
  const pkg = readJson("../package.json");
  assert.equal(server.version, pkg.version);
  assert.equal(server.name, "com.fillfolio/mcp");
  assert.ok(server.description.length <= 100);
  assert.deepEqual(server.remotes, [{ type: "streamable-http", url: contract.resource }]);
  assert.equal("packages" in server, false);
});


test("Gemini settings preserve the separate Free/paid resource and exact registered identity", () => {
  const server=readJson("../examples/gemini-settings.json").mcpServers.fillfolio;
  assert.equal(server.httpUrl,"https://free-mcp.fillfolio.com/mcp");
  assert.deepEqual(server.oauth,{enabled:true,clientId:"fillfolio-free-gemini-cli",scopes:["portfolio:read"],redirectUri:"http://localhost:7777/oauth/callback"});
  assert.equal(contract.resource,"https://fillfolio.com/api/mcp");
  assert.deepEqual(contract.authentication.oauthScopes,["mcp:read"]);
});
