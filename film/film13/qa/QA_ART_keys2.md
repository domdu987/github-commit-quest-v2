# QA-art, TAKE gate, film 13 key takes, round 2 (s17 re-render, s26 re-render, reveal/aha s20-s25)
Reviewer: QA-art (Opus). Rules: film/QA_TEAM.md (QA-art + Stricter QA C), production-lessons.md section 2, client extras
(no round-blob splash/dust/smoke - a splash needs a spray crown + droplets; characters on moving things move with them).
Judged on 360x640 phone sheets (1 frame / 0.5 s, red line = y 880) plus dense crops.
Scratch: /tmp/claude-0/-home-user-github-commit-quest-v2/f68faafd-58e7-5eaf-b5d5-5d4b103780c5/scratchpad/qaart13b2/
(<take>_phone.jpg, s21_dense.jpg, s22_dense.jpg, s17_q2_dense.jpg, s17_crops.jpg, s26_fall_dense.jpg, s26_purse_dense.jpg, full frames).
i = take frame index, g = first_g + i.

| take | density | light/colour | composition | acting | key moment | match | verdict |
|---|---|---|---|---|---|---|---|
| s17 false payoff | 7 | 7 | 6 | 7 | 6 (Q2 cup 4) | 7 | **FIX-FIRST** (one fix, shot 19) |
| s20 whistle | 6 | 8 | 6 | 7 | 7 | 7 | **PASS** |
| s21 bars together | 7 | 7 | 6 | 5 | **3** | 4 | **FIX-FIRST** |
| s22 jack close | 6 | 8 | 6 | 5 | **3** | 6 | **FIX-FIRST** |
| s23 hotel rises | 7 | 8 | 5 | 6 | **2** | 5 | **FIX-FIRST** |
| s24 aha wide | 7 | 8 | 5 | 5 | **3** | 6 | **FIX-FIRST** |
| s25 thousands of jacks | 4 | 6 | 5 | - | **3** | 3 | **FIX-FIRST** |
| s26 ending | 8 | 8 | 7 | 7 | 7 (purse 4) | 8 | **FIX-FIRST** (light, shot 30) |

The one-image mechanism (whistle -> 500 men turn TOGETHER -> the hotel rises evenly) does NOT read on the phone yet. Three root causes:
(a) s21 and s25 are an open-air pit under the sky with nothing above the jacks (small loose plank pads) - no hotel, no floor beams.
    It reads as a field of machines, not "under the hotel", and it contradicts s20/s22 (closed cellar with beams).
(b) Nothing ever moves UP in a way the eye can measure: no shot shows jack -> beam -> building rising against a fixed reference.
(c) s25 levers turn in a diagonal WAVE - the opposite of "together".

---------------------------------------------------------------------------------------------------------------
## s17 (shots 17-19). FIX-FIRST, one blocking fix
Better than round 1: room dressed (wallpaper, chandelier, window wall, patterned rug <= 30 %), shot 17 has the half-lidded smug face
with cup at chest and the city far below; shot 18 now shows two tea discs, flat and still, with the window behind - still reads
"nothing moved" (i75-150). Mouth only in Q2.
Blocking:
1. Shot 19 (i151-201): the raised cup sits at the extreme LEFT frame edge (x ~0-40 of 720), half cut off; he is also cropped at the
   edge, and the top 30 % is empty purple ceiling with chandelier drips. The Q2 toast does not read. Reframe (pan/truck left ~150 px or
   move the cast right) so he stands in the left third with the cup fully in frame, raised in front of / beside his face on the open
   side, and tilt down so the ceiling is <= 15 %.
Non-blocking: shot 17 he still faces camera more than the glass; fine since the smug look reads.

## s20 (shot 20, whistle). PASS
Pullman centred among the jack columns under the beams, warm lamp glow; the arm goes up and the whistle goes to the mouth at i45-60
(g 1339-1354, on 'นกหวีดดัง' g ~1344). Reads. Note: lower 40 % is bare reflective planks; a few workers by the jacks in the background
would help the cut to s21 (non-blocking).

## s21 (shot 21, 500 men turn TOGETHER). FIX-FIRST - the most important image of the film
- Open sky with cartoon clouds above the pit (whole take): no floor/hotel above the jacks. Each jack carries a loose square pad. The
  viewer cannot see what is being lifted. Continuity break vs s20/s22 (beam ceiling).
- The bars are thin grey 1-2 px lines at phone size; across i0-60 they sit at mixed angles, so a synchronized half turn is not visible.
  Worker poses barely change.
Fixes:
1. Put the hotel's floor/beam grid (as in s20/s22) over the whole field, lit from below by the lamps; frame high-angle from inside the
   cellar so beams top-of-frame and the rows below are both in shot. No sky.
