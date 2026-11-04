# -*- coding: utf-8 -*-
"""The three panels (identity, system, contact), drawn on an 840px canvas. Copy lives here."""
import math

from common import W, X0, X1, MONO, Doc, wrap

EMAIL = "javohirabduvahhobov@gmail.com"
SUMMARY = ("I ship the whole pipeline: Flutter on the client, a Node.js / Express API in the middle, "
           "PostgreSQL underneath, and an admin panel wired to all of it.")


# ═══════════════════════════ 001 · IDENTITY ═══════════════════════════
def header(c):
    H = 444
    d = Doc(c, H, "Javohir Abduvahhobov. Full-stack and mobile engineer. Flutter, Node.js, PostgreSQL, React, TypeScript. BSc Software Engineering, open to work.")
    hi, ink, mid, line = c["hi"], c["ink"], c["mid"], c["line"]
    b = d.topbar("JAVOHIR.IO", "開発者", "4A 41 56 4F 48 49 52") + d.rail("001", "01", "cross")

    b += d.tech("Javohir Abduvahhobov", X0, 98, 44, hi, max_w=X1 - X0)
    b += d.mono("FULL-STACK & MOBILE ENGINEER", X0, 124, 12, ink, tracking=2.6)
    b += d.ruler(X0, 138, X1 - X0)

    # left column: summary + readouts
    lw = 300
    for i, ln_ in enumerate(wrap(SUMMARY, MONO, 12, lw, .1)):
        b += d.mono(ln_, X0, 178 + i * 19, 12, ink, tracking=.1)
    for i, (k, v, live) in enumerate([("DEGREE", "BSC SOFTWARE ENG.", False), ("CORE", "FLUTTER / NODE.JS / PG", False),
                                       ("STATUS", "OPEN TO WORK", True), ("REPLY", "WITHIN A DAY", False)]):
        b += d.kv(X0, 284 + i * 24, lw, k, v, 12, live=live)
    b += d.ln(X0, 260.5, X0 + lw, 260.5, line, 1) + d.ln(X0, 368.5, X0 + lw, 368.5, line, 1)

    # right column: the stack map
    px, py, pw, ph = 404, 158, 400, 210
    cx, cy = px + pw / 2, py + ph / 2 + 2
    d.d(f'<linearGradient id="sg" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="{hi}" stop-opacity="0"/><stop offset="1" stop-color="{hi}" stop-opacity=".16"/></linearGradient>')
    d.d(f'<clipPath id="pc"><rect x="{px}" y="{py}" width="{pw}" height="{ph}"/></clipPath>')
    d.k(f"@keyframes scan{{from{{transform:translateY(-26px)}}to{{transform:translateY({ph}px)}}}} .scan{{animation:scan 7s linear infinite}}")
    b += d.grid(px, py, pw, ph, 20, .55) + d.rect(px, py, pw, ph, line, 1)
    b += d.ln(px, cy, px + 10, cy, hi, 1) + d.ln(px + pw - 10, cy, px + pw, cy, hi, 1) + d.ln(cx, py, cx, py + 10, hi, 1) + d.ln(cx, py + ph - 10, cx, py + ph, hi, 1)
    b += f'<circle cx="{cx}" cy="{cy}" r="88" fill="none" stroke="{ink}" stroke-opacity=".7" stroke-width="1"/>'
    b += (f'<g class="sr" style="transform-origin:{cx}px {cy}px"><circle cx="{cx}" cy="{cy}" r="99" fill="none" stroke="{mid}" stroke-width="1" '
          f'stroke-dasharray="2 5"/></g>')
    b += d.mesh(cx, cy, 70, "ring", 11, k=4)
    b += d.dot(cx, cy, 2.4)
    for ang, label, side in ((-150, "FLUTTER", -1), (-30, "NODE.JS", 1), (62, "POSTGRES", 1)):
        a = math.radians(ang)
        nx, ny = cx + 88 * math.cos(a), cy + 88 * math.sin(a)
        ex = nx + side * 30
        b += d.ln(nx, ny, ex, ny, hi, 1.1) + d.dot(nx, ny, 3.2, hi) + f'<circle cx="{nx:.1f}" cy="{ny:.1f}" r="6" fill="none" stroke="{hi}" stroke-opacity=".5"/>'
        b += d.mono(label, ex + side * 6, ny + 4, 11, hi, "end" if side < 0 else "start", 1.2)
    b += f'<g clip-path="url(#pc)"><g class="scan"><rect x="{px}" y="{py}" width="{pw}" height="26" fill="url(#sg)"/>{d.ln(px, py + 26, px + pw, py + 26, hi, .55)}</g></g>'
    b += d.brackets(px - 4, py - 4, pw + 8, ph + 8, 12, hi, 1.4)
    b += d.mono("STACK_MAP", px + 10, py + ph - 10, 9, mid, tracking=1) + d.mono("SCAN", px + pw - 22, py + 16, 9, mid, "end", 1) + d.dot(px + pw - 12, py + 13, 2.2, hi, "bl")

    # bottom strip
    b += d.barcode(X0, 388, lw, 20, 7)
    b += d.rect(404, 382, 400, 32, line, 1) + d.wave(405, 386, 398, 24, 5, 240, .55)
    b += d.mono("ONE ENGINEER / THE WHOLE PIPELINE", X0, 432, 10, mid, tracking=1)
    b += d.mono("WAVEFORM_DATA", 404, 432, 10, mid, tracking=1) + d.dotmatrix(X1 - 48, 424, 9, 2, 3, 5, 3)
    return d.render(b)


