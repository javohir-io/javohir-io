TITLES = {
    "title-about": "ABOUT ME",
    "title-stack": "TECH STACK",
    "title-stats": "GITHUB STATS",
    "title-connect": "LET'S CONNECT",
    "title-projects": "WHAT I BUILD",
}

COLORS = ["#00f5ff", "#7f5af0", "#ff2fd0", "#ffd60a", "#39ff88"]


def build_title(text):
    font_size = 40
    step = 30
    total_w = step * len(text)
    W = int(total_w + 80)
    H = 90
    start_x = 40 + step / 2
    baseline = 56

    letters = []
    for i, ch in enumerate(text):
        x = start_x + i * step
        color = COLORS[i % len(COLORS)]
        dur = round(1.8 + (i % 4) * 0.2, 2)
        begin = round(i * 0.06, 2)
        if ch == " ":
            continue
        safe_ch = ch.replace("&", "&amp;").replace("'", "&#39;")
        letters.append(f'''
    <text x="{x:.1f}" y="{baseline}" text-anchor="middle" font-family="Consolas, monospace"
          font-weight="800" font-size="{font_size}" fill="{color}">
      {safe_ch}
      <animateTransform attributeName="transform" type="translate"
        values="0 0; 0 -10; 0 0; 0 6; 0 0" keyTimes="0;0.25;0.5;0.75;1"
        dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>
    </text>''')

    letters_block = "".join(letters)

    svg = f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="ul" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#00f5ff" stop-opacity="0"/>
      <stop offset="50%" stop-color="#7f5af0"/>
      <stop offset="100%" stop-color="#ff2fd0" stop-opacity="0"/>
    </linearGradient>
  </defs>
  {letters_block}
  <rect x="20" y="72" width="{W-40}" height="3" fill="url(#ul)">
    <animate attributeName="width" values="0;{W-40};{W-40}" keyTimes="0;0.6;1" dur="2.4s" repeatCount="indefinite"/>
  </rect>
</svg>'''
    return W, H, svg


for key, text in TITLES.items():
    W, H, svg = build_title(text)
    path = f'/home/claude/readme-project/assets/{key}.svg'
    with open(path, 'w') as f:
        f.write(svg)
    print(key, W, H)
