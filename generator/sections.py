# -*- coding: utf-8 -*-
"""The seven Y2K panels. Each builder takes a palette `c` and returns an SVG string."""
import math
from common import W, MX, BOLD, MED, MONO, MONOB, PIX, Doc, wrap, holo_at

EMAIL = "javohirabduvahhobov@gmail.com"
ROLES = ["Flutter developer", "Node.js backend engineer", "React & TypeScript developer", "Software engineer"]


def _sparkles(d, pts):
    return "".join(d.star(x, y, r, delay=i * .9, dur=3 + (i % 3)) for i, (x, y, r) in enumerate(pts))


def hero(c):
    H = 880
    d = Doc(c, H, "Javohir Abduvahhobov — Full-stack & mobile engineer")
    b = d.backdrop()
    ink, mute = c["ink"], c["mute"]

    # top meta row
    b += d.globe(MX + 18, 66, 16, op=.9)
    for i, t in enumerate(["PORTFOLIO.2026", "FLUTTER / NODE.JS / REACT", "FULL-STACK & MOBILE"]):
        b += d.label(t, MX + 46, 58 + i * 14, 10, mute if i else ink, tracking=1.6)
    b += f'<rect x="{W - MX - 128}" y="44" width="92" height="32" rx="16" fill="none" stroke="{c["line"]}" stroke-opacity="{c["line_op"]}" stroke-width="1.4"/>'
    b += d.label("2026", W - MX - 82, 64, 12, ink, anchor="middle", tracking=3)
    b += d.chrome_star(W - MX + 4, 60, 18)

    # the name
    b += d.chrome("JAVOHIR", W / 2, 262, 160, xs=1.12, max_w=888)
    n = d.text("ABDUVAHHOBOV", W / 2, 352, 84, ink, font=BOLD, anchor="middle", tracking=1, xs=1.25, max_w=888)
    b += n["svg"]

    # intro
    para = "Full-stack and mobile engineer shipping the whole pipeline: Flutter on the client, Node.js and PostgreSQL underneath."
    for i, ln in enumerate(wrap(para, MED, 15.5, 300)):
        b += d.text(ln, MX, 418 + i * 24, 15.5, ink, font=MED)["svg"]

    # centrepiece: CD + liquid metal
    b += d.cd(470, 655, 205, tilt=-22, squash=.6, spin=20)
    b += d.chrome_blob(640, 700, 84, seed=11, dur=12, sx=1.05, sy=1.1, rot=.4)
    b += d.chrome_blob(612, 560, 24, seed=4, dur=9)
    b += d.chrome_blob(430, 806, 20, seed=8, dur=10)
    b += d.chrome_blob(560, 612, 13, seed=2, dur=8)

    b += "".join(d.bubble(x, y, r, delay=i * 2, dur=10 + i) for i, (x, y, r) in enumerate([(545, 560, 16), (840, 480, 12), (640, 790, 10), (300, 760, 9)]))

    # window: role.exe (roles cycle)
    wx, wy, ww, wh = MX, 505, 292, 164
    b += d.window(wx, wy, ww, wh, "role.exe")
    b += d.label("WELCOME TO THE PIPELINE", wx + 18, wy + 58, 10, mute)
    d.k("@keyframes role{0%{opacity:0;transform:translateY(8px)}4%{opacity:1;transform:none}23%{opacity:1;transform:none}27%,100%{opacity:0;transform:translateY(-8px)}}"
        ".role{opacity:0;animation:role 12s ease-in-out infinite}")
    for i, r in enumerate(ROLES):
        for j, ln in enumerate(wrap(r.lower(), BOLD, 22, ww - 36)):
            pass
        lines = wrap(r, BOLD, 21, ww - 40)
        g = "".join(d.text(ln, wx + 18, wy + 92 + j * 26, 21, ink, font=BOLD, tracking=-.3)["svg"] for j, ln in enumerate(lines))
        b += f'<g class="role" style="animation-delay:{i * 3}s">{g}</g>'
    b += f'<rect x="{wx + 18}" y="{wy + 128}" width="{ww - 36}" height="8" rx="4" fill="none" stroke="{c["line"]}" stroke-opacity="{c["line_op"]}"/>'
    b += (f'<rect x="{wx + 20}" y="{wy + 130}" width="{ww - 40}" height="4" rx="2" fill="url(#holo)">'
          f'<animate attributeName="width" values="0;{ww - 40};{ww - 40}" keyTimes="0;.85;1" dur="3s" repeatCount="indefinite"/></rect>')
    b += d.label("LOADING VISUALS...", wx + 18, wy + 154, 9, mute)

    # window: stack.dll
    sx, sy, sw, sh = 646, 402, 298, 214
    b += d.window(sx, sy, sw, sh, "stack.dll")
    items = [("MOBILE", "Flutter"), ("BACKEND", "Node.js"), ("DATABASE", "PostgreSQL"), ("FRONTEND", "React"), ("LANGUAGE", "TypeScript"), ("DEVOPS", "Docker")]
    for i, (k, v) in enumerate(items):
        yy = sy + 62 + i * 21
        b += d.label(f"0{i + 1} //", sx + 18, yy, 10.5, mute) + d.label(k, sx + 58, yy, 10.5, ink, tracking=1.4) + d.label(v.upper(), sx + sw - 18, yy, 10.5, c["accent"], anchor="end", tracking=1.2, bold=True)
        b += f'<rect x="{sx + 14}" y="{yy - 11}" width="{sw - 28}" height="16" rx="8" fill="url(#holo)" opacity="0"><animate attributeName="opacity" values="0;.22;0;0" keyTimes="0;.08;.16;1" dur="9s" begin="{i * 1.5}s" repeatCount="indefinite"/></rect>'
    b += d.label("OK", sx + sw - 44, sy + sh - 14, 10, ink, anchor="middle", tracking=2)
    b += f'<rect x="{sx + sw - 74}" y="{sy + sh - 30}" width="60" height="22" rx="4" fill="none" stroke="{c["line"]}" stroke-opacity="{c["line_op"]}"/>'

    # window: data_stream
    tx, ty, tw, th = MX, 700, 292, 126
    b += d.window(tx, ty, tw, th, "data_stream", bar=28)
    b += d.terrain(tx + 8, ty + 36, tw - 16, th - 44, col=c["accent"] if c["name"] == "dark" else "#5b61b8")

    # window: connect.online
    cx_, cy_, cw, ch = 706, 668, 238, 158
    b += d.window(cx_, cy_, cw, ch, "connect.online", bar=28)
    b += d.label("STATUS: ONLINE", cx_ + 16, cy_ + 54, 10, ink)
    b += d.label("CONNECTED TO PIPELINE", cx_ + 16, cy_ + 70, 9, mute)
    b += d.globe(cx_ + 56, cy_ + 112, 30, col=ink)
    b += f'<circle cx="{cx_ + cw - 28}" cy="{cy_ + 54}" r="4" fill="#7dffb0"/><circle class="ping" cx="{cx_ + cw - 28}" cy="{cy_ + 54}" r="4" fill="none" stroke="#7dffb0" stroke-width="1.4"/>'
    d.k("@keyframes ping{0%{transform:scale(1);opacity:.8}100%{transform:scale(3.2);opacity:0}}.ping{transform-box:fill-box;transform-origin:center;animation:ping 2.2s ease-out infinite}")
    b += d.eq(cx_ + 112, cy_ + 112, 12, 9, 40, col=c["accent"], w=4)

    # ambient
    b += _sparkles(d, [(110, 160, 12), (900, 190, 10), (330, 470, 9), (610, 480, 14), (930, 640, 9), (60, 640, 8), (500, 850, 10)])
    b += d.flare(250, 395, 12, "#ffb48a", 1) + d.flare(960, 330, 10, "#8fd0ff", 2.2)
    b += d.ticker(MX, 855, W - 2 * MX, "FULL-STACK & MOBILE ENGINEER + AVAILABLE FOR OPPORTUNITIES + BSC SOFTWARE ENGINEERING", 10.5, 40, mute)
    b += d.frame()
    return d.render(b)


