# QA s21 (film 18, render team 4)
Range g 1596-1682, take.mkv frames 1590..1688 (99 frames), transition in: cut.
Render: 720x1280, 12 samples, OIDN, 2 threads, 28.7 s/frame wall (two renders at once).

## Frame diff (90x160 grey, in-shot frames only)
median 6.99, p90 15.08, min 2.1, max 18.66, frames < 1: 0 (rule: median >= 4, p90 >= 12)

## Max chin y per head (rule < 880)
{"soldier_stand_a": 642, "soldier_cheer_cup_b": 641, "soldier_stand_c": 641, "soldier_freeze_a": 628, "soldier_freeze_b": 630, "soldier_freeze_c": 630}

## Notes
- Round 4 rework: it now comes OUT OF THE DARK. Deep night (moon, city glow, lit gate dimmed, sky black, gate lintel faces removed). The herd is dark with tiny tail embers until g 1624, then the tail flames flare over ~22 frames (flame card on every tail tip, nearest 10 carry warm point lights, coats glow warm) so at the word g 1646 there are 8+ trailing flames against black.
- Found and fixed a set bug: the flame-card material read its flicker props (fu / fk) from the card, the set writes them on the root, so every flame card rendered BLACK. c18 now copies them to the card each frame.
- Charging face overlay (frown, angry brows) on every ox; two solid-black soldier silhouettes in 3/4 profile facing the herd (4-6 D... 6.8 and 7.6 D from the lens), they freeze at the snap; the third soldier is gone so nothing stands in front of the hero ox; a 3D toon-glazed bronze cup falls from the hand anchor on the word.
- ONE x1.5 snap at g 1644 held to the end; push 9 %/s, slide 6 px/s, sway. Ground ~25 %.
- QA_AUTO "blur" FAIL (36 frames, g 1590-1625) is the dark-to-fire design: the early frames are dark and soft by intent (no depth of field anywhere); not a defect.
- Blades keep the cast's bronze colour; no new specular edge could be drawn without editing the cast.
- Round 6: cast ox_figure(face='rage') on every ox (cast18 pulled from film18/main); flame cards leaning back (~40 deg, roll about the view axis); three soldier silhouettes (9, 9.8 and 13 D out) in a shock pose (arms up, leaning back), frozen at the snap; gate and wall lamps held at 35 % until g 1626 and brought up over 20 frames; camera tilted up a little (floor before the snap about 30 %); chins <= 862.
- Round 8: tan watch posts and pale stakes at the gap removed (faces sunk); camera tilted down (look_at z 3.2) so the hero mouth sits ~y 900 at the end and soldier chins <= 704 (rule not fully met for the hero mouth); 3 star glints coded at g 1645-1652 (not verified in a frame). Soldiers still black silhouettes in the shock pose; jaw drop / lit rim / cup-fall rework not done. QA_AUTO blur FAIL = dark opening frames.
- Director round 11/12: camera look_at z 1.7 (not tilted up: measured the opposite way); hero mouth y ~730 on the RENDERED g 1675 frame (rule 860; script projection 700 + ~125 px render offset); soldiers got a warm solid-colour rim copy (fire side). Found and fixed a helper bug: actors sharing a mesh shared the first actor's material (tints were ignored) in s21's c18.py.
- NOT good: at the end of the take the hero ox covers most of the silhouettes (only a sliver of one soldier at the right edge in g 1675), so their shock does not read there; the cup fall is not visible in that frame; ground share not measured (deep night, bare floor ~35-40 % before the snap). Contact sheet is real (6 frames).

See QA_AUTO.md and phone_sheet.jpg.
