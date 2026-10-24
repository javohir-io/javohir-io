# -*- coding: utf-8 -*-
"""The six HUD panels, laid out like a cyber-poster: katakana caption, hollow headline, angular frame,
blue label bars with Japanese text, vertical side text, barcode / INT.SYS footer row."""
from common import (W, M, BG, INK, PH, PHD, WHITE, BLUE, BLUE_DK, BOLD, MONO, PIX, JP, Doc, wrap)

EMAIL = "javohirabduvahhobov@gmail.com"
ROLES = ["FLUTTER DEVELOPER", "NODE.JS BACKEND ENGINEER", "REACT & TYPESCRIPT DEVELOPER", "SOFTWARE ENGINEER"]
FW = W - 2 * M - 36          # frame width: leaves a gutter on the right for the vertical Japanese text
VX = W - M - 12              # x of that vertical text
SUMMARY = ("Full-stack and mobile engineer who ships the entire pipeline — Flutter on the client, a Node.js / Express "
           "REST API in the middle, PostgreSQL underneath, and a lightweight admin panel wired to it all.")


def caption(d, jp, y=48):
    return d.glowg(d.jp(jp, W / 2, y, 13, INK, "middle", 4))


# ═══════════════════════════ HERO ═══════════════════════════
def hero():
    H = 1012
    d = Doc(H, "Javohir Abduvahhobov — Full-stack & mobile engineer")
    b = d.backdrop() + caption(d, "ジャヴォヒル・アブドゥヴァッホボフ")
    o1, _ = d.outline("JAVOHIR", W / 2, 222, 200, xs=1.3, sw=1.8, max_w=W - 2 * M)
    s2, _ = d.solid("ABDUVAHHOBOV", W / 2, 298, 80, xs=1.3, max_w=W - 2 * M)
    b += o1 + s2

    vx, vy, vw, vh = M, 346, FW, 280
    b += d.halftone(vx + 14, vy + 14, vw - 28, vh - 28)
    b += d.hud(vx, vy, vw, vh, cut=28)
    b += d.mono("ACTIVE SESSION", vx + vw - 98, vy - 12, 8.5, PH, anchor="end", tracking=1.8) + d.jp("オンライン", vx + vw - 88, vy - 8, 10, PH)
    b += f'<circle cx="{vx + vw}" cy="{vy}" r="3.4" fill="{BG}" stroke="{WHITE}" stroke-width="1.3"/>'
    b += d.vjp("フルスタック開発者", VX, vy + vh / 2, 15)
    b += d.hatch(vx + 44, vy + 24, 4) + d.hatch(vx + 44, vy + vh - 30, 4)
    b += d.mono("SCANNING IN PROGRESS", vx + 44, vy + 58, 10, WHITE, tracking=1.8) + d.jp("スキャン中", vx + 250, vy + 62, 11, WHITE)
    b += d.glowg(d.counter(vx + 44, vy + 84, 18, WHITE))
    b += f'<rect x="{vx + 44}" y="{vy + 96}" width="200" height="6" fill="none" stroke="{WHITE}" stroke-opacity=".8"/>'
    b += f'<rect x="{vx + 46}" y="{vy + 98}" width="196" height="2" fill="{WHITE}"><animate attributeName="width" values="0;196;196" keyTimes="0;.96;1" dur="12s" repeatCount="indefinite"/></rect>'
    cx, cy, cw, ch = vx + 44, vy + 140, 500, 84
    b += d.box(cx, cy, cw, ch, WHITE, .9, 1.2, fill=BG) + d.label_bar(cx, cy - 12, 150, "役割", "ROLE.EXE")
    d.k("@keyframes role{0%{opacity:0}3%{opacity:1}23%{opacity:1}26%,100%{opacity:0}}.role{opacity:0;animation:role 12s steps(1,end) infinite}")
    for i, r in enumerate(ROLES):
        t = d.text("> " + r, cx + 24, cy + 52, 22, INK, PIX, tracking=1, max_w=cw - 70)
        b += f'<g class="role" style="animation-delay:{i * 3}s">{d.glowg(t["svg"])}</g>'
    b += d.cursor(cx + cw - 36, cy + 34, 22, 12, WHITE)
    px = vx + vw - 280
    b += d.box(px, vy + 100, 250, 62, WHITE, .8, 1.1, fill=BG)
    for i, (k, v) in enumerate([("MOBILE", "FLUTTER"), ("BACKEND", "NODE.JS"), ("DATA", "POSTGRESQL")]):
        b += d.mono(k, px + 14, vy + 123 + i * 15, 9.5, PH, tracking=1.6) + d.mono(v, px + 236, vy + 123 + i * 15, 9.5, WHITE, anchor="end", tracking=1.6, bold=True)
    b += d.code_box(vx + vw - 280, vy + vh - 64, "2026", ["SEC - FS", "ACM 004 - ROLE", "STATUS - ONLINE"])

    # chunky word + paragraph, like FLEX
    b += d.arrow_nw(M, 668, 22)
    sv, _ = d.solid("DEV", M + 34, 800, 170, xs=1.3, anchor="start", max_w=430)
    b += sv
    b += d.para(SUMMARY, 520, 686, 408, 9.5, 16)
    # label-bar columns + stacked outline
    for x, jp, en, txt in ((M, "モバイル", "MOBILE", "Flutter client with Dart, http, shared_preferences and file_picker."),
                           (M + 268, "バックエンド", "BACKEND", "Node.js and Express REST API with JWT auth, bcryptjs and multer uploads.")):
        b += d.label_bar(x, 852, 236, jp, en) + d.bullets(x, 888) + d.para(txt, x, 922, 236, 8.5, 13)
    o2, _ = d.outline("FULL", 600, 902, 74, xs=1.3, sw=1.5, anchor="start", max_w=328)
    o3, _ = d.outline("STACK", 600, 972, 74, xs=1.3, sw=1.5, anchor="start", max_w=328)
    b += o2 + o3
    b += d.crt()
    return d.render(b)


