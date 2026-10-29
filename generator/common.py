# -*- coding: utf-8 -*-
"""Design system for the profile panels.

Quiet, editorial, technical: near-black (or paper), one pink, pale-gray type, hairline rounded boxes, tiny justified
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

from earth_data import LAND

W = 840
M = 40                       # page margin
HERE = os.path.dirname(os.path.abspath(__file__))

DARK = dict(name="dark", bg="#000000", hi="#f2f2f0", ink="#cfcfcc", mid="#8e8e8b", dim="#2a2a2a", acc="#ee1ca4",
            card_line=.0, speck="#ffffff", speck_op=.5)
LIGHT = dict(name="light", bg="#f3f3f2", hi="#0a0a0a", ink="#1b1b1a", mid="#5d5d5a", dim="#cfcfcc", acc="#d8109a",
             card_line=.12, speck="#000000", speck_op=.4)


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


def justify_(text, font, size, width, tracking=0.0):
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

    def mono(self, t, x, y, size=11, fill=None, anchor="start", tracking=1.2, opacity=None):
        return self.text(t, x, y, size, fill or self.c["mid"], MONO, anchor, tracking, opacity=opacity)["svg"]

    def para(self, text, x, y, width, size=14, lead=22, fill=None, tracking=0.0, upper=False, justify=False):
        """Caption paragraph in sentence case, ragged right (justified only on request)."""
        out = ""
        for i, (words, gap, last) in enumerate(justify_(text.upper() if upper else text, SANS, size, width, tracking)):
            cx = x
            for wd in words:
                out += self.text(wd, cx, y + i * lead, size, fill or self.c["ink"], SANS, tracking=tracking)["svg"]
                cx += SANS.width(wd, size, tracking) + (gap if justify else SANS.width(" ", size, tracking) + tracking)
        return out

    # ── primitives ──
    def rule(self, x1, y1, x2, y2, op=.35, col=None, dash=None):
        da = f' stroke-dasharray="{dash}"' if dash else ""
        return f'<path d="M{x1} {y1}L{x2} {y2}" stroke="{col or self.c["ink"]}" stroke-opacity="{op}" stroke-width="1"{da}/>'

    def rbox(self, x, y, w, h, r=12, col=None, op=.6, sw=1.3, fill=None):
        f = f'fill="{fill}"' if fill else 'fill="none"'
        return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" {f} stroke="{col or self.c["ink"]}" stroke-opacity="{op}" stroke-width="{sw}"/>'

    def brackets(self, x, y, w, h, ln=16, col=None, sw=1.3):
        col = col or self.c["acc"]
        return (f'<path d="M{x} {y + ln}V{y}H{x + ln}M{x + w - ln} {y}H{x + w}V{y + ln}M{x + w} {y + h - ln}V{y + h}H{x + w - ln}M{x + ln} {y + h}H{x}V{y + h - ln}" '
                f'fill="none" stroke="{col}" stroke-width="{sw}"/>')

    def pill(self, x, y, w, h, text, col=None, size=9, tracking=1.8):
        col = col or self.c["acc"]
        return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h / 2}" fill="none" stroke="{col}" stroke-width="1.2"/>'
                + self.mono(text, x + w / 2, y + h / 2 + size * .36, size, self.c["ink"], "middle", tracking))

    def dot(self, x, y, r=3.2, pulse=True):
        acc = self.c["acc"]
        o = f'<circle cx="{x}" cy="{y}" r="{r}" fill="{acc}"/>'
        if pulse:
            o += f'<circle class="ping" cx="{x}" cy="{y}" r="{r}" fill="none" stroke="{acc}" stroke-width="1"/>'
        return o

    def head(self, num, title, sub=None):
        c = self.c
        o = self.text(num, M, 54, 28, c["acc"], TECH, tracking=1)["svg"]
        o += self.text(title, M + 58, 49, 21, c["hi"], TECH, tracking=.2)["svg"]
        return o + self.rule(M, 68, W - M, 68, .3)

    def camera(self, x, y, w, h):
        """Viewfinder corners, borrowed from the type-specimen poster."""
        return self.brackets(x, y, w, h, 20, self.c["acc"], 1.6)

    def card(self):
        c = self.c
        stroke = f' stroke="{c["ink"]}" stroke-opacity="{c["card_line"]}"' if c["card_line"] else ""
        return f'<rect x=".5" y="6.5" width="{W - 1}" height="{self.h - 13}" rx="16" fill="{c["bg"]}"{stroke}/>'

    def dust(self, *a, **k):
        return ""

    # ── live pieces ──
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
            out += f'<path d="{poly}" fill="{c["bg"]}"/><path d="{line}" fill="none" stroke="{c["ink"]}" stroke-width="{.9 + .6 * v:.2f}" stroke-opacity="{.5 + .45 * v:.2f}"/>'
        pk = [P(pu, pv) for pu, pv, *_ in peaks]
        pid = self.uid("sf")
        self.d(f'<clipPath id="{pid}"><rect x="{x - 10}" y="{y}" width="{w + 20}" height="{h}"/></clipPath>')
        self.d(f'<linearGradient id="{pid}g" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["acc"]}" stop-opacity="0"/><stop offset="1" stop-color="{c["acc"]}" stop-opacity=".22"/></linearGradient>')
        scan = (f'<g clip-path="url(#{pid})"><g><rect x="{x - 10}" y="-46" width="{w + 20}" height="46" fill="url(#{pid}g)"/><rect x="{x - 10}" y="-1" width="{w + 20}" height="1.4" fill="{c["acc"]}"/>'
                f'<animateTransform attributeName="transform" type="translate" values="0 {y};0 {y + h + 46};0 {y + h + 46}" keyTimes="0;.8;1" dur="8s" repeatCount="indefinite"/></g></g>')
        return out + scan, pk

    # ── 3D wireframes ──
    def earth(self, cx, cy, R, dur=40, K=18):
        """Rotating wireframe Earth: graticule + coarse continent outlines, hidden side parked on the limb."""
        c = self.c
        ink = c["ink"]
        mid = self.uid("em")
        self.d(f'<radialGradient id="{mid}g"><stop offset=".8" stop-color="#fff"/><stop offset="1" stop-color="#000"/></radialGradient>'
               f'<mask id="{mid}"><circle cx="{cx}" cy="{cy}" r="{R + 1}" fill="url(#{mid}g)"/></mask>')

        def frame(theta):
            d = ""
            for poly in LAND:
                pts, vis = [], []
                for lon, lat in poly:
                    lam, ph = math.radians(lon + theta), math.radians(lat)
                    x, z, y = math.cos(ph) * math.sin(lam), math.cos(ph) * math.cos(lam), -math.sin(ph)
                    pts.append([x, y])
                    vis.append(z > 0)
                n = len(pts)
                if not any(vis):
                    ax = sum(p[0] for p in pts) / n
                    ay = sum(p[1] for p in pts) / n
                    m = math.hypot(ax, ay) or 1
                    pts = [[ax / m, ay / m]] * n
                else:
                    start = next(i for i in range(n) if vis[i])           # walk hidden runs, parking each on the limb
                    i = 0
                    while i < n:
                        j = (start + i) % n
                        if vis[j]:
                            i += 1
                            continue
                        run = []
                        while i < n and not vis[(start + i) % n]:
                            run.append((start + i) % n)
                            i += 1
                        ax = sum(pts[k][0] for k in run) / len(run)
                        ay = sum(pts[k][1] for k in run) / len(run)
                        m = math.hypot(ax, ay) or 1
                        for k in run:
                            pts[k] = [ax / m, ay / m]
                d += "M" + "L".join(f"{cx + x * R:.0f} {cy + y * R:.0f}" for x, y in pts) + "Z"
            return d
        vals = ";".join(frame(-360 * k / K) for k in range(K)) + ";" + frame(0)
        lat = "".join(f'<path d="M{cx - R * math.cos(math.radians(a)):.1f} {cy - R * math.sin(math.radians(a)):.1f}H{cx + R * math.cos(math.radians(a)):.1f}"/>' for a in (-60, -30, 0, 30, 60))
        mer = ""
        for i in range(6):
            ph = math.pi * i / 6
            v = ";".join(f"{R * abs(math.sin(ph - 2 * math.pi * k / 36)):.2f}" for k in range(37))
            mer += f'<ellipse cx="{cx}" cy="{cy}" rx="{R}" ry="{R}"><animate attributeName="rx" values="{v}" dur="{dur}s" repeatCount="indefinite"/></ellipse>'
        return (f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="{c["bg"]}"/>'
                f'<g fill="none" stroke="{ink}" stroke-width="1" stroke-opacity=".34">{lat}{mer}</g>'
                f'<g mask="url(#{mid})"><path d="{frame(0)}" fill="none" stroke="{ink}" stroke-width="1.5" stroke-linejoin="round"><animate attributeName="d" values="{vals}" dur="{dur}s" repeatCount="indefinite"/></path></g>'
                f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{ink}" stroke-opacity=".9" stroke-width="1.5"/>')

    def orbit(self, cx, cy, R, rx, ry, rot=-16, dur=9):
        """A ring around the globe with a pink satellite; the far half passes behind it."""
        c = self.c
        acc = c["acc"]
        ring = f'M{-rx} 0A{rx} {ry} 0 1 0 {rx} 0A{rx} {ry} 0 1 0 {-rx} 0'
        front = f'M{-rx} 0A{rx} {ry} 0 0 0 {rx} 0'
        back = (f'<g transform="translate({cx} {cy}) rotate({rot})"><path d="{ring}" fill="none" stroke="{c["ink"]}" stroke-opacity=".5" stroke-width="1.2"/></g>')
        top = (f'<g transform="translate({cx} {cy}) rotate({rot})"><path d="{front}" fill="none" stroke="{c["ink"]}" stroke-opacity=".95" stroke-width="1.4"/>'
               f'<circle r="3.8" fill="{acc}"><animateMotion dur="{dur}s" repeatCount="indefinite" path="{front} A{rx} {ry} 0 0 0 {-rx} 0"/>'
               f'<animate attributeName="opacity" values="1;0" keyTimes="0;.5" calcMode="discrete" dur="{dur}s" repeatCount="indefinite"/></circle></g>')
        return back, top

    SOLIDS = {}

    def solid(self, kind, cx, cy, s, dur=18, tilt=22):
        """A small rotating wireframe object: cube, phone, cylinder, monitor, ico."""
        c = self.c
        V, E, period = _solid(kind)
        K = 8
        ax = math.radians(tilt)

        def frame(ay):
            out = []
            ca, sa = math.cos(ay), math.sin(ay)
            for x, y, z in V:
                x1, z1 = x * ca + z * sa, -x * sa + z * ca
                y1 = y * math.cos(ax) - z1 * math.sin(ax)
                out.append((cx + x1 * s, cy - y1 * s))
            return "".join(f"M{out[a][0]:.1f} {out[a][1]:.1f}L{out[b][0]:.1f} {out[b][1]:.1f}" for a, b in E)
        vals = ";".join(frame(math.radians(period * k / K)) for k in range(K + 1))
        return (f'<path d="{frame(0)}" fill="none" stroke="{c["ink"]}" stroke-width="1.4" stroke-linecap="round" stroke-opacity=".95">'
                f'<animate attributeName="d" values="{vals}" dur="{dur * period / 360:.1f}s" repeatCount="indefinite"/></path>')


BASE_CSS = """
@media (prefers-reduced-motion: reduce){*{animation:none!important}}
@keyframes ping{0%{transform:scale(1);opacity:.8}100%{transform:scale(3.4);opacity:0}}
.ping{transform-box:fill-box;transform-origin:center;animation:ping 2.8s ease-out infinite}
@keyframes blink{0%,60%{opacity:1}61%,100%{opacity:.15}}
.blink{animation:blink 2.2s steps(1) infinite}
""".strip()


def _box(w, h, d):
    V = [(sx * w, sy * h, sz * d) for sx in (-1, 1) for sy in (-1, 1) for sz in (-1, 1)]
    E = [(a, b) for a in range(8) for b in range(a + 1, 8) if bin(a ^ b).count("1") == 1]
    return V, E


def _solid(kind):
    if kind == "cube":
        V, E = _box(.8, .8, .8)
        return V, E, 90
    if kind == "phone":
        V, E = _box(.5, 1.0, .08)
        n = len(V)
        for sx, sy in ((-1, -1), (-1, 1), (1, 1), (1, -1)):
            V.append((sx * .42, sy * .86, .08))
        E += [(n, n + 1), (n + 1, n + 2), (n + 2, n + 3), (n + 3, n)]
        return V, E, 180
    if kind == "monitor":
        V, E = _box(1.25, .8, .07)
        n = len(V)
        for sx, sy in ((-1, -1), (-1, 1), (1, 1), (1, -1)):
            V.append((sx * 1.12, sy * .68, .07))
        V += [(0, -.8, 0), (0, -1.12, 0), (-.45, -1.12, 0), (.45, -1.12, 0)]
        E += [(n, n + 1), (n + 1, n + 2), (n + 2, n + 3), (n + 3, n), (n + 4, n + 5), (n + 6, n + 7)]
        return V, E, 180
    if kind == "cylinder":
        V, E, N = [], [], 16
        for yy in (1.0, .34, -.34, -1.0):
            base = len(V)
            V += [(.85 * math.cos(2 * math.pi * i / N), yy, .85 * math.sin(2 * math.pi * i / N)) for i in range(N)]
            E += [(base + i, base + (i + 1) % N) for i in range(N)]
        for i in (0, 4, 8, 12):
            E += [(i, 3 * N + i)]
        return V, E, 90
    if kind == "ico":
        p = (1 + 5 ** .5) / 2
        V = [(0, sa, sb * p) for sa in (-1, 1) for sb in (-1, 1)] + [(sa, sb * p, 0) for sa in (-1, 1) for sb in (-1, 1)] + [(sb * p, 0, sa) for sa in (-1, 1) for sb in (-1, 1)]
        E = [(a, b) for a in range(12) for b in range(a + 1, 12) if abs(sum((u - v) ** 2 for u, v in zip(V[a], V[b])) - 4) < 1e-6]
        return V, E, 360
    raise ValueError(kind)
