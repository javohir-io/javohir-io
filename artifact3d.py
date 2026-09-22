# -*- coding: utf-8 -*-
"""
Pure-SVG "3D": we compute real 3D rotation + weak-perspective projection in
Python across N keyframes, then bake each vertex/edge's per-frame (x,y,opacity,
width) into SMIL <animate values="f0;f1;f2;...;f0"> lists. The browser does no
3D math at all — it's just interpolating between pre-computed 2D frames — but
because those frames come from a real rotating 3D model (with depth-based
shading and scale), the result reads as a genuinely rotating solid, not a
2D trick. No JS, works anywhere SMIL works (GitHub included).
"""
import math

# ---------------------------------------------------------------- 3D core

def normalize(v):
    x, y, z = v
    n = math.sqrt(x*x + y*y + z*z)
    return (x/n, y/n, z/n)

def rot_x(v, a):
    x, y, z = v
    ca, sa = math.cos(a), math.sin(a)
    return (x, y*ca - z*sa, y*sa + z*ca)

def rot_y(v, a):
    x, y, z = v
    ca, sa = math.cos(a), math.sin(a)
    return (x*ca + z*sa, y, -x*sa + z*ca)

def rot_z(v, a):
    x, y, z = v
    ca, sa = math.cos(a), math.sin(a)
    return (x*ca - y*sa, x*sa + y*ca, z)

def build_icosahedron():
    phi = (1 + 5**0.5) / 2
    raw = [
        (-1, phi, 0), (1, phi, 0), (-1, -phi, 0), (1, -phi, 0),
        (0, -1, phi), (0, 1, phi), (0, -1, -phi), (0, 1, -phi),
        (phi, 0, -1), (phi, 0, 1), (-phi, 0, -1), (-phi, 0, 1),
    ]
    verts = [normalize(v) for v in raw]
    n = len(verts)
    def d(a, b):
        return math.sqrt(sum((a[k]-b[k])**2 for k in range(3)))
    ds = [d(verts[i], verts[j]) for i in range(n) for j in range(i+1, n)]
    minlen = min(ds)
    edges = [(i, j) for i in range(n) for j in range(i+1, n) if abs(d(verts[i], verts[j]) - minlen) < 1e-6]
    return verts, edges

def build_tetrahedron():
    raw = [(1,1,1), (1,-1,-1), (-1,1,-1), (-1,-1,1)]
    verts = [normalize(v) for v in raw]
    edges = [(i, j) for i in range(4) for j in range(i+1, 4)]
    return verts, edges

def build_ring(count, radius, tilt):
    """points on a circle in the XZ plane, pre-tilted, used as an orbiting debris ring"""
    pts = []
    for k in range(count):
        a = 2 * math.pi * k / count
        p = (radius * math.cos(a), 0.0, radius * math.sin(a))
        p = rot_x(p, tilt)
        pts.append(p)
    return pts

def project(v, scale, cx, cy, focal=4.2):
    x, y, z = v
    f = focal / (focal + z)
    return (cx + x * scale * f, cy + y * scale * f, f)

def depth_to_opacity(f, lo=0.28, hi=1.0, flo=0.62, fhi=1.55):
    t = (f - flo) / (fhi - flo)
    t = max(0.0, min(1.0, t))
    return lo + t * (hi - lo)

def depth_to_width(f, lo=0.7, hi=2.4, flo=0.62, fhi=1.55):
    t = (f - flo) / (fhi - flo)
    t = max(0.0, min(1.0, t))
    return lo + t * (hi - lo)

def fmt_list(vals, nd=2):
    return ";".join(f"{v:.{nd}f}" for v in vals)

def animate_tags(attr, values, dur, nd=2, extra=""):
    return f'<animate attributeName="{attr}" values="{fmt_list(values, nd)}" dur="{dur}s" begin="0s" repeatCount="indefinite" calcMode="linear"{extra}/>'

# ---------------------------------------------------------------- frame baking

