# QA s02 (shot 2, g 80..177; take g 76..185)
RESTO resto_table DAY 1889. Maupassant seated, napkin tucked, blissful (eyes closed), fork cycle (40 f) + chew bob; bread basket + glasses FG from the set.
Starts tight (head 190-237 px, window hidden behind him), push 15 %/s + slide 100 px/s + orbit; SNAP PULL-OUT x0.5 g 137..152 on "เดียวกันนั้น" (event g 139) reveals the riveted X-braced girders across the window and Paris/Seine/Trocadero below.
- Colour (QA §G): runtime grade exposure -0.9 EV + compositor saturation 1.45 (the raw resto_table frame is white cloth, luma 152 / sat 0.34). qa_stats: **saturation 0.590, brightness 97.4**, in-shot motion median 3.82 p90 5.30.
- deliver.py frame-diff (in-shot g 81..177): median 3.73, p90 9.62 (target 4 / 12): UNDER. A close seated shot over a static room; the snap pull-out is the only large motion.
- Heads: head centre y 677-688, bottom max 795 (<880), head 123-237 px, never cut by the frame; no face > 35 % of frame height. No mouth moves. Nothing floats (seated behind the cloth); no bars across his face (girders at the sides).
- qa_auto PASS (magenta 0). 13.5-22 s/frame wall (shared cores), 8 spp. Dissolve-out handle 8 frames.
