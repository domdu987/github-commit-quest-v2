# QA-art — TAKE gate, film 20 key shots (2026-11-20, Opus)

Inputs: v3/film20/{s01,s15,s19,s21} take.mkv (s15 from its two parts), meta.json, framediff.json, shot.py; shot_plan rows 1/15/19/21;
QA_TEAM.md (client taste, QA-art, Stricter QA C); production-lessons §2 + §10; my set notes v3/set3d20/QA_ART.md (R5/R6).
Frames extracted at 2 fps at full size (720x1280) and at 360x640, plus single frames at the event g, in
/tmp/claude-0/-home-user-github-commit-quest-v2/ef039ac4-2646-5d6b-b692-04a5aa8620ca/scratchpad/takeart/<take>/ (full/, ph/, phone_row.jpg).
Frame numbers below are global g (take frame n = g - first_g).

Scores: set = set/staging density, light = light & colour, comp = composition & phone legibility, act = acting,
key = key-moment clarity & beauty, cam = camera rhythm.

| take | set | light | comp | act | key | cam | verdict |
|---|---|---|---|---|---|---|---|
| s01 HOOK | 7 | 8 | 5 | 6 | 7 | 8 | **FIX** |
| s15 FALSE PAYOFF | 6 | 8 | 5 | 7 | 7 | 6 | **FIX** |
| s19 REVEAL 1 | 5 | 6 | 4 | 4 | 3 | 3 | **FIX** |
| s21 REVEAL 2 | 7 | 7 | 6 | – | 5 | 7 | **FIX** |

No take passes yet. s01 and s15 need small fixes; s19 needs a re-block; s21 needs ring and glow fixes.

---

## s01 HOOK (g 0-79): FIX (small)
What works: a very strong first image. The whole orange tower, fully lit, fills a deep-blue sky behind Maupassant. You get the
Eiffel Tower at a glance at phone size. The camera moves on frame 0, and the snap on "เกลียดหอคอย" (g 25-40) is a clear beat
(p90 12.6). The sneer (g 0-26) and the squint-disgust (g 48+) both read at 360x640. The fair stalls, the dome and the flags give the
back half depth.

Problems:
1. **Lamp-post (the known item): reject it as is.** It is an unlit, untextured near-black pole with no lamp head. From g 0 to about
   g 24 it slants from the top edge down to the ground at x 30-230, crossing the sky right next to his head. At phone size it reads as
   a black scratch or render glitch over the most important second of the film, not as a lamp. After the snap a black diagonal sliver
   stays in the top-left corner until g 83. The bench beside it (g 0-24) is also a flat black slab with no wood.
2. The "turn away" (yaw +0.30 -> -0.85, g 45-53) does not read on the flat card. In the last second he is still square to the lens
   with a squint, so the beat is "squints" rather than "turns his nose away from the tower".

Fixes:
- F1 (g 0-83, shot.move_set_dressing): keep the lamp-post but make it a lamp. Give it the set's dark-green iron material with the
  lit lantern head in frame. Stand it upright: roll it so it is vertical in frame instead of slanting, or move it 0.5 m further left
  so it sits at x 0-60 and never crosses his silhouette or the tower. It must leave frame cleanly with the snap at g 25-40. **No
  sliver may stay in a corner after g 40**: if the move can't avoid that, hide the object from g 41.
- F2 (g 0-24): give the bench its wood material and the warm sun key (it renders black now), or move it 0.4 m right so only its end
  shows.
- F3 (g 45-60): sell the turn. Keep the yaw, but key head_roll -10 deg plus chin-up pitch +0.15 and slide the gaze hard right
  (gaze x +0.9) with the avoid expression, so the nose visibly points away from the tower. The hmph at g 61-66 stays.

## s15 FALSE PAYOFF (g 996-1092): FIX
What works: the tower legs, flags and pavilions are bright and warm. The sash and tricolour make the official readable. The red wax
seal reads even at phone size. The snap onto Eiffel (g 1064-1080) with the sweat drop and dropped smile is a clear, funny payoff
frame.

Problems:
1. The bottom 40-45 % of the frame is empty blue-grey ground at every frame before the snap. The two characters are small (head
   about 55 px at phone) and stand side by side with a gap between them. The plan asked for a "two-shot in depth", and the frame
   instead looks like a wide establishing shot with nothing near the lens. There is no FG prop, even though the set has the
   lamp-post and bench.
2. The handover (g 1008-1022) is only an arm stretch between two tiny figures, and you can't really read it at phone size.
3. The rhythm is flat until the snap: framediff p90 is 7.3 (target 12), and from g 996 to g 1060 it is a slow even drift.

Fixes:
- F1 (whole take): lower the camera aim and move the camera 30-35 % closer, or use 28 mm in place of 22 mm, so ground is at most
  25 % of the frame and the heads reach at least 85 px at phone size (about 170 px at full res). Keep the first-platform arch and
  flags in the top third.
- F2: stage it in depth. Put the official about 1 D nearer the lens on the right, with Eiffel behind him to the left, so the
  document travels toward the lens on the reach. Bring a fair FG (bench end, or 2-3 crowd card heads/hats at 1.5 D) into the bottom
  corner for parallax.
- F3 (g 1004-1012): add a small push-in (about x1.15, 8 f) on "ใบอนุญาต" so the seal handover lands as a beat and p90 reaches 12.
  Keep the existing snap at g 1064.

## s19 REVEAL 1 — antenna wire (g 1302-1381): FIX (re-block)
What works: the dusk palette (violet sky, lit orange tower, warm hut window) is beautiful. The glowing white wires read clearly
against the sky.

