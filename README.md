# Multimodal Spatial Imaging Group — website

The public website for the **Multimodal Spatial Imaging Group (MSIG)** at the
University of Calgary. It's a [Jekyll](https://jekyllrb.com/) site hosted on
**GitHub Pages**, built to match the MSIL Design System and — most importantly —
to be **easy to keep up to date**.

> **You almost never edit HTML or CSS.** Nearly all content lives in plain-text
> data files under [`_data/`](_data/). Edit a file, commit, and GitHub rebuilds
> the site automatically (usually within a minute).

---

## ⚡ Common tasks (start here)

### Add or update a student / researcher
1. Put their photo in [`assets/img/team/`](assets/img/team/) (a square JPG/PNG
   looks best, e.g. `jane.jpg`).
2. Open [`_data/people.yml`](_data/people.yml) and copy an existing entry under
   `team:`. Paste it and edit the fields:
   ```yaml
   - name: Jane Doe
     role: PhD Student
     photo: assets/img/team/jane.jpg
     short: One line shown on the collapsed card.
     bio: >-
       A longer paragraph shown when the card is expanded.
     interests:
       - Sensor Calibration
       - SLAM
     projects:
       - Some project they work on
     links:
       - label: LinkedIn
         href: "https://www.linkedin.com/in/janedoe/"
         icon: fa-brands fa-linkedin
   ```
   Anything optional (`photo`, `bio`, `interests`, `projects`, `links`) can be
   removed if you don't have it. **Order in the file = order on the page.**
3. Commit. Done.

### Graduate someone (move a student to Alumni)
Cut their detail down to one line and move it into the right group under
`alumni:` in [`_data/people.yml`](_data/people.yml):
```yaml
- { name: "Jane Doe", year: "2027", thesis: "Their thesis title" }
```

`alumni:` is a list of **collapsible groups**, rendered in file order:

| `id` | Title | Who |
|---|---|---|
| `phd` | PhD | Supervised as first advisor |
| `msc` | MSc | Supervised as first advisor |
| `meng` | MEng | Supervised as first advisor |
| `co-supervised` | Co-Supervised | Lichti on the supervisory committee |
| `postdoc` | Post-Doctoral Associates | `year` is the postdoc term, not a degree |

`year` and `thesis` are both optional — leave either blank and it simply isn't
drawn. A member may also carry `degree: PhD` / `MSc` / `MEng`, which renders as
a coloured badge beside the name. **Only use it where a group mixes levels**
(Co-Supervised does); in the PhD/MSc/MEng groups the group title already says
it, so a badge would just repeat.

The PhD/MSc lists are maintained from `Lichti_Derek_students_theses.xlsx` (kept
outside this repo, one level up). The MEng, Co-Supervised and Post-Doctoral
groups are **not** in that spreadsheet — they were supplied by hand, so don't
regenerate the section from the xlsx without carrying them across.

> The template renders `year`, `name`, `degree` and `thesis` and nothing else.
> A `position:` field ("Now at …") is **not** displayed, despite an unused
> `.alumni-row__pos` style existing — adding one has no effect today.

### Publications
The Publications page builds itself when it loads, from two sources:

1. **ORCID** supplies the list — every paper on the PI's ORCID record, grouped
   into a collapsible section per year (the two most recent open on arrival).
2. **Crossref** fills in the bibliographic detail ORCID doesn't carry — authors,
   volume, issue and pages — looked up by DOI. Each entry gets a **Cite** button
   that copies a formatted citation.

Add a paper to ORCID and it appears here on the next page load. **Most of the
time there is nothing to edit.** The two cases that need you:

#### A paper that isn't in ORCID
Add it to [`_data/publications.yml`](_data/publications.yml). These entries are
**never sent to Crossref** — what you type is exactly what renders and what the
Cite button copies, so fill in everything you have:

```yaml
- title: "Modelling extreme wide-angle lens cameras"
  authors: "Lichti, D. D., Tredoux, W., & Maalek, R."   # APA style, see below
  journal: "The Photogrammetric Record"
  volume: "36"
  issue: "176"
  pages: "360-380"
  year: "2021"
  month: 12          # optional, orders entries within a year
  doi: "10.1111/phor.12385"   # optional, bare DOI — no https://doi.org/ prefix
```

