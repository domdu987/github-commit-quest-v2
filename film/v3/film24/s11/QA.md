# s11 QA: film 24, shot 11 (sea chase): three swordsmen on j_near's bow

Delivered: `take.mkv.partaa/ab` (cat them to get take.mkv; libx264rgb crf 6, 30 fps, first_g 1107, 156 frames g 1107..1262, 55 MB split 40M),
`meta.json` (g0 1113, g1 1257 exclusive), `cues.json`, `contact.jpg`, `QA_AUTO.md` + `phone_sheet.jpg` (qa_auto PASS), `shot.py`, `deliver.py`.
g 1113..1256 = shot 11 (37.09-41.91 s), 6 in + 6 out handle frames in 3D. Hard cuts at both ends.

| rule | how / measured |
|---|---|
| nothing floats, contact shadow | 3 cards Child-Of the j_near ride at soldier_chase_a..c, decal on the deck, sun shadow; soles on the planks |
| no shake, one eased move | own camera on the bow deck, travelling with the ship (x += 3 D/s) plus one slow lateral slide 1.6 D (0.35 sine + 0.65 linear); qa_jitter median 0.13 px |
| never static > 6 frames | qa_auto: none |
| nothing parented to camera | unparented |
| feet planted | one ship-local point per card; screen step max 1.88 / 1.53 / 1.94 px per frame (camera slide only) |
| no duplicates | ashi_a24, ashi_c24 (mirrored) and ashi_d24: three members, different heights/hats; katana angles differ |
| near bigger than far | head w a 95-97 and c 100-102 (nearer) > b 74-76 (farther) |
| heads above y 880 | head bottoms max 627 px |
| sharp | DOF off |
| mouths | no quote: fixed expression mouths |
| tone | no injury, no fire |

Set state keyed each frame: set_fleet_chase (g-1107)/30, korean_turn 0, spikes 3, ports 0, damage 0, cannon smoke 0.
Deviations: the camera is a custom one (higher and closer than the preset 'chase', which showed heads of only 40 px behind the deck wall);
j_near's square sail is hidden at runtime (its visibility keys from set_damage dropped, hide_render on) because it covered two of the three soldiers;
the sail's absence is not noticeable at this size. A first render with the sail was thrown away. Render 37.7 s wall / 72.8 s cpu per frame.
