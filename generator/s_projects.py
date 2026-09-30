# -*- coding: utf-8 -*-
import random
from collections import deque

import typo
from kit import (Ctx, frame, border, dust, sparkles, diamond, star4, fade_line, hair, chip, flow_dot,
                 link_path, paragraph, bullets, card, W)


def gold_text(c):
    return c["gold2"] if c["is_dark"] else c["gold"]


def chip_row(x, x0, y, labels, max_x, primary=(), h=28, size=12.5):
    """Flow chips left→right, wrapping at max_x. Returns (svg, y_after)."""
    out, cx = [], x0
    for lab in labels:
        w = x.w_(lab, "sansm", size, 0.2) + 30 + (15 if lab in primary else 0)
        if cx + w > max_x:
            cx, y = x0, y + h + 8
        s, w = chip(x, cx, y, lab, primary=lab in primary, h=h, size=size)
        out.append(s)
        cx += w + 8
    return "\n".join(out), y + h


def abox(x, bx, by, bw, bh, title, sub, hot=False):
    c = x.c
    return (f'<rect x="{bx}" y="{by}" width="{bw}" height="{bh}" rx="8" fill="{c["chip_fill"]}" stroke="{c["gold"]}" '
            f'stroke-opacity="{0.75 if hot else 0.42}" stroke-width="{1.3 if hot else 1}"/>'
            + x.t(title, bx + bw / 2, by + bh / 2 - 2, 15, c["text"], "sansm", anchor="middle", ls=0.2)
            + x.t(sub, bx + bw / 2, by + bh / 2 + 17, 12.5, c["text3"], "sans", anchor="middle"))


def title_fit(x, text, max_w, size=54, min_size=30):
    while size > min_size and x.w_(text, "serif", size) > max_w:
        size -= 2
    return size


# ===========================================================================
def oson_svg(c):
    h = 520
    x = Ctx(c, "os", h, title="OsonIjara: full-stack rental-listing platform",
            desc="Flutter app on Netlify talks to a FastAPI backend on Render over REST and WebSockets; PostgreSQL on Neon and optional Cloudflare R2 storage.")
    u = x.uid
    lx, cw = 64, 450
    parts = []
    size = title_fit(x, "OsonIjara", cw)
    parts.append(x.t("OsonIjara", lx, 112, size, c["text"], "serif"))
    parts.append(x.t("Rental-listing platform, full stack", lx, 146, 19, gold_text(c), "serifi"))
    p, y = paragraph(x, "People browse, search, filter, save and publish properties, then message each other in real time. "
                        "Admins moderate listings. Flutter on the front, FastAPI behind it, PostgreSQL underneath.",
                     lx, 190, cw, 15.5, c["text2"], lh=25)
    parts.append(p)
    feats = ["JWT authentication", "Property CRUD with ownership checks", "Advanced filtering and search", "Image uploads",
             "Bookmarks and user profiles", "WebSocket chat with unread tracking", "Admin moderation",
             "Pytest suite and GitHub Actions CI"]
    b, y = bullets(x, feats, lx, y + 22, 214, cols=2, size=14, lh=27)
    parts.append(b)

    # right: architecture
    px0, px1, py0, py1 = 562, W - 64, 60, 424
    parts.append(f'<rect x="{px0}" y="{py0}" width="{px1-px0}" height="{py1-py0}" rx="8" fill="{c["chip_fill"]}" fill-opacity="0.35" '
                 f'stroke="{c["gold"]}" stroke-opacity="0.16"/>')
    cx = (px0 + px1) / 2
    bw = 196
    boxes = [abox(x, cx - bw / 2, 84, bw, 62, "Flutter app", "Netlify"),
             abox(x, cx - bw / 2, 206, bw, 62, "FastAPI", "Render", hot=True),
             abox(x, px0 + 26, 328, 148, 62, "PostgreSQL", "Neon, SQLAlchemy"),
             abox(x, px1 - 26 - 148, 328, 148, 62, "Cloudflare R2", "Optional storage")]
    rest_x, ws_x = cx - 22, cx + 22
    links = [
        link_path(x, f"rest{u}", f"M{rest_x} 146 V206"),
        link_path(x, f"ws{u}", f"M{ws_x} 206 V146", color=c["rose"], op=0.7),
        link_path(x, f"db{u}", f"M{cx-30} 268 C{cx-30} 300 {px0+100} 300 {px0+100} 328"),
        link_path(x, f"r2{u}", f"M{cx+30} 268 C{cx+30} 300 {px1-100} 300 {px1-100} 328", op=0.35),
    ]
    dots = (flow_dot(x, f"rest{u}", 2.2, 0) + flow_dot(x, f"rest{u}", 2.2, 1.1)
            + flow_dot(x, f"ws{u}", 1.7, 0.4, color=c["rose"]) + flow_dot(x, f"ws{u}", 1.7, 1.3, color=c["rose"])
            + flow_dot(x, f"db{u}", 2.6, 0.6) + flow_dot(x, f"db{u}", 2.6, 1.9))
    labels = (x.t("REST and JWT", rest_x - 12, 181, 12.5, c["text3"], "sans", anchor="end")
              + x.t("WebSocket", ws_x + 12, 181, 12.5, c["rose"], "sansm", ls=0.2)
)
    parts += [*links, dots, *boxes, labels]
    parts.append(x.t("Local development runs in Docker Compose.", cx, 412, 12.5, c["text3"], "sans", anchor="middle"))

    chips_y = max(y, py1) + 26
    chips, chips_end = chip_row(x, lx, chips_y, ["Flutter", "Dart", "FastAPI", "Python", "PostgreSQL", "SQLAlchemy", "JWT", "WebSockets", "Docker"],
                                W - 64, primary=("Flutter", "FastAPI", "PostgreSQL"))
    parts.append(chips)
    x.h = int(chips_end + 52)

    body = "\n".join([frame(x, r=6), f'<g clip-path="url(#clip{u})">{dust(x, 9, seed=41, rise=70, sizes=(0.6, 1.4))}</g>',
                      *parts, sparkles(x, [(530, 90), (940, 470)], seed=2), border(x, r=6)])
    return x.render(body)


