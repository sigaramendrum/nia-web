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
| Buttons | Write `[Label](/link/){: .button}` on its own line |

Each page's URL is the `permalink:` in its header, matching the old Squarespace URLs.

## Status (2026-11-26)
- **Phase 1 done:** content converted from the Squarespace export (13 pages, 5 stories).
  `<!-- section N: theme=... -->` comments record the old layout's colour blocks for phase 3.
- **Phase 2 next:** images still load from Squarespace's CDN; they get copied into `assets/`.
- **Phase 3:** layouts (`_layouts/`), styles, nav, footer and redirects. Until then `.nojekyll`
  stays, and Pages is off.

Full plan: `nia/20_marketing/website/2026-11-26 Plan Website Migration.md` (private repo).
