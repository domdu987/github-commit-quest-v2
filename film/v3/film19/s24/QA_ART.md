# QA-art, TAKE gate: s24 (shot 24, HALL hall_table EVENING, the King times the watch) — FIX-FIRST

Frames checked (take index / g): 9/1933, 30/1954, 50/1974, 75/1999, 85/2009, 103/2027, 112/2036 (full size + 360x640).
Frames: /tmp/claude-0/-home-user-github-commit-quest-v2/a108c86f-deb9-528c-85fa-39b541349af8/scratchpad/artend/s24_*.jpg

| Criterion | Score |
|---|---|
| Set density / ornament | 8 |
| Lighting & colour | 6 |
| Composition / phone legibility | 4 |
| Acting (squint, watch compare) | 6 |
| Key moment ("every day, ten weeks") | 4 |
| Match to refs / client taste | 6 |
| **Overall** | **5.5** |

## Why FIX-FIRST
This shot carries the hardest idea of the ending: the King timed it himself, every day, for ten weeks. At phone size it does not read.
- For the first two thirds the King is a 80-110 px head at the far end of a long table (f 9-75). His gold watch and the H4 are under 20 px, so "comparing two watches" is invisible; he just looks like a grumpy man behind candelabra.
- The candle stubs (the time-lapse device) are only in frame from about f 45 to f 80 and show at most 5 of 10. On the snap word "สิบสัปดาห์" (g 2006, take index 82) the camera has already slid past them: at the key word the stubs are OUT of frame.
- The ending (f 95-112, the frames that cut to s25) is filled by a foreground candelabra whose flames clip to flat white cylinders (about 150 x 300 px of blown highlight); the King is cut at the right edge behind it. This is the "candle passing the lens" problem QA.md mentions, still present.
- Lower 30 % of f 9-50 is the dark underside of the table: dead area.

## Fixes (shot.py)
1. Camera: start closer and keep the King, both watches and the stub row in one frame for the whole shot. Move `CAM_LOC0` to about (-0.6, 0.6, 2.6) and `CAM_LOOK0` to about (0.2, 4.25, 2.3) (looking at `KING_M`), `push=0.07`, `slide_px=-40`, `arc_deg_s=6`. Target: King head 160-230 px wide, centre y 500-620 throughout.
2. Snap: aim the snap at the stub row plus the King, not past them: `shift=(0.6, -0.2)` (a small downward pan) instead of (2.00, 0.30), `k=1.25`. At g 2006 all ten stubs and the King's face must be in frame together.
3. Stubs: keep `stubs_at(g)` but stage the row across the near table edge in frame lower third (y 820-1000 at f 82), left to right, so the count visibly grows; land 10 by g 2006 (currently at G1-1 = 2027): `stubs_at = clamp((g-G0)/(G_SNAP-G0))*10`. The time-lapse should peak on "สิบสัปดาห์", not after it.
4. Candelabra: keep it out of the last 20 frames (or behind the King), or drop its flame emission so nothing clips; the last frame before the cut must be the King, not a blown candle. If you want a FG prop, use the cold stub row, not a lit candelabra.
5. Pose: make the watches readable: raise both hands to face height (hand y 0.75-0.95 instead of 0.45-0.87), keep the H4 (silver) and the gold watch about 0.5 D apart beside the eyes, and scale both watch props about 1.5x. Keep the squint.

## Continuity
Chair present (`set_kings_chair(True)`, red chair right of the King), King stands beside it, same as s26 (KING_M there is beside the chair). Blue coat consistent. Window dusk blue, warm interior: EVENING consistent with s25/s26. The H4 is in the King's left hand here; it disappears in s26.

---
# Re-review after the fix round (TAKE gate, key takes): PASS, 7.0

Frames checked (take index / g): 9/1933, 35/1959, 60/1984, 82/2006 (snap word), 95/2019, 112/2036 at full size and 360x640, plus contact.jpg and phone_sheet.jpg.
Frames: /tmp/claude-0/-home-user-github-commit-quest-v2/a108c86f-deb9-528c-85fa-39b541349af8/scratchpad/artkey/s24_*.png

| Criterion | Before | Now |
|---|---|---|
| Set density / ornament | 8 | 8 |
| Lighting & colour | 6 | 7 |
| Composition / phone legibility | 4 | 6.5 |
| Acting (squint, watch compare) | 6 | 7 |
| Key moment ("every day, ten weeks") | 4 | 6.5 |
| Match to refs / client taste | 6 | 7 |
| **Overall** | **5.5** | **7.0** |

