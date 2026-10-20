# Generator

Every SVG in `../assets` is produced by this folder.

```bash
pip install -r requirements.txt
python generator/build.py
```

- `common.py` is the HUD design system: the palette (near-black, phosphor periwinkle, white line-work, one blue accent),
  the outlined-type engine, and the parts: `hud` (cut-corner frame with nodes), `tab` (blue label bar), `outline` /
  `solid` (extended headline type), `halftone`, `counter`, `wave`, `eq`, `packet`, `ticker`, `barcode`, `button`, and
  `crt` (scanlines, scan band, grain, vignette).
- `sections.py` has one builder per panel: hero, profile, architecture, stack, contact, soundtrack, footer.
- `fonts/` holds Poppins Bold, Geist Mono and Silkscreen (SIL OFL 1.1), used only to turn text into vector outlines at
  build time, so nothing loads from the network when the page is viewed.

Motion is plain SVG (CSS keyframes and SMIL), which GitHub allows inside an `<img>`; scripts, video and `<foreignObject>`
are stripped, so none are used. Visitors with "reduce motion" on see a still image.

Colours are the constants at the top of `common.py`. Copy lives in `sections.py`.
