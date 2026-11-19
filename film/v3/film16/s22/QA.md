# s22 QA: film 16, shot 22 ("ทางออกคือแก้ว", the answer is glass) -- LINE line_wagon, AFTER_RAIN

## Delivered
- take.mkv: 92 frames, g 1372..1463 (shot = g 1381..1454; 9 handle frames each side), libx264rgb crf 6, 26.0 MB (no split needed).
- transition_in: dissolve 11 f; transition_out: hard cut at g 1455 (to s23).
- cues.json, contact.jpg, framediff.json, QA_AUTO.md (PASS), phone_sheet.jpg.

## Beats (event g = round((t+0.10)*30))
| g | beat |
|---|---|
| 1372-1381 | Morse on the wagon bed, hand on the neck of the nearest crate bottle ("ทางออกคือแก้ว" 1384); camera moving |
| 1382 | the bottle leaves the crate (a runtime copy of the crate glass + glint meshes without that bottle switches on, the hand-held copy appears in the same place) |
| 1383-1398 | lifted to the sun, tilting up; snap push x1.9 with pan on "แก้ว" (1389-1402, word 1392) |
| 1396-1410 | sun-star flare on the held glass; second twinkle 1432-1442; slow bob afterwards |

## Checked
- Heads 181 -> 357 px wide, centre y 576-615, lowest head bottom 800: whole head above y 880. Head sits left of frame centre, the bottle at upper right, so the bottle never covers the face.
- Hand pinned to the bottle (error <= 0.1 D). The crate has 7 bottles after the pick; the picked one is gone from the crate.
- Held bottle = LN.beer_bottle with the crate's own glass material at the crate's scale (the cast16 card bottle is 0.8 D, a different size from the set's 2 D bottles).
- No text, no DOF, no mouth movement (smile expression only).
- No magenta, no retried frames. The wagon side board fills the lower left in the first frames and hides his legs (stand mark is on the bed).

## Frame-diff (in-shot g 1382..1454), v2 after the director's request
median 4.12  p90 13.27  (target >= 4 / >= 12): MET (v1 was 3.63 / 9.61).
- The camera does not truck toward the crate any more (that filled the lens with crate bottles). Instead the LOOK POINT swings: an eased pan toward the raised bottle on the snap (13 f, x1.9, peak 2.0, 0.38 D swing) plus a slow continuing pan 0.28 D/s, on top of push 8 %/s, slide -80 px/s, arc -14 deg/s. The sky, trees and farm sweep past; Morse drifts to the left third and the bottle with its glint stays upper centre.
- Draft (360x640) gave 4.00 / 12.53; the final 4.12 / 13.27.
- Side effect: from about g 1421 his hair touches the left frame edge (head centre x 170-235 px, 330-345 px wide); the face, bottle and glint are fully in frame. The 7 remaining crate bottles show in the lower right.

## Differs from the plan
- Mark morse_wagon_bed moved 0.75 D toward the crate so the hand reaches the neck.
- Expression "happy / smile" instead of the pose's "excited" (the open grin read as manic).
- Camera is the preset side of the wagon, raised 0.8 D (the side boards hid the crate at the preset height); motion comes from look-point pans, not a truck toward the crate.
- 10.85 s/frame wall, 20.9 s CPU (720x1280, 7 spp, 2 procs x 2 threads).
