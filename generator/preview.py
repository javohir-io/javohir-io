# -*- coding: utf-8 -*-
"""Dev tool: render built SVGs in Chromium exactly like a README <img>, at chosen animation times.
Usage: python3 generator/preview.py header dark 0.8 4 ..."""
import os, sys, time
from playwright.sync_api import sync_playwright
ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
name, theme, times = sys.argv[1], sys.argv[2], [float(t) for t in sys.argv[3:]] or [3.0]
svg = os.path.join(ROOT, "assets", "dark" if theme == "dark" else "", f"{name}.svg")
bg = "#0d1117" if theme == "dark" else "#ffffff"
os.makedirs("/home/claude/shots", exist_ok=True)
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={"width": 1000, "height": 800}, device_scale_factor=1)
    html = f"/home/claude/shots/_{name}-{theme}.html"
    open(html, "w").write(f'<body style="margin:0;background:{bg}"><img id=i src="file://{svg}" style="display:block;width:1000px"></body>')
    pg.goto(f"file://{html}")
    t0 = time.time()
    for t in times:
        time.sleep(max(0, t - (time.time() - t0)))
        el = pg.query_selector("#i")
        out = f"/home/claude/shots/{name}-{theme}-{t:g}s.png"
        el.screenshot(path=out)
        print(out)
    b.close()
