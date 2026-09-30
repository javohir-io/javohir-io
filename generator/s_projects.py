# -*- coding: utf-8 -*-
import random
from collections import deque

import typo
from kit import (Ctx, frame, border, rosette, sq, hair, fade_line, cross, flow_dot, link_path, paragraph, card, chamfer, gt, W)


def abox(x, bx, by, bw, bh, title, sub, hot=False):
    c = x.c
    return (f'<polygon points="{chamfer(bx, by, bw, bh, 9)}" fill="{c["chip_fill"]}" stroke="{c["gold"]}" stroke-opacity="{0.9 if hot else 0.45}" stroke-width="{1.4 if hot else 1}"/>'
            + x.t(title, bx + bw / 2, by + bh / 2 - 1, 14, c["text"], "sansm", anchor="middle", ls=0.4)
            + x.t(sub, bx + bw / 2, by + bh / 2 + 16, 11.5, c["text3"], "sans", anchor="middle"))


def tech_line(x, items, px, py):
    return x.t("  /  ".join(i.upper() for i in items), px, py, 11.5, gt(x.c), "sansm", ls=2.4)


def bracket_box(x, x0, y0, x1, y1):
    c = x.c
    s = 16
    d = (f"M{x0} {y0+s}V{y0}H{x0+s}M{x1-s} {y0}H{x1}V{y0+s}M{x1} {y1-s}V{y1}H{x1-s}M{x0+s} {y1}H{x0}V{y1-s}")
    return f'<path d="{d}" fill="none" stroke="{c["steel"]}" stroke-opacity="0.55"/>'


def _panel(x, title, tagline, tech, cat, text_x, cw):
    c = x.c
    size = 60
    while x.w_(title, "serif", size) > cw and size > 30:
        size -= 2
    out = [x.t(cat.upper(), text_x, 96, 11.5, gt(c), "sansm", ls=3.4),
           fade_line(x, text_x, text_x + 44, 108, "cat", 1, both=False, sw=2),
           x.t(title, text_x, 176, size, c["text"], "serif")]
    p, y = paragraph(x, tagline, text_x, 214, cw, 16.5, c["text2"], lh=27)
    out.append(p)
    out.append(tech_line(x, tech, text_x, y + 26))
    return "\n".join(out), y + 26


def oson_svg(c):
    h = 340
    x = Ctx(c, "os", h, title="OsonIjara: full-stack rental-listing platform",
            desc="Flutter app on Netlify talks to FastAPI on Render over REST and WebSockets, with PostgreSQL on Neon and optional Cloudflare R2.")
    u = x.uid
    txt, _ = _panel(x, "OsonIjara", "Rental listings with real-time chat and admin moderation.",
                    ["Flutter", "FastAPI", "PostgreSQL", "WebSockets"], "Full stack", 76, 430)
    d0, d1 = 552, W - 64
    bw, by = 84, 128
    xs = [d0 + 6, d0 + 6 + (d1 - d0 - 12 - bw) / 2, d1 - 6 - bw]
    boxes = [abox(x, xs[0], by, bw, 66, "Flutter", "Netlify"), abox(x, xs[1], by, bw, 66, "FastAPI", "Render", hot=True),
             abox(x, xs[2], by, bw, 66, "PostgreSQL", "Neon"), abox(x, xs[1], 236, bw, 50, "R2", "Optional")]
    ym = by + 33
    links = [link_path(x, f"rest{u}", f"M{xs[0]+bw} {ym+8}H{xs[1]}"),
             link_path(x, f"ws{u}", f"M{xs[1]} {ym-8}H{xs[0]+bw}", color=c["good"], op=0.8),
             link_path(x, f"db{u}", f"M{xs[1]+bw} {ym}H{xs[2]}"),
             link_path(x, f"r2{u}", f"M{xs[1]+bw/2} {by+66}V236", op=0.4)]
    dots = (flow_dot(x, f"rest{u}", 1.8, 0) + flow_dot(x, f"ws{u}", 1.8, 0.7, color=c["good"])
            + flow_dot(x, f"db{u}", 1.8, 0.3) + flow_dot(x, f"db{u}", 1.8, 1.2))
    labels = (x.t("REST", (xs[0] + bw + xs[1]) / 2, ym + 26, 10.5, c["text3"], "sansm", anchor="middle", ls=2)
              + x.t("WS", (xs[0] + bw + xs[1]) / 2, ym - 20, 10.5, c["good"], "sansm", anchor="middle", ls=2))
    body = "\n".join([frame(x), f'<g clip-path="url(#clip{u})">{rosette(x, 780, 170, 210, 26, 200, c["steel"], 0.09 if c["is_dark"] else 0.14)}</g>',
                      txt, bracket_box(x, d0 - 12, 78, d1 + 12, 306), *links, dots, *boxes, labels, border(x)])
    return x.render(body)


