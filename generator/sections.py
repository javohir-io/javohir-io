# -*- coding: utf-8 -*-
"""The seven HUD panels. Each builder returns an SVG string."""
import math
from common import (W, M, BG, INK, PH, PHD, WHITE, BLUE, BLUE_DK, BOLD, MONO, MONOB, PIX, Doc, wrap)

EMAIL = "javohirabduvahhobov@gmail.com"
ROLES = ["FLUTTER DEVELOPER", "NODE.JS BACKEND ENGINEER", "REACT & TYPESCRIPT DEVELOPER", "SOFTWARE ENGINEER"]


def top_bar(d, left, right, y=44):
    o = d.pix(left, M, y, 15, PH)
    o += d.pix(right, W - M - 22, y, 15, PH, anchor="end")
    o += f'<rect class="blink" x="{W - M - 12}" y="{y - 11}" width="12" height="12" fill="{PH}"/>'
    return d.glowg(o) + (f'<path d="M{M} {y + 16}H{W - M}" stroke="{PH}" stroke-opacity=".45"/>'
                          f'<circle cx="{M}" cy="{y + 16}" r="3.2" fill="{BG}" stroke="{PH}"/><circle cx="{W - M}" cy="{y + 16}" r="3.2" fill="{BG}" stroke="{PH}"/>')


# ═══════════════════════════ HERO ═══════════════════════════
def hero():
    H = 700
    d = Doc(H, "Javohir Abduvahhobov — Full-stack & mobile engineer")
    b = d.backdrop()
    b += top_bar(d, "SUBJECT: JAVOHIR.A", "STATUS: ONLINE")

    o1, r1 = d.outline("JAVOHIR", W / 2, 208, 200, xs=1.3, sw=1.8, max_w=W - 2 * M)
    b += o1
    s2, r2 = d.solid("ABDUVAHHOBOV", W / 2, 282, 80, xs=1.3, max_w=W - 2 * M)
    b += s2

    # the scan viewport
    vx, vy, vw, vh = M, 322, W - 2 * M, 270
    b += d.halftone(vx + 14, vy + 14, vw - 28, vh - 28)
    b += d.hud(vx, vy, vw, vh, cut=28)
    b += d.hatch(vx + 44, vy + 24, 4) + d.hatch(vx + 44, vy + vh - 30, 4)
    # scan status
    b += d.mono("SCANNING IN PROGRESS", vx + 44, vy + 56, 10, WHITE, tracking=1.8)
    b += d.glowg(d.counter(vx + 44, vy + 82, 18, WHITE))
    b += f'<rect x="{vx + 44}" y="{vy + 94}" width="200" height="6" fill="none" stroke="{WHITE}" stroke-opacity=".8"/>'
    b += f'<rect x="{vx + 46}" y="{vy + 96}" width="196" height="2" fill="{WHITE}"><animate attributeName="width" values="0;196;196" keyTimes="0;.96;1" dur="12s" repeatCount="indefinite"/></rect>'
    # role readout
    cx, cy, cw, ch = vx + 44, vy + 136, 520, 84
    b += d.box(cx, cy, cw, ch, WHITE, .9, 1.2, fill=BG)
    b += d.tab(cx, cy - 11, 74, "ROLE.EXE", 22)
    d.k("@keyframes role{0%{opacity:0}3%{opacity:1}23%{opacity:1}26%,100%{opacity:0}}.role{opacity:0;animation:role 12s steps(1,end) infinite}")
    cur_x = {}
    for i, r in enumerate(ROLES):
        t = d.text("> " + r, cx + 24, cy + 52, 22, INK, PIX, tracking=1, max_w=cw - 70)
        b += f'<g class="role" style="animation-delay:{i * 3}s" filter="url(#glow)">{t["svg"]}</g>'
    b += d.cursor(cx + cw - 36, cy + 34, 22, 12, WHITE)
    # right readout
    for i, (k, v) in enumerate([("MOBILE", "FLUTTER"), ("BACKEND", "NODE.JS"), ("DATA", "POSTGRESQL")]):
        yy = vy + vh - 78 + i * 20
        b += d.mono(k, vx + vw - 250, yy, 10.5, PH, tracking=1.6) + d.mono(v, vx + vw - 44, yy, 10.5, WHITE, anchor="end", tracking=1.6, bold=True)
    b += d.box(vx + vw - 120, vy + 40, 76, 34, WHITE, .9, fill=BG) + d.pix("2026", vx + vw - 82, vy + 63, 16, WHITE, anchor="middle")

    # bottom row
    by = 624
    b += f'<rect x="{M}" y="{by}" width="124" height="34" rx="17" fill="none" stroke="{WHITE}" stroke-opacity=".85" stroke-width="1.3"/>' + d.pix("W-2026", M + 62, by + 23, 14, WHITE, anchor="middle")
    b += d.barcode(400, by + 2, 200, 30, 4) + d.mono("SERIAL NO.", 400, by + 48, 8, PHD, tracking=1.4) + d.mono("JA-2026-0001", 600, by + 48, 8, PHD, anchor="end", tracking=1.4)
    b += d.mono("TARGET DETECTED", W - M - 150, by + 12, 8, PHD, tracking=1.6) + d.mono("OPEN FOR OPPORTUNITIES", W - M - 150, by + 26, 8, PH, tracking=1.2)
    b += d.tab(W - M - 150, by + 34, 150, "INT.SYS", 20, 9)
    b += d.crt()
    return d.render(b)


