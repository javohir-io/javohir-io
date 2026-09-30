# -*- coding: utf-8 -*-
import math
import typo
from kit import Ctx, frame, border, dust, sparkles, diamond, star4, fade_line, hair, W


def name_gradient(x, gid):
    c = x.c
    stops = "".join(f'<stop offset="{o}" stop-color="{col}"/>' for o, col in c["name_stops"])
    x.defs(f'<linearGradient id="{gid}" x1="0" y1="0" x2="1" y2="0">{stops}</linearGradient>')
    return f"url(#{gid})"


# ---------------------------------------------------------------------------
def divider_svg(c):
    x = Ctx(c, "dv", 34, title="divider")
    u, cx = x.uid, W / 2
    x.defs(f'<linearGradient id="sg{u}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{c["gold2"]}" stop-opacity="0"/>'
           f'<stop offset="0.5" stop-color="{c["gold2"]}" stop-opacity="1"/><stop offset="1" stop-color="{c["gold2"]}" stop-opacity="0"/></linearGradient>')
    x.css(f"@keyframes sl{u}{{from{{transform:translateX(-380px)}}to{{transform:translateX(380px)}}}}"
          f".sl{u}{{animation:sl{u} 7s ease-in-out infinite alternate}}")
    body = "\n".join([
        fade_line(x, 60, cx - 30, 17, "a", 0.75, both=False),
        f'<g transform="translate({W} 0) scale(-1 1)">{fade_line(x, 60, cx - 30, 17, "b", 0.75, both=False)}</g>',
        diamond(cx, 17, 5, c["gold"]),
        diamond(cx - 17, 17, 2.2, c["gold"], 0.6), diamond(cx + 17, 17, 2.2, c["gold"], 0.6),
        f'<rect class="sl{u}" x="{cx-90}" y="16" width="180" height="2" fill="url(#sg{u})"/>',
    ])
    return x.render(body)


