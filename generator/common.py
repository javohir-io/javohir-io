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
# Obsidian + platinum with an emerald accent. `alt` is the cool second colour used
# only for the chromatic-split in the glitch effect.
DARK = dict(
    name="dark",
    bg="#06080a", bg2="#0c1215", node="#080b0d",
    ink="#edf2f0", text2="#a2adab", text3="#7b8785",
    accent="#34d399", accent_hi="#a7f3d0", accent_lo="#047857", alt="#38bdf8",
    line="#1a2428", dot="#2a373c", glow_op=0.14, scan_op=0.07, vinyl="#040506",
)
LIGHT = dict(
    name="light",
    bg="#f7f8f6", bg2="#e8ece9", node="#ffffff",
    ink="#0a100e", text2="#44514d", text3="#5c6a66",
    accent="#047857", accent_hi="#10b981", accent_lo="#065f46", alt="#0369a1",
    line="#d0d9d4", dot="#bcc8c3", glow_op=0.13, scan_op=0.09, vinyl="#0a100e",
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
        return "\n".join(f'<path id="{gid}" pathLength="100" d="{FONT.path(g)}"/>' for gid, g in sorted(self.used.items()))


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
@keyframes rise{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:translateY(0)}}
@keyframes fade{from{opacity:0}to{opacity:1}}
@keyframes comet{from{stroke-dashoffset:0}to{stroke-dashoffset:-100}}
@keyframes blink{0%,48%{opacity:1}52%,100%{opacity:0}}
@keyframes ping{0%{transform:scale(1);opacity:.7}100%{transform:scale(4.2);opacity:0}}
.cm{stroke-dasharray:11 89;animation:comet 6s linear infinite}
.blink{animation:blink 1.1s steps(1) infinite}
.ping{transform-box:fill-box;transform-origin:center;animation:ping 2.8s ease-out infinite}
""".strip()


def svg_open(h, title, w=W):
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" '
            f'xmlns:xlink="http://www.w3.org/1999/xlink" role="img" aria-label="{esc(title)}">'
            f'<title>{esc(title)}</title>')


def accent_gradient(c, gid="ag"):
    return (f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0">'
            f'<stop offset="0" stop-color="{c["accent_hi"]}"/><stop offset="1" stop-color="{c["accent"]}"/></linearGradient>')


def ghost(reg, text, x, y, size, c, anchor="start", tracking=0.0, sw=1.1, op=0.5,
          dur=7.0, stagger=0.35, comet=True):
    """Outline-only lettering with a light that runs around each glyph's contour."""
    glyphs, w = FONT.layout(text, size, tracking)
    x0 = x - (w / 2 if anchor == "middle" else w if anchor == "end" else 0)
    s = size / FONT.upm
    base, run = [], []
    for i, (g, gx, ch) in enumerate(glyphs):
        if not FONT.path(g):
            continue
        gid = reg.ref(g)
        tf = f"translate({x0 + gx:.2f} {y:.2f}) scale({s:.5f} {-s:.5f})"
        base.append(f'<use xlink:href="#{gid}" transform="{tf}"/>')
        run.append(f'<use xlink:href="#{gid}" transform="{tf}" style="animation-duration:{dur}s;animation-delay:{-i * stagger:.2f}s"/>')
    swu = sw / s
    out = (f'<g fill="none" stroke="{c["accent"]}" stroke-width="{swu:.1f}" stroke-opacity="{op}" stroke-linejoin="round">{"".join(base)}</g>')
    if comet:
        out += (f'<g class="cm-g" fill="none" stroke="{c["accent_hi"]}" stroke-width="{swu * 1.5:.1f}" stroke-linecap="round" '
                f'stroke-linejoin="round">{"".join(u.replace("<use ", "<use class=\"cm\" ") for u in run)}</g>')
    return dict(svg=out, width=w, x0=x0)


def diamond(cx, cy, r, stroke, bg=None, fill=None, sw=1):
    pts = f"{cx},{cy-r} {cx+r},{cy} {cx},{cy+r} {cx-r},{cy}"
    return f'<polygon points="{pts}" fill="{fill or bg or "none"}" stroke="{stroke}" stroke-width="{sw}"/>'


