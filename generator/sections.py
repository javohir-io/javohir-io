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

    kv = [("ROLE", "FULL-STACK & MOBILE"), ("DEGREE", "BSC SOFTWARE ENG.")]
    x = M
    for k, v in kv:
        b += d.mono(f"{k} :", x, 44, 8.5, acc) + d.mono(v, x + MONO.width(f"{k} : ", 8.5, 1.4) + 4, 44, 8.5, mid)
        x += MONO.width(f"{k} : {v}", 8.5, 1.4) + 48

    b += d.text("Javohir Abduvahhobov", M, 100, 36, hi, TECH, tracking=-.2)["svg"]
    b += d.rbox(M, 118, W - 2 * M, 8, 2, ink, .4)
    b += (f'<rect x="{M + 1.5}" y="119.5" width="70" height="5" fill="{acc}"><animate attributeName="x" values="{M + 1.5};{W - M - 71.5};{M + 1.5}" '
          f'keyTimes="0;.5;1" calcMode="spline" keySplines=".6 0 .4 1;.6 0 .4 1" dur="9s" repeatCount="indefinite"/></rect>')

    # left: viewfinder around the ridge-line terrain, three peaks
    vx, vy, vw, vh = M, 150, 470, 252
    sf, pk = d.surface(vx + 14, vy + 22, vw - 28, vh - 30, rows=20, cols=52)
    b += sf + d.camera(vx, vy, vw, vh)
    for (px, py), (k, dx, dy, anc) in zip(pk, [("MOBILE", -24, -30, "end"), ("API", 22, -36, "start"), ("DATA", 26, -22, "start")]):
        lx, ly = px + dx, py + dy
        b += f'<path d="M{px:.1f} {py:.1f}L{lx:.1f} {ly:.1f}" stroke="{acc}" stroke-width="1"/>' + d.dot(px, py, 2.8)
        b += d.mono(k, lx + (4 if anc == "start" else -4), ly + 3, 8, acc, anc, 1.6)

    # right: caption + Earth
    rx, rw = 580, W - M - 580
    b += d.para(SUMMARY, rx, 170, rw, 10, 17)
    ey, eh = 262, 140
    ecx, ecy, R = rx + rw / 2, ey + eh / 2, 56
    back, top = d.orbit(ecx, ecy, R, 134, 24)
    b += d.brackets(rx, ey, rw, eh, 16, acc) + back + d.earth(ecx, ecy, R) + top
    b += d.dust(3, 30)
    return d.render(b)


# ═══════════════════════════ SYSTEM ═══════════════════════════
def ecosystem(c):
    H = 330
    d = Doc(c, H, "Architecture — Flutter app, Express API, PostgreSQL, admin panel, Docker")
    b = d.card() + d.head("02", "System, end to end.")
    acc, mid, ink, hi = c["acc"], c["mid"], c["ink"], c["hi"]

    b += d.rbox(316, 98, W - M - 316, 206, 18, ink, .35).replace('/>', ' stroke-dasharray="3 6"/>')
    lab = "DOCKER"
    lw = MONO.width(lab, 8, 1.8) + 30
    b += f'<rect x="338" y="86" width="{lw:.0f}" height="24" rx="12" fill="{c["bg"]}"/>' + d.pill(338, 86, lw, 24, lab, acc, 8, 1.8)

    def node(x, y, w, h, title, kind, s, tall=False):
        o = d.rbox(x, y, w, h, 12, ink, .55)
        if tall:
            o += d.solid(kind, x + w / 2, y + h / 2 - 12, s) + d.text(title, x + 20, y + h - 18, 17, hi, TECH, tracking=.2)["svg"]
        else:
            o += d.text(title, x + 22, y + h / 2 + 6, 17, hi, TECH, tracking=.2)["svg"] + d.solid(kind, x + w - 46, y + h / 2, s)
        return o

    b += node(M, 114, 204, 176, "Flutter app", "phone", 40, True)
    b += node(344, 114, 228, 78, "Express API", "cube", 19)
    b += node(344, 212, 228, 78, "Admin panel", "monitor", 17)
    b += node(716, 114, 204, 176, "PostgreSQL", "cylinder", 36, True)

    for pid, path, ex, dur, dl in (("l1", "M260 153H344", (260, 153, 344, 153), 2.6, 0), ("l2", "M572 153H716", (572, 153, 716, 153), 2.0, .6), ("l3", "M458 192V212", (458, 192, 458, 212), 1.2, .3)):
        b += f'<path id="{pid}" d="{path}" fill="none" stroke="{ink}" stroke-opacity=".6"/>'
        b += f'<circle cx="{ex[0]}" cy="{ex[1]}" r="2.4" fill="{acc}"/><circle cx="{ex[2]}" cy="{ex[3]}" r="2.4" fill="{acc}"/>'
        b += f'<circle r="3" fill="{acc}"><animateMotion dur="{dur}s" begin="{dl}s" repeatCount="indefinite"><mpath xlink:href="#{pid}"/></animateMotion></circle>'
    b += d.dust(7, 26)
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
COLS = [[0, 2, 3], [1, 4, 5]]


