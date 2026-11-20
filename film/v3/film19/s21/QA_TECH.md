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

## Round 7 (director QA-tech) - FAIL
Checked: take.mkv 109 frames, meta g0 1665 / g1 1756 (shot 1665-1755), first_g 1656; 6 fps frames in /tmp/qa19_r7b/s21/ and EVERY frame g1720-1756 in /tmp/qa19_r7b/s21/all/ (viewed at 36 frames plus head crops).
Numbers: frame-diff (90x160 grey, bilinear, 90 consecutive in-shot pairs g1665-1755): median 5.86 (>= 4 OK), p90 10.42 (>= 10 OK, thin margin), min 1.73, max 12.0. No frozen runs (min consecutive diff 2.7), no black frames, no pops.
Passed: both characters fully inside the frame (x 35-700) incl. feet, no half-character cut; face height ~20 % (< 35 %); heads y centre ~ 560-640 (< 880); feet on the sand with contact shadows (astro shadow soft but present all through g1720-1756); William holds the H4 up calmly to the end, his face is NEVER covered by the quadrant (the swing across faces is gone); mouths fixed (astro wavy frown, William smile), no lip-sync; astro moves constantly (lean/wobble every ~0.5 s).
Issues:
1. Quadrant still overlaps astro19_c's own face. It now sits on the cap/forehead like a visor, but its lower edge and the black pivot blob cover astro's brow and the upper half of one eye (right eye) in many frames: strongest at g1733-1737, g1744-1752 and g1754-1756 (e.g. g1735, g1750: eye half hidden by the pivot), and the pivot touches the eye corner in g1720-1732 as well. The brief says it must never cover a face. Fix: raise the quadrant 25-35 px above the brow (or hold it at the side of the head) so the pivot clears both eyes.
2. g1724-1729: quadrant tip comes within ~10 px of William's tricorne brim (tangent, no overlap on his face). Minor, re-space.
3. g1720-1756: palm trunk runs directly behind William's head and hat (tangent), minor.
4. William stands almost still (only the camera drift and slight sway) for the whole 3 s; allowed by the brief ("calm") but breaks the 1.5 s rule in the letter. Suggest a small watch-hand wave or head tilt at g1700 and g1730.
5. Eye-line: astro eyes still squint toward the lens, not up (note carried from round 2).

## Round 9 (director QA-tech) - PASS (with notes)
Checked: take.mkv 109 frames, meta g0 1665 / g1 1756 (shot g1665-1755), first_g 1656; 6 fps frames in /tmp/qa19_r9b/s21/f6/ and every frame in /tmp/qa19_r9b/s21/all/ (file index = g - 1656 + 1); g1720-1756 viewed frame by frame as head crops.
Numbers (measured by QA-tech):
- Frame-diff (90x160 grey, bilinear, 89 consecutive in-shot pairs g1665-1755): median 6.12 (>= 4 OK), p90 11.89 (>= 10 OK), min 1.89, max 13.41. No pop, no black frame, no frozen run.
- Quadrant: lifted. In g1720-1756 it sits above the helmet like a crest and never touches astro19_c's brow or either eye (round 7 issue 1 FIXED). It never covers William's face or eyes. The green sleeve/hand holding it passes next to astro's right cheek/ear edge at g1720-1735 but no eye is hidden.
- Quadrant tip vs William's tricorne: closest approach at g1725-1726 and g1742-1743, about 30-35 px by eye (corner to brim tip, mostly vertical offset). >= 20 px OK (measured by eye on 1:1 crops, not pixel-segmented).
- Characters: both fully inside the frame (x ~ 20-700), no half-character cut; astro face ~16-20 % of frame height (< 35 %); head centres y ~ 450-640 (< 880); feet on sand with contact shadows, nothing floats. Mouths fixed (astro wavy frown, William smile), no lip-sync.
- Motion/no-still rule: astro moves constantly (region diff never below 8). William's head/torso and watch-hand region shows bursts of motion at about g1672-1680 (nod), g1692-1696, g1700-1706 (glance/turn), g1722-1730, g1744-1752 with no gap longer than ~20 frames (0.7 s); lowest region diff 3.9. Nobody still > 1.5 s.
Notes:
1. William's new acts are small at phone scale. The nod at g~1672-1680 (head dips ~15-20 px) reads. The glance from g~1695 is hard to read because William's eyes are closed arcs and the head turn is slight. The thumb-wipe g1722-1746 reads only as a small watch/hand jiggle (~10-20 px). Not a fail, but QA-art may want a bigger head turn toward the astronomer.
2. g1720-1756: the palm trunk still runs directly behind William's head/hat (tangent), minor.
3. Astro eye-line still squints toward the lens (carried note).
4. At g1750-1755 astro leans so his hair-tail comes within ~25-40 px of the left edge; still inside.