Write `authors` the way Crossref formats them so the page reads consistently:
`Family, I. I., Family, I., & Family, I. I.` — surname first, initials with
periods, `&` before the last name.

If that paper later turns up in ORCID, **the ORCID copy is dropped in favour of
this one** (matched on DOI, or on title when there's no DOI), so nothing ever
lists twice. You can delete the YAML entry then, but leaving it is harmless.

#### A paper in ORCID that shouldn't be listed
Editorials, errata, duplicate ORCID records. Name it in
[`_data/publications_hidden.yml`](_data/publications_hidden.yml):

```yaml
- doi: "10.1016/j.isprsjprs.2020.08.022"
  note: "Editorial, not a research paper — for whoever reads this next"
```

Match on `doi` where you can (exact and stable) or on `title` where there is no
DOI. `note` is a comment for humans; the site ignores it.

#### Two things not to break
- `data-crossref-mailto` in [`publications.html`](publications.html) carries the
  contact address from `_data/contact.yml`. It puts the Crossref lookups in
  their **"polite pool"** — without it the anonymous pool rate-limits us hard
  enough that most of the detail silently fails to load. Don't remove it.
- To point the page at a different researcher, change `data-orcid` in the same
  file. The logic is `initPublications()` in
  [`assets/js/site.js`](assets/js/site.js).

If ORCID is unreachable, the hand-entered papers still render on their own.

### Post a news item
Add to the **top** of [`_data/news.yml`](_data/news.yml):
```yaml
- date: Jul 2026
  text: Something noteworthy happened.
```

### Add a project
Add a block to [`_data/projects.yml`](_data/projects.yml) (drop any images in
`assets/img/projects/` first). Each project becomes an expandable card on the
**Research → Projects** tab. See the comments at the top of that file.

### Add a gallery image
Drop the image in `assets/img/gallery/` and add a `{ src, caption }` line to
[`_data/gallery.yml`](_data/gallery.yml). Images show at their natural shape
(no cropping) in a masonry grid; clicking one opens a full-size lightbox.

### Add facility photos
Drop lab photos in `assets/img/facilities/` and update the `gallery:` list in
[`_data/facilities.yml`](_data/facilities.yml).

The **lead photo** at the top of the page is `lab.image` in the same file. It has
two layouts:

```yaml
lab:
  image: assets/img/facilities/geovm-panorama.jpg
  image_wide: true    # panorama: spans the viewport, text underneath
```

Set `image_wide` for panoramas and anything wider than about 2:1 — it spans the
full width of the browser with the description below. Leave it off for an
ordinary photo and it sits in a 300 px column beside the text instead. Using the
narrow layout for a wide image **crops it to its middle third**, which is what
prompted the flag.

### Replace the logo
There are three pieces of artwork, each doing a different job:

| File | Used for |
|---|---|
| [`assets/img/main_logo_background.svg`](assets/img/main_logo_background.svg) | The full mark on a teal chip. **The favicon**, in tabs and in search results. |
| [`assets/img/main_logo.svg`](assets/img/main_logo.svg) | The canonical mark, on transparent. The SEO publisher logo. |
| [`assets/img/tab_logo.svg`](assets/img/tab_logo.svg) | A reduced mark (no ring) that reads better at 16 px. Kept as an alternative; not currently used. |
| [`_includes/logo.svg`](_includes/logo.svg) | **A copy of `main_logo.svg`** that gets inlined into the navbar. |
| `favicon.ico`, `assets/img/favicon-*.png`, `assets/img/apple-touch-icon.png` | Rasterised from `main_logo_background.svg` for search engines — see below. |
| [`assets/img/social-card.png`](assets/img/social-card.png) | The 1200×630 `og:image` thumbnail for shared links. Run `python tools/render_social_card.py` to regenerate. |

⚠️ **`_includes/logo.svg` must be updated by hand whenever `main_logo.svg`
changes.** It is a separate copy on purpose: it swaps the two brand colours for
the `--logo-ink` / `--logo-accent` CSS variables so the mark follows the
dark-mode toggle. An `<img>` can't do that — the browser renders a linked SVG in
its own document, where the site's variables don't reach — and the brand teal
measures only **1.7:1** against the dark navbar, i.e. invisible. In dark mode
`--logo-ink` (in [`_sass/_tokens.scss`](_sass/_tokens.scss)) lightens to the same
hue at 5.4:1.

The favicon needs no such treatment: its teal chip supplies its own contrast on
both light and dark tab strips.

**The favicon is rasterised, not linked as SVG.** Browsers prefer an SVG icon
over a PNG when both are offered, and an SVG-only favicon is what left Google
showing a generic globe beside the site name. So the tab icon, the Firefox
tab-group icon and the search-result icon are all served from PNG/ICO files
generated from `main_logo_background.svg`. After changing the mark, re-run:

```bash
python tools/render_favicons.py
```

That rewrites `favicon.ico`, `assets/img/favicon-{48,96,192,512}.png` and
`assets/img/apple-touch-icon.png`. It needs only Pillow (`pip install pillow`) —
it redraws the mark's geometry directly rather than rasterising the SVG, so if
you edit `main_logo_background.svg` you must mirror the change in the script's
coordinates. `favicon.ico` belongs at the repo root: crawlers that ignore the
`<link>` tags still probe `/favicon.ico` at the domain root.

Search engines take **days to weeks** to pick up a new favicon, and Google does
not guarantee showing one even when every guideline is met.

### Change contact details / address / map
Edit [`_data/contact.yml`](_data/contact.yml). It feeds the Contact page, the
home-page profile card, and the footer.

### Change open positions
Edit [`_data/positions.yml`](_data/positions.yml). Set it to `[]` (empty) when
you're not recruiting.

### Edit research themes
Edit [`_data/themes.yml`](_data/themes.yml). Icons are
[Font Awesome 6](https://fontawesome.com/search?o=r&m=free) class names.

### Edit the site title / description / social links
Edit [`_config.yml`](_config.yml). **This is the one file where a change needs a
server restart if you're previewing locally** (GitHub rebuilds it fine on push).

---

## 🗂 Where everything lives

```
_data/            ← ALL editable content
  people.yml         PI, faculty, team, collaborators, alumni groups
  publications.yml   papers missing from ORCID (merged into the live list)
  publications_hidden.yml
                     ORCID entries to leave off the page
  facilities.yml     lead photo + carousel + instrument lists
  projects.yml  themes.yml  news.yml  gallery.yml  positions.yml
  contact.yml        address, email, map centre — also feeds the footer
  navigation.yml     the navbar links
_includes/        ← reusable HTML snippets
  navbar.html  footer.html  head.html
  logo.svg           the navbar mark, inlined (see "Replace the logo")
  member-card.html   a person card on the People page
  people-accordion.html
                     the Alumni groups (year/name/degree/thesis rows)
  project-card.html  section-heading.html
_layouts/         ← the page shell (default.html wraps every page)
_sass/            ← styles, ported from the MSIL Design System
  _tokens.scss      colours, type, spacing, motion (the single source of truth)
  _base.scss        element defaults
  _components.scss  buttons, cards, tags, badges, tabs, carousel, navbar …
  _layout.scss      page-specific layout
  _responsive.scss  mobile / tablet breakpoints
assets/
  css/main.scss   ← bundles the _sass partials into /assets/css/main.css
  js/site.js      ← all interactivity (theme, tabs, expanders, carousel,
                    accordions, and the Publications fetch/render)
  img/            ← team/  projects/  gallery/  facilities/  + the logo SVGs
index.html        ← About / Home          (the 6 pages are plain HTML that
research.html     ← Research                 mostly loop over _data files)
publications.html ← Publications
people.html       ← People
facilities.html   ← Facilities
contact.html      ← Contact
_config.yml       ← site-wide settings
```

The pages are server-rendered, so **their content is in the HTML** (good for
search engines and works without JavaScript). `site.js` mostly just *adds*
interactivity on top.

**The Publications page is the one exception:** its list is fetched and built in
the browser, so the papers are not in the page source. Two consequences worth
knowing — searching the repo (or "View Source") will not find a paper title, and
that page alone needs JavaScript to show anything.

---

## 🚀 Deploying to GitHub Pages

Deployment is **fully automatic**. The repo's Pages source is set to "GitHub
Actions", and [`.github/workflows/deploy.yml`](.github/workflows/deploy.yml)
builds the Jekyll site and publishes it on every push to `main`.

**To update the live site: edit a file, commit, and push to `main`.** The Action
builds and deploys in ~2 minutes. You can watch progress under the repo's
**Actions** tab.

The site is served at **<http://www.msig.ca>** (custom domain, set by the
`CNAME`); <https://multimodalsig.github.io> redirects there.

> ### ⚠️ If your change "didn't work", check the cache first
> Browsers hold on to `main.css`, `site.js` and images — which keep the same
> filenames between deploys — so you can be looking at a **successfully deployed
> page still using the old stylesheet**. This bites regularly, and it looks
> exactly like a broken change: a new layout that renders in its old form, or an
> updated photo that comes back at its old size.
>
> **Hard-refresh (Ctrl+Shift+R, or Cmd+Shift+R) before concluding anything is
> wrong.** Confirm the deploy went green under **Actions** first.

There is nothing to configure, but for reference the one-time setting is
**Settings → Pages → Build and deployment → Source: GitHub Actions**.

Notes:
- The previous al-folio site is preserved on the **`al-folio-backup`** branch.
- The `gh-pages` branch is unused now (Pages deploys via the workflow artifact,
  not from a branch).

---

## 🔧 Previewing locally (optional)

You only need this if you want to see changes before pushing. GitHub will build
the site regardless.

```bash
# one-time: install Ruby (https://www.ruby-lang.org), then:
bundle install
# every time:
bundle exec jekyll serve
# open http://localhost:4000
```

On Windows, [RubyInstaller](https://rubyinstaller.org/) with the Devkit is the
easiest path. If you don't want to install Ruby, just push to a branch and use a
GitHub Pages preview / the live rebuild.

---

## 🎨 Design system

Styling is a faithful CSS port of the **MSIL Design System** (University of
Calgary red `#b5121b`, Roboto + Roboto Slab type, MDB card shadows). Every colour
and size is a CSS custom property in [`_sass/_tokens.scss`](_sass/_tokens.scss) —
change a token there and it updates everywhere, in both light and dark mode. The
sun/moon button in the navbar toggles the theme and remembers the choice.

---

## ✅ Conventions & tips

- **YAML is whitespace-sensitive** — indent with spaces, not tabs, and keep the
  `- ` list dashes lined up. If a build fails, a stray indent is the usual cause.
- Wrap long text with `>-` (see existing entries) so you can break lines without
  inserting line breaks into the output.
- Quote any value containing a colon, `#`, or starting punctuation: `title: "Re: …"`.
- Icons are Font Awesome 6 free classes — search at
  <https://fontawesome.com/search?o=r&m=free> (use `fa-solid …` or `fa-brands …`).
- Images: keep them reasonably sized (≤ ~500 KB). Square images work best for
  headshots; 16:9 for project/gallery images.
- **Web formats only: JPG, PNG, SVG, WebP.** Browsers cannot display **TIFF** at
  all — a `.tif` dropped in `assets/img/` renders as a broken image, with no
  build error to warn you. Convert first. Roughly 2× the widest size the image
  is displayed at is plenty (the content column is 930 px, so ~1920 px covers a
  high-DPI screen; a full-width panorama can justify more).

---

## 🕳 Known gaps

- **The Publications page is invisible to search engines.** The list is fetched
  in the browser from the ORCID API and enriched from Crossref, so the HTML that
  crawlers receive contains only "Fetching the latest publications…". The
  `_data/publications.yml` entries do reach the page, but only inside a
  `<script type="application/json">` tag, which is not indexable content. For a
  research group this is the highest-value content on the site — paper titles
  are how people find the lab. Fixing it means rendering the list at build time
  (sync ORCID into `_data/publications.yml` on a schedule, then loop over it in
  Liquid) and keeping the live fetch only as a top-up.
- `geovm-room.jpg` is the same shot as `geovm-primary.jpg` (same 1600×747 frame,
  re-encoded). It was dropped from the carousel as a duplicate and is now
  unreferenced — safe to delete.