## Earlier fixes
1. Camera closer, King 160-230 px throughout: **PARTLY FIXED / OPEN (minor).** The King is 117-217 px, but the first second is still about 120 px at the far end of the table.
2. Snap shows the stubs and the King together at g 2006: **FIXED.** Both are in frame on the word. Only about 5 of the 10 stubs are in frame, though; the rest are cut off at the right edge.
3. Stubs grow left to right in the lower third and reach 10 by the snap: **FIXED.** The row grows visibly through f 35-82, at y 830-1030.
4. No blown candelabra in the last frames; the King ends the shot: **FIXED.** The flames are small and not clipped, and the King is the last subject.
5. Watches at face height, 1.5x: **FIXED** for scale. Two white dials read beside his chest at phone size and the squint reads. But the table orrery (h19_hall orrery at (0.0, 3.85)) now sits right in front of the watches and his chest, so the brass rings tangle with the dials.

## New / remaining notes (polish if re-rendering anyway; not blocking)
- Hide the orrery for this shot (in shot.py, the same way the stubs are moved: find the orrery objects and set hide_render, or move them +1.5 D in x). The two dials then read alone.
- Snap shift (1.30, -0.20) to about (0.9, -0.25), so all ten stubs and the King's face are in frame at g 2006. The King's right shoulder is cut at the frame edge now.
- The brass telescope eyepiece hangs as an out-of-context lump top-left in every frame. Move CAM_LOC0 x from -1.60 to about -1.2, or accept it as foreground depth.
- The bare wooden block at the front centre (f 35-95) is a dead shape. It could take the gold pocket watch's case or be cropped by tilting down 0.1.
- Frame-diff 3.95 / 9.96 is just under target. A slightly larger arc (12) would cover it.

---
## Round 3 (TAKE gate, key takes, regression check after polish re-render): PASS, 7.0

Frames checked (take index / g): 9/1933, 35/1959, 60/1984, 82/2006, 95/2019, 112/2036 at full size and 360x640, plus contact.jpg and phone_sheet.jpg.
Frames: /tmp/claude-0/-home-user-github-commit-quest-v2/a108c86f-deb9-528c-85fa-39b541349af8/scratchpad/artkey6/s24_*.png

The camera and King mark changed (KING_M x 0.85, CAM_LOC0 (-0.50, 2.40, 2.55), snap shift (2.40, -0.25)). There are no regressions that block.
- **The R2 passes hold.** Stubs grow left to right in the lower third. At g 2006 the King, both watches and the whole stub row (about 10) are in one frame. No blown candelabra at the end. The King ends the shot.
- **Improved.** The orrery no longer tangles with the watches, and the two dials read clean beside his chest. After the snap (f 95-112) the King is a big, clear subject (head about 260 px) with both watches and the squint, which is the strongest image of the shot. The telescope lump top-left is gone.
- **New, minor.** At the snap word the lit candelabra stands between the lens and the King, with its flames at his shoulder height (bright but not clipped). After the snap, the right 40 % of the frame is a plain wooden lectern block (dead shape). If re-rendering anyway, cut the snap shift from 2.40 to about 1.9 so the globe and lectern sit at the edge.
- The first second still has the King small (about 120 px) at the far end. This is unchanged and accepted.

| | R2 | R3 |
|---|---|---|
| **Overall** | **7.0** | **7.0** |

## Round 8 (director QA-art, MERGED take 24+25+26, the ENDING): FIX, 6.9

Take: /tmp/s24.mkv (take.mkv.partaa + partab), first_g 1924, g 1924-2159, frame index = g - 1924. I viewed it at 3 fps, every frame of both whips (g 2018-2033 and g 2084-2098), the punch-in (g 2066-2094), and the bag and ending (g 2094-2159), at full size and at 360x640.
Frames: /tmp/qa19_r8art/s24/all_NNN.png. Sheets: /tmp/qa19_r8art/s24_3fps.jpg, s24_whips.jpg, s24_beg_phone.jpg, s24_end_phone.jpg, s24_bag.jpg, s24_astropop.jpg.

