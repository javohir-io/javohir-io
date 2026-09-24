# -*- coding: utf-8 -*-
from common import (WIDTH, MONO, SANS, esc, svg_open, frame_defs, decode_text,
                     rain_columns, panel_rain, chip, CHIP_PULSE_CSS)

ROLES = ["Flutter Developer", "Node.js Backend Engineer", "React & TypeScript Dev", "Software Engineer"]
GLITCH = dict(cycle=3.0, steps=5, gap=0.25)  # shared ~3s glitch cadence for every label


def header_svg(c, theme):
    h = 320
    uid = "hdr"
    css_rain, rain_svg = rain_columns(uid, 1 if theme == "dark" else 2, c["rain_head"], c["rain_body"], WIDTH, h, n_cols=46, rows=10)
    css_name, name_svg = decode_text(uid, "name", "JAVOHIR ABDUVAHHOBOV", WIDTH/2, h/2 - 6, 42,
                                      c["text"], c["accent"], anchor="middle", spacing="1.5",
                                      seed=101, **GLITCH)

    role_css, role_svg = [], []
    period = 8.0
    step = period / len(ROLES)
    for i, role in enumerate(ROLES):
        delay = -round(i * step, 3)
        name = f"role{uid}{i}"
        role_css.append(f'''@keyframes {name}{{
          0%{{opacity:0}} 2%{{opacity:1}} {step/period*100-6:.1f}%{{opacity:1}} {step/period*100-2:.1f}%{{opacity:0}} 100%{{opacity:0}}
        }}''')
        role_svg.append(
            f'<text x="{WIDTH/2}" y="{h/2+34}" text-anchor="middle" font-family="{MONO}" font-size="15" '
            f'letter-spacing="2" fill="{c["text2"]}" style="animation:{name} {period}s linear {delay}s infinite">'
            f'&gt; {esc(role)}</text>'
        )

    return f'''{svg_open(h, title="Javohir Abduvahhobov — header")}
  <style>
    {css_rain}
    {css_name}
    {"".join(role_css)}
    @keyframes blink{uid}{{0%,45%{{opacity:1}}50%,95%{{opacity:0}}100%{{opacity:1}}}}
    .dot{uid}{{animation:blink{uid} 1.4s steps(1) infinite}}
    @keyframes spin{uid}{{from{{transform:rotate(0)}}to{{transform:rotate(360deg)}}}}
    .ring{uid}{{animation:spin{uid} 7s linear infinite;transform-origin:{WIDTH-60}px 54px}}
    @keyframes cursor{uid}{{0%,50%{{opacity:1}}51%,100%{{opacity:0}}}}
    .cur{uid}{{animation:cursor{uid} 1s steps(1) infinite}}
  </style>
  {frame_defs(c, uid, WIDTH, h)}
  <g clip-path="url(#clip{uid})">
    {rain_svg}
    <rect x="0" y="0" width="{WIDTH}" height="{h}" fill="{c['bg']}" opacity="0.08"/>
  </g>

  <circle class="dot{uid}" cx="34" cy="34" r="4" fill="{c['good']}"/>
  <text x="46" y="38" font-family="{MONO}" font-size="12.5" letter-spacing="1.5" fill="{c['text2']}">SYSTEM ONLINE</text>

  <g class="ring{uid}" stroke="{c['accent']}" fill="none" opacity="0.55">
    <circle cx="{WIDTH-60}" cy="54" r="16" stroke-dasharray="6 10"/>
  </g>
  <circle cx="{WIDTH-60}" cy="54" r="3" fill="{c['accent']}"/>

  {name_svg}
  {"".join(role_svg)}

  <text x="34" y="{h-24}" font-family="{MONO}" font-size="13" fill="{c['text3']}">root@javohir:~$ whoami<tspan class="cur{uid}">_</tspan></text>
  <text x="{WIDTH-34}" y="{h-24}" text-anchor="end" font-family="{MONO}" font-size="12.5" fill="{c['text3']}">BSc Software Engineering</text>
</svg>'''