# ===========================================================================
def career_svg(c):
    x = Ctx(c, "cp", 470, title="Career Services Portal: full-stack internship and career platform",
            desc="Flutter student app and an HTML admin panel both call an Express API backed by PostgreSQL.")
    u = x.uid
    rx, cw = 520, 416
    parts = []
    size = title_fit(x, "Career Services Portal", cw, size=44)
    parts.append(x.t("Career Services Portal", rx, 112, size, c["text"], "serif"))
    parts.append(x.t("Internships and applications, end to end", rx, 146, 19, gold_text(c), "serifi"))
    p, y = paragraph(x, "Students find internships, apply with a PDF or Word resume and book interviews from an interactive calendar. "
                        "A separate admin web panel manages jobs, applications and interviews.",
                     rx, 190, cw, 15.5, c["text2"], lh=25)
    parts.append(p)
    feats = ["Student sign-up", "Internship search", "Job bookmarks", "Resume upload",
             "Interview scheduling", "Interactive calendar", "Profile photos", "Admin job CRUD",
             "Application management", "Interview management"]
    b, y = bullets(x, feats, rx, y + 22, 200, cols=2, size=13.5, lh=26, gap=16)
    parts.append(b)
    chips_y = y + 22
    chips, chips_end = chip_row(x, rx, chips_y, ["Flutter", "Dart", "Node.js", "Express", "PostgreSQL", "JWT", "Multer"], W - 64,
                                primary=("Flutter", "Node.js", "PostgreSQL"))
    parts.append(chips)
    h = int(chips_end + 52)
    x.h = h

    # left: architecture, vertically centred on the panel
    px0, px1, py0, py1 = 64, 484, 60, h - 60
    parts.append(f'<rect x="{px0}" y="{py0}" width="{px1-px0}" height="{py1-py0}" rx="8" fill="{c["chip_fill"]}" fill-opacity="0.35" '
                 f'stroke="{c["gold"]}" stroke-opacity="0.16"/>')
    cy = (py0 + py1) / 2 - 10
    ax = px1 - 24 - 150
    boxes = [abox(x, px0 + 24, cy - 126, 170, 62, "Flutter app", "Students"),
             abox(x, px0 + 24, cy + 64, 170, 62, "Admin panel", "HTML, CSS, JavaScript"),
             abox(x, ax, cy - 31, 150, 62, "Express API", "JWT, Multer", hot=True),
             abox(x, ax, cy + 92, 150, 56, "PostgreSQL", "Jobs and interviews")]
    links = [
        link_path(x, f"a{u}", f"M{px0+194} {cy-95} C{ax-30} {cy-95} {ax-40} {cy} {ax} {cy}"),
        link_path(x, f"b{u}", f"M{px0+194} {cy+95} C{ax-30} {cy+95} {ax-40} {cy} {ax} {cy}"),
        link_path(x, f"d{u}", f"M{ax+75} {cy+31} V{cy+92}"),
    ]
    dots = (flow_dot(x, f"a{u}", 2.4, 0) + flow_dot(x, f"a{u}", 2.4, 1.2)
            + flow_dot(x, f"b{u}", 2.4, 0.5) + flow_dot(x, f"b{u}", 2.4, 1.7)
            + flow_dot(x, f"d{u}", 1.4, 0.2))
    parts += [*links, dots, *boxes]
    parts.append(x.t("One REST API serves both clients.", (px0 + px1) / 2, py1 - 20, 12.5, c["text3"], "sans", anchor="middle"))

    body = "\n".join([frame(x, r=6), f'<g clip-path="url(#clip{u})">{dust(x, 9, seed=43, rise=70, sizes=(0.6, 1.4))}</g>',
                      *parts, sparkles(x, [(500, 84), (60, h - 30)], seed=4), border(x, r=6)])
    return x.render(body)


