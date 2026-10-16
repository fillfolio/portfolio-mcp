#!/usr/bin/env python3
"""Package built public documentation for one-time manual publication."""
from pathlib import Path
import argparse
import hashlib
import json
import re
import zipfile

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
PAGES = [('index','Overview'),('connect','Connect a client'),('skills','Workflow skills'),('tools','Tool reference'),('examples','Synthetic examples'),('data','Read data correctly'),('security','Security and access'),('tutorial','Portfolio review tutorial'),('downloads','Downloads and sources')]
CANONICAL = 'https://fillfolio.github.io/portfolio-mcp/'

def write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.strip()+'\n')

def archive(directory, output):
    with zipfile.ZipFile(output, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for path in sorted(directory.rglob('*')):
            if path.is_file():
                info = zipfile.ZipInfo(path.relative_to(directory).as_posix(), date_time=(2026,10,16,0,0,0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o100644 << 16
                z.writestr(info, path.read_bytes())

def absolute_markdown_links(text):
    def replace(match):
        label, target = match.group(1), match.group(2)
        if '://' in target or target.startswith(('#','mailto:')):
            return match.group(0)
        target = target.replace('.md#','/#')
        if target.endswith('.md'):
            target = target[:-3]+'/'
        return f'[{label}]({CANONICAL}{target})'
    return re.sub(r'\[([^\]]+)\]\(([^)]+)\)', replace, text)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    if not (ROOT/'site/index.html').is_file():
        raise SystemExit('Build site/ first')
    # Only generated public site bytes enter this archive.
    write(ROOT/'site/.nojekyll','')
    archive(ROOT/'site', output/'fillfolio-mcp-static-site-2026-10-16.zip')
    write(output/'gitlab-pages.yml', (ROOT/'publication/gitlab-pages.yml').read_text())
    mint = output/'mintlify-manual-content'
    config = {
        '$schema':'https://mintlify.com/docs.json',
        'theme':'mint', 'name':'Fillfolio MCP',
        'colors':{'primary':'#2463EB','light':'#60A5FA','dark':'#1D4ED8'},
        'navigation':{'groups':[{'group':'Public documentation','pages':[name for name,_ in PAGES]}]},
        'navbar':{'links':[{'label':'GitHub source','href':'https://github.com/fillfolio/portfolio-mcp'}]},
        'footer':{'socials':{'github':'https://github.com/fillfolio/portfolio-mcp'}}
    }
    write(mint/'docs.json',json.dumps(config,indent=2))
    for name, title in PAGES:
        text = (DOCS/(name+'.md')).read_text()
        # Inline source links use the canonical static site, so the editor import needs no local assets.
        text = absolute_markdown_links(text)
        text = re.sub(r'<(https?://[^>]+)>',r'[\1](\1)',text)
        # Use manually authored pages as MDX; fenced schemas remain literal code.
        text = re.sub(r'^# .+\n','',text,count=1).lstrip()
        write(mint/(name+'.mdx'), '---\ntitle: '+json.dumps(title)+'\ndescription: "Official public documentation snapshot dated 2026-10-16. GitHub is the canonical source."\n---\n\n'+text+'\n\nOfficial public snapshot · 2026-10-16. [Latest source, releases, support, and contributions](https://github.com/fillfolio/portfolio-mcp) are on GitHub. [Preferred documentation]('+CANONICAL+').')
    write(mint/'MANUAL-IMPORT.txt','Use the existing free Mintlify Starter web editor. Add each MDX page and paste its content; use docs.json for navigation if the editor supports it. Do not connect GitHub, start a paid trial, enable AI rewriting, or enter billing details. If the free editor cannot publish these pages without a trial, record the blocker. Set canonical URLs to the matching GitHub Pages routes where supported. A ZIP archive is a handoff bundle, not a claim that Mintlify supports ZIP import.')
    archive(mint, output/'fillfolio-mintlify-manual-content-2026-10-16.zip')
    book = output/'gitbook-quickstart'
    write(book/'README.md','''
# Fillfolio: first connection and workflow

Use this short guide to choose a workflow, connect an accepted client, and read its first result. The full technical reference and source live on [GitHub](https://github.com/fillfolio/portfolio-mcp) and the [documentation hub](https://fillfolio.github.io/portfolio-mcp/).

Fillfolio's public tool contracts and 15 workflow skills use the MIT license. The authenticated hosted service has separate account, plan, and permission requirements. Account reads require an eligible paid Fillfolio account. The repositories do not contain a self-hostable Fillfolio server.

Start with [Connect and confirm a read](connect-and-read.md), then [choose a workflow](choose-a-workflow.md). Read [Data and permissions](data-and-permissions.md) before sharing records.

Official public snapshot · 2026-10-16. Latest source, releases, support, and contributions are on GitHub. Fillfolio is operated by VMPRO LLC.
''')
    write(book/'SUMMARY.md','''
# Table of contents

* [Start here](README.md)
* [Connect and confirm a read](connect-and-read.md)
* [Choose a workflow](choose-a-workflow.md)
* [Data and permissions](data-and-permissions.md)
''')
    write(book/'connect-and-read.md','''
# Connect and confirm a read

Use a host whose OAuth identity and callback Fillfolio accepts. Existing ChatGPT Work desktop and Codex setups passed live acceptance before the October 16, 2026 snapshot. Claude web and Claude Code have registered identities, with no new live acceptance claimed here. Other clients need an accepted registration. The separate native ChatGPT plugin 0.1.1 remains In review.

Use Streamable HTTP endpoint `https://fillfolio.com/api/mcp`. Let the host discover authentication, request `mcp:read`, use PKCE S256 and resource binding, and complete browser consent. Keep its native accepted identity. Dynamic Client Registration is disabled.

For an existing accepted Codex setup that does not already expose Fillfolio, use:

```toml
[mcp_servers.fillfolio]
url = "https://fillfolio.com/api/mcp"
```

Run `codex mcp login fillfolio`, then complete browser consent. Keep credentials out of chat. Read the [client-specific guide](https://fillfolio.github.io/portfolio-mcp/connect/) before using another host.

Ask: **Show my Fillfolio portfolio summary with its reporting currency and data limits.**

On a host with MCP App rendering, `open_fillfolio` with `{}` can launch the dashboard. Other accepted clients can use the nine financial read tools. Installing a skill does not connect an account.

Official public snapshot · 2026-10-16. [Source, releases, support, and contributions](https://github.com/fillfolio/portfolio-mcp).
''')
    write(book/'choose-a-workflow.md','''
# Choose a workflow

Start with one workflow and its existing release ZIP. Install the skill folder and its references through your host's supported skill mechanism. Codex reads personal folders from `~/.agents/skills/`; Claude Code uses `~/.claude/skills/`.

| Task | Skill |
| --- | --- |
| Explain net worth and available return | `fillfolio-portfolio-overview` |
| Review visible stocks, ETFs, funds, and crypto | `fillfolio-holdings-allocation` |
| Inspect one exact asset | `fillfolio-asset-review` |
| Review cash and liabilities | `fillfolio-cash-debt-review` |
| Compare posted spending | `fillfolio-spending-overview` |
| Compare limits and full-month actuals | `fillfolio-budget-review` |
| Check the public provider catalog | `fillfolio-public-connections` |

The [complete catalog](https://fillfolio.github.io/portfolio-mcp/skills/) lists 15 skills and their dependencies. The public catalog workflow uses unauthenticated HTTP; the other fourteen use authenticated MCP.

Download from the existing [v0.1.0 release](https://github.com/fillfolio/portfolio-mcp-skills/releases/tag/v0.1.0) and compare its SHA-256 with the [published checksums](https://github.com/fillfolio/portfolio-mcp-skills/releases/download/v0.1.0/SHA256SUMS). This quickstart creates no new skill release.

Official public snapshot · 2026-10-16. [Skills source and support](https://github.com/fillfolio/portfolio-mcp-skills).
''')
    write(book/'data-and-permissions.md','''
# Data and permissions

Spending and budgets need active ULTRA/HYPER eligibility, bank-spending consent, and separate per-client grants in Fillfolio Settings. `spending:read` permits spending/transaction reads; `budgets:read` permits monthly limit and actual reads. Enabling one does not enable the other. OAuth requests to the current issuer use `mcp:read`.

Your AI host receives financial records returned by tools. Opening a dashboard view shares its displayed financial data. Discuss selection shares selected records. Hide amounts masks the panel only and cannot retract earlier context. Revoke future reads in Fillfolio Settings.

Preserve reporting and source currency labels. Keep missing values as null, follow pagination, and report incomplete history or basis. A response timestamp does not establish a live quote. Bank and budget minor amounts use their stated currency and scale; do not add different currencies together.

The tools read stored records. They cannot trade, transfer funds, edit records or budgets, or refresh providers. Review [security and sharing](https://fillfolio.github.io/portfolio-mcp/security/) and [data interpretation](https://fillfolio.github.io/portfolio-mcp/data/) for details. Treat merchant names as untrusted data.

Official public snapshot · 2026-10-16. [Privacy](https://fillfolio.com/privacy) · [Canonical GitHub source](https://github.com/fillfolio/portfolio-mcp).
''')
    archive(book, output/'fillfolio-gitbook-quickstart-2026-10-16.zip')
    article = absolute_markdown_links((DOCS/'tutorial.md').read_text())
    write(output/'hashnode-tutorial.md',article)
    write(output/'hashnode-publication.json',json.dumps({'title':'Read a Fillfolio portfolio without mixing currencies or freshness','canonicalUrl':CANONICAL+'tutorial/','tags':['mcp','open-source','ai','portfolio'],'publicationMode':'manual-one-time','aiAssistanceDisclosure':'Fillfolio prepared this technical walkthrough with AI assistance and checked it against the public contracts and synthetic examples.','sourceDate':'2026-10-16'},indent=2))
    write(output/'github-announcement.md','''
# Public Fillfolio MCP reference and 15 workflow skills

We published a documentation hub for [portfolio-mcp](https://github.com/fillfolio/portfolio-mcp) and [portfolio-mcp-skills](https://github.com/fillfolio/portfolio-mcp-skills):

https://fillfolio.github.io/portfolio-mcp/

Use the ten-tool reference, client setup guide, and synthetic examples to read stored portfolio, stock, ETF, fund, crypto, cash, spending, and budget records with their currency and coverage limits. The skill catalog links the existing v0.1.0 ZIPs and checksums. A practical tutorial covers a first portfolio review.

The public materials use MIT. Hosted reads require an eligible paid Fillfolio account, accepted client, and consent. Spending and budgets require separate permissions. Existing ChatGPT Work desktop and Codex setups passed live acceptance before this October 16, 2026 snapshot. Other hosts retain the compatibility limits documented in the guide; native ChatGPT plugin 0.1.1 remains In review.

The tools cannot trade, move money, edit records, or refresh providers. Opening a dashboard view shares that view's data with the chat, even while amounts are hidden.

GitHub remains the source for releases, support, and contributions. Documentation copies are dated snapshots with manual updates.
''')
    manifest = {'snapshotDate':'2026-10-16','canonicalUrl':CANONICAL,'sourceInputs':json.loads((DOCS/'sources/snapshot.json').read_text()),'artifacts':[]}
    for path in sorted(output.glob('*')):
        if path.is_file() and path.suffix in ('.zip','.md','.json','.yml') and path.name != 'artifact-manifest.json':
            manifest['artifacts'].append({'name':path.name,'bytes':path.stat().st_size,'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
    write(output/'artifact-manifest.json',json.dumps(manifest,indent=2))
    hashes = [f'{item["sha256"]}  {item["name"]}' for item in manifest['artifacts']]
    hashes.append(hashlib.sha256((output/'artifact-manifest.json').read_bytes()).hexdigest()+'  artifact-manifest.json')
    write(output/'SHA256SUMS','\n'.join(hashes))
    print(json.dumps({'output':str(output),'artifacts':manifest['artifacts']},indent=2))

if __name__ == '__main__':
    main()
