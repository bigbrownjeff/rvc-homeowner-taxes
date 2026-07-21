---
name: headless-mobile-render-gotchas
description: Chrome headless clamps window width (~500px min) so "390px" renders are left-crops of a wider layout; dark full-bleed bands false-positive edge-overflow detectors
metadata:
  type: feedback
---

Two artifacts that faked a mobile-overflow bug on voices.html (2026-07-20):
- **`--window-size=390,...` does not give a 390px layout** — headless new clamps
  window width around 500px, so the screenshot is the LEFT 390px of a wider layout
  and all text looks clipped mid-word at the right edge. Verify mobile layout at
  760px (still inside the max-width:760px media query, above the clamp), or use a
  real-device screenshot. Media-query application CAN be confirmed at 390 (rules
  fire); text-wrap correctness CANNOT.
- **Dark-pixel edge-scan detectors count full-bleed dark backgrounds** (the green
  #1e6b3d bands avg <100 luminance) as "clipped text." Exclude rows whose whole
  edge region is one flat color before claiming overflow.
Also real, from the same session: iOS Safari auto-zooms on focus of any input with
font-size <16px and never zooms back — the actual cause of the "endless scroll on
mobile" report. Keep form inputs at 16px+.
