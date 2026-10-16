# Refresh captured public inputs

This source snapshot uses public data only. It does not read the private Fillfolio repository or a signed-in account.

1. Clone the current public `fillfolio/portfolio-mcp` and `fillfolio/portfolio-mcp-skills` repositories into fresh directories. Record both exact commit IDs.
2. Copy the reviewed MCP `contract/tools.json` into `docs/sources/tool-contract.json` and the reviewed skill `catalog.json` into `docs/sources/skills-catalog.json`.
3. Keep `contract/tools.json` in the documentation repository consistent with the captured tool contract. Review schema changes before generating references.
4. Inspect the selected public GitHub skills release. Record exact asset names, URLs, SHA-256 hashes, and the dereferenced release tag commit in `snapshot.json`. Verify downloaded existing archives against those hashes. Copy the release's `SHA256SUMS` as `skills-SHA256SUMS.txt` without editing it.
5. Update the snapshot date, source commits, input hashes, authored compatibility notes, and manual publication text. Keep registration evidence distinct from live host acceptance.
6. Run the offline generator, strict MkDocs build, and documentation checks. Inspect the site at desktop and mobile widths before publication.

The public MCP contract, authored compatibility notes, and current source guides remain authoritative. Do not infer new client support from a successful documentation build.
