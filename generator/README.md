# Generator

Every SVG in `../assets` (light) and `../assets/dark` is produced here.

```bash
pip install -r requirements.txt
python generator/build.py
```

- `common.py` holds the two palettes (`DARK`, `LIGHT`), the outlined-type engine and the drawing helpers:
  `head` (numeral + title), `rbox` / `pill` / `brackets` / `camera` (hairline shapes and viewfinder corners),
  `surface` (ridge-line terrain with a scan sweep), `earth` + `orbit` (rotating wireframe Earth with a satellite),
  `solid` (rotating wireframe objects: cube, phone, monitor, cylinder, ico), `globe`, `dust`.
- `earth_data.py` holds the simplified continent outlines used by the Earth model.
- `sections.py` has one builder per panel: masthead, system, stack, contact.
- `fonts/` holds Instrument Sans, Tektur and Geist Mono (SIL OFL 1.1), used only to convert text to vector outlines at
  build time, so nothing loads from the network when the page is viewed.

Panels are drawn on an 840px canvas (about GitHub's README width) with no text under 11px, so type stays readable
when the page is narrower. Motion is plain SVG (CSS keyframes and SMIL), which GitHub allows inside an `<img>`, and is slow and sparse. Visitors
with "reduce motion" turned on see a still image. Colours and the single pink (`acc`) live at the top of `common.py`;
copy lives in `sections.py`.
