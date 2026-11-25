# OFFBEAT — Culture, without the algorithm

An independent, English-language editorial demo inspired by the static, multi-page structure of `COAD_Demo`. Built with HTML, CSS, vanilla JavaScript, and a Python standard-library page builder. This is a separate local repository; it has not been uploaded or published.

## Start locally

From this repository directory:

```sh
python3 scripts/build.py
python3 -m http.server 4173 --directory dist
```

Open http://localhost:4173. Serve over HTTP rather than opening HTML files directly, because articles load a local JSON file. No dependency installation is required. Upload the contents of `dist/` to any static host to deploy.

## Five pages, five supplied palettes

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

The builder copies this file verbatim inside the `<head>` of all five pages, before the site JavaScript. It supports native parser execution; no client-side HTML injection is used. Changes become active after rebuilding. Do not edit generated page heads directly.

```html
<script async src="https://your-script-provider.example/tag.js"
        data-site="your-site-code"></script>
```

Use your real provider URL and attributes. No advertising or tracking scripts are active by default. Scripts that modify the visible `<header>` must wait for `DOMContentLoaded` or use `defer`.

## Interactions

- Navigation opens five real pages, with the current section underlined.
- Story images include a “Read story” label. Titles, article buttons, navigation, and saved stories are links.
- Links have pointer cursors and hover underlines. Buttons have hover feedback; keyboard controls have visible focus outlines.
- “Coming soon” is a native disabled button with a dashed border, reduced opacity, and an unavailable cursor.
- Search matches story titles, case-insensitively. Category and search conditions combine. Filters reset when navigating or refreshing; zero results offer Reset filters.
- Articles open in an accessible modal with a shareable `?story=` URL. Close, Escape, and clicking outside the modal dismiss it.
- Save/remove stories using the article control. The reading list is shared across all pages in the same browser using local storage. If storage is blocked, it lasts for the current page visit.
- Article loading failures and unknown story IDs display explicit messages.
- Layout adapts to mobile, tablet, and desktop. Motion respects reduced-motion preferences.

## Advertising demo mounts

Each page includes a collapsed, unfilled `<ins class="cox-ad-unit">` after the latest stories, with a distinct `offbeat_<page>_midfeed` code. Replace it with an actual configured unit code when integrating. Empty mounts show no advertisement label or reserved blank space. These are demonstration mounts, not claims of a configured COAD integration. The source template's deployment instructions and publisher identifiers are not copied into live configuration.

## Editing

- `scripts/build.py`: page metadata, editorial text, navigation, and shared markup.
- `assets/site.css`: responsive layout, five themes, and interaction styles.
- `assets/site.js`: search, filters, reading room, and local reading list.
- `shared/head-scripts.html`: the single source for head scripts across every page.
- `dist/`: ready-to-serve output; regenerate after editing sources.

All editorial content is illustrative, not live news or verified reporting. There are no accounts, audio streams, or subscriptions. All photos are stored locally, so the finished website does not request remote images or fonts.

## Image credits

`concert.jpg` and `crowd.jpg` are reused from the supplied demo. See `REFERENCE-CREDITS.md` for the original asset credits (the full reference inventory is preserved, including assets not used here).

Additional Unsplash source images:

- Fashion: https://images.unsplash.com/photo-1483985988355-763728e1935b
- Cinema: https://images.unsplash.com/photo-1489599849927-2ee91cede3ba
- Gaming: https://images.unsplash.com/photo-1493711662062-fa541adb3fc8

## Verification

The build and JavaScript syntax checks passed. Browser checks covered article open/close, save/remove, category filtering, empty search results, filter reset, disabled controls, and all five pages at a 390px mobile viewport with no horizontal overflow. Desktop visual review used the Discover page. Real third-party script behavior requires the provider's configured script and unit codes.
