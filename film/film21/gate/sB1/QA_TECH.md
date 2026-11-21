# QA-tech sB1 v3 (team7 e6f1968)

## Verdict: FAIL (1 blocking: blue pavilions in the English camp)
Method: all 29 sheet frames (every 5th, g159-299) in 6-up strips, g298, g219, g274 and g159/g301 at full size from take.mkv (143 frames, 720x1280, g159-301). Colour brightness and saturation judged as normalized; content only.

## Beat table
| g | beat | result |
|---|---|---|
| 159-200 | high over the valley, glide south over river, bridge at left | Reads. Camp is a cluster of tiny tents (blue-violet, see issue 1). Hills navy, fields murky purple/brown, orange meadow at left. Cut in at g159 is fine (hard cut from A2). |
| 200-245 | steep dive onto the camp | Reads as motion; tent domes, striped pavilions, smoke wisps, parade column visible. Much brighter than v2 (no murk). Still violet in the shade. g231 soft = streak, accepted. |
| 245-270 | levelling out, "ENGLISH CAMP" sign appears | Sign first readable about g255 (small), clear from about g270. |
| 270-298 | approach, land at P_CAMP | Sign legible, white text on dark board, fills about 35 % of width at g298. Knights on caparisoned red/gold horses parade right of the sign (7.74 s = g292). Smoke plumes and light shafts visible. |
| 299-301 | handles | Continue the same move (sign and flag grow), no jump. meta cam_out "P_CAMP at g298 continuing NE". |

## Checks
- Camera: one continuous eased move, rhythm median 11.2 / p90 18.2, 0 cuts, no pops. End matches P_CAMP (camp_wide) by the team's meta; sign left of centre, flag and tent in the foreground as in the preset. I could not check the pose numerically.
- Heads: all cast tiny, well above y 880 and mostly in y 600-860 at g298. No face over 35 %. Nobody cut by the frame edge. No mouths visible. No blood.
- Floating: nothing floats. Contact shadows are present.
- Characters acting: parade riders and footmen are tiny, read as a moving column. Weak on a phone, see issue 3.
- Banners/smoke near the lens: none. The red flag pole in the foreground (g259-301) grows toward the lens and its base leaves the bottom edge at g294-301. It is a set prop, not a character; non-blocking.
- Regression vs old report: murk fixed, red/lime neon gone, smoke is now thin wisps and no longer grey slabs, sign readable earlier. The meadow at the bottom is still a flat green (see issue 4).

## Issues
1. BLOCKING, g159-250 (and in a lighter form g255-301): blue pavilions in the English camp. Many white and pale tents render saturated blue-violet (sampled g219 tent domes at rgb 85,71,222 and 95,74,198; g159-200 camp reads as a blue/purple cluster). The big white tent in the foreground at g255-301 has violet-blue faces, and the pale tent under the sign at g298 is lavender. The brief says NO blue in the English camp. The worker's own notes say the blue variants were removed, so this is probably the white/default tent material taking the cool shade or sky bounce light. Fix: give the pale tents a warm ivory or cream base and cut the cool ambient or shade tint on tents in this segment. Re-check at g159-250 and the foreground tent. Mid-dive violet in the shade needs the same warm lift.
2. Non-blocking, g159-245: the valley beyond the camp is navy-indigo (hills) and murky purple (fields). It is not neon and not pink, but it is cold next to the warm camp. Optional fix: warmer hill and field tint in the valley_wide to camp transition so it matches the set palette in B2 and A2.
3. Non-blocking, g270-298: the parade is small (riders about 30-40 px). It reads as a parade of red/gold riders in front of the sign but is weak on a phone. Optional fix: end or dip about 10 % lower or closer, only if P_CAMP is kept.
4. Non-blocking, g255-301: the lower 40 % of the frame is plain green meadow, with only a flag and one tent in the foreground. Optional fix: props, a horse line or a fence in the foreground.
5. Non-blocking, g270-301: the sign board is dark navy. It is a sign, not a pavilion, caparison, shield, banner or surcoat, so I do not count it as English blue, but a dark brown or black board would be safer.
