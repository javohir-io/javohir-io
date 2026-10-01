# -*- coding: utf-8 -*-
import math, random
import typo
from kit import (Ctx, frame, border, embers, ribbon, rosette, label, image, hair, cross, fade_line, paragraph, silver_grad,
                 ticks_h, ticks_v, flow_dot, W)


def divider_svg(c):
    x = Ctx(c, "dv", 30, title="divider")
    u, cx = x.uid, W / 2
    x.defs(f'<linearGradient id="sg{u}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{c["red2"]}" stop-opacity="0"/><stop offset="0.5" stop-color="{c["red2"]}"/><stop offset="1" stop-color="{c["red2"]}" stop-opacity="0"/></linearGradient>')
    x.css(f"@keyframes sl{u}{{from{{transform:translateX(-380px)}}to{{transform:translateX(380px)}}}}.sl{u}{{animation:sl{u} 7s ease-in-out infinite alternate}}")
    body = "\n".join([fade_line(x, 80, cx - 22, 15, "a", 0.8, both=False), f'<g transform="translate({W} 0) scale(-1 1)">{fade_line(x, 80, cx - 22, 15, "b", 0.8, both=False)}</g>',
                      f'<rect x="{cx-5}" y="10" width="10" height="10" transform="rotate(45 {cx} 15)" fill="none" stroke="{c["red"]}" stroke-width="1.4"/>',
                      f'<rect x="{cx-1.8}" y="13.2" width="3.6" height="3.6" transform="rotate(45 {cx} 15)" fill="{c["red2"]}"/>',
                      f'<rect class="sl{u}" x="{cx-90}" y="14" width="180" height="2" fill="url(#sg{u})"/>'])
    return x.render(body)


def about_svg(c):
    h = 560
    x = Ctx(c, "ab", h, title="About Javohir")
    u = x.uid
    lx = 60
    x.css(f"@keyframes dr{u}{{from{{transform:scaleX(0)}}}}.dr{u}{{transform-box:view-box;transform-origin:{lx}px 0;animation:dr{u} 1.2s cubic-bezier(.2,.7,.2,1) both}}"
          f"@keyframes sn{u}{{from{{transform:translateY(-70px)}}to{{transform:translateY(470px)}}}}.sn{u}{{animation:sn{u} 5.5s ease-in-out infinite}}"
          f"@keyframes pu{u}{{from{{opacity:.45}}to{{opacity:1}}}}.pu{u}{{animation:pu{u} 2.8s ease-in-out infinite alternate}}")
    fill = silver_grad(x, f"tg{u}")
    parts = [label(x, lx, 84, "About")]
    y = 148
    for ln in typo.wrap("From a Figma frame to a deployed product.", "disp", 46, 470):
        parts.append(x.t(ln, lx, y, 46, fill, "disp", ls=-0.5))
        y += 54
    rows = [("EDUCATION", "B.Sc. Software Engineering, Turin Polytechnic University in Tashkent"), ("STRONGEST IN", "Dart, Python, JavaScript"),
            ("FOCUS", "Flutter, backend, system design, cloud"), ("LANGUAGES", "Uzbek, English (B2), Russian")]
    ry = y + 14
    for i, (lab, val) in enumerate(rows):
        lines = typo.wrap(val, "sans", 14, 330)
        parts.append(f'<rect class="dr{u}" x="{lx}" y="{ry}" width="500" height="1" fill="{c["red"]}" fill-opacity="0.5" style="animation-delay:{i*0.12:.2f}s"/>')
        parts.append(x.t(lab, lx, ry + 30, 10.5, c["red"], "sansm", ls=3.2))
        for j, ln in enumerate(lines):
            parts.append(x.t(ln, lx + 160, ry + 30 + j * 21, 14, c["text"], "sans"))
        ry += 22 + len(lines) * 21 + 10
    parts.append(f'<rect class="dr{u}" x="{lx}" y="{ry}" width="500" height="1" fill="{c["red"]}" fill-opacity="0.5" style="animation-delay:.5s"/>')
    x.h = h = int(ry + 56)
    pw_, ph_ = 340, 453
    px, py = 620, (h - ph_) // 2
    x.defs(f'<clipPath id="pc{u}"><rect x="{px}" y="{py}" width="{pw_}" height="{ph_}"/></clipPath>'
           f'<linearGradient id="sg{u}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{c["red2"]}" stop-opacity="0"/><stop offset="0.5" stop-color="{c["red2"]}" stop-opacity="0.35"/><stop offset="1" stop-color="{c["red2"]}" stop-opacity="0"/></linearGradient>'
           f'<linearGradient id="vg{u}" x1="0" y1="0" x2="0" y2="1"><stop offset="0.55" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.85"/></linearGradient>')
    pic = (f'<g clip-path="url(#pc{u})">{image("pic-about.webp", px, py, pw_, ph_)}<rect x="{px}" y="{py}" width="{pw_}" height="{ph_}" fill="url(#vg{u})"/>'
           f'<rect class="sn{u}" x="{px}" y="{py}" width="{pw_}" height="70" fill="url(#sg{u})"/></g>'
           f'<rect x="{px-.5}" y="{py-.5}" width="{pw_+1}" height="{ph_+1}" fill="none" stroke="{c["red"]}" stroke-opacity="0.6"/>'
           f'<path class="pu{u}" d="M{px-12} {py+30}V{py-12}H{px+30}M{px+pw_-30} {py+ph_+12}H{px+pw_+12}V{py+ph_-30}" fill="none" stroke="{c["red2"]}" stroke-width="2"/>')
    body = "\n".join([frame(x), pic, f'<g clip-path="url(#clip{u})">{embers(x, 12, 3, rise=90)}</g>', *parts, border(x)])
    return x.render(body)