def _pixel_icons(d, x, y, px=5):
    """Pixel planet, hourglass, folder and smiley — each with its own little animation."""
    out = ""
    # planet
    pl = {"a": "#c9b8ff", "b": "#7f6cf0", "r": "#ff8fe0"}
    rows = []
    for j in range(11):
        r = ""
        for i in range(11):
            dx, dy = i - 5, j - 5
            ring = .8 < (dx / 6.2) ** 2 + ((dy + .3) / 1.7) ** 2 < 1.25
            body = dx * dx + dy * dy <= 19
            r += "r" if (ring and (dy >= 0 or not body)) else ("a" if body and dx + dy < 2 else "b" if body else ".")
        rows.append(r)
    out += f'<g class="bob">{d.pixel(x, y, rows, pl, px)}</g>'
    d.k("@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-4px)}}.bob{animation:bob 3s ease-in-out infinite}")
    # hourglass
    hx = x + 13 * px
    frame = ["bbbbbbbbb"] + ["........."] * 9 + ["bbbbbbbbb"]
    glass = [".a.......a.", ] 
    hg = {"b": "#8fa2ff", "s": "#ffd98a"}
    out += d.pixel(hx, y, ["sssssssss", "ssssssss.", ".sssssss.", "..sssss..", "...sss...", "....s....", "...s.s...", "..s...s..", ".s.....s.", "s.......s", "sssssssss"], {"s": "#8fa2ff"}, px)
    d.k("@keyframes drain{from{transform:scaleY(1)}to{transform:scaleY(0)}}@keyframes fill{from{transform:scaleY(0)}to{transform:scaleY(1)}}"
        ".drain{transform-box:fill-box;transform-origin:bottom;animation:drain 4s steps(5) infinite}.fill{transform-box:fill-box;transform-origin:bottom;animation:fill 4s steps(5) infinite}")
    out += d.pixel(hx + px, y + px, ["ssssss", ".ssss.", "..ss.."], {"s": "#ffd98a"}, px, cls="drain")
    out += d.pixel(hx + px, y + 8 * px, ["..ss..", ".ssss.", "ssssss"], {"s": "#ffd98a"}, px, cls="fill")
    # folder
    fx = x + 25 * px
    fol = ["yyyy.......", "yyyyyyyyyyy", "yaaaaaaaaay", "yaaaaaaaaay", "yaaaaaaaaay", "yaaaaaaaaay", "yyyyyyyyyyy"]
    out += f'<g class="bob" style="animation-delay:-1s">{d.pixel(fx, y + 2 * px, fol, {"y": "#ff8fe0", "a": "#ffc9ef"}, px)}</g>'
    # smiley
    sx = x + 38 * px
    face = ["...yyyyy...", ".yyyyyyyyy.", "yyyyyyyyyyy", "yyyyyyyyyyy", "yyyyyyyyyyy", "yyyyyyyyyyy", "yyyyyyyyyyy", "yyyyyyyyyyy", ".yyyyyyyyy.", "...yyyyy..."]
    out += d.pixel(sx, y, face, {"y": "#fff3a8"}, px)
    out += d.pixel(sx + 3 * px, y + 3 * px, ["#...#", "#...#"], {"#": "#14163f"}, px, cls="eyes")
    out += d.pixel(sx + 2 * px, y + 6 * px, ["#.....#", ".#####."], {"#": "#14163f"}, px)
    d.k("@keyframes blink2{0%,90%,100%{transform:scaleY(1)}94%{transform:scaleY(.1)}}.eyes{transform-box:fill-box;transform-origin:center;animation:blink2 4s infinite}")
    return out


