# Downloads and captured sources

Snapshot date: **2026-10-16**. Prefer the documentation at <https://fillfolio.github.io/portfolio-mcp/>.

## Public source commits

| Repository | Captured commit |
| --- | --- |
| [portfolio-mcp](https://github.com/fillfolio/portfolio-mcp) | [`86f8b914c33239fbb38ae442ae27f3ca2c490ebc`](https://github.com/fillfolio/portfolio-mcp/commit/86f8b914c33239fbb38ae442ae27f3ca2c490ebc) |
| [portfolio-mcp-skills](https://github.com/fillfolio/portfolio-mcp-skills) | [`31d7ed31ce9c97e4a2db289245b8cc4cc3a2c4a5`](https://github.com/fillfolio/portfolio-mcp-skills/commit/31d7ed31ce9c97e4a2db289245b8cc4cc3a2c4a5) |

Read the [snapshot metadata](sources/snapshot.json), [tool contract](sources/tool-contract.json), [skills catalog](sources/skills-catalog.json), and [MIT license](sources/MIT-LICENSE.txt). Source repositories remain canonical for current releases, support, and contributions.

## Existing skills release

Release [v0.1.0](https://github.com/fillfolio/portfolio-mcp-skills/releases/tag/v0.1.0) points to commit `f913279652e875c8de6b7d76d20c44189a71327a`. It predates the current captured skills documentation commit. This site links the existing files and does not rebuild or replace that release.

| File | Size in bytes | SHA-256 |
| --- | ---: | --- |
| [portfolio-mcp-skills-v0.1.0.zip](https://github.com/fillfolio/portfolio-mcp-skills/releases/download/v0.1.0/portfolio-mcp-skills-v0.1.0.zip) | 107524 | `444617bcfc2156686a01cfb97ebe49841873264fe230695ea4e40063d12ffd72` |
| [release-manifest.json](https://github.com/fillfolio/portfolio-mcp-skills/releases/download/v0.1.0/release-manifest.json) | 6770 | `d3b8c4df8a5bcfc815ac8bb9d25f9d5728ca09d9729151ca1be299b3d432cd51` |
| [SHA256SUMS](https://github.com/fillfolio/portfolio-mcp-skills/releases/download/v0.1.0/SHA256SUMS) | 1749 | `79cfd9042691b2e1d41d587e383028c3450294ebcc55eda6dc938113025baac7` |

Standalone skill ZIP links and hashes appear in the [workflow catalog](skills.md). The release checksum file uses `skills/<name>.zip` paths; GitHub serves those standalone files by their basename. Match the basename and digest when downloading one file.

Verify a selected download with your operating system's SHA-256 utility. On macOS:

```sh
shasum -a 256 fillfolio-portfolio-overview.zip
```

Compare the result with the exact hash listed for that file. A checksum verifies file identity; it does not establish host OAuth compatibility.

## Machine-readable documentation

[llms.txt](llms.txt) lists the documentation and source links. [llms-full.txt](llms-full.txt) includes the authored pages and generated references. These files provide text for readers and agents; they do not install a connection or guarantee search indexing.

## Support and contributions

Use [portfolio-mcp issues](https://github.com/fillfolio/portfolio-mcp/issues) for contract/docs reports and [portfolio-mcp-skills issues](https://github.com/fillfolio/portfolio-mcp-skills/issues) for workflow reports. Do not post financial records or credentials in a public issue.

Public materials use MIT. Fillfolio operates the hosted service under separate [terms](https://fillfolio.com/terms) and [privacy disclosures](https://fillfolio.com/privacy).
