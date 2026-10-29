# -*- coding: utf-8 -*-
"""Design system for the profile panels.

Quiet, editorial, technical: near-black (or paper), one red, pale-gray type, hairline rounded boxes, tiny justified
caption paragraphs. Type is converted to vector outlines at build time, so nothing loads from the network when
the page is viewed. Motion is plain SVG (CSS + SMIL), which GitHub allows inside an <img>, and is kept slow and rare.
"""
import math
import os
import random
import re
from xml.sax.saxutils import escape as _esc

from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.ttLib import TTFont

W = 1000
M = 56                       # page margin
HERE = os.path.dirname(os.path.abspath(__file__))

DARK = dict(name="dark", bg="#060606", hi="#ececea", ink="#c9c9c6", mid="#92928f", dim="#2e2e2d", red="#e0242c",
            card_line=.0, speck="#ffffff", speck_op=.55, grain=.5)
LIGHT = dict(name="light", bg="#eae9e5", hi="#0b0b0b", ink="#1c1c1b", mid="#595956", dim="#cdccc7", red="#cf1f27",
             card_line=.14, speck="#000000", speck_op=.45, grain=.5)


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

    def path(self, g, xs=1.0):
        k = (g, xs)
        if k not in self._pc:
            pen = SVGPathPen(self.gs)
            self.gs[g].draw(TransformPen(pen, (xs, 0, 0, 1, 0, 0)) if xs != 1 else pen)
            self._pc[k] = pen.getCommands()
        return self._pc[k]

    def layout(self, text, size, tracking=0.0, xs=1.0):
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
            x += adv * s * xs + tracking
        return out, max(0.0, x - tracking)

    def width(self, text, size, tracking=0.0, xs=1.0):
        return self.layout(text, size, tracking, xs)[1]



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
TECH = Font(os.path.join(_FD, "Tektur-Medium.ttf"), "t")
MONO = Font(os.path.join(_FD, "GeistMono-Regular.ttf"), "m")


def justify(text, font, size, width, tracking=0.0):
    """Greedy-wrap `text`, returning [(words, gap, is_last)] with the gap that justifies each full line."""
    words = text.split()
    sp = font.width(" ", size, tracking) + tracking
    lines, cur, cw = [], [], 0.0
    for wd in words:
        ww = font.width(wd, size, tracking)
        if cur and cw + sp + ww > width:
            lines.append(cur)
            cur, cw = [], 0.0
        cw += (sp if cur else 0) + ww
        cur.append(wd)
    if cur:
        lines.append(cur)
    out = []
    for i, ln in enumerate(lines):
        last = i == len(lines) - 1
        tw = sum(font.width(w_, size, tracking) for w_ in ln)
        gap = sp if (last or len(ln) == 1) else (width - tw) / (len(ln) - 1)
        out.append((ln, gap, last))
    return out