def career_svg(c):
    h = 340
    x = Ctx(c, "cp", h, title="Career Services Portal: full-stack internship and career platform",
            desc="A Flutter student app and an HTML admin panel share one Express API backed by PostgreSQL.")
    u = x.uid
    txt, _ = _panel(x, "Career Services Portal", "Internships, applications and interview scheduling for students.",
                    ["Flutter", "Node.js", "Express", "PostgreSQL"], "Full stack", 540, 384)
    d0, d1 = 64, 478
    bw = 92
    cyy = 186
    xa, xb, xc = d0 + 6, d0 + 6 + 156, d1 - 6 - bw
    boxes = [abox(x, xa, cyy - 92, bw, 58, "Flutter", "Students"), abox(x, xa, cyy + 34, bw, 58, "Admin", "HTML, JS"),
             abox(x, xb, cyy - 33, bw, 66, "Express", "JWT, Multer", hot=True), abox(x, xc, cyy - 33, bw, 66, "PostgreSQL", "Data")]
    links = [link_path(x, f"a{u}", f"M{xa+bw} {cyy-63}C{xb-30} {cyy-63} {xb-30} {cyy-8} {xb} {cyy-8}"),
             link_path(x, f"b{u}", f"M{xa+bw} {cyy+63}C{xb-30} {cyy+63} {xb-30} {cyy+8} {xb} {cyy+8}"),
             link_path(x, f"d{u}", f"M{xb+bw} {cyy}H{xc}")]
    dots = (flow_dot(x, f"a{u}", 2.0, 0) + flow_dot(x, f"b{u}", 2.0, 0.8) + flow_dot(x, f"d{u}", 1.4, 0.2) + flow_dot(x, f"d{u}", 1.4, 0.9))
    body = "\n".join([frame(x), f'<g clip-path="url(#clip{u})">{rosette(x, 260, 170, 210, 26, 200, c["steel"], 0.09 if c["is_dark"] else 0.14)}</g>',
                      txt, bracket_box(x, d0 - 12, 78, d1 + 12, 306), *links, dots, *boxes, border(x)])
    return x.render(body)


# ------------------------------------------------------------------ small tiles
def _maze(cols, rows, seed):
    rnd = random.Random(seed)
    right = [[True] * cols for _ in range(rows)]
    down = [[True] * cols for _ in range(rows)]
    seen = [[False] * cols for _ in range(rows)]
    stack = [(0, 0)]
    seen[0][0] = True
    while stack:
        cx, cy = stack[-1]
        nb = [(nx, ny, d) for nx, ny, d in [(cx+1, cy, "r"), (cx-1, cy, "l"), (cx, cy+1, "d"), (cx, cy-1, "u")]
              if 0 <= nx < cols and 0 <= ny < rows and not seen[ny][nx]]
        if not nb:
            stack.pop(); continue
        nx, ny, d = rnd.choice(nb)
        if d == "r": right[cy][cx] = False
        if d == "l": right[ny][nx] = False
        if d == "d": down[cy][cx] = False
        if d == "u": down[ny][nx] = False
        seen[ny][nx] = True
        stack.append((nx, ny))
    prev, q = {(0, 0): None}, deque([(0, 0)])
    while q:
        cx, cy = q.popleft()
        if (cx, cy) == (cols-1, rows-1): break
        for nx, ny, ok in [(cx+1, cy, cx+1 < cols and not right[cy][cx]), (cx-1, cy, cx > 0 and not right[cy][cx-1]),
                           (cx, cy+1, cy+1 < rows and not down[cy][cx]), (cx, cy-1, cy > 0 and not down[cy-1][cx])]:
            if ok and (nx, ny) not in prev:
                prev[(nx, ny)] = (cx, cy); q.append((nx, ny))
    path, cur = [], (cols-1, rows-1)
    while cur:
        path.append(cur); cur = prev[cur]
    return right, down, path[::-1]


