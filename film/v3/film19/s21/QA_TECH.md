# QA_TECH s21 - FAIL
Checked: qa_auto PASS, 6 fps sheet g1656-1761, meta g0 1665 / g1 1755 (plan 55.49-58.53 -> 1665/1755 OK), DIS 13 in / DIS 11 out handles 9/9 OK, framediff median 7.35 / p90 12.84 OK, DAY_BARBADOS beach OK, no text, no blur, mouths fixed (no lip-sync). William holds H4 calmly g1656-1706; astro19_c wobbles the quadrant, attached to his raised hand.
Issues:
1. g1741-1755 (head limit): astro head bottom reaches y ~ 900-925 (meta head_centre_y max 788, head 457 px wide) = inside the caption band (>= 880); head centre also > 760 (out of 450-760). Fix: end the push earlier / raise the camera so the head centre stays <= 760 and chin < 880.
2. g1706-1755: both heads clipped by the frame. Astro's head/hat is cut by the left edge from g1711; William's hat/face is cut by the right edge g1706-1755 (face half off at g1741-1751). Fix: push to a two-shot framing, not a close-up of the pair; keep x 20-700.
3. g1711-1755 (plan coverage / prop): William's H4 hand is out of frame after the push (last seen g1701-1706), so "William holds the H4 calmly" is lost for the second half; the shoes are also cut at the bottom. Fix: reframe to keep his watch in view.
4. g1696-1761: astro looks into the lens, not at the sky he is "fumbling at" (eye-line). Fix: eyes up-left toward the quadrant.
5. g1686-1691: astro mouth changes from flat frown to wavy zig-zag. Expression swap, not lip-sync, but it is a mouth shape change outside quote windows; hold one mouth shape.
6. g1656-1706: astro feet have only a faint shadow; William's feet OK. Minor.

## Round 2 - PASS (notes)
Checked: qa_auto PASS (cut g1756 = handle boundary); 6 fps + cut sheet g1656-1761; meta g0 1665 / g1 1755, DIS 13 in / DIS 11 out, 9 f handles OK; frame-diff median 6.59 / p90 12.85 (measured).
Verification of round 1: 1 head limit FIXED (chin <= ~700, centre <= 735). 2 clipping FIXED (both heads inside x 20-700 through g1755). 3 H4 in hand FIXED (William holds the H4 to the end, shoes in frame). 4 eye-line NOT fixed (astro eyes still squint forward/down toward the lens while the quadrant points at the sky) - NOTE only, the wince reads as squinting at the sun. 5 mouth FIXED (one wavy mouth throughout). 6 shadows FIXED.
Notes: (a) g1736-1745 and g1761 the quadrant fan covers half of William face/hat (g1761 is in the dissolve handle). (b) astro eye-line as above.