def _chip(d, c, t, x, y, primary, size=11.5):
    w = MONO.width(t, size, .6) + 24
    if primary:
        o = (f'<rect x="{x}" y="{y}" width="{w:.1f}" height="26" rx="13" fill="url(#holo)" stroke="#fff" stroke-opacity=".9"/>'
             + d.text(t, x + 12, y + 17, size, "#0a0b1f", font=MONOB, tracking=.6)["svg"])
    else:
        o = (f'<rect x="{x}" y="{y}" width="{w:.1f}" height="26" rx="13" fill="{c["line"]}" fill-opacity="{.07 if c["name"] == "dark" else .35}" stroke="{c["line"]}" stroke-opacity="{c["line_op"] * .8:.2f}"/>'
             + d.text(t, x + 12, y + 17, size, c["ink"], font=MONO, tracking=.6)["svg"])
    return o, w


# ═══════════════════════════ PROFILE ═══════════════════════════
def profile(c):
    H = 660
    d = Doc(c, H, "Profile — one engineer, the whole pipeline")
    b = d.backdrop([(160, 120, 300, 160, "#c28bff"), (880, 150, 280, 200, "#7ee8ff"), (500, 620, 380, 140, "#ff8fe0")])
    ink, mute = c["ink"], c["mute"]
    b += d.label("SYSTEM_OVERVIEW v2.6", MX, 62, 10.5, mute, tracking=2)
    lines = ["ONE ENGINEER.", "THE WHOLE", "PIPELINE."]
    size = 560 / BOLD.width(lines[0], 1, 0, 1.12)
    size = min(size, 84)
    for i, ln in enumerate(lines):
        b += d.chrome(ln, MX + 6, 168 + i * (size * 1.12), size, xs=1.12, anchor="start", sheen=(i == 0))
    # liquid ring + friends
    b += d.liquid_ring(790, 190, 92, thick=58, seed=3, dur=14, sx=1.05, sy=.95)
    b += d.chrome_blob(925, 90, 20, seed=4) + d.chrome_blob(660, 290, 14, seed=6)
    b += "".join(d.bubble(x, y, r, delay=i * 2.2, dur=9 + i) for i, (x, y, r) in enumerate([(905, 300, 18), (700, 80, 11), (950, 215, 9)]))
    b += d.chrome_star(930, 330, 22)

    # holographic slab behind the window
    b += ('<g><path d="M70 372L520 346Q552 345 546 376L520 596Q516 622 486 624L96 632Q64 632 62 600L50 410Q48 376 70 372Z" fill="url(#holo)" stroke="#fff" stroke-opacity=".8" stroke-width="1.5" opacity=".92"/>'
          '<path d="M70 372L520 346Q552 345 546 376L540 420L60 440Z" fill="#fff" opacity=".18"/></g>')
    # window
    wx, wy, ww, wh = 330, 360, W - 330 - MX, 250
    b += d.window(wx, wy, ww, wh, "system.overview")
    para = ("Full-stack and mobile engineer who ships the entire pipeline — Flutter on the client, a Node.js / Express "
            "REST API in the middle, PostgreSQL underneath, and a lightweight admin panel wired to it all.")
    for i, ln in enumerate(wrap(para, MED, 14.5, 236)):
        b += d.text(ln, wx + 22, wy + 66 + i * 23, 14.5, ink, font=MED)["svg"]
    rows = [("01", "DEGREE", "BSc Software Engineering"), ("02", "DISCIPLINES", "Mobile, backend, DB, admin"), ("03", "STATUS", "Open to opportunities")]
    rx0 = wx + 296
    rw = ww - 296 - 20
    for i, (n_, k, v) in enumerate(rows):
        yy = wy + 54 + i * 62
        b += (f'<rect x="{rx0}" y="{yy}" width="{rw}" height="50" rx="25" fill="{c["line"]}" fill-opacity="{.08 if c["name"] == "dark" else .4}" stroke="url(#edge)" stroke-width="1.3"/>'
              + d.label(n_, rx0 + 22, yy + 21, 10, mute) + d.label(k, rx0 + 44, yy + 21, 9.5, mute, tracking=1.6)
              + d.text(v, rx0 + 22, yy + 40, 14, ink, font=BOLD, max_w=rw - 70)["svg"])
        b += f'<circle cx="{rx0 + rw - 24}" cy="{yy + 25}" r="9" fill="none" stroke="{c["accent"]}" stroke-width="1.4"/><circle cx="{rx0 + rw - 24}" cy="{yy + 25}" r="3.5" fill="{c["accent"]}" class="blink" style="animation-delay:{i * .33}s"/>'
    b += _sparkles(d, [(300, 330, 11), (40, 330, 9), (620, 120, 10), (960, 480, 12)])
    b += d.flare(560, 346, 11, "#ffb48a", 1.4)
    b += d.frame()
    return d.render(b)


