# -*- coding: utf-8 -*-
"""HUD / terminal design system for the profile SVGs.

Near-black poster, phosphor periwinkle data, white line-work frames, one deep-blue accent. Type is converted to
vector outlines at build time (nothing loads from the network). Motion is plain SVG (CSS + SMIL), which GitHub
allows inside an <img>.
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
M = 36            # inner margin
HERE = os.path.dirname(os.path.abspath(__file__))

THEME = os.environ.get("HUD_THEME", "dark")
if THEME == "dark":
    BG, INK, PH, PHD, WHITE = "#04040a", "#e9e9ff", "#a9a3ff", "#5d58b8", "#f5f5fa"
    BLUE, BLUE_DK = "#2b57f0", "#0b1f6b"
    BASE_FILL, BASE_OP, VIG, GRAIN, GLOW = BLUE_DK, .55, .65, .16, True
else:  # light = the same poster printed on paper: black line-work, indigo data, same blue
    BG, INK, PH, PHD, WHITE = "#f1f1f6", "#0a0a16", "#1f2a9c", "#8087bd", "#0a0a16"
    BLUE, BLUE_DK = "#2b57f0", "#1a3fb4"
    BASE_FILL, BASE_OP, VIG, GRAIN, GLOW = BLUE, .10, .0, .10, False


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


_FD = os.path.join(HERE, "fonts")
BOLD = Font(os.path.join(_FD, "Poppins-Bold.ttf"), "b")
MONO = Font(os.path.join(_FD, "GeistMono-Regular.ttf"), "r")
MONOB = Font(os.path.join(_FD, "GeistMono-Bold.ttf"), "t")
PIX = Font(os.path.join(_FD, "Silkscreen-Regular.ttf"), "p")
JP = Font(os.path.join(_FD, "NotoSansJP-Bold-subset.otf"), "j")


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



# ═══════════════════════════════════ DOC ═══════════════════════════════════
class Doc:
    """One SVG panel: collects defs/css, hands out ids, owns every drawing helper."""

    def __init__(self, h, title):
        self.h, self.title = h, title
        self.glyphs, self.defs, self.css, self.n = {}, [], [], 0
        self._base()

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

    def text(self, t, x, y, size, fill=INK, font=MONO, anchor="start", tracking=0.0, xs=1.0, max_w=None, opacity=None, raw=False):
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
            return dict(uses=uses, width=w, x0=x0, size=size)
        op = f' opacity="{opacity}"' if opacity is not None else ""
        return dict(svg=f'<g fill="{fill}"{op}>{"".join(uses)}</g>', width=w, x0=x0, size=size)

    def mono(self, t, x, y, size=11, fill=PH, anchor="start", tracking=1.0, opacity=None, bold=False, max_w=None):
        return self.text(t, x, y, size, fill, MONOB if bold else MONO, anchor, tracking, max_w=max_w, opacity=opacity)["svg"]

    def pix(self, t, x, y, size=16, fill=PH, anchor="start", tracking=1.0, max_w=None, opacity=None):
        return self.text(t, x, y, size, fill, PIX, anchor, tracking, max_w=max_w, opacity=opacity)["svg"]

    def outline(self, t, x, y, size, xs=1.3, sw=1.8, col=WHITE, anchor="middle", max_w=None, tracking=0.0):
        """Hollow extended lettering, line-art style."""
        r = self.text(t, x, y, size, font=BOLD, anchor=anchor, tracking=tracking, xs=xs, max_w=max_w, raw=True)
        k = BOLD.upm / r["size"]
        return f'<g fill="none" stroke="{col}" stroke-width="{sw * k:.0f}" stroke-linejoin="miter">{"".join(r["uses"])}</g>', r

    def solid(self, t, x, y, size, xs=1.3, col=WHITE, anchor="middle", max_w=None, tracking=0.0):
        r = self.text(t, x, y, size, col, BOLD, anchor, tracking, xs, max_w)
        return r["svg"], r

    # ── scene ──
    def _base(self):
        GR, GB = (.75, 1) if THEME == 'dark' else (.1, .3)
        self.d('<filter id="glow" x="-10%" y="-40%" width="120%" height="180%"><feGaussianBlur in="SourceGraphic" stdDeviation="1.6" result="a"/>'
               '<feGaussianBlur in="SourceGraphic" stdDeviation="5" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="a"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
        self.d('<filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="6"/></filter>')
        self.d(f'<filter id="grain" x="0" y="0" width="100%" height="100%"><feTurbulence type="fractalNoise" baseFrequency=".9" numOctaves="2" seed="4"/>'
               '<feColorMatrix type="matrix" values="0 0 0 0 {GR}  0 0 0 0 {GR}  0 0 0 0 {GB}  0 0 0 1.1 -.5"/></filter>')
        self.d(f'<pattern id="scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1.4" fill="{PH}" opacity=".06"/></pattern>')
        self.d(f'<clipPath id="cc"><rect x="0" y="6" width="{W}" height="{self.h - 12}" rx="10"/></clipPath>')
        self.d(f'<radialGradient id="vig" cx=".5" cy=".5" r=".75"><stop offset=".55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="{VIG}"/></radialGradient>')
        self.d(f'<linearGradient id="band" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{PH}" stop-opacity="0"/><stop offset=".5" stop-color="{PH}" stop-opacity=".07"/><stop offset="1" stop-color="{PH}" stop-opacity="0"/></linearGradient>')

    def backdrop(self):
        return f'<rect x=".5" y="6.5" width="{W - 1}" height="{self.h - 13}" rx="10" fill="{BG}"/>'

    def crt(self):
        """Drawn last: scanlines, a slow scan band, grain, vignette and the card edge."""
        h = self.h
        return (f'<g clip-path="url(#cc)" style="pointer-events:none"><rect y="6" width="{W}" height="{h - 12}" fill="url(#scan)"/>'
                f'<rect x="0" y="-80" width="{W}" height="80" fill="url(#band)"><animate attributeName="y" values="-80;{h};{h}" keyTimes="0;.7;1" dur="9s" repeatCount="indefinite"/></rect>'
                f'<rect y="6" width="{W}" height="{h - 12}" filter="url(#grain)" opacity="{GRAIN}"/>'
                f'<rect y="6" width="{W}" height="{h - 12}" fill="url(#vig)"/></g>'
                f'<rect x=".5" y="6.5" width="{W - 1}" height="{h - 13}" rx="10" fill="none" stroke="{PH}" stroke-opacity=".28"/>')

    def glowg(self, inner):
        return f'<g filter="url(#glow)">{inner}</g>' if GLOW else f'<g>{inner}</g>'

    def hud(self, x, y, w, h, cut=24, col=WHITE, sw=1.4, cuts="tl,br", nodes=True):
        pts = [(x, y), (x + w, y), (x + w, y + h), (x, y + h)]
        c = set(cuts.split(","))
        p = []
        if "tl" in c:
            p += [(x, y + cut), (x + cut, y)]
        else:
            p += [(x, y)]
        if "tr" in c:
            p += [(x + w - cut, y), (x + w, y + cut)]
        else:
            p += [(x + w, y)]
        if "br" in c:
            p += [(x + w, y + h - cut), (x + w - cut, y + h)]
        else:
            p += [(x + w, y + h)]
        if "bl" in c:
            p += [(x + cut, y + h), (x, y + h - cut)]
        else:
            p += [(x, y + h)]
        d = "M" + "L".join(f"{a:.1f} {b:.1f}" for a, b in p) + "Z"
        o = f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{sw}" stroke-linejoin="miter"/>'
        if nodes:
            o += "".join(f'<circle cx="{a:.1f}" cy="{b:.1f}" r="3.4" fill="{BG}" stroke="{col}" stroke-width="1.3"/>' for a, b in p[::2])
        return o

    def hatch(self, x, y, n=4, h=9, step=9, col=WHITE):
        return "".join(f'<path d="M{x + i * step} {y + h}l5 {-h}h3l-5 {h}z" fill="{col}"/>' for i in range(n))

    def corners(self, x, y, w, h, ln=16, col=PH, sw=1.6):
        return (f'<path d="M{x} {y + ln}V{y}H{x + ln}M{x + w - ln} {y}H{x + w}V{y + ln}M{x + w} {y + h - ln}V{y + h}H{x + w - ln}M{x + ln} {y + h}H{x}V{y + h - ln}" '
                f'fill="none" stroke="{col}" stroke-width="{sw}"/>')

    def tab(self, x, y, w, text, h=22, size=10, fill=BLUE, ink="#ffffff"):
        return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}"/>' + self.mono(text, x + 10, y + h / 2 + size * .36, size, ink, tracking=1.4, bold=True)

    def box(self, x, y, w, h, col=PH, op=.7, sw=1.2, fill=None):
        f = f'fill="{fill}"' if fill else 'fill="none"'
        return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" {f} stroke="{col}" stroke-opacity="{op}" stroke-width="{sw}"/>'

    def button(self, x, y, w, h, label, size=13):
        t = self.text(label, x + w / 2, y + h / 2 + size * .36, size, "#fff", PIX, "middle", 1.4)["svg"]
        return (f'<rect class="glow2" x="{x}" y="{y}" width="{w}" height="{h}" fill="{BLUE}" filter="url(#soft)"/>'
                f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{BLUE}" stroke="#9db4ff" stroke-width="1.2"/>' + t)

    def cursor(self, x, y, h=18, w=10, col=PH):
        return f'<rect class="blink" x="{x:.1f}" y="{y}" width="{w}" height="{h}" fill="{col}"/>'

    def counter(self, x, y, size, fill, dur=12, n=26, anchor="start"):
        out = ""
        for i in range(n):
            v = round(i * 100 / (n - 1))
            kt = [0, i / n, (i + 1) / n]
            if i == 0:
                vals, kts = "visible;hidden", f"0;{1 / n:.4f}"
            elif i == n - 1:
                vals, kts = "hidden;visible", f"0;{i / n:.4f}"
            else:
                vals, kts = "hidden;visible;hidden", f"0;{i / n:.4f};{(i + 1) / n:.4f}"
            g = self.text(f"{v}%", x, y, size, fill, PIX, anchor, 1)["svg"]
            out += f'<g visibility="hidden">{g}<animate attributeName="visibility" values="{vals}" keyTimes="{kts}" calcMode="discrete" dur="{dur}s" repeatCount="indefinite"/></g>'
        return out

    def halftone(self, x, y, w, h, col=BLUE, step=8, r=2.1):
        """Dot-matrix field whose bands of dots drift across, standing in for the posters' blue 'image'."""
        pid, mid_, gid, cid = self.uid("pt"), self.uid("mk"), self.uid("mg"), self.uid("hc")
        self.d(f'<pattern id="{pid}" width="{step}" height="{step}" patternUnits="userSpaceOnUse"><circle cx="{step / 2}" cy="{step / 2}" r="{r}" fill="{col}"/></pattern>')
        stops = "".join(f'<stop offset="{i / 8:.3f}" stop-color="#fff" stop-opacity="{.15 + .85 * (.5 + .5 * math.sin(i / 8 * 2 * math.pi * 1.0 + 1)) ** 1.6:.2f}"/>' for i in range(9))
        self.d(f'<linearGradient id="{gid}" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="320" y2="120" spreadMethod="repeat">{stops}'
               f'<animateTransform attributeName="gradientTransform" type="translate" from="0 0" to="320 0" dur="9s" repeatCount="indefinite"/></linearGradient>')
        self.d(f'<mask id="{mid_}"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#{gid})"/></mask>')
        self.d(f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath>')
        return (f'<g clip-path="url(#{cid})"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{BASE_FILL}" opacity="{BASE_OP}"/>'
                f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#{pid})" mask="url(#{mid_})"/></g>')

    def eq(self, x, y, n, step, hmax, col=PH, w=3, seed=1):
        rnd = random.Random(seed + n)
        return "".join(f'<rect class="eq" x="{x + i * step:.1f}" y="{y - hmax / 2:.1f}" width="{w}" height="{hmax}" fill="{col}" '
                       f'style="animation-duration:{rnd.uniform(.5, 1.3):.2f}s;animation-delay:-{rnd.uniform(0, 1.3):.2f}s"/>' for i in range(n))

    def barcode(self, x, y, w, h, seed=1, col=PH):
        rnd = random.Random(seed)
        out, cx = "", x
        while cx < x + w - 2:
            bw = rnd.choice([1, 1, 2, 3])
            out += f'<rect x="{cx}" y="{y}" width="{bw}" height="{h}" fill="{col}"/>'
            cx += bw + rnd.choice([1, 2, 2, 3])
        return f'<g opacity=".85">{out}</g>'

    def ticker(self, x, y, w, text, size=10, dur=34, col=PHD, tracking=2.0):
        item = text + "     //     "
        tw = MONO.width(item, size, tracking)
        reps = int(w / tw) + 2
        mid_ = self.uid("tk")
        self.d(f'<linearGradient id="{mid_}g" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".08" stop-color="#fff"/><stop offset=".92" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
               f'<mask id="{mid_}"><rect x="{x}" y="{y - 20}" width="{w}" height="30" fill="url(#{mid_}g)"/></mask>')
        self.k(f"@keyframes {mid_}k{{to{{transform:translateX({-tw:.1f}px)}}}}.{mid_}{{animation:{mid_}k {dur}s linear infinite}}")
        run = "".join(self.text(item, x + i * tw, y, size, col, MONO, tracking=tracking)["svg"] for i in range(reps))
        return f'<g mask="url(#{mid_})"><g class="{mid_}">{run}</g></g>'

    def packet(self, pid, path, dur, delay=0.0, col=WHITE):
        return (f'<g><rect x="-3.5" y="-3.5" width="7" height="7" fill="{col}"/><rect x="-9" y="-9" width="18" height="18" fill="{BLUE}" opacity=".45" filter="url(#soft)"/>'
                f'<animateMotion dur="{dur}s" begin="{delay}s" repeatCount="indefinite"><mpath xlink:href="#{pid}"/></animateMotion></g>')

    def wave(self, x, y, w, h, grid=20):
        """Oscilloscope panel: static grid, three drifting sine traces."""
        g = "".join(f'<path d="M{x + i * grid} {y}V{y + h}" stroke="{PH}" stroke-opacity=".2"/>' for i in range(1, int(w / grid)))
        g += "".join(f'<path d="M{x} {y + j * grid}H{x + w}" stroke="{PH}" stroke-opacity=".2"/>' for j in range(1, int(h / grid)))
        cy = y + h / 2
        N = 60

        def d_(ph, amp, f):
            return "M" + "L".join(f"{x + i * w / N:.1f} {cy - amp * math.sin(i / N * f * 2 * math.pi + ph):.1f}" for i in range(N + 1))
        tr = ""
        for amp, f, op, dur in ((h * .32, 3, 1, 7), (h * .2, 5, .6, 9), (h * .14, 2, .4, 11)):
            vals = ";".join(d_(ph, amp, f) for ph in (0, math.pi / 2, math.pi, 3 * math.pi / 2, 2 * math.pi))
            tr += f'<path d="{d_(0, amp, f)}" fill="none" stroke="{PH}" stroke-opacity="{op}" stroke-width="1.6"><animate attributeName="d" values="{vals}" dur="{dur}s" repeatCount="indefinite"/></path>'
        return f'<g fill="none" stroke-width="1">{g}</g>{self.box(x, y, w, h, PH, .7)}{tr}'

    # ── poster parts (Japanese labels, vertical text, code box, arrow) ──
    def jp(self, t, x, y, size=12, fill=None, anchor="start", tracking=0.5, max_w=None):
        return self.text(t, x, y, size, fill or INK, JP, anchor, tracking, max_w=max_w)["svg"]

    def vjp(self, chars, x, cy, size=15, fill=None, step=None):
        """Vertical Japanese text, one character per cell, centred on cy."""
        step = step or size * 1.28
        y0 = cy - (len(chars) - 1) * step / 2
        out = ""
        for i, c in enumerate(chars):
            g = self.text(c, x, y0 + i * step + size * .36, size, fill or INK, JP, "middle")["svg"]
            out += f'<g transform="rotate(90 {x} {y0 + i * step:.1f})">{g}</g>' if c == "ー" else g   # long-vowel mark runs vertically
        return out

    def label_bar(self, x, y, w, jp, en=None, h=24):
        """The blue bar with a katakana label that heads each column in the poster."""
        o = f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{BLUE}"/>' + self.text(jp, x + 12, y + h / 2 + 4.6, 12.5, "#ffffff", JP, tracking=.6)["svg"]
        if en:
            o += self.mono(en, x + w - 10, y + h / 2 + 3.4, 8.5, "#cfd9ff", anchor="end", tracking=1.4)
        return o

    def bullets(self, x, y):
        return f'<rect x="{x}" y="{y}" width="9" height="9" fill="{WHITE}"/><rect x="{x + 16}" y="{y}" width="9" height="9" fill="none" stroke="{WHITE}" stroke-width="1.3"/>'

    def code_box(self, x, y, num, lines):
        o = self.box(x, y, 64, 30, WHITE, .95, 1.4, fill=BG) + self.pix(num, x + 32, y + 21, 16, WHITE, anchor="middle")
        for i, ln in enumerate(lines):
            o += self.mono(ln, x + 76, y + 9 + i * 10.5, 7.5, PH, tracking=1.2)
        return o

    def arrow_nw(self, x, y, s=22, col=None):
        col = col or WHITE
        return f'<path d="M{x + s} {y + s}L{x} {y}M{x} {y + s * .6}V{y}H{x + s * .6}" fill="none" stroke="{col}" stroke-width="3"/>'

    def pill(self, x, y, w, h, text, size=13):
        return (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{h / 2}" fill="none" stroke="{WHITE}" stroke-opacity=".9" stroke-width="1.4"/>'
                + self.pix(text, x + w / 2, y + h / 2 + size * .36, size, WHITE, anchor="middle"))

    def para(self, text, x, y, w, size=9, lead=14, fill=None, tracking=.7):
        return "".join(self.mono(ln, x, y + i * lead, size, fill or INK, tracking=tracking) for i, ln in enumerate(wrap(text.upper(), MONO, size, w, tracking)))


BASE_CSS = """
@media (prefers-reduced-motion: reduce){*{animation:none!important}}
@keyframes blink{0%,49%{opacity:1}50%,100%{opacity:0}}
.blink{animation:blink 1.1s steps(1) infinite}
@keyframes eq{from{transform:scaleY(.1)}to{transform:scaleY(1)}}
.eq{transform-box:fill-box;transform-origin:center;animation:eq .8s steps(6) infinite alternate}
@keyframes glow2{0%,100%{opacity:.25}50%{opacity:.8}}
.glow2{animation:glow2 2.6s ease-in-out infinite}
@keyframes spin{to{transform:rotate(360deg)}}
.spin{transform-box:fill-box;transform-origin:center;animation:spin 24s linear infinite}
""".strip()
