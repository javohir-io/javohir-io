# Generator

Every SVG in `../assets` (light) and `../assets/dark` is produced by this folder.

```bash
pip install -r requirements.txt
python generator/build.py
```

- `common.py` — palettes, the outlined-type engine, shared ornaments (frames, glints, dust)
- `sections.py` — one builder per panel (hero, profile, architecture, stack, contact, soundtrack, footer, divider)
- `fonts/` — Lora (SIL OFL 1.1). Used only to turn display text into vector outlines at build time,
  so the serif looks identical on every device. Nothing is loaded from the network at view time.

To change the look, edit the two palettes at the top of `common.py`. To change copy, edit `sections.py`.
