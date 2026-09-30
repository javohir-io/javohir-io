# -*- coding: utf-8 -*-
"""Shared building blocks for every SVG: drawing context, luxury frame, dust, sparkles, chips."""
import random
from xml.sax.saxutils import escape as _esc

import typo

W = 1000


def esc(s):
    return _esc(str(s))


class Ctx:
    """Collects CSS / defs / used glyphs for one SVG file, then renders the final document."""

    def __init__(self, c, uid, h, w=W, title="section", desc=""):
        self.c, self.uid, self.w, self.h = c, uid, w, h
        self.title, self.desc = title, desc
        self._css, self._defs = [], []
        self.used = {k: set() for k in typo.FONTS}
        self.reduced = []      # extra rules for prefers-reduced-motion

    # ---- ids / css / defs -------------------------------------------------
    def id(self, name):
        return f"{name}{self.uid}"

    def css(self, rule):
        self._css.append(rule)

    def defs(self, s):
        self._defs.append(s)

    # ---- text ---------------------------------------------------------------
    def t(self, s, x, y, size, fill=None, font="sans", anchor="start", ls=0,
          opacity=None, cls=None, style=None, extra="", fs_attr=None):
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

    # ---- document -----------------------------------------------------------
    def render(self, body):
        font_css = typo.font_face_css(self.used)
        reduced = "".join(self.reduced)
        css = "\n".join(self._css)
        return (
            f'<svg width="{self.w}" height="{self.h}" viewBox="0 0 {self.w} {self.h}" '
            f'xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'role="img" aria-label="{esc(self.title)}">\n'
            f'<title>{esc(self.title)}</title>\n'
            + (f'<desc>{esc(self.desc)}</desc>\n' if self.desc else "")
            + f'<style>\n{font_css}\n{css}\n'
            f'@media (prefers-reduced-motion: reduce){{*{{animation:none!important}}{reduced}}}\n</style>\n'
            f'<defs>\n{chr(10).join(self._defs)}\n</defs>\n{body}\n</svg>\n'
        )


# ---------------------------------------------------------------------------
# small shapes
# ---------------------------------------------------------------------------
def diamond(x, y, r, fill, opacity=1, stroke=None, sw=1):
    st = f' stroke="{stroke}" stroke-width="{sw}"' if stroke else ""
    return (f'<path d="M{x} {y-r} L{x+r} {y} L{x} {y+r} L{x-r} {y} Z" fill="{fill}" '
            f'opacity="{opacity}"{st}/>')


def star4(x, y, r, fill, opacity=1):
    k = r * 0.16
    d = (f"M{x} {y-r} Q{x+k} {y-k} {x+r} {y} Q{x+k} {y+k} {x} {y+r} "
         f"Q{x-k} {y+k} {x-r} {y} Q{x-k} {y-k} {x} {y-r} Z")
    return f'<path d="{d}" fill="{fill}" opacity="{opacity}"/>'


def hair(x1, x2, y, color, op=0.3, sw=1):
    return f'<line x1="{x1}" y1="{y}" x2="{x2}" y2="{y}" stroke="{color}" stroke-opacity="{op}" stroke-width="{sw}"/>'


