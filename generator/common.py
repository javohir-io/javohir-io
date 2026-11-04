# -*- coding: utf-8 -*-
"""Drawing engine for the HUD panels.

Monochrome only: near-black (or paper) ground, hairlines, tiny mono readouts, wireframe meshes, barcodes.
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

from jp_glyphs import GLYPHS as JP, UPM as JP_UPM

W = 840            # canvas width, about GitHub's README column
X0, X1 = 84, 804   # content area (the left 84px is the rail)
HERE = os.path.dirname(os.path.abspath(__file__))

DARK = dict(name="dark", bg="#070707", hi="#f1f1ef", ink="#c4c4c1", mid="#7c7c79", line="#3a3a38", grid="#262625", dim="#242423", edge="#2a2a29")
LIGHT = dict(name="light", bg="#f3f3f1", hi="#0a0a0a", ink="#222221", mid="#6a6a67", line="#b4b4b0", grid="#dededa", dim="#dcdcd8", edge="#cfcfcb")


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
TECH = Font(os.path.join(_FD, "Tektur-Medium.ttf"), "t")
MONO = Font(os.path.join(_FD, "GeistMono-Regular.ttf"), "m")

BASE_CSS = """
@keyframes spin{to{transform:rotate(360deg)}}
@keyframes spinr{to{transform:rotate(-360deg)}}
@keyframes blink{0%,58%{opacity:1}62%,100%{opacity:.12}}
@keyframes flow{to{stroke-dashoffset:-16}}
@keyframes nudge{50%{transform:translate(2.5px,-2.5px)}}
.sp{animation:spin 110s linear infinite}
.sr{animation:spinr 150s linear infinite}
.sf{animation:spin 36s linear infinite}
.bl{animation:blink 1.8s steps(1,end) infinite}
.fl{animation:flow 1.1s linear infinite}
.nd{animation:nudge 2.6s ease-in-out infinite}
@media (prefers-reduced-motion:reduce){*{animation:none!important}}
"""


class Doc:
    """One SVG panel: collects defs / css, hands out ids, owns every drawing helper."""

    def __init__(self, c, h, title):
        self.c, self.h, self.title = c, h, title
        self.glyphs, self.jglyphs, self.defs, self.css, self.n = {}, {}, [], [], 0

    def uid(self, p="i"):
        self.n += 1
        return f"{p}{self.n}"

    def d(self, s):
        self.defs.append(s)

    def k(self, s):
        self.css.append(s)

    def render(self, body):
        c = self.c
        gl = "\n".join(f'<path id="{gid}" d="{f.path(g)}"/>' for gid, (f, g) in sorted(self.glyphs.items()))
        gl += "\n" + "\n".join(f'<path id="{gid}" d="{d}"/>' for gid, d in sorted(self.jglyphs.items()))
        bg = (f'<rect x=".5" y=".5" width="{W - 1}" height="{self.h - 1}" rx="8" fill="{c["bg"]}" stroke="{c["edge"]}"/>')
        return (f'<svg width="{W}" height="{self.h}" viewBox="0 0 {W} {self.h}" xmlns="http://www.w3.org/2000/svg" '
                f'xmlns:xlink="http://www.w3.org/1999/xlink" role="img" aria-label="{esc(self.title)}"><title>{esc(self.title)}</title>\n'
                f'<defs>\n{gl}\n{chr(10).join(self.defs)}\n</defs>\n<style>\n{BASE_CSS}\n{chr(10).join(self.css)}\n</style>\n{bg}\n{body}\n</svg>')

    # ── type ──
    def _gref(self, font, g):
        gid = f"{font.key}_" + re.sub(r"[^A-Za-z0-9]", "_", g)
        self.glyphs[gid] = (font, g)
        return gid

    def text(self, t, x, y, size, fill=None, font=MONO, anchor="start", tracking=0.0, max_w=None, opacity=None):
        glyphs, w = font.layout(t, size, tracking)
        if max_w and w > max_w:
            k = max_w / w
            size, tracking = size * k, tracking * k
            glyphs, w = font.layout(t, size, tracking)
        x0 = x - (w / 2 if anchor == "middle" else w if anchor == "end" else 0)
        s = size / font.upm
        uses = [f'<use xlink:href="#{self._gref(font, g)}" transform="translate({x0 + gx:.2f} {y:.2f}) scale({s:.5f} {-s:.5f})"/>'
                for g, gx in glyphs if font.path(g)]
        op = f' opacity="{opacity}"' if opacity is not None else ""
        return dict(svg=f'<g fill="{fill or self.c["ink"]}"{op}>{"".join(uses)}</g>', width=w, x0=x0)

    def mono(self, t, x, y, size=11, fill=None, anchor="start", tracking=0.6, opacity=None):
        return self.text(t, x, y, size, fill or self.c["mid"], MONO, anchor, tracking, opacity=opacity)["svg"]

    def tech(self, t, x, y, size, fill=None, anchor="start", tracking=0.0, max_w=None):
        return self.text(t, x, y, size, fill or self.c["hi"], TECH, anchor, tracking, max_w)["svg"]

    def jp(self, t, x, y, size, fill=None, anchor="start", tracking=1.0):
        s = size / JP_UPM
        w = sum(JP[ch][0] * s + tracking for ch in t) - tracking
        x0 = x - (w if anchor == "end" else w / 2 if anchor == "middle" else 0)
        uses, cx = [], x0
        for ch in t:
            adv, d = JP[ch]
            gid = "j_" + format(ord(ch), "x")
            self.jglyphs[gid] = d
            uses.append(f'<use xlink:href="#{gid}" transform="translate({cx:.2f} {y:.2f}) scale({s:.5f} {-s:.5f})"/>')
            cx += adv * s + tracking
        return f'<g fill="{fill or self.c["mid"]}">{"".join(uses)}</g>'

    # ── hairline primitives ──
    def ln(self, x1, y1, x2, y2, col=None, op=1.0, w=1.0, dash=None):
        da = f' stroke-dasharray="{dash}"' if dash else ""
        return f'<path d="M{x1:g} {y1:g}L{x2:g} {y2:g}" stroke="{col or self.c["line"]}" stroke-opacity="{op}" stroke-width="{w}"{da} fill="none"/>'

    def rect(self, x, y, w, h, col=None, op=1.0, sw=1.0, r=0, fill="none", dash=None):
        da = f' stroke-dasharray="{dash}"' if dash else ""
        return (f'<rect x="{x + .5:g}" y="{y + .5:g}" width="{w - 1:g}" height="{h - 1:g}" rx="{r}" fill="{fill}" '
                f'stroke="{col or self.c["line"]}" stroke-opacity="{op}" stroke-width="{sw}"{da}/>')

    def brackets(self, x, y, w, h, n=10, col=None, sw=1.4):
        col = col or self.c["hi"]
        x2, y2 = x + w, y + h
        return (f'<path d="M{x} {y + n}V{y}H{x + n}M{x2 - n} {y}H{x2}V{y + n}M{x2} {y2 - n}V{y2}H{x2 - n}M{x + n} {y2}H{x}V{y2 - n}" '
                f'fill="none" stroke="{col}" stroke-width="{sw}"/>')

    def grid(self, x, y, w, h, step=20, op=.5):
        p = []
        for gx in range(int(step), int(w), int(step)):
            p.append(f"M{x + gx} {y}V{y + h}")
        for gy in range(int(step), int(h), int(step)):
            p.append(f"M{x} {y + gy}H{x + w}")
        return f'<path d="{"".join(p)}" stroke="{self.c["grid"]}" stroke-width="1" fill="none"/>'

    def ruler(self, x, y, w, step=6, every=5):
        p = []
        for i in range(0, int(w / step) + 1):
            h = 7 if i % every == 0 else 3.5
            p.append(f"M{x + i * step} {y}v{h}")
        return f'<path d="{"".join(p)}" stroke="{self.c["mid"]}" stroke-opacity=".8" stroke-width="1" fill="none"/>'

    def dot(self, x, y, r=2.2, col=None, cls=""):
        k = f' class="{cls}"' if cls else ""
        return f'<circle cx="{x:g}" cy="{y:g}" r="{r}" fill="{col or self.c["hi"]}"{k}/>'

    # ── instruments ──
    def dial(self, cx, cy, r, kind="cross"):
        c = self.c
        o = f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{c["ink"]}" stroke-width="1.2"/>'
        o += f'<circle cx="{cx}" cy="{cy}" r="{r - 5}" fill="none" stroke="{c["line"]}" stroke-width="1" stroke-dasharray="1.5 3"/>'
        ticks = "".join(f"M{cx + (r + 2) * math.cos(a):.1f} {cy + (r + 2) * math.sin(a):.1f}L{cx + (r + 5) * math.cos(a):.1f} {cy + (r + 5) * math.sin(a):.1f}"
                        for a in [i * math.pi / 6 for i in range(12)])
        o += f'<path d="{ticks}" stroke="{c["mid"]}" stroke-width="1" fill="none"/>'
        i = r - 8
        if kind == "cross":
            o += f'<path d="M{cx - i} {cy}H{cx + i}M{cx} {cy - i}V{cy + i}" stroke="{c["hi"]}" stroke-width="1.1" fill="none"/>' + self.dot(cx, cy, 2.2)
        elif kind == "x":
            d = i * .72
            o += f'<path d="M{cx - d:.1f} {cy - d:.1f}L{cx + d:.1f} {cy + d:.1f}M{cx + d:.1f} {cy - d:.1f}L{cx - d:.1f} {cy + d:.1f}" stroke="{c["hi"]}" stroke-width="1.4" fill="none"/>'
        else:
            o += f'<circle cx="{cx}" cy="{cy}" r="{i * .55:.1f}" fill="none" stroke="{c["hi"]}" stroke-width="1.2"/>' + self.dot(cx, cy, 1.8)
        # one slow arc that turns
        o += (f'<g class="sf" style="transform-origin:{cx}px {cy}px"><path d="M{cx} {cy - r + 2.5}A{r - 2.5} {r - 2.5} 0 0 1 {cx + (r - 2.5) * .5:.1f} {cy - (r - 2.5) * .866:.1f}" '
              f'stroke="{c["hi"]}" stroke-width="2" fill="none"/></g>')
        return o

    def barcode(self, x, y, w, h, seed, op=.9):
        rng, p, cx = random.Random(seed), [], x
        while cx < x + w - 1:
            bw = rng.choice([1, 1, 1, 2, 2, 3])
            if cx + bw > x + w:
                break
            p.append(f"M{cx} {y}h{bw}v{h}h-{bw}z")
            cx += bw + rng.choice([1, 1, 2, 2, 3])
        return f'<path d="{"".join(p)}" fill="{self.c["ink"]}" fill-opacity="{op}"/>'

    def bars(self, x, y, w, h, seed, n=34, col=None):
        rng, p = random.Random(seed), []
        step = w / n
        v = .5
        for i in range(n):
            v = max(.08, min(1, v + rng.uniform(-.3, .3)))
            bh = max(1.5, h * v)
            p.append(f"M{x + i * step:.1f} {y + h}h{max(step - 2, 1):.1f}v-{bh:.1f}h-{max(step - 2, 1):.1f}z")
        return f'<path d="{"".join(p)}" fill="{col or self.c["ink"]}" fill-opacity=".85"/>'

    def wave(self, x, y, w, h, seed, period=240, amp=.5, scroll=True, col=None):
        """A seamless trace that scrolls sideways. `period` px repeat."""
        rng = random.Random(seed)
        n = int(period / 3)
        base = [rng.uniform(-1, 1) for _ in range(n)]
        pts = []
        for i in range(n + 1):
            t = i / n
            v = (math.sin(t * 2 * math.pi * 3) * .35 + base[i % n] * .55 * (.4 + .6 * abs(math.sin(t * 2 * math.pi)))) * amp
            pts.append((i * period / n, h / 2 - v * h))
        seg = "".join(f"{'M' if i == 0 else 'L'}{px:.1f} {py:.1f}" for i, (px, py) in enumerate(pts))
        d = seg + "".join(f"L{px + period:.1f} {py:.1f}" for px, py in pts[1:]) + "".join(f"L{px + 2 * period:.1f} {py:.1f}" for px, py in pts[1:])
        cid = self.uid("cw")
        self.d(f'<clipPath id="{cid}"><rect x="{x}" y="{y - 2}" width="{w}" height="{h + 4}"/></clipPath>')
        name = self.uid("sc")
        if scroll:
            self.k(f"@keyframes {name}{{to{{transform:translateX(-{period}px)}}}} .{name}{{animation:{name} {period / 14:.0f}s linear infinite}}")
        cls = f' class="{name}"' if scroll else ""
        return (f'<g clip-path="url(#{cid})"><g transform="translate({x} {y})"><g{cls}><path d="{d}" fill="none" stroke="{col or self.c["ink"]}" '
                f'stroke-width="1" stroke-linejoin="round"/></g></g></g>')

    def dotmatrix(self, x, y, cols, rows, seed, step=6, size=3):
        rng, p = random.Random(seed), []
        for r in range(rows):
            for cc in range(cols):
                if rng.random() < .55:
                    p.append(f"M{x + cc * step} {y + r * step}h{size}v{size}h-{size}z")
        return f'<path d="{"".join(p)}" fill="{self.c["ink"]}" fill-opacity=".8"/>'

    # ── wireframe meshes ──
    def mesh(self, cx, cy, R, kind, seed, k=3, maxd=None, spin=True):
        c = self.c
        rng = random.Random(seed)
        pts = []
        if kind == "blob":
            n = 30
            for i in range(n):
                a = 2 * math.pi * i / n + rng.uniform(-.14, .14)
                r = R * (.45 + .55 * rng.random() ** .8)
                pts.append((r * math.cos(a), r * math.sin(a)))
            maxd = maxd or R * .62
        elif kind == "ring":
            n = 40
            for i in range(n):
                a = 2 * math.pi * i / n + rng.uniform(-.06, .06)
                r = R * rng.uniform(.78, 1.0)
                pts.append((r * math.cos(a), r * math.sin(a)))
            for i in range(14):
                a = 2 * math.pi * i / 14 + .3
                pts.append((R * rng.uniform(.4, .56) * math.cos(a), R * rng.uniform(.4, .56) * math.sin(a)))
            maxd = maxd or R * .52
        else:  # rose: concentric rings, each turned a little
            for ring, nn in ((1.0, 24), (.72, 18), (.46, 12), (.22, 6)):
                for i in range(nn):
                    a = 2 * math.pi * i / nn + ring * 1.7
                    pts.append((R * ring * math.cos(a), R * ring * math.sin(a)))
            maxd = maxd or R * .36
        edges = set()
        for i, (ax, ay) in enumerate(pts):
            near = sorted(((math.hypot(ax - bx, ay - by), j) for j, (bx, by) in enumerate(pts) if j != i))[:k]
            for dd, j in near:
                if dd <= maxd:
                    edges.add((min(i, j), max(i, j)))
        lines = "".join(f"M{pts[i][0]:.1f} {pts[i][1]:.1f}L{pts[j][0]:.1f} {pts[j][1]:.1f}" for i, j in sorted(edges))
        nodes = "".join(f"M{px - 1.3:.1f} {py - 1.3:.1f}h2.6v2.6h-2.6z" for px, py in pts)
        body = (f'<path d="{lines}" stroke="{c["ink"]}" stroke-opacity=".6" stroke-width=".8" fill="none"/>'
                f'<path d="{nodes}" fill="{c["hi"]}"/>')
        g = '<g class="sp" style="transform-origin:0px 0px">' if spin else "<g>"
        return f'<g transform="translate({cx} {cy})">{g}{body}</g></g>'

    # ── composed blocks ──
    def kv(self, x, y, w, key, val, size=12, hi=True, live=False):
        c = self.c
        kw = MONO.width(key, size, .5)
        vw = MONO.width(val, size, .3)
        o = self.mono(key, x, y, size, c["mid"], tracking=.5) + self.mono(val, x + w, y, size, c["hi"] if hi else c["ink"], "end", .3)
        o += self.ln(x + kw + 8, y - 3, x + w - vw - 8 - (14 if live else 0), y - 3, c["line"], 1, 1, "1 3")
        if live:
            o += self.dot(x + w - vw - 6, y - 4, 2.6, c["hi"], "bl")
        return o

    def topbar(self, left, jp, tag):
        c = self.c
        o = self.mono(left, 20, 21, 11, c["hi"], tracking=1.4)
        o += self.mono(tag, 20 + MONO.width(left, 11, 1.4) + 22, 21, 11, c["mid"], tracking=1.2)
        o += self.jp(jp, W - 20, 22, 13, c["ink"], "end", 2)
        o += self.ln(20, 34.5, W - 20, 34.5, c["line"], 1) + self.ln(20, 37.5, 160, 37.5, c["mid"], .8)
        return o

    def rail(self, num, label, kind, y=60):
        c = self.c
        o = self.mono(num, 20, y, 11, c["hi"], tracking=1.4)
        o += self.dial(40, y + 44, 16, kind)
        o += f'<rect x="20" y="{y + 82}" width="20" height="3" fill="{c["hi"]}"/>'
        o += self.mono("DATA SET", 20, y + 99, 8, c["mid"], tracking=.6) + self.mono(label, 20, y + 110, 8, c["mid"], tracking=.6)
        return o
