# -*- coding: utf-8 -*-
"""The seven panels. Each builder takes a palette `c` and returns an SVG string."""
from common import (W, MX, BOLD, MED, LIME, VIOLET, Glyphs, otext, mid, wrap, pill, tag, glow, glass,
                    card, assemble, esc)

EMAIL = "javohirabduvahhobov@gmail.com"
HEAD = 50   # size of every section headline


def _pills(c):
    """The three role pills share one colour order everywhere: neutral, lime, violet."""
    return [(c["p1"], c["p1_ink"]), (c["lime"], c["lime_ink"]), (c["violet"], c["violet_ink"])]


# ═══════════════════════════════════ HERO ═══════════════════════════════════
def hero(c):
    H = 760
    reg = Glyphs()
    cd, back = card(c, H)

    # name: both lines share one size, fitted to the widest line
    SZ = otext(reg, "abduvahhobov", 0, 0, 120, c["ink"], tracking=-4.8, max_w=880)["size"]
    n1 = otext(reg, "javohir", W / 2, 162, SZ, c["ink"], anchor="middle", tracking=-SZ * .04)
    n2 = otext(reg, "abduvahhobov", W / 2, 292, SZ, c["ink"], anchor="middle", tracking=-SZ * .04)

    # stack of role pills, like a swatch card
    PX, PW, PH, GAP, Y0 = 130, 740, 92, 8, 346
    roles = [("Flutter developer", "mobile"), ("Node.js backend engineer", "api"), ("React & TypeScript developer", "web")]
    pills = []
    for i, ((title, tg), (fill, ink)) in enumerate(zip(roles, _pills(c))):
        y = Y0 + i * (PH + GAP)
        t = otext(reg, title, PX + 86, mid(y + PH / 2, 27), 27, ink)["svg"]
        g = otext(reg, tg, PX + PW - 72, mid(y + PH / 2, 21), 21, ink, font=MED, anchor="end", opacity=.62)["svg"]
        dur = 9 + i
        pills.append(f'<g class="sw{i}">{pill(PX, y, PW, PH, fill=fill)}{t}{g}</g>')
    sway = "".join(f"@keyframes sw{i}{{0%,100%{{transform:translateX({d}px)}}50%{{transform:translateX({-d}px)}}}}"
                   f".sw{i}{{animation:sw{i} {9 + i * 1.5}s ease-in-out infinite}}" for i, d in enumerate([9, -9, 9]))

    row_y = Y0 + 3 * PH + 2 * GAP + 44
    tg = [tag(reg, c, "full-stack & mobile engineer", 0, 0), tag(reg, c, "available for opportunities", 0, 0, dot=True),
          tag(reg, c, "BSc software engineering", 0, 0)]
    total = sum(t["width"] for t in tg) + 12 * 2
    x, row = (W - total) / 2, ""
    for lab, dot in (("full-stack & mobile engineer", False), ("available for opportunities", True), ("BSc software engineering", False)):
        t = tag(reg, c, lab, x, row_y, dot=dot)
        row += t["svg"]
        x += t["width"] + 12

    gl = c["glow_lime"]
    glows = (glow(c, 20, 560, 220, 120, -20, LIME, gl, cls="d1") + glow(c, 1000, 450, 180, 120, 25, LIME, gl, cls="d2")
             + glow(c, 900, 700, 240, 90, 0, VIOLET, c["glow_violet"], cls="d1")
             + (glow(c, 170, 350, 100, 26, 0, "#fff", c["halo"], cls="d2") if c["halo"] else ""))
    glasses = glass(c, "g1", 36, 428, 152, 222, 60, seed=0, cls="d1") + glass(c, "g2", 848, 418, 176, 136, 56, seed=1, cls="d2")
    body = (f'{back}<g clip-path="url(#cc)">{glows}{"".join(pills)}{glasses}</g>'
            f'{n1["svg"]}{n2["svg"]}{row}')
    return assemble(H, "Javohir Abduvahhobov — Full-stack & mobile engineer", reg, sway, cd, body)