STACK = [("LANGUAGES", ["Dart", "Python", "JavaScript", "Kotlin", "Java", "C"]), ("MOBILE AND WEB", ["Flutter", "Jetpack Compose", "HTML and CSS"]),
         ("BACKEND", ["FastAPI", "Node.js", "Express", "WebSockets"]), ("DATA", ["PostgreSQL", "SQLite"]),
         ("CLOUD AND DEVOPS", ["Docker", "GitHub Actions", "Google Cloud", "Render", "Netlify"]), ("IOT AND DESIGN", ["ESP32", "MQTT", "OpenCV", "Figma"])]
PRIMARY = {"Dart", "Python", "JavaScript", "Flutter", "FastAPI", "Node.js", "PostgreSQL"}


def stack_svg(c):
    x = Ctx(c, "sk", 700, title="Technical stack", desc="Languages, mobile, backend, data, cloud and IoT tools. Items marked red are the ones I reach for most.")
    u = x.uid
    x.css(f"@keyframes dr{u}{{from{{transform:scaleX(0)}}}}.dr{u}{{transform-box:view-box;transform-origin:60px 0;animation:dr{u} 1.3s cubic-bezier(.2,.7,.2,1) both}}"
          f"@keyframes bl{u}{{from{{opacity:.45}}to{{opacity:1}}}}.bl{u}{{animation:bl{u} 3s ease-in-out infinite alternate}}"
          f"@keyframes bz{u}{{from{{transform:scale(1)}}to{{transform:scale(1.04)}}}}.bz{u}{{transform-origin:760px 120px;animation:bz{u} 16s ease-in-out infinite alternate}}")
    x.defs(f'<linearGradient id="lg{u}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#000" stop-opacity="0.9"/><stop offset="0.5" stop-color="#000" stop-opacity="0.55"/><stop offset="1" stop-color="#000" stop-opacity="0"/></linearGradient>')
    fill = silver_grad(x, f"tg{u}")
    banner = f'<g clip-path="url(#clip{u})"><g class="bz{u}">{image("pic-stack.webp", 0, 0, 1000, 340)}</g><rect width="640" height="340" fill="url(#lg{u})"/></g>'
    parts = [label(x, 60, 92, "Stack"), x.t("The toolbox", 60, 156, 54, fill, "disp", ls=-0.5),
             x.t("Red marks what I reach for most.", 60, 196, 15, c["text2"], "serifi")]
    y = 300
    for gi, (lab, items) in enumerate(STACK):
        parts.append(f'<rect class="dr{u}" x="60" y="{y}" width="{W-120}" height="1" fill="{c["red"]}" fill-opacity="0.4" style="animation-delay:{gi*0.1:.2f}s"/>')
        parts.append(x.t(lab, 60, y + 40, 11, c["red"], "sansm", ls=3.2))
        cx = 300
        for it in items:
            prim = it in PRIMARY
            if prim:
                parts.append(f'<rect class="bl{u}" x="{cx}" y="{y+27}" width="7" height="7" fill="{c["red"]}" style="animation-delay:-{(gi*7+len(it))%30/10:.1f}s"/>')
                cx += 16
            f_ = "sansm" if prim else "sans"
            parts.append(x.t(it, cx, y + 40, 16, c["text"] if prim else c["text2"], f_))
            cx += x.w_(it, f_, 16) + 34
        y += 54
    parts.append(f'<rect class="dr{u}" x="60" y="{y}" width="{W-120}" height="1" fill="{c["red"]}" fill-opacity="0.4" style="animation-delay:.7s"/>')
    x.h = int(y + 54)
    body = "\n".join([frame(x), banner, f'<g clip-path="url(#clip{u})">{embers(x, 10, 8, rise=80)}</g>', *parts, border(x)])
    return x.render(body)


