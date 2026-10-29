# -*- coding: utf-8 -*-
"""The four panels, drawn on an 840px canvas (about GitHub's README width) with type that stays readable when scaled down."""
from common import W, M, SANS, TECH, MONO, Doc

EMAIL = "javohirabduvahhobov@gmail.com"
SUMMARY = ("Full-stack and mobile engineer who ships the entire pipeline — Flutter on the client, a Node.js / Express "
           "REST API in the middle, PostgreSQL underneath, and a lightweight admin panel wired to it all.")


# ═══════════════════════════ MASTHEAD ═══════════════════════════
def hero(c):
    H = 484
    d = Doc(c, H, "Javohir Abduvahhobov — Full-stack & mobile engineer")
    b = d.card()
    acc, mid, ink, hi = c["acc"], c["mid"], c["ink"], c["hi"]

    x = M
    for k, v in (("ROLE", "FULL-STACK & MOBILE"), ("DEGREE", "BSC SOFTWARE ENG.")):
        b += d.mono(f"{k} :", x, 44, 11, acc) + d.mono(v, x + MONO.width(f"{k} : ", 11, 1.2) + 4, 44, 11, mid)
        x += MONO.width(f"{k} : {v}", 11, 1.2) + 40

    b += d.text("Javohir Abduvahhobov", M, 104, 42, hi, TECH, tracking=-.3)["svg"]
    b += d.rbox(M, 124, W - 2 * M, 8, 2, ink, .5)
    b += (f'<rect x="{M + 1.5}" y="125.5" width="64" height="5" fill="{acc}"><animate attributeName="x" values="{M + 1.5};{W - M - 65.5};{M + 1.5}" '
          f'keyTimes="0;.5;1" calcMode="spline" keySplines=".6 0 .4 1;.6 0 .4 1" dur="9s" repeatCount="indefinite"/></rect>')

    # left: viewfinder around the ridge-line terrain
    vx, vy, vw, vh = M, 160, 366, 292
    sf, pk = d.surface(vx + 12, vy + 30, vw - 24, vh - 40, rows=18, cols=46)
    b += sf + d.camera(vx, vy, vw, vh)
    for (px, py), (k, dx, dy, anc) in zip(pk, [("MOBILE", -22, -30, "end"), ("API", 20, -38, "start"), ("DATA", 24, -22, "start")]):
        lx, ly = px + dx, py + dy
        b += f'<path d="M{px:.1f} {py:.1f}L{lx:.1f} {ly:.1f}" stroke="{acc}" stroke-width="1.3"/>' + d.dot(px, py, 3.2)
        b += d.mono(k, lx + (5 if anc == "start" else -5), ly + 4, 11, acc, anc, 1.4)

    # right: summary + Earth
    rx, rw = 440, W - M - 440
    b += d.para(SUMMARY, rx, 186, rw, 14.5, 23)
    ey, eh = 296, 156
    ecx, ecy, R = rx + rw / 2, ey + eh / 2, 47
    back, top = d.orbit(ecx, ecy, R, 114, 20)
    b += d.brackets(rx, ey, rw, eh, 18, acc, 1.8) + back + d.earth(ecx, ecy, R) + top
    return d.render(b)


# ═══════════════════════════ SYSTEM ═══════════════════════════
def ecosystem(c):
    H = 344
    d = Doc(c, H, "Architecture — Flutter app, Express API, PostgreSQL, admin panel, Docker")
    b = d.card() + d.head("02", "System, end to end.")
    acc, mid, ink, hi = c["acc"], c["mid"], c["ink"], c["hi"]

    b += d.rbox(228, 100, W - M - 228, 218, 18, ink, .45).replace('/>', ' stroke-dasharray="3 6"/>')
    lab = "DOCKER"
    lw = MONO.width(lab, 11, 1.6) + 32
    b += f'<rect x="250" y="87" width="{lw:.0f}" height="26" rx="13" fill="{c["bg"]}"/>' + d.pill(250, 87, lw, 26, lab, acc, 11, 1.6)

    def node(x, y, w, h, title, kind, s, tall=False):
        o = d.rbox(x, y, w, h, 12, ink, .7)
        if tall:
            o += d.solid(kind, x + w / 2, y + h / 2 - 14, s) + d.text(title, x + 18, y + h - 20, 18, hi, TECH, tracking=.2)["svg"]
        else:
            o += d.text(title, x + 18, y + h / 2 + 6.5, 18, hi, TECH, tracking=.2)["svg"] + d.solid(kind, x + w - 34, y + h / 2, s)
        return o

    b += node(M, 118, 154, 188, "Flutter app", "phone", 34, True)
    b += node(250, 118, 206, 88, "Express API", "cube", 15)
    b += node(250, 218, 206, 88, "Admin panel", "monitor", 13)
    b += node(604, 118, 168, 188, "PostgreSQL", "cylinder", 31, True)

    for pid, path, ex, dur, dl in (("l1", "M194 162H250", (194, 162, 250, 162), 2.4, 0), ("l2", "M456 162H604", (456, 162, 604, 162), 2.2, .6), ("l3", "M353 206V218", (353, 206, 353, 218), 1.0, .3)):
        b += f'<path id="{pid}" d="{path}" fill="none" stroke="{ink}" stroke-opacity=".7" stroke-width="1.3"/>'
        b += f'<circle cx="{ex[0]}" cy="{ex[1]}" r="3" fill="{acc}"/><circle cx="{ex[2]}" cy="{ex[3]}" r="3" fill="{acc}"/>'
        b += f'<circle r="3.6" fill="{acc}"><animateMotion dur="{dur}s" begin="{dl}s" repeatCount="indefinite"><mpath xlink:href="#{pid}"/></animateMotion></circle>'
    return d.render(b)