# ---------------------------------------------------------------------------
def about_svg(c):
    x = Ctx(c, "ab", 440, title="About Javohir",
            desc="Introduction and a summary of education, strengths and focus.")
    u = x.uid
    left_x, col_w = 64, 420
    head = "From a Figma frame to a deployed product."
    head_lines = typo.wrap(head, "serif", 38, col_w)
    y = 100
    parts = []
    for ln in head_lines:
        parts.append(x.t(ln, left_x, y, 38, c["text"], "serif"))
        y += 48
    y += 6
    para = ("I'm a software engineering graduate who likes taking an idea from a UI prototype to a working application: "
            "the interface in Figma, then the API, database, authentication, file uploads, real-time communication, "
            "deployment and tests behind it.")
    for ln in typo.wrap(para, "sans", 15.5, col_w):
        parts.append(x.t(ln, left_x, y + 12, 15.5, c["text2"], "sans", ls=0.1))
        y += 26
    y += 22
    for ln in typo.wrap("I care about software that pairs good UX with a reliable backend and real data.", "serifi", 18, col_w):
        parts.append(x.t(ln, left_x, y, 18, c["gold"] if not c["is_dark"] else c["gold2"], "serifi"))
        y += 27

    # right column: label / value rows
    rx, lw, vw = 566, 124, 252
    rows = [
        ("Education", "B.Sc. Software Engineering, Turin Polytechnic University in Tashkent"),
        ("Strongest in", "Dart and Flutter, Python, JavaScript and Node.js"),
        ("Also works with", "Kotlin, Java, C, HTML and CSS"),
        ("Focus", "Flutter, backend development, system design, cloud-connected apps"),
        ("Curious about", "ESP32 and MQTT, computer vision, automation"),
    ]
    ry = 62
    x.css(f"@keyframes dr{u}{{from{{transform:scaleX(0)}}}}.dr{u}{{transform-origin:{rx}px 0;transform-box:view-box;animation:dr{u} 1.3s cubic-bezier(.2,.7,.2,1) both}}")
    right = []
    for i, (lab, val) in enumerate(rows):
        lines = typo.wrap(val, "sans", 14.5, vw)
        rh = max(1, len(lines)) * 22 + 26
        right.append(f'<rect class="dr{u}" x="{rx}" y="{ry}" width="{W - 64 - rx}" height="1" fill="{c["gold"]}" fill-opacity="0.38" style="animation-delay:{0.15*i:.2f}s"/>')
        right.append(x.t(lab, rx, ry + 30, 12.5, c["gold"], "sansm", ls=0.4))
        for j, ln in enumerate(lines):
            right.append(x.t(ln, rx + lw, ry + 30 + j * 22, 14.5, c["text"], "sans"))
        ry += rh
    right.append(f'<rect class="dr{u}" x="{rx}" y="{ry}" width="{W - 64 - rx}" height="1" fill="{c["gold"]}" fill-opacity="0.38" style="animation-delay:{0.15*len(rows):.2f}s"/>')

    # vertical rule with a light travelling down it
    vx = 530
    x.defs(f'<path id="vp{u}" d="M{vx} 60 V{x.h-60}"/>')
    rule = (f'<line x1="{vx}" y1="60" x2="{vx}" y2="{x.h-60}" stroke="{c["gold"]}" stroke-opacity="0.25"/>'
            f'<circle r="2.4" fill="{c["gold2"]}"><animateMotion dur="5.5s" repeatCount="indefinite" keyPoints="0;1;0" keyTimes="0;0.5;1" calcMode="linear"><mpath xlink:href="#vp{u}"/></animateMotion></circle>'
            f'<circle r="7" fill="{c["gold2"]}" opacity="0.18"><animateMotion dur="5.5s" repeatCount="indefinite" keyPoints="0;1;0" keyTimes="0;0.5;1" calcMode="linear"><mpath xlink:href="#vp{u}"/></animateMotion></circle>')

    body = "\n".join([
        frame(x, r=6),
        f'<g clip-path="url(#clip{u})">{dust(x, 14, seed=21, rise=60)}</g>',
        "\n".join(parts), rule, "\n".join(right),
        sparkles(x, [(500, 40), (930, 380), (60, 385)], seed=8),
        border(x, r=6),
    ])
    return x.render(body)


# ---------------------------------------------------------------------------
STEPS = ["Idea", "User flow", "Wireframe", "Figma prototype", "Frontend", "Backend and API",
         "Database", "Testing", "Deployment"]


