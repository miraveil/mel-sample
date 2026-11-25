"""Build the OFFBEAT static magazine. No external dependencies."""
from pathlib import Path
import html
import json
import shutil

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'dist'
OUT.mkdir(exist_ok=True)
shutil.copytree(ROOT / 'assets', OUT / 'assets', dirs_exist_ok=True)
HEAD = (ROOT / 'shared/head-scripts.html').read_text()
STORIES = json.loads((ROOT / 'content/stories.json').read_text())
(OUT / 'assets/stories.json').write_text(json.dumps(STORIES, ensure_ascii=False))
E = lambda text: html.escape(str(text), quote=True)
SECTIONS = {
 'index': ('Discover', 'Culture, without the algorithm.', 'Your next obsession starts here. A considered mix of music, screen culture, games, and personal style.', 'live-show'),
 'entertainment': ('Entertainment', 'A different kind of screen time.', 'Film-club rituals, unexpected perspectives, and the craft behind the screen.', 'small-cinema'),
 'music': ('Music', 'Find your new frequency.', 'Live rooms, deep listening, and the small discoveries that stay with you.', 'opening-act'),
 'gaming': ('Gaming', 'Play outside the usual.', 'Shared screens, thoughtfully built worlds, and a little more room for play.', 'shared-screen'),
 'fashion': ('Fashion', 'Wear your point of view.', 'Personal style over passing trends. Make more of the wardrobe you already have.', 'personal-style'),
}
BY_ID = {s['id']: s for s in STORIES}
ALTS = {'concert.jpg':'A raised hand in a crowd facing an illuminated concert stage', 'crowd.jpg':'Festival audience watching a live performance', 'cinema.jpg':'Rows of red seats in a cinema auditorium', 'film.jpg':'A film camera and movie-making equipment', 'gaming.jpg':'A gaming setup with illuminated screens', 'controller.jpg':'A video game controller', 'fashion.jpg':'A woman wearing sunglasses and a red coat', 'wardrobe.jpg':'Clothing arranged in a fashion store', 'studio.jpg':'Musical instruments and recording equipment', 'microphone.jpg':'A microphone ready for a performance'}
PAGES = []

def url(s): return f'story-{s["id"]}.html'
def category_items(category): return [s for s in STORIES if s['category'] == category]
def img(s, lazy=True): return f'<img src="assets/images/{s["image"]}" alt="{E(ALTS[s["image"]])}" width="1200" height="800" {"loading=lazy" if lazy else ""}>'
def meta(s): return f'<div class="card-meta">{E(s["topic"])} <span>· {s["minutes"]} min read</span></div>'
def card(s):
 return f'''<article class="story-card" data-category="{s['category']}" data-topic="{E(s['topic'])}" data-search="{E((s['title']+' '+s['desc']+' '+s['topic']+' '+s['category']).lower())}"><a class="card-image" href="{url(s)}" aria-label="Read {E(s['title'])}">{img(s)}<span class="image-label">Read story</span></a>{meta(s)}<h3><a href="{url(s)}">{E(s['title'])}</a></h3><p>{E(s['desc'])}</p></article>'''
def radar(s): return f'<a class="radar-item" href="{url(s)}">{meta(s)}<h3>{E(s["title"])}</h3><span class="read-label">Read story</span></a>'
def ad(slug): return f'<div class="ad-wrap"><span>Advertisement</span><ins class="cox-ad-unit" data-cox-unit="offbeat_{slug}_midfeed" style="display:block;width:100%"></ins></div>'
def write(slug, title, description, body, theme='index', active=None):
 nav=''.join(f'<a href="{key}.html" {"aria-current=page" if active==key else ""}>{data[0]}</a>' for key,data in SECTIONS.items())
 document=f'''<!doctype html><html lang="en" data-theme="{theme}"><head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{E(title)} — OFFBEAT</title><meta name="description" content="{E(description)}"><meta property="og:title" content="{E(title)} — OFFBEAT"><meta property="og:description" content="{E(description)}"><meta property="og:type" content="{'article' if slug.startswith('story-') else 'website'}"><link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/site.css">
<!-- Shared head scripts: edit shared/head-scripts.html, then rebuild. -->
{HEAD}
<script src="assets/site.js" defer></script></head><body><a class="skip" href="#main">Skip to content</a>
<div class="topline"><div class="container"><span>INDEPENDENT MINDS. SHARED OBSESSIONS.</span><span>An editorial demo · The Culture Issue</span></div></div>
<header class="container"><div class="masthead"><a class="brand" href="index.html" aria-label="Offbeat home">offbeat<span>✳</span></a><span class="brand-note">A little off the mainstream.<br>A lot more interesting.</span><a class="pill" href="reading-list.html">Your reading list <span class="saved-count">0</span></a></div><div class="nav-row"><nav aria-label="Main navigation">{nav}</nav><a class="search-link" href="search.html">Search <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="10" cy="10" r="6"/><path d="m15 15 5 5"/></svg></a></div><nav class="secondary-nav" aria-label="Magazine"><span>THE CULTURE DESK</span><a href="weekend.html">The Weekend Edit</a><a href="search.html">Explore all stories</a><a href="about.html">About Offbeat</a></nav></header>
<main id="main" class="container">{body}</main>
<footer class="container"><a class="brand" href="index.html">offbeat<span>✳</span></a><p>Music. Screen. Play. Style.<br>Culture for the endlessly curious.</p><nav aria-label="Footer"><a href="about.html">About</a><a href="weekend.html">Weekend Edit</a><a href="reading-list.html">Reading list</a><a href="search.html">Search</a></nav><span>© 2026 OFFBEAT<br>Original demo editorial content.</span></footer></body></html>'''
 (OUT/f'{slug}.html').write_text(document)
 PAGES.append(slug+'.html')
