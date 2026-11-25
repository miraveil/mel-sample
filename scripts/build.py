"""Build OFFBEAT with the reference news site's homepage, category, and article layouts."""
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
ALTS = {'concert.jpg': 'A raised hand in a crowd facing an illuminated concert stage', 'crowd.jpg': 'Festival audience watching a live performance', 'cinema.jpg': 'Rows of red seats in a cinema auditorium', 'film.jpg': 'A film camera and movie-making equipment', 'gaming.jpg': 'A gaming setup with illuminated screens', 'controller.jpg': 'A video game controller', 'fashion.jpg': 'A woman wearing sunglasses and a red coat', 'wardrobe.jpg': 'Clothing arranged in a fashion store', 'studio.jpg': 'Music recording equipment', 'microphone.jpg': 'A microphone ready for a performance'}
PAGES = []


def url(story):
    return f'story-{story["id"]}.html'


def category_items(category):
    return [s for s in STORIES if s['category'] == category]


def img(story, lazy=True):
    loading = ' loading="lazy"' if lazy else ''
    return f'<img src="assets/images/{story["image"]}" alt="{E(ALTS[story["image"]])}" width="1200" height="800"{loading}>'


def meta(story):
    return f'<p class="card-meta">{E(story["topic"])} <span>· {story["minutes"]} min read</span></p>'


def card(story):
    search = E(' '.join(story[k] for k in ('title', 'desc', 'topic', 'category')).lower())
    return f'''<article class="story-card" data-category="{story['category']}" data-topic="{E(story['topic'])}" data-minutes="{story['minutes']}" data-search="{search}">
<a class="card-image" href="{url(story)}" aria-label="Read {E(story['title'])}">{img(story)}</a>
<div class="story-copy"><h3><a href="{url(story)}">{E(story['title'])}</a></h3><p class="story-description">{E(story['desc'])}</p>{meta(story)}</div></article>'''


def compact(story):
    return f'<article class="compact-story"><a class="compact-image" href="{url(story)}" aria-label="Read {E(story["title"])}">{img(story)}</a><div><h3><a href="{url(story)}">{E(story["title"])}</a></h3>{meta(story)}</div></article>'


def ad(slug):
    return f'<div class="ad-wrap"><span>Advertisement</span><ins class="cox-ad-unit" data-cox-unit="offbeat_{slug}_midfeed" style="display:block;width:100%"></ins></div>'


def section_head(title, target, label='View all'):
    return f'<div class="print-head"><h2>{E(title)}</h2><a href="{target}">{E(label)}</a></div>'


def sidebar(items, toc=''):
    selected = items[:5]
    recommendations = items[-3:]
    contents = f'<section class="sidebar-box contents"><h2>In this story</h2>{toc}</section>' if toc else ''
    rank = ''.join(f'<li><a href="{url(s)}">{E(s["title"])}</a></li>' for s in selected)
    return f'''<aside class="sidebar" aria-label="Editor’s selection and related reading">{contents}
<section class="sidebar-box"><h2>Editor’s selection</h2><ol class="rank">{rank}</ol></section>
<section class="sidebar-box"><h2>More to explore</h2>{''.join(compact(s) for s in recommendations)}</section>
<section class="sidebar-box weekend-note"><p class="eyebrow">WATCH · LISTEN · PLAY · WEAR</p><h2>The Weekend Edit</h2><p>Four good ways to make more of your time off.</p><a class="text-link" href="weekend.html">Explore the collection</a></section></aside>'''


