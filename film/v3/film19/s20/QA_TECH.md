# s20 QA_TECH

## Round 2: FAIL
Shot 20, HALL hall_low DAY, take g1572-1673 (handles 9/9; meta g0 1581, g1 1665 exclusive: note), 6 fps + cuts g1581/g1665 +-3 checked. qa_auto PASS. No text, no black/magenta/blank, no frozen run, no pop, no blur. Mouth: first opens g1627, last open g1668, inside g 1631-1667 +-5: OK; astro19 alone. Snap on "ฟลุ๊ค" g1632: visible g1632-1642: OK. Heads centre y ~ 570-640, nothing at 880. Frame-diff (take.mkv): median 3.79, p90 9.66 vs target >= 4 / >= 12.
1. g1581-1665 (whole shot): frame-diff median 3.79 (< 4), p90 9.66 (< 12). Fix: push 9 %/s is not reaching the frame (slow ~1 %/frame); add slide >= 50 px/s and a faster snap (x1.6 over 13 f), re-measure with deliver.py.
2. g1597-1625: plan "shrugs, palms up": the shrug (cue peak g1615) is not legible; shoulders barely move and the hands stay hidden behind the wig/sides, no palms up until g1632+ (hands low at the sides, not palms up). Fix: lift both arms out to the sides, palms up, elbows bent, with a 0.06 D shoulder rise, timed g1605-1625.
NOTES: g1572-1620 feet have only faint contact shadows on the carpet; thick black arc (armillary) at upper left g1572-1592 is the set; wig clipped by the left edge at g1642-1672 in the close-up (acceptable); meta g1 = 1665 exclusive.

## Round 3: FAIL
Checked 6 fps + cuts g1581/g1665 +-3 (take g1572-1673), qa_auto PASS. No text, no black/magenta, no frozen, no blur. Mouth: first open g1627, last g1672, inside g1631-1667 +-5; astro19 alone: OK. Heads centre y ~ 470-640, nothing at 880. Frame-diff (take.mkv, g1582-1664): median 4.13, p90 10.71 (passes, but only just; deliver framediff.json on the source frames says 3.80 / 10.16, i.e. below 4: re-measure on the final conform).
Earlier issues: R2-1 frame-diff FIXED on the mkv (marginal); R2-2 shrug: FIXED in the wide g1613-1636 (both arms out to the sides, readable), BUT see 1. QA_ART round 4 (FIX-FIRST 6.5): fix 1 FIXED, fix 4 FIXED, fix 2 OPEN (squash 0.02, head_roll -6), fix 3 OPEN.
1. g1640-1665 (QA_ART fix 3 / R2-2): from the snap on, both arms and hands run off the left and right frame edges (hands/cuffs cropped at x 0 and x 720), so the shrug is lost on the quote; the visible hands are small dark mitts, not open palms. Fix: snap k 1.4 -> 1.25 / peak 2.6 -> 2.0 so both palms stay inside x 40-680, hands skin/white so they read on the navy coat.
2. g1627-1672 (QA_ART fix 2): shoulder squash/head roll not visible; the shrug carries only through the arms. Fix: squash (1.04, 0.96) and head_roll -10 on the pump.
Notes: QA-art must PASS this key shot before conform (it is still FIX-FIRST); left wig lappet crops at the edge g1654-1672 (accepted); meta g1=1665 exclusive.

## Round 5: PASS
Checked 6 fps + cuts g1581/g1665 +-3 (take g1572-1673), qa_auto PASS. No text/black/magenta/frozen/blur. Mouth: first open g1626 (window 1626-1672), last open g1666, flat afterwards, inside g1631-1667 +-5; astro19 only. Heads centre y ~ 470-640. Frame-diff g1582-1664: median 4.48 / p90 11.28 OK.
Earlier: R3-1 FIXED: both hands/cuffs are now inside the frame through the snap (hands at x ~ 60-100 and 600-680, no cropping); R3-2 squash/head roll visible.
NOTES: the hands are small dark mitts, palms do not read as open; QA-art still has to PASS this key shot before conform; left wig lappet crops at the edge g1654-1672 (accepted).

## Round 6 (director QA-tech): PASS (re-judged against the exact §G3 text)
Re-judged against the exact QA_TEAM §G3 text: shoes/shins cropped at the bottom g1634-1664 and a sliver of left coat hem g1648-1664 are normal low-angle medium framing; the figure is whole (face, wig, torso, palms-up hands) in every frame, no hand or face carrying the action is cut. Issues 1 and 2 below are downgraded to non-blocking notes. The black curved bar top-left g1572-1592 is set dressing: a large black ring/arc with a brass brace in the foreground (armillary/instrument ring), seen close to the lens; it sweeps out of frame by about g1597, never crosses the face; not an artefact.
Take g1572-1673 (meta g0 1581, g1 1665 exclusive), frames at 6 fps + every frame g1628-1646 (snap) + g1651-1663 (pump 2) + g1672-1673, in /tmp/qa19_r6b/s20/. Re-render with face caps.
PASS items: frame-diff (90x160 grey bilinear, in-shot g1581-1663, computed here) median 4.65, p90 12.01 (>= 4 / >= 10); min 2.94, no frozen run, no black frame, luma min 65. Mouth closed g1572-1622, moving g1627-1667 inside 54.25-55.45 s +-0.15 s (g1623-1668); none after. Shrug g1609-1621 with palms up, hands visible and not clipped. Face (no wig) about 16-21 % of frame height at the snap peak g1631-1636 and at the end (< 35 %). Wig bottom about y 825 at the end (< 880). Snap g1631-1636 (diff 14-18) reads as an intentional FOV punch, no pop. Eye-line to lens, astro19 alone, no cut-in-half.
Issues:
1. g1634-1664 (handle to g1673): shoes and shins are cut by the bottom edge once the push settles (only the hands may be clipped). Fix: cap the push scale at about 1.15 and keep the frame centre about 60 px lower so the shoes stay in, or end the push at the knee-high framing of g1628.
2. g1648-1664: the left hem of the coat is cut by the left edge (body, not a hand). Fix: reduce the slide so the coat stays inside x >= 0.
NOTES: a black curved bar at the top left g1572-1592 (telescope cable or ring) is a bit odd but attached to the telescope, no face crossing; contact shadows visible only g1572-1633.
