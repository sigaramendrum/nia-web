# nia-web

The public website for NIA: **niapower.org** (GitHub Pages, built with Jekyll).

**PUBLIC repo.** Only content that is already public or meant for the site. No finance data, no
private personal data, no `_system`. Planning notes live in the private `nia` repo
(`20_marketing/website/`). Student stories here are the ones published with the student's consent.

## How the site is built (2026-11-26)
The pages mirror the Squarespace site exactly, at desktop and phone widths. Each page keeps
Squarespace's section-and-grid layout: every block's position is in the page's own `<style>`, for
desktop and for phones. Arun asked for the same layout with no visible change.

| To change | Edit |
|---|---|
| Text on a page | The page's `.html` file (e.g. `about.html`; `index.html` is the home page; stories are in `stories/`). Change the words inside the existing tags. |
| Top menu | `_data/navigation.yml` (`main:`) and `_includes/mirror-header.html` |
| Footer | `_includes/mirror-footer.html` |
| Colours, fonts, spacing | `assets/css/mirror.css` (section themes are at the top) |
| Grid row heights measured from the old site | `assets/css/rows.css` (generated; normally leave alone) |
| Images | `assets/images/` (WebP). Keep the `alt` text describing the picture. |
| Redirect an old URL | Add it under `redirect_from:` in the target page's header |

Links have **no leading slash** (`about/`, not `/about/`). The layout sets `<base href>`, so the same
links work on the preview and on niapower.org.

`_tools/` holds the one-off scripts that built the mirror from the live site (`mirror.py`) and applied
the content changes agreed with Arun (`fixes.py`: AID INDIA replaces Pardada Pardadi and Shishu
Shakthi, the 2004 incorporation, the Nia Inspire FAQ, alt text, fixed links). Jekyll ignores them.
`_archive/` keeps the earlier Markdown version.

## Status
- Preview: https://sigaramendrum.github.io/nia-web/ (hidden from search engines).
- Checked block by block against niapower.org at 1357px and 390px wide. Every page matches to within
  3px, except where content was changed on purpose (Partners; About on phones, where one sentence
  is a line longer).
- Not yet done: the contact form (phase 4; the form area shows the email address for now) and the
  cutover (after 1 Dec): set `url` and `baseurl` in `_config.yml`, add a `CNAME`, point DNS.

Full plan: `nia/20_marketing/website/2026-11-26 Plan Website Migration.md` (private repo).
