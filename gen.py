#!/usr/bin/env python3
"""
LIMITLESS — README asset generator, v2
Dual-theme (GitHub light + dark), gold-forward, with three signature motifs:
  1. the capacity dial (percentage gauge, Lucy-style)
  2. gold letter-rain (the NZT / "words won't stop" scene from Limitless)
  3. glitch-reveal type (scrambled glyphs snapping into real words)
Everything is generated code, not hand-drawn, so the whole palette or layout
can be re-tuned from the token tables below and re-rendered in one shot.

Run: python3 gen.py   -> writes ./assets/*.svg (light) + ./assets/dark/*.svg
"""
import os, math, random

W = 960
HERE = os.path.dirname(os.path.abspath(__file__))

FONT_MONO = "'JetBrains Mono','SFMono-Regular','Cascadia Code',Consolas,monospace"
FONT_SANS = "'Space Grotesk','Segoe UI',Inter,sans-serif"
GLYPHS = "01ABCDEFGHIJKLMNOPQRSTUVWXYZ#%$*+"

# ---------------------------------------------------------------- themes --
def theme(name):
    if name == "dark":
        return dict(
            name="dark", folder="dark",
            BG="#07070a", BG2="#0b0b11", LINE="#1d1d26", LINE2="#141419",
            INK="#f2ede1", MUTED="#8a8374", DIM="#524d42",
            GOLD="#d9a441", GOLD_HI="#ffce6e", GOLD_LO="#3a2a0c", GOLD_GHOST="#6b4a14",
            CYAN="#35e3ff", CYAN_LO="#0c5b70",
            RAIN_HEAD="#fff6dd", RAIN_MID="#e8b94a", GRAIN_OP="0.5",
        )
    return dict(
        name="light", folder="",
        BG="#f7f1e0", BG2="#efe6cc", LINE="#ddcd9f", LINE2="#e6d9b0",
        INK="#171208", MUTED="#63543a", DIM="#8a7850",
        GOLD="#a8720a", GOLD_HI="#e3a300", GOLD_LO="#eddcae", GOLD_GHOST="#dcc179",
        CYAN="#0d7c8f", CYAN_LO="#bfe3e6",
        RAIN_HEAD="#7a4e00", RAIN_MID="#c2860a", GRAIN_OP="0.18",
    )

def head(w, h):
    return f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" xmlns="http://www.w3.org/2000/svg" role="img">'

def style_block(T):
    return f"""
<style>
text {{ font-family: {FONT_MONO}; }}
.sans {{ font-family: {FONT_SANS}; }}
.ink {{ fill:{T['INK']}; }}
.muted {{ fill:{T['MUTED']}; }}
.dim {{ fill:{T['DIM']}; }}
.gold {{ fill:{T['GOLD']}; }}
.goldHi {{ fill:{T['GOLD_HI']}; }}
.cyan {{ fill:{T['CYAN']}; }}
@keyframes blink {{ 0%,49% {{ opacity:1 }} 50%,100% {{ opacity:0 }} }}
.cursor {{ animation: blink 1.1s step-end infinite; }}
</style>
"""

def defs_common(uid, T):
    return f"""
<defs>
<radialGradient id="glow{uid}" cx="50%" cy="40%" r="68%">
<stop offset="0%" stop-color="{T['GOLD']}" stop-opacity="{'0.17' if T['name']=='dark' else '0.20'}"/>
<stop offset="55%" stop-color="{T['GOLD']}" stop-opacity="0.04"/>
<stop offset="100%" stop-color="{T['GOLD']}" stop-opacity="0"/>
</radialGradient>
<linearGradient id="sweep{uid}" x1="0" y1="0" x2="1" y2="0">
<stop offset="0%" stop-color="{T['GOLD_HI']}" stop-opacity="0"/>
<stop offset="50%" stop-color="{T['GOLD_HI']}" stop-opacity="0.55"/>
<stop offset="100%" stop-color="{T['GOLD_HI']}" stop-opacity="0"/>
</linearGradient>
<linearGradient id="goldbar{uid}" x1="0" y1="0" x2="1" y2="0">
<stop offset="0%" stop-color="{T['GOLD_GHOST']}"/>
<stop offset="55%" stop-color="{T['GOLD']}"/>
<stop offset="100%" stop-color="{T['GOLD_HI']}"/>
</linearGradient>
<linearGradient id="cyanbar{uid}" x1="0" y1="0" x2="1" y2="0">
<stop offset="0%" stop-color="{T['CYAN_LO']}"/>
<stop offset="100%" stop-color="{T['CYAN']}"/>
</linearGradient>
<radialGradient id="dot{uid}" cx="50%" cy="50%" r="50%">
<stop offset="0%" stop-color="{T['GOLD_HI']}" stop-opacity="0.95"/>
<stop offset="100%" stop-color="{T['GOLD_HI']}" stop-opacity="0"/>
</radialGradient>
<linearGradient id="raing{uid}" x1="0" y1="0" x2="0" y2="1">
<stop offset="0%" stop-color="{T['RAIN_MID']}" stop-opacity="0"/>
<stop offset="72%" stop-color="{T['RAIN_MID']}" stop-opacity="0.55"/>
<stop offset="100%" stop-color="{T['RAIN_HEAD']}" stop-opacity="1"/>
</linearGradient>
<radialGradient id="coin{uid}" cx="35%" cy="30%" r="75%">
<stop offset="0%" stop-color="{T['GOLD_HI']}"/>
<stop offset="55%" stop-color="{T['GOLD']}"/>
<stop offset="100%" stop-color="{T['GOLD_GHOST']}"/>
</radialGradient>
<pattern id="hex{uid}" width="26" height="30" patternUnits="userSpaceOnUse" patternTransform="scale(0.9)">
<path d="M13 0 L26 7.5 L26 22.5 L13 30 L0 22.5 L0 7.5 Z" fill="none" stroke="{T['GOLD']}" stroke-width="0.6"/>
</pattern>
<filter id="grain{uid}" x="0" y="0" width="100%" height="100%">
<feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" stitchTiles="stitch" result="n"/>
<feColorMatrix in="n" type="matrix" values="0 0 0 0 1  0 0 0 0 0.82  0 0 0 0 0.4  0.045 0.045 0.045 0 0"/>
</filter>
</defs>
"""