| Beat | Status |
|---|---|
| King compares watches (g 1933-2021) | Good, and the strongest part of the take. The King squints at the gold pocket watch and the H4 at chest height under the arched night window. The candle-stub row grows across the green table, and at the snap on "สิบสัปดาห์" the King, both dials and the stubs are in one frame. The candelabra in front of him is fine. |
| Whip 1 (g 2022-2029) | Good. It is a real whip with heavy directional blur and lands clean on the mocker. It reads as the same room (red walls, window, telescope). |
| Mocker + "เป๊ะ" | Reads. The big wig, the spectacles pushed up, the O-mouth, the wide eyes, the sweat drop and the tremble all show. The punch-in on "เป๊ะ" (g 2069-2082) is modest (head about 1.3x), the face stays under 35 %, and the hold is about 1 s, which is legal punctuation. His shoes are on the carpet, so he is grounded. |
| Whip 2 (g 2086-2093) | Good blur. It lands on Harrison at the table with the King behind him and the telescope overhead. |
| **Mocker pop at the landing (BLOCKER)** | **g 2093-2096: the mocker's card is still on screen at the left edge, cut in half (wig, face and coat), sharp from g 2094. At g 2097 it vanishes and the background appears behind it.** This breaks "nobody cut in half" and is a visible pop right after the whip. |
| Bag lands (g 2105-2107) | Reads: it drops from the top, lands with a squash and spills gold coins. It is fat and gold, and it reads as the prize at phone size. |
| Harrison grins / King nods | **Weak.** Harrison goes from a neutral face to a small closed-mouth smile (g ~2126) and reaches one arm to the bag. The King's nod happens at about 60 px head width in the background, closed-eye and content, and barely registers on a phone. It is the film's payoff, but the emotion is "mildly pleased". |
| Composition of the ending | From g 2094 to about 2145, the lower ~40 % of the frame is the dark front panel of the table plus dark carpet: a dead slab (it sits in the caption band, but it is still half the frame for 1.7 s). The final push (g 2145-2159) fixes it: Harrison, the bag and the King in the frame, moving. The telescope tube runs just over Harrison's head at the end (a near-tangent, not through his face). |

**Does the irony read?** Yes, mostly. The chain King timing the watch -> whip -> the jaw-dropped mocker on "ตามที่นักดาราศาสตร์ท้าไว้เป๊ะ" -> whip back to the reward reads as cause and shock. Keeping the telescope in the table frame ties him to the room. It would land harder if the mocker were still visible, stunned, when the bag lands.

**Satisfying and funny?** Satisfying: yes (the gold bag and the King's approval). Funny: only mildly. The ending has no comic button; Harrison's reaction is too small for the last 2 s of the film.

| Criterion | Score |
|---|---|
| Set (hall, window, orrery, telescope, books) | 8.5 |
| Light & colour (candles, cool night window, red/green/blue; sat 0.66, brightness 64.6) | 7.5 |
| Composition / phone | 6 |
| Acting | 6.5 |
| Key moment (dare came true + reward) | 7 |
| Match to refs (R5 travel/whips, R4 candle interior) | 7.5 |
| **Overall** | **6.9 - FIX (re-render g 2088-2159 only)** |

Fixes:
1. **Mocker card at the whip-2 landing (blocker).** Recommended, because it also sharpens the irony: keep the mocker on screen for the ending. Place him FULLY in frame at the left of the table, behind Harrison's shoulder or by the telescope, at about 0.6-0.7 of Harrison's size. Keep the jaw-drop and tremble going, and on the bag landing (g 2107) give him a second shock beat (the wig flips up or his spectacles drop). Minimum fix: hide his card from g 2090, while the whip blur is heaviest, so no half-card is ever on a sharp frame.
2. **A bigger payoff on Harrison:** from g 2110, an open-mouth grin (teeth or "D" mouth), eyes squeezed happy, both arms up or hugging the bag, plus a squash-hop on the landing. That makes the last word "ไอ้ช่างไม้" the button.
3. **Make the King's nod readable:** a bigger nod (2 nods, +-12 deg) or bring his mark 0.3 D forward, so his head is at least 100 px wide during g 2113-2157.
4. **Remove the dead table front:** tilt the ending camera down 0.1-0.15 D or raise it, so the green tabletop with the bag and coins fills the lower third instead of the dark panel during g 2094-2145.
5. (Polish) Lift the telescope tube 0.1 D so it clears the top of Harrison's head in the last 15 frames.
Keep the King segment, both whips and the punch-in on "เป๊ะ" as they are.
