# QA-art: SET gate round 2, film 9 `set3d9` (wall_site + mortar macro)

I reviewed all 33 finals in `wall_work/final/` at full size (720x1280) and `contact.jpg`, against ref A t0040 / t0062 / t0072 / t0096 / t0104, ref B t0033 and `film/analysis/sheets/*.jpg`. The characters are still placeholder cards, so acting is scored on staging only.

## Verdict: **FIX-FIRST** (macro only)

The site world is ready to ship. Skies, density, wall_top, the outer face and the collapse all moved up, and smoke, steam and dust are now crisp. The reveal macro is much better, but it still does not read in one glance on a phone. It is the film's key image and the client's explicit fix #3, so it blocks. The blockers are listed at the end, and they are all inside `mortar_macro*`.

## Scores (1-10, round 1 in brackets)

| area | score | note |
|---|---|---|
| Set density / ornament | **8** (7) | `two_sections` DAY/RAIN/BATTLE now have a fully dressed lower 40 % (cart, buckets, planks, tool rack, second brazier, extra workers). `wall_top` is paved and crenellated, with tubs, a crane and a second figure. `two_shot_low` and `pour_close` are rich (jars, bricks, troughs, scaffold). Still sparse: `aftermath_dawn` (bare wall, empty top 30 % and bottom 25 %), `cannon_line` (bottom 30 % bare grass), `gate_dusk` (bare dirt bottom half). |
| Lighting & colour | **7** (7) | The DAY sky is fixed: warm blue with gold-topped cartoon clouds, no bleached top third, very close to ref A t0062. DUSK and DAWN stay beautiful. Weak spots: the `two_sections_out` BATTLE sky is still flat navy in the top 25 %, and from this camera there is no glow band behind the wall. BATTLE clouds are repeated identical "bun" discs in rows, which reads as stamped. `aftermath_dawn` is cold blue-violet with no sun on the wall, which is wrong for the ending. The macro now has the right 2-tone idea (gold/cyan against blue-grey) but too little of the frame carries it. |
| Composition / framing | **7** (6) | `two_sections_out` now has a foreground (torch, fence, barrel), the banner-pole shadows are gone, and the wall fills about y 330-1000. `wall_top` sits at eye height looking along the walk, though the walkway still takes about 40 %. The `cannon_line` hero cannon is fully in frame. The macro is square-on and centred, but the subject band is only about 18 % of the frame height (see blockers). |
| Character acting (staging) | **7** (6) | `two_shot_low` and `pour_close` give real medium shots: heads are large, clear and above y 880, and posture reads. The wide shots still carry tiny figures, as expected. |
| Key moments | hook **8** / reveal **6** / collapse **8** / ending **5** | Hook: the cauldron is unchanged and strong. Reveal: the rice web now reads as an ordered gold radial net, but the frame is mostly dead speckled grey, and the plain crack reads as black tentacles (see below). Collapse: `col0.35` is now warm-lit, and the tumbling brick slabs read clearly against the sky. Ending (`aftermath_dawn`, new): a flat frontal wall with 3 dents, cold and empty. The dents read, but it is not a payoff image. |
| Overall match to references | **7** (6) | The site frames now sit comfortably in ref A/B's family. The macro is closer to t0104 in intent (centred, graphic, gold focus) but not yet in clarity or richness. |

## Smoke / dust / steam: no longer blurry: **SOLVED**
All billows now have hard cel silhouettes with lit tops and shaded undersides: steam in `cauldron` and `site_wide`, battle smoke in `cannon_line` and `site_wide` BATTLE, collapse dust in `col1.0`, and the impact puffs. Nothing reads as a soft wash. Minor, non-blocking notes:
- The cauldron steam in DAY/RAIN reads slightly glassy and bluish, like a stack of translucent marshmallows.
- In `col1.0` the overlapping dust shells show faint internal seams.
- The `cannon_line` ghost-face column is gone.

## Last round's fixes A-E

