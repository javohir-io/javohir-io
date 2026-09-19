# -*- coding: utf-8 -*-
import os, html, math, random

random.seed(7)

OUT_LIGHT = "/home/claude/readme-v2/assets"
OUT_DARK  = "/home/claude/readme-v2/assets/dark"
os.makedirs(OUT_LIGHT, exist_ok=True)
os.makedirs(OUT_DARK, exist_ok=True)

SANS = "'Space Grotesk','Segoe UI',Inter,sans-serif"
MONO = "'JetBrains Mono','SFMono-Regular','Cascadia Code',Consolas,monospace"
WIDTH = 960

# ---- black / white / red — pushed into more shades, more alien, more alive.
LIGHT = dict(
    ink="#0a0a0a", ink2="#000000",
    white="#ffffff", off="#f6f6f6",
    muted="#4d4d4d", dim="#8a8a8a", dim2="#b8b8b8",
    accent="#d21f2c",     # crimson — primary
    accent2="#8a1015",    # deep blood — structural / secondary
    accent3="#ff0044",    # hot rose-red — ghost / glitch channel
    accent4="#7a0c12",    # near-black red — deepest shade
    line="#e2e2e2", line2="#cfcfcf", panel="#ffffff", grid="#eeeeee",
)
DARK = dict(
    ink="#f5f5f5", ink2="#ffffff",
    white="#0a0a0a", off="#050505",
    muted="#a8a8a8", dim="#6e6e6e", dim2="#454545",
    accent="#ff2b39",
    accent2="#8a1015",
    accent3="#ff0044",
    accent4="#3a0508",
    line="#242424", line2="#161616", panel="#0a0a0a", grid="#131313",
)

ALIEN = list("⌬⏃⏄⎈⏚⌀⍜⍟⏛⌇⏢⎊⍚⏦⌐⏰◬◭◮⟁⟒⟟⟠⟡⧫◈◉⌭⌮⎔⏣⟴⟵⊘⊙⊚")

def esc(s):
    return html.escape(str(s), quote=True)

def rnd_alien(n=1, seed=None):
    r = random.Random(seed)
    return "".join(r.choice(ALIEN) for _ in range(n))

def stable_hash(s):
    return sum(ord(ch) for ch in str(s))

def tw(s, size, factor=0.605):
    return len(str(s)) * size * factor

def svg_open(h, w=WIDTH):
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'xmlns="http://www.w3.org/2000/svg" role="img">')

def defs_and_style(c, uid, extra=""):
    return f'''<defs>
<pattern id="hex{uid}" width="26" height="30" patternUnits="userSpaceOnUse" patternTransform="scale(0.62)">
<path d="M13 0 L26 7.5 L26 22.5 L13 30 L0 22.5 L0 7.5 Z" fill="none" stroke="{c["grid"]}" stroke-width="1"/>
</pattern>
<radialGradient id="vign{uid}" cx="50%" cy="35%" r="75%">
<stop offset="0%" stop-color="{c["accent"]}" stop-opacity="0.05"/>
<stop offset="100%" stop-color="{c["accent"]}" stop-opacity="0"/>
</radialGradient>
<linearGradient id="sweep{uid}" x1="0" y1="0" x2="1" y2="0">
<stop offset="0%" stop-color="{c["accent"]}" stop-opacity="0"/>
<stop offset="50%" stop-color="{c["accent"]}" stop-opacity="0.11"/>
<stop offset="100%" stop-color="{c["accent"]}" stop-opacity="0"/>
</linearGradient>
<radialGradient id="core{uid}" cx="50%" cy="50%" r="50%">
<stop offset="0%" stop-color="{c["accent"]}" stop-opacity="0.9"/>
<stop offset="60%" stop-color="{c["accent2"]}" stop-opacity="0.5"/>
<stop offset="100%" stop-color="{c["accent2"]}" stop-opacity="0"/>
</radialGradient>
<filter id="noise{uid}" x="-20%" y="-20%" width="140%" height="140%">
<feTurbulence type="fractalNoise" baseFrequency="0.85" numOctaves="2" stitchTiles="stitch" result="n"/>
<feColorMatrix in="n" type="matrix" values="0 0 0 0 1  0 0 0 0 0.08  0 0 0 0 0.08  0.25 0.25 0.25 0 0"/>
</filter>
<filter id="blur{uid}" x="-60%" y="-60%" width="220%" height="220%">
<feGaussianBlur stdDeviation="3.2"/>
</filter>
<filter id="softblur{uid}" x="-60%" y="-60%" width="220%" height="220%">
<feGaussianBlur stdDeviation="1.1"/>
</filter>
{extra}
</defs>
<style>
text {{ font-family: {MONO}; }}
.sans {{ font-family: {SANS}; }}
.ink {{ fill:{c["ink"]}; }}
.muted {{ fill:{c["muted"]}; }}
.dim {{ fill:{c["dim"]}; }}
.dim2 {{ fill:{c["dim2"]}; }}
.accent {{ fill:{c["accent"]}; }}
.accent2 {{ fill:{c["accent2"]}; }}
.accent3 {{ fill:{c["accent3"]}; }}
.line {{ stroke:{c["line"]}; }}
@keyframes blink{uid} {{ 0%,49% {{ opacity:1 }} 50%,100% {{ opacity:0 }} }}
.cursor{uid} {{ animation: blink{uid} 1.05s steps(1,end) infinite; }}
@keyframes drift{uid} {{ 0% {{ transform:translateY(0) }} 100% {{ transform:translateY(30px) }} }}
</style>'''

