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
    x.css(f"@keyframes br{u}{{from{{opacity:.5}}to{{opacity:1}}}}.br{u}{{animation:br{u} 4.5s ease-in-out infinite alternate}}"
          f"@keyframes fl{u}{{from{{transform:translateY(0)}}to{{transform:translateY(-5px)}}}}.fl{u}{{animation:fl{u} 6s ease-in-out infinite alternate}}"
          f"@keyframes cm{u}{{from{{stroke-dashoffset:0}}to{{stroke-dashoffset:-1000}}}}.cm{u}{{animation:cm{u} 12s linear infinite}}"
          f"@keyframes dr{u}{{from{{transform:scaleX(0)}}}}.dr{u}{{transform-box:view-box;transform-origin:{lx}px 0;animation:dr{u} 1.2s cubic-bezier(.2,.7,.2,1) both}}")
    x.defs(f'<radialGradient id="hl{u}"><stop offset="0" stop-color="{c["red"]}" stop-opacity="0.45"/><stop offset="1" stop-color="{c["red"]}" stop-opacity="0"/></radialGradient>')
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
    x.h = int(ry + 56)
    art = (f'<circle class="br{u}" cx="770" cy="260" r="260" fill="url(#hl{u})"/>'
           f'<circle cx="770" cy="248" r="190" fill="none" stroke="{c["red"]}" stroke-opacity="0.35"/>'
           f'<circle class="cm{u}" cx="770" cy="248" r="190" fill="none" stroke="{c["red2"]}" stroke-width="1.8" pathLength="1000" stroke-dasharray="70 930" stroke-linecap="round"/>'
           f'<g class="fl{u}">{image("statue-head.webp", 570, 70, 400, 444)}</g>')
    body = "\n".join([frame(x), f'<g clip-path="url(#clip{u})">{art}</g>', ribbon(x, "M1010 300C960 380 930 450 910 512", "a", 1),
                      f'<g clip-path="url(#clip{u})">{embers(x, 14, 3, rise=90)}</g>', *parts, border(x)])
    return x.render(body)


STACK = [("LANGUAGES", ["Dart", "Python", "JavaScript", "Kotlin", "Java", "C"]), ("MOBILE AND WEB", ["Flutter", "Jetpack Compose", "HTML and CSS"]),
         ("BACKEND", ["FastAPI", "Node.js", "Express", "WebSockets"]), ("DATA", ["PostgreSQL", "SQLite"]),
         ("CLOUD AND DEVOPS", ["Docker", "GitHub Actions", "Google Cloud", "Render", "Netlify"]), ("IOT AND DESIGN", ["ESP32", "MQTT", "OpenCV", "Figma"])]
PRIMARY = {"Dart", "Python", "JavaScript", "Flutter", "FastAPI", "Node.js", "PostgreSQL"}


def stack_svg(c):
    x = Ctx(c, "sk", 500, title="Technical stack", desc="Languages, mobile, backend, data, cloud and IoT tools. Items marked red are the ones I reach for most.")
    u = x.uid
    x.css(f"@keyframes dr{u}{{from{{transform:scaleX(0)}}}}.dr{u}{{transform-box:view-box;transform-origin:60px 0;animation:dr{u} 1.3s cubic-bezier(.2,.7,.2,1) both}}"
          f"@keyframes bl{u}{{from{{opacity:.45}}to{{opacity:1}}}}.bl{u}{{animation:bl{u} 3s ease-in-out infinite alternate}}")
    fill = silver_grad(x, f"tg{u}")
    parts = [label(x, 60, 82, "Stack"), x.t("The toolbox", 60, 138, 44, fill, "disp", ls=-0.5),
             x.t("RED MARKS WHAT I REACH FOR MOST", W - 60, 134, 10.5, c["text3"], "sansm", anchor="end", ls=3)]
    y = 170
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
    body = "\n".join([frame(x), f'<g clip-path="url(#clip{u})">{embers(x, 10, 8, rise=80)}</g>', *parts, border(x)])
    return x.render(body)


STEPS = ["Idea", "User flow", "Wireframe", "Figma", "Frontend", "Backend", "Database", "Testing", "Deploy"]


