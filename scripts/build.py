"""Build five standalone pages; inject shared/head-scripts.html into every head."""
from pathlib import Path
import html
import shutil

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / 'dist'
OUT.mkdir(exist_ok=True)
shutil.copytree(ROOT / 'assets', OUT / 'assets', dirs_exist_ok=True)
head_scripts = (ROOT / 'shared/head-scripts.html').read_text()
pages = [
    ('index', 'Discover', 'Culture, without the algorithm.', 'Your next obsession starts here. A considered mix of music, screen culture, games, and personal style.', 'The art of getting lost in a live show', 'Music', 'concert.jpg', 'Inside the moments that turn a room full of strangers into a community.', 'Read the story'),
    ('entertainment', 'Entertainment', 'A different kind of screen time.', 'From the opening frame to the closing credits. Stories for people who love a good story.', 'Why the small cinema still matters', 'Screen culture', 'cinema.jpg', 'A love letter to the shared silence, the big screen, and the stories we carry home.', 'Read the feature'),
    ('music', 'Music', 'Find your new frequency.', 'Sounds worth sitting with. Meet the scenes, spaces, and ideas behind the music.', 'Get there for the opening act', 'Live music', 'crowd.jpg', 'Beyond the setlist: the little things that make a night of live music unforgettable.', 'Read the feature'),
    ('gaming', 'Gaming', 'Play outside the usual.', 'New worlds, thoughtful design, and the joy of pressing start. For the curious player.', 'The joy of playing together', 'Player culture', 'gaming.jpg', 'How a shared screen becomes a place to connect, compete, and make memories.', 'Read the feature'),
    ('fashion', 'Fashion', 'Wear your point of view.', 'Personal style over passing trends. Explore the details that make a look your own.', 'A wardrobe that feels like you', 'Personal style', 'fashion.jpg', 'Less chasing trends, more finding the pieces you want to live in.', 'Read the feature'),
]
stories = [
    dict(id='live-show', category='Music', title='The art of getting lost in a live show', image='concert.jpg', desc='The best nights are the ones when you forget to check your phone.', body=['There is a particular moment at a live show when the room changes. A familiar rhythm arrives, conversations fall away, and attention settles on the same small patch of stage.', 'Try arriving before the opening act. Notice how the room sounds from the back, give the support artist your attention, and leave room for a song you do not know. Curiosity is often a better guide than a perfect setlist.', 'Bring hearing protection, respect the people around you, and let a few moments pass without recording them. Sometimes the best souvenir is simply remembering how it felt.']),
    dict(id='small-cinema', category='Entertainment', title='Why the small cinema still matters', image='cinema.jpg', desc='A big-screen ritual with a very human scale.', body=['A small cinema makes a film feel like a local event. The lobby, the familiar seats, and a room of people choosing to watch together become part of the experience.', 'Choose something outside your usual genre. Read the programme notes after the film, sit through the credits, and compare impressions with a friend. A screening can be the beginning of a conversation.', 'At home, borrow the ritual: put your phone away, lower the lights, and give one story your full attention. The room matters, but so does the intention.']),
    dict(id='shared-screen', category='Gaming', title='The joy of playing together', image='gaming.jpg', desc='Make room on the sofa. Some worlds are better shared.', body=['Playing together gives ordinary evenings a little structure: a shared challenge, a surprising mistake, and a reason to try one more time.', 'Start with a game that welcomes everyone at the table. Explain one mechanic at a time, take breaks, and make space for different levels of experience. The point is a good evening together.', 'Cooperative games are useful when competition gets in the way. Pick a shared goal, talk through your plan, and celebrate the small saves as much as the final win.']),
    dict(id='personal-style', category='Fashion', title='A wardrobe that feels like you', image='fashion.jpg', desc='Build around the pieces you reach for, again and again.', body=['Personal style often begins with noticing what already works. The jacket you always take, the shoes you can walk in, and the colour that makes an ordinary day feel brighter are useful clues.', 'Choose a few favourites and try them in unfamiliar combinations. Change a proportion, repeat a colour, or add one textured layer. Photograph the combinations you want to remember.', 'Before buying something new, imagine how it fits into three outfits you already wear. Taking care of your clothes and making considered repairs can be part of the same creative process.']),
    dict(id='opening-act', category='Music', title='Get there for the opening act', image='crowd.jpg', desc='Your next favourite sound might be on stage early.', body=['An opening set is an invitation to arrive without expectations. You may not know the words, but that can make listening more attentive.', 'Find a comfortable spot, give the artist a full song before deciding, and note a track name if something stays with you. Discovery does not have to happen on a feed.', 'If you enjoy the set, look for the artist’s official releases afterwards. A little curiosity can turn an early arrival into the highlight of the night.']),
]
import json
(OUT / 'assets/stories.json').write_text(json.dumps(stories))
for slug, name, heading, intro, feature, category, image, desc, cta in pages:
    nav = ''.join(f'<a href="{s}.html" {"aria-current=page" if s == slug else ""}>{n}</a>' for s,n,*_ in pages)
    featured = next(s for s in stories if s['title'] == feature)
    ordered = sorted(stories, key=lambda s: s['category'] != name) if slug != 'index' else stories
    cards = ''.join(f'''<article class="story-card" data-category="{s['category']}" data-search="{html.escape(s['title'].lower())}">
      <a class="card-image" href="{slug}.html?story={s['id']}" aria-label="Read {html.escape(s['title'])}"><img src="assets/images/{s['image']}" alt="{html.escape(s['desc'])}" loading="lazy" width="700" height="460"><span class="image-label">Read story</span></a>
      <div class="card-meta">{s['category']} <span>· 3 min read</span></div><h3><a href="{slug}.html?story={s['id']}">{s['title']}</a></h3><p>{s['desc']}</p></article>''' for s in ordered)
    document = f'''<!doctype html>
<html lang="en" data-theme="{slug}">
<head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>{name} — OFFBEAT</title><meta name="description" content="{intro}">
<link rel="icon" href="assets/favicon.svg" type="image/svg+xml"><link rel="stylesheet" href="assets/site.css">
<!-- Centralized head scripts: edit shared/head-scripts.html and rebuild. -->
{head_scripts}
<script src="assets/site.js" defer></script></head>
<body><a class="skip" href="#main">Skip to content</a>
<div class="topline"><div class="container"><span>INDEPENDENT MINDS. SHARED OBSESSIONS.</span><span>An editorial demo · Vol. 01</span></div></div>
<header class="container"><div class="masthead"><a class="brand" href="index.html" aria-label="Offbeat home">offbeat<span>✳</span></a><span class="brand-note">A little off the mainstream.<br>A lot more interesting.</span><a class="pill" href="#reading-list">Your reading list <span class="saved-count">0</span></a></div>
<div class="nav-row"><nav aria-label="Main navigation">{nav}</nav><a class="search-link" href="#search">Search <svg width="17" height="17" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="10" cy="10" r="6"/><path d="m15 15 5 5"/></svg></a></div></header>
<main id="main" class="container"><section class="intro"><div><p class="eyebrow">THE {name.upper()} EDIT</p><h1>{heading}</h1></div><p>{intro}</p></section>
<section class="feature-grid" aria-label="Featured stories"><article class="hero"><img src="assets/images/{image}" alt="{html.escape(desc)}" width="1400" height="900"><div class="hero-shade"></div><div class="hero-copy"><span class="tag">THE COVER STORY</span><p class="hero-category">{category} / Long reads</p><h2><a href="{slug}.html?story={featured['id']}">{feature}</a></h2><p>{desc}</p><a class="button button-light" href="{slug}.html?story={featured['id']}">{cta}</a></div></article>
<aside class="editors"><div class="aside-heading"><span class="eyebrow">ON OUR RADAR</span><span aria-hidden="true">✳</span></div><h2>Good things.<br>Worth your time.</h2><p class="aside-desc">A few places to start when you want something different.</p>
{''.join(f'<a class="radar-item" href="{slug}.html?story={s["id"]}"><span class="card-meta">{s["category"]}</span><h3>{s["title"]}</h3><span class="read-label">Read story</span></a>' for s in ordered[:3])}
<div class="soon"><span>OFFBEAT RADIO</span><button disabled title="Offbeat Radio is not available in this demo">Coming soon</button></div></aside></section>
<section class="latest" aria-labelledby="latest-title"><div class="section-heading"><div><p class="eyebrow">STAY CURIOUS</p><h2 id="latest-title">The latest edit<span>✳</span></h2></div><span class="muted">Fresh perspectives. No endless scrolling.</span></div>
<div class="filter-bar"><div class="filters" role="group" aria-label="Filter stories">{''.join(f'<button class="filter" data-filter="{c}" aria-pressed="{str(c == "All").lower()}">{c}</button>' for c in ['All','Entertainment','Music','Gaming','Fashion'])}</div><label class="search-field" id="search"><span class="sr-only">Search story titles</span><input type="search" placeholder="Search stories…" aria-label="Search story titles"></label></div>
<p id="result-status" class="sr-only" role="status"></p><div class="story-grid">{cards}</div><div class="empty" hidden>No stories found. Try another title or choose a different category.<button id="reset" class="button">Reset filters</button></div></section>
<div class="ad-wrap"><span>Advertisement</span><ins class="cox-ad-unit" data-cox-unit="offbeat_{slug}_midfeed" style="display:block;width:100%"></ins></div>
<section class="reading-list" id="reading-list"><div><p class="eyebrow">MAKE IT YOURS</p><h2>A little inspiration, saved for later.</h2><p>Save stories as you read. Your list stays in this browser.</p></div><div id="saved-stories" aria-live="polite"></div></section>
<section class="closing"><span aria-hidden="true">✳</span><div><p class="eyebrow">FOLLOW YOUR CURIOSITY</p><h2>More than one thing.<br>Just like you.</h2></div><a class="button" href="{'music' if slug == 'index' else 'index'}.html">{'Explore music' if slug == 'index' else 'Discover all stories'}</a></section></main>
<footer class="container"><a class="brand" href="index.html">offbeat<span>✳</span></a><p>Music. Screen. Play. Style.<br>Culture for the endlessly curious.</p><span>© 2026 OFFBEAT<br>Illustrative editorial content.</span></footer>
<dialog id="story-dialog" aria-labelledby="dialog-title"><div class="dialog-top"><span class="eyebrow">OFFBEAT / THE READING ROOM</span><button class="close-button" aria-label="Close article">Close ×</button></div><div id="article-content"></div></dialog>
</body></html>'''
    (OUT / f'{slug}.html').write_text(document)
print('Built five pages in dist/. Shared head scripts applied to every page.')