# ===========================================================================
# small cards
# ===========================================================================
def _maze(cols, rows, seed):
    rnd = random.Random(seed)
    right = [[True] * cols for _ in range(rows)]     # wall on right side of cell?
    down = [[True] * cols for _ in range(rows)]      # wall below cell?
    seen = [[False] * cols for _ in range(rows)]
    stack = [(0, 0)]
    seen[0][0] = True
    while stack:
        cx, cy = stack[-1]
        nb = [(nx, ny, d) for nx, ny, d in [(cx + 1, cy, "r"), (cx - 1, cy, "l"), (cx, cy + 1, "d"), (cx, cy - 1, "u")]
              if 0 <= nx < cols and 0 <= ny < rows and not seen[ny][nx]]
        if not nb:
            stack.pop()
            continue
        nx, ny, d = rnd.choice(nb)
        if d == "r": right[cy][cx] = False
        if d == "l": right[ny][nx] = False
        if d == "d": down[cy][cx] = False
        if d == "u": down[ny][nx] = False
        seen[ny][nx] = True
        stack.append((nx, ny))
    # BFS solution start→end
    prev, q = {(0, 0): None}, deque([(0, 0)])
    while q:
        cx, cy = q.popleft()
        if (cx, cy) == (cols - 1, rows - 1):
            break
        for nx, ny, ok in [(cx + 1, cy, cx + 1 < cols and not right[cy][cx]), (cx - 1, cy, cx > 0 and not right[cy][cx - 1]),
                           (cx, cy + 1, cy + 1 < rows and not down[cy][cx]), (cx, cy - 1, cy > 0 and not down[cy - 1][cx])]:
            if ok and (nx, ny) not in prev:
                prev[(nx, ny)] = (cx, cy)
                q.append((nx, ny))
    path, cur = [], (cols - 1, rows - 1)
    while cur:
        path.append(cur)
        cur = prev[cur]
    return right, down, path[::-1]


def art_loop(x, ox, oy, aw, ah):
    c, u = x.c, x.uid
    cols, rows, cell = 17, 5, 25
    right, down, path = _maze(cols, rows, seed=11)
    mx, my = ox + (aw - cols * cell) / 2, oy + (ah - rows * cell) / 2
    walls = [f"M{mx} {my} H{mx+cols*cell} V{my+rows*cell} H{mx} Z"]
    for j in range(rows):
        for i in range(cols):
            if right[j][i] and i < cols - 1:
                walls.append(f"M{mx+(i+1)*cell} {my+j*cell} v{cell}")
            if down[j][i] and j < rows - 1:
                walls.append(f"M{mx+i*cell} {my+(j+1)*cell} h{cell}")
    d = "M" + " L".join(f"{mx+(i+.5)*cell:.1f} {my+(j+.5)*cell:.1f}" for i, j in path)
    x.css(f"@keyframes lp{u}{{from{{stroke-dashoffset:100}}to{{stroke-dashoffset:0}}}}"
          f".lp{u}{{animation:lp{u} 6.5s linear infinite}}")
    return (f'<path d="{" ".join(walls)}" fill="none" stroke="{c["gold"]}" stroke-opacity="0.55" stroke-width="1.3" stroke-linecap="square"/>'
            f'<path d="{d}" fill="none" stroke="{c["gold"]}" stroke-opacity="0.16" stroke-width="2" stroke-linejoin="round"/>'
            f'<path class="lp{u}" d="{d}" pathLength="100" fill="none" stroke="{c["gold2"]}" stroke-width="3" stroke-linecap="round" '
            f'stroke-linejoin="round" stroke-dasharray="7 93"/>'
            f'<path class="lp{u}" d="{d}" pathLength="100" fill="none" stroke="{c["rose"]}" stroke-width="3" stroke-linecap="round" '
            f'stroke-linejoin="round" stroke-dasharray="5 95" style="animation-delay:0.75s"/>'
            + diamond(mx + cell / 2, my + cell / 2, 4, c["gold2"]) + diamond(mx + (cols - .5) * cell, my + (rows - .5) * cell, 4, c["rose"]))


