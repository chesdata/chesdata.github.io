# chesdata.eu — static site

Jekyll site for the Chapel Hill Expert Survey, built to run free on GitHub Pages.

Content lives in the `.md` files at the root. Each one is plain HTML inside a
Markdown wrapper, so you can edit text without touching the layout. The shared
header, footer, and analytics live in `_layouts/default.html`. All colours and
type are defined once at the top of `assets/css/main.css`.

---

## 1. Preview locally, before any GitHub work

```
python3 build-preview.py
open _preview/index.html
```

This is a shim that fakes the Jekyll build so you can look at the design in a browser right now. It is not used by the published site. If you edit a `.md` file, re-run it.

## 2. Put it on GitHub Pages

1. Create a repository. If you name it `<account>.github.io` the site lives at
   `https://<account>.github.io`; any other name puts it at
   `https://<account>.github.io/<repo>`.
2. Push these files to the default branch.
3. Repo **Settings → Pages** → set Source to *Deploy from a branch*, branch
   `main`, folder `/ (root)`.
4. Wait a minute, then open the `github.io` URL. **This is your test site.**
   chesdata.eu keeps running on Squarespace, untouched.
5. If the build fails, the **Actions** tab shows the error.

## 3. Turn on GoatCounter

1. Register at <https://www.goatcounter.com> and pick a site code.
2. Put that code in `_config.yml` under `goatcounter_code`.
3. Your dashboard is at `https://chesdata.goatcounter.com`. Pageviews, referrers,  and countries appear there within seconds of a visit.

The snippet is already wired into the layout, so every page is tracked once you set the code. Set `goatcounter_code:` to empty to switch tracking off.

GoatCounter sets no cookies and stores no IP addresses, so no consent banner is needed. Non-commercial use is free.

## 4. Move the data files

Data files go in **Releases**, not in the repo tree. Releases are built for distributing binaries, they give each file a permanent download URL, and they keep the repo itself small and fast to clone.

1. Repo → **Releases** → *Draft a new release*.
2. Tag it after the wave, e.g. `ches-2024`.
3. Drag the `.dta`, `.csv`, and `.pdf` files into the attachments box.
4. Publish, then right-click each attached file to copy its download URL.
5. Paste those URLs into the `href` of the matching `.file` links on that
   survey's page (`ches-europe.md`, `ches-la.md`, `ches-israel.md`,
   `ches-canada.md`, `ches-speed.md`). Every dataset currently on the site has already been wired up this way — this step is only for a future wave, or if you re-upload a file under a different name.

## 5. Point chesdata.eu at it — do this last

**See `DNS-CUTOVER.md`.** It has the exact records to change, the values to
change them to, and the old values to roll back to, all read off live DNS.

Three things worth knowing before you open it:

- **DNS is managed at GoDaddy**, not Squarespace. The nameservers are
  `ns17`/`ns18.domaincontrol.com`. Squarespace hosts the site but doesn't
  control the records, so nothing needs doing inside Squarespace.
- **The domain runs Microsoft 365 email.** The cutover changes the four apex
  `A` records and the `www` `CNAME` and *nothing else*. Do not bulk-delete the
  Squarespace records — the `MX`, `SPF`, and `autodiscover` records live in the
  same zone and the mail dies with them.
- **The `CNAME` file is already committed**, so GitHub Pages redirects
  `chesdata.github.io` to `www.chesdata.eu` — which is still Squarespace. That
  means the "look at the test site first" advice above no longer works at that
  URL. Use `python3 build-preview.py` locally instead, or drop the `CNAME` file
  temporarily. The deployed build itself was verified page-by-page on
  7 August 2026 and is sound.

---

## URLs

Most permalinks reproduce the existing Squarespace paths (`/our-team/`,
`/ches-europe/`, `/contact-us/`) so published citations keep resolving after
cutover.

Three pages are the exception: CHES-Latin America, CHES-Israel, and
CHES-Canada moved from their original bare Squarespace paths (`/chesla/`,
`/chesisrael/`, `/chescanada/`) to hyphenated ones (`/ches-la/`,
`/ches-israel/`, `/ches-canada/`) for consistency with `/ches-europe/` and the
rest of the family. Each old path still resolves — `chesla.md`,
`chesisrael.md`, and `chescanada.md` at the repo root are redirect stubs
(`layout: null`, a `<meta http-equiv="refresh">`, and a manual fallback link)
that forward to the new path automatically, so nothing that's already cited
the old URLs breaks.

