# -*- coding: utf-8 -*-
"""The eight panels. Each builder takes a palette `c` and returns an SVG string."""
import math
import random

from common import (roman, W, MX, SANS, BASE_CSS, Glyphs, otext, stext, esc, svg_open, diamond, glint,
                    ghost, panel, burst_kf, accent_gradient)

ROLES = ["FLUTTER DEVELOPER", "NODE.JS BACKEND ENGINEER", "REACT & TYPESCRIPT DEVELOPER", "SOFTWARE ENGINEER"]
EMAIL = "javohirabduvahhobov@gmail.com"
EXTRA_CSS = "@keyframes mote{0%{opacity:0;transform:translateY(0)}20%{opacity:.9}80%{opacity:.9}100%{opacity:0;transform:translateY(-70px)}}"


def _assemble(h, title, reg, css, defs, body):
    return (f'{svg_open(h, title)}\n<defs>\n{reg.defs()}\n{defs}\n</defs>\n'
            f'<style>\n{BASE_CSS}\n{EXTRA_CSS}\n{css}\n</style>\n{body}\n</svg>')


def _rise(base, step, dur=1.3):
    return lambda i, ch: f"animation:rise {dur}s cubic-bezier(.16,.84,.3,1) {base + i * step:.2f}s both"


def motes(c, n, seed, xr, yr):
    rnd = random.Random(seed)
    out = []
    for _ in range(n):
        x, y = rnd.uniform(*xr), rnd.uniform(*yr)
        s = rnd.choice([1.6, 2, 2.4])
        out.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{s}" height="{s}" opacity="0" '
                   f'style="animation:mote {rnd.uniform(8, 15):.1f}s linear {-rnd.uniform(0, 15):.1f}s infinite"/>')
    return f'<g fill="{c["accent_hi"]}">{"".join(out)}</g>'


