# s20 QA_TECH

## Round 2: FAIL
Shot 20, HALL hall_low DAY, take g1572-1673 (handles 9/9; meta g0 1581, g1 1665 exclusive: note), 6 fps + cuts g1581/g1665 +-3 checked. qa_auto PASS. No text, no black/magenta/blank, no frozen run, no pop, no blur. Mouth: first opens g1627, last open g1668, inside g 1631-1667 +-5: OK; astro19 alone. Snap on "ฟลุ๊ค" g1632: visible g1632-1642: OK. Heads centre y ~ 570-640, nothing at 880. Frame-diff (take.mkv): median 3.79, p90 9.66 vs target >= 4 / >= 12.
1. g1581-1665 (whole shot): frame-diff median 3.79 (< 4), p90 9.66 (< 12). Fix: push 9 %/s is not reaching the frame (slow ~1 %/frame); add slide >= 50 px/s and a faster snap (x1.6 over 13 f), re-measure with deliver.py.
2. g1597-1625: plan "shrugs, palms up": the shrug (cue peak g1615) is not legible; shoulders barely move and the hands stay hidden behind the wig/sides, no palms up until g1632+ (hands low at the sides, not palms up). Fix: lift both arms out to the sides, palms up, elbows bent, with a 0.06 D shoulder rise, timed g1605-1625.
NOTES: g1572-1620 feet have only faint contact shadows on the carpet; thick black arc (armillary) at upper left g1572-1592 is the set; wig clipped by the left edge at g1642-1672 in the close-up (acceptable); meta g1 = 1665 exclusive.