# ═══════════════════════════ PROFILE ═══════════════════════════
def profile():
    H = 750
    d = Doc(H, "Profile — subject record")
    b = d.backdrop() + caption(d, "対象者記録")
    o, _ = d.outline("PROFILE", W / 2, 192, 150, xs=1.3, sw=1.8, max_w=760)
    b += o
    fy, rh = 232, 42
    rows = [("NAME", "JAVOHIR ABDUVAHHOBOV"), ("FUNCTION", "FULL-STACK & MOBILE ENGINEER"), ("DEGREE", "BSC SOFTWARE ENGINEERING"),
            ("DISCIPLINES", "MOBILE, BACKEND, DB, ADMIN"), ("STACK", "FLUTTER / NODE.JS / POSTGRESQL"), ("STATUS", "OPEN TO OPPORTUNITIES"), ("REPLY TIME", "WITHIN A DAY")]
    fh = rh * len(rows) + 24
    b += d.hud(M, fy, FW, fh, cut=26) + d.vjp("プロフィール", VX, fy + fh / 2, 15)
    b += d.hatch(M + FW - 96, fy + 10, 4)
    txt = ""
    for i, (k, v) in enumerate(rows):
        yy = fy + 12 + i * rh
        if i:
            b += f'<path d="M{M + 24} {yy}H{M + FW - 24}" stroke="{WHITE}" stroke-opacity=".35"/>'
        txt += d.pix(k, M + 28, yy + 28, 15, PH) + d.pix(v, M + FW - 28, yy + 28, 15, INK, anchor="end", max_w=560)
    b += d.glowg(txt)
    by = fy + fh + 44
    b += d.label_bar(M, by, 270, "概要", "SUMMARY") + d.bullets(M, by + 38) + d.para(SUMMARY, M, by + 72, 520, 9.5, 16)
    wx = 610
    b += d.label_bar(wx, by, 140, "信号", "SIGNAL") + d.wave(wx, by + 34, FW + M - wx, 96, 16)
    b += d.crt()
    return d.render(b)