# ═══════════════════════════════════ HERO ═══════════════════════════════════
def hero(c):
    h, SZ, TR, y1, y2 = 430, 84, 7, 178, 262
    reg = Glyphs()
    pd, back, _, pcss = panel(c, W, h, glow=(0.78, 1.0), glow_r=0.75)
    n1 = otext(reg, "JAVOHIR", MX, y1, SZ, c["ink"], tracking=TR, anim=_rise(.2, .07))
    n2 = otext(reg, "ABDUVAHHOBOV", MX, y2, SZ, c["ink"], tracking=TR, anim=_rise(.65, .05))
    assert n2["x0"] + n2["width"] < W - MX

    name_clip = f'{n1["clip"]}{n2["clip"]}'
    bands = [(116, 30, c["accent"], "gb1", [(45, [-14, 10, -6]), (80, [12, -8])]),
             (150, 24, c["alt"], "gb2", [(45.5, [18, -12, 8]), (80.5, [-16, 9])]),
             (200, 26, c["ink"], "gb3", [(46, [-10, 14, -7]), (79.5, [10, -14])]),
             (232, 34, c["accent_hi"], "gb4", [(46.5, [12, -9]), (81, [-10, 6, -4])])]
    kf = [burst_kf("gA", [(44, [-6, 4, -3, 5]), (79, [5, -4, 3])], op=.7),
          burst_kf("gB", [(44.5, [6, -4, 3, -5]), (79.5, [-5, 4, -3])], op=.7)]
    kf += [burst_kf(nm, bs, op=.85) for _, _, _, nm, bs in bands]
    kf.append("@keyframes jit{0%{transform:translate(0,0)}44%{transform:translate(2px,0)}45%{transform:translate(-2px,0)}"
              "46%{transform:translate(1px,0)}47%{transform:translate(0,0)}79%{transform:translate(-2px,0)}"
              "80%{transform:translate(2px,0)}81%{transform:translate(0,0)}100%{transform:translate(0,0)}}")
    kf.append("@keyframes tear{0%{opacity:0}45%{opacity:.95;transform:translateY(0)}46%{transform:translateY(34px)}"
              "47%{transform:translateY(66px)}48%{opacity:0}80%{opacity:.95;transform:translateY(8px)}81%{transform:translateY(46px)}"
              "82%{opacity:0}100%{opacity:0}}")
    gcls = ("".join(f".{nm}{{animation:{nm} 8s steps(1,end) infinite}}" for nm in
                    ["gA", "gB"] + [b[3] for b in bands])
            + ".jit{animation:jit 8s steps(1,end) infinite}.tear{animation:tear 8s steps(1,end) infinite}")

    clips = "".join(f'<clipPath id="{nm}c"><rect x="0" y="{y}" width="{W}" height="{bh}"/></clipPath>' for y, bh, _, nm, _ in bands)
    glitch = (f'<g class="gA" opacity="0"><g fill="{c["accent"]}">{name_clip}</g></g>'
              f'<g class="gB" opacity="0"><g fill="{c["alt"]}">{name_clip}</g></g>'
              + "".join(f'<g clip-path="url(#{nm}c)"><g class="{nm}" opacity="0"><g fill="{col}">{name_clip}</g></g></g>'
                        for _, _, col, nm, _ in bands)
              + f'<rect class="tear" x="{MX}" y="116" width="{W-2*MX}" height="1.6" fill="{c["accent_hi"]}" opacity="0"/>')

    role_css = ("@keyframes slide{0%{transform:translateY(26px);opacity:0}4%{transform:translateY(0);opacity:1}"
                "22%{transform:translateY(0);opacity:1}27%{transform:translateY(-26px);opacity:0}100%{transform:translateY(-26px);opacity:0}}"
                ".role{animation:slide 14s cubic-bezier(.2,.8,.2,1) infinite}"
                "@keyframes prog{from{transform:scaleX(0)}to{transform:scaleX(1)}}"
                ".prog{transform-box:fill-box;transform-origin:left center;animation:prog 3.5s linear infinite}"
                "@keyframes streak{0%{transform:translateX(0)}28%{transform:translateX(1600px)}100%{transform:translateX(1600px)}}"
                ".streak{animation:streak 11s cubic-bezier(.4,0,.3,1) 2s infinite}"
                "@keyframes draw{from{stroke-dashoffset:34}to{stroke-dashoffset:0}}")
    roles = "".join(
        f'<text class="role" opacity="0" x="{MX}" y="318" font-family="{SANS}" font-size="14" font-weight="600" letter-spacing="4.2" '
        f'style="animation-delay:{i * 3.5}s"><tspan fill="{c["accent"]}">{roman(i + 1)}</tspan><tspan dx="18" fill="{c["ink"]}">{esc(r)}</tspan></text>'
        for i, r in enumerate(ROLES))

    ghost_ja = ghost(reg, "JA", W - MX, y1 + 10, 160, c, anchor="end", tracking=8, sw=1.1, op=.42, dur=8, stagger=2.4)
    # glint() emits <clipPath>/<linearGradient>/<line>/<g>; keep the drawable parts in body, definitions in defs
    bt = glint(c, "bt", MX, W - MX, 372, dur=9, delay=1)
    defs = pd + clips + (f'<clipPath id="rclip"><rect x="{MX}" y="292" width="600" height="34"/></clipPath>'
                         f'<linearGradient id="streakg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{c["accent_hi"]}" stop-opacity="0"/>'
                         f'<stop offset=".5" stop-color="{c["accent_hi"]}" stop-opacity=".09"/><stop offset="1" stop-color="{c["accent_hi"]}" stop-opacity="0"/></linearGradient>')
    css = pcss + role_css + "".join(kf) + gcls

    body = f'''{back}
<g clip-path="url(#pclip)"><g transform="skewX(-20)"><rect class="streak" x="-420" y="0" width="150" height="{h}" fill="url(#streakg)"/></g></g>
{motes(c, 14, 7, (40, 960), (60, 400))}
{ghost_ja["svg"]}
<line x1="{MX}" y1="44" x2="{MX+30}" y2="44" stroke="{c['accent']}" stroke-width="1.5" stroke-dasharray="34" style="animation:draw 1s ease-out .3s both"/>
{stext("FULL-STACK & MOBILE ENGINEER", MX + 46, 48, 12, c["text2"], weight=600, tracking=4.4, extra='style="animation:fade 1.2s ease-out .5s both"')}
{stext("PORTFOLIO — MMXXVI", W - MX, 48, 11, c["text3"], anchor="end", weight=500, tracking=3.6)}
<g class="jit">{n1["svg"]}{n2["svg"]}</g>
{glitch}
<line x1="{MX}" y1="288" x2="{MX+600}" y2="288" stroke="{c['line']}"/>
<g clip-path="url(#rclip)">{roles}</g>
<line x1="{MX}" y1="332" x2="{MX+600}" y2="332" stroke="{c['line']}"/>
<rect class="prog" x="{MX}" y="331" width="600" height="2" fill="{c['accent']}"/>
{bt}
<rect x="{MX}" y="394" width="7" height="7" fill="{c['accent']}"/><rect class="ping" x="{MX}" y="394" width="7" height="7" fill="none" stroke="{c['accent']}"/>
{stext("AVAILABLE FOR OPPORTUNITIES", MX + 20, 402, 12, c["text2"], weight=500, tracking=3.6)}
{stext("BSc SOFTWARE ENGINEERING", W - MX, 402, 12, c["text3"], anchor="end", weight=500, tracking=3.6)}'''
    return _assemble(h, "Javohir Abduvahhobov — Full-stack & Mobile Engineer", reg, css, defs, body)


