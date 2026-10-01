# Generator

Every graphic in `assets/` is produced by these scripts, in a light and a dark variant.

```bash
pip install -r requirements.txt
python3 generator/prep_images.py      # (optional) re-cut the pictures in generator/img from their sources
python3 generator/build.py            # rebuild everything
python3 generator/build.py about      # rebuild a single file
```

- `theme.py` holds the palette. `typo.py` measures text and embeds subsetted fonts. `kit.py` has the stage, embers, ribbons, labels, waveform and embedded images.
- `s_hero.py` and `s_sections.py` draw the sections. Each section has its own picture: hero (open-handed statue), About (halftone torso), Stack (crying angel), Workflow (neon statue), Closing (winged angel). `registry.py` lists which file each one produces.
- Fonts (`fonts/`): TeX Gyre Termes Bold (GUST Font License), Lora Italic and Poppins Light/Medium (SIL OFL). Each SVG embeds only the glyphs it uses, so the typography is identical on every device.
- Edit the copy in the `s_*.py` files, rebuild, commit `assets/`.
