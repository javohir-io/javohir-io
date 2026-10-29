# Generator

Every SVG in `../assets` (light) and `../assets/dark` is produced here.

```bash
pip install -r requirements.txt
python generator/build.py
```

- `common.py` holds the two palettes (`DARK`, `LIGHT`), the outlined-type engine and every drawing helper:
  `head` (pink numeral + title), `para` (small justified caption), `rbox` / `pill` / `brackets` / `camera` (hairline shapes and viewfinder corners),
  `surface` (ridge-line terrain with a scan sweep), `bars` (signal), `globe`, `meter`, `dust`.
- `sections.py` has one builder per panel: masthead, system, stack, contact.
- `fonts/` holds Instrument Sans, Tektur and Geist Mono (SIL OFL 1.1). They are only used to convert text to vector
  outlines at build time, so nothing loads from the network when the page is viewed.

Motion is plain SVG (CSS keyframes and SMIL), which GitHub allows inside an `<img>`, and is deliberately slow and sparse.
Visitors with "reduce motion" turned on see a still image. Colours and the single pink (`acc`) live at the top of `common.py`;
copy lives in `sections.py`.
