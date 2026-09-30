# -*- coding: utf-8 -*-
"""Two palettes, one identity.

Dark  — "Midnight aubergine": deep plum ink, champagne gold, pearl text,
        with a faint iridescent (rose / lilac / aqua) glow borrowed from the soundtrack's mood.
Light — "Ivory atelier": warm paper, antique brass, plum-ink text, same iridescent accents.
"""

DARK = dict(
    name="dark",
    is_dark=True,
    bg="#0E0912", bg2="#1B1123", panel="#150D1C",
    gold="#D9BF8C", gold2="#F5E6C4", gold3="#9A7B45",
    text="#F3EDE4", text2="#BCB0C2", text3="#887D90",
    rose="#E9A3C0", lilac="#A88BEB", aqua="#7FD3CC",
    good="#84DBAA",
    chip_fill="#1E1428",
    name_stops=[(0, "#F9EFD6"), (0.5, "#FFFFFF"), (1, "#E6CC98")],
    band="#FFFFFF", band_op=0.85,
    aurora_op=0.20, spot_op=0.16,
    line_op=0.42, line2_op=0.16,
)

LIGHT = dict(
    name="light",
    is_dark=False,
    bg="#FBF6EE", bg2="#EFE6D6", panel="#FFFDF8",
    gold="#8F6D2D", gold2="#C9A45C", gold3="#6B4F1D",
    text="#241A2E", text2="#5E5169", text3="#7A6F85",
    rose="#C9709B", lilac="#7B5BC9", aqua="#3E9E97",
    good="#2E8B57",
    chip_fill="#FFFDF8",
    name_stops=[(0, "#3A2A4A"), (0.5, "#241A2E"), (1, "#5B3F6E")],
    band="#FFF3CF", band_op=0.95,
    aurora_op=0.16, spot_op=0.20,
    line_op=0.55, line2_op=0.22,
)

THEMES = {"light": LIGHT, "dark": DARK}
