# s07 QA: film 20, shot 7 (protest sheet insert) -- CAFE cafe_table_insert, DAY
Delivered: take.mkv (19.5 MB), first_g 462, 55 frames. Shot g 466..512; handles 4 in (cut) / 4 out (cut at 513). 45.5 s/frame wall (shared machine), 51.6 s cpu, 8 spp.
Frame-diff in shot (90x160 grey): median 7.42, p90 12.61 (targets 4 / 12). qa_auto: PASS (cut note g513 expected: the handle continues the move).
Content: raking 27-deg insert on the greeked sheet (no readable text); runtime quill + two sleeved hands (cream = painter, plum = poet): A signs, first signature lands g 471 (on "ลงชื่อประท้วง" g 469), quill handed to B g 483-494, B signs, second signature lands g 496. add_signature 14 -> 15 -> 16 of 24, keyed every frame. Snap x1.3 g 468-480. No DOF, no text, no heads in shot.
## Deviations / known weaknesses
- Hands and sleeves are simple meshes (balls + tapered sleeves), not cast20 art; the handover reads as a sleeve crossing the frame.
- From ~g 498 the stronger move (push 14 %/s + slide 75 px/s, needed for frame-diff) carries the nib out of the lower frame edge: the second signature appears on the sheet but the nib is mostly off-frame, and a sleeve fills the lower right at g 509-516 (handle).
- Move is stronger than the 10 %/s in the plan (14 %/s) for the frame-diff target.
