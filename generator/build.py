import os, sys
sys.path.insert(0, os.path.dirname(__file__))
from common import LIGHT, DARK
from sections import (header_svg, whoami_svg, ecosystem_svg, stack_svg,
                       transmission_svg, soundtrack_svg, footer_svg, divider_svg)

OUT_LIGHT = "/mnt/user-data/outputs/assets"
OUT_DARK = "/mnt/user-data/outputs/assets/dark"
os.makedirs(OUT_LIGHT, exist_ok=True)
os.makedirs(OUT_DARK, exist_ok=True)

SECTIONS = {
    "header.svg": header_svg,
    "whoami.svg": whoami_svg,
    "ecosystem.svg": ecosystem_svg,
    "stack.svg": stack_svg,
    "transmission.svg": transmission_svg,
    "footer.svg": footer_svg,
    "divider.svg": divider_svg,
}

for fname, fn in SECTIONS.items():
    light_svg = fn(LIGHT, "light")
    dark_svg = fn(DARK, "dark")
    with open(os.path.join(OUT_LIGHT, fname), "w") as f:
        f.write(light_svg)
    with open(os.path.join(OUT_DARK, fname), "w") as f:
        f.write(dark_svg)
    print("wrote", fname)

light_snd, snd_url = soundtrack_svg(LIGHT, "light")
dark_snd, _ = soundtrack_svg(DARK, "dark")
with open(os.path.join(OUT_LIGHT, "soundtrack.svg"), "w") as f:
    f.write(light_snd)
with open(os.path.join(OUT_DARK, "soundtrack.svg"), "w") as f:
    f.write(dark_snd)
print("wrote soundtrack.svg — link:", snd_url)

print("done")
