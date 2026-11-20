# s02 QA_TECH: FAIL
Shot 2, SHIP ship_aerial NOON, take g48-118 (handles 9+9), 6 fps + cuts g57/g110 +-3 checked. qa_auto: PASS (cuts report "no visible change" = expected, handle continues in 3D). No text, no black/magenta/blank frames, no frozen run, no pop, no blur.
## Issues
1. Whole take (in-shot g57-109): frame-diff median 2.04, p90 2.31 (re-measured 2.04 / 2.31) vs target >= 4 / >= 12. FAIL. Ship barely changes size or position in frame; the orbit/crane is not readable. Fix: raise pull to ~9-10 %/s with a real slide/crane (frame-visible travel >= 30 px/s), add the planned pull-back + rise so the ship visibly shrinks, and let the V-wake lengthen (plan row 17 look). Re-measure on a draft.
2. g48-118 (every frame): hard vertical seam / lighter rectangle in the sea below the ship at x ~435 px (y ~ 600-760 of 1280), a tile edge of the re-fitted sea grid or a glare patch. Reads as a render artifact. Fix: widen/overlap the sea grid or hide the patch (move the sun glitter reflection or the grid join out of frame).
3. g48-118: lower ~45 % of frame (y > 700) is flat empty teal; ship occupies 15 % of frame height. Composition weak for the lone-ship hook of "เรือเรือนเดียว"; the plan wants a high drift. Fix: lower the horizon / put the ship in the lower third and let more sea texture (swell/foam, FG gull) fill the bottom, or frame the pull-back so the ship moves down-frame.
4. meta.json: g1 = 110 is exclusive; plan g1 = round(3.65*30)-1 = 109 (shot_ranges 57-109 is right). g0 = 57 matches. Handles in/out 9/9 present. Note only: state the convention or set g1 = 109.

## Round 2: FAIL
Re-checked at 6 fps + cuts g57/g110 +-3 (take g48-118, handles 9/9 in meta). qa_auto PASS (cut "no visible change" = expected handle). No text, no black/magenta/blank, no frozen, no pop, no blur. Frame-diff (take.mkv, deliver.py method): median 3.87, p90 4.76 vs target >= 4 / >= 12.
Earlier issues: 1 NOT FIXED (diff), 2 FIXED (seam gone), 3 mostly FIXED (ship now ~45 % of frame height, orbit/pull readable), 4 note still true (g1=110 exclusive).
1. g57-109 (whole shot): frame-diff median 3.87 (< 4), p90 4.76 (< 12). Motion is a smooth uniform drift; no eased accent, nothing fast. Fix: raise pull to 9-10 %/s plus a faster slide/orbit (visible travel >= 50 px/s), or add a late eased 1.3x push (13-15 f) so p90 reaches 12; re-measure with deliver.py.
NOTES (not blocking): g48-63 overexposed white glitter patch at the left frame edge (x 0-30, y 100-300) fades by g73; g88-118 a gull is clipped by the left edge (wing, ~x 0-20); bottom ~30 % is still plain teal.

## Round 5: FAIL
Checked 6 fps + cuts g57/g110 +-3 (take g48-118), qa_auto PASS, no text/black/magenta/frozen/blur. Frame-diff (take.mkv, 90x160 grey bilinear, g58-109): median 3.81 / p90 18.07 (rule: median >= 4, p90 >= 10).
Earlier: R2-1 (diff) NOT FIXED on the median (p90 now OK); ship fully in frame throughout.
1. g57-109 (frame-diff): median 3.81 < 4. Fix: raise the mid-shot drift/orbit by about 10 % (or lift the pull speed) so the median clears 4 with margin; keep the late accent, re-measure.
NOTES: g48-75 blown-out white glitter patches at the left edge; gull clipped by the left edge g88-118 (not a key prop).
