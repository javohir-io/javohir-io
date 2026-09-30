# -*- coding: utf-8 -*-
import typo
from kit import (Ctx, frame, border, dust, sparkles, diamond, star4, fade_line, hair, chip,
                 paragraph, bullets, W)


def gt(c):
    return c["gold2"] if c["is_dark"] else c["gold"]


# ===========================================================================
STACK = [
    ("Languages", ["Dart", "Python", "JavaScript", "Kotlin", "Java", "C", "HTML", "CSS"]),
    ("Mobile and web", ["Flutter", "Flutter Web", "Material 3", "Jetpack Compose", "Android XML", "ChangeNotifier"]),
    ("Backend", ["FastAPI", "Node.js", "Express", "SQLAlchemy", "Pydantic", "Uvicorn", "REST APIs", "WebSockets", "Multer"]),
    ("Data", ["PostgreSQL", "SQLite", "SQL", "Neon", "Connection pooling", "Migrations"]),
    ("Auth and security", ["JWT", "bcrypt", "python-jose", "Role-based access", "Ownership checks"]),
    ("Cloud and DevOps", ["Docker", "Docker Compose", "GitHub Actions", "Google Cloud", "Render", "Netlify", "Cloudflare R2", "Git and GitHub"]),
    ("Testing", ["pytest", "FastAPI TestClient", "SQLite test databases", "CI on GitHub Actions"]),
    ("Design", ["Figma", "Canva", "Prototyping", "Design systems", "User flows"]),
    ("IoT and vision", ["ESP32", "Arduino", "PlatformIO", "MQTT", "OpenCV", "MediaPipe", "PCB design"]),
    ("Everyday tools", ["VS Code", "Android Studio", "Postman", "Trello", "Gantt charts"]),
]
PRIMARY = {"Dart", "Flutter", "Python", "JavaScript", "Node.js", "FastAPI", "PostgreSQL"}


def stack_svg(c):
    x = Ctx(c, "sk", 600, title="Technical stack",
            desc="Languages, mobile, backend, data, security, cloud, testing, design and IoT tools. Gold chips are the ones I reach for most.")
    u = x.uid
    x.css(f"@keyframes dr{u}{{from{{transform:scaleX(0)}}}}.dr{u}{{transform-origin:64px 0;transform-box:view-box;animation:dr{u} 1.4s cubic-bezier(.2,.7,.2,1) both}}")
    parts = [x.t("The toolbox", 64, 88, 36, c["text"], "serif"),
             x.t("Gold marks what I reach for most.", 64, 118, 18, gt(c), "serifi")]
    cx0, cx1 = 262, W - 64
    y = 146
    for gi, (label, items) in enumerate(STACK):
        rows, cx, ry = [], cx0, y + 20
        for it in items:
            prim = it in PRIMARY
            w = x.w_(it, "sansm", 13, 0.2) + 30 + (15 if prim else 0)
            if cx + w > cx1:
                cx, ry = cx0, ry + 40
            s, w = chip(x, cx, ry, it, primary=prim, h=30, size=13)
            rows.append(s)
            cx += w + 8
        parts.append(f'<rect class="dr{u}" x="64" y="{y}" width="{W-128}" height="1" fill="{c["gold"]}" fill-opacity="0.3" style="animation-delay:{gi*0.09:.2f}s"/>')
        parts.append(x.t(label, 64, y + 42, 20, c["text"], "serif"))
        parts += rows
        y = ry + 30 + 20
    x.h = int(y + 16)
    body = "\n".join([frame(x, r=6), f'<g clip-path="url(#clip{u})">{dust(x, 10, seed=71, rise=60, sizes=(0.6, 1.4))}</g>',
                      *parts, border(x, r=6)])
    return x.render(body)


