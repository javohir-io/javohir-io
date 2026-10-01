# -*- coding: utf-8 -*-
"""One palette, taken from the reference: near-black, crimson, marble silver."""

RED = dict(
    name="red",
    bg="#050405", bg2="#0C0709", panel="#0A0607",
    red="#E5161F", red2="#FF3A43", red3="#7E0C13", redline="#3A0A0F",
    text="#F1F1F1", text2="#A3A3A3", text3="#6C6C6C", silver="#CFCFCF",
    good="#E5161F",
    name_stops=[(0, "#FFFFFF"), (0.32, "#D6D6D6"), (0.52, "#8A8A8A"), (0.74, "#E9E9E9"), (1, "#9D9D9D")],
    band="#FFFFFF", band_op=0.7,
)
THEMES = {"red": RED}
