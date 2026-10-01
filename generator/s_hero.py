# -*- coding: utf-8 -*-
import math
from kit import (Ctx, frame, border, embers, ribbon, wave, label, image, hair, cross, fade_line, paragraph, silver_grad, W)


def icon(kind, x, y, c, s=1.0):
    """Simple 24px outline marks (drawn, not logos): flutter, python, js, node, postgres, docker."""
    st = f'fill="none" stroke="{c["silver"]}" stroke-width="1.4" stroke-linejoin="round" stroke-linecap="round"'
    g = {
        "flutter": '<path d="M14 2.5H20L9 13.5L5.8 10.3Z"/><path d="M14.2 13H20L14.2 18.8L11.2 21.8L8.2 18.8Z"/>',
        "python": '<path d="M4.5 12V7.5Q4.5 3.5 8.5 3.5H12.5Q16 3.5 16 7V10H8.5Q6.5 10 6.5 12Z"/><path d="M19.5 12V16.5Q19.5 20.5 15.5 20.5H11.5Q8 20.5 8 17V14H15.5Q17.5 14 17.5 12Z"/><circle cx="8.8" cy="6.6" r=".7"/><circle cx="15.2" cy="17.4" r=".7"/>',
        "js": '<rect x="3.5" y="3.5" width="17" height="17"/><path d="M9.5 10.5V15Q9.5 16.5 8 16.5Q7 16.5 6.6 15.8"/><path d="M17 11.2Q16.5 10.4 15.4 10.4Q14 10.4 14 11.6Q14 12.6 15.4 13.1Q17 13.6 17 14.8Q17 16.3 15.4 16.3Q14.2 16.3 13.6 15.4"/>',
        "node": '<path d="M12 2.5L20.2 7.2V16.8L12 21.5L3.8 16.8V7.2Z"/><path d="M9 15.8V8.4L15 15.6V8.4"/>',
        "postgres": '<ellipse cx="12" cy="6" rx="7" ry="2.8"/><path d="M5 6V18Q5 20.8 12 20.8Q19 20.8 19 18V6"/><path d="M5 12Q5 14.8 12 14.8Q19 14.8 19 12"/>',
        "docker": '<path d="M2.5 12.5H19.2Q21 12 21.8 10.6Q20.2 10 19.4 10.4Q19.2 8.6 17.8 8L17.4 8.8"/><path d="M2.5 12.5Q3 18.5 10.5 18.5Q17.5 18.5 19.2 12.5"/><rect x="5" y="9.5" width="2.6" height="2.4"/><rect x="8.2" y="9.5" width="2.6" height="2.4"/><rect x="11.4" y="9.5" width="2.6" height="2.4"/><rect x="8.2" y="6.6" width="2.6" height="2.4"/><rect x="11.4" y="6.6" width="2.6" height="2.4"/>',
    }[kind]
    return f'<g transform="translate({x} {y}) scale({s})" {st}>{g}</g>'


