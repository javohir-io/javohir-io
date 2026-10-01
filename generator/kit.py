# -*- coding: utf-8 -*-
"""Shared building blocks: drawing context, frame, embers, ribbons, labels, waveform, embedded statue images."""
import base64, math, os, random
from functools import lru_cache
from xml.sax.saxutils import escape as _esc

import typo

W = 1000
HERE = os.path.dirname(os.path.abspath(__file__))


def esc(s):
    return _esc(str(s))


class Ctx:
    def __init__(self, c, uid, h, w=W, title="section", desc=""):
        self.c, self.uid, self.w, self.h = c, uid, w, h
        self.title, self.desc = title, desc
        self._css, self._defs = [], []
        self.used = {k: set() for k in typo.FONTS}
        self.reduced = []

    def id(self, name):
        return f"{name}{self.uid}"

    def css(self, rule):
        self._css.append(rule)

    def defs(self, s):
        self._defs.append(s)

    def t(self, s, x, y, size, fill=None, font="sans", anchor="start", ls=0, opacity=None, cls=None, style=None, extra=""):
        fill = fill or self.c["text"]
        spec = typo.FONTS[font]
        self.used[font] |= set(str(s))
        miss = typo.missing_glyphs(str(s), font)
        if miss:
            print(f"   ! [{self.uid}] glyphs missing in {font}: {miss}")
        a = f'x="{x}" y="{y}" font-family="{spec["stack"]}" font-weight="{spec["weight"]}" font-size="{size}" fill="{fill}"'
        if spec.get("style") == "italic":
            a += ' font-style="italic"'
        if anchor != "start":
            a += f' text-anchor="{anchor}"'
        if ls:
            a += f' letter-spacing="{ls}"'
        if opacity is not None:
            a += f' opacity="{opacity}"'
        if cls:
            a += f' class="{cls}"'
        if style:
            a += f' style="{style}"'
        return f'<text {a} {extra}>{esc(s)}</text>'

    def w_(self, s, font, size, ls=0):
        return typo.width(s, font, size, ls)

    def render(self, body):
        font_css = typo.font_face_css(self.used)
        return (
            f'<svg width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" xmlns="http://www.w3.org/2000/svg" '
            f'xmlns:xlink="http://www.w3.org/1999/xlink" role="img" aria-label="{esc(self.title)}">\n<title>{esc(self.title)}</title>\n'
            + (f'<desc>{esc(self.desc)}</desc>\n' if self.desc else "")
            + f'<style>\n{font_css}\n{chr(10).join(self._css)}\n'
            f'@media (prefers-reduced-motion: reduce){{*{{animation:none!important}}{"".join(self.reduced)}}}\n</style>\n'
            f'<defs>\n{chr(10).join(self._defs)}\n</defs>\n{body}\n</svg>\n')


@lru_cache(maxsize=None)
def _b64(name):
    with open(os.path.join(HERE, "img", name), "rb") as f:
        return base64.b64encode(f.read()).decode()


def image(name, x, y, w, h, op=1, extra=""):
    return (f'<image x="{x}" y="{y}" width="{w}" height="{h}" opacity="{op}" preserveAspectRatio="xMidYMid meet" {extra} '
            f'href="data:image/webp;base64,{_b64(name)}"/>')


def hair(x1, x2, y, color, op=0.3, sw=1):
    return f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{color}" stroke-opacity="{op}" stroke-width="{sw}"/>'


