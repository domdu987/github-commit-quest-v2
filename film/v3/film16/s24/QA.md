# s24 QA (v2, after the TAKE gate): film 16, shot 24 (the REVEAL macro) -- LINE bottle_macro, AFTER_RAIN

## What changed against v1 (TAKE gate / QA-art: no dark wet pole, pulse parked instead of carrying on, flat static end, qa_auto blur flag, cut-off wire stub)
- **Dark wet pole in frame:** field-side camera (ladder hidden), glass in the upper third, the pole fills the centre from the glass down to the wheat for the whole shot. The pole's texture-driven base colour is multiplied by (0.34, 0.31, 0.38) and glossier. Cyan appears ONLY in the glass and on the wire: the pole stays dead dark under the glowing neck, and the glass above it lights up only while the pulse is inside it (g 1553-1560).
- **The pulse carries on:** one comet (TG.set_pulse, keyed every frame) comes along the wire from the left, slides into the glass at g 1556 (glass glows cyan, rim highlight) and runs on along the outgoing wire to the right, trail tapering to the wire, until it leaves the frame (about g 1582). It travels screen-LEFT to RIGHT.
- **Sky <= 40 %:** hills, wet field, rail and far trees fill the lower half; the pole and neck the centre.
- **qa_auto:** PASS (the v1 blur flag came from a sky-only whip; the whip now has the pole, trees and rail in view).
- **Static ending:** slow push 9 %/s, slide 70 px/s and arc -15 deg/s give a slow orbit round the glass and the pole to the end.
- Sun glare: the wet ground washed out the first frames (white blob); the ground wetness is set to 0.15 for this shot (puddles hidden), the pole stays dark by its own darkening.
- Not done: the weak sparks creeping down at the rim (small emissive spheres are in the build, keyed g 1568-1600, but are too small to read at 720 px); the pulse light is linked to the glass only, which is what keeps the pole dark.

## Round 2 (director's request): what changed
- **Wet look on the pole:** a thin specular streak up the sun-lit side, four clear drips that creep down the pole (keyed per frame), and a small dark glossy puddle at its foot (a flat ellipse, roughness 0.32).
- **Wider camera:** level, 8.5 D off the line, so the whole pole down to its foot and puddle is in frame for the first second: ground, rail, road, crates and the spool fill the lower half, hills and trees the middle; sky about 40 %. A slow push, then the snap (x1.35, 13 f) on "ไม่รั่วลงเสา" lifts the framing onto the neck and the dark pole under it; the foot goes out of frame after the push.
- **Neck glow held 11 frames:** the pulse head sits inside the glass from g 1556 to 1567 (barely creeping), so the glass glows cyan for 11 frames ("อยู่แต่ในลวด" 1561), then the pulse runs on along the outgoing wire to the right.
- **Frame-diff:** median 4.77, p90 12.75 (target >= 4 / >= 12): MET. qa_auto PASS (no blur flag).
- Not done: the weak sparks at the rim (still too small to read); the puddle is dark but small, and the ground wetness stays 0.15 (sun glare), so the ground itself reads dry.

## Delivered
- take.mkv: 93 frames, g 1531..1623 (shot g 1540..1614, 9 handle frames each side), 24.4 MB. Hard cuts in (1540) and out (1615).
- QA_AUTO.md (PASS), phone_sheet.jpg, contact.jpg, cues.json, meta.json, framediff.json.

## Beats
| g | beat |
|---|---|
| 1540-1555 | pulse runs along the wire from the left ("ไฟเลยวิ่ง" 1543); camera pans with it (6-7 f lag) |
| 1556-1560 | head enters the glass: glass glows cyan ("อยู่แต่ในลวด" 1561); pole below dark |
| 1560-1582 | pulse continues along the outgoing wire and out of frame |
| 1579-1592 | snap push x1.35 onto the neck and the dark pole on "ไม่รั่วลงเสา" (1582) |
| 1592-1614 | slow orbit on the dead dark pole under the unlit glass ("สักหยด" 1604) |

## Frame-diff (in-shot g 1541..1614)
median 4.1  p90 12.47  (target >= 4 / >= 12): MET (just).

## Checked
- No text, no DOF, no cast, no magenta; glass is the shared clear dense bottle-green; nothing in the caption band but pole and field.
- 7.9 s/frame wall, 15.18 s CPU (720x1280, 7 spp, 2 procs x 2 threads).
