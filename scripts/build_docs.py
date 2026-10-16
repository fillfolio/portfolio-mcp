#!/usr/bin/env python3
"""Generate static references from captured public inputs. No network/account access."""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
SOURCES = DOCS / 'sources'
CANONICAL = 'https://fillfolio.github.io/portfolio-mcp/'
BRAND_LINKS = '[Developer website](https://fillfolio.com/) · [Official MCP connection page](https://fillfolio.com/mcp)'

def read_json(name):
    return json.loads((SOURCES / name).read_text())

def write(name, content):
    if name.endswith('.md') and BRAND_LINKS not in content:
        content = content.rstrip() + '\n\n' + BRAND_LINKS
    (DOCS / name).write_text(content.strip() + '\n')

def json_block(value):
    return '```json\n' + json.dumps(value, indent=2, ensure_ascii=False) + '\n```\n'

def main():
    metadata = read_json('snapshot.json')
    contract = read_json('tool-contract.json')
    catalog = read_json('skills-catalog.json')
    for filename, key in [('tool-contract.json', 'contractSha256'), ('skills-catalog.json', 'catalogSha256')]:
        digest = hashlib.sha256((SOURCES / filename).read_bytes()).hexdigest()
        if digest != metadata[key]:
            raise SystemExit(f'Captured {filename} differs from snapshot metadata')
    if (ROOT / 'contract/tools.json').read_bytes() != (SOURCES / 'tool-contract.json').read_bytes():
        raise SystemExit('Current and captured public tool contracts differ; review before building')
    tool_names = [tool['name'] for tool in contract['tools']]
    if len(tool_names) != 10 or len(set(tool_names)) != 10:
        raise SystemExit('Review a tool-count change before publication')
    if len(catalog['skills']) != 15 or len({s['name'] for s in catalog['skills']}) != 15:
        raise SystemExit('Review a skill-count change before publication')
    for skill in catalog['skills']:
        if not set(skill['tools']).issubset(tool_names):
            raise SystemExit(f'Unknown tool dependency in {skill["name"]}')
    assets = {asset['name']: asset for asset in metadata['skillsRelease']['assets']}
    mcp_commit = metadata['repositories']['portfolio-mcp']['commit']
    skill_commit = metadata['repositories']['portfolio-mcp-skills']['commit']
    tools = [
        '# Tool reference',
        '',
        f'Public contract snapshot: **{metadata["snapshotDate"]}**, MCP commit [`{mcp_commit}`](https://github.com/fillfolio/portfolio-mcp/commit/{mcp_commit}).',
        '',
        'Fillfolio exposes ten read-only tools. A connected host may discover a subset because of account eligibility, client grants, or rendering support. Namespaces vary by host.',
        '',
        '**OAuth scope:** `mcp:read`. The permission column below records internal Fillfolio application grants. Do not request those names as extra OAuth scopes. Spending and budgets need independent per-client permission.',
        '',
        '| Tool | Internal read permission | Input fields |',
        '| --- | --- | --- |'
    ]
    for tool in contract['tools']:
        fields = ', '.join(f'`{key}`' for key in tool['input'].get('properties', {})) or '`{}` only'
        tools.append(f'| [`{tool["name"]}`](#{tool["name"]}) | `{tool["scope"]}` | {fields} |')
    tools += ['', '## Response envelope', '',
        'The nine financial tools return structured content and JSON text with `asOf`, `partial`, `missing`, and tool-specific `data`. Keep missing values and coverage warnings. `asOf` records response generation, not quote freshness.', '',
        json_block({'asOf':'2026-10-16T12:00:00.000Z','partial':False,'missing':[],'data':{}}),
        '`open_fillfolio` returns launch text and UI metadata instead of the financial envelope. It advertises `ui://fillfolio/dashboard-v4.html` with MIME type `text/html;profile=mcp-app` for supporting hosts. [Dashboard sharing](security.md#financial-records-shared-with-your-ai-host)', '',
        'The shapes below come from the captured contract. Read the [complete JSON contract](sources/tool-contract.json) for output schemas, enums, security metadata, and resource CSP. [Data interpretation rules](data.md) cover pagination and field meaning.']
    for tool in contract['tools']:
        tools += ['', f'## {tool["name"]}', '', tool['description'], '',
                  f'Internal permission: `{tool["scope"]}`. OAuth: `mcp:read`. Read-only: **yes**.', '',
                  '### Input', '', json_block(tool['input'])]
        if tool.get('availability'):
            tools += ['', 'Availability: ' + tool['availability'] + '.']
        shape = {k: tool[k] for k in ('data', 'item', 'result') if k in tool}
        if shape:
            tools += ['', '### Returned fields', '', json_block(shape)]
        elif tool.get('outputSchema'):
            props = tool['outputSchema']['properties']['data']['properties']
            tools += ['', '### Returned fields', '',
                      'Data keys: ' + ', '.join(f'`{key}`' for key in props) + '. See the complete output schema in the linked contract.']
    write('tools.md', '\n'.join(tools))
    skill_lines = ['# Workflow skills', '',
        f'Library **{catalog["version"]}** contains **{len(catalog["skills"])}** instruction-only workflows. Source snapshot: **{metadata["snapshotDate"]}**, [`{skill_commit}`](https://github.com/fillfolio/portfolio-mcp-skills/commit/{skill_commit}).', '',
        'Install only the workflows you need. Use an existing release ZIP or copy its canonical skill folder to the directory your host documents. Keep `SKILL.md` and references together. A ZIP installer needs the skill folder at the archive root.', '',
        'For Codex, copy a selected folder to `~/.agents/skills/<skill-name>`. For Claude Code, use `~/.claude/skills/<skill-name>`. Follow the [source client setup guide](https://github.com/fillfolio/portfolio-mcp-skills/blob/' + skill_commit + '/docs/client-setup.md) for host-specific installation and compatibility limits.', '',
        'The first fourteen workflows use authenticated MCP. The public connection catalog uses unauthenticated HTTP and requires a host with an HTTP/web capability. Installing instructions does not connect your account.', '',
        'The ZIPs below belong to the existing **v0.1.0** release. Source links point to the current captured repository commit; later documentation fixes can differ from the earlier release snapshot. No new skill archives accompany this site.', '',
        '| Workflow | Tools | Existing ZIP |', '| --- | --- | --- |']
    for skill in catalog['skills']:
        asset = assets[skill['name'] + '.zip']
        dependencies = ', '.join(f'`{x}`' for x in skill['tools']) or 'Public HTTP catalog'
        skill_lines.append(f'| [{skill["title"]}](#{skill["name"]}) | {dependencies} | [Download]({asset["browser_download_url"]}) |')
    for skill in catalog['skills']:
        asset = assets[skill['name'] + '.zip']
        source = f'https://github.com/fillfolio/portfolio-mcp-skills/tree/{skill_commit}/{skill["path"]}'
        access = 'Authenticated MCP; account and client permissions apply.' if skill['access'] == 'authenticated-mcp' else 'Public HTTP; no account sign-in. This workflow cannot read private records.'
        skill_lines += ['', f'## {skill["name"]}', '', skill['title'] + '. ' + access, '',
                        f'[Canonical source folder]({source}) · [Existing release ZIP]({asset["browser_download_url"]})', '',
                        'SHA-256:', '', '```text\n' + asset['digest'].removeprefix('sha256:') + '\n```']
    write('skills.md', '\n'.join(skill_lines))
    download_lines = ['# Downloads and captured sources', '',
        f'Snapshot date: **{metadata["snapshotDate"]}**. Prefer the documentation at <{CANONICAL}>.', '',
        '## Public source commits', '', '| Repository | Captured commit |', '| --- | --- |']
    for name, repo in metadata['repositories'].items():
        download_lines.append(f'| [{name}]({repo["url"]}) | [`{repo["commit"]}`]({repo["url"]}/commit/{repo["commit"]}) |')
    download_lines += ['', 'Read the [snapshot metadata](sources/snapshot.json), [tool contract](sources/tool-contract.json), [skills catalog](sources/skills-catalog.json), and [MIT license](sources/MIT-LICENSE.txt). Source repositories remain canonical for current releases, support, and contributions.', '',
        '## Existing skills release', '',
        f'Release [v0.1.0]({metadata["skillsRelease"]["url"]}) points to commit `{metadata["skillsRelease"]["commit"]}`. It predates the current captured skills documentation commit. This site links the existing files and does not rebuild or replace that release.', '',
        '| File | Size in bytes | SHA-256 |', '| --- | ---: | --- |']
    for name in ('portfolio-mcp-skills-v0.1.0.zip','release-manifest.json','SHA256SUMS'):
        asset = assets[name]
        download_lines.append(f'| [{name}]({asset["browser_download_url"]}) | {asset["size"]} | `{asset["digest"].removeprefix("sha256:")}` |')
    download_lines += ['', 'Standalone skill ZIP links and hashes appear in the [workflow catalog](skills.md). The release checksum file uses `skills/<name>.zip` paths; GitHub serves those standalone files by their basename. Match the basename and digest when downloading one file.', '',
        'Verify a selected download with your operating system\'s SHA-256 utility. On macOS:', '',
        '```sh\nshasum -a 256 fillfolio-portfolio-overview.zip\n```', '',
        'Compare the result with the exact hash listed for that file. A checksum verifies file identity; it does not establish host OAuth compatibility.', '',
        '## Machine-readable documentation', '',
        '[llms.txt](llms.txt) lists the documentation and source links. [llms-full.txt](llms-full.txt) includes the authored pages and generated references. These files provide text for readers and agents; they do not install a connection or guarantee search indexing.', '',
        '## Support and contributions', '',
        'Use [portfolio-mcp issues](https://github.com/fillfolio/portfolio-mcp/issues) for contract/docs reports and [portfolio-mcp-skills issues](https://github.com/fillfolio/portfolio-mcp-skills/issues) for workflow reports. Do not post financial records or credentials in a public issue.', '',
        'Public materials use MIT. Fillfolio operates the hosted service under separate [terms](https://fillfolio.com/terms) and [privacy disclosures](https://fillfolio.com/privacy).']
    write('downloads.md', '\n'.join(download_lines))
    llms = ['# Fillfolio MCP public documentation', '',
        '> MIT contracts and 15 instruction-only workflows for stored Fillfolio portfolio, stocks, ETFs, funds, crypto, cash, spending, and budget reads.', '',
        f'Snapshot: {metadata["snapshotDate"]}. Canonical documentation: {CANONICAL}', '',
        'Account reads require an eligible paid Fillfolio account, accepted preregistered client/callback, OAuth mcp:read with PKCE S256 and resource binding, and consent. Spending and budgets require independent internal client grants. DCR is disabled.', '',
        'Existing ChatGPT Work desktop and Codex setups passed live acceptance before this snapshot. Claude web and Claude Code have registered identities, with no new live acceptance claimed here. Other clients need accepted registration. Native ChatGPT plugin 0.1.1 remains In review as of 2026-10-16.', '',
        'Tools read stored data and cannot trade, transfer, edit records, or refresh providers. Opening a dashboard view shares its displayed financial data with the chat. Hide amounts masks the panel only. Keep currencies, nulls, partial warnings, coverage and synchronization fields. Response generation time does not establish quote freshness.', '',
        BRAND_LINKS, '', '## Documentation']
    for path, title in [('connect','Connect a client'),('skills','Workflow catalog and existing release ZIPs'),('tools','Ten-tool reference'),('examples','Invented data examples'),('data','Currency, pagination and completeness rules'),('security','Access and sharing'),('tutorial','First portfolio review tutorial'),('downloads','Exact source commits and checksums')]:
        llms.append(f'- [{title}]({CANONICAL}{path}/)')
    llms += ['', '## Canonical sources', '- [MCP contract and helper](https://github.com/fillfolio/portfolio-mcp)', '- [Workflow skills](https://github.com/fillfolio/portfolio-mcp-skills)', '- [Complete documentation text](' + CANONICAL + 'llms-full.txt)']
    write('llms.txt', '\n'.join(llms))
    full = ['# Fillfolio MCP complete documentation', '', f'Snapshot {metadata["snapshotDate"]}. Canonical {CANONICAL}', '', BRAND_LINKS, '',
            'Public sources: ' + json.dumps(metadata['repositories'], sort_keys=True), '']
    for name in ('index','connect','skills','tools','examples','data','security','tutorial','downloads','maintain'):
        full += ['\n---\n', f'Source: {CANONICAL}' + ('' if name == 'index' else name + '/'), '', (DOCS/(name+'.md')).read_text()]
    write('llms-full.txt', '\n'.join(full))
    write('robots.txt', 'User-agent: *\nAllow: /\nSitemap: ' + CANONICAL + 'sitemap.xml')
    print('Generated references: 10 tools, 15 skills, 18 existing release assets, llms.txt and llms-full.txt')

if __name__ == '__main__':
    main()
