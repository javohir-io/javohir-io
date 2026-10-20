"""Regenerates every SVG in ../assets.

    pip install -r requirements.txt
    python generator/build.py
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

from sections import (contact, ecosystem, footer, hero,  # noqa: E402
                      profile, soundtrack, stack)

OUT = os.path.join(os.path.dirname(HERE), "assets")
SECTIONS = {
    "header.svg": hero,
    "whoami.svg": profile,
    "ecosystem.svg": ecosystem,
    "stack.svg": stack,
    "transmission.svg": contact,
    "soundtrack.svg": soundtrack,
    "footer.svg": footer,
}

os.makedirs(OUT, exist_ok=True)
for fname, fn in SECTIONS.items():
    svg = fn()
    with open(os.path.join(OUT, fname), "w", encoding="utf-8") as f:
        f.write(svg)
    print(f"{fname:18} {len(svg) / 1024:6.1f} KB")
print("done")