def _fingerprint(d, x, y, w, h):
    """Concentric broken rings with a scan line travelling over them."""
    cx, cy = x + w / 2, y + h / 2
    rings = ""
    for i in range(1, 15):
        rx, ry = 5 + i * 4.6, 8 + i * 6.2
        dash = f"{6 + (i * 7) % 11} {2 + (i * 5) % 6}"
        rings += f'<ellipse cx="{cx}" cy="{cy}" rx="{rx:.1f}" ry="{ry:.1f}" fill="none" stroke="{PH}" stroke-width="1.5" stroke-dasharray="{dash}" stroke-opacity="{.95 - i * .03:.2f}"/>'
    cid = d.uid("fp")
    d.d(f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}"/></clipPath>')
    scan = (f'<g clip-path="url(#{cid})"><rect x="{x}" y="{y}" width="{w}" height="3" fill="{WHITE}" opacity=".9">'
            f'<animate attributeName="y" values="{y};{y + h - 3};{y}" dur="4.5s" repeatCount="indefinite"/></rect></g>')
    return d.glowg(rings) + scan + d.corners(x + 8, y + 8, w - 16, h - 16, 16, PH)


# ═══════════════════════════ PROFILE ═══════════════════════════
def profile():
    H = 548
    d = Doc(H, "Profile — subject record")
    b = d.backdrop()
    b += top_bar(d, "SUBJECT RECORD", "PROFILE.DAT")
    # left column
    lx, lw = M, 252
    b += d.box(lx, 84, lw, 200, PH, .6) + _fingerprint(d, lx, 84, lw, 200)
    b += d.box(lx, 298, lw, 210, PH, .6) + d.tab(lx, 298, 84, "SUMMARY", 22)
    para = ("Full-stack and mobile engineer who ships the entire pipeline — Flutter on the client, a Node.js / Express "
            "REST API in the middle, PostgreSQL underneath, and a lightweight admin panel wired to it all.")
    for i, ln in enumerate(wrap(para.upper(), MONO, 10, lw - 32)):
        b += d.mono(ln, lx + 16, 346 + i * 17, 10, INK, tracking=.6)
    # record table
    tx, tw, rh = 310, W - M - 310, 44
    rows = [("NAME", "JAVOHIR ABDUVAHHOBOV"), ("FUNCTION", "FULL-STACK & MOBILE ENGINEER"), ("DEGREE", "BSC SOFTWARE ENGINEERING"),
            ("DISCIPLINES", "MOBILE, BACKEND, DB, ADMIN"), ("STACK", "FLUTTER / NODE.JS / POSTGRESQL"), ("STATUS", "OPEN TO OPPORTUNITIES"),
            ("REPLY TIME", "WITHIN A DAY")]
    b += d.box(tx, 84, tw, rh * len(rows), WHITE, .9, 1.3)
    txt = ""
    for i, (k, v) in enumerate(rows):
        yy = 84 + i * rh
        if i:
            b += f'<path d="M{tx} {yy}H{tx + tw}" stroke="{WHITE}" stroke-opacity=".5"/>'
        txt += d.pix(k, tx + 16, yy + 29, 15, PH) + d.pix(v, tx + tw - 16, yy + 29, 15, INK, anchor="end", max_w=tw - 190)
    b += d.glowg(txt)
    # oscilloscope
    wy = 84 + rh * len(rows) + 16
    b += d.wave(tx, wy, tw, 508 - wy) + d.tab(tx, wy, 70, "SIGNAL", 20, 9)
    b += d.hatch(tx + tw - 46, wy + 8, 4)
    b += d.crt()
    return d.render(b)