STEPS = ["Idea", "User flow", "Wireframe", "Figma", "Frontend", "Backend", "Database", "Testing", "Deploy"]


def workflow_svg(c):
    h = 380
    x = Ctx(c, "wf", h, title="Workflow: idea, user flow, wireframe, Figma, frontend, backend, database, testing, deploy")
    u = x.uid
    fill = silver_grad(x, f"tg{u}")
    n, x0, x1, ty, dur = len(STEPS), 90, W - 90, 262, 12.0
    x.css(f"@keyframes st{u}{{0%{{fill-opacity:1}}14%{{fill-opacity:1}}50%,100%{{fill-opacity:0}}}}.st{u}{{fill-opacity:0;animation:st{u} {dur}s ease-out infinite}}"
          f"@keyframes lb{u}{{0%{{opacity:1}}30%,100%{{opacity:.55}}}}.lb{u}{{opacity:.55;animation:lb{u} {dur}s ease-out infinite}}"
          f"@keyframes nb{u}{{from{{opacity:.5}}to{{opacity:.85}}}}.nb{u}{{animation:nb{u} 5s ease-in-out infinite alternate}}")
    x.defs(f'<linearGradient id="dk{u}" x1="0" y1="0" x2="0" y2="1"><stop offset="0.45" stop-color="#000" stop-opacity="0"/><stop offset="1" stop-color="#000" stop-opacity="0.7"/></linearGradient>')
    pic = f'<g clip-path="url(#clip{u})"><g class="nb{u}">{image("pic-workflow.webp", 130, -20, 740, 432)}</g><rect width="{W}" height="{h}" fill="url(#dk{u})"/></g>'
    nodes, labels = [], []
    for i, name in enumerate(STEPS):
        px = x0 + (x1 - x0) * i / (n - 1)
        dl = -(dur - dur * i / (n - 1)) if i else 0
        nodes.append(f'<rect x="{px-6.5}" y="{ty-6.5}" width="13" height="13" fill="{c["bg"]}" stroke="{c["red"]}" stroke-width="1.3" transform="rotate(45 {px:.1f} {ty})"/>'
                     f'<rect class="st{u}" x="{px-6.5}" y="{ty-6.5}" width="13" height="13" fill="{c["red2"]}" transform="rotate(45 {px:.1f} {ty})" style="animation-delay:{dl:.2f}s"/>')
        above = i % 2 == 0
        labels.append(x.t(name.upper(), px, ty - 28 if above else ty + 42, 11.5, c["text"], "sansm", anchor="middle", ls=2.2, cls=f"lb{u}", style=f"animation-delay:{dl:.2f}s"))
        labels.append(f'<path d="M{px:.1f} {ty-10 if above else ty+10}V{ty-20 if above else ty+20}" stroke="{c["red"]}" stroke-opacity="0.6"/>')
    x.defs(f'<path id="wp{u}" d="M{x0} {ty}H{x1}"/>')
    track = (ticks_h(x0, ty, x1 - x0, 96, 12, c["silver"], 0.3, ln=3, lm=3) + f'<line x1="{x0}" y1="{ty}" x2="{x1}" y2="{ty}" stroke="{c["red"]}" stroke-opacity="0.6"/>')
    runner = (f'<rect x="-18" y="-2" width="36" height="4" fill="{c["red2"]}"><animateMotion dur="{dur}s" repeatCount="indefinite" calcMode="linear"><mpath xlink:href="#wp{u}"/></animateMotion></rect>'
              f'<rect x="-40" y="-9" width="80" height="18" fill="{c["red"]}" opacity="0.16"><animateMotion dur="{dur}s" repeatCount="indefinite" calcMode="linear"><mpath xlink:href="#wp{u}"/></animateMotion></rect>')
    body = "\n".join([frame(x), pic, label(x, 60, 76, "Workflow"), x.t("From idea to deployment", 60, 124, 36, fill, "disp", ls=-0.3), track, runner, *nodes, *labels, border(x)])
    return x.render(body)