def bg_rect(w, h, uid, T, grain=True, hex_grid=True):
    g = f'<rect width="{w}" height="{h}" filter="url(#grain{uid})" opacity="{T["GRAIN_OP"]}"/>' if grain else ""
    hx = f'<rect width="{w}" height="{h}" fill="url(#hex{uid})" opacity="{"0.26" if T["name"]=="dark" else "0.30"}"/>' if hex_grid else ""
    return f'<rect width="{w}" height="{h}" fill="{T["BG"]}"/>{hx}{g}<rect width="{w}" height="{h}" fill="url(#glow{uid})"/>'

def frame(w, h, T, corners=True):
    out = [f'<rect x="0.5" y="0.5" width="{w-1}" height="{h-1}" fill="none" stroke="{T["LINE"]}" stroke-width="1"/>']
    if corners:
        L = 18
        pts = [(2,2,1,1),(w-2,2,-1,1),(2,h-2,1,-1),(w-2,h-2,-1,-1)]
        for x,y,sx,sy in pts:
            out.append(f'<path d="M{x} {y+L*sy} L{x} {y} L{x+L*sx} {y}" fill="none" stroke="{T["GOLD"]}" stroke-width="1.6" opacity="0.85"/>')
    return "".join(out)

def converge_lines(cx, cy, w, h, uid, T, n=22, opacity=0.05):
    out = [f'<g stroke="{T["GOLD"]}" stroke-width="1" opacity="{opacity}">']
    for i in range(n):
        ang = (i / n) * 2 * math.pi
        x2 = cx + math.cos(ang) * w
        y2 = cy + math.sin(ang) * h
        out.append(f'<line x1="{cx}" y1="{cy}" x2="{x2:.1f}" y2="{y2:.1f}"/>')
    out.append("</g>")
    return "".join(out)

def synapse_field(w, h, uid, T, n=26, seed=1):
    rnd = random.Random(seed)
    out = ['<g>']
    pts = [(rnd.uniform(0, w), rnd.uniform(0, h)) for _ in range(n)]
    out.append(f'<g stroke="{T["CYAN"]}" stroke-width="0.6" opacity="0.14">')
    for i, (x1, y1) in enumerate(pts):
        for (x2, y2) in pts[i+1:]:
            if math.hypot(x1 - x2, y1 - y2) < 130:
                out.append(f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}"/>')
    out.append("</g>")
    for x, y in pts:
        d = 1.6 + rnd.random() * 1.4
        dur = 2.6 + rnd.random() * 2.6
        delay = rnd.random() * 3
        out.append(
            f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{d:.1f}" fill="{T["CYAN"]}" opacity="0.4">'
            f'<animate attributeName="opacity" values="0.1;0.8;0.1" dur="{dur:.1f}s" '
            f'begin="{delay:.1f}s" repeatCount="indefinite"/></circle>'
        )
    out.append("</g>")
    return "".join(out)

# ------------------------------------------------------------ gold motifs --
def sparkle_field(w, h, uid, T, n=10, seed=2):
    rnd = random.Random(seed)
    out = ['<g>']
    for _ in range(n):
        x, y = rnd.uniform(10, w-10), rnd.uniform(10, h-10)
        s = 3 + rnd.random() * 4
        dur = 2 + rnd.random() * 3
        delay = rnd.random() * 4
        rot = rnd.uniform(0, 90)
        out.append(
            f'<g transform="translate({x:.1f} {y:.1f}) rotate({rot:.0f})" opacity="0">'
            f'<animate attributeName="opacity" values="0;0.9;0" dur="{dur:.1f}s" begin="{delay:.1f}s" repeatCount="indefinite"/>'
            f'<path d="M0 {-s} L{s*0.28} {-s*0.28} L{s} 0 L{s*0.28} {s*0.28} L0 {s} L{-s*0.28} {s*0.28} L{-s} 0 L{-s*0.28} {-s*0.28} Z" fill="{T["GOLD_HI"]}"/>'
            f'</g>'
        )
    out.append("</g>")
    return "".join(out)