def intro(kicker,title,desc): return f'<section class="intro"><div><p class="eyebrow">{E(kicker)}</p><h1>{E(title)}</h1></div><p>{E(desc)}</p></section>'
def browse(items, category=None, page_size=9):
 options=['All']+([category] if category else ['Entertainment','Music','Gaming','Fashion'])
 topics=sorted({s['topic'] for s in items})
 filters=''.join(f'<button class="filter" data-filter="{c}" aria-pressed="{str(c=="All").lower()}">{c}</button>' for c in options) if not category else ''.join(f'<button class="filter" data-topic-filter="{E(t)}" aria-pressed="{str(t=="All topics").lower()}">{E(t)}</button>' for t in ['All topics']+topics)
 return f'''<section class="latest browse" data-page-size="{page_size}" aria-labelledby="latest-title"><div class="section-heading"><div><p class="eyebrow">STAY CURIOUS</p><h2 id="latest-title">{'Explore the archive' if not category else 'More from '+category}<span>✳</span></h2></div><span class="muted">{len(items)} stories, each with a different perspective.</span></div><div class="filter-bar"><div class="filters" role="group" aria-label="Filter stories">{filters}</div><label class="search-field"><span class="sr-only">Search stories</span><input type="search" placeholder="Search stories…" aria-label="Search stories"></label></div><div class="browse-meta"><p id="result-status" role="status"></p><label>Order <select id="sort" aria-label="Sort stories"><option value="editorial">Editorial order</option><option value="title">Title A–Z</option><option value="short">Shortest reads</option></select></label></div><div class="story-grid">{''.join(card(s) for s in items)}</div><div class="empty" hidden>No stories found. Try a different title, topic, or category.<button id="reset" class="button">Reset filters</button></div><nav class="pagination" aria-label="Story pages"><button class="button" id="previous">Previous</button><span id="page-status"></span><button class="button" id="next">Next</button></nav></section>'''
def closing(): return '<section class="closing"><span aria-hidden="true">✳</span><div><p class="eyebrow">A LITTLE LESS SCROLLING</p><h2>Make a little room<br>for a good weekend.</h2></div><a class="button" href="weekend.html">Open the Weekend Edit</a></section>'

