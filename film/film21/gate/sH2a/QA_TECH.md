# QA-tech sH2a v2 (team3 408ada8)

Inspected: take.mkv (54 f, 720x1280, g1342-1395), contact.jpg, phone_sheet.jpg, f6/ every 5th frame (g1342-1392) at full size, handle frames g1393-1395, plus per-frame luma, clipping and frame-difference measurements. Colour judged as content only (conform normalises brightness, saturation, yellow cast).

## VERDICT: PASS (0 blocking, 4 non-blocking)

## qa_auto "suspected blur" (g1347, 1349-1352): override, not a defect
g1347 at full size is crisp: faces, moustaches, helmet rims, spear tips, plank edges and grass blades are all sharp. There is no DOF in the render. The flag comes from the smooth sky and water plus the planned fast crane-up, whose motion streak on the near sand is mild and reads as acceptable motion blur. Frame-to-frame change is steady at about 28-31 over the crane (g1350-1362), with no pop and no spin. Ignore the flag.

## Fixed against the old list (QA_TECH v1 / QA_ART v1)
| old item | now |
|---|---|
| Garish lemon sand, clipped yellow slab, luma 111-119 at P_TOP | End frame luma 105 (g1392 about 103). Clipped R=G>=250 pixels are about 1.5 % in the crane, 0 % at the ends. Neon cyan rim is reduced (foam_k halved). The sand is still lemon-yellow by hue but that is normalised at the conform. |
| Cork did not read (dark smudge, one tiny banner) | Scots wall is now blue, 5 ranks deep, with 4 large saltire banners (about 25-30 px at P_TOP). The deck ends AT the wall (g1362 and g1392). It reads as a plug. |
| English in the loop were dark dashes with blue caps | A solid crimson block of 440 packed bodies. It reads on the phone sheet (g1372, g1387) as a red mass. No blue on the English, and the neck cast are crimson. |
| South-bank half missing (umbrella tops only) | A crimson block of 221 is visible on the south bank in frame (g1372-1392). |
| Nadir spin (n14-17) | Fixed. The heading arcs smoothly, never overhead, and the frame difference is flat (28-32). |
| Heads / handles | Handles g1342-1344 continue H1's descent. g1393-1395 continue the drift at low speed (frame difference about 5), consistent with an ease-out into P_TOP. |

## Checks
- **Bottle and cork:** the loop silhouette (bulb with neck) reads instantly. The crimson block sits inside, and the blue wall with saltires plugs the bridge mouth. The south-bank crimson block is lower right. It reads at phone size (about 1.5 s hold).
- **End at P_TOP:** g1392 is the specified pose (south looking north, loop, bridge mouth and south camp in frame), with a slow drift in the handles.
- **Heads (neck, g1342-1352):** crimson English cast with worried faces, sweat drops and helmets, with the correct rim. The faces are not cut by the frame edge. The rows of English heads behind the Scots wall at g1347 are small and ambiguous (see 2).
- **Floating:** nothing hangs. The neck cast have contact shadows, and the troops stand on the sand with shadows (g1362).
- **Colour story:** no blue on the English. Blue means Scots only (wall, banners). Crimson means the English.
- **Camera clearance:** no clipping through the bridge, tree or banners. The camera passes the large saltire flag at g1352-1357 with no intersection. The lens stays above the terrain.
- **Bloodless:** yes.
- **Joins:** P_NECK exact at g1345 and P_TOP exact at g1392. The D6 dissolves have 3 handle frames on each side.
- **Rhythm:** median 26.5 and p90 29.8 are high but expected for the 1 s fast crane. The drift tail is calm.

## Issues
1. NON-BLOCKING, g1372-1395: at P_TOP the crimson south-bank block is partly hidden between the striped pavilion umbrellas, which also fill the caption band (y >= 880). Fix if time allows: clear a few pavilions in front of the block or nudge the block 20-30 m north.
2. NON-BLOCKING, g1345-1357: the English heads behind the Scots wall at the bridge mouth (g1347) read as a row of white heads on top of the blue wall. Fix: lower them or offset them so the wall silhouette stays pure blue.
3. NON-BLOCKING, g1357-1372: the loop floor and meadow are a flat, empty sand plane. The colour is normalised at the conform. The cork and bottle read, so this is only a polish item (a few more props or pegs on the floor).
4. NON-BLOCKING, g1350-1365: mid-crane luma dips to about 72 (g1350-1352) and then climbs to about 105. The conform should even it out. Check the join into H2b at P_TOP.
