# -*- coding: utf-8 -*-
"""The three panels. All copy lives here."""
import math

from common import W, MONO, SANS, Doc, cube, wrap

EMAIL = "javohirabduvahhobov@gmail.com"
SUMMARY = ("I build mobile and web apps, from the screen to the database. AI tools are part of my workflow, "
           "and I own the review and testing of what I ship.")
L = 48          # left margin
R = W - 48      # right edge


# ═══════════════════════════ IDENTITY ═══════════════════════════
def header(c):
    H = 340
    d = Doc(c, H, "Javohir Abduvahhobov. Full-stack and mobile engineer. BSc Software Engineering, open to opportunities.")
    hi, ink, mid, line, acc = c["hi"], c["ink"], c["mid"], c["line"], c["acc"]
    b = d.dot(L + 3, 55, 3, acc) + d.mono("Full-stack & mobile engineer", L + 16, 59, 12, mid, tracking=.4)
    b += d.bold("Javohir", L - 2, 122, 54, hi, tracking=-1.2) + d.bold("Abduvahhobov", L - 2, 178, 54, hi, tracking=-1.2)
    b += d.para(SUMMARY, L, 220, 400, 15, 23, ink)
    b += d.line(L, 288.5, R, 288.5, line)
    b += d.mono("BSc Software Engineering", L, 316, 12, mid)
    x = L + MONO.width("BSc Software Engineering", 12, .2) + 22
    b += d.line(x, 305, x, 319, line)
    b += d.dot(x + 18, 312, 3, acc, "pl") + d.mono("Open to opportunities", x + 30, 316, 12, mid)

    # the globe: land dots on a tilted sphere, turning slowly
    ox, oy, rr = 636, 158, 88
    g, defs = d._globe(ox, oy, rr)
    b += f'<ellipse cx="{ox}" cy="{oy + 112}" rx="66" ry="7" fill="none" stroke="{line}" stroke-dasharray="2 4"/>' + g
    return d.render(b, defs)


# ═══════════════════════════ SYSTEM ═══════════════════════════
LAYERS = [
    ("Client", "Flutter, Dart, React, TypeScript",
     "Packages: http, shared_preferences, file_picker, google_fonts, intl, cupertino_icons.", "phone"),
    ("Server", "Node.js, Express, JWT, Python",
     "Admin panel in HTML, CSS and JavaScript. Packages: bcryptjs, multer, cors, morgan, dotenv, uuid, pg.", "cube"),
    ("Data and ops", "PostgreSQL, Docker, npm",
     "Docker runs the API, admin panel and database together. Git and GitHub for source.", "db"),
]


def system(c):
    H = 408
    d = Doc(c, H, "System. Client: Flutter, Dart, React, TypeScript. Server: Node.js, Express, JWT, Python. Data and ops: PostgreSQL, Docker, npm.")
    hi, ink, mid, line, acc = c["hi"], c["ink"], c["mid"], c["line"], c["acc"]
    b = d.bold("System", L, 66, 22, hi) + d.sans("One pipeline, three layers.", L, 90, 14, mid)

    cx, A, t = 176, 32, 7
    pitch, cy0 = 92, 150
    ys = [cy0 + i * pitch for i in range(3)]

    # connectors between layers (behind the plates)
    for i in range(2):
        y1, y2 = ys[i] + t + A + 2, ys[i + 1] - A - 2
        b += d.line(cx, y1, cx, y2, acc, 1.2, 1, "3 3", "fl")

    for i, ((name, tech, note, kind), cy) in enumerate(zip(LAYERS, ys)):
        g = f'<g class="b{i + 1}">'
        g += d.box(cx, cy + t, A, A, t, "plate", grid=True)       # plate: top face centre at (cx, cy)
        if kind == "phone":
            g += d.box(cx, cy, 8, 4, 26, "obj")
        elif kind == "cube":
            g += d.box(cx, cy, 11, 11, 20, "obj")
        else:
            g += d.cylinder(cx, cy + 6, 16, 18)
        b += g + "</g>"
        # leader + text
        b += d.line(cx + 2 * A + 12, cy, 318, cy, line) + d.dot(cx + 2 * A + 12, cy, 2.4, acc)
        b += d.bold(name, 336, cy - 6, 17, hi) + d.sans(tech, 336, cy + 16, 14, ink)
        b += d.para(note, 574, cy - 8, 218, 11.5, 17, mid, MONO, .1)
    return d.render(b)


# ═══════════════════════════ CONTACT ═══════════════════════════
def contact(c):
    H = 156
    d = Doc(c, H, f"Contact: {EMAIL}. Open to opportunities, usually replies within a day.")
    hi, ink, mid, line, acc = c["hi"], c["ink"], c["mid"], c["line"], c["acc"]
    v, e = cube()
    b = d.wire(78, 78, 25, v, e, 90, 18, 30, tilt=30, persp=.05)
    b += d.bold("Always happy to chat.", 130, 68, 21, hi)
    b += d.dot(133, 93, 3, acc, "pl") + d.sans("Open to opportunities", 146, 98, 14, ink)
    b += d.sans("Usually replies within a day", 130, 119, 14, mid)

    bx, by, bw, bh = 462, 50, 330, 56
    b += f'<rect x="{bx + .5}" y="{by + .5}" width="{bw - 1}" height="{bh - 1}" rx="10" fill="none" stroke="{acc}" stroke-opacity=".7"/>'
    b += d.sans(EMAIL, bx + 22, by + 34, 17, hi, max_w=bw - 84)
    cx, cy = bx + bw - 28, by + bh / 2
    b += (f'<g stroke="{hi}" stroke-width="1.5" fill="none" stroke-linecap="round"><path d="M{cx - 6} {cy + 6}L{cx + 6} {cy - 6}M{cx - 4} {cy - 6}H{cx + 6}V{cy + 4}"/></g>')
    return d.render(b)
