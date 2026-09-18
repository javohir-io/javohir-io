# -*- coding: utf-8 -*-
import os, html

OUT_LIGHT = "/home/claude/readme-pkg/assets"
OUT_DARK  = "/home/claude/readme-pkg/assets/dark"
os.makedirs(OUT_LIGHT, exist_ok=True)
os.makedirs(OUT_DARK, exist_ok=True)

FONT = "'JetBrains Mono','SFMono-Regular','Cascadia Code','Consolas',monospace"
WIDTH = 900

LIGHT = dict(
    ink="#0d1117", muted="#57606a", dim="#8a929c",
    accent="#3b5bfd", accent2="#0f9d78",
    line="#d7dce2", faint="#f0f2f5", panel="#fafbfc",
)
DARK = dict(
    ink="#e6edf3", muted="#9aa4b2", dim="#6b7684",
    accent="#7c9fff", accent2="#3ddba8",
    line="#26303c", faint="#111722", panel="#0c1017",
)

def esc(s):
    return html.escape(s, quote=True)

def tw(s, size, factor=0.605):
    """approximate monospace text width"""
    return len(s) * size * factor

def svg_open(h, w=WIDTH):
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'xmlns="http://www.w3.org/2000/svg" role="img">')

def style_block(c):
    return f'''<style>
text {{ font-family: {FONT}; }}
.ink {{ fill:{c["ink"]}; }}
.muted {{ fill:{c["muted"]}; }}
.dim {{ fill:{c["dim"]}; }}
.accent {{ fill:{c["accent"]}; }}
.accent2 {{ fill:{c["accent2"]}; }}
.line {{ stroke:{c["line"]}; }}
</style>'''

