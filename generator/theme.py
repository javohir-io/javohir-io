# -*- coding: utf-8 -*-
"""Two palettes, one identity: horology + motorsport.

Dark  - "Obsidian": near-black with a racing-green undertone, titanium text, burnished bronze accent.
Light - "Bone & carbon": cool concrete paper, carbon-black text, deep bronze accent.
"""

DARK = dict(
    name="dark", is_dark=True,
    bg="#080B0C", bg2="#11171A", chip_fill="#0D1315",
    gold="#C39A5E", gold2="#EBCF9C", gold3="#8A6631",
    text="#EEF1EF", text2="#A9B3B7", text3="#758086",
    steel="#8FA6B4", emerald="#22896B", good="#46D19B",
    name_stops=[(0, "#B4BFC3"), (0.25, "#F6F8F7"), (0.5, "#D3DADC"), (0.75, "#FFFFFF"), (1, "#B4BFC3")],
    band="#FFFFFF", band_op=0.75,
    glow_op=0.20, spot_op=0.10, carbon_a=0.030, carbon_b=0.28,
    line_op=0.50, line2_op=0.16,
    ink="#0A0E0F",
)

LIGHT = dict(
    name="light", is_dark=False,
    bg="#EDEFEC", bg2="#DCE1DE", chip_fill="#F7F8F6",
    gold="#8A6229", gold2="#B98A44", gold3="#5F4218",
    text="#0E1416", text2="#424D52", text3="#627076",
    steel="#4F6878", emerald="#1D6B54", good="#1E9A6E",
    name_stops=[(0, "#2B3A40"), (0.5, "#0B1113"), (1, "#2B3A40")],
    band="#FFF4D6", band_op=0.95,
    glow_op=0.16, spot_op=0.30, carbon_a=0.05, carbon_b=0.0,
    line_op=0.60, line2_op=0.22,
    ink="#FFFFFF",
)

THEMES = {"light": LIGHT, "dark": DARK}
