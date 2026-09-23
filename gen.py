#!/usr/bin/env python3
"""
LIMITLESS — README asset generator
Visual language: Limitless (2011) amber/gold "unlocked" glow + converging
infinite-corridor perspective, crossed with Lucy (2014) cyan synapse-network
HUD and percentage-of-capacity readouts. Dark, premium, quiet except for one
recurring signature motif: the capacity dial.

Run: python3 gen.py   -> writes ./assets/*.svg
"""
import os, math, random

random.seed(41)
OUT = os.path.join(os.path.dirname(__file__), "assets")
os.makedirs(OUT, exist_ok=True)
W = 960

# ---- tokens ----------------------------------------------------------
BG        = "#07070a"
BG2       = "#0b0b11"
LINE      = "#1c1c24"
LINE2     = "#131318"
INK       = "#f2ede1"
MUTED     = "#8a8374"
DIM       = "#524d42"
GOLD      = "#d9a441"
GOLD_HI   = "#ffce6e"
GOLD_LO   = "#3a2a0c"
CYAN      = "#35e3ff"
CYAN_LO   = "#0c5b70"

FONT_MONO = "'JetBrains Mono','SFMono-Regular','Cascadia Code',Consolas,monospace"
FONT_SANS = "'Space Grotesk','Segoe UI',Inter,sans-serif"

def style_block():
    return f"""
<style>
text {{ font-family: {FONT_MONO}; }}
.sans {{ font-family: {FONT_SANS}; }}
.ink {{ fill:{INK}; }}
.muted {{ fill:{MUTED}; }}
.dim {{ fill:{DIM}; }}
.gold {{ fill:{GOLD}; }}
.goldHi {{ fill:{GOLD_HI}; }}
.cyan {{ fill:{CYAN}; }}
.line {{ stroke:{LINE}; }}
.tick {{ letter-spacing:.4px; }}
@keyframes blink {{ 0%,49% {{ opacity:1 }} 50%,100% {{ opacity:0 }} }}
.cursor {{ animation: blink 1.1s step-end infinite; }}
</style>
"""

def defs_common(uid):
    """Shared gradients / filters. uid keeps ids unique per file (harmless, but tidy)."""
    return f"""
<defs>
<radialGradient id="glow{uid}" cx="50%" cy="42%" r="65%">
<stop offset="0%" stop-color="{GOLD}" stop-opacity="0.16"/>
<stop offset="55%" stop-color="{GOLD}" stop-opacity="0.05"/>
<stop offset="100%" stop-color="{GOLD}" stop-opacity="0"/>
</radialGradient>
<linearGradient id="sweep{uid}" x1="0" y1="0" x2="1" y2="0">
<stop offset="0%" stop-color="{GOLD}" stop-opacity="0"/>
<stop offset="50%" stop-color="{GOLD}" stop-opacity="0.5"/>
<stop offset="100%" stop-color="{GOLD}" stop-opacity="0"/>
</linearGradient>
<linearGradient id="goldbar{uid}" x1="0" y1="0" x2="1" y2="0">
<stop offset="0%" stop-color="{GOLD_LO}"/>
<stop offset="55%" stop-color="{GOLD}"/>
<stop offset="100%" stop-color="{GOLD_HI}"/>
</linearGradient>
<linearGradient id="cyanbar{uid}" x1="0" y1="0" x2="1" y2="0">
<stop offset="0%" stop-color="{CYAN_LO}"/>
<stop offset="100%" stop-color="{CYAN}"/>
</linearGradient>
<radialGradient id="dot{uid}" cx="50%" cy="50%" r="50%">
<stop offset="0%" stop-color="{GOLD_HI}" stop-opacity="0.95"/>
<stop offset="100%" stop-color="{GOLD_HI}" stop-opacity="0"/>
</radialGradient>
<filter id="soft{uid}" x="-60%" y="-60%" width="220%" height="220%">
<feGaussianBlur stdDeviation="2.4"/>
</filter>
<filter id="grain{uid}" x="0" y="0" width="100%" height="100%">
<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch" result="n"/>
<feColorMatrix in="n" type="matrix" values="0 0 0 0 1  0 0 0 0 0.85  0 0 0 0 0.55  0.05 0.05 0.05 0 0"/>
</filter>
</defs>
"""

