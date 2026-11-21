# s04 QA: film 22, take s04 (Beck's lodgings NIGHT; match push from the OLD map to Beck)

Delivered: `take.mkv` (libx264rgb crf 6, 30 fps, **first_g 318, g 318..455 = 138 frames**, 720x1280, 14 samples + denoise, no captions/audio), `meta.json`, `cues.json`, `contact.jpg` (every 6th frame, cyan line y 880), `phone_sheet.jpg`, `QA_AUTO.md` (PASS), `GROUND.md` (PASS), `jitter.txt`, `shot.py`, `c22.py`.
Plan range g 324-449 (10.81-15.00 s); handles: 318-323 (6 frames before: the 9-frame match dissolve from s03 is centred on the start) and 450-455 (6 frames after: travel join into s05).

## Beats (narration +0.10 s, local k = g - 324)
| g | beat |
|---|---|
| 324-335 | camera ON the OLD map (MAP OF LONDON, river, tangled lines, lilac-grey like s03's end after team 4's tint), then pulls back and slides right along the wall (3-5 D/s, eased) |
| 336-350 | cork board with the circuit diagrams; Beck appears at the cork board (turns toward us, circuit in hand) 10.81 |
| 350-364 (11.55) | he reaches up and pins a circuit sheet to the cork board (the sheet lands at g 360) |
| 364-394 (12.34) | holds a second circuit up beside the board and studies it |
| 394-402 (13.03) | steps (walk cycle) to the little table, reads the NOTICE letter, sad sigh (mouth o), pushes the letter aside at g 418 |
| 418-449 (13.97) | picks up the ruler (walk cycle with the ruler), walks to the board and leans in with the pen at the start of the blue line; same pose and camera as s05 frame 450 |

## SET_GATE / QA_TECH mandatory items
- **7 (NOTICE beat, basket):** the wastebasket is moved at runtime to the far-left corner and the little table (+ the NOTICE letter) is shifted 1.2 D left, so Beck's legs, feet and contact shadow are visible during the whole NOTICE beat (g 394-420, see contact tiles 396-414).
- **J3 / QA_TECH 32:** the take starts about 25 % closer on the map than the old s04 start key (distance 3.7 D, lens 30): the map and its title fill the frame, wallpaper bands are about 27 % of the frame (portrait frame, landscape map: closer would cut the title). Tint is the lodgings' own lilac-grey. Plan: 9-frame eased match dissolve.
- **J4:** s05 camera key 0 is this take's camera at local 126 (g 450) with the same speed; Beck is in the same pose (beck_rule_line, pen at the start of the blue line) and position.
- **Nothing floats (QA section K):** `python3 shot.py ground` -> GROUND.md PASS (frames every 10th). Runtime lifts: trunk, key_lamp 0.063 D and the rolls pot 0.013 D (their ink hull sat below the floor); wall items (frame, map, cork, shelf, posters, pendant, coat hook) are marked `mounted` (seen touching their wall/cord in the stills). Every Beck card has a contact disc under the feet (`beck.card_shadow`).
- **No camera shake (section L):** camera = the planned key list gaussian-smoothed (sigma 5 frames, one key per frame); `qa_jitter.py`: see `jitter.txt`, no second above 2 px (overall median 0.74 px).

## Numbers (138 frames)
| measure | value | target |
|---|---|---|
| mean saturation | 0.63 | >= 0.50 |
| vivid | 65 % | >= 45 % |
| mean luma | 88.7 | 85-110 |
| top-third luma | 89 | <= 115 |
| shade hue 240-260 | **49 % of frames, median 239** (my own estimator; the lodgings shade is pure blue 235-245) | >= 80 % |
| magenta | 0.0 % (qa_auto strict) | <= 10 % |
| in-shot frame diff 90x160 grey | median **12.51**, p90 **26.25**, min 3.66 | median >= 4, p90 >= 12 |
`qa_auto.py` PASS. Render 14-17 s per frame (2-4 concurrent processes).

## Known issues
- Around g 348-352 Beck is at the right edge of the frame, partly hidden by the foreground NOTICE letter / cut by the frame edge for about 6 frames, while the camera slides from the map to him.
- Shade hue is slightly below the 240-260 band in 51 % of frames (pure deep blue 235-239); not changed (grading is not allowed).
- Title of the OLD map is cut by the right edge on the first 4 frames (g 318-321, dissolve handle); whole from g 324.
- The pendant bulb enters the top edge at the end (flat disc, about 1 % of pixels).
- Mouths closed all take (no quote); the "o" mouth in the NOTICE pose is the sigh.
