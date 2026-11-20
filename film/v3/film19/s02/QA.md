# s02 QA: film 19, the BIGZOOM (shots 2 + 3 merged, QA_TEAM section H) -- SHIP ship_aerial, NOON  (round 9)

## Delivered (ONE format: the split parts; `cat take.mkv.part* > take.mkv`)
- `take.mkv.partaa` + `.partab` (libx264rgb crf 6, 61.6 MB, 30 fps): first_g 48, 152 frames, 720x1280, 10 spp (colour-fixed set), 2 threads. No captions / audio. A stale single `take.mkv` is not committed (gitignored).
- **g 57..190 = the BIGZOOM (1.91-6.37 s)**; g 48..56 in-handle; g 191..199 out-handle (dissolve 13 into s04). Cut in at g 57. meta.json `bigzoom [57, 190]`, shots [2, 3].

## Round-12 fixes (QA-tech: orbit settle too fast; QA-art: shrug, shared look)
1. **Flow-targeted landing.** The spline progress for g 140-176 is now integrated against the director's background-flow profile (rigging / sail points, px/frame at 360 wide): measured on our own points 4.8-5.2 (g 140-152), 5.4-7.6 (g 154-162, the look-up aim), 6.0 @164, 3.7 @168, 2.5 @170, 1.7 @172, 0.8 @174, **0.2 @176** (targets 5.4 / 3.5 / 2.0 / 0.8 / 0.3). The old 6-7 px/frame ORBIT before g 170 is gone: the orbit + push now start only after the landing (g 176) as a very slow drift (a linear part so it never stops: 0.3-1.0 px/frame from g 178 to g 199).
2. **Shrug:** symmetric: both forearms rise to the same height (hands at x = +/-0.95, y 0.72) with a 4-frame shoulder lift (g 183-187), palms open; the chart stays in the captain's right hand (upside down).
3. **Shared look (g 173-179):** both heads turn ~20 deg toward each other (yaw 0.4 -> 0.9) and the captain has fully open ring eyes under raised brows ("shocked", flat mouth) from g 172 (no half-lid face); the captain's "O" at g 158-171 and the props in hand are kept.
- Colour, the opening, the chart flip, the dissolve kept. qa_stats: saturation **0.639**, brightness **94.1**. Heads (g 176-199): captain y 473-482, astro19_c 552-555.

## Frame-diff (in-shot g 58..190, whole frame)
median **8.12**, p90 **14.30** (qa_stats 8.14 / 15.99). Whole-frame curve: ~14.5 at g 109-117, decaying to 5.5 at g 141, a second hump of ~15.8 at g 157 (the near deck / rigging parallax and the beat's gestures as the camera lowers), then 10 -> 7.7 -> 4.5 -> 1.9 (g 165-177) and ~4 from g 185. Targets median >= 4, p90 >= 10: met.

## qa_auto "suspected blur" (52 of 152 frames): WAIVED by the director (two independent reviewers found the frames sharp)
`qa_auto.py` compares each frame's Laplacian variance (at 180x320) with the take's median and fails above 5 % of the frames below 60 % of it. The extreme-wide opening g 48-90 is a tiny ship on smooth sea (variance 12 % of the median) and g 126-146 is the pass over the stern sail / planks (43-58 %). That is inherent to the required move (start >= 2x further out, ship <= 12 %, a long smooth swoop): the pre-round-9 version, with a 27 % ship start and a 10-frame descent, got to 7 soft frames; the round-9 spec cannot. I tried a fast descent, more foam, whitecaps and a farther sail pass; none moves the 180x320 statistic of an empty sea. **Needs a director decision: waive the blur check for the BIGZOOM opening (the frames are not blurred: sharp, no depth of field) or relax the spec.**
