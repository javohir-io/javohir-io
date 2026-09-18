# How to use this

1. Create (or open) the special repo named exactly **`javohir-io`** on GitHub —
   that's the one GitHub turns into your profile page.
2. Drop everything from this zip into the repo root, keeping the folder structure:
   ```
   README.md
   assets/            (light-theme SVGs)
   assets/dark/       (dark-theme SVGs)
   ```
3. Commit and push. GitHub will pick the right SVG automatically based on the
   viewer's site theme (light/dark) — that's what the `<picture>` +
   `prefers-color-scheme` markup in the README does.

## What's real vs. placeholder

Everything about your stack, the JobFlow app architecture, and your bio is
built from what you told me — that's real. Two small things are placeholders
you'll want to swap:

- **"Flutter Arcade Game"** — I don't know the actual name of your game, so I
  used a generic label. Tell me the real title (and repo link) and I'll
  regenerate `assets/projects.svg` + `assets/dark/projects.svg` with it.
- **`view repo →` links** — both project cards currently point at your
  profile (`github.com/javohir-io`) rather than the specific repos, since I
  don't have the exact repo slugs. Send them over and I'll bake the real
  links in.

## Editing anything else yourself

Every visual is a plain SVG generated from `gen.py` (included) — open any
`.svg` file in a text editor and tweak the `<text>` content directly, or ask
me to change the copy/colors/layout and I'll regenerate the pair for you.
The GitHub stats and contribution graph are live, external widgets (via
github-readme-stats/github-readme-activity-graph) — no file editing needed,
they update on their own.

## Color tokens (in case you want to retheme)

| | Light | Dark |
|---|---|---|
| ink (text) | `#0d1117` | `#e6edf3` |
| muted | `#57606a` | `#9aa4b2` |
| accent | `#3b5bfd` | `#7c9fff` |
| accent 2 | `#0f9d78` | `#3ddba8` |
| line | `#d7dce2` | `#26303c` |