# ═══════════════════════════════════ PROFILE ═══════════════════════════════════
def profile(c):
    H = 500
    reg = Glyphs()
    cd, back = card(c, H)
    lines = ["one engineer.", "the whole", "pipeline."]
    head = "".join(otext(reg, t, MX, 150 + i * 72, 64, c["ink"], tracking=-2.4)["svg"] for i, t in enumerate(lines))
    para = ("Full-stack and mobile engineer who ships the entire pipeline — Flutter on the client, a Node.js / Express "
            "REST API in the middle, PostgreSQL underneath, and a lightweight admin panel wired to it all.")
    pl = wrap(para, MED, 16.5, 470)
    ptxt = "".join(otext(reg, t, MX, 350 + i * 28, 16.5, c["mute"], font=MED)["svg"] for i, t in enumerate(pl))

    cx, cw, ph, gap, y0 = 600, 336, 102, 12, 100
    creds = [("degree", "BSc software engineering", 0), ("disciplines", "mobile, backend, db, admin", 26), ("status", "open to opportunities", 0)]
    col = ""
    for i, ((lab, val, off), (fill, ink)) in enumerate(zip(creds, _pills(c))):
        y = y0 + i * (ph + gap)
        x = cx - off
        col += (pill(x, y, cw, ph, fill=fill)
                + otext(reg, lab, x + 40, y + 38, 14, ink, font=MED, opacity=.62)["svg"]
                + otext(reg, val, x + 40, y + 70, 19, ink, max_w=cw - 80)["svg"])
    glows = glow(c, 940, 470, 200, 80, 0, LIME, c["glow_lime"] * .6, cls="d1") + glow(c, 80, 500, 200, 60, 0, VIOLET, c["glow_violet"] * .7, cls="d2")
    body = f'{back}<g clip-path="url(#cc)">{glows}</g>{head}{ptxt}{col}'
    return assemble(H, "Profile — one engineer, the whole pipeline", reg, "", cd, body)


# ═══════════════════════════════════ ARCHITECTURE ═══════════════════════════════════
def ecosystem(c):
    H = 560
    reg = Glyphs()
    cd, back = card(c, H)
    head = otext(reg, "system, end to end.", MX, 116, HEAD, c["ink"], tracking=-2)["svg"]

    # the docker tank
    tank = (f'<rect x="336" y="190" width="600" height="330" rx="90" fill="none" stroke="{c["line"]}" stroke-width="2" stroke-dasharray="3 9" stroke-linecap="round"/>')
    dock = tag(reg, c, "runs in docker", 392, 172, size=14, h=36, pad=20, fill=c["bg"], ink=c["ink"])
    dock_svg = (f'<rect x="372" y="172" width="{dock["width"] + 40:.1f}" height="36" rx="18" fill="{c["bg"]}"/>'
                f'{pill(372, 172, dock["width"] + 40, 36, stroke=c["line"])}'
                + otext(reg, "runs in docker", 372 + 20 + 20, mid(190, 14), 14, c["ink"], font=MED)["svg"])

    NW, NH = 212, 88
    nodes = [("flutter app", "dart, http, file_picker", 64, 262, 0), ("express api", "jwt, bcryptjs, multer", 368, 262, 1),
             ("postgresql", "users, jobs, interviews", 702, 262, 2)]
    fills = _pills(c)
    nsvg = ""
    for title, sub, x, y, k in nodes:
        fill, ink = fills[k]
        nsvg += (pill(x, y, NW, NH, fill=fill)
                 + otext(reg, title, x + NW / 2, y + 40, 22, ink, anchor="middle", tracking=-.5)["svg"]
                 + otext(reg, sub, x + NW / 2, y + 64, 13, ink, font=MED, anchor="middle", opacity=.66)["svg"])
    # admin panel sits quietly underneath the API
    ax, ay, ah = 368, 414, 76
    nsvg += (pill(ax, ay, NW, ah, stroke=c["ink"], sw=2)
             + otext(reg, "admin panel", ax + NW / 2, ay + 34, 20, c["ink"], anchor="middle", tracking=-.4)["svg"]
             + otext(reg, "html, css, javascript", ax + NW / 2, ay + 57, 13, c["mute"], font=MED, anchor="middle")["svg"])

    lanes = [("l1", "M276 300H368", 2.6, 0.0), ("l1b", "M368 312H276", 2.6, 1.3),
             ("l2", "M580 300H702", 2.6, 0.5), ("l2b", "M702 312H580", 2.6, 1.8),
             ("l3", "M474 352V414", 1.8, 1.0), ("l3b", "M486 414V352", 1.8, 1.9)]
    lsvg = ""
    for pid, d, dur, begin in lanes:
        back_lane = pid.endswith("b")
        col, op = (c["ink"], .55) if back_lane else (c["dot"], 1)
        lsvg += (f'<path id="{pid}" d="{d}" fill="none" stroke="{c["line"]}" stroke-width="3" stroke-linecap="round"/>'
                 f'<circle r="5" fill="{col}" opacity="{op}"><animateMotion dur="{dur}s" begin="{begin}s" repeatCount="indefinite"><mpath xlink:href="#{pid}"/></animateMotion></circle>')
    labels = (otext(reg, "jwt", 322, 286, 13, c["mute"], font=MED, anchor="middle")["svg"]
              + otext(reg, "pg", 641, 286, 13, c["mute"], font=MED, anchor="middle")["svg"]
              + otext(reg, "rest", 502, 388, 13, c["mute"], font=MED)["svg"])
    glows = glow(c, 80, 520, 220, 70, 0, VIOLET, c["glow_violet"] * .6, cls="d1") + glow(c, 960, 60, 180, 60, 0, LIME, c["glow_lime"] * .5, cls="d2")
    body = f'{back}<g clip-path="url(#cc)">{glows}</g>{head}{tank}{dock_svg}{lsvg}{nsvg}{labels}'
    return assemble(H, "Architecture — Flutter app, Express API, PostgreSQL, admin panel, Docker", reg, "", cd, body)