def gold_coin(cx, cy, r, uid, T, dur=5, delay=0):
    return (
        f'<g transform="translate({cx} {cy})">'
        f'<animateTransform attributeName="transform" type="scale" additive="sum" '
        f'values="1,1;0.08,1;1,1" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/>'
        f'<g transform="translate({-1} {-1})">'
        f'<circle r="{r}" fill="url(#coin{uid})" stroke="{T["GOLD_HI"]}" stroke-width="1"/>'
        f'<circle r="{r-5}" fill="none" stroke="{T["BG"]}" stroke-width="1" opacity="0.5"/>'
        f'<text x="0" y="{r*0.34:.1f}" text-anchor="middle" class="sans" font-size="{r:.0f}" '
        f'font-weight="800" fill="{T["BG"]}">L</text>'
        f'</g></g>'
    )

def rain_stream(x, h, uid, T, seed, n_chars=9, char_h=15, font_size=13, dur=5, delay=0):
    rnd = random.Random(seed)
    stream_h = n_chars * char_h
    tspans = []
    for i in range(n_chars):
        ch = rnd.choice(GLYPHS)
        tspans.append(f'<tspan x="{x:.1f}" y="{i*char_h}">{ch}</tspan>')
    span_min = -stream_h - rnd.uniform(0, 40)
    span_max = h + rnd.uniform(0, 40)
    return (
        f'<g opacity="0.9"><animateTransform attributeName="transform" type="translate" '
        f'values="0,{span_min:.0f};0,{span_max:.0f}" dur="{dur:.2f}s" begin="{delay:.2f}s" repeatCount="indefinite"/>'
        f'<text font-size="{font_size}" fill="url(#raing{uid})">{"".join(tspans)}</text></g>'
    )

def rain_field(w, h, uid, T, n_columns=14, seed=11, streams_per_col=(1, 2), font_size=13,
               dur_range=(4.5, 9.5), col_span=None, field_opacity=0.8):
    rnd = random.Random(seed)
    out = [f'<g opacity="{field_opacity}">']
    xs = col_span or (16, w - 16)
    for c in range(n_columns):
        x = rnd.uniform(*xs)
        for _ in range(rnd.randint(*streams_per_col)):
            dur = rnd.uniform(*dur_range)
            delay = rnd.uniform(0, dur)
            n_chars = rnd.randint(6, 12)
            out.append(rain_stream(x, h, uid, T, rnd.randint(0, 99999), n_chars=n_chars,
                                    font_size=font_size, dur=dur, delay=delay))
    out.append("</g>")
    return "".join(out)

def gtext(x, y, text, uid, T, cls="ink", font_size=13, anchor="start", weight=400,
          cycle=None, seed=None, letter_spacing=None, family=None):
    """Lightweight constant glitch: text spends a brief instant per cycle as
    scrambled noise, then holds the real word. Two <text> elements only, so
    it's cheap enough to use on every label in the repo."""
    seed = seed if seed is not None else (abs(hash(text)) % 9973)
    rnd = random.Random(seed)
    cycle = cycle if cycle is not None else round(rnd.uniform(6.5, 12.5), 2)
    begin = round((seed % 41) / 11, 2)
    n = max(1, len(text.replace("&amp;", "&")))
    scr = "".join(rnd.choice(GLYPHS) for _ in range(min(n, 28)))
    step = max(0.012, 0.55 / cycle)
    kt = f"0;{step:.5f};1"
    ls = f' letter-spacing="{letter_spacing}"' if letter_spacing else ""
    fam = "sans " if family == "sans" else ""
    return (
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" class="{fam}{cls}" font-size="{font_size}" '
        f'font-weight="{weight}"{ls} opacity="0">{scr}'
        f'<animate attributeName="opacity" values="1;0;0" keyTimes="{kt}" dur="{cycle}s" begin="{begin}s" repeatCount="indefinite"/></text>'
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" class="{fam}{cls}" font-size="{font_size}" '
        f'font-weight="{weight}"{ls} opacity="1">{text}'
        f'<animate attributeName="opacity" values="0;1;1" keyTimes="{kt}" dur="{cycle}s" begin="{begin}s" repeatCount="indefinite"/></text>'
    )

