import random

random.seed(42)

W, H = 1200, 320
title = "JAVOHIR ABDUVAHHOBOV"
font_size = 58
letter_spacing = 40  # approx horizontal step per char (monospace-ish via textLength trick not needed, we just space manually)

# compute total width and center
total_w = letter_spacing * len(title)
start_x = (W - total_w) / 2 + letter_spacing / 2
baseline_y = 150

colors = ["#00f5ff", "#7f5af0", "#ff2fd0", "#ffd60a", "#39ff88"]

letters_svg = []
for i, ch in enumerate(title):
    x = start_x + i * letter_spacing
    color = colors[i % len(colors)]
    dur = round(2.2 + (i % 5) * 0.15, 2)
    begin = round((i * 0.07), 2)
    if ch == " ":
        continue
    letters_svg.append(f'''
    <text x="{x:.1f}" y="{baseline_y}" text-anchor="middle" font-family="'Segoe UI', Verdana, Arial, sans-serif"
          font-weight="800" font-size="{font_size}" fill="{color}" filter="url(#glow)" opacity="0.97">
      {ch}
      <animateTransform attributeName="transform" type="translate"
        values="0 0; 0 -14; 0 0; 0 8; 0 0"
        keyTimes="0;0.25;0.5;0.75;1"
        dur="{dur}s" begin="{begin}s" repeatCount="indefinite" />
      <animate attributeName="fill-opacity" values="0.7;1;0.7" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>
    </text>''')

letters_block = "".join(letters_svg)

# particles - small floating dots with random paths
particles = []
for i in range(46):
    cx = random.uniform(0, W)
    cy = random.uniform(0, H)
    r = round(random.uniform(0.8, 2.6), 2)
    color = random.choice(colors)
    dur = round(random.uniform(4, 10), 2)
    dx = random.uniform(-60, 60)
    dy = random.uniform(-40, 40)
    delay = round(random.uniform(0, 6), 2)
    op = round(random.uniform(0.25, 0.85), 2)
    particles.append(f'''
    <circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r}" fill="{color}" opacity="{op}">
      <animateTransform attributeName="transform" type="translate"
        values="0 0; {dx:.1f} {dy:.1f}; 0 0" dur="{dur}s" begin="{delay}s" repeatCount="indefinite" />
      <animate attributeName="opacity" values="{op};0.05;{op}" dur="{dur}s" begin="{delay}s" repeatCount="indefinite"/>
    </circle>''')
particles_block = "".join(particles)

subtitle = "Mobile &amp; Backend Engineer  ·  Flutter  ·  Node.js  ·  PostgreSQL  ·  ML/DL Enthusiast"
sub_len = len(subtitle)
typing_dur = 6.5

svg = f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="bgGrad" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" stop-color="#05060f">
        <animate attributeName="stop-color" values="#05060f;#0b0f2b;#1a0b2b;#05060f" dur="10s" repeatCount="indefinite"/>
      </stop>
      <stop offset="50%" stop-color="#0b0f2b">
        <animate attributeName="stop-color" values="#0b0f2b;#1a0b2b;#05060f;#0b0f2b" dur="10s" repeatCount="indefinite"/>
      </stop>
      <stop offset="100%" stop-color="#1a0b2b">
        <animate attributeName="stop-color" values="#1a0b2b;#05060f;#0b0f2b;#1a0b2b" dur="10s" repeatCount="indefinite"/>
      </stop>
    </linearGradient>
    <filter id="glow" x="-60%" y="-60%" width="220%" height="220%">
      <feGaussianBlur stdDeviation="4" result="blur"/>
      <feMerge>
        <feMergeNode in="blur"/>
        <feMergeNode in="SourceGraphic"/>
      </feMerge>
    </filter>
    <clipPath id="typeClip">
      <rect x="0" y="0" height="40" width="0">
        <animate attributeName="width" values="0;900;900;0;0" keyTimes="0;0.42;0.55;0.58;1"
                  dur="{typing_dur}s" repeatCount="indefinite"/>
      </rect>
    </clipPath>
  </defs>

  <rect width="{W}" height="{H}" fill="url(#bgGrad)" rx="18"/>

  <!-- floating particles -->
  {particles_block}

  <!-- animated title letters -->
  {letters_block}

  <!-- typewriter subtitle -->
  <g transform="translate(150, 205)">
    <text x="0" y="0" font-family="Consolas, 'Courier New', monospace" font-size="19" fill="#8be9fd" clip-path="url(#typeClip)">
      &gt; {subtitle}
      <animate attributeName="fill" values="#8be9fd;#ff2fd0;#39ff88;#8be9fd" dur="6s" repeatCount="indefinite"/>
    </text>
    <rect x="-2" y="-16" width="3" height="22" fill="#39ff88">
      <animate attributeName="opacity" values="1;0;1" dur="0.8s" repeatCount="indefinite"/>
      <animateTransform attributeName="transform" type="translate" values="0 0;900 0;900 0;0 0;0 0"
        keyTimes="0;0.42;0.55;0.58;1" dur="{typing_dur}s" repeatCount="indefinite"/>
    </rect>
  </g>

  <!-- pulsing border ring accents -->
  <rect x="4" y="4" width="{W-8}" height="{H-8}" rx="16" fill="none" stroke="url(#bgGrad)" stroke-width="0"/>
  <rect x="2" y="2" width="{W-4}" height="{H-4}" rx="16" fill="none" stroke="#7f5af0" stroke-width="1.4" opacity="0.55">
    <animate attributeName="stroke" values="#7f5af0;#00f5ff;#ff2fd0;#7f5af0" dur="8s" repeatCount="indefinite"/>
  </rect>
</svg>'''

with open('/home/claude/readme-project/assets/header.svg', 'w') as f:
    f.write(svg)

print("header.svg written", len(svg), "bytes")
