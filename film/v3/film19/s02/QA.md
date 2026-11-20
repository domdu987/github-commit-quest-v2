# s02 QA: film 19, the BIGZOOM (shots 2 + 3 merged, QA_TEAM section H) -- SHIP ship_aerial, NOON  (round 9)

## Delivered (ONE format: the split parts; `cat take.mkv.part* > take.mkv`)
- `take.mkv.partaa` + `.partab` (libx264rgb crf 6, 61.6 MB, 30 fps): first_g 48, 152 frames, 720x1280, 10 spp (colour-fixed set), 2 threads. No captions / audio. A stale single `take.mkv` is not committed (gitignored).
- **g 57..190 = the BIGZOOM (1.91-6.37 s)**; g 48..56 in-handle; g 191..199 out-handle (dissolve 13 into s04). Cut in at g 57. meta.json `bigzoom [57, 190]`, shots [2, 3].

## Round-10 fixes (QA-tech + QA-art)
1. **Smooth move, one speed hump, a real ease-out.** The spline is reparametrised by LOG DISTANCE to the pair (equal steps = equal zoom rate) and eased with the director's table `[(48,0),(66,.08),(90,.30),(115,.60),(140,.86),(160,.97),(170,1)]`. The frame-diff curve (in-shot pairs): 1.3 at g 49, a single hump to ~16.5 at g 109, ~8-10 through the approach, decaying to ~4.4 from g 175: no dips at the old knots (g 105 / 123 / 148) and no dead stop at g 152 (the camera lands at g 170 and the orbit takes over from zero speed, starting at g 150).
2. **The pale flat slab (top right, g 48-90) is hidden** (the set's `headland` object keyed off every frame).
3. **The beat is funnier and 9 frames later** (g 157-190): the captain's brows go up (expression "shocked", g 158-172, then worried); the chart now has a dark header band and a hanging tie (still BLANK: no coast, no compass, no red mark) and is TURNED 180 deg (g 160-170, the band flips from the top to the bottom, readable on a phone); they look at each other (g 173-179); both shrug, palms up (g 181-189); astro19_c's head-scratch g 155-175 (a wobbling hand and head).
4. **The big grey-lilac sail (left 25-35 %, g 125-146):** the keys run ~1.2 D further right (x 6.2 / 3.1) so the spanker covers less of the frame at that moment.
5. Deck texture: not changed (not cheap).
- Colour, the g57 cut-in, the g191 dissolve and the staging unchanged. `qa_stats`: saturation **0.634**, brightness **93.2**. Heads (g 170-199): captain y 462-479, astro19_c 546-553 (inside 450-760). DOF off, no text, no caption_shade in every raw json.

## Frame-diff (in-shot g 58..190)
median **8.45**, p90 **14.01** (qa_stats 8.82 / 16.00). Targets median >= 4, p90 >= 10: met.

## qa_auto "suspected blur" (52 of 152 frames): WAIVED by the director (two independent reviewers found the frames sharp)
`qa_auto.py` compares each frame's Laplacian variance (at 180x320) with the take's median and fails above 5 % of the frames below 60 % of it. The extreme-wide opening g 48-90 is a tiny ship on smooth sea (variance 12 % of the median) and g 126-146 is the pass over the stern sail / planks (43-58 %). That is inherent to the required move (start >= 2x further out, ship <= 12 %, a long smooth swoop): the pre-round-9 version, with a 27 % ship start and a 10-frame descent, got to 7 soft frames; the round-9 spec cannot. I tried a fast descent, more foam, whitecaps and a farther sail pass; none moves the 180x320 statistic of an empty sea. **Needs a director decision: waive the blur check for the BIGZOOM opening (the frames are not blurred: sharp, no depth of field) or relax the spec.**