# ===========================================================================
def focus_svg(c):
    x = Ctx(c, "fc", 520, title="Current focus and what I want to build")
    u = x.uid
    cols = [
        ("Sharpening now", ["Flutter and Dart", "Backend development", "REST API design", "PostgreSQL", "Software architecture",
                            "Testing", "Docker and cloud deployment", "System design", "Clean, maintainable code"]),
        ("Want to build", ["Full-stack applications", "Mobile applications", "Developer tools", "SaaS products", "Real-time applications",
                           "Cloud-connected applications", "IoT systems", "Automation", "AI-assisted applications"]),
        ("How I build", ["RESTful API design", "Repository pattern", "Service-based frontend architecture", "Authentication middleware",
                         "Environment-based configuration", "Reusable UI components", "Dockerized development", "Automated tests and CI"]),
    ]
    parts = [x.t("Where I'm heading", 64, 88, 36, c["text"], "serif"),
             x.t("Good UX, a reliable backend, real data, practical functionality.", 64, 120, 18, gt(c), "serifi")]
    colw, gap = 250, 61
    top = 170
    ends = []
    for i, (head, items) in enumerate(cols):
        cx = 64 + i * (colw + gap)
        parts.append(x.t(head, cx, top + 6, 24, c["text"], "serif"))
        parts.append(fade_line(x, cx, cx + 90, top + 22, f"h{i}", 0.9, both=False))
        b, ey = bullets(x, items, cx, top + 56, colw, cols=1, size=14, lh=28)
        parts.append(b)
        ends.append(ey)
        if i:
            vx = cx - gap / 2
            x.defs(f'<path id="vl{u}{i}" d="M{vx} {top-10} V{top+300}"/>')
            parts.append(f'<line x1="{vx}" y1="{top-10}" x2="{vx}" y2="{top+300}" stroke="{c["gold"]}" stroke-opacity="0.22"/>'
                         f'<circle r="2.2" fill="{c["gold2"]}"><animateMotion dur="{5+i}s" repeatCount="indefinite" keyPoints="0;1;0" keyTimes="0;.5;1" calcMode="linear"><mpath xlink:href="#vl{u}{i}"/></animateMotion></circle>')
    x.h = int(max(ends) + 34)
    body = "\n".join([frame(x, r=6), f'<g clip-path="url(#clip{u})">{dust(x, 10, seed=72, rise=60, sizes=(0.6, 1.4))}</g>',
                      *parts, sparkles(x, [(930, 70), (900, 130)], seed=9), border(x, r=6)])
    return x.render(body)


# ===========================================================================
def philosophy_svg(c):
    h = 380
    x = Ctx(c, "ph", h, title="Build it. Understand it. Improve it.")
    u, cx = x.uid, W / 2
    phrases = ["Build it.", "Understand it.", "Improve it."]
    size, gap = 46, 40
    widths = [x.w_(p, "serif", size) for p in phrases]
    total = sum(widths) + gap * 2
    px = cx - total / 2
    base_y = 160
    cyc = 9.0
    parts, pos = [], px
    for i, (p, w) in enumerate(zip(phrases, widths)):
        a = i * 100 / 3
        x.css(f"@keyframes ph{u}{i}{{0%,{a:.1f}%{{opacity:0}}{a+4:.1f}%{{opacity:1}}{a+30:.1f}%{{opacity:1}}{min(a+34,100):.1f}%,100%{{opacity:0}}}}"
              f"@keyframes ul{u}{i}{{0%,{a:.1f}%{{transform:scaleX(0)}}{a+10:.1f}%{{transform:scaleX(1)}}{a+30:.1f}%{{transform:scaleX(1)}}{min(a+34,100):.1f}%,100%{{transform:scaleX(0)}}}}")
        parts.append(x.t(p, pos, base_y, size, c["text"], "serif", opacity=0.34))
        parts.append(x.t(p, pos, base_y, size, c["text"], "serif", style=f"animation:ph{u}{i} {cyc}s ease-in-out infinite"))
        parts.append(f'<rect x="{pos}" y="{base_y+16}" width="{w:.1f}" height="2" fill="{c["gold2"]}" '
                     f'style="transform-box:fill-box;transform-origin:left;animation:ul{u}{i} {cyc}s ease-in-out infinite"/>')
        pos += w + gap
    x.reduced.append(f"text[style*='ph{u}']{{opacity:1!important}}")
    para = ("AI tools are part of my workflow: research, debugging, learning unfamiliar APIs. I still want to understand the "
            "architecture and decisions behind the code, so the goal is to move from making things work to knowing why they "
            "work and building them better.")
    p, _ = paragraph(x, para, cx, 240, 700, 15.5, c["text2"], lh=26, anchor="middle")
    body = "\n".join([frame(x, r=6), f'<g clip-path="url(#clip{u})">{dust(x, 16, seed=73, rise=80)}</g>',
                      fade_line(x, 300, 700, 52, "top", 0.6), x.t("Development philosophy", cx, 44, 13, gt(c), "sansm", anchor="middle", ls=2),
                      *parts, p, sparkles(x, [(120, 100), (880, 110), (200, 300), (800, 310)], seed=17), border(x, r=6)])
    return x.render(body)