# ═══════════════════════════════════ PROFILE ═══════════════════════════════════
def profile(c):
    h = 346
    reg = Glyphs()
    pd, back, front, pcss = panel(c, W, h, "I", "PROFILE", glow=(0.9, 0.25))
    hl = otext(reg, "One engineer. The whole pipeline.", MX, 136, 38, c["ink"])
    lines = ["Full-stack and mobile engineer who ships the entire pipeline —",
             "Flutter on the client, a Node.js / Express REST API in the middle,",
             "PostgreSQL underneath, and a lightweight admin panel wired to it all."]
    para = "".join(stext(t, MX, 180 + i * 26, 15.5, c["text2"]) for i, t in enumerate(lines))
    gh = ghost(reg, "I", W - MX, 238, 180, c, anchor="end", tracking=6, dur=7, stagger=1.5)
    creds = [("DEGREE", "BSc Software Engineering"), ("DISCIPLINES", "Mobile · Backend · DB · Admin"),
             ("STATUS", "Open to opportunities")]
    cols = []
    for i, (lab, val) in enumerate(creds):
        x = MX + i * 286
        cols.append(f'<line x1="{x}" y1="266" x2="{x+272}" y2="266" stroke="{c["line"]}"/>'
                    f'<rect class="fill" x="{x}" y="265" width="272" height="2" fill="{c["accent"]}" style="animation-delay:{i * 1.4}s"/>'
                    + stext(lab, x, 292, 11.5, c["text3"], weight=600, tracking=3.6)
                    + otext(reg, val, x, 320, 19, c["ink"], max_w=268)["svg"])
    css = pcss + ("@keyframes fill{0%{transform:scaleX(0);opacity:1}20%{transform:scaleX(1);opacity:1}88%{transform:scaleX(1);opacity:1}100%{transform:scaleX(1);opacity:0}}"
                  ".fill{transform-box:fill-box;transform-origin:left center;animation:fill 8s cubic-bezier(.5,0,.2,1) infinite}")
    body = f'{back}{front}{gh["svg"]}{hl["svg"]}{para}{"".join(cols)}'
    return _assemble(h, "Profile — one engineer, the whole pipeline", reg, css, pd, body)


# ═══════════════════════════════════ ARCHITECTURE ═══════════════════════════════════
def _brackets(x, y, w, h, l=16):
    return (f"M{x} {y+l}V{y}H{x+l}M{x+w-l} {y}H{x+w}V{y+l}M{x+w} {y+h-l}V{y+h}H{x+w-l}M{x+l} {y+h}H{x}V{y+h-l}")