def art_loop(x, ox, oy, aw, ah):
    c, u = x.c, x.uid
    cols, rows, cell = 17, 5, 25
    right, down, path = _maze(cols, rows, 11)
    mx, my = ox + (aw - cols * cell) / 2, oy + (ah - rows * cell) / 2
    walls = [f"M{mx} {my}H{mx+cols*cell}V{my+rows*cell}H{mx}Z"]
    for j in range(rows):
        for i in range(cols):
            if right[j][i] and i < cols - 1: walls.append(f"M{mx+(i+1)*cell} {my+j*cell}v{cell}")
            if down[j][i] and j < rows - 1: walls.append(f"M{mx+i*cell} {my+(j+1)*cell}h{cell}")
    d = "M" + " L".join(f"{mx+(i+.5)*cell:.1f} {my+(j+.5)*cell:.1f}" for i, j in path)
    x.css(f"@keyframes lp{u}{{from{{stroke-dashoffset:100}}to{{stroke-dashoffset:0}}}}.lp{u}{{animation:lp{u} 6.5s linear infinite}}")
    return (f'<path d="{" ".join(walls)}" fill="none" stroke="{c["steel"]}" stroke-opacity="0.6" stroke-width="1.2"/>'
            f'<path class="lp{u}" d="{d}" pathLength="100" fill="none" stroke="{c["gold2"]}" stroke-width="3" stroke-linejoin="round" stroke-dasharray="8 92"/>'
            f'<path class="lp{u}" d="{d}" pathLength="100" fill="none" stroke="{c["good"]}" stroke-width="3" stroke-linejoin="round" stroke-dasharray="5 95" style="animation-delay:.8s"/>'
            + sq(mx + cell / 2, my + cell / 2, 4, c["gold2"]) + sq(mx + (cols - .5) * cell, my + (rows - .5) * cell, 4, c["good"]))


def art_gesture(x, ox, oy, aw, ah):
    c, u = x.c, x.uid
    names = ["Camera", "MediaPipe", "MQTT", "Broker", "ESP32", "LED"]
    n = len(names)
    x0, x1, my = ox + 40, ox + aw - 40, oy + ah / 2
    xs = [x0 + (x1 - x0) * i / (n - 1) for i in range(n)]
    dur = 5.0
    x.css(f"@keyframes gn{u}{{0%{{fill-opacity:1}}12%{{fill-opacity:1}}50%,100%{{fill-opacity:0}}}}.gn{u}{{fill-opacity:0;animation:gn{u} {dur}s ease-out infinite}}"
          f"@keyframes led{u}{{0%,88%{{opacity:0;transform:scale(1)}}94%{{opacity:.9;transform:scale(1.8)}}100%{{opacity:0;transform:scale(1)}}}}"
          f".led{u}{{transform-box:fill-box;transform-origin:center;opacity:0;animation:led{u} {dur}s ease-out infinite}}")
    x.defs(f'<path id="gp{u}" d="M{x0} {my}H{x1}"/>')
    s = [f'<use xlink:href="#gp{u}" stroke="{c["gold"]}" stroke-opacity="0.5" stroke-width="1.2" fill="none"/>']
    for i, (px, nm) in enumerate(zip(xs, names)):
        dl = -(dur - dur * i / (n - 1)) if i else 0
        col = c["good"] if i == n - 1 else c["gold2"]
        s.append(f'<rect x="{px-6:.1f}" y="{my-6}" width="12" height="12" fill="{c["bg"]}" stroke="{c["good"] if i == n-1 else c["gold"]}" stroke-width="1.3" transform="rotate(45 {px:.1f} {my})"/>')
        s.append(f'<rect class="gn{u}" x="{px-6:.1f}" y="{my-6}" width="12" height="12" fill="{col}" transform="rotate(45 {px:.1f} {my})" style="animation-delay:{dl:.2f}s"/>')
        s.append(x.t(nm.upper(), px, my - 20 if i % 2 == 0 else my + 32, 10.5, c["text2"], "sansm", anchor="middle", ls=1.6))
    s.append(f'<circle class="led{u}" cx="{xs[-1]:.1f}" cy="{my}" r="15" fill="{c["good"]}"/>')
    s.append(f'<rect x="-3.5" y="-3.5" width="7" height="7" fill="{c["gold2"]}"><animateMotion dur="{dur}s" repeatCount="indefinite" calcMode="linear"><mpath xlink:href="#gp{u}"/></animateMotion></rect>')
    return "\n".join(s)