# ═══════════════════════════════════ DOC ═══════════════════════════════════
class Doc:
    """One SVG panel: collects defs/css, hands out ids, owns every drawing helper."""

    def __init__(self, c, h, title):
        self.c, self.h, self.title = c, h, title
        self.glyphs, self.defs, self.css, self.n = {}, [], [], 0
        self.d(f'<clipPath id="cc"><rect x="0" y="6" width="{W}" height="{h - 12}" rx="16"/></clipPath>')

    def uid(self, p="i"):
        self.n += 1
        return f"{p}{self.n}"

    def d(self, s):
        self.defs.append(s)

    def k(self, s):
        self.css.append(s)

    def render(self, body):
        gl = "\n".join(f'<path id="{gid}" d="{f.path(g, xs)}"/>' for gid, (f, g, xs) in sorted(self.glyphs.items()))
        return (f'<svg width="{W}" height="{self.h}" viewBox="0 0 {W} {self.h}" xmlns="http://www.w3.org/2000/svg" '
                f'xmlns:xlink="http://www.w3.org/1999/xlink" role="img" aria-label="{esc(self.title)}"><title>{esc(self.title)}</title>\n'
                f'<defs>\n{gl}\n{chr(10).join(self.defs)}\n</defs>\n<style>\n{BASE_CSS}\n{chr(10).join(self.css)}\n</style>\n{body}\n</svg>')

    # ── type ──
    def gref(self, font, g, xs):
        gid = f"{font.key}{int(xs * 100)}_" + re.sub(r"[^A-Za-z0-9]", "_", g)
        self.glyphs[gid] = (font, g, xs)
        return gid

    def text(self, t, x, y, size, fill=None, font=SANS, anchor="start", tracking=0.0, xs=1.0, max_w=None, opacity=None):
        glyphs, w = font.layout(t, size, tracking, xs)
        if max_w and w > max_w:
            k = max_w / w
            size, tracking = size * k, tracking * k
            glyphs, w = font.layout(t, size, tracking, xs)
        x0 = x - (w / 2 if anchor == "middle" else w if anchor == "end" else 0)
        s = size / font.upm
        uses = [f'<use xlink:href="#{self.gref(font, g, xs)}" transform="translate({x0 + gx:.2f} {y:.2f}) scale({s:.5f} {-s:.5f})"/>'
                for g, gx in glyphs if font.path(g, xs)]
        op = f' opacity="{opacity}"' if opacity is not None else ""
        return dict(svg=f'<g fill="{fill or self.c["ink"]}"{op}>{"".join(uses)}</g>', width=w, x0=x0, size=size)

    def mono(self, t, x, y, size=9, fill=None, anchor="start", tracking=1.4, opacity=None):
        return self.text(t, x, y, size, fill or self.c["mid"], MONO, anchor, tracking, opacity=opacity)["svg"]

    def para(self, text, x, y, width, size=10, lead=16, fill=None, tracking=.5, upper=True):
        """Small, justified, uppercase caption paragraph, like the posters."""
        out = ""
        for i, (words, gap, last) in enumerate(justify(text.upper() if upper else text, SANS, size, width, tracking)):
            cx = x
            for wd in words:
                out += self.text(wd, cx, y + i * lead, size, fill or self.c["ink"], SANS, tracking=tracking)["svg"]
                cx += SANS.width(wd, size, tracking) + gap
        return out

    # ── primitives ──
    def rule(self, x1, y1, x2, y2, op=.28, col=None, dash=None):
        da = f' stroke-dasharray="{dash}"' if dash else ""
        return f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{col or self.c["ink"]}" stroke-opacity="{op}" stroke-width="1"{da}/>'

    def rbox(self, x, y, w, h, r=12, col=None, op=.45, sw=1, fill=None):
        f = f'fill="{fill}"' if fill else 'fill="none"'
        return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" {f} stroke="{col or self.c["ink"]}" stroke-opacity="{op}" stroke-width="{sw}"/>'

    def brackets(self, x, y, w, h, ln=16, col=None, sw=1.3):
        col = col or self.c["red"]
        return (f'<path d="M{x} {y + ln}V{y}H{x + ln}M{x + w - ln} {y}H{x + w}V{y + ln}M{x + w} {y + h - ln}V{y + h}H{x + w - ln}M{x + ln} {y + h}H{x}V{y + h - ln}" '
                f'fill="none" stroke="{col}" stroke-width="{sw}"/>')

    def pill(self, x, y, w, h, text, col=None, size=9, tracking=1.8):
        col = col or self.c["red"]
        return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h / 2}" fill="none" stroke="{col}" stroke-width="1.2"/>'
                + self.mono(text, x + w / 2, y + h / 2 + size * .36, size, self.c["ink"], "middle", tracking))

    def dot(self, x, y, r=3.2, pulse=True):
        red = self.c["red"]
        o = f'<circle cx="{x}" cy="{y}" r="{r}" fill="{red}"/>'
        if pulse:
            o += f'<circle class="ping" cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{red}" stroke-width="1"/>'
        return o

    def head(self, num, title, sub=None):
        c = self.c
        o = self.text(num, M, 98, 50, c["red"], TECH, tracking=1)["svg"]
        o += self.text(title, M + 98, 80, 25, c["hi"], SANS, tracking=-.4)["svg"]
        if sub:
            o += self.mono(sub, M + 98, 104, 9, c["mid"], tracking=1.8)
        return o + self.rule(M, 128, W - M, 128, .22)

    def card(self):
        c = self.c
        stroke = f' stroke="{c["ink"]}" stroke-opacity="{c["card_line"]}"' if c["card_line"] else ""
        return f'<rect x=".5" y="6.5" width="{W - 1}" height="{self.h - 13}" rx="16" fill="{c["bg"]}"{stroke}/>'

    def dust(self, seed=1, n=70):
        """Sparse dust specks and a very light grain, like a worn print."""
        c = self.c
        rnd = random.Random(seed)
        sp = "".join(f'<circle cx="{rnd.uniform(8, W - 8):.0f}" cy="{rnd.uniform(14, self.h - 14):.0f}" r="{rnd.choice([.5, .6, .8, 1.0, 1.3]):.1f}" opacity="{rnd.uniform(.12, c["speck_op"]):.2f}"/>' for _ in range(n))
        self.d('<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".8" numOctaves="1" seed="9"/>'
               '<feColorMatrix type="matrix" values="0 0 0 0 1  0 0 0 0 1  0 0 0 0 1  0 0 0 9 -5.2"/></filter>' if c["name"] == "dark" else
               '<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".8" numOctaves="1" seed="9"/>'
               '<feColorMatrix type="matrix" values="0 0 0 0 0  0 0 0 0 0  0 0 0 0 0  0 0 0 9 -5.2"/></filter>')
        return (f'<g clip-path="url(#cc)" style="pointer-events:none"><rect y="6" width="{W}" height="{self.h - 12}" filter="url(#grain)" opacity=".045"/>'
                f'<g fill="{c["speck"]}">{sp}</g></g>')

    # ── live pieces ──
    def bars(self, x, y, n, step, hmax, w=5.5, seed=3):
        """Signal bars (red). Each breathes at its own slow pace."""
        rnd = random.Random(seed)
        o = ""
        for i in range(n):
            base = .22 + .78 * abs(math.sin(i * .55 + 1.1) * math.cos(i * .23))
            h = hmax * base
            o += (f'<rect class="bar" x="{x + i * step:.1f}" y="{y - h:.1f}" width="{w}" height="{h:.1f}" fill="{self.c["red"]}" '
                  f'style="animation-duration:{rnd.uniform(2.6, 5.4):.1f}s;animation-delay:-{rnd.uniform(0, 5):.1f}s"/>')
        return o

    def meter(self, x, y, label=None):
        """Three small red segments that fill in turn."""
        red = self.c["red"]
        o = "".join(f'<rect x="{x + i * 26}" y="{y}" width="22" height="5" fill="{red}" opacity=".25"><animate attributeName="opacity" values=".25;1;1;.25" keyTimes="0;.12;.8;1" dur="6s" begin="{i * 1.1}s" repeatCount="indefinite"/></rect>' for i in range(3))
        if label:
            o += self.mono(label, x + 88, y + 5.5, 7.5, self.c["mid"], tracking=1.6)
        return o

    def globe(self, cx, cy, r, col=None, spin=18, n=5):
        col = col or self.c["ink"]
        K = 36
        mer = []
        for i in range(n):
            ph = math.pi * i / n
            vals = ";".join(f"{r * abs(math.cos(ph + 2 * math.pi * k / K)):.2f}" for k in range(K + 1))
            mer.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{r}" fill="none"><animate attributeName="rx" values="{vals}" dur="{spin}s" repeatCount="indefinite"/></ellipse>')
        lat = "".join(f'<ellipse cx="{cx}" cy="{cy + r * y:.1f}" rx="{r * math.sqrt(1 - y * y):.1f}" ry="{r * math.sqrt(1 - y * y) * .16:.1f}" fill="none"/>' for y in (-.55, 0, .55))
        return f'<g stroke="{col}" stroke-width="1" opacity=".9"><circle cx="{cx}" cy="{cy}" r="{r}" fill="none"/>{"".join(mer)}{lat}</g>'

    def rings(self, cx, cy, r, col=None):
        col = col or self.c["ink"]
        return f'<g fill="none" stroke="{col}" stroke-width="1.3"><circle cx="{cx - r * .45}" cy="{cy}" r="{r}"/><circle cx="{cx + r * .45}" cy="{cy}" r="{r}"/></g>'

    def surface(self, x, y, w, h, rows=26, cols=70):
        """Ridge-line terrain, back rows hidden by front ones. Returns (svg, peak points) so labels can point at the peaks."""
        c = self.c
        peaks = [(-.55, .42, 1.0, .30, .20), (.30, .30, .78, .26, .22), (.62, .66, .66, .22, .20)]   # u, v, amp, su, sv

        def H(u, v):
            z = sum(a * math.exp(-((u - pu) ** 2 / su ** 2 + (v - pv) ** 2 / sv ** 2)) for pu, pv, a, su, sv in peaks)
            return z + .045 * math.sin(7 * u + 4 * v) * (.4 + v)

        def P(u, v):
            half = .30 + .62 * v
            return (x + w * (.5 + u * half * .5 / .62 * .62), y + h * (.22 + .74 * v) - H(u, v) * h * .36)
        out = ""
        for r in range(rows):
            v = r / (rows - 1)
            pts = [P(-1 + 2 * i / cols, v) for i in range(cols + 1)]
            line = "M" + "L".join(f"{a:.1f} {b:.1f}" for a, b in pts)
            poly = line + f"L{pts[-1][0]:.1f} {y + h + 20}L{pts[0][0]:.1f} {y + h + 20}Z"
            out += f'<path d="{poly}" fill="{c["bg"]}"/><path d="{line}" fill="none" stroke="{c["ink"]}" stroke-width="{.7 + .5 * v:.2f}" stroke-opacity="{.38 + .5 * v:.2f}"/>'
        pk = [P(pu, pv) for pu, pv, *_ in peaks]
        pid = self.uid("sf")
        self.d(f'<clipPath id="{pid}"><rect x="{x - 10}" y="{y}" width="{w + 20}" height="{h}"/></clipPath>')
        self.d(f'<linearGradient id="{pid}g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["red"]}" stop-opacity="0"/><stop offset="1" stop-color="{c["red"]}" stop-opacity=".22"/></linearGradient>')
        scan = (f'<g clip-path="url(#{pid})"><g><rect x="{x - 10}" y="-46" width="{w + 20}" height="46" fill="url(#{pid}g)"/><rect x="{x - 10}" y="-1" width="{w + 20}" height="1.4" fill="{c["red"]}"/>'
                f'<animateTransform attributeName="transform" type="translate" values="0 {y};0 {y + h + 46};0 {y + h + 46}" keyTimes="0;.8;1" dur="8s" repeatCount="indefinite"/></g></g>')
        return out + scan, pk


BASE_CSS = """
@media (prefers-reduced-motion: reduce){*{animation:none!important}}
@keyframes bar{from{transform:scaleY(.35)}to{transform:scaleY(1)}}
.bar{transform-box:fill-box;transform-origin:bottom;animation:bar 3.6s ease-in-out infinite alternate}
@keyframes ping{0%{transform:scale(1);opacity:.8}100%{transform:scale(3.4);opacity:0}}
.ping{transform-box:fill-box;transform-origin:center;animation:ping 2.8s ease-out infinite}
@keyframes blink{0%,60%{opacity:1}61%,100%{opacity:.15}}
.blink{animation:blink 2.2s steps(1) infinite}
""".strip()
