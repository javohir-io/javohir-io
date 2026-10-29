"""Regenerates every SVG in ../assets (light) and ../assets/dark.

    pip install -r requirements.txt
    python generator/build.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from common import DARK, LIGHT  # noqa: E402
from sections import contact, ecosystem, hero, stack  # noqa: E402

ROOT = os.path.join(os.path.dirname(HERE), "assets")
PANELS = {"header.svg": hero, "ecosystem.svg": ecosystem, "stack.svg": stack, "transmission.svg": contact}

for palette, out in ((LIGHT, ROOT), (DARK, os.path.join(ROOT, "dark"))):
    os.makedirs(out, exist_ok=True)
    for fname, fn in PANELS.items():
        svg = fn(palette)
        with open(os.path.join(out, fname), "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"{palette['name']:5} {fname:18} {len(svg) / 1024:6.1f} KB")
print("done")
