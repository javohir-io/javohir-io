# -*- coding: utf-8 -*-
import typo
from kit import (Ctx, frame, border, rosette, dial, sq, hair, fade_line, ticks_v, cross, chamfer, paragraph, gt, W)

# Trimmed to what matters. Bright = what I reach for most.
STACK = [
    ("LANGUAGES", ["Dart", "Python", "JavaScript", "Kotlin", "Java", "C"]),
    ("MOBILE AND WEB", ["Flutter", "Jetpack Compose", "HTML and CSS"]),
    ("BACKEND", ["FastAPI", "Node.js", "Express", "WebSockets"]),
    ("DATA", ["PostgreSQL", "SQLite"]),
    ("CLOUD AND DEVOPS", ["Docker", "GitHub Actions", "Google Cloud", "Render", "Netlify"]),
    ("IOT AND DESIGN", ["ESP32", "MQTT", "OpenCV", "Figma"]),
]
PRIMARY = {"Dart", "Python", "JavaScript", "Flutter", "FastAPI", "Node.js", "PostgreSQL"}


def stack_svg(c):
    x = Ctx(c, "sk", 500, title="Technical stack", desc="Languages, mobile, backend, data, cloud and IoT tools. Bright entries are the ones I reach for most.")
    u = x.uid
    x.css(f"@keyframes dr{u}{{from{{transform:scaleX(0)}}}}.dr{u}{{transform-box:view-box;transform-origin:76px 0;animation:dr{u} 1.3s cubic-bezier(.2,.7,.2,1) both}}"
          f"@keyframes bl{u}{{from{{opacity:.5}}to{{opacity:1}}}}.bl{u}{{animation:bl{u} 3.2s ease-in-out infinite alternate}}")
    parts = [x.t("The toolbox", 76, 92, 38, c["text"], "serif"),
             x.t("BRIGHT MARKS WHAT I REACH FOR MOST", W - 76, 88, 11, c["text3"], "sansm", anchor="end", ls=2.6)]
    y, vx = 128, 316
    for gi, (label, items) in enumerate(STACK):
        parts.append(f'<rect class="dr{u}" x="76" y="{y}" width="{W-152}" height="1" fill="{c["gold"]}" fill-opacity="0.35" style="animation-delay:{gi*0.1:.2f}s"/>')
        parts.append(x.t(label, 76, y + 42, 12, gt(c), "sansm", ls=3))
        cx = 316
        for it in items:
            prim = it in PRIMARY
            if prim:
                parts.append(f'<rect class="bl{u}" x="{cx}" y="{y+29}" width="8" height="8" fill="{gt(c)}" style="animation-delay:-{(gi*7+len(it))%30/10:.1f}s"/>')
                tx = cx + 16
            else:
                tx = cx
            parts.append(x.t(it, tx, y + 42, 17, c["text"] if prim else c["text2"], "serif" if prim else "sans"))
            cx = tx + x.w_(it, "serif" if prim else "sans", 17) + 34
        y += 58
    parts.append(f'<rect class="dr{u}" x="76" y="{y}" width="{W-152}" height="1" fill="{c["gold"]}" fill-opacity="0.35" style="animation-delay:.7s"/>')
    x.h = int(y + 56)
    body = "\n".join([frame(x), *parts, cross(76, 52, 6, c["gold"], .6), border(x)])
    return x.render(body)