def workflow_svg(c):
    h = 300
    x = Ctx(c, "wf", h, title="Workflow: idea, user flow, wireframe, Figma, frontend, backend, database, testing, deploy")
    u = x.uid
    fill = silver_grad(x, f"tg{u}")
    n, x0, x1, ty, dur = len(STEPS), 90, W - 90, 208, 12.0
    x.css(f"@keyframes st{u}{{0%{{fill-opacity:1}}14%{{fill-opacity:1}}50%,100%{{fill-opacity:0}}}}.st{u}{{fill-opacity:0;animation:st{u} {dur}s ease-out infinite}}"
          f"@keyframes lb{u}{{0%{{opacity:1}}30%,100%{{opacity:.5}}}}.lb{u}{{opacity:.5;animation:lb{u} {dur}s ease-out infinite}}")
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
    body = "\n".join([frame(x), label(x, 60, 76, "Workflow"), x.t("From idea to deployment", 60, 122, 34, fill, "disp", ls=-0.3), track, runner, *nodes, *labels, border(x)])
    return x.render(body)


# ---------------------------------------------------------------- player
TRACK = dict(title="Formula", artist="Labrinth", album="Euphoria: Season 1 Soundtrack, 2019", seconds=92)


def _envelope(n, seed=7):
    rnd = random.Random(seed)
    return [max(0.1, min(1, 0.28 + 0.5 * math.sin(math.pi * min(1, i / (n - 1) * 1.05)) ** 1.4 + 0.12 * math.sin(i / (n - 1) * 11)
                         + 0.08 * math.sin(i / (n - 1) * 27 + 1.3) + rnd.uniform(-0.12, 0.12))) for i in range(n)]


