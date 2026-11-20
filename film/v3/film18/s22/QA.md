# QA s22 (film 18, render team 4)
Range g 1683-1741, take.mkv frames 1677..1747 (71 frames), transition in: cut.
Render: 720x1280, 12 samples, OIDN, 2 threads, 20.2 s/frame wall (two renders at once).

## Frame diff (90x160 grey, in-shot frames only)
median 9.52, p90 13.32, min 6.04, max 15.73, frames < 1: 0 (rule: median >= 4, p90 >= 12)

## Max chin y per head (rule < 880)
{"hero": 513, "soldier": 495}

## Notes
- Round 4 rework: deep night (moon, cityglow and gate lintel removed, sky black); charging ox face overlay (frown + angry brows) on the front-3/4 gallop card; the hero's OWN tail flame is a flame card on the tail tip with a warm point light (found and fixed: the set's flame-card material read its flicker props from the wrong object, so flames rendered black; the card now gets fu/fk each frame).
- Frozen soldier at the left edge (kept in frame, scaled with the snap) in front-3/4; dark glazed barrel bottom-right; ground about 25 %.
- ONE held +15 % punch-in at g 1731 ("วาววับ" 57.64 s) with a star glint sprite on each blade tip g 1732-1745 (tip positions estimated from the head anchor: the front view has no tip anchors).
- Deviation: p90 frame diff 8.9 (target 12): no pulses, so motion comes from push 9 %/s, slide 14 px/s and sway only. The soldier's helmet still overlaps the edge of the hero flame at the start.
- Round 5: the cast's ox_figure(face='rage') is used (cast18 pulled from film18/main); hero mirrored so its OWN tail flame (flame card on the tail tip, leaning 40 deg, warm light) sits on the right, clear of the soldier; the soldier at the left edge; the grey watch post on the right is removed (palisade faces); camera closer (lens 27, ox about 60 % of the width at the end); star glints kept.
- Deviation: the hero's tail flame leaves the right edge during the last ~10 frames of the push; the soldier's face is partly hidden behind the ox head at the end.
- Round 6: punch-in cut to +8 % and homed on the head-to-tail span; barrel removed; the soldier moved to x ~0.6-0.7 in front of the ox (clear of the tail flame at the right edge); star glint is a big 4-point flash over g 1732-1739; hero scaled 0.8 so head, horns and the tail flame stay in frame. Ground about 30 %.
- Round 8 (must-fix): blue moonlit sky restored (moon and sky back); watch-post tripod brazier and its flames removed (palisade faces + flame_pg*); soldier at x ~0.65-0.80 front-3/4 (yaw -35), no flame behind him; ox head at x 0.05-0.45, mouth about y 880 (head 595 chin figure in meta is the head box, mouth ~880: borderline vs rule 860); star glints are a single clean 4-point star g 1732-1739 (not on both blade tips: one position estimate only); camera tilted down, so ground is ~40 %, not fixed.
- Not verified: blades both visible at all frames; ground share.
- Round 11b CORRECTION: the earlier take did NOT remove the brazier (my note was wrong; nothing had been rendered to check). Ray cast showed it is faces of the merged 'wood' mesh (watch post at 7.5,-41.4); now sunk, confirmed gone on a rendered g 1742 still. Script-side projection over g 1683-1741: ox mouth worst y 808 (rule 860), head x 0.16-0.41 (band 0.08-0.45); soldier now right and behind the ox (box x 0.49-1.11 by a crude +-1 D box). Ground ~45 %.
- Gate 12 (rendered check, g 1738): punch removed (steady push only); ox mouth about y 800 on the RENDERED frame, muzzle inside the frame; the ox's own tail flame is in frame (right edge ~x 0.97); soldier fully inside the frame at x ~0.7-0.85; glazed pot and reed bundle in the bottom corners, ground_share 0.03-0.05 (g 1683 / 1710 / 1742). NOT fixed: the ox's reed bundle still crosses the soldier's chest and can read as a broom; I did not measure every frame.
- Gate 13 + rule I: ox shrunk to 0.45, soldier at x ~0.88 fully in frame, cool moon-blue rim on soldier and hero. Rendered g 1713/1725/1737 (checked by eye): hero jaw about y 800-830 (projected anchor max 797). NOT fixed: the tail flame still stands right beside the soldier's head (well under the 60 px the director asked for), the soldier still faces the lens, and the flame stays in frame but touches the right edge region.

See QA_AUTO.md and phone_sheet.jpg.
