# -*- coding: utf-8 -*-
"""The six panels. Each builder takes a palette `c` and returns an SVG string."""
from common import W, M, SANS, SANSB, TECH, MONO, Doc

EMAIL = "javohirabduvahhobov@gmail.com"
SUMMARY = ("Full-stack and mobile engineer who ships the entire pipeline — Flutter on the client, a Node.js / Express "
           "REST API in the middle, PostgreSQL underneath, and a lightweight admin panel wired to it all.")


# ═══════════════════════════ HERO ═══════════════════════════
def hero(c):
    H = 668
    d = Doc(c, H, "Javohir Abduvahhobov — Full-stack & mobile engineer")
    b = d.card()
    red, mid, ink, hi = c["red"], c["mid"], c["ink"], c["hi"]

    # meta row, spread across the page
    items = [("ROLE", "FULL-STACK & MOBILE"), ("STACK", "FLUTTER / NODE.JS / POSTGRESQL"), ("DEGREE", "BSC SOFTWARE ENG."), ("STATUS", "OPEN TO WORK")]
    ws = [MONO.width(f"{k} : {v}", 8.5, 1.4) for k, v in items]
    gap = (W - 2 * M - sum(ws)) / (len(items) - 1)
    x = M
    for (k, v), w in zip(items, ws):
        kw = MONO.width(f"{k} : ", 8.5, 1.4)
        b += d.mono(f"{k} :", x, 50, 8.5, red) + d.mono(v, x + kw + 4, 50, 8.5, mid)
        x += w + gap

    b += d.text("Javohir Abduvahhobov", M, 130, 44, hi, SANS, tracking=-1.4)["svg"]
    # the empty bar under the title, with one red block shuttling along it
    b += d.rbox(M, 158, W - 2 * M, 14, 3, ink, .5)
    b += (f'<rect x="{M + 2}" y="160" width="84" height="10" fill="{red}"><animate attributeName="x" values="{M + 2};{W - M - 86};{M + 2}" '
          f'keyTimes="0;.5;1" calcMode="spline" keySplines=".6 0 .4 1;.6 0 .4 1" dur="9s" repeatCount="indefinite"/></rect>')

    # left: numeral + ridge-line terrain with three annotated peaks
    sf, pk = d.surface(M, 236, 512, 372)
    b += sf
    b += d.text("01", M, 276, 58, red, TECH, tracking=1)["svg"]
    b += d.mono("PROFILE", M, 302, 8.5, mid, tracking=2.2) + d.mono("END-TO-END ENGINEER", M, 318, 8.5, mid, tracking=2.2)
    notes = [("MOBILE", "FLUTTER", -30, -64, "end"), ("API", "NODE.JS", 24, -74, "start"), ("DATA", "POSTGRESQL", 30, -46, "start")]
    for (px, py), (k, v, dx, dy, anc) in zip(pk, notes):
        lx, ly = px + dx, py + dy
        b += f'<path d="M{px:.1f} {py:.1f}L{lx:.1f} {ly:.1f}H{lx + (22 if anc == "start" else -22):.1f}" fill="none" stroke="{red}" stroke-width="1"/>' + d.dot(px, py)
        tx = lx + (28 if anc == "start" else -28)
        b += d.mono(k, tx, ly - 6, 8, red, anc, 1.8) + d.mono(v, tx, ly + 8, 9, ink, anc, 1.4)
    b += d.pill(M + 150, 620, 212, 28, "REF — JA-2026-0001")

    # right: caption paragraph, signal panel, year + globe
    rx, rw = 604, W - M - 604
    b += d.para(SUMMARY, rx, 238, rw, 10, 17)
    sy = 372
    b += d.brackets(rx, sy, rw, 148, 18)
    b += d.text("Signal", rx + 20, sy + 40, 22, red, TECH, tracking=.5)["svg"]
    b += d.bars(rx + 20, sy + 108, 25, 12.6, 56)
    b += d.mono("PIPELINE // END TO END", rx + 20, sy + 132, 8, red, tracking=1.6)
    ow = MONO.width("ONLINE", 8, 1.2)
    b += d.mono("ONLINE", rx + rw - 20, sy + 132, 8, ink, "end", 1.2) + f'<circle class="blink" cx="{rx + rw - 20 - ow - 12:.1f}" cy="{sy + 129.5}" r="3" fill="{red}"/>'
    b += d.mono("STATUS //", rx + rw - 20 - ow - 22, sy + 132, 8, red, "end", 1.6)
    b += d.text("MMXXVI", rx, 596, 44, hi, TECH, tracking=1)["svg"] + d.globe(W - M - 22, 580, 22)
    b += d.meter(rx, 626, "SCANNING ON PROGRESS")
    b += d.dust(3)
    return d.render(b)