# ═══════════════════════════ 002 · SYSTEM ═══════════════════════════
COLS = [
    dict(name="CLIENT", tag="A", kind="blob", seed=21, cap="UI_LAYER",
         rows=[("FLUTTER", "FRAMEWORK"), ("DART", "LANGUAGE"), ("REACT", "UI LIBRARY"), ("TYPESCRIPT", "LANGUAGE"), ("HTML/CSS/JS", "ADMIN PANEL")],
         mods=["http", "shared_preferences", "file_picker", "google_fonts", "intl", "cupertino_icons"]),
    dict(name="SERVER", tag="B", kind="ring", seed=8, cap="API_LAYER",
         rows=[("NODE.JS", "RUNTIME"), ("EXPRESS", "REST API"), ("PYTHON", "LANGUAGE"), ("JWT", "AUTH"), ("PG", "DB DRIVER")],
         mods=["bcryptjs", "multer", "cors", "morgan", "dotenv", "uuid"]),
    dict(name="DATA / OPS", tag="C", kind="rose", seed=4, cap="DATA_LAYER",
         rows=[("POSTGRESQL", "DATABASE"), ("DOCKER", "CONTAINERS"), ("GIT", "VERSIONING"), ("GITHUB", "HOSTING"), ("NPM", "PACKAGES")],
         mods=None),
]


