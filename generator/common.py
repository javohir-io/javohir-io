# -*- coding: utf-8 -*-
"""Shared design system for the luxury / minimal profile SVGs.

Everything visual lives here: palettes, the outlined-type engine (so the serif
looks identical on every machine, no webfont needed), and small reusable
ornaments (frames, glints, dust, diamonds).
"""
import math
import os
import random
from xml.sax.saxutils import escape as _esc

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

W = 1000
MX = 72                      # horizontal page margin inside every panel
SANS = "'Helvetica Neue', 'Segoe UI', Inter, Roboto, Arial, sans-serif"
HERE = os.path.dirname(os.path.abspath(__file__))

# ─────────────────────────────── palettes ───────────────────────────────
DARK = dict(
    name="dark",
    bg="#09090a", bg2="#121214", node="#0d0d0f",
    ink="#eee8da", text2="#aaa395", text3="#827c6f",
    gold="#c8aa72", gold_hi="#f3e2b8", gold_lo="#8a6f3e",
    line="#2b2b2e", glow_op=0.13, vinyl="#050506",
)
LIGHT = dict(
    name="light",
    bg="#f9f6ef", bg2="#eee9dc", node="#fcfaf5",
    ink="#16140f", text2="#575245", text3="#716b5c",
    gold="#8f6d2b", gold_hi="#c29a47", gold_lo="#654a17",
    line="#d8d1be", glow_op=0.16, vinyl="#16140f",
)


def esc(s):
    return _esc(str(s))


# ───────────────────────── outlined type engine ─────────────────────────

class Font:
    def __init__(self, path):
        self.tt = TTFont(path)
        self.gs = self.tt.getGlyphSet()
        self.cmap = self.tt.getBestCmap()
        self.upm = self.tt["head"].unitsPerEm
        self.hmtx = self.tt["hmtx"]
        self.kern = self._load_kern()
        self._path_cache = {}

    def _load_kern(self):
        kern = {}
        if "GPOS" not in self.tt:
            return kern
        gpos = self.tt["GPOS"].table
        idxs = set()
        for fr in gpos.FeatureList.FeatureRecord:
            if fr.FeatureTag == "kern":
                idxs.update(fr.Feature.LookupListIndex)
        for i in idxs:
            for st in gpos.LookupList.Lookup[i].SubTable:
                st = getattr(st, "ExtSubTable", st)
                if st.__class__.__name__ != "PairPos":
                    continue
                cov = st.Coverage.glyphs
                if st.Format == 1:
                    for g1, ps in zip(cov, st.PairSet):
                        for rec in ps.PairValueRecord:
                            v = getattr(rec.Value1, "XAdvance", 0) if rec.Value1 else 0
                            if v:
                                kern.setdefault((g1, rec.SecondGlyph), v)
                elif st.Format == 2:
                    cd1, cd2 = st.ClassDef1.classDefs, st.ClassDef2.classDefs
                    for g1 in cov:
                        rec = st.Class1Record[cd1.get(g1, 0)]
                        for g2, c2 in cd2.items():
                            v = rec.Class2Record[c2].Value1
                            xa = getattr(v, "XAdvance", 0) if v else 0
                            if xa:
                                kern.setdefault((g1, g2), xa)
        return kern

    def path(self, gname):
        if gname not in self._path_cache:
            pen = SVGPathPen(self.gs)
            self.gs[gname].draw(pen)
            self._path_cache[gname] = pen.getCommands()
        return self._path_cache[gname]

    def layout(self, text, size, tracking=0.0, kerning=True):
        """-> ([(glyph, x_px)], width_px). Y-up font units are scaled by caller."""
        s = size / self.upm
        out, x = [], 0.0
        names = [self.cmap.get(ord(ch)) for ch in text]
        for i, g in enumerate(names):
            if g is None:
                g = ".notdef" if ".notdef" in self.gs else None
            if g is None:
                continue
            out.append((g, x, text[i]))
            adv = self.hmtx[g][0]
            if kerning and i + 1 < len(names) and names[i + 1]:
                adv += self.kern.get((g, names[i + 1]), 0)
            x += adv * s + tracking
        width = max(0.0, x - tracking)
        return out, width


FONT = Font(os.path.join(HERE, "fonts", "Lora-Variable.ttf"))


class Glyphs:
    """Per-SVG registry: each distinct glyph outline is stored once in <defs>."""

    def __init__(self):
        self.used = {}

    def ref(self, g):
        gid = "g_" + "".join(ch if ch.isalnum() else "_" for ch in g)
        self.used[gid] = g
        return gid

    def defs(self):
        return "\n".join(f'<path id="{gid}" d="{FONT.path(g)}"/>' for gid, g in sorted(self.used.items()))


