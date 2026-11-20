# QA s22 (film 18, render team 4)
Range g 1683-1741, take.mkv frames 1677..1747 (71 frames), transition in: cut.
Render: 720x1280, 12 samples, OIDN, 2 threads, 20.7 s/frame wall (two renders at once).

## Frame diff (90x160 grey, in-shot frames only)
median 9.07, p90 12.8, min 3.71, max 17.21, frames < 1: 0 (rule: median >= 4, p90 >= 12)

## Max chin y per head (rule < 880)
{"hero": 766, "soldier": 726}

## Notes
- Round 4 rework: deep night (moon, cityglow and gate lintel removed, sky black); charging ox face overlay (frown + angry brows) on the front-3/4 gallop card; the hero's OWN tail flame is a flame card on the tail tip with a warm point light (found and fixed: the set's flame-card material read its flicker props from the wrong object, so flames rendered black; the card now gets fu/fk each frame).
- Frozen soldier at the left edge (kept in frame, scaled with the snap) in front-3/4; dark glazed barrel bottom-right; ground about 25 %.
- ONE held +15 % punch-in at g 1731 ("วาววับ" 57.64 s) with a star glint sprite on each blade tip g 1732-1745 (tip positions estimated from the head anchor: the front view has no tip anchors).
- Deviation: p90 frame diff 8.9 (target 12): no pulses, so motion comes from push 9 %/s, slide 14 px/s and sway only. The soldier's helmet still overlaps the edge of the hero flame at the start.
- Round 5: the cast's ox_figure(face='rage') is used (cast18 pulled from film18/main); hero mirrored so its OWN tail flame (flame card on the tail tip, leaning 40 deg, warm light) sits on the right, clear of the soldier; the soldier at the left edge; the grey watch post on the right is removed (palisade faces); camera closer (lens 27, ox about 60 % of the width at the end); star glints kept.
- Deviation: the hero's tail flame leaves the right edge during the last ~10 frames of the push; the soldier's face is partly hidden behind the ox head at the end.

See QA_AUTO.md and phone_sheet.jpg.
