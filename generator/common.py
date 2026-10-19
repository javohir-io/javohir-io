# -*- coding: utf-8 -*-
"""Shared design system: black / white / banana yellow / plum violet, built from capsules.

Everything visual lives here: the two palettes, the outlined-type engine (Poppins is turned into
vector paths at build time, so the type looks identical everywhere and nothing loads at view time),
and the reusable pieces: card, pill, glass capsule, blurred glow blobs.
"""
import os
import re
from xml.sax.saxutils import escape as _esc

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

W = 1000          # every panel is 1000 wide
MX = 64           # horizontal page margin
CARD_R = 44       # corner radius of each panel
HERE = os.path.dirname(os.path.abspath(__file__))

# ─────────────────────────────── palette ───────────────────────────────
BLACK, WHITE, LIME, VIOLET = "#000000", "#FEFFFC", "#D0FF00", "#8116E0"


def mix(a, b, t):
    """t of colour a over colour b."""
    pa = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    pb = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x * t + y * (1 - t)):02x}" for x, y in zip(pa, pb))


# Dark: black poster, white pill. Light: white poster, the white pill becomes black.
# `p1` is the neutral pill, `lime`/`violet` keep their colour in both modes.
DARK = dict(
    name="dark", bg=BLACK, ink=WHITE, mute=mix(WHITE, BLACK, .62), line=mix(WHITE, BLACK, .24),
    band=mix(WHITE, BLACK, .075), p1=WHITE, p1_ink=BLACK, lime=LIME, lime_ink=BLACK,
    violet=VIOLET, violet_ink=WHITE, dot=LIME, card_stroke=None,
    glow_lime=.85, glow_violet=.55, halo=.34,
)
LIGHT = dict(
    name="light", bg=WHITE, ink=BLACK, mute=mix(BLACK, WHITE, .62), line=mix(BLACK, WHITE, .24),
    band=mix(BLACK, WHITE, .06), p1=BLACK, p1_ink=WHITE, lime=LIME, lime_ink=BLACK,
    violet=VIOLET, violet_ink=WHITE, dot=VIOLET, card_stroke=mix(BLACK, WHITE, .12),
    glow_lime=.7, glow_violet=.32, halo=0,
)


def esc(s):
    return _esc(str(s))


# ───────────────────────── outlined type engine ─────────────────────────
class Font:
    def __init__(self, path, key):
        self.key = key
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

    def layout(self, text, size, tracking=0.0):
        """-> ([(glyph, x_px)], width_px)."""
        s = size / self.upm
        out, x = [], 0.0
        names = [self.cmap.get(ord(ch)) for ch in text]
        for i, g in enumerate(names):
            if g is None:
                g = ".notdef" if ".notdef" in self.gs else None
            if g is None:
                continue
            out.append((g, x))
            adv = self.hmtx[g][0]
            if i + 1 < len(names) and names[i + 1]:
                adv += self.kern.get((g, names[i + 1]), 0)
            x += adv * s + tracking
        return out, max(0.0, x - tracking)

    def width(self, text, size, tracking=0.0):
        return self.layout(text, size, tracking)[1]


_FD = os.path.join(HERE, "fonts")
BOLD = Font(os.path.join(_FD, "Poppins-Bold.ttf"), "b")
MED = Font(os.path.join(_FD, "Poppins-Medium.ttf"), "m")


class Glyphs:
    """Per-SVG registry: each distinct glyph outline is stored once in <defs>."""

    def __init__(self):
        self.used = {}

    def ref(self, font, g):
        gid = font.key + "_" + re.sub(r"[^A-Za-z0-9]", "_", g)
        self.used[gid] = (font, g)
        return gid

    def defs(self):
        return "\n".join(f'<path id="{gid}" d="{f.path(g)}"/>' for gid, (f, g) in sorted(self.used.items()))


def otext(reg, text, x, y, size, fill, font=BOLD, anchor="start", tracking=0.0, max_w=None, opacity=None):
    """Outlined text on baseline y. Returns dict(svg, width, x0, size)."""
    glyphs, w = font.layout(text, size, tracking)
    if max_w and w > max_w:
        k = max_w / w
        size, tracking = size * k, tracking * k
        glyphs, w = font.layout(text, size, tracking)
    x0 = x - (w / 2 if anchor == "middle" else w if anchor == "end" else 0)
    s = size / font.upm
    uses = []
    for g, gx in glyphs:
        if not font.path(g):
            continue
        uses.append(f'<use xlink:href="#{reg.ref(font, g)}" transform="translate({x0 + gx:.2f} {y:.2f}) scale({s:.5f} {-s:.5f})"/>')
    op = f' opacity="{opacity}"' if opacity is not None else ""
    return dict(svg=f'<g fill="{fill}"{op}>{"".join(uses)}</g>', width=w, x0=x0, size=size)


def mid(cy, size):
    """Baseline that optically centres lowercase Poppins text on cy."""
    return cy + size * 0.34


def wrap(text, font, size, max_w):
    lines, cur = [], ""
    for word in text.split():
        t = (cur + " " + word).strip()
        if cur and font.width(t, size) > max_w:
            lines.append(cur)
            cur = word
        else:
            cur = t
    if cur:
        lines.append(cur)
    return lines


# ───────────────────────────── scaffolding ──────────────────────────────
BASE_CSS = """
@media (prefers-reduced-motion: reduce){*{animation:none!important}}
@keyframes ping{0%{transform:scale(1);opacity:.75}100%{transform:scale(3.4);opacity:0}}
.ping{transform-box:fill-box;transform-origin:center;animation:ping 2.6s ease-out infinite}
@keyframes drift{0%,100%{transform:translate(0,0)}50%{transform:translate(28px,-20px)}}
@keyframes drift2{0%,100%{transform:translate(0,0)}50%{transform:translate(-24px,16px)}}
.d1{animation:drift 15s ease-in-out infinite}
.d2{animation:drift2 18s ease-in-out infinite}
""".strip()


