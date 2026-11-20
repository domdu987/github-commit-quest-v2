# QA s22 (shot 22 AHA, g1561..1655, handles 1557-1560 / 1656-1659)
- qa_auto PASS (QA_AUTO.md; note 'cuts with no visible change' = handles are 3-D continuations). take.mkv is 47.6 MB > 45: delivered as take.mkv.part* (40 MB parts); take.mkv itself is gitignored.
- qa_stats: `take.mkv: 3.4s ... saturation 0.654, brightness 74.4, in-shot motion median 5.94 p90 8.31`
- 103 frames, 11.0 s/frame wall, 21.09 cpu (2 procs x 2 threads, 720x1280, 8 spp).
- Frame-diff in shot (90x160 grey): median 5.09 PASS, p90 7.49 (target 12: MISS). Levers used: whip-tilt down from the lit tower at the cut (g1557-1572), 10 deg/s arc, push 7 %/s, three snaps (g1584, g1605, g1640), 4 px handheld sway, cheer bounce; the dark night ground keeps the metric low.
- Heads: [45, 69] px wide (wide shot of 5, rule >= 40), centre y [604, 812], lowest bottom 847 (< 880); nobody is cut by the frame edge except the officer's elbow on the last 2 frames; nobody floats (contact decals + proxy shadows).
## Beats
1561-1585 men hold bars on shoulders; 1586 'ไร้ประโยชน์' they stop (blink swap 1585-87); 1607-1619 all three DROP their bars (3-D bars tumble to the gravel, prop leaves the hand on a blink 1606-08); 1625-1630 officer salutes (card mirrored to face Eiffel); 1628-1630 Eiffel worried -> proud on a blink; 1632 men cheer (blink 1631-33, bounce ~0.06 D); 1628-1659 wagon + scrap cart roll away (set objects keyed); 1642 snap push on 'ขาดไม่ได้'.
## Take-gate round-1 self-fixes (WORKER20 s6/s7)
- brightness 62.9 -> 74.4 (scene exposure +0.95), saturation 0.654.
- Ground slab: lit foreground kegs at the left/right sides (kit20, sides only, lateral >= 2.5 m so the push passes beside them); the group fills the middle third and the tower the top half. Remaining dark slab under y ~880 sits under the captions.
- Heads 45-84 px (the principals Eiffel 58-76 px) vs the >= 60 px rule: Eiffel is 57-67 px at the end of the shot, a wide of five.
## Deviations
- 'Crowbar' = cast5 pickaxe prop (the card kit has no crowbar); the dropped bars are plain 3-D cylinders.
- Marks bunched at runtime (not the preset marks) so five characters fit; camera tower_dusk_chars moved 2.5 D back, lens shift +0.10 -> -0.03.
- Mouths: held open mouths of the 'shocked' / 'cheer' expressions only (never animated).
- Hue not measured. p90 frame-diff below 12 (see above).
