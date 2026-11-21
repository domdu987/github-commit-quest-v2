# QA-tech, SET gate, set3d9, ROUND 2 (film 9, wall_site + macro)
Checked: contact.jpg (33 tiles + 6 refs), all 33 finals in wall_work/final at 720x1280 (y 880 line drawn, 1:1 crops of wall_top_battle and gate_dusk), wall_API.md, shot_plan.md.

## VERDICT: PASS (conditional). No picture failure. All blocking coverage gaps (shots 2, 4, 6, 19) now have a camera. Open items are small-figure legibility (shots 7, 12), the "today" variant of shot 17, and minor polish.

## Picture checks (round 2)
- Blur/DOF: none. Billows are now hard-edged cartoon shapes and read as intentional. Macro bricks sharp.
- Black / magenta / blank / tofu: none. Dark macro bricks are intentional. No Thai text in any frame.
- Floating / z-fight: none. Cannon_line_impg: one detached white puff right of the foreground smoke column (x ~ 540-600, y ~ 600) reads as a floating cloud, cosmetic only.
- Heads vs y 880: all staged heads above it (two_shot_low heads ~ 390-560, pour_close Lin ~ 440-600, wall_top_battle general ~ 480-600). Tightest still site_wide lin chin 852.
- Clipping: two_shot_low Lin's hat brim touches the right frame edge (x ~ 715); a small dark object (crane arm / pole) sits beside his hat at x ~ 690-700. Minor.

## Previous issues
1. Shot 6 two-shot: FIXED. `two_shot_low` DAY: general left, Lin right, low eye-level, wall + scaffold behind, both faces readable. (See new issue A for the right-edge crop.)
2. Shot 4 gate: FIXED, weak. `gate_dusk` shows the gate tower, mountains and the host on the horizon (black/red banners + pale dust bank at left, smoke at right). Works as a "hint", but banners are ~10-15 px tall and the dust is pale blobs. See new issue B.
3. Shot 18 inner face crack: FIXED enough. The inner BATTLE frame is brighter and the stair-step cracks on the general's section are readable (low contrast). `two_sections_out` crack0.66 and the crack0.33 star + dust puff read clearly. Use the outer view for the hero crack read.
4. Shot 19 wall_top BATTLE: FIXED. `wall_top_battle` exists, 30-course height correct, general on top (head fine), BATTLE sky, crane and basket. The collapse is on `two_sections_out` col0.35 / 1.0 (both fine: debris, dust, torch foreground). No army visible from this camera (not needed).
5. Shot 17 aftermath: PARTLY FIXED. `aftermath_dawn` now exists: three dents with embedded balls on Lin's outer face, wall whole, blue DAWN. Dents are dark and a bit small. There is still no "today" weathered variant and no moss (API admits it). Needs a decision: do the dissolve with a post/grade, or render a moss variant. `site_wide_DAWN` itself still has no dents (use aftermath_dawn, or add dents for the wide shot).
6. Smoke softness: FIXED. Billows now hard-edged two-tone. Collapse dust (col1.0) is still translucent and slightly soft at the overlapping edges, acceptable.
7. Small figures, shots 7 and 12: NOT FIXED. Workers are ~55-85 px tall in `site_wide` / `two_sections`; no closer worker camera. `two_shot_low` and `pour_close` help for shots 2 and 6 only. Lin in `two_sections_RAIN` (shot 12) is ~80 px with no expression readable. FIX: a medium camera on the workers stand point for shot 7 and one on Lin for shot 12, or approve a crop of the existing render in the take.
8. Blown highlights: FIXED (site_wide DAY, two_sections DAY and wall_top DAY no longer clip visibly).
9. Macro shards: FIXED. Shards are now brick-red and grey grit. Crack ribbons still read as black cartoon ribbons with a tan lip, drawn over the ball only before impact; at t 0.45 the ball is in front. Beat is showable. Rice macro (t 0 / 0.36 / 0.9) shows web, ball + glow, and held ring; the dent at 0.9 is subtle (ball gone, web glowing).
10. site_wide lin chin 852: NOT FIXED (unchanged, 28 px margin). Handle in the take (lower the cam about 1 D or confirm card scale).

## New issues
A. `two_shot_low` (shot 6): Lin is ~20% of the frame and his hat touches the right edge, with a dark object beside it. Mouth sync is only for the general, so acceptable. FIX (optional): shift the look-at about 0.5 D toward +x (or move Lin's stand point 0.3 D left).
B. `gate_dusk` (shot 4): the horizon hint is faint. FIX (optional): scale the horizon banners about 1.5x or darken the dust bank. A client who wants "something on the horizon" will read it, but only just.
C. Shot 2: `pour_close` shows Lin at the trough with the cauldron; the pour of milky soup and the troweling between bricks are cast/FX work, not in the set. Camera is OK (Lin head above 880).
D. Shot 16 check: at macro 0.9 the "ball only dents" read relies on the ring glow; make sure the take keeps the ball visible (embedded or resting) at the dent frame.

## Coverage by shot
1 cauldron DAY ok. 2 pour_close ok. 3 site_wide DAY ok. 4 gate_dusk ok (weak, B). 5 cauldron DAY ok. 6 two_shot_low ok. 7 site_wide / two_sections, figures small (7). 8 two_sections DAY ok. 9 cauldron DAWN ok. 10 two_sections DAY h-keyed ok. 11 wall_top DAY ok. 12 two_sections RAIN ok, Lin small (7). 13 wall_top RAIN ok. 14 cannon_line BATTLE ok (gunners distant). 15 / 16 macro ok. 17 aftermath_dawn ok, "today" variant open (5). 18 two_sections_out crack frames ok. 19 wall_top_battle + two_sections_out collapse ok.