# ═══════════════════════════ ARCHITECTURE ═══════════════════════════
def ecosystem(c):
    H = 640
    d = Doc(c, H, "Architecture — Flutter app, Express API, PostgreSQL, admin panel, Docker")
    b = d.backdrop([(120, 520, 300, 140, "#7ee8ff"), (880, 120, 300, 160, "#c28bff"), (560, 620, 360, 120, "#ff8fe0")])
    ink, mute, acc = c["ink"], c["mute"], c["accent"]
    b += d.chrome("SYSTEM, END TO END.", MX, 136, 60, xs=1.12, anchor="start", max_w=760)
    b += d.label("SYS_DASHBOARD / PIPELINE", MX, 62, 10.5, mute, tracking=2)
    b += d.chrome_star(W - MX - 10, 90, 26)

    # docker frame
    fx, fy, fw, fh = 336, 196, 608, 410
    b += (f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" rx="34" fill="none" stroke="{acc}" stroke-opacity=".7" stroke-width="1.6" stroke-dasharray="4 8" stroke-linecap="round">'
          f'<animate attributeName="stroke-dashoffset" from="0" to="-48" dur="3s" repeatCount="indefinite"/></rect>')
    b += f'<rect x="{fx + 28}" y="{fy - 14}" width="132" height="28" rx="14" fill="{c["bg1"] if c["name"] == "dark" else "#e6e8f4"}" stroke="{acc}" stroke-opacity=".7"/>' + d.label("DOCKER.CONTAINER", fx + 94, fy + 4, 9.5, acc, anchor="middle", tracking=1.2)

    nodes = {}

    def node(key, x, y, w, h, title, sub, icon):
        nodes[key] = (x, y, w, h)
        o = d.window(x, y, w, h, title, bar=30)
        o += icon(x, y, w, h)
        o += d.text(sub[0], x + 18, y + h - 38, 17, ink, font=BOLD, tracking=-.3)["svg"] + d.label(sub[1], x + 18, y + h - 17, 10, mute, tracking=.8)
        return o

    def phone(x, y, w, h):
        px, py = x + w - 78, y + 44
        return (f'<rect x="{px}" y="{py}" width="44" height="76" rx="9" fill="none" stroke="{ink}" stroke-width="1.5"/><rect x="{px + 15}" y="{py + 5}" width="14" height="3" rx="1.5" fill="{ink}"/>'
                f'<rect x="{px + 7}" y="{py + 18}" width="30" height="46" rx="4" fill="url(#holo)" opacity=".85"/><circle cx="{px + 22}" cy="{py + 70}" r="2" fill="{ink}"/>')

    def server(x, y, w, h):
        px, py = x + w - 90, y + 46
        o = "".join(f'<rect x="{px}" y="{py + i * 24}" width="56" height="18" rx="5" fill="none" stroke="{ink}" stroke-width="1.5"/><circle cx="{px + 11}" cy="{py + 9 + i * 24}" r="2.6" fill="{acc}" class="blink" style="animation-delay:{i * .4}s"/><line x1="{px + 20}" y1="{py + 9 + i * 24}" x2="{px + 48}" y2="{py + 9 + i * 24}" stroke="{ink}" stroke-opacity=".5"/>' for i in range(3))
        return o

    def cyl(x, y, w, h):
        px, py, cw, ch = x + w - 92, y + 48, 60, 70
        o = f'<path d="M{px} {py + 8}V{py + ch - 8}A{cw / 2} 9 0 0 0 {px + cw} {py + ch - 8}V{py + 8}" fill="none" stroke="{ink}" stroke-width="1.5"/><ellipse cx="{px + cw / 2}" cy="{py + 8}" rx="{cw / 2}" ry="9" fill="url(#holo)" stroke="{ink}" stroke-width="1.5"/>'
        for k in (1, 2):
            o += f'<path d="M{px} {py + 8 + k * 17}A{cw / 2} 9 0 0 0 {px + cw} {py + 8 + k * 17}" fill="none" stroke="{ink}" stroke-opacity=".6"/>'
        return o

    def browser(x, y, w, h):
        px, py = x + w - 92, y + 46
        return (f'<rect x="{px}" y="{py}" width="62" height="50" rx="6" fill="none" stroke="{ink}" stroke-width="1.5"/><line x1="{px}" y1="{py + 12}" x2="{px + 62}" y2="{py + 12}" stroke="{ink}" stroke-width="1.2"/>'
                f'<circle cx="{px + 8}" cy="{py + 6}" r="1.8" fill="{ink}"/><circle cx="{px + 15}" cy="{py + 6}" r="1.8" fill="{ink}"/><rect x="{px + 8}" y="{py + 20}" width="28" height="6" rx="3" fill="url(#holo)"/>'
                f'<rect x="{px + 8}" y="{py + 31}" width="46" height="4" rx="2" fill="{ink}" opacity=".4"/><rect x="{px + 8}" y="{py + 39}" width="34" height="4" rx="2" fill="{ink}" opacity=".4"/>')

    b += node("app", MX, 296, 236, 168, "flutter_app.exe", ("Flutter app", "DART, HTTP, FILE_PICKER"), phone)
    b += node("api", 366, 240, 250, 168, "express_api.js", ("Express API", "JWT, BCRYPTJS, MULTER"), server)
    b += node("db", 664, 240, 250, 168, "postgresql.db", ("PostgreSQL", "USERS, JOBS, INTERVIEWS"), cyl)
    b += node("admin", 366, 436, 250, 140, "admin_panel.html", ("Admin panel", "HTML, CSS, JAVASCRIPT"), browser)

    # links with packets
    def link(path, lab, lx, ly, dur, delay):
        o = f'<path id="lk{lx}" d="{path}" fill="none" stroke="{acc}" stroke-opacity=".55" stroke-width="1.6" stroke-dasharray="3 7"><animate attributeName="stroke-dashoffset" from="0" to="-40" dur="1.6s" repeatCount="indefinite"/></path>'
        o += (f'<g><circle r="9" fill="{acc}" opacity=".5" filter="url(#b4)"/><circle r="4.2" fill="#fff"/>'
              f'<animateMotion dur="{dur}s" begin="{delay}s" repeatCount="indefinite"><mpath xlink:href="#lk{lx}"/></animateMotion></g>')
        o += d.label(lab, lx, ly, 9.5, ink, anchor="middle", tracking=1.4, bold=True)
        return o

    b += link("M292 380H366", "JWT", 329, 366, 2.4, 0)
    b += link("M616 324H664", "PG", 640, 310, 1.8, .6)
    b += link("M491 408V436", "REST", 524, 428, 1.6, .3)

    # sys_dashboard sparkline
    dx, dy, dw, dh = 664, 436, 250, 140
    b += d.window(dx, dy, dw, dh, "sys_dashboard", bar=30)
    b += d.label("NETWORK STATUS", dx + 18, dy + 52, 9.5, mute) + d.label("ONLINE", dx + dw - 18, dy + 52, 9.5, "#7dffb0", anchor="end", bold=True)
    pts = lambda ph: "M" + "L".join(f"{dx + 18 + i * (dw - 36) / 24:.1f} {dy + 100 - 18 * math.sin(i * .55 + ph) - 9 * math.sin(i * 1.3 + ph * 1.7):.1f}" for i in range(25))
    b += (f'<path d="{pts(0)}" fill="none" stroke="{acc}" stroke-width="2" stroke-linecap="round"><animate attributeName="d" values="{pts(0)};{pts(2.1)};{pts(4.2)};{pts(6.283)}" dur="6s" repeatCount="indefinite"/></path>')
    b += d.eq(dx + 18, dy + 120, 28, 8, 12, col=c["line"] if c["name"] == "dark" else "#5b61b8", w=3)
    b += _sparkles(d, [(280, 220, 11), (60, 560, 9), (960, 600, 10), (640, 170, 8)])
    b += d.flare(46, 290, 9, "#8fd0ff", .5)
    b += d.frame()
    return d.render(b)