def ecosystem(c):
    h = 480
    reg = Glyphs()
    pd, back, front, pcss = panel(c, W, h, "II", "ARCHITECTURE", glow=(0.5, 0.0), glow_r=0.9)
    hl = otext(reg, "System, end to end.", MX, 136, 38, c["ink"])
    NW, NH = 208, 96
    nodes = [("A", "FLUTTER APP", "Dart · http · file_picker", 72, 226, 0.0),
             ("B", "EXPRESS API", "JWT · bcryptjs · multer", 408, 226, 0.0),
             ("C", "POSTGRESQL", "users · jobs · interviews", 722, 226, 0.0),
             ("D", "ADMIN PANEL", "HTML · CSS · JavaScript", 408, 360, 0.0)]
    flash_begin = {"B": 0.0, "C": 0.5, "D": 1.0}
    nsvg = []
    for k, (idx, title, sub, x, y, _) in enumerate(nodes):
        t = otext(reg, title, x + NW / 2, y + 54, 16, c["ink"], anchor="middle", tracking=3)
        nh = NH if y == 226 else 76
        flash = ""
        if idx in flash_begin:
            flash = (f'<rect x="{x}" y="{y}" width="{NW}" height="{nh}" fill="{c["accent"]}" opacity="0">'
                     f'<animate attributeName="opacity" values=".2;0;0" keyTimes="0;.3;1" dur="2.6s" begin="{flash_begin[idx]}s" repeatCount="indefinite"/></rect>')
        sub_y = y + (74 if nh == NH else 62)
        ty = y + (54 if nh == NH else 44)
        t = otext(reg, title, x + NW / 2, ty, 16, c["ink"], anchor="middle", tracking=3)
        nsvg.append(f'''<g><rect x="{x}" y="{y}" width="{NW}" height="{nh}" fill="{c['node']}" stroke="{c['line']}"/>{flash}
<rect class="cm" pathLength="100" x="{x+.5}" y="{y+.5}" width="{NW-1}" height="{nh-1}" fill="none" stroke="{c['accent_hi']}" stroke-width="1.5" style="animation-duration:9s;animation-delay:{-k * 2.3:.1f}s"/>
<path d="{_brackets(x, y, NW, nh)}" fill="none" stroke="{c['accent']}" stroke-width="1.6"/>
{stext(roman(k + 1), x + 16, y + 26, 11.5, c["accent"], weight=700, tracking=2)}
{t["svg"]}{stext(sub, x + NW / 2, sub_y, 12.5, c["text3"], anchor="middle", tracking=.4)}</g>''')
    dock = (f'<rect x="386" y="168" width="558" height="288" fill="none" stroke="{c["accent"]}" stroke-opacity=".35" stroke-dasharray="2 6"/>'
            f'<rect x="408" y="187" width="6" height="6" fill="{c["accent"]}"/>'
            + stext("DOCKERIZED", 422, 194, 11.5, c["text3"], weight=600, tracking=4))
    lanes = [("f1", "M280 268H408", 2.6, 0.0), ("f1r", "M408 280H280", 2.6, 1.3),
             ("f2", "M616 268H722", 2.6, 0.5), ("f2r", "M722 280H616", 2.6, 1.8),
             ("f3", "M494 322V360", 1.6, 1.0), ("f3r", "M506 360V322", 1.6, 1.8)]
    lsvg = []
    for pid, d, dur, begin in lanes:
        trail = "".join(
            f'<rect x="-3.5" y="-3.5" width="7" height="7" transform="rotate(45)" fill="{c["accent_hi"]}" opacity="{op}">'
            f'<animateMotion dur="{dur}s" begin="{begin + dl}s" repeatCount="indefinite"><mpath xlink:href="#{pid}"/></animateMotion></rect>'
            for dl, op in [(0, 1), (.09, .5), (.18, .22)])
        lsvg.append(f'<path id="{pid}" d="{d}" fill="none" stroke="{c["line"]}"/>'
                    f'<path d="{d}" fill="none" stroke="{c["accent"]}" stroke-opacity=".55" stroke-dasharray="2 8"><animate attributeName="stroke-dashoffset" from="20" to="0" dur="1.6s" repeatCount="indefinite"/></path>'
                    + trail)
    labels = (stext("JWT", 344, 254, 11, c["text3"], anchor="middle", weight=600, tracking=2.5)
              + stext("pg", 669, 254, 11, c["text3"], anchor="middle", weight=600, tracking=2.5)
              + stext("REST", 520, 345, 11, c["text3"], weight=600, tracking=2.5))
    body = f'{back}{front}{hl["svg"]}{dock}{"".join(lsvg)}{"".join(nsvg)}{labels}'
    css = pcss + ".cm{stroke-dasharray:9 91}"
    return _assemble(h, "Architecture — Flutter, Express API, PostgreSQL, admin panel, Docker", reg, css, pd, body)


