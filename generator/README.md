# Generator

Every graphic in `assets/` is produced by these scripts, in a light and a dark variant.

```bash
pip install -r requirements.txt
python3 generator/build.py            # rebuild everything
python3 generator/build.py player     # rebuild a single file
```

- `theme.py` holds the two palettes. `typo.py` measures text and embeds subsetted fonts. `kit.py` has the chamfered frame, carbon weave, guilloche rosette, rulers and watch dial.
- `s_*.py` files draw the sections. `registry.py` lists which file each one produces.
- Fonts (`fonts/`) are Lora, and Poppins Light and Medium, all under the SIL Open Font License. Each SVG embeds only the glyphs it uses, so the typography is identical on every device.
- Edit the copy in the `s_*.py` files, rebuild, commit `assets/`.