def glitch_reveal(x, y, text, uid, T, cls="ink", font_size=16, anchor="start",
                   weight=700, cycle=9, seed=5, family="sans", letter_spacing=None):
    rnd = random.Random(seed)
    n = len(text)
    frames = ["".join(rnd.choice(GLYPHS) for _ in range(n)) for _ in range(3)] + [text]
    nf = len(frames)  # 4
    step = 0.1 / cycle
    keytimes = [0] + [round(step * (i + 1), 5) for i in range(nf - 1)] + [1]
    kt_str = ";".join(f"{k:.5f}" for k in keytimes)
    ls = f' letter-spacing="{letter_spacing}"' if letter_spacing else ""
    fam = "sans" if family == "sans" else ""
    out = []
    for i, frame_txt in enumerate(frames):
        vals = [0] * len(keytimes)
        vals[i] = 1
        if i == nf - 1:
            vals[-1] = 1
        vals_str = ";".join(str(v) for v in vals)
        opac = 0 if i < nf - 1 else 1
        out.append(
            f'<text x="{x}" y="{y}" text-anchor="{anchor}" class="{fam} {cls}" font-size="{font_size}" '
            f'font-weight="{weight}"{ls} opacity="{opac}">{frame_txt}'
            f'<animate attributeName="opacity" values="{vals_str}" keyTimes="{kt_str}" '
            f'dur="{cycle}s" repeatCount="indefinite"/></text>'
        )
    # faint chromatic-aberration ghost on the settled word, for a lived-in glitch feel
    out.append(
        f'<text x="{x}" y="{y}" text-anchor="{anchor}" class="{fam}" font-size="{font_size}" '
        f'font-weight="{weight}"{ls} fill="{T["CYAN"]}" opacity="0">{text}'
        f'<animate attributeName="opacity" values="0;0;0;0.35;0" dur="{cycle}s" repeatCount="indefinite"/>'
        f'<animate attributeName="x" values="{x};{x};{x};{x-1.5};{x}" dur="{cycle}s" repeatCount="indefinite"/>'
        f'</text>'
    )
    return "".join(out)

def capacity_dial(cx, cy, r, uid, T, pct_snapshots, dur=7, label="CAPACITY", font_size=None):
    circ = 2 * math.pi * r
    n = len(pct_snapshots)
    out = []
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{T["LINE"]}" stroke-width="6"/>')
    out.append(
        f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="url(#goldbar{uid})" '
        f'stroke-width="6" stroke-linecap="round" stroke-dasharray="{circ:.1f}" '
        f'transform="rotate(-90 {cx} {cy})">'
        f'<animate attributeName="stroke-dashoffset" '
        f'values="{circ:.1f};{circ*0.02:.1f};{circ:.1f}" dur="{dur}s" repeatCount="indefinite"/>'
        f'</circle>'
    )
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{r-16}" fill="none" stroke="{T["LINE2"]}" stroke-width="1" stroke-dasharray="1 5" opacity="0.6"/>')
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
        out.append(f'<text x="{cx}" y="{cy+r-8:.1f}" text-anchor="middle" class="dim" font-size="9" letter-spacing="2">{label}</text>')
    return "".join(out)

def write(name, svg, T):
    folder = os.path.join(HERE, "assets", T["folder"]) if T["folder"] else os.path.join(HERE, "assets")
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, name)
    with open(path, "w") as f:
        f.write(svg)
    print(T["name"], name, len(svg), "bytes")

# ---------------------------------------------------------------- HEADER --
def make_header(T):
    uid = "h" + T["folder"]; w, h = W, 300
    s = [head(w, h), defs_common(uid, T), style_block(T)]
    s.append(bg_rect(w, h, uid, T))
    s.append(rain_field(w, h, uid, T, n_columns=14, seed=101, streams_per_col=(1,2),
                         font_size=12, dur_range=(4,10), col_span=(16,42), field_opacity=0.5))
    s.append(rain_field(w, h, uid, T, n_columns=18, seed=102, streams_per_col=(1,2),
                         font_size=12, dur_range=(4,10), col_span=(630,900), field_opacity=0.5))
    s.append(converge_lines(w*0.5, h*0.36, w, h, uid, T, n=24, opacity=0.045))
    s.append(sparkle_field(w, h, uid, T, n=12, seed=21))
    s.append(frame(w, h, T))
    s.append(f'<line x1="0" y1="{h-1}" x2="{w}" y2="{h-1}" stroke="url(#sweep{uid})" stroke-width="2">'
              f'<animate attributeName="x1" values="-200;{w}" dur="5s" repeatCount="indefinite"/>'
              f'<animate attributeName="x2" values="0;{w+200}" dur="5s" repeatCount="indefinite"/></line>')
    s.append(gtext(60, 66, "SUBJECT — 001 // NZT-STATE ACTIVE", uid, T, cls="dim", font_size=11, letter_spacing="3", seed=201))
    s.append(glitch_reveal(60, 146, "JAVOHIR ABDUVAHHOBOV", uid, T, cls="ink", font_size=45,
                            weight=700, cycle=11, seed=4))
    s.append(gtext(60, 180, "Full-Stack &amp; Mobile Developer", uid, T, cls="muted", font_size=18, weight=600, family="sans", seed=202, cycle=9.4))
    s.append(f'<text x="60" y="222" class="gold" font-size="13" letter-spacing="1">every synapse firing at once<tspan class="cursor gold">_</tspan></text>')
    s.append(capacity_dial(w-98, 88, 40, uid, T, [0, 34, 61, 100], dur=6, label="ACCESS"))
    s.append("</svg>")
    write("header.svg", "".join(s), T)

