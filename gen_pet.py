W, H = 1200, 140
ground_y = 118

svg = f'''<svg width="{W}" height="{H}" viewBox="0 0 {W} {H}" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="groundGrad" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0%" stop-color="#0d1117"/>
      <stop offset="50%" stop-color="#151a2e"/>
      <stop offset="100%" stop-color="#0d1117"/>
    </linearGradient>
    <filter id="petGlow" x="-50%" y="-50%" width="200%" height="200%">
      <feGaussianBlur stdDeviation="1.6" result="b"/>
      <feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge>
    </filter>
  </defs>

  <rect width="{W}" height="{H}" fill="url(#groundGrad)" rx="14"/>
  <line x1="0" y1="{ground_y+14}" x2="{W}" y2="{ground_y+14}" stroke="#2a2f4a" stroke-width="2" stroke-dasharray="6 8">
    <animate attributeName="stroke-dashoffset" values="0;-140" dur="6s" repeatCount="indefinite"/>
  </line>

  <!-- walking fox group; moves left<->right across the full banner and flips direction -->
  <g id="fox">
    <animateMotion path="M 40 0 H {W-140} H 40 Z" keyPoints="0;0.5;1" keyTimes="0;0.5;1"
      calcMode="linear" dur="16s" repeatCount="indefinite"/>
    <g id="foxBody" filter="url(#petGlow)">
      <!-- tail -->
      <path d="M -6 { ground_y-18 } q -22 -6 -26 14 q -2 14 16 12" fill="#ff8a3d" stroke="#c9611c" stroke-width="1.5">
        <animateTransform attributeName="transform" type="rotate" values="0 -6 {ground_y-6};-14 -6 {ground_y-6};0 -6 {ground_y-6}" dur="0.6s" repeatCount="indefinite"/>
      </path>
      <!-- back legs -->
      <rect x="8" y="{ground_y-14}" width="6" height="16" rx="2" fill="#c9611c">
        <animateTransform attributeName="transform" type="rotate" values="18 11 {ground_y-14};-18 11 {ground_y-14};18 11 {ground_y-14}" dur="0.4s" repeatCount="indefinite"/>
      </rect>
      <rect x="34" y="{ground_y-14}" width="6" height="16" rx="2" fill="#c9611c">
        <animateTransform attributeName="transform" type="rotate" values="-18 37 {ground_y-14};18 37 {ground_y-14};-18 37 {ground_y-14}" dur="0.4s" repeatCount="indefinite"/>
      </rect>
      <!-- body -->
      <ellipse cx="30" cy="{ground_y-22}" rx="30" ry="15" fill="#ff8a3d" stroke="#c9611c" stroke-width="1.5"/>
      <ellipse cx="30" cy="{ground_y-14}" rx="26" ry="8" fill="#fff6ea" opacity="0.9"/>
      <!-- front legs -->
      <rect x="14" y="{ground_y-14}" width="6" height="16" rx="2" fill="#c9611c">
        <animateTransform attributeName="transform" type="rotate" values="-18 17 {ground_y-14};18 17 {ground_y-14};-18 17 {ground_y-14}" dur="0.4s" repeatCount="indefinite"/>
      </rect>
      <rect x="48" y="{ground_y-14}" width="6" height="16" rx="2" fill="#c9611c">
        <animateTransform attributeName="transform" type="rotate" values="18 51 {ground_y-14};-18 51 {ground_y-14};18 51 {ground_y-14}" dur="0.4s" repeatCount="indefinite"/>
      </rect>
      <!-- head -->
      <g>
        <animateTransform attributeName="transform" type="translate" values="0 0;0 -3;0 0" dur="0.4s" repeatCount="indefinite"/>
        <path d="M 52 {ground_y-34} q 20 -6 26 6 q 3 8 -6 12 q -12 4 -20 -4 Z" fill="#ff8a3d" stroke="#c9611c" stroke-width="1.5"/>
        <path d="M 60 {ground_y-40} l 6 12 l -12 2 Z" fill="#ff8a3d" stroke="#c9611c" stroke-width="1.2"/>
        <path d="M 76 {ground_y-40} l -2 12 l 12 -4 Z" fill="#ff8a3d" stroke="#c9611c" stroke-width="1.2"/>
        <circle cx="75" cy="{ground_y-26}" r="2" fill="#0d1117"/>
        <circle cx="79" cy="{ground_y-22}" r="1.4" fill="#0d1117"/>
      </g>
    </g>
  </g>

  <text x="{W/2}" y="24" text-anchor="middle" font-family="Consolas, monospace" font-size="12" fill="#5b6270" opacity="0.7">
    thanks for stopping by — say hi to my fox 🦊
  </text>
</svg>'''

with open('/home/claude/readme-project/assets/pet.svg', 'w') as f:
    f.write(svg)
print("pet.svg written", len(svg))