for slug,(name,heading,description,lead_id) in SECTIONS.items():
 featured=BY_ID[lead_id]
 items=STORIES if slug=='index' else category_items(name)
 picks=[s for s in items if s['id']!=lead_id][:3]
 hero=f'''<section class="feature-grid" aria-label="Featured stories"><article class="hero">{img(featured,False)}<div class="hero-shade"></div><div class="hero-copy"><span class="tag">THE COVER STORY</span><p class="hero-category">{E(featured['category'])} / {E(featured['topic'])}</p><h2><a href="{url(featured)}">{E(featured['title'])}</a></h2><p>{E(featured['desc'])}</p><a class="button button-light" href="{url(featured)}">Read the feature</a></div></article><aside class="editors"><div class="aside-heading"><span class="eyebrow">THE EDITOR’S PICKS</span><span aria-hidden="true">✳</span></div><h2>Good things.<br>Worth your time.</h2><p class="aside-desc">Take the scenic route through culture.</p>{''.join(radar(s) for s in picks)}<a class="aside-more" href="{'search' if slug=='index' else 'weekend'}.html">{'Browse all 24 stories' if slug=='index' else 'Visit the Weekend Edit'}</a></aside></section>'''
 body=intro('THE '+name.upper()+' EDIT',heading,description)+hero
 if slug=='index':
  body+='<section class="desk-directory" aria-label="Explore the sections">'+''.join(f'<a href="{key}.html"><span class="eyebrow">{label}</span><strong>{tagline}</strong><span>Explore 6 stories</span></a>' for key,label,tagline in [('entertainment','SCREEN','For the love of a story.'),('music','SOUND','A different frequency.'),('gaming','PLAY','A world worth entering.'),('fashion','STYLE','Make it your own.')])+'</section>'
  body+=browse(items,page_size=9)+ad(slug)
  for key,(label,_,desc,_) in list(SECTIONS.items())[1:]:
   group=category_items(label)[-3:]
   body+=f'<section class="category-strip"><div class="section-heading"><div><p class="eyebrow">THE {label.upper()} DESK</p><h2>{label}</h2></div><a class="text-link" href="{key}.html">Visit {label.lower()}</a></div><div class="story-grid">'+''.join(card(s) for s in group)+'</div></section>'
 else:
  body+=f'<section class="section-note"><span class="eyebrow">FROM THE DESK</span><p>{E(description)} Six reads to help you see familiar things a little differently.</p></section>'+browse(items,category=name,page_size=6)+ad(slug)
  cross=[s for s in STORIES if s['category']!=name][:3]
  body+='<section class="category-strip"><div class="section-heading"><h2>Outside your usual</h2><a class="text-link" href="index.html">Discover more</a></div><div class="story-grid">'+''.join(card(s) for s in cross)+'</div></section>'
 write(slug,name,description,body+closing(),slug,slug)

for s in STORIES:
 theme=s['category'].lower()
 group=category_items(s['category'])
 current=group.index(s)
 previous=group[(current-1)%len(group)]
 following=group[(current+1)%len(group)]
 related=[x for x in group if x['id']!=s['id']][:3]
 toc=''.join(f'<a href="#section-{i}">{E(sec["heading"])}</a>' for i,sec in enumerate(s['sections'],1))
 paragraphs=''.join(f'<section id="section-{i}"><h2>{E(sec["heading"])}</h2>'+''.join(f'<p>{E(p)}</p>' for p in sec['paragraphs'])+'</section>' for i,sec in enumerate(s['sections'],1))
 body=f'''<nav class="breadcrumbs" aria-label="Breadcrumb"><a href="index.html">Discover</a><span>/</span><a href="{theme}.html">{s['category']}</a><span>/</span><span>{E(s['topic'])}</span></nav><header class="article-heading"><p class="eyebrow">{E(s['category'])} / {E(s['topic'])}</p><h1>{E(s['title'])}</h1><p class="article-deck">{E(s['desc'])}</p><div class="article-byline"><span class="author-badge" aria-hidden="true">✳</span><div><strong>{s['author']}</strong><span>Culture Issue · {s['minutes']} min read</span></div><button class="button" data-save="{s['id']}" aria-pressed="false">Save story</button><button class="share-button" data-share>Copy link</button></div><p class="action-status" role="status"></p></header><figure class="article-figure">{img(s,False)}<figcaption>{E(ALTS[s['image']])}. Editorial illustration.</figcaption></figure><div class="article-layout"><aside class="article-toc"><p class="eyebrow">IN THIS STORY</p>{toc}<a class="back-category" href="{theme}.html">More from {s['category']}</a></aside><article class="article-body">{paragraphs}<blockquote>“{E(s['desc'])}”</blockquote><p class="article-disclosure">An original Offbeat demo essay. This is evergreen editorial content, not a reported interview or live news article.</p><div class="article-end"><span class="eyebrow">KEEP THIS ONE</span><p>Something to come back to?</p><button class="button" data-save="{s['id']}" aria-pressed="false">Save story</button><a class="text-link" href="reading-list.html">Open your reading list</a></div></article></div>{ad(s['id'])}<nav class="article-next" aria-label="More articles"><a href="{url(previous)}"><span class="eyebrow">PREVIOUS READ</span><strong>{E(previous['title'])}</strong></a><a href="{url(following)}"><span class="eyebrow">NEXT READ</span><strong>{E(following['title'])}</strong></a></nav><section class="category-strip"><div class="section-heading"><h2>Keep the curiosity going</h2><a class="text-link" href="{theme}.html">All {s['category'].lower()} stories</a></div><div class="story-grid">{''.join(card(x) for x in related)}</div></section>'''
 write('story-'+s['id'],s['title'],s['desc'],body,theme,theme)

