# -*- coding: utf-8 -*-
"""The four panels. Each builder takes a palette `c` and returns an SVG string."""
from common import W, M, SANS, TECH, MONO, Doc

EMAIL = "javohirabduvahhobov@gmail.com"
SUMMARY = ("Full-stack and mobile engineer who ships the entire pipeline — Flutter on the client, a Node.js / Express "
           "REST API in the middle, PostgreSQL underneath, and a lightweight admin panel wired to it all.")


# ═══════════════════════════ MASTHEAD ═══════════════════════════
def hero(c):
    H = 424
    d = Doc(c, H, "Javohir Abduvahhobov — Full-stack & mobile engineer")
    b = d.card()
    acc, mid, ink, hi = c["acc"], c["mid"], c["ink"], c["hi"]

    items = [("ROLE", "FULL-STACK & MOBILE"), ("DEGREE", "BSC SOFTWARE ENG."), ("STATUS", "OPEN TO OPPORTUNITIES")]
    ws = [MONO.width(f"{k} : {v}", 8.5, 1.4) for k, v in items]
    gap = (W - 2 * M - sum(ws)) / (len(items) - 1)
    x = M
    for (k, v), w in zip(items, ws):
        b += d.mono(f"{k} :", x, 44, 8.5, acc) + d.mono(v, x + MONO.width(f"{k} : ", 8.5, 1.4) + 4, 44, 8.5, mid)
        x += w + gap

    b += d.text("Javohir Abduvahhobov", M, 100, 36, hi, TECH, tracking=-.2)["svg"]
    b += d.rbox(M, 118, W - 2 * M, 8, 2, ink, .4)
    b += (f'<rect x="{M + 1.5}" y="119.5" width="70" height="5" fill="{acc}"><animate attributeName="x" values="{M + 1.5};{W - M - 71.5};{M + 1.5}" '
          f'keyTimes="0;.5;1" calcMode="spline" keySplines=".6 0 .4 1;.6 0 .4 1" dur="9s" repeatCount="indefinite"/></rect>')

    # left: viewfinder around the ridge-line terrain, three annotated peaks
    vx, vy, vw, vh = M, 150, 470, 252
    sf, pk = d.surface(vx + 14, vy + 22, vw - 28, vh - 30, rows=22, cols=60)
    b += sf + d.camera(vx, vy, vw, vh)
    for (px, py), (k, v, dx, dy, anc) in zip(pk, [("MOBILE", "FLUTTER", -26, -34, "end"), ("API", "NODE.JS", 22, -40, "start"), ("DATA", "POSTGRESQL", 26, -24, "start")]):
        lx, ly = px + dx, py + dy
        b += f'<path d="M{px:.1f} {py:.1f}L{lx:.1f} {ly:.1f}" stroke="{acc}" stroke-width="1"/>' + d.dot(px, py, 2.8)
        tx = lx + (4 if anc == "start" else -4)
        b += d.mono(k, tx, ly - 2, 8, acc, anc, 1.6) + d.mono(v, tx, ly + 10, 8.5, ink, anc, 1.3)

    # right: caption + signal
    rx, rw = 580, W - M - 580
    b += d.para(SUMMARY, rx, 170, rw, 10, 17)
    sy = 280
    b += d.brackets(rx, sy, rw, 122, 16, acc)
    b += d.text("Signal", rx + 18, sy + 34, 16, acc, TECH, tracking=.5)["svg"]
    b += d.bars(rx + 18, sy + 90, 26, 13.4, 40)
    ow = MONO.width("ONLINE", 8, 1.2)
    b += d.mono("PIPELINE // END TO END", rx + 18, sy + 108, 7.5, mid, tracking=1.5)
    b += d.mono("ONLINE", rx + rw - 18, sy + 108, 7.5, ink, "end", 1.2) + f'<circle class="blink" cx="{rx + rw - 18 - ow - 9:.1f}" cy="{sy + 105.6}" r="2.8" fill="{acc}"/>'
    b += d.dust(3, 36)
    return d.render(b)