def whoami_svg(c, theme):
    h = 230
    uid = "who"
    css_rain, rain_svg = panel_rain(uid, 11, c, WIDTH, h, n_cols=30, opacity=0.10)
    label_css, label_svg = decode_text(uid, "lbl", "01 // WHOAMI", 34, 44, 15, c["accent"], c["text3"],
                                        anchor="start", spacing="2", seed=201, **GLITCH)

    lines = [
        "Full-stack & mobile engineer who ships the whole pipeline —",
        "Flutter on the client, a Node.js/Express REST API in the middle,",
        "PostgreSQL underneath, and a lightweight admin panel wired to it all.",
    ]
    para_css, para_svg = [], []
    for i, line in enumerate(lines):
        pcss, psvg = decode_text(uid, f"p{i}", line, 34, 90 + i * 26, 16.5, c["text"], c["text3"],
                                  anchor="start", weight="500", seed=300 + i, **GLITCH)
        para_css.append(pcss)
        para_svg.append(psvg)

    tags = ["BSc Software Engineering", "Mobile + Backend + DB + Admin", "Open to opportunities"]
    chip_css, tag_svg = [], []
    tx = 34
    ty = h - 40
    for i, t in enumerate(tags):
        ccss, el, w = chip(c, tx, ty - 14, t, uid=uid, key=f"tag{i}", dur=3.0 + i * 0.3, seed=500 + i)
        chip_css.append(ccss)
        tag_svg.append(el)
        tx += w + 12

    return f'''{svg_open(h, title="whoami")}
  <style>
    {css_rain}
    {label_css}
    {"".join(para_css)}
    {"".join(chip_css)}
  </style>
  {frame_defs(c, uid, WIDTH, h)}
  <g clip-path="url(#clip{uid})">{rain_svg}</g>
  {label_svg}
  <line x1="34" y1="56" x2="{WIDTH-34}" y2="56" stroke="{c['border']}" stroke-width="1"/>
  {"".join(para_svg)}
  {"".join(tag_svg)}
</svg>'''