def _contact(c, uid, kicker, main, sub, icon, ttl):
    h, w = 150, 490
    x = Ctx(c, uid, h, w=w, title=ttl)
    size = 24
    while x.w_(main, "disp", size, -0.3) > w - 150 and size > 14:
        size -= 1
    u = x.uid
    x.css(f"@keyframes ch{u}{{from{{stroke-dashoffset:0}}to{{stroke-dashoffset:-1000}}}}.ch{u}{{animation:ch{u} 9s linear infinite}}")
    chase = f'<rect class="ch{u}" x="0.5" y="0.5" width="{w-1}" height="{h-1}" fill="none" stroke="{c["red2"]}" stroke-width="2" pathLength="1000" stroke-dasharray="80 920"/>'
    fill = silver_grad(x, f"tg{u}")
    body = "\n".join([frame(x), icon(x), label(x, 112, 60, kicker, 10.5, 4, 24, c["red"]), x.t(main, 112, 96, size, fill, "disp", ls=-0.3),
                      x.t(sub, 112, 123, 12.5, c["text3"], "sans", ls=0.3), border(x, brackets=True), chase])
    return x.render(body)


def _mail(x):
    c = x.c
    return (f'<rect x="38" y="52" width="52" height="38" fill="none" stroke="{c["red"]}" stroke-width="1.6"/><path d="M39 55L64 74L89 55" fill="none" stroke="{c["red"]}" stroke-width="1.6" stroke-linejoin="round"/>')


def _git(x):
    c = x.c
    return (f'<g fill="{c["bg"]}" stroke="{c["red"]}" stroke-width="1.6"><rect x="48" y="46" width="12" height="12"/><rect x="48" y="96" width="12" height="12"/><rect x="78" y="62" width="12" height="12"/></g>'
            f'<g fill="none" stroke="{c["red"]}" stroke-width="1.6"><path d="M54 58V96"/><path d="M54 90Q54 72 78 68"/></g>'
            f'<rect x="-3" y="-3" width="6" height="6" fill="{c["red2"]}"><animateMotion dur="2.8s" repeatCount="indefinite" path="M54 96V58"/></rect>')


def contact_email_svg(c):
    return _contact(c, "ce", "Write to me", "javohir.abduvahhobov@gmail.com", "Open your mail app", _mail, "Email Javohir at javohir.abduvahhobov@gmail.com")


def contact_github_svg(c):
    return _contact(c, "cg", "Follow the work", "github.com/javohir-io", "Code and commits", _git, "Javohir on GitHub: github.com/javohir-io")




