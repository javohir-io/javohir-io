# -*- coding: utf-8 -*-
"""Cut the red statue out of its black backdrop (alpha from a cleaned mask) and export small WebP crops
that the SVGs embed as data URIs. Run once; build.py reads generator/img/*.webp."""
import io, os
import numpy as np
from PIL import Image
from scipy import ndimage as ndi

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "img", "statue-source.png")
OUT = os.path.join(HERE, "img")


def cutout():
    im = Image.open(SRC).convert("RGB")
    a = np.asarray(im).astype(np.float32)
    R = a[..., 0]
    h, w = R.shape
    # fitted backdrop glow: strongest top-left, fading right and down
    ys = np.array([0, 100, 200, 700, 900, 1050, h], dtype=np.float32)
    gs = np.array([74, 64, 56, 32, 22, 19, 18], dtype=np.float32)
    g = np.interp(np.arange(h), ys, gs)[:, None]
    bg = g * np.exp(-np.arange(w)[None, :] / 270.0) * 1.12
    m = R > bg + 16
    m = ndi.binary_closing(m, structure=np.ones((11, 11)), iterations=2)
    m = ndi.binary_fill_holes(m)
    # the face is in deep shadow (R ~ 1-30): fill it explicitly
    yy, xx = np.mgrid[0:h, 0:w]
    face = ((xx - 706) / 82.0) ** 2 + ((yy - 346) / 100.0) ** 2 <= 1
    m = m | face
    m = ndi.binary_closing(m, structure=np.ones((7, 7)))
    m = ndi.binary_fill_holes(m)
    lab, n = ndi.label(m)
    sizes = ndi.sum(m, lab, range(1, n + 1))
    keep = np.isin(lab, [i + 1 for i, s_ in enumerate(sizes) if s_ > 6000])
    keep = ndi.binary_opening(keep, structure=np.ones((3, 3)))
    alpha = ndi.gaussian_filter(keep.astype(np.float32), 2.0)
    alpha = np.clip((alpha - 0.3) / 0.45, 0, 1)
    yy1 = np.linspace(0, 1, h)[:, None]
    alpha *= np.clip((1 - yy1) / 0.20, 0, 1) ** 1.2
    # lift the crushed shadows a little so the face reads as dark red marble, not a hole
    rgb = a.copy()
    rgb[..., 0] = np.clip(rgb[..., 0] * 1.0 + 26 * (1 - np.clip(rgb[..., 0] / 90, 0, 1)), 0, 255)
    rgba = np.dstack([rgb, alpha * 255]).astype(np.uint8)
    return Image.fromarray(rgba, "RGBA")


def save(img, name, width, q=80):
    r = img.resize((width, round(img.height * width / img.width)), Image.LANCZOS)
    path = os.path.join(OUT, name)
    r.save(path, "WEBP", quality=q, method=6, alpha_quality=85)
    print(f"{name:22} {r.size}  {os.path.getsize(path)/1024:6.1f} KB")


def _rgba(path):
    return Image.open(os.path.join(OUT, path)).convert("RGBA")


def _fade(img, left=0.0, right=0.0, top=0.0, bottom=0.0):
    """Multiply the alpha by soft ramps on each edge (fractions of width/height)."""
    a = np.asarray(img).astype(np.float32)
    h, w = a.shape[:2]
    m = np.ones((h, w), np.float32)
    xs, ys = np.arange(w)[None, :] / w, np.arange(h)[:, None] / h
    if left:   m *= np.clip(xs / left, 0, 1)
    if right:  m *= np.clip((1 - xs) / right, 0, 1)
    if top:    m *= np.clip(ys / top, 0, 1)
    if bottom: m *= np.clip((1 - ys) / bottom, 0, 1)
    a[..., 3] *= m
    return Image.fromarray(a.astype(np.uint8), "RGBA")


def section_pictures():
    """One picture per section, each cropped for its slot."""
    # About: halftone torso, portrait window
    im = _rgba("src-halftone.jpg")
    save(im.crop((0, 300, 736, 1281)), "pic-about.webp", 420, 74)
    # Stack: crying angel, wide cinematic banner that melts into black at the bottom
    im = _rgba("src-crying-angel.jpg").crop((0, 0, 736, 250))
    save(_fade(im, bottom=0.55), "pic-stack.webp", 1000, 76)
    # Workflow: neon golden-ratio statue, centre band with soft left/right edges
    im = _rgba("src-neon.jpg").crop((0, 90, 736, 520))
    save(_fade(im, left=0.28, right=0.28, top=0.12, bottom=0.12), "pic-workflow.webp", 900, 74)
    # Closing: winged angel painting, full width
    im = _rgba("src-winged.jpg")
    save(im, "pic-closing.webp", 1000, 72)


if __name__ == "__main__":
    full = cutout()
    save(full, "statue-hero.webp", 640)
    section_pictures()
