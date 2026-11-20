# s15 QA (merged shots 15 + 16): film 19, SHIP ship_deck NOON, ONE continuous take (QA_TEAM §I: no cut inside)

## Delivered
- `take.mkv` (libx264rgb crf 6, 73.6 MB, split in `take.mkv.partaa/ab`; `cat take.mkv.part* > take.mkv`): g 1086..1288 = 203 frames, first_g 1086. Shot range g 1096..1279 (36.52-42.65 s, 184 f); handle in g 1086..1095 (10 f, DIS 15 in from s14), out g 1280..1288 (9 f; hard CUT to s17 at g 1280). 720x1280, 11 spp, 2 threads. `qa_auto` PASS. meta.json (shots [15, 16]), cues.json, contact.jpg, phone_sheet.jpg, framediff.json. **The s16 folder is dropped** (this take replaces it).
- Built on the colour-fixed set (film19/main ff204d3 merged).

## Shot (no cut)
| g | beat |
|---|---|
| 1096-1163 | "ความลับคือ เที่ยงวันกลางทะเล ดวงอาทิตย์": William aims the quadrant straight up (angle -85, pitch -0.45), the captain shades his eyes and looks up; two sailors haul a rope in the background (a heave every 1.2 s); `set_sun_overhead` 0 -> 1 on every frame; camera drifts in (push 10 %/s, slide, small arc) |
| 1164-1184 | SNAP / tilt up toward the sun on "อยู่ตรงหัว" (38.98 = g 1172): a camera-parented sun glare disc + halo fades in at the top right; both stay fully in frame |
| 1186-1207 | with no cut the camera cranes back down and away from the sun (zoom x0.47), William lowers the quadrant and brings the H4 (scale 2.0) out on his palm; the captain steps in and drops his hand; the sun glare fades out |
| 1208-1228 | SNAP push to William on "บอกเวลาที่" (40.5 = g 1218), H4 held in front of his chest toward the lens |
| 1229-1288 | medium shot, H4 readable (~100-120 px dial), push 10 %/s with a slow arc; captain leans in to look at the watch (pitch +0.1, gaze to the hand), sailors keep hauling |

## Checks
- Ship ride: cards parented to ship_root (parent inverse taken at t = 0), camera `C.on_ship`, `set_sea` / `set_roll` / `set_sun_overhead` keyed with the same t on every frame; feet and contact shadows on the deck in every frame.
- Frame: heads centre y 444-726 in shot, width 50 (the far sailor) - 217 px (William / captain), lowest head bottom 835; face width at the end 195-215 px = under 30 % of the frame; both William and the captain fully inside the frame for the whole shot (captain left edge >= ~40 px, William right edge <= ~714 px).
- Colour (`film/qa_stats.py`): **saturation 0.434, brightness 124.5** (target sat >= 0.40, luma 70-135).
- Frame-diff (in-shot pairs, 90x160 grey): **median 4.08, p90 10.70** (draft 4.07 / 10.54); the whole file incl. handles: median 4.63 / p90 11.68. Weak spot: the last 2 s (g 1230-1279) sit at ~2.8: the flat sail / deck gives little diff and the pair fills the frame, so there is no room for more parallax.
- No DOF, no text, no caption_shade; mouths still (nobody speaks). Nobody stands still for more than 1.5 s: William / the captain sway and blink every 0.4-1.5 s, the sailors haul.
- s/frame: 23.2 wall / 45.0 cpu.

## Differs from the plan / known
- The sun is a screen-space glare (camera-parented disc), not a set object; it fades in on the snap and out during the crane down.
- The captain's mark moves 0.6 D (feet glide, legs stand) while the camera pulls away (g 1188-1214) so he is beside William for the watch.
- The hauling sailors' rope end floats in the air (cast pose rope19); they are small and in the background.
- After the pull-back the heads sit at y ~600 (above the 880 band, within the 450-760 range).