# ═══════════════════════════ ARCHITECTURE ═══════════════════════════
def ecosystem():
    H = 650
    d = Doc(H, "Architecture — Flutter app, Express API, PostgreSQL, admin panel, Docker")
    b = d.backdrop() + caption(d, "システム構成")
    o, _ = d.outline("END TO END", W / 2, 172, 110, xs=1.3, sw=1.7, max_w=720)
    b += o

    def node(x, y, w, h, jp, en, title, sub, bw=170):
        o = d.box(x, y, w, h, WHITE, .95, 1.3, fill=BG) + d.label_bar(x, y - 12, bw, jp, en)
        return o + d.glowg(d.pix(title, x + 18, y + 56, 20, WHITE)) + d.mono(sub, x + 18, y + 82, 9.5, PH, tracking=1.2)

    b += d.hud(300, 236, 628, 350, cut=24, col=PH, sw=1.2, cuts="tr,bl") + d.label_bar(330, 225, 150, "コンテナ", "DOCKER")
    b += d.vjp("パイプライン", VX, 411, 15)
    b += node(M, 300, 220, 112, "クライアント", "CLIENT", "FLUTTER APP", "DART, HTTP, FILE_PICKER", 178)
    b += node(330, 280, 250, 112, "サーバー", "API", "EXPRESS API", "JWT, BCRYPTJS, MULTER", 150)
    b += node(660, 280, 240, 112, "データ", "DATA", "POSTGRESQL", "USERS, JOBS, INTERVIEWS", 150)
    b += node(330, 450, 250, 100, "管理", "ADMIN", "ADMIN PANEL", "HTML, CSS, JAVASCRIPT", 150)
    for pid, path, lab, lx, ly, dur, dl in (("l1", "M256 346H330", "JWT", 293, 334, 2.4, 0), ("l2", "M580 336H660", "PG", 620, 324, 1.8, .5), ("l3", "M455 392V450", "REST", 480, 426, 1.5, .2)):
        b += f'<path id="{pid}" d="{path}" fill="none" stroke="{WHITE}" stroke-opacity=".85" stroke-dasharray="4 5"/>'
        b += d.packet(pid, path, dur, dl) + d.mono(lab, lx, ly, 9, WHITE, anchor="middle" if lab != "REST" else "start", tracking=1.4, bold=True)
    b += d.box(660, 450, 240, 100, PH, .6) + d.label_bar(660, 438, 150, "ネットワーク", "NET") + d.wave(668, 466, 224, 76, 14)
    b += d.crt()
    return d.render(b)


# ═══════════════════════════ STACK ═══════════════════════════
STACK = [
    ("モバイル", "MOBILE", "FLUTTER APP", ["Flutter", "Dart", "http", "shared_preferences", "file_picker", "google_fonts", "intl", "cupertino_icons"]),
    ("バックエンド", "BACKEND", "NODE.JS API", ["Node.js", "Express", "JWT", "bcryptjs", "multer", "cors", "morgan", "dotenv", "uuid", "pg"]),
    ("データベース", "DATABASE", "RELATIONAL", ["PostgreSQL"]),
    ("管理パネル", "ADMIN", "LIGHTWEIGHT WEB", ["HTML", "CSS", "JavaScript"]),
    ("フロントエンド", "FRONTEND", "LANGUAGES", ["React", "TypeScript", "Python"]),
    ("ツール", "TOOLING", "DEV WORKFLOW", ["npm", "Git", "GitHub", "Docker"]),
]