# ═══════════════════════════ ARCHITECTURE ═══════════════════════════
def ecosystem():
    H = 580
    d = Doc(H, "Architecture — Flutter app, Express API, PostgreSQL, admin panel, Docker")
    b = d.backdrop()
    b += top_bar(d, "SYSTEM MAP", "PIPELINE.SYS")
    o, _ = d.outline("END TO END", M, 160, 100, xs=1.3, sw=1.6, anchor="start", max_w=560)
    b += o

    def node(x, y, w, h, tab, title, sub):
        o = d.box(x, y, w, h, WHITE, .95, 1.3, fill=BG) + d.tab(x, y - 11, len(tab) * 8 + 24, tab, 22)
        o += d.glowg(d.pix(title, x + 18, y + 54, 20, WHITE)) + d.mono(sub, x + 18, y + 80, 9.5, PH, tracking=1.2)
        return o

    # docker frame
    b += d.hud(300, 206, W - M - 300, 340, cut=24, col=PH, sw=1.2, cuts="tr,bl")
    b += d.tab(330, 195, 96, "DOCKER", 22, 10, fill=BLUE_DK)
    b += node(M, 270, 220, 112, "CLIENT", "FLUTTER APP", "DART, HTTP, FILE_PICKER")
    b += node(330, 250, 250, 112, "API", "EXPRESS API", "JWT, BCRYPTJS, MULTER")
    b += node(690, 250, 250, 112, "DATA", "POSTGRESQL", "USERS, JOBS, INTERVIEWS")
    b += node(330, 420, 250, 100, "ADMIN", "ADMIN PANEL", "HTML, CSS, JAVASCRIPT")

    links = [("l1", "M256 316H330", "JWT", 293, 304, 2.4, 0), ("l2", "M580 306H690", "PG", 635, 294, 1.8, .5), ("l3", "M455 362V420", "REST", 480, 396, 1.5, .2)]
    for pid, path, lab, lx, ly, dur, dl in links:
        b += f'<path id="{pid}" d="{path}" fill="none" stroke="{WHITE}" stroke-opacity=".85" stroke-dasharray="4 5"/>'
        b += d.packet(pid, path, dur, dl) + d.mono(lab, lx, ly, 9, WHITE, anchor="middle" if lab != "REST" else "start", tracking=1.4, bold=True)
    b += d.box(690, 420, 250, 100, PH, .6) + d.tab(690, 409, 100, "NETWORK", 22, 10, fill=BLUE_DK) + d.wave(698, 438, 234, 74, 14)
    b += d.crt()
    return d.render(b)


# ═══════════════════════════ STACK ═══════════════════════════
STACK = [
    ("MOBILE", "FLUTTER APP", ["Flutter", "Dart", "http", "shared_preferences", "file_picker", "google_fonts", "intl", "cupertino_icons"]),
    ("BACKEND", "NODE.JS API", ["Node.js", "Express", "JWT", "bcryptjs", "multer", "cors", "morgan", "dotenv", "uuid", "pg"]),
    ("DATABASE", "RELATIONAL", ["PostgreSQL"]),
    ("ADMIN PANEL", "LIGHTWEIGHT WEB", ["HTML", "CSS", "JavaScript"]),
    ("FRONTEND", "LANGUAGES", ["React", "TypeScript", "Python"]),
    ("TOOLING", "DEV WORKFLOW", ["npm", "Git", "GitHub", "Docker"]),
]


