# Generator

Every SVG in `../assets/light` and `../assets/dark` is produced here.

```bash
pip install -r requirements.txt
python generator/build.py
```

- `common.py` – the two palettes (`LIGHT`, `DARK`), the outlined-type engine and the drawing helpers:
  `topbar` / `rail` (header strip and numbered side rail), `dial` (circular instrument), `mesh` (wireframe point
  clouds: `blob`, `ring`, `rose`), `wave` (scrolling trace), `bars`, `barcode`, `dotmatrix`, `grid`, `ruler`,
  `brackets`, `kv` (leader-dot readout row).
- `sections.py` – one builder per panel (`header`, `system`, `contact`). All copy lives here.
- `jp_glyphs.py` – outlines of the handful of Japanese glyphs used as decorative labels (Noto Sans CJK JP, SIL OFL 1.1).
- `fonts/` – Tektur (display) and Geist Mono (readouts), SIL OFL 1.1. They are only used to turn text into vector
  outlines at build time, so nothing loads from the network when the page is viewed.

Panels are drawn on an 840px canvas (about GitHub's README width). Motion is plain CSS inside the SVG, which GitHub
allows inside an `<img>`; it is slow and sparse, and visitors with "reduce motion" turned on see a still image.
Colours are the `LIGHT` / `DARK` dicts at the top of `common.py`.
