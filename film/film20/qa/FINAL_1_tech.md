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
