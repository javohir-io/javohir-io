# Generator

Every SVG in `../assets` (light) and `../assets/dark` is produced by this folder.

```bash
pip install -r requirements.txt
python generator/build.py
```

- `common.py` — the palette (`DARK`, `LIGHT`), the outlined-type engine, and the shared pieces: `card` (rounded slab),
  `pill`, `tag` (outlined label pill), `glow` (blurred colour blobs) and `glass` (frosted capsule with liquid inside)
- `sections.py` — one builder per panel: hero, profile, architecture, stack, contact, soundtrack, footer
- `fonts/` — Poppins Bold and Medium (SIL OFL 1.1). Used only to turn text into vector outlines at build time,
  so the type looks identical on every device. Nothing is loaded from the network at view time.

## Palette

| name | hex | used for |
| --- | --- | --- |
| Blanche White | `#FEFFFC` | text and the neutral pill on dark; the card on light |
| Banana Yellow | `#D0FF00` | lime pills, buttons, glow |
| Plum Violet | `#8116E0` | violet pills, glow, accents on light |
| Black | `#000000` | the card on dark; text and the neutral pill on light |

To change the look, edit `DARK` and `LIGHT` at the top of `common.py`. To change copy, edit `sections.py`.