def art_gesture(x, ox, oy, aw, ah):
    c, u = x.c, x.uid
    names = ["Camera", "OpenCV and MediaPipe", "MQTT", "Cloud broker", "ESP32", "LED"]
    n = len(names)
    x0, x1, my = ox + 44, ox + aw - 44, oy + ah / 2 + 2
    xs = [x0 + (x1 - x0) * i / (n - 1) for i in range(n)]
    dur = 5.0
    x.css(f"@keyframes gn{u}{{0%{{fill-opacity:1;transform:scale(1.6)}}10%{{fill-opacity:.9;transform:scale(1)}}50%,100%{{fill-opacity:0}}}}"
          f".gn{u}{{transform-box:fill-box;transform-origin:center;fill-opacity:0;animation:gn{u} {dur}s ease-out infinite}}"
          f"@keyframes led{u}{{0%,90%{{opacity:0;transform:scale(1)}}95%{{opacity:1;transform:scale(1.9)}}100%{{opacity:0;transform:scale(1)}}}}"
          f".led{u}{{transform-box:fill-box;transform-origin:center;opacity:0;animation:led{u} {dur}s ease-out infinite}}")
    x.defs(f'<path id="gp{u}" d="M{x0} {my} H{x1}"/>')
    s = [f'<use xlink:href="#gp{u}" stroke="{c["gold"]}" stroke-opacity="0.35" stroke-width="1.2" fill="none"/>',
         f'<use xlink:href="#gp{u}" stroke="{c["gold"]}" stroke-opacity="0.6" stroke-width="1.2" stroke-dasharray="2 6" stroke-linecap="round" fill="none"/>']
    for i, (px, nm) in enumerate(zip(xs, names)):
        dl = -(dur - dur * i / (n - 1)) if i else 0
        last = i == n - 1
        s.append(f'<circle cx="{px:.1f}" cy="{my}" r="7" fill="{c["bg"]}" stroke="{c["rose"] if last else c["gold"]}" stroke-width="1.2"/>')
        s.append(f'<circle class="gn{u}" cx="{px:.1f}" cy="{my}" r="7" fill="{c["rose"] if last else c["gold2"]}" style="animation-delay:{dl:.2f}s"/>')
        above = i % 2 == 0
        s.append(x.t(nm, px, my - 20 if above else my + 32, 12.5, c["text2"], "sansm", anchor="middle", ls=0.1))
    s.append(f'<circle cx="{xs[-1]:.1f}" cy="{my}" r="16" fill="{c["rose"]}" opacity="0" class="led{u}"/>')
    s.append(f'<circle r="3.6" fill="{c["gold2"]}"><animateMotion dur="{dur}s" repeatCount="indefinite" calcMode="linear"><mpath xlink:href="#gp{u}"/></animateMotion></circle>'
             f'<circle r="11" fill="{c["gold2"]}" opacity="0.16"><animateMotion dur="{dur}s" repeatCount="indefinite" calcMode="linear"><mpath xlink:href="#gp{u}"/></animateMotion></circle>')
    return "\n".join(s)


