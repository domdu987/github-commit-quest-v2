# s22 QA: film 6b, shots 22-25 (plan 41.27-48.60 s), bakery AFTERNOON / MORNING

Delivered `take.mkv` = g 1232..1463 (232 frames, first_g 1232; 720x1280, 12 samples, libx264rgb crf 6). g 1238..1457 = shots 22-25,
g 1232..1237 = in-handle (shot 22, rendered in 3D), g 1458..1463 = out-handle (shot 25 crane continues). Transition in: cut.
`take.mkv` is over 45 MB, so it is split into `take.mkv.partaa`, `take.mkv.partab` (`cat take.mkv.part* > take.mkv`).
Also meta.json, cues.json, contact.jpg (16 frames), compare.jpg (5 finals + ref sheet pink_0), shot.py, deliver.py.

## Shots (g = round((t + 0.1) * 30) for events)
| shot | g | picture | camera |
|---|---|---|---|
| 22A | 1232-1286 | AFTERNOON, empty shop: CU kit, arm across, thinking; worried -> determined on "ว่าลุงไม่ได้โกง" (g 1259) + small nod; street + blue facades behind | 24 mm push in + drift |
| 22B | 1287-1310 | punch-in on "ขนมปังก้อนเดิม": kit raises the morning loaf (prop x1.6) beside his face, stunned -> determined squint | 24 mm push |
| 23 | 1311-1343 | MORNING (cool): ECU loaf pan, beam wobbles to level (settled ~g 1330), parchment tag "500 ก.", white puffs off the warm loaf | 26 mm push |
| 24 | 1344-1387 | AFTERNOON (gold), same framing: no steam; on "ตกบ่ายเหลือ" the loaf pan RISES (beam -8, g 1348-1364, overshoot); tag flips (squash) to red "480 ก." g 1361-1367 on "สี่ร้อย" | 26 mm push + tilt up |
| 25A | 1388-1427 | MORNING: ECU fresh loaves on the cooling table, set steam 1.5 + big billboard white puffs ("ควันขาว ๆ") | 24 mm low push |
| 25B | 1428-1463 | cut on "ขนมปังทุก": crane up into the white cloud | 22 mm crane |

## Rules
- No DOF; everything sharp. No mouth movement (no quote). Kit head 0.45-0.49 H centre, width ~380-470 px (53-65 % of the frame width); no heads in 23-25.
- Thai tags: SVG + embedded Kanit Black, rasterised by v3/set3d/raster.js (C.svg_pngs), PropCard parented to the loaf pan (moves with the beam).
- Complementary colour: deliver.py per-shot grade. Afternoon = gold highlights + blue-violet shadows; dawn = cool, with the steam kept white. The street
  facades in 22-24 give the blue counter-colour.

## Fixes made on the finals
- First full pass: dense overlapping puffs in 25 went to black blocks (transparent bounce limit) -> transparent_max_bounces 128, 25 re-rendered.
- 24: the push cropped "480 ก." at the right edge -> shorter push, 24 re-rendered.

## Differences from the plan
- 22: "looks at a morning loaf" = kit holds the loaf up beside his face (22B), not a loaf on a counter. kit_think's "chin" arm reads as arms crossed.
- 23/24 morning vs afternoon is told by the light, the grade, the steam (23 only) and the tag; the loaf mesh is the same size.
- Internal punch-in cuts at g 1287 and 1428, plus the plan cuts at 1311, 1344 and 1388.