# ═══════════════════════════ PROFILE ═══════════════════════════
def profile(c):
    H = 530
    d = Doc(c, H, "Profile — one engineer, the whole pipeline")
    b = d.card() + d.head("02", "One engineer, the whole pipeline.", "SUBJECT RECORD")
    red, mid, ink, hi = c["red"], c["mid"], c["ink"], c["hi"]
    b += d.para(SUMMARY, M, 172, 400, 10.5, 18)
    stats = [("04", "ROLES"), ("06", "STACK GROUPS"), ("01", "PIPELINE")]
    for i, (n, lab) in enumerate(stats):
        sx = M + i * 138
        b += d.text(n, sx, 340, 40, hi, TECH, tracking=1)["svg"] + d.mono(lab, sx, 362, 8.5, mid, tracking=2)
        if i:
            b += d.rule(sx - 22, 312, sx - 22, 368, .25)
    b += d.rule(M, 392, 456, 392, .2)
    b += d.pill(M, 420, 214, 28, "REF — JA-2026-0001")
    # record
    bx, by, bw, bh = 520, 158, W - M - 520, 330
    b += d.rbox(bx, by, bw, bh, 16, ink, .45)
    rows = [("NAME", "Javohir Abduvahhobov"), ("FUNCTION", "Full-stack & mobile engineer"), ("DEGREE", "BSc Software Engineering"),
            ("DISCIPLINES", "Mobile, backend, database, admin"), ("STACK", "Flutter / Node.js / PostgreSQL"), ("STATUS", "Open to opportunities"), ("REPLY TIME", "Within a day")]
    rh = (bh - 20) / len(rows)
    for i, (k, v) in enumerate(rows):
        yy = by + 10 + i * rh
        if i:
            b += d.rule(bx + 20, yy, bx + bw - 20, yy, .16)
        b += d.mono(k, bx + 22, yy + rh / 2 + 3, 8.5, mid, tracking=1.8)
        b += d.text(v, bx + 150, yy + rh / 2 + 4.6, 13.5, hi, SANS, max_w=bw - 150 - 40)["svg"]
        if k == "STATUS":
            b += d.dot(bx + bw - 28, yy + rh / 2)
    b += d.dust(5)
    return d.render(b)


# ═══════════════════════════ ARCHITECTURE ═══════════════════════════
def ecosystem(c):
    H = 530
    d = Doc(c, H, "Architecture — Flutter app, Express API, PostgreSQL, admin panel, Docker")
    b = d.card() + d.head("03", "System, end to end.", "PIPELINE / CONTAINERIZED")
    red, mid, ink, hi = c["red"], c["mid"], c["ink"], c["hi"]

    b += d.rbox(316, 176, W - M - 316, 310, 22, ink, .38).replace('/>', ' stroke-dasharray="3 6"/>')
    lab = "RUNS IN DOCKER"
    lw = MONO.width(lab, 8.5, 1.8) + 40
    b += f'<rect x="346" y="162" width="{lw:.0f}" height="28" rx="14" fill="{c["bg"]}"/>' + d.pill(346, 162, lw, 28, lab, red, 8.5, 1.8)

    def node(x, y, w, h, kicker, title, sub):
        return (d.rbox(x, y, w, h, 14, ink, .55) + d.mono(kicker, x + 22, y + 30, 8, red, tracking=2)
                + d.text(title, x + 22, y + 62, 20, hi, SANS, tracking=-.3)["svg"] + d.mono(sub, x + 22, y + 84, 9, mid, tracking=1.2))

    b += node(M, 206, 210, 104, "CLIENT", "Flutter app", "DART, HTTP, FILE_PICKER")
    b += node(356, 206, 236, 104, "API", "Express API", "JWT, BCRYPTJS, MULTER")
    b += node(670, 206, 244, 104, "DATA", "PostgreSQL", "USERS, JOBS, INTERVIEWS")
    b += node(356, 362, 236, 104, "ADMIN", "Admin panel", "HTML, CSS, JAVASCRIPT")
    # live signal tile
    b += d.rbox(670, 362, 244, 104, 14, ink, .55) + d.mono("SIGNAL", 692, 392, 7.5, red, tracking=2) + d.bars(692, 448, 18, 11.6, 36, w=5, seed=8)

    for pid, path, lab_, lx, ly, dur, dl in (("l1", "M266 258H356", "JWT", 292, 246, 2.6, 0), ("l2", "M592 258H670", "PG", 631, 246, 2.0, .6), ("l3", "M474 310V362", "REST", 486, 340, 1.6, .3)):
        b += f'<path id="{pid}" d="{path}" fill="none" stroke="{ink}" stroke-opacity=".6"/>'
        ex = {"l1": (266, 258, 356, 258), "l2": (592, 258, 670, 258), "l3": (474, 310, 474, 362)}[pid]
        b += f'<circle cx="{ex[0]}" cy="{ex[1]}" r="2.6" fill="{red}"/><circle cx="{ex[2]}" cy="{ex[3]}" r="2.6" fill="{red}"/>'
        b += f'<circle r="3.2" fill="{red}"><animateMotion dur="{dur}s" begin="{dl}s" repeatCount="indefinite"><mpath xlink:href="#{pid}"/></animateMotion></circle>'
        b += d.mono(lab_, lx, ly, 8.5, mid, "middle" if lab_ != "REST" else "start", 1.6)
    b += d.dust(7)
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


