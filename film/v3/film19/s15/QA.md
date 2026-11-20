# s15 QA (merged shots 15 + 16): film 19, SHIP ship_deck NOON, ONE continuous take (QA_TEAM §I: no cut inside)

## Delivered
- `take.mkv` (libx264rgb crf 6, 62.7 MB, split in `take.mkv.partaa/ab`; `cat take.mkv.part* > take.mkv`): g 1086..1288 = 203 frames, first_g 1086. Shot range g 1096..1279 (36.52-42.65 s, 184 f); handle in g 1086..1095 (10 f, DIS 15 in from s14), out g 1280..1288 (9 f; hard CUT to s17 at g 1280). 720x1280, 11 spp, 2 threads. `qa_auto` PASS. meta.json (shots [15, 16]), cues.json, contact.jpg, phone_sheet.jpg, framediff.json. **The s16 folder is dropped** (this take replaces it).
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
## Round 8 (director review: the MECHANISM must read on a phone) - whole take re-rendered, g 1086..1288
1. **Sun overhead reads at the snap (g 1172):** the sun is a bright disc (+halo) now parented 2.5 D from the lens (it used to sit behind the main sail), top-CENTRE (360,125), fading in on the snap; the camera tilts up so William's quadrant points straight up under it and the deck falls to the bottom ~25 % (heads y ~745). From g 1171 the sails stop casting the big diagonal shadow (visible_shadow keyed off during the snap, the pop hidden in the whip): a pool under the feet remains; `set_sun_overhead` is 1 by g 1176.
2. **Home time contrast:** the H4's hands now show 8:00 (cast19 `_h4_body` patched at runtime in shot.py: hour hand at 8, minute at 12); on "บอกเวลาที่" (g 1218) the camera pushes in x1.75 and the watch pops to scale 3.0 for ~1 s: dial ~170-190 px at 720x1280 (faces 270 px = 37 % at the peak only), then it eases back to a medium shot (faces ~215 px, 30 %). No lid engraving.
3. **Sun and watch in ONE frame (g 1229-1288):** the sun fades back in at the top (g 1226-1250) while a slow crane-up / arc keeps the watch at the bottom of the pair; the pair is centred.
4. **Nobody still > 1.5 s:** William sights and adjusts the quadrant (hand, angle +-6 deg, glint, lean, head roll every 0.5-1 s), the captain shifts weight, moves his shading hand and turns his head; from g 1236 the captain leans 0.2 D toward the watch and looks surprised (expr `shocked`), William glances up at the sun and back to the watch (g 1238-1262). The two sailors haul in a 1.2 s loop and stay inside the frame (marks moved in: (3.1, -25.0) and (-2.7, -24.6)); the captain stands beside William for the whole take (mark offset 1.6 / 1.15 D: no glide).
5. **Deck foreground:** two rope coils, two buckets and a grating on the quarterdeck planks in front of the lens (parented to ship_root); the deck is under ~25 % of the frame from the snap on, ~40 % in the first second (the coil / bucket pieces fill its corners).
6. **Colour:** exposure -0.62 EV (-0.3 more), grade saturation 1.32, deeper blue sky ramp, sails darkened ~18 %, all set from shot.py (the set is unchanged): **`film/qa_stats.py`: saturation 0.509, brightness 108.4.**

## Round 9 (director: QA-tech blockers + polish) - whole take re-rendered, g 1086..1288
1. **Sun no longer blinks:** the 3D glare card (which faded out during the crane down and made a faint square in the denoiser) is gone. The sun is now an image-space overlay (`sunfx.py`, applied in `deliver.py`, screen blend, radial alpha falloff to 0, no card edge): it fades in once (halo g 1154-1168, 6 frames BEFORE the disc g 1160-1172) and then stays steady to g 1288 through the dial push.
2. **William's eyes are OPEN** (expr `neutral` + smile) for the whole H4 phase: he looks at the watch, glances up at the sun (g 1238-1262) and back down; his eyes are visible in every frame.
3. **Square edge:** gone with the card (see 1).
4. **Bloom before the disc:** halo first, disc 6 frames later with a 5 px soft rim.
5. **Sun x:** 560 px during g 1166-1190 (straight above William's raised quadrant), gliding to top-centre 360 by g 1230 (the pair is centred there).
6. **Sail shadow:** the sails, spanker and jibs stop casting one after another from g 1146 to 1172 (the diagonal shadow shortens and goes before the snap ends); only the pool under their feet remains.
7. **Captain's hat brim air:** he stands 0.1 D closer to William (mark offset 1.7 / 1.15) and the dial-push zoom is x1.79 after a deeper pull-back (x0.65): the captain's hat brim keeps >= 70 px from the left edge from g 1218 to the end (the brim is estimated at 20 % of the head width beyond the head disc), William's brim <= ~715 px.

## Round 10 (director: the glance) - g 1186..1288 re-rendered
Note: in the frames the half-lid frown that snapped open at g 1248 was the CAPTAIN (the left figure; William is the right one with the watch). Both are fixed.
1. **William:** ring (open) eyes with a smile (expr `excited`, mouth `smile`) for the whole H4 phase from g ~1196 (he looks at the watch, pupils low); the glance: g 1236-1241 head pitch -0.32 and roll +11 deg, pupils at the very top of the eye whites (gaze y -1.2), held g 1241-1248, back down g 1248-1254 to the watch.
2. **Captain:** ring eyes (expr `shocked`, closed mouth) from the reveal (g ~1200) instead of half-lid slits; the mouth stays closed and opens over ~10 frames g 1234-1246 (("open", w, h) blended), no one-frame snap.
3. **Exposure:** scene exposure keyed -0.62 -> -0.82 EV over g 1188-1204 (the sails' base colour is texture driven, so a base-colour tweak did nothing); the sun is a post overlay and stays as is. Whole-file brightness 113.6 -> 110.8 (about 105 in the last 2 s).

## Round 11 (director: p90 margin) - g 1186..1288 re-rendered; glance, eyes and mouth blend unchanged
- **Stronger dial push:** the pull-back before it is deeper (x0.55 instead of x0.65, g 1188-1206) and the dial push x2.12 (net framing unchanged: faces 235 px = 33 % at the peak, hat brims inside the frame: captain's >= ~55 px from the left edge, William's <= ~705 px), so both snaps move faster.
- **More life in the last second:** from g 1250 a second drift segment (CAM_C: push 10 %/s, slide -50 px/s, arc -9 deg/s, continuing from the pose at g 1250) keeps the frame moving to the end; the last pairs went from ~1.7 to ~3.0; William's right brim <= ~695 px, the captain's left brim >= ~120 px, the sailors stay inside.
- Env overrides `B_PARAMS` / `C_PARAMS` in shot.py were used for the tuning (defaults = the delivered values).

## Numbers (final)
- QA's method (ffmpeg bilinear 90x160 grey, pairs g 1097..1279, on the joined parts): **median 4.87, p90 11.11**. deliver.py: median 4.52 / p90 9.87.
- `film/qa_stats.py`: **saturation 0.511, brightness 111.1** (the -0.2 EV from round 10 is kept); `qa_auto` PASS.
- Heads in shot: centre y 430-773, width 50-237; one format: `take.mkv.partaa/partab`.