def write(slug, title, description, body, theme='index', active=None):
    nav = ''.join(f'<a href="{key}.html" {"aria-current=page" if active == key else ""}>{data[0]}</a>' for key, data in SECTIONS.items())
    ticker = ''
    if slug == 'index':
        headlines = ''.join(f'<a href="{url(BY_ID[id])}">{E(BY_ID[id]["title"])}</a>' for id in ('small-cinema', 'shared-screen', 'personal-style'))
        ticker = f'<div class="headline-band"><div class="container"><span class="headline-label">In the edit</span><div class="headline-track">{headlines}</div></div></div>'
    document = f'''<!doctype html>
<html lang="en" data-theme="{theme}">
<head>
<meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{E(title)} — OFFBEAT</title><meta name="description" content="{E(description)}">
<meta property="og:title" content="{E(title)} — OFFBEAT"><meta property="og:description" content="{E(description)}"><meta property="og:type" content="{'article' if slug.startswith('story-') else 'website'}">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/site.css">
<!-- Shared head scripts: edit shared/head-scripts.html, then rebuild. -->
{HEAD}
<script src="assets/site.js" defer></script>
</head>
<body>
<a class="skip" href="#main">Skip to content</a>
<header class="site-header">
<div class="topbar"><div class="container topbar-inner"><span>The Culture Issue · Editorial demo</span><div><a href="about.html">About Offbeat</a><a href="reading-list.html">Reading list</a></div></div></div>
<div class="container masthead"><a class="brand" href="index.html" aria-label="Offbeat home"><span class="brand-name">offbeat<span>✳</span></span><span class="brand-tagline">Music · Screen · Play · Style</span></a><div class="masthead-tools"><a class="search-link" href="search.html" aria-label="Search stories"><svg width="19" height="19" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="10" cy="10" r="6"/><path d="m15 15 5 5"/></svg></a><a class="button reading-link" href="reading-list.html">Reading list <span class="saved-count">0</span></a></div><button class="menu-toggle" type="button" aria-expanded="false" aria-controls="site-nav">Menu</button></div>
<nav class="site-nav" id="site-nav" aria-label="Main navigation"><div class="container nav-inner">{nav}<a href="weekend.html" {"aria-current=page" if slug == 'weekend' else ""}>Weekend Edit</a></div></nav>
</header>{ticker}
<main id="main" class="container">{body}</main>
<footer class="site-footer"><div class="container footer-grid"><div><a class="brand" href="index.html"><span class="brand-name">offbeat<span>✳</span></span></a><p>Culture for the endlessly curious.<br>Music, screen, play, and personal style.</p></div><div><h2>Sections</h2><nav aria-label="Footer sections">{''.join(f'<a href="{key}.html">{data[0]}</a>' for key, data in SECTIONS.items() if key != 'index')}</nav></div><div><h2>The magazine</h2><nav aria-label="Footer magazine"><a href="about.html">About Offbeat</a><a href="weekend.html">Weekend Edit</a><a href="search.html">Explore all stories</a></nav></div><div><h2>Your reading</h2><nav aria-label="Footer reading"><a href="reading-list.html">Saved stories <span class="saved-count">0</span></a><a href="search.html">Find a story</a></nav><p>Original illustrative editorial content.</p></div></div><div class="container footer-bottom"><span>© 2026 OFFBEAT</span><span>A little off the mainstream. A lot more interesting.</span></div></footer>
</body></html>'''
    (OUT / f'{slug}.html').write_text(document)
    PAGES.append(slug + '.html')


def intro(kicker, title, description):
    return f'<section class="page-head"><p class="eyebrow">{E(kicker)}</p><h1>{E(title)}</h1><p>{E(description)}</p></section>'


