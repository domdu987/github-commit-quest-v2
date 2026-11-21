# QA-art: film 23 set (r1), look/SET approval

Checked at full size: set_sheet.jpg (19 shots, first/mid/last), set_finals.jpg, NOTES.md, GROUND_SET.md, shot_plan.md, cast_sheet.jpg. Reference: film/ref/a (deep, saturated, warm practicals against blue night).
Ground: 18 537 checks, 0 FAIL. Nothing floats; S12/S13 tank lift and S19 balloon are the planned airborne exceptions.

## FIELDS: **FIX** (S01)
1. First frame: drop the straight-down camera. Start as a high OBLIQUE view (about 120 D up, pitched 35-45 deg down), aimed along the lane at the detailed square, with the dawn horizon in the top 20 %. Then descend and push as now.
2. Hide the edge of the detailed square. Carry hedges, trees and lane strips past its border, or keep the border out of every frame of the descent. The flat voronoi tiles may only appear far off, never as the subject.
3. Last frame: move the camera off the hedge block, which is now a dark purple wall over the left 40 %. Frame the lead tank 3/4 on, with the waving soldier's head at 0.40-0.55 of frame height.
4. Re-measure shade hue on the new first frame. The target is 240-260; 216 now.

## LANE: **PASS**
The set is vivid, dense and well lit (warm sun against violet shade). Render teams may start. The shots listed below must change before they render.

## CAMP: **PASS**
The moon rim against the lantern pools and the orange tent works, and the frames are rich. Shot fixes are below.

## RHINE: **FIX** (S14-S18)
1. Remove the haze and lavender cast. Cut the ambient/world emission on the ground and remove the mist layers. Ground lit at hue 215-230, shade at navy 245-250, 8-15 % of pixels below value 0.25. Sandbags and crates should read khaki/wood, not pink.
2. Warm against cool: put 2-3x the lantern power on the decoy field, with warm pools of 1.5-2 D and lit truck cabs and tent glow. The balloon field must read as glowing from across the river (S17).
3. Foregrounds: in S14 the lower 45 % is empty, in S16 the lower 55 % is bare grey ground, and in S15 the first frame shows pink reed sticks. Dress the near bank 1-2 D from the lens with crate stacks, folded-rubber bundles, a pump, a lantern and rope coils.
4. River: make it deep navy with a clear moon path and warm lantern streaks in the reflections, and lower the frequency of the ripple noise. Right now it reads as blue static.
5. Rebuild S18. Move the camera low and oblique (2-3 D above the water). Run the pontoon bridge diagonally through the frame, put a boat with paddlers and the dog 3-5 D from the lens, and keep the far-bank troops and trees busy. Add a warm orange band on the pre-dawn horizon against the blue. Water may fill no more than about 35 % of the frame.
6. Shade hue: S14-S16 measure 235-237 and S18 231. Tint the ambient on sky_night_r and on the ground to hue 248.

## Per-shot notes (must change before render)
- **S01**: see FIELDS.
- **S04**: in the last frame the foreground soldier's head is in y 880-950. End the crane higher, or move the mark about 1 D up-frame.
- **S09**: in the last frame the sound man's head sits at about y 900-1000. End the push higher, or move him so his head centre is at y ≤ 760.
- **S10**: in the mid frame the "U.S. ARMY" crate text sits at about y 930. Move the crate or the camera so the text is below y 960. In the first frame, put radio sets and a map on the flat orange tent wall.
- **S12**: shade hue 233 (lane dirt) and 264 (mid). Set the per-surface ambient on the dirt to hue 248.
- **S13**: the cyclists leave the frame; in the last frame only a hand and a wheel are left. Key them to brake and stop by the mid frame (the plan says "cyclists stare, one falls off"). Track the camera so both stay at x 0.15-0.85, heads above y 860 (the beret head touches y 880 in the first frame).
- **S14-S18**: see RHINE.
- **S17**: the left observer is cut off at the frame edge. Slide the camera so both Germans are whole and the far field fills the band behind them.
- **S19**: in the first frame the "DECOY M4" text is at about y 925. Lower the crate or start the camera higher. Shade hue 273 (violet under the pile): tint the shadow on the grass under the pile toward blue (248).
- **S07**: mid shade hue 236. Use the same dirt-ambient fix as S12.

## Director acceptance of the FIELDS/RHINE fix round (2026-11-21)
FIELDS S01: all 4 fixes applied (oblique start 120 D up, end 3/4 on lead tank, hue 241) -> PASS.
RHINE: no lavender cast, warm lantern pools vs navy, river reflections, dressed foregrounds, S17 observers whole -> PASS for render.
Accepted deviations (night exterior, allowed by the skill's hue note): shade hue 227-234, dark share low, S16 mid luma 62.
Team 3 shot notes: S16 lift exposure a little (lanterns/cab glow) so luma ≥ 70; S18 add a second boat and keep water ≤ 40 % by tilting up.
