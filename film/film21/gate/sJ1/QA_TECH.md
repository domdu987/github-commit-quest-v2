# QA-tech sJ1 (team8 fddc54e)

**Verdict: FAIL** (3 blocking: gag 1 unreadable, missing cloak/stool read, bottom third a blue-violet void). Technical side is clean; all fixes are framing/set dressing.

Segment g1640-1708 (69 fr), plan row J1 (line 78): CUT in, push-in on Cressingham's EMPTY table, scale tip on "เร็วดี" (55.80 -> g1677), chest slam on "ประหยัดดี" (56.22 -> g1690), then W (whip left) into J2 (river_low, joined by W, so the whip-out is correct).

## Frame-difference check (ffmpeg, 180x320 grey, mean abs diff)
- g1641-1702: 3.1 to 10.2, smooth waves (low 3.1-4.0 at g1658, g1673, g1689 where the sway reverses; high 8-10 at g1649, g1666, g1683, g1697). No spike. **No hard cuts inside the segment.**
- rhythm.py's "4 CUTS" are g1705, 1706, 1707, 1708 (diff 42, 43, 44, 54): these are the planned whip frames (g1703 22, g1704 34 ramp up). Not real cuts. Non-blocking, expected; ask for those 4 to be passed as whip frames, not cuts.
- The scale tip (g1678) and chest slam (g1690-1692) produce no frame-diff spike (small objects): they are not hard cuts, they are in-shot gags.
- Holds: min diff 3.1 (far above the 0.25 px/frame floor); 0 frames under 0.25, no near-static hold. Median 5.6, p90 7.2 (p90 is below the 12 target of WORKER21 only because the take is one gentle push; the whip is excluded by rhythm).
- Frame 1 is a clean hard cut in from I (no handle needed per the plan).

## Beat table
| g | caption / t | beat | result |
|---|---|---|---|
| 1640-1676 | "เหรัญญิก พูดถูกทุกคำ" 54.53-55.80 | table reveal, push-in + sway | Table, chest "KING'S TREASURY", lantern, barrel readable. Table strip is only ~12 % of frame height (y 480-740 of 1280). Stool with cloak NOT readable (only a stool seat under the table, no cloak). Nobody on set: OK (Cressingham absent, good). |
| 1677-1681 | "เร็วดี" 55.80 | scale tips | Beam starts to tilt at g1678 (about 1 frame late, acceptable), swings through g1690. Beam sits at the right edge, half hidden behind the front tent pole, pans empty, no coins in the pans. Hard to read as a gag on a phone. |
| 1690-1692 | "ประหยัดดี" 56.22 | chest lid slam | Lid starts closing at g1690, shut at g1692, small rebound: on the word, readable (chest is on the left, in clear view). Good. |
| 1693-1702 | 56.4-56.7 | push settles | Fine. Scale beam now at right edge, cut by frame edge. |
| 1703-1708 | 56.7-56.88 | whip left | 6 frames, accelerating yaw, ends on camp pikes and tents (g1708). Frames are crisp, not blurred (strobing, see non-blocking). |

## Checks
- Heads: none in frame, bloodless: OK. No Cressingham: OK (nothing says his fate). Comic: lantern, oversized umbrella canopy are fine.
- Nothing floats: lantern hangs on a rod, scale hangs from its post, chest/ledger on the table. OK. Check scale pans: they hover with nothing in them, acceptable.
- Frame edges: scale beam and pole are cropped by the right edge from g1675 to g1702 (see blocking 1).
- Palette: no blue in the English camp props; the red/yellow canopy is correct. The ground (lower ~35 %) is a dark blue-violet grey (see blocking 3). Turquoise water is the river, fine.
- Camera: one push + sway; the sway reverses 3 times in 2 s (about 15-frame period), reads slightly like a wobble rather than an arc.

## Issues
1. **BLOCKING, g1675-1702, gag 1 (scale tip) unreadable.** The scale is on the right edge behind the front tent pole and is cut by the frame; pans are empty, so a tip has nothing to show. Fix: re-frame so the scale sits in the middle third clear of the pole (shift the camera ~0.5 m left or move the scale toward the chest), hide or move the front pole out of shot, put 3-4 coins in the pans so the tip is visible, make the scale about 1.5x larger.
2. **BLOCKING, g1640-1702, the plan's "stool with his cloak" is not readable.** The only stool is a small seat under the table; no cloak. Fix: put a draped cloak (crimson/gold) on a stool in the left-middle foreground in clear view, and make it the first read (g1640-1676), so the "EMPTY table, Cressingham gone" read lands.
3. **BLOCKING (set palette), g1640-1702, the lower ~35 % of the frame is a flat dark blue-violet ground** with nothing in it (the take notes say the rug is hidden). This is a blue slab in the English camp, and wastes a third of a 720x1280 frame. Fix: tilt the camera down or lower the table into the frame centre, restore the rug (crimson/gold stripes) or warm dirt/straw, and fill the foreground with props (coin sacks, ledger, quill).
4. Non-blocking, g1640-1702: table too small in frame (12 % height). Push in closer (end distance about 3 m rather than 4.3 m) so the chest and scale fill more of the frame; the camera currently only moves 8 %/s.
5. Non-blocking, g1640-1702: sway reverses every ~15 frames (diff dips to 3.1). Use one monotone eased arc.
6. Non-blocking, g1703-1708: whip frames are sharp, no motion blur; add blur or streaks (g1707 is already flagged by qa_auto) so it reads as a whip, not a strobe. Tell the rhythm run to pass g1705-1708 as the whip.
7. Non-blocking, cue: set the scale-tip sound at g1678 (not g1677) to match the visual; chest thud at g1692 (visual), though the word is at g1690.
