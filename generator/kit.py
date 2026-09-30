# -*- coding: utf-8 -*-
"""Shared building blocks: drawing context, chamfered frame, carbon weave, engraving, rulers, watch dial."""
import math
import random
from xml.sax.saxutils import escape as _esc

import typo

W = 1000
CUT = 22          # chamfer size on the top-left and bottom-right corners


def esc(s):
    return _esc(str(s))


class Ctx:
    """Collects CSS / defs / used glyphs for one SVG file, then renders the final document."""

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

    def t(self, s, x, y, size, fill=None, font="sans", anchor="start", ls=0,
          opacity=None, cls=None, style=None, extra=""):
        fill = fill or self.c["text"]
        spec = typo.FONTS[font]
        self.used[font] |= set(str(s))
        miss = typo.missing_glyphs(str(s), font)
        if miss:
            print(f"   ! [{self.uid}] glyphs missing in {font}: {miss}")
        a = (f'x="{x}" y="{y}" font-family="{spec["stack"]}" font-weight="{spec["weight"]}" '
             f'font-size="{size}" fill="{fill}"')
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
        css = "\n".join(self._css)
        return (
            f'<svg width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" '
            f'xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'role="img" aria-label="{esc(self.title)}">\n<title>{esc(self.title)}</title>\n'
            + (f'<desc>{esc(self.desc)}</desc>\n' if self.desc else "")
            + f'<style>\n{font_css}\n{css}\n'
            f'@media (prefers-reduced-motion: reduce){{*{{animation:none!important}}{"".join(self.reduced)}}}\n</style>\n'
            f'<defs>\n{chr(10).join(self._defs)}\n</defs>\n{body}\n</svg>\n')


# ---------------------------------------------------------------------------
# primitives
# ---------------------------------------------------------------------------
def gt(c):
    """Accent colour that reads on the current theme."""
    return c["gold2"] if c["is_dark"] else c["gold"]


def chamfer(x, y, w, h, cut=CUT):
    return (f"{x+cut},{y} {x+w},{y} {x+w},{y+h-cut} {x+w-cut},{y+h} {x},{y+h} {x},{y+cut}")


def sq(x, y, r, fill, op=1):
    return f'<rect x="{x-r}" y="{y-r}" width="{2*r}" height="{2*r}" fill="{fill}" opacity="{op}"/>'


def hair(x1, x2, y, color, op=0.3, sw=1):
    return f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{color}" stroke-opacity="{op}" stroke-width="{sw}"/>'