def stack(c):
    CW, GAPX, CH, TS, TP, Y0 = 424, 40, 22, 9.5, 20, 92
    layout, bottoms = {}, []
    for ci, col in enumerate(COLS):
        y = Y0
        for gi in col:
            rows, cur = [[]], 0
            for t in STACK[gi][1]:
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
    b = d.card() + d.head("03", "Tools of the trade.") + d.solid("ico", W - M - 18, 42, 13, dur=22)
    for gi, (name, _) in enumerate(STACK):
        x0, y0, rows = layout[gi]
        b += d.text(name, x0, y0 + 12, 14, hi, TECH, tracking=.2)["svg"]
        for ri, row in enumerate(rows):
            x, ty = x0, y0 + 24 + ri * (CH + 6)
            for ti, (t, w) in enumerate(row):
                prim = ri == 0 and ti == 0
                b += d.rbox(x, ty, w, CH, CH / 2, acc if prim else ink, 1 if prim else .36, 1.2 if prim else 1)
                b += d.mono(t, x + TP / 2, ty + CH / 2 + 3.2, TS, hi if prim else ink, tracking=.6)
                x += w + 6
    b += d.dust(9, 22)
    return d.render(b)


# ═══════════════════════════ CONTACT ═══════════════════════════
def contact(c):
    H = 216
    d = Doc(c, H, f"Contact — {EMAIL}")
    acc, mid, ink, hi = c["acc"], c["mid"], c["ink"], c["hi"]
    b = d.card() + d.head("04", "Let’s build something lasting.") + d.globe(W - M - 18, 42, 14)
    bx, by, bw, bh = M, 92, W - 2 * M, 64
    b += d.rbox(bx, by, bw, bh, 14, acc, .95, 1.3)
    b += d.text(EMAIL, bx + 26, by + 42, 27, hi, TECH, tracking=.2, max_w=bw - 150)["svg"]
    cx, cy = bx + bw - 40, by + bh / 2
    b += (f'<circle cx="{cx}" cy="{cy}" r="20" fill="none" stroke="{acc}" stroke-width="1.2"/><g><path d="M{cx - 7} {cy + 7}L{cx + 7} {cy - 7}M{cx - 6} {cy - 7}H{cx + 7}V{cy + 6}" '
          f'fill="none" stroke="{hi}" stroke-width="1.6"/><animateTransform attributeName="transform" type="translate" values="0 0;2.5 -2.5;0 0" dur="2.6s" repeatCount="indefinite"/></g>')
    b += d.dot(M + 4, 190) + d.text("Available for opportunities", M + 20, 195, 12.5, hi, SANS)["svg"]
    b += d.dust(11, 18)
    return d.render(b)
