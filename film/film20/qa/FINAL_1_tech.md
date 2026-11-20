# FINAL gate 1 (QA-tech), film 20, film20_rc2.mp4 (68.2 s, 720x1280@30, 2046 frames)
Verdict: **PASS with 1 flag** (BIGZOOM 2 is shorter than the 3-6 s rule, see 4).

## 1. qa_auto (--cuts 80,1093,1431,1911,1968 --first_g 0)
- QA_AUTO PASS. 2046 frames, 0 frozen, 0 black (min frame luma 49), 0 blank, magenta 0.0 %.
- Blur: 15 "soft" frames in 2 runs (g176-182 = T02->T03 dissolve ghosting; g252-259 = BIGZOOM 1 close scaffold push). g254 checked by eye: sharp textured lattice, not blur. OK.
- Cuts: all 5 planned hard cuts present as single-frame spikes (frame-diff 41-74) at g80, 1093, 1431, 1912, 1968. Note: take meta says shot 26 begins g1912, the call list says 1911: 1-frame naming difference, the cut is a clean single frame. qa_auto's own note "no visible change within +-2" for the planned list is a false alarm (its test is on a different diff scale; my direct frame diff shows the spikes).
- 4 more large diffs are in-take camera events, not cuts: g910/912 (planned snap crane-ups of shot 14), g1391 (push through the hut window, T18/T21), g1795 (push through the restaurant frame, BIGZOOM 2). Viewed by eye: continuous geometry, no flash.

