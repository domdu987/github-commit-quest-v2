# QA-art, film 21 take A1 (HOOK, BIGZOOM 1 first half, g0-80 + handles)

Looked at: g0, g40, g80 at full size, 3x crops of the bridge and the crest, contact.jpg, phone_sheet.jpg (360x640), next to ref_shorts R5_sheet.jpg (and the README stats table).

## Scores (1-10)
| criterion | score | note |
|---|---|---|
| Set density / ornament | 6 | Real geography in one frame: castle rock top-left, the river loop, bridge, camp tents, farms, pines, hills. But the fields are a procedural patchwork and Abbey Craig reads as a bald pink-white lump with red dots. |
| Lighting & colour | 3 | Sat 0.77 is above every reference (R5, the most saturated, is 0.65). The fields are neon red / lime / yellow tiles, like a thermal or NDVI map; the river has a glowing cyan halo; shadows go to deep navy-black. The film's signature colours (English crimson + gold vs saltire blue) are not present, because everything is red-orange-green. Garish: **yes**. |
| Composition / framing | 5 | Good map read (loop, bridge, hill in a diagonal) and the hill-to-bridge line sets up A2. But the subject of the line is the soldiers, and at phone size the bridge is a hairline and the hill crest has no figures. By g80 the lump fills the bottom 45 % of the frame. |
| Character acting | 2 | No readable characters: knights are 2-4 px specks, Scots absent. |
| Key moment (hook image) | 3 | In the first 1-2 s on a phone, the viewer sees a psychedelic map, not "soldiers watching the enemy cross two by two". The narration line has nothing on screen to point at. |
| Match to references | 3 | Refs use controlled, painterly colour with one dominant hue (R5 storm blue) and clear readable subjects even in wides (the ship in R5 is always findable). This frame has neither. |

- Move: continuous and eased, no pops, sharp throughout (no blur, no DOF). p90 8.15 is **not** the problem for a high extreme wide; the problem is that nothing in the frame grabs. A slightly faster first second would still help (see QA_TECH 5).
- §G 2 (floating): nothing floats; trees and tents sit on the ground with shadows. §G 3 (distance): wide, correct for a BIGZOOM start. §H 1: the start is extreme wide and high, but the "tiny but findable" character is missing.
- Rim light: known film-wide limitation; nothing to light here. Noted, not scored.
- End pose matches P_A (by shot.py key); the handles continue the move, so the D6 to A2 will work. A2 must match the velocity at g80.

## Verdict: **FIX-FIRST**

## Fixes (in order of impact)
1. **Regrade the valley to the film's signature palette.** Target sat ~0.55-0.60, vivid ~55-60 % (still above §I's 0.50 / 45 %). Cut the red/orange field tiles to a few; make the farms 2-3 greens with some straw-gold; narrow or remove the cyan glow on the riverbanks; lift the navy shadow floor. Give Abbey Craig a grey-green crag + gorse material instead of the pale pink rock. Then the only strong crimson/gold is the English column and camp, and the only strong blue/white is the Scots and their saltires.
2. **Make the Scots findable from g0.** Put the Scots line on the open shelf of the crest on the camera side, out from under the pines, with 2-3 oversized saltire banners (blue with a white X). It should read as a blue-white line on the 360x640 phone sheet at g0, still under 5 % of the frame height. A warm sun patch, or the fixed light shaft, landing on them would lead the eye.
3. **Make the bridge column read "two by two".** Fill the whole deck with pairs and continue the column onto both causeways. Use crimson/white caparisons and one gold pennon per pair so the line is a red double-dotted stripe across the teal water. If it still does not read on the phone sheet, start the move 15-20 % lower or closer (the start pose is free; only P_A is fixed).
4. **Fix the light shaft on the crag.** Replace the flat horizontal yellow slabs (crest NW edge, all frames) with a diagonal, soft volumetric shaft from the sun direction, aimed at the Scots (see fix 2). If that is not possible, remove it from A1.