def fade_line(ctx, x1, x2, y, key, op=0.9, sw=1, both=True, color=None):
    color = color or ctx.c["gold"]
    gid = ctx.id("fl" + key)
    if both:
        stops = (f'<stop offset="0" stop-color="{color}" stop-opacity="0"/><stop offset="0.5" stop-color="{color}" stop-opacity="{op}"/>'
                 f'<stop offset="1" stop-color="{color}" stop-opacity="0"/>')
    else:
        stops = f'<stop offset="0" stop-color="{color}" stop-opacity="{op}"/><stop offset="1" stop-color="{color}" stop-opacity="0"/>'
    ctx.defs(f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0">{stops}</linearGradient>')
    return f'<rect x="{x1}" y="{y - sw/2}" width="{x2-x1}" height="{sw}" fill="url(#{gid})"/>'


def cross(x, y, s, color, op=0.6):
    return (f'<path d="M{x-s} {y}H{x+s}M{x} {y-s}V{y+s}" stroke="{color}" stroke-opacity="{op}" stroke-width="1" fill="none"/>')


def ticks_h(x, y, w, n, major, color, op=0.5, ln=5, lm=10, up=False):
    d = ""
    for i in range(n + 1):
        px = x + w * i / n
        L = lm if i % major == 0 else ln
        d += f"M{px:.1f} {y}v{-L if up else L}"
    return f'<path d="{d}" stroke="{color}" stroke-opacity="{op}" stroke-width="1" fill="none"/>'


def ticks_v(x, y, h, n, major, color, op=0.5, ln=5, lm=10, left=False):
    d = ""
    for i in range(n + 1):
        py = y + h * i / n
        L = lm if i % major == 0 else ln
        d += f"M{x} {py:.1f}h{-L if left else L}"
    return f'<path d="{d}" stroke="{color}" stroke-opacity="{op}" stroke-width="1" fill="none"/>'


def rosette(ctx, cx, cy, r, n=28, spin=140, color=None, op=0.14):
    """Guilloche engraving: a rosette of rotated ellipses plus concentric rings, slowly turning."""
    color = color or ctx.c["gold"]
    u = ctx.uid
    ctx.css(f"@keyframes ro{u}{{to{{transform:rotate(360deg)}}}}.ro{u}{{transform-origin:{cx}px {cy}px;animation:ro{u} {spin}s linear infinite}}")
    els = "".join(f'<ellipse cx="{cx}" cy="{cy}" rx="{r}" ry="{r*0.42:.1f}" transform="rotate({i*180/n:.2f} {cx} {cy})"/>' for i in range(n))
    rings = "".join(f'<circle cx="{cx}" cy="{cy}" r="{r*k:.1f}"/>' for k in (0.28, 0.5, 1.0))
    return (f'<g fill="none" stroke="{color}" stroke-opacity="{op}" stroke-width="0.8">'
            f'<g class="ro{u}">{els}</g>{rings}</g>')


def dial(ctx, cx, cy, r, label=None, hand_s=20, key="d", show_hand=True):
    """A small watch-dial emblem with a sweeping seconds hand."""
    c, u = ctx.c, ctx.uid
    ctx.css(f"@keyframes hd{u}{key}{{to{{transform:rotate(360deg)}}}}.hd{u}{key}{{transform-origin:{cx}px {cy}px;animation:hd{u}{key} {hand_s}s linear infinite}}")
    d = ""
    for i in range(60):
        a = math.radians(i * 6 - 90)
        L = 6 if i % 5 == 0 else 3
        d += f"M{cx+(r-L)*math.cos(a):.1f} {cy+(r-L)*math.sin(a):.1f}L{cx+r*math.cos(a):.1f} {cy+r*math.sin(a):.1f}"
    s = [f'<circle cx="{cx}" cy="{cy}" r="{r+6}" fill="{c["bg"]}" fill-opacity="0.6" stroke="{c["gold"]}" stroke-opacity="0.5"/>',
         f'<path d="{d}" stroke="{c["gold"]}" stroke-opacity="0.85" stroke-width="1" fill="none"/>']
    if label:
        s.append(ctx.t(label, cx, cy + 6, r * 0.5, gt(c), "serif", anchor="middle", ls=1))
    if show_hand:
        s.append(f'<g class="hd{u}{key}"><line x1="{cx}" y1="{cy+7}" x2="{cx}" y2="{cy-r+4}" stroke="{c["gold2"]}" stroke-width="1.4"/>'
                 f'<circle cx="{cx}" cy="{cy-r+7}" r="2" fill="{c["good"]}"/></g>')
    return "\n".join(s)


# ---------------------------------------------------------------------------
# frame
# ---------------------------------------------------------------------------
def frame(ctx, cut=CUT, glow=True, scan=False):
    """Chamfered obsidian panel: gradient, carbon weave, drifting green + steel glows. Returns the background group."""
    c, w, h, u = ctx.c, ctx.w, ctx.h, ctx.uid
    poly = chamfer(0, 0, w, h, cut)
    carbon_b = (f'<rect x="4" y="0" width="4" height="4" fill="#000" fill-opacity="{c["carbon_b"]}"/>'
                f'<rect x="0" y="4" width="4" height="4" fill="#000" fill-opacity="{c["carbon_b"]}"/>') if c["carbon_b"] else ""
    ctx.defs(f'''<clipPath id="clip{u}"><polygon points="{poly}"/></clipPath>
<linearGradient id="bg{u}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c['bg2']}"/><stop offset="0.55" stop-color="{c['bg']}"/><stop offset="1" stop-color="{c['bg2']}"/></linearGradient>
<pattern id="cw{u}" width="8" height="8" patternUnits="userSpaceOnUse"><rect width="4" height="4" fill="{'#fff' if c['is_dark'] else '#000'}" fill-opacity="{c['carbon_a']}"/><rect x="4" y="4" width="4" height="4" fill="{'#fff' if c['is_dark'] else '#000'}" fill-opacity="{c['carbon_a']}"/>{carbon_b}</pattern>
<radialGradient id="spot{u}" cx="50%" cy="0%" r="75%"><stop offset="0" stop-color="{c['steel']}" stop-opacity="{c['spot_op']}"/><stop offset="1" stop-color="{c['steel']}" stop-opacity="0"/></radialGradient>
<radialGradient id="gE{u}"><stop offset="0" stop-color="{c['emerald']}" stop-opacity="{c['glow_op']}"/><stop offset="1" stop-color="{c['emerald']}" stop-opacity="0"/></radialGradient>
<radialGradient id="gB{u}"><stop offset="0" stop-color="{c['gold']}" stop-opacity="{c['glow_op']*0.7:.3f}"/><stop offset="1" stop-color="{c['gold']}" stop-opacity="0"/></radialGradient>
<linearGradient id="scan{u}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c['steel']}" stop-opacity="0"/><stop offset="0.5" stop-color="{c['steel']}" stop-opacity="0.10"/><stop offset="1" stop-color="{c['steel']}" stop-opacity="0"/></linearGradient>''')
    layers = [f'<rect width="{w}" height="{h}" fill="url(#bg{u})"/>', f'<rect width="{w}" height="{h}" fill="url(#cw{u})"/>',
              f'<rect width="{w}" height="{h}" fill="url(#spot{u})"/>']
    if glow:
        for i, (g, fx, fy, rad, dur, dx, dy) in enumerate([("gE", 0.15, 0.75, 300, 26, 80, -30), ("gB", 0.88, 0.25, 260, 30, -70, 30)]):
            ctx.css(f"@keyframes au{u}{i}{{from{{transform:translate(0,0)}}to{{transform:translate({dx}px,{dy}px)}}}}"
                    f".au{u}{i}{{animation:au{u}{i} {dur}s ease-in-out infinite alternate}}")
            layers.append(f'<circle class="au{u}{i}" cx="{w*fx:.0f}" cy="{h*fy:.0f}" r="{rad}" fill="url(#{g}{u})"/>')
    if scan:
        ctx.css(f"@keyframes sc{u}{{from{{transform:translateY(-90px)}}to{{transform:translateY({h+10}px)}}}}.sc{u}{{animation:sc{u} 9s linear infinite}}")
        layers.append(f'<rect class="sc{u}" x="0" y="0" width="{w}" height="90" fill="url(#scan{u})"/>')
    return f'<g clip-path="url(#clip{u})">' + "".join(layers) + "</g>"


def border(ctx, cut=CUT, chase=False, rivets=True):
    c, w, h, u = ctx.c, ctx.w, ctx.h, ctx.uid
    o, i = chamfer(0.5, 0.5, w - 1, h - 1, cut), chamfer(8.5, 8.5, w - 17, h - 17, cut - 6)
    s = [f'<polygon points="{o}" fill="none" stroke="{c["gold"]}" stroke-opacity="{c["line_op"]}"/>',
         f'<polygon points="{i}" fill="none" stroke="{c["steel"]}" stroke-opacity="{c["line2_op"]}"/>']
    # bright L-brackets on the two square corners
    b = 26
    s.append(f'<path d="M{w-b} 0.5H{w-0.5}V{b}M0.5 {h-b}V{h-0.5}H{b}" fill="none" stroke="{c["gold2"] if c["is_dark"] else c["gold"]}" stroke-width="2"/>')
    if rivets:
        for (rx, ry) in [(w - 17, 17), (17, h - 17)]:
            s.append(f'<circle cx="{rx}" cy="{ry}" r="3.4" fill="{c["chip_fill"]}" stroke="{c["gold"]}" stroke-opacity="0.8"/>'
                     f'<path d="M{rx-2} {ry+2}L{rx+2} {ry-2}" stroke="{c["gold"]}" stroke-opacity="0.8"/>')
    if chase:
        ctx.css(f"@keyframes ch{u}{{from{{stroke-dashoffset:0}}to{{stroke-dashoffset:-1000}}}}.ch{u}{{animation:ch{u} 12s linear infinite}}")
        s.append(f'<polygon class="ch{u}" points="{o}" fill="none" stroke="{c["gold2"]}" stroke-width="2" pathLength="1000" '
                 f'stroke-dasharray="90 910" stroke-linecap="butt"/>')
    return "\n".join(s)


def flow_dot(ctx, path_id, dur=2.6, begin=0.0, r=3, color=None):
    color = color or ctx.c["gold2"]
    return (f'<rect x="{-r}" y="{-r}" width="{2*r}" height="{2*r}" fill="{color}"><animateMotion dur="{dur}s" begin="{begin}s" repeatCount="indefinite">'
            f'<mpath xlink:href="#{path_id}"/></animateMotion></rect>'
            f'<rect x="{-r*2.4}" y="{-r*2.4}" width="{r*4.8}" height="{r*4.8}" fill="{color}" opacity="0.16"><animateMotion dur="{dur}s" begin="{begin}s" repeatCount="indefinite">'
            f'<mpath xlink:href="#{path_id}"/></animateMotion></rect>')


def link_path(ctx, pid, d, dashed=True, color=None, op=0.55):
    color = color or ctx.c["gold"]
    dash = ' stroke-dasharray="3 5"' if dashed else ""
    return f'<path id="{pid}" d="{d}" fill="none" stroke="{color}" stroke-opacity="{op}" stroke-width="1.2"{dash}/>'


def paragraph(ctx, text, x, y, max_w, size=15, color=None, font="sans", lh=None, ls=0, anchor="start"):
    color = color or ctx.c["text2"]
    lh = lh or round(size * 1.6)
    out = []
    for ln in typo.wrap(text, font, size, max_w, ls):
        out.append(ctx.t(ln, x, y, size, color, font, ls=ls, anchor=anchor))
        y += lh
    return "\n".join(out), y


def card(ctx, x, y, w, h, key, cut=16):
    """Chamfered sub-panel for SVGs holding several cards. Returns (bg, edge, clip_id)."""
    c, u = ctx.c, ctx.uid
    cid, gid = f"cc{u}{key}", f"cg{u}{key}"
    ctx.defs(f'<clipPath id="{cid}"><polygon points="{chamfer(x, y, w, h, cut)}"/></clipPath>'
             f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c["bg2"]}"/><stop offset="1" stop-color="{c["bg"]}"/></linearGradient>')
    bg = (f'<polygon points="{chamfer(x, y, w, h, cut)}" fill="url(#{gid})"/>'
          f'<g clip-path="url(#{cid})"><rect x="{x}" y="{y}" width="{w}" height="{h}" fill="url(#cw{u})"/></g>')
    edge = (f'<polygon points="{chamfer(x+.5, y+.5, w-1, h-1, cut)}" fill="none" stroke="{c["gold"]}" stroke-opacity="{c["line_op"]}"/>'
            f'<path d="M{x+w-20} {y+.5}H{x+w-.5}V{y+20}M{x+.5} {y+h-20}V{y+h-.5}H{x+20}" fill="none" stroke="{gt(c)}" stroke-width="1.8"/>')
    return bg, edge, cid
