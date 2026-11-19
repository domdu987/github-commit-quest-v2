# QA reveal round 3 - combined QA-art + QA-tech TAKE gate, film 13 s21 s22 s24 s25 (team 6 round 3)
Reviewer: QA-art (Opus) acting as combined reviewer. Inputs: QA_ART_keys3.md blocking items, QA_TECH_s21_r2.md / s24_r2 / s25_r2
blocking items, QA_TEAM.md standard checks, production-lessons.md section 2, client extras (no round-blob dust/smoke/halos; people on
moving things move with them). s17 shot 19, s20 and s23 passed earlier and were not re-delivered (used here only for the joins).
Method: every frame decoded; qa_auto per take; 360x640 phone sheets (1 frame / 0.5 s, red line = y 880); dense/full-res crops;
pixel measurements; join sheet of last/first shot frames s20 -> s25.
Scratch: /tmp/claude-0/-home-user-github-commit-quest-v2/f68faafd-58e7-5eaf-b5d5-5d4b103780c5/scratchpad/qaart13b4/
(<take>_phone.jpg, s21_swing.jpg, s21_faces.jpg, s21_bottom.jpg, s21_debris_s25top.jpg, s22_cap.jpg, s22_contact.jpg, s24_gap.jpg,
s24_lamp.jpg, joins.jpg, <take>_QA_AUTO.md/). i = take frame index, g = first_g + i.

| take | qa_auto | verdict |
|---|---|---|
| s21 bars together | PASS (66 fr) | **PASS** |
| s22 jack close | PASS (63 fr) | **FIX-FIRST** (2 fixes) |
| s24 aha wide | PASS (77 fr) | **FIX-FIRST** (3 fixes) |
| s25 thousands of jacks | PASS (90 fr) | **FIX-FIRST** (regression: open-air pit again) |

---------------------------------------------------------------------------------------------------------------
## s21 (g 1356-1421). PASS
- Keys3 blocking item fixed: camera now held; the beam underside measured at y 594 -> 574 -> 554 full-res (i0-14 / i26-40 / i52-65),
  i.e. a clean ~10 px step on phone at each swing, 20 px total, at the moment all bars swing. Unison swing reads (all bars end-on at
  i19-22 and i45-48, no wave). Cellar with beams and lamps, no sky; continuity s20 -> s21 -> s22 good.
- Workers' feet stay on the floor, bars at hand height - fixes the riding-blocks note. Mouths closed/grimace. Heads y ~560-700 (< 880).
- QA-tech r2 item 1: the brick-textured navy slab is gone. What remains bottom-left (x ~170-420, y ~1190-1280) is an untextured soft
  shadow, consistent with the other jack shadows - not debris. A dark hex shape below the near jack base at i50 (g 1406) is the swinging
  bar end / its shadow, 1-3 frames in motion. No white shards found. Not blocking.
Non-blocking: lower ~30 % is floor/mud with angular shadows (mostly under the caption); a tiny background worker shows a red open mouth
around i30 - close it if anything is re-rendered.

## s22 (g 1410-1472). FIX-FIRST
Fixed: camera height locked; chalk line on the post top; the screw cap climbs ~60-80 px full-res (~35 px on phone) past the chalk line
across the swing - the rise is now measurable; the half turn of the bar reads.
Blocking:
1. The cap still touches nothing (keys3 item 1 not fixed). Full-res crops (s22_contact.jpg, i4 and i58) show a clear band of orange lamp
   light between the cap top and the beams/boards above for the whole take; the "bearing plank on the cap" from the team's notes is not
   visible in frame. Put a visible plank/beam resting ON the cap (distinct colour from the ceiling, inside the frame above the cap,
   phone y ~250-300) and raise it with the cap, so the image is "the jack pushes the beam up".
2. Caption band: the worker's face (white area) spans y 818-1004 full-res from i36 to the end, centre y ~900-916 - his head is at/below
   the y 880 line and the caption (y ~856-944) will cover his face. Raise the worker / tilt the camera down so his head centre is <= 800
   (or move him higher in frame by framing the jack from a little lower), keeping the cap + plank in the upper third.
Non-blocking: worker half off the left edge at i0-20.

## s24 (g 1531-1607). FIX-FIRST
Fixed: side-on view, the hotel on a lit band of jacks + cribbing across the base (~95 px full-res, ~48 px on phone), stair to the side
on the ground, QA-tech's dark wedges beside the awnings / leaning boxes no longer seen.
Blocking:
1. Workers in the gap (keys3 + QA-tech item 1, still open): only ONE tiny worker (red) is visible, half hidden behind a jack (s24_gap.jpg).
   Place 5-8 tiny worker cards clearly inside the lit gap between the cribbing stacks, in front of the jacks, feet on the ground, heads
   well below the hotel underside (and <= y 840), one with arms raised/cheering.
2. Jump cut s23 -> s24 (joins.jpg): s24 opens on almost the same side-on angle, hotel position and scale as the last frame of s23 - it
   reads as a jump, not as the "aha wide". Go clearly wider (camera much further back / higher, lens 17): the whole hotel front with both
   corners on its cribbing, the gap band running the full width, the street and people tiny. This also fills the empty lower 45 % of mud.
3. Round glow halo: the street lamp head carries a pale round halo against the sky (y ~260-420 full-res, visible on the phone sheet) -
   client rule "no halos". Remove the glow sprite (or turn the daytime lamp off).

## s25 (g 1596-1685). FIX-FIRST - regression
Now ~5000 jacks from a high 36 deg view, unison swing (the field flips together at i60) - "thousands" is achieved. But:
Blocking:
1. It is an OPEN-AIR PIT again: pale yellow sky with lilac slab clouds and a horizon/flat desert across the top ~25 %, brick rim walls,
   no hotel, no beams, nothing above the jacks (s21_debris_s25top.jpg). This is exactly the round-1/keys2 root cause (a) and breaks
   continuity with s20/s21/s22 (enclosed cellar) - the viewer no longer sees that the jacks are holding up the hotel.
2. At phone size the field is a uniform moire texture; no worker is readable; the bars cannot be seen turning, only a brightness flip.
Fix: keep the dense field but frame it INSIDE the cellar: camera just under the joists (about 3-4 D above the floor), looking down
25-35 deg along the aisles, the beam grid / hotel underside filling the top 15-25 % of the frame (no sky, no horizon, no rim walls),
rows of jacks receding to lamp-lit depth; near rows large enough that jacks, bars and worker cards read (>= 20-30 px per jack on phone);
workers in the aisles; all bars swing on one beat (g 1612-1624 / 1650-1662); slow rise or drift inside the cellar.

---------------------------------------------------------------------------------------------------------------
## Joins (joins.jpg)
s20 -> s21 cellar -> cellar OK; s21 -> s22 OK; s22 -> s23 cellar -> street OK; s23 -> s24 near jump cut (s24 fix 2); s24 -> s25 street ->
open-air pit breaks the "under the hotel" space (s25 fix 1).

## Summary
PASS: s21. FIX-FIRST: s22 (plank on the cap; head out of the caption band), s24 (5-8 visible workers in the gap; go much wider to avoid
the jump cut from s23; remove the lamp halo), s25 (put the dense field back under the hotel's beams, no sky; readable jacks/workers).