# --------------------------------------------------------------- IGNITION --
def make_ignition(T):
    """The homage panel: gold letter-rain + a glitch-typed line, in the spirit
    of the scene where the words won't stop coming."""
    uid = "i" + T["folder"]; w, h = W, 360
    s = [head(w, h), defs_common(uid, T), style_block(T)]
    s.append(bg_rect(w, h, uid, T))
    s.append(rain_field(w, h, uid, T, n_columns=52, seed=202, streams_per_col=(3,4),
                         font_size=14, dur_range=(3.5, 8.5)))
    s.append(frame(w, h, T))
    s.append(gtext(w/2, 44, "00 — IGNITION", uid, T, cls="dim", font_size=11, anchor="middle", letter_spacing="4", seed=211))

    cx, cy = w/2, h/2 + 6
    s.append(f'<rect x="{cx-300}" y="{cy-72}" width="600" height="144" rx="4" fill="{T["BG"]}" opacity="{"0.72" if T["name"]=="dark" else "0.55"}" stroke="{T["GOLD"]}" stroke-width="1" stroke-opacity="0.35"/>')
    s.append(glitch_reveal(cx, cy-18, "TOOK THE PILL.", uid, T, cls="ink", font_size=34,
                            anchor="middle", weight=800, cycle=10, seed=41, letter_spacing="1"))
    s.append(glitch_reveal(cx, cy+34, "SHIPPED THE FEATURE.", uid, T, cls="goldHi", font_size=34,
                            anchor="middle", weight=800, cycle=10, seed=57, letter_spacing="1"))
    s.append(gtext(cx, cy+70, "keystrokes: unlimited. coffee: irrelevant.", uid, T, cls="muted", font_size=12, anchor="middle", seed=221))

    s.append(gold_coin(78, h-56, 26, uid, T, dur=4.5, delay=0.4))
    s.append(gold_coin(w-78, h-56, 18, uid, T, dur=5.5, delay=1.6))
    s.append("</svg>")
    write("ignition.svg", "".join(s), T)

# ---------------------------------------------------------------- WHOAMI --
def make_whoami(T):
    uid = "w" + T["folder"]; w, h = W, 380
    s = [head(w, h), defs_common(uid, T), style_block(T)]
    s.append(bg_rect(w, h, uid, T))
    s.append(synapse_field(w, h, uid, T, n=30, seed=3))
    s.append(rain_field(w, h, uid, T, n_columns=7, seed=303, streams_per_col=(1,2),
                         font_size=11, dur_range=(7,12), col_span=(w-90, w-20)))
    s.append(frame(w, h, T))
    s.append(gtext(40, 56, "01 — WHOAMI", uid, T, cls="dim", font_size=11, letter_spacing="3", seed=231))
    s.append(f'<line x1="40" y1="72" x2="{w-40}" y2="72" stroke="{T["LINE"]}" stroke-width="1"/>')

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
                  f'{gtext(40, y, k, uid, T, cls="muted", font_size=14, seed=240+i)}'
                  f'{gtext(185, y, v, uid, T, cls="ink", font_size=14, seed=250+i)}</g>')
        y += 30
    body = ("one codebase, one brain: from the screen a user taps, through the",
            "api that authenticates them, down to the postgres schema underneath.",
            "software engineering graduate — the kind who reads the whole stack",
            "trace before asking for help.")
    y += 14
    for i, line in enumerate(body):
        delay = 1.1 + 0.18 * i
        s.append(f'<g opacity="0"><animate attributeName="opacity" values="0;0;1" dur="0.5s" begin="{delay:.2f}s" fill="freeze"/>'
                  f'{gtext(40, y, line, uid, T, cls="dim", font_size=12.5, seed=260+i)}</g>')
        y += 20
    s.append(gtext(40, h-26, "// still reading — capacity has not capped yet", uid, T, cls="dim", font_size=10.5, seed=271))

    s.append(capacity_dial(w-150, h*0.46, 76, uid, T, [4, 19, 47, 68, 92, 100], dur=8, label="CAPACITY"))
    s.append("</svg>")
    write("whoami.svg", "".join(s), T)

