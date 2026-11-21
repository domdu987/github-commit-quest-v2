# s09 QA_TECH

## Round 2: FAIL
Shot 9, HALL hall_low DAY (closer), take g652-781 (handles 9/9; meta g0 661, g1 773 exclusive: note), 6 fps + cuts g661/g773 +-3 checked. qa_auto PASS. No text, no black/magenta/blank, no frozen run, no pop, no blur. Mouth: moves g652-777, all inside g 627-776 (+-5): OK; astro19 alone on frame: OK. Heads centre y ~ 540-600, bottom well above 880 (closer framing). Pocket watch is held in his raised glove and swings with the hand: OK. Snap on "จับเวลาเอง" g748: visible g747-757: OK. Eye-line to lens (low angle, mocking): OK.
1. g661-772 (whole shot): frame-diff median 4.38, p90 10.74 (< 12). Fix: a faster snap (x1.5 over 13 f, eased) at g748 and a slightly stronger slide so p90 reaches 12; re-measure with deliver.py.
NOTES: g757-777 wig right edge exits the frame (acceptable in this close-up); no feet visible (low closer framing), so contact shadows cannot be checked; the "bow" reads as a sway/lean, not a clear deep bow (plan: mock-royal bow), watch reading as "timing" is clear.

## Round 3: FAIL
Checked 6 fps + cuts g661/g773 +-3 (take g652-781), qa_auto PASS. No text, no black/magenta, no frozen, no blur. Mouth moves g652-777 only, inside 627-776 +-5 (astro19 alone): OK. Heads centre ~ 530-610, bottom < 880. Watch swings in his glove. Snap on "จับเวลาเอง" g748 visible.
Earlier issues: R2-1 NOT FIXED and worse.
1. g662-772 (R2-1): frame-diff (take.mkv, g662-772) median 3.29 (< 4), p90 5.95 (< 10); deliver framediff.json 3.12 / 5.51 (round 2 was 4.38 / 10.74, so the move got weaker). FAIL against median >= 4 / p90 >= 10. Fix: restore the push + slide of the previous render and add the faster snap (x1.5 over 13 f, eased) at g748.
Notes: right wig lappet crops at the right edge g756-772 (face inside, close-up, accepted in R2); bow still reads as sway; no feet visible; meta g1=773 exclusive.

## Round 6 (director QA-tech): PASS (re-judged against the exact §G3 text)
Re-judged against the exact QA_TEAM §G3 text ("No character cut in half by a frame edge"): shoes/shins cropped at the bottom g748-772 and a sliver of left coat hem/sleeve g742-772 are normal low-angle medium framing; the figure is whole (face, wig, torso, both hands and the watch all inside) in every frame. Issues 1 and 2 below are downgraded to non-blocking notes. No other blocking issue.
Take g652-781 (meta g0 661, g1 773 exclusive), frames at 6 fps + every frame g743-762 (snap) + g720-734 + g773-780, in /tmp/qa19_r6b/s09/. Re-render with face caps.
PASS items: frame-diff (90x160 grey bilinear, in-shot g661-771, computed here) median 5.36, p90 11.36 (>= 4 / >= 10); min 2.30, no frozen run, no black frame, luma min 57. Mouth moves only inside the quote window (meta list empty; seen open g652-777, closed/flat at g774-775, no talking after +0.15 s in the shot; handle g779-780 shows mouth movement, outside the cut, non-blocking). Face (no wig) about 16-19 % of frame height at the g748-752 punch peak (< 35 %). Wig bottom about y 780-800 at peak (< 880). Eye-line to lens, pocket watch held in glove and swings with the hand, astro19 alone, no cut-in-half. The snap g743-762 reads as an intended push. Extra push g722-729 (diff 15-18, head grows then eases back g730-734) is smooth, no pop.
Issues:
1. g748-772 (and handle to g781): both shoes and lower shins are cut by the bottom edge (only the hands may be clipped). Fix: after the snap hold framing so the shoes stay in (reduce the push scale to <= 1.12 or tilt up less), or pull the mark back 0.2 m.
2. g742-772: the left hem and sleeve of the star coat are cut by the left edge (body clipped, not a hand). Fix: slide the camera right or reduce the slide during the snap so the left coat stays inside x >= 0.
NOTES: the "bow" still reads as sway/lean (carried over, art note); contact shadows at the feet are only visible g652-745.