write('search','Explore all stories','Find your next read across music, entertainment, gaming, and fashion.',intro('THE ARCHIVE','Follow a thread. Find a story.','Search by title, description, topic, or category. All 24 stories, in one place.')+browse(STORIES,page_size=12))
write('reading-list','Your reading list','A personal collection of Offbeat stories, saved in this browser.',intro('YOUR OWN LITTLE CORNER','Good reads. Kept close.','Your saved stories live in this browser. Pick up where your curiosity left off.')+'<section class="saved-page"><p id="storage-note" role="status">Your list is stored on this device. No account needed.</p><div id="saved-stories" class="saved-grid" aria-live="polite"></div><a class="button" href="search.html">Find your next read</a></section>')
weekend=[('WATCH','Set the scene','Make a film night feel like an occasion.','movie-night'),('LISTEN','Give a record your attention','One album. A comfortable chair. Nothing on shuffle.','album-front-to-back'),('PLAY','Make it a shared adventure','Find the kind of challenge everyone can enjoy.','co-op-night'),('WEAR','Rediscover a good combination','Your favourite outfit deserves another outing.','repeat-outfits')]
body=intro('THE WEEKEND EDIT','Four good ways to slow down.','A small collection for your time off. Something to watch, something to hear, a reason to play, and a little personal style.')
for label,title,desc,id in weekend:
 s=BY_ID[id]
 body+=f'<section class="weekend-feature"><a class="weekend-image" href="{url(s)}">{img(s)}</a><div><p class="eyebrow">{label} / THE WEEKEND EDIT</p><h2>{title}</h2><p>{desc}</p><h3><a href="{url(s)}">{E(s["title"])}</a></h3><a class="button" href="{url(s)}">Read the guide</a></div></section>'
body+='<section class="category-strip"><div class="section-heading"><h2>Leave room for a detour</h2><a class="text-link" href="search.html">The full archive</a></div><div class="story-grid">'+''.join(card(BY_ID[id]) for id in ['short-films','make-a-mixtape','game-photo-mode'])+'</div></section>'
write('weekend','The Weekend Edit','Four ways to make more of your time off: watch, listen, play, and wear.',body,'entertainment')
write('about','About Offbeat','An independent-minded demo magazine about the culture we make time for.',intro('HELLO, WE’RE OFFBEAT','A little off the mainstream.','A magazine-shaped space for music, screen culture, games, and personal style.')+'''<section class="about-grid"><div class="about-mark" aria-hidden="true">✳</div><article class="article-body"><h2>For people with more than one interest.</h2><p>You can care about a film’s final frame and the right song for the journey home. You can love a difficult game and a familiar outfit. Offbeat brings those interests into the same room.</p><p>Our edit is built around attention: listen to a whole record, notice how a story sounds, play with someone new, and look again at the things you already own.</p><h2>The shape of this edition</h2><p>Explore four culture desks, six articles in each section, and a Weekend Edit that connects them. Every article has its own page, related reading, and a place in your personal reading list.</p><h2>A note on this website</h2><p>Offbeat is a demonstration magazine. The essays are original illustrative content. They are not live news, reported interviews, release announcements, or reviews based on hands-on access. Images illustrate themes rather than document the stories.</p><h2>Your reading list</h2><p>Saving a story stores its identifier in this browser. There is no account or server-side reading history. Remove a story from your list to remove its saved identifier. Clearing browser storage also clears the list.</p><h2>What is available</h2><p>All article links, category sections, search, topic filters, sorting, pagination, sharing, and saved-story controls work. The site does not offer ticket sales, accounts, subscriptions, or audio streaming.</p><a class="button" href="index.html">Start exploring</a></article></section>''')
# Remove only obsolete generated HTML pages, preserving unrelated files.
manifest=OUT/'.generated-pages.json'
if manifest.exists():
 for name in json.loads(manifest.read_text()):
  if name not in PAGES and Path(name).name==name and name.endswith('.html'):
   (OUT/name).unlink(missing_ok=True)
manifest.write_text(json.dumps(PAGES,indent=2)+'\n')
print(f'Built {len(PAGES)} pages, {len(STORIES)} dedicated articles. Shared head scripts included on every page.')