def system(c):
    H = 622
    d = Doc(c, H, "System. Client: Flutter, Dart, React, TypeScript. Server: Node.js, Express, Python, JWT. Data and ops: PostgreSQL, Docker, Git, GitHub, npm.")
    hi, ink, mid, line = c["hi"], c["ink"], c["mid"], c["line"]
    b = d.topbar("SYSTEM.MAP", "システム", "STACK / FLOW") + d.rail("002", "02", "x")

    cw, gap = 232, 12
    for i, col in enumerate(COLS):
        x = X0 + i * (cw + gap)
        b += d.mono(col["name"], x, 62, 11, hi, tracking=1.6) + d.mono(f"0{i + 1}/03", x + cw, 62, 11, mid, "end", 1)
        b += d.ln(x, 70.5, x + cw, 70.5, hi, .9)
        for r, (k, v) in enumerate(col["rows"]):
            b += d.kv(x, 92 + r * 20, cw, k, v, 12, hi=True)
        # plot
        py, ph = 190, 122
        b += d.grid(x, py, cw, ph, 20, .5) + d.rect(x, py, cw, ph, line, 1) + d.brackets(x - 3, py - 3, cw + 6, ph + 6, 8, hi, 1.2)
        b += d.mesh(x + cw / 2, py + ph / 2, 50, col["kind"], col["seed"], k=3)
        b += d.mono(col["cap"], x + 8, py + ph - 8, 9, mid, tracking=1)
        b += d.mono(f"{col['tag']}", x + cw - 10, py + 16, 9, hi, "end", 1)
        # modules
        b += d.mono("MODULES" if col["mods"] else "WAVEFORM_DATA", x, 334, 11, mid, tracking=1.6)
        if col["mods"]:
            for m, name in enumerate(col["mods"]):
                b += d.rect(x, 346 + m * 16 + 2, 5, 5, mid, 1) + d.mono(name, x + 14, 354 + m * 16, 11, ink, tracking=.3)
        else:
            b += d.rect(x, 342, cw, 100, line, 1)
            b += d.wave(x + 1, 350, cw - 2, 34, 9, 232, .55) + d.bars(x + 8, 392, cw - 16, 36, 12, 30)
            b += d.ln(x, 388.5, x + cw, 388.5, line, 1)

    # architecture strip
    sy, sh = 462, 140
    b += d.rect(X0, sy, X1 - X0, sh, line, 1) + d.brackets(X0 - 3, sy - 3, X1 - X0 + 6, sh + 6, 10, hi, 1.4)
    b += d.mono("FLOW", X0 + 12, sy + 20, 10, mid, tracking=1.6)
    ny, r = sy + 76, 24
    fx, ax, dx, mx = 170, 450, 710, 450

    # docker boundary
    dkx0, dky0, dkx1, dky1 = 340, sy + 14, 786, sy + sh - 12
    b += d.rect(dkx0, dky0, dkx1 - dkx0, dky1 - dky0, mid, .9, 1, 10, dash="3 5")
    lw_ = MONO.width("DOCKER", 10, 1.6) + 16
    b += f'<rect x="{dkx0 + 16}" y="{dky0 - 7}" width="{lw_:.0f}" height="14" fill="{c["bg"]}"/>' + d.mono("DOCKER", dkx0 + 24, dky0 + 3.5, 10, hi, tracking=1.6)

    def node(cx, cy, rr, label, glyph):
        return d.dial(cx, cy, rr, "ring") + glyph + d.mono(label, cx, cy + rr + 22, 11, hi, "middle", 1.2)

    # glyphs inside the dials
    phone = d.rect(fx - 5, ny - 8, 10, 16, hi, 1, 1.3, 2, fill=c["bg"])
    api = d.mono("{ }", ax, ny + 4, 12, hi, "middle", 0)
    cyl = (f'<path d="M{dx - 8} {ny - 6}v12M{dx + 8} {ny - 6}v12" stroke="{hi}" stroke-width="1.3" fill="none"/>'
           f'<ellipse cx="{dx}" cy="{ny - 6}" rx="8" ry="3" fill="{c["bg"]}" stroke="{hi}" stroke-width="1.3"/>'
           f'<path d="M{dx - 8} {ny + 6}a8 3 0 0 0 16 0" stroke="{hi}" stroke-width="1.3" fill="none"/>')
    b += node(fx, ny, r, "FLUTTER APP", phone) + node(ax, ny, r, "EXPRESS API", api) + node(dx, ny, r, "POSTGRESQL", cyl)

    # admin panel satellite
    ay = sy + 36
    b += d.rect(mx - 9, ay - 6, 18, 12, hi, 1, 1.2, 1, fill=c["bg"]) + d.ln(mx - 4, ay + 9, mx + 4, ay + 9, hi, 1, 1.2)
    b += d.mono("ADMIN PANEL", mx + 20, ay + 4, 11, ink, tracking=1)
    b += d.ln(mx, ay + 10, mx, ny - r - 6, line, 1) + d.ln(mx, ay + 14, mx, ny - r - 8, hi, 1.2, 1.2, "3 5").replace('fill="none"', 'fill="none" class="fl"')

    # moving flow lines
    for (x1_, x2_, lab, lx) in ((fx + r + 8, ax - r - 8, "REST + JWT", fx + 110), (ax + r + 8, dx - r - 8, "pg driver", (ax + dx) / 2)):
        b += d.ln(x1_, ny, x2_, ny, line, 1) + d.ln(x1_, ny, x2_, ny, hi, 1.3, 1.3, "3 5").replace('fill="none"', 'fill="none" class="fl"')
        b += d.mono(lab, lx, ny - 10, 10, mid, "middle", 1)
    return d.render(b)


# ═══════════════════════════ 003 · CONTACT ═══════════════════════════
def contact(c):
    H = 200
    d = Doc(c, H, f"Contact: {EMAIL}. Open to work, usually replies within a day.")
    hi, ink, mid, line = c["hi"], c["ink"], c["mid"], c["line"]
    b = d.topbar("OPEN.CHANNEL", "連絡", "SEND / RECEIVE") + d.rail("003", "03", "ring")

    bx, by, bw, bh = X0, 60, X1 - X0, 72
    b += d.rect(bx, by, bw, bh, line, 1) + d.brackets(bx - 3, by - 3, bw + 6, bh + 6, 12, hi, 1.5)
    b += d.tech(EMAIL, bx + 24, by + 46, 30, hi, max_w=bw - 120)
    cx, cy = bx + bw - 40, by + bh / 2
    b += (f'<circle cx="{cx}" cy="{cy}" r="19" fill="none" stroke="{hi}" stroke-width="1.3"/><g class="nd"><path d="M{cx - 7} {cy + 7}L{cx + 7} {cy - 7}'
          f'M{cx - 6} {cy - 7}H{cx + 7}V{cy + 6}" fill="none" stroke="{hi}" stroke-width="1.6"/></g>')
    b += d.dot(X0 + 5, 160, 3, hi, "bl") + d.mono("AVAILABLE FOR OPPORTUNITIES", X0 + 18, 164, 12, hi, tracking=1.2)
    b += d.mono("REPLIES WITHIN A DAY", X1, 164, 12, mid, "end", 1.2)
    b += d.barcode(X0, 176, X1 - X0, 10, 31, .8)
    return d.render(b)