If you rename another page's permalink later, add a matching redirect stub
using one of these three files as a template, and update the internal links
in `_config.yml`'s `nav:` and any page that links to it — Jekyll won't warn
you about a link pointing at a path that no longer has real content.

## Current structure

Ten pages build: About (`/`), CHES-Europe, CHES-Latin America, CHES-Israel,
CHES-Canada, SPEED-CHES, CHES-South Asia, CHES-USA, Team, Contact. The three
regional pages and all three SPEED waves were pulled from the live chesdata.eu
and are complete, with citations and DOIs. CHES-Europe carries every wave from
the 1984–1999 Ray–Marks–Steenbergen survey through 2024. South Asia and USA are
marked placeholders — no survey has run yet for either.

**Team is not in the header nav, and nothing else links to it either.** This
paragraph used to say it was reachable from the footer's Explore list and from
each survey page's "Team" section. Checked 7 August 2026: it isn't. `/our-team/`
has zero inbound links from any page — the footer, the nav, and every survey
page. It builds, it's in `sitemap.xml`, and search engines will index it, but no
visitor can reach it by clicking.

So it's a decision, not an oversight to fix by halves: either link it — add
`Team` back to `nav:` in `_config.yml`, or put it in the footer — or drop the
page. A half-written orphan that only Google can find is the worst of the three.

**Nav labels are short** (`Europe`, `Latin America`, ...) rather than spelled
out (`CHES-Latin America`), because with eight items plus CHES Interactive the
long form overflows a laptop-width header. Page titles and headings are
unaffected — only the top nav is shortened. The long-form list is commented
in `_config.yml` if you want to revert.

## What still needs your content

Reviewed 7 August 2026. Where a gap is flagged on the page itself, it's marked
with a bordered note — delete the note once you've filled the section in.

- `ches-speed.md` — what SPEED stands for. The page carries all three waves
  (2017 FLASH, 2020 COVID-19, 2023 Ukraine) but never expands the acronym. A
  fuller intro to the series would help too, if one exists beyond what the
  three dataset entries say.
- `ches-southasia.md`, `ches-usa.md` — everything; no survey has been fielded
  for either yet.
- `our-team.md` — bios for Bakker, Hooghe, Marks, Steenbergen, and the rest of
  Vachudova's. Worth settling whether the page is linked at all before writing
  them; see "Current structure" above.
- The homepage photo from Squarespace (`DSC_7147.jpg`) — deliberately left out
  for now. Drop it in `assets/img/` if you change your mind; several treatments
  were mocked up.

### Done since this list was written

- `index.md` — the mission section is current. It covers seven waves through
  2024 and names Latin America, Canada, Israel, South Asia, the USA, and SPEED.
  The old note said it stopped at six waves in 2019.
- `ches-europe.md` — complete. Every wave has an entry: the 1984–1999
  Ray–Marks–Steenbergen survey, 1999, 2002, 2006, 2010, 2014, 2019, 2024, plus
  the 2007, 2014, and 2019 candidate country surveys and the trend file. The
  2017 FLASH survey isn't missing — it lives on `ches-speed.md`, which is where
  it belongs.

## Data files — rescued

This section used to warn that the Latin America, Israel, and Canada datasets
were still hosted at `chesdata.eu/s/...` and would die with the Squarespace
subscription. That's no longer true, and it contradicted
`DATA-FILES-TO-RESCUE.md`, which records the rescue as finished.

Verified 7 August 2026: no page on the site links to `chesdata.eu/s/` any more.
Every dataset, codebook, and questionnaire link points at a GitHub Release under
`github.com/chesdata/chesdata.github.io/releases/download/...`. **Cancelling
Squarespace costs no data.** See `DATA-FILES-TO-RESCUE.md` for the release tags.

The one Squarespace asset never brought across is the homepage photo
(`DSC_7147.jpg`), which was deliberately left out — see the note above.

## The domain

chesdata.eu moved from Squarespace to GitHub Pages on 7 August 2026. See
`DNS-CUTOVER.md` for what changed, what the zone looks like now, and how to roll
back while the Squarespace subscription is still live.
