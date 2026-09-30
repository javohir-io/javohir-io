# -*- coding: utf-8 -*-
import typo
from kit import (Ctx, frame, border, rosette, dial, sq, hair, fade_line, ticks_v, ticks_h, cross, gt, paragraph, W)


def divider_svg(c):
    x = Ctx(c, "dv", 30, title="divider")
    u, cx = x.uid, W / 2
    x.defs(f'<linearGradient id="sg{u}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{c["gold2"]}" stop-opacity="0"/>'
           f'<stop offset="0.5" stop-color="{c["gold2"]}" stop-opacity="1"/><stop offset="1" stop-color="{c["gold2"]}" stop-opacity="0"/></linearGradient>')
    x.css(f"@keyframes sl{u}{{from{{transform:translateX(-380px)}}to{{transform:translateX(380px)}}}}.sl{u}{{animation:sl{u} 7s ease-in-out infinite alternate}}")
    body = "\n".join([
        fade_line(x, 80, cx - 24, 15, "a", 0.8, both=False),
        f'<g transform="translate({W} 0) scale(-1 1)">{fade_line(x, 80, cx - 24, 15, "b", 0.8, both=False)}</g>',
        f'<rect x="{cx-5}" y="10" width="10" height="10" transform="rotate(45 {cx} 15)" fill="none" stroke="{c["gold"]}" stroke-width="1.4"/>',
        sq(cx, 15, 2.2, gt(c)),
        f'<rect class="sl{u}" x="{cx-90}" y="14" width="180" height="2" fill="url(#sg{u})"/>',
    ])
    return x.render(body)


def about_svg(c):
    h = 410
    x = Ctx(c, "ab", h, title="About Javohir")
    u = x.uid
    lx, cw = 76, 440
    parts = []
    y = 112
    for ln in typo.wrap("From a Figma frame to a deployed product.", "serif", 42, cw):
        parts.append(x.t(ln, lx, y, 42, c["text"], "serif"))
        y += 54
    parts.append(fade_line(x, lx, lx + 64, y - 24, "h", 1, both=False, sw=2))
    p, y = paragraph(x, "Software engineer building across mobile, web, backend and IoT.", lx, y + 10, cw, 16, c["text2"], lh=26)
    parts.append(p)

    rx = 590
    rows = [("EDUCATION", "B.Sc. Software Engineering, Turin Polytechnic University in Tashkent"),
            ("STRONGEST IN", "Dart and Flutter, Python, JavaScript"),
            ("FOCUS", "Flutter, backend, system design, cloud"),
            ("LANGUAGES", "Uzbek, English (B2), Russian")]
    ry = 70
    x.css(f"@keyframes dr{u}{{from{{transform:scaleX(0)}}}}.dr{u}{{transform-box:view-box;transform-origin:{rx}px 0;animation:dr{u} 1.2s cubic-bezier(.2,.7,.2,1) both}}")
    right = []
    for i, (lab, val) in enumerate(rows):
        lines = typo.wrap(val, "sans", 15, 320)
        rh = 30 + len(lines) * 22 + 14
        right.append(f'<rect class="dr{u}" x="{rx}" y="{ry}" width="{W-76-rx}" height="1" fill="{c["gold"]}" fill-opacity="0.4" style="animation-delay:{0.14*i:.2f}s"/>')
        right.append(x.t(lab, rx, ry + 26, 11.5, gt(c), "sansm", ls=2.6))
        for j, ln in enumerate(lines):
            right.append(x.t(ln, rx, ry + 52 + j * 22, 15, c["text"], "sans"))
        ry += rh
    right.append(f'<rect class="dr{u}" x="{rx}" y="{ry}" width="{W-76-rx}" height="1" fill="{c["gold"]}" fill-opacity="0.4" style="animation-delay:.6s"/>')

    vx = 548
    x.defs(f'<path id="vp{u}" d="M{vx} 70 V{h-70}"/>')
    rule = (ticks_v(vx, 70, h - 140, 30, 5, c["steel"], 0.4, ln=4, lm=9)
            + f'<rect x="{vx-1}" y="70" width="2" height="{h-140}" fill="{c["gold"]}" fill-opacity="0.18"/>'
            + f'<rect x="-9" y="-1.5" width="18" height="3" fill="{gt(c)}"><animateMotion dur="6s" repeatCount="indefinite" keyPoints="0;1;0" keyTimes="0;.5;1" calcMode="linear"><mpath xlink:href="#vp{u}"/></animateMotion></rect>')
    body = "\n".join([frame(x), *parts, rule, *right, cross(lx, 50, 6, c["gold"], .6), border(x)])
    return x.render(body)