# ═══════════════════════════════════ STACK ═══════════════════════════════════
STACK = [
    ("MOBILE", "Flutter app", ["Flutter", "Dart", "http", "shared_preferences", "file_picker", "google_fonts", "intl", "cupertino_icons"]),
    ("BACKEND", "Node.js API", ["Node.js", "Express", "JWT", "bcryptjs", "multer", "cors", "morgan", "dotenv", "uuid", "pg"]),
    ("DATABASE", "Relational", ["PostgreSQL"]),
    ("ADMIN PANEL", "Lightweight web", ["HTML", "CSS", "JavaScript"]),
    ("FRONTEND & OTHER", "Languages", ["React", "TypeScript", "Python"]),
    ("TOOLING", "Dev workflow", ["npm", "Git", "GitHub", "Docker"]),
]


def _wrap(items, maxw):
    lines, cur = [[]], 0
    for it in items:
        w = len(it) * 7.4 + (32 if lines[-1] else 0)
        if cur + w > maxw and lines[-1]:
            lines.append([])
            cur, w = 0, len(it) * 7.4
        lines[-1].append(it)
        cur += w
    return lines


def stack(c):
    CW, PAD, y0 = 285, 24, 164
    reg = Glyphs()
    wrapped = [_wrap(items, CW - 2 * PAD) for _, _, items in STACK]
    row_h = [96 + max(len(wrapped[r * 3 + k]) for k in range(3)) * 26 + 14 for r in range(2)]
    h = y0 + sum(row_h) + 28
    pd, back, front, pcss = panel(c, W, h, "III", "STACK", glow=(0.85, 0.0))
    hl = otext(reg, "Tools of the trade.", MX, 136, 38, c["ink"])
    out, spots = [], []
    ys = [y0, y0 + row_h[0]]
    out.append(f'<line x1="{MX}" y1="{y0}" x2="{W-MX}" y2="{y0}" stroke="{c["line"]}"/>')
    out.append(f'<line x1="{MX}" y1="{ys[1]}" x2="{W-MX}" y2="{ys[1]}" stroke="{c["line"]}"/>')
    out.append(f'<line x1="{MX}" y1="{ys[1]+row_h[1]}" x2="{W-MX}" y2="{ys[1]+row_h[1]}" stroke="{c["line"]}"/>')
    for k in (1, 2):
        out.append(f'<line x1="{MX + k*CW}" y1="{y0}" x2="{MX + k*CW}" y2="{ys[1]+row_h[1]}" stroke="{c["line"]}"/>')
    for gi, (label, sub, items) in enumerate(STACK):
        r, col = divmod(gi, 3)
        cx, cy, rh = MX + col * CW, ys[r], row_h[r]
        gh = ghost(reg, roman(gi + 1), cx + CW - PAD, cy + 64, 44, c, anchor="end", sw=.9, op=.38, comet=False)
        out.append(gh["svg"])
        out.append(stext(label, cx + PAD, cy + 38, 12, c["ink"], weight=700, tracking=3))
        out.append(stext(sub, cx + PAD, cy + 58, 12, c["text3"], tracking=.5))
        for li, line in enumerate(wrapped[gi]):
            spans = ""
            for ii, it in enumerate(line):
                primary = (li == 0 and ii == 0)
                if ii:
                    spans += f'<tspan dx="14" fill="{c["text3"]}">·</tspan><tspan dx="14"'
                else:
                    spans += "<tspan"
                spans += f' fill="{c["accent"] if primary else c["ink"]}" font-weight="{700 if primary else 500}">{esc(it)}</tspan>'
            out.append(f'<text x="{cx + PAD}" y="{cy + 96 + li * 26}" font-family="{SANS}" font-size="13">{spans}</text>')
        spots.append(f'<g opacity="0" class="spot" style="animation-delay:{gi * 2}s"><rect x="{cx+.5}" y="{cy+.5}" width="{CW-1}" height="{rh-1}" fill="{c["accent"]}" fill-opacity=".07"/>'
                     f'<rect x="{cx}" y="{cy-.5}" width="{CW}" height="2" fill="{c["accent"]}"/></g>')
    css = pcss + ("@keyframes spot{0%{opacity:0}4%{opacity:1}15%{opacity:1}20%{opacity:0}100%{opacity:0}}"
                  ".spot{animation:spot 12s linear infinite}")
    body = f'{back}{front}{hl["svg"]}{"".join(spots)}{"".join(out)}'
    return _assemble(h, "Stack — Flutter, Node.js, PostgreSQL, React, TypeScript, Docker", reg, css, pd, body)


