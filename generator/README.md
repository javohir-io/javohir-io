# Generator

Every SVG in `../assets/light` and `../assets/dark` is produced here.

```bash
pip install -r requirements.txt
python generator/build.py
```

- `common.py`: the two palettes (`LIGHT`, `DARK`), the outlined-type engine, isometric solids (`box`, `cylinder`),
  `wire` (a wireframe turning in 3D) and `_globe` (the dot-matrix Earth).
- `sections.py`: one builder per panel. All copy lives here.
- `land.py`: coarse hand-made continent outlines, used only to place the globe's dots.
- `fonts/`: Instrument Sans and Geist Mono (SIL OFL 1.1), used only to turn text into vector outlines at build time,
  so nothing loads from the network when the page is viewed.

Panels are 840px wide, about GitHub's README column. Motion is slow and sparse: the turning globe, floating layers,
a flowing dashed connector and a pulsing status dot. The globe, layers and connector stop for visitors with
"reduce motion" turned on.
