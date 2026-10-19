# Generator

Every SVG in `../assets` (light) and `../assets/dark` is produced by this folder.

```bash
pip install -r requirements.txt
python generator/build.py
```

- `common.py` is the Y2K design system. It holds the two palettes (`DARK`, `LIGHT`), the outlined-type engine,
  and every animated element as a method on `Doc`: `chrome` (liquid-chrome lettering with a travelling sheen),
  `cd` (spinning holographic disc), `liquid_ring` and `chrome_blob` (shape-morphing metal), `globe` (rotating
  wireframe), `terrain` (rolling perspective grid), `window`, `button`, `eq`, `ticker`, `barcode`, `star`,
  `flare`, `bubble`, `holo_orb`.
- `sections.py` has one builder per panel: hero, profile, architecture, stack, contact, soundtrack, footer.
- `fonts/` holds Poppins (Bold, Medium), Geist Mono and Silkscreen, all SIL OFL 1.1. They are only used to turn text
  into vector outlines at build time, so nothing loads from the network when the page is viewed.

Everything moves with plain SVG (CSS keyframes and SMIL), which GitHub allows inside an `<img>`. Scripts, video and
`<foreignObject>` are stripped by GitHub, so none are used. Visitors with "reduce motion" turned on get a still image.

To change colours edit `DARK` / `LIGHT` and `HOLO` / `CHROME` at the top of `common.py`. To change copy edit `sections.py`.