# ═══════════════════════════════════ CONTACT ═══════════════════════════════════
def contact(c):
    h = 350
    reg = Glyphs()
    pd, back, front, pcss = panel(c, W, h, "IV", "CONTACT", glow=(0.88, 0.45), glow_r=0.6)
    hl = otext(reg, "Let’s build something lasting.", MX, 136, 38, c["ink"])
    em = otext(reg, EMAIL, MX, 216, 44, "url(#ag)")
    bx, by = 864, 172
    rings = "".join(f'<rect x="{bx-20}" y="{by-20}" width="40" height="40" fill="none" stroke="{c["accent"]}" '
                    f'style="transform-box:fill-box;transform-origin:center;animation:bring 4.5s ease-out {-i * 1.5}s infinite" opacity="0"/>' for i in range(3))
    beacon = (f'{rings}<rect x="{bx-34}" y="{by-34}" width="68" height="68" fill="none" stroke="{c["accent"]}" stroke-opacity=".35" stroke-dasharray="2 6" '
              f'style="transform-box:fill-box;transform-origin:center;animation:spin 24s linear infinite"/>'
              f'{diamond(bx, by, 6, c["accent_hi"], fill=c["accent_hi"])}')
    TL, ty = 1240, 309
    txt = (f'<tspan fill="{c["accent"]}" font-weight="700">AVAILABLE FOR OPPORTUNITIES</tspan>'
           f'<tspan fill="{c["text3"]}"> · </tspan>FLUTTER<tspan fill="{c["text3"]}"> · </tspan>NODE.JS<tspan fill="{c["text3"]}"> · </tspan>REACT'
           f'<tspan fill="{c["text3"]}"> · </tspan>TYPESCRIPT<tspan fill="{c["text3"]}"> · </tspan>POSTGRESQL<tspan fill="{c["text3"]}"> · </tspan>DOCKER<tspan fill="{c["text3"]}"> · </tspan>')
    tk = "".join(f'<text x="{MX + k*TL}" y="{ty}" textLength="{TL}" lengthAdjust="spacing" font-family="{SANS}" font-size="12" '
                 f'font-weight="600" letter-spacing="3" fill="{c["text2"]}">{txt}</text>' for k in range(2))
    defs = pd + (f'<linearGradient id="tkf" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset=".07" stop-color="#fff"/>'
                 f'<stop offset=".93" stop-color="#fff"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>'
                 f'<mask id="tkm"><rect x="{MX}" y="286" width="{W-2*MX}" height="36" fill="url(#tkf)"/></mask>')
    css = pcss + ("@keyframes bring{0%{transform:rotate(45deg) scale(.45);opacity:.9}100%{transform:rotate(45deg) scale(3.4);opacity:0}}"
                  "@keyframes spin{to{transform:rotate(360deg)}}"
                  f"@keyframes tick{{to{{transform:translateX(-{TL}px)}}}}.tick{{animation:tick 32s linear infinite}}")
    body = f'''{back}{front}
{motes(c, 8, 33, (720, 960), (80, 260))}
{hl["svg"]}{beacon}
{em["svg"]}
<rect class="blink" x="{MX + em['width'] + 12}" y="184" width="3" height="36" fill="{c['accent']}"/>
{glint(c, "em", MX, MX + em["width"], 240, dur=5.2, length=190)}
{stext("REPLY TIME — USUALLY WITHIN A DAY", MX, 266, 11.5, c["text3"], weight=500, tracking=3.2)}
<line x1="{MX}" y1="286" x2="{W-MX}" y2="286" stroke="{c['line']}"/><line x1="{MX}" y1="322" x2="{W-MX}" y2="322" stroke="{c['line']}"/>
<g mask="url(#tkm)"><g class="tick">{tk}</g></g>'''
    return _assemble(h, f"Contact — {EMAIL}", reg, css, defs, body)


