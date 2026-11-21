# QA-tech, SET gate, set3d10 (film 10: harbour + sea), self-check by the set builder

I checked the following against film/QA_TEAM.md (QA-tech checklist) and the client's hard rules:
- `contact.jpg`: 23 tiles.
- All 23 finals in `harbour_work/final/` at 720x1280, with 1:1 crops of torpedo_chase, topdown_sea C, periscope_close and quay_low.
- `final_log.txt`, `hue_rows.txt`, `t_anim.py` (ALL OK, 34 checks), `digest` determinism, `film10/shot_plan.md`.

This is a builder's self-check, not the independent QA-tech / QA-art review: both reviewers still have to run the SET gate before the client sees the sheet.

## VERDICT: PASS (conditional)
- No picture failure is open.
- Every planned shot has a preset and state.
- The open items are legibility and look notes. They are listed under "Open, not blocking".

## Picture checks (final round)
- **Blur / DOF:** none. `make_camera` turns DOF off. The billows (funnel smoke, the hit plume) are hard-edged cartoon shapes. The DUSK sky's soft orange streaks were replaced in round 1 by crisp cartoon clouds.
- **Text / signs:** none in any frame. There is no Thai text, so no tofu is possible. Flags are plain shapes (ensign, pennant). The periscope crosshair has tick marks only, no numbers.
- **Black / magenta / blank frames:** none. `periscope_pov` is mostly black, but that is the intended lens vignette.
- **Heads vs y 880:** every staged chin is above the line:

  | preset | chin px |
  |---|---|
  | hull_plank | 625 |
  | quay_low | 699 / 716 |
  | bridge_deck | 632 |
  | periscope_close | 522 |
  | hull_side | 579 / 808 |
  | harbour_wide | 671-793 |

  The tightest is the hull_side sailor at 808.
- **Floating / contact:**
  - The painter stands on the hanging stage.
  - The admiral stands on the bridge-wing deck (z 12.05 = platform top).
  - The captain stands in the conning-tower well behind the rail (fixed in round 2).
  - The quay figures stand on the quay.
  - Wakes, foam and markers lie on the water.
- **Clipping / occlusion:** quay_low had a crate stack hiding the painter's body, and periscope_close had the captain's legs showing above the tower rim. Both are fixed in round 2.
- **Scale:** the cards are 3.0-3.3 D tall. The hull freeboard is 8.6 D and the funnels reach 20 D, which reads as a stylised warship against the figures.
- **Determinism:** `digest` matches in two processes. The round-2 fix replaced Python's per-process `hash()` seeds for the smoke.
- **Render budget:** 12.7-21.3 CPU s per frame, all under 25.
- **Hue:** the shade hue of every frame is in 240-260 (240.1-257.9, strict band, `harbour_hue.py`).

## Issues found and fixed during this pass (with backups)
**Round 1** (`bak_r1`):
1. harbour_wide was blocked by the warehouse roofs and a crane, and the quay lay in the warehouse shadow. Fixed by reframing the camera, moving the warehouses back 10 D and moving the crane.
2. The sea and harbour water had hue about 212 (cyan-blue), so the shade hue was out. Fixed with blue-violet water, warm glints and a lower sky mirror.
3. In periscope_pov the eye sat inside the periscope head, so the frame was all dark. Fixed by moving the eye to the front of the head.
4. Foam was lavender (in shade). Fixed by adding a glow term.
5. The torpedo was hidden under the swell. Fixed by raising it to awash, with a foam V.
6. The DUSK sky was soft and smeared. Fixed with the crisp cartoon-cloud painter.
7. bridge_deck did not show the dazzle ship and cropped the admiral. Fixed with a computed over-shoulder camera.

**Round 2** (`bak_r2`):
1. `clear_keys()`, inherited from film 8/9, deleted the drivers, which froze the ship bob and the gulls. It now drops only the keyed actions; caught by `t_anim.py`.
2. The digest was non-deterministic (`hash()` seeds).
3. The ROADS ship layout repeated, so two pairs of ships overlapped. Replaced with an explicit layout.
4. Merchant c1 overlapped the ghost at s 10. Moved it to x -150.
5. In topdown, the torpedo wake was invisible: too thin, and covered by the cyan aim dashes. It is now wider with a solid core, and reveal C hides the aim lines.
6. The hit plume target was off-screen. It is now on c3, larger and taller.
7. DUSK was too dark. The shade and lift were raised.
8. The bridge roof was an untextured slab. Box UVs are tiled now, and pipes and signal lamps were added.
9. Staging: the captain's height and the quay_low crates (see Clipping above).
10. Two contact labels were wrong or overlapping.