- **A. Rebuild the macro to rival t0104: PARTLY SOLVED.** Done: a near square-on camera with the impact dead centre and the joint as a horizontal band; bricks in cool low-detail shade; about 130 faceted cyan crystals that now read as minerals; an ordered rice web of radial spokes, rings and nodes; a visible held state at 0.9 (brighter centre glow); brick-red and grey shards on the plain side; a gold-against-blue-grey palette. Still wrong (blockers 1-3 below):
  - The band is only about y 520-760 (18 % of the height), and the bricks above and below do not read as bricks. They are uniform speckled dark grey, like asphalt, with no visible bevels or joints apart from a sliver at the left edge.
  - The plain cracks are smooth curling tubes with zipper teeth, which read as an octopus or tentacles, not fractures. No hot running front is visible at 0.45 or 0.9, and at 0.45 the orange flash fans read as hairbrushes.
  - Rice 0.36: the dent ring renders beside the ball as a dark loop, so the ball reads as a kettlebell or teapot.
  - In a one-glance phone read, rice t0/0.9 gives "a glowing gold net in a strip on a dark wall" (good). Plain 0.9 gives "black tentacles". Neither says "brick wall joint".
- **B. DAY skies + lower midground: SOLVED.** The sky is warm blue with gold-lit clouds, in the style of ref A t0062. The `two_sections` lower 40 % is fully dressed.
- **C. Re-stage the outer-face battle frames: MOSTLY SOLVED.** The foreground dressing is in, the banner shadows are gone, and the collapse debris is warm-lit and reads as bricks. Remaining (non-blocking): the top 25 % is flat navy with no glow band behind the wall from this camera. The general's cracks at `crack0.66` are faint translucent decals that barely read at phone size (`crack0.33` reads better thanks to the dust puff).
- **D. `wall_top`: SOLVED.** The camera is at eye height looking along the walk, the top is paved with crenels, and there are tubs, a crane, the scaffold and two figures. The walk still takes about 40 % against the asked ≤33 %, which is acceptable.
- **E. `cannon_line`: PARTLY SOLVED.** The hero cannon is fully framed and the ghost-face smoke is removed. The ball in flight is still not visible in `impg1@0.22`: the general's slot-1 ball is out of this view or hidden, and only a white puff shows near the gate. The bottom 30 % is bare grass. Non-blocking: the flight can be shown in the take with a slot whose arc crosses this frame.

## Blockers (macro only; fix these, re-render the 6 `mortar_macro*` frames, then SHIP)

1. **Make the joint own the frame and the bricks read as bricks** (`macro_front`). Push in or narrow the FOV so the bed joint fills about 35-40 % of the height (about y 400-880), centred. Show one full brick edge above and below with a bevel catching a thin warm rim (or the blue rim) and the joint lip shadow, plus a visible head joint near centre-left, so the frame says "mortar between bricks" in one glance. Keep the bricks dark and low-detail, but give them a readable silhouette.
2. **Plain cracks must look like fractures.** Replace the curling tubes with 3-5 jagged, mostly straight zig-zag polylines that taper to a point. Use a dark core and a pale chipped lip, with no sawtooth "zipper" teeth. Make the hot orange running front visible at the crack tips at t 0.45-0.6. Replace the comb-like orange flash fans at 0.45 with a round flash or star burst.
3. **Rice 0.36 ball "handle".** Hide or put behind the ball the dark loop (dent ring) that shows beside it, and make the bright pulse ring at the hit read around the ball, so the impact frame reads as ball hits, gold ring flares.

## Strongly recommended, not blocking
- `aftermath_dawn` (ending): add warm low dawn sun raking across the wall from one side so the dents cast shadows and the bricks glow gold. Add sky gradient and clouds in the empty top, and a foreground (rubble of the general's section, a banner, Lin) in the empty bottom 25 %.
- `two_sections_out` BATTLE: an orange-red glow band and a lit smoke bank behind the wall in the top third. Make the general's crack decals more opaque and darker so `crack0.66` reads on a phone.
- BATTLE clouds: vary disc size, spacing and row offsets so they stop looking stamped.