# ═══════════════════════════ STACK ═══════════════════════════
STACK = [
    ("mobile.dll", "FLUTTER APP", ["Flutter", "Dart", "http", "shared_preferences", "file_picker", "google_fonts", "intl", "cupertino_icons"]),
    ("backend.js", "NODE.JS API", ["Node.js", "Express", "JWT", "bcryptjs", "multer", "cors", "morgan", "dotenv", "uuid", "pg"]),
    ("database.db", "RELATIONAL", ["PostgreSQL"]),
    ("admin_panel.html", "LIGHTWEIGHT WEB", ["HTML", "CSS", "JavaScript"]),
    ("frontend.ts", "LANGUAGES", ["React", "TypeScript", "Python"]),
    ("tooling.sh", "DEV WORKFLOW", ["npm", "Git", "GitHub", "Docker"]),
]
COLS = [[0, 4], [1, 5], [2, 3]]


def stack(c):
    CW, GAP, X0, Y0 = 288, 12, MX, 200
    d = Doc(c, 900, "Stack — Flutter, Node.js, PostgreSQL, React, TypeScript, Docker")
    ink, mute = c["ink"], c["mute"]
    body, heights, plans = "", [], {}
    for gi, (title, sub, items) in enumerate(STACK):
        rows, cur = [[]], 0
        for t in items:
            w = MONO.width(t, 11.5, .6) + 24
            if rows[-1] and cur + 6 + w > CW - 32:
                rows.append([])
                cur = 0
            cur += (6 if rows[-1] else 0) + w
            rows[-1].append(t)
        plans[gi] = rows
        heights.append(32 + 44 + len(rows) * 32 + 10)
    colpos = []
    for ci, col in enumerate(COLS):
        y = Y0
        for gi in col:
            colpos.append((gi, X0 + ci * (CW + GAP), y, heights[gi]))
            y += heights[gi] + GAP
    bottoms = [max(p[2] + p[3] for p in colpos if p[1] == X0 + ci * (CW + GAP)) for ci in range(3)]
    pix_y = bottoms[2]
    H = int(max(bottoms[0], bottoms[1], pix_y + 130)) + 40
    d.h = H
    d = Doc(c, H, d.title)
    b = d.backdrop([(140, 160, 300, 160, "#c28bff"), (860, 140, 300, 160, "#7ee8ff"), (500, H - 60, 400, 140, "#ff8fe0")])
    b += d.label("FILE_EXPLORER / TOOLS", MX, 62, 10.5, mute, tracking=2)
    b += d.chrome("TOOLS OF THE TRADE.", MX, 150, 62, xs=1.12, anchor="start", max_w=680)
    for i in range(6):
        b += d.holo_orb(W - MX - 150 + i * 30, 96, 12, delay=i * 1.2)
    b += d.label("GRADIENT STUDIES", W - MX, 130, 9, mute, anchor="end", tracking=1.6)
    b += d.chrome_star(W - MX - 6, 160, 12)
    for gi, x, y, h in colpos:
        title, sub, _ = STACK[gi]
        b += d.window(x, y, CW, h, title, bar=30)
        b += d.label(sub, x + 16, y + 50, 9.5, mute, tracking=1.8)
        for ri, row in enumerate(plans[gi]):
            cx = x + 16
            for ti, t in enumerate(row):
                o, w = _chip(d, c, t, cx, y + 64 + ri * 32, ri == 0 and ti == 0)
                b += o
                cx += w + 6
    # pixel graphics window
    px_x = X0 + 2 * (CW + GAP)
    ph = H - 40 - pix_y
    b += d.window(px_x, pix_y, CW, ph, "pixel_graphics.bmp", bar=30)
    b += _pixel_icons(d, px_x + 18, pix_y + 52, 4)
    sw = [holo_at(i / 12) for i in range(12)]
    for i, col in enumerate(sw):
        b += f'<rect x="{px_x + 18 + i * 21}" y="{pix_y + ph - 28}" width="17" height="10" rx="2" fill="{col}" class="glow" style="animation-delay:{i * .22}s"/>'
    b += _sparkles(d, [(40, 130, 10), (980, 330, 9), (1000 - 30, H - 70, 10), (30, H - 60, 8)])
    b += d.frame()
    return d.render(b)


