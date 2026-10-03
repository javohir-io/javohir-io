"""Regenerates every SVG in ../assets (light) and ../assets/dark.

    pip install -r requirements.txt
    python generator/build.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from common import DARK, LIGHT                                    # noqa: E402
from sections import (contact, divider, ecosystem, footer, hero,   # noqa: E402
                      profile, soundtrack, stack)

ROOT = os.path.dirname(HERE)
OUT = {"light": os.path.join(ROOT, "assets"), "dark": os.path.join(ROOT, "assets", "dark")}
SECTIONS = {
    "header.svg": hero,
    "whoami.svg": profile,
    "ecosystem.svg": ecosystem,
    "stack.svg": stack,
    "transmission.svg": contact,
    "soundtrack.svg": soundtrack,
    "footer.svg": footer,
    "divider.svg": divider,
}

for d in OUT.values():
    os.makedirs(d, exist_ok=True)

for theme, palette in (("light", LIGHT), ("dark", DARK)):
    for fname, fn in SECTIONS.items():
        svg = fn(palette)
        with open(os.path.join(OUT[theme], fname), "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"{theme:5} {fname:18} {len(svg)/1024:6.1f} KB")
print("done")