def stack(c):
    X0, X1, TS, TP, CH = 330, W - M, 10, 26, 26
    plans, ys, y = [], [], 152
    for _, _, items in STACK:
        rows, cur = [[]], 0
        for t in items:
            w = MONO.width(t, TS, .6) + TP
            if rows[-1] and cur + 8 + w > X1 - X0:
                rows.append([])
                cur = 0
            cur += (8 if rows[-1] else 0) + w
            rows[-1].append((t, w))
        h = 34 + len(rows) * (CH + 8) - 8 + 8
        plans.append(rows)
        ys.append((y, h))
        y += h
    H = int(y + 36)
    d = Doc(c, H, "Stack — Flutter, Node.js, PostgreSQL, React, TypeScript, Docker")
    red, mid, ink, hi = c["red"], c["mid"], c["ink"], c["hi"]
    b = d.card() + d.head("04", "Tools of the trade.", "SIX GROUPS / TWENTY-NINE ITEMS")
    for i, ((name, sub, _), rows, (yy, h)) in enumerate(zip(STACK, plans, ys)):
        if i:
            b += d.rule(M, yy - 4, W - M, yy - 4, .16)
        b += d.mono(f"4.{i + 1}", M, yy + 34, 9, red, tracking=1.6) + d.text(name, M + 40, yy + 36, 17, hi, SANS, tracking=-.2)["svg"] + d.mono(sub, M + 40, yy + 54, 8, mid, tracking=1.8)
        for ri, row in enumerate(rows):
            x, ty = X0, yy + 16 + ri * (CH + 8)
            for ti, (t, w) in enumerate(row):
                prim = ri == 0 and ti == 0
                b += d.rbox(x, ty, w, CH, CH / 2, red if prim else ink, 1 if prim else .38, 1.2 if prim else 1)
                b += d.mono(t, x + TP / 2, ty + CH / 2 + 3.4, TS, hi if prim else ink, tracking=.6)
                x += w + 8
    b += d.dust(9)
    return d.render(b)


# ═══════════════════════════ CONTACT ═══════════════════════════
def contact(c):
    H = 372
    d = Doc(c, H, f"Contact — {EMAIL}")
    red, mid, ink, hi = c["red"], c["mid"], c["ink"], c["hi"]
    b = d.card() + d.head("05", "Let’s build something lasting.", "OPEN CHANNEL")
    bx, by, bw, bh = M, 160, W - 2 * M, 118
    b += d.rbox(bx, by, bw, bh, 18, red, .95, 1.3)
    b += d.mono("TO", bx + 30, by + 38, 8, mid, tracking=2.4)
    b += d.text(EMAIL, bx + 30, by + 86, 36, hi, TECH, tracking=.2, max_w=bw - 190)["svg"]
    cx, cy = bx + bw - 62, by + bh / 2
    b += (f'<circle cx="{cx}" cy="{cy}" r="32" fill="none" stroke="{red}" stroke-width="1.3"/><g><path d="M{cx - 11} {cy + 11}L{cx + 11} {cy - 11}M{cx - 9} {cy - 11}H{cx + 11}V{cy + 9}" '
          f'fill="none" stroke="{hi}" stroke-width="1.8"/><animateTransform attributeName="transform" type="translate" values="0 0;3 -3;0 0" dur="2.6s" repeatCount="indefinite"/></g>')
    b += d.dot(M + 4, 318) + d.text("Available for opportunities", M + 22, 323, 13.5, hi, SANS)["svg"]
    b += d.text("Usually replies within a day", 330, 323, 13.5, mid, SANS)["svg"]
    b += d.dust(11)
    return d.render(b)


# ═══════════════════════════ FOOTER ═══════════════════════════
def footer(c):
    H = 168
    d = Doc(c, H, "Thank you for visiting")
    red, mid, ink, hi = c["red"], c["mid"], c["ink"], c["hi"]
    b = d.card()
    lab = "ENGINEER / FLUTTER / NODE.JS / REACT / MMXXVI"
    lw = MONO.width(lab, 9, 1.8) + 56
    b += d.pill((W - lw) / 2, 54, lw, 32, lab, red, 9, 1.8)
    b += d.rings(M + 20, 70, 11) + d.mono("© 2026 JAVOHIR ABDUVAHHOBOV", W - M, 74, 8, mid, "end", 1.8)
    b += d.mono("THANK YOU FOR VISITING", W / 2, 124, 8.5, mid, "middle", 2.6)
    b += d.dust(13, 40)
    return d.render(b)