# ═══════════════════════════ CONTACT ═══════════════════════════
def contact(c):
    H = 560
    d = Doc(c, H, f"Contact — {EMAIL}")
    b = d.backdrop([(140, 120, 300, 160, "#7ee8ff"), (880, 460, 320, 180, "#c28bff"), (500, 560, 380, 120, "#ff8fe0")])
    ink, mute, acc = c["ink"], c["mute"], c["accent"]
    b += d.label("CONNECT.ONLINE", MX, 62, 10.5, mute, tracking=2)
    s = min(78, 600 / BOLD.width("SOMETHING LASTING.", 1, 0, 1.1))
    b += d.chrome("LET’S BUILD", MX + 4, 150, s, xs=1.1, anchor="start") + d.chrome("SOMETHING LASTING.", MX + 4, 150 + s * 1.15, s, xs=1.1, anchor="start", sheen=False)
    b += d.globe(840, 150, 70, col=ink, spin=18, n=7)
    b += f'<ellipse cx="840" cy="150" rx="104" ry="30" fill="none" stroke="{acc}" stroke-opacity=".8" transform="rotate(-18 840 150)"/>'
    b += f'<g transform="rotate(-18 840 150)"><circle r="5" fill="#fff"><animateMotion dur="6s" repeatCount="indefinite" path="M840 120a104 30 0 1 1 -.1 0"/></circle></g>' if False else ""
    b += d.chrome_blob(930, 60, 18, seed=2) + d.chrome_star(742, 70, 18)
    # compose window
    wx, wy, ww, wh = MX, 300, W - 2 * MX, 210
    b += d.window(wx, wy, ww, wh, "compose.exe")
    b += d.label("TO:", wx + 24, wy + 68, 11, mute, tracking=2)
    em = d.text(EMAIL, wx + 70, wy + 74, 31, ink, font=BOLD, tracking=-.6, max_w=ww - 360)
    b += em["svg"]
    cxp = em["x0"] + em["width"] + 8
    b += f'<rect x="{cxp:.1f}" y="{wy + 48}" width="3" height="32" fill="{acc}" class="blink"/>'
    b += f'<line x1="{wx + 24}" y1="{wy + 94}" x2="{wx + ww - 24}" y2="{wy + 94}" stroke="{c["line"]}" stroke-opacity="{c["line_op"] * .5:.2f}"/>'
    b += d.label("SUBJECT:", wx + 24, wy + 124, 11, mute, tracking=2) + d.text("Let’s build something lasting", wx + 110, wy + 129, 15, ink, font=MED)["svg"]
    b += d.label("STATUS:", wx + 24, wy + 156, 11, mute, tracking=2)
    b += f'<circle cx="{wx + 108}" cy="{wy + 152}" r="4.5" fill="#7dffb0"/><circle class="ping" cx="{wx + 108}" cy="{wy + 152}" r="4.5" fill="none" stroke="#7dffb0" stroke-width="1.4"/>'
    d.k("@keyframes ping{0%{transform:scale(1);opacity:.8}100%{transform:scale(3.2);opacity:0}}.ping{transform-box:fill-box;transform-origin:center;animation:ping 2.2s ease-out infinite}")
    b += d.text("Available for opportunities", wx + 124, wy + 157, 15, ink, font=MED)["svg"]
    b += d.label("USUALLY REPLIES WITHIN A DAY", wx + 24, wy + 188, 9.5, mute, tracking=1.8)
    b += d.button(wx + ww - 276, wy + 132, 244, 54, "SEND MESSAGE  ↗".replace("  ↗", ""), 15)
    b += f'<path d="M{wx + ww - 70} {wy + 168}l14 -14m-12 0h12v12" fill="none" stroke="#0a0b1f" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><animateTransform attributeName="transform" type="translate" values="0 0;3 -3;0 0" dur="2s" repeatCount="indefinite"/></path>'
    b += "".join(d.bubble(x, y, r, delay=i * 2, dur=10 + i) for i, (x, y, r) in enumerate([(620, 250, 14), (700, 220, 9)]))
    b += _sparkles(d, [(60, 270, 9), (610, 120, 11), (960, 270, 10)])
    b += d.flare(700, 190, 10, "#ffb48a", 1)
    b += d.frame()
    return d.render(b)