def philosophy_svg(c):
    h = 290
    x = Ctx(c, "ph", h, title="Build it. Understand it. Improve it.")
    u, cx = x.uid, W / 2
    phrases = ["Build it.", "Understand it.", "Improve it."]
    size, gap = 50, 44
    widths = [x.w_(p, "serif", size) for p in phrases]
    pos = cx - (sum(widths) + gap * 2) / 2
    base_y, cyc = 150, 9.0
    parts = []
    for i, (p, w) in enumerate(zip(phrases, widths)):
        a = i * 100 / 3
        x.css(f"@keyframes ph{u}{i}{{0%,{a:.1f}%{{opacity:0}}{a+4:.1f}%{{opacity:1}}{a+30:.1f}%{{opacity:1}}{min(a+34,100):.1f}%,100%{{opacity:0}}}}"
              f"@keyframes ul{u}{i}{{0%,{a:.1f}%{{transform:scaleX(0)}}{a+10:.1f}%{{transform:scaleX(1)}}{a+30:.1f}%{{transform:scaleX(1)}}{min(a+34,100):.1f}%,100%{{transform:scaleX(0)}}}}")
        parts.append(x.t(p, pos, base_y, size, c["text"], "serif", opacity=0.3))
        parts.append(x.t(p, pos, base_y, size, c["text"], "serif", style=f"animation:ph{u}{i} {cyc}s ease-in-out infinite"))
        parts.append(f'<rect x="{pos}" y="{base_y+18}" width="{w:.1f}" height="2" fill="{c["gold2"] if c["is_dark"] else c["gold"]}" style="transform-box:fill-box;transform-origin:left;animation:ul{u}{i} {cyc}s ease-in-out infinite"/>')
        pos += w + gap
    x.reduced.append(f"text[style*='ph{u}']{{opacity:1!important}}")
    body = "\n".join([
        frame(x),
        f'<g clip-path="url(#clip{u})">{rosette(x, cx, 150, 200, 26, 220, c["steel"], 0.11 if c["is_dark"] else 0.17)}</g>',
        x.t("PHILOSOPHY", cx, 60, 11.5, gt(c), "sansm", anchor="middle", ls=5),
        fade_line(x, cx - 60, cx + 60, 72, "t", 0.8),
        *parts,
        x.t("AI speeds me up. Understanding the code is still my job.", cx, 232, 16, c["text2"], "serifi", anchor="middle"),
        border(x)])
    return x.render(body)


def _contact(c, uid, kicker, main, sub, icon_fn, ttl, mail=False):
    h, w = 150, 490
    x = Ctx(c, uid, h, w=w, title=ttl)
    u = x.uid
    g = gt(c)
    size = 25
    while x.w_(main, "serif", size) > w - 150 and size > 15:
        size -= 1
    body = "\n".join([
        frame(x), icon_fn(x, g),
        x.t(kicker, 116, 62, 11.5, g, "sansm", ls=3),
        x.t(main, 116, 96, size, c["text"], "serif"),
        x.t(sub, 116, 122, 13, c["text3"], "sans", ls=0.3),
        border(x, chase=True)])
    return x.render(body)


def _mail_icon(x, g):
    c = x.c
    return (f'<polygon points="{chamfer(40, 52, 52, 38, 9)}" fill="{c["chip_fill"]}" stroke="{g}" stroke-width="1.6"/>'
            f'<path d="M41 55L66 74L91 55" fill="none" stroke="{g}" stroke-width="1.6" stroke-linejoin="round"/>')


def _git_icon(x, g):
    c = x.c
    return (f'<g fill="{c["chip_fill"]}" stroke="{g}" stroke-width="1.6"><rect x="48" y="46" width="12" height="12"/><rect x="48" y="96" width="12" height="12"/>'
            f'<rect x="78" y="62" width="12" height="12"/></g><g fill="none" stroke="{g}" stroke-width="1.6"><path d="M54 58V96"/><path d="M54 90Q54 72 78 68"/></g>'
            f'<rect x="-3" y="-3" width="6" height="6" fill="{c["gold2"]}"><animateMotion dur="2.8s" repeatCount="indefinite" path="M54 96V58"/></rect>')


def contact_email_svg(c):
    return _contact(c, "ce", "WRITE TO ME", "javohir.abduvahhobov@gmail.com", "Open your mail app", _mail_icon,
                    "Email Javohir at javohir.abduvahhobov@gmail.com")


def contact_github_svg(c):
    return _contact(c, "cg", "FOLLOW THE WORK", "github.com/javohir-io", "Projects, code and commits", _git_icon,
                    "Javohir on GitHub: github.com/javohir-io")
