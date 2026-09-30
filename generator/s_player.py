# -*- coding: utf-8 -*-
"""Soundtrack player. GitHub strips <audio>, <iframe> and JavaScript from READMEs, so a *playing* player is impossible
there. This card is a living illustration of one — vinyl spinning, waveform filling, timer ticking over the real
92-second length of the track — and the whole card is a link that opens the track on Spotify."""
import math
import random

from kit import Ctx, frame, border, dust, sparkles, diamond, star4, fade_line, hair, W

TRACK = dict(
    title="Formula",
    artist="Labrinth",
    album="Euphoria: Season 1 Soundtrack, 2019",
    seconds=92,
    url="https://open.spotify.com/track/6EtKlIQmGPB9SX8UjDJG5s",
)


def _envelope(n, seed=7):
    """Slow-building, cinematic amplitude curve with fine-grained variation."""
    rnd = random.Random(seed)
    out = []
    for i in range(n):
        t = i / (n - 1)
        base = 0.28 + 0.5 * math.sin(math.pi * min(1, t * 1.05)) ** 1.4
        swell = 0.12 * math.sin(t * 11) + 0.08 * math.sin(t * 27 + 1.3)
        out.append(max(0.1, min(1, base + swell + rnd.uniform(-0.12, 0.12))))
    return out