# ═══════════════════════════ SYSTEM ═══════════════════════════
def ecosystem(c):
    H = 330
    d = Doc(c, H, "Architecture — Flutter app, Express API, PostgreSQL, admin panel, Docker")
    b = d.card() + d.head("02", "System, end to end.", "FLUTTER / EXPRESS / POSTGRESQL")
    acc, mid, ink, hi = c["acc"], c["mid"], c["ink"], c["hi"]

    b += d.rbox(306, 100, W - M - 306, 202, 18, ink, .35).replace('/>', ' stroke-dasharray="3 6"/>')
    lab = "DOCKER"
    lw = MONO.width(lab, 8, 1.8) + 30
    b += f'<rect x="330" y="88" width="{lw:.0f}" height="24" rx="12" fill="{c["bg"]}"/>' + d.pill(330, 88, lw, 24, lab, acc, 8, 1.8)

    def node(x, y, w, h, kicker, title, sub):
        ky, ty, sy = (24, 49, h - 14) if h > 70 else (20, 40, h - 9)
        return (d.rbox(x, y, w, h, 12, ink, .55) + d.mono(kicker, x + 20, y + ky, 7.5, acc, tracking=2)
                + d.text(title, x + 20, y + ty, 17, hi, TECH, tracking=.2)["svg"] + d.mono(sub, x + 20, y + sy, 8, mid, tracking=1.2))

    b += node(M, 124, 200, 76, "CLIENT", "Flutter app", "DART, HTTP, FILE_PICKER")
    b += node(336, 124, 224, 76, "API", "Express API", "JWT, BCRYPTJS, MULTER")
    b += node(700, 124, 224, 76, "DATA", "PostgreSQL", "USERS, JOBS, INTERVIEWS")
    b += node(336, 226, 224, 64, "ADMIN", "Admin panel", "HTML, CSS, JAVASCRIPT")
    b += d.rbox(700, 226, 224, 64, 12, ink, .55) + d.mono("SIGNAL", 720, 250, 7.5, acc, tracking=2) + d.bars(720, 276, 17, 11.2, 18, w=5, seed=8)

    for pid, path, lab_, lx, ly, dur, dl in (("l1", "M256 162H336", "JWT", 296, 152, 2.6, 0), ("l2", "M560 162H700", "PG", 630, 152, 2.0, .6), ("l3", "M448 200V226", "REST", 460, 217, 1.4, .3)):
        b += f'<path id="{pid}" d="{path}" fill="none" stroke="{ink}" stroke-opacity=".6"/>'
        ex = {"l1": (256, 162, 336, 162), "l2": (560, 162, 700, 162), "l3": (448, 200, 448, 226)}[pid]
        b += f'<circle cx="{ex[0]}" cy="{ex[1]}" r="2.4" fill="{acc}"/><circle cx="{ex[2]}" cy="{ex[3]}" r="2.4" fill="{acc}"/>'
        b += f'<circle r="3" fill="{acc}"><animateMotion dur="{dur}s" begin="{dl}s" repeatCount="indefinite"><mpath xlink:href="#{pid}"/></animateMotion></circle>'
        b += d.mono(lab_, lx, ly, 8, mid, "middle" if lab_ != "REST" else "start", 1.6)
    b += d.dust(7, 30)
    return d.render(b)


# ═══════════════════════════ STACK ═══════════════════════════
STACK = [
    ("Mobile", "FLUTTER APP", ["Flutter", "Dart", "http", "shared_preferences", "file_picker", "google_fonts", "intl", "cupertino_icons"]),
    ("Backend", "NODE.JS API", ["Node.js", "Express", "JWT", "bcryptjs", "multer", "cors", "morgan", "dotenv", "uuid", "pg"]),
    ("Database", "RELATIONAL", ["PostgreSQL"]),
    ("Admin panel", "LIGHTWEIGHT WEB", ["HTML", "CSS", "JavaScript"]),
    ("Frontend", "LANGUAGES", ["React", "TypeScript", "Python"]),
    ("Tooling", "DEV WORKFLOW", ["npm", "Git", "GitHub", "Docker"]),
]
COLS = [[0, 2, 3], [1, 4, 5]]      # which groups sit in which column


