# -*- coding: utf-8 -*-
"""Build every SVG (light + dark) into ../assets. Usage: python3 generator/build.py [name ...]"""
import os, sys, xml.dom.minidom
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from theme import RED

from s_hero import header_svg

SECTIONS = {
    "header.svg": header_svg,
}
try:
    from registry import EXTRA
    SECTIONS.update(EXTRA)
except ImportError:
    pass

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
OUT = os.path.join(ROOT, "assets")
os.makedirs(OUT, exist_ok=True)

only = set(sys.argv[1:])
for fname, fn in SECTIONS.items():
    if only and fname.replace(".svg", "") not in only:
        continue
    for theme in (RED,):
        svg = fn(theme)
        xml.dom.minidom.parseString(svg.encode("utf-8"))      # fail loudly on malformed XML
        path = os.path.join(OUT, fname)
        with open(path, "w", encoding="utf-8") as f:
            f.write(svg)
        print(f"  {fname:26} {len(svg)/1024:6.1f} KB")
print("done")
