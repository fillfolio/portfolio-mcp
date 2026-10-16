# Manual publication

Build with the commands in `docs/maintain.md`. Publish only the generated `site/` files to static hosting. Never upload `.git`, a virtual environment, account configuration, or this workspace's audit outputs.

`gitlab-pages.yml` allows only manual web pipelines on `codex/docs-pages`. Upload the static-site ZIP beside it as named in the template; it extracts that validated artifact into `public/`. `.readthedocs.yaml` builds the committed documentation source; disable webhook and automatic triggers in Read the Docs before publication.

`scripts/package_docs.py --output <directory>` creates static-site, Mintlify manual-content, and distinct GitBook quickstart ZIPs plus an artifact checksum manifest. These are documentation artifacts, not new skills releases.

Use the publication date and input commits in `docs/sources/snapshot.json`. Preserve the existing GitHub skills release ZIPs and their checksum links. Copies must identify GitHub as the source for releases, support, and contributions.
