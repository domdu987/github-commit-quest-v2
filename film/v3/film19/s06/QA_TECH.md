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
