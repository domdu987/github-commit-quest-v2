# TAKE8 QA s03 (T03, round 6) - verdict: PASS with notes

Measured on frames g170-411 (all frames for luma/motion; contact sheet of g171/180/190/200/210/370/374/378/385/411 viewed).

## Round-7 blocker (deck underside) - FIXED
- Near-black share (luma<25) top 35 %: g370 7.6 %, g380 5.5 %, g390 5.0 %, g411 3.2 % (was 51 % at g378-382). Peak 7.6 % at g370; luma<40 share peaks 15 %. Underside reads as lit orange-brown wood.
- Mean luma g374-411: 89.9 (min 84.7), was 64-75. Target 85-110 met.
- Brightness ramp g362-376: luma 119 -> 117 -> 108 -> 103 -> 100 -> 92 -> 88; steps <= 4 per frame, monotone, no pop/flicker. (The drop is the dark deck entering frame, smooth.) Frame-to-frame diff 10 -> 34 over g361-375 is camera move, no spike; take max 40.2 at g324 (the known whip pan), motion median 13.8, p90 31.3.
- White bulb / smoke: gone at g366-380 (only the small dark crane hook at the left edge, reads as a hook).

## g170-215
- Warm marker: yellow-orange dot, no white core (white-ish px >235 = 0 at g171-190), gone by ~g190. OK. Gravel disc: not visible at g200/210. OK.
- Seams: g215->216 luma 112.1 -> 112.0, diff 8.5 (neighbours 8.2); g339->340 luma 104.9 -> 104.8, diff 25.1 (neighbours 25.2). No jump.

## Dissolve s03 -> s06
- Handle frames g396-411: s03 luma 91 -> 89, s06 81; step ~9 (was 8), mean abs diff ~52-56 (different scenes, as in prior rounds). 13-frame dissolve hides it; clean.

## Notes (not blocking)
- Marker is small (~12 px); Eiffel himself still ~1-3 px until ~g190 (known, accepted soft pass in TAKE7).
- Luma falls 119 -> 85 over g362-378 (scene content); fine under the dissolve ramp.
- Dark brown flat plate underside of the deck still the largest dark mass at g378 (~15 % of top is <40) but reads as wood.
