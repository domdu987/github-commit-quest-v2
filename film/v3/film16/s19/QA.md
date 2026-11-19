# s19 QA: film 16, shot 19 (LINE line_wide, DAY) -- revision 2 (after the TAKE gate)
- Delivered: g 1217..1276 (60 f): shot g 1226..1267, 9-f handles each side (dissolve in 13 f from shot 18). 7 spp, ~8.8 s/frame wall. QA_AUTO PASS.
- Gate fixes:
  1. No pop: the real set pole 3 is parented to a pivot at its foot and tilts from 40 deg to the vertical (eased) over g 1217-1258; it settles into place at g 1258 and the shot's hand props are gone (they were the cause of the swap). meta/cues now say pole_planted_wire_on 1258 (the frame it happens).
  2. Hands keep the pole: both hands of Morse and each worker are pinned to the real pole (hand heights 2.3-2.9 D) on every frame, and the crew walks forward with the rising pole; they hold it after it is planted (hand error <= 1.3 D on the far worker, <= 0.6 D others).
  3. The wire: span pole 2 -> pole 3 top (bare, straight on the wood) switches on when the pole is planted; the pole top and the wire stay in frame after the snap.
  4. Morse + both workers are in frame in every frame (worker_b at the left, worker_a red at the right edge at the end, partly overlapped by the edge only in the handle).
  5. Eye-lines: gaze (0.9, -1.0) = up the pole to its top, expression determined.
  6. The clipped slabs / dark holes at the bottom were the furrow leftovers (trench_* / pipe_* meshes clipped to zero length that still cast ground shadows); hidden at runtime. The ground is clean.
- Camera: wide (start distance ~9 D, heads 77-130 px: wide shot), snap x1.65 g 1243..1256 with a 1.8 D pan landing as the pole is planted, slide -85 px/s, slow pull; heads y 710-810, max head bottom 871 (< 880 inside the shot).
- Frame-diff: median 4.71, p90 12.26 (targets 4 / 12).
- Differs: light is plain DAY (no overcast variant in the set). Characters stand at marks near the pole base, not morse_wide.