## 2. qa_stats / qa_stats2
| metric | film 20 | rule | |
|---|---|---|---|
| saturation | 0.565 | >= 0.50 | PASS |
| vivid % (sat>=0.5) | 57.4 | >= 45 | PASS |
| luma | 95.4 (night beat 43-52 s: 91.6; 40-50 s 87.9) | 85-110 | PASS |
| in-shot motion median | 7.95 | >= 4 | PASS |
| p90 | 24.25 | >= 12 | PASS |
| hard cuts | 5 planned + 4 in-take snaps/pass-throughs = 9 max | <= 12, target 4-10 | PASS |
(qa_stats' own cut detector reports only 5 "shots" because dissolves and travel takes hide the joins; the real hard-cut count is from the frame-diff list above.)

## 3. Film 2 vs film 20 (same analyser, 90x160 grey, 30 fps)
| | film 2 sky_poker_v3 | film 20 rc2 | verdict |
|---|---|---|---|
| duration | 65.6 s | 68.2 s | |
| shot length | 29 detected shots, mean 2.26 s, median 1.37 s | 15 takes, mean 4.5 s (27 beat shots, mean 2.5 s inside travel takes) | longer by design (QA §I travel instead of cutting; camera never still) |
| hard cuts | ~28 (many <1 s) | 5 (+4 in-take snaps) | better (§I limit 12) |
| motion median / p90 | 4.75 / 16.9 (in-shot 4.66 / 15.5) | 7.95 / 24.25 (in-shot 7.92 / 23.9) | better (+67 % / +43 %) |
| moving-camera frames (diff > 2) | 78 % | 96.8 % (diff > 4: 86 % vs 59 %) | better |
| near-still frames (diff < 1) | 10.2 % | 1.0 % | better |
| close-ups | not auto-measurable; film 2 plan has ~4-5 close inserts | 3 (punch-in on Eiffel s11, push-in "สักครั้ง" s10, jeer push s17) | within §I.6 (<= 3) |
| saturation / vivid % / luma | 0.490 / 49.4 / 94.0 | 0.565 / 57.4 / 95.4 | better |
Nothing in film 20 is worse than film 2 by > 10 % (shot length is longer, which is the §I intent; the camera-motion numbers cover it).

## 4. BIGZOOM (frames viewed every 4-8 frames)
- **BIGZOOM 1, 5.93-10.60 s (g178-317; T03 s03)**: g178-184 dissolve in; g186-196 extreme wide over Paris roofs/Seine/site, Eiffel invisible or a dot (< 2 %); g204 ~6 %; g225 ~12 %; g250 ~17 %; g280 ~29 %; g298-312 ~36-38 % medium, he points up (the "วิศวกรไอเฟล" beat). < 5 % -> 35 % in about 3.1 s (g~200 -> g~298); whole move from start about 3.9 s. **PASS** (passes close to girders, tents, barrels on the way).
- **BIGZOOM 2, 57.75-61.77 s (g1732-1852; T24 s24)**: g1734 dissolve in; g1750-1776 whole finished tower, Paris, Maupassant not findable (< 3 %); g1782-1788 push through the lattice, restaurant sign appears, he is ~5 %; g1795 ~9 %; g1806-1812 ~35-40 % medium, first bite at g1812 (60.4 s, matches 60.48). 5 % -> 35 % in only about 0.7 s; whole move (clean start g1745 to landing g1812) is about 2.2-2.7 s, then a 1.4 s hold. **FLAG: shorter than the 3-6 s rule**, and the "findable < 5 % in the window" start is not shown (tower only). Not a technical defect; decision for the director whether the rule or the shot wins. The move itself is continuous (one cut-free push), eased, with foreground lattice and sign.
- Angle types used (>= 4 required, 8 found): high bird's-eye (BIGZOOM 1 and 2 openings, tower-from-above), low hero angle (s01 tower_low, s09 cafe_low), over-the-shoulder (s08 window, s26 resto view), through a foreground frame (hut window, restaurant frame/girders in BIGZOOM 2), crane up/down (s03 leg crane, s14 three crane-ups, s21 summit rise/swoop), side tracking/slide (s06 cafe slide, s12 girder stack), whip tilt (s19 down antenna wire), crash pull-out (s27). PASS.

## 5. Joins (frame diff and luma, +-3 frames)
- Dissolves g178, 404, 753, 996, 1221, 1656, 1732, 1853: diffs smooth (4-15), luma monotone steps of 1-3, no black, no flash, no dup/missing frame. 604 match: no spike (diff 4.6-6.2). PASS.
- Hard cuts g80 (luma 97->89), g1093 (84->108), g1431 (89->74), g1912, g1968 (97->68): single-frame cuts, no black/flash frames. Frame count 2046 = expected, so no dropped frames.
- Odd frame: g1430 (last frame before the night cut) is a darker warm frame (luma 71 vs 89 around it, spark-gap lamp pulse inside the hut), 1 frame, matches the "spark gap flashes" beat; acceptable, mentioned for the director.
- Luma by 10 s window: 98, 101, 96, 95, 96, 88, 93: no dark outlier; darkest frame 49 (night, g1393 = hut interior), not black.

## §E review: BIGZOOM 2 (FINAL gate)
Independent second reviewer (Opus), measured on film20_rc2 assembled frames (f index = g), full 720x1280, frame-diff on 90x160 grey. Rule QA_TEAM §H.1: one continuous move, start EXTREME WIDE with the character < 5 % of frame height **but findable**, end on a medium of the **character** at 35-60 %, lasting 3-6 s with ease in/out.

**1. BIGZOOM 2 measurements (s24, g1732-1852).** Subject A = Maupassant (visible figure, top of hair to tabletop; in brackets the implied seated figure, hair to seat, ~1.3x, since the table hides his lap). Subject B = the restaurant window unit (sign top to sill).

| g | t (s) | Maupassant | window unit | what is seen |
|---|---|---|---|---|
| 1732 | 57.73 | not visible | ~0.6 % | dissolve from s23 (crowd overlay), tower small |
| 1750 | 58.33 | not visible (pane renders as a flat yellow lit square) | ~1.0 % | whole tower + Paris, slow push |
| 1770 | 59.00 | not visible (yellow square) | ~2.2 % | tower fills frame, first floor centred |
| 1785 | 59.50 | ~6 % (~8 %) | ~53 % | through the lattice, RESTAURANT sign, he is in the opening |
| 1795 | 59.83 | ~11 % (~14 %) | > 100 % (sign cropped) | crossing the window frame |
| 1805 | 60.17 | ~20 % (~26 %) | inside | inside the restaurant |
| 1815 | 60.50 | ~26 % (~34 %) | inside | bite starts |
| 1830 | 61.00 | ~29 % (~38 %) | inside | landed, slow drift |
(Finer: window 3.2 % at g1778, 7.3 % at g1780, 20 % at g1782. Maupassant first readable as a figure ~g1776 at < 1 %, ~3 % at g1782.)

- Frame diff shows the move's shape: g1736-1775 slow drift (diff 4-6/frame), then **g1776-1800 a whoosh (diff 20-44/frame, peak 42-44 at g1783 and g1795)**, settle g1800-1818 (19 -> 5), hold/drift g1818-1852 (2.5-3.7). It is continuous (smooth diff envelope, no single-frame spike), so it is not a cut, but about 80 % of the zoom happens in 0.8 s.
- Window unit: last < 5 % g1779, first >= 35 % ~g1784: **0.17 s**.
- Maupassant: last < 5 % g1784; >= 35 % visible figure **never** (peaks ~29 %); implied seated figure >= 35 % ~g1818: **~1.1 s**. Whole camera move from the clean wide (g1745) to landing (g1818): **2.4 s**.
- Start condition: at g1736-1772 he is not findable at all; the window pane renders as a flat yellow lit square (no interior). The "< 5 % but findable" start only exists for about 8 frames (g1776-1783) in the middle of the whoosh.
- The s24 take reviewer's "3.2 s" counts camera time from g1724 (pre-dissolve handle) to g1819, not subject < 5 % -> 35 %. The FINAL tech reviewer's numbers (0.7 s, 2.2-2.7 s overall, he not findable at the start) are confirmed; my 5 % -> landing is even a little longer (1.1 s) only because I put the landing at the 35 % implied-figure point.
- **Ruling: BIGZOOM 2 FAILS §H.1** (duration 3-6 s not met by any reasonable subject definition; character not findable at the wide start; visible-figure landing 29 %, under the 35 % floor). It is a good continuous, eased push with foreground lattice and sign, but it is a whoosh-in, not a big zoom.

**2. Other candidate moves in the film (contact sheet every 24 f, then every 6 f on candidates).**
- BIGZOOM 1 s03 g178-317: not re-measured in detail; the frames I saw agree with the PASS above. It is the only qualifying move.
- Night antenna take g1302-1430 (s19-s20), the best other candidate: tower wide g1336 -> tilt down the wire -> hut g1366 -> through the hut window g1391 -> soldier at the key g1396. The soldier is hidden inside the hut until g1391 (never findable at < 5 %), lands at ~24 % of frame height, move ~2 s. **Does not qualify.**
- Whip pull-out g1431-1560 (s21) and crash pull-out g1968-2045 (s27): reverse moves (character -> wide), §H needs wide -> character. **Do not qualify.**
- Café slide (s06), construction count snaps (s12-s14), fair (s15/s23), dusk/AHA pushes (s18/s22): the characters are already 15-40 % at the start, and the moves are 8-10 %/s slides or snaps. **Do not qualify.**

**3. Rule: the film does NOT satisfy §H ">= 2 BIGZOOMs" (1 of 2). FINAL gate BLOCKED on §H until s24 is fixed.**

Cheapest fix: re-render s24 only (take g1724-1858 with handles; splice g1732-1852, same dissolves and cut, audio unchanged). Re-timing the existing frames cannot work: the zoom is spread over about 25 rendered frames at 20-44 diff/frame, and slowing it 4x would need invented viewpoints (optical-flow interpolation through the lattice will ghost). A 2D crop-in on the wide frames would need about 10x enlargement at 720p.
Changes for the re-render (same set, same path geometry, same lighting):
1. **Re-time the camera along its existing path with log-distance (constant perceived zoom rate) easing** instead of the current back-loaded curve: the distance to the window table falls exponentially from g1736 to g1828 with a short ease-in/out at each end. Target: window unit < 5 % until ~g1745, Maupassant < 5 % until ~g1790 and then rising steadily, landing at >= 35 % at ~g1826-1828. That gives **wide -> landing about 3.0-3.1 s**, then a 0.8 s slow drift to the cut at g1852. Keep the pass through the lattice and the RESTAURANT sign, now taking about 1 s instead of 0.3 s.
2. **Move the end pose closer by about 1.25x** (or narrow the FOV about 20 %) so his visible figure (hair to tabletop) is 36-40 % at landing, with the table edge and the chair top still in the bottom of the frame.
3. **Make him findable at the start:** turn the restaurant pane from the flat yellow emissive square into clear glass (or an open pane), so the lit interior and his white face read as a dot in the first-floor window from g1745. Optionally use a slightly warmer practical light behind him.
4. **Move the first-bite keyframe from ~g1812 to ~g1824-1828** (60.8-60.9 s, still inside "กินข้าวบนหอ" which starts at 60.48). Keep his mouth closed until then.
Then redo the s24 take QA (measure g1736-1852 every 4 frames against these numbers) and re-run the FINAL item 4 and joins at g1732 and g1853.
