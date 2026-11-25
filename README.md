# OFFBEAT — Culture, without the algorithm

An independent, English-language editorial demo inspired by the static, multi-page structure of `COAD_Demo`. Built with HTML, CSS, vanilla JavaScript, and a Python standard-library page builder. Source repository: https://github.com/miraveil/mel-sample.

## Start locally

From this repository directory:

```sh
python3 scripts/build.py
python3 -m http.server 4173 --directory dist
```

Open http://localhost:4173. Serve over HTTP rather than opening HTML files directly, because articles load a local JSON file. No dependency installation is required. Upload the contents of `dist/` to any static host to deploy.

## Deploy on Vercel

The repository includes `vercel.json`. Import `miraveil/mel-sample` and keep **Root Directory** at the repository root (leave it empty, or use `.`). The configuration selects the static-site preset, builds and verifies the magazine, then serves `dist/`.

| Setting | Value |
| --- | --- |
| Framework Preset | Other |
| Root Directory | Repository root; not `dist` |
| Build Command | `python3 scripts/build.py && python3 scripts/check.py` |
| Output Directory | `dist` |

The build command and output directory are versioned in `vercel.json`. A deployment from `main` rebuilds all pages, so edits to `shared/head-scripts.html` are included automatically after committing and pushing them.

If an older deployment displays `404 NOT_FOUND`, deploy the latest `main` commit containing `vercel.json`. Check that the project is connected to this repository and that Root Directory points to the repository root. If automatic Git deployments are disabled, trigger a new deployment from the latest commit in the Vercel dashboard. Redeploying an older commit does not include this fix.

## 33 pages, five supplied palettes

| Page | Reference | Palette |
| --- | --- | --- |
| Discover (`index.html`) | Image 1 | `#F3EDDE`, `#CFD11A`, `#436D49`, `#ABC0B2`, `#1C0103` |
| Music (`music.html`) | Image 2 | `#768340`, `#060409`, `#51375B`, `#5A3598`, `#AE9ABB` |
| Gaming (`gaming.html`) | Image 3 | `#102B53`, `#50698D`, `#CEB5D4`, `#4E7AB1`, `#7D9FC0` |
| Fashion (`fashion.html`) | Image 4 | `#BDC7C0`, `#85222F`, `#5F0309`, `#4A0A0F`, `#220B09` |
| Entertainment (`entertainment.html`) | Image 5 | `#F9EFBD`, `#F0DC92`, `#D2A941`, `#946C18`, `#975B09` |

Additional neutral shades support readable text, overlays, and borders. The hex labels in the supplied references take precedence when a printed RGB value differs.

## Add scripts to every page head

1. Open **`shared/head-scripts.html`**.
2. Paste complete script tags **outside the existing HTML comment**. External scripts, inline scripts, and provider-specific attributes are supported.
3. Run `python3 scripts/build.py`.
4. Refresh the preview or upload the updated `dist/` folder.

The builder copies this file verbatim inside the `<head>` of all 33 pages, including every article and collection, before the site JavaScript. It supports native parser execution; no client-side HTML injection is used. Changes become active after rebuilding. Do not edit generated page heads directly.

```html
<script async src="https://your-script-provider.example/tag.js"
        data-site="your-site-code"></script>
```

Use your real provider URL and attributes. No advertising or tracking scripts are active by default. Scripts that modify the visible `<header>` must wait for `DOMContentLoaded` or use `defer`.

## The expanded magazine

- 1 Discover homepage with a cover feature, editor’s picks, section directory, archive, and four category desks.
- 4 category hubs: Entertainment, Music, Gaming, Fashion. Each contains six articles and topic filters.
- 24 dedicated article pages with a headline, deck, reading time, byline, hero image, three sections, contents links, save controls, previous/next reading, and related stories.
- 1 Weekend Edit collection connecting watch, listen, play, and style.
- 1 searchable archive with category filters, sorting, and pagination.
- 1 reading-list page with saved stories and individual remove controls.
- 1 About page explaining the magazine and demo scope.

