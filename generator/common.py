# -*- coding: utf-8 -*-
"""Y2K design system for the profile SVGs.

Chrome type, holographic gradients, glass windows, a spinning CD, a morphing liquid-metal blob,
wireframe globes, lens flares and pixel art, all of it animated with plain SVG (CSS + SMIL), which is
what GitHub allows inside an <img>. Type is converted to vector outlines at build time, so nothing is
loaded from the network when the page is viewed.
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
MX = 56
CARD_R = 36
HERE = os.path.dirname(os.path.abspath(__file__))

HOLO = ["#7ee8ff", "#8fa2ff", "#c28bff", "#ff8fe0", "#ffc79a", "#fff3a8", "#9dffd0"]
CHROME = [(0, "#ffffff"), (.16, "#e4e9ff"), (.34, "#8791e6"), (.46, "#1a1c58"), (.5, "#070820"), (.55, "#5f6bd8"), (.7, "#c4cfff"), (.86, "#ffffff"), (1, "#97a2f4")]


def mix(a, b, t):
    pa = [int(a[i:i + 2], 16) for i in (1, 3, 5)]
    pb = [int(b[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x * t + y * (1 - t)):02x}" for x, y in zip(pa, pb))


DARK = dict(
    name="dark", bg1="#04040c", bg2="#0c0d2a", ink="#f4f6ff", mute="#a2a8d4", line="#ffffff", line_op=.26,
    glass1=.13, glass2=.03, bar_op=.09, grid_op=.05, blob_op=.3, shadow=False, rim="#ffffff", ink_inv="#0a0b1f",
    card_stroke="#ffffff", card_stroke_op=.14, accent="#7ee8ff", dim="#3a3f7a",
)
LIGHT = dict(
    name="light", bg1="#e6e8f4", bg2="#c4c8e2", ink="#0a0b1f", mute="#474c7a", line="#ffffff", line_op=.95, glass1=.62,
    glass2=.22, bar_op=.4, grid_op=.5, blob_op=.7, shadow=True, rim="#ffffff", ink_inv="#f4f6ff",
    card_stroke="#8d93c9", card_stroke_op=.35, accent="#5b61b8", dim="#9aa0d0",
)


def esc(s):
    return _esc(str(s))


def holo_at(t):
    """Smooth walk through the holographic palette, t in [0,1) wraps."""
    t = (t % 1.0) * (len(HOLO))
    i = int(t) % len(HOLO)
    return mix(HOLO[(i + 1) % len(HOLO)], HOLO[i], t - int(t))


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


_FD = os.path.join(HERE, "fonts")
BOLD = Font(os.path.join(_FD, "Poppins-Bold.ttf"), "b")
MED = Font(os.path.join(_FD, "Poppins-Medium.ttf"), "m")
MONO = Font(os.path.join(_FD, "GeistMono-Regular.ttf"), "r")
MONOB = Font(os.path.join(_FD, "GeistMono-Bold.ttf"), "t")
PIX = Font(os.path.join(_FD, "Silkscreen-Regular.ttf"), "p")


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


# ═══════════════════════════════════ DOC ═══════════════════════════════════
class Doc:
    """One SVG panel. Collects defs/css, hands out unique ids, and owns every drawing helper."""

    def __init__(self, c, h, title):
        self.c, self.h, self.title = c, h, title
        self.glyphs = {}
        self.defs, self.css, self.n = [], [], 0
        self.base()

    # ── plumbing ──
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

    def text(self, t, x, y, size, fill=None, font=MED, anchor="start", tracking=0.0, xs=1.0, max_w=None, opacity=None, raw=False):
        glyphs, w = font.layout(t, size, tracking, xs)
        if max_w and w > max_w:
            k = max_w / w
            size, tracking = size * k, tracking * k
            glyphs, w = font.layout(t, size, tracking, xs)
        x0 = x - (w / 2 if anchor == "middle" else w if anchor == "end" else 0)
        s = size / font.upm
        uses = [f'<use xlink:href="#{self.gref(font, g, xs)}" transform="translate({x0 + gx:.2f} {y:.2f}) scale({s:.5f} {-s:.5f})"/>'
                for g, gx in glyphs if font.path(g, xs)]
        if raw:
            return dict(uses=uses, width=w, x0=x0, size=size, y=y)
        op = f' opacity="{opacity}"' if opacity is not None else ""
        return dict(svg=f'<g fill="{fill or self.c["ink"]}"{op}>{"".join(uses)}</g>', width=w, x0=x0, size=size, uses=uses)

    def label(self, t, x, y, size=11, fill=None, anchor="start", tracking=1.2, opacity=None, bold=False):
        return self.text(t, x, y, size, fill or self.c["mute"], font=MONOB if bold else MONO, anchor=anchor, tracking=tracking, opacity=opacity)["svg"]

    def chrome(self, t, x, y, size, xs=1.3, tracking=0.0, anchor="middle", max_w=None, sheen=True, rim=None):
        """Liquid-chrome lettering: silver rim, dark keyline, banded sky/horizon fill, gloss, travelling sheen."""
        r = self.text(t, x, y, size, font=BOLD, anchor=anchor, tracking=tracking, xs=xs, max_w=max_w, raw=True)
        size = r["size"]
        k = BOLD.upm / size            # px -> glyph units (gradients and strokes live in glyph space)
        top_f, bot_f = .74 * BOLD.upm, -.02 * BOLD.upm
        top, bot = y - size * .74, y + size * .02
        gid, sid, cid = self.uid("ch"), self.uid("sh"), self.uid("cl")
        stops = "".join(f'<stop offset="{o}" stop-color="{col}"/>' for o, col in CHROME)
        gy = f'gradientUnits="userSpaceOnUse" x1="0" y1="{top_f:.0f}" x2="0" y2="{bot_f:.0f}"'
        self.d(f'<linearGradient id="{gid}" {gy}>{stops}</linearGradient>')
        self.d(f'<linearGradient id="{gid}r" {gy}><stop offset="0" stop-color="#ffffff"/><stop offset=".5" stop-color="#aeb8ff"/><stop offset="1" stop-color="#ffffff"/></linearGradient>')
        self.d(f'<linearGradient id="{gid}g" gradientUnits="userSpaceOnUse" x1="0" y1="{top_f:.0f}" x2="0" y2="{top_f * .25:.0f}">'
               f'<stop offset="0" stop-color="#fff" stop-opacity=".95"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>')
        hs = "".join(f'<stop offset="{i / (len(HOLO) - 1):.3f}" stop-color="{col}"/>' for i, col in enumerate(HOLO))
        self.d(f'<linearGradient id="{gid}h" gradientUnits="userSpaceOnUse" x1="0" y1="{top_f:.0f}" x2="{BOLD.upm * 1.1:.0f}" y2="{bot_f:.0f}">{hs}</linearGradient>')
        self.d(f'<clipPath id="{cid}">{"".join(r["uses"])}</clipPath>')
        rw = max(5.0, size * .07) * k
        u = "".join(r["uses"])
        out = (f'<g fill="none" stroke="url(#{gid}r)" stroke-width="{rw:.0f}" stroke-linejoin="round">{u}</g>'
               f'<g fill="none" stroke="#12143a" stroke-width="{rw * .45:.0f}" stroke-linejoin="round">{u}</g>'
               f'<g fill="url(#{gid})">{u}</g>'
               f'<g fill="url(#{gid}h)" opacity=".22" style="mix-blend-mode:overlay">{u}</g>'
               f'<g fill="url(#{gid}g)" opacity=".6">{u}</g>'
               f'<g fill="none" stroke="#fff" stroke-opacity=".8" stroke-width="{1.3 * k:.0f}" stroke-linejoin="round">{u}</g>')
        if sheen:
            x0, x1 = r["x0"] - 120, r["x0"] + r["width"] + 60
            self.d(f'<linearGradient id="{sid}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/>'
                   f'<stop offset=".5" stop-color="#fff" stop-opacity=".95"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>')
            out += (f'<g clip-path="url(#{cid})"><g transform="skewX(-22)"><rect x="0" y="{top - 10:.1f}" width="90" height="{bot - top + 24:.1f}" fill="url(#{sid})" opacity=".9">'
                    f'<animate attributeName="x" values="{x0:.0f};{x1:.0f};{x1:.0f}" keyTimes="0;.42;1" dur="6.5s" repeatCount="indefinite"/></rect></g></g>')
        return out

    # ── scene ──
    def base(self):
        c = self.c
        for b in (2, 4, 8, 20, 44):
            self.d(f'<filter id="b{b}" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="{b}"/></filter>')
        stops = "".join(f'<stop offset="{i / len(HOLO):.3f}" stop-color="{col}"/>' for i, col in enumerate(HOLO + [HOLO[0]]))
        stops = "".join(f'<stop offset="{i / len(HOLO):.4f}" stop-color="{col}"/>' for i, col in enumerate(HOLO + [HOLO[0]]))
        self.d(f'<linearGradient id="holo" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="520" y2="140" spreadMethod="repeat">{stops}'
               f'<animateTransform attributeName="gradientTransform" type="translate" from="0 0" to="520 0" dur="12s" repeatCount="indefinite"/></linearGradient>')
        stops_c = "".join(f'<stop offset="{o}" stop-color="{col}"/>' for o, col in CHROME)
        self.d(f'<linearGradient id="chromeG" x1="0" y1="0" x2="0" y2="1">{stops_c}</linearGradient>')
        self.d(f'<linearGradient id="chromeD" x1="0" y1="0" x2="1" y2="1">{stops_c}</linearGradient>')
        self.d(f'<linearGradient id="edge" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c["line"]}" stop-opacity="{min(1, c["line_op"] + .35)}"/>'
               f'<stop offset=".5" stop-color="{c["line"]}" stop-opacity="{c["line_op"] * .45:.2f}"/><stop offset="1" stop-color="{c["line"]}" stop-opacity="{c["line_op"] * .9:.2f}"/></linearGradient>')
        self.d(f'<clipPath id="cc"><rect x="0" y="6" width="{W}" height="{self.h - 12}" rx="{CARD_R}"/></clipPath>')
        self.d(f'<linearGradient id="bgv" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["bg1"]}"/><stop offset="1" stop-color="{c["bg2"]}"/></linearGradient>')
        self.d('<pattern id="grid" width="36" height="36" patternUnits="userSpaceOnUse"><path d="M36 0H0V36" fill="none" stroke="%s" stroke-opacity="%s" stroke-width="1"/></pattern>'
               % (c["line"] if c["name"] == "dark" else "#ffffff", c["grid_op"]))
        if c["shadow"]:
            self.d('<filter id="sh" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="10" stdDeviation="12" flood-color="#5a60a8" flood-opacity=".28"/></filter>')

    def backdrop(self, blobs=None):
        """Poster slab: gradient, drifting iridescent light, fine grid, hairline border."""
        c, h = self.c, self.h
        blobs = blobs if blobs is not None else [(140, h * .25, 300, 180, "#7ee8ff"), (860, h * .3, 320, 200, "#c28bff"),
                                                  (520, h * .95, 380, 160, "#ff8fe0"), (900, h * .9, 220, 140, "#9dffd0")]
        bl = "".join(f'<ellipse class="d{i % 3}" cx="{x:.0f}" cy="{y:.0f}" rx="{rx}" ry="{ry}" fill="{col}" opacity="{c["blob_op"]}" filter="url(#b44)"/>'
                     for i, (x, y, rx, ry, col) in enumerate(blobs))
        return (f'<rect x=".5" y="6.5" width="{W - 1}" height="{h - 13}" rx="{CARD_R}" fill="url(#bgv)"/>'
                f'<g clip-path="url(#cc)">{bl}<rect y="6" width="{W}" height="{h - 12}" fill="url(#grid)"/></g>')

    def frame(self):
        c = self.c
        return f'<rect x=".5" y="6.5" width="{W - 1}" height="{self.h - 13}" rx="{CARD_R}" fill="none" stroke="{c["card_stroke"]}" stroke-opacity="{c["card_stroke_op"]}"/>'

    def star(self, cx, cy, r, fill="#fff", delay=0.0, dur=3.6, glow=True, spin=True):
        d = "M0 -1C.07 -.16 .16 -.07 1 0C.16 .07 .07 .16 0 1C-.07 .16 -.16 .07 -1 0C-.16 -.07 -.07 -.16 0 -1Z"
        g = (f'<g transform="translate({cx} {cy}) scale({r})"><path d="{d}" fill="{fill}" opacity=".55" filter="url(#b2)" transform="scale(1.15)"/></g>' if glow else "")
        return (f'{g}<g transform="translate({cx} {cy})"><g class="tw" style="animation-duration:{dur}s;animation-delay:-{delay}s">'
                f'<path d="{d}" transform="scale({r})" fill="{fill}"/></g></g>')

    def chrome_star(self, cx, cy, r, dur=26):
        d = "M0 -1C.09 -.2 .2 -.09 1 0C.2 .09 .09 .2 0 1C-.09 .2 -.2 .09 -1 0C-.2 -.09 -.09 -.2 0 -1Z"
        return (f'<g transform="translate({cx} {cy})"><g class="pulse"><g class="spin" style="animation-duration:{dur}s">'
                f'<path d="{d}" transform="scale({r * 1.06})" fill="#14163f" stroke="#14163f" stroke-width="{.06}" stroke-linejoin="round"/>'
                f'<path d="{d}" transform="scale({r})" fill="url(#chromeD)" stroke="#fff" stroke-width="{.035}" stroke-linejoin="round"/>'
                f'<path d="{d}" transform="scale({r * .72})" fill="none" stroke="#fff" stroke-opacity=".7" stroke-width="{.02}"/></g></g></g>')

    def flare(self, cx, cy, r, color="#ffffff", delay=0.0, dur=4.4):
        gid = self.uid("fl")
        self.d(f'<radialGradient id="{gid}"><stop offset="0" stop-color="#fff"/><stop offset=".25" stop-color="{color}" stop-opacity=".9"/><stop offset="1" stop-color="{color}" stop-opacity="0"/></radialGradient>')
        return (f'<g transform="translate({cx} {cy})"><g class="flare" style="animation-duration:{dur}s;animation-delay:-{delay}s">'
                f'<circle r="{r}" fill="url(#{gid})"/><ellipse rx="{r * 2.6}" ry="{r * .09}" fill="#fff" opacity=".9"/>'
                f'<ellipse rx="{r * .09}" ry="{r * 2.2}" fill="#fff" opacity=".9"/><circle r="{r * .22}" fill="#fff"/></g></g>')

    def bubble(self, cx, cy, r, delay=0.0, dur=11.0, rise=70):
        gid = self.uid("bu")
        self.d(f'<radialGradient id="{gid}" cx=".5" cy=".5" r=".5"><stop offset=".55" stop-color="#fff" stop-opacity="0"/>'
               f'<stop offset=".85" stop-color="#8fa2ff" stop-opacity=".35"/><stop offset="1" stop-color="#ff8fe0" stop-opacity=".75"/></radialGradient>')
        k = self.uid("bk")
        self.k(f"@keyframes {k}{{0%{{transform:translate(0,0)}}50%{{transform:translate(10px,{-rise / 2}px)}}100%{{transform:translate(0,{-rise}px)}}}}")
        return (f'<g style="animation:{k} {dur}s ease-in-out -{delay}s infinite alternate"><g transform="translate({cx} {cy})">'
                f'<circle r="{r}" fill="url(#{gid})" stroke="#fff" stroke-opacity=".55" stroke-width="1"/>'
                f'<ellipse cx="{-r * .34}" cy="{-r * .4}" rx="{r * .22}" ry="{r * .12}" fill="#fff" opacity=".9" transform="rotate(-35 {-r * .34} {-r * .4})"/></g></g>')

    # blobs
    def _blob_d(self, cx, cy, radii, sx=1.0, sy=1.0, rot=0.0):
        n = len(radii)
        pts = []
        for i, r in enumerate(radii):
            a = 2 * math.pi * i / n + rot
            pts.append((cx + r * sx * math.cos(a), cy + r * sy * math.sin(a)))
        d = f"M{pts[0][0]:.1f} {pts[0][1]:.1f}"
        for i in range(n):
            p0, p1, p2, p3 = pts[i - 1], pts[i], pts[(i + 1) % n], pts[(i + 2) % n]
            c1 = (p1[0] + (p2[0] - p0[0]) / 6, p1[1] + (p2[1] - p0[1]) / 6)
            c2 = (p2[0] - (p3[0] - p1[0]) / 6, p2[1] - (p3[1] - p1[1]) / 6)
            d += f"C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {p2[0]:.1f} {p2[1]:.1f}"
        return d + "Z"

    def _morph(self, pid, cx, cy, R, n, var, seed, dur, sx=1.0, sy=1.0, rot=0.0, frames=4):
        rnd = random.Random(seed)
        fr = []
        for _ in range(frames - 1):
            fr.append(self._blob_d(cx, cy, [R * (1 + rnd.uniform(-var, var)) for _ in range(n)], sx, sy, rot))
        fr.append(fr[0])
        # frames[0] first so the loop closes
        vals = ";".join(fr)
        kt = ";".join(f"{i / (len(fr) - 1):.3f}" for i in range(len(fr)))
        ks = ";".join(".45 0 .55 1" for _ in range(len(fr) - 1))
        self.d(f'<path id="{pid}" d="{fr[0]}"><animate attributeName="d" values="{vals}" keyTimes="{kt}" calcMode="spline" keySplines="{ks}" dur="{dur}s" repeatCount="indefinite"/></path>')

    def liquid_ring(self, cx, cy, R, thick=44, seed=3, dur=13, sx=1.0, sy=1.0):
        """A glass/chrome tube bent into a loop that slowly changes shape."""
        pid = self.uid("rg")
        self._morph(pid, cx, cy, R, 7, .22, seed, dur, sx, sy)
        layers = [(thick, "#10123a", "none", 1), (thick - 4, "url(#chromeD)", "none", 1), (thick * .62, "url(#holo)", "none", .9),
                  (thick * .3, "#ffffff", "none", .35)]
        out = "".join(f'<use xlink:href="#{pid}" fill="none" stroke="{col}" stroke-width="{w:.1f}" opacity="{op}" stroke-linejoin="round"/>' for w, col, _, op in layers)
        out += (f'<use xlink:href="#{pid}" fill="none" stroke="#fff" stroke-width="{thick * .16:.1f}" stroke-linecap="round" opacity=".95" transform="translate({-thick * .16:.1f} {-thick * .2:.1f})" '
                f'stroke-dasharray="110 520" filter="url(#b2)"><animate attributeName="stroke-dashoffset" from="0" to="-630" dur="{dur * .8}s" repeatCount="indefinite"/></use>')
        out += (f'<use xlink:href="#{pid}" fill="none" stroke="#7ee8ff" stroke-width="{thick * .1:.1f}" stroke-linecap="round" opacity=".7" transform="translate({thick * .14:.1f} {thick * .2:.1f})" '
                f'stroke-dasharray="70 560"><animate attributeName="stroke-dashoffset" from="-300" to="-930" dur="{dur * .9}s" repeatCount="indefinite"/></use>')
        return out

    def chrome_blob(self, cx, cy, R, seed=5, dur=11, sx=1.0, sy=1.0, rot=0.0):
        """Solid liquid-metal blob."""
        pid, rid = self.uid("bl"), self.uid("rd")
        self._morph(pid, cx, cy, R, 8, .26, seed, dur, sx, sy, rot)
        self.d(f'<radialGradient id="{rid}" cx=".32" cy=".28" r=".7"><stop offset="0" stop-color="#fff" stop-opacity=".95"/><stop offset=".35" stop-color="#fff" stop-opacity=".12"/>'
               f'<stop offset="1" stop-color="#000" stop-opacity=".25"/></radialGradient>')
        return (f'<use xlink:href="#{pid}" fill="#10123a" stroke="#10123a" stroke-width="5" stroke-linejoin="round"/>'
                f'<use xlink:href="#{pid}" fill="url(#chromeD)" stroke="#fff" stroke-width="2" stroke-linejoin="round"/>'
                f'<use xlink:href="#{pid}" fill="url(#holo)" opacity=".38" style="mix-blend-mode:overlay"/>'
                f'<use xlink:href="#{pid}" fill="url(#{rid})"/>'
                f'<use xlink:href="#{pid}" fill="none" stroke="#fff" stroke-width="3" stroke-linecap="round" opacity=".9" stroke-dasharray="60 400" filter="url(#b2)">'
                f'<animate attributeName="stroke-dashoffset" from="0" to="-460" dur="{dur * .7}s" repeatCount="indefinite"/></use>')

    def cd(self, cx, cy, r, tilt=-24, squash=.62, spin=18, id_=None):
        """Holographic disc: rainbow wedges turn while the glare stays put."""
        cid = self.uid("cd")
        hole, hub = r * .1, r * .3
        N = 48
        wedges = []
        for i in range(N):
            a0, a1 = math.radians(i * 360 / N), math.radians((i + 1.6) * 360 / N)
            col = holo_at(i / N * 1.5)
            col = mix("#ffffff", col, .42 * (.5 + .5 * math.sin(i / N * 4 * math.pi)))
            col = mix("#4b3fc0", col, .34 * (.5 + .5 * math.cos(i / N * 4 * math.pi + 1.6)))
            wedges.append(f'<path d="M{cx} {cy}L{cx + r * 1.1 * math.cos(a0):.1f} {cy + r * 1.1 * math.sin(a0):.1f}A{r * 1.1:.1f} {r * 1.1:.1f} 0 0 1 {cx + r * 1.1 * math.cos(a1):.1f} {cy + r * 1.1 * math.sin(a1):.1f}Z" fill="{col}"/>')
        ring = (f"M{cx - r} {cy}a{r} {r} 0 1 0 {2 * r} 0a{r} {r} 0 1 0 {-2 * r} 0Z"
                f"M{cx - hole} {cy}a{hole} {hole} 0 1 0 {2 * hole} 0a{hole} {hole} 0 1 0 {-2 * hole} 0Z")
        self.d(f'<clipPath id="{cid}"><path clip-rule="evenodd" d="{ring}"/></clipPath>')
        self.d(f'<radialGradient id="{cid}r" cx=".5" cy=".5" r=".5"><stop offset=".25" stop-color="#fff" stop-opacity=".0"/><stop offset=".62" stop-color="#fff" stop-opacity=".0"/>'
               f'<stop offset="1" stop-color="#fff" stop-opacity=".28"/></radialGradient>')
        glare = "".join(f'<path d="M{cx} {cy}L{cx + r * math.cos(math.radians(a)):.1f} {cy + r * math.sin(math.radians(a)):.1f}A{r} {r} 0 0 1 '
                        f'{cx + r * math.cos(math.radians(a + 26)):.1f} {cy + r * math.sin(math.radians(a + 26)):.1f}Z" fill="#fff" opacity=".42"/>' for a in (200, 20))
        grooves = "".join(f'<circle cx="{cx}" cy="{cy}" r="{r * f:.1f}" fill="none" stroke="#fff" stroke-opacity=".12" stroke-width=".8"/>' for f in (.42, .5, .58, .66, .74, .82, .9))
        body = (f'<ellipse cx="{cx}" cy="{cy + r * .06}" rx="{r}" ry="{r}" fill="#000" opacity=".28" filter="url(#b8)"/>'
                f'<g clip-path="url(#{cid})"><g filter="url(#b2)"><g><animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="{spin}s" repeatCount="indefinite"/>{"".join(wedges)}</g></g>'
                f'<g filter="url(#b8)">{glare}</g>{grooves}<circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{cid}r)"/>'
                f'<circle cx="{cx}" cy="{cy}" r="{hub}" fill="#fff" opacity=".24"/><circle cx="{cx}" cy="{cy}" r="{hub}" fill="none" stroke="#fff" stroke-opacity=".8" stroke-width="1.5"/>'
                f'<circle cx="{cx}" cy="{cy}" r="{hub * .62}" fill="none" stroke="#fff" stroke-opacity=".45"/></g>'
                f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#fff" stroke-opacity=".9" stroke-width="2"/>'
                f'<circle cx="{cx}" cy="{cy}" r="{hole}" fill="none" stroke="#fff" stroke-opacity=".8" stroke-width="1.5"/>')
        return f'<g transform="rotate({tilt} {cx} {cy}) translate({cx} {cy}) scale(1 {squash}) translate({-cx} {-cy})">{body}</g>'

    def globe(self, cx, cy, r, col=None, spin=16, n=6, op=.85):
        col = col or self.c["ink"]
        K = 36
        mer = []
        for i in range(n):
            ph = math.pi * i / n
            vals = ";".join(f"{r * abs(math.cos(ph + 2 * math.pi * k / K)):.2f}" for k in range(K + 1))
            mer.append(f'<ellipse cx="{cx}" cy="{cy}" rx="{r:.1f}" ry="{r}" fill="none"><animate attributeName="rx" values="{vals}" dur="{spin}s" repeatCount="indefinite"/></ellipse>')
        lat = "".join(f'<ellipse cx="{cx}" cy="{cy + r * y:.1f}" rx="{r * math.sqrt(1 - y * y):.1f}" ry="{r * math.sqrt(1 - y * y) * .16:.1f}" fill="none"/>' for y in (-.62, -.3, 0, .3, .62))
        return (f'<g stroke="{col}" stroke-width="1" opacity="{op}"><circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke-width="1.4"/>{"".join(mer)}{lat}</g>')

    def terrain(self, x, y, w, h, col="#8fa2ff"):
        """Perspective wire floor that rolls towards you, with a data wave on the horizon."""
        cid = self.uid("tr")
        self.d(f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath>')
        hz, vpx = y + h * .34, x + w / 2
        rays = "".join(f'<line x1="{vpx + k * w * .028:.1f}" y1="{hz:.1f}" x2="{vpx + k * w * .17:.1f}" y2="{y + h}" />' for k in range(-6, 7))
        K, N = 14, 7
        rows = ""
        for j in range(N):
            ph = j / N
            ys = [hz + (y + h - hz) * (((ph + k / K) % 1) ** 2.2) for k in range(K + 1)]
            ops = [math.sin(math.pi * ((ph + k / K) % 1)) ** .6 for k in range(K + 1)]
            rows += (f'<rect x="{x}" width="{w}" height="1.2" fill="{col}"><animate attributeName="y" values="{";".join(f"{v:.1f}" for v in ys)}" dur="3.6s" repeatCount="indefinite"/>'
                     f'<animate attributeName="opacity" values="{";".join(f"{v:.2f}" for v in ops)}" dur="3.6s" repeatCount="indefinite"/></rect>')
        pts = lambda ph, amp: "M" + "L".join(f"{x + i * w / 40:.1f} {hz - 4 - amp * math.sin(i * .55 + ph) * (1 - abs(i - 20) / 24):.1f}" for i in range(41))
        wave = (f'<path d="{pts(0, 10)}" fill="none" stroke="{"#fff" if self.c["name"] == "dark" else "#2b2f78"}" stroke-width="1.6"><animate attributeName="d" values="{pts(0, 10)};{pts(2.1, 14)};{pts(4.2, 8)};{pts(6.28, 10)}" dur="5s" repeatCount="indefinite"/></path>')
        return f'<g clip-path="url(#{cid})"><g stroke="{col}" stroke-opacity=".5" stroke-width="1">{rays}</g>{rows}{wave}</g>'

    def eq(self, x, y, n, step, hmax, col="#fff", w=3):
        rnd = random.Random(n * 7)
        bars = "".join(f'<rect class="eq" x="{x + i * step:.1f}" y="{y - hmax / 2:.1f}" width="{w}" height="{hmax}" rx="{w / 2}" fill="{col}" '
                       f'style="animation-duration:{rnd.uniform(.5, 1.4):.2f}s;animation-delay:-{rnd.uniform(0, 1.4):.2f}s"/>' for i in range(n))
        return bars

    def glass(self, x, y, w, h, rx=16, tint=None, shade=True):
        c = self.c
        g = self.uid("gl")
        tint = tint or "#ffffff"
        self.d(f'<linearGradient id="{g}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{tint}" stop-opacity="{c["glass1"]}"/><stop offset="1" stop-color="{tint}" stop-opacity="{c["glass2"]}"/></linearGradient>')
        flt = ' filter="url(#sh)"' if (c["shadow"] and shade) else ""
        under = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{c["bg1"] if c["name"] == "dark" else "#ffffff"}" opacity="{.68 if c["name"] == "dark" else .45}"{flt}/>'
        return under + f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="url(#{g})" stroke="url(#edge)" stroke-width="1.3"/>'

    def window(self, x, y, w, h, title, rx=16, bar=32, ctrl=True, tint=None):
        c = self.c
        out = self.glass(x, y, w, h, rx, tint)
        tp = f"M{x} {y + bar}V{y + rx}a{rx} {rx} 0 0 1 {rx} {-rx}H{x + w - rx}a{rx} {rx} 0 0 1 {rx} {rx}V{y + bar}Z"
        out += f'<path d="{tp}" fill="{c["line"] if c["name"] == "dark" else "#ffffff"}" opacity="{c["bar_op"]}"/>'
        out += f'<line x1="{x + 1}" y1="{y + bar}" x2="{x + w - 1}" y2="{y + bar}" stroke="{c["line"]}" stroke-opacity="{c["line_op"] * .5:.2f}"/>'
        out += self.label(title, x + 16, y + bar / 2 + 4, 11, c["ink"], tracking=.8)
        if ctrl:
            for i, sym in enumerate(("-", "o", "x")):
                bx = x + w - 20 - (2 - i) * 22
                by = y + bar / 2
                out += f'<rect x="{bx - 8}" y="{by - 8}" width="16" height="16" rx="4" fill="none" stroke="{c["line"]}" stroke-opacity="{min(1, c["line_op"] + .1)}"/>'
                if sym == "-":
                    out += f'<line x1="{bx - 4}" y1="{by + 3}" x2="{bx + 4}" y2="{by + 3}" stroke="{c["ink"]}" stroke-width="1.4"/>'
                elif sym == "o":
                    out += f'<rect x="{bx - 4}" y="{by - 4}" width="8" height="8" fill="none" stroke="{c["ink"]}" stroke-width="1.3"/>'
                else:
                    out += f'<path d="M{bx - 4} {by - 4}L{bx + 4} {by + 4}M{bx + 4} {by - 4}L{bx - 4} {by + 4}" stroke="{c["ink"]}" stroke-width="1.4"/>'
        return out

    def button(self, x, y, w, h, label, size=13, pulse=True):
        c = self.c
        pid = self.uid("bt")
        self.d(f'<clipPath id="{pid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h / 2}"/></clipPath>')
        t = self.text(label, x + w / 2, y + h / 2 + size * .36, size, "#0a0b1f", font=BOLD, anchor="middle", tracking=.4)
        glow = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h / 2}" fill="url(#holo)" filter="url(#b8)" class="glow"/>' if pulse else ""
        return (glow + f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h / 2}" fill="url(#holo)" stroke="#fff" stroke-width="1.6"/>'
                f'<g clip-path="url(#{pid})"><rect x="{x}" y="{y}" width="{w}" height="{h * .5}" fill="#fff" opacity=".42"/>'
                f'<rect x="{x - 80}" y="{y - 4}" width="40" height="{h + 8}" fill="#fff" opacity=".55" transform="skewX(-20)" class="btnsheen"/></g>' + t["svg"])

    def barcode(self, x, y, w, h, seed=1, col=None):
        c = self.c
        col = col or c["ink"]
        rnd = random.Random(seed)
        out, cx = "", x
        while cx < x + w - 2:
            bw = rnd.choice([1, 1, 2, 3])
            out += f'<rect x="{cx}" y="{y}" width="{bw}" height="{h}" fill="{col}"/>'
            cx += bw + rnd.choice([1, 2, 2, 3])
        return (f'<g opacity=".9">{out}</g><rect x="{x}" y="{y - 2}" width="2" height="{h + 4}" fill="{c["accent"]}"><animate attributeName="x" values="{x};{x + w};{x}" dur="4.5s" repeatCount="indefinite"/></rect>')

    def ticker(self, x, y, w, text, size=11, dur=28, col=None, tracking=2.2):
        c = self.c
        col = col or c["mute"]
        item = text + "     ✦     "
        item = item.replace("✦", "+")
        tw = MONO.width(item, size, tracking)
        reps = int(w / tw) + 2
        mid = self.uid("tk")
        self.d(f'<linearGradient id="{mid}g" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".08" stop-color="#fff"/><stop offset=".92" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
               f'<mask id="{mid}"><rect x="{x}" y="{y - 20}" width="{w}" height="30" fill="url(#{mid}g)"/></mask>')
        self.k(f"@keyframes {mid}k{{to{{transform:translateX({-tw:.1f}px)}}}}.{mid}{{animation:{mid}k {dur}s linear infinite}}")
        run = "".join(self.text(item, x + i * tw, y, size, col, font=MONO, tracking=tracking)["svg"] for i in range(reps))
        return f'<g mask="url(#{mid})"><g class="{mid}">{run}</g></g>'

    def pixel(self, x, y, rows, pal, px=5, cls="", style=""):
        out = ""
        for j, row in enumerate(rows):
            for i, ch in enumerate(row):
                if ch in pal:
                    out += f'<rect x="{x + i * px}" y="{y + j * px}" width="{px}" height="{px}" fill="{pal[ch]}"/>'
        cl = f' class="{cls}"' if cls else ""
        st = f' style="{style}"' if style else ""
        return f"<g{cl}{st}>{out}</g>"

    def holo_orb(self, cx, cy, r, delay=0.0):
        gid = self.uid("or")
        self.d(f'<radialGradient id="{gid}" cx=".35" cy=".3" r=".8"><stop offset="0" stop-color="#fff"/><stop offset=".25" stop-color="#d9ccff"/><stop offset=".6" stop-color="#8fa2ff"/><stop offset="1" stop-color="#ff8fe0"/></radialGradient>')
        return (f'<g class="hue" style="animation-delay:-{delay}s"><circle cx="{cx}" cy="{cy}" r="{r}" fill="url(#{gid})" stroke="#fff" stroke-opacity=".8"/>'
                f'<ellipse cx="{cx - r * .3}" cy="{cy - r * .38}" rx="{r * .3}" ry="{r * .16}" fill="#fff" opacity=".85" transform="rotate(-30 {cx - r * .3} {cy - r * .38})"/></g>')


BASE_CSS = """
@media (prefers-reduced-motion: reduce){*{animation:none!important}}
@keyframes tw{0%,100%{transform:scale(.35) rotate(0);opacity:.25}50%{transform:scale(1) rotate(90deg);opacity:1}}
.tw{transform-box:fill-box;transform-origin:center;animation:tw 3.6s ease-in-out infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.spin{transform-box:fill-box;transform-origin:center;animation:spin 26s linear infinite}
@keyframes pulse{0%,100%{transform:scale(1)}50%{transform:scale(1.12)}}
.pulse{transform-box:fill-box;transform-origin:center;animation:pulse 4.5s ease-in-out infinite}
@keyframes flare{0%,100%{transform:scale(.7);opacity:.6}50%{transform:scale(1.15);opacity:1}}
.flare{animation:flare 4.4s ease-in-out infinite}
@keyframes d0{0%,100%{transform:translate(0,0)}50%{transform:translate(40px,-24px)}}
@keyframes d1{0%,100%{transform:translate(0,0)}50%{transform:translate(-34px,22px)}}
@keyframes d2{0%,100%{transform:translate(0,0)}50%{transform:translate(24px,30px)}}
.d0{animation:d0 17s ease-in-out infinite}.d1{animation:d1 21s ease-in-out infinite}.d2{animation:d2 19s ease-in-out infinite}
@keyframes eq{from{transform:scaleY(.12)}to{transform:scaleY(1)}}
.eq{transform-box:fill-box;transform-origin:center;animation:eq .8s ease-in-out infinite alternate}
@keyframes hue{0%{filter:hue-rotate(0)}100%{filter:hue-rotate(360deg)}}
.hue{animation:hue 9s linear infinite}
@keyframes glow{0%,100%{opacity:.35}50%{opacity:.95}}
.glow{animation:glow 2.8s ease-in-out infinite}
@keyframes btnsheen{0%,55%{transform:translateX(0)}100%{transform:translateX(420px)}}
.btnsheen{animation:btnsheen 3.4s ease-in-out infinite}
@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}
.blink{animation:blink 1s steps(1) infinite}
""".strip()