Problems:
1. **The reveal shape is wrong.** The plan says "starts on the summit, whip-tilt down along the wire to the ground". The take
   instead opens wide, with the whole tower, the wire, the hut and Eiffel all visible from frame 1. The whip (g 1343-1352) is a
   short pan right and down, so nothing is revealed: the wire's foot was on screen the whole time.
2. **Near-static holds:** framediff is 1.4-1.6 from g 1302 to g 1342 (1.4 s) and 1.1 from g 1356 to g 1381 (0.9 s). Median is 1.52
   (target 4). This breaks §10.
3. Old Eiffel is about 40 px tall at phone size. His "point up" reads as a hand near his hat. After the whip the left edge cuts
   him in half (g 1350-1381) and he stays cut.
4. The bottom 30-35 % is a flat, saturated blue ground (it reads as a pool of blue paint at phone size).

Fixes:
- F1 (g 1302-1342): **start tight on the summit.** Aim at SUMMIT with pitch about 40-45 deg (or 35 mm for g 1302-1342 only, back to
  22 mm by g 1352) so the lit spire top and the wire's top anchor fill the upper half. Add Old Eiffel's pointing arm and hat as a
  near FG silhouette at the bottom-left (1.2-1.5 D), so "he points up" and "the summit" share one frame. Keep a push of 8 %/s plus a
  slide of 40 px/s so the frame never rests.
- F2 (g 1343-1352): **real whip-tilt down the wire.** Lerp the aim from the summit to the wire foot (POST_AIM), with a pitch change
  of at least 30 deg and the yaw following the wire, peak 1.9. Allow 2-3 frames of motion streak, and land with the wire foot and the
  lit hut window at the centre.
- F3 (g 1353-1381): after the whip, push 9 %/s on the hut (no hold, frame-diff of at least 3). Frame Old Eiffel either fully in
  frame on the left third, pointing at the hut, or fully out. No half-body on the edge.
- F4: frame the ground so it is at most 20 % of the frame, or let the hut's warm window spill and the wagon cover it. Desaturate the
  ground shade about 15 %, staying inside hue 240-260.

## s21 REVEAL 2 — signal rings (g 1431-1559): FIX
What works: the whip pull-out from the summit (g 1428-1440) lands well: the summit, then the whole night tower with lamp necklaces,
trees, the lit avenue and the hut. The rhythm meets the target (median 9.3, p90 12.3). The night is a rich ultramarine with warm
lamp dots, and the tower reads instantly.

Problems:
1. **The rings do not read as coming FROM the top.** shot.py hides every ring while age < 0.1, so no ring is ever seen being born
   at the summit. Five or six large arcs are always on screen at once and cross the tower at mid-height. At phone size they read as
   a stack of white lines or a music stave behind the tower, not as ripples spreading out over Paris.
2. **The "whole lattice glows" moment (g 1530-1539) bleaches the tower** to a pale pink-grey ghost. It loses the Eiffel red and the
   warm lamps, and looks washed out rather than charged. At the same moment the wire turns into a thick white bar that leaves the
   frame toward the top-left, which is a new direction (before that it ran down the tower's face), so it reads as a stray beam.
3. Once the camera has pulled out, Paris is mostly hidden behind the trees and a single building, so "over the whole of Paris" is
   lost. The rooftop sea seen at g 1427-1431 is gone.

Fixes:
- F1 (rings, all frames, shot.rings): show the birth. Unhide rings from age 0 at radius 8-30 m with a bright small flash at the
  summit lamp. Keep only 3-4 rings alive (period 36 f, a ring every 9-12 f), with strength fading by radius
  (5 -> 0) so the outer arcs dissolve instead of stacking. This is the same as set note R5.
- F2 (g 1530-1559, S.wire_glow): build the glow as an ADDED blue-white emission (hue about 200, strength ramp 0 -> 1) on the
  lattice edges and the wires, over the red iron base. Don't lerp the base colour toward white. Check one frame at 360x640: the tower
  must still be red-orange with blue-white lines along it.
- F3 (wire, g 1520-1559): keep the wire's screen path the same as before the snap, from the summit down the face to the hut, or hide
  the far-left run that leaves the frame. No wire should cut across the empty sky.
- F4 (g 1441-1559): raise the camera 20-30 m (or tilt 3-4 deg down after the pull-out) so a band of lit Paris roofs is visible under
  the rings on both sides of the tower. Move the two near trees to the right of the axis out of the line of the hut and the city.

---

## s01 rev2 (commit df6d01b, re-checked 2026-11-20 at 4 fps full size + 2 fps 360x640): **PASS**
Scores: set 8 / light 8 / comp 8 / act 7 / key 8 / cam 8. F1 done: the lamp-post is now upright dark-green iron with a lit lantern at the
left edge (x 0-60). It never crosses his face or the tower, and it is gone after the snap with no corner sliver. F3 done: the head roll
plus chin-up after g45 reads as "nose away" at phone size, together with the squint. §G: sat 0.567 / luma 97 are in band. Feet touch the
ground with contact shadows, and no bar passes through a face. The face is at most 18 % of frame height, nothing floats, and he is not
cut by a side edge (the waist cut after the snap is a normal medium shot).
Non-blocking note: F2 is only partly done. For g 0-20 the bench shows as a dark grey sliver at the right edge (x 620-720). It is
acceptable, but the wood should read lighter if this take is ever re-rendered.
§H film-level flag for the director: s01 is 2.67 s, so it cannot hold a 3-6 s BIGZOOM. shot_plan.md has no BIGZOOM marked yet. The
hook BIGZOOM has to be planned elsewhere (or s01 re-planned); this does not block this take.