def ecosystem_svg(c, theme):
    h = 420
    uid = "eco"
    css_rain, rain_svg = panel_rain(uid, 12, c, WIDTH, h, n_cols=34, opacity=0.08)
    label_css, label_svg = decode_text(uid, "lbl", "02 // ECOSYSTEM", 34, 44, 15, c["accent"], c["text3"],
                                        anchor="start", spacing="2", seed=401, **GLITCH)

    box_css = []

    def box(key, x, y, w, bh, title, sub):
        tcss, tsvg = decode_text(uid, f"bt{key}", title, x + w/2, y + bh/2 - 3, 14, c["text"], c["accent"],
                                  anchor="middle", weight="700", seed=hash(key) & 0xffff, **GLITCH)
        scss, ssvg = decode_text(uid, f"bs{key}", sub, x + w/2, y + bh/2 + 16, 11, c["text3"], c["accent2"],
                                  anchor="middle", weight="500", seed=(hash(key) + 1) & 0xffff, **GLITCH)
        box_css.append(tcss)
        box_css.append(scss)
        return f'''<g>
      <rect x="{x}" y="{y}" width="{w}" height="{bh}" rx="10" fill="{c['chip_bg']}" stroke="{c['border']}" stroke-width="1.3"/>
      {tsvg}
      {ssvg}
    </g>'''

    def flow(path_id, d, delay=0.0):
        return f'''
    <path id="{path_id}" d="{d}" fill="none" stroke="{c['accent']}" stroke-width="1.6" stroke-dasharray="4 6" opacity="0.6">
      <animate attributeName="stroke-dashoffset" from="40" to="0" dur="1.6s" repeatCount="indefinite"/>
    </path>
    <circle r="3" fill="{c['accent2']}">
      <animateMotion dur="2.6s" begin="{delay}s" repeatCount="indefinite">
        <mpath xlink:href="#{path_id}"/>
      </animateMotion>
    </circle>'''

    flutter = box("flu", 40, 110, 190, 74, "FLUTTER APP", "Dart • http • file_picker")
    api = box("api", 300, 110, 190, 74, "EXPRESS API", "JWT • bcryptjs • multer")
    db = box("db", 560, 110, 190, 74, "POSTGRESQL", "users • jobs • interviews")
    admin = box("adm", 300, 250, 190, 74, "ADMIN PANEL", "HTML • CSS • JS")
    docker = f'''<rect x="270" y="86" width="510" height="260" rx="14" fill="none" stroke="{c['border']}" stroke-width="1" stroke-dasharray="3 6" opacity="0.6"/>
    <text x="290" y="104" font-family="{MONO}" font-size="11" letter-spacing="1.5" fill="{c['text3']}">DOCKERIZED</text>'''

    flows = (
        flow("f1eco", "M230,147 H300", 0)
        + flow("f2eco", "M490,147 H560", 0.4)
        + flow("f3eco", "M395,184 V250", 0.8)
    )

    auth_note = f'<text x="265" y="140" text-anchor="end" font-family="{MONO}" font-size="10.5" fill="{c["text3"]}">JWT ➜</text>'
    resumes_note = f'<text x="405" y="230" font-family="{MONO}" font-size="10.5" fill="{c["text3"]}">multer</text>'
    legend = (f'<text x="34" y="{h-24}" font-family="{MONO}" font-size="11.5" fill="{c["text3"]}">'
              f'client → REST API → relational store, admin panel talks to the same API, containers via Docker</text>')

    return f'''{svg_open(h, title="ecosystem")}
  <style>
    {css_rain}
    {label_css}
    {"".join(box_css)}
  </style>
  {frame_defs(c, uid, WIDTH, h)}
  <g clip-path="url(#clip{uid})">{rain_svg}</g>
  {label_svg}
  <line x1="34" y1="56" x2="{WIDTH-34}" y2="56" stroke="{c['border']}" stroke-width="1"/>
  {docker}
  {flows}
  {flutter}
  {api}
  {db}
  {admin}
  {auth_note}
  {resumes_note}
  {legend}
</svg>'''


STACK_GROUPS = [
    ("MOBILE — FLUTTER APP", ["Flutter", "Dart", "http", "shared_preferences", "file_picker", "google_fonts", "intl", "cupertino_icons"]),
    ("BACKEND — NODE.JS API", ["Node.js", "Express", "JWT", "bcryptjs", "multer", "cors", "morgan", "dotenv", "uuid", "pg"]),
    ("DATABASE", ["PostgreSQL"]),
    ("ADMIN PANEL", ["HTML", "CSS", "JavaScript"]),
    ("FRONTEND / OTHER", ["React", "TypeScript", "Python"]),
    ("DEV TOOLS & WORKFLOW", ["npm", "Git", "GitHub", "Docker"]),
]


def stack_svg(c, theme):
    row_h = 62
    h = 70 + row_h * len(STACK_GROUPS)
    uid = "stk"
    css_rain, rain_svg = panel_rain(uid, 13, c, WIDTH, h, n_cols=34, opacity=0.07)
    label_css, label_svg = decode_text(uid, "lbl", "03 // STACK", 34, 44, 15, c["accent"], c["text3"],
                                        anchor="start", spacing="2", seed=501, **GLITCH)
    rows = []
    chip_css = []
    y = 78
    for gi, (group, items) in enumerate(STACK_GROUPS):
        gcss, gsvg = decode_text(uid, f"grp{gi}", group, 34, y, 12, c["text3"], c["accent"],
                                  anchor="start", weight="600", spacing="1.5", seed=600 + gi, **GLITCH)
        chip_css.append(gcss)
        rows.append(gsvg)
        x = 34
        cy = y + 16
        for ii, item in enumerate(items):
            ccss, el, w = chip(c, x, cy, item, uid=uid, key=f"g{gi}i{ii}",
                                dur=3.0 + (ii % 3) * 0.2, seed=700 + gi * 20 + ii)
            chip_css.append(ccss)
            rows.append(el)
            x += w + 10
        y += row_h
    return f'''{svg_open(h, title="stack")}
  <style>
    {css_rain}
    {label_css}
    {"".join(chip_css)}
  </style>
  {frame_defs(c, uid, WIDTH, h)}
  <g clip-path="url(#clip{uid})">{rain_svg}</g>
  {label_svg}
  <line x1="34" y1="56" x2="{WIDTH-34}" y2="56" stroke="{c['border']}" stroke-width="1"/>
  {"".join(rows)}
</svg>'''


