# -*- coding: utf-8 -*-
import os, html, math

OUT_LIGHT = "/home/claude/readme-pkg/assets"
OUT_DARK  = "/home/claude/readme-pkg/assets/dark"
os.makedirs(OUT_LIGHT, exist_ok=True)
os.makedirs(OUT_DARK, exist_ok=True)

SANS = "'Space Grotesk','Segoe UI',Inter,sans-serif"
MONO = "'JetBrains Mono','SFMono-Regular','Cascadia Code',Consolas,monospace"
WIDTH = 900

# ---- a genuinely different palette: tinted violet "console panel", not plain black-on-white / white-on-black
LIGHT = dict(
    ink="#141225", muted="#5b5770", dim="#8b87a3",
    accent="#6851ff", accent2="#0f9d78",
    line="#e2defa", panel="#faf9ff", dot="#eae6fb", shadow="#000000",
)
DARK = dict(
    ink="#eeeafc", muted="#a8a2c6", dim="#6f698c",
    accent="#a996ff", accent2="#3ddba8",
    line="#2a2645", panel="#100e1e", dot="#1c1832", shadow="#000000",
)

def esc(s):
    return html.escape(s, quote=True)

def tw(s, size, factor=0.605, sans=False):
    f = 0.52 if sans else factor
    return len(s) * size * f

def svg_open(h, w=WIDTH):
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'xmlns="http://www.w3.org/2000/svg" role="img">')

def defs_and_style(c, uid):
    return f'''<defs>
<pattern id="dots{uid}" width="15" height="15" patternUnits="userSpaceOnUse">
<circle cx="1.4" cy="1.4" r="1.1" fill="{c["dot"]}"/>
</pattern>
</defs>
<style>
text {{ font-family: {MONO}; }}
.sans {{ font-family: {SANS}; }}
.ink {{ fill:{c["ink"]}; }}
.muted {{ fill:{c["muted"]}; }}
.dim {{ fill:{c["dim"]}; }}
.accent {{ fill:{c["accent"]}; }}
.accent2 {{ fill:{c["accent2"]}; }}
.line {{ stroke:{c["line"]}; }}
</style>'''

def panel(c, h, uid, w=WIDTH, m=4, rx=18):
    pw, ph = w - m * 2, h - m * 2
    out = [f'<rect x="{m}" y="{m}" width="{pw}" height="{ph}" rx="{rx}" fill="{c["panel"]}" stroke="{c["line"]}" stroke-width="1.2"/>']
    out.append(f'<rect x="{m}" y="{m}" width="{pw}" height="{ph}" rx="{rx}" fill="url(#dots{uid})" opacity="0.55"/>')
    out.append(corner_brackets(c, m, m, pw, ph))
    return "\n".join(out)

def corner_brackets(c, x, y, w, h, size=13, inset=9, sw=2):
    pts = [
        (x+inset, y+inset, 1, 1),
        (x+w-inset, y+inset, -1, 1),
        (x+inset, y+h-inset, 1, -1),
        (x+w-inset, y+h-inset, -1, -1),
    ]
    out = []
    for px, py, dx, dy in pts:
        out.append(f'<path d="M {px} {py+size*dy} L {px} {py} L {px+size*dx} {py}" '
                    f'fill="none" stroke="{c["accent"]}" stroke-width="{sw}" stroke-linecap="round" opacity="0.85"/>')
    return "\n".join(out)

def hex_points(cx, cy, r):
    pts = []
    for i in range(6):
        a = math.radians(60 * i - 30)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return " ".join(f"{px:.1f},{py:.1f}" for px, py in pts)

def hex_badge(c, cx, cy, label, r=17):
    return (f'<polygon points="{hex_points(cx,cy,r)}" fill="{c["panel"]}" stroke="{c["accent"]}" stroke-width="1.6"/>'
            f'<text x="{cx}" y="{cy+4.5}" font-size="12.5" text-anchor="middle" class="accent sans" font-weight="700">{esc(label)}</text>')

def section_head(c, num, title, x=40, y=54, sub=None):
    out = [hex_badge(c, x+16, y-6, num)]
    out.append(f'<text x="{x+44}" y="{y}" font-size="19" class="ink sans" font-weight="700">{esc(title)}</text>')
    if sub:
        out.append(f'<text x="{x+44}" y="{y+19}" font-size="11.5" class="dim">{esc(sub)}</text>')
    return "\n".join(out)

