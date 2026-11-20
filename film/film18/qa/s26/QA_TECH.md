# QA-tech round 17 s26: FAIL
Checked: 6 fps sheet (27 frames), every frame g2015-2062 (48 frames, montages plus full-size crops), bottom-strip crops g2020-2030, 2x crop of g2030 bottom-left, first and last frames. Director numbers accepted (ground 0.295, frame-diff 10.12/12.59, qa_auto blur on g1950-2010).

## Blockers
1. **Dark untextured block at the bottom, still present (round-16 blocker 2 NOT fixed).** From about g2020 to g2032 a flat dark-purple/navy hexagonal prism enters the bottom-left (about 180 px wide, 100-130 px tall at 720x1280, y about 1150-1280), grows and slides right. It is a solid, unlit, untextured shell with a small orange/brown stake poking out of it (looks like an inverted-hull outline of a post rendered as a solid). Visible in d001-d018 (g2015-2032) bottom strip and in the 2x crop of g2030. This is exactly ALL_TEAMS rule 2 (no untextured navy slab/beam). The team's QA.md admits it did not check every frame. Fix: hide that post / its outline shell (or give it a lit wood material and no flat shell), then check every frame g2015-2035 at the bottom.

## Round-16 blocker 1 verified FIXED
- No pale translucent straight-edged rectangles over the city wall at any frame g2015-2062; the wall is clean, banners and lanterns intact. Tail smoke is round soft puffs, no rectangular smoke cards at g2020 or later.

## Re-confirmed
- BIGZOOM: g1958 general is a tiny figure (about 2 %), g2066 about 45 %, end about 54 %. One continuous eased crane/swing, no cut, no pulse. Plaque 即墨 readable at start.
- Findable at start: small figure in a warm pool on the road, clear of the gate banner and roof.
- Ox mouths about y 750-830 at the end (<= 860). No face in y 880-950 (general's face y about 400-650; only feet and helmet prop near the band). No pole through a face. General whole in frame throughout (hat and raised arm stay inside the frame; at the end he is fully inside).
- No halos or colour fringes. Rim light reads as a clean pale outline on the general and oxen.
- No glitches, flicker or frozen frames in the checked range.

## Notes
- Fine stripe/moire-like texture on the roof tiles at g1958-1975 (extreme wide), only visible at 2x; accepted.
- Field panels at g1990-2012 slightly banded; accepted as in round 16.
- Helmet prop at the bottom-left from g2046 is lit and outlined; fine.