def transmission_svg(c, theme, email="javohirabduvahhobov@gmail.com"):
    h = 190
    uid = "tra"
    css_rain, rain_svg = panel_rain(uid, 14, c, WIDTH, h, n_cols=30, opacity=0.09)
    label_css, label_svg = decode_text(uid, "lbl", "04 // OPEN A CHANNEL", 34, 44, 15, c["accent"], c["text3"],
                                        anchor="start", spacing="2", seed=601, **GLITCH)
    status_css, status_svg = decode_text(uid, "status", "AVAILABLE FOR OPPORTUNITIES", 78, 105, 12.5,
                                          c["good"], c["accent"], anchor="start", weight="600",
                                          spacing="1.5", seed=602, **GLITCH)
    email_css, email_svg = decode_text(uid, "email", email, 34, 150, 22, c["text"], c["accent"],
                                        anchor="start", weight="700", seed=603, **GLITCH)

    ping = f'''<circle cx="52" cy="100" r="4" fill="{c['good']}"/>
    <circle cx="52" cy="100" r="4" fill="none" stroke="{c['good']}" stroke-width="1.5">
      <animate attributeName="r" from="4" to="18" dur="2.2s" repeatCount="indefinite"/>
      <animate attributeName="opacity" from="0.8" to="0" dur="2.2s" repeatCount="indefinite"/>
    </circle>'''

    return f'''{svg_open(h, title="contact")}
  <style>
    {css_rain}
    {label_css}
    {status_css}
    {email_css}
  </style>
  {frame_defs(c, uid, WIDTH, h)}
  <g clip-path="url(#clip{uid})">{rain_svg}</g>
  {label_svg}
  <line x1="34" y1="56" x2="{WIDTH-34}" y2="56" stroke="{c['border']}" stroke-width="1"/>
  {ping}
  {status_svg}
  <a xlink:href="mailto:{email}">{email_svg}</a>
  <text x="{WIDTH-34}" y="150" text-anchor="end" font-family="{MONO}" font-size="13" fill="{c['text3']}">reply time: usually &lt; 24h</text>
</svg>'''


