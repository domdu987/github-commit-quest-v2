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