def pill(c, x, y, label, h=24, fs=12, pad=10, fg=None):
    w = tw(label, fs) + pad * 2
    fg = fg or c["ink"]
    return (f'<rect x="{x}" y="{y}" width="{w:.1f}" height="{h}" rx="5" '
            f'fill="{c["panel"]}" stroke="{c["line"]}" stroke-width="1"/>'
            f'<text x="{x+pad}" y="{y+h/2+4.2}" font-size="{fs}" fill="{fg}">{esc(label)}</text>'), w

def pill_row(c, items, x0, y0, max_w, gap=7, row_gap=9, h=24, fs=12):
    out, x, y = [], x0, y0
    for label in items:
        svg, w = pill(c, x, y, label, h, fs)
        if x + w > x0 + max_w:
            x = x0
            y += h + row_gap
            svg, w = pill(c, x, y, label, h, fs)
        out.append(svg)
        x += w + gap
    return "\n".join(out), y + h

# ---------------------------------------------------------------- HEADER
def header_svg(c):
    h = 216
    uid = "h"
    s = [svg_open(h), defs_and_style(c, uid), panel(c, h, uid)]
    s.append(f'<circle cx="52" cy="52" r="4" fill="{c["accent2"]}"/>')
    s.append(f'<circle cx="52" cy="52" r="9" fill="none" stroke="{c["accent2"]}" stroke-width="1" opacity="0.5"/>')
    s.append(f'<text x="70" y="57" font-size="12.5" class="accent" letter-spacing="0.5">system online</text>')
    s.append(f'<text x="40" y="100" font-size="32" class="ink sans" font-weight="700">Javohir Abduvahhobov</text>')
    s.append(f'<text x="40" y="126" font-size="14.5" class="muted">Full-stack &amp; Mobile Developer</text>')
    s.append(f'<text x="40" y="150" font-size="12" class="dim">Flutter · Node.js · React · PostgreSQL · Python</text>')
    tx, ty, tw_, th_ = 552, 42, 316, 132
    s.append(f'<rect x="{tx}" y="{ty}" width="{tw_}" height="{th_}" rx="10" fill="{c["dot"]}" opacity="0.4" stroke="{c["line"]}" stroke-width="1"/>')
    s.append(f'<rect x="{tx}" y="{ty}" width="{tw_}" height="26" rx="10" fill="{c["panel"]}" stroke="{c["line"]}" stroke-width="1"/>')
    s.append(f'<rect x="{tx}" y="{ty+13}" width="{tw_}" height="13" fill="{c["panel"]}"/>')
    for i, col in enumerate([c["muted"], c["muted"], c["accent2"]]):
        s.append(f'<circle cx="{tx+20+i*16}" cy="{ty+13}" r="4.5" fill="{col}"/>')
    s.append(f'<text x="{tx+tw_/2}" y="{ty+17}" font-size="10.5" class="dim" text-anchor="middle">javohir-io ~ profile</text>')
    lines = ["$ whoami", "javohir_abduvahhobov", "$ status --check", "shipping · learning · online"]
    for i, ln in enumerate(lines):
        col = 'class="accent2"' if ln.startswith("$") else 'class="muted"'
        s.append(f'<text x="{tx+20}" y="{ty+56+i*20}" font-size="12" {col}>{esc(ln)}</text>')
    s.append(f'<rect x="{tx+20}" y="{ty+56+3*20-11}" width="7" height="13" fill="{c["accent2"]}" opacity="0.85"/>')
    s.append("</svg>")
    return "\n".join(s)