Articles inherit their category palette. Discover, Search, About, and Reading List use the green palette; Weekend Edit uses the gold palette.

## Interactions

- Category links and article images/titles open real standalone pages.
- Search matches title, description, topic, and category. Search terms are reflected in the URL and restored on refresh.
- Category filters on Discover/Search and topic filters on category hubs combine with search. Filters and sorting reset on navigation or refresh.
- Sort by editorial order, title A–Z, or reading time. Discover displays nine results per page; Search displays twelve. Previous/Next controls are disabled at their boundaries. Single-page results hide pagination.
- Zero results offer Reset filters. Reset clears the query, filter, and sorting.
- Save/remove buttons on article pages update together. Saved stories persist across pages using browser local storage. The dedicated reading list supports individual removal and a useful empty state.
- Browser storage failures display a message. Cross-tab storage updates refresh saved counts and lists.
- Copy link uses the browser clipboard; a selectable link field is displayed if clipboard access fails.
- Previous/next article links stay within the article’s category. Related cards offer additional reading.
- Legacy `?story=` URLs from the first edition redirect to their matching article pages.
- Links use hover underlines and pointer cursors. Buttons have hover/focus feedback. Disabled pagination uses dashed borders, reduced opacity, and an unavailable cursor.
- No account, ticket sales, subscriptions, audio stream, or fabricated news feed is presented.

## Advertising demo mounts

Each main hub and article page includes a collapsed, unfilled `<ins class="cox-ad-unit">` after the latest stories, with a distinct `offbeat_<page>_midfeed` code. Replace it with an actual configured unit code when integrating. Empty mounts show no advertisement label or reserved blank space. These are demonstration mounts, not claims of a configured COAD integration. The source template's deployment instructions and publisher identifiers are not copied into live configuration.

## Editing

- `scripts/build.py`: page metadata, navigation, layouts, and shared markup.
- `content/stories.json`: the 24 editorial articles and their category/topic metadata.
- `scripts/check.py`: generated link, asset, fragment, heading, content, and shared-head verification.
- `assets/site.css`: responsive layout, five themes, and interaction styles.
- `assets/site.js`: search, filters, sorting, pagination, sharing, and the local reading list.
- `shared/head-scripts.html`: the single source for head scripts across every page.
- `dist/`: ready-to-serve output; regenerate after editing sources.

All editorial content is illustrative, not live news or verified reporting. There are no accounts, audio streams, or subscriptions. All photos are stored locally, so the finished website does not request remote images or fonts.

## Image credits

`concert.jpg` and `crowd.jpg` are reused from the supplied demo. See `REFERENCE-CREDITS.md` for the original asset credits (the full reference inventory is preserved, including assets not used here).

Additional Unsplash source images (saved locally):

- Fashion: https://images.unsplash.com/photo-1483985988355-763728e1935b
- Cinema: https://images.unsplash.com/photo-1489599849927-2ee91cede3ba
- Gaming: https://images.unsplash.com/photo-1493711662062-fa541adb3fc8
- Microphone: https://images.unsplash.com/photo-1516280440614-37939bbacd81
- Studio: https://images.unsplash.com/photo-1511671782779-c97d3d27a1d4
- Film: https://images.unsplash.com/photo-1485846234645-a62644f84728
- Controller: https://images.unsplash.com/photo-1614294149010-950b698f72c0
- Wardrobe: https://images.unsplash.com/photo-1441986300917-64674bd600d8

## Verification

```sh
python3 scripts/build.py
python3 scripts/check.py
node --check assets/site.js
```

All 33 generated pages are checked for local link targets, section anchors, exactly one main heading, unique IDs, and the shared head content. The content check verifies 24 unique articles and six articles in each category. Browser checks cover pagination, search/no results/reset, category/topic filters, title sorting, article navigation, saving across pages, and removal. Mobile layout checks cover the five palettes and the new page layouts. Real third-party script behavior requires a configured provider script and unit codes.