# ---------------------------------------------------------------- LIVE / GLITCH PRIMITIVES

def static_burst(c, uid, x, y, w, h, period=7, begin=0):
    return (f'<g clip-path="url(#clip{uid})">'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" filter="url(#noise{uid})" opacity="0">'
            f'<animate attributeName="opacity" values="0;0;0.5;0.12;0.4;0;0" '
            f'keyTimes="0;0.63;0.645;0.66;0.672;0.69;1" dur="{period}s" begin="{begin}s" repeatCount="indefinite"/>'
            f'</rect></g>')

def scanline(c, uid, x, y, w, h, period=3.2, begin=0):
    return (f'<g clip-path="url(#clip{uid})">'
            f'<rect x="{x}" y="{-2}" width="{w}" height="2" fill="{c["accent"]}" opacity="0.16">'
            f'<animate attributeName="y" values="{y-2};{y+h}" dur="{period}s" begin="{begin}s" repeatCount="indefinite"/>'
            f'</rect></g>')

def radar_sweep(c, uid, cx, cy, r, dur=5, begin=0):
    """a rotating radar arm + fading rings, alien-scanner style"""
    out = [f'<g>']
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{c["line"]}" stroke-width="1"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{r*0.66:.1f}" fill="none" stroke="{c["line"]}" stroke-width="1" stroke-dasharray="2,4"/>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="{r*0.33:.1f}" fill="none" stroke="{c["line"]}" stroke-width="1"/>')
    out.append(f'<g>')
    out.append(f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>')
    out.append(f'<path d="M {cx} {cy} L {cx} {cy-r}" stroke="{c["accent"]}" stroke-width="1.4" opacity="0.9"/>')
    out.append(f'<path d="M {cx} {cy} L {cx+r*0.9:.1f} {cy-r*0.35:.1f} L {cx} {cy} L {cx} {cy-r} Z" fill="url(#core{uid})" opacity="0.35"/>')
    out.append('</g>')
    for i, rr in enumerate([r*0.2, r*0.45, r*0.72, r]):
        out.append(f'<circle cx="{cx}" cy="{cy}" r="2" fill="none" stroke="{c["accent"]}" stroke-width="1.3" opacity="0">'
                    f'<animate attributeName="r" values="2;{rr:.1f}" dur="3s" begin="{begin+i*0.7:.1f}s" repeatCount="indefinite"/>'
                    f'<animate attributeName="opacity" values="0.55;0" dur="3s" begin="{begin+i*0.7:.1f}s" repeatCount="indefinite"/>'
                    f'</circle>')
    out.append(f'<circle cx="{cx}" cy="{cy}" r="3" fill="{c["accent"]}"/>')
    out.append('</g>')
    return "\n".join(out)

def glitch_text(c, uid, x, y, text, fs, weight=700, period=5, begin=0, cls="ink sans", anchor="start"):
    """RGB-split cyberpunk glitch burst on a headline, settles back to normal"""
    kt = "0;0.55;0.565;0.578;0.59;0.60;1"
    ta = f' text-anchor="{anchor}"' if anchor != "start" else ""
    out = [f'<g>']
    out.append(f'<animateTransform attributeName="transform" attributeType="XML" type="translate" '
                f'values="0,0;0,0;3,-1;-4,1;2,0;0,0;0,0" keyTimes="{kt}" dur="{period}s" begin="{begin}s" repeatCount="indefinite"/>')
    out.append(f'<text x="{x-4}" y="{y}" font-size="{fs}" font-weight="{weight}" fill="#00e5ff" class="sans" opacity="0"{ta}>'
                f'<animate attributeName="opacity" values="0;0;0.85;0;0.7;0;0" keyTimes="{kt}" dur="{period}s" begin="{begin}s" repeatCount="indefinite"/>{esc(text)}</text>')
    out.append(f'<text x="{x+4}" y="{y}" font-size="{fs}" font-weight="{weight}" fill="{c["accent3"]}" class="sans" opacity="0"{ta}>'
                f'<animate attributeName="opacity" values="0;0;0.8;0;0.65;0;0" keyTimes="{kt}" dur="{period}s" begin="{begin}s" repeatCount="indefinite"/>{esc(text)}</text>')
    out.append(f'<text x="{x}" y="{y}" font-size="{fs}" font-weight="{weight}" class="{cls}"{ta}>'
                f'<animate attributeName="opacity" values="1;1;0.55;1;0.6;1;1" keyTimes="{kt}" dur="{period}s" begin="{begin}s" repeatCount="indefinite"/>{esc(text)}</text>')
    out.append('</g>')
    return "\n".join(out)

def decode_text(c, uid, x, y, text, fs, begin=0, cycle=13, cls="ink", charw_factor=0.61, glyph_seed=None):
    """
    Per-character alive text: renders as alien glyph noise first, decodes into the
    real character, then re-glitches briefly at random points in the loop.
    """
    charw = fs * charw_factor
    out = [f'<g font-size="{fs}">']
    for i, ch in enumerate(text):
        xi = x + i * charw
        if ch == " ":
            continue
        stagger = i * 0.028
        b = begin + stagger
        glyph = rnd_alien(1, seed=(glyph_seed or 0) * 97 + i)
        reflash = round(0.78 + (i % 5) * 0.02, 3)
        kt = f"0;0.001;0.07;0.075;{reflash};{reflash+0.012};{reflash+0.02};1"
        out.append(f'<text x="{xi:.1f}" y="{y}" class="accent">{esc(glyph)}'
                    f'<animate attributeName="opacity" values="0;1;1;0;0;1;0;0" keyTimes="{kt}" '
                    f'dur="{cycle}s" begin="{b:.3f}s" repeatCount="indefinite"/></text>')
        out.append(f'<text x="{xi:.1f}" y="{y}" class="{cls}">{esc(ch)}'
                    f'<animate attributeName="opacity" values="0;0;0;1;1;0;1;1" keyTimes="{kt}" '
                    f'dur="{cycle}s" begin="{b:.3f}s" repeatCount="indefinite"/></text>')
    out.append('</g>')
    return "\n".join(out), x + len(text) * charw

def matrix_rain(c, uid, x, y, w, h, cols=None, begin=0):
    """falling alien/binary character columns, clipped to a region"""
    cols = cols or max(6, int(w / 26))
    out = [f'<g clip-path="url(#clip{uid})" opacity="0.5">']
    r = random.Random(stable_hash(uid) + 1)
    for i in range(cols):
        cx = x + i * (w / cols) + (w / cols) / 2
        dur = round(r.uniform(3.5, 7.5), 2)
        delay = round(r.uniform(0, 6), 2)
        chars = [r.choice(ALIEN + list("01")) for _ in range(6)]
        col_out = [f'<g>']
        col_out.append(f'<animateTransform attributeName="transform" type="translate" '
                        f'values="0,{-h}; 0,{h}" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/>')
        for j, ch in enumerate(chars):
            op = round(1 - j * 0.16, 2)
            col_out.append(f'<text x="{cx:.1f}" y="{y + j*15}" font-size="11" fill="{c["accent"]}" opacity="{max(op,0.05)}">{esc(ch)}</text>')
        col_out.append('</g>')
        out.append("".join(col_out))
    out.append('</g>')
    return "\n".join(out)

def corner_brackets(c, x, y, w, h, size=13, inset=9, sw=2, hex_tick=True):
    pts = [
        (x+inset, y+inset, 1, 1), (x+w-inset, y+inset, -1, 1),
        (x+inset, y+h-inset, 1, -1), (x+w-inset, y+h-inset, -1, -1),
    ]
    out = []
    for px, py, dx, dy in pts:
        out.append(f'<path d="M {px} {py+size*dy} L {px} {py} L {px+size*dx} {py}" '
                    f'fill="none" stroke="{c["accent"]}" stroke-width="{sw}" stroke-linecap="round" opacity="0.9"/>')
        if hex_tick:
            out.append(f'<circle cx="{px}" cy="{py}" r="1.6" fill="{c["accent"]}"/>')
    return "\n".join(out)

def hex_points(cx, cy, r):
    pts = []
    for i in range(6):
        a = math.radians(60 * i - 30)
        pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return " ".join(f"{px:.1f},{py:.1f}" for px, py in pts)

def hex_badge(c, cx, cy, label, r=17, spin=False, dur=18):
    out = [f'<g>']
    if spin:
        out.append(f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="{dur}s" repeatCount="indefinite"/>')
    out.append(f'<polygon points="{hex_points(cx,cy,r)}" fill="{c["panel"]}" stroke="{c["accent"]}" stroke-width="1.6"/>')
    out.append('</g>')
    out.append(f'<text x="{cx}" y="{cy+4.5}" font-size="12.5" text-anchor="middle" class="accent sans" font-weight="700">{esc(label)}</text>')
    return "\n".join(out)

def section_head(c, num, title, x=40, y=54, sub=None):
    out = [hex_badge(c, x+16, y-6, num, spin=True, dur=26)]
    out.append(f'<text x="{x+44}" y="{y}" font-size="19" class="ink sans" font-weight="700">{esc(title)}</text>')
    if sub:
        out.append(f'<text x="{x+44}" y="{y+19}" font-size="11.5" class="dim">{esc(sub)}</text>')
    return "\n".join(out)

def pulse_dot(c, cx, cy, r=4, ring_r=13, dur=2.2, begin=0):
    return (f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="{c["accent"]}"/>'
            f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{c["accent"]}" stroke-width="1.4" opacity="0.65">'
            f'<animate attributeName="r" values="{r};{ring_r};{r}" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>'
            f'<animate attributeName="opacity" values="0.65;0;0.65" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>'
            f'</circle>')

def pill(c, x, y, label, h=24, fs=12, pad=10, fg=None, pulse=False, begin=0):
    w = tw(label, fs) + pad * 2
    fg = fg or c["ink"]
    out = [f'<rect x="{x}" y="{y}" width="{w:.1f}" height="{h}" rx="5" '
           f'fill="{c["panel"]}" stroke="{c["line"]}" stroke-width="1"/>']
    if pulse:
        out.append(f'<rect x="{x}" y="{y}" width="{w:.1f}" height="{h}" rx="5" fill="none" stroke="{c["accent"]}" stroke-width="1" opacity="0">'
                    f'<animate attributeName="opacity" values="0;0.8;0" dur="2.6s" begin="{begin}s" repeatCount="indefinite"/></rect>')
    out.append(f'<text x="{x+pad}" y="{y+h/2+4.2}" font-size="{fs}" fill="{fg}">{esc(label)}</text>')
    return "\n".join(out), w

def pill_row(c, items, x0, y0, max_w, gap=7, row_gap=9, h=24, fs=12, pulse=False):
    out, x, y = [], x0, y0
    for i, label in enumerate(items):
        svg, w = pill(c, x, y, label, h, fs, pulse=pulse, begin=(i % 6) * 0.45)
        if x + w > x0 + max_w:
            x = x0
            y += h + row_gap
            svg, w = pill(c, x, y, label, h, fs, pulse=pulse, begin=(i % 6) * 0.45)
        out.append(svg)
        x += w + gap
    return "\n".join(out), y + h

def circuit_pulse_line(c, uid, x1, y1, x2, y2, dur=2.4, begin=0, dot_r=2.6):
    length = abs(x2 - x1) + abs(y2 - y1)
    out = [f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c["line"]}" stroke-width="1.2"/>']
    out.append(f'<circle r="{dot_r}" fill="{c["accent"]}">'
                f'<animateMotion path="M {x1} {y1} L {x2} {y2}" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>'
                f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.08;0.92;1" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>'
                f'</circle>')
    return "\n".join(out)

def panel(c, h, uid, w=WIDTH, m=4, rx=20, sweep_dur=6, sweep_begin=0, glitch_begin=1.5, scan_begin=0.4, radar=None):
    pw, ph = w - m * 2, h - m * 2
    out = [f'<clipPath id="clip{uid}"><rect x="{m}" y="{m}" width="{pw}" height="{ph}" rx="{rx}"/></clipPath>']
    out.append(f'<rect x="{m}" y="{m}" width="{pw}" height="{ph}" rx="{rx}" fill="{c["panel"]}" stroke="{c["line"]}" stroke-width="1.2"/>')
    out.append(f'<rect x="{m}" y="{m}" width="{pw}" height="{ph}" rx="{rx}" fill="url(#hex{uid})" opacity="0.9"/>')
    out.append(f'<rect x="{m}" y="{m}" width="{pw}" height="{ph}" rx="{rx}" fill="url(#vign{uid})"/>')
    sw = pw * 0.55
    out.append(f'<g clip-path="url(#clip{uid})">'
                f'<rect x="{-sw}" y="{m}" width="{sw}" height="{ph}" fill="url(#sweep{uid})">'
                f'<animate attributeName="x" from="{-sw}" to="{w}" dur="{sweep_dur}s" begin="{sweep_begin}s" repeatCount="indefinite"/>'
                f'</rect></g>')
    out.append(scanline(c, uid, m, m, pw, ph, period=3.4 + (stable_hash(uid) % 5) * 0.3, begin=scan_begin))
    out.append(static_burst(c, uid, m, m, pw, ph, period=6.5 + (stable_hash(uid) % 4), begin=glitch_begin))
    if radar:
        rx_, ry_, rr_ = radar
        out.append(f'<g clip-path="url(#clip{uid})">{radar_sweep(c, uid, rx_, ry_, rr_, dur=7, begin=0.3)}</g>')
    out.append(corner_brackets(c, m, m, pw, ph))
    out.append(f'<rect x="{m}" y="{m}" width="{pw}" height="{ph}" rx="{rx}" fill="none" stroke="{c["accent"]}" stroke-width="1" opacity="0.18"/>')
    return "\n".join(out)

def box(c, x, y, w, h, title, sub=None, accent=False):
    stroke = c["accent"] if accent else c["line"]
    out = [f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="7" fill="{c["panel"]}" stroke="{stroke}" stroke-width="1.3"/>']
    out.append(f'<text x="{x+w/2}" y="{y+h/2 - (5 if sub else -4)}" font-size="12.5" class="ink sans" text-anchor="middle" font-weight="700">{esc(title)}</text>')
    if sub:
        out.append(f'<text x="{x+w/2}" y="{y+h/2+14}" font-size="10.5" class="dim" text-anchor="middle">{esc(sub)}</text>')
    return "\n".join(out)

def arrow(c, x1, y1, x2, y2, label=None, flow_dur=1.1, flow_begin=0, flicker=False):
    length = abs(x2 - x1) + abs(y2 - y1)
    out = []
    if flicker:
        kt = "0;0.8;0.81;0.85;0.86;0.9;1"
        out.append(f'<animate attributeName="opacity" values="1;1;0.15;0.15;1;1;1" keyTimes="{kt}" dur="9s" begin="4s" repeatCount="indefinite"/>')
    out.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c["line"]}" stroke-width="1.3"/>')
    out.append(f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="{c["accent"]}" stroke-width="1.6" '
                f'stroke-dasharray="7,6" opacity="0.9">'
                f'<animate attributeName="stroke-dashoffset" from="{length}" to="0" dur="{flow_dur}s" '
                f'begin="{flow_begin}s" repeatCount="indefinite"/></line>')
    hl = 6
    if x2 >= x1:
        out.append(f'<path d="M {x2} {y2} l {-hl*1.4:.1f} {-4:.1f} l 0 {8:.1f} z" fill="{c["accent"]}"/>')
    else:
        out.append(f'<path d="M {x2} {y2} l {hl*1.4:.1f} {-4:.1f} l 0 {8:.1f} z" fill="{c["accent"]}"/>')
    if label:
        lx, ly = (x1+x2)/2 - (tw(label,10.5)+10)/2, (y1+y2)/2 - 9
        out.append(f'<rect x="{lx}" y="{ly}" width="{tw(label,10.5)+10}" height="15" fill="{c["panel"]}"/>')
        out.append(f'<text x="{lx+5}" y="{ly+11}" font-size="10.5" class="dim">{esc(label)}</text>')
    inner = "\n".join(out)
    return f'<g>{inner}</g>' if flicker else inner

# ---------------------------------------------------------------- HEADER
def header_svg(c):
    h = 280
    uid = "h"
    s = [svg_open(h), defs_and_style(c, uid), panel(c, h, uid, sweep_dur=7, radar=(WIDTH-96, 70, 42))]
    s.append(pulse_dot(c, 52, 52))
    s.append(f'<text x="70" y="57" font-size="12.5" class="accent" letter-spacing="0.5">system online // signal locked</text>')
    name_svg, _ = decode_text(c, uid, 40, 118, "JAVOHIR ABDUVAHHOBOV", 32, begin=0.4, cycle=16, cls="ink sans", glyph_seed=1)
    s.append(f'<g font-weight="800" font-family="{SANS}">{name_svg}</g>')
    s.append(glitch_text(c, uid, 40, 146, "Full-stack & Mobile Developer", 15.5, weight=600, period=6.4, begin=3.1, cls="muted sans"))
    s.append(f'<text x="40" y="170" font-size="12" class="dim">Flutter · Node.js · React · PostgreSQL · Python · ML / DL</text>')

    tx, ty, tw_, th_ = 40, 196, WIDTH - 80, 62
    s.append(f'<rect x="{tx}" y="{ty}" width="{tw_}" height="{th_}" rx="9" fill="{c["off"]}" opacity="0.6" stroke="{c["line"]}" stroke-width="1"/>')
    lines = ["$ whoami", "javohir_abduvahhobov — engineer, root access: full-stack"]
    s.append(f'<text x="{tx+18}" y="{ty+24}" font-size="12" class="accent">{esc(lines[0])}</text>')
    s.append(f'<text x="{tx+18}" y="{ty+44}" font-size="12" class="muted">{esc(lines[1])}</text>')
    kt = "0;0.7;0.71;0.75;0.76;0.8;1"
    base = "$ status --check → shipping . learning . online"
    glitched = "$ status --check → signal . lost . re-sync"
    s.append(f'<text x="{tx+320}" y="{ty+24}" font-size="12" class="muted">{esc(base)}'
              f'<animate attributeName="opacity" values="1;1;0;0;1;1;1" keyTimes="{kt}" dur="8.5s" begin="3s" repeatCount="indefinite"/></text>')
    s.append(f'<text x="{tx+320}" y="{ty+24}" font-size="12" fill="{c["accent"]}" opacity="0">{esc(glitched)}'
              f'<animate attributeName="opacity" values="0;0;1;1;0;0;0" keyTimes="{kt}" dur="8.5s" begin="3s" repeatCount="indefinite"/></text>')
    cx = tx + 320 + tw(base, 12) + 4
    s.append(f'<rect class="cursor{uid}" x="{cx}" y="{ty+13}" width="7" height="13" fill="{c["accent"]}"/>')
    s.append("</svg>")
    return "\n".join(s)

# ---------------------------------------------------------------- REACTOR (new hero)
SATELLITES = [
    ("MOBILE", "flutter / dart"),
    ("BACKEND", "node.js / express"),
    ("DATABASE", "postgresql"),
    ("WEB", "react / ts"),
    ("ML · DL", "python"),
]

def reactor_svg(c):
    h = 340
    uid = "r"
    s = [svg_open(h), defs_and_style(c, uid), panel(c, h, uid, sweep_dur=9, sweep_begin=-2)]
    title_svg, _ = decode_text(c, uid, 40, 48, "SYSTEM CORE", 20, begin=0.2, cycle=15, cls="ink sans", glyph_seed=2)
    s.append(f'<g font-weight="800">{title_svg}</g>')
    s.append(f'<text x="40" y="68" font-size="11.5" class="dim">profile initialized // cross-referencing repositories'
              f'<tspan class="cursor{uid}">_</tspan></text>')

    cx, cy = WIDTH/2, 168
    core_r = 40
    for i, rr in enumerate([90, 122, 156]):
        dashes = ["4,6", "2,5", "6,3"][i]
        ddur = [30, 46, 60][i]
        direction = "360" if i % 2 == 0 else "-360"
        s.append(f'<g><animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="{direction} {cx} {cy}" dur="{ddur}s" repeatCount="indefinite"/>'
                  f'<circle cx="{cx}" cy="{cy}" r="{rr}" fill="none" stroke="{c["line"]}" stroke-width="1.1" stroke-dasharray="{dashes}" opacity="0.85"/></g>')

    s.append(f'<circle cx="{cx}" cy="{cy}" r="{core_r+18}" fill="url(#core{uid})" opacity="0.7">'
              f'<animate attributeName="r" values="{core_r+14};{core_r+24};{core_r+14}" dur="3.2s" repeatCount="indefinite"/></circle>')
    s.append(f'<polygon points="{hex_points(cx,cy,core_r)}" fill="{c["panel"]}" stroke="{c["accent"]}" stroke-width="2">'
              f'<animate attributeName="stroke-width" values="2;3;2" dur="2.4s" repeatCount="indefinite"/></polygon>')
    s.append(f'<text x="{cx}" y="{cy-4}" text-anchor="middle" font-size="11.5" class="accent sans" font-weight="700">JAVOHIR</text>')
    s.append(f'<text x="{cx}" y="{cy+12}" text-anchor="middle" font-size="9.5" class="dim">core v2.0</text>')

    n = len(SATELLITES)
    for i, (label, sub) in enumerate(SATELLITES):
        angle0 = (360 / n) * i - 90
        radius = 150 if i % 2 == 0 else 150
        dur = 34 + i * 5
        direction = 1 if i % 2 == 0 else -1
        s.append(f'<g><animateTransform attributeName="transform" type="rotate" from="{angle0} {cx} {cy}" to="{angle0+direction*360} {cx} {cy}" dur="{dur}s" repeatCount="indefinite"/>')
        s.append(f'<line x1="{cx}" y1="{cy}" x2="{cx+radius}" y2="{cy}" stroke="{c["line"]}" stroke-width="1"/>')
        s.append(f'<circle r="2.4" fill="{c["accent"]}"><animateMotion path="M {cx} {cy} L {cx+radius} {cy}" dur="{2+i*0.3:.1f}s" begin="{i*0.4:.1f}s" repeatCount="indefinite"/>'
                  f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.1;0.9;1" dur="{2+i*0.3:.1f}s" begin="{i*0.4:.1f}s" repeatCount="indefinite"/></circle>')
        s.append(f'<g transform="translate({cx+radius},{cy})">')
        s.append(f'<g><animateTransform attributeName="transform" type="rotate" from="{-(angle0)} 0 0" to="{-(angle0+direction*360)} 0 0" dur="{dur}s" repeatCount="indefinite"/>')
        bw = max(96, tw(label, 11) + 26)
        s.append(f'<rect x="{-bw/2:.1f}" y="-13" width="{bw:.1f}" height="26" rx="13" fill="{c["panel"]}" stroke="{c["accent"]}" stroke-width="1.4"/>')
        s.append(f'<text x="0" y="-1" text-anchor="middle" font-size="10.5" class="ink sans" font-weight="700">{esc(label)}</text>')
        s.append(f'<text x="0" y="10.5" text-anchor="middle" font-size="8" class="dim">{esc(sub)}</text>')
        s.append('</g></g></g>')

    logs = [
        ("OK", "mobile.flutter — build passing"),
        ("OK", "backend.node — 5 tables synced"),
        ("OK", "web.react_ts — deployed"),
        ("..", "ml.deep_learning — training epoch 42"),
    ]
    gx = [40, 500]
    gy = [292, 316]
    idx = 0
    for row in range(2):
        for col_i in range(2):
            if idx >= len(logs):
                break
            tag, text = logs[idx]
            col = c["accent"] if tag == "OK" else c["dim"]
            xx, yy = gx[col_i], gy[row]
            s.append(f'<rect x="{xx}" y="{yy-8}" width="7" height="7" fill="{col}"><animate attributeName="opacity" values="1;0.3;1" dur="1.6s" begin="{idx*0.3}s" repeatCount="indefinite"/></rect>')
            s.append(f'<text x="{xx+14}" y="{yy-2}" font-size="10.5" class="muted">[{esc(tag)}] {esc(text)}</text>')
            idx += 1
    s.append("</svg>")
    return "\n".join(s)

# ---------------------------------------------------------------- WHOAMI
def whoami_svg(c):
    h = 280
    uid = "w"
    s = [svg_open(h), defs_and_style(c, uid), panel(c, h, uid, sweep_dur=8, sweep_begin=-2)]
    s.append(section_head(c, "01", "whoami"))
    tick_svg, _ = decode_text(c, uid, 620, 40, "// ACCESS: ROOT", 10.5, begin=1.2, cycle=17, cls="dim", glyph_seed=3)
    s.append(tick_svg)
    bio = [
        "Software engineer who builds products end-to-end \u2014 from the Flutter",
        "screen a user taps, through the API that authenticates them, down to",
        "the PostgreSQL schema underneath. Software engineering graduate with a",
        "background in Machine Learning, Deep Learning & Data Mining, now",
        "focused on shipping full-stack apps, APIs and the odd game.",
    ]
    first_line_svg, _ = decode_text(c, uid, 40, 92, bio[0], 13.5, begin=0.3, cycle=18, cls="ink", glyph_seed=4)
    s.append(first_line_svg)
    for i, ln in enumerate(bio[1:], start=1):
        s.append(f'<text x="40" y="{92+i*22}" font-size="13.5" class="ink">{esc(ln)}</text>')
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
    footer_svg2, _ = decode_text(c, uid, 40, frow_y + 34, "// clearance granted — full profile privileges unlocked", 10.5, begin=2, cycle=19, cls="dim", glyph_seed=5)
    s.append(footer_svg2)
    s.append("</svg>")
    return "\n".join(s)

# ---------------------------------------------------------------- ECOSYSTEM
def ecosystem_svg(c):
    h = 380
    uid = "e"
    s = [svg_open(h), defs_and_style(c, uid), panel(c, h, uid, sweep_dur=9, sweep_begin=-4)]
    s.append(section_head(c, "02", "ecosystem", sub="system map \u2014 how the pieces talk to each other"))

    bw, bh, by = 160, 56, 104
    x_mobile, x_api, x_db = 70, 400, 730
    s.append(box(c, x_mobile, by, bw, bh, "MOBILE CLIENT", "flutter / dart", accent=True))
    s.append(box(c, x_api, by, bw, bh, "REST API", "node.js / express", accent=True))
    s.append(box(c, x_db, by, bw, bh, "POSTGRESQL", "5 relational tables"))
    s.append(arrow(c, x_mobile+bw, by+bh/2, x_api, by+bh/2, "http + jwt", flow_dur=1.0, flow_begin=0, flicker=True))
    s.append(arrow(c, x_api+bw, by+bh/2, x_db, by+bh/2, "pg pool", flow_dur=1.0, flow_begin=0.5))

    ax, ay = 400, by + bh + 46
    s.append(box(c, ax, ay, bw, 46, "ADMIN PANEL", "html / css / js"))
    s.append(arrow(c, ax+bw/2, ay, ax+bw/2, by+bh, "rest", flow_dur=1.0, flow_begin=0.25))
    s.append(f'<text x="{x_db}" y="{by+bh+22}" font-size="9.5" class="dim">users . jobs . saved_jobs . applications . interviews</text>')

    dy = ay + 46 + 34
    s.append(f'<line x1="40" y1="{dy}" x2="{WIDTH-40}" y2="{dy}" class="line" stroke-width="1" stroke-dasharray="3,4"/>')
    s.append(f'<text x="40" y="{dy+21}" font-size="10.5" class="dim">parallel tracks \u2014 separate from the api above</text>')
    ty2 = dy + 33
    s.append(box(c, 70, ty2, 210, 46, "WEB CLIENT", "react + typescript"))
    s.append(box(c, 375, ty2, 210, 46, "ML / DEEP LEARNING", "python . applied academically"))
    s.append(box(c, 680, ty2, 210, 46, "MOBILE GAME", "flutter / dart"))
    s.append("</svg>")
    return "\n".join(s)

# ---------------------------------------------------------------- STACK
def stack_svg(c):
    h = 320
    uid = "s"
    s = [svg_open(h), defs_and_style(c, uid), panel(c, h, uid, sweep_dur=10, sweep_begin=-6)]
    s.append(section_head(c, "03", "stack"))
    groups = [
        ("mobile", ["Flutter", "Dart", "http", "shared_preferences", "file_picker", "google_fonts", "intl", "cupertino_icons"]),
        ("backend", ["Node.js", "Express", "JWT", "bcryptjs", "multer", "cors", "morgan", "dotenv", "uuid", "pg"]),
        ("web & admin", ["React", "TypeScript", "HTML", "CSS", "JavaScript"]),
        ("data & ml", ["PostgreSQL", "Python", "Machine Learning", "Deep Learning", "Data Mining"]),
        ("also", ["Kotlin", "C", "Android Studio", "Git", "GitHub", "npm"]),
    ]
    y = 78
    for gi, (label, items) in enumerate(groups):
        s.append(f'<circle cx="46" cy="{y+9}" r="2.6" fill="{c["accent"]}"><animate attributeName="opacity" values="1;0.3;1" dur="2s" begin="{gi*0.3}s" repeatCount="indefinite"/></circle>')
        s.append(f'<text x="56" y="{y+13}" font-size="10.5" class="accent" letter-spacing="0.5">{esc(label)}</text>')
        row, y2 = pill_row(c, items, 152, y, WIDTH - 152 - 40, h=22, fs=11, pulse=(gi % 2 == 0))
        s.append(row)
        y = y2 + 13
    s.append("</svg>")
    return "\n".join(s)

# ---------------------------------------------------------------- TRANSMISSION (contact)
def transmission_svg(c):
    h = 220
    uid = "t"
    s = [svg_open(h), defs_and_style(c, uid), panel(c, h, uid, sweep_dur=8, sweep_begin=-1)]

    ticker = " ".join(rnd_alien(3) for _ in range(20))
    s.append(f'<g clip-path="url(#clip{uid})">')
    s.append(f'<text x="0" y="26" font-size="13" class="dim2" letter-spacing="2">{esc(ticker + "   " + ticker)}'
              f'<animateTransform attributeName="transform" type="translate" values="0,0;-900,0" dur="22s" repeatCount="indefinite"/></text>')
    s.append('</g>')

    title_svg, _ = decode_text(c, uid, 40, 76, "LET'S CONNECT", 26, begin=0.3, cycle=15, cls="ink sans", glyph_seed=6)
    s.append(f'<g font-weight="800">{title_svg}</g>')
    s.append(f'<text x="40" y="98" font-size="11.5" class="muted">transmission channel open \u2014 reply time: usually same day</text>')

    by = 130
    bw1 = tw("javohirabduvahhobov@gmail.com", 12.5) + 60
    s.append(f'<rect x="40" y="{by}" width="{bw1:.1f}" height="34" rx="17" fill="{c["panel"]}" stroke="{c["accent"]}" stroke-width="1.4"/>')
    s.append(pulse_dot(c, 62, by+17, r=3, ring_r=9, dur=2.4))
    s.append(f'<text x="78" y="{by+21}" font-size="12.5" class="ink">javohirabduvahhobov@gmail.com</text>')

    gx = 40 + bw1 + 16
    bw2 = tw("github.com/javohir-io", 12.5) + 60
    s.append(f'<rect x="{gx:.1f}" y="{by}" width="{bw2:.1f}" height="34" rx="17" fill="{c["panel"]}" stroke="{c["accent"]}" stroke-width="1.4"/>')
    s.append(pulse_dot(c, gx+22, by+17, r=3, ring_r=9, dur=2.4, begin=0.6))
    s.append(f'<text x="{gx+38:.1f}" y="{by+21}" font-size="12.5" class="ink">github.com/javohir-io</text>')

    sy = by + 34 + 30
    bars_x = WIDTH - 40 - 90
    s.append(f'<text x="{bars_x}" y="{sy-10}" font-size="9.5" class="dim">signal</text>')
    for i in range(8):
        bh = 6 + (i % 4) * 5
        s.append(f'<rect x="{bars_x + i*11}" y="{sy - bh}" width="6" height="{bh}" fill="{c["accent"]}" opacity="0.85">'
                  f'<animate attributeName="height" values="{bh};{bh*0.3:.1f};{bh}" dur="{0.9+i*0.07:.2f}s" repeatCount="indefinite"/>'
                  f'<animate attributeName="y" values="{sy-bh};{sy-bh*0.3:.1f};{sy-bh}" dur="{0.9+i*0.07:.2f}s" repeatCount="indefinite"/>'
                  f'</rect>')

    s.append(f'<text x="40" y="{sy+6}" font-size="10.5" class="dim">status: open to collaborate \u2014 always happy to talk shop</text>')
    s.append("</svg>")
    return "\n".join(s)

# ---------------------------------------------------------------- MATRIX FOOTER
def matrix_footer_svg(c):
    h = 190
    uid = "f"
    s = [svg_open(h), defs_and_style(c, uid), panel(c, h, uid, sweep_dur=7, sweep_begin=-3)]
    s.append(matrix_rain(c, uid, 4, -20, WIDTH-8, h+20, begin=0))
    s.append(f'<rect x="4" y="4" width="{WIDTH-8}" height="{h-8}" rx="20" fill="{c["panel"]}" opacity="0.72"/>')

    s.append(pulse_dot(c, 48, 50))
    s.append(f'<text x="64" y="55" font-size="13" class="ink">currently: sharpening Flutter + Node, exploring more ML-driven side projects</text>')
    s.append(f'<text x="48" y="82" font-size="11.5" class="muted">thanks for scrolling \u2014 open to collaborate, always happy to talk shop.</text>')

    bottom_svg, _ = decode_text(c, uid, 48, 116, "END OF TRANSMISSION", 12.5, begin=1.5, cycle=17, cls="accent2", glyph_seed=7)
    s.append(bottom_svg)

    kt = "0;0.75;0.76;0.8;0.81;0.85;1"
    s.append(f'<text x="{WIDTH-40}" y="82" font-size="10.5" class="dim" text-anchor="end">// EOF'
              f'<animate attributeName="opacity" values="1;1;0;0;1;1;1" keyTimes="{kt}" dur="10s" begin="5s" repeatCount="indefinite"/></text>')
    s.append(f'<text x="{WIDTH-40}" y="82" font-size="10.5" fill="{c["accent"]}" text-anchor="end" opacity="0">// 0x5F'
              f'<animate attributeName="opacity" values="0;0;1;1;0;0;0" keyTimes="{kt}" dur="10s" begin="5s" repeatCount="indefinite"/></text>')
    s.append(f'<text x="{WIDTH-40}" y="150" font-size="9.5" class="dim2" text-anchor="end">javohir-io \u00b7 built with pure svg, no js, no gifs</text>')
    s.append("</svg>")
    return "\n".join(s)

# ---------------------------------------------------------------- DIVIDER
def divider_svg(c):
    h = 40
    uid = "d"
    s = [svg_open(h), defs_and_style(c, uid)]
    midy = h/2
    pts = [(0,midy),(200,midy),(230,midy-12),(WIDTH-230,midy-12),(WIDTH-200,midy),(WIDTH,midy)]
    path_d = "M " + " L ".join(f"{x} {y}" for x, y in pts)
    s.append(f'<path d="{path_d}" fill="none" stroke="{c["line"]}" stroke-width="1.2"/>')
    s.append(f'<circle r="3" fill="{c["accent"]}"><animateMotion path="{path_d}" dur="5s" repeatCount="indefinite"/></circle>')
    for x, y in [(200,midy),(230,midy-12),(WIDTH-230,midy-12),(WIDTH-200,midy)]:
        s.append(f'<circle cx="{x}" cy="{y}" r="2.2" fill="{c["dim"]}"/>')
    s.append(f'<polygon points="{hex_points(WIDTH/2, midy-12, 6)}" fill="{c["panel"]}" stroke="{c["accent"]}" stroke-width="1.3"/>')
    s.append("</svg>")
    return "\n".join(s)

BANNERS = {
    "header.svg": header_svg,
    "reactor.svg": reactor_svg,
    "whoami.svg": whoami_svg,
    "ecosystem.svg": ecosystem_svg,
    "stack.svg": stack_svg,
    "transmission.svg": transmission_svg,
    "footer.svg": matrix_footer_svg,
    "divider.svg": divider_svg,
}

for fname, fn in BANNERS.items():
    with open(os.path.join(OUT_LIGHT, fname), "w") as f:
        f.write(fn(LIGHT))
    with open(os.path.join(OUT_DARK, fname), "w") as f:
        f.write(fn(DARK))

print("done", list(BANNERS.keys()))
