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

## Round 6 (director QA-tech): FAIL
Take g652-781 (meta g0 661, g1 773 exclusive), frames at 6 fps + every frame g743-762 (snap) + g720-734 + g773-780, in /tmp/qa19_r6b/s09/. Re-render with face caps.
PASS items: frame-diff (90x160 grey bilinear, in-shot g661-771, computed here) median 5.36, p90 11.36 (>= 4 / >= 10); min 2.30, no frozen run, no black frame, luma min 57. Mouth moves only inside the quote window (meta list empty; seen open g652-777, closed/flat at g774-775, no talking after +0.15 s in the shot; handle g779-780 shows mouth movement, outside the cut, non-blocking). Face (no wig) about 16-19 % of frame height at the g748-752 punch peak (< 35 %). Wig bottom about y 780-800 at peak (< 880). Eye-line to lens, pocket watch held in glove and swings with the hand, astro19 alone, no cut-in-half. The snap g743-762 reads as an intended push. Extra push g722-729 (diff 15-18, head grows then eases back g730-734) is smooth, no pop.
Issues:
1. g748-772 (and handle to g781): both shoes and lower shins are cut by the bottom edge (only the hands may be clipped). Fix: after the snap hold framing so the shoes stay in (reduce the push scale to <= 1.12 or tilt up less), or pull the mark back 0.2 m.
2. g742-772: the left hem and sleeve of the star coat are cut by the left edge (body clipped, not a hand). Fix: slide the camera right or reduce the slide during the snap so the left coat stays inside x >= 0.
NOTES: the "bow" still reads as sway/lean (carried over, art note); contact shadows at the feet are only visible g652-745.
