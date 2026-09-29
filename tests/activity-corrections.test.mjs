import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import test from "node:test";

const contract = JSON.parse(readFileSync(new URL("../contract/tools.json", import.meta.url), "utf8"));
const activity = contract.tools.find(tool => tool.name === "list_activity");
const fixture = JSON.parse(readFileSync(new URL("./fixtures/activity-corrections.json", import.meta.url), "utf8"));
const item = activity.outputSchema.properties.data.properties.items.items;

// Validate the JSON Schema forms used by the published activity contract without
// adding a runtime dependency to the public contract package.
function accepts(schema, value) {
  if (schema.anyOf) return schema.anyOf.some(branch => accepts(branch, value));
  if (schema.enum && !schema.enum.includes(value)) return false;
  if (schema.type === "null") return value === null;
  if (schema.type === "object") {
    if (!value || typeof value !== "object" || Array.isArray(value)) return false;
    if ((schema.required ?? []).some(key => !(key in value))) return false;
    if (schema.additionalProperties === false && Object.keys(value).some(key => !(key in schema.properties))) return false;
    return Object.entries(schema.properties).every(([key, child]) => !(key in value) || accepts(child, value[key]));
  }
  if (schema.type === "array") return Array.isArray(value) && value.every(entry => accepts(schema.items, entry));
  if (schema.type === "integer") return Number.isInteger(value) && (schema.minimum == null || value >= schema.minimum) && (schema.maximum == null || value <= schema.maximum);
  if (schema.type === "number") return typeof value === "number" && Number.isFinite(value);
  return typeof value === schema.type;
}

test("legacy activity and optional correction provenance satisfy the strict output contract", () => {
  assert.equal(accepts(activity.outputSchema, fixture), true);
  assert.deepEqual(item.required, ["id", "date", "type", "assetId", "amount", "currency", "quantity", "source"]);
  assert.equal(item.required.includes("correction"), false);
  assert.equal(accepts(item, fixture.data.items[0]), true);
  assert.equal(activity.readOnly, true);
  assert.equal(activity.scope, "activity:read");
});

test("effective cash direction preserves the original and provider resolution does not reverse it twice", () => {
  const [, corrected, resolved] = fixture.data.items;
  assert.equal(corrected.type, "deposit");
  assert.equal(corrected.amount, -corrected.correction.providerAmount);
  assert.equal(corrected.correction.providerSubtype, "withdrawal");
  assert.equal(resolved.amount, resolved.correction.providerAmount);
  assert.equal(resolved.correction.correctionStatus, "provider_resolved");
});

test("private connection identifiers and undocumented provenance fields are rejected", () => {
  const corrected = fixture.data.items[1];
  assert.equal(accepts(item, { ...corrected, plaidItemId: "synthetic-private-item" }), false);
  assert.equal(accepts(item, { ...corrected, correction: { ...corrected.correction, sourceFingerprint: "synthetic-private-fingerprint" } }), false);
  assert.equal(accepts(item, { ...corrected, correction: { ...corrected.correction, correctionStatus: "unknown" } }), false);
});
