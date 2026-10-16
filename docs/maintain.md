# Maintain this documentation snapshot

GitHub holds the canonical source and support channels. Documentation copies show a dated snapshot. This publication has no synchronization job or recurring posting schedule.

## Build offline after dependency installation

Use Python 3.10 or later and a local virtual environment:

```sh
python3 -m venv .venv-docs
.venv-docs/bin/python -m pip install -r requirements-docs.txt
.venv-docs/bin/python scripts/build_docs.py
.venv-docs/bin/python -m mkdocs build --strict
.venv-docs/bin/python scripts/check_docs.py
```

The generator reads the captured public contract and skill catalog from this repository. It requires no account, credentials, network fetch, or live financial data. `check_docs.py` checks the generated contract/catalog references, fixture arithmetic, canonical tags, and local site links.

To update the snapshot, review both current public repositories, refresh the three files in `docs/sources/` using the instructions in [snapshot-source-update.md](sources/snapshot-source-update.md), change the date and source references in the authored pages, rebuild, and verify. Keep release archive links pinned to the release you checked. A new source snapshot does not require a new skills release.

## Manual publication routes

- **GitHub Pages:** copy the generated `site/` contents to a dedicated `gh-pages` branch, include `.nojekyll`, and configure Pages to serve that branch's root. No scheduled workflow is needed.
- **Cloudflare Pages:** use Direct Upload with the generated `site/` directory or its ZIP. Use a free provider subdomain. Do not connect GitHub or enable build hooks.
- **GitLab Pages:** use the existing public MCP copy and a dedicated deployment branch. Upload the validated static-site ZIP and use `publication/gitlab-pages.yml` as `.gitlab-ci.yml` on `codex/docs-pages`. The pipeline extracts that ZIP into `public/`. It permits only a manually started web pipeline; repository pushes cannot start it. Run the manual pipeline on the deployment branch without changing imported source branches.
- **Read the Docs Community:** import the public repository URL, select the documentation source branch, and use `.readthedocs.yaml`. Disable webhooks and automatic build triggers; start an initial build by hand. Keep only this repository's MIT code/skill documentation in that project. Stop if the platform requires a paid commercial plan.
- **Mintlify Starter:** import the prepared Markdown/MDX pages through the web editor. Keep Git sync, AI features, paid trials, and billing setup off. Use the generated navigation from the manual publication bundle.
- **GitBook Free:** import the distinct quickstart Markdown ZIP. Use ordinary Free, with Git sync and AI rewriting off.

Review the actual free-plan status before publishing. Skip a route that asks for payment, a trial, or card setup. Set the preferred canonical URL to `https://fillfolio.github.io/portfolio-mcp/` where the host supports it. Keep the snapshot date and GitHub source links on each copy.

## Announcements

The [tutorial](tutorial.md) is the original article. A manual Hashnode cross-post should retain its canonical URL. Publish one GitHub Announcements discussion for both repositories. Use GitHub issues and contributions rather than new help desks on the mirror hosts.

No financial operations, client registrations, or production authentication changes belong in this documentation rollout.