# ═══════════════════════════════════ STACK ═══════════════════════════════════
STACK = [
    ("mobile", "flutter app", ["Flutter", "Dart", "http", "shared_preferences", "file_picker", "google_fonts", "intl", "cupertino_icons"]),
    ("backend", "node.js api", ["Node.js", "Express", "JWT", "bcryptjs", "multer", "cors", "morgan", "dotenv", "uuid", "pg"]),
    ("database", "relational", ["PostgreSQL"]),
    ("admin panel", "lightweight web", ["HTML", "CSS", "JavaScript"]),
    ("frontend & other", "languages", ["React", "TypeScript", "Python"]),
    ("tooling", "dev workflow", ["npm", "Git", "GitHub", "Docker"]),
]


def stack(c):
    reg = Glyphs()
    CH, CG, CP, FS = 38, 8, 18, 14
    X0, X1 = 330, W - MX - 30
    bands, y = [], 158
    for gi, (label, sub, items) in enumerate(STACK):
        rows, cur = [[]], 0
        for it in items:
            w = MED.width(it, FS) + 2 * CP
            if rows[-1] and cur + CG + w > X1 - X0:
                rows.append([])
                cur = 0
            cur += (CG if rows[-1] else 0) + w
            rows[-1].append((it, w))
        bh = max(96, 2 * 29 + len(rows) * CH + (len(rows) - 1) * CG)
        bands.append((y, bh, rows))
        y += bh + 10
    H = y + 22
    cd, back = card(c, H)
    head = otext(reg, "tools of the trade.", MX, 116, HEAD, c["ink"], tracking=-2)["svg"]
    fills = [(c["lime"], c["lime_ink"]), (c["violet"], c["violet_ink"]), (c["p1"], c["p1_ink"])] * 2
    out = ""
    for gi, ((label, sub, _), (by, bh, rows)) in enumerate(zip(STACK, bands)):
        out += f'<rect x="{MX}" y="{by}" width="{W - 2 * MX}" height="{bh}" rx="48" fill="{c["band"]}"/>'
        fill, ink = fills[gi]
        ly = by + bh / 2
        out += otext(reg, label, MX + 40, ly - 2, 22, c["ink"], tracking=-.5)["svg"]
        out += otext(reg, sub, MX + 40, ly + 22, 13.5, c["mute"], font=MED)["svg"]
        top = by + (bh - (len(rows) * CH + (len(rows) - 1) * CG)) / 2
        for ri, row in enumerate(rows):
            x = X0
            for ii, (it, w) in enumerate(row):
                cy = top + ri * (CH + CG)
                if ri == 0 and ii == 0:
                    out += pill(x, cy, w, CH, fill=fill) + otext(reg, it, x + CP, mid(cy + CH / 2, FS), FS, ink)["svg"]
                else:
                    out += pill(x, cy, w, CH, stroke=c["line"]) + otext(reg, it, x + CP, mid(cy + CH / 2, FS), FS, c["ink"], font=MED)["svg"]
                x += w + CG
    glows = glow(c, 960, 90, 200, 70, 0, LIME, c["glow_lime"] * .55, cls="d1")
    body = f'{back}<g clip-path="url(#cc)">{glows}</g>{head}{out}'
    return assemble(H, "Stack — Flutter, Node.js, PostgreSQL, React, TypeScript, Docker", reg, "", cd, body)