def bg_rect(w, h, uid, grain=True):
    g = f'<rect width="{w}" height="{h}" filter="url(#grain{uid})" opacity="0.5"/>' if grain else ""
    return f'<rect width="{w}" height="{h}" fill="{BG}"/>{g}<rect width="{w}" height="{h}" fill="url(#glow{uid})"/>'

def converge_lines(cx, cy, w, h, uid, n=22, opacity=0.05):
    """Limitless-style infinite-corridor lines radiating from a vanishing point."""
    out = [f'<g stroke="{GOLD}" stroke-width="1" opacity="{opacity}">']
    for i in range(n):
        ang = (i / n) * 2 * math.pi
        x2 = cx + math.cos(ang) * w
        y2 = cy + math.sin(ang) * h
        out.append(f'<line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}"/>')
    out.append("</g>")
    return "".join(out)

def synapse_field(w, h, uid, n=26, seed=1):
    rnd = random.Random(seed)
    out = [f'<g>']
    pts = [(rnd.uniform(0, w), rnd.uniform(0, h)) for _ in range(n)]
    # faint connecting lines between near neighbours
    out.append(f'<g stroke="{CYAN}" stroke-width="0.6" opacity="0.12">')
    for i, (x1, y1) in enumerate(pts):
        for (x2, y2) in pts[i+1:]:
            if math.hypot(x1 - x2, y1 - y2) < 130:
                out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"/>')
    out.append("</g>")
    for i, (x, y) in enumerate(pts):
        d = 1.6 + rnd.random() * 1.4
        dur = 2.6 + rnd.random() * 2.6
        delay = rnd.random() * 3
        out.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{d:.1f}" fill="{CYAN}" opacity="0.35">'
            f'<animate attributeName="opacity" values="0.1;0.75;0.1" dur="{dur:.1f}s" '
            f'begin="{delay:.1f}s" repeatCount="indefinite"/></circle>'
        )
    out.append("</g>")
    return "".join(out)

def capacity_dial(cx, cy, r, uid, pct_snapshots, dur=7, label="CAPACITY", font_size=None):
    """The signature motif: an arc that sweeps like a loading dial, with a
    percentage readout that steps through snapshots in sync."""
    circ = 2 * math.pi * r
    n = len(pct_snapshots)
    step = 1 / n
    out = []
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{LINE}" stroke-width="6"/>')
    out.append(
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="url(#goldbar{uid})" '
        f'stroke-width="6" stroke-linecap="round" stroke-dasharray="{circ:.1f}" '
        f'transform="rotate(-90 {cx} {cy})">'
        f'<animate attributeName="stroke-dashoffset" '
        f'values="{circ:.1f};{circ*0.02:.1f};{circ:.1f}" dur="{dur}s" repeatCount="indefinite"/>'
        f'</circle>'
    )
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{r-16}" fill="none" stroke="{LINE2}" stroke-width="1" stroke-dasharray="1 5" opacity="0.6"/>')
    fs = font_size or round(r * 0.62)
    for i, val in enumerate(pct_snapshots):
        vals = ["0"] * n
        vals[i] = "1"
        vals_str = ";".join(vals + [vals[0]])
        out.append(
            f'<text x="{cx}" y="{cy+fs*0.32:.1f}" text-anchor="middle" class="sans goldHi" '
            f'font-size="{fs}" font-weight="700" opacity="0">{val}%'
            f'<animate attributeName="opacity" values="{vals_str}" dur="{dur}s" repeatCount="indefinite"/>'
            f'</text>'
        )
    if r >= 50:
        out.append(f'<text x="{cx}" y="{cy+r-8:.1f}" text-anchor="middle" class="dim tick" font-size="9">{label}</text>')
    return "".join(out)

def head(w, h):
    return f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img">'

def write(name, svg):
    path = os.path.join(OUT, name)
    with open(path, "w") as f:
        f.write(svg)
    print(name, len(svg), "bytes")

