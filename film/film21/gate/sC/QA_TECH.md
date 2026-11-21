# QA-tech sC v2 (team3 9756c30)
g418-541 (124 frames, 720x1280, CUT in), checked at 5-frame steps (f6), full-size crops at g433/448/458/468/518-533, QA.md, meta.json. Colour level waived (conform); palette content judged.

## Verdict: PASS (no blocking issues; 4 non-blocking fixes)

## Beat table
| g | narration | what shows | result |
|---|---|---|---|
| 418-455 | 13.8-15.0 "ระหว่างกลาง" | high look down the bridge, column of 3D knights, camp at right, river left | reads; bridge is clearly the only crossing. Column riders look like red/yellow sleds (horses not legible), rigid |
| 455-490 | 15.0-16.5 "สะพานไม้แคบ ๆ ... เดียว" | descent past camp tents, pair of cast knights appear at the deck end, sign comes in | OK, parallax through tents, no blur |
| 490-520 | 16.5-17.3 "ม้าสองตัว" | camera behind the pair, STIRLING BRIDGE sign above them, river and hills behind | OK, knights crimson/gold, torsos above rail, heads y ~480-700 |
| 520-541 | 17.3-17.97 "ก็เต็มแล้ว" | push in, near knight "belly suck", far knight sweat drop (g~533) | beat is weak (see 1) |

## Checks
- Heads above y 880 and in 450-760 band: yes. Nobody cut by frame edge: yes (far right horse head leaves the frame at g538, a prop-level crop, acceptable). Face height max about 7 %, far under 35 %.
- Nothing floats: riders on horses, horses on deck, rails do not cross faces. Cloud in the sky is a sky prop, fine.
- Camera clearance: stays above the rail, no clipping, no flipped cards. Ends with sand and rail below the knights (about 35 % of frame), improved vs old report.
- Mouths: all closed, nobody speaks. Bloodless: yes.
- Colour story: knights, barding and column are crimson/gold/cream, no Scots blue on the English side (old issue 2 fixed). Horizon smoke blades gone (old issue 4 fixed).
- Old issue 3 (framing waste): fixed.

## Issues
1. NON-BLOCKING, g520-541: the belly-suck is still hard to read at phone size. The near (right) knight looks nearly unchanged, only a slight lean and a tiny sweat drop on the far knight (g533). Fix: squash the near knight torso harder (x0.65 wide, tabard slack, helmet tilts back) and hold it 10 frames from g524; enlarge both sweat drops 1.5x. Deadpan faces also under-sell the comedy: add a "squint/puff" face on g524.
2. NON-BLOCKING, g418-470: a few true blue tents/flags remain in the English camp (small blue tent left at g448-468, navy tents at g458, blue-purple flag at the far left g418-430); the rest read blue only because of shadow. Fix: recolour those tents/flags to cream/red/gold in the set (camp is meant to be blue-free).
3. NON-BLOCKING, g418-460: the 3D column on the bridge reads as boxes/sleds from above (horse bodies not visible), and it marches rigidly. Fix: give the column horse shapes with a slight bob, or thin it to 6 pairs so each reads as a knight on a horse.
4. NON-BLOCKING, g500-541: the two knights are near-identical (same grey helmets, same crimson barding), which weakens the "two horses" count at small size. Fix: make the far knight's helmet or plume gold, as in the plan.