def art_vintage(x, ox, oy, aw, ah):
    c, u = x.c, x.uid
    px, py, pw, ph = ox + 92, oy + 8, 84, ah - 16
    x.defs(f'<clipPath id="ph{u}"><rect x="{px+5}" y="{py+9}" width="{pw-10}" height="{ph-18}" rx="8"/></clipPath>'
           f'<linearGradient id="sh{u}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="{c["gold2"]}" stop-opacity="0"/>'
           f'<stop offset="0.5" stop-color="{c["gold2"]}" stop-opacity="0.45"/><stop offset="1" stop-color="{c["gold2"]}" stop-opacity="0"/></linearGradient>')
    x.css(f"@keyframes shm{u}{{from{{transform:translateX(-70px)}}to{{transform:translateX(120px)}}}}.shm{u}{{animation:shm{u} 3.2s ease-in-out infinite}}"
          f"@keyframes swy{u}{{from{{transform:rotate(-5deg)}}to{{transform:rotate(5deg)}}}}"
          f".swy{u}{{transform-origin:{ox+aw-140}px {oy+34}px;animation:swy{u} 3.4s ease-in-out infinite alternate}}"
          f"@keyframes swt{u}{{from{{transform:rotate(9deg)}}to{{transform:rotate(-9deg)}}}}"
          f".swt{u}{{transform-origin:{ox+aw-96}px {oy+73}px;animation:swt{u} 2.2s ease-in-out infinite alternate}}")
    ink, dim = c["gold"], c["gold"]
    phone = (f'<rect x="{px}" y="{py}" width="{pw}" height="{ph}" rx="14" fill="{c["chip_fill"]}" stroke="{ink}" stroke-opacity="0.7"/>'
             f'<g clip-path="url(#ph{u})">'
             f'<rect x="{px+12}" y="{py+18}" width="34" height="6" rx="3" fill="{ink}" fill-opacity="0.55"/>'
             f'<rect x="{px+12}" y="{py+32}" width="{pw-24}" height="50" rx="6" fill="{c["rose"]}" fill-opacity="0.22"/>'
             f'<rect x="{px+12}" y="{py+90}" width="{(pw-32)/2}" height="30" rx="5" fill="{ink}" fill-opacity="0.2"/>'
             f'<rect x="{px+20+(pw-32)/2}" y="{py+90}" width="{(pw-32)/2}" height="30" rx="5" fill="{ink}" fill-opacity="0.2"/>'
             f'<rect class="shm{u}" x="{px}" y="{py+9}" width="50" height="{ph-18}" fill="url(#sh{u})"/></g>'
             f'<rect x="{px+pw/2-9}" y="{py+4}" width="18" height="3" rx="1.5" fill="{ink}" fill-opacity="0.5"/>')
    hx, hy = ox + aw - 140, oy + 34
    hanger = (f'<g class="swy{u}"><path d="M{hx} {hy} v-9 a7 7 0 1 1 7 -7" fill="none" stroke="{c["gold2"]}" stroke-width="1.6" stroke-linecap="round"/>'
              f'<path d="M{hx} {hy} L{hx-58} {hy+34} Q{hx-64} {hy+39} {hx-56} {hy+39} H{hx+56} Q{hx+64} {hy+39} {hx+58} {hy+34} Z" '
              f'fill="{c["rose"]}" fill-opacity="0.12" stroke="{c["gold2"]}" stroke-width="1.6" stroke-linejoin="round"/></g>'
              f'<g class="swt{u}"><line x1="{hx+44}" y1="{hy+39}" x2="{hx+44}" y2="{hy+62}" stroke="{c["gold"]}" stroke-opacity="0.7"/>'
              f'<rect x="{hx+34}" y="{hy+62}" width="20" height="28" rx="3" fill="{c["chip_fill"]}" stroke="{c["gold2"]}" stroke-opacity="0.9"/>'
              f'<circle cx="{hx+44}" cy="{hy+69}" r="2.4" fill="none" stroke="{c["gold2"]}"/>'
              f'<line x1="{hx+39}" y1="{hy+79}" x2="{hx+49}" y2="{hy+79}" stroke="{c["gold"]}" stroke-opacity="0.6"/></g>')
    # the hanger is drawn with its centre nudged over the base line for symmetry
    return phone + hanger


