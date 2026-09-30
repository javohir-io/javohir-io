# -*- coding: utf-8 -*-
"""Soundtrack player, drawn as a chronograph.

GitHub strips <audio>, <iframe> and JavaScript from READMEs, so a *playing* player cannot exist there.
This card is a living illustration of one: the dial's 92 ticks are the 92 seconds of the track, the sweep hand
makes one lap per play, the waveform fills and the timer counts in step. The whole card links to Spotify."""
import math
import random

from kit import Ctx, frame, border, rosette, sq, hair, fade_line, cross, chamfer, gt, W

TRACK = dict(title="Formula", artist="Labrinth", album="Euphoria: Season 1 Soundtrack, 2019", seconds=92)


def _envelope(n, seed=7):
    rnd = random.Random(seed)
    out = []
    for i in range(n):
        t = i / (n - 1)
        base = 0.28 + 0.5 * math.sin(math.pi * min(1, t * 1.05)) ** 1.4
        out.append(max(0.1, min(1, base + 0.12 * math.sin(t * 11) + 0.08 * math.sin(t * 27 + 1.3) + rnd.uniform(-0.12, 0.12))))
    return out


def player_svg(c):
    h = 460
    T = TRACK["seconds"]
    x = Ctx(c, "pl", h, title=f"Soundtrack: {TRACK['title']} by {TRACK['artist']}. Click to play on Spotify.",
            desc="Chronograph-style player card: a dial whose ticks are the seconds of the track, a sweep hand, a spinning record, a filling waveform and a running timer.")
    u = x.uid
    g = gt(c)
    ink = c["ink"]
    cx, cy = 250, 226

    x.defs(f'''<radialGradient id="vin{u}"><stop offset="0" stop-color="#1B2326"/><stop offset="1" stop-color="#050708"/></radialGradient>
<linearGradient id="lbl{u}" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{c['gold2']}"/><stop offset="0.55" stop-color="{c['gold']}"/><stop offset="1" stop-color="{c['gold3']}"/></linearGradient>
<linearGradient id="shn{u}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.5" stop-color="#fff" stop-opacity="0.13"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<radialGradient id="dg{u}"><stop offset="0.6" stop-color="{c['emerald']}" stop-opacity="0.22"/><stop offset="1" stop-color="{c['emerald']}" stop-opacity="0"/></radialGradient>''')

    # --- bezel + knurling -------------------------------------------------
    knurl = "".join(f"M{cx+157*math.cos(math.radians(a)):.1f} {cy+157*math.sin(math.radians(a)):.1f}L{cx+163*math.cos(math.radians(a)):.1f} {cy+163*math.sin(math.radians(a)):.1f}"
                    for a in [i * 3 for i in range(120)])
    bezel = (f'<circle cx="{cx}" cy="{cy}" r="190" fill="url(#dg{u})"/>'
             f'<circle cx="{cx}" cy="{cy}" r="164" fill="{c["bg"]}" fill-opacity="0.75" stroke="{c["gold"]}" stroke-opacity="0.7"/>'
             f'<path d="{knurl}" stroke="{c["steel"]}" stroke-opacity="0.5" fill="none"/>'
             f'<circle cx="{cx}" cy="{cy}" r="152" fill="none" stroke="{c["steel"]}" stroke-opacity="0.25"/>')

    # --- 92 second ticks (each lights as the hand passes, then fades) ----------
    x.css(f"@keyframes tk{u}{{0%{{stroke:{c['gold2']};stroke-opacity:1}}10%,100%{{stroke:{c['steel']};stroke-opacity:.38}}}}"
          f".tk{u}{{stroke:{c['steel']};stroke-opacity:.38;stroke-width:1.4;animation:tk{u} {T}s linear infinite}}")
    tk = []
    for i in range(T):
        a = math.radians(i / T * 360 - 90)
        r0 = 126 if i % 10 == 0 else 136
        tk.append(f'<line class="tk{u}" x1="{cx+r0*math.cos(a):.1f}" y1="{cy+r0*math.sin(a):.1f}" x2="{cx+146*math.cos(a):.1f}" y2="{cy+146*math.sin(a):.1f}" style="animation-delay:{i}s"/>')
    nums = []
    for s in range(10, T - 5, 10):
        a = math.radians(s / T * 360 - 90)
        nums.append(x.t(str(s), cx + 112 * math.cos(a), cy + 112 * math.sin(a) + 4, 11, c["text3"], "sansm", anchor="middle", ls=0.4))
    x.css(f"@keyframes pg{u}{{from{{stroke-dashoffset:92}}to{{stroke-dashoffset:0}}}}.pg{u}{{animation:pg{u} {T}s linear infinite}}")
    arc = (f'<circle cx="{cx}" cy="{cy}" r="150" fill="none" stroke="{c["gold"]}" stroke-opacity="0.16" stroke-width="2"/>'
           f'<circle class="pg{u}" cx="{cx}" cy="{cy}" r="150" fill="none" stroke="{c["gold2"]}" stroke-width="2.4" pathLength="92" '
           f'stroke-dasharray="92 92" stroke-dashoffset="92" transform="rotate(-90 {cx} {cy})"/>')

    # --- record -------------------------------------------------------------
    vr = 88
    grooves = "".join(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#fff" stroke-opacity="{0.05 if r % 8 else 0.1}"/>' for r in range(32, vr - 3, 4))
    wedge = lambda a1, a2: (f"M{cx} {cy} L{cx+vr*math.cos(math.radians(a1)):.1f} {cy+vr*math.sin(math.radians(a1)):.1f} "
                            f"A{vr} {vr} 0 0 1 {cx+vr*math.cos(math.radians(a2)):.1f} {cy+vr*math.sin(math.radians(a2)):.1f} Z")
    x.css(f"@keyframes sp{u}{{to{{transform:rotate(360deg)}}}}.sp{u}{{transform-origin:{cx}px {cy}px;animation:sp{u} 3.4s linear infinite}}"
          f"@keyframes sw{u}{{to{{transform:rotate(360deg)}}}}.sw{u}{{transform-origin:{cx}px {cy}px;animation:sw{u} {T}s linear infinite}}")
    record = (f'<circle cx="{cx}" cy="{cy}" r="{vr}" fill="url(#vin{u})" stroke="{c["gold"]}" stroke-opacity="0.45"/>{grooves}'
              f'<g class="sp{u}"><circle cx="{cx}" cy="{cy}" r="30" fill="url(#lbl{u})"/>'
              f'<circle cx="{cx}" cy="{cy}" r="22" fill="none" stroke="{ink}" stroke-opacity="0.35" stroke-dasharray="2 4"/>'
              f'<rect x="{cx-2}" y="{cy-27}" width="4" height="9" fill="{ink}" fill-opacity="0.6"/></g>'
              f'<path d="{wedge(-50, -20)}" fill="url(#shn{u})"/><path d="{wedge(130, 160)}" fill="url(#shn{u})"/>')
    hand = (f'<g class="sw{u}"><line x1="{cx}" y1="{cy+30}" x2="{cx}" y2="{cy-148}" stroke="{c["gold2"]}" stroke-width="1.8"/>'
            f'<rect x="{cx-3}" y="{cy+22}" width="6" height="18" fill="{c["gold2"]}"/>'
            f'<rect x="{cx-2.5}" y="{cy-146}" width="5" height="16" fill="{c["good"]}"/></g>'
            f'<circle cx="{cx}" cy="{cy}" r="6.5" fill="{c["bg"]}" stroke="{c["gold2"]}" stroke-width="1.6"/><circle cx="{cx}" cy="{cy}" r="2" fill="{c["gold2"]}"/>')

    # --- right column ---------------------------------------------------------
    rx0, rx1 = 480, W - 70
    x.css(f"@keyframes eq{u}{{from{{transform:scaleY(.25)}}to{{transform:scaleY(1)}}}}.eq{u}{{transform-box:fill-box;transform-origin:bottom;animation:eq{u} .9s ease-in-out infinite alternate}}")
    eq = "".join(f'<rect class="eq{u}" x="{rx0+i*6}" y="78" width="3" height="16" fill="{g}" style="animation-duration:{d}s;animation-delay:-{i*0.23:.2f}s"/>'
                 for i, d in enumerate([0.7, 1.05, 0.85, 1.2, 0.6]))
    head = "\n".join([
        eq, x.t("NOW SPINNING", rx0 + 40, 91, 12, g, "sansm", ls=3.4),
        x.t(TRACK["title"], rx0 - 3, 180, 84, c["text"], "serif"),
        x.t(TRACK["artist"].upper(), rx0, 220, 17, c["text"], "sansm", ls=8),
        x.t(TRACK["album"], rx0, 250, 16, c["text3"] if not c["is_dark"] else c["text2"], "serifi"),
        hair(rx0, rx0 + 70, 268, c["gold"], 0.9, 2),
    ])

    n = 94
    bw = 3.0
    gap = (rx1 - rx0 - bw * n) / (n - 1)
    env = _envelope(n)
    wy, maxh = 322, 46
    dim, lit = [], []
    for i, e in enumerate(env):
        bx = rx0 + i * (bw + gap)
        bh = max(4, e * maxh)
        r_ = f'<rect x="{bx:.1f}" y="{wy-bh/2:.1f}" width="{bw}" height="{bh:.1f}" fill="%s"/>'
        dim.append(r_ % f'{c["steel"]}" fill-opacity="0.3')
        lit.append(r_ % g)
    x.defs(f'<clipPath id="prog{u}"><rect x="{rx0-2}" y="{wy-32}" width="0" height="64"><animate attributeName="width" from="0" to="{rx1-rx0+4}" dur="{T}s" repeatCount="indefinite"/></rect></clipPath>')
    playhead = (f'<g><line x1="0" y1="{wy-32}" x2="0" y2="{wy+32}" stroke="{c["gold2"]}" stroke-width="1.4"/>'
                f'<rect x="-4" y="{wy+32}" width="8" height="8" fill="{c["gold2"]}"/>'
                f'<animateTransform attributeName="transform" type="translate" from="{rx0}" to="{rx1}" dur="{T}s" repeatCount="indefinite"/></g>')

    x.css(f"@keyframes tm{u}{{0%{{opacity:1}}{100/T:.4f}%{{opacity:0}}100%{{opacity:0}}}}.tm{u}{{opacity:0;animation:tm{u} {T}s steps(1,end) infinite}}")
    x.reduced.append(f".t0{u}{{opacity:1!important}}")
    timers = [x.t(f"{s//60}:{s%60:02d}", rx0, 378, 14, c["text2"], "sansm", ls=1, cls=f"tm{u}" + (f" t0{u}" if s == 0 else ""), style=f"animation-delay:{s}s") for s in range(T + 1)]
    total = x.t(f"{T//60}:{T%60:02d}", rx1, 378, 14, c["text3"], "sansm", anchor="end", ls=1)

    # controls
    ccx, ccy = rx0 + 60, 414
    x.css(f"@keyframes pr{u}{{from{{r:24;opacity:.7}}to{{r:38;opacity:0}}}}.pr{u}{{animation:pr{u} 2.6s ease-out infinite}}")
    ctl = (f'<g stroke="{c["text2"]}" stroke-width="1.7" fill="{c["text2"]}" stroke-linejoin="round">'
           f'<path d="M{ccx-72} {ccy-8}V{ccy+8}" fill="none"/><path d="M{ccx-50} {ccy-9}L{ccx-62} {ccy}L{ccx-50} {ccy+9}Z"/>'
           f'<path d="M{ccx+72} {ccy-8}V{ccy+8}" fill="none"/><path d="M{ccx+50} {ccy-9}L{ccx+62} {ccy}L{ccx+50} {ccy+9}Z"/></g>'
           f'<circle class="pr{u}" cx="{ccx}" cy="{ccy}" r="24" fill="none" stroke="{c["gold2"]}" stroke-width="1.3"/>'
           f'<circle cx="{ccx}" cy="{ccy}" r="24" fill="{g}"/>'
           f'<path d="M{ccx-6} {ccy-10}L{ccx+11} {ccy}L{ccx-6} {ccy+10}Z" fill="{ink}"/>')
    pw, ph, px, py = 230, 44, rx1 - 230, ccy - 22
    btn = (f'<polygon points="{chamfer(px, py, pw, ph, 12)}" fill="none" stroke="{c["gold"]}" stroke-width="1.2"/>'
           f'<g transform="translate({px+28} {ccy})"><circle r="10" fill="{g}"/><g fill="none" stroke="{ink}" stroke-width="1.7" stroke-linecap="round">'
           f'<path d="M-5.6 -2.8Q0 -5 5.8 -1.8"/><path d="M-4.6 0.8Q0 -0.8 4.8 1.6"/><path d="M-3.6 4.2Q0 3 3.8 4.4"/></g></g>'
           + x.t("PLAY ON SPOTIFY", px + 50, ccy + 4.5, 12.5, c["text"], "sansm", ls=2.4))

    # spectrum
    rnd = random.Random(3)
    x.css(f"@keyframes spc{u}{{from{{transform:scaleY(.12)}}to{{transform:scaleY(1)}}}}.spc{u}{{transform-box:fill-box;transform-origin:bottom;animation:spc{u} 1s ease-in-out infinite alternate}}")
    nb, spec = 120, []
    for i in range(nb):
        bx = 30 + i * (940 / nb)
        env_ = 0.3 + 0.7 * math.sin(math.pi * i / nb) ** 0.8
        hh = (6 + rnd.random() * 14) * env_ + 3
        spec.append(f'<rect class="spc{u}" x="{bx:.1f}" y="{h-16-hh:.1f}" width="2.4" height="{hh:.1f}" fill="{c["steel"]}" fill-opacity="0.32" '
                    f'style="animation-duration:{0.55+rnd.random()*0.9:.2f}s;animation-delay:-{rnd.random()*2:.2f}s"/>')

    body = "\n".join([
        frame(x, scan=False),
        f'<g clip-path="url(#clip{u})">{rosette(x, 700, 220, 300, 30, 220, c["steel"], 0.09 if c["is_dark"] else 0.14)}{"".join(spec)}</g>',
        bezel, arc, "".join(tk), "".join(nums), record, hand,
        head, "".join(dim), f'<g clip-path="url(#prog{u})">{"".join(lit)}</g>', playhead,
        "".join(timers), total, ctl, btn,
        cross(rx1, 78, 6, c["gold"], 0.7),
        border(x, chase=True),
    ])
    return x.render(body)
