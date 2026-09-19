# How to make this go live on your GitHub profile

GitHub profile READMEs only animate correctly when the SVGs are served as **raw files from a real repo** — not pasted inline as markdown — so follow these steps exactly.

## 1. Create the special profile repo

1. Go to https://github.com/new
2. Repository name must be **exactly** your username: `javohir-io`
3. Make it **Public**
4. Check "Add a README file", then create it (you'll overwrite it next)

GitHub detects a repo named after your username and shows its README on your profile page automatically.

## 2. Upload the files

Clone it locally, then copy in everything from this zip:

```bash
git clone https://github.com/javohir-io/javohir-io.git
cd javohir-io
# copy README.md and the assets/ folder from this zip into this directory
git add .
git commit -m "insane animated profile readme"
git push
```

Your folder structure should look like:

```
javohir-io/
├── README.md
└── assets/
    ├── header.svg
    ├── pet.svg
    ├── wave-divider.svg
    ├── footer.svg
    ├── title-about.svg
    ├── title-stack.svg
    ├── title-stats.svg
    ├── title-projects.svg
    ├── title-connect.svg
    ├── orbit-mobile.svg
    ├── orbit-backend.svg
    ├── orbit-database.svg
    ├── orbit-web.svg
    ├── orbit-languages.svg
    └── orbit-ml.svg
```

The `README.md` already references everything as relative paths (`assets/header.svg` etc.), which GitHub resolves correctly once both files sit in the same repo — no need to hardcode your raw.githubusercontent.com URL.

## 3. Wait a minute, then check your profile

Visit `https://github.com/javohir-io` — the header, the walking fox, the orbiting tech rings, and the stat widgets should all be live and animating.

## Why it's built this way (and what to know)

- **The animation is real, not a gif.** Every moving piece — the wavy letters, the walking fox, the orbiting skill pills, the typewriter subtitle, the wave dividers — is done with native SVG `SMIL` animation (`<animate>`, `<animateTransform>`, `<animateMotion>`). Browsers render this natively when GitHub serves the raw SVG file, so it keeps animating for as long as someone has the page open — no JavaScript required (GitHub strips `<script>` tags from READMEs for security, so SMIL is the only path to real motion).
- **The stats/streak/top-langs/activity-graph/trophy images are genuinely live** — they're generated on-demand by open-source community services (github-readme-stats, github-readme-streak-stats, github-readme-activity-graph, github-profile-trophy) every time someone loads your profile, using your real GitHub data at that moment.
- **The view counter** (komarev.com badge) increments live on every profile visit.
- If you ever want to swap the color theme, every SVG's `<defs>` block at the top has the gradient/stroke colors in one place — the whole thing is `#00f5ff` (cyan) / `#7f5af0` (violet) / `#ff2fd0` (magenta) / `#39ff88` (green) / `#ffd60a` (gold), so changing those five hex values anywhere updates the whole palette.
- Want the fox to be a cat, dog, or something else? Open `assets/pet.svg` in a text editor — the shapes are simple `<path>`/`<ellipse>`/`<rect>` primitives, easy to nudge.
- File sizes were left uncompressed on purpose per your request — nothing here has been minified. If GitHub ever complains about total repo size (it won't, this is only ~100 KB combined) you can safely minify with any SVG minifier.

## Regenerating / customizing

Every asset was generated from a small Python script — they're included so you can tweak anything (title text, palette, orbit items, walk speed) and regenerate instantly:

```
gen_header.py    → assets/header.svg
gen_pet.py       → assets/pet.svg
gen_orbits.py    → assets/orbit-*.svg
gen_titles.py    → assets/title-*.svg
gen_wave_footer.py → assets/wave-divider.svg, assets/footer.svg
```

Edit the script, run `python3 <script>.py`, and the corresponding SVG updates.
