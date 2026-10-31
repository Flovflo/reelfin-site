# ReelFin Site

Static public marketing, support, privacy and terms pages for ReelFin.

## Local preview

```bash
python3 scripts/build_homepages.py
python3 -m http.server 8136 --bind 127.0.0.1
```

- English: `http://127.0.0.1:8136/`
- Français: `http://127.0.0.1:8136/fr/`

`index.html` and `fr/index.html` are checked-in static output. Edit the copy or
shared markup in `scripts/build_homepages.py`, then rerun it. Python's standard
library is sufficient; there are no runtime dependencies, external fonts,
analytics scripts or cookie storage on the marketing site.

The shared CSS also styles the existing support, privacy and terms pages. Their
policy and support wording is maintained directly in those HTML files.

## Product media

`assets/media/cinema/` contains web-optimised native ReelFin captures and fictional
poster artwork. Product captures show the app's demonstration library. They are
marketing illustrations, not evidence of live-server playback or media supplied
with ReelFin. On-page credits state that the artwork is fictional and content is
not included.

The poster manifest is `assets/media/cinema/posters.json`; its order controls the
feature preview and horizontal library rail. The Mac platform is explicitly
labelled in development, with no public Mac download link.

The current collection contains 40 original fictional posters. Source hashes and
the coverage of the seven refreshed iPhone, iPad and Apple TV captures are recorded
in `assets/media/cinema/native-captures.json`. Existing Duo captures remain in use
until new native Open/Closed captures are available; they still show Aurora.
The refreshed iPad asset is retained for preparation and is not inserted in the
public page. The FR/EN social previews use the new cinema composition.

## Checks

```bash
python3 scripts/build_homepages.py
node --check assets/site.js
git diff --check
```

Preview the English and French pages, navigation, FAQ disclosures, support and
legal pages at mobile, tablet and desktop sizes. Respect reduced-motion settings
and keep all local asset and App Store links working.

## Deployment

GitHub Pages uses `.github/workflows/deploy-site.yml`. A push to `main` deploys the
site. Creating a local preview does not publish anything.

- Marketing: `https://flovflo.github.io/reelfin-site/`
- French: `https://flovflo.github.io/reelfin-site/fr/`
- Privacy: `https://flovflo.github.io/reelfin-site/privacy.html`
- Support: `https://flovflo.github.io/reelfin-site/support.html`
- Terms: `https://flovflo.github.io/reelfin-site/terms.html`
