"""Regenerates every SVG in ../assets (light) and ../assets/dark.

    pip install -r requirements.txt
    python generator/build.py
"""
import importlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
ROOT = os.path.join(os.path.dirname(HERE), "assets")
NAMES = {"header.svg": "hero", "whoami.svg": "profile", "ecosystem.svg": "ecosystem", "stack.svg": "stack",
         "transmission.svg": "contact", "footer.svg": "footer"}

for theme, out in (("light", ROOT), ("dark", os.path.join(ROOT, "dark"))):
    os.environ["HUD_THEME"] = theme          # the palette is picked when common.py loads
    import common
    import sections
    importlib.reload(common)
    importlib.reload(sections)
    os.makedirs(out, exist_ok=True)
    for fname, fn in NAMES.items():
        svg = getattr(sections, fn)()
        with open(os.path.join(out, fname), "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"{theme:5} {fname:18} {len(svg) / 1024:6.1f} KB")
print("done")