def stack():
    X0, X1, TS, TP = 300, W - M, 11.5, 22
    plans, y, ys = [], 206, []
    for label, sub, items in STACK:
        rows, cur = [[]], 0
        for t in items:
            w = MONO.width(t, TS, .8) + TP
            if rows[-1] and cur + 8 + w > X1 - X0:
                rows.append([])
                cur = 0
            cur += (8 if rows[-1] else 0) + w
            rows[-1].append((t, w))
        h = max(64, 26 + len(rows) * 34)
        plans.append(rows)
        ys.append((y, h))
        y += h
    H = int(y + 40)
    d = Doc(H, "Stack — Flutter, Node.js, PostgreSQL, React, TypeScript, Docker")
    b = d.backdrop()
    b += top_bar(d, "TOOLS INDEX", "6 GROUPS")
    o, _ = d.outline("STACK", M, 168, 110, xs=1.3, sw=1.6, anchor="start", max_w=420)
    b += o
    b += d.hud(M, 190, W - 2 * M, y - 190 + 14, cut=22, col=WHITE, sw=1.3, cuts="tr,bl")
    for i, ((label, sub, _), rows, (yy, h)) in enumerate(zip(STACK, plans, ys)):
        if i:
            b += f'<path d="M{M} {yy + 7}H{W - M}" stroke="{PH}" stroke-opacity=".3"/>'
        b += (f'<rect x="{M + 6}" y="{yy + 16}" width="4" height="{h - 28}" fill="{BLUE}" opacity="0">'
              f'<animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;.02;.14;.16;1" dur="12s" begin="{i * 2}s" repeatCount="indefinite"/></rect>')
        b += d.glowg(d.pix(label, M + 22, yy + 36, 15, WHITE)) + d.mono(sub, M + 22, yy + 54, 9, PHD, tracking=1.6)
        for ri, row in enumerate(rows):
            x = X0
            ty = yy + 22 + ri * 34
            for ti, (t, w) in enumerate(row):
                if ri == 0 and ti == 0:
                    b += f'<rect x="{x}" y="{ty}" width="{w:.1f}" height="26" fill="{BLUE}"/>' + d.mono(t, x + TP / 2, ty + 17, TS, "#fff", tracking=.8, bold=True)
                else:
                    b += d.box(x, ty, w, 26, PH, .55) + d.mono(t, x + TP / 2, ty + 17, TS, INK, tracking=.8)
                x += w + 8
    b += d.crt()
    return d.render(b)


# ═══════════════════════════ CONTACT ═══════════════════════════
def contact():
    H = 440
    d = Doc(H, f"Contact — {EMAIL}")
    b = d.backdrop()
    b += top_bar(d, "CHANNEL", "OPEN")
    o, _ = d.outline("CONNECT", M, 168, 104, xs=1.3, sw=1.6, anchor="start", max_w=620)
    b += o
    tx, ty, tw, th = M, 196, W - 2 * M, 200
    b += d.hud(tx, ty, tw, th, cut=24, col=WHITE, sw=1.3) + d.tab(tx + 30, ty - 11, 96, "TERMINAL", 22)
    b += d.glowg(d.pix("> OPENING CHANNEL ........ OK", tx + 30, ty + 56, 14, PH)
                 + d.pix("> TARGET:", tx + 30, ty + 102, 14, PH)
                 + d.pix(EMAIL, tx + 150, ty + 106, 30, WHITE, max_w=tw - 190)
                 + d.pix("> STATUS: AVAILABLE FOR OPPORTUNITIES", tx + 30, ty + 150, 14, PH))
    b += d.cursor(tx + 30 + PIX.width("> STATUS: AVAILABLE FOR OPPORTUNITIES", 14, 1) + 10, ty + 137, 16, 9, WHITE)
    bx, by, bw, bh = tx + tw - 270, ty + th - 62, 240, 44
    b += d.button(bx, by, bw, bh, "SEND MESSAGE")
    b += f'<path d="M{bx + bw - 30} {by + 29}l12 -12m-10 0h10v10" fill="none" stroke="#fff" stroke-width="2"/>'
    b += d.mono("REPLY WITHIN A DAY", bx + bw, by - 10, 8.5, PHD, anchor="end", tracking=1.6)
    b += d.hatch(tx + tw - 90, ty + 18, 4)
    b += d.crt()
    return d.render(b)