## Round 10 (director QA-tech) - FAIL
Checked: take.mkv 109 frames 720x1280 30 fps, meta g0 1665 / g1 1756 (shot g1665-1755), first_g 1656; 6 fps frames in /tmp/qa19_r10b/s21/f6/, every frame in /tmp/qa19_r10b/s21/all/ (file index = g - 1656 + 1); montages of every frame g1665-1755, 1:1 crops of the quadrant/tricorne, left edge, William's face and the watch.
Numbers (measured by QA-tech, 90x160 grey bilinear, 90 in-shot pairs g1666-1755):
- Frame-diff: median 6.85 (>= 4 OK), p90 13.00 (>= 10 OK), min 2.04 (g1699), max 14.99 (g1749). No pop, no black frame (min frame mean 106), no frozen run.
- Quadrant vs William's tricorne (segmented: gold fill vs the dark hat body, edge to edge, outline ~3-4 px not subtracted): gap 11 px at g1708 and g1726, 12 at g1706, 13 at g1741, 14 at g1727 and g1742, 17 at g1705, 19 at g1707, 24 at g1725 and g1740. Real gap after the outline is ~5-10 px; by eye the fan visually touches the brim at g1726-1727 and g1741. REQUIREMENT >= 20 px FAILS at g1705-1708, g1725-1727, g1740-1742.
- Quadrant never covers William's face or eyes; never covers astro19_c's eyes/face (sits above the helmet like a crest; pivot clear of the brow all through).
- EDGE: astro19_c is cut/touched by the LEFT frame edge at g1695-1700 (quadrant left corner and hair tail at x ~ 0-10, hand ~ x 25) and the hair tail is within ~10 px of the left edge g1752-1755. Brief says no character cut by an edge.
- William's glance: eyes are closed arcs through g1698, switch to open half-lid eyes at g1699-1700 (56.65 s, ~5 frames after 56.5 s) and the head turns toward the astronomer g1700-1712. Reads (a smug lid-eyes glance, no pupils).
- Thumb circular rub g1718-1750: reads as the watch/hand bobbing in a small loop (~30-50 px) under his chin, the thumb itself is not visible (sleeve hides it); the loop is legible only as watch wobble, not as a thumb rub. At g1750 his eyes become happy arcs.
- Astronomer "looking up": head tilts back with the quadrant lifted (g1665-1680, g1736-1744), but the eyes stay a forward/downward squint, no upward pupil. Mouth: fixed wavy frown, no lip-sync.
- Foreground crates/barrels: barrel + dark crate at right (g1665-1740) and dark crate right of William (g1721-1755) sit on the sand with shadows, boat hull at left, rope coil lower-left from g1707: nothing floats; no prop touches a face. Tangent: palm trunk runs directly behind William's head/ponytail g1668-1756 (tangent; read as an ear-pole), and the right barrel/crate is tangent to the palm base. Props are cut by the side edges (acceptable).
- Characters: faces ~16-20 % of frame height, head centres y ~ 450-640 (< 880), feet on sand with shadows. Rim light visible and vivid colours OK.
- Nobody still > 1.5 s (astro constant, William watch/head acts every <= 20 frames).
Issues:
1. FAIL: quadrant to William's tricorne gap < 20 px (5-10 px real) at g1705-1708, g1725-1727, g1740-1742. Fix: move the quadrant 25+ px left/up or shift William right ~30 px in those windows.
2. FAIL: astro19_c cut/touched by the left edge g1695-1700 and hair tail ~10 px from it g1752-1755. Fix: shift the framing right/astro right by ~40-60 px.
3. Thumb rub not legible as a thumb (see above). Suggest showing the thumb on the watch crystal.
4. Palm trunk tangent behind William's head g1668-1756.
5. Astro eye-line still squints forward, not up.