# ---- HEADER ------------------------------------------------------------
def make_header():
    uid = "h"; w, h = W, 300
    s = [head(w, h), defs_common(uid), style_block()]
    s.append(bg_rect(w, h, uid))
    s.append(converge_lines(w*0.5, h*0.36, w, h, uid, n=26, opacity=0.05))
    s.append(synapse_field(w, h, uid, n=18, seed=7))
    s.append(f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" fill="none" stroke="{LINE}" stroke-width="1"/>')
    s.append(f'<line x1="0" y1="{h-1}" x2="{w}" y2="{h-1}" stroke="url(#sweep{uid})" stroke-width="2">'
              f'<animate attributeName="x1" values="-200;{w}" dur="5s" repeatCount="indefinite"/>'
              f'<animate attributeName="x2" values="0;{w+200}" dur="5s" repeatCount="indefinite"/></line>')
    s.append(f'<text x="60" y="68" class="tick dim" font-size="11" letter-spacing="3">SUBJECT — 001 / NZT-STATE ACTIVE</text>')
    s.append(f'<text x="60" y="146" class="sans ink" font-size="45" font-weight="700">JAVOHIR ABDUVAHHOBOV</text>')
    s.append(f'<text x="60" y="180" class="sans muted" font-size="18">Full-Stack &amp; Mobile Developer</text>')
    s.append(f'<text x="60" y="222" class="gold" font-size="13" letter-spacing="1">every synapse firing at once<tspan class="cursor gold">_</tspan></text>')
    # small access dial, tucked top-right, clear of the headline
    s.append(capacity_dial(w-98, 88, 40, uid, [0, 34, 61, 100], dur=6, label="ACCESS"))
    s.append("</svg>")
    write("header.svg", "".join(s))

# ---- WHOAMI --------------------------------------------------------------
def make_whoami():
    uid = "w"; w, h = W, 380
    s = [head(w, h), defs_common(uid), style_block()]
    s.append(bg_rect(w, h, uid))
    s.append(synapse_field(w, h, uid, n=22, seed=3))
    s.append(f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" fill="none" stroke="{LINE}" stroke-width="1"/>')
    s.append(f'<text x="40" y="56" class="tick dim" font-size="11" letter-spacing="3">01 — WHOAMI</text>')
    s.append(f'<line x1="40" y1="72" x2="{w-40}" y2="72" stroke="{LINE}" stroke-width="1"/>')

    lines = [
        ("based:", "Tashkent, UZ"),
        ("role:", "full-stack &amp; mobile engineer"),
        ("stack:", "flutter . node.js . react . postgresql"),
        ("also studying:", "machine learning . deep learning . data mining"),
    ]
    y = 118
    for i, (k, v) in enumerate(lines):
        delay = 0.25 * i
        s.append(f'<g opacity="0"><animate attributeName="opacity" values="0;0;1" dur="0.6s" begin="{delay:.2f}s" fill="freeze"/>'
                  f'<text x="40" y="{y}" class="muted" font-size="14">{k}</text>'
                  f'<text x="185" y="{y}" class="ink" font-size="14">{v}</text></g>')
        y += 30
    body = ("one codebase, one brain: from the screen a user taps, through the",
            "api that authenticates them, down to the postgres schema underneath.",
            "software engineering graduate — the kind who reads the whole stack",
            "trace before asking for help.")
    y += 14
    for i, line in enumerate(body):
        delay = 1.1 + 0.18 * i
        s.append(f'<text x="40" y="{y}" class="dim" font-size="12.5" opacity="0">{line}'
                  f'<animate attributeName="opacity" values="0;0;1" dur="0.5s" begin="{delay:.2f}s" fill="freeze"/></text>')
        y += 20
    s.append(f'<text x="40" y="{h-26}" class="dim" font-size="10.5" opacity="0.7">// still reading — capacity has not capped yet</text>')

    s.append(capacity_dial(w-150, h*0.46, 76, uid, [4, 19, 47, 68, 92, 100], dur=8, label="CAPACITY"))
    s.append("</svg>")
    write("whoami.svg", "".join(s))

# ---- NEURAL / ECOSYSTEM ---------------------------------------------------
def make_neural():
    uid = "n"; w, h = W, 460
    s = [head(w, h), defs_common(uid), style_block()]
    s.append(bg_rect(w, h, uid))
    s.append(f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" fill="none" stroke="{LINE}" stroke-width="1"/>')
    s.append(f'<text x="40" y="46" class="tick dim" font-size="11" letter-spacing="3">02 — ECOSYSTEM / SYNAPSE MAP</text>')
    s.append(f'<line x1="40" y1="62" x2="{w-40}" y2="62" stroke="{LINE}" stroke-width="1"/>')

    cx, cy = w/2, h/2 + 20
    core_r = 46
    nodes = [
        ("mobile", "flutter . dart", -150, -120),
        ("web", "react . typescript", 150, -120),
        ("api", "node.js . express", -220, 40),
        ("data", "postgresql . docker", 220, 40),
        ("ml/ai", "python . deep learning", -120, 170),
        ("devops", "git . github . ci", 120, 170),
    ]
    # connecting lines, drawn in
    lg = [f'<g stroke="{GOLD}" stroke-width="1.2" opacity="0.55">']
    for i, (label, sub, dx, dy) in enumerate(nodes):
        x, y = cx+dx, cy+dy
        length = math.hypot(dx, dy)
        delay = 0.15 * i
        lg.append(f'<line x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" stroke-dasharray="{length:.1f}" '
                   f'stroke-dashoffset="{length:.1f}"><animate attributeName="stroke-dashoffset" '
                   f'values="{length:.1f};0" dur="1s" begin="{delay:.2f}s" fill="freeze"/></line>')
    lg.append("</g>")
    s.append("".join(lg))

    # core node
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{core_r+18}" fill="url(#dot{uid})" opacity="0.5"/>')
    s.append(f'<circle cx="{cx}" cy="{cy}" r="{core_r}" fill="{BG2}" stroke="url(#goldbar{uid})" stroke-width="2.5"/>')
    s.append(f'<text x="{cx}" y="{cy-4}" text-anchor="middle" class="sans goldHi" font-size="15" font-weight="700">CORE</text>')
    s.append(f'<text x="{cx}" y="{cy+14}" text-anchor="middle" class="dim" font-size="9.5">javohir-io</text>')

    for i, (label, sub, dx, dy) in enumerate(nodes):
        x, y = cx+dx, cy+dy
        delay = 1.0 + 0.12 * i
        s.append(f'<g opacity="0"><animate attributeName="opacity" values="0;0;1" dur="0.5s" begin="{delay:.2f}s" fill="freeze"/>')
        s.append(f'<circle cx="{x}" cy="{y}" r="6" fill="{CYAN}">'
                  f'<animate attributeName="r" values="6;8;6" dur="{2.4+0.3*i:.1f}s" repeatCount="indefinite"/></circle>')
        anchor = "start" if dx >= 0 else "end"
        tx = x + (16 if dx >= 0 else -16)
        s.append(f'<text x="{tx}" y="{y-6}" text-anchor="{anchor}" class="sans ink" font-size="14" font-weight="600">{label}</text>')
        s.append(f'<text x="{tx}" y="{y+12}" text-anchor="{anchor}" class="muted" font-size="10.5">{sub}</text>')
        s.append("</g>")

    s.append("</svg>")
    write("ecosystem.svg", "".join(s))

# ---- STACK -----------------------------------------------------------
def make_stack():
    uid = "s"; w, h = W, 420
    s = [head(w, h), defs_common(uid), style_block()]
    s.append(bg_rect(w, h, uid, grain=False))
    s.append(f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" fill="none" stroke="{LINE}" stroke-width="1"/>')
    s.append(f'<text x="40" y="46" class="tick dim" font-size="11" letter-spacing="3">03 — STACK / CAPACITY LOADOUT</text>')
    s.append(f'<line x1="40" y1="62" x2="{w-40}" y2="62" stroke="{LINE}" stroke-width="1"/>')

    cols = [
        ("mobile", [("Flutter", 92), ("Dart", 88), ("Kotlin", 60)]),
        ("frontend", [("React", 85), ("TypeScript", 78), ("HTML/CSS", 90)]),
        ("backend", [("Node.js", 88), ("Express", 82), ("PostgreSQL", 75)]),
        ("learning", [("Deep Learning", 46), ("Data Mining", 52), ("Docker", 40)]),
    ]
    col_w = (w - 80) / 4
    bar_w = col_w - 30
    for ci, (title, rows) in enumerate(cols):
        cx0 = 40 + ci * col_w
        s.append(f'<text x="{cx0}" y="92" class="gold tick" font-size="11" letter-spacing="1.5">{title}</text>')
        y = 116
        for ri, (label, pct) in enumerate(rows):
            delay = 0.5 + (ci * 3 + ri) * 0.09
            s.append(f'<text x="{cx0}" y="{y}" class="ink" font-size="12.5">{label}</text>')
            s.append(f'<text x="{cx0+bar_w}" y="{y}" text-anchor="end" class="dim" font-size="10.5">{pct}%</text>')
            track_y = y + 8
            s.append(f'<rect x="{cx0}" y="{track_y}" width="{bar_w}" height="4" rx="2" fill="{LINE}"/>')
            target = bar_w * pct / 100
            s.append(f'<rect x="{cx0}" y="{track_y}" width="0" height="4" rx="2" fill="url(#goldbar{uid})">'
                      f'<animate attributeName="width" values="0;{target:.1f}" dur="1s" begin="{delay:.2f}s" fill="freeze"/></rect>')
            y += 40
        y += 6

    s.append(f'<line x1="40" y1="{h-70}" x2="{w-40}" y2="{h-70}" stroke="{LINE}" stroke-width="1"/>')
    s.append(f'<text x="40" y="{h-44}" class="dim" font-size="11">git . github . jwt . bcrypt . docker . multer . uuid — daily drivers, not decoration</text>')
    s.append(f'<text x="40" y="{h-22}" class="dim" font-size="10.5" opacity="0.75">still climbing: ml / deep learning / data mining — capacity not yet capped</text>')
    s.append("</svg>")
    write("stack.svg", "".join(s))

# ---- TRANSMISSION / CONTACT --------------------------------------------
def make_transmission():
    uid = "t"; w, h = W, 240
    s = [head(w, h), defs_common(uid), style_block()]
    s.append(bg_rect(w, h, uid))
    s.append(converge_lines(w*0.5, h*1.3, w, h, uid, n=20, opacity=0.045))
    s.append(f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" fill="none" stroke="{LINE}" stroke-width="1"/>')
    s.append(f'<text x="40" y="44" class="tick dim" font-size="11" letter-spacing="3">04 — TRANSMISSION</text>')
    s.append(f'<circle cx="130" cy="41" r="4" fill="{GOLD_HI}"><animate attributeName="opacity" values="1;0.25;1" dur="1.6s" repeatCount="indefinite"/></circle>')
    s.append(f'<text x="142" y="45" class="gold" font-size="10.5" letter-spacing="1">ONLINE</text>')
    s.append(f'<line x1="40" y1="60" x2="{w-40}" y2="60" stroke="{LINE}" stroke-width="1"/>')

    rows = [
        ("email", "javohirabduvahhobov@gmail.com"),
        ("github", "github.com/javohir-io"),
        ("based", "Tashkent, UZ  ·  open to remote work"),
    ]
    y = 108
    for i, (k, v) in enumerate(rows):
        s.append(f'<text x="40" y="{y}" class="dim tick" font-size="10.5" letter-spacing="1">{k}</text>')
        s.append(f'<text x="150" y="{y}" class="ink" font-size="15">{v}</text>')
        y += 34

    s.append(f'<text x="40" y="{h-24}" class="muted" font-size="11.5">say the word — the next 200 IQ points are on me.<tspan class="cursor gold">_</tspan></text>')
    s.append("</svg>")
    write("transmission.svg", "".join(s))

# ---- FREQUENCY / SOUNDTRACK --------------------------------------------
def make_frequency():
    uid = "f"; w, h = W, 130
    s = [head(w, h), defs_common(uid), style_block()]
    s.append(bg_rect(w, h, uid, grain=False))
    s.append(f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" fill="none" stroke="{LINE}" stroke-width="1"/>')
    s.append(f'<text x="30" y="34" class="tick dim" font-size="10.5" letter-spacing="2">SIGNAL — WHAT PLAYS WHILE IT COMPILES</text>')
    s.append(f'<text x="30" y="58" class="sans ink" font-size="16" font-weight="600">open on Spotify →</text>')

    bars = 46
    rnd = random.Random(9)
    bx0, by = 30, 96
    bw = (w - 60) / bars
    for i in range(bars):
        peak = 8 + rnd.random() * 34
        dur = 0.6 + rnd.random() * 0.9
        delay = rnd.random() * 0.8
        x = bx0 + i * bw
        s.append(f'<rect x="{x:.1f}" y="{by-peak:.1f}" width="{bw*0.55:.1f}" height="{peak:.1f}" rx="1.5" fill="url(#goldbar{uid})" opacity="0.85">'
                  f'<animate attributeName="height" values="{peak*0.3:.1f};{peak:.1f};{peak*0.3:.1f}" '
                  f'dur="{dur:.2f}s" begin="{delay:.2f}s" repeatCount="indefinite"/>'
                  f'<animate attributeName="y" values="{by-peak*0.3:.1f};{by-peak:.1f};{by-peak*0.3:.1f}" '
                  f'dur="{dur:.2f}s" begin="{delay:.2f}s" repeatCount="indefinite"/></rect>')
    s.append("</svg>")
    write("soundtrack.svg", "".join(s))

# ---- DIVIDER -----------------------------------------------------------
def make_divider():
    uid = "d"; w, h = W, 34
    s = [head(w, h)]
    s.append(defs_common(uid))
    s.append(f'<rect width="{w}" height="{h}" fill="{BG}"/>')
    s.append(f'<line x1="0" y1="{h/2}" x2="{w}" y2="{h/2}" stroke="{LINE}" stroke-width="1"/>')
    s.append(f'<line x1="-200" y1="{h/2}" x2="0" y2="{h/2}" stroke="url(#sweep{uid})" stroke-width="1.6">'
              f'<animate attributeName="x1" values="-200;{w}" dur="4s" repeatCount="indefinite"/>'
              f'<animate attributeName="x2" values="0;{w+200}" dur="4s" repeatCount="indefinite"/></line>')
    s.append(f'<circle cx="{w/2}" cy="{h/2}" r="2.4" fill="{GOLD_HI}"><animate attributeName="opacity" values="0.3;1;0.3" dur="2.4s" repeatCount="indefinite"/></circle>')
    s.append("</svg>")
    write("divider.svg", "".join(s))

# ---- FOOTER --------------------------------------------------------------
def make_footer():
    uid = "e"; w, h = W, 170
    s = [head(w, h), defs_common(uid), style_block()]
    s.append(bg_rect(w, h, uid))
    s.append(converge_lines(w*0.5, h*0.5, w, h*1.4, uid, n=24, opacity=0.05))
    s.append(f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" fill="none" stroke="{LINE}" stroke-width="1"/>')
    s.append(f'<text x="{w/2}" y="{h/2-6}" text-anchor="middle" class="sans goldHi" font-size="20" font-weight="700" letter-spacing="2">CAPACITY: UNBOUNDED</text>')
    s.append(f'<text x="{w/2}" y="{h/2+22}" text-anchor="middle" class="dim" font-size="11">thanks for reading this far — that\u2019s already more than most<tspan class="cursor gold">_</tspan></text>')
    s.append("</svg>")
    write("footer.svg", "".join(s))

if __name__ == "__main__":
    make_header(); make_whoami(); make_neural(); make_stack()
    make_transmission(); make_frequency(); make_divider(); make_footer()
