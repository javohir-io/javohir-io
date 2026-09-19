W = 1200
H_DIV = 90
H_FOOT = 220

wave_div = f'''<svg width="{W}" height="{H_DIV}" viewBox="0 0 {W} {H_DIV}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="wg1" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#00f5ff"/>
      <stop offset="50%" stop-color="#7f5af0"/>
      <stop offset="100%" stop-color="#ff2fd0"/>
    </linearGradient>
  </defs>
  <path fill="url(#wg1)" opacity="0.85">
    <animate attributeName="d" dur="6s" repeatCount="indefinite"
      values="
      M0,45 C150,90 350,0 600,45 C850,90 1050,0 1200,45 L1200,90 L0,90 Z;
      M0,45 C150,0 350,90 600,45 C850,0 1050,90 1200,45 L1200,90 L0,90 Z;
      M0,45 C150,90 350,0 600,45 C850,90 1050,0 1200,45 L1200,90 L0,90 Z"/>
  </path>
  <path fill="#0d1117" opacity="0.5">
    <animate attributeName="d" dur="4.5s" repeatCount="indefinite"
      values="
      M0,60 C200,30 400,80 600,55 C800,30 1000,75 1200,55 L1200,90 L0,90 Z;
      M0,60 C200,80 400,30 600,55 C800,75 1000,30 1200,55 L1200,90 L0,90 Z;
      M0,60 C200,30 400,80 600,55 C800,30 1000,75 1200,55 L1200,90 L0,90 Z"/>
  </path>
</svg>'''

with open('/home/claude/readme-project/assets/wave-divider.svg', 'w') as f:
    f.write(wave_div)

footer_text = "Thanks for visiting my profile — let's build something great"

footer = f'''<svg width="{W}" height="{H_FOOT}" viewBox="0 0 {W} {H_FOOT}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="fg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%" stop-color="#05060f"/>
      <stop offset="100%" stop-color="#1a0b2b"/>
    </linearGradient>
    <linearGradient id="fw" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#ff2fd0"/>
      <stop offset="50%" stop-color="#00f5ff"/>
      <stop offset="100%" stop-color="#39ff88"/>
    </linearGradient>
    <filter id="fglow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="3" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>
  <rect width="{W}" height="{H_FOOT}" fill="url(#fg)"/>
  <path fill="url(#fw)" opacity="0.9">
    <animate attributeName="d" dur="7s" repeatCount="indefinite"
      values="
      M0,60 C200,20 400,100 600,60 C800,20 1000,100 1200,60 L1200,0 L0,0 Z;
      M0,60 C200,100 400,20 600,60 C800,100 1000,20 1200,60 L1200,0 L0,0 Z;
      M0,60 C200,20 400,100 600,60 C800,20 1000,100 1200,60 L1200,0 L0,0 Z"/>
  </path>

  <g filter="url(#fglow)">
    <text x="{W/2}" y="140" text-anchor="middle" font-family="Consolas, monospace" font-size="24" font-weight="700" fill="#f5f6ff">
      {footer_text}
      <animate attributeName="fill" values="#f5f6ff;#39ff88;#00f5ff;#ff2fd0;#f5f6ff" dur="8s" repeatCount="indefinite"/>
    </text>
  </g>

  <g transform="translate({W/2-10},165)">
    <path d="M0,0 C-6,-8 -18,-8 -18,2 C-18,10 0,20 0,20 C0,20 18,10 18,2 C18,-8 6,-8 0,0 Z" fill="#ff2fd0">
      <animateTransform attributeName="transform" type="scale" values="1;1.25;1" dur="1.1s" repeatCount="indefinite" additive="sum"/>
    </path>
  </g>

  <text x="{W/2}" y="205" text-anchor="middle" font-family="Consolas, monospace" font-size="13" fill="#8890a8">
    javohirabduvahhobov@gmail.com · @javohir-io
  </text>
</svg>'''

with open('/home/claude/readme-project/assets/footer.svg', 'w') as f:
    f.write(footer)

print("wave + footer written")
