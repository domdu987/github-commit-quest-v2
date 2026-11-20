# QA s21 (film 18, render team 4)
Range g 1596-1682, take.mkv frames 1590..1688 (99 frames), transition in: cut.
Render: 720x1280, 12 samples, OIDN, 2 threads, 32.9 s/frame wall (two renders at once).

## Frame diff (90x160 grey, in-shot frames only)
median 5.55, p90 13.4, min 1.56, max 18.49, frames < 1: 0 (rule: median >= 4, p90 >= 12)

## Max chin y per head (rule < 880)
{"soldier_stand_a": 748, "soldier_cheer_cup_b": 747, "soldier_freeze_a": 871, "soldier_freeze_b": 861}

## Notes
- Round 4 rework: it now comes OUT OF THE DARK. Deep night (moon, city glow, lit gate dimmed, sky black, gate lintel faces removed). The herd is dark with tiny tail embers until g 1624, then the tail flames flare over ~22 frames (flame card on every tail tip, nearest 10 carry warm point lights, coats glow warm) so at the word g 1646 there are 8+ trailing flames against black.
- Found and fixed a set bug: the flame-card material read its flicker props (fu / fk) from the card, the set writes them on the root, so every flame card rendered BLACK. c18 now copies them to the card each frame.
- Charging face overlay (frown, angry brows) on every ox; two solid-black soldier silhouettes in 3/4 profile facing the herd (4-6 D... 6.8 and 7.6 D from the lens), they freeze at the snap; the third soldier is gone so nothing stands in front of the hero ox; a 3D toon-glazed bronze cup falls from the hand anchor on the word.
- ONE x1.5 snap at g 1644 held to the end; push 9 %/s, slide 6 px/s, sway. Ground ~25 %.
- QA_AUTO "blur" FAIL (36 frames, g 1590-1625) is the dark-to-fire design: the early frames are dark and soft by intent (no depth of field anywhere); not a defect.
- Blades keep the cast's bronze colour; no new specular edge could be drawn without editing the cast.

See QA_AUTO.md and phone_sheet.jpg.
