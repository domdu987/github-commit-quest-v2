# s06 QA_TECH: FAIL
Shot 6, HALL hall_table DAY, take g347-474 (handles 9+9, in side DIS 13), 6 fps + cuts g356/g466 +-3 checked. qa_auto PASS. No text, no black/magenta, no blur, no frozen run, no pop. Mouths: expression slit only (fixed), no talking: OK. Bag drop g378-387 visible on the word "รางวัล" (g378): OK; push-in g437-457 on "สองหมื่นปอนด์" (g447): OK.
## Issues
1. g347-474 (whole shot, all frames): frame-diff median 4.53 OK, but p90 6.68 vs target >= 12 (re-measured 4.53 / 6.68). FAIL. No strong move; the snap (g439-454) is the only change. Fix: a faster eased snap (x2-2.5 over 13-15 f) and more slide (>= 50 px/s) so p90 reaches 12.
2. g392-474: astro19_b (planned: leans in beside astro19, eyes glint) is gone: only a grey sliver at the right edge at g387-397, none later. Plan coverage missing. Fix: place astro_b on the right of the table at a mark that stays in frame during the push-in, mirrored, eyes on the bag.
3. g347-377: astro19 (left) is clipped by the left frame edge (wig and half of his head cut at x=0) and astro_b is cut at the right edge. Fix: pull marks inward 0.5 D or open the lens.
4. g447-474: head centre y ~ 375-450 (sheet cell y 125-150 of 427 => 375-450 of 1280), above the 450-760 band; head crowds the top of the frame (wig at y ~ 200). Fix: lower the camera / tilt so the head centre is at y >= 480 at the end of the push.
5. g437-474: the lower 45 % of the frame is empty flat green baize (y > 700), poor composition at the end of the push. Fix: tilt up / lower the table edge, or put the bag lower in frame so the baize carries the bounce.
6. g392-474: eye-line: astro's pupils stay on the lens/up-right, never on the bag (planned "eyes on it, glint"). Fix: aim the pupils at the bag on the drop (g378-390) and keep the glint.
7. g392-474: the bag shows no bounce squash after landing (g387 lands, g392 same shape). Fix: add a 2-3 frame 0.08 D bounce.
8. meta.json g1 = 466 is exclusive (plan g1 = 465). Note only.

## Round 2: FAIL
Re-checked at 6 fps + cuts g356/g466 +-3 (take g347-474). qa_auto PASS. No text, no black/magenta, no frozen, no blur. Bag drop on "รางวัล" g378-387 and push on "สองหมื่นปอนด์" g447: OK. Mouths: fixed expressions, no lip-sync: OK. Frame-diff (take.mkv): median 5.16, p90 10.81 (< 12). Handles 9/9 and g0 = 356 OK.
Earlier issues: 2 FIXED (astro_b present right of table, eyes wide), 3 FIXED for g347-377, 4 FIXED (head centre now ~ 480-560), 5 FIXED (table fills the lower frame), 6 mostly FIXED (eyes wide, glint; pupils on the bag in g397-422), 7 not verifiable at 6 fps (bag sits slightly lower at g392 than g387: acceptable), 8 note still true (g1=466 exclusive).
1. g356-465 (whole shot): p90 10.81 vs target >= 12 (median 5.16 OK). Fix: make the g437-457 snap faster (x2.2 over 13 f) or add 60 px/s slide so p90 reaches 12.
2. g447-466: end of the push crops both astronomers: astro (left) wig and shoulder cut by the left edge, astro_b (right) head about 40 % cut by the right edge from g452. Fix: end the push framed on the bag with both heads inside (stop at ~x1.5, or pan so the bag is centred) or tighten their marks toward the bag by 0.5 D.

## Round 3: PASS
Checked 6 fps + cuts g356/g466 +-3 (take g347-474), qa_auto PASS. No text, no black/magenta, no frozen, no blur. Mouths fixed expressions. Frame-diff (take.mkv, g357-465): median 7.70, p90 12.36: OK. Heads centre ~ 480-600, nothing at 880. Bag drop g378-387 and push on "สองหมื่นปอนด์" g447: OK. astro_b present on the right with wide eyes.
Earlier issues: R2-1 p90 FIXED. R2-2 clipping at end of push: MOSTLY FIXED; both heads and faces inside through g465.
Notes: (a) g463-465 astro19 outer wig lappet/sleeve touches the left edge (~230 rows cut at g464-465), astro_b wig tip touches right edge g457-463; ends on the cut, not noticeable at phone size; stop the push ~2 f earlier if re-rendered. (b) meta g1=466 exclusive.