def stack():
    X0, X1, TS, TP = 316, M + FW - 24, 11.5, 22
    plans, ys, y = [], [], 244
    for _, _, _, items in STACK:
        rows, cur = [[]], 0
        for t in items:
            w = MONO.width(t, TS, .8) + TP
            if rows[-1] and cur + 8 + w > X1 - X0:
                rows.append([])
                cur = 0
            cur += (8 if rows[-1] else 0) + w
            rows[-1].append((t, w))
        h = max(70, 28 + len(rows) * 34)
        plans.append(rows)
        ys.append((y, h))
        y += h
    H = int(y + 44)
    d = Doc(H, "Stack — Flutter, Node.js, PostgreSQL, React, TypeScript, Docker")
    b = d.backdrop() + caption(d, "技術スタック")
    o, _ = d.outline("STACK", W / 2, 178, 150, xs=1.3, sw=1.8, max_w=640)
    b += o
    b += d.hud(M, 220, FW, y - 220 + 14, cut=26) + d.vjp("開発ツール", VX, (220 + y + 14) / 2, 15)
    for i, ((jp, en, sub, _), rows, (yy, h)) in enumerate(zip(STACK, plans, ys)):
        if i:
            b += f'<path d="M{M + 24} {yy + 7}H{M + FW - 24}" stroke="{PH}" stroke-opacity=".3"/>'
        b += (f'<rect x="{M + 6}" y="{yy + 16}" width="4" height="{h - 28}" fill="{BLUE}" opacity="0"><animate attributeName="opacity" values="0;1;1;0;0" '
              f'keyTimes="0;.02;.14;.16;1" dur="12s" begin="{i * 2}s" repeatCount="indefinite"/></rect>')
        b += d.label_bar(M + 24, yy + 22, 214, jp, en) + d.mono(sub, M + 24, yy + 62, 8.5, PHD, tracking=1.6)
        for ri, row in enumerate(rows):
            x, ty = X0, yy + 22 + ri * 34
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
    H = 470
    d = Doc(H, f"Contact — {EMAIL}")
    b = d.backdrop() + caption(d, "連絡先")
    o, _ = d.outline("CONNECT", W / 2, 188, 130, xs=1.3, sw=1.8, max_w=760)
    b += o
    tx, ty, tw, th = M, 232, FW, 196
    b += d.hud(tx, ty, tw, th, cut=26) + d.label_bar(tx + 30, ty - 12, 190, "ターミナル", "TERMINAL") + d.vjp("接続中", VX, ty + th / 2, 15)
    b += d.glowg(d.pix("> OPENING CHANNEL ........ OK", tx + 30, ty + 58, 14, PH) + d.pix("> TARGET:", tx + 30, ty + 104, 14, PH)
                 + d.pix(EMAIL, tx + 150, ty + 108, 30, WHITE, max_w=tw - 190) + d.pix("> STATUS: AVAILABLE FOR OPPORTUNITIES", tx + 30, ty + 152, 14, PH))
    b += d.cursor(tx + 30 + PIX.width("> STATUS: AVAILABLE FOR OPPORTUNITIES", 14, 1) + 10, ty + 139, 16, 9, WHITE)
    bx, by, bw, bh = tx + tw - 292, ty + th - 64, 262, 46
    b += d.button(bx, by, bw, bh, "") + d.jp("メッセージを送る", bx + 22, by + 29, 14, "#ffffff")
    b += f'<path d="M{bx + bw - 34} {by + 31}l12 -12m-10 0h10v10" fill="none" stroke="#fff" stroke-width="2"/>'
    b += d.jp("1日以内に返信", bx + bw, by - 10, 10, PH, anchor="end") + d.hatch(tx + tw - 90, ty + 18, 4)
    b += d.crt()
    return d.render(b)


# ═══════════════════════════ FOOTER ═══════════════════════════
def footer():
    H = 370
    d = Doc(H, "Thank you for visiting")
    b = d.backdrop() + caption(d, "ご覧いただきありがとうございます")
    o, _ = d.outline("THANK YOU", W / 2, 214, 180, xs=1.3, sw=1.8, max_w=W - 2 * M)
    b += o
    by = 276
    b += d.pill(M, by, 126, 34, "W-2026", 14) + d.mono("JAVOHIR ABDUVAHHOBOV", M, by + 58, 8.5, PH, tracking=1.6)
    b += d.barcode(392, by, 216, 34, 7) + d.mono("SERIAL NO.", 392, by + 50, 8, PHD, tracking=1.4) + d.mono("JA-2026-0001", 608, by + 50, 8, PHD, anchor="end", tracking=1.4)
    rx = W - M
    for i, (jp, en) in enumerate((("対象を検出", "TARGET DETECTED"), ("プロトコル開始", "INITIATE PROTOCOL"))):
        yy = by + 10 + i * 18
        b += d.jp(jp, rx, yy, 10, PH, anchor="end") + d.mono(en, rx - JP.width(jp, 10, .5) - 12, yy, 8, PHD, anchor="end", tracking=1.6)
    b += d.tab(rx - 112, by + 40, 90, "INT.SYS", 22, 10)
    b += d.box(rx - 16, by + 45, 14, 14, WHITE, .9, 1.3)
    b += d.crt()
    return d.render(b)