def fade_line(ctx, x1, x2, y, key, op=0.9, sw=1, both=True, color=None):
    color = color or ctx.c["red"]
    gid = ctx.id("fl" + key)
    if both:
        stops = (f'<stop offset="0" stop-color="{color}" stop-opacity="0"/><stop offset="0.5" stop-color="{color}" stop-opacity="{op}"/>'
                 f'<stop offset="1" stop-color="{color}" stop-opacity="0"/>')
    else:
        stops = f'<stop offset="0" stop-color="{color}" stop-opacity="{op}"/><stop offset="1" stop-color="{color}" stop-opacity="0"/>'
    ctx.defs(f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0">{stops}</linearGradient>')
    return f'<rect x="{x1}" y="{y - sw/2}" width="{x2-x1}" height="{sw}" fill="url(#{gid})"/>'


def cross(x, y, s, color, op=0.6):
    return f'<path d="M{x-s} {y}H{x+s}M{x} {y-s}V{y+s}" stroke="{color}" stroke-opacity="{op}" fill="none"/>'


def label(ctx, x, y, text, size=11, ls=5.5, line=34, color=None):
    """Reference-style section label: a short red rule and tracked caps."""
    c = ctx.c
    return (f'<rect x="{x}" y="{y-4}" width="{line}" height="1.4" fill="{c["red"]}"/>'
            + ctx.t(text.upper(), x + line + 14, y, size, color or c["silver"], "sansm", ls=ls))


def ticks_h(x, y, w, n, major, color, op=0.5, ln=5, lm=10):
    d = ""
    for i in range(n + 1):
        px = x + w * i / n
        d += f"M{px:.1f} {y}v{lm if i % major == 0 else ln}"
    return f'<path d="{d}" stroke="{color}" stroke-opacity="{op}" fill="none"/>'


def ticks_v(x, y, h, n, major, color, op=0.5, ln=5, lm=10, left=False):
    d = ""
    for i in range(n + 1):
        py = y + h * i / n
        L = lm if i % major == 0 else ln
        d += f"M{x} {py:.1f}h{-L if left else L}"
    return f'<path d="{d}" stroke="{color}" stroke-opacity="{op}" fill="none"/>'


def rosette(ctx, cx, cy, r, n=28, spin=160, color=None, op=0.12):
    color = color or ctx.c["red"]
    u = ctx.uid
    ctx.css(f"@keyframes ro{u}{{to{{transform:rotate(360deg)}}}}.ro{u}{{transform-origin:{cx}px {cy}px;animation:ro{u} {spin}s linear infinite}}")
    els = "".join(f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{r*0.42:.1f}" transform="rotate({i*180/n:.2f} {cx} {cy})"/>' for i in range(n))
    rings = "".join(f'<circle cx="{cx}" cy="{cy}" r="{r*k:.1f}"/>' for k in (0.3, 0.55, 1.0))
    return f'<g fill="none" stroke="{color}" stroke-opacity="{op}" stroke-width="0.8"><g class="ro{u}">{els}</g>{rings}</g>'


# ---------------------------------------------------------------------------
def frame(ctx, glow=True, bottom_glow=True):
    """Black stage with a faint crimson bloom. Returns the background group; call border() last."""
    c, w, h, u = ctx.c, ctx.w, ctx.h, ctx.uid
    ctx.defs(f'''<clipPath id="clip{u}"><rect width="{w}" height="{h}"/></clipPath>
<linearGradient id="bg{u}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c['bg2']}"/><stop offset="0.5" stop-color="{c['bg']}"/><stop offset="1" stop-color="{c['bg2']}"/></linearGradient>
<radialGradient id="gR{u}"><stop offset="0" stop-color="{c['red']}" stop-opacity="0.30"/><stop offset="1" stop-color="{c['red']}" stop-opacity="0"/></radialGradient>
<linearGradient id="fl{u}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c['red']}" stop-opacity="0"/><stop offset="1" stop-color="{c['red']}" stop-opacity="0.24"/></linearGradient>''')
    layers = [f'<rect width="{w}" height="{h}" fill="url(#bg{u})"/>']
    if glow:
        for i, (fx, fy, rad, dur, dx, dy) in enumerate([(0.06, 0.12, 300, 24, 50, 30), (0.96, 0.92, 340, 28, -50, -30)]):
            ctx.css(f"@keyframes au{u}{i}{{from{{transform:translate(0,0)}}to{{transform:translate({dx}px,{dy}px)}}}}.au{u}{i}{{animation:au{u}{i} {dur}s ease-in-out infinite alternate}}")
            layers.append(f'<circle class="au{u}{i}" cx="{w*fx:.0f}" cy="{h*fy:.0f}" r="{rad}" fill="url(#gR{u})" opacity="0.5"/>')
    if bottom_glow:
        layers.append(f'<rect x="0" y="{h-110}" width="{w}" height="110" fill="url(#fl{u})"/>')
    return f'<g clip-path="url(#clip{u})">' + "".join(layers) + "</g>"


def border(ctx, brackets=True):
    c, w, h = ctx.c, ctx.w, ctx.h
    s = [f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" fill="none" stroke="{c["red3"]}" stroke-opacity="0.55"/>']
    if brackets:
        b = 28
        s.append(f'<path d="M0.5 {b}V0.5H{b}M{w-b} 0.5H{w-0.5}V{b}M{w-0.5} {h-b}V{h-0.5}H{w-b}M{b} {h-0.5}H0.5V{h-b}" fill="none" stroke="{c["red"]}" stroke-width="1.6"/>')
    return "\n".join(s)


def embers(ctx, n=24, seed=1, x0=0, x1=None, y0=0, y1=None, rise=110, sizes=(0.6, 1.8)):
    x1 = x1 or ctx.w
    y1 = y1 or ctx.h
    u = ctx.uid
    rnd = random.Random(seed)
    ctx.css(f"@keyframes em{u}{{0%{{transform:translateY(0);opacity:0}}15%{{opacity:1}}85%{{opacity:.7}}100%{{transform:translateY(-{rise}px);opacity:0}}}}")
    out = []
    for _ in range(n):
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0 + 40, y1)
        col = ctx.c["red2"] if rnd.random() < 0.6 else ctx.c["silver"]
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{rnd.uniform(*sizes):.2f}" fill="{col}" opacity="0" style="animation:em{u} {rnd.uniform(8,18):.1f}s linear -{rnd.uniform(0,18):.1f}s infinite"/>')
    return "\n".join(out)


def ribbon(ctx, d, key, delay=0.0, width=1.2):
    """A thin crimson ribbon with a light that travels along it."""
    c, u = ctx.c, ctx.uid
    gid = ctx.id("rb" + key)
    ctx.defs(f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c["red"]}" stop-opacity="0"/><stop offset="0.5" stop-color="{c["red"]}" stop-opacity="0.95"/><stop offset="1" stop-color="{c["red"]}" stop-opacity="0"/></linearGradient>')
    ctx.css(f"@keyframes rd{u}{key}{{from{{stroke-dashoffset:0}}to{{stroke-dashoffset:-1000}}}}.rd{u}{key}{{animation:rd{u}{key} 8s linear {delay}s infinite}}")
    return (f'<path d="{d}" fill="none" stroke="url(#{gid})" stroke-width="{width}"/>'
            f'<path d="{d}" fill="none" stroke="url(#{gid})" stroke-width="{width*5}" opacity="0.10"/>'
            f'<path class="rd{u}{key}" d="{d}" pathLength="1000" fill="none" stroke="{c["red2"]}" stroke-width="{width*1.6}" stroke-dasharray="46 954" stroke-linecap="round"/>')


def wave(ctx, x, y, n=36, w=104, hmax=22, key="w"):
    """Animated equaliser bars (the 'sound' cue in the reference header)."""
    c, u = ctx.c, ctx.uid
    rnd = random.Random(5)
    ctx.css(f"@keyframes wv{u}{key}{{from{{transform:scaleY(.18)}}to{{transform:scaleY(1)}}}}.wv{u}{key}{{transform-box:fill-box;transform-origin:center;animation:wv{u}{key} 1s ease-in-out infinite alternate}}")
    step = w / n
    out = []
    for i in range(n):
        env = 0.35 + 0.65 * math.sin(math.pi * i / n) ** 0.7
        hh = max(3, hmax * env * (0.4 + 0.6 * rnd.random()))
        out.append(f'<rect class="wv{u}{key}" x="{x+i*step:.1f}" y="{y-hh/2:.1f}" width="1.3" height="{hh:.1f}" fill="{c["silver"]}" fill-opacity="0.85" style="animation-duration:{0.5+rnd.random()*0.9:.2f}s;animation-delay:-{rnd.random()*2:.2f}s"/>')
    return "".join(out)


def flow_dot(ctx, path_id, dur=2.6, begin=0.0, r=3, color=None):
    color = color or ctx.c["red2"]
    return (f'<rect x="{-r}" y="{-r}" width="{2*r}" height="{2*r}" fill="{color}"><animateMotion dur="{dur}s" begin="{begin}s" repeatCount="indefinite"><mpath xlink:href="#{path_id}"/></animateMotion></rect>'
            f'<rect x="{-r*2.4}" y="{-r*2.4}" width="{r*4.8}" height="{r*4.8}" fill="{color}" opacity="0.18"><animateMotion dur="{dur}s" begin="{begin}s" repeatCount="indefinite"><mpath xlink:href="#{path_id}"/></animateMotion></rect>')


def paragraph(ctx, text, x, y, max_w, size=15, color=None, font="sans", lh=None, ls=0, anchor="start"):
    color = color or ctx.c["text2"]
    lh = lh or round(size * 1.6)
    out = []
    for ln in typo.wrap(text, font, size, max_w, ls):
        out.append(ctx.t(ln, x, y, size, color, font, ls=ls, anchor=anchor))
        y += lh
    return "\n".join(out), y


def silver_grad(ctx, gid, vertical=True):
    stops = "".join(f'<stop offset="{o}" stop-color="{col}"/>' for o, col in ctx.c["name_stops"])
    d = 'x1="0" y1="0" x2="0.12" y2="1"' if vertical else 'x1="0" y1="0" x2="1" y2="0"'
    ctx.defs(f'<linearGradient id="{gid}" {d}>{stops}</linearGradient>')
    return f"url(#{gid})"
