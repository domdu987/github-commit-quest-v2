# s02 QA: film 19, the BIGZOOM (shots 2 + 3 merged, QA_TEAM section H) -- SHIP ship_aerial, NOON  (round 9)

## Delivered (ONE format: the split parts; `cat take.mkv.part* > take.mkv`)
- `take.mkv.partaa` + `.partab` (libx264rgb crf 6, 61.6 MB, 30 fps): first_g 48, 152 frames, 720x1280, 10 spp (colour-fixed set), 2 threads. No captions / audio. A stale single `take.mkv` is not committed (gitignored).
- **g 57..190 = the BIGZOOM (1.91-6.37 s)**; g 48..56 in-handle; g 191..199 out-handle (dissolve 13 into s04). Cut in at g 57. meta.json `bigzoom [57, 190]`, shots [2, 3].

## Round-9 fixes (QA-art)
1. **Timing: one smooth swoop.** The easing table is now `[(48,0),(66,.10),(90,.35),(115,.70),(135,.92),(152,1)]`: ease in over the first 1.5 s, the descent g 90-130, landing on the medium at g ~152 (5.1 s). Frame-diff peaks ~21 (was 40).
2. **Truly extreme wide start.** The camera starts ~640 D out and 395 D up: the ship is ~10 % of the frame height, captain19 and astro19_c ~4 px (under 5 %, findable). The sea is endless (scattered whitecaps added through the set's own `streaks` hook: runtime, no set edit).
3. **Pass detail on the way down.** The keys run 6-10 D higher: over the stern at the level of the mizzen sails, past the spanker at ~1.9 D and through the shrouds / rigging, then dive to the quarterdeck.
4. **The beat "nobody knows where we are".** The chart is **BLANK** (a runtime patch of cast19's chart drawer: parchment + a fold, no coast, no compass, no red mark). g 148-166: the captain lifts and turns the chart over, brows up (worried); astro19_c lowers the quadrant and gives an obvious head-scratch (wobbling hand and head); g 164-170 they look at each other; g 172-186 both shrug (arms out, palms up, the chart and quadrant dropped). Nobody is still for more than ~1 s (continuous sway, blinks, wobble). No mouth movement.
- Colour kept (colour-fixed set); g57 cut-in and the g191 dissolve kept; staging unchanged (cards ride `ship_root`, camera rides the deck).

## Checks
- **Heads (g 150-199):** captain19 head centre y 454-521 (155-180 px wide), astro19_c 541-578 (134-177 px): all inside 450-760; faces 12-14 % of the frame height (<= 35 %); each figure 33-45 % of the frame height.
- **qa_stats.py:** saturation **0.641** (>= 0.40), brightness **93.6** (70-135).
- **Frame-diff (in-shot g 58..190):** median **5.46**, p90 **18.35** (qa_stats 5.63 / 19.24). Targets median >= 4, p90 >= 10: met.
- DOF off, no text, no caption_shade in every raw json.
- **Cost:** 25 s/frame wall (48 s cpu) at 2 threads (the aerial preset's own is 16 s; the extra is the two cards, the 1500x2000 sea grid and the whitecap lines).

## OPEN: qa_auto "suspected blur" FAIL (58 of 152 frames)
`qa_auto.py` compares each frame's Laplacian variance (at 180x320) with the take's median and fails above 5 % of the frames below 60 % of it. The extreme-wide opening g 48-90 is a tiny ship on smooth sea (variance 12 % of the median) and g 126-146 is the pass over the stern sail / planks (43-58 %). That is inherent to the required move (start >= 2x further out, ship <= 12 %, a long smooth swoop): the pre-round-9 version, with a 27 % ship start and a 10-frame descent, got to 7 soft frames; the round-9 spec cannot. I tried a fast descent, more foam, whitecaps and a farther sail pass; none moves the 180x320 statistic of an empty sea. **Needs a director decision: waive the blur check for the BIGZOOM opening (the frames are not blurred: sharp, no depth of field) or relax the spec.**
