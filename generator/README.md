# Generator

Every SVG in `../assets` (light) and `../assets/dark` is produced by this folder.

```bash
pip install -r requirements.txt
python generator/build.py
```

- `common.py` is the HUD design system. It holds the light and dark palettes (picked via the `HUD_THEME` variable,
  which `build.py` sets for you), the outlined-type engine, and the parts: `hud` (cut-corner frame with nodes),
  `label_bar` (blue Japanese label bar), `vjp` (vertical Japanese text), `outline` / `solid` (extended headline type),
  `code_box`, `halftone`, `counter`, `wave`, `eq`, `packet`, `barcode`, `button` and `crt` (scanlines, scan band, grain).
- `sections.py` has one builder per panel: hero, profile, architecture, stack, contact, footer.
- `subset_jp.py` rebuilds `fonts/NotoSansJP-Bold-subset.otf` so it holds only the characters used in `sections.py`.
  Run it after you change any Japanese text (it needs the Noto Sans CJK font on your machine):
  `python generator/subset_jp.py /path/to/NotoSansCJK-Bold.ttc`
- `fonts/` holds Poppins Bold, Geist Mono, Silkscreen and the Noto Sans JP subset (all SIL OFL 1.1). They are only used to
  turn text into vector outlines at build time, so nothing loads from the network when the page is viewed.

Motion is plain SVG (CSS keyframes and SMIL), which GitHub allows inside an `<img>`; scripts, video and `<foreignObject>`
are stripped, so none are used. Visitors with "reduce motion" on see a still image.
