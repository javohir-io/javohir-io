# -*- coding: utf-8 -*-
from kit import Ctx, frame, border, rosette, dial, sq, hair, fade_line, ticks_v, cross, gt, W

ROLES = ["Cross-platform apps with Flutter", "REST APIs with FastAPI and Node.js",
         "Real-time systems over WebSockets", "Connected devices with ESP32 and MQTT"]


def header_svg(c):
    h = 450
    x = Ctx(c, "hd", h, title="Javohir Abduvahhobov, software developer",
            desc="Animated header with the name, a watch-dial emblem and a cycling list of what I build.")
    u, cx = x.uid, W / 2
    name = "JAVOHIR ABDUVAHHOBOV"
    size = 50
    while x.w_(name, "sansm", size, size * 0.17) > 840:
        size -= 1
    ls = size * 0.17

    stops = "".join(f'<stop offset="{o}" stop-color="{col}"/>' for o, col in c["name_stops"])
    x.defs(f'''<linearGradient id="nm{u}" x1="0" y1="0" x2="1" y2="0">{stops}</linearGradient>
<linearGradient id="wipe{u}" gradientUnits="userSpaceOnUse" x1="1000" y1="0" x2="1300" y2="0"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#000"/>
  <animateTransform attributeName="gradientTransform" type="translate" from="-1320 0" to="0 0" dur="2.4s" calcMode="spline" keyTimes="0;1" keySplines="0.32 0 0.15 1" fill="freeze"/></linearGradient>
<mask id="wm{u}" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{h}"><rect width="{W}" height="{h}" fill="url(#wipe{u})"/></mask>
<linearGradient id="band{u}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{c['band']}" stop-opacity="0"/><stop offset="0.5" stop-color="{c['band']}" stop-opacity="{c['band_op']}"/><stop offset="1" stop-color="{c['band']}" stop-opacity="0"/></linearGradient>''')
    ny = 238
    nm_fill = x.t(name, cx, ny, size, f"url(#nm{u})", "sansm", anchor="middle", ls=ls)
    nm_mask = x.t(name, cx, ny, size, "#fff", "sansm", anchor="middle", ls=ls)
    x.defs(f'<mask id="tm{u}" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{h}">{nm_mask}</mask>')
    x.css(f"@keyframes sw{u}{{0%{{transform:translateX(-260px) skewX(-20deg)}}30%,100%{{transform:translateX(1180px) skewX(-20deg)}}}}.sw{u}{{animation:sw{u} 8s ease-in-out 3s infinite}}")
    shimmer = f'<g mask="url(#tm{u})"><rect class="sw{u}" x="0" y="190" width="130" height="70" fill="url(#band{u})"/></g>'

    # side rulers with travelling markers
    rl, rr = 46, W - 46
    y0, ry = 70, h - 150
    x.css(f"@keyframes mk{u}{{from{{transform:translateY(0)}}to{{transform:translateY({ry-6}px)}}}}.mk{u}{{animation:mk{u} 7s ease-in-out infinite alternate}}"
          f".mk{u}b{{animation:mk{u} 9s ease-in-out infinite alternate-reverse}}")
    rulers = (ticks_v(rl, y0, ry, 40, 5, c["steel"], 0.45) + ticks_v(rr, y0, ry, 40, 5, c["steel"], 0.45, left=True)
              + f'<rect class="mk{u}" x="{rl}" y="{y0-1.5}" width="20" height="3" fill="{gt(c)}"/>'
              + f'<rect class="mk{u}b" x="{rr-20}" y="{y0-1.5}" width="20" height="3" fill="{gt(c)}"/>')

    sub = x.t("SOFTWARE DEVELOPER", cx, 302, 14, gt(c), "sansm", anchor="middle", ls=9)
    period = 4.2 * len(ROLES)
    step = 100 / len(ROLES)
    roles = []
    for i, r in enumerate(ROLES):
        nmk = f"ro{u}{i}"
        a, b, cc, d = i * step, i * step + 2.5, (i + 1) * step - 3, (i + 1) * step - 0.4
        x.css(f"@keyframes {nmk}{{0%,{a:.2f}%{{opacity:0;transform:translateY(8px)}}{b:.2f}%{{opacity:1;transform:translateY(0)}}"
              f"{cc:.2f}%{{opacity:1;transform:translateY(0)}}{d:.2f}%{{opacity:0;transform:translateY(-6px)}}100%{{opacity:0}}}}")
        roles.append(x.t(r, cx, 352, 21, c["text2"], "serifi", anchor="middle", ls=0.4,
                         style=f"opacity:{1 if i == 0 else 0};animation:{nmk} {period}s ease-in-out infinite"))
    x.reduced.append(f"text[style*='ro{u}0']{{opacity:1!important}}")

    x.css(f"@keyframes ping{u}{{from{{r:4;opacity:.8}}to{{r:14;opacity:0}}}}.ping{u}{{animation:ping{u} 2.4s ease-out infinite}}")
    by = h - 34
    bar = (hair(84, W - 84, by - 24, c["gold"], 0.22)
           + f'<circle cx="86" cy="{by}" r="3.6" fill="{c["good"]}"/><circle class="ping{u}" cx="86" cy="{by}" r="4" fill="none" stroke="{c["good"]}" stroke-width="1.3"/>'
           + x.t("github.com/javohir-io", 100, by + 4.5, 13, c["text2"], "sans", ls=0.5)
           + x.t("TURIN POLYTECHNIC UNIVERSITY IN TASHKENT", W - 84, by + 4.5, 11.5, c["text3"], "sansm", anchor="end", ls=2.2))

    body = "\n".join([
        frame(x, scan=True),
        f'<g clip-path="url(#clip{u})">{rosette(x, cx, 220, 250, 30, 160, c["steel"], 0.16 if c["is_dark"] else 0.22)}</g>',
        rulers,
        fade_line(x, 130, cx - 60, 92, "l", 0.7, both=False),
        f'<g transform="translate({W} 0) scale(-1 1)">{fade_line(x, 130, cx - 60, 92, "r", 0.7, both=False)}</g>',
        dial(x, cx, 92, 30, "JA", 24, "h"),
        f'<g mask="url(#wm{u})">{nm_fill}</g>', shimmer,
        fade_line(x, cx - 180, cx + 180, 268, "m", 0.7), sq(cx, 268, 3.2, gt(c)),
        sub, "".join(roles), bar,
        cross(84, 60, 6, c["gold"], 0.7), cross(W - 84, 60, 6, c["gold"], 0.7),
        border(x, chase=True),
    ])
    return x.render(body)