# ═══════════════════════════ SOUNDTRACK ═══════════════════════════
def soundtrack(track="We Do What We Want (Edit)", artist="Alan Fitzpatrick"):
    H = 300
    d = Doc(H, f"Now playing — {track} by {artist}")
    b = d.backdrop()
    b += top_bar(d, "AUDIO.SYS", "NOW PLAYING")
    px, py, ps = M, 84, 190
    b += d.box(px, py, ps, ps, PH, .6)
    cx, cy = px + ps / 2, py + ps / 2
    disc = "".join(f'<circle cx="{cx}" cy="{cy}" r="{r}" fill="none" stroke="{PH}" stroke-width="1.3" stroke-dasharray="{2 + r % 5} {3 + r % 4}"/>' for r in range(20, 82, 6))
    disc += f'<circle cx="{cx}" cy="{cy}" r="82" fill="none" stroke="{WHITE}" stroke-width="1.6"/><path d="M{cx} {cy - 82}V{cy - 20}" stroke="{WHITE}" stroke-width="2"/><circle cx="{cx}" cy="{cy}" r="8" fill="{BLUE}" stroke="{WHITE}"/>'
    b += d.glowg(f'<g class="spin" style="animation-duration:9s">{disc}</g>') + d.corners(px + 6, py + 6, ps - 12, ps - 12, 14)
    tx = 270
    b += d.glowg(d.pix(track.upper(), tx, 128, 26, WHITE, max_w=W - M - tx - 10))
    b += d.mono(artist.upper(), tx, 154, 11, PH, tracking=2)
    b += d.eq(tx, 196, 44, 8.4, 34, col=PH, w=4)
    pw = 430
    b += f'<path d="M{tx} 250H{tx + pw}" stroke="{PH}" stroke-opacity=".4" stroke-width="2"/>'
    b += (f'<rect x="{tx}" y="249" width="{pw}" height="2" fill="{WHITE}" class="prog"/>'
          f'<rect x="-4" y="244" width="8" height="12" fill="{WHITE}"><animate attributeName="x" values="{tx - 4};{tx + pw - 4}" dur="36s" repeatCount="indefinite"/></rect>')
    d.k("@keyframes prog{from{transform:scaleX(0)}to{transform:scaleX(1)}}.prog{transform-box:fill-box;transform-origin:left;animation:prog 36s linear infinite}")
    b += d.mono("00:00", tx, 272, 8.5, PHD, tracking=1.4) + d.mono("320KBPS", tx + pw, 272, 8.5, PHD, anchor="end", tracking=1.4)
    b += d.button(W - M - 236, 224, 236, 44, "LISTEN ON SPOTIFY", 12)
    b += d.crt()
    return d.render(b)


# ═══════════════════════════ FOOTER ═══════════════════════════
def footer():
    H = 340
    d = Doc(H, "Thank you for visiting")
    b = d.backdrop()
    b += top_bar(d, "END OF FILE", "SESSION CLOSED")
    o, r = d.outline("THANK YOU", W / 2, 206, 180, xs=1.3, sw=1.8, max_w=W - 2 * M)
    b += o
    b += d.barcode(M, 250, 170, 30, 7) + d.mono("JAVOHIR ABDUVAHHOBOV", M, 298, 8.5, PH, tracking=1.6) + d.mono("SERIAL NO. JA-2026-0001", M, 312, 8, PHD, tracking=1.4)
    b += d.mono("THE AESTHETIC OF A DIGITAL DREAM.", W - M, 262, 9, PH, anchor="end", tracking=1.8) + d.mono("2026 // CRAFTED WITH INTENT", W - M, 278, 9, PHD, anchor="end", tracking=1.8)
    b += d.tab(W - M - 90, 288, 90, "INT.SYS", 20, 9)
    b += d.ticker(M + 200, 303, W - 2 * M - 420, "THANK YOU FOR VISITING", 9, 30)
    b += d.crt()
    return d.render(b)