def workflow_svg(c):
    h = 330
    x = Ctx(c, "wf", h, title="Development workflow: idea, user flow, wireframe, Figma prototype, frontend, backend and API, database, testing, deployment")
    u = x.uid
    n = len(STEPS)
    x0, x1 = 96, W - 96
    pts = []
    for i in range(n):
        px = x0 + (x1 - x0) * i / (n - 1)
        py = 212 + (-20 if i % 2 == 0 else 20)
        pts.append((px, py))
    d = f"M{pts[0][0]:.1f} {pts[0][1]}"
    for (ax, ay), (bx, by) in zip(pts, pts[1:]):
        dx = (bx - ax) / 2
        d += f" C{ax+dx:.1f} {ay} {bx-dx:.1f} {by} {bx:.1f} {by}"
    dur = 12.0

    x.css(f"@keyframes np{u}{{0%{{fill-opacity:1;transform:scale(1.5)}}12%{{fill-opacity:.9;transform:scale(1)}}55%,100%{{fill-opacity:0;transform:scale(1)}}}}"
          f".np{u}{{transform-box:fill-box;transform-origin:center;animation:np{u} {dur}s ease-out infinite;fill-opacity:0}}"
          f"@keyframes lb{u}{{0%{{opacity:1}}30%,100%{{opacity:.62}}}}.lb{u}{{animation:lb{u} {dur}s ease-out infinite;opacity:.62}}")
    nodes, labels = [], []
    for i, ((px, py), name) in enumerate(zip(pts, STEPS)):
        t = dur * i / (n - 1)
        dl = -(dur - t) if i else 0
        nodes.append(f'<circle cx="{px:.1f}" cy="{py}" r="7.5" fill="{c["bg"]}" stroke="{c["gold"]}" stroke-width="1.2"/>'
                     f'<circle class="np{u}" cx="{px:.1f}" cy="{py}" r="7.5" fill="{c["gold2"]}" style="animation-delay:{dl:.2f}s"/>')
        above = i % 2 == 0
        ly = py - 24 if above else py + 34
        labels.append(x.t(name, px, ly, 14, c["text"], "sansm", anchor="middle", ls=0.2, cls=f"lb{u}",
                          style=f"animation-delay:{dl:.2f}s"))

    x.defs(f'<path id="wp{u}" d="{d}"/>')
    track = (f'<use xlink:href="#wp{u}" fill="none" stroke="{c["gold"]}" stroke-opacity="0.32" stroke-width="1.2"/>'
             f'<use xlink:href="#wp{u}" fill="none" stroke="{c["gold"]}" stroke-opacity="0.55" stroke-width="1.2" stroke-dasharray="2 7" stroke-linecap="round"/>')
    runner = (f'<circle r="4" fill="{c["gold2"]}"><animateMotion dur="{dur}s" repeatCount="indefinite" calcMode="linear"><mpath xlink:href="#wp{u}"/></animateMotion></circle>'
              f'<circle r="13" fill="{c["gold2"]}" opacity="0.16"><animateMotion dur="{dur}s" repeatCount="indefinite" calcMode="linear"><mpath xlink:href="#wp{u}"/></animateMotion></circle>')

    body = "\n".join([
        frame(x, r=6),
        x.t("From idea to deployment", 64, 84, 34, c["text"], "serif"),
        x.t("The path most of my projects follow.", 64, 114, 17, c["gold"] if not c["is_dark"] else c["gold2"], "serifi"),
        track, "\n".join(nodes), runner, "\n".join(labels),
        border(x, r=6),
    ])
    return x.render(body)


# ---------------------------------------------------------------------------
def footer_svg(c):
    h = 210
    x = Ctx(c, "ft", h, title="Let's create something useful.")
    u, cx = x.uid, W / 2
    fill = name_gradient(x, f"fg{u}")
    x.css(f"@keyframes pu{u}{{from{{transform:scale(.85);opacity:.6}}to{{transform:scale(1.15);opacity:1}}}}"
          f".pu{u}{{transform-box:fill-box;transform-origin:center;animation:pu{u} 3.2s ease-in-out infinite alternate}}")
    body = "\n".join([
        frame(x, r=6),
        f'<g clip-path="url(#clip{u})">{dust(x, 20, seed=31, rise=70)}</g>',
        fade_line(x, 80, cx - 40, 62, "l", 0.7, both=False),
        f'<g transform="translate({W} 0) scale(-1 1)">{fade_line(x, 80, cx - 40, 62, "r", 0.7, both=False)}</g>',
        f'<g class="pu{u}">{star4(cx, 62, 15, c["gold2"] if c["is_dark"] else c["gold"])}</g>',
        x.t("Let's create something useful.", cx, 128, 40, fill, "serifi", anchor="middle"),
        x.t("Software developer, Flutter, backend, full-stack, IoT", cx, 160, 14.5, c["text2"], "sans", anchor="middle", ls=0.5),
        x.t("Every graphic on this page is a hand-built SVG, generated by the code in /generator.", cx, 187, 12.5, c["text3"], "sans", anchor="middle", ls=0.2),
        sparkles(x, [(180, 120), (820, 130), (300, 60), (700, 60)], seed=13),
        border(x, r=6),
    ])
    return x.render(body)