# ===========================================================================
def _meter(x, mx, my, mw, fill, delay, segments=None, hot=None):
    c, u = x.c, x.uid
    if segments:
        seg_w = (mw - 5 * (segments - 1)) / segments if False else (mw - 5 * (segments - 1)) / segments
        out = []
        for i in range(segments):
            sx = mx + i * (seg_w + 5)
            lit = i < fill
            out.append(f'<rect x="{sx:.1f}" y="{my}" width="{seg_w:.1f}" height="6" rx="3" fill="{c["gold"]}" fill-opacity="0.16"/>')
            if lit:
                out.append(f'<rect class="mt{u}" x="{sx:.1f}" y="{my}" width="{seg_w:.1f}" height="6" rx="3" fill="{c["gold2"] if c["is_dark"] else c["gold"]}" '
                           f'style="animation-delay:{delay+i*0.12:.2f}s;transform-origin:{sx:.1f}px 0"/>')
        return "".join(out)
    return (f'<rect x="{mx}" y="{my}" width="{mw}" height="6" rx="3" fill="{c["gold"]}" fill-opacity="0.16"/>'
            f'<rect class="mt{u}" x="{mx}" y="{my}" width="{mw*fill:.1f}" height="6" rx="3" fill="{c["gold2"] if c["is_dark"] else c["gold"]}" '
            f'style="animation-delay:{delay:.2f}s;transform-origin:{mx}px 0"/>')


def credentials_svg(c):
    h = 500
    x = Ctx(c, "cr", h, title="Education and languages")
    u = x.uid
    x.css(f"@keyframes mt{u}{{from{{transform:scaleX(0)}}}}.mt{u}{{transform-box:view-box;animation:mt{u} 1.3s cubic-bezier(.2,.7,.2,1) both}}"
          f"@keyframes sr{u}{{to{{transform:rotate(360deg)}}}}.sr{u}{{transform-origin:112px 112px;animation:sr{u} 50s linear infinite}}")
    parts = []
    # seal
    sx, sy = 112, 112
    parts.append(f'<circle class="sr{u}" cx="{sx}" cy="{sy}" r="38" fill="none" stroke="{c["gold"]}" stroke-opacity="0.6" stroke-dasharray="1 6" stroke-linecap="round" stroke-width="2"/>')
    parts.append(f'<circle cx="{sx}" cy="{sy}" r="30" fill="{c["chip_fill"]}" stroke="{c["gold"]}" stroke-opacity="0.85"/>')
    g = c["gold2"] if c["is_dark"] else c["gold"]
    parts.append(f'<path d="M{sx} {sy-13} L{sx+20} {sy-3} L{sx} {sy+7} L{sx-20} {sy-3} Z" fill="none" stroke="{g}" stroke-width="1.6" stroke-linejoin="round"/>'
                 f'<path d="M{sx-11} {sy+1} V{sy+11} Q{sx} {sy+18} {sx+11} {sy+11} V{sy+1}" fill="none" stroke="{g}" stroke-width="1.6" stroke-linejoin="round"/>'
                 f'<path d="M{sx+20} {sy-3} V{sy+9}" stroke="{g}" stroke-width="1.6" stroke-linecap="round"/>')
    lx, lw = 64, 380
    parts.append(x.t("Education", lx, 200, 34, c["text"], "serif"))
    y = 240
    for ln in typo.wrap("Turin Polytechnic University in Tashkent", "serif", 23, lw):
        parts.append(x.t(ln, lx, y, 23, c["text"], "serif"))
        y += 30
    parts.append(x.t("Bachelor of Science, Software Engineering", lx, y + 4, 17, gt(c), "serifi"))
    p, _ = paragraph(x, "A foundation in software engineering, programming, databases, web and mobile development, computer networks, "
                        "IoT, software project management, UI/UX and system development.", lx, y + 38, lw, 14.5, c["text2"], lh=23)
    parts.append(p)

    # divider
    parts.append(f'<line x1="500" y1="60" x2="500" y2="{h-60}" stroke="{c["gold"]}" stroke-opacity="0.22"/>')
    x.defs(f'<path id="cv{u}" d="M500 60 V{h-60}"/>')
    parts.append(f'<circle r="2.2" fill="{c["gold2"]}"><animateMotion dur="6s" repeatCount="indefinite" keyPoints="0;1;0" keyTimes="0;.5;1" calcMode="linear"><mpath xlink:href="#cv{u}"/></animateMotion></circle>')

    # languages
    rx, rw = 556, 380
    parts.append(x.t("Languages", rx, 96, 34, c["text"], "serif"))
    rows = [
        ("Uzbek", "Native", dict(fill=1.0)),
        ("English", "Upper-intermediate, B2", dict(fill=4, segments=6)),
        ("Russian", "Full professional comprehension, limited speaking", None),
    ]
    ry = 148
    for i, (lang, level, meter) in enumerate(rows):
        parts.append(hair(rx, rx + rw, ry - 30, c["gold"], 0.28))
        parts.append(x.t(lang, rx, ry, 24, c["text"], "serif"))
        parts.append(x.t(level, rx + rw, ry - 1, 14, c["text2"], "sans", anchor="end") if meter else "")
        if meter:
            parts.append(_meter(x, rx, ry + 16, rw, meter["fill"], 0.2 + i * 0.35, segments=meter.get("segments")))
            if meter.get("segments"):
                for k, lab in enumerate(["A1", "A2", "B1", "B2", "C1", "C2"]):
                    seg_w = (rw - 25) / 6
                    parts.append(x.t(lab, rx + k * (seg_w + 5) + seg_w / 2, ry + 40, 11.5, c["gold"] if lab == "B2" else c["text3"],
                                     "sansm" if lab == "B2" else "sans", anchor="middle"))
            ry += 90
        else:
            parts.append(x.t("Understanding", rx, ry + 26, 13, c["text3"], "sans"))
            parts.append(_meter(x, rx + 108, ry + 20, rw - 108, 0.86, 0.9))
            parts.append(x.t("Speaking", rx, ry + 52, 13, c["text3"], "sans"))
            parts.append(_meter(x, rx + 108, ry + 46, rw - 108, 0.4, 1.1))
            parts.append(x.t("Full professional comprehension, limited speaking", rx, ry + 82, 13.5, c["text2"], "sans"))
            ry += 110
    fy = h - 54
    for ln in typo.wrap("Actively improving technical English: speaking and professional writing.", "serifi", 16.5, rw):
        parts.append(x.t(ln, rx, fy, 16.5, gt(c), "serifi"))
        fy += 24
    body = "\n".join([frame(x, r=6), f'<g clip-path="url(#clip{u})">{dust(x, 12, seed=74, rise=60, sizes=(0.6, 1.4))}</g>',
                      *parts, border(x, r=6)])
    return x.render(body)


