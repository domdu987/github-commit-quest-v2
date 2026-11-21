# QA-tech FINAL gate, film 19 v3 (film-13 rules: gate 3 + §D.1 script checks): PASS (6 non-blocking notes)

Film: release19/harrison_v3.mp4 (720x1280, 30 fps, 2160 frames, 72.0 s). Inputs used: /tmp/claude-0/final_v3/f2 (144 frames at 2 fps, viewed as six sheets with the y 880 caption line drawn), plus my own every-frame analysis (/tmp/qa19_final: 360x640 grey and 90x160 grey of all 2160 frames) and single-frame extractions of the soft runs and cuts.

## 1. qa_auto (run myself)
`python3 qa_auto.py release19/harrison_v3.mp4 --cuts 57,262,466,545,661,773,1280,1581,1933 --first_g 0` -> FAIL only on "suspected blur on 222 frames" plus the note "planned cuts with no visible change within +-2: g262, 466, 545, 661, 1280, 1933"; magenta 0.0 %; no black, blank, magenta, frozen run or unplanned pop flagged. My own pass agrees: no black frame (minimum frame luma 66.1 at g2041, maximum 137.6), no frozen run (no 4-frame run with diff < 0.15), Laplacian median 549.

## 2. Soft runs (219 frames under 0.6x the median in 15 runs): all motion, dissolve or content; no real blur or DOF
Viewed by eye at full size or in crops:
| run (g) | frames | lowest lap / median | verdict |
| 57-80 | 24 | 0.32 | s02 extreme-wide sea, flat water and sky, ship/rigging crisp: false positive (waived, re-confirmed) |
| 132-141 | 10 | 0.56 | s02 descent past the sail, flat grey-lilac sail face: content |
| 839-849 | 11 | 0.36 | s10 whip (diff 24-44): planned motion blur |
| 859-864, 937-940 | 6 + 4 | 0.51, 0.53 | dissolves (s10->s11, s11->s12): blend of two frames |
| 967-988 | 21 | 0.57-0.59 | s12 night workshop, dark soft-lit set and the g960-972 whip: dark content |
| 1321-1373 | 53 | 0.42 | s17 aerial of the ship on open sea: frames g1300, 1321, 1335, 1345, 1355, 1365, 1372, 1380 viewed; the ship, rigging, wake foam and cloud edges are sharp, the soft area is flat smooth water and the horizon haze; no blur, no DOF, captions sharp: content |
| 1469-1470 | 2 | 0.46 | s19 wide hold, flat sky/sea (waived mechanism) |
| 1821-1827 | 7 | 0.43 | s22 whip: planned |
| 1854-1909 | 56 | 0.38 | s22->s23 dissolve (g1848-1864) then the dark evening door; g1860, 1880, 1895, 1905 viewed: Harrison, door, panelling and wall are sharp, the low variance is the dark, flat wall and floor: content |
| 2023-2029, 2087-2093 | 7 + 7 | 0.24, 0.21 | s24 whips 1 and 2 (diff 25-34): planned |
| 2038-2041, 2071-2077 | 4 + 7 | 0.58, 0.57 | s24 snaps (diff 5-10): g2035, 2038, 2040, 2074 viewed, the astronomer's face, wig, coat and shelves are sharp; flat red wall and large face lower the variance: content |
No defocus or DOF anywhere in the film; the longest true blur is the whips (7-11 frames, planned and accepted since rounds 5/8).

## 3. Hard cuts (frame-diff of the planned frame against its neighbours; local median 4.6-9.6)
| cut g | diff at g (neighbours before / after) | max-diff frame | luma |
| 57 | 62.8 (8.0 / 2.3) | 57 (offset 0) | 100.0 -> 84.8 |
| 262 | 56.3 (6.0 / 16.3) | 262 (0) | 111.3 -> 69.0 |
| 466 | 52.2 (15.1 / 7.8) | 466 (0) | 94.9 -> 78.3 |
| 545 | 47.8 (0.8 / 6.0) | 545 (0) | 81.5 -> 78.4 |
| 661 | 49.8 (8.1 / 6.9) | 661 (0) | 92.4 -> 79.4 |
| 773 | 65.7 (5.2 / 6.4) | 773 (0) | 82.9 -> 101.0 |
| 1280 | 50.3 (3.3 / 5.5) | 1280 (0) | 117.3 -> 106.2 |
| 1581 | 71.0 (5.8 / 6.3) | 1581 (0) | 117.4 -> 75.5 |
| 1933 | 46.1 (5.6 / 3.3) | 1933 (0) | 67.5 -> 101.8 |
All nine cuts fall exactly on the planned frame (offset 0, spike 8-10x the local median). The six cuts qa_auto reports as "no visible change" (g262, 466, 545, 661, 1280, 1933) are only below its absolute threshold (46-56 on my scale, a 14-pixel-scale artefact of its 12-or-8x-median rule on busy neighbours); they are real cuts on the right frame, including the three hall-to-hall cuts (466 s07 hall_window, 545 s08 hall_low, 661 s09 closer): 47.8-52.2, clean, with no dissolve-like ramp before or after. The take handle frames sit under the cuts, so there is no one-frame flash of the wrong shot.

