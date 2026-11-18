# s01 v3 TAKE gate re-check (QA-art + tech), film 14 hook, g0-186, cuts g66/g123

## VERDICT: FAIL (3 blocking, all small/local)

Frames: qa_recheck/all (every frame), qa_recheck/f6 (6 fps + cuts ±3), sheets in qa_recheck/sheets
(phone_a/b = 180x320 phone size with y880 line, pop0, hang, cut66, cut123, full_* = 720x1280 with y840/y880 lines, zoom_kid, zoom_feet).
Numbers (every frame, 180x320 L1 diff): median 2.61. Cuts g66 (49.5) and g123 (39.0) exactly on plan.
Other spikes: g0->g1 6.9 (2.6x median, a pop), g33-40 5.9-7.6 (the hive tween, spread over 8 frames, no single spike).
No frozen run (no frame diff < 0.3). No black/magenta frames.

## v2 blocking items
- A. Hive in hands from g0: FIXED for the hive (hive + bar in his hands at g0, no hive pop).
  BUT NEW pop g0->g1: at g0 the farmer card is ~20 % larger and ~70 px further left/up (hat 220-560 x vs 995-1210-720), then snaps
  to its real key at g1; background and ladder do not move, so it is the card, not the camera. It is the first frame of the film.
- B. Hang continuous, same hive: PARTLY. No swap/teleport any more (same hive, tweened g33-40). But the tween is ~7 frames (0.25 s)
  and the hive slides down-left and shrinks away from his hands; it ends at the far-left edge, cut by the frame edge, at y ~780-960,
  i.e. in the caption band. On the phone it reads as "he dropped/slid it off", not "he hung it". His hands are empty from g36.
- C. Kid head above y 840, not cut by the edge: FIXED (borderline). Kid fully in frame from g0-65, cap top ~725-740, chin ~835-845
  at g44-65 (touches 840, well above 880). g0-35 the bottom of the held hive overlaps the top of his head (reads as behind, ok).
  (QA.md's "y 735-800" is cap-to-eyes, not the chin.)
- Shot 2 sky <= ~20 % and a bigger farmer: FIXED. Pure sky ~12-15 %, ~20-25 % incl. gaps around the acacia; farmer hat-to-feet
  ~415 px (v2 ~250).
- Shot 3 less ground, real sweep, ladder behind hive: PARTLY.
  Ladder: FIXED (no longer in front of the hive; stands right, behind the farmer).
  Ground: NOT really: bare laterite y ~800-1280 = ~37 % of the frame (v2 ~45 %), only a rock and two sticks.
  Sweep: NOT: g150-180 is a forearm lift to the right at shoulder height holding the stick; no full-arm extension, and it points
  right into the maize, away from the mountain (peak at x ~480, he is at x ~560-670 pointing to x 700+). Pan is a small drift.

## Other checks
- Heads vs y 880: all OK in all three shots (shot 2 villagers ~500-640, shot 3 farmer ~500-650, kid shot 1 chin ~840).
- Contact shadows: shot 1 kid ok (dark patch at ~y 900); shot 2 blue shadow patches under villagers ok; shot 3 farmer's feet
  (y ~860-875) have almost no contact shadow (note).
- Ladder parenting: shot 1 after the hang (g44-65) his legs end ~y 845, soles ~y 900 sit at/right of the right rail, half off the
  rung (reads as hanging beside the ladder); no slide seen. Shot 2 feet on the platform/rung at y ~630, no slide. OK-ish (note).
- Acting (note): shot 2 villagers now wide-eyed with round "O" mouths, they read as shocked/alarmed, not as laughing at him.
  The mockery beat is carried only by shot 1 (kid/woman laughing with tears). Youth (blue cap) partly covered by a maize leaf card;
  woman cut by the right edge in shot 2.
- Shot 2 bottom ~40 % (y 760-1280) is grass tufts + shadows on bare ground (note; sky fixed, ground now empty).
- Continuity (note): shot 1/3 shelter is a lean-to roof with the hive hanging under a bar; shot 2 shows a gable roof with the hive
  on a bar. Check it is the same structure from another side.
- Mouths: no talking. Sharp, no DOF.

## Phone read, first 2 s (g0-60)
Yes for the core image: beekeeper hat on a ladder holding a big hive with bees, kid and woman laughing at him, mountain/acacias,
reads in < 1 s. The hang does not read: the hive slides off to the bottom-left and ends half off-frame under the caption band.

## Blocking (send back)
1. g0: farmer card pop (larger, shifted) for one frame, then snaps at g1. Fix: re-render g0 with the same farmer key as g1
   (key the card/hooks on frame 0 too).
2. g32-65: hang ends at the left edge, cut off, at y ~780-960 (caption band), and the 7-frame slide reads as a drop. Fix: move the
   hanger (or frame/pan left with the hive) so the hung hive lands in the middle third (x ~120-450, y <= 820) fully in frame;
   stretch the move to 12-15 frames with his hands on the bar until it hooks, release after.
3. g148-180 (shot 3): no real sweep and it points away from the mountain. Fix: full arm extended up-left toward the peak (or pan so
   the hills are on his pointing side), held >= 15 frames, camera follows the hand; at the same time lift framing ~0.4 m so the
   bare ground is <= 25 %.

## Non-blocking notes
Shot 2 villager expressions read as shock (prefer laugh-with-tears like shot 1); shot 2 empty ground ~40 %; youth behind a leaf,
woman cut at right; shot 1 post-hang feet half off the rung; shot 3 farmer contact shadow weak; kid chin touching y 840.
