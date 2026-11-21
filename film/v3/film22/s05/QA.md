# s05 QA: film 22, take s05 (Beck's lodgings NIGHT; crane up to top-down over the board)

Delivered: `take.mkv` (libx264rgb crf 6, 30 fps, **first_g 444, g 444..576 = 133 frames**, 720x1280, 14 samples + denoise, no captions/audio), `meta.json`, `cues.json`, `contact.jpg`, `phone_sheet.jpg`, `QA_AUTO.md` (PASS), `GROUND.md` (PASS), `jitter.txt`, `shot.py`, `c22.py`.
Plan g 450-576 (15.00-19.22 s); handles 444-449 (6 before: travel join from s04); none after (hard cut 1 to s06 at 577).

## Beats (narration +0.10 s, k = g - 450)
| g | beat |
|---|---|
| 450-458 | continues s04's last frame (J4): Beck leans in at the board with ruler and pen (same pose, camera = s04 camera at g 450 and speed); crane up begins |
| 455 (15.08 "ให้เหมือนวงจร") | he holds the circuit diagram up beside the new map; a circuit sheet then lies beside the map on the board (side by side, same look) |
| 464-476 | Beck (card, upright at the board's lower edge, head in the upper third) steps back and dissolves over 5 frames as his own arms enter |
| 478-496 (16.02 "เส้นตรงล้วน") | 3D arms from the bottom edge (sleeve with black garter, rolled cuff, forearm, hand): right hand + pen rules the straight BLUE line along the ruler held by the left hand |
| 506-516 (16.83 "หักมุม 45 องศา") | the set square lands flat at g 506 (clack) and the GREEN line bends exactly 45 degrees (strict 0/45/90 geometry: flat run first, then diagonal and vertical) |
| 520-536 | YELLOW line drawn |
| 538-562 (18.09 "ไม่สนระยะจริงเลย") | his open hand (thumb) squeezes the far stations inward, the yellow line shortens; the OLD map lies on the floor in the lower-right corner of the frame for the whole take |
Camera: crane up from Beck's eye line (z 4.6) to z 9.0 above the board, pitch from about 15 degrees to about 60 degrees down, roll to -10 degrees (slow rotate), lens 30 -> 26 (the whole paper stays in frame); 1-3 D/s, eased.

## SET_GATE 8 (team 1, s05) mandatory items
- **No Beck card lying on the paper:** the card is only used in g 444-476, upright on the floor with a contact disc; after that only his 3D forearm/sleeve/hand/pen (built in shot.py, `arm3d`) enter from the bottom edge and the sleeve is visible to the edge.
- **Start (0-25):** Beck upright at the board's lower edge, head in the upper third of the frame (not in the caption band).
- **OLD map in a corner from 18.09 s to the end:** it is in the lower-right corner from the first frames to the last (floor sheet, texture old_map, same file as the platform/lodgings map), fully inside the frame, MAP OF LONDON readable.
- **Lamp/paper light:** pendant bulbs are dimmed to 55 % at runtime; luma 103.6 (<= 110). Shade hue: see numbers.
- QA_TECH 4 (head vs caption band): heads above y 880 for the whole card phase; head centre about y 470-640 at g 444-470.

## Section K / L
- **Nothing floats:** `python3 shot.py ground` -> GROUND.md PASS. Fixes made: the circuit sheet lies on the paper (z 0.012), the set square is placed flat on the paper (no descent), the open hand and pen touch the paper. Arms are the only limbs; their shoulders are outside the frame.
- **No camera shake:** camera keys gaussian-smoothed (sigma 4 frames, one key per frame); `qa_jitter.py`: no second above 2 px, overall median 0.29 px (`jitter.txt`).

## Numbers (133 frames)
| measure | value | target |
|---|---|---|
| mean saturation | 0.58 | >= 0.50 |
| vivid | 59.7 % | >= 45 % |
| mean luma | 103.6 | 85-110 |
| top-third luma | 100.7 | <= 115 |
| shade hue 240-260 | **26 % of frames, median 264** (my estimator) | >= 80 % (NOT met) |
| magenta | 0.0 % qa_auto strict (12.6 % by my wide hue test: the wall curtains and the pink floor runner) | <= 10 % |
| in-shot frame diff 90x160 grey | median **6.58**, p90 **14.17**, min 1.37 | median >= 4, p90 >= 12 |
`qa_auto.py` PASS.

## Known issues
- Shade hue is above the band (median 264): the lilac paper/board light dominates a top-down view. Not graded (not allowed); the director may lower the lodgings key.
- The 3D arms are simple tubes (comic, no fingers); the white sleeves read lilac-blue in the blue shade.
- The old map on the floor is partly under the right arm at g 504-540.
- Pendant bulbs show at the top edge in g 450-470 (dimmed).
- Mouths closed (no quote).
