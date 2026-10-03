# -*- coding: utf-8 -*-
"""The eight panels of the profile. Each builder takes a palette `c` and returns an SVG string."""
import math
import random

from common import (W, MX, SANS, BASE_CSS, Glyphs, otext, stext, esc, svg_open, frame, diamond,
                    glint, dust, section_header, gold_gradient)

ROLES = ["FLUTTER DEVELOPER", "NODE.JS BACKEND ENGINEER", "REACT & TYPESCRIPT DEVELOPER", "SOFTWARE ENGINEER"]
EMAIL = "javohirabduvahhobov@gmail.com"
SPOTIFY = "https://open.spotify.com/track/2qGvgsRsmrB0Y7Y4MmuP1M"


def _assemble(h, title, reg, css, defs, body):
    return (f'{svg_open(h, title)}\n<defs>\n{reg.defs()}\n{defs}\n</defs>\n<style>\n{BASE_CSS}\n{css}\n</style>\n{body}\n</svg>')


def _rise(base, step, dur=1.4):
    return lambda i, ch: f"animation:rise {dur}s cubic-bezier(.16,.84,.3,1) {base + i * step:.2f}s both"


# ═════════════════════════════════ HERO ═════════════════════════════════
def _dial(c, cx, cy, R):
    """Engine-turned watch dial: counter-rotating guilloché, bezel, sweeping seconds hand."""
    g = []
    inner = R - 30

    def rosette(n, r, off, op, sw=0.55):
        cs = "".join(
            f'<circle cx="{cx + off * math.cos(2 * math.pi * i / n):.2f}" cy="{cy + off * math.sin(2 * math.pi * i / n):.2f}" r="{r}"/>'
            for i in range(n))
        return f'<g fill="none" stroke="{c["gold"]}" stroke-width="{sw}" stroke-opacity="{op}">{cs}</g>'

    spin = lambda a, d: (f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" '
                         f'to="{a} {cx} {cy}" dur="{d}s" repeatCount="indefinite"/>')
    g.append(f'<clipPath id="dialclip"><circle cx="{cx}" cy="{cy}" r="{inner}"/></clipPath>')
    g.append(f'<g clip-path="url(#dialclip)">'
             f'<g>{rosette(56, 74, 48, .42)}{spin(360, 90)}</g>'
             f'<g>{rosette(44, 52, 66, .36)}{spin(-360, 120)}</g>'
             f'{rosette(84, 20, 104, .5)}</g>')
    # bezel rings
    g.append(f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{c["gold"]}" stroke-opacity=".75"/>'
             f'<circle cx="{cx}" cy="{cy}" r="{R-5}" fill="none" stroke="{c["gold"]}" stroke-opacity=".28"/>'
             f'<circle cx="{cx}" cy="{cy}" r="{inner}" fill="none" stroke="{c["gold"]}" stroke-opacity=".35"/>')
    # minute track
    minor, major = [], []
    for i in range(60):
        a = math.radians(i * 6 - 90)
        r1, r2 = (R - 22, R - 11) if i % 5 == 0 else (R - 15, R - 11)
        seg = f"M{cx + r1 * math.cos(a):.2f} {cy + r1 * math.sin(a):.2f}L{cx + r2 * math.cos(a):.2f} {cy + r2 * math.sin(a):.2f}"
        (major if i % 5 == 0 else minor).append(seg)
    g.append(f'<path d="{"".join(minor)}" stroke="{c["gold"]}" stroke-opacity=".55" stroke-width=".8" fill="none"/>'
             f'<path d="{"".join(major)}" stroke="{c["gold_hi"]}" stroke-width="1.6" fill="none"/>')
    g.append(diamond(cx, cy - R + 5, 3.2, c["gold_hi"], fill=c["gold_hi"]))
    # comet arcs orbiting the bezel
    rr = R + 9
    circ = 2 * math.pi * rr
    for seg, dur, op, direction in [(150, 26, .95, 1), (60, 26, .45, 1)]:
        off = 0 if seg == 150 else circ / 2
        g.append(f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="none" stroke="{c["gold_hi"]}" stroke-width="1.3" '
                 f'stroke-linecap="round" stroke-opacity="{op}" stroke-dasharray="{seg} {circ:.1f}" '
                 f'transform="rotate({off / circ * 360:.1f} {cx} {cy})">'
                 f'<animateTransform attributeName="transform" type="rotate" from="{off / circ * 360:.1f} {cx} {cy}" '
                 f'to="{off / circ * 360 + 360 * direction:.1f} {cx} {cy}" dur="{dur}s" repeatCount="indefinite"/></circle>')
    # seconds hand — emerges from beneath the centre disc
    g.append(f'<g><line x1="{cx}" y1="{cy + 26}" x2="{cx}" y2="{cy - R + 24}" stroke="{c["gold_hi"]}" stroke-width="1.2"/>'
             f'<circle cx="{cx}" cy="{cy - R + 62}" r="4.2" fill="none" stroke="{c["gold_hi"]}" stroke-width="1.2"/>'
             f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="60s" repeatCount="indefinite"/></g>')
    # centre disc + monogram (added by caller for glyph registry)
    g.append(f'<circle cx="{cx}" cy="{cy}" r="46" fill="{c["bg"]}" stroke="{c["gold"]}" stroke-opacity=".85"/>'
             f'<circle cx="{cx}" cy="{cy}" r="41" fill="none" stroke="{c["gold"]}" stroke-opacity=".3"/>')
    return "".join(g)


def hero(c):
    h = 450
    reg = Glyphs()
    cx, cy, R = 810, 202, 152
    fdefs, fbody = frame(c, W, h, glow=(0.81, 0.45), glow_r=0.55)

    n1 = otext(reg, "JAVOHIR", MX, 184, 48, c["ink"], tracking=7, anim=_rise(.25, .07))
    n2 = otext(reg, "ABDUVAHHOBOV", MX, 246, 48, c["ink"], tracking=7, anim=_rise(.7, .06))
    assert n2["x0"] + n2["width"] < cx - R - 24, "name collides with dial"
    mono = otext(reg, "JA", cx + 1.5, cy + 11, 31, "url(#gold)", anchor="middle", tracking=3)

    rule_w = 168
    roles = []
    css_roles = ("@keyframes role{0%{opacity:0;transform:translateX(12px)}4%{opacity:1;transform:translateX(0)}"
                 "22%{opacity:1;transform:translateX(0)}27%{opacity:0;transform:translateX(-10px)}100%{opacity:0}}")
    for i, r in enumerate(ROLES):
        roles.append(stext(r, MX + 38, 327, 13, c["gold"], weight=600, tracking=4, opacity=1 if i == 0 else 0,
                           extra=f'style="animation:role 14s linear {i * 3.5 + 1.6}s infinite"'))

    css = css_roles + f'''
@keyframes draw{{from{{stroke-dashoffset:{rule_w}}}to{{stroke-dashoffset:0}}}}
@keyframes sheen{{0%{{transform:translateX(0)}}34%{{transform:translateX(1050px)}}100%{{transform:translateX(1050px)}}}}
.sheen{{animation:sheen 10s cubic-bezier(.45,0,.3,1) 3.4s infinite}}
.drawn{{stroke-dasharray:{rule_w};animation:draw 1.5s cubic-bezier(.5,0,.2,1) 1.1s both}}
.pulse{{animation:pulse 2.8s ease-out infinite}}
@keyframes pulse{{0%{{r:3;opacity:.9}}100%{{r:14;opacity:0}}}}'''

    defs = f'''{fdefs}
<clipPath id="nameclip">{n1["clip"]}{n2["clip"]}</clipPath>
<linearGradient id="sheeng" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{c['gold_hi']}" stop-opacity="0"/><stop offset=".5" stop-color="{c['gold_hi']}" stop-opacity="1"/><stop offset="1" stop-color="{c['gold_hi']}" stop-opacity="0"/></linearGradient>'''

    body = f'''{fbody}
{dust(c, 26, W, h, 7, x_range=(30, 960), y_range=(40, 400), opacity=.75)}
<g style="animation:fade 2.6s ease-out .2s both">{_dial(c, cx, cy, R)}{mono["svg"]}</g>

<line x1="{MX}" y1="93" x2="{MX+26}" y2="93" stroke="{c['gold']}" style="stroke-dasharray:26;animation:draw 1s ease-out .3s both"/>
{stext("FULL-STACK & MOBILE ENGINEER", MX + 42, 97, 12, c["text2"], weight=500, tracking=4.4, extra='style="animation:fade 1.2s ease-out .5s both"')}

{n1["svg"]}{n2["svg"]}
<g clip-path="url(#nameclip)"><g transform="skewX(-18)"><rect class="sheen" x="-260" y="100" width="170" height="180" fill="url(#sheeng)"/></g></g>

<line class="drawn" x1="{MX}" y1="284" x2="{MX+rule_w}" y2="284" stroke="{c['gold']}" stroke-width="1.2"/>
<g style="animation:fade 1s ease-out 2.3s both">{diamond(MX + rule_w + 14, 284, 3.4, c["gold_hi"], fill=c["gold_hi"])}</g>

<line x1="{MX}" y1="322" x2="{MX+24}" y2="322" stroke="{c['gold']}" stroke-opacity=".7"/>
{"".join(roles)}

<line x1="{MX}" y1="386" x2="{W-MX}" y2="386" stroke="{c['line']}"/>
<circle cx="{MX+3}" cy="414" r="3" fill="{c['gold']}"/>
<circle class="pulse" cx="{MX+3}" cy="414" r="3" fill="none" stroke="{c['gold']}"/>
{stext("AVAILABLE FOR OPPORTUNITIES", MX + 18, 418, 12, c["text2"], weight=500, tracking=3.6)}
{stext("BSc SOFTWARE ENGINEERING", W - MX, 418, 12, c["text3"], anchor="end", weight=500, tracking=3.6)}'''
    return _assemble(h, "Javohir Abduvahhobov — Full-stack & Mobile Engineer", reg, css, defs, body)


# ═════════════════════════════════ PROFILE ═════════════════════════════════
def profile(c):
    h = 306
    reg = Glyphs()
    fdefs, fbody = frame(c, W, h, glow=(0.15, 0.0), glow_r=0.9)
    head = section_header(c, reg, "I", "PROFILE")
    hl = otext(reg, "One engineer. The whole pipeline.", MX, 150, 36, c["ink"])
    lines = ["Full-stack and mobile engineer who ships the entire pipeline —",
             "Flutter on the client, a Node.js / Express REST API in the middle,",
             "PostgreSQL underneath, and a lightweight admin panel wired to it all."]
    para = "".join(stext(t, MX, 200 + i * 27, 15.5, c["text2"]) for i, t in enumerate(lines))
    creds = [("DEGREE", "BSc Software Engineering"), ("DISCIPLINES", "Mobile · Backend · DB · Admin"),
             ("STATUS", "Open to opportunities")]
    cx_ = 704
    items = []
    for i, (lab, val) in enumerate(creds):
        y = 128 + i * 62
        lx = cx_ + (16 if lab == "STATUS" else 0)
        items.append(stext(lab, lx, y, 11.5, c["text3"], weight=600, tracking=3.6))
        items.append(otext(reg, val, cx_, y + 28, 19.5, c["ink"], max_w=224)["svg"])
    pulse = (f'<circle cx="{cx_+3}" cy="{128+124-4}" r="3" fill="{c["gold"]}"/>'
             f'<circle cx="{cx_+3}" cy="{128+124-4}" r="3" fill="none" stroke="{c["gold"]}"><animate attributeName="r" values="3;13" dur="2.8s" repeatCount="indefinite"/>'
             f'<animate attributeName="opacity" values=".9;0" dur="2.8s" repeatCount="indefinite"/></circle>')
    body = f'''{fbody}
{head}
{hl["svg"]}
{para}
{glint(c, "vr", 668, 268, 98, dur=6.5, vertical=True, length=90)}
{"".join(items)}{pulse}'''
    return _assemble(h, "Profile — one engineer, the whole pipeline", reg, "", fdefs, body)


# ═════════════════════════════════ ARCHITECTURE ═════════════════════════════════
def ecosystem(c):
    h = 490
    reg = Glyphs()
    fdefs, fbody = frame(c, W, h, glow=(0.5, 0.0), glow_r=0.9)
    head = section_header(c, reg, "II", "ARCHITECTURE")
    hl = otext(reg, "System, end to end.", MX, 136, 36, c["ink"])
    NW, NH, ny = 216, 84, 214
    nodes = [("01", "FLUTTER APP", "Dart · http · file_picker", 72, ny),
             ("02", "EXPRESS API", "JWT · bcryptjs · multer", 392, ny),
             ("03", "POSTGRESQL", "users · jobs · interviews", 712, ny),
             ("04", "ADMIN PANEL", "HTML · CSS · JavaScript", 392, 350)]
    nsvg = []
    for k, (idx, title, sub, x, y) in enumerate(nodes):
        t = otext(reg, title, x + NW / 2, y + 50, 15.5, c["ink"], anchor="middle", tracking=3)
        nsvg.append(f'''<g>
<rect x="{x}" y="{y}" width="{NW}" height="{NH}" fill="{c['node']}" stroke="{c['gold']}" stroke-opacity=".38"/>
<rect x="{x+.5}" y="{y+.5}" width="{NW-1}" height="{NH-1}" fill="none" stroke="{c['gold_hi']}" stroke-width="1.6" pathLength="100" stroke-dasharray="9 91" style="animation:scan 9s linear {-k*2.2:.1f}s infinite"/>
{stext(idx, x + 14, y + 23, 11, c["gold"], weight=600, tracking=2)}
{t["svg"]}
{stext(sub, x + NW / 2, y + 70, 12.5, c["text3"], anchor="middle", tracking=.4)}
</g>''')
    # docker enclosure
    dock = (f'<rect x="368" y="176" width="584" height="284" fill="none" stroke="{c["gold"]}" stroke-opacity=".32" stroke-dasharray="2 6"/>'
            f'{stext("DOCKERIZED", 392, 199, 11.5, c["text3"], weight=600, tracking=4)}')
    paths = {"f1": "M288 256H392", "f2": "M608 256H712", "f3": "M500 298V350"}
    flows = []
    for pid, d in paths.items():
        flows.append(f'<path id="{pid}" d="{d}" fill="none" stroke="{c["gold"]}" stroke-opacity=".35"/>'
                     f'<path d="{d}" fill="none" stroke="{c["gold_hi"]}" stroke-width="1.4" stroke-dasharray="3 7" stroke-opacity=".9">'
                     f'<animate attributeName="stroke-dashoffset" from="20" to="0" dur="1.4s" repeatCount="indefinite"/></path>')
    arrows = (f'<path d="M386 251.5L394 256L386 260.5Z" fill="{c["gold_hi"]}"/>'
              f'<path d="M706 251.5L714 256L706 260.5Z" fill="{c["gold_hi"]}"/>'
              f'<path d="M495.5 344L500 352L504.5 344Z" fill="{c["gold_hi"]}"/>')

    def bead(pid, dur, begin, rev=False):
        kp = ' keyPoints="1;0" keyTimes="0;1" calcMode="linear"' if rev else ""
        return (f'<circle r="3.4" fill="{c["gold_hi"]}" filter="url(#bglow)"><animateMotion dur="{dur}s" begin="{begin}s" '
                f'repeatCount="indefinite" rotate="0"{kp}><mpath xlink:href="#{pid}"/></animateMotion></circle>')

    beads = (bead("f1", 2.6, 0) + bead("f2", 2.6, .5) + bead("f2", 2.6, 1.8, True) + bead("f3", 2.2, 1.0) + bead("f3", 2.2, 2.1, True))
    labels = (stext("JWT", 340, 242, 11, c["text3"], anchor="middle", weight=600, tracking=2.5)
              + stext("pg", 660, 242, 11, c["text3"], anchor="middle", weight=600, tracking=2.5)
              + stext("REST", 514, 328, 11, c["text3"], weight=600, tracking=2.5))
    defs = (fdefs + '<filter id="bglow" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="2" result="b"/>'
            '<feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>')
    css = "@keyframes scan{to{stroke-dashoffset:-100}}"
    body = f'''{fbody}
{head}
{hl["svg"]}
{dock}
{"".join(flows)}{arrows}
{"".join(nsvg)}
{labels}
{beads}'''
    return _assemble(h, "Architecture — Flutter, Express API, PostgreSQL, admin panel, Docker", reg, css, defs, body)


# ═════════════════════════════════ STACK ═════════════════════════════════
STACK = [
    ("MOBILE", "Flutter app", ["Flutter", "Dart", "http", "shared_preferences", "file_picker", "google_fonts", "intl", "cupertino_icons"]),
    ("BACKEND", "Node.js API", ["Node.js", "Express", "JWT", "bcryptjs", "multer", "cors", "morgan", "dotenv", "uuid", "pg"]),
    ("DATABASE", "Relational", ["PostgreSQL"]),
    ("ADMIN PANEL", "Lightweight web", ["HTML", "CSS", "JavaScript"]),
    ("FRONTEND & OTHER", "Languages", ["React", "TypeScript", "Python"]),
    ("TOOLING", "Dev workflow", ["npm", "Git", "GitHub", "Docker"]),
]


def stack(c):
    reg = Glyphs()
    x0, x1, ch, gx, gy = 300, W - MX, 28, 8, 8
    rows, y = [], 178
    chips_all = []
    for gi, (label, sub, items) in enumerate(STACK):
        cx_, cy_, lines = x0, 0, 1
        placed = []
        for ii, it in enumerate(items):
            w = round(len(it) * 7.1 + 28)
            if cx_ + w > x1:
                cx_, lines = x0, lines + 1
            placed.append((it, cx_, lines - 1, w, ii == 0))
            cx_ += w + gx
        block_h = 26 + lines * ch + (lines - 1) * gy
        rows.append((gi, label, sub, placed, y, block_h))
        y += block_h + 14
    h = y + 24
    fdefs, fbody = frame(c, W, h, glow=(0.85, 0.0), glow_r=0.8)
    head = section_header(c, reg, "III", "STACK")
    hl = otext(reg, "Tools of the trade.", MX, 136, 36, c["ink"])
    out, clip = [], []
    for gi, label, sub, placed, ry, bh in rows:
        if gi:
            out.append(f'<line x1="{MX}" y1="{ry-7}" x2="{x1}" y2="{ry-7}" stroke="{c["line"]}"/>')
        num = otext(reg, f"{gi+1:02d}", MX, ry + 30, 18, "url(#gold)")
        out.append(num["svg"])
        out.append(stext(label, MX + 42, ry + 17, 12, c["ink"], weight=600, tracking=3))
        out.append(stext(sub, MX + 42, ry + 35, 12, c["text3"], tracking=.5))
        for it, px, line, w, primary in placed:
            py = ry + 10 + line * (ch + gy)
            stroke = c["gold"] if primary else c["line"]
            sop = ".75" if primary else "1"
            out.append(f'<rect x="{px}" y="{py}" width="{w}" height="{ch}" fill="{c["node"]}" stroke="{stroke}" stroke-opacity="{sop}"/>')
            out.append(stext(it, px + w / 2, py + 18.2, 12.5, c["gold"] if primary else c["ink"], anchor="middle", weight=600 if primary else 500, tracking=.2))
            clip.append(f'<rect x="{px}" y="{py}" width="{w}" height="{ch}"/>')
    css = "@keyframes wash{0%{transform:translateX(0)}45%{transform:translateX(1150px)}100%{transform:translateX(1150px)}}.wash{animation:wash 9s cubic-bezier(.45,0,.3,1) 1s infinite}"
    defs = (fdefs + f'<clipPath id="chipclip">{"".join(clip)}</clipPath>'
            f'<linearGradient id="washg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{c["gold_hi"]}" stop-opacity="0"/>'
            f'<stop offset=".5" stop-color="{c["gold_hi"]}" stop-opacity="{.30 if c["name"]=="dark" else .42}"/><stop offset="1" stop-color="{c["gold_hi"]}" stop-opacity="0"/></linearGradient>')
    body = f'''{fbody}
{head}
{hl["svg"]}
{"".join(out)}
<g clip-path="url(#chipclip)"><g transform="skewX(-18)"><rect class="wash" x="-300" y="150" width="190" height="{h-150}" fill="url(#washg)"/></g></g>'''
    return _assemble(h, "Stack — Flutter, Node.js, PostgreSQL, React, TypeScript, Docker", reg, css, defs, body)


# ═════════════════════════════════ CONTACT ═════════════════════════════════
def contact(c):
    h = 312
    reg = Glyphs()
    fdefs, fbody = frame(c, W, h, glow=(0.85, 0.5), glow_r=0.7)
    head = section_header(c, reg, "IV", "CONTACT")
    hl = otext(reg, "Let’s build something lasting.", MX, 138, 36, c["ink"])
    em = otext(reg, EMAIL, MX, 216, 40, "url(#gold)")
    rx, ry = 840, 176
    rings = "".join(
        f'<circle cx="{rx}" cy="{ry}" r="8" fill="none" stroke="{c["gold"]}" stroke-width="1">'
        f'<animate attributeName="r" values="8;86" dur="5.4s" begin="{-i*1.8}s" repeatCount="indefinite"/>'
        f'<animate attributeName="opacity" values=".8;0" dur="5.4s" begin="{-i*1.8}s" repeatCount="indefinite"/></circle>'
        for i in range(3))
    sig = f'{rings}{diamond(rx, ry, 5, c["gold_hi"], fill=c["gold_hi"])}<circle cx="{rx}" cy="{ry}" r="22" fill="none" stroke="{c["gold"]}" stroke-opacity=".35" stroke-dasharray="2 5"><animateTransform attributeName="transform" type="rotate" from="0 {rx} {ry}" to="360 {rx} {ry}" dur="30s" repeatCount="indefinite"/></circle>'
    body = f'''{fbody}
{dust(c, 9, W, h, 33, x_range=(720, 960), y_range=(90, 290), opacity=.55)}
{head}
{hl["svg"]}
{sig}
{em["svg"]}
{glint(c, "em", MX, MX + em["width"], 238, dur=5.2, length=170)}
<circle cx="{MX+3}" cy="276" r="3" fill="{c['gold']}"/>
<circle cx="{MX+3}" cy="276" r="3" fill="none" stroke="{c['gold']}"><animate attributeName="r" values="3;14" dur="2.8s" repeatCount="indefinite"/><animate attributeName="opacity" values=".9;0" dur="2.8s" repeatCount="indefinite"/></circle>
{stext("AVAILABLE FOR OPPORTUNITIES", MX + 18, 280, 12, c["text2"], weight=500, tracking=3.6)}
{stext("REPLY TIME — USUALLY UNDER 24 HOURS", W - MX, 280, 12, c["text3"], anchor="end", weight=500, tracking=3.2)}'''
    return _assemble(h, f"Contact — {EMAIL}", reg, "", fdefs, body)


# ═════════════════════════════════ SOUNDTRACK ═════════════════════════════════
def soundtrack(c, track="We Do What We Want (Edit)", artist="Alan Fitzpatrick"):
    h = 200
    reg = Glyphs()
    fdefs, fbody = frame(c, W, h, glow=(0.12, 0.5), glow_r=0.7)
    vx, vy, VR = 150, 100, 64
    grooves = "".join(f'<circle cx="{vx}" cy="{vy}" r="{r}" fill="none" stroke="#ffffff" stroke-opacity="{.07 if r%8 else .13}" stroke-width=".7"/>' for r in range(24, VR - 2, 3))
    vinyl = f'''<g><circle cx="{vx}" cy="{vy}" r="{VR}" fill="{c['vinyl']}" stroke="{c['gold']}" stroke-opacity=".55"/>{grooves}
<circle cx="{vx}" cy="{vy}" r="22" fill="url(#gold)"/><circle cx="{vx}" cy="{vy}" r="17" fill="none" stroke="{c['bg']}" stroke-opacity=".35" stroke-width=".8"/>
<path d="M{vx} {vy-22}A22 22 0 0 1 {vx} {vy+22}" fill="none"/>
<circle cx="{vx}" cy="{vy-10}" r="1.8" fill="{c['bg']}" fill-opacity=".55"/>
<circle cx="{vx}" cy="{vy}" r="3" fill="{c['vinyl']}"/>
<animateTransform attributeName="transform" type="rotate" from="0 {vx} {vy}" to="360 {vx} {vy}" dur="7s" repeatCount="indefinite"/></g>
<path d="M{vx} {vy} L{vx+VR*.85:.1f} {vy-VR*.5:.1f} A{VR} {VR} 0 0 0 {vx+VR*.5:.1f} {vy-VR*.85:.1f}Z" fill="#fff" fill-opacity=".05"/>
<path d="M{vx} {vy} L{vx-VR*.85:.1f} {vy+VR*.5:.1f} A{VR} {VR} 0 0 0 {vx-VR*.5:.1f} {vy+VR*.85:.1f}Z" fill="#fff" fill-opacity=".05"/>'''
    px, py = 262, 40
    arm = f'''<g><circle cx="{px}" cy="{py}" r="8" fill="{c['node']}" stroke="{c['gold']}"/><circle cx="{px}" cy="{py}" r="2.4" fill="{c['gold']}"/>
<path d="M{px} {py}L{px-8} {py+66}L{vx+52} {vy+30}" fill="none" stroke="{c['gold_hi']}" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round"/>
<rect x="{vx+44}" y="{vy+26}" width="14" height="6" rx="1" fill="{c['gold_hi']}" transform="rotate(-24 {vx+51} {vy+29})"/>
<animateTransform attributeName="transform" type="rotate" values="0 {px} {py};1.4 {px} {py};0 {px} {py};-0.8 {px} {py};0 {px} {py}" dur="9s" repeatCount="indefinite"/></g>'''
    tx = 330
    ttl = otext(reg, track, tx, 104, 25, c["ink"])
    # equalizer: thin vertical lines, mirrored around a baseline
    rnd = random.Random(11)
    bars, ex0, ey = [], 704, 108
    for i in range(23):
        x = ex0 + i * 9.8
        hh = rnd.uniform(12, 60) * (0.55 + 0.45 * math.sin(i / 22 * math.pi))
        d, dl = rnd.uniform(.7, 1.6), -rnd.uniform(0, 2)
        bars.append(f'<rect class="eq" x="{x:.1f}" y="{ey-hh/2:.1f}" width="2" height="{hh:.1f}" style="animation-duration:{d:.2f}s;animation-delay:{dl:.2f}s"/>')
    css = ("@keyframes eq{from{transform:scaleY(.18)}to{transform:scaleY(1)}}"
           ".eq{transform-box:fill-box;transform-origin:center;animation:eq 1s ease-in-out infinite alternate}")
    # progress line
    py2 = 160
    prog = f'''<line x1="{tx}" y1="{py2}" x2="{W-MX}" y2="{py2}" stroke="{c['line']}"/>
<line x1="{tx}" y1="{py2}" x2="{tx}" y2="{py2}" stroke="{c['gold']}" stroke-width="1.6"><animate attributeName="x2" values="{tx};{W-MX}" dur="38s" repeatCount="indefinite"/></line>
<circle cx="{tx}" cy="{py2}" r="3.4" fill="{c['gold_hi']}" filter="url(#bglow)"><animate attributeName="cx" values="{tx};{W-MX}" dur="38s" repeatCount="indefinite"/></circle>'''
    defs = fdefs + '<filter id="bglow" x="-200%" y="-200%" width="500%" height="500%"><feGaussianBlur stdDeviation="2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
    body = f'''{fbody}
{vinyl}{arm}
<circle cx="{tx+3}" cy="58" r="3" fill="{c['gold']}"><animate attributeName="opacity" values="1;.35;1" dur="2s" repeatCount="indefinite"/></circle>
{stext("NOW PLAYING", tx + 16, 62, 12, c["gold"], weight=600, tracking=4)}
{stext("LISTEN ON SPOTIFY  →", W - MX, 62, 12, c["text2"], anchor="end", weight=600, tracking=3.4)}
{ttl["svg"]}
{stext(artist.upper(), tx, 133, 12.5, c["text2"], weight=500, tracking=4.2)}
<g fill="{c['gold']}" fill-opacity=".85">{"".join(bars)}</g>
{prog}'''
    return _assemble(h, f"Soundtrack — {track} by {artist}", reg, css, defs, body)


# ═════════════════════════════════ FOOTER ═════════════════════════════════
def footer(c):
    h = 236
    reg = Glyphs()
    fdefs, fbody = frame(c, W, h, glow=(0.5, 1.0), glow_r=0.8)
    mx_, my_ = W / 2, 66
    mono = otext(reg, "JA", mx_ + 1, my_ + 7, 21, "url(#gold)", anchor="middle", tracking=2)
    crest = f'''<circle cx="{mx_}" cy="{my_}" r="27" fill="none" stroke="{c['gold']}" stroke-opacity=".8"/>
<circle cx="{mx_}" cy="{my_}" r="22" fill="none" stroke="{c['gold']}" stroke-opacity=".3"/>
<circle cx="{mx_}" cy="{my_}" r="27" fill="none" stroke="{c['gold_hi']}" stroke-width="1.5" stroke-linecap="round" stroke-dasharray="26 144">
<animateTransform attributeName="transform" type="rotate" from="0 {mx_} {my_}" to="360 {mx_} {my_}" dur="9s" repeatCount="indefinite"/></circle>{mono["svg"]}'''
    hl = otext(reg, "Thank you for visiting.", W / 2, 152, 32, c["ink"], anchor="middle")
    body = f'''{fbody}
{dust(c, 26, W, h, 5, x_range=(40, 960), y_range=(80, 130), opacity=.7)}
{glint(c, "fl", MX, mx_ - 46, my_, dur=6.4, length=140)}
{glint(c, "fr", mx_ + 46, W - MX, my_, dur=6.4, delay=3.2, length=140)}
{crest}
{hl["svg"]}
{stext("JAVOHIR ABDUVAHHOBOV  ·  MMXXVI", W / 2, 196, 12, c["text3"], anchor="middle", weight=500, tracking=5)}'''
    return _assemble(h, "Thank you for visiting", reg, "", fdefs, body)


# ═════════════════════════════════ DIVIDER ═════════════════════════════════
def divider(c):
    h = 34
    reg = Glyphs()
    cx_, cy_ = W / 2, h / 2
    defs = (f'<linearGradient id="fadeline" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{c["gold"]}" stop-opacity="0"/>'
            f'<stop offset=".5" stop-color="{c["gold"]}" stop-opacity=".7"/><stop offset="1" stop-color="{c["gold"]}" stop-opacity="0"/></linearGradient>'
            f'<clipPath id="dvc"><rect x="{MX}" y="0" width="{W-2*MX}" height="{h}"/></clipPath>'
            f'<linearGradient id="dvg" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{c["gold_hi"]}" stop-opacity="0"/><stop offset=".5" stop-color="{c["gold_hi"]}"/><stop offset="1" stop-color="{c["gold_hi"]}" stop-opacity="0"/></linearGradient>')
    body = f'''<line x1="{MX}" y1="{cy_}" x2="{cx_-26}" y2="{cy_}" stroke="url(#fadeline)"/>
<line x1="{cx_+26}" y1="{cy_}" x2="{W-MX}" y2="{cy_}" stroke="url(#fadeline)" transform="rotate(180 {(cx_+26+W-MX)/2} {cy_})"/>
<g clip-path="url(#dvc)"><rect x="{MX-200}" y="{cy_-.75}" width="200" height="1.5" fill="url(#dvg)"><animate attributeName="x" values="{MX-200};{W-MX};{W-MX}" keyTimes="0;.6;1" dur="8s" repeatCount="indefinite"/></rect></g>
{diamond(cx_ - 15, cy_, 2, c["gold"], fill=c["gold"])}{diamond(cx_ + 15, cy_, 2, c["gold"], fill=c["gold"])}
{diamond(cx_, cy_, 5, c["gold_hi"], bg=c["bg"], sw=1.2)}{diamond(cx_, cy_, 1.8, c["gold_hi"], fill=c["gold_hi"])}'''
    return _assemble(h, "", reg, "", defs, body).replace(' role="img" aria-label=""', ' aria-hidden="true"')
