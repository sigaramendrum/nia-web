# nia-web

The public website for NIA: **niapower.org** (GitHub Pages, built with Jekyll).

**PUBLIC repo.** Only content that is already public or meant for the site. No finance data, no
private personal data, no `_system`. Planning notes and anything private live in the private `nia`
repo (`20_marketing/website/`). Student stories here are the ones published with the student's
consent.

## Where to edit what
| To change | Edit |
|---|---|
| A page's text | `<page>.md` at the top level (e.g. `about.md`, `inspire.md`, `donate.md`). `index.md` is the home page. |
| Team and board on /about | `_data/team.yml` |
| A story, or add one | `_posts/YYYY-MM-DD-<name>.md` (shows at `/stories/<name>/`) |
| The Stories list | `stories.md` |
| Top menu and footer links | `_data/navigation.yml` |
| Colours, fonts, spacing | `assets/css/main.css` |
| Buttons | Write `[Label](link/){: .button}` on its own line |
| Images | Put the file in `assets/images/` and write `![What it shows](assets/images/<file>)` |
| A coloured block | Wrap it in `<section class="band green" markdown="1">` … `</section>` (white, light, blush, green, navy, violet) |
| Redirect an old URL | Add it under `redirect_from:` in the target page's header |

**Links have no leading slash** (`about/`, not `/about/`). The layout sets `<base href>`, so the same
links work on the preview (`/nia-web/`) and on niapower.org.

Each page's URL is the `permalink:` in its header, matching the old Squarespace URLs.

## Status (2026-11-26)
- **Phase 1 done:** content converted from the Squarespace export (13 pages, 5 stories).
  `<!-- section N: theme=... -->` comments record the old layout's colour blocks for phase 3.
- **Phase 2 done:** the 65 images the pages use are in `assets/images/` (WebP, web size, with alt
  text; backgrounds and icons are marked decorative). Fonts are in `assets/fonts/` (Anton, Inter, both
  OFL) and logos are in `assets/logo/`.
- **Phase 3:** layouts (`_layouts/`), styles (`assets/css/main.css`), nav and footer
  (`_data/navigation.yml`) and redirects (`/home`, `/events` → home; `/cart`, `/contact-copy` → donate).
  Preview: https://sigaramendrum.github.io/nia-web/. At cutover, set `url` and `baseurl` in `_config.yml`.

Full plan: `nia/20_marketing/website/2026-11-26 Plan Website Migration.md` (private repo).
