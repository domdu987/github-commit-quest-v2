# QA re-check s15 v2 (shots 15-17, g 995-1173): QA-art + tech items. VERDICT: FAIL

Frames checked: all 179 extracted; viewed at 6 fps (every 5th g, 995-1170) plus every cut +-3 (1059-1065, 1124-1130, 1164-1170), 51 frames,
at phone size (360x640 sheets with the y 880 line) and at full size (g 1055, 1100, 1150, plus a 2x crop of the hive at g 1150).
Working files: scratchpad/qa_s15r/ (f/gNNNN.png, sheet_0-4.jpg, crop1150.png).

## v1 items (shots 15-17 only)
| v1 item | status | note |
|---|---|---|
| TECH 3 / night elephants brighter than soil (shot 16) | PARTLY | Better: luma elephant 54 vs soil 46 (g 1100), shot 15 52 vs 39 (g 1040). They no longer read as pale cut-outs; still a little above the soil. Not blocking. |
| TECH 4 / contact shadows (15, 16) | PARTLY | Shot 16: dark patches under the matriarch's and calf's feet read. Shot 15: feet sit in grass, shadows barely visible. Not blocking. |
| TECH 5 / ART 2 sleeping hives do not read | NOT | Now 12 bee cards, but each one is drawn on an OPAQUE BLACK RECTANGLE (alpha lost): a jagged black block hangs off the hive front, outside the box outline (g 1127-1173, clearest at 1150 and 1164). The bees have open eyes and read awake. On the phone it reads as "a black blob with bees on it", not sleeping bees. |
| TECH 6 / ART 2 foreground clutter in 17 | FIXED | Pumpkins, pot and vines gone; open soil in the bottom of the frame. |
| TECH 7 / ART 2 shot 17 lit like sunset | NOT | The whole frame is still amber: mean RGB at g 1150 is (66, 34, 17) vs shot 16 (76, 67, 125). The roof underside fills the top quarter and glows orange. The hard cut 1126->1127 still reads as a change from night to sunset. |
| TECH 10 / matriarch arrives at the fence, trunk off the calf | PARTLY | Trunk is now clear of the calf. No fence wire is visible in shot 16 (corn and one hive box behind only), so "she walks straight to the fence" relies on shot 15. Not blocking alone. |
| TECH 11 / ART 3 empty sky and ground | PARTLY | Olive smear at the lower left of 15 still there g 995-1005, gone after. Sky is about 45-48 % of the frame in 15 (g 1055) and about 44 % in 16 (g 1100), worse than the 25-30 % target. This is also why the heads sit low (blocker 3). |
| TECH 12 / herd barely advances | FIXED | The herd visibly grows and moves forward g 995 -> 1061 (dolly + walk). |
| TECH 13 / phone read of 17 | NOT | See blockers 1-2. |

## Tech
- Pops / frozen runs: none. The largest frame diffs are the two planned cuts (1062: 12.8, 1127: 34.2). The next largest is 3.7. The smallest per-frame diff is 0.9 (g 1112-1120, slow but moving). No black or magenta frames.
- Steep down-view on elephants: none. The camera is low and side or front on in 15 and 16.
- Heads above y 880: FAIL on the calf (blocker 3). The adult heads are at y 600-720.
- Calf overlapping the mother (16): the calf stands in front of her front legs and its ear is cut by the right frame edge. It reads as "with the calf", but the frame is cramped and the calf's face sits in the caption band.

## Blockers (round 2)
1. **g 1127-1173 (shot 17): the bees are a black blob.** Each bee card renders on an opaque black rectangle.
   Fix: render the bee sprite with alpha (RGBA PNG; the material uses alpha blend/clip, not opaque, and does not premultiply onto black). Use a closed-eye or dozing bee pose (set_bees asleep). Optionally add 1-2 small drifting "z" so the sleep reads at phone size.
2. **g 1127-1173 (shot 17): the shot is lit like sunset, not night.** The frame is warm orange (mean RGB 66/34/17) and the roof underside glows.
   Fix: drop the warm practical lights, light the scene with the cool moon key used in 15/16 (blue channel at or above red), grade the roof underside down about 50 % and tilt the camera so the roof takes at most 10-15 % of the top. Target: the same blue-violet night grade as g 1100.
3. **g 1045-1126 (end of 15 and all of 16): the calf's head is in the caption band.** Its eye is at about y 885 at g 1055 and about y 925 at g 1062-1126 (rule: heads above y 880).
   Fix: tilt or raise the framing so the subjects move up about 150-200 px. This also cuts the sky from about 45 % to about 30 %. In 16, also move the calf about 0.5 m back and to the left so it is not cut by the right edge and does not sit on the mother's front legs.