# ------------------------------------------------------------- ECOSYSTEM --
def make_neural(T):
    uid = "n" + T["folder"]; w, h = W, 460
    s = [head(w, h), defs_common(uid, T), style_block(T)]
    s.append(bg_rect(w, h, uid, T))
    s.append(sparkle_field(w, h, uid, T, n=14, seed=61))
    s.append(rain_field(w, h, uid, T, n_columns=6, seed=161, streams_per_col=(1,1),
                         font_size=11, dur_range=(6,11), col_span=(16,44), field_opacity=0.35))
    s.append(rain_field(w, h, uid, T, n_columns=6, seed=162, streams_per_col=(1,1),
                         font_size=11, dur_range=(6,11), col_span=(w-44,w-16), field_opacity=0.35))
    s.append(frame(w, h, T))
    s.append(gtext(40, 46, "02 — ECOSYSTEM / SYNAPSE MAP", uid, T, cls="dim", font_size=11, letter_spacing="3", seed=281))
    s.append(f'<line x1="40" y1="62" x2="{w-40}" y2="62" stroke="{T["LINE"]}" stroke-width="1"/>')

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
    lg = [f'<g stroke="{T["GOLD"]}" stroke-width="1.2">']
    for i, (label, sub, dx, dy) in enumerate(nodes):
        x, y = cx+dx, cy+dy
        length = math.hypot(dx, dy)
        delay = 0.15 * i
        flick = 3.2 + 0.4 * i
        lg.append(f'<line x1="{cx}" y1="{cy}" x2="{x}" y2="{y}" stroke-dasharray="{length:.1f}" '
                   f'stroke-dashoffset="{length:.1f}" opacity="0.55"><animate attributeName="stroke-dashoffset" '
                   f'values="{length:.1f};0" dur="1s" begin="{delay:.2f}s" fill="freeze"/>'
                   f'<animate attributeName="opacity" values="0.35;0.65;0.35" dur="{flick:.1f}s" begin="{1+delay:.2f}s" repeatCount="indefinite"/></line>')
    lg.append("</g>")
    s.append("".join(lg))

    s.append(f'<g><animateTransform attributeName="transform" type="scale" additive="sum" values="1,1;1.035,1.035;1,1" dur="5s" repeatCount="indefinite"/>'
              f'<circle cx="{cx}" cy="{cy}" r="{core_r+18}" fill="url(#dot{uid})" opacity="0.5"/>'
              f'<circle cx="{cx}" cy="{cy}" r="{core_r}" fill="{T["BG2"]}" stroke="url(#goldbar{uid})" stroke-width="2.5"/>'
              f'<text x="{cx}" y="{cy-4}" text-anchor="middle" class="sans goldHi" font-size="15" font-weight="700">CORE</text>'
              f'<text x="{cx}" y="{cy+14}" text-anchor="middle" class="dim" font-size="9.5">javohir-io</text></g>')

    for i, (label, sub, dx, dy) in enumerate(nodes):
        x, y = cx+dx, cy+dy
        delay = 1.0 + 0.12 * i
        fdur = 4.2 + i * 0.6
        ax, ay = (7 if dx >= 0 else -7), (5 if i % 2 == 0 else -5)
        s.append(f'<g opacity="0"><animate attributeName="opacity" values="0;0;1" dur="0.5s" begin="{delay:.2f}s" fill="freeze"/>')
        s.append(f'<g><animateTransform attributeName="transform" type="translate" '
                  f'values="0,0; {ax},{ay}; 0,{-ay}; {-ax},{ay}; 0,0" dur="{fdur:.1f}s" repeatCount="indefinite"/>')
        s.append(f'<circle cx="{x}" cy="{y}" r="6" fill="{T["CYAN"]}">'
                  f'<animate attributeName="r" values="6;8;6" dur="{2.4+0.3*i:.1f}s" repeatCount="indefinite"/></circle>')
        anchor = "start" if dx >= 0 else "end"
        tx = x + (16 if dx >= 0 else -16)
        s.append(gtext(tx, y-6, label, uid, T, cls="ink", font_size=14, anchor=anchor, weight=600, family="sans", seed=300+i))
        s.append(gtext(tx, y+12, sub, uid, T, cls="muted", font_size=10.5, anchor=anchor, seed=310+i))
        s.append("</g></g>")

    s.append("</svg>")
    write("ecosystem.svg", "".join(s), T)