STEPS = ["Idea", "User flow", "Wireframe", "Figma", "Frontend", "Backend", "Database", "Testing", "Deploy"]


def workflow_svg(c):
    h = 250
    x = Ctx(c, "wf", h, title="Workflow: idea, user flow, wireframe, Figma, frontend, backend, database, testing, deploy")
    u = x.uid
    n = len(STEPS)
    x0, x1, ty = 96, W - 96, 150
    dur = 12.0
    x.css(f"@keyframes st{u}{{0%{{fill-opacity:1}}14%{{fill-opacity:1}}50%,100%{{fill-opacity:0}}}}.st{u}{{fill-opacity:0;animation:st{u} {dur}s ease-out infinite}}"
          f"@keyframes lb{u}{{0%{{opacity:1}}30%,100%{{opacity:.55}}}}.lb{u}{{opacity:.55;animation:lb{u} {dur}s ease-out infinite}}")
    nodes, labels = [], []
    for i, name in enumerate(STEPS):
        px = x0 + (x1 - x0) * i / (n - 1)
        dl = -(dur - dur * i / (n - 1)) if i else 0
        nodes.append(f'<rect x="{px-7}" y="{ty-7}" width="14" height="14" fill="{c["bg"]}" stroke="{c["gold"]}" stroke-width="1.3" transform="rotate(45 {px:.1f} {ty})"/>'
                     f'<rect class="st{u}" x="{px-7}" y="{ty-7}" width="14" height="14" fill="{c["gold2"]}" transform="rotate(45 {px:.1f} {ty})" style="animation-delay:{dl:.2f}s"/>')
        above = i % 2 == 0
        labels.append(x.t(name.upper(), px, ty - 26 if above else ty + 40, 12, c["text"], "sansm", anchor="middle", ls=2, cls=f"lb{u}", style=f"animation-delay:{dl:.2f}s"))
        labels.append(f'<path d="M{px:.1f} {ty-10 if above else ty+10}V{ty-20 if above else ty+20}" stroke="{c["gold"]}" stroke-opacity="0.5"/>')
    x.defs(f'<path id="wp{u}" d="M{x0} {ty}H{x1}"/>')
    track = (ticks_h(x0, ty, x1 - x0, 96, 12, c["steel"], 0.35, ln=3, lm=3)
             + f'<line x1="{x0}" y1="{ty}" x2="{x1}" y2="{ty}" stroke="{c["gold"]}" stroke-opacity="0.55"/>')
    runner = (f'<rect x="-18" y="-2" width="36" height="4" fill="{c["gold2"]}"><animateMotion dur="{dur}s" repeatCount="indefinite" calcMode="linear"><mpath xlink:href="#wp{u}"/></animateMotion></rect>'
              f'<rect x="-40" y="-9" width="80" height="18" fill="{c["gold2"]}" opacity="0.12"><animateMotion dur="{dur}s" repeatCount="indefinite" calcMode="linear"><mpath xlink:href="#wp{u}"/></animateMotion></rect>')
    body = "\n".join([frame(x), x.t("From idea to deployment", 76, 84, 30, c["text"], "serif"),
                      *[track, runner], *nodes, *labels, border(x)])
    return x.render(body)


def footer_svg(c):
    h = 200
    x = Ctx(c, "ft", h, title="Let's create something useful.")
    u, cx = x.uid, W / 2
    stops = "".join(f'<stop offset="{o}" stop-color="{col}"/>' for o, col in c["name_stops"])
    x.defs(f'<linearGradient id="fg{u}" x1="0" y1="0" x2="1" y2="0">{stops}</linearGradient>')
    body = "\n".join([
        frame(x),
        f'<g clip-path="url(#clip{u})">{rosette(x, cx, 110, 190, 26, 200, c["steel"], 0.13 if c["is_dark"] else 0.2)}</g>',
        dial(x, cx, 52, 20, None, 12, "f"),
        x.t("Let's create something useful.", cx, 132, 38, f"url(#fg{u})", "serifi", anchor="middle"),
        x.t("SOFTWARE DEVELOPER   /   FLUTTER   /   BACKEND   /   IOT", cx, 166, 11.5, c["text3"], "sansm", anchor="middle", ls=3),
        border(x),
    ])
    return x.render(body)
