# QA s22 (shot 22 AHA, g1561..1655, handles 1557-1560 / 1656-1659)
- qa_auto PASS (QA_AUTO.md; note 'cuts with no visible change' = handles are 3-D continuations). Delivered as take.mkv.part* (45.2 MB > 45: split into 40 MB parts; take.mkv itself not in git).
- 103 frames, 10.11 s/frame wall, 19.44 cpu (2 procs x 2 threads, 720x1280, 8 spp).
- Frame-diff in shot: median 4.39 (target 4 PASS), p90 5.5 (target 12 MISS). Dark night ground fills half the frame; handheld sway + arc + zoom + 2 small snaps + bounce lifted it from 2.0/3.4 to this, a crash move was not possible without losing the group.
- Heads: [46, 71] px wide, centre y [598, 706], lowest bottom 742 (< 880). Eiffel/officer/men stay inside the frame; the officer's head is partly at the right edge only on the last 2-3 frames.
## Beats (events frames)
1561-1585 men hold bars on shoulders; 1586 'ไร้ประโยชน์' they stop (blink swap 1585-87); 1607-1619 all three drop their bars (3-D bars tumble to the gravel, prop leaves the hand on a blink 1606-08); 1625-1630 officer salutes (card mirrored to face Eiffel); 1628-1630 Eiffel worried -> proud on a blink; 1632 men cheer (blink 1631-33, bounce ~0.06 D); 1628-1659 wagon + scrap cart roll away to the right (set objects keyed); 1642 snap push.
## Deviations
- 'Crowbar' = cast5 pickaxe prop (card kit has no crowbar); the fallen bars are plain 3-D cylinders.
- Marks bunched at runtime (not the preset marks) so five characters fit at 15 D; camera tower_dusk_chars moved 2.5 D back, lens shift +0.10 -> -0.03, tilt +3 deg -> +8.
- Lower ~40 % of the frame is empty blue ground under the captions (R2-N4): tilt keeps rising; the preset FG (lamp-post) is a thin pole at the left edge, no big FG prop.
- Mouths: held open mouths of the 'shocked' / 'cheer' expressions only (never animated), per cast notes.
- Hue not measured (no hue20 run).