def svg_open(h, title):
    return (f'<svg width="{W}" height="{h}" viewBox="0 0 {W} {h}" xmlns="http://www.w3.org/2000/svg" '
            f'xmlns:xlink="http://www.w3.org/1999/xlink" role="img" aria-label="{esc(title)}"><title>{esc(title)}</title>')


def assemble(h, title, reg, css, defs, body):
    return (f'{svg_open(h, title)}\n<defs>\n{reg.defs()}\n{defs}\n</defs>\n'
            f'<style>\n{BASE_CSS}\n{css}\n</style>\n{body}\n</svg>')


def card(c, h):
    """Rounded poster slab with a 6px transparent margin top and bottom (the gap between panels).
    Returns (defs, back). Anything that should be cut by the slab goes in <g clip-path="url(#cc)">."""
    ch = h - 12
    stroke = f' stroke="{c["card_stroke"]}"' if c["card_stroke"] else ""
    defs = (f'<clipPath id="cc"><rect x="0" y="6" width="{W}" height="{ch}" rx="{CARD_R}"/></clipPath>'
            '<filter id="b6" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="6"/></filter>'
            '<filter id="b14" x="-40%" y="-40%" width="180%" height="180%"><feGaussianBlur stdDeviation="14"/></filter>'
            '<filter id="b34" x="-60%" y="-60%" width="220%" height="220%"><feGaussianBlur stdDeviation="34"/></filter>'
            '<linearGradient id="rim" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#fff" stop-opacity=".7"/>'
            '<stop offset=".45" stop-color="#fff" stop-opacity=".1"/><stop offset="1" stop-color="#fff" stop-opacity=".35"/></linearGradient>')
    back = f'<rect x="0.5" y="6.5" width="{W-1}" height="{ch-1}" rx="{CARD_R}" fill="{c["bg"]}"{stroke}/>'
    return defs, back


def pill(x, y, w, h, fill=None, stroke=None, sw=1.5, op=None, extra=""):
    f = f'fill="{fill}"' if fill else 'fill="none"'
    s = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    o = f' fill-opacity="{op}"' if op is not None else ""
    return f'<rect x="{x:.2f}" y="{y:.2f}" width="{w:.2f}" height="{h:.2f}" rx="{h / 2:.2f}" {f}{o}{s} {extra}/>'


def tag(reg, c, text, x, y, size=15, h=42, pad=26, dot=False, anchor="start", fill=None, ink=None, stroke=True):
    """Outlined (or filled) pill sized to its label. Returns dict(svg, width)."""
    tw = MED.width(text, size)
    extra = 22 if dot else 0
    w = tw + 2 * pad + extra
    x0 = x - (w / 2 if anchor == "middle" else w if anchor == "end" else 0)
    ink = ink or c["ink"]
    out = pill(x0, y, w, h, fill=fill, stroke=c["line"] if (stroke and not fill) else None, sw=1.5)
    tx = x0 + pad
    if dot:
        dx, dy = x0 + pad + 4, y + h / 2
        out += (f'<circle cx="{dx}" cy="{dy}" r="4.5" fill="{c["dot"]}"/>'
                f'<circle class="ping" cx="{dx}" cy="{dy}" r="4.5" fill="none" stroke="{c["dot"]}" stroke-width="1.5"/>')
        tx += extra
    out += otext(reg, text, tx, mid(y + h / 2, size), size, ink, font=MED)["svg"]
    return dict(svg=out, width=w, x0=x0)


def glow(c, cx, cy, rx, ry, rot, color, op, blur="b34", cls=""):
    cl = f' class="{cls}"' if cls else ""
    return (f'<g{cl}><ellipse cx="{cx}" cy="{cy}" rx="{rx}" ry="{ry}" transform="rotate({rot} {cx} {cy})" '
            f'fill="{color}" opacity="{op}" filter="url(#{blur})"/></g>')


def glass(c, gid, x, y, w, h, rx, seed=0, cls="d1"):
    """A frosted capsule with liquid lime/violet matter moving inside it."""
    cx, cy = x + w / 2, y + h / 2
    sh = [(-.28, -.18, .62, .5, -25), (.2, .28, .5, .38, 30), (.05, -.34, .34, .22, 10)]
    inner = ""
    for i, (ox, oy, sx, sy, rot) in enumerate(sh):
        px, py = cx + ox * w * (1 if (i + seed) % 2 else -1), cy + oy * h
        inner += (f'<ellipse cx="{px:.1f}" cy="{py:.1f}" rx="{w * sx:.1f}" ry="{h * sy * .55:.1f}" '
                  f'transform="rotate({rot + seed * 20} {px:.1f} {py:.1f})" fill="#000" opacity=".82" filter="url(#b6)"/>')
    inner += f'<circle cx="{cx + w * .12 * (-1 if seed % 2 else 1):.1f}" cy="{y + h * .72:.1f}" r="{min(w, h) * .2:.1f}" fill="{VIOLET}" filter="url(#b6)"/>'
    return (f'<clipPath id="{gid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}"/></clipPath>'
            f'<g clip-path="url(#{gid})"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{LIME}" opacity=".9"/>'
            f'<g class="{cls}">{inner}</g>'
            f'<ellipse cx="{x + w * .32:.1f}" cy="{y + h * .12:.1f}" rx="{w * .5:.1f}" ry="{h * .14:.1f}" fill="#fff" opacity=".16"/></g>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="none" stroke="url(#rim)" stroke-width="2"/>')
