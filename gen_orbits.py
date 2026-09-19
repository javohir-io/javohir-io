import math

W, H = 1200, 380
cx, cy = W/2, H/2 + 10

PALETTE = ["#00f5ff", "#7f5af0", "#ff2fd0", "#ffd60a", "#39ff88", "#ff6b6b", "#4ea8ff", "#f2a65a"]

CATEGORIES = {
    "mobile": {
        "title": "MOBILE — Flutter App",
        "core": "Flutter",
        "items": ["Dart", "http", "shared_preferences", "file_picker", "google_fonts", "intl", "cupertino_icons"],
    },
    "backend": {
        "title": "BACKEND — Node.js API",
        "core": "Node.js",
        "items": ["Express", "JWT", "bcryptjs", "multer", "cors", "morgan", "dotenv", "uuid", "pg"],
    },
    "database": {
        "title": "DATABASE",
        "core": "PostgreSQL",
        "items": ["users", "jobs", "saved_jobs", "applications", "interviews"],
    },
    "web": {
        "title": "WEB",
        "core": "React",
        "items": ["TypeScript", "REST APIs", "Vite/Node tooling"],
    },
    "languages": {
        "title": "LANGUAGES &amp; TOOLS",
        "core": "Python",
        "items": ["Kotlin", "C", "Android Studio", "Git &amp; GitHub", "npm", "Admin HTML/CSS/JS"],
    },
    "ml": {
        "title": "MACHINE LEARNING",
        "core": "ML / DL",
        "items": ["Data Mining", "Deep Learning", "scikit-learn style workflows", "Model Evaluation"],
    },
}


def build_orbit(title, core, items):
    n = len(items)
    radius = 130
    ring2_radius = 175
    svg_parts = []
    svg_parts.append(f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <radialGradient id="coreGrad" cx="50%" cy="50%" r="60%">
      <stop offset="0%" stop-color="#1a0b2b"/>
      <stop offset="100%" stop-color="#05060f"/>
    </radialGradient>
    <filter id="g" x="-80%" y="-80%" width="260%" height="260%">
      <feGaussianBlur stdDeviation="3" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <rect width="{W}" height="{H}" rx="18" fill="url(#coreGrad)"/>
  <text x="{W/2}" y="40" text-anchor="middle" font-family="Consolas, monospace" font-size="20" font-weight="700" fill="#e6e6f0" letter-spacing="2">{title}</text>
''')

    # orbit rings (visual)
    svg_parts.append(f'  <circle cx="{cx}" cy="{cy}" r="{radius}" fill="none" stroke="#2a2f4a" stroke-width="1" stroke-dasharray="3 6" opacity="0.7"/>\n')
    svg_parts.append(f'  <circle cx="{cx}" cy="{cy}" r="{ring2_radius}" fill="none" stroke="#2a2f4a" stroke-width="1" stroke-dasharray="2 8" opacity="0.5"/>\n')

    # rotating group of orbit lines for flair
    svg_parts.append(f'''  <g>
    <animateTransform attributeName="transform" type="rotate" from="0 {cx} {cy}" to="360 {cx} {cy}" dur="40s" repeatCount="indefinite"/>
    <circle cx="{cx}" cy="{cy}" r="{ring2_radius}" fill="none" stroke="#39ff88" stroke-width="1.5" stroke-dasharray="1 40" opacity="0.9"/>
  </g>\n''')

    # core node
    svg_parts.append(f'''  <g filter="url(#g)">
    <circle cx="{cx}" cy="{cy}" r="46" fill="#0d1117" stroke="#00f5ff" stroke-width="2">
      <animate attributeName="r" values="46;50;46" dur="3s" repeatCount="indefinite"/>
      <animate attributeName="stroke" values="#00f5ff;#7f5af0;#ff2fd0;#00f5ff" dur="6s" repeatCount="indefinite"/>
    </circle>
    <text x="{cx}" y="{cy+6}" text-anchor="middle" font-family="Consolas, monospace" font-size="15" font-weight="700" fill="#fff">{core}</text>
  </g>\n''')

    # orbiting items, alternating between two radii, each with its own rotation speed via animateTransform on a wrapper <g> rotating around center, item itself counter-rotated to stay upright
    for i, item in enumerate(items):
        r = radius if i % 2 == 0 else ring2_radius
        color = PALETTE[i % len(PALETTE)]
        start_angle = (360 / n) * i
        dur = 18 + (i % 4) * 6
        direction_to = 360 if i % 2 == 0 else -360
        # bubble width based on text length
        bw = max(70, 12 * len(item) * 0.62 + 24)
        bh = 26
        svg_parts.append(f'''  <g>
    <animateTransform attributeName="transform" type="rotate" from="{start_angle} {cx} {cy}" to="{start_angle+direction_to} {cx} {cy}" dur="{dur}s" repeatCount="indefinite"/>
    <g transform="translate({cx+r},{cy})">
      <g>
        <animateTransform attributeName="transform" type="rotate" from="{-start_angle} 0 0" to="{-(start_angle+direction_to)} 0 0" dur="{dur}s" repeatCount="indefinite"/>
        <rect x="{-bw/2:.1f}" y="{-bh/2:.1f}" width="{bw:.1f}" height="{bh}" rx="13" fill="#0d1117" stroke="{color}" stroke-width="1.4" opacity="0.95"/>
        <circle cx="{-bw/2+13:.1f}" cy="0" r="4" fill="{color}">
          <animate attributeName="opacity" values="1;0.35;1" dur="{2+i*0.2:.1f}s" repeatCount="indefinite"/>
        </circle>
        <text x="8" y="5" text-anchor="middle" font-family="Consolas, monospace" font-size="12.5" fill="#dcdfe8">{item}</text>
      </g>
    </g>
  </g>\n''')

    svg_parts.append('</svg>')
    return "".join(svg_parts)


for key, cfg in CATEGORIES.items():
    content = build_orbit(cfg["title"], cfg["core"], cfg["items"])
    path = f'/home/claude/readme-project/assets/orbit-{key}.svg'
    with open(path, 'w') as f:
        f.write(content)
    print(key, len(content))
