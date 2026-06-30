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
- { name: "Jane Doe", year: "2027", thesis: "Their thesis title", position: "Now at …" }
```
(`position` is optional.)

### Publications (no editing needed)
The Publications page builds itself **live from ORCID** every time it loads, so
there is nothing to maintain: when the PI adds a paper to their ORCID record, it
appears here automatically, grouped by year with a DOI link.

To point the page at a different ORCID iD, change the `data-orcid` value near the
top of [`publications.html`](publications.html). The fetch/parse logic lives in
`initPublications()` in [`assets/js/site.js`](assets/js/site.js).

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
Drop real GeoVM lab photos in `assets/img/facilities/` and update the `gallery:`
list in [`_data/facilities.yml`](_data/facilities.yml). (The current facility
photos are placeholders.)

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
_data/            ← ALL editable content (people, projects, themes, news, …)
_includes/        ← reusable HTML snippets (navbar, footer, cards, headings)
_layouts/         ← the page shell (default.html wraps every page)
_sass/            ← styles, ported from the MSIL Design System
  _tokens.scss      colours, type, spacing, motion (the single source of truth)
  _base.scss        element defaults
  _components.scss  buttons, cards, tags, badges, tabs, carousel, …
  _layout.scss      page-specific layout
  _responsive.scss  mobile / tablet breakpoints
assets/
  css/main.scss   ← bundles the _sass partials into /assets/css/main.css
  js/site.js      ← all interactivity (theme toggle, tabs, expanders, carousel)
  img/            ← images (team/, projects/, and landscape stand-ins)
index.html        ← About / Home          (the 6 pages are plain HTML that
research.html     ← Research                 mostly loop over _data files)
publications.html ← Publications
people.html       ← People
facilities.html   ← Facilities
contact.html      ← Contact
_config.yml       ← site-wide settings
```

The pages are server-rendered, so **all content is in the HTML** (good for
search engines and works without JavaScript). `site.js` only *adds*
interactivity on top — nothing depends on it to read the page.

---

## 🚀 Deploying to GitHub Pages

This site uses only GitHub-Pages-approved plugins, so **GitHub builds it for you
— no GitHub Action required.**

1. Put these files at the root of the **`multimodalsig.github.io`** repository
   (for a user/org page the repo must be named `<org>.github.io`).
2. In the repo: **Settings → Pages → Build and deployment → Source:**
   *Deploy from a branch*, branch `main`, folder `/ (root)`.
3. Push. The site goes live at <https://multimodalsig.github.io> within ~1 min.

> If you'd rather keep the site in a subfolder or a different repo, set `baseurl`
> in `_config.yml` accordingly (e.g. `baseurl: "/repo-name"`).

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
