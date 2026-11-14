# s03 QA: film 8, shots 3-7 (the bazaar at NOON)

Delivered: `take.mkv` (libx264rgb crf 6, 30 fps, **first_g 172, 442 frames = g 172..613**, 166 MB, committed split as
`take.mkv.partaa..partad`: `cat take.mkv.part* > take.mkv`), plus meta.json, cues.json (11 cues), contact.jpg (16 frames, cyan = y 880),
compare.jpg. Scripts: shot.py (probe / stills / final), deliver.py, qa.py (-> work/qa.txt), sheet.py; helpers ../common.py.
g 172..177 in-handle (dissolve from s01's night; transition_in dissolve 8 frames), g 178..607 plan shots 3-7, g 608..613 out-handle. All in 3D.
One location (bazaar, NOON), one build, five set-ups (internal id = plan shot):

| shot | g | set-up | action |
|---|---|---|---|
| 3 | 178-257 (+172-177) | crane down the street to the bazaar_wide height, 20 mm, (0.2,-14.5,13) -> (0.4,-12,6.6) | arcades, awnings, goods, lantern strings, merchant stall, iwan + turquoise dome in sun; woman with jar and second woman cross, boy runs, old man with stick; faint heat shimmer (post, far street band only, <= 0.9 px) |
| 4 | 258-357 | square at the well, eye level, push + orbit 3.4 D, 22 mm | woman + old man fan themselves sweating (fan angle animated, heat fx), boy hops foot to foot on the hot ground (shocked, sweat) |
| 5 | 358-431 | merchant_stall area, push in, 22 mm | the merchant on his takht over the giant jars, big belly laugh (squash / lean / head bounce; static laughing mouth) |
| 6 | 432-540 | low medium two-shot (z 1.9, pitch up 9-10), 19 mm, slow push | merchant (left, up on the takht) raises his finger and points down at farid; LIP-SYNC g 435-540 (14.4-17.9 s) as ('open', w, h) from the narration RMS envelope, 'flat' in the pauses; sharper jab + grin on "ไอ้บ้า" (g 476-488); farid (right) arms folded, calm smug smile -> happy closed-eye smile, slow blinks |
| 7 | 541-607 (+608-613) | street-level wide north to the iwan, slow push, 20 mm | farid walks calmly through the street (smug smile) while the woman laughs, the old man and a second woman point, the boy laughs, the merchant laughs on his takht ("ไอ้บ้าน้ำแข็ง" g 584) |

## Client rules
- No DOF (common.Take, before every render). Everything sharp.
- User taste: wide / medium framings of the dense lit bazaar, calm always-moving camera (crane, pushes, orbit), no text signs.
- Heads above y 880 in every frame (qa: "none" below for every actor). Main heads: shot 5 merchant 0.43-0.46 H, shot 6 merchant 0.43 / farid 0.52 H.
- Mouths move only in the merchant quote (shot 6, g 435-540). Laughing / fanning / jeering mouths are static expression mouths.

## QA (work/qa.txt)
Pops only at the 4 planned cuts (257/258, 357/358, 431/432, 540/541). Near-still transitions: none (median frame change 2.9 levels).
No magenta / black frames, no retried frames.
Hue (all): red 11.8, orange 30.2, blue 43.9, violet 3.4, magenta 2.3, sat 0.47, val 0.61: warm sunlit brick + blue sky / shade; magenta <= 4.7 (shot 6, the crimson coat).

## Seconds per frame
14.6 s wall / 28.8 s CPU mean (2 threads, two processes at once, 12 samples, denoise FAST). Bazaar sprites with up to 6 actors.

## Fixed during the work
- Draft 1: shot 4 camera inside the west arcade, shot 6 merchant off frame, shot 5 a woman blocking the lens -> re-staged.
- First finals: actors' z was dropped (place() takes xy + z): the merchant stood inside his takht (legs cut) and the boy did not hop. Fixed, shots 4-7 re-rendered; shot 3 (all at z 0) kept.

## Differences from the plan
- Shot 5 shows the merchant alone (farid in front blocked him); farid appears in the two-shot (6) and walking in 7.
- Shot 7 is a street-level wide (not the high bazaar_wide preset) so the jeering townsfolk read.
- Heat shimmer is a mild 2D post wobble on shot 3's far band, not a 3D effect.
