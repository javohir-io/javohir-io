# -*- coding: utf-8 -*-
"""Drawing engine: quiet neutral palette, hairlines, isometric solids and a slowly turning wireframe.
All text is converted to vector outlines at build time, so nothing loads from the network when the page is viewed.
Motion is plain CSS inside the SVG (GitHub allows it inside an <img>) and switches off for "reduce motion".
"""
import math
import os
import random
import re
from xml.sax.saxutils import escape as _esc

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont


W = 840
HERE = os.path.dirname(os.path.abspath(__file__))


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
        self._pc = {}

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

    def path(self, g):
        if g not in self._pc:
            pen = SVGPathPen(self.gs)
            self.gs[g].draw(pen)
            self._pc[g] = pen.getCommands()
        return self._pc[g]

    def layout(self, text, size, tracking=0.0):
        s = size / self.upm
        out, x = [], 0.0
        names = [self.cmap.get(ord(ch)) for ch in text]
        for i, g in enumerate(names):
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


def wrap(text, font, size, max_w, tracking=0.0):
    lines, cur = [], ""
    for word in text.split():
        t = (cur + " " + word).strip()
        if cur and font.width(t, size, tracking) > max_w:
            lines.append(cur)
            cur = word
        else:
            cur = t
    if cur:
        lines.append(cur)
    return lines


_FD = os.path.join(HERE, "fonts")
SANS = Font(os.path.join(_FD, "InstrumentSans-Regular.ttf"), "s")
SANSB = Font(os.path.join(_FD, "InstrumentSans-Bold.ttf"), "b")
MONO = Font(os.path.join(_FD, "GeistMono-Regular.ttf"), "m")

# Neutral palettes tuned to sit on GitHub's own light / dark canvas. One muted slate-blue accent.
DARK = dict(name="dark", hi="#e6edf3", ink="#b7c0ca", mid="#7d8590", line="#30363d", soft="#21262d", acc="#8aa6c8",
            top="#1b222b", left="#131920", right="#0e1319", otop="#2b3644", oleft="#1e2732", oright="#161d26")
LIGHT = dict(name="light", hi="#1f2328", ink="#3d444d", mid="#6e7781", line="#d0d7de", soft="#e6eaee", acc="#4a6a94",
             top="#f6f8fa", left="#e8ecf0", right="#dce2e8", otop="#ffffff", oleft="#eef1f4", oright="#e1e6eb")

CSS = """
@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-3px)}}
@keyframes flow{to{stroke-dashoffset:-12}}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.25}}
.b1{animation:bob 7s ease-in-out infinite}
.b2{animation:bob 7s ease-in-out -2.4s infinite}
.b3{animation:bob 7s ease-in-out -4.8s infinite}
.fl{animation:flow 1.4s linear infinite}
.pl{animation:pulse 3s ease-in-out infinite}
@media (prefers-reduced-motion:reduce){*{animation:none!important}}
"""