def browse(items, category=None, page_size=9):
    topics = sorted({s['topic'] for s in items})
    if category:
        filters = ''.join(f'<button class="filter" data-topic-filter="{E(topic)}" aria-pressed="{str(topic == "All topics").lower()}">{E(topic)}</button>' for topic in ['All topics'] + topics)
    else:
        filters = ''.join(f'<button class="filter" data-filter="{value}" aria-pressed="{str(value == "All").lower()}">{value}</button>' for value in ['All', 'Entertainment', 'Music', 'Gaming', 'Fashion'])
    return f'''<section class="browse" data-page-size="{page_size}" aria-labelledby="latest-title">
<h2 class="sr-only" id="latest-title">{'All '+category.lower()+' stories' if category else 'Explore the archive'}</h2>
<div class="filters" role="group" aria-label="Filter stories">{filters}</div>
<div class="browse-controls"><label class="search-field"><span class="sr-only">Search stories</span><input type="search" placeholder="Search stories…" aria-label="Search stories"></label><label class="sort-label">Order <select id="sort" aria-label="Sort stories"><option value="editorial">Editorial order</option><option value="title">Title A–Z</option><option value="short">Shortest reads</option></select></label></div>
<p id="result-status" class="result-status" role="status"></p>
<div class="story-grid story-list">{''.join(card(s) for s in items)}</div>
<div class="empty" hidden>No stories found. Try a different title, topic, or category.<button id="reset" class="button">Reset filters</button></div>
<nav class="pagination" aria-label="Story pages"><button class="button" id="previous">Previous</button><span id="page-status"></span><button class="button" id="next">Next</button></nav></section>'''


def print_section(category, mode='columns'):
    key = category.lower()
    items = category_items(category)
    if mode == 'columns':
        contents = '<div class="print-cols">' + ''.join(card(s) for s in items[:3]) + '</div>'
    else:
        contents = '<div class="print-list">' + ''.join(compact(s) for s in items[:3]) + '</div>'
    return f'<section class="print-section" aria-label="{category}">{section_head(category, key+".html")}{contents}</section>'


# Homepage: lead and latest sidebar, full-width category blocks, paired lists,
# photo-led stories, and a closing editorial selection, following news/index.html.
lead = BY_ID['live-show']
latest_ids = ['movie-night', 'album-front-to-back', 'co-op-night', 'repeat-outfits', 'short-films', 'music-credits', 'game-photo-mode']
latest = ''.join(f'<li><a class="latest-thumb" href="{url(BY_ID[id])}" aria-label="Read {E(BY_ID[id]["title"])}">{img(BY_ID[id])}</a><div><span class="latest-category">{BY_ID[id]["category"]}</span><a href="{url(BY_ID[id])}">{E(BY_ID[id]["title"])}</a></div></li>' for id in latest_ids)
body = f'''<section class="front" aria-labelledby="front-title"><article class="front-lead"><a class="front-lead-media" href="{url(lead)}" aria-label="Read {E(lead['title'])}">{img(lead, False)}</a><p class="kicker">Music · Live culture</p><h1 id="front-title"><a href="{url(lead)}">{E(lead['title'])}</a></h1><p class="front-sapo">{E(lead['desc'])} Inside the moments that turn a room full of strangers into a community.</p><p class="byline">The Offbeat Edit <span>·</span> Culture Issue <span>·</span> {lead['minutes']} min read</p></article><aside class="front-latest" aria-labelledby="front-latest-title"><h2 id="front-latest-title">Latest in the edit</h2><ul>{latest}</ul></aside></section>'''
body += print_section('Music') + ad('index')
body += '<div class="print-split">' + print_section('Entertainment', 'list') + print_section('Gaming', 'list') + '</div>'
body += print_section('Fashion')
photo_ids = ['short-films', 'make-a-mixtape', 'game-photo-mode']
body += '<section class="print-section photo-section">' + section_head('A different perspective', 'weekend.html', 'Weekend Edit') + '<div class="photo-grid">' + ''.join(f'<a href="{url(BY_ID[id])}">{img(BY_ID[id])}<span>{E(BY_ID[id]["title"])}</span></a>' for id in photo_ids) + '</div></section>'
body += '<section class="editor-selection">' + section_head('Editor’s selection', 'search.html', 'Explore all stories') + '<ol>' + ''.join(f'<li><span>{s["category"]}</span><a href="{url(s)}">{E(s["title"])}</a></li>' for s in [BY_ID[id] for id in ['music-credits', 'sound-of-film', 'backlog', 'secondhand', 'spoiler-etiquette']]) + '</ol></section>'
write('index', 'Discover', SECTIONS['index'][2], body, 'index', 'index')