def art_vintage(x, ox, oy, aw, ah):
    c, u = x.c, x.uid
    pw, ph = 84, ah - 6
    px, py = ox + aw / 2 - 90, oy + 3
    x.defs(f'<clipPath id="ph{u}"><rect x="{px+5}" y="{py+10}" width="{pw-10}" height="{ph-20}"/></clipPath>'
           f'<linearGradient id="sh{u}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{c["gold2"]}" stop-opacity="0"/><stop offset="0.5" stop-color="{c["gold2"]}" stop-opacity="0.4"/><stop offset="1" stop-color="{c["gold2"]}" stop-opacity="0"/></linearGradient>')
    x.css(f"@keyframes shm{u}{{from{{transform:translateX(-60px)}}to{{transform:translateX(110px)}}}}.shm{u}{{animation:shm{u} 3.2s ease-in-out infinite}}"
          f"@keyframes sw{u}{{from{{transform:rotate(-7deg)}}to{{transform:rotate(7deg)}}}}.sw{u}{{transform-origin:{px+pw+70}px {py+8}px;animation:sw{u} 2.6s ease-in-out infinite alternate}}")
    phone = (f'<polygon points="{chamfer(px, py, pw, ph, 12)}" fill="{c["chip_fill"]}" stroke="{c["gold"]}" stroke-opacity="0.8"/>'
             f'<g clip-path="url(#ph{u})"><rect x="{px+12}" y="{py+20}" width="34" height="5" fill="{c["gold"]}" fill-opacity="0.6"/>'
             f'<rect x="{px+12}" y="{py+34}" width="{pw-24}" height="46" fill="{c["steel"]}" fill-opacity="0.2"/>'
             f'<rect x="{px+12}" y="{py+88}" width="{(pw-32)/2}" height="28" fill="{c["gold"]}" fill-opacity="0.22"/>'
             f'<rect x="{px+20+(pw-32)/2}" y="{py+88}" width="{(pw-32)/2}" height="28" fill="{c["gold"]}" fill-opacity="0.22"/>'
             f'<rect class="shm{u}" x="{px}" y="{py+10}" width="46" height="{ph-20}" fill="url(#sh{u})"/></g>')
    tx = px + pw + 70
    tag = (f'<g class="sw{u}"><line x1="{tx}" y1="{py+8}" x2="{tx}" y2="{py+34}" stroke="{c["gold"]}" stroke-opacity="0.8"/>'
           f'<polygon points="{chamfer(tx-30, py+34, 60, 74, 12)}" fill="{c["chip_fill"]}" stroke="{c["gold2"]}" stroke-opacity="0.9"/>'
           f'<circle cx="{tx}" cy="{py+50}" r="4" fill="none" stroke="{c["gold2"]}"/>'
           f'<path d="M{tx-16} {py+72}H{tx+16}M{tx-16} {py+84}H{tx+8}" stroke="{c["gold"]}" stroke-opacity="0.7"/></g>')
    return phone + tag


