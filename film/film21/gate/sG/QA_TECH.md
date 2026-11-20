# QA-tech sG (team8 862c04a)

**Verdict: FAIL** (content; colour numbers ignored per Colour policy). qa_auto PASS, but 2 blocking content issues.

## Beat by beat (frames inspected at full size and on contact/phone sheet)
| Beat (plan row G) | g | Result |
|---|---|---|
| Open behind the Scots, looking down at the column crossing two by two, about half over | 1141-1145 | PARTIAL. Scots in the foreground (profile, spear shafts) and a wide valley read well. The bridge is a thin line about 30 px tall at the far horizon. The "two by two" column and "half over" are NOT readable at phone size. Dark pole/spear cuts about 20 % of the frame. |
| Yawning knight on the causeway | 1141-1160 | NOT READABLE. Not identifiable at all in any frame (scaled x2.2 and still a speck). |
| Arc down to a low hero angle | 1146-1186 | Arc exists, but g1146-1160 is blocked and g1161-1181 is abstract (see issues). Arrives at the low angle at about 1186, fine. |
| Pine light shafts against the sky | 1171-1186 | Shafts only in the top-down terrain frames. The low hero frames show a blue sky and a thin yellow cloud streak, no pines. Weak but acceptable. |
| Horn blow on cue (39.69 = g1194) | 1194-1238 | OK. Horn up at 1196, cheeks puffed, readable by 1206. Nobody else's mouth moves. |
| Wallace lifts sword | 1196-1236 | Readable at 1206-1236 (sword up, brown hair, grey tunic). Small, but clear. |
| Snap push x1.5 + shake | 1194-1208 | Present, good. |
| Continuity into H1 (hill_over behind runners) | 1236 | Hard cut, so acceptable. Scots end at the low hill pose, H1 starts behind them. |

## Checks
- Heads above y 880: pass (heads about y 500-810).
- Face size: horn blower at the end about 9 % of frame height, pass.
- Nothing floats: pass (feet and contact shadows present).
- Edge cuts: the ledge Scot at the left edge is partly cut at 1141 (profile, behind a pole). The helmet Scot at the left edge in 1186-1206 is occluded by the foreground spear and the edge. Non-blocking.
- Colour story: Scots in saltire blue only, no English visible (far camp is red/white tents, fine). Pass.
- Bloodless: pass.
- Army density: only 5 Scots at the hill, no mass of troops. The plan's "army" is only implied. Non-blocking, as this is a hero beat.

## Issues
1. **BLOCKING, g1146-1160, camera clearance and foreground blocking.** The camera skims a pine trunk and canopy plus a boulder. At 1146 a black pole plus an orange trunk fill about 35 % of the frame. At 1151 a dark-green canopy fills about 45 % and a grey boulder is in the lower foreground. At 1156 the canopy and boulder dominate. These are unreadable frames, not parallax. Fix: move the lift waypoint (g1152) laterally by at least 4 m from the pine at the ledge and 3 m from the boulder, raise it, or push the pine out of the path in the set. Alternatively let it pass through only thin elements (branches) for under 6 frames.
2. **BLOCKING, g1141-1160, opening not readable.** The bridge and column are tiny, and the yawning knight is not visible at all. The opening must show "two by two, half over" and the yawn. Fix: start with the camera lower and closer or with a tighter FOV so the bridge fills about 25 % of the frame width and about 120 px of height. Scale the causeway knight by about x4 (not x2.2) and give the yawn a visible bounce. Hold about 12 frames (to g1153) before the arc.
3. NON-BLOCKING, g1161-1181. The top-down terrain frames (scatter of red/orange blobs, over-exposed light shafts) are abstract and carry no story. They are a short transit, but the camera should show the Scots or the hill ridge sooner. Fix: shorten the transit or pitch up earlier.
4. NON-BLOCKING, g1186-1200. The foreground spear crosses the frame diagonally and hides the left Scot. Fix: shift the spear out of the frame or lower it.
5. NON-BLOCKING, g1186-1238. The low-angle shot lacks pine light shafts (only a thin streak at the right) and shows only 5 Scots. Fix: add pines and shafts on the ridge, or 4-6 more Scots on the slope.
