# QA — film21 segment I (the AHA, bridge jam) — redo after the TAKE gate

take.mkv: g 1519-1639 (121 frames @30 fps), 720x1280, 32 samples, ~60 s/frame. Cut in, no handles.

## Gate fixes
1. English all crimson and gold: second rider recoloured (crimson surcoat, red great helm, gold caparison; bare-headed variant after the pop), column mats red/gold only. Done with a manual recolour in c21.py (not the new cast21 defaults from film21/main 528bf9d, which I had not pulled when these finals were rendered).
2. Final crane ends directly over the bridge, looking down its length, the jammed column two by two filling the frame vertically; no tents. VIVID eased to (1.4, 1.1, 0.9) at the top (set default for the ride).
3. Nose-to-tail beat: ride camera raised ~1 m so legs and heads show; the two horses end up nose into rump.
4. Popped helmet: bright bascinet with crimson plume, slow spin (reads as a helmet).
5. Mouths: shocked open mouths held still, nobody speaks.
Kept: ride-along, helmet pop (f62), snap pull-out on "เหมือนกัน" (local f89).

## Automated
- qa_auto.py: PASS; rhythm.py: 0 cuts, median 8.93, p90 23.32 OK
- qa_stats.py: sat 0.673, brightness 77.0 (below the 85-110 band; per director policy luma/yellow cast is normalised at the conform, no re-render)
- qa_stats2.py: vivid 77.6 %

## Known weaknesses
- Mean luma 77 (dark water in the ride); terrain in the crane is still bright yellow.
- Bridge is narrow in the crane (~20 % of width) because the deck is 2.6 m wide.
- ~30 % of the ride frame is dark water.
- path_draft.mp4 = 25 frames, 10 fps, final camera path.