# ---------------------------------------------------------------- WHOAMI
def whoami_svg(c):
    h = 258
    uid = "w"
    s = [svg_open(h), defs_and_style(c, uid), panel(c, h, uid)]
    s.append(section_head(c, "01", "whoami"))
    bio = [
        "Software engineer who builds products end-to-end \u2014 from the Flutter",
        "screen a user taps, through the API that authenticates them, down to",
        "the PostgreSQL schema underneath. Computer science graduate with a",
        "background in Machine Learning, Deep Learning &amp; Data Mining, now",
        "focused on shipping full-stack apps, APIs and the odd game.",
    ]
    for i, ln in enumerate(bio):
        s.append(f'<text x="40" y="{92+i*22}" font-size="13.5" class="ink">{ln}</text>')
    facts = [("role", "full-stack & mobile developer"), ("focus", "flutter . node.js . react"),
             ("background", "ml / deep learning / data mining"), ("based", "tashkent, uz")]
    fy = 92 + len(bio) * 22 + 20
    s.append(f'<line x1="40" y1="{fy-16}" x2="{WIDTH-40}" y2="{fy-16}" class="line" stroke-width="1"/>')
    fx, frow_y, max_w = 40, fy + 6, WIDTH - 80
    for k, v in facts:
        label = f'{k}:'
        pair_w = tw(label, 12.5) + 8 + tw(v, 12.5)
        if fx + pair_w > 40 + max_w:
            fx = 40
            frow_y += 24
        s.append(f'<text x="{fx}" y="{frow_y}" font-size="12.5" class="accent">{esc(label)}</text>')
        s.append(f'<text x="{fx+tw(label,12.5)+8}" y="{frow_y}" font-size="12.5" class="muted">{esc(v)}</text>')
        fx += pair_w + 30
    s.append("</svg>")
    return "\n".join(s)

# ---------------------------------------------------------------- ECOSYSTEM
def box(c, x, y, w, h, title, sub=None, accent=False):
    stroke = c["accent"] if accent else c["line"]
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{c["panel"]}" stroke="{stroke}" stroke-width="1.3"/>']
    out.append(f'<text x="{x+w/2}" y="{y+h/2 - (5 if sub else -4)}" font-size="12.5" class="ink sans" text-anchor="middle" font-weight="700">{esc(title)}</text>')
    if sub:
        out.append(f'<text x="{x+w/2}" y="{y+h/2+14}" font-size="10.5" class="dim" text-anchor="middle">{esc(sub)}</text>')
    return "\n".join(out)

def arrow(c, x1, y1, x2, y2, label=None):
    out = [f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c["accent"]}" stroke-width="1.3" opacity="0.7"/>']
    hl = 6
    if x2 >= x1:
        out.append(f'<path d="M {x2} {y2} l {-hl*1.4:.1f} {-4:.1f} l 0 {8:.1f} z" fill="{c["accent"]}" opacity="0.85"/>')
    else:
        out.append(f'<path d="M {x2} {y2} l {hl*1.4:.1f} {-4:.1f} l 0 {8:.1f} z" fill="{c["accent"]}" opacity="0.85"/>')
    if label:
        lx, ly = (x1+x2)/2 - (tw(label,10.5)+10)/2, (y1+y2)/2 - 9
        out.append(f'<rect x="{lx}" y="{ly}" width="{tw(label,10.5)+10}" height="15" fill="{c["panel"]}"/>')
        out.append(f'<text x="{lx+5}" y="{ly+11}" font-size="10.5" class="dim">{esc(label)}</text>')
    return "\n".join(out)

def ecosystem_svg(c):
    h = 372
    uid = "e"
    s = [svg_open(h), defs_and_style(c, uid), panel(c, h, uid)]
    s.append(section_head(c, "02", "ecosystem", sub="system map \u2014 how the pieces talk to each other"))

    bw, bh, by = 148, 54, 100
    x_mobile, x_api, x_db = 64, 302, 560
    s.append(box(c, x_mobile, by, bw, bh, "MOBILE CLIENT", "flutter / dart", accent=True))
    s.append(box(c, x_api, by, bw, bh, "REST API", "node.js / express", accent=True))
    s.append(box(c, x_db, by, bw, bh, "POSTGRESQL", "5 relational tables"))
    s.append(arrow(c, x_mobile+bw, by+bh/2, x_api, by+bh/2, "http + jwt"))
    s.append(arrow(c, x_api+bw, by+bh/2, x_db, by+bh/2, "pg pool"))

    ax, ay = 302, by + bh + 44
    s.append(box(c, ax, ay, bw, 44, "ADMIN PANEL", "html / css / js"))
    s.append(arrow(c, ax+bw/2, ay, ax+bw/2, by+bh, "rest"))
    s.append(f'<text x="{x_db}" y="{by+bh+22}" font-size="9.5" class="dim">users . jobs . saved_jobs . applications . interviews</text>')

    dy = ay + 44 + 32
    s.append(f'<line x1="40" y1="{dy}" x2="{WIDTH-40}" y2="{dy}" class="line" stroke-width="1" stroke-dasharray="3,4"/>')
    s.append(f'<text x="40" y="{dy+21}" font-size="10.5" class="dim">parallel tracks \u2014 separate from the api above</text>')
    ty2 = dy + 33
    s.append(box(c, 64, ty2, 190, 44, "WEB CLIENT", "react + typescript"))
    s.append(box(c, 356, ty2, 190, 44, "ML / DEEP LEARNING", "python . applied academically"))
    s.append(box(c, 648, ty2, 188, 44, "MOBILE GAME", "flutter / dart"))
    s.append("</svg>")
    return "\n".join(s)