def glint(c, gid, x1, x2, y, dur=6.0, delay=0.0, length=150, op=1.0, base=None):
    """Hairline with a bright highlight that travels along it."""
    base = base or c["line"]
    return f"""<clipPath id="{gid}c"><rect x="{x1}" y="{y-3}" width="{x2-x1}" height="6"/></clipPath>
<linearGradient id="{gid}g" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{c['accent_hi']}" stop-opacity="0"/><stop offset=".5" stop-color="{c['accent_hi']}" stop-opacity="{op}"/><stop offset="1" stop-color="{c['accent_hi']}" stop-opacity="0"/></linearGradient>
<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{base}"/>
<g clip-path="url(#{gid}c)"><rect x="{x1-length}" y="{y-.75}" width="{length}" height="1.5" fill="url(#{gid}g)">
<animate attributeName="x" values="{x1-length};{x2};{x2}" keyTimes="0;.55;1" dur="{dur}s" begin="{-delay}s" repeatCount="indefinite"/></rect></g>"""


def panel(c, w, h, idx=None, label=None, glow=(0.85, 0.0), glow_r=0.8, scan_dur=11.0):
    """Shared slab: dot-grid, soft glow, travelling scan band, hairline border, two corner ticks.
    Returns (defs, back, front, css). `front` carries the label row when idx/label are given."""
    defs = f"""<linearGradient id="bgv" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c['bg2']}"/><stop offset="1" stop-color="{c['bg']}"/></linearGradient>
<radialGradient id="glow" cx="{glow[0]}" cy="{glow[1]}" r="{glow_r}"><stop offset="0" stop-color="{c['accent']}" stop-opacity="{c['glow_op']}"/><stop offset="1" stop-color="{c['accent']}" stop-opacity="0"/></radialGradient>
<pattern id="dots" width="22" height="22" patternUnits="userSpaceOnUse"><circle cx="1" cy="1" r=".85" fill="{c['dot']}"/></pattern>
<radialGradient id="dotfade" cx=".5" cy=".55" r=".72"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></radialGradient>
<mask id="dotmask"><rect width="{w}" height="{h}" fill="url(#dotfade)"/></mask>
<linearGradient id="scang" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c['accent']}" stop-opacity="0"/><stop offset=".5" stop-color="{c['accent']}" stop-opacity="{c['scan_op']}"/><stop offset="1" stop-color="{c['accent']}" stop-opacity="0"/></linearGradient>
<clipPath id="pclip"><rect width="{w}" height="{h}"/></clipPath>
{accent_gradient(c)}"""
    back = f"""<rect width="{w}" height="{h}" fill="url(#bgv)"/>
<rect width="{w}" height="{h}" fill="url(#glow)"/>
<rect width="{w}" height="{h}" fill="url(#dots)" mask="url(#dotmask)"/>
<g clip-path="url(#pclip)"><rect class="scan" x="0" y="-150" width="{w}" height="150" fill="url(#scang)"/></g>
<rect x=".5" y=".5" width="{w-1}" height="{h-1}" fill="none" stroke="{c['line']}"/>
<path d="M0 22V0H22" fill="none" stroke="{c['accent']}" stroke-width="2"/>
<path d="M{w} {h-22}V{h}H{w-22}" fill="none" stroke="{c['accent']}" stroke-width="2"/>"""
    front = ""
    if label:
        front = (f'<rect x="{MX}" y="40" width="7" height="7" fill="{c["accent"]}"/>'
                 f'<rect class="ping" x="{MX}" y="40" width="7" height="7" fill="none" stroke="{c["accent"]}"/>'
                 + stext(idx, MX + 20, 48, 12, c["accent"], weight=700, tracking=2.5)
                 + stext("/", MX + 46, 48, 12, c["text3"], weight=400)
                 + stext(label, MX + 62, 48, 12, c["ink"], weight=600, tracking=4.2)
                 + stext("JAVOHIR ABDUVAHHOBOV", w - MX, 48, 11, c["text3"], anchor="end", weight=500, tracking=3.6)
                 + glint(c, "hd", MX, w - MX, 64, dur=8.5, delay=2.0))
    css = f"@keyframes scan{{from{{transform:translateY(0)}}to{{transform:translateY({h + 150}px)}}}}.scan{{animation:scan {scan_dur}s linear infinite}}"
    return defs, back, front, css


def burst_kf(name, bursts, op=0.95):
    """Stepped keyframes for glitch bursts. bursts = [(start_pct, [dx, dx, ...]), ...] — each dx lasts 1% of the cycle."""
    fr = ["0%{opacity:0;transform:translate(0,0)}"]
    for start, dxs in bursts:
        for k, dx in enumerate(dxs):
            fr.append(f"{start + k:.1f}%{{opacity:{op};transform:translate({dx}px,0)}}")
        fr.append(f"{start + len(dxs):.1f}%{{opacity:0;transform:translate(0,0)}}")
    fr.append("100%{opacity:0}")
    return f"@keyframes {name}{{{''.join(fr)}}}"
