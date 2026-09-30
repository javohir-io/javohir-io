# -*- coding: utf-8 -*-
"""Typography engine.

GitHub renders README SVGs through <img>, which blocks external font loading — so instead of
hoping the visitor has a nice serif installed, every SVG embeds a *subset* of the exact fonts it
uses (only the glyphs that appear in that file) as base64 WOFF. Same typography on every device.

Fonts (both SIL Open Font License):
  serif  — Lora Regular / Lora Italic (display: name, titles, quotes)
  sans   — Poppins Light 300          (body copy)
  sansm  — Poppins Medium 500         (labels, chips)
"""
import base64, io, os
from functools import lru_cache
from fontTools.ttLib import TTFont
from fontTools import subset

HERE = os.path.dirname(os.path.abspath(__file__))
FONT_DIR = os.path.join(HERE, "fonts")

FONTS = {
    "serif": dict(file="Lora-Regular.ttf", family="JA Serif", weight=400, style="normal",
                  stack="'JA Serif',Lora,'Palatino Linotype',Palatino,Georgia,serif"),
    "serifi": dict(file="Lora-Italic.ttf", family="JA Serif", weight=400, style="italic",
                   stack="'JA Serif',Lora,'Palatino Linotype',Palatino,Georgia,serif"),
    "sans":  dict(file="Poppins-Light.ttf", family="JA Sans", weight=300, style="normal",
                  stack="'JA Sans',Poppins,'Segoe UI',Helvetica,Arial,sans-serif"),
    "sansm": dict(file="Poppins-Medium.ttf", family="JA Sans", weight=500, style="normal",
                  stack="'JA Sans',Poppins,'Segoe UI',Helvetica,Arial,sans-serif"),
}


@lru_cache(maxsize=None)
def _font(key):
    return TTFont(os.path.join(FONT_DIR, FONTS[key]["file"]))


@lru_cache(maxsize=None)
def _metrics(key):
    f = _font(key)
    cmap = f.getBestCmap()
    hmtx = f["hmtx"]
    upem = f["head"].unitsPerEm
    return cmap, hmtx, upem


def width(text, key, size, ls=0.0):
    """Advance width of `text` in px (no kerning — close enough for layout)."""
    cmap, hmtx, upem = _metrics(key)
    total = 0
    for ch in text:
        g = cmap.get(ord(ch))
        if g is None:
            g = ".notdef"
        total += hmtx[g][0]
    return total / upem * size + ls * len(text)


def wrap(text, key, size, max_w, ls=0.0):
    words, lines, cur = text.split(), [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if width(trial, key, size, ls) <= max_w or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def missing_glyphs(text, key):
    cmap, _, _ = _metrics(key)
    return sorted({ch for ch in text if ord(ch) not in cmap and not ch.isspace()})


def _subset_b64(key, chars):
    opts = subset.Options()
    opts.flavor = "woff"
    opts.layout_features = ["kern"]
    opts.name_IDs = []
    opts.notdef_outline = True
    opts.hinting = False
    opts.desubroutinize = True
    font = TTFont(os.path.join(FONT_DIR, FONTS[key]["file"]))
    sub = subset.Subsetter(opts)
    sub.populate(text="".join(sorted(chars)) + " ")
    sub.subset(font)
    buf = io.BytesIO()
    font.flavor = "woff"
    font.save(buf)
    return base64.b64encode(buf.getvalue()).decode()


def font_face_css(used):
    """`used` = {font_key: set(chars)} → @font-face rules with embedded subsets."""
    rules = []
    for key, chars in used.items():
        if not chars:
            continue
        spec = FONTS[key]
        b64 = _subset_b64(key, chars)
        rules.append(
            f"@font-face{{font-family:'{spec['family']}';font-weight:{spec['weight']};font-style:{spec['style']};"
            f"src:url(data:font/woff;base64,{b64}) format('woff')}}"
        )
    return "\n".join(rules)
