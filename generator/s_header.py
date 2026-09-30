# -*- coding: utf-8 -*-
from kit import Ctx, frame, border, dust, sparkles, diamond, fade_line, hair, W

ROLES = [
    "cross-platform apps with Flutter",
    "REST APIs with FastAPI and Node.js",
    "real-time chat over WebSockets",
    "connected devices with ESP32 and MQTT",
]


def header_svg(c):
    h = 430
    x = Ctx(c, "hd", h, title="Javohir Abduvahhobov, software developer",
            desc="Animated header: name, roles that cycle, and a live status line.")
    u = x.uid
    cx = W / 2

    # ---- name: one orchestrated reveal, then an occasional shimmer ---------------------
    stops = "".join(f'<stop offset="{o}" stop-color="{col}"/>' for o, col in c["name_stops"])
    x.defs(f'<linearGradient id="nm{u}" x1="0" y1="0" x2="1" y2="0">{stops}</linearGradient>')
    x.defs(f'''<linearGradient id="wipe{u}" gradientUnits="userSpaceOnUse" x1="1000" y1="0" x2="1300" y2="0">
  <stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#000"/>
  <animateTransform attributeName="gradientTransform" type="translate" from="-1320 0" to="0 0" dur="2.6s"
    calcMode="spline" keyTimes="0;1" keySplines="0.32 0 0.15 1" fill="freeze"/>
</linearGradient>
<mask id="wm{u}" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{h}"><rect width="{W}" height="{h}" fill="url(#wipe{u})"/></mask>
<linearGradient id="band{u}" x1="0" y1="0" x2="1" y2="0">
  <stop offset="0" stop-color="{c['band']}" stop-opacity="0"/><stop offset="0.5" stop-color="{c['band']}" stop-opacity="{c['band_op']}"/><stop offset="1" stop-color="{c['band']}" stop-opacity="0"/>
</linearGradient>''')
    name_y, size = 226, 72
    name_kw = dict(font="serif", anchor="middle", ls=1.5)
    name_fill = x.t("Javohir Abduvahhobov", cx, name_y, size, f"url(#nm{u})", **name_kw)
    name_mask = x.t("Javohir Abduvahhobov", cx, name_y, size, "#fff", **name_kw)
    x.defs(f'<mask id="tm{u}" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{h}">{name_mask}</mask>')
    x.css(f"@keyframes sw{u}{{0%{{transform:translateX(-260px) skewX(-18deg)}}34%,100%{{transform:translateX(1180px) skewX(-18deg)}}}}"
          f".sw{u}{{animation:sw{u} 9s ease-in-out 3s infinite}}")
    shimmer = (f'<g mask="url(#tm{u})"><rect class="sw{u}" x="0" y="130" width="150" height="130" fill="url(#band{u})"/></g>')

    # ---- crest -------------------------------------------------------------------------
    x.css(f"@keyframes rot{u}{{to{{transform:rotate(360deg)}}}}@keyframes rotr{u}{{to{{transform:rotate(-360deg)}}}}"
          f".r1{u}{{transform-origin:{cx}px 92px;animation:rot{u} 60s linear infinite}}"
          f".r2{u}{{transform-origin:{cx}px 92px;animation:rotr{u} 42s linear infinite}}")
    crest = f'''<g>
  <circle class="r1{u}" cx="{cx}" cy="92" r="34" fill="none" stroke="{c['gold']}" stroke-opacity="0.55" stroke-dasharray="1 7" stroke-linecap="round" stroke-width="2"/>
  <circle class="r2{u}" cx="{cx}" cy="92" r="27" fill="none" stroke="{c['gold']}" stroke-opacity="0.35" stroke-dasharray="14 9"/>
  <circle cx="{cx}" cy="92" r="21" fill="{c['bg']}" fill-opacity="0.55" stroke="{c['gold']}" stroke-opacity="0.9"/>
  {x.t("JA", cx, 99, 19, c['gold2'] if c['is_dark'] else c['gold'], "serif", anchor="middle", ls=1)}
</g>'''
    crest_lines = (fade_line(x, 130, cx - 52, 92, "cl", 0.7, both=False).replace('x="130"', 'x="130"')
                   + f'<g transform="translate({2*cx} 0) scale(-1 1)">{fade_line(x, 130, cx - 52, 92, "cr", 0.7, both=False)}</g>')

    # ---- subtitle + role carousel --------------------------------------------------------
    sub = x.t("Software developer", cx, 282, 24, c["gold2"] if c["is_dark"] else c["gold"], "serif", anchor="middle", ls=7)
    period = 4.2 * len(ROLES)
    step = 100 / len(ROLES)
    roles, rules = [], []
    for i, r in enumerate(ROLES):
        name = f"ro{u}{i}"
        a, b, cc, d = i * step, i * step + 2.5, (i + 1) * step - 3, (i + 1) * step - 0.4
        pre = f"{a:.2f}%{{opacity:0;transform:translateY(7px)}}"
        rules.append(f"@keyframes {name}{{0%,{a:.2f}%{{opacity:0;transform:translateY(7px)}}{b:.2f}%{{opacity:1;transform:translateY(0)}}"
                     f"{cc:.2f}%{{opacity:1;transform:translateY(0)}}{d:.2f}%{{opacity:0;transform:translateY(-6px)}}100%{{opacity:0}}}}")
        first = "opacity:1;" if i == 0 else "opacity:0;"
        roles.append(x.t(r, cx, 358, 18, c["text2"], "sans", anchor="middle", ls=0.6,
                         style=f"{first}animation:{name} {period}s ease-in-out infinite"))
    for r in rules:
        x.css(r)
    x.reduced.append(f"text[style*='ro{u}0']{{opacity:1!important}}")

    # small static lead-in so the carousel reads as a sentence
    lead = x.t("Currently building", cx, 326, 13, c["text3"], "sansm", anchor="middle", ls=2.4)

    # ---- bottom bar ------------------------------------------------------------------------
    x.css(f"@keyframes ping{u}{{from{{r:4;opacity:.7}}to{{r:15;opacity:0}}}}.ping{u}{{animation:ping{u} 2.4s ease-out infinite}}")
    by = h - 36
    bar = (hair(40, W - 40, by - 24, c["gold"], 0.2)
           + f'<circle cx="52" cy="{by}" r="4" fill="{c["good"]}"/>'
           + f'<circle class="ping{u}" cx="52" cy="{by}" r="4" fill="none" stroke="{c["good"]}" stroke-width="1.4"/>'
           + x.t("github.com/javohir-io", 68, by + 4.5, 13.5, c["text2"], "sans", ls=0.3)
           + x.t("B.Sc. Software Engineering, Turin Polytechnic University in Tashkent", W - 40, by + 4.5, 13.5, c["text3"], "sans",
                 anchor="end", ls=0.3))

    # ---- glints ---------------------------------------------------------------------------
    glints = sparkles(x, [(150, 120), (842, 140), (250, 300), (760, 296), (95, 232), (910, 228)], seed=5)

    body = "\n".join([
        frame(x, r=6),
        f'<g clip-path="url(#clip{u})">{dust(x, 30, seed=11, y1=h-70)}</g>',
        crest_lines, crest,
        f'<g mask="url(#wm{u})">{name_fill}</g>',
        shimmer,
        glints,
        sub, lead, "".join(roles),
        bar,
        border(x, r=6, chase=True),
    ])
    return x.render(body)