## Round (camera-shake pass, film-13 rules): PASS (3 non-blocking notes)
Take s09 (HALL hall_low closer, g661-772, handles g652-660 / 773-781), re-rendered by team 4 for camera shake. Judged only by film/skill_film13/QA_TEAM_film13.md (base checklist + §B). My frames: /tmp/qa19_r21/s09/gNNNN.png from take.mkv (g700 byte-identical to /tmp/qa19_ov/s09). qa_auto run myself (--cuts 661,773 --first_g 652): PASS (only the handle note at g661 / g773; magenta 0.0 %). qa_jitter reproduced: 3s 2.1 px, median 1.59. GROUND.md PASS.
Camera vs actor: same masked-background tracking as s08 (actor masked, LK + RANSAC similarity, second difference of the image-centre shift, seconds aligned to the take start): second 0 (g653-682) median |d2| 0.35 px (max 1.6); second 1 (g683-712) 0.31 (max 2.4 at g688); second 2 (g713-742) 0.76 (max 2.5 at g722, the eased x1.10 deep-bow punch); second 3 (g743-772) 0.73 (max 2.9 at g748, the eased x1.16 quote punch / snap). Overall 0.52 px; frames with |d2| > 2: g688-689, 693, 695, 722, 748, 776-777. So the 2.1 px qa_jitter reads for second 3 is the bow sway of the actor over a steady camera (camera 0.73 px), and the one-directional travel (slide 25 -> 60 px/s, orbit 7 -> 11 deg/s, camera speed 2.5 -> 1.3 px/f) is smooth: no pump, no reversal.
Checklist:
- Blur/DOF: none; Laplacian variance median 336, min 278.
- Heads below y 880: none (wig top ~y 230-420, chin <= ~560 of 1280).
- Clipped sprites/props: nobody cut mid-body in the medium (g652-720 shows feet and legs); from the bow g722-760 the legs leave the bottom edge (a punch-in crop, not a clip). Pocket watch is visible in the right hand g668-734 (sampled g668, 684, 700, 716, 734); at the quote punch g752 the arm is raised and the watch is hidden behind the wig/hand: acceptable.
- Floating feet / contact shadows: feet on the carpet with contact shadows in g652-740 (sheet and g668-734 crops); GROUND PASS; nothing floating.
- Pops/jumps outside cuts: none. Frame-diff in shot g662-772: median 4.59, p90 11.95, max 21.69 (the snap g747-752), min 2.84; ratio jumps only at g723/g729 (the deep-bow punch, eased) and g747-748 (x2.06 / x1.57, the planned quick push-in on "จับเวลาเอง" 24.82 s). No black/blank/magenta frames (luma 68.9, per frame 57.1-78.1; saturation 0.704). No frozen runs (nothing under 0.3).
- Continuity: s08 g659-660 (close-up, quote punch) -> s09 g661 (medium, same mocker, same costume, same hall, same lighting) planned hard cut; s09 g771-772 (medium-close, mid-bow) -> s10 g773 (hall_wide, the whole Board laughing, the mocker on the right of the aisle) planned hard cut; costume and light consistent.
- Plan coverage (shot_plan row 9, 22.02-25.78): mock-royal bow while miming timing a pocket watch, mouth moving (window g652-781), quick push-in on "จับเวลาเอง" (g747): all visible.
- Mouth: lip-sync inside the quote window g652-781 only; no mouth movement outside it.
- Nobody still > 1.5 s: the actor sways, bows and mimes throughout.
Numbered notes (non-blocking): 1. qa_jitter prints 2.1 px for second 3 (0.1 px over its 2.0 line): the bow sway, camera 0.73 px. 2. Legs leave the bottom edge from the deep bow (g722-760); brief punch-in crop. 3. Luma 68.9 / saturation 0.70 (deep red hall); film-13 has no luma rule.
Verdict: PASS.