# ═══════════════════════════ SOUNDTRACK ═══════════════════════════
def soundtrack(c, track="We Do What We Want (Edit)", artist="Alan Fitzpatrick"):
    H = 340
    d = Doc(c, H, f"Now playing — {track} by {artist}")
    b = d.backdrop([(160, 200, 300, 140, "#c28bff"), (860, 60, 300, 120, "#7ee8ff"), (700, 340, 300, 100, "#ff8fe0")])
    ink, mute, acc = c["ink"], c["mute"], c["accent"]
    wx, wy, ww, wh = MX, 36, W - 2 * MX, H - 72
    b += d.window(wx, wy, ww, wh, "y2k_vibes.mp3")
    b += d.cd(wx + 140, wy + 160, 104, tilt=-8, squash=.9, spin=9)
    tx = wx + 290
    b += d.text(track, tx, wy + 88, 28, ink, font=BOLD, tracking=-.6, max_w=420)["svg"]
    b += d.text(artist, tx, wy + 114, 15, mute, font=MED)["svg"]
    b += d.label("320KBPS", wx + ww - 24, wy + 62, 9.5, mute, anchor="end", tracking=1.6)
    # live waveform
    b += d.eq(tx, wy + 158, 36, 9.4, 46, col=acc if c["name"] == "dark" else "#5b61b8", w=3.4)
    # progress
    py = wy + 208
    pw = 360
    b += f'<rect x="{tx}" y="{py - 3}" width="{pw}" height="6" rx="3" fill="{c["line"]}" fill-opacity="{.18 if c["name"] == "dark" else .6}"/>'
    d.k("@keyframes prog{from{transform:scaleX(0)}to{transform:scaleX(1)}}.prog{transform-box:fill-box;transform-origin:left;animation:prog 36s linear infinite}")
    b += f'<rect class="prog" x="{tx}" y="{py - 3}" width="{pw}" height="6" rx="3" fill="url(#holo)"/>'
    b += f'<circle r="7" cy="{py}" fill="#fff" stroke="{acc}" stroke-width="2"><animate attributeName="cx" values="{tx};{tx + pw}" dur="36s" repeatCount="indefinite"/></circle>'
    b += d.label("0:00", tx, py + 24, 9.5, mute) + d.label("PLAYING", tx + pw, py + 24, 9.5, mute, anchor="end")
    # controls
    kx = tx + pw + 60
    b += (f'<g fill="none" stroke="{ink}" stroke-width="1.8" stroke-linejoin="round"><path d="M{kx - 34} {py - 10}v20M{kx - 22} {py - 10}l-12 10 12 10z"/><path d="M{kx + 70} {py - 10}v20M{kx + 58} {py - 10}l12 10 -12 10z"/></g>')
    b += f'<circle cx="{kx + 18}" cy="{py}" r="22" fill="url(#holo)" stroke="#fff" stroke-width="1.6" class="pulse"/><path d="M{kx + 12} {py - 9}l16 9 -16 9z" fill="#0a0b1f"/>'
    b += d.button(wx + ww - 24 - 216, wy + 136, 216, 44, "LISTEN ON SPOTIFY", 12.5)
    b += _sparkles(d, [(46, 40, 9), (960, 300, 9), (990, 110, 8)])
    b += d.flare(wx + 262, wy + 38, 8, "#ffb48a", 2)
    b += d.frame()
    return d.render(b)


