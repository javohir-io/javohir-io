# Generator

Every SVG in `../assets/light` and `../assets/dark` is produced here.

```bash
pip install -r requirements.txt
python generator/build.py
```

- `common.py`: the two palettes (`LIGHT`, `DARK`), the outlined-type engine, isometric solids (`box`, `cylinder`) and `wire`
  (a wireframe turning in 3D, pre-computed as SVG path frames).
- `sections.py`: one builder per panel. All copy lives here.
- `fonts/`: Instrument Sans and Geist Mono (SIL OFL 1.1), used only to turn text into vector outlines at build time,
  so nothing loads from the network when the page is viewed.

Panels are 840px wide, about GitHub's README column. Motion is slow and sparse: floating layers, a flowing dashed
connector, a pulsing status dot, and the turning solids.