# ═══════════════════════════ STACK ═══════════════════════════
STACK = [
    ("Mobile", ["Flutter", "Dart", "http", "shared_preferences", "file_picker", "google_fonts", "intl", "cupertino_icons"]),
    ("Backend", ["Node.js", "Express", "JWT", "bcryptjs", "multer", "cors", "morgan", "dotenv", "uuid", "pg"]),
    ("Database", ["PostgreSQL"]),
    ("Admin panel", ["HTML", "CSS", "JavaScript"]),
    ("Frontend", ["React", "TypeScript", "Python"]),
    ("Tooling", ["npm", "Git", "GitHub", "Docker"]),
]
COLS = [[0, 4, 5], [1, 2, 3]]


def stack(c):
    CW, GAPX, CH, TS, TP, Y0 = 360, 40, 28, 12, 22, 94
    layout, bottoms = {}, []
    for ci, col in enumerate(COLS):
        y = Y0
        for gi in col:
            rows, cur = [[]], 0
            for t in STACK[gi][1]:
                w = MONO.width(t, TS, .5) + TP
                if rows[-1] and cur + 7 + w > CW:
                    rows.append([])
                    cur = 0
                cur += (7 if rows[-1] else 0) + w
                rows[-1].append((t, w))
            layout[gi] = (M + ci * (CW + GAPX), y, rows)
            y += 32 + len(rows) * (CH + 8) + 12
        bottoms.append(y)
    H = int(max(bottoms) + 4)
    d = Doc(c, H, "Stack — Flutter, Node.js, PostgreSQL, React, TypeScript, Docker")
    acc, mid, ink, hi = c["acc"], c["mid"], c["ink"], c["hi"]
    b = d.card() + d.head("03", "Tools of the trade.") + d.solid("ico", W - M - 14, 40, 11.5, dur=22)
    for gi, (name, _) in enumerate(STACK):
        x0, y0, rows = layout[gi]
        b += d.text(name, x0, y0 + 15, 17, hi, TECH, tracking=.2)["svg"]
        for ri, row in enumerate(rows):
            x, ty = x0, y0 + 30 + ri * (CH + 8)
            for ti, (t, w) in enumerate(row):
                prim = ri == 0 and ti == 0
                b += d.rbox(x, ty, w, CH, CH / 2, acc if prim else ink, 1 if prim else .55, 1.5 if prim else 1.2)
                b += d.mono(t, x + TP / 2, ty + CH / 2 + 4, TS, hi if prim else ink, tracking=.5)
                x += w + 7
    return d.render(b)


# ═══════════════════════════ CONTACT ═══════════════════════════
def contact(c):
    H = 236
    d = Doc(c, H, f"Contact — {EMAIL}")
    acc, mid, ink, hi = c["acc"], c["mid"], c["ink"], c["hi"]
    b = d.card() + d.head("04", "Let’s build something lasting.") + d.globe(W - M - 14, 38, 11.5)
    bx, by, bw, bh = M, 94, W - 2 * M, 70
    b += d.rbox(bx, by, bw, bh, 16, acc, 1, 1.8)
    b += d.text(EMAIL, bx + 24, by + 45, 29, hi, TECH, tracking=.1, max_w=bw - 110)["svg"]
    cx, cy = bx + bw - 38, by + bh / 2
    b += (f'<circle cx="{cx}" cy="{cy}" r="20" fill="none" stroke="{acc}" stroke-width="1.6"/><g><path d="M{cx - 7} {cy + 7}L{cx + 7} {cy - 7}M{cx - 6} {cy - 7}H{cx + 7}V{cy + 6}" '
          f'fill="none" stroke="{hi}" stroke-width="1.8"/><animateTransform attributeName="transform" type="translate" values="0 0;2.5 -2.5;0 0" dur="2.6s" repeatCount="indefinite"/></g>')
    b += d.dot(M + 5, 200) + d.text("Available for opportunities", M + 22, 205, 15, hi, SANS)["svg"]
    return d.render(b)