# ═══════════════════════════════════ CONTACT ═══════════════════════════════════
def contact(c):
    H = 440
    reg = Glyphs()
    cd, back = card(c, H)
    head = otext(reg, "let’s build something lasting.", MX, 116, HEAD, c["ink"], tracking=-2, max_w=W - 2 * MX)["svg"]
    cy0, ch = 168, 132
    r = ch / 2
    em = otext(reg, EMAIL, MX + 52, mid(cy0 + r, 40), 40, c["lime_ink"], tracking=-1.2, max_w=640)
    bx, by = W - MX - r, cy0 + r
    arrow = (f'<g><circle cx="{bx}" cy="{by}" r="46" fill="#000000"/>'
             f'<path d="M{bx-14} {by+14}L{bx+14} {by-14}M{bx-12} {by-14}H{bx+14}V{by+12}" fill="none" stroke="#FEFFFC" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>'
             f'<animateTransform attributeName="transform" type="translate" values="0 0;4 -4;0 0" dur="2.2s" repeatCount="indefinite"/></g>')
    mail = (pill(MX, cy0, W - 2 * MX, ch, fill=c["lime"]) + em["svg"] + arrow)
    ty = cy0 + ch + 38
    t1 = tag(reg, c, "available for opportunities", MX, ty, dot=True)
    t2 = tag(reg, c, "usually replies within a day", MX + t1["width"] + 12, ty)
    glows = glow(c, 940, 440, 240, 80, 0, VIOLET, c["glow_violet"], cls="d1") + glow(c, 40, 60, 160, 60, 0, LIME, c["glow_lime"] * .5, cls="d2")
    body = f'{back}<g clip-path="url(#cc)">{glows}</g>{head}{mail}{t1["svg"]}{t2["svg"]}'
    return assemble(H, f"Contact — {EMAIL}", reg, "", cd, body)