def art_kindness(x, ox, oy, aw, ah):
    c, u = x.c, x.uid
    x.css(f"@keyframes tk{u}{{0%,4%{{stroke-dashoffset:24}}16%,84%{{stroke-dashoffset:0}}96%,100%{{stroke-dashoffset:24}}}}"
          f".tk{u}{{stroke-dasharray:24;animation:tk{u} 9s ease-in-out infinite backwards}}"
          f"@keyframes hb{u}{{0%,100%{{transform:scale(1)}}14%{{transform:scale(1.16)}}28%{{transform:scale(1)}}42%{{transform:scale(1.1)}}}}"
          f".hb{u}{{transform-box:fill-box;transform-origin:center;animation:hb{u} 2.4s ease-in-out infinite}}")
    rows = [(0, 128), (1, 96), (2, 150)]
    lx = ox + 64
    s = []
    for i, wbar in rows:
        yy = oy + 22 + i * 40
        s.append(f'<rect x="{lx}" y="{yy}" width="26" height="26" rx="7" fill="{c["chip_fill"]}" stroke="{c["gold"]}" stroke-opacity="0.75"/>')
        s.append(f'<path class="tk{u}" d="M{lx+6} {yy+13.5} l5.5 5.5 l10 -12" fill="none" stroke="{c["gold2"]}" stroke-width="2.6" '
                 f'stroke-linecap="round" stroke-linejoin="round" style="animation-delay:{i*1.6:.1f}s"/>')
        s.append(f'<rect x="{lx+40}" y="{yy+8}" width="{wbar}" height="9" rx="4.5" fill="{c["gold"]}" fill-opacity="0.28"/>')
    hx, hy = ox + aw - 112, oy + ah / 2
    heart = f"M{hx} {hy+22} C{hx-46} {hy-8} {hx-24} {hy-40} {hx} {hy-16} C{hx+24} {hy-40} {hx+46} {hy-8} {hx} {hy+22} Z"
    s.append(f'<path class="hb{u}" d="{heart}" fill="{c["rose"]}" fill-opacity="0.2" stroke="{c["rose"]}" stroke-width="1.6" stroke-linejoin="round"/>')
    s.append(sparkles(x, [(hx + 46, hy - 34), (hx - 52, hy - 26), (hx + 40, hy + 26)], seed=6, size=(4, 7)))
    return "\n".join(s)


CARDS = {
    "loop": dict(title="The Loop", tech="Flutter, Dart", art=art_loop,
                 text="A procedurally generated horror maze survival game built around exploration, atmosphere and replayability. "
                      "The maze is generated dynamically instead of relying on one fixed level, so every playthrough is different."),
    "gesture": dict(title="AI gesture control", tech="Python, OpenCV, MediaPipe, ESP32, MQTT, Docker", art=art_gesture,
                    text="Computer vision recognizes hand gestures and controls an ESP32 remotely. Commands travel over MQTT "
                         "through a broker running in Docker on a Google Cloud VM."),
    "vintage": dict(title="Vintage Heaven", tech="Kotlin, Jetpack Compose, Figma", art=art_vintage,
                    text="A vintage and handmade e-commerce Android prototype. I co-founded it and covered project management, "
                         "UI/UX design, Figma prototyping and the Android build, planned with Trello and Gantt charts."),
    "kindness": dict(title="Random Acts of Kindness", tech="Kotlin, XML, Android", art=art_kindness,
                     text="A lightweight Android app with daily kindness tasks, task tracking, motivational stories and "
                          "several screens, with local functionality."),
}


def _row(c, uid, keys, title):
    h = 400
    x = Ctx(c, uid, h, title=title)
    parts = []
    cw, gap = 488, 24
    for i, k in enumerate(keys):
        spec = CARDS[k]
        cx = i * (cw + gap)
        bg, edge, cid = card(x, cx, 0, cw, h, k)
        ah = 150
        art = spec["art"](x, cx + 24, 26, cw - 48, ah)
        inner = [x.t(spec["title"], cx + 36, 236, title_fit(x, spec["title"], cw - 72, size=32, min_size=24), c["text"], "serif")]
        tech_lines = typo.wrap(spec["tech"], "sansm", 12.5, cw - 72, 0.3)
        ty = 264
        for ln in tech_lines:
            inner.append(x.t(ln, cx + 36, ty, 12.5, gold_text(c), "sansm", ls=0.3))
            ty += 19
        p, _ = paragraph(x, spec["text"], cx + 36, ty + 14, cw - 72, 14, c["text2"], lh=22)
        inner.append(p)
        parts.append(f'{bg}<g clip-path="url(#{cid})">{dust(x, 5, seed=60+i, x0=cx, x1=cx+cw, y1=200, rise=50)}</g>'
                     f'<line x1="{cx+36}" y1="{26+ah+6}" x2="{cx+cw-36}" y2="{26+ah+6}" stroke="{c["gold"]}" stroke-opacity="0.2"/>'
                     f'{art}{"".join(inner)}{edge}')
    return x.render("\n".join(parts))


def row1_svg(c):
    return _row(c, "r1", ["loop", "gesture"], "The Loop and AI gesture control")


def row2_svg(c):
    return _row(c, "r2", ["vintage", "kindness"], "Vintage Heaven and Random Acts of Kindness")
