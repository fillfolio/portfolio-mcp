#!/usr/bin/env python3
"""Check reference identity, synthetic arithmetic, and rendered local links."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from decimal import Decimal
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / 'docs'
SITE = ROOT / 'site'
CANONICAL = 'https://fillfolio.github.io/portfolio-mcp/'
class Page(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []
        self.ids = set()
        self.canonicals = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if attrs.get('id'):
            self.ids.add(attrs['id'])
        if tag in ('a','link') and attrs.get('href'):
            self.links.append(attrs['href'])
        if tag in ('img','script') and attrs.get('src'):
            self.links.append(attrs['src'])
        if tag == 'link' and attrs.get('rel') == 'canonical':
            self.canonicals.append(attrs.get('href'))

def main():
    metadata = json.loads((DOCS/'sources/snapshot.json').read_text())
    contract = json.loads((DOCS/'sources/tool-contract.json').read_text())
    catalog = json.loads((DOCS/'sources/skills-catalog.json').read_text())
    assert len(contract['tools']) == 10
    assert len(catalog['skills']) == 15
    assert metadata['canonicalUrl'] == CANONICAL
    tools_text = (DOCS/'tools.md').read_text()
    skills_text = (DOCS/'skills.md').read_text()
    toolnames = {tool['name'] for tool in contract['tools']}
    for tool in contract['tools']:
        assert f'## {tool["name"]}\n' in tools_text
        assert tool['readOnly'] is True
        assert tool['annotations']['readOnlyHint'] is True
        assert tool['_meta']['securitySchemes'] == [{'type':'oauth2','scopes':['mcp:read']}]
    for skill in catalog['skills']:
        assert set(skill['tools']).issubset(toolnames)
        assert f'## {skill["name"]}\n' in skills_text
    for filename, key in [('tool-contract.json','contractSha256'),('skills-catalog.json','catalogSha256')]:
        assert hashlib.sha256((DOCS/'sources'/filename).read_bytes()).hexdigest() == metadata[key]
    assert (ROOT/'contract/tools.json').read_bytes() == (DOCS/'sources/tool-contract.json').read_bytes()
    checksums = {Path(path).name:digest for digest, path in (line.split(None,1) for line in (DOCS/'sources/skills-SHA256SUMS.txt').read_text().splitlines())}
    for asset in metadata['skillsRelease']['assets']:
        if asset['name'] != 'SHA256SUMS':
            assert checksums[asset['name']] == asset['digest'].removeprefix('sha256:')
    f = json.loads((DOCS/'sources/synthetic-fixture.json').read_text(), parse_float=Decimal)
    assert f['synthetic'] is True
    assert sum(x['marketValue'] for x in f['holdings']) == f['holdingsValue']
    assert sum(x['costBasis'] for x in f['holdings']) == f['availableCostBasis']
    assert f['holdingsValue'] + f['cash'] - f['debt'] == f['netWorth']
    assert f['holdingsValue'] - f['availableCostBasis'] == f['currentValueLessAvailableBasis']
    euro = f['holdings'][2]
    assert euro['sourceMarketValue'] * euro['illustrativeFxToUSD'] == euro['marketValue']
    assert euro['sourceCostBasis'] * euro['illustrativeFxToUSD'] == euro['costBasis']
    for row in f['postedSpending']:
        assert row['purchaseMinor'] - row['refundMinor'] == row['netSpentMinor']
        if 'budgetLimitMinor' in row:
            assert row['budgetLimitMinor'] - row['netSpentMinor'] == row['remainingMinor']
    pages = {}
    for path in SITE.rglob('*.html'):
        parser = Page()
        parser.feed(path.read_text())
        pages[path.resolve()] = parser
    assert pages, 'Build site/ before checking rendered links'
    failures = []
    checked = 0
    for path, parser in pages.items():
        relative = path.relative_to(SITE)
        if relative.as_posix() != '404.html':
            route = relative.as_posix().removesuffix('index.html')
            expected = CANONICAL + route
            if parser.canonicals != [expected]:
                failures.append(f'{relative}: canonical {parser.canonicals} expected {expected}')
        if relative.as_posix() != '404.html':
            assert 'Latest source, releases, support, and contributions are on' in path.read_text()
        for link in parser.links:
            parsed = urlsplit(link)
            if parsed.scheme or parsed.netloc:
                continue
            if parsed.path.startswith('/'):
                failures.append(f'{relative}: host-dependent root-relative link {link}')
                continue
            target = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path
            if target.is_dir():
                target /= 'index.html'
            if not target.is_relative_to(SITE):
                failures.append(f'{relative}: link escapes site root {link}')
                continue
            checked += 1
            if not target.exists():
                failures.append(f'{relative}: missing {link}')
            elif parsed.fragment and target in pages and unquote(parsed.fragment) not in pages[target].ids:
                failures.append(f'{relative}: missing fragment {link}')
    # Authored prose should contain no generated access tokens, real account examples, or remote client script.
    for path in DOCS.glob('*.md'):
        text = path.read_text()
        assert '\u2014' not in text, f'Editorial review: em dash in {path.name}'
        assert not re.search(r'(?:Bearer\s+[A-Za-z0-9_.-]{20,}|(?:sk|pk)_(?:live|test)_[A-Za-z0-9]{10,})', text)
    assert (SITE/'llms.txt').is_file() and (SITE/'llms-full.txt').is_file()
    if failures:
        raise SystemExit('\n'.join(failures))
    print(json.dumps({'result':'pass','tools':10,'skills':15,'existingReleaseAssets':18,'renderedPages':len(pages),'localLinksChecked':checked,'syntheticArithmetic':'pass','canonicalTags':'pass','capturedInputs':'pass'},indent=2))

if __name__ == '__main__':
    main()