# ═══════════════════════════════════ SOUNDTRACK ═══════════════════════════════════
def soundtrack(c, track="we do what we want (edit)", artist="alan fitzpatrick"):
    H = 260
    reg = Glyphs()
    cd, back = card(c, H)
    cx, cy, R = 150, 130, 84
    grooves = "".join(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="#fff" stroke-opacity="{.1 if r % 6 else .2}" stroke-width=".8"/>' for r in range(32, R - 2, 3))
    vinyl = (f'<g><circle cx="{cx}" cy="{cy}" r="{R}" fill="#000"/>'
             f'<circle cx="{cx}" cy="{cy}" r="{R}" fill="none" stroke="{c["ink"] if c["name"]=="dark" else "#000"}" stroke-opacity=".28" stroke-width="1.5"/>{grooves}'
             f'<circle cx="{cx}" cy="{cy}" r="27" fill="{LIME}"/><circle cx="{cx}" cy="{cy-13}" r="4" fill="{VIOLET}"/><circle cx="{cx}" cy="{cy}" r="4.5" fill="#000"/>'
             f'<path d="M{cx} {cy} L{cx+R*.92:.1f} {cy-R*.38:.1f} A{R} {R} 0 0 0 {cx+R*.38:.1f} {cy-R*.92:.1f}Z" fill="#fff" fill-opacity=".07"/>'
             f'<animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="7s" repeatCount="indefinite"/></g>')
    tx = 290
    np_w = MED.width("now playing", 14) + 2 * 22 + 34
    nowp = pill(tx, 50, np_w, 38, stroke=c["line"])
    bars = "".join(f'<rect class="eq" x="{tx + 24 + i * 6}" y="61" width="3.4" height="16" rx="1.7" fill="{c["dot"]}" style="animation-duration:{d}s;animation-delay:-{dl}s"/>'
                   for i, (d, dl) in enumerate([(.7, .1), (.5, .3), (.9, .2), (.6, .5)]))
    nowp += bars + otext(reg, "now playing", tx + 22 + 34, mid(69, 14), 14, c["ink"], font=MED)["svg"]
    ttl = otext(reg, track, tx, 148, 36, c["ink"], tracking=-1.2, max_w=W - MX - tx - 4)
    art = otext(reg, artist, tx, 182, 17, c["mute"], font=MED)
    bw = 232
    bxp = W - MX - bw
    btn = (pill(bxp, 49, bw, 40, fill=c["lime"]) + otext(reg, "listen on spotify", bxp + 26, mid(69, 15), 15, c["lime_ink"])["svg"]
           + f'<path d="M{bxp+bw-46} 78L{bxp+bw-28} 60M{bxp+bw-44} 60H{bxp+bw-28}V76" fill="none" stroke="{c["lime_ink"]}" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"/>')
    py = 214
    prog = (f'<rect x="{tx}" y="{py-4}" width="{W-MX-tx}" height="8" rx="4" fill="{c["band"]}"/>'
            f'<rect class="pg" x="{tx}" y="{py-4}" width="{W-MX-tx}" height="8" rx="4" fill="{c["dot"] if c["name"]=="dark" else c["violet"]}"/>'
            f'<circle r="8" cy="{py}" fill="{c["ink"]}"><animate attributeName="cx" values="{tx+4};{W-MX-4}" dur="40s" repeatCount="indefinite"/></circle>')
    css = ("@keyframes eq{from{transform:scaleY(.25)}to{transform:scaleY(1)}}"
           ".eq{transform-box:fill-box;transform-origin:center;animation:eq .7s ease-in-out infinite alternate}"
           "@keyframes pg{from{transform:scaleX(0)}to{transform:scaleX(1)}}"
           ".pg{transform-box:fill-box;transform-origin:left center;animation:pg 40s linear infinite}")
    glows = glow(c, 60, 250, 240, 70, 0, VIOLET, c["glow_violet"], cls="d1") + glow(c, 700, 0, 220, 60, 0, LIME, c["glow_lime"] * .45, cls="d2")
    body = f'{back}<g clip-path="url(#cc)">{glows}</g>{vinyl}{nowp}{btn}{ttl["svg"]}{art["svg"]}{prog}'
    return assemble(H, f"Soundtrack — {track} by {artist}", reg, css, cd, body)


# ═══════════════════════════════════ FOOTER ═══════════════════════════════════
def footer(c):
    H = 360
    reg = Glyphs()
    cd, back = card(c, H)
    t = otext(reg, "thank you", W / 2, 210, 190, c["ink"], anchor="middle", tracking=-8, max_w=W - 2 * MX)
    t1 = tag(reg, c, "javohir abduvahhobov", 0, 0)
    t2 = tag(reg, c, "crafted with intent, 2026", 0, 0)
    total = t1["width"] + t2["width"] + 12
    ry, x = 268, (W - total) / 2
    row = tag(reg, c, "javohir abduvahhobov", x, ry)["svg"] + tag(reg, c, "crafted with intent, 2026", x + t1["width"] + 12, ry)["svg"]
    glows = (glow(c, 10, 330, 230, 110, -15, LIME, c["glow_lime"], cls="d1") + glow(c, 990, 350, 230, 110, 15, LIME, c["glow_lime"], cls="d2")
             + glow(c, 500, 380, 260, 60, 0, VIOLET, c["glow_violet"], cls="d1"))
    gl = glass(c, "g3", 884, 232, 150, 120, 52, seed=1, cls="d2")
    body = f'{back}<g clip-path="url(#cc)">{glows}{gl}</g>{t["svg"]}{row}'
    return assemble(H, "Thank you for visiting", reg, "", cd, body)