2. Make the bars thick (3-4x), light-coloured, and key ALL bars at the same angle at the whistle, then all swing 180 deg together in
   ~12 frames with every worker leaning into it in the same pose (one big unison gesture), hold, and the beams above move up a visible
   step (>= 8-12 px on phone) at the same moment.

## s22 (shot 22, one jack close). FIX-FIRST
- The bar is a thin rod that pokes out behind the jack; across i0-60 it moves only slightly; no half-turn arc, the screw does not
  visibly climb, the beam above does not lift (s22_dense.jpg).
- The worker sits on a block in the left half, legs splayed; the jack head is half-hidden behind his body.
Fixes: frame jack + bar + beam contact in one shot (cap of the screw meeting the beam in upper third, worker's hands on the bar in the
middle). Bar thick and long; he pushes it through a clear 180 deg arc (~15 frames); the threads visibly spiral up and the cap/beam rise
by a hair that is still >= 6-8 px at phone size (add a chalk mark or a gap line against a fixed post as the reference).

## s23 (shot 23, outside: the hotel rises evenly). FIX-FIRST
- Same failure as round-1 s01: the camera cranes up while the lift goes up, so in frame the facade moves DOWN (portico y ~170 -> ~240
  on phone, i0 -> i75). The stair runs from the ground to the portico and no cribbing/void is visible under the building, so nothing
  says "rising".
- Bottom-left a white smeared round blob (puddle reflection) from i45 on - reads as a blob, client rule.
Fixes:
1. Lock the camera (or slow push in only) and frame a corner of the hotel side-on so the base line, the growing void with lit cribbing
   and jacks under the ground floor, and a fixed reference (lamp post / neighbour shop / worker) are all visible; key h 0.5 -> 0.8 so the
   base climbs >= 60 px on phone, level at both corners.
2. Detach the stair (it stays on the ground while the building rises away from it) - this also sets up the ending.
3. Remove the white puddle blob.

## s24 (shot 24, aha: high on cribbing, no machine). FIX-FIRST
- The cribbing is a thin glowing strip (~60 px full-res, y 860-940) mostly hidden by four workers and the stair that runs to the ground;
  the hotel reads as standing on the street, not high. A brown box on two legs (stool/cart?) in the foreground grows toward camera and
  is a confusing prop; mud fills the lower 30 %.
Fixes: raise h to 0.9 as planned so a dark void + stacked cribbing band of >= 120 px full-res runs the whole width; move the workers to
stand UNDER the hotel inside the void (tiny, for scale) instead of in front of it; frame a little lower/three-quarter so the band is at
y 600-800; remove the box prop.

## s25 (shot 25, thousands of jacks turning together). FIX-FIRST
- Open-air pit under sky again, no hotel/beams above, no workers, monotone orange field that ends as a flat texture at i45-89.
- Levers turn in a diagonal WAVE (team QA.md) - this says "one after another", the opposite of the story fact (all at once).
Fixes: put the beam grid/hotel underside above (lamps glowing between beams), add worker cards in the aisles, and make all levers turn
in unison on one beat (no wave). If the shot rises, rise inside the cellar toward the beams, not out into the sky.

## s26 (shots 26-30, ending). FIX-FIRST (light, one blocking fix)
Big improvement. Shot 26/27 (i0-95): door and portico sit high on lit cribbing and jacks, he is visible in the doorway from i0, panic
face reads. Shot 28 (i96-195): side-on, the stair stops low with the cribbing between it and the portico - the 2 m drop now reads on
the phone. Shot 29 (i196-234): he steps off, hat flies, tumbles past the cribbing into the mud, a spiky brown crown with flying bits
(i213-222) - acceptable as a crown, not a blob. Waist-deep in mud, hat on head, dizzy: good.
Blocking:
1. Shot 30 purse (i235-320): the purse first lies beside him / then simply hangs from Pullman's hand; the rich man never holds or
   offers it (no raised arm). The pay-off "he must pay, as he said" does not read. Stage it: purse in HIS raised hand (i ~240-265),
   Pullman's hand meets it and takes it (i ~270-285), Pullman holds it up a moment, the rich man sulks.
Non-blocking: the splash shards are wood-coloured spikes - darker wet brown with a few round droplets would read more as mud; the
ground around the hole is dry tan - darken a wet ring around it.

---------------------------------------------------------------------------------------------------------------
## Summary
PASS: s20. FIX-FIRST light: s17 (shot 19 cup framing), s26 (shot 30 purse handover). FIX-FIRST heavy: s21, s22, s23, s24, s25 -
the reveal/aha does not yet show the one-image mechanism. Priority: (1) put the hotel underside/beams over the jack field in s21/s25 and
make the turn a single unison beat with a visible rise; (2) s23 locked-camera side-on rise with a growing void and a detached stair;
(3) s24 high on a thick cribbing band with tiny workers underneath; (4) s22 visible half-turn arc and screw climb.