class Doc:
    def __init__(self, c, h, title):
        self.c, self.h, self.title, self.glyphs = c, h, title, {}

    def render(self, body, defs=""):
        c = self.c
        gl = "\n".join(f'<path id="{gid}" d="{f.path(g)}"/>' for gid, (f, g) in sorted(self.glyphs.items()))
        return (f'<svg width="{W}" height="{self.h}" viewBox="0 0 {W} {self.h}" xmlns="http://www.w3.org/2000/svg" '
                f'xmlns:xlink="http://www.w3.org/1999/xlink" role="img" aria-label="{esc(self.title)}"><title>{esc(self.title)}</title>\n'
                f'<defs>\n{gl}\n{defs}\n</defs>\n<style>{CSS}</style>\n'
                f'<rect x=".5" y=".5" width="{W - 1}" height="{self.h - 1}" rx="10" fill="none" stroke="{c["line"]}"/>\n{body}\n</svg>')

    def text(self, t, x, y, size, fill=None, font=SANS, anchor="start", tracking=0.0, max_w=None):
        glyphs, w = font.layout(t, size, tracking)
        if max_w and w > max_w:
            k = max_w / w
            size, tracking = size * k, tracking * k
            glyphs, w = font.layout(t, size, tracking)
        x0 = x - (w / 2 if anchor == "middle" else w if anchor == "end" else 0)
        s = size / font.upm
        uses = []
        for g, gx in glyphs:
            if not font.path(g):
                continue
            gid = f"{font.key}_" + re.sub(r"[^A-Za-z0-9]", "_", g)
            self.glyphs[gid] = (font, g)
            uses.append(f'<use xlink:href="#{gid}" transform="translate({x0 + gx:.2f} {y:.2f}) scale({s:.5f} {-s:.5f})"/>')
        return f'<g fill="{fill or self.c["ink"]}">{"".join(uses)}</g>'

    def sans(self, t, x, y, size=15, fill=None, **k):
        return self.text(t, x, y, size, fill or self.c["ink"], SANS, **k)

    def bold(self, t, x, y, size=18, fill=None, **k):
        return self.text(t, x, y, size, fill or self.c["hi"], SANSB, **k)

    def mono(self, t, x, y, size=12, fill=None, **k):
        k.setdefault("tracking", .2)
        return self.text(t, x, y, size, fill or self.c["mid"], MONO, **k)

    def para(self, text, x, y, width, size=15, lead=23, fill=None, font=SANS, tracking=0.0):
        return "".join(self.text(ln, x, y + i * lead, size, fill or self.c["ink"], font, tracking=tracking)
                       for i, ln in enumerate(wrap(text, font, size, width, tracking)))

    def line(self, x1, y1, x2, y2, col=None, w=1, op=1, dash=None, cls=""):
        da = f' stroke-dasharray="{dash}"' if dash else ""
        k = f' class="{cls}"' if cls else ""
        return f'<path d="M{x1:g} {y1:g}L{x2:g} {y2:g}" stroke="{col or self.c["line"]}" stroke-width="{w}" stroke-opacity="{op}" fill="none"{da}{k}/>'

    def dot(self, x, y, r=3, col=None, cls=""):
        k = f' class="{cls}"' if cls else ""
        return f'<circle cx="{x:g}" cy="{y:g}" r="{r}" fill="{col or self.c["acc"]}"{k}/>'

    # ── isometric solids (2:1) ──
    def _p(self, cx, cy, A, B, i, j, lift=0):
        return (cx + i * A - j * B, cy + .5 * (i * A + j * B) - lift)

    def box(self, cx, cy, A, B, h, kind="plate", grid=False):
        """Box whose bottom-face centre is (cx, cy). kind: plate (large, quiet) or obj (small, lighter, accent edge)."""
        c = self.c
        top, left, right = (c["top"], c["left"], c["right"]) if kind == "plate" else (c["otop"], c["oleft"], c["oright"])
        st = c["line"] if kind == "plate" else c["acc"]
        P = lambda i, j, l=0: self._p(cx, cy, A, B, i, j, l)
        poly = lambda pts: "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts) + "Z"
        o = (f'<path d="{poly([P(-1, 1), P(1, 1), P(1, 1, h), P(-1, 1, h)])}" fill="{left}" stroke="{st}" stroke-linejoin="round"/>'
             f'<path d="{poly([P(1, 1), P(1, -1), P(1, -1, h), P(1, 1, h)])}" fill="{right}" stroke="{st}" stroke-linejoin="round"/>'
             f'<path d="{poly([P(-1, -1, h), P(1, -1, h), P(1, 1, h), P(-1, 1, h)])}" fill="{top}" stroke="{st}" stroke-linejoin="round"/>')
        if grid:
            g = []
            for t in (.25, .5, .75):
                lerp = lambda a, b: (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
                a1, a2 = lerp(P(-1, -1, h), P(1, -1, h)), lerp(P(-1, 1, h), P(1, 1, h))
                b1, b2 = lerp(P(-1, -1, h), P(-1, 1, h)), lerp(P(1, -1, h), P(1, 1, h))
                g.append(f"M{a1[0]:.1f} {a1[1]:.1f}L{a2[0]:.1f} {a2[1]:.1f}M{b1[0]:.1f} {b1[1]:.1f}L{b2[0]:.1f} {b2[1]:.1f}")
            o += f'<path d="{"".join(g)}" stroke="{c["line"]}" stroke-opacity=".55" fill="none"/>'
        return o

    def cylinder(self, cx, cy, r, h):
        c = self.c
        return (f'<path d="M{cx - r} {cy - h}V{cy}A{r} {r / 2} 0 0 0 {cx + r} {cy}V{cy - h}Z" fill="{c["oleft"]}" stroke="{c["acc"]}" stroke-linejoin="round"/>'
                f'<ellipse cx="{cx}" cy="{cy - h}" rx="{r}" ry="{r / 2}" fill="{c["otop"]}" stroke="{c["acc"]}"/>'
                f'<path d="M{cx - r} {cy - h * .5}A{r} {r / 2} 0 0 0 {cx + r} {cy - h * .5}" fill="none" stroke="{c["acc"]}" stroke-opacity=".5"/>')

    # ── turning wireframe (pure SMIL path morph between pre-computed frames) ──
    def wire(self, cx, cy, R, verts, edges, sym_deg, frames, dur, tilt=24, persp=.1):
        c = self.c
        tl = math.radians(tilt)

        def project(vs, th):
            out = []
            for x, y, z in vs:
                x, z = x * math.cos(th) + z * math.sin(th), -x * math.sin(th) + z * math.cos(th)
                y, z = y * math.cos(tl) - z * math.sin(tl), y * math.sin(tl) + z * math.cos(tl)
                f = 1 / (1 - persp * z)
                out.append((cx + x * R * f, cy - y * R * f))
            return out

        el, dl = [], []
        for k in range(frames + 1):
            pts = project(verts, math.radians(sym_deg * k / frames))
            el.append("".join(f"M{pts[a][0]:.1f} {pts[a][1]:.1f}L{pts[b][0]:.1f} {pts[b][1]:.1f}" for a, b in edges))
            dl.append("".join(f"M{x:.1f} {y:.1f}h0" for x, y in pts))
        a = lambda vals: f'<animate attributeName="d" dur="{dur}s" repeatCount="indefinite" values="{";".join(vals)}"/>'
        return (f'<path d="{el[0]}" fill="none" stroke="{c["acc"]}" stroke-width="1.1" stroke-linejoin="round" stroke-opacity=".9">{a(el)}</path>'
                f'<path d="{dl[0]}" fill="none" stroke="{c["hi"]}" stroke-width="3.4" stroke-linecap="round">{a(dl)}</path>')


def icosahedron():
    s5 = math.sqrt(5)
    v = [(0, 1, 0)]
    v += [(2 / s5 * math.cos(math.radians(72 * i)), 1 / s5, 2 / s5 * math.sin(math.radians(72 * i))) for i in range(5)]
    v += [(2 / s5 * math.cos(math.radians(72 * i + 36)), -1 / s5, 2 / s5 * math.sin(math.radians(72 * i + 36))) for i in range(5)]
    v.append((0, -1, 0))
    e = []
    for i in range(5):
        e += [(0, 1 + i), (1 + i, 1 + (i + 1) % 5), (1 + i, 6 + i), (1 + i, 6 + (i - 1) % 5),
              (6 + i, 6 + (i + 1) % 5), (6 + i, 11)]
    return v, e


def cube():
    v = [(x, y, z) for x in (-1, 1) for y in (-1, 1) for z in (-1, 1)]
    e = [(i, j) for i in range(8) for j in range(i + 1, 8) if sum(a != b for a, b in zip(v[i], v[j])) == 1]
    return v, e