# ═══════════════════════════════════ SOUNDTRACK ═══════════════════════════════════
def soundtrack(c, track="We Do What We Want (Edit)", artist="Alan Fitzpatrick"):
    h = 212
    reg = Glyphs()
    pd, back, _, pcss = panel(c, W, h, glow=(0.12, 0.5), glow_r=0.7)
    cx, cy, VR, RB = 150, 106, 44, 56
    rnd = random.Random(4)
    bars = []
    N = 60
    for i in range(N):
        a = i * 360 / N
        dur, dl = rnd.uniform(.55, 1.5), -rnd.uniform(0, 1.5)
        bars.append(f'<g transform="rotate({a:.2f} {cx} {cy})"><rect class="eq" x="{cx-1}" y="{cy-RB-22}" width="2" height="22" '
                    f'style="animation-duration:{dur:.2f}s;animation-delay:{dl:.2f}s"/></g>')
    grooves = "".join(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#fff" stroke-opacity="{.07 if r % 6 else .14}" stroke-width=".7"/>' for r in range(19, VR - 1, 3))
    vinyl = f'''<g><circle cx="{cx}" cy="{cy}" r="{VR}" fill="{c['vinyl']}" stroke="{c['accent']}" stroke-opacity=".5"/>{grooves}
<circle cx="{cx}" cy="{cy}" r="15" fill="url(#ag)"/><circle cx="{cx}" cy="{cy-7}" r="1.6" fill="{c['bg']}" fill-opacity=".6"/><circle cx="{cx}" cy="{cy}" r="2.6" fill="{c['vinyl']}"/>
<path d="M{cx} {cy} L{cx+VR*.9:.1f} {cy-VR*.4:.1f} A{VR} {VR} 0 0 0 {cx+VR*.4:.1f} {cy-VR*.9:.1f}Z" fill="#fff" fill-opacity=".06"/>
<path d="M{cx} {cy} L{cx-VR*.9:.1f} {cy+VR*.4:.1f} A{VR} {VR} 0 0 0 {cx-VR*.4:.1f} {cy+VR*.9:.1f}Z" fill="#fff" fill-opacity=".06"/>
<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="8s" repeatCount="indefinite"/></g>'''
    tx = 292
    ttl = otext(reg, track, tx, 122, 30, c["ink"])
    bw = 230
    bxp = W - MX - bw
    btn = (f'<rect x="{bxp}" y="40" width="{bw}" height="36" fill="none" stroke="{c["accent"]}"/>'
           f'<rect x="{bxp}" y="40" width="{bw}" height="36" fill="{c["accent"]}" opacity="0"><animate attributeName="opacity" values="0;.12;0" dur="3.2s" repeatCount="indefinite"/></rect>'
           + stext("LISTEN ON SPOTIFY", bxp + 20, 63, 11.5, c["accent"], weight=700, tracking=3)
           + f'<g><path d="M{bxp+bw-38} 58h16m-6-6l6 6l-6 6" fill="none" stroke="{c["accent"]}" stroke-width="1.6"/>'
             f'<animateTransform attributeName="transform" type="translate" values="0 0;5 0;0 0" dur="1.6s" repeatCount="indefinite"/></g>')
    py = 182
    prog = (f'<line x1="{tx}" y1="{py}" x2="{W-MX}" y2="{py}" stroke="{c["line"]}"/>'
            f'<line x1="{tx}" y1="{py}" x2="{tx}" y2="{py}" stroke="{c["accent"]}" stroke-width="2"><animate attributeName="x2" values="{tx};{W-MX}" dur="40s" repeatCount="indefinite"/></line>'
            f'<rect x="{tx-4}" y="{py-4}" width="8" height="8" fill="{c["accent_hi"]}" transform="rotate(45 {tx} {py})"><animate attributeName="x" values="{tx-4};{W-MX-4}" dur="40s" repeatCount="indefinite"/></rect>')
    css = pcss + ("@keyframes eq{from{transform:scaleY(.12)}to{transform:scaleY(1)}}"
                  ".eq{transform-box:fill-box;transform-origin:center bottom;animation:eq 1s ease-in-out infinite alternate}")
    body = f'''{back}
<circle cx="{cx}" cy="{cy}" r="{RB-5}" fill="none" stroke="{c['accent']}" stroke-opacity=".25"/>
<g fill="{c['accent']}" fill-opacity=".9">{"".join(bars)}</g>{vinyl}
<rect x="{tx}" y="56" width="7" height="7" fill="{c['accent']}"><animate attributeName="opacity" values="1;.25;1" dur="2s" repeatCount="indefinite"/></rect>
{stext("NOW PLAYING", tx + 20, 64, 12, c["accent"], weight=700, tracking=4)}
{btn}
{ttl["svg"]}
{stext(artist.upper(), tx, 150, 12.5, c["text2"], weight=500, tracking=4.2)}
{prog}'''
    return _assemble(h, f"Soundtrack — {track} by {artist}", reg, css, pd, body)


# ═══════════════════════════════════ FOOTER ═══════════════════════════════════
def footer(c):
    h = 240
    reg = Glyphs()
    pd, back, _, pcss = panel(c, W, h, glow=(0.5, 1.0), glow_r=0.8)
    wm = ghost(reg, "JAVOHIR ABDUVAHHOBOV", W / 2, 128, 60, c, anchor="middle", tracking=4, sw=1.0, op=.55, dur=10, stagger=.5)
    body = f'''{back}
{motes(c, 18, 5, (60, 940), (60, 200))}
{glint(c, "ft", MX, W - MX, 52, dur=8, delay=2)}
{wm["svg"]}
{glint(c, "fb", MX, W - MX, 160, dur=8, delay=6)}
{stext("THANK YOU FOR VISITING", W / 2, 192, 12, c["ink"], anchor="middle", weight=600, tracking=6)}
{stext("CRAFTED WITH INTENT  ·  MMXXVI", W / 2, 214, 11, c["text3"], anchor="middle", weight=500, tracking=4.4)}'''
    return _assemble(h, "Thank you for visiting", reg, pcss, pd, body)


# ═══════════════════════════════════ DIVIDER ═══════════════════════════════════
def divider(c):
    h, cx, cy = 28, W / 2, 14
    reg = Glyphs()
    sq = "".join(f'<rect x="{cx - 17 + i * 12}" y="{cy - 3}" width="6" height="6" fill="{c["accent"]}" opacity=".25" style="animation:seq 1.8s linear {i * .3}s infinite"/>' for i in range(3))
    css = "@keyframes seq{0%,100%{opacity:.2}20%{opacity:1}45%{opacity:.2}}"
    body = (glint(c, "dl", MX, cx - 34, cy, dur=7, delay=0, length=120)
            + glint(c, "dr", cx + 34, W - MX, cy, dur=7, delay=3.5, length=120) + sq)
    return _assemble(h, "", reg, css, "", body).replace(' role="img" aria-label=""', ' aria-hidden="true"')