def stack(c):
    CW, GAPX, CH, TS, TP, Y0 = 424, 40, 22, 9.5, 20, 92
    layout, bottoms = {}, []
    for ci, col in enumerate(COLS):
        y = Y0
        for gi in col:
            rows, cur = [[]], 0
            for t in STACK[gi][2]:
                w = MONO.width(t, TS, .6) + TP
                if rows[-1] and cur + 6 + w > CW:
                    rows.append([])
                    cur = 0
                cur += (6 if rows[-1] else 0) + w
                rows[-1].append((t, w))
            layout[gi] = (M + ci * (CW + GAPX), y, rows)
            y += 24 + len(rows) * (CH + 6) + 14
        bottoms.append(y)
    H = int(max(bottoms) + 14)
    d = Doc(c, H, "Stack — Flutter, Node.js, PostgreSQL, React, TypeScript, Docker")
    acc, mid, ink, hi = c["acc"], c["mid"], c["ink"], c["hi"]
    b = d.card() + d.head("03", "Tools of the trade.", "SIX GROUPS / TWENTY-NINE ITEMS")
    for gi, (name, sub, _) in enumerate(STACK):
        x0, y0, rows = layout[gi]
        b += d.text(name, x0, y0 + 12, 14, hi, TECH, tracking=.2)["svg"] + d.mono(sub, x0 + CW, y0 + 11, 7.5, mid, "end", 1.8)
        for ri, row in enumerate(rows):
            x, ty = x0, y0 + 24 + ri * (CH + 6)
            for ti, (t, w) in enumerate(row):
                prim = ri == 0 and ti == 0
                b += d.rbox(x, ty, w, CH, CH / 2, acc if prim else ink, 1 if prim else .36, 1.2 if prim else 1)
                b += d.mono(t, x + TP / 2, ty + CH / 2 + 3.2, TS, hi if prim else ink, tracking=.6)
                x += w + 6
    b += d.dust(9, 24)
    return d.render(b)


# ═══════════════════════════ CONTACT ═══════════════════════════
def contact(c):
    H = 232
    d = Doc(c, H, f"Contact — {EMAIL}")
    acc, mid, ink, hi = c["acc"], c["mid"], c["ink"], c["hi"]
    b = d.card() + d.head("04", "Let’s build something lasting.", "OPEN CHANNEL")
    bx, by, bw, bh = M, 92, W - 2 * M, 64
    b += d.rbox(bx, by, bw, bh, 14, acc, .95, 1.3)
    b += d.text(EMAIL, bx + 26, by + 42, 27, hi, TECH, tracking=.2, max_w=bw - 150)["svg"]
    cx, cy = bx + bw - 40, by + bh / 2
    b += (f'<circle cx="{cx}" cy="{cy}" r="20" fill="none" stroke="{acc}" stroke-width="1.2"/><g><path d="M{cx - 7} {cy + 7}L{cx + 7} {cy - 7}M{cx - 6} {cy - 7}H{cx + 7}V{cy + 6}" '
          f'fill="none" stroke="{hi}" stroke-width="1.6"/><animateTransform attributeName="transform" type="translate" values="0 0;2.5 -2.5;0 0" dur="2.6s" repeatCount="indefinite"/></g>')
    b += d.dot(M + 4, 190) + d.text("Available for opportunities", M + 20, 195, 12.5, hi, SANS)["svg"]
    b += d.text("Usually replies within a day", 300, 195, 12.5, mid, SANS)["svg"]
    b += d.mono("© 2026 JAVOHIR ABDUVAHHOBOV", W - M, 194, 7.5, mid, "end", 1.8)
    b += d.dust(11, 22)
    return d.render(b)
