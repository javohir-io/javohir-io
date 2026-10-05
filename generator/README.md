# Generator

Every SVG in `../assets` (light) and `../assets/dark` is produced by this folder.

```bash
pip install -r requirements.txt
python generator/build.py
```

- `common.py` — palettes, the outlined-type engine, shared pieces (panel slab, ghost lettering, glints, glitch keyframes)
- `sections.py` — one builder per panel (hero, profile, architecture, stack, contact, soundtrack, footer, divider)
- `fonts/` — Lora (SIL OFL 1.1). Used only to turn display text into vector outlines at build time,
  so the serif looks identical on every device. Nothing is loaded from the network at view time.

To change the look, edit the two palettes (`DARK`, `LIGHT`) at the top of `common.py` — `accent` is the main colour, `alt` is the second colour used in the name glitch. To change copy, edit `sections.py`.
