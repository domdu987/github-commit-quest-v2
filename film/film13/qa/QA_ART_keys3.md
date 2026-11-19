# QA-art, TAKE gate, film 13 key takes, round 3 (s17 shot 19, reveal/aha s21-s25)
Reviewer: QA-art (Opus). Rules: film/QA_TEAM.md (QA-art + Stricter QA C), production-lessons.md section 2, client extras
(no round-blob dust/smoke/halos; people on moving things move with them). Previous notes: QA_ART_keys2.md.
Judged on 360x640 phone sheets (1 frame / 0.5 s, red line = y 880) plus dense crops; i = take frame index, g = first_g + i.
Scratch: /tmp/claude-0/-home-user-github-commit-quest-v2/f68faafd-58e7-5eaf-b5d5-5d4b103780c5/scratchpad/qaart13b3/
(<take>_phone.jpg, s21_swing.jpg, s21_step.jpg, s21_dense.jpg, s22_dense.jpg, s22_cap.jpg, s23_base.jpg, s17_cup.jpg, all frames in <take>/).

| take | round-2 blocking fixes | verdict |
|---|---|---|
| s17 (shot 19 only) | cup framing fixed | **PASS** |
| s20 whistle | (context, passed in round 2) | PASS (unchanged) |
| s21 bars together | cellar + beams fixed; thick bars + unison swing fixed; beam step NOT visible | **FIX-FIRST** (one fix) |
| s22 jack close | one-frame jack+bar+post fixed; swing reads; cap does not touch the beam, rise not measurable | **FIX-FIRST** |
| s23 hotel rises | locked camera, growing lit gap, stair stays down, blob gone - all fixed | **PASS** |
| s24 aha wide | gap still hidden, no workers, foreground planks | **FIX-FIRST** |
| s25 thousands of jacks | ceiling + workers + unison fixed; not "thousands", not high-wide, repeats s21 | **FIX-FIRST** |

---------------------------------------------------------------------------------------------------------------
## s17 shot 19 (i151-201). PASS
Rich man in the left third, cup + saucer fully in frame, raised beside his face on the open side with the hand under it (s17_cup.jpg,
i155/i190); lady and gentleman fully in frame; ceiling ~15-18 %. Q2 toast reads. Shots 17-18 unchanged (passed).
Non-blocking: the cup is small on phone (~27 px); a touch bigger/closer would help, not required.

## s21 (shot 21). FIX-FIRST, one blocking fix
Fixed: enclosed cellar under the hotel's beam grid, no sky, warm lamps between jacks (continuity with s20 good). Bars are thick blue
rods, all at one angle, and swing TOGETHER: at i19-22 (g 1375-1378) every bar in the field turns end-on at the same moment, then all
lie flat again at i25 - unison reads on the phone. Workers hold the bar ends in one pose.
Blocking:
1. The beams do not visibly step up. The step is 0.08 D per swing while the camera trucks ~5.5 D forward and rises 0.1 D during the shot,
   so the beam line and bar line sit at the same y before and after each swing (s21_step.jpg i12/i28/i38/i54: beam underside and bar
   line move < 3 px on phone). Fix: hold the camera still (or slow push only, no z change) from g 1366 to g 1412, and make the step
   read: lift >= 0.2 D per swing (or move the camera closer so the nearest beam is ~4 D away), so the main beam and every jack head jump
   >= 10-12 px on phone in the 12 swing frames. A lit gap line between the near beam and a fixed timber post/wall mark would make it
   unmistakable.
Non-blocking: the bar line runs across the workers' mouths/noses at camera height - camera 0.3-0.5 D higher would separate faces from
bars; workers riding up on visible dark blocks looks odd (they stand on the cellar floor, not on the hotel) - better to keep feet on
the floor and let the hands/bar rise.

## s22 (shot 22). FIX-FIRST
Fixed: screw cap, bar and a timber post in one frame; the bar makes a readable half turn (i18 pointing right -> i27 end-on -> i33 across
behind), the threads lengthen a little.
Blocking:
1. The screw cap does not touch anything: a band of orange lamp light shows between the cap and the beam/ceiling above it for the whole
   take (s22_cap.jpg i6/i20/i34/i56). The jack is not lifting the hotel in the picture. Put a beam (or a bearing plank under the beam)
   sitting ON the cap, in the upper third, and lift both together.
2. The rise is not measurable: cap top moves ~7 px on phone while the camera also rises 0.1 D, and the cream mark on the post is not
   legible at phone size. Lock camera z, make the mark a bright chalk line (>= 6 px tall on phone) on the post right at the cap/beam
   line at i0, and let cap + beam climb >= 10 px above it by the end of the swing (i33).
Non-blocking: before the swing (i0-20) the worker is half off the left edge; bar crosses his mouth after the swing.

## s23 (shot 23). PASS
Camera near-locked, side-on: the hotel base climbs and a warm lit void with jacks and cribbing opens under it (gap ~5 px -> ~40 px on
phone, s23_base.jpg i0/i40/i81); the stair stays on the ground and a gap opens between its top and the portico - this reads and sets up
the ending. No puddle blob; ground glints are vertical streaks, not round blobs.
Non-blocking: at the end the jack tops sit slightly below the building's underside (thin light line between them) - lift the jack
heads/cribbing with the building so it is carried, not hovering; base rise ~38 px on phone (asked >= 60) is enough because the gap
reads.

## s24 (shot 24, aha). FIX-FIRST
Front-low, straight on the portico: the wide grand stair fills the middle third and hides the void; the gap is only a thin glowing line
behind the stair top at i45-75 (phone y ~340); no workers anywhere; the lower third is a pile of foreground planks that slides out of
frame. The aha "high on cribbing, no machine, tiny workers beneath" does not read.
Fixes:
1. Shoot from a three-quarter / side angle (like s23 but wider, lens 17, further back) so the stair is not between camera and the void;
   at h 0.85 -> 1.0 the dark void + stacked cribbing band must run the whole width and be >= 60 px tall on phone (y ~300-400).
2. Put 5-10 tiny worker cards standing INSIDE the void under the hotel (feet on the ground, heads well below the underside) for scale.
3. Remove the foreground plank pile; keep the stair standing on the ground at one side with the visible gap to the door.

## s25 (shot 25). FIX-FIRST
Fixed: beam ceiling above, workers in the aisles, bars swing in unison (i60, no wave). But it is the same low eye-level framing as s21
(camera at bar height, one band of jacks at y 300-420, top 45 % bare ceiling, lower 35 % bare dirt); ~207 jacks, it reads as "a row of
jacks again", not "thousands", and there is no high wide / slow rise.
Fixes:
1. Camera high under the beams (just below the joists) looking down ~25-35 deg along the aisles, lens 18, so dozens of rows of jack
   heads + bars + workers recede to a lamp-lit vanishing point and fill >= 60 % of the frame; slow rise/drift inside the cellar.
2. Use the dense field (s15's under_rows dense build / set_jack_count high) so the far rows read as thousands; more lamps glowing
   between rows to give depth.
3. Keep the unison swing on one beat (g 1612-1624 and/or 1650-1662) - from above the 180 deg arcs of all bars will read as one
   synchronized pattern.

---------------------------------------------------------------------------------------------------------------
## Summary
PASS: s17 (shot 19), s23 (s20 stays PASS). FIX-FIRST: s21 (visible beam step only), s22 (cap must touch the beam + legible rise vs a
mark), s24 (side/three-quarter wide with a full-width void and tiny workers, no stair in front), s25 (high wide over a dense field).