def closing_svg(c):
    h = 560
    x = Ctx(c, "cl", h, title="Build it. Understand it. Improve it. Let's create something useful.")
    u, cx = x.uid, W / 2
    fill = silver_grad(x, f"tg{u}")
    x.defs(f'<radialGradient id="vg{u}" cx="0.5" cy="0.45" r="0.7"><stop offset="0" stop-color="#000" stop-opacity="0.35"/><stop offset="1" stop-color="#000" stop-opacity="0.9"/></radialGradient>'
           f'<linearGradient id="tb{u}" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#000" stop-opacity="0.55"/><stop offset="0.4" stop-color="#000" stop-opacity="0.1"/><stop offset="1" stop-color="#000" stop-opacity="0.8"/></linearGradient>')
    x.css(f"@keyframes bz{u}{{from{{transform:scale(1)}}to{{transform:scale(1.05)}}}}.bz{u}{{transform-origin:500px 260px;animation:bz{u} 18s ease-in-out infinite alternate}}")
    pic = (f'<g clip-path="url(#clip{u})"><g class="bz{u}">{image("pic-closing.webp", 0, -4, 1000, 561)}</g>'
           f'<rect width="{W}" height="{h}" fill="url(#vg{u})"/><rect width="{W}" height="{h}" fill="url(#tb{u})"/></g>')
    phrases = ["Build it.", "Understand it.", "Improve it."]
    size, gap = 54, 46
    widths = [x.w_(p, "disp", size, -0.5) for p in phrases]
    pos = cx - (sum(widths) + gap * 2) / 2
    by, cyc = 250, 9.0
    parts = []
    for i, (p, w) in enumerate(zip(phrases, widths)):
        a = i * 100 / 3
        x.css(f"@keyframes ph{u}{i}{{0%,{a:.1f}%{{opacity:0}}{a+4:.1f}%{{opacity:1}}{a+30:.1f}%{{opacity:1}}{min(a+34,100):.1f}%,100%{{opacity:0}}}}"
              f"@keyframes ul{u}{i}{{0%,{a:.1f}%{{transform:scaleX(0)}}{a+10:.1f}%{{transform:scaleX(1)}}{a+30:.1f}%{{transform:scaleX(1)}}{min(a+34,100):.1f}%,100%{{transform:scaleX(0)}}}}")
        parts.append(x.t(p, pos, by, size, c["text"], "disp", ls=-0.5, opacity=0.34))
        parts.append(x.t(p, pos, by, size, fill, "disp", ls=-0.5, style=f"animation:ph{u}{i} {cyc}s ease-in-out infinite"))
        parts.append(f'<rect x="{pos}" y="{by+16}" width="{w:.1f}" height="2" fill="{c["red2"]}" style="transform-box:fill-box;transform-origin:left;animation:ul{u}{i} {cyc}s ease-in-out infinite"/>')
        pos += w + gap
    x.reduced.append(f"text[style*='ph{u}']{{opacity:1!important}}")
    body = "\n".join([frame(x, bottom_glow=False), pic, label(x, 60, 72, "Philosophy"), *parts,
                      x.t("AI speeds me up. Understanding the code is still my job.", cx, 316, 16, c["text"], "serifi", anchor="middle", opacity=0.85),
                      fade_line(x, cx - 90, cx + 90, 400, "m", 0.9), f'<rect x="{cx-3.5}" y="{396.5}" width="7" height="7" transform="rotate(45 {cx} 400)" fill="{c["red"]}"/>',
                      x.t("Let's create something useful.", cx, 462, 42, fill, "disp", anchor="middle", ls=-0.4),
                      x.t("SOFTWARE DEVELOPER   /   FLUTTER   /   BACKEND   /   IOT", cx, 502, 11, c["text2"], "sansm", anchor="middle", ls=3.4),
                      f'<g clip-path="url(#clip{u})">{embers(x, 18, 9, rise=100)}</g>', border(x)])
    return x.render(body)
