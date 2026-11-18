# s03 QA: film 10, shots 3-4, sea SEA_DAY
Delivered: take.mkv (split in parts) g 128..298 (171 frames, 720x1280, 12 samples, crf 6), first_g 128, g0 134, g1 293, 6 frames of handle each side. transition_in: cut.
- g 128..212 shot 3 convoy_wide: grey ships (hero ship kept plain, set_stripes 0), dived U-boat periscope + feather in the foreground, slow push; set_convoy keyed every frame.
- g 213..298 shot 4: lower closer camera toward the far merchant c3; set_hit rises from g 226 (water column, then dark smoke, no fire/gore); periscope sinks g 262..292 (set_uboat periscope 1 -> 0), the U-boat dives. Cut at g 213 detected by qa_auto (PASS).
- Deck crew placeholders swapped for cast10 sailors (tiny, riding ships). No mouths move. No DOF. No actors above the caption band issue (no large heads).
- Known: the hit ship is small at the horizon and partly behind a nearer merchant; the plume/smoke still read on the phone sheet. The sea is the approved smooth teal water, unchanged.

## Rework (QA-tech FAIL, round 2)
- Shot 3: low close camera 9 D behind the periscope (big tube + head + foam feather in the foreground), convoy readable behind; push 23 -> 28 mm.
- Shot 4: different, wider angle (periscope smaller at the right, the hit merchant moved to a clear lane at runtime via its root so nothing blocks it): bigger plume (x1.2) and smoke from g 222, the merchant lists (root roll to 0.17 rad), the periscope sinks g 244..288, push-in 22 -> 28 mm. Cut g212/213 now changes size, angle and subject.