def player_svg(c):
    h = 404
    T = TRACK["seconds"]
    x = Ctx(c, "pl", h, title=f"Soundtrack: {TRACK['title']} by {TRACK['artist']}. Click to play on Spotify.",
            desc="Animated player card with a spinning record, a waveform that fills over the length of the track, a running timer and a live spectrum.")
    u = x.uid
    g = c["gold2"] if c["is_dark"] else c["gold"]
    ink = "#120B18"

    # ---------------- defs ----------------
    x.defs(f'''<radialGradient id="glow{u}"><stop offset="0.55" stop-color="{c['rose']}" stop-opacity="0.30"/><stop offset="1" stop-color="{c['rose']}" stop-opacity="0"/></radialGradient>
<linearGradient id="sleeve{u}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#5B3FA8"/><stop offset="0.5" stop-color="#C46A9C"/><stop offset="1" stop-color="#3E8E8C"/></linearGradient>
<linearGradient id="lbl{u}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c['rose']}"/><stop offset="0.5" stop-color="{c['lilac']}"/><stop offset="1" stop-color="{c['aqua']}"/></linearGradient>
<radialGradient id="vinyl{u}"><stop offset="0" stop-color="#1C1424"/><stop offset="1" stop-color="#07040B"/></radialGradient>
<linearGradient id="sheen{u}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.5" stop-color="#fff" stop-opacity="0.16"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<clipPath id="sl{u}"><rect x="56" y="82" width="204" height="204" rx="6"/></clipPath>''')

    # ---------------- vinyl ----------------
    vx, vy, vr = 262, 184, 104
    grooves = "".join(f'<circle cx="{vx}" cy="{vy}" r="{r}" fill="none" stroke="#fff" stroke-opacity="{0.05 if r % 8 else 0.09}"/>'
                      for r in range(44, vr - 4, 4))
    x.css(f"@keyframes spin{u}{{to{{transform:rotate(360deg)}}}}.spin{u}{{transform-origin:{vx}px {vy}px;animation:spin{u} 3.6s linear infinite}}"
          f"@keyframes arm{u}{{from{{transform:rotate(-24deg)}}}}.arm{u}{{transform-origin:392px 74px;animation:arm{u} 2.4s cubic-bezier(.3,.7,.2,1) both}}"
          f"@keyframes bob{u}{{from{{transform:rotate(-.6deg)}}to{{transform:rotate(.6deg)}}}}.bob{u}{{transform-origin:392px 74px;animation:bob{u} 2.8s ease-in-out 2.4s infinite alternate}}")
    wedge = lambda a1, a2: (f"M{vx} {vy} L{vx+vr*math.cos(math.radians(a1)):.1f} {vy+vr*math.sin(math.radians(a1)):.1f} "
                            f"A{vr} {vr} 0 0 1 {vx+vr*math.cos(math.radians(a2)):.1f} {vy+vr*math.sin(math.radians(a2)):.1f} Z")
    vinyl = f'''<circle cx="{vx}" cy="{vy}" r="{vr+34}" fill="url(#glow{u})"/>
<circle cx="{vx}" cy="{vy}" r="{vr}" fill="url(#vinyl{u})" stroke="{c['gold']}" stroke-opacity="0.5"/>
{grooves}
<g class="spin{u}">
  <line x1="{vx}" y1="{vy-vr+5}" x2="{vx}" y2="{vy-vr+15}" stroke="{c['gold2']}" stroke-width="2" stroke-linecap="round"/>
  <circle cx="{vx}" cy="{vy}" r="36" fill="url(#lbl{u})"/>
  <circle cx="{vx}" cy="{vy}" r="36" fill="none" stroke="#fff" stroke-opacity="0.35"/>
  <circle cx="{vx}" cy="{vy}" r="27" fill="none" stroke="{ink}" stroke-opacity="0.35" stroke-dasharray="2 4"/>
  {star4(vx, vy-17, 6, "#fff", 0.9)}
</g>
<path d="{wedge(-52, -22)}" fill="url(#sheen{u})"/><path d="{wedge(128, 158)}" fill="url(#sheen{u})"/>
<circle cx="{vx}" cy="{vy}" r="4.5" fill="{c['bg']}" stroke="{c['gold']}" stroke-opacity="0.8"/>'''

    # ---------------- sleeve ----------------
    rings = "".join(f'<circle cx="230" cy="112" r="{r}" fill="none" stroke="#fff" stroke-opacity="{0.22 - r/900:.2f}"/>' for r in range(30, 240, 26))
    sleeve = f'''<rect x="56" y="82" width="204" height="204" rx="6" fill="url(#sleeve{u})"/>
<g clip-path="url(#sl{u})">{rings}<rect x="56" y="82" width="204" height="204" fill="{ink}" opacity="0.28"/></g>
<text x="76" y="262" font-family="{x_stack_serif()}" font-style="italic" font-size="22" fill="#fff" fill-opacity="0.92">Euphoria</text>
<rect x="56.5" y="82.5" width="203" height="203" rx="6" fill="none" stroke="#fff" stroke-opacity="0.35"/>'''
    x.used["serifi"] |= set("Euphoria")
    sleeve_sparks = sparkles(x, [(96, 118), (170, 152), (222, 214), (120, 208)], seed=44, size=(4, 8))

    # ---------------- tonearm ----------------
    arm = f'''<g class="arm{u}"><g class="bob{u}">
  <path d="M392 74 L392 122 Q392 140 372 156 L330 196" fill="none" stroke="{c['gold2']}" stroke-width="3.2" stroke-linecap="round" stroke-linejoin="round"/>
  <rect x="318" y="190" width="20" height="10" rx="2" transform="rotate(-42 328 195)" fill="{c['gold']}"/>
</g></g>
<circle cx="392" cy="74" r="13" fill="{c['chip_fill']}" stroke="{c['gold']}" stroke-width="1.5"/>
<circle cx="392" cy="74" r="4" fill="{c['gold2']}"/>'''

    # ---------------- right column ----------------
    rx0, rx1 = 452, W - 64
    eq = []
    x.css(f"@keyframes eq{u}{{from{{transform:scaleY(.25)}}to{{transform:scaleY(1)}}}}"
          f".eq{u}{{transform-box:fill-box;transform-origin:bottom;animation:eq{u} .9s ease-in-out infinite alternate}}")
    for i, dur in enumerate([0.7, 1.05, 0.85, 1.2, 0.6]):
        eq.append(f'<rect class="eq{u}" x="{rx0+i*6}" y="{56}" width="3.4" height="16" rx="1.7" fill="{g}" style="animation-duration:{dur}s;animation-delay:-{i*0.23:.2f}s"/>')
    label = x.t("Now spinning", rx0 + 40, 69, 13, g, "sansm", ls=2)
    title = x.t(TRACK["title"], rx0 - 2, 142, 68, c["text"], "serif")
    artist = x.t(TRACK["artist"], rx0, 178, 22, c["text"], "sans", ls=0.6)
    album = x.t(TRACK["album"], rx0, 206, 16, g, "serifi")

    # waveform
    n = 86
    bw, bg_ = 4.0, (rx1 - rx0 - 4.0 * 86) / 85
    env = _envelope(n)
    cy, maxh = 256, 44
    bars_dim, bars_lit = [], []
    for i, e in enumerate(env):
        bx = rx0 + i * (bw + bg_)
        bh = max(4, e * maxh)
        r_ = f'<rect x="{bx:.1f}" y="{cy-bh/2:.1f}" width="{bw}" height="{bh:.1f}" rx="2" fill="%s"/>'
        bars_dim.append(r_ % f'{c["gold"]}" fill-opacity="0.26')
        bars_lit.append(r_ % (g))
    x.defs(f'<clipPath id="prog{u}"><rect x="{rx0-2}" y="{cy-30}" width="0" height="60">'
           f'<animate attributeName="width" from="0" to="{rx1-rx0+4}" dur="{T}s" repeatCount="indefinite"/></rect></clipPath>')
    playhead = (f'<g><line x1="0" y1="{cy-30}" x2="0" y2="{cy+30}" stroke="{c["gold2"]}" stroke-width="1.4" stroke-opacity="0.9"/>'
                f'<circle cy="{cy+34}" r="4.6" fill="{c["gold2"]}"/><circle cy="{cy+34}" r="11" fill="{c["gold2"]}" opacity="0.18"/>'
                f'<animateTransform attributeName="transform" type="translate" from="{rx0}" to="{rx1}" dur="{T}s" repeatCount="indefinite"/></g>')

    # timer: one text per second, each visible for exactly one second of the 92 s loop
    x.css(f"@keyframes tm{u}{{0%{{opacity:1}}{100/T:.4f}%{{opacity:0}}100%{{opacity:0}}}}"
          f".tm{u}{{opacity:0;animation:tm{u} {T}s steps(1,end) infinite}}")
    x.reduced.append(f".t0{u}{{opacity:1!important}}")
    timers = []
    for s in range(T + 1):
        s_ = min(s, T)
        timers.append(x.t(f"{s_//60}:{s_%60:02d}", rx0, 316, 13.5, c["text2"], "sansm", ls=0.6,
                          cls=f"tm{u}" + (f" t0{u}" if s == 0 else ""), style=f"animation-delay:{s}s"))
    total = x.t(f"{T//60}:{T%60:02d}", rx1, 316, 13.5, c["text3"], "sansm", anchor="end", ls=0.6)

    # controls
    ccx, ccy = rx0 + 58, 358
    x.css(f"@keyframes pr{u}{{from{{r:22;opacity:.6}}to{{r:36;opacity:0}}}}.pr{u}{{animation:pr{u} 2.6s ease-out infinite}}")
    controls = f'''<g fill="none" stroke="{c['text2']}" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round">
  <path d="M{ccx-64} {ccy-8} V{ccy+8}"/><path d="M{ccx-44} {ccy-9} L{ccx-56} {ccy} L{ccx-44} {ccy+9} Z" fill="{c['text2']}"/>
  <path d="M{ccx+64} {ccy-8} V{ccy+8}"/><path d="M{ccx+44} {ccy-9} L{ccx+56} {ccy} L{ccx+44} {ccy+9} Z" fill="{c['text2']}"/></g>
<circle class="pr{u}" cx="{ccx}" cy="{ccy}" r="22" fill="none" stroke="{c['gold2']}" stroke-width="1.4"/>
<circle cx="{ccx}" cy="{ccy}" r="22" fill="{c['gold2'] if c['is_dark'] else c['gold']}"/>
<path d="M{ccx-6} {ccy-10} L{ccx+11} {ccy} L{ccx-6} {ccy+10} Z" fill="{ink if c['is_dark'] else '#fff'}"/>'''

    # spotify pill
    pw, ph_, px_, py_ = 216, 42, rx1 - 216, 337
    sg = f"translate({px_+26} {py_+ph_/2})"
    pill = f'''<rect x="{px_}" y="{py_}" width="{pw}" height="{ph_}" rx="21" fill="none" stroke="{c['gold']}" stroke-opacity="0.9"/>
<g transform="{sg}"><circle r="10" fill="{g}"/><g fill="none" stroke="{ink if c['is_dark'] else '#fff'}" stroke-width="1.7" stroke-linecap="round">
<path d="M-5.6 -2.8 Q0 -5 5.8 -1.8"/><path d="M-4.6 0.8 Q0 -0.8 4.8 1.6"/><path d="M-3.6 4.2 Q0 3 3.8 4.4"/></g></g>
{x.t("Play on Spotify", px_+46, py_+ph_/2+5, 14.5, c['text'], "sansm", ls=0.4)}'''

    # spectrum along the bottom edge
    rnd = random.Random(3)
    x.css(f"@keyframes sp{u}{{from{{transform:scaleY(.12)}}to{{transform:scaleY(1)}}}}"
          f".sp{u}{{transform-box:fill-box;transform-origin:bottom;animation:sp{u} 1s ease-in-out infinite alternate}}")
    spec = []
    nb = 72
    for i in range(nb):
        bx = 20 + i * (960 / nb)
        env_ = 0.35 + 0.65 * math.sin(math.pi * i / nb) ** 0.8
        hh = (8 + rnd.random() * 14) * env_ + 4
        spec.append(f'<rect class="sp{u}" x="{bx:.1f}" y="{h-12-hh:.1f}" width="6" height="{hh:.1f}" rx="2" fill="{c["gold"]}" fill-opacity="0.34" '
                    f'style="animation-duration:{0.55+rnd.random()*0.9:.2f}s;animation-delay:-{rnd.random()*2:.2f}s"/>')

    body = "\n".join([
        frame(x, r=6),
        f'<g clip-path="url(#clip{u})">{dust(x, 22, seed=91, rise=90, y1=h-30)}</g>',
        f'<g clip-path="url(#clip{u})">{"".join(spec)}</g>',
        f'<g transform="translate(0 12)">{vinyl}{sleeve}{sleeve_sparks}{arm}</g>',
        "".join(eq), label, title, artist, album,
        "".join(bars_dim), f'<g clip-path="url(#prog{u})">{"".join(bars_lit)}</g>', playhead,
        "".join(timers), total, controls, pill,
        sparkles(x, [(960, 50), (430, 34), (600, 100)], seed=12),
        border(x, r=6, chase=True),
    ])
    return x.render(body)


def x_stack_serif():
    import typo
    return typo.FONTS["serifi"]["stack"]
