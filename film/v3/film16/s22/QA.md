# s22 QA (v3, after the TAKE gate): film 16, shot 22 ("ทางออกคือแก้ว") -- LINE line_wagon, AFTER_RAIN

## Delivered
- take.mkv: 92 frames, g 1372..1463 (shot g 1381..1454, 9 handle frames each side), 30.4 MB. Dissolve in 11 f, hard cut out at g 1455 (to s23).
- QA_AUTO.md, phone_sheet.jpg, contact.jpg, cues.json, meta.json, framediff.json.

## Beats (event g = round((t+0.10)*30))
| g | beat |
|---|---|
| 1372-1381 | Morse on the wagon bed, hand on the neck of the nearest crate bottle ("ทางออกคือแก้ว" 1384) |
| 1382 | the bottle leaves the crate (runtime copy of the crate glass / glint meshes without that bottle switches on; the held copy appears in the same place) |
| 1383-1398 | lifted up beside his head; snap x1.9 with pan on "แก้ว" (1389-1402, word 1392) |
| 1396-1410 | sun-star flare on the held glass; he looks up at the bottle (eyes open, gaze up) |
| 1411-1413 | blink; at g 1412 the happy smile (swap on the closed frame); second twinkle 1432-1442 |

## TAKE-gate notes handled
- **Frame-diff:** median 4.64, p90 12.4 (target >= 4 / >= 12): MET. Camera = look-point pans (an eased pan toward the raised bottle on the snap, then a slow continuing pan) plus push 8 %/s, slide -80 px/s, arc -14 deg/s. It never trucks toward the crate, so crate bottles stay at the frame edge.
- **No flat orange wall:** the camera is 2.2 D higher; the wagon side board is now a strip below the frame / the bed planks and the pallet box, with long shadows; Morse's legs and the bed under his feet are visible in the first frames (contact shadow on).
- **Bottle not cropped:** the held bottle stays inside the frame (x 380-600 px, glass top y >= 330) for the whole shot.
- **Eye-line:** eyes open and looking up at the bottle from g 1383, smile only after the glint (g 1412).
- **Sun:** the sun itself is not in the frame; sun-stars flare on the held glass and the crate necks (a sun disc was not added).

## Checked
- Heads 181 -> 357 px wide, centre y 559-610, lowest head bottom 752 (< 880). Hand pinned to the bottle neck (error <= 0.1 D). No text, no DOF, mouth still, no magenta.
- The crate has 7 bottles after the pick (the picked one is removed from the copy).
- Hair touches the left edge for a few frames around the snap peak; face, bottle and glint stay in frame.

## Seconds per frame
13.29 s wall / 24.97 s CPU (720x1280, 7 spp; two renders were running at once).