# ----------------------------------------------------------------- STACK --
def make_stack(T):
    uid = "s" + T["folder"]; w, h = W, 420
    s = [head(w, h), defs_common(uid, T), style_block(T)]
    s.append(bg_rect(w, h, uid, T, grain=False))
    s.append(rain_field(w, h, uid, T, n_columns=4, seed=171, streams_per_col=(1,1),
                         font_size=10, dur_range=(7,12), col_span=(16,36), field_opacity=0.3))
    s.append(rain_field(w, h, uid, T, n_columns=4, seed=172, streams_per_col=(1,1),
                         font_size=10, dur_range=(7,12), col_span=(w-36,w-16), field_opacity=0.3))
    s.append(frame(w, h, T))
    s.append(gtext(40, 46, "03 — STACK / CAPACITY LOADOUT", uid, T, cls="dim", font_size=11, letter_spacing="3", seed=321))
    s.append(f'<line x1="40" y1="62" x2="{w-40}" y2="62" stroke="{T["LINE"]}" stroke-width="1"/>')

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
        s.append(gtext(cx0, 92, title, uid, T, cls="gold", font_size=11, letter_spacing="1.5", seed=330+ci))
        y = 116
        for ri, (label, pct) in enumerate(rows):
            delay = 0.5 + (ci * 3 + ri) * 0.09
            s.append(gtext(cx0, y, label, uid, T, cls="ink", font_size=12.5, seed=340+ci*3+ri))
            s.append(gtext(cx0+bar_w, y, f"{pct}%", uid, T, cls="dim", font_size=10.5, anchor="end", seed=360+ci*3+ri))
            track_y = y + 8
            s.append(f'<rect x="{cx0}" y="{track_y}" width="{bar_w}" height="4" rx="2" fill="{T["LINE"]}"/>')
            target = bar_w * pct / 100
            s.append(f'<rect x="{cx0}" y="{track_y}" width="0" height="4" rx="2" fill="url(#goldbar{uid})">'
                      f'<animate attributeName="width" values="0;{target:.1f}" dur="1s" begin="{delay:.2f}s" fill="freeze"/></rect>')
            hi_delay = 1.6 + delay
            s.append(f'<rect x="{cx0}" y="{track_y}" width="10" height="4" rx="2" fill="{T["RAIN_HEAD"]}" opacity="0">'
                      f'<animate attributeName="opacity" values="0;0;0.9;0" dur="2.6s" begin="{hi_delay:.2f}s" repeatCount="indefinite"/>'
                      f'<animate attributeName="x" values="{cx0};{cx0};{cx0+target-10:.1f};{cx0+target-10:.1f}" dur="2.6s" begin="{hi_delay:.2f}s" repeatCount="indefinite"/></rect>')
            y += 40
        y += 6

    s.append(f'<line x1="40" y1="{h-70}" x2="{w-40}" y2="{h-70}" stroke="{T["LINE"]}" stroke-width="1"/>')
    s.append(gtext(40, h-44, "git . github . jwt . bcrypt . docker . multer . uuid — daily drivers, not decoration", uid, T, cls="dim", font_size=11, seed=380))
    s.append(gtext(40, h-22, "still climbing: ml / deep learning / data mining — capacity not yet capped", uid, T, cls="dim", font_size=10.5, seed=381))
    s.append("</svg>")
    write("stack.svg", "".join(s), T)

# ---------------------------------------------------------- TRANSMISSION --
def make_transmission(T):
    uid = "t" + T["folder"]; w, h = W, 240
    s = [head(w, h), defs_common(uid, T), style_block(T)]
    s.append(bg_rect(w, h, uid, T))
    s.append(converge_lines(w*0.5, h*1.3, w, h, uid, T, n=20, opacity=0.04))
    s.append(rain_field(w, h, uid, T, n_columns=10, seed=181, streams_per_col=(1,2),
                         font_size=11, dur_range=(6,11), col_span=(610,900), field_opacity=0.4))
    s.append(frame(w, h, T))
    s.append(gtext(40, 44, "04 — TRANSMISSION", uid, T, cls="dim", font_size=11, letter_spacing="3", seed=391))
    s.append(f'<circle cx="{w-120}" cy="41" r="4" fill="{T["GOLD_HI"]}"><animate attributeName="opacity" values="1;0.25;1" dur="1.6s" repeatCount="indefinite"/></circle>')
    s.append(gtext(w-108, 45, "ONLINE", uid, T, cls="gold", font_size=10.5, letter_spacing="1", seed=392))
    s.append(f'<line x1="40" y1="60" x2="{w-40}" y2="60" stroke="{T["LINE"]}" stroke-width="1"/>')
    s.append(f'<rect x="0" y="59" width="{w}" height="1" fill="{T["GOLD_HI"]}" opacity="0">'
              f'<animate attributeName="opacity" values="0;0.16;0" dur="3.4s" repeatCount="indefinite"/>'
              f'<animate attributeName="y" values="70;{h-30};70" dur="3.4s" repeatCount="indefinite"/></rect>')

    rows = [
        ("email", "javohirabduvahhobov@gmail.com"),
        ("github", "github.com/javohir-io"),
        ("based", "Tashkent, UZ  ·  open to remote work"),
    ]
    y = 108
    for i, (k, v) in enumerate(rows):
        s.append(gtext(40, y, k, uid, T, cls="dim", font_size=10.5, letter_spacing="1", seed=400+i))
        s.append(gtext(150, y, v, uid, T, cls="ink", font_size=15, seed=410+i))
        y += 34

    s.append(gtext(40, h-24, "say the word — the next 200 IQ points are on me.", uid, T, cls="muted", font_size=11.5, seed=421))
    s.append("</svg>")
    write("transmission.svg", "".join(s), T)

