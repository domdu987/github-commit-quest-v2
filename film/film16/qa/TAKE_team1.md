# TAKE gate QA-tech, film 16, render team 1 (takes s02, s03, s25, s27) -- branch render16/team1 @ 4592c9d
Method: ffmpeg decode of every frame, 6 fps sheets plus every cut +-3 frames viewed, frame-diff recomputed (90x160 grey, mean abs diff of consecutive in-shot frames), film/qa_auto.py run on each take.mkv (all four: PASS, 0 % magenta, no frozen/black frames, no unplanned pops).
No take.mkv was split (all single files).

| take | verdict | frame-diff median / p90 (recomputed, in-shot) |
|---|---|---|
| s02 (shot 2) | PASS (notes) | 7.69 / 34.35 (whip g69-80 inflates p90; post-whip g81-109 ~7.2 flat) |
| s03 (shot 3) | PASS (notes) | 6.89 / 16.65 (snap g157-170 peaks 19) |
| s25 (shot 25) | FAIL | 17.95 / 30.38 (wipe g1615-1626 inflates; post-wipe g1627-1706 median ~16) |
| s27 (shot 27) | FAIL | 5.99 / 15.43 (snap g1770-1781 peaks 16.6) |
(Team-reported numbers differ slightly (5.29/27.48, 5.39/13.02, 14.26/29.06, 4.61/13.83): different resize filter. Both pass 4/12 everywhere.)

## s02 -- PASS
Heads: all in-shot heads above y 880 (head bottom max ~739 in shot; the meta's 893 is on handle frames g60-66 where he is off-screen). Heads 106-158 px (wide range OK). Feet on the grass with a contact shadow. Mouth still (smile only). Camera never parked (min diff 6.3). Cut in at g69 is mid-whip (diff 42 -> 8 by g80), correct for the plan's one whip. Row of teal bottle-neck poles marches to the horizon, ladder at the pole, train creeping at left. No text, no DOF, no black/magenta.
NOTES (non-blocking):
1. g69-72: only fence + wheat visible (whip arrival), Morse enters frame left at g70; fine as whip, but poles are not readable until g73.
2. g85-109: lower 40 % of the frame is empty grass whose texture looks soft/blurry (low-res ground texture stretched). Not DOF, but reads as blur. Fix if re-rendered: bigger grass texture or foreground props (spool/crate) in the lower third.
3. Morse's eyes look at the camera, not down the line he points along. Fix: eye-line toward the pole row (head/eye swap or pose with gaze right).
4. Planned poles are small (bottle necks only just visible at phone size); nudge the camera lower/closer to a near pole if re-rendered.
5. s02 end g109 (+/-3 g107-112 checked): smooth continuation, no pop. Continuity into s03: costume/colours identical, ladder hidden in s03 as intended.

## s03 -- PASS
Heads above 880 (head bottom max 810, at the snap peak). Contact shadow under boots, scale OK, grin only (mouth never moves, no speech). Train rolls past behind the pole line, moves -x with smoke trailing back: direction consistent. Snap on "รถไฟ" g157-170 lands on the word (5.24 s -> g160). No pop at the cut +-3 (g107-113, g165-171). No text, no DOF.
NOTES:
1. Plan beat "taps the wire": the wire is only a sliver at the top-right corner and Morse points at the train instead (team disclosed). Acceptable because "รถไฟ" is the word, but if re-rendered put the wire/pole top into frame or make the tap visible.
2. Eye-line: Morse looks at the camera while pointing at the train. Fix: gaze toward the train.
3. Steam from the loco becomes a floating chain of white balls disconnected from the funnel (g131-169, set design). Reads cartoon-ish; fix in the set (puff size variation / fade) for the next set revision.
4. g121-131: pole shaft crosses the torso in front of the coat for a few frames (depth ordering), minor.

## s25 -- FAIL (1 blocking)
Heads: no characters. No black/magenta; one soft frame g1607 is the intended wipe edge. Object wipe (red carriage panel) fully covers g1609-1626, so the dissolve at g1615 is hidden, ok (the wipe's panel has uniform red + window frame, no text).
BLOCKING:
1. g1656-1706 (about 50 frames = 1.7 s of a 3.07 s shot, plus the first 12 frames are the wipe so only ~1.3 s shows the train): the train is gone from frame by g1666 (last sliver of cowcatcher at g1666-1671); frames g1676-1706 show only empty field, a pole and the pulse dash on the wire. Plan beat "the train races along the rail; the pulse overtakes it and leaves it far behind" is therefore not visible: the overtake (g1646-1656) happens with the loco cropped at the right edge and nothing shows the train "far behind". The camera outruns the train (26.6 D/s vs 12 D/s) so the train leaves frame to the right; the viewer sees only an empty landscape. Fix: lower the camera track speed to ~15-17 D/s (or add a gentle pull-back/crane up on the snap) so loco + at least one carriage stay in frame until about g1680, then let the pulse pull away to the left while the train is still visible, small, at the right of frame; keep the snap on "บัลติมอร์" (g1643-1656) but frame the overtake with the loco centred. Re-run qa_auto afterwards.
NOTES:
2. The pulse is a thin cyan dash with a small white head (about 15 px); legibility on the phone sheet is marginal against the clouds. Fix: bigger glowing head (2x), longer comet tail.
3. g1636-1656: train is small (wide) and low in frame, lower half is fence/field; consider lowering the camera so the loco is bigger.
4. Black birds sitting on the wire (g1636-1696) are a nice touch but one is placed ON the pulse path (g1671, g1696) and the pulse passes through them; remove or move them.
5. Frame-diff median is inflated by the wipe; post-wipe it is ~16, fine.

## s27 -- FAIL (1 blocking)
Heads above 880 (max bottom 771), heads 69-153 px, feet on the platform with shadows, waving hands attached, no mouth speech (grins only), snap on "ก่อนรถไฟตั้ง" g1768-1782 correct. Cut +-3 (g1764-1770, g1802-1808): no pop. No text/DOF/black. Dissolve out (planned shot 28) fine.
BLOCKING:
1. Plan beat "the train only now puffing in, late" is not readable. Until g1795 no train is visible at all (lower 45 % of the frame is an orange/red slab with a white stripe and rails); from g1795-1813 only a grey boxy cowcatcher/boiler corner enters the lower right (no smoke, no wheels, no funnel), which reads as an abstract grey wedge, not a train. The shot also loses the station sign / lamp post per the team's own note. Fix: place the camera so the loco (funnel + smoke puff + boiler front) is visible in the right third from about g1785, e.g. camera on the platform side looking along the rail with the group in the left third and the loco entering from the right at medium scale; accept heads of ~90-110 px, or put the camera 2.5-3 D back from the rail and use the pull-back to reveal the loco. Add a smoke plume rising above the loco so it reads as "puffing". Remove the orange slab dominating the lower half (crop it with a lower camera pitch or a higher look point).
NOTES:
2. Eye-lines: all four platform people look at the camera, not at the arriving train. Fix: look toward the right (train) for at least two of them; waving at the camera is OK for the others.
3. The crate pile hides two people's legs (team disclosed); acceptable.
4. Frame-diff passes (5.99 / 15.43) but the first 10 frames (g1767-1769 before the snap) sit at 4.4-5.5, close to the floor; keep the snap on the word.
