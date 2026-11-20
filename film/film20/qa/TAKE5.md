# QA-tech TAKE gate round 5, film 20: s06 s21 s24 (+ s09 for the join check)
Method: takes rebuilt from parts, all frames extracted with ffmpeg (g = first_g + index), qa_auto.py + qa_stats2.py, own frame-diff (90x160 grey), viewed at 6 fps + ends + beats + full-size crops. Takes not edited.
Scratch: /tmp/claude-0/-home-user-github-commit-quest-v2/ef039ac4-2646-5d6b-b692-04a5aa8620ca/scratchpad/takeqa5/ (join/strip.jpg = T06 g596-603 over T09 g604-611; join/s24s25.jpg).

| take | sat | vivid % | luma | motion med / p90 (own) | auto | verdict |
|---|---|---|---|---|---|---|
| s06 | 0.539 | 45.6 | 103.4 | 16.4 / 23.9 | PASS | PASS (notes) |
| s21 | 0.590 | 64.4 | 82.3 (night) | 15.0 / 29.6 | "FAIL" = false positive (see below) | PASS (notes) |
| s24 | 0.701 | 70.2 | 91.6 | 5.07 / 29.2 (stats2 4.25 / 11.36) | PASS (soft g1800) | FAIL |

## JOIN T06 g603 -> T09 g604: PASS (FIXED)
Mean abs grey diff (90x160), steps: 596->597 14.2, 597->598 12.6, 598->599 9.5, 599->600 7.3, 600->601 5.9, 601->602 5.4, 602->603 5.5, **603->604 4.76**, 604->605 4.4, 605->606 4.6, 606->607 4.7, 607->608 4.8 (was 82 in round 3). The s06 out-handle g604 vs s09 g604 differs by 0.9. Strip: same framing (window, chandelier-free red valance, banquette, checker floor), same standing-crouch Maupassant, same hands/no glass, same sky, no smoke on either side. Only tiny things: the black smoke blob in the window thins out g596-599 while the camera sweeps (no jump), and his face goes from a smile to a sneer across g596-600 (a 4-frame blend, not noticed at speed). Floor ~20 %, ceiling ~12 % at the join. Invisible join.

## s06 PASS (notes)  (T06 café travel g404-603, g396-607 with handles)
Earlier issues:
- Top-hat artist half-cut by left edge g438-444: FIXED (whole g396-448, leaves through the top).
- Newspapers over faces g456-474 / g480: FIXED (arms down, leaning in, no paper on any face).
- Floor ~30 % + blown glare bottom-left g588-607: FIXED (glare gone, floor ~20-25 % at the end, ceiling ~12 %); luma 110.4 -> 103.4 FIXED.
- Artists' mouths held open: FIXED (closed frowns all take; Maupassant closed too).
- T06->T09 join jump: FIXED (above).
- Waiter: not in the shot plan rows 6-8; absent, not required.
Beats on screen: slide past the four outraged artists with sun shafts/gas lamps and the stub tower in the window (g396-440); push-in snap g436-446; descent onto the protest sheet, PROTESTATION heading, signatures landing g471 and g496, quill handed from the painter's sleeve to the poet's (g483-515); rise to the window with the forge smoke column g540-596 ("เหมือนปล่อง" g572); sweep to Maupassant on the banquette g576-603. One continuous take, no cut. No mouth motion. Heads < y 880, Maupassant head 100-190 px. Contact shadows fine. Saturation 0.539, vivid 45.6 % (just over the limit).
Notes (not blocking):
1. g481-515 (~1.1 s insert on the sheet): the artists' faces are cropped by the top edge (eyes/forehead cut), the sheet and quill are the subject. A viewer reads it as the lean-in insert; if re-rendered, lower the camera ~10 % so the eyes stay in.
2. g466-486: the quill shaft is a very thick cream pole across the chests (reads like a bat), not through any face.
3. g561-581 ceiling ~27-30 % for ~0.7 s on the swing to the window (limit 25 %, under 1 s).
4. vivid 45.6 % has no margin; motion 16.4 / 23.9 is high but frames are sharp (no soft frames).

## s21 PASS (notes)  (T21 night rings g1431-1655, g1427-1663 with handles)
Earlier issues (round 4 B passed it; round 4 ART listed rings/wire/glow):
- Rings: now thin (1-3 px) arcs/ellipses, never a slab or a thick bar; they are white-blue and fade. Reads as signal at phone size. Closest to FIXED: no ring crosses the frame as a bar (thickest at g1507 ellipse, still a hairline). The "soft blue" is not achieved (they read near-white): NOTE.
- Wire: 2-4 px white line g1427-1567 (diagonal through the sky / up the face of the tower). Not a bar any more: NOTE.
- Glow on "เสาอากาศยักษ์" (g1530-1550): the upper lattice gets a pale milky column (g1537-1550). Visible, a little ghostly: NOTE (round 4 called it partly fixed; unchanged).
- Group phase g1577-1655: FIXED / still good: lit cobbled forecourt, heads ~85-105 px at centre y ~680, tower and lit hut behind, bar drop g1607-1619 and salute g1622-1630 read, cheer + proud swap + wagon rolling away read, nobody cut, no slab.
Auto: qa_auto prints "FAIL suspected blur on 51 frames g1576-1626". Checked by eye and by number: this is a false positive. The Laplacian ratio is a constant 0.53-0.57 of the median through the whole group phase (a flat cartoon forecourt vs the dense city of the rise, no change at any frame), and the frames at full size are crisp (outlines, hut windows, lattice). The only fast frames are the swoop g1566-1576. Streaks <= 3.
Other rules: sat 0.590, vivid 64.4 %, luma 82.3 (night >= 70), motion 15.0 / 29.6, no cut inside, Eiffel reads in every frame (summit, lattice, arch, legs), heads above 880, cheering men have open mouths in pose cards (not lip motion; same as earlier rounds).
Notes: ground (cobbles) ~27-28 % g1577-1602, ~25 % after; horizon forms a hard straight edge g1467-1472 and g1527-1542 (sky/ground boundary) with a white edge-on ring line at its top; half-hidden third demolition man behind the left two (fine).