## Round 11 (director QA-tech) - PASS (with notes)
Checked: take.mkv 109 frames 720x1280 30 fps, meta g0 1665 / g1 1756 (shot g1665-1755), first_g 1656; 6 fps frames in /tmp/qa19_r11/s21/f6/ (22), every frame in /tmp/qa19_r11/s21/all/ (file index = g - 1656 + 1); 6 fps sheet viewed whole, worst-frame crops at 1:1 with a 50 px grid, left-edge strips for g1696-1700, g1752-1755, g1740-1744.
Numbers (measured by QA-tech):
- Frame-diff (90x160 grey, ffmpeg bilinear, 90 consecutive in-shot pairs g1666-1755, i.e. frame pairs inside g1665-1755): median 6.86 (>= 4 OK), p90 12.84 (>= 10 OK), min 2.26, max 14.87. No pop, no black frame (min frame mean 110.7), no frozen run (no pair < 2.0).
- ROUND 10 ISSUE 1 (fan to tricorne, FIXED): quadrant gap to William's tricorne at the worst frames, measured on 1:1 crops with a grid: g1706-1708 about 60-65 px (fan right edge / sleeve to brim left tip), g1725-1727 about 60 px, g1740-1743 about 60-75 px. Automatic fan-segment (gold) to hat-body (dark) minimum is 87 px at g1707, 89 at g1706 and g1743, 98-103 at g1725-1727, 107-109 at g1741-1742 (hat body only, brim tips/outline excluded, so by-eye ~60 px is the conservative figure). All >= 20 px (was 5-10 px). The fan never touches or covers William's face/hat.
- ROUND 10 ISSUE 2 (left edge, FIXED): astro19_c at g1695-1700: closest part is the quadrant left corner / glove at x ~ 50-55 (g1698-1699), green coat x 62 at g1699, hair tail ~ 70+; air >= ~50 px (need >= 30 OK; was 0-10). g1752-1755: hair tail x ~ 140-165, glove ~ 145: air >= ~140 px. No character touches or is cut by the left or right edge anywhere g1665-1755 (William's hat/ponytail right side x <= ~700).
- Astronomer pupils: now look up (circle eyes with pupils at the top, visible at g1690, g1712, g1735 and the whole shot); eye-line to the quadrant/sky FIXED (carried note closed). Mouth fixed wavy frown, no lip-sync, no mouth movement.
- William glance: eyes are closed arcs through g1697, open half-lid eyes from g1698 (not g1696 as briefed; 2 frames / 0.07 s late, not noticeable) with the head turning toward the astronomer; reads clearly now. Happy arcs again at the end.
- Watch rub: bigger loop; the watch swings visibly (~60-80 px incl. camera drift) and the dark glove/thumb is visible against the watch at g1737-1743. Reads as a watch rub at phone scale. OK.
- Characters: both fully inside the frame with feet on sand and contact shadows; no half-character cut; faces ~15-20 % of frame height (< 35 %); head centres y ~ 450-640 (< 880); nothing floats (crates, barrels, rope coil, boat hull sit on sand); no prop touches or crosses a face; quadrant never covers astro's eyes or William's face. Camera pulled back: wider, shows sea, ships, palm, set; vivid colours/rim light OK.
- No-still rule: region frame-diff (astro half and William half of frame) min 5.5 / 3.4 per consecutive pair, no run < 2.0; both act continuously (astro wobble, William glance/watch loop/nod). Nobody still > 1.5 s.
Notes (non-blocking):
1. Palm trunk still tangent directly behind William's head/ponytail for most of the shot (carried minor).
2. g1699 astro's glove/fan corner is the closest point to the left edge (~50 px) - fine but do not push the framing further left.
3. William glance opens at g1698 instead of g1696 (see above).
VERDICT: PASS - both Round 10 failures fixed (fan gap ~60 px >= 20; left air >= ~50 px >= 30), all usual checks pass, frame-diff median 6.86 / p90 12.84.