def header_svg(c):
    h = 600
    x = Ctx(c, "hd", h, title="Javohir Abduvahhobov, software developer",
            desc="Hero: the name in marble silver behind a red statue, with ribbons of light and the tools I build with.")
    u, cx = x.uid, 500

    # --- name ------------------------------------------------------------------------------
    A, B = "JAVOHIR", "ABDUVAHHOBOV"
    size = 120
    while x.w_(B, "disp", size, -1) > 872 and size > 40:
        size -= 1
    y1, y2 = 196, 196 + round(size * 0.94)
    fill = silver_grad(x, f"nm{u}")
    x.defs(f'''<linearGradient id="wipe{u}" gradientUnits="userSpaceOnUse" x1="1000" y1="0" x2="1300" y2="0"><stop offset="0" stop-color="#fff"/><stop offset="1" stop-color="#000"/>
  <animateTransform attributeName="gradientTransform" type="translate" from="-1320 0" to="0 0" dur="2.4s" calcMode="spline" keyTimes="0;1" keySplines="0.32 0 0.15 1" fill="freeze"/></linearGradient>
<mask id="wm{u}" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{h}"><rect width="{W}" height="{h}" fill="url(#wipe{u})"/></mask>
<linearGradient id="band{u}" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#fff" stop-opacity="0"/><stop offset="0.5" stop-color="#fff" stop-opacity="{c['band_op']}"/><stop offset="1" stop-color="#fff" stop-opacity="0"/></linearGradient>
<radialGradient id="halo{u}"><stop offset="0" stop-color="{c['red']}" stop-opacity="0.42"/><stop offset="0.6" stop-color="{c['red']}" stop-opacity="0.10"/><stop offset="1" stop-color="{c['red']}" stop-opacity="0"/></radialGradient>''')
    kw = dict(font="disp", anchor="middle", ls=-1)
    cxs = (cx + 38, cx)
    name_rim = x.t(A, cxs[0], y1, size, "none", **kw, extra=f'stroke="{c["red"]}" stroke-opacity="0.5" stroke-width="2.4"') + \
               x.t(B, cxs[1], y2, size, "none", **kw, extra=f'stroke="{c["red"]}" stroke-opacity="0.5" stroke-width="2.4"')
    name_fill = x.t(A, cxs[0], y1, size, fill, **kw) + x.t(B, cxs[1], y2, size, fill, **kw)
    name_mask = x.t(A, cxs[0], y1, size, "#fff", **kw) + x.t(B, cxs[1], y2, size, "#fff", **kw)
    x.defs(f'<mask id="tm{u}" maskUnits="userSpaceOnUse" x="0" y="0" width="{W}" height="{h}">{name_mask}</mask>')
    x.css(f"@keyframes sw{u}{{0%{{transform:translateX(-300px) skewX(-20deg)}}34%,100%{{transform:translateX(1200px) skewX(-20deg)}}}}.sw{u}{{animation:sw{u} 9s ease-in-out 3.2s infinite}}")
    shimmer = f'<g mask="url(#tm{u})"><rect class="sw{u}" x="0" y="{y1-size}" width="150" height="{size*2.1:.0f}" fill="url(#band{u})"/></g>'

    # --- statue ----------------------------------------------------------------------------
    x.css(f"@keyframes fl{u}{{from{{transform:translateY(0)}}to{{transform:translateY(-6px)}}}}.fl{u}{{animation:fl{u} 6s ease-in-out infinite alternate}}"
          f"@keyframes br{u}{{from{{opacity:.55}}to{{opacity:1}}}}.br{u}{{animation:br{u} 4.5s ease-in-out infinite alternate}}"
          f"@keyframes cm{u}{{from{{stroke-dashoffset:0}}to{{stroke-dashoffset:-1000}}}}.cm{u}{{animation:cm{u} 10s linear infinite}}")
    sw_, sx, sy = 570, 215, 176
    statue = f'<g class="fl{u}">{image("statue-hero.webp", sx, sy, sw_, round(sw_ * 493 / 640))}</g>'
    glow = f'<circle class="br{u}" cx="{cx}" cy="360" r="320" fill="url(#halo{u})"/>'
    ring = (f'<circle cx="{cx}" cy="292" r="236" fill="none" stroke="{c["red"]}" stroke-opacity="0.38"/>'
            f'<circle class="cm{u}" cx="{cx}" cy="292" r="236" fill="none" stroke="{c["red2"]}" stroke-width="1.8" pathLength="1000" stroke-dasharray="70 930" stroke-linecap="round"/>'
            f'<circle cx="{cx}" cy="292" r="262" fill="none" stroke="{c["silver"]}" stroke-opacity="0.07"/>')

    # --- ribbons -------------------------------------------------------
    ribbons = (ribbon(x, "M-10 200C120 150 250 80 420 -10", "a") + ribbon(x, "M-10 230C140 170 280 100 470 -10", "b", 2.5, 0.8)
               + ribbon(x, "M1010 350C940 430 900 520 850 612", "c", 4) + ribbon(x, "M1010 395C960 470 930 540 905 612", "d", 1.2, 0.8))
    # --- left column --------------------------------------------------------------------
    lx = 60
    tag = (x.t("Turning ideas", lx, 404, 25, c["text"], "sans") + x.t("into working", lx, 434, 25, c["text"], "sans")
           + x.t("software.", lx, 464, 25, c["red"], "sans"))
    para, _ = paragraph(x, "Building efficient, practical products across mobile, web, backend and IoT.", lx, 496, 250, 12.5, c["text3"], lh=20)
    icons = ["flutter", "python", "js", "node", "postgres", "docker"]
    box = f'<rect x="{lx}" y="540" width="278" height="46" fill="none" stroke="{c["silver"]}" stroke-opacity="0.22"/>'
    icos = "".join(icon(k, lx + 19 + i * 43, 551, c) for i, k in enumerate(icons))
    bar = f'<rect x="{lx-1}" y="360" width="1.6" height="108" fill="{c["red"]}"/>'

    # --- right column + top + bottom -----------------------------------------------------
    x.css(f"@keyframes sc{u}{{0%{{transform:translateY(0);opacity:0}}20%{{opacity:1}}80%{{opacity:1}}100%{{transform:translateY(34px);opacity:0}}}}.sc{u}{{animation:sc{u} 2.2s ease-in-out infinite}}")
    right = (f'<rect x="838" y="116" width="1.6" height="44" fill="{c["red"]}"/>'
             + x.t("IDEAS", 858, 126, 10, c["text2"], "sansm", ls=5) + x.t("CODE", 858, 143, 10, c["text2"], "sansm", ls=5) + x.t("REALITY", 858, 160, 10, c["text2"], "sansm", ls=5))
    scroll = (x.t("SCROLL", 0, 0, 9, c["text3"], "sansm", ls=4, extra=f'transform="translate(968 444) rotate(-90)"')
              + f'<rect x="967.5" y="456" width="1" height="46" fill="{c["red"]}" fill-opacity="0.4"/><rect class="sc{u}" x="966" y="456" width="4" height="4" fill="{c["red2"]}"/>')
    top = x.t("JA", lx - 2, 74, 44, c["text"], "disp")

    body = "\n".join([
        frame(x), f'<g clip-path="url(#clip{u})">{glow}{ring}</g>', ribbons,
        f'<g mask="url(#wm{u})">{name_rim}{name_fill}</g>', shimmer, statue,
        f'<g clip-path="url(#clip{u})">{embers(x, 28, 7, y0=80, rise=130)}</g>',
        bar, tag, para, box, icos, right, scroll, top,
        border(x),
    ])
    return x.render(body)
