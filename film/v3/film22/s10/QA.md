# QA s10 (team 4): the turn, g 1197-1300 (+6 handle frames each side, file g 1191-1306, 116 frames)
take.mkv is split (`cat take.mkv.part* > take.mkv`, libx264rgb crf 6, 30 fps, 720x1280).

## What is in it
- CUT on "แต่วันนั้น". Side tracking along the near platform (eased, slide + lens push), a red train pulls in out of the dark tunnel (headlight, set_train), the official hides behind the foreground slatted bench, waiting passengers unfold their pocket maps from 41.28 s (local 41-52) then walk to the doors (66+), pass_child smiles with the map, doors open at 42.4 s (local 78), 1-s push-in on the official's jaw drop (local 78-103, sweat, trembling variants).
- Fixes from the set gate (SET_GATE items 21 + QA_TECH): MIND THE GAP edge plates hidden (they read reversed); the pink slab bench replaced by a slatted wooden bench with iron legs; hanging WAY OUT sign removed (TO TRAINS kept) so nothing is cut at the frame edge; official placed behind the bench and kept inside the frame (no edge cut).
- Mouths still (no quote in this take). Characters always change drawing (sway variants, walkers with walk cycle cards, jaw-drop variants).

## Numbers (take.mkv)
```
STATS
take.mkv       dur   3.9s shots   1 mean 3.87s med 3.87s <1s  0 >4s  0 | sat 0.678 vivid% 74.4 luma  94.5 contrast 50.9 detail 10.01 warm 19.3% cool 69.6% | motion med 5.02 p90 12.96 still%  0.0
JITTER
overall median jitter px 0.39
AUTO
# QA_AUTO PASS  (take.mkv, 116 frames, 30.00 fps, g 1191-1306)

## Notes
- planned cuts with no visible change within +-2 frames: g [1197]
- magenta share 0.0 %

Phone sheet: phone_sheet.jpg (cyan line = caption band y 880). Judge legibility on it.
GROUND RESULT: PASS (0 failures)

```
- Required: sat >= 0.50, vivid >= 45 %, luma 85-110: PASS (0.68 / 74 % / 94.5). In-shot frame-diff median >= 4, p90 >= 12: PASS (5.0 / 13.0).
- qa_auto: PASS. The planned cut at 1197 is the take start (nothing before it in this file but handles).
- QA_TEAM section L (no shake): qa_jitter prints no second above 2 px (overall median 0.39 px). The first draft measured 2.4 px in the push-in second; the lens range was reduced (34-40 -> 33-37) and re-rendered.
- QA_TEAM section K: GROUND.md = PASS. Set pieces flagged `mounted` after being seen touching their wall/vault/cord: vault ribs, hanging globes (rods to the vault), clock, end-wall liner and WAY OUT panel, wall posters/name panels, OLD map frame, train door decals, the new bench (feet on the floor). Glow quads (tunnel lamps, globe halos, light pools, headlights) flagged airborne. Every card has a contact shadow (cast_card shadow; walkers move their shadow with them).
- Heads: all heads above y 880 except the planned jaw-drop punch-in where the face is large (about 45 % of the frame, head centre near y 560, chin about y 790).
- Hue: shade hue is in the 240-260 family on the platform; the final frames are the red train (warm) against the blue vault, so the last frames carry more red than blue; no magenta (0.0 %).

## Join notes
- J6 s10 -> s11: the take ends on the required 1-s jaw-drop punch-in, so it cannot also travel through the train door. Use a dissolve of at most 6 frames into team 5's door view of the carriage (the handle frames 1301-1306 hold the push-in and are there for it). transition_in of s10 is a hard cut.
- Frame 0 of the take (g 1197) is the first picture after the cut: the platform from the bench, official behind it.