def fade_line(ctx, x1, x2, y, key, op=0.9, sw=1, both=True):
    """Hairline that fades out at one or both ends (gold)."""
    gid = ctx.id("fl" + key)
    stops = (f'<stop offset="0" stop-color="{ctx.c["gold"]}" stop-opacity="0"/>'
             f'<stop offset="0.5" stop-color="{ctx.c["gold"]}" stop-opacity="{op}"/>'
             f'<stop offset="1" stop-color="{ctx.c["gold"]}" stop-opacity="0"/>') if both else (
             f'<stop offset="0" stop-color="{ctx.c["gold"]}" stop-opacity="{op}"/>'
             f'<stop offset="1" stop-color="{ctx.c["gold"]}" stop-opacity="0"/>')
    ctx.defs(f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0">{stops}</linearGradient>')
    return f'<rect x="{x1}" y="{y - sw/2}" width="{x2-x1}" height="{sw}" fill="url(#{gid})"/>'


# ---------------------------------------------------------------------------
# frame: background, spotlight, aurora, double hairline border, corner jewels
# ---------------------------------------------------------------------------
def frame(ctx, r=6, aurora=True, spot=True, chase=False, aurora_cfg=None):
    c, w, h = ctx.c, ctx.w, ctx.h
    u = ctx.uid
    ctx.defs(f'''<clipPath id="clip{u}"><rect width="{w}" height="{h}" rx="{r}"/></clipPath>
<linearGradient id="bg{u}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c['bg']}"/><stop offset="1" stop-color="{c['bg2']}"/></linearGradient>
<radialGradient id="spot{u}" cx="50%" cy="0%" r="80%"><stop offset="0" stop-color="{c['gold2']}" stop-opacity="{c['spot_op']}"/><stop offset="1" stop-color="{c['gold2']}" stop-opacity="0"/></radialGradient>
<radialGradient id="aurR{u}"><stop offset="0" stop-color="{c['rose']}" stop-opacity="{c['aurora_op']}"/><stop offset="1" stop-color="{c['rose']}" stop-opacity="0"/></radialGradient>
<radialGradient id="aurL{u}"><stop offset="0" stop-color="{c['lilac']}" stop-opacity="{c['aurora_op']}"/><stop offset="1" stop-color="{c['lilac']}" stop-opacity="0"/></radialGradient>
<radialGradient id="aurA{u}"><stop offset="0" stop-color="{c['aqua']}" stop-opacity="{c['aurora_op']*0.8:.3f}"/><stop offset="1" stop-color="{c['aqua']}" stop-opacity="0"/></radialGradient>''')

    layers = [f'<rect width="{w}" height="{h}" fill="url(#bg{u})"/>']
    if spot:
        layers.append(f'<rect width="{w}" height="{h}" fill="url(#spot{u})"/>')
    if aurora:
        cfg = aurora_cfg or [("aurL", 0.18, 0.30, 300, 26, 70, 30), ("aurR", 0.82, 0.62, 280, 30, -80, -20),
                             ("aurA", 0.55, 1.00, 240, 34, 60, -40)]
        for i, (g, fx, fy, rad, dur, dx, dy) in enumerate(cfg):
            ctx.css(f"@keyframes au{u}{i}{{from{{transform:translate(0,0)}}to{{transform:translate({dx}px,{dy}px)}}}}"
                    f".au{u}{i}{{animation:au{u}{i} {dur}s ease-in-out infinite alternate}}")
            layers.append(f'<circle class="au{u}{i}" cx="{w*fx:.0f}" cy="{h*fy:.0f}" r="{rad}" fill="url(#{g}{u})"/>')
    return f'<g clip-path="url(#clip{u})">' + "".join(layers) + "</g>"


def border(ctx, r=6, chase=False, jewels=True):
    """Double hairline border + corner jewels (drawn above content)."""
    c, w, h, u = ctx.c, ctx.w, ctx.h, ctx.uid
    s = [f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="{r}" fill="none" stroke="{c["gold"]}" '
         f'stroke-opacity="{c["line_op"]}"/>',
         f'<rect x="8.5" y="8.5" width="{w-17}" height="{h-17}" rx="{max(r-3,1)}" fill="none" stroke="{c["gold"]}" '
         f'stroke-opacity="{c["line2_op"]}"/>']
    if jewels:
        for (x, y) in [(8.5, 8.5), (w-8.5, 8.5), (w-8.5, h-8.5), (8.5, h-8.5)]:
            s.append(diamond(x, y, 3.2, c["gold"], 0.95))
    if chase:
        ctx.css(f"@keyframes ch{u}{{from{{stroke-dashoffset:0}}to{{stroke-dashoffset:-1000}}}}"
                f".ch{u}{{animation:ch{u} 11s linear infinite}}")
        ctx.defs(f'<linearGradient id="chg{u}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{c["gold2"]}" stop-opacity="0"/>'
                 f'<stop offset="1" stop-color="{c["gold2"]}" stop-opacity="1"/></linearGradient>')
        s.append(f'<rect class="ch{u}" x="0.5" y="0.5" width="{w-1}" height="{h-1}" rx="{r}" fill="none" '
                 f'stroke="{c["gold2"]}" stroke-width="1.6" pathLength="1000" stroke-dasharray="70 930" '
                 f'stroke-linecap="round" opacity="0.95"/>')
    return "\n".join(s)


# ---------------------------------------------------------------------------
# living details
# ---------------------------------------------------------------------------
def dust(ctx, n=26, seed=1, x0=0, x1=None, y0=0, y1=None, rise=90, sizes=(0.7, 1.9)):
    """Gold motes drifting upward and fading — cheap (transform + opacity only)."""
    x1 = x1 or ctx.w
    y1 = y1 or ctx.h
    u = ctx.uid
    rnd = random.Random(seed)
    ctx.css(f"@keyframes dust{u}{{0%{{transform:translateY(0);opacity:0}}18%{{opacity:1}}82%{{opacity:.85}}"
            f"100%{{transform:translateY(-{rise}px);opacity:0}}}}")
    out = []
    for i in range(n):
        x, y = rnd.uniform(x0, x1), rnd.uniform(y0 + 20, y1)
        r = rnd.uniform(*sizes)
        dur, dl = rnd.uniform(9, 20), -rnd.uniform(0, 20)
        col = ctx.c["gold2"] if rnd.random() < 0.7 else (ctx.c["rose"] if rnd.random() < 0.5 else ctx.c["aqua"])
        out.append(f'<circle cx="{x:.0f}" cy="{y:.0f}" r="{r:.2f}" fill="{col}" opacity="0" '
                   f'style="animation:dust{u} {dur:.1f}s linear {dl:.1f}s infinite"/>')
    return "\n".join(out)


def sparkles(ctx, pts, seed=3, size=(5, 9), dur=(3.2, 6.5)):
    """Four-point glints that scale in/out. `pts` = list of (x, y)."""
    u = ctx.uid
    rnd = random.Random(seed)
    ctx.css(f"@keyframes tw{u}{{0%,100%{{transform:scale(.15) rotate(0deg);opacity:0}}50%{{transform:scale(1) rotate(45deg);opacity:1}}}}"
            f".tw{u}{{transform-box:fill-box;transform-origin:center;animation:tw{u} 4s ease-in-out infinite}}")
    out = []
    for (x, y) in pts:
        r = rnd.uniform(*size)
        col = ctx.c["gold2"]
        d, dl = rnd.uniform(*dur), -rnd.uniform(0, 6)
        out.append(f'<g class="tw{u}" style="animation-duration:{d:.1f}s;animation-delay:{dl:.1f}s">{star4(x, y, r, col)}</g>')
    return "\n".join(out)


def chip(ctx, x, y, label, primary=False, h=30, size=13):
    """Outlined pill. Primary chips carry a gold gem and a breathing fill."""
    c = ctx.c
    pad = 15
    gem = 15 if primary else 0
    tw = ctx.w_(label, "sansm", size, 0.2)
    w = tw + pad * 2 + gem
    r = h / 2
    if primary:
        ctx.css(f"@keyframes br{ctx.uid}{{from{{opacity:.10}}to{{opacity:.26}}}}.br{ctx.uid}{{animation:br{ctx.uid} 3.4s ease-in-out infinite alternate}}")
        s = (f'<rect class="br{ctx.uid}" x="{x}" y="{y}" width="{w:.1f}" height="{h}" rx="{r}" fill="{c["gold"]}" style="animation-delay:-{(x*7+y*3)%34/10:.1f}s"/>'
             f'<rect x="{x+.5}" y="{y+.5}" width="{w-1:.1f}" height="{h-1}" rx="{r}" fill="none" stroke="{c["gold"]}" stroke-opacity="0.85"/>'
             + diamond(x + pad, y + h / 2, 3.2, c["gold"])
             + ctx.t(label, x + pad + gem - 1, y + h / 2 + size * 0.36, size, c["text"], "sansm", ls=0.2))
    else:
        s = (f'<rect x="{x+.5}" y="{y+.5}" width="{w-1:.1f}" height="{h-1}" rx="{r}" fill="{c["chip_fill"]}" '
             f'stroke="{c["gold"]}" stroke-opacity="0.32"/>'
             + ctx.t(label, x + pad, y + h / 2 + size * 0.36, size, c["text2"], "sansm", ls=0.2))
    return s, w


def flow_dot(ctx, path_id, dur=2.6, begin=0.0, r=3.2, color=None):
    color = color or ctx.c["gold2"]
    return (f'<circle r="{r}" fill="{color}"><animateMotion dur="{dur}s" begin="{begin}s" repeatCount="indefinite">'
            f'<mpath xlink:href="#{path_id}"/></animateMotion></circle>'
            f'<circle r="{r*2.6}" fill="{color}" opacity="0.18"><animateMotion dur="{dur}s" begin="{begin}s" repeatCount="indefinite">'
            f'<mpath xlink:href="#{path_id}"/></animateMotion></circle>')


def link_path(ctx, pid, d, dashed=True, color=None, op=0.55):
    color = color or ctx.c["gold"]
    dash = ' stroke-dasharray="3 5"' if dashed else ""
    return f'<path id="{pid}" d="{d}" fill="none" stroke="{color}" stroke-opacity="{op}" stroke-width="1.2"{dash}/>'


# ---------------------------------------------------------------------------
# text layout helpers
# ---------------------------------------------------------------------------
def paragraph(ctx, text, x, y, max_w, size=15, color=None, font="sans", lh=None, ls=0, anchor="start"):
    """Wrapped paragraph. Returns (svg, y_after_last_line)."""
    color = color or ctx.c["text2"]
    lh = lh or round(size * 1.6)
    out = []
    for ln in typo.wrap(text, font, size, max_w, ls):
        out.append(ctx.t(ln, x, y, size, color, font, ls=ls, anchor=anchor))
        y += lh
    return "\n".join(out), y


def bullets(ctx, items, x, y, col_w, cols=2, size=13.5, lh=25, gap=18, color=None):
    """Gem-bulleted list flowing down `cols` columns. Returns (svg, y_after_tallest_col)."""
    color = color or ctx.c["text"]
    per = -(-len(items) // cols)
    out, ends = [], []
    for ci in range(cols):
        cx = x + ci * (col_w + gap)
        cy = y
        for it in items[ci * per:(ci + 1) * per]:
            lines = typo.wrap(it, "sans", size, col_w - 16)
            out.append(diamond(cx + 3, cy - size * 0.32, 2.6, ctx.c["gold"], 0.9))
            for j, ln in enumerate(lines):
                out.append(ctx.t(ln, cx + 16, cy + j * (lh * 0.84), size, color, "sans"))
            cy += lh + (len(lines) - 1) * lh * 0.84
        ends.append(cy)
    return "\n".join(out), max(ends)


def card(ctx, x, y, w, h, key, r=6):
    """Self-contained panel used when an SVG holds several cards. Returns (svg, clip_id)."""
    c, u = ctx.c, ctx.uid
    cid, gid = f"cc{u}{key}", f"cg{u}{key}"
    ctx.defs(f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}"/></clipPath>'
             f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c["bg"]}"/>'
             f'<stop offset="1" stop-color="{c["bg2"]}"/></linearGradient>')
    s = (f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="url(#{gid})"/>')
    edge = (f'<rect x="{x+.5}" y="{y+.5}" width="{w-1}" height="{h-1}" rx="{r}" fill="none" stroke="{c["gold"]}" stroke-opacity="{c["line_op"]}"/>'
            f'<rect x="{x+7.5}" y="{y+7.5}" width="{w-15}" height="{h-15}" rx="{max(r-3,1)}" fill="none" stroke="{c["gold"]}" stroke-opacity="{c["line2_op"]}"/>'
            + "".join(diamond(px, py, 2.6, c["gold"], 0.9) for px, py in
                      [(x+7.5, y+7.5), (x+w-7.5, y+7.5), (x+w-7.5, y+h-7.5), (x+7.5, y+h-7.5)]))
    return s, edge, cid