def art_kindness(x, ox, oy, aw, ah):
    c, u = x.c, x.uid
    x.css(f"@keyframes tk{u}{{0%,4%{{stroke-dashoffset:24}}16%,84%{{stroke-dashoffset:0}}96%,100%{{stroke-dashoffset:24}}}}"
          f".tk{u}{{stroke-dasharray:24;animation:tk{u} 9s ease-in-out infinite backwards}}"
          f"@keyframes rg{u}{{from{{stroke-dashoffset:100}}to{{stroke-dashoffset:22}}}}.rg{u}{{animation:rg{u} 9s ease-in-out infinite alternate}}")
    lx = ox + 70
    s = []
    for i, wbar in enumerate([128, 96, 150]):
        yy = oy + 20 + i * 40
        s.append(f'<rect x="{lx}" y="{yy}" width="26" height="26" fill="{c["chip_fill"]}" stroke="{c["gold"]}" stroke-opacity="0.85"/>')
        s.append(f'<path class="tk{u}" d="M{lx+6} {yy+13.5}l5.5 5.5l10-12" fill="none" stroke="{c["gold2"]}" stroke-width="2.6" stroke-linecap="square" style="animation-delay:{i*1.6:.1f}s"/>')
        s.append(f'<rect x="{lx+40}" y="{yy+8}" width="{wbar}" height="9" fill="{c["steel"]}" fill-opacity="0.35"/>')
    gx, gy, gr = ox + aw - 96, oy + ah / 2, 40
    s.append(f'<circle cx="{gx}" cy="{gy}" r="{gr}" fill="none" stroke="{c["steel"]}" stroke-opacity="0.3" stroke-width="5"/>')
    s.append(f'<circle class="rg{u}" cx="{gx}" cy="{gy}" r="{gr}" fill="none" stroke="{c["gold2"]}" stroke-width="5" pathLength="100" stroke-dasharray="100 100" transform="rotate(-90 {gx} {gy})"/>')
    s.append(sq(gx, gy, 4, c["good"]))
    return "\n".join(s)


CARDS = {
    "loop": dict(title="The Loop", tech=["Flutter", "Dart"], art=art_loop,
                 text="A procedurally generated horror maze. No two runs are alike."),
    "gesture": dict(title="Gesture control", tech=["Python", "OpenCV", "ESP32", "MQTT"], art=art_gesture,
                    text="Hand gestures, read by computer vision, control an ESP32."),
    "vintage": dict(title="Vintage Heaven", tech=["Kotlin", "Compose", "Figma"], art=art_vintage,
                    text="A vintage and handmade e-commerce prototype. Co-founder, design and Android."),
    "kindness": dict(title="Acts of Kindness", tech=["Kotlin", "Android"], art=art_kindness,
                     text="Daily kindness tasks, tracking and motivational stories."),
}


def _row(c, uid, keys, title):
    h = 350
    x = Ctx(c, uid, h, title=title)
    parts = []
    cw, gap = 488, 24
    for i, k in enumerate(keys):
        spec = CARDS[k]
        cx = i * (cw + gap)
        bg, edge, cid = card(x, cx, 0, cw, h, k)
        ah = 150
        art = spec["art"](x, cx + 24, 30, cw - 48, ah)
        p, y = paragraph(x, spec["text"], cx + 40, 274, cw - 80, 14.5, c["text2"], lh=22)
        parts.append(f'{bg}{art}<line x1="{cx+40}" y1="204" x2="{cx+cw-40}" y2="204" stroke="{c["gold"]}" stroke-opacity="0.25"/>'
                     + x.t(spec["title"], cx + 40, 240, 30, c["text"], "serif")
                     + p + tech_line(x, spec["tech"], cx + 40, y + 12) + edge)
    return x.render("\n".join(parts))


def row1_svg(c): return _row(c, "r1", ["loop", "gesture"], "The Loop and gesture control")
def row2_svg(c): return _row(c, "r2", ["vintage", "kindness"], "Vintage Heaven and Acts of Kindness")