def ruler(c, y, w=WIDTH, x0=0, step=14, tick=5):
    """thin horizontal ruler with tick marks, signature motif"""
    parts = [f'<line x1="{x0}" y1="{y}" x2="{x0+w}" y2="{y}" class="line" stroke-width="1"/>']
    n = int(w // step)
    for i in range(n + 1):
        x = x0 + i * step
        h = tick if i % 5 == 0 else tick * 0.5
        parts.append(f'<line x1="{x}" y1="{y}" x2="{x}" y2="{y+h}" class="line" stroke-width="1"/>')
    return "\n".join(parts)

def section_tag(c, num, slug, x=32, y=40):
    """small module-path style section marker e.g. 01.whoami"""
    return f'''<rect x="{x}" y="{y-14}" width="7" height="7" class="accent" fill="{c["accent"]}"/>
<text x="{x+16}" y="{y}" font-size="13" class="muted" letter-spacing="0.5">{num}.{esc(slug)}</text>'''

def pill(c, x, y, label, h=24, fs=12.5, pad=10, fg=None, border=None):
    w = tw(label, fs) + pad * 2
    fg = fg or c["ink"]
    border = border or c["line"]
    return (f'<rect x="{x}" y="{y}" width="{w:.1f}" height="{h}" rx="4" '
            f'fill="{c["faint"]}" stroke="{border}" stroke-width="1"/>'
            f'<text x="{x+pad}" y="{y+h/2+4.5}" font-size="{fs}" fill="{fg}">{esc(label)}</text>'), w

def pill_row(c, items, x0, y0, max_w, gap=8, row_gap=10, h=24, fs=12.5):
    out = []
    x, y = x0, y0
    for label in items:
        svg, w = pill(c, x, y, label)
        if x + w > x0 + max_w:
            x = x0
            y += h + row_gap
            svg, w = pill(c, x, y, label)
        out.append(svg)
        x += w + gap
    return "\n".join(out), y + h

# ---------------------------------------------------------------- HEADER
def header_svg(c):
    h = 208
    s = [svg_open(h), style_block(c)]
    s.append(f'<rect x="0" y="0" width="{WIDTH}" height="{h}" fill="none"/>')
    # left: name block
    s.append(f'<text x="32" y="58" font-size="15" class="accent" letter-spacing="1">// engineering profile</text>')
    s.append(f'<text x="32" y="100" font-size="34" font-weight="700" class="ink">Javohir Abduvahhobov</text>')
    s.append(f'<text x="32" y="128" font-size="15" class="muted">Full-stack &amp; Mobile Developer <tspan class="dim">/</tspan> ML &amp; DL Student</text>')
    s.append(f'<text x="32" y="154" font-size="12.5" class="dim">Flutter · Node.js · React · PostgreSQL · Python</text>')
    # terminal window motif, right side
    tx, ty, tw_, th_ = 560, 48, 308, 118
    s.append(f'<rect x="{tx}" y="{ty}" width="{tw_}" height="{th_}" rx="8" fill="{c["panel"]}" stroke="{c["line"]}" stroke-width="1"/>')
    s.append(f'<rect x="{tx}" y="{ty}" width="{tw_}" height="24" rx="8" fill="{c["faint"]}" stroke="{c["line"]}" stroke-width="1"/>')
    s.append(f'<rect x="{tx}" y="{ty+12}" width="{tw_}" height="12" fill="{c["faint"]}"/>')
    for i, col in enumerate([c["muted"], c["muted"], c["accent2"]]):
        s.append(f'<circle cx="{tx+18+i*16}" cy="{ty+12}" r="4.5" fill="{col}"/>')
    s.append(f'<text x="{tx+tw_/2}" y="{ty+16}" font-size="10.5" class="dim" text-anchor="middle">~/javohir-io</text>')
    lines = ["$ whoami", "javohir_abduvahhobov", "$ status --check", "building · shipping · learning"]
    for i, ln in enumerate(lines):
        col = 'class="accent2"' if ln.startswith("$") else 'class="muted"'
        s.append(f'<text x="{tx+18}" y="{ty+50+i*18}" font-size="12" {col}>{esc(ln)}</text>')
    s.append(f'<rect x="{tx+18}" y="{ty+50+3*18-11}" width="7" height="13" class="accent2" fill="{c["accent2"]}" opacity="0.85"/>')
    s.append(ruler(c, h - 1))
    s.append("</svg>")
    return "\n".join(s)

# ---------------------------------------------------------------- WHOAMI
def whoami_svg(c):
    h = 260
    s = [svg_open(h), style_block(c)]
    s.append(section_tag(c, "01", "whoami"))
    bio = [
        "Software engineer who builds products end-to-end \u2014 from the Flutter",
        "screen a user taps, through the API that authenticates them, down to",
        "the PostgreSQL schema underneath. Currently studying Machine Learning,",
        "Deep Learning &amp; Data Mining at university alongside shipping full-stack",
        "apps and the occasional game.",
    ]
    for i, ln in enumerate(bio):
        s.append(f'<text x="32" y="{72+i*22}" font-size="14.5" class="ink">{ln}</text>')
    facts = [("role", "full-stack & mobile developer"), ("focus", "flutter . node.js . react"),
             ("studying", "machine learning / deep learning / data mining"), ("based", "tashkent, uz")]
    fy = 72 + len(bio) * 22 + 22
    s.append(f'<line x1="32" y1="{fy-16}" x2="{WIDTH-32}" y2="{fy-16}" class="line" stroke-width="1"/>')
    fx, frow_y, max_w = 32, fy + 6, WIDTH - 64
    for k, v in facts:
        label = f'{k}:'
        pair_w = tw(label, 12.5) + 8 + tw(v, 12.5)
        if fx + pair_w > 32 + max_w:
            fx = 32
            frow_y += 24
        s.append(f'<text x="{fx}" y="{frow_y}" font-size="12.5" class="accent">{esc(label)}</text>')
        s.append(f'<text x="{fx+tw(label,12.5)+8}" y="{frow_y}" font-size="12.5" class="muted">{esc(v)}</text>')
        fx += pair_w + 34
    s.append(ruler(c, h - 1))
    s.append("</svg>")
    return "\n".join(s)

# ---------------------------------------------------------------- ECOSYSTEM
def box(c, x, y, w, h, title, sub=None, accent=False):
    stroke = c["accent"] if accent else c["line"]
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="6" fill="{c["panel"]}" stroke="{stroke}" stroke-width="1.2"/>']
    out.append(f'<text x="{x+w/2}" y="{y+h/2 - (6 if sub else -4)}" font-size="13" class="ink" text-anchor="middle" font-weight="600">{esc(title)}</text>')
    if sub:
        out.append(f'<text x="{x+w/2}" y="{y+h/2+14}" font-size="10.5" class="dim" text-anchor="middle">{esc(sub)}</text>')
    return "\n".join(out)

def arrow(c, x1, y1, x2, y2, label=None, dashed=False, lx=None, ly=None):
    dash = ' stroke-dasharray="4,3"' if dashed else ""
    out = [f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c["muted"]}" stroke-width="1.2"{dash}/>']
    # arrow head
    import math
    ang = math.atan2(y2 - y1, x2 - x1)
    hl = 6
    for da in (0.5, -0.5):
        hx = x2 - hl * (1) * (0.9) * (1)
    ax1 = x2 - hl * (1) * (1)
    out.append(f'<path d="M {x2} {y2} l {-hl*1.4:.1f} {-4:.1f} l 0 {8:.1f} z" fill="{c["muted"]}"/>' if x2 > x1 else
                f'<path d="M {x2} {y2} l {hl*1.4:.1f} {-4:.1f} l 0 {8:.1f} z" fill="{c["muted"]}"/>')
    if label:
        out.append(f'<rect x="{(lx if lx is not None else (x1+x2)/2-16)}" y="{(ly if ly is not None else (y1+y2)/2-9)}" width="{tw(label,10.5)+10}" height="15" fill="{c["faint"]}"/>')
        out.append(f'<text x="{(lx if lx is not None else (x1+x2)/2-16)+5}" y="{(ly if ly is not None else (y1+y2)/2-9)+11}" font-size="10.5" class="dim">{esc(label)}</text>')
    return "\n".join(out)

def ecosystem_svg(c):
    h = 380
    s = [svg_open(h), style_block(c)]
    s.append(section_tag(c, "02", "ecosystem"))
    s.append(f'<text x="32" y="66" font-size="12.5" class="muted">system map \u2014 how the pieces talk to each other</text>')

    bw, bh, by = 150, 54, 92
    x_mobile, x_api, x_db = 60, 300, 560
    s.append(box(c, x_mobile, by, bw, bh, "MOBILE CLIENT", "flutter / dart", accent=True))
    s.append(box(c, x_api, by, bw, bh, "REST API", "node.js / express", accent=True))
    s.append(box(c, x_db, by, bw, bh, "POSTGRESQL", "5 relational tables"))
    s.append(arrow(c, x_mobile+bw, by+bh/2, x_api, by+bh/2, "http + jwt"))
    s.append(arrow(c, x_api+bw, by+bh/2, x_db, by+bh/2, "pg pool"))

    # admin panel below api, arrow upward
    ax, ay = 300, by + bh + 46
    s.append(box(c, ax, ay, bw, 44, "ADMIN PANEL", "html / css / js"))
    s.append(arrow(c, ax+bw/2, ay, ax+bw/2, by+bh, "rest"))

    # db schema note
    s.append(f'<text x="{x_db}" y="{by+bh+22}" font-size="10" class="dim">users . jobs . saved_jobs . applications . interviews</text>')

    # side tracks: web + ml, separated by dashed divider
    dy = ay + 44 + 34
    s.append(f'<line x1="32" y1="{dy}" x2="{WIDTH-32}" y2="{dy}" class="line" stroke-width="1" stroke-dasharray="3,4"/>')
    s.append(f'<text x="32" y="{dy+22}" font-size="11" class="dim">parallel tracks \u2014 separate from the api above</text>')
    ty2 = dy + 34
    s.append(box(c, 60, ty2, 190, 44, "WEB CLIENT", "react + typescript"))
    s.append(box(c, 300, ty2, 190, 44, "ML / DL / DATA MINING", "python . coursework + research"))
    s.append(box(c, 560, ty2, 190, 44, "MOBILE GAME", "flutter / dart"))

    s.append(ruler(c, h - 1))
    s.append("</svg>")
    return "\n".join(s)

# ---------------------------------------------------------------- PROJECTS
def project_card(c, x, y, w, h, tag, title, desc_lines, stack_items, link):
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{c["panel"]}" stroke="{c["line"]}" stroke-width="1"/>']
    out.append(f'<rect x="{x}" y="{y}" width="4" height="{h}" fill="{c["accent"]}" rx="2"/>')
    out.append(f'<text x="{x+22}" y="{y+30}" font-size="10.5" class="dim" letter-spacing="0.5">{esc(tag)}</text>')
    out.append(f'<text x="{x+22}" y="{y+54}" font-size="16" class="ink" font-weight="700">{esc(title)}</text>')
    ly = y + 78
    for ln in desc_lines:
        out.append(f'<text x="{x+22}" y="{ly}" font-size="12" class="muted">{esc(ln)}</text>')
        ly += 18
    ly += 4
    row, ly2 = pill_row(c, stack_items, x+22, ly, w-44, h=20, fs=10.5, gap=6, row_gap=8)
    out.append(row)
    out.append(f'<text x="{x+22}" y="{y+h-16}" font-size="10.5" class="accent">{esc(link)}</text>')
    return "\n".join(out)

def projects_svg(c):
    h = 300
    s = [svg_open(h), style_block(c)]
    s.append(section_tag(c, "03", "projects"))
    cw = (WIDTH - 64 - 20) / 2
    s.append(project_card(
        c, 32, 56, cw, h - 80, "case 01 / full-stack",
        "JobFlow \u2014 Job Application Platform",
        ["Flutter app + Node/Express API + Postgres.",
         "JWT auth, resume uploads, interview calendar,",
         "and a plain-JS admin panel on the same API."],
        ["Flutter", "Node/Express", "PostgreSQL", "JWT", "Multer", "Admin Panel"],
        "view repo \u2192 github.com/javohir-io",
    ))
    s.append(project_card(
        c, 32 + cw + 20, 56, cw, h - 80, "case 02 / game dev",
        "Flutter Arcade Game",
        ["A mobile game built solo with Flutter & Dart.",
         "Custom game loop and UI, no external game",
         "engine \u2014 just the framework and the logic."],
        ["Flutter", "Dart", "Game Loop", "Custom UI"],
        "view repo \u2192 github.com/javohir-io",
    ))
    s.append(ruler(c, h - 1))
    s.append("</svg>")
    return "\n".join(s)

# ---------------------------------------------------------------- STACK
def stack_svg(c):
    h = 300
    s = [svg_open(h), style_block(c)]
    s.append(section_tag(c, "04", "stack"))
    groups = [
        ("mobile", ["Flutter", "Dart", "http", "shared_preferences", "file_picker", "google_fonts", "intl", "cupertino_icons"]),
        ("backend", ["Node.js", "Express", "JWT", "bcryptjs", "multer", "cors", "morgan", "dotenv", "uuid", "pg"]),
        ("web & admin", ["React", "TypeScript", "HTML", "CSS", "JavaScript"]),
        ("data & ml", ["PostgreSQL", "Python", "Machine Learning", "Deep Learning", "Data Mining"]),
        ("also", ["Kotlin", "C", "Android Studio", "Git", "GitHub", "npm"]),
    ]
    y = 58
    for label, items in groups:
        s.append(f'<text x="32" y="{y+13}" font-size="11" class="accent" letter-spacing="0.5">{esc(label)}</text>')
        row, y2 = pill_row(c, items, 130, y, WIDTH - 130 - 32, h=22, fs=11, gap=6, row_gap=8)
        s.append(row)
        y = y2 + 12
    s.append(ruler(c, h - 1))
    s.append("</svg>")
    return "\n".join(s)

# ---------------------------------------------------------------- PHILOSOPHY
def philosophy_svg(c):
    h = 148
    s = [svg_open(h), style_block(c)]
    s.append(f'<text x="32" y="56" font-size="46" class="accent" font-weight="700" opacity="0.5">\u201c</text>')
    s.append(f'<text x="70" y="58" font-size="20" class="ink" font-weight="700">Ship the full stack, not just the feature.</text>')
    s.append(f'<text x="70" y="88" font-size="13" class="muted">Prototype fast, refactor with intent \u2014 and treat every layer,</text>')
    s.append(f'<text x="70" y="108" font-size="13" class="muted">from the schema to the screen, as worth getting right.</text>')
    s.append(ruler(c, h - 1))
    s.append("</svg>")
    return "\n".join(s)

# ---------------------------------------------------------------- FOOTER
def footer_svg(c):
    h = 108
    s = [svg_open(h), style_block(c)]
    s.append(f'<circle cx="40" cy="40" r="5" fill="{c["accent2"]}"/>')
    s.append(f'<text x="56" y="45" font-size="13.5" class="ink">currently: sharpening Flutter + Node, exploring more ML-driven side projects</text>')
    s.append(f'<text x="40" y="76" font-size="12" class="muted">thanks for scrolling \u2014 open to collaborate, always happy to talk shop.</text>')
    s.append(f'<text x="{WIDTH-32}" y="76" font-size="11" class="dim" text-anchor="end">// EOF</text>')
    s.append("</svg>")
    return "\n".join(s)

BANNERS = {
    "header.svg": header_svg,
    "whoami.svg": whoami_svg,
    "ecosystem.svg": ecosystem_svg,
    "projects.svg": projects_svg,
    "stack.svg": stack_svg,
    "philosophy.svg": philosophy_svg,
    "footer.svg": footer_svg,
}

for fname, fn in BANNERS.items():
    with open(os.path.join(OUT_LIGHT, fname), "w") as f:
        f.write(fn(LIGHT))
    with open(os.path.join(OUT_DARK, fname), "w") as f:
        f.write(fn(DARK))

print("done", os.listdir(OUT_LIGHT))