# ===========================================================================
def contact_email_svg(c, email="javohir.abduvahhobov@gmail.com"):
    h, w = 150, 490
    x = Ctx(c, "ce", h, w=w, title=f"Email Javohir at {email}")
    u = x.uid
    x.css(f"@keyframes fl{u}{{0%,100%{{transform:rotate(0)}}50%{{transform:rotate(-4deg)}}}}.fl{u}{{transform-origin:66px 66px;animation:fl{u} 3.6s ease-in-out infinite}}")
    g = gt(c)
    icon = (f'<g class="fl{u}"><rect x="42" y="52" width="46" height="34" rx="4" fill="{c["chip_fill"]}" stroke="{g}" stroke-width="1.6"/>'
            f'<path d="M43 55 L65 72 L87 55" fill="none" stroke="{g}" stroke-width="1.6" stroke-linejoin="round"/></g>')
    size = 23
    while x.w_(email, "serif", size) > w - 158 and size > 15:
        size -= 1
    body = "\n".join([
        frame(x, r=6, aurora_cfg=[("aurL", 0.15, 0.2, 200, 22, 40, 20), ("aurR", 0.9, 0.9, 200, 26, -40, -20)]),
        f'<g clip-path="url(#clip{u})">{dust(x, 6, seed=81, rise=40)}</g>',
        icon,
        x.t("Write to me", 112, 62, 13, g, "sansm", ls=1.6),
        x.t(email, 112, 94, size, c["text"], "serif"),
        x.t("Open your mail app", 112, 122, 13, c["text3"], "sans"),
        border(x, r=6, chase=True),
    ])
    return x.render(body)


def contact_github_svg(c):
    h, w = 150, 490
    x = Ctx(c, "cg", h, w=w, title="Javohir on GitHub: github.com/javohir-io")
    u = x.uid
    g = gt(c)
    x.defs(f'<path id="gb{u}" d="M56 96 V60 Q56 52 64 52 H72"/>')
    icon = (f'<g fill="none" stroke="{g}" stroke-width="1.6" stroke-linecap="round">'
            f'<circle cx="56" cy="100" r="6" fill="{c["chip_fill"]}"/><circle cx="56" cy="50" r="6" fill="{c["chip_fill"]}"/>'
            f'<circle cx="86" cy="62" r="6" fill="{c["chip_fill"]}"/><path d="M56 56 V94"/><path d="M56 88 Q56 68 80 66"/></g>'
            f'<circle r="2.4" fill="{c["gold2"]}"><animateMotion dur="2.8s" repeatCount="indefinite" path="M56 94 V58"/></circle>'
            f'<circle r="2.4" fill="{c["rose"]}"><animateMotion dur="2.8s" begin="1.2s" repeatCount="indefinite" path="M56 88 Q56 68 80 66"/></circle>')
    body = "\n".join([
        frame(x, r=6, aurora_cfg=[("aurL", 0.85, 0.2, 200, 24, -40, 20), ("aurA", 0.1, 0.9, 200, 28, 40, -20)]),
        f'<g clip-path="url(#clip{u})">{dust(x, 6, seed=82, rise=40)}</g>',
        icon,
        x.t("Follow the work", 112, 62, 13, g, "sansm", ls=1.6),
        x.t("github.com/javohir-io", 112, 94, 25, c["text"], "serif"),
        x.t("Projects, code and commits", 112, 122, 13, c["text3"], "sans"),
        border(x, r=6, chase=True),
    ])
    return x.render(body)