def otext(reg, text, x, y, size, fill, anchor="start", tracking=0.0, max_w=None,
          anim=None, opacity=None, kerning=True):
    """Outlined text. Returns dict(svg, clip, width, x0).

    anim(i, char) -> inline style string for a per-glyph wrapper (for staggered reveals).
    clip -> the same glyphs as bare <use> nodes, ready to drop inside a <clipPath>.
    """
    glyphs, w = FONT.layout(text, size, tracking, kerning)
    if max_w and w > max_w:
        k = max_w / w
        size, tracking = size * k, tracking * k
        glyphs, w = FONT.layout(text, size, tracking, kerning)
    x0 = x - (w / 2 if anchor == "middle" else w if anchor == "end" else 0)
    s = size / FONT.upm
    uses, clips = [], []
    for i, (g, gx, ch) in enumerate(glyphs):
        if not FONT.path(g):
            continue
        gid = reg.ref(g)
        tf = f"translate({x0 + gx:.2f} {y:.2f}) scale({s:.5f} {-s:.5f})"
        u = f'<use xlink:href="#{gid}" transform="{tf}"/>'
        clips.append(u)
        st = anim(i, ch) if anim else None
        uses.append(f'<g style="{st}">{u}</g>' if st else u)
    op = f' opacity="{opacity}"' if opacity is not None else ""
    return dict(svg=f'<g fill="{fill}"{op}>{"".join(uses)}</g>', clip="".join(clips), width=w, x0=x0, size=size)


def stext(text, x, y, size, fill, anchor="start", weight=400, tracking=0, opacity=None, extra=""):
    """Live (system font) text for small UI copy."""
    a = f'x="{x}" y="{y}" font-family="{SANS}" font-size="{size}" font-weight="{weight}" fill="{fill}"'
    if anchor != "start":
        a += f' text-anchor="{anchor}"'
    if tracking:
        a += f' letter-spacing="{tracking}"'
    if opacity is not None:
        a += f' opacity="{opacity}"'
    return f"<text {a} {extra}>{esc(text)}</text>"


# ───────────────────────────── scaffolding ──────────────────────────────
BASE_CSS = """
@media (prefers-reduced-motion: reduce){*{animation:none!important}}
@keyframes rise{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:translateY(0)}}
@keyframes fade{from{opacity:0}to{opacity:1}}
@keyframes dust{0%{opacity:0;transform:translateY(0)}20%{opacity:1}75%{opacity:1}100%{opacity:0;transform:translateY(-64px)}}
""".strip()


def svg_open(h, title, w=W):
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" '
            f'xmlns:xlink="http://www.w3.org/1999/xlink" role="img" aria-label="{esc(title)}">'
            f'<title>{esc(title)}</title>')


def gold_gradient(c, gid="gold", horizontal=True):
    x2, y2 = ("1", "0") if horizontal else ("0", "1")
    return (f'<linearGradient id="{gid}" x1="0" y1="0" x2="{x2}" y2="{y2}">'
            f'<stop offset="0" stop-color="{c["gold_lo"]}"/><stop offset=".5" stop-color="{c["gold_hi"]}"/>'
            f'<stop offset="1" stop-color="{c["gold"]}"/></linearGradient>')


def frame(c, w, h, glow=(0.5, 0.0), glow_r=0.8):
    """Panel background, vignette glow, hairline double frame, corner diamonds.
    Returns (defs, body)."""
    defs = f'''<linearGradient id="bgv" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c['bg2']}"/><stop offset="1" stop-color="{c['bg']}"/></linearGradient>
<radialGradient id="glow" cx="{glow[0]}" cy="{glow[1]}" r="{glow_r}"><stop offset="0" stop-color="{c['gold']}" stop-opacity="{c['glow_op']}"/><stop offset="1" stop-color="{c['gold']}" stop-opacity="0"/></radialGradient>
{gold_gradient(c)}'''
    m = 10
    body = f'''<rect width="{w}" height="{h}" fill="url(#bgv)"/>
<rect width="{w}" height="{h}" fill="url(#glow)"/>
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" fill="none" stroke="{c['line']}"/>
<rect x="{m}.5" y="{m}.5" width="{w-2*m-1}" height="{h-2*m-1}" fill="none" stroke="{c['gold']}" stroke-opacity=".28"/>
{diamond(m, m, 3.2, c['gold'], bg=c['bg'])}{diamond(w-m, m, 3.2, c['gold'], bg=c['bg'])}
{diamond(m, h-m, 3.2, c['gold'], bg=c['bg'])}{diamond(w-m, h-m, 3.2, c['gold'], bg=c['bg'])}'''
    return defs, body