def player_svg(c):
    h, T = 460, TRACK["seconds"]
    x = Ctx(c, "pl", h, title=f"Soundtrack: {TRACK['title']} by {TRACK['artist']}. Click to play on Spotify.",
            desc="Chronograph-style player: a dial whose ticks are the seconds of the track, a sweep hand, a spinning record, a filling waveform and a running timer.")
    u, cx, cy = x.uid, 250, 226
    fill = silver_grad(x, f"tg{u}")
    x.defs(f'''<radialGradient id="vin{u}"><stop offset="0" stop-color="#1a1112"/><stop offset="1" stop-color="#050303"/></radialGradient>
<linearGradient id="lbl{u}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c['red2']}"/><stop offset="0.6" stop-color="{c['red']}"/><stop offset="1" stop-color="{c['red3']}"/></linearGradient>
<linearGradient id="shn{u}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.5" stop-color="#fff" stop-opacity="0.13"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<radialGradient id="dg{u}"><stop offset="0.6" stop-color="{c['red']}" stop-opacity="0.26"/><stop offset="1" stop-color="{c['red']}" stop-opacity="0"/></radialGradient>''')
    knurl = "".join(f"M{cx+157*math.cos(math.radians(a)):.1f} {cy+157*math.sin(math.radians(a)):.1f}L{cx+163*math.cos(math.radians(a)):.1f} {cy+163*math.sin(math.radians(a)):.1f}" for a in range(0, 360, 3))
    bezel = (f'<circle cx="{cx}" cy="{cy}" r="196" fill="url(#dg{u})"/><circle cx="{cx}" cy="{cy}" r="164" fill="{c["bg"]}" fill-opacity="0.8" stroke="{c["red"]}" stroke-opacity="0.75"/>'
             f'<path d="{knurl}" stroke="{c["silver"]}" stroke-opacity="0.35" fill="none"/><circle cx="{cx}" cy="{cy}" r="152" fill="none" stroke="{c["silver"]}" stroke-opacity="0.18"/>')
    x.css(f"@keyframes tk{u}{{0%{{stroke:{c['red2']};stroke-opacity:1}}10%,100%{{stroke:{c['silver']};stroke-opacity:.34}}}}.tk{u}{{stroke:{c['silver']};stroke-opacity:.34;stroke-width:1.4;animation:tk{u} {T}s linear infinite}}")
    tk = "".join(f'<line class="tk{u}" x1="{cx+(126 if i%10==0 else 136)*math.cos(math.radians(i/T*360-90)):.1f}" y1="{cy+(126 if i%10==0 else 136)*math.sin(math.radians(i/T*360-90)):.1f}" '
                 f'x2="{cx+146*math.cos(math.radians(i/T*360-90)):.1f}" y2="{cy+146*math.sin(math.radians(i/T*360-90)):.1f}" style="animation-delay:{i}s"/>' for i in range(T))
    nums = "".join(x.t(str(s), cx + 112 * math.cos(math.radians(s / T * 360 - 90)), cy + 112 * math.sin(math.radians(s / T * 360 - 90)) + 4, 11, c["text3"], "sansm", anchor="middle", ls=0.4) for s in range(10, T - 5, 10))
    x.css(f"@keyframes pg{u}{{from{{stroke-dashoffset:92}}to{{stroke-dashoffset:0}}}}.pg{u}{{animation:pg{u} {T}s linear infinite}}")
    arc = (f'<circle cx="{cx}" cy="{cy}" r="150" fill="none" stroke="{c["red"]}" stroke-opacity="0.18" stroke-width="2"/>'
           f'<circle class="pg{u}" cx="{cx}" cy="{cy}" r="150" fill="none" stroke="{c["red2"]}" stroke-width="2.4" pathLength="92" stroke-dasharray="92 92" stroke-dashoffset="92" transform="rotate(-90 {cx} {cy})"/>')
    vr = 88
    grooves = "".join(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#fff" stroke-opacity="{0.05 if r % 8 else 0.1}"/>' for r in range(32, vr - 3, 4))
    wedge = lambda a1, a2: f"M{cx} {cy} L{cx+vr*math.cos(math.radians(a1)):.1f} {cy+vr*math.sin(math.radians(a1)):.1f} A{vr} {vr} 0 0 1 {cx+vr*math.cos(math.radians(a2)):.1f} {cy+vr*math.sin(math.radians(a2)):.1f} Z"
    x.css(f"@keyframes sp{u}{{to{{transform:rotate(360deg)}}}}.sp{u}{{transform-origin:{cx}px {cy}px;animation:sp{u} 3.4s linear infinite}}.sw{u}{{transform-origin:{cx}px {cy}px;animation:sp{u} {T}s linear infinite}}")
    record = (f'<circle cx="{cx}" cy="{cy}" r="{vr}" fill="url(#vin{u})" stroke="{c["red"]}" stroke-opacity="0.5"/>{grooves}'
              f'<g class="sp{u}"><circle cx="{cx}" cy="{cy}" r="30" fill="url(#lbl{u})"/><circle cx="{cx}" cy="{cy}" r="22" fill="none" stroke="#000" stroke-opacity="0.4" stroke-dasharray="2 4"/><rect x="{cx-2}" y="{cy-27}" width="4" height="9" fill="#000" fill-opacity="0.55"/></g>'
              f'<path d="{wedge(-50,-20)}" fill="url(#shn{u})"/><path d="{wedge(130,160)}" fill="url(#shn{u})"/>')
    hand = (f'<g class="sw{u}"><line x1="{cx}" y1="{cy+30}" x2="{cx}" y2="{cy-148}" stroke="{c["silver"]}" stroke-width="1.8"/><rect x="{cx-3}" y="{cy+22}" width="6" height="18" fill="{c["silver"]}"/>'
            f'<rect x="{cx-2.5}" y="{cy-146}" width="5" height="16" fill="{c["red2"]}"/></g><circle cx="{cx}" cy="{cy}" r="6.5" fill="{c["bg"]}" stroke="{c["silver"]}" stroke-width="1.6"/><circle cx="{cx}" cy="{cy}" r="2" fill="{c["red2"]}"/>')
    rx0, rx1 = 480, W - 70
    x.css(f"@keyframes eq{u}{{from{{transform:scaleY(.25)}}to{{transform:scaleY(1)}}}}.eq{u}{{transform-box:fill-box;transform-origin:bottom;animation:eq{u} .9s ease-in-out infinite alternate}}")
    eq = "".join(f'<rect class="eq{u}" x="{rx0+i*6}" y="78" width="3" height="16" fill="{c["red"]}" style="animation-duration:{d}s;animation-delay:-{i*0.23:.2f}s"/>' for i, d in enumerate([0.7, 1.05, 0.85, 1.2, 0.6]))
    head = "\n".join([eq, x.t("NOW SPINNING", rx0 + 40, 91, 11.5, c["red"], "sansm", ls=3.6), x.t(TRACK["title"], rx0 - 3, 182, 88, fill, "disp", ls=-1),
                      x.t(TRACK["artist"].upper(), rx0, 222, 16, c["text"], "sansm", ls=8), x.t(TRACK["album"], rx0, 252, 16, c["text2"], "serifi"), hair(rx0, rx0 + 70, 270, c["red"], 1, 2)])
    n, bw = 94, 3.0
    gap = (rx1 - rx0 - bw * n) / (n - 1)
    wy, maxh = 324, 46
    dim, lit = [], []
    for i, e in enumerate(_envelope(n)):
        bx, bh = rx0 + i * (bw + gap), max(4, e * 46)
        r_ = f'<rect x="{bx:.1f}" y="{wy-bh/2:.1f}" width="{bw}" height="{bh:.1f}" fill="%s"/>'
        dim.append(r_ % f'{c["silver"]}" fill-opacity="0.22'); lit.append(r_ % c["red"])
    x.defs(f'<clipPath id="prog{u}"><rect x="{rx0-2}" y="{wy-32}" width="0" height="64"><animate attributeName="width" from="0" to="{rx1-rx0+4}" dur="{T}s" repeatCount="indefinite"/></rect></clipPath>')
    playhead = (f'<g><line x1="0" y1="{wy-32}" x2="0" y2="{wy+32}" stroke="{c["red2"]}" stroke-width="1.4"/><rect x="-4" y="{wy+32}" width="8" height="8" fill="{c["red2"]}"/>'
                f'<animateTransform attributeName="transform" type="translate" from="{rx0}" to="{rx1}" dur="{T}s" repeatCount="indefinite"/></g>')
    x.css(f"@keyframes tm{u}{{0%{{opacity:1}}{100/T:.4f}%{{opacity:0}}100%{{opacity:0}}}}.tm{u}{{opacity:0;animation:tm{u} {T}s steps(1,end) infinite}}")
    x.reduced.append(f".t0{u}{{opacity:1!important}}")
    timers = [x.t(f"{s//60}:{s%60:02d}", rx0, 380, 14, c["text"], "sansm", ls=1, cls=f"tm{u}" + (f" t0{u}" if s == 0 else ""), style=f"animation-delay:{s}s") for s in range(T + 1)]
    total = x.t(f"{T//60}:{T%60:02d}", rx1, 380, 14, c["text3"], "sansm", anchor="end", ls=1)
    ccx, ccy = rx0 + 60, 416
    x.css(f"@keyframes pr{u}{{from{{r:24;opacity:.7}}to{{r:38;opacity:0}}}}.pr{u}{{animation:pr{u} 2.6s ease-out infinite}}")
    ctl = (f'<g stroke="{c["text2"]}" stroke-width="1.7" fill="{c["text2"]}" stroke-linejoin="round"><path d="M{ccx-72} {ccy-8}V{ccy+8}" fill="none"/><path d="M{ccx-50} {ccy-9}L{ccx-62} {ccy}L{ccx-50} {ccy+9}Z"/>'
           f'<path d="M{ccx+72} {ccy-8}V{ccy+8}" fill="none"/><path d="M{ccx+50} {ccy-9}L{ccx+62} {ccy}L{ccx+50} {ccy+9}Z"/></g>'
           f'<circle class="pr{u}" cx="{ccx}" cy="{ccy}" r="24" fill="none" stroke="{c["red2"]}" stroke-width="1.3"/><circle cx="{ccx}" cy="{ccy}" r="24" fill="{c["red"]}"/>'
           f'<path d="M{ccx-6} {ccy-10}L{ccx+11} {ccy}L{ccx-6} {ccy+10}Z" fill="#fff"/>')
    pw, ph, px, py = 230, 44, rx1 - 230, ccy - 22
    btn = (f'<rect x="{px+.5}" y="{py+.5}" width="{pw-1}" height="{ph-1}" fill="none" stroke="{c["red"]}" stroke-width="1.2"/>'
           f'<path d="M{px+pw-14} {py+.5}H{px+pw-.5}V{py+14}" fill="none" stroke="{c["red2"]}" stroke-width="1.8"/>'
           f'<g transform="translate({px+28} {ccy})"><circle r="10" fill="{c["silver"]}"/><g fill="none" stroke="#000" stroke-width="1.7" stroke-linecap="round"><path d="M-5.6 -2.8Q0 -5 5.8 -1.8"/><path d="M-4.6 0.8Q0 -0.8 4.8 1.6"/><path d="M-3.6 4.2Q0 3 3.8 4.4"/></g></g>'
           + x.t("PLAY ON SPOTIFY", px + 50, ccy + 4.5, 12.5, c["text"], "sansm", ls=2.4))
    rnd = random.Random(3)
    x.css(f"@keyframes spc{u}{{from{{transform:scaleY(.12)}}to{{transform:scaleY(1)}}}}.spc{u}{{transform-box:fill-box;transform-origin:bottom;animation:spc{u} 1s ease-in-out infinite alternate}}")
    spec = "".join(f'<rect class="spc{u}" x="{30+i*(940/120):.1f}" y="{h-16-hh:.1f}" width="2.4" height="{hh:.1f}" fill="{c["red"]}" fill-opacity="0.38" style="animation-duration:{0.55+rnd.random()*0.9:.2f}s;animation-delay:-{rnd.random()*2:.2f}s"/>'
                   for i in range(120) for hh in [(6 + rnd.random() * 14) * (0.3 + 0.7 * math.sin(math.pi * i / 120) ** 0.8) + 3])
    body = "\n".join([frame(x), f'<g clip-path="url(#clip{u})">{rosette(x, 700, 220, 300, 30, 220, c["red"], 0.10)}{spec}</g>', bezel, arc, tk, nums, record, hand, head,
                      "".join(dim), f'<g clip-path="url(#prog{u})">{"".join(lit)}</g>', playhead, "".join(timers), total, ctl, btn, border(x)])
    return x.render(body)


# ---------------------------------------------------------------- philosophy / contact / footer
def philosophy_svg(c):
    h = 330
    x = Ctx(c, "ph", h, title="Build it. Understand it. Improve it.")
    u, cx = x.uid, W / 2
    fill = silver_grad(x, f"tg{u}")
    phrases = ["Build it.", "Understand it.", "Improve it."]
    size, gap = 54, 46
    widths = [x.w_(p, "disp", size, -0.5) for p in phrases]
    pos = cx - (sum(widths) + gap * 2) / 2
    by, cyc = 170, 9.0
    parts = []
    for i, (p, w) in enumerate(zip(phrases, widths)):
        a = i * 100 / 3
        x.css(f"@keyframes ph{u}{i}{{0%,{a:.1f}%{{opacity:0}}{a+4:.1f}%{{opacity:1}}{a+30:.1f}%{{opacity:1}}{min(a+34,100):.1f}%,100%{{opacity:0}}}}"
              f"@keyframes ul{u}{i}{{0%,{a:.1f}%{{transform:scaleX(0)}}{a+10:.1f}%{{transform:scaleX(1)}}{a+30:.1f}%{{transform:scaleX(1)}}{min(a+34,100):.1f}%,100%{{transform:scaleX(0)}}}}")
        parts.append(x.t(p, pos, by, size, c["text"], "disp", ls=-0.5, opacity=0.26))
        parts.append(x.t(p, pos, by, size, fill, "disp", ls=-0.5, style=f"animation:ph{u}{i} {cyc}s ease-in-out infinite"))
        parts.append(f'<rect x="{pos}" y="{by+16}" width="{w:.1f}" height="2" fill="{c["red"]}" style="transform-box:fill-box;transform-origin:left;animation:ul{u}{i} {cyc}s ease-in-out infinite"/>')
        pos += w + gap
    x.reduced.append(f"text[style*='ph{u}']{{opacity:1!important}}")
    x.defs(f'<radialGradient id="pg{u}"><stop offset="0" stop-color="{c["red"]}" stop-opacity="0.32"/><stop offset="1" stop-color="{c["red"]}" stop-opacity="0"/></radialGradient>')
    body = "\n".join([frame(x), f'<g clip-path="url(#clip{u})"><circle cx="{cx}" cy="190" r="300" fill="url(#pg{u})"/>{image("statue-small.webp", cx-210, 20, 420, 324, 0.22)}</g>',
                      label(x, 60, 72, "Philosophy"), *parts,
                      x.t("AI speeds me up. Understanding the code is still my job.", cx, 262, 16, c["text2"], "serifi", anchor="middle"),
                      f'<g clip-path="url(#clip{u})">{embers(x, 14, 4, rise=90)}</g>', border(x)])
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


def footer_svg(c):
    h = 250
    x = Ctx(c, "ft", h, title="Let's create something useful.")
    u, cx = x.uid, W / 2
    fill = silver_grad(x, f"tg{u}")
    x.css(f"@keyframes cm{u}{{from{{stroke-dashoffset:0}}to{{stroke-dashoffset:-1000}}}}.cm{u}{{animation:cm{u} 12s linear infinite}}")
    ring = (f'<circle cx="{cx}" cy="{h/2}" r="170" fill="none" stroke="{c["red"]}" stroke-opacity="0.3"/>'
            f'<circle class="cm{u}" cx="{cx}" cy="{h/2}" r="170" fill="none" stroke="{c["red2"]}" stroke-width="1.8" pathLength="1000" stroke-dasharray="70 930" stroke-linecap="round"/>')
    body = "\n".join([frame(x), f'<g clip-path="url(#clip{u})">{ring}</g>', ribbon(x, "M-10 230C150 180 300 120 470 -10", "a"), ribbon(x, "M1010 270C900 250 800 180 700 -10", "b", 3),
                      x.t("JA", cx, 84, 40, c["text"], "disp", anchor="middle"), x.t("Let's create something useful.", cx, 150, 44, fill, "disp", anchor="middle", ls=-0.4),
                      x.t("SOFTWARE DEVELOPER   /   FLUTTER   /   BACKEND   /   IOT", cx, 196, 11, c["text2"], "sansm", anchor="middle", ls=3.4),
                      f'<g clip-path="url(#clip{u})">{embers(x, 18, 9, rise=100)}</g>', border(x)])
    return x.render(body)
