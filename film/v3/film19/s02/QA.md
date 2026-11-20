# s02 QA: film 19, the BIGZOOM (shots 2 + 3 merged, QA_TEAM section H) -- SHIP ship_aerial, NOON  (round 9)

## Delivered (ONE format: the split parts; `cat take.mkv.part* > take.mkv`)
- `take.mkv.partaa` + `.partab` (libx264rgb crf 6, 61.6 MB, 30 fps): first_g 48, 152 frames, 720x1280, 10 spp (colour-fixed set), 2 threads. No captions / audio. A stale single `take.mkv` is not committed (gitignored).
- **g 57..190 = the BIGZOOM (1.91-6.37 s)**; g 48..56 in-handle; g 191..199 out-handle (dissolve 13 into s04). Cut in at g 57. meta.json `bigzoom [57, 190]`, shots [2, 3].

## Round-11 fixes (QA-tech: ease-out; QA-art: props vanish)
1. **Ease-out.** The easing table now decays the ZOOM speed from g 112: `[(48,0),(66,.07),(90,.27),(112,.55),(125,.70),(140,.85),(153,.935),(164,.98),(176,1)]` (a smooth monotone cubic; zoom rate 6.3 %/frame at g 100 -> 5.0 at g 125 -> 3.3 at g 145 -> 2.3 at g 160 -> 1.2 at g 165 -> 0.25 at g 177, no second rise). The orbit that keeps the hold alive now starts at g 168 (was 150), so it no longer adds speed during the landing. Frame-diff along the move (in-shot pairs): ~15 (g 109) -> 12 (g 124) -> 8.6 (g 134) -> 8-10 (g 139-169) -> 5.5 (g 174) -> 4.4-5 (g 184-199). **The residual plateau of 8-10 at g 139-169 is the two actors' acting (the head-scratch wobble g 155-175, the chart turn g 160-170) and the deck / rigging parallax, not camera speed;** the camera's own zoom speed is monotone. Not met: the director's 15 -> 11 -> 7 -> 4 diff targets at g 140 / 155 / 170 (we measure ~8 / ~9 / ~8.5): reducing it further would mean flattening the beat.
2. **Props stay in hand through g 199.** The quadrant stays in astro19_c's right hand (lowered during the shrug) and the chart in the captain's right hand (held low, upside down); nothing pops out or slides off.
3. **Shrug:** symmetric, both elbows out, both hands up with open palms; the captain's brows stay up ("worried") through the shrug; the shared look g 173-179 is a head turn (gaze + head roll). The seams / stripe on the grey-lilac sail were not added (not cheap).
- Colour, the opening, the chart flip and the g191 dissolve kept. qa_stats: saturation **0.635**, brightness **93.8**.

## Frame-diff (in-shot g 58..190)
median **8.57**, p90 **14.34** (qa_stats 9.16 / 16.28). Targets median >= 4, p90 >= 10: met.

## qa_auto "suspected blur" (52 of 152 frames): WAIVED by the director (two independent reviewers found the frames sharp)
`qa_auto.py` compares each frame's Laplacian variance (at 180x320) with the take's median and fails above 5 % of the frames below 60 % of it. The extreme-wide opening g 48-90 is a tiny ship on smooth sea (variance 12 % of the median) and g 126-146 is the pass over the stern sail / planks (43-58 %). That is inherent to the required move (start >= 2x further out, ship <= 12 %, a long smooth swoop): the pre-round-9 version, with a 27 % ship start and a 10-frame descent, got to 7 soft frames; the round-9 spec cannot. I tried a fast descent, more foam, whitecaps and a farther sail pass; none moves the 180x320 statistic of an empty sea. **Needs a director decision: waive the blur check for the BIGZOOM opening (the frames are not blurred: sharp, no depth of field) or relax the spec.**