def bake_wireframe(verts, edges, frames, cx, cy, scale, wx, wy, wz, phase=0.0):
    """returns per-edge dict of frame lists, and per-vertex frame lists"""
    edge_frames = {e: {"x1": [], "y1": [], "x2": [], "y2": [], "op": [], "w": []} for e in edges}
    vert_frames = {i: {"cx": [], "cy": [], "r": [], "op": []} for i in range(len(verts))}
    for fi in range(frames + 1):
        t = (fi / frames) * 2 * math.pi + phase
        rotated = []
        for v in verts:
            p = rot_y(v, wy * t)
            p = rot_x(p, wx * t)
            p = rot_z(p, wz * t)
            rotated.append(project(p, scale, cx, cy))
        for i, (sx, sy, f) in enumerate(rotated):
            vert_frames[i]["cx"].append(sx)
            vert_frames[i]["cy"].append(sy)
            vert_frames[i]["r"].append(1.1 + depth_to_width(f) * 0.7)
            vert_frames[i]["op"].append(depth_to_opacity(f))
        for (a, b) in edges:
            sax, say, fa = rotated[a]
            sbx, sby, fb = rotated[b]
            avg_f = (fa + fb) / 2
            edge_frames[(a, b)]["x1"].append(sax)
            edge_frames[(a, b)]["y1"].append(say)
            edge_frames[(a, b)]["x2"].append(sbx)
            edge_frames[(a, b)]["y2"].append(sby)
            edge_frames[(a, b)]["op"].append(depth_to_opacity(avg_f))
            edge_frames[(a, b)]["w"].append(depth_to_width(avg_f))
    return edge_frames, vert_frames

def bake_points(points3d, frames, cx, cy, scale, wx, wy, wz, phase=0.0):
    out = [{"cx": [], "cy": [], "r": [], "op": []} for _ in points3d]
    for fi in range(frames + 1):
        t = (fi / frames) * 2 * math.pi + phase
        for i, v in enumerate(points3d):
            p = rot_y(v, wy * t)
            p = rot_x(p, wx * t)
            p = rot_z(p, wz * t)
            sx, sy, f = project(p, scale, cx, cy)
            out[i]["cx"].append(sx)
            out[i]["cy"].append(sy)
            out[i]["r"].append(0.9 + depth_to_width(f) * 0.55)
            out[i]["op"].append(depth_to_opacity(f, lo=0.15, hi=0.95))
    return out

def render_wireframe_svg(edge_frames, vert_frames, dur, c, edge_color_key="accent", vert_color_key="accent"):
    out = []
    for e, fr in edge_frames.items():
        out.append(
            f'<line x1="{fr["x1"][0]:.2f}" y1="{fr["y1"][0]:.2f}" x2="{fr["x2"][0]:.2f}" y2="{fr["y2"][0]:.2f}" '
            f'stroke="{c[edge_color_key]}" stroke-width="{fr["w"][0]:.2f}" stroke-opacity="{fr["op"][0]:.2f}" stroke-linecap="round">'
            + animate_tags("x1", fr["x1"], dur)
            + animate_tags("y1", fr["y1"], dur)
            + animate_tags("x2", fr["x2"], dur)
            + animate_tags("y2", fr["y2"], dur)
            + animate_tags("stroke-opacity", fr["op"], dur, nd=3)
            + animate_tags("stroke-width", fr["w"], dur)
            + '</line>'
        )
    for i, fr in vert_frames.items():
        out.append(
            f'<circle cx="{fr["cx"][0]:.2f}" cy="{fr["cy"][0]:.2f}" r="{fr["r"][0]:.2f}" '
            f'fill="{c[vert_color_key]}" opacity="{fr["op"][0]:.2f}">'
            + animate_tags("cx", fr["cx"], dur)
            + animate_tags("cy", fr["cy"], dur)
            + animate_tags("r", fr["r"], dur)
            + animate_tags("opacity", fr["op"], dur, nd=3)
            + '</circle>'
        )
    return "\n".join(out)

def render_points_svg(point_frames, dur, c, color_key="ink"):
    out = []
    for fr in point_frames:
        out.append(
            f'<circle cx="{fr["cx"][0]:.2f}" cy="{fr["cy"][0]:.2f}" r="{fr["r"][0]:.2f}" '
            f'fill="{c[color_key]}" opacity="{fr["op"][0]:.2f}">'
            + animate_tags("cx", fr["cx"], dur)
            + animate_tags("cy", fr["cy"], dur)
            + animate_tags("r", fr["r"], dur)
            + animate_tags("opacity", fr["op"], dur, nd=3)
            + '</circle>'
        )
    return "\n".join(out)
