# QA-art R4: film 17 take s10 (THE REVEAL, g1336-1520, commit 72847cc, render17/team9): FIX-FIRST (1 post-only fix, 1 small finger fix)

Reviewer: QA-art. This is the TAKE gate for a key shot, and the client has delegated approval to QA.
Scope, as promised in R3: the finger insert g1406-1419, the card shot g1474-1520, and the QA_AUTO blur list on card frames. I also took a quick look at the box switch-off g1420-1441. Every other item was accepted in R3 and I have not reopened it.

How I reviewed:
- I read phone_sheet.jpg first.
- I extracted all 185 frames from take.mkv (built from the two parts, which are byte-identical). All 66 f6/ frames match the take exactly.
- I extracted the R3 take (e6fe1c2) from git for A/B comparison.
- I built 360x640 strips (finger, boxes, card, finger against ear) and full-res crops.
- I measured these myself: Laplacian variance, mean luma, card bbox, card paper RGB, caliper-jaw x per frame, and phase-correlation camera shift.
- Frames outside the re-rendered ranges differ from R3 only by encoder noise (mean |d| < 0.6). The exception is g1420-21, which really did change (mean |d| 9, from the new 72 W fill key). The team's QA.md says those two frames are unchanged. They still read fine.

## Claims against the frames
| # | Team claim | What the frames show | |
|---|---|---|---|
| 1 | Finger: calipers + hand span ~83 % of the width (x 0-600) | **False.** At g1416 the beam runs x ~130-420, which is **~290 px (40 %)**. Bertillon's hand/forearm on the beam is **not visible** in any frame. | - |
| 1b | Finger 25-30 px wide, between closing jaws | The finger is wider than claimed, **~42-45 px** of pink fill (x 338-381), which helps. It does sit between the jaws. But the jaws **never close**. The left jaw's inner edge reaches x ~306 at g1416, then opens 2 px by g1419. That leaves a gap of ~25-30 px on the left and ~15-20 px on the right. | WEAK |
| 1c | Head large at left | True. Bertillon's half-face covers x 0-240 and doesn't hurt. | OK |
| 2 | Card g1510 496 px (69 %), centred | **True.** I measure the bright area at x 105-612 = **~507 px (70 %)**, centre x ~358, rows 490-722. That meets the size target. | PASS |
| 2b | Push-in only, sharp for the last 15 frames | **True.** There is no pull-out. Camera shift is <= 1 px/frame from g1500. Laplacian is flat at 253-259 over g1505-1520. | PASS |
| 2c | Hero box rim not visible; card stands in front of it | True. **I waive the rim/gap requirement.** At g1486-1502 the card plainly rises out of the open drawer, and its bottom tucks behind the drawer front, so the viewer sees where it came from. | OK |
| 2d | Warm pool, surroundings -18 % | **Surroundings: roughly true** (shot mean luma 80 against 93 in R3, bottom third 44). **Warm pool: false, it is cooler.** Card paper at g1510 is RGB **(210, 215, 221)**, blue above red. In R3 it was (227, 221, 212). Cause: `post.py` builds the tint as `[1+0.06p, 1, 1-0.05p]` and applies it to a cv2 **BGR** image. That boosts **blue** by 6 % and cuts **red** by 5 % in the pool, the opposite of the comment. On top of that, the -17 % card exposure has dropped the paper from ~221 to ~212 luma. At phone size the payoff card now reads as cold grey-white. | **FAIL** |
| 3 | QA_AUTO blur on g1483-90, g1514-17 = low texture, not blur | **True.** Full-frame Laplacian is 177-199 at g1483-88 and 250-256 at g1490 and g1514-17 (g1514-17 is identical to g1510). The whip frames are at 7-15. These flags are false positives. **I accept them**, so log a waiver in QA_AUTO. | PASS |
| 4 | Box switch-off: dark boxes near-black | True. At 360x640, 6 lit boxes turn to 1 at g1422/26/30/34/38, and the count reads even harder than in R3. The black boxes are flat and lose their form, but the yellow tabs keep them reading as boxes. The hero box is still lit at g1441. | PASS |

## What a first-time phone viewer gets
They get head -> drawer -> **pink stick between calipers beside Dupont's ear** -> 6 boxes become 1 -> lid -> ear -> **a big card rising out of the drawer**.
- The card is now big, centred, sharp and legible (portraits, hand, fingerprint), which is a large gain over R3. But it is cold and dimmer than R3, so it does not feel like a warm reveal.
- The finger no longer reads as "arm". It now reads as a pink tube hanging from the beam. That is because no fist is visible: the finger's base ends just above a dark blue bin (x 340-430, y 780-900), so it looks like it stands in the bin. And because the beam sits at Dupont's ear height, ~60 px from his ear, the shot previews the ear beat that follows (g1462-1471) instead of reading as its own step.

## Scores (R3 -> R4)
| Area | R3 | R4 | Notes |
|---|---|---|---|
| Mechanism clarity (phone) | 7 | 7.5 | Card 6.5 -> 8, finger 3 -> 5, boxes 8 -> 8.5. |
| Key image / beauty | 7.5 | 7.5 | The size and framing gain is cancelled out by the cold card. |
| Light / colour | 7.5 | 6.5 | The card is cooler than R3. The pool is inverted. |
| Camera | 7 | 8 | The card push-in is right. |

## Verdict: FIX-FIRST
Two fixes, in priority order. Everything else is accepted, including the card size, framing, push-in and sharpness, the boxes, and the blur-list waiver.

### 1. Card warmth, g1476-1520 (post only, no re-render)
- In `post.py`, swap the channel order of the pool tint so that it **adds red and cuts blue** in BGR: `np.stack([1.0 - 0.05*pool, 1.0, 1.0 + 0.06*pool], -1)`.
- Ease the card-paper part of the -17 % exposure so the paper does not end up darker than R3.
- **Targets at g1505-1515:**
  - Card paper (e.g. x 110-330, y 540-600): **R - B >= +10**, paper luma **>= 220**.
  - **< 1 %** of pixels >= 248.
  - Surroundings stay where they are now (shot mean ~76-82).
- On the phone sheet, g1510/1516 should read as the warmest thing on screen.

### 2. Finger insert, g1406-1419 (finger frames only)
These are the minimum to pass:
- **(a) Close the jaws.** By g1417, both jaw tips should be within <= 4 px of the finger outline: left jaw from x ~306 to ~330, right jaw from ~400 to ~388 at full res. Hold them closed through g1419. They must not open again.
- **(b) Show the fist.** Dupont's knuckles and the base of the finger must be visible under it, with the finger rising out of a hand. Move or hide the dark bin under it (x 340-430, y 780-900) so the finger does not stand in it.

Preferred, if it costs only a camera key:
- Push in ~1.3-1.4x around x 360 / y 650 so the beam fills >= 400 px.
- Dupont's eye/ear should mostly leave the frame, so the shot stops pre-echoing the ear insert.

### Non-blocking
- A pale green bottle outline sits in the card's name field (g1510 at ~x 490-520, y 495-545) on every card frame. If this is not intended card art, remove it. It is barely visible at phone size.
- Fix QA.md, which says g1420-21 is unchanged; it changed with the fill key, and that is fine. It also claims an 83 % span.

### R5 re-check (I will look only at these)
- Paper RGB/luma on g1505-1515, and the phone sheet at g1510/1516.
- The finger strip at 360x640: the jaws touch the finger and a fist is visible.
- Nothing else will be reopened. If both fixes land as specified, the take passes.