# --------------------------------------------------------------- SIGNAL ---
def make_frequency(T):
    uid = "f" + T["folder"]; w, h = W, 92
    s = [head(w, h), defs_common(uid, T), style_block(T)]
    s.append(bg_rect(w, h, uid, T, grain=False))
    s.append(sparkle_field(w, h, uid, T, n=6, seed=91))
    s.append(frame(w, h, T))

    s.append(gtext(28, 38, "Who Are You, Really?", uid, T, cls="ink", font_size=16, weight=700, family="sans", seed=441))
    s.append(gtext(28, 58, "Mikky Ekko", uid, T, cls="muted", font_size=12, seed=442))
    s.append(f'<circle cx="30" cy="74" r="6" fill="none" stroke="{T["GOLD"]}" stroke-width="1"><animate attributeName="opacity" values="0.5;1;0.5" dur="1.8s" repeatCount="indefinite"/></circle>')
    s.append(f'<path d="M28 71 L28 77 L33 74 Z" fill="{T["GOLD_HI"]}"/>')
    s.append(gtext(44, 78, "click to play", uid, T, cls="dim", font_size=10, seed=443))

    bars = 30
    rnd = random.Random(9)
    bx0, bx1, by = 380, w - 26, 68
    bw = (bx1 - bx0) / bars
    for i in range(bars):
        peak = 6 + rnd.random() * 26
        dur = 0.6 + rnd.random() * 0.9
        delay = rnd.random() * 0.8
        x = bx0 + i * bw
        s.append(f'<rect x="{x:.1f}" y="{by-peak:.1f}" width="{bw*0.55:.1f}" height="{peak:.1f}" rx="1.5" fill="url(#goldbar{uid})" opacity="0.85">'
                  f'<animate attributeName="height" values="{peak*0.3:.1f};{peak:.1f};{peak*0.3:.1f}" '
                  f'dur="{dur:.2f}s" begin="{delay:.2f}s" repeatCount="indefinite"/>'
                  f'<animate attributeName="y" values="{by-peak*0.3:.1f};{by-peak:.1f};{by-peak*0.3:.1f}" '
                  f'dur="{dur:.2f}s" begin="{delay:.2f}s" repeatCount="indefinite"/></rect>')
    s.append("</svg>")
    write("soundtrack.svg", "".join(s), T)

# --------------------------------------------------------------- DIVIDER --
def make_divider(T):
    uid = "d" + T["folder"]; w, h = W, 34
    s = [head(w, h), defs_common(uid, T)]
    s.append(f'<rect width="{w}" height="{h}" fill="{T["BG"]}"/>')
    s.append(f'<line x1="0" y1="{h/2}" x2="{w}" y2="{h/2}" stroke="{T["LINE"]}" stroke-width="1"/>')
    s.append(f'<line x1="-200" y1="{h/2}" x2="0" y2="{h/2}" stroke="url(#sweep{uid})" stroke-width="1.6">'
              f'<animate attributeName="x1" values="-200;{w}" dur="4s" repeatCount="indefinite"/>'
              f'<animate attributeName="x2" values="0;{w+200}" dur="4s" repeatCount="indefinite"/></line>')
    s.append(f'<circle cx="{w/2}" cy="{h/2}" r="2.4" fill="{T["GOLD_HI"]}"><animate attributeName="opacity" values="0.3;1;0.3" dur="2.4s" repeatCount="indefinite"/></circle>')
    for fx in (w*0.2, w*0.8):
        s.append(f'<circle cx="{fx}" cy="{h/2}" r="1.6" fill="{T["GOLD"]}" opacity="0.5">'
                  f'<animate attributeName="cy" values="{h/2-4};{h/2+4};{h/2-4}" dur="{3+fx/500:.1f}s" repeatCount="indefinite"/></circle>')
    s.append("</svg>")
    write("divider.svg", "".join(s), T)

# ---------------------------------------------------------------- FOOTER --
def make_footer(T):
    uid = "e" + T["folder"]; w, h = W, 180
    s = [head(w, h), defs_common(uid, T), style_block(T)]
    s.append(bg_rect(w, h, uid, T))
    s.append(rain_field(w, h, uid, T, n_columns=10, seed=808, streams_per_col=(1,1),
                         font_size=12, dur_range=(5,10), col_span=(16, w*0.28)))
    s.append(rain_field(w, h, uid, T, n_columns=10, seed=809, streams_per_col=(1,1),
                         font_size=12, dur_range=(5,10), col_span=(w*0.72, w-16)))
    s.append(converge_lines(w*0.5, h*0.5, w, h*1.4, uid, T, n=22, opacity=0.045))
    s.append(frame(w, h, T))
    s.append(f'<rect x="{w*0.22}" y="{h/2-42}" width="{w*0.56}" height="84" rx="4" fill="{T["BG"]}" opacity="{"0.78" if T["name"]=="dark" else "0.58"}" stroke="{T["GOLD"]}" stroke-width="1" stroke-opacity="0.35"/>')
    s.append(glitch_reveal(w/2, h/2-2, "CAPACITY: UNBOUNDED", uid, T, cls="goldHi", font_size=20,
                            anchor="middle", weight=700, cycle=13, seed=71, letter_spacing="2"))
    s.append(gtext(w/2, h/2+24, "thanks for reading this far — that\u2019s already more than most", uid, T, cls="dim", font_size=11, anchor="middle", seed=431))
    s.append("</svg>")
    write("footer.svg", "".join(s), T)

if __name__ == "__main__":
    for tname in ("light", "dark"):
        T = theme(tname)
        make_header(T); make_ignition(T); make_whoami(T); make_neural(T)
        make_stack(T); make_transmission(T); make_frequency(T)
        make_divider(T); make_footer(T)