# ═══════════════════════════ FOOTER ═══════════════════════════
def footer(c):
    H = 420
    d = Doc(c, H, "Thank you for visiting")
    b = d.backdrop([(120, 340, 320, 140, "#7ee8ff"), (880, 330, 320, 140, "#c28bff"), (500, 120, 360, 120, "#ff8fe0")])
    ink, mute = c["ink"], c["mute"]
    b += d.chrome_blob(96, 84, 24, seed=9, dur=10) + d.chrome_blob(936, 240, 24, seed=12, dur=9)
    b += d.chrome("THANK YOU", W / 2, 236, 190, xs=1.12, max_w=860)
    b += "".join(d.bubble(x, y, r, delay=i * 1.7, dur=9 + i) for i, (x, y, r) in enumerate([(160, 280, 16), (850, 290, 13), (500, 320, 9), (260, 90, 10), (760, 70, 12)]))
    b += d.chrome_star(W - 70, 70, 18)
    b += d.barcode(MX, 300, 120, 34, seed=5, col=ink)
    b += d.label("JAVOHIR ABDUVAHHOBOV", MX, 358, 9.5, ink, tracking=1.6) + d.label("DS.2026 / SYSTEMATIC VISUAL LANGUAGE", MX, 374, 9, mute, tracking=1.4)
    b += d.label("THE AESTHETIC OF A DIGITAL DREAM.", W - MX, 322, 10.5, ink, anchor="end", tracking=2)
    b += d.label("2026 — ∞", W - MX, 344, 10.5, mute, anchor="end", tracking=2)
    b += d.ticker(MX, 396, W - 2 * MX, "CRAFTED WITH INTENT + THANK YOU FOR VISITING + CRAFTED WITH INTENT", 10, 36, mute)
    b += _sparkles(d, [(220, 70, 11), (700, 330, 10), (960, 230, 9), (40, 250, 9), (400, 340, 8)])
    b += d.flare(330, 120, 10, "#ffb48a", 1) + d.flare(680, 90, 9, "#8fd0ff", 2.4)
    b += d.frame()
    return d.render(b)
