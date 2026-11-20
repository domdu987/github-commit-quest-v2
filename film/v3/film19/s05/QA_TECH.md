# s05 QA_TECH: FAIL
Shot 5, SHIP ship_rocks STORM_DUSK, take g253-364 (handles 9+9, out side DIS 13), 6 fps + cuts g262/g356 +-3 checked. qa_auto PASS. No text, no black/magenta, no frozen run, no blur. Frame-diff re-measured median 6.22, p90 21.73: OK. Spike g332-333 (diff ~30) = the planned ONE shake (g330): OK. Mouths: expressions only, no lip-sync: OK. Heads in band (foreground sailor head centre y ~ 650).
## Issues
1. g268-363: plan says sailors (plural) bail in buckets. Only the foreground sailor bails (scoop arc seen g283, g303, g323, g343). The other two sailors are tiny and stacked behind the captain, overlapping each other and the captain's shoulder; no visible bucket action. Fix: spread the three sailors in depth/x (marks), each with a bucket, so three arcs read.
2. g268-308: the red-bandana sailor stands/hangs on top of the rail bulwark (feet above the bulwark top edge). WORKER19 §6: keep characters off the rail bulwark. Fix: restage inboard on the deck.
3. g283-343: the captain is half covered by the sail/mast edge (right half of body hidden), reads as clipped. Fix: move him 0.5 D to the right/inboard.
4. g263-264: the foreground sailor is clipped by the right frame edge as he enters (arm/leg cut). Acceptable on a whip entrance, but g263-265 hold 3 frames; shorten to the first 2 frames.
5. g268-363: black round/rectangular silhouettes at bottom right (cannon, bottom-right corner) render solid black (set note says violet) and a box at the bottom left; they read as black blobs. Fix: lift the ambient on the cannon material or crop them out of the FG.
6. g262-273 whip: the whip pan is gentle (diff 7 in g262-270, peaks only at g271-279 after the arrival), so the "whip arrival" is actually late; the first 8 frames are near-static. Fix: put the whip peak on g262-268.
7. framediff.json says "pairs g 192..261" (shot 4's range) but the numbers are shot 5's (re-measured 6.22 / 21.73); fix the label.
8. meta.json g1 = 356 is exclusive (plan g1 = 355). Note only.
