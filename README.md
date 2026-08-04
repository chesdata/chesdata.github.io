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

This is a shim that fakes the Jekyll build so you can look at the design in a
browser right now. It is not used by the published site. If you edit a `.md`
file, re-run it.

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
3. Your dashboard is at `https://<code>.goatcounter.com`. Pageviews, referrers,
   and countries appear there within seconds of a visit.

The snippet is already wired into the layout, so every page is tracked once you
set the code. Set `goatcounter_code:` to empty to switch tracking off.

GoatCounter sets no cookies and stores no IP addresses, so no consent banner is
needed. Non-commercial use is free.

## 4. Move the data files

Data files go in **Releases**, not in the repo tree. Releases are built for
distributing binaries, they give each file a permanent download URL, and they
keep the repo itself small and fast to clone.

1. Repo → **Releases** → *Draft a new release*.
2. Tag it after the wave, e.g. `ches-2024`.
3. Drag the `.dta`, `.csv`, and `.pdf` files into the attachments box.
4. Publish, then right-click each attached file to copy its download URL.
5. Paste those URLs into the `href` of the matching `.file` links in
   `ches-europe.md`, `chesla.md`, etc. Right now they all point at the releases
   page as a placeholder.

Limits worth knowing: individual files are hard-blocked above 100 MB, and
GitHub asks you to keep total repo size under 1 GB. CHES files are nowhere near
either number.

Consider also depositing each wave on Zenodo for a permanent DOI. Papers citing
a DOI rather than a URL will keep resolving regardless of where the site lives.

## 5. Point chesdata.eu at it — do this last

Only after the test site looks right.

1. Add a file named `CNAME` at the repo root containing exactly:
   ```
   www.chesdata.eu
   ```
2. Update DNS. **Check first where chesdata.eu's DNS is actually managed** —
   the domain is registered at GoDaddy, but if Squarespace is running the DNS
   then the nameservers point at Squarespace and that's where records must
   change, or you move nameservers back to GoDaddy first.
3. Your canonical URL is already `www.chesdata.eu`, which is the easy case: it
   needs one `CNAME` record for `www` pointing at `<account>.github.io`. Using
   the bare `chesdata.eu` as primary instead requires four `A` records with
   GitHub's IP addresses. **Read the current IPs off GitHub's own docs rather
   than copying them from anywhere else** — they have changed before:
   <https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site>
4. Back in **Settings → Pages**, enter the custom domain, wait for the DNS
   check to pass, then tick **Enforce HTTPS**. The certificate is issued
   automatically and is free.
5. Leave Squarespace active for a week or two. If anything is wrong you can
   point DNS straight back at it. Cancel only once you're satisfied.

---

## URLs are deliberately unchanged

The `permalink` in each file reproduces the existing Squarespace paths
(`/our-team/`, `/ches-europe/`, `/chesla/`, `/chesisrael/`, `/chescanada/`,
`/contact-us/`). Published articles cite these URLs, so keeping them means no
citation breaks at the cutover.

## Current structure

Ten pages build: About (`/`), CHES-Europe, CHES-Latin America, CHES-Israel,
CHES-Canada, SPEED-CHES, CHES-South Asia, CHES-USA, Team, Contact. The three
regional pages and both SPEED datasets were pulled from the live chesdata.eu
and are complete, with citations and DOIs. South Asia and USA are marked
placeholders — no survey has run yet for either.

**Team is not in the header nav.** It's linked from the footer's Explore list
and from each survey page's "Team" section. Restore it to `nav:` in
`_config.yml` if you'd rather it stayed in the header.

**Nav labels are short** (`Europe`, `Latin America`, ...) rather than spelled
out (`CHES-Latin America`), because with eight items plus CHES Interactive the
long form overflows a laptop-width header. Page titles and headings are
unaffected — only the top nav is shortened. The long-form list is commented
in `_config.yml` if you want to revert.

## What still needs your content

Marked with a bordered note in the page itself:

- `our-team.md` — bios for Bakker, Hooghe, Marks, Steenbergen; rest of
  Vachudova's bio
- `ches-europe.md` — the 1999, 2002, 2006, 2010, 2014 wave entries, the 2017
  FLASH survey, and the Balkan candidate country surveys (all confirmed to
  exist on chesdata.eu, just not yet transcribed here)
- `speed-ches.md` — what SPEED stands for; a fuller intro to the series if
  one exists beyond what the two dataset pages say
- `ches-south-asia.md`, `ches-usa.md` — everything; no survey has been
  fielded for either yet
- `index.md` — mission paragraph still says six waves through 2019; doesn't
  mention Israel, Canada, South Asia, or the USA
- The homepage photo from Squarespace (`DSC_7147.jpg`) — a decision was made
  to leave it out for now (see chat history); drop it in `assets/img/` if
  you change your mind, several treatments were mocked up

Delete each note once you've filled the section in.

## Data files still on Squarespace

See `DATA-FILES-TO-RESCUE.md` — every dataset file for Latin America, Israel,
and Canada is still hosted at `chesdata.eu/s/...` and will die when the
Squarespace subscription ends. Download them before cancelling.