# Category pages: breadcrumb, title, topic controls, horizontal story rows and rail.
for slug, (name, heading, description, _) in list(SECTIONS.items())[1:]:
    items = category_items(name)
    others = [s for s in STORIES if s['category'] != name][:5]
    breadcrumb = f'<nav class="breadcrumbs" aria-label="Breadcrumb"><a href="index.html">Discover</a><span>/</span><span aria-current="page">{name}</span></nav>'
    body = breadcrumb + f'<section class="page-head category-head"><h1>{name}</h1><p>{E(description)}</p></section>'
    body += '<div class="news-layout"><div class="news-main">' + browse(items, category=name, page_size=6) + ad(slug) + '</div>' + sidebar(others) + '</div>'
    write(slug, name, description, body, slug, slug)

# Article pages: headline, standfirst, hero, and prose all share the main column.
for story in STORIES:
    theme = story['category'].lower()
    group = category_items(story['category'])
    current = group.index(story)
    previous = group[(current - 1) % len(group)]
    following = group[(current + 1) % len(group)]
    related = [s for s in group if s['id'] != story['id']]
    toc = ''.join(f'<a href="#section-{i}">{E(section["heading"])}</a>' for i, section in enumerate(story['sections'], 1))
    paragraphs = ''.join(f'<section id="section-{i}"><h2>{E(section["heading"])}</h2>' + ''.join(f'<p>{E(text)}</p>' for text in section['paragraphs']) + '</section>' for i, section in enumerate(story['sections'], 1))
    body = f'''<nav class="breadcrumbs" aria-label="Breadcrumb"><a href="index.html">Discover</a><span>/</span><a href="{theme}.html">{story['category']}</a><span>/</span><span>{E(story['topic'])}</span></nav>
<div class="news-layout article-page"><article class="article-main"><header class="article-heading"><p class="kicker">{E(story['category'])} · {E(story['topic'])}</p><h1>{E(story['title'])}</h1><p class="article-deck">{E(story['desc'])}</p><p class="byline">By <strong>{story['author']}</strong> <span>·</span> Culture Issue <span>·</span> {story['minutes']} min read</p><div class="article-actions"><button class="button" data-save="{story['id']}" aria-pressed="false">Save story</button><button class="share-button" data-share>Copy link</button></div><p class="action-status" role="status"></p></header>
<figure class="article-figure">{img(story, False)}<figcaption>{E(ALTS[story['image']])}. Editorial illustration.</figcaption></figure>
<div class="article-body">{paragraphs}<blockquote>{E(story['desc'])}</blockquote></div>
<div class="article-tags"><a href="{theme}.html">{story['category']}</a><a href="{theme}.html?q={E(story['topic'])}">{E(story['topic'])}</a></div>
<p class="article-disclosure">Original illustrative editorial content from the Offbeat demo edition.</p>
{ad(story['id'])}<div class="article-end"><h2>Save this story for another day</h2><button class="button" data-save="{story['id']}" aria-pressed="false">Save story</button><a class="text-link" href="reading-list.html">Open your reading list</a></div>
<section class="related-section">{section_head('Related stories', theme+'.html')}<div class="story-grid related-grid">{''.join(card(s) for s in related[:3])}</div></section>
<nav class="article-next" aria-label="More articles"><a href="{url(previous)}"><span>Previous read</span><strong>{E(previous['title'])}</strong></a><a href="{url(following)}"><span>Next read</span><strong>{E(following['title'])}</strong></a></nav></article>{sidebar(related, toc)}</div>'''
    write('story-' + story['id'], story['title'], story['desc'], body, theme, theme)

write('search','Explore all stories','Find your next read across music, entertainment, gaming, and fashion.',intro('THE ARCHIVE','Explore all stories','Search by title, description, topic, or category. All 24 stories, in one place.')+'<div class="news-layout"><div class="news-main">'+browse(STORIES,page_size=12)+'</div>'+sidebar(STORIES[:5])+'</div>')
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