def soundtrack_svg(c, theme, track="We Do What We Want (Edit)", artist="Alan Fitzpatrick",
                    url="https://open.spotify.com/track/2qGvgsRsmrB0Y7Y4MmuP1M"):
    h = 130
    uid = "snd"
    css_rain, rain_svg = panel_rain(uid, 15, c, WIDTH, h, n_cols=30, opacity=0.08)
    title_css, title_svg = decode_text(uid, "title", track, 96, 62, 17, c["text"], c["accent"],
                                        anchor="start", weight="700", seed=801, **GLITCH)
    artist_css, artist_svg = decode_text(uid, "artist", artist, 96, 82, 13, c["text2"], c["accent2"],
                                          anchor="start", weight="500", seed=802, **GLITCH)

    # spinning vinyl record
    vinyl = f'''<g style="transform-origin:52px 65px;animation:spin{uid} 4s linear infinite">
      <circle cx="52" cy="65" r="26" fill="{c['bg2']}" stroke="{c['border']}" stroke-width="1.4"/>
      <circle cx="52" cy="65" r="20" fill="none" stroke="{c['border']}" stroke-width="0.8"/>
      <circle cx="52" cy="65" r="15" fill="none" stroke="{c['border']}" stroke-width="0.8"/>
      <circle cx="52" cy="65" r="8" fill="{c['accent']}"/>
      <circle cx="52" cy="65" r="2.2" fill="{c['bg']}"/>
    </g>'''

    # small equalizer bars
    bars = []
    heights = [10, 20, 14, 24, 8, 18]
    for i, base in enumerate(heights):
        x = WIDTH - 210 + i * 14
        dur = 0.6 + (i % 3) * 0.15
        bars.append(f'''<rect x="{x}" y="{h/2 - base/2}" width="7" height="{base}" rx="2" fill="{c['accent']}" opacity="0.85"
        style="transform-origin:{x+3.5}px {h/2}px;animation:eq{uid}{i} {dur}s ease-in-out infinite alternate"/>''')
        pass
    eq_css = "\n".join(
        f"@keyframes eq{uid}{i}{{from{{transform:scaleY(0.35)}}to{{transform:scaleY(1)}}}}" for i in range(len(heights))
    )

    click = f'<text x="{WIDTH-34}" y="{h-22}" text-anchor="end" font-family="{MONO}" font-size="12" letter-spacing="1" fill="{c["accent"]}">▶ click to play</text>'

    body = f'''{svg_open(h, title="soundtrack")}
  <style>
    {css_rain}
    {title_css}
    {artist_css}
    {eq_css}
    @keyframes spin{uid}{{from{{transform:rotate(0)}}to{{transform:rotate(360deg)}}}}
  </style>
  {frame_defs(c, uid, WIDTH, h, radius=16)}
  <g clip-path="url(#clip{uid})">{rain_svg}</g>
  {vinyl}
  <text x="34" y="40" font-family="{MONO}" font-size="11" letter-spacing="1.5" fill="{c['text3']}">SOUNDTRACK</text>
  {title_svg}
  {artist_svg}
  {"".join(bars)}
  {click}
</svg>'''
    return body, url


def footer_svg(c, theme):
    h = 150
    uid = "ftr"
    css_rain, rain_svg = rain_columns(uid, 3 if theme == "dark" else 4, c["rain_head"], c["rain_body"], WIDTH, h, n_cols=44, rows=8)
    css_txt, txt_svg = decode_text(uid, "end", "// THANKS FOR SCROLLING — LET'S BUILD SOMETHING", WIDTH/2, h/2 + 6, 15,
                                    c["text2"], c["accent"], anchor="middle", spacing="1", seed=701, **GLITCH)
    return f'''{svg_open(h, title="footer")}
  <style>
    {css_rain}
    {css_txt}
    @keyframes cur{uid}{{0%,50%{{opacity:1}}51%,100%{{opacity:0}}}}
  </style>
  {frame_defs(c, uid, WIDTH, h, radius=16)}
  <g clip-path="url(#clip{uid})" opacity="0.55">{rain_svg}</g>
  {txt_svg}
</svg>'''


def divider_svg(c, theme):
    h = 20
    uid = "div"
    return f'''<svg width="{WIDTH}" height="{h}" viewBox="0 0 {WIDTH} {h}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="dg{uid}" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="{c['accent']}" stop-opacity="0"/>
      <stop offset="50%" stop-color="{c['accent']}" stop-opacity="0.9"/>
      <stop offset="100%" stop-color="{c['accent']}" stop-opacity="0"/>
    </linearGradient>
  </defs>
  <style>
    @keyframes slide{uid}{{0%{{transform:translateX(-40%)}}100%{{transform:translateX(40%)}}}}
    .sweep{uid}{{animation:slide{uid} 3.4s ease-in-out infinite alternate}}
  </style>
  <line x1="0" y1="{h/2}" x2="{WIDTH}" y2="{h/2}" stroke="{c['border']}" stroke-width="1"/>
  <rect class="sweep{uid}" x="{WIDTH*0.3}" y="{h/2-1}" width="{WIDTH*0.4}" height="2" fill="url(#dg{uid})"/>
</svg>'''