## Coverage by shot (shot_plan.md)
| shot | preset and state |
|---|---|
| 1 | `hull_plank` DAY, `set_stripes` keyed 0 → 0.47 (the zigzag reaches the brush) |
| 2 | `harbour_wide` DAY, st 1 |
| 3 | `convoy_wide` (dived U-boat, periscope and feather in the foreground) |
| 4 | `convoy_wide` + `set_hit` on c3, then `set_uboat` dive keyed |
| 5-7 | `quay_low` (marks `admiral_stride_from` → `admiral_quay`; push-in is the take's camera move) |
| 8 | `harbour_wide` (+ sailor marks on the deck / quay) |
| 9, 10 | `hull_side` st 1 / st 2 |
| 11 | `harbour_wide` DUSK st 3 (or `hull_side` DUSK st 3) |
| 12 | `convoy_wide` |
| 13 | `periscope_pov` (pan the camera; the overlay follows) |
| 14, 20 | `bridge_deck` (`admiral_bridge`, `painter_bridge`) |
| 15 | `periscope_close` (captain in the tower; the U-boat interior is not built: the brief marks it optional) |
| 16 | `torpedo_chase` with `torpedo_cam(u)` per frame |
| 17 | `topdown_sea` A (lead buoy, gold aim line) |
| 18 | `periscope_pov` + `set_ghost` fade |
| 19 | `topdown_sea` C (`s` keyed 0 → 12, ghost sails -x, the wake passes behind the real stern) |
| 21 | `harbour_wide` `hd` keyed 0 → 1 |
| 22 | `harbour_wide` `hd1,st0` (the berth ship is the last grey one: the admiral's) |
| 23 | `hull_plank` with `admiral_plank`, st 0 → 0.3 |

## Open, not blocking (for QA-art and the takes)
- **A. Tiny figures and ships in the wide shots.** In `harbour_wide` heads are about 10 px; use quay_low / hull_side / hull_plank for acting. In `topdown_sea` ships are about 120 px and the torpedo is a few pixels, so the wake and the ghost carry the read. The lower 40 % of topdown is open sea.
- **B. The `torpedo_chase` wake** is a fairly solid white band near the camera rather than bubbles.
- **C. Sea frames are about 76 % blue chroma**, against about 29 % in the references, and red is low. The warmth sits only in the horizon band, the glints and the ships. The DAY harbour frames are warmer (red 17, orange 27).
- **D. DUSK harbour frames** are dark in the lower half (long shadows across the quay), lit by lamps.
- **E. The periscope feather** seen from high above (topdown, bottom-left) is a small white V that could read as a glyph. Consider dive 0.85 with the feather hidden in the take, or crop.
- **F. Stage-1/2 stripes** in `hull_side` cover the hull only (the funnels stay grey until stage 3). The difference between st 0 / 1 / 2 is clear at full size and modest at phone size.
- **G.** Placeholder cast only.


## Round 3 (QA-art FAIL on the sea + client brief): self re-check
- All 5 QA-art blockers are addressed:
  1. **topdown reframed.** 45° oblique; ships at about 60-70 % of the width; the torpedo start sits just off the bottom; at most a far merchant pair at the top.
  2. **All dashed lines, arrows and rings removed.** Two real buoys replace them: gold ahead of the real bow, cyan ahead of the ghost's bow.
  3. **Torpedo and wake readable.** Dark torpedo with a warm nose glint and a big foam V; the wake is about 8 D wide (25-30 px). C shows a 34 D gap behind the real stern. Big bow waves and aft smoke on both ships; the periscope feather is hidden in topdown.
  4. **periscope_pov ghost.** Mirrored, offset -18 (bow about 28 % past the real stern), translucent body, emissive silhouette rim, its own bow wave.
  5. **Sea warmed and desaturated.** Teal near, blue far, warm face term and glitter. Blue chroma is 42 % (≤ 50, met). Red + orange is 18 % (**below the 20 % target**: open-water frames can't reach it while keeping the client's turquoise sea).
- **Client brief** (pretty toy-model ships, 1917 palette, warm teal sea) is applied to every ship in both locations, and a beauty tile was added.
- **Fixed during this round:**
  - The inverted-hull ghost rim filled the whole silhouette white through the translucent body; it is now limited to grazing faces.
  - The ghost foam used solid quads; it now has its own alpha-mapped foam material.
  - `set_flames` re-lit the hidden buoy lamps; they are now plain lights.
  - Variant dazzle images were saved without alpha, which turned the antifouling band black.
  - The quay_low DUSK brazier stood in front of the admiral; it was moved to the frame edge.
- **Checks:** no text, no DOF, all chins above y 880 (unchanged staging). `t_anim.py`: 38 checks, ALL OK.
- **Open:**
  - topdown C is at 25.3 CPU s (about 1 % over budget).
  - red + orange is under 20 % in the sea frames.
  - The torpedo_chase wake is still a broad white band near the camera (QA-art "not blocking").
  - The shade-hue metric now counts the teal sea and navy paint (see API §0).


## Round 4 (client detail pass): self re-check
- **Rules:** no DOF. No text: the background cards are cast placeholders, and crates and awnings carry no markings. The sea glitter and wave light are crisp cel bands rather than soft washes; an earlier soft-gradient warm term read as blur and was replaced.
- **Fixed during this round:**
  - Soft cloud reflections and a diagonal moiré on the swell: the sky mirror is now mostly a flat tint, and the chop is smaller and incommensurate.
  - topdown at 33.6 CPU s: the sea noises were reduced to one octave.
  - A new channel buoy sat in the periscope sightline and the topdown torpedo lane; it was moved.
- **Open:**
  - The topdown frames sit at about 30 CPU s, the budget edge.
  - beauty_harbour's lower half (warehouse roofs and wagons in shade) is dark at DUSK.
  - The background cards reuse 5 placeholder poses.
  - The torpedo_chase wake is still a broad white band.
Round 3 (toon sea) rejected by client 2026-11-18; restored round-2 sea from bak_r8. Toon version kept in bak_r9.