def diamond(cx, cy, r, stroke, bg=None, fill=None, sw=1):
    pts = f"{cx},{cy-r} {cx+r},{cy} {cx},{cy+r} {cx-r},{cy}"
    f = fill or bg or "none"
    return f'<polygon points="{pts}" fill="{f}" stroke="{stroke}" stroke-width="{sw}"/>'


def glint(c, gid, x1, x2, y, dur=6.0, delay=0.0, length=150, vertical=False, op=1.0):
    """A hairline with a bright traveling highlight. Clip keeps the light on the line."""
    if not vertical:
        return f'''<clipPath id="{gid}c"><rect x="{x1}" y="{y-3}" width="{x2-x1}" height="6"/></clipPath>
<linearGradient id="{gid}g" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{c['gold_hi']}" stop-opacity="0"/><stop offset=".5" stop-color="{c['gold_hi']}" stop-opacity="{op}"/><stop offset="1" stop-color="{c['gold_hi']}" stop-opacity="0"/></linearGradient>
<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{c['line']}" stroke-width="1"/>
<g clip-path="url(#{gid}c)"><rect x="{x1-length}" y="{y-.75}" width="{length}" height="1.5" fill="url(#{gid}g)">
<animate attributeName="x" values="{x1-length};{x2};{x2}" keyTimes="0;.55;1" dur="{dur}s" begin="{-delay}s" repeatCount="indefinite"/></rect></g>'''
    # vertical: x1 is the x position, (x2 = y2) y range is y..x2
    y1, y2 = y, x2
    return f'''<clipPath id="{gid}c"><rect x="{x1-3}" y="{y1}" width="6" height="{y2-y1}"/></clipPath>
<linearGradient id="{gid}g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c['gold_hi']}" stop-opacity="0"/><stop offset=".5" stop-color="{c['gold_hi']}" stop-opacity="{op}"/><stop offset="1" stop-color="{c['gold_hi']}" stop-opacity="0"/></linearGradient>
<line x1="{x1}" y1="{y1}" x2="{x1}" y2="{y2}" stroke="{c['line']}" stroke-width="1"/>
<g clip-path="url(#{gid}c)"><rect x="{x1-.75}" y="{y1-length}" width="1.5" height="{length}" fill="url(#{gid}g)">
<animate attributeName="y" values="{y1-length};{y2};{y2}" keyTimes="0;.6;1" dur="{dur}s" begin="{-delay}s" repeatCount="indefinite"/></rect></g>'''


def dust(c, n, w, h, seed, x_range=None, y_range=None, scale=1.0, opacity=0.7):
    """Slow drifting gold motes — ambient life without noise."""
    rnd = random.Random(seed)
    x0, x1 = x_range or (20, w - 20)
    y0, y1 = y_range or (30, h - 10)
    els = []
    for _ in range(n):
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0, y1)
        r = rnd.choice([0.7, 0.9, 1.1, 1.4]) * scale
        dur, dl = rnd.uniform(9, 18), -rnd.uniform(0, 18)
        els.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" style="animation:dust {dur:.1f}s linear {dl:.1f}s infinite"/>')
    return f'<g fill="{c["gold_hi"] if c["name"]=="dark" else c["gold"]}" opacity="{opacity}">{"".join(els)}</g>'


def section_header(c, reg, numeral, label, y=66, x_end=None):
    """Roman numeral (outlined serif) + tracked label + glinting hairline to the right."""
    x_end = x_end or W - MX
    num = otext(reg, numeral, MX, y + 7, 22, "url(#gold)")
    lx = MX + num["width"] + 18
    lbl = stext(label, lx, y + 4, 11.5, c["text2"], weight=500, tracking=4)
    approx = len(label) * 11.5 * 0.64 + len(label) * 4
    rule = glint(c, "hdr", lx + approx + 24, x_end, y, dur=7.5, delay=1.5)
    end = diamond(x_end, y, 3, c["gold"], bg=c["bg"])
    sep = f'<line x1="{lx-9}" y1="{y-9}" x2="{lx-9}" y2="{y+9}" stroke="{c["gold"]}" stroke-opacity=".5"/>'
    return f"{num['svg']}{sep}{lbl}{rule}{end}"
