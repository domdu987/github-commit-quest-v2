# s01 v4 TAKE gate re-check (QA-art + tech), film 14 hook, g0-186, cuts g66/g123 (round 4)

## VERDICT: FAIL (1 blocking: shot 3 gesture still does not read as a sweep/point)

Frames: qa_recheck4/all (every frame g0-186), sheets in qa_recheck4/sheets: pop0 (g0-5), hang_a/hang_b (g28-68 every 2nd),
s3 (every 6th, shot 3), zoom_s3 (g144-186 every 3rd, crop on the farmer), phone (every 6th at 135x240 with y830/y880 lines),
full_a..d (720x1280 with px grid, y830 yellow / y880 cyan). Also judged the team's phone_sheet.jpg.

Tech (every frame, 180x320 L1 diff): median 1.96. Cuts g65->66 57.6 and g122->123 54.9, exactly on plan.
g0->g1 2.67 (= neighbours 2.7-2.9; v3 was 6.9). Only other run above 2x median is g23-44 (4.0-6.0, peak g32-35):
the camera pitch/pan + hive travel of the hang, smooth ramp up and down, no single-frame spike. Shot 3 flat 1.2-1.7
(slow drift, no jump). No frozen frames (min diff > 0.3), no black, no magenta. 187 frames, 30 fps, 720x1280.

## v3 blocking items
1. g0-1 farmer-card pop: FIXED. g0 and g1 identical in card size/position (hat, face, hive, bees); diff g0->g1 is normal.
2. Hang landing: FIXED. Same hive carried g0-30, travels onto the hanger g30-44 with his hands on the bar while the camera
   pitches down/left with it (14 frames + ~20 frames of camera ease; reads as a placed hang, not a drop). Landed hive at
   g44-65 is under the roof, left-centre, fully in frame: x ~45-360, y ~670-845. Bottom edge ~15 px past the 830 wish, still
   well above 880 (note only). His soles are on the rungs (y ~935-965) after the hang.
3. Shot 3 sweep + ground: PARTLY -> still blocking.
   Sweep: the left arm rises g147-159 and holds g159-186, but it ends bent, upright beside his head with the hand hidden behind
   the head/hat brim (x ~520-560, y ~700-760). No extended arm, no visible hand pointing at the peak (peak x ~480, y ~430,
   up-left of him). Full size it reads as "hand behind the head / scratching"; at phone size the gesture is invisible
   (phone.jpg g162-186, phone_sheet g165/g180 look like a standing man). The team's own QA.md calls it "more arm up than a point".
   Ground: PARTLY. Bare/low-plant ground from ~y 880-900 to 1280 = ~30 % (v3 ~37 %, target <= 25 %); sky is ~34 %, so the
   farmer (hat-to-feet ~690-1080) is small in the lower half. Polish-level on its own.
Shot 2 laughing villagers: FIXED. Elder, kid (yellow cap) and youth (blue cap) all eyes squeezed, open grins, tear drops;
   reads as laughing at him. Woman still cut by the right edge (note).
Kid chin above y 830: FIXED. Shot 1 kid (green shirt) chin ~740-800 (g44-65), shot 2 kid chin ~650.

## Heads above y 880
All OK. Shot 1 farmer ~460-640, woman ~510-600, kid <= 800; shot 2 all heads 380-660; shot 3 farmer head ~690-820.

## New / notes (non-blocking)
- Shot 1 g0-30: the bottom of the held hive dips to y ~880-890 (into the caption band) before the hang; a bee or two at ~900.
- Shot 1: the kid is now mostly hidden (behind the hive g0-30, behind the farmer's arm g36-65, only a face sliver); the
  mockery is carried by the woman (laugh with tears, clear). Acceptable since shot 2 carries the kid laughing.
- Shot 3: farmer drifts right with the pan; at g186 hat/veil reaches x ~710 (touching the right edge).
- Shot 2: bottom ~38 % still bare ground with long shadows (as v3).
- Shot 1: ~40 % ground under the ladder (y 880-1280) after the camera pitch down (empty but has the ladder/feet).

## Phone read, first 2 s (g0-60)
Yes. Beekeeper hat on a ladder with a big hive and bees, woman laughing with tears beside him, mountain and acacias; reads in
< 1 s. The hang now reads (hive slides onto the bar under the roof, stays in frame). Kid barely registers in shot 1.

## Blocking (send back)
1. Shot 3 g148-186: the point must read. Fix: left arm fully extended up-left toward the peak (shoulder ~x 540,y 790 ->
   hand ~x 400-450, y ~600-650), hand silhouetted clear of the head/hat, not behind it; hold g164-186. Keep the pan, but stop
   the drift so he stays >= 40 px inside the right edge. If cheap, tilt up/push in so ground <= 25 % (not required).
Everything else in this take passes; only shot 3 frames g148-186 need re-rendering.