## 4. Film-13 checklist across the film (2 fps + every cut +-3)
- Heads above y 880: yes in all 144 sheet frames (cyan line) and the cuts; the lowest heads are Harrison's at the hook (face about y 330-500) and the big close-ups (astronomer, s08 g~1310-1410 at 22-24 s, face to about y 800, chin above the line); captions sit on the 880 band below faces. PASS.
- Nothing floating: contact shadows on every standing character in the 2 fps frames (workshop, ship deck, hall, beach); the three sailors on the beach stand on the crate/sand with shadows (the float fix holds); the ceiling-hung lantern and chandelier rings hang from beams by design. PASS.
- Nobody cut in half: no character cut by a frame edge except the planned whips/dissolves and, as notes, the captain's hand at the left edge in s02 g190-199 (hidden under the s04 dissolve) and the astronomer's wig / wall edge in s24 (g2009-2027, face intact). PASS.
- Pops: none unplanned. Frame-diff spikes outside cuts are only the planned snaps and whips (g44-45 hook snap 18, g330-338 s05 shake 21-35, g640-643 s08 quote snap 19-27, g748-755 s09 snap, g839-846 s10 whip, g918-923 s11 snap, g996 s12 swap, g1172 s15 snap, g1375-1380 dissolve into s17/s18 (the 11-frame dissolve out of the ship deck: 20-26 in the first six frames of the window; see note 2), g1633-1638 s20 snap, g1706 s21 snap, g1822-1823 s22 whip, g1903-1908 s23 snap, g2007-2011 and g2024-2029 s24, g2076-2092 s24 whips, g2148-2153 s24 snap). No spike lacks a script event. PASS.
- Frozen runs: none (min frame-diff over the film 0.8, the s07 handle); no black frames (min luma 66.1).
- Thai text: captions render correctly in all 144 frames (no tofu or black blobs; sampled hook, s04 ship, hall, s17 sea, s23 door, s24 table), white with dark outline, inside the 880 band, text matches the narration beats; none clipped by the frame edges. PASS.
- Mouths: only the quoted lines move (astronomer "นาฬิกาเนี่ยนะ!" and "จับเวลาเอง", "ฟลุ๊ค"); other faces carry expression mouths; the held shock "O" mouths (captain s02, astronomer s24) are expression.
- Stillness: someone moves in every shot; the long static-looking ones (s17 ship at sea) are camera moves over a moving wake.
- Colour: saturation 0.582 (team), luma 91.2 (team; my grey mean per second 68-127), no black/magenta.

## 5. Continuity across dissolves (luma start / mid / end, largest per-frame step inside the window)
191 (s02->s04): 96.6 / 105.0 / 114.1, 2.1 | 356 (s05->s06): 86.7 / 85.2 / 79.0, 1.4 | 862 (s10->s11): 101.6 / 101.4 / 100.1, 0.6 | 938 (s11->s12): 108.7 / 97.7 / 83.8, 3.3 | 1016 (s12->s14): 88.0 / 94.0 / 103.3, 2.3 | 1096 (s14->s15): 103.6 / 106.1 / 105.7, 0.6 | 1384 (s17->s18): 131.8 / 110.6 / 90.3, 6.3 | 1468 (s18->s19): 103.6 / 105.5 / 107.4, 0.6 | 1665 (s20->s21 window; hall to beach): 85.0 / 102.8 / 120.8, 4.2 | 1756 (s21->s22; beach to hall): 112.1 / 94.8 / 76.4, 5.5 | 1856 (s22->s23): 87.9 / 87.7 / 87.1, 1.0.
All dissolves are smooth ramps (no frame with a step above 6.3, none with a flash); places and times of day change as planned. The 1665 dissolve is s20->s21 (hall to beach) and the s21->s22 at 1756 returns to the hall.

## 6. Brightness jumps after the grade (hard cuts)
The big steps are all planned place or time changes: g262 (-42, bright storm-dusk deck cut from a bright aerial to a dark dusk ship), g1581 (-42, bright beach to the red hall), g1933 (+34, the dark evening door s23 to the brighter evening hall s24; per-second grey luma 68 -> 102), g773 (+18), g466 (-17), g57 (-15, workshop to the wide sea), g661 (-13), g1280 (-11). The hall cuts s07/s08/s09 (466, 545, 661) stay within 3-17 and the dark s08/s09 close-ups sit at luma 67-79 while the next hall shot (s10, g773) steps to 101; this +18 is the same hall at a brighter exposure (flagged in the s10 re-check); the dark-to-bright 1933 step crosses a cut inside the same evening hall.

## Numbered issues (all non-blocking)
1. g1933 (s23 -> s24 hard cut): luma +34 (dark evening door to the brighter evening hall table); the grade could lift s23 by about 10 or lower s24 by about 8 so the evening reads continuous.
2. g773 (s09 -> s10 hard cut, same hall): luma +18 (79 -> 101); the previous s10 re-check already flagged it; optional grade match.
3. g1375-1380: the s17 -> s18 dissolve window carries diff 20-26 in its first frames (the aerial ship cutting to the new view while the wake animates): reads as a fast dissolve; fine, but the brightest section of the film (luma 118-138 at 39-42 s, the noon deck and aerial sea) is above the 85-110 band; note only.
4. s24 (g2009-2027): the King's wig touches the left frame edge (face intact), and a candle edge shows at the left; unchanged since s24 round 4.
5. s02 g190-199: the captain's outstretched glove grazes the left frame edge (under the dissolve into s04): accepted earlier.
6. Whip blurs are 7-11 frames long (s10 g839-849, s22 g1821-1827, s24 g2023-2029 and g2087-2093) versus the film-13 text's "1-3 frames of streak": the same accepted whips as before.

Verdict: PASS under film-13 rules. No blocking issue; the six notes above are for the conform grade or the director.
