# Film 11 style board (Jenner, cowpox, Berkeley 1796)

Files: `style_board.jpg` (A | B | C, 480x853 each + label strip), `still_A.png`, `still_B.png`, `still_C.png` (720x1280), `hue_rows.txt`, `hue.json`.
Build: `python3 ../dairy_board.py A B C` (module `set3d11/dairy_board.py` + `dairy_board_tex.py`; sheet `../make_board.py`; hue `../board_hue.py`).
Settings: Cycles CPU, 32 samples, OIDN denoise, 4 threads, no depth of field, no text, 22 mm camera, one hard sun key + a no-shadow warm bounce sun, painted blue-violet shade.

| still | render time (wall / CPU) | shade hue (target 240-260) | magenta share (target <= 10 %) |
|---|---|---|---|
| A cowshed, golden morning (KEY) | 13.2 s / 51.6 s | 240.4 (shaded 37 % of frame) | 6.9 % |
| B village exterior, low angle | 8.3 s / 32.1 s | 242.4 (shaded 7 % of frame) | 1.4 % |
| C cowshed, late amber (ALT) | 14.9 s / 57.9 s | 244.0 (shaded 66 % of frame) | 6.6 % |

Other hue-report numbers (red / orange / blue / violet %, sat, val): A 42.3 / 21.9 / 20.6 / 4.9, 0.39, 0.46; B 5.0 / 36.1 / 25.5 / 1.9, 0.40, 0.73; C 17.6 / 10.0 / 44.3 / 17.9, 0.46, 0.44.
(The hue_report "target band" is the old reference-clip band; B is a bright daylight exterior with val 0.73 and a lot of green, C is shade heavy on purpose.)

## A. Cowshed, golden morning (KEY preset), eye-level wide
Timber-framed Cotswold barn: oak posts, tie beams, king posts, braces, rafters, hay loft with hay heaps and ladder, plank walls with gaps, wooden stalls with two cows, hanging lanterns, harness on pegs, bales, churns, pails, wheelbarrow, hens, cats, swallows, straw on the earth floor.
Low hard sun (elev 20 deg) pours through the open door and plank gaps: warm golden key, cast shadows, dust motes and faint light shafts in the beams (all sharp); Blossom (brown-and-white cow), the milkmaid on the milking stool, Jenner and James stand in the sun pool.
Shade is blue-violet (hue 240), wood and straw stay warm; golden-amber exterior glows through the door.

## B. Village exterior, low angle wide
Jenner's honey-stone cottage with a deep thatched roof, eyebrow dormers, chimneys with smoke, porch and climbing roses; the little rustic round thatched hut in the garden; cottage-garden flowers (hollyhocks, delphiniums, roses, marigolds), white picket fence with gate, dry-stone wall, straw skeps, bean poles.
Lane and verge with wild flowers in the foreground, an orchard with blossom trees and the cow Blossom, a church tower on a hillside, patchwork rolling Gloucestershire hills with sheep, crisp cartoon cumulus with lavender undersides.
Sun 36 deg from front-left, hard cast shadows (fence, grass, hens); the doctor (green waistcoat), Jenner, James and the milkmaid stand at the gate.

## C. Cowshed, late-afternoon amber, high angle (alternative to A)
Same barn and props as A, camera high at the front looking down into the aisle, sun 11 deg so the amber light rakes across the whole floor with long, harder shadows and strong contrast.
Shade is cooler and deeper (blue-violet 244, bigger area: 66 % of frame), the lit areas are more orange; the loft and roof timbers read as a dark ceiling.
Choose A for friendlier, brighter morning warmth, C for dramatic contrast (the high angle also shows more floor props).

## Known gaps (mood board, not final)
- People are placeholder_actor puppet cards, the cow, hens and cats are low-poly blobs (no legs bending, no faces).
- Foreground floor of A/C is large and fairly empty below y 880 (caption band); mid-ground is the dense part.
- B: near-camera flowers are chunky polygons, the thatch is a flat texture (no straw detail), no depth-sorted hills haze beyond the compositor mist.
- C: a front tie beam and the roof slab cut across the top-left of the frame.
- Sky is a painted dome; sun beams are faint additive wedges plus a low compositor glare, not volumetrics.
