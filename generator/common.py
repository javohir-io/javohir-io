# -*- coding: utf-8 -*-
import random
from xml.sax.saxutils import escape as _esc

WIDTH = 1000
MONO = "'JetBrains Mono', 'Fira Code', Consolas, monospace"
SANS = "'Segoe UI', Inter, Helvetica, Arial, sans-serif"
SCRAMBLE = list("01▓▒░#%&@*+-=<>/\\{}[]ABCDEFGHIJKLMNOPQRSTUVWXYZ")

LIGHT = dict(
    bg="#ffffff", bg2="#f6f8fa", panel="#ffffff", border="#d0d7de",
    frame="#0969da", text="#1f2328", text2="#57606a", text3="#8c959f",
    accent="#0969da", accent2="#8250df", good="#1a7f37",
    rain_head="#0b3d24", rain_body="#2da44e",
    chip_bg="#f6f8fa", chip_border="#d0d7de",
)
DARK = dict(
    bg="#05070a", bg2="#0a0e14", panel="#0a0e14", border="#1c2530",
    frame="#22d3ee", text="#e6edf3", text2="#8b949e", text3="#5b6572",
    accent="#22d3ee", accent2="#a78bfa", good="#3fb950",
    rain_head="#eafff2", rain_body="#39ff8f",
    chip_bg="#0d1420", chip_border="#1c2530",
)


def esc(s):
    return _esc(str(s))