# ---------------------------------------------------------------- STACK
def stack_svg(c):
    h = 300
    uid = "s"
    s = [svg_open(h), defs_and_style(c, uid), panel(c, h, uid)]
    s.append(section_head(c, "03", "stack"))
    groups = [
        ("mobile", ["Flutter", "Dart", "http", "shared_preferences", "file_picker", "google_fonts", "intl", "cupertino_icons"]),
        ("backend", ["Node.js", "Express", "JWT", "bcryptjs", "multer", "cors", "morgan", "dotenv", "uuid", "pg"]),
        ("web & admin", ["React", "TypeScript", "HTML", "CSS", "JavaScript"]),
        ("data & ml", ["PostgreSQL", "Python", "Machine Learning", "Deep Learning", "Data Mining"]),
        ("also", ["Kotlin", "C", "Android Studio", "Git", "GitHub", "npm"]),
    ]
    y = 76
    for label, items in groups:
        s.append(f'<text x="40" y="{y+13}" font-size="10.5" class="accent" letter-spacing="0.5">{esc(label)}</text>')
        row, y2 = pill_row(c, items, 136, y, WIDTH - 136 - 40, h=22, fs=11)
        s.append(row)
        y = y2 + 12
    s.append("</svg>")
    return "\n".join(s)

# ---------------------------------------------------------------- PHILOSOPHY
def philosophy_svg(c):
    h = 156
    uid = "p"
    s = [svg_open(h), defs_and_style(c, uid), panel(c, h, uid)]
    s.append(f'<text x="40" y="66" font-size="46" class="accent sans" font-weight="700" opacity="0.45">\u201c</text>')
    s.append(f'<text x="78" y="66" font-size="19" class="ink sans" font-weight="700">Ship the full stack, not just the feature.</text>')
    s.append(f'<text x="78" y="94" font-size="12.5" class="muted">Prototype fast, refactor with intent \u2014 and treat every layer,</text>')
    s.append(f'<text x="78" y="114" font-size="12.5" class="muted">from the schema to the screen, as worth getting right.</text>')
    s.append("</svg>")
    return "\n".join(s)

# ---------------------------------------------------------------- FOOTER
def footer_svg(c):
    h = 112
    uid = "f"
    s = [svg_open(h), defs_and_style(c, uid), panel(c, h, uid)]
    s.append(f'<circle cx="48" cy="44" r="4" fill="{c["accent2"]}"/>')
    s.append(f'<circle cx="48" cy="44" r="9" fill="none" stroke="{c["accent2"]}" stroke-width="1" opacity="0.5"/>')
    s.append(f'<text x="64" y="49" font-size="13" class="ink">currently: sharpening Flutter + Node, exploring more ML-driven side projects</text>')
    s.append(f'<text x="48" y="80" font-size="11.5" class="muted">thanks for scrolling \u2014 open to collaborate, always happy to talk shop.</text>')
    s.append(f'<text x="{WIDTH-40}" y="80" font-size="10.5" class="dim" text-anchor="end">// EOF</text>')
    s.append("</svg>")
    return "\n".join(s)

BANNERS = {
    "header.svg": header_svg,
    "whoami.svg": whoami_svg,
    "ecosystem.svg": ecosystem_svg,
    "stack.svg": stack_svg,
    "philosophy.svg": philosophy_svg,
    "footer.svg": footer_svg,
}

for fname, fn in BANNERS.items():
    with open(os.path.join(OUT_LIGHT, fname), "w") as f:
        f.write(fn(LIGHT))
    with open(os.path.join(OUT_DARK, fname), "w") as f:
        f.write(fn(DARK))

print("done", list(BANNERS.keys()))