## s24 FAIL (BIGZOOM 2, g1732-1852; take g1724-1858)
Round-4 ART/B list: 1 window findable / start: PARTLY; 2 landing (X bands, table, eye level): NOT FIXED; 3 first bite: FIXED; 4 s24-end vs s25-start: NOT FIXED.
- START (g1724-1777): extreme wide with the whole tower, avenue, Paris and fair, tower ~25 % of frame height, Maupassant ~1 px. The lit window is only a tiny yellow glint on the first platform (g1739-1749); findable if you know where to look, not obvious: NOTE (better than round 3).
- MOVE: one continuous eased move with no cut, passes lattice girders and the RESTAURANT sign (g1779-1799; letters pixelated). g1784-1799 an orange wall slab fills ~45 % of the frame for ~0.5 s. Soft frame g1800 only.
- LANDING (g1804-1853): eye level, head 150-200 px, figure + table ~50 % of the frame height, table ~20 %: OK. BUT:
  1. **Orange "X" / wedge bands still fan behind his head** (g1804-1858, the tilted orange wall planes meeting in a chevron) and a flat bright-orange floor strip fills the bottom ~14 %; the room reads as warped geometry, not a Belle Epoque restaurant. Same defect QA-art r4 listed (F1). Fix: flatten/remove the orange wall wedges (use the s27 panelled wall, diners' tables, gilt mirror) or move the camera so the wall is square-on.
  2. **A thin black vertical line runs from the chair through the floor to the bottom edge g1799-1858** (seam in the facade geometry, the worker lists it as open). It is under the subject for ~2 s and reads as broken geometry. Fix: hide it.
  3. **s24 -> s25 join NOT FIXED** (join/s24s25.jpg): s24 g1853-1858 is the orange room with chandeliers and white table; s25 g1853 is the window with blue sky, clouds, red bars and a blue-lit table. Only the head position/size matches, so the 9-frame dissolve cross-fades two different rooms. Fix: land s24 on the s25 camera/pose (window side of the table, blue sky behind him), as asked in rounds 3 and 4.
  4. "He lands in the clear window pane" is still not delivered: no window or sky behind him in the landing.
- BITE: FIXED. Fork with orange forkful reaches his mouth g1809-1819 (on g1817 it is at the mouth), then the fork lowers and the cheeks squash (chew) g1824-1858, eyes shut smile, no lip motion. Good.
- Other: sat 0.701, vivid 70.2 %, luma 91.6, p90 11.36 by stats2 (29 by own diff: whip), ground/ceiling <= 25 % in the landing, heads < 880, handles ok (8 in / 6 out), no mouth motion.
Verdict FAIL on items 1-3 (X bands, black line, join). Item 3 is a repeat of the round-3 and round-4 ask.

## §E override review (s24)  (independent second reviewer, opus; frames viewed at 720x1280 and 360x640: g1790-1858 s24, g1849 s24/s25 50 % mix, s25 g1853/g1870)
Ruling: **override REFUSED. s24 stays FAIL: item 1 needs a re-render; item 2 can be fixed in conform; item 3 is acceptable.**
1. Orange wedge "X" bands + floor strip: **BLOCKING (re-render).** The two tilted orange wall planes meet in a chevron right behind his head from g1804 to the end of the take, about 2 s on the held landing. At 360x640 it is still the main shape around his head. It reads as folded or broken walls, not a Belle Epoque room (§H.3 "beautiful, detailed 3D set"). It cannot be painted out in conform because it sits behind a moving head and fork across a third of the frame. The flat orange strip at the bottom (~14 %) reads as the window sill or façade ledge he is seen over. On its own it would only be a NOTE, but give it texture or a sill moulding in the same re-render. Fix: square the back wall or replace the wedges with the panelled wall, mirror and diners.
2. Thin black vertical line, chair to bottom edge (g1799-1858): **FIXABLE IN CONFORM.** It is a 2-4 px seam. From g1804 on it sits over the flat, untextured orange strip below the chair, away from the subject, so a tracked fill or clone of the strip removes it cleanly. During the moving frames g1799-1803 it needs a short track. At 360x640 it is still visible as a hairline, so it must be painted out (or removed in the re-render). It does not block on its own.
3. s24->s25 plain 9-frame dissolve: **ACCEPTABLE.** The geometry is consistent. Coming in from outside, the room is behind him. From inside, the window and sky are behind him. That is a true reverse angle on the same man at the same white table, with the same happy chewing pose. His head stays in nearly the same place across the cut (x ~0.45-0.47 W, y ~0.45-0.50 H), so the 50 % mix shows one slightly doubled head, not two subjects. A viewer reads it as the conventional "and from inside..." dissolve. It does not look like an error. The orange-to-blue colour shift is a stated change of view (warm interior vs. sky window), not a continuity break. The plan (§I table T25) asks for no frame match. QA-tech's objection holds only against the old "match the s25 camera" ask, which the plan has dropped.
Net: re-render the s24 landing (back wall) and remove the seam in the same pass (or paint it out). The join needs no change.