def svg_open(h, w=WIDTH, title="section"):
    return (f'<svg width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'role="img" aria-label="{esc(title)}">')


def frame_defs(c, uid, w, h, radius=16):
    """Rounded panel background + hairline border + corner HUD brackets."""
    bl = 22  # bracket length
    corners = f'''
  <g stroke="{c['frame']}" stroke-width="1.5" fill="none" opacity="0.85">
    <path d="M1 {bl} V1 H{bl}"/>
    <path d="M{w-bl} 1 H{w-1} V{bl}"/>
    <path d="M{w-1} {h-bl} V{h-1} H{w-bl}"/>
    <path d="M{bl} {h-1} H1 V{h-bl}"/>
  </g>'''
    return f'''<defs>
    <clipPath id="clip{uid}"><rect x="0" y="0" width="{w}" height="{h}" rx="{radius}" ry="{radius}"/></clipPath>
    <linearGradient id="bgg{uid}" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="{c['bg']}"/>
      <stop offset="100%" stop-color="{c['bg2']}"/>
    </linearGradient>
    <radialGradient id="glow{uid}" cx="50%" cy="0%" r="75%">
      <stop offset="0%" stop-color="{c['accent']}" stop-opacity="0.16"/>
      <stop offset="100%" stop-color="{c['accent']}" stop-opacity="0"/>
    </radialGradient>
    <filter id="softglow{uid}" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="2" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <g clip-path="url(#clip{uid})">
    <rect x="0" y="0" width="{w}" height="{h}" fill="url(#bgg{uid})"/>
    <rect x="0" y="0" width="{w}" height="{h}" fill="url(#glow{uid})"/>
  </g>
  <rect x="1" y="1" width="{w-2}" height="{h-2}" rx="{radius}" ry="{radius}" fill="none" stroke="{c['border']}" stroke-width="1"/>
  {corners}'''


def decode_text(uid, key, text, x, y, size, color, ghost, anchor="start",
                 weight="700", family=None, spacing=None, cycle=3.0,
                 frame_dur=0.055, steps=5, gap=0.25, seed=None):
    """Returns (css_rules, svg_markup) for a per-character 'decode from noise' loop."""
    family = family or MONO
    r = random.Random(seed if seed is not None else hash((uid, key, text)) & 0xffffffff)
    frames = []
    for _ in range(steps - 1):
        frames.append("".join(ch if ch == " " else r.choice(SCRAMBLE) for ch in text))
    frames.append(text)

    bounds = [i * frame_dur for i in range(steps)]
    bounds.append(max(cycle - gap, bounds[-1] + frame_dur))
    css, els = [], []
    attrs = f'x="{x}" y="{y}" text-anchor="{anchor}" font-family="{family}" font-weight="{weight}" font-size="{size}"'
    if spacing:
        attrs += f' letter-spacing="{spacing}"'
    for i, frame in enumerate(frames):
        s_pct = bounds[i] / cycle * 100
        e_pct = bounds[i + 1] / cycle * 100
        e_pct = min(e_pct, 99.9)
        s_pct = min(s_pct, e_pct - 0.05)
        name = f"dc{uid}{key}{i}"
        css.append(
            f'@keyframes {name}{{0%{{opacity:0}} {s_pct:.3f}%{{opacity:0}} '
            f'{min(s_pct+0.3,e_pct):.3f}%{{opacity:1}} {e_pct:.3f}%{{opacity:1}} '
            f'{min(e_pct+0.3,99.95):.3f}%{{opacity:0}} 100%{{opacity:0}}}}'
        )
        fill = color if i == steps - 1 else ghost
        op = "" if i == steps - 1 else 'opacity="0.75"'
        style = (f'animation:{name} {cycle}s steps(1) infinite;')
        els.append(f'<text {attrs} fill="{fill}" {op} style="{style}">{esc(frame)}</text>')
    return "\n".join(css), "\n".join(els)


def rain_columns(uid, seed, color_head, color_body, w, h, n_cols=40, char_h=15, rows=10):
    random.seed(seed)
    spacing = w / n_cols
    cols = []
    for i in range(n_cols):
        x = round(i * spacing + random.uniform(-3, 3), 1)
        dur = round(random.uniform(4.0, 9.0), 2)
        delay = round(random.uniform(-9, 0), 2)
        chars = [random.choice(SCRAMBLE) for _ in range(rows)]
        tspans = []
        for j, ch in enumerate(chars):
            op = 1 if j == 0 else max(0.05, 0.5 - j * 0.055)
            fill = color_head if j == 0 else color_body
            dy = 0 if j == 0 else char_h
            tspans.append(f'<tspan x="{x}" dy="{dy}" fill="{fill}" opacity="{op:.2f}">{esc(ch)}</tspan>')
        cols.append(
            f'<text class="rain{uid}" font-family="{MONO}" font-size="13" '
            f'style="animation-duration:{dur}s;animation-delay:{delay}s">{"".join(tspans)}</text>'
        )
    fall_h = rows * char_h + 40
    css = f'''@keyframes fall{uid}{{
      0%{{transform:translateY(-{fall_h}px);opacity:0}}
      8%{{opacity:1}} 92%{{opacity:1}}
      100%{{transform:translateY({h+40}px);opacity:0}}
    }}
    .rain{uid}{{animation-name:fall{uid};animation-timing-function:linear;animation-iteration-count:infinite}}'''
    return css, "\n".join(cols)


def chip(c, x, y, text, uid="chp", key="", w=None, h=28, delay=0.0, dur=3.0, seed=None):
    """Chip pill whose label glitches/decodes on the same ~3s cadence as everything else."""
    w = w or (len(text) * 7.2 + 26)
    css, txt_svg = decode_text(uid, key or text, text, x + w / 2, y + h / 2 + 4, 12.5,
                                c["text"], c["accent"], anchor="middle", weight="600",
                                cycle=dur, steps=4, gap=0.3, seed=seed)
    box = f'''<g>
    <rect x="{x}" y="{y}" width="{w:.0f}" height="{h}" rx="7" fill="{c['chip_bg']}" stroke="{c['chip_border']}" stroke-width="1"/>
    {txt_svg}
  </g>'''
    return css, box, w


CHIP_PULSE_CSS = "@keyframes chippulse{0%,100%{opacity:0.82}50%{opacity:1}}"


def panel_rain(uid, seed, c, w, h, n_cols=34, opacity=0.16):
    """A subtle full-panel letter/number rain layer, meant to sit under content."""
    css, svg = rain_columns(uid, seed, c["rain_head"], c["rain_body"], w, h, n_cols=n_cols, rows=max(6, h // 22))
    return css, f'<g opacity="{opacity}">{svg}</g>'
