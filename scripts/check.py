"""Check generated magazine links, structure, content, and shared head injection."""
from collections import Counter
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import urlsplit, unquote
import json

ROOT=Path(__file__).resolve().parent.parent
OUT=ROOT/'dist'
class Page(HTMLParser):
    def __init__(self,text):
        super().__init__(); self.ids=[]; self.links=[]; self.h1=0; self.head=False; self.head_html=''; self.feed(text)
    def handle_starttag(self,tag,attrs):
        attrs=dict(attrs)
        if tag=='h1': self.h1+=1
        if 'id' in attrs: self.ids.append(attrs['id'])
        for key in ('href','src'):
            if key in attrs: self.links.append(attrs[key])
pages={p.name:Page(p.read_text()) for p in OUT.glob('*.html')}
assert len(pages)==33,f'Expected 33 pages, got {len(pages)}'
shared=(ROOT/'shared/head-scripts.html').read_text()
for name,page in pages.items():
    assert page.h1==1,(name,'Expected one h1')
    assert len(page.ids)==len(set(page.ids)),(name,'Duplicate IDs')
    head=(OUT/name).read_text().split('</head>')[0]
    assert shared in head,(name,'Shared scripts missing from head')
    for link in page.links:
        parsed=urlsplit(link)
        if parsed.scheme or parsed.netloc: continue
        target=unquote(parsed.path) or name
        assert (OUT/target).is_file(),(name,'Broken target',link)
        if parsed.fragment and target in pages:
            assert unquote(parsed.fragment) in pages[target].ids,(name,'Missing fragment',link)
stories=json.loads((ROOT/'content/stories.json').read_text())
assert len(stories)==len({s['id'] for s in stories})==24
assert set(Counter(s['category'] for s in stories).values())=={6}
for s in stories:
    assert 'story-'+s['id']+'.html' in pages
    assert len(s['sections'])>=3
    assert all(section['paragraphs'] for section in s['sections'])
assert json.loads((OUT/'assets/stories.json').read_text())==stories
# Verify the reference's three distinct page structures stay in the generated output.
home=(OUT/'index.html').read_text()
for marker in ['class="front"', 'class="front-latest"', 'class="print-cols"', 'class="print-split"', 'class="photo-grid"']:
    assert marker in home, ('Homepage layout missing',marker)
for category in ['entertainment','music','gaming','fashion']:
    page=(OUT/f'{category}.html').read_text()
    for marker in ['class="news-layout"', 'class="news-main"', 'story-list', 'class="sidebar"']:
        assert marker in page,(category,'Category layout missing',marker)
for story in stories:
    page=(OUT/f'story-{story["id"]}.html').read_text()
    for marker in ['class="article-main"', 'class="article-heading"', 'class="article-figure"', 'class="sidebar"']:
        assert marker in page,(story['id'],'Article layout missing',marker)
print('PASS: 33 pages; 24 unique articles; six per category; all local links, assets, fragments, headings, and shared head scripts verified.')
