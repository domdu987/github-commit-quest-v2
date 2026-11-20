# QA-art: TAKE gate round 5, film 20 (2026-11-20, Opus)

**Inputs**
- Takes v3/film20/s06 (join only; T09 = s09 already passed), s21 and s24, rebuilt from take.mkv.part*. Also their QA.md, meta.json, contact.jpg and phone_sheet.jpg.
- Rules: QA_TEAM.md (client taste, QA-art, §G, §H, §I) and the ref_shorts sheets.
- My earlier reviews: TAKE3_ART.md and TAKE4_ART.md.

**Frames**
- s21 and s24 at 2 fps, full size and 360x640, in /tmp/claude-0/-home-user-github-commit-quest-v2/ef039ac4-2646-5d6b-b692-04a5aa8620ca/scratchpad/takeart5/<take>/{full,ph}/.
- Extra strips in the same folder:
  - join.jpg: s06 g596-603 on top, s09 g604-611 below.
  - joinpair.jpg: g603 next to g604 at full size.
  - s24_start.jpg, s24_bite.jpg (g1804-1830, every 2nd frame), s21_a.jpg and s21_b.jpg.

**Scores** (1-10):

| take | set | light | comp | act | key | cam | chan | verdict |
|---|---|---|---|---|---|---|---|---|
| s06 -> s09 MATCH join | 7 | 7 | 7 | 6 | 8 | 8 | 7 | **PASS** |
| s21 REVEAL 2 rings -> aha | 7 | 8 | 7 | 7 | 7 | 8 | 8 | **PASS** |
| s24 BIGZOOM 2 | 6 | 7 | 6 | 7 | 7 | 7 | 7 | **PASS** (with conform notes) |

## s06 -> s09 join: PASS
- **TAKE3 s09 F1 (jump at the match): FIXED.**
  - g603 and g604 show the same pose: Maupassant crouched on the banquette edge with no glass, the same window, the same girder stumps and the same floor.
  - The mean abs grey diff g603 -> g604 is 4.84, which is the same as normal motion inside the take.
  - On the 8+8 strip the join cannot be seen. The forge smoke thins away by g603, so there is no pop.
- The s06 meta.json `end_cam` still lists the old pose (3.533, 6.506, 0.983), while QA.md lists the new one. This is a paperwork mismatch only; the picture is right. The render team should correct the meta.
- **§G** on the s06 phone sheet: no floating and no slicing.

## s21: PASS
- **F1 rings (round 4): FIXED.**
  - The rings are now thin, pale arcs that fade as they spread, and they no longer read as scratches. Most are near-white and only faintly blue at full size (g1502-1532), with a clearer blue at g1547. None is a thick bar.
- **F2 wire: FIXED.** The wire is a thin, 2-3 px pale line at both g1427 and g1547. The full-height white bar is gone.
- **F2 glow/pulse: FIXED. I accept it.**
  - At g1547 the lower lattice and legs take a short pink-white rim pulse, while the upper iron stays red-orange.
  - The pulse reads as "the iron lights up". It does not read as a milky column. It is a little pinker than blue-white, but it is brief, so this does not block.
- The group phase (g1577-1655) is unchanged from the round-4 PASS: cobbles, drop, salute, cheer, and the lit tower behind.
- **§G:** clean on every 0.5 s tile. There are no white slashes in the group framing.

## s24: PASS
**Round-4 items:**
- **F1 landing: FIXED.**
  - The camera now lands at eye level with a 55 mm look.
  - His head is about 180 px and fully clear of the caption band.
  - The "X" ceiling bands have gone; the back wall now only folds into a shallow V behind his head. Chandeliers and lattice beams sit at the top, and white-clothed tables show at the sides.
  - The table is laden (glasses, plates, carafes) and takes about 20 % of the frame. With the flat orange sill band at the bottom (about 14 %), the foreground is about a third of the frame. I accept this.
- **F2 the bite: FIXED.**
  - At g1806-1818 a big orange forkful rises and reaches his mouth, keyed on "กินข้าวบนหอ".
  - His eyes close in pleasure, then the fork lowers (g1820-1830). This reads on the phone sheet.
  - The cheek-squash chew is subtle, but the beat is clear.
- **F3 start target: PARTLY FIXED. I accept it.**
  - A small warm red-yellow window glows at the centre of the first platform from g1724. It is the only warm dot in the frame, but it is only about 5 px at phone size.
  - The peach horizon band (the lower third of the sky) is still there. It lasts about 1.5 s, and the upper sky is clear blue.

**Conform notes (non-blocking, about 1 s each):**
1. Paint out the thin black vertical seam below the table and through the chair in the landing frames (g1819-1858). It is the same set seam as in s27.
2. If grading allows, cool the horizon in g1724-1770 toward blue.

## Cross-take
- **Colour:** on brand. s21 is deep night blue against lit red-orange iron; s24 is red/orange interior warmth after a blue-sky wide.
- **§G:** all three are clean on every 0.5 s tile. No floating, no slicing and no face over 35 % of the frame.
- All film 20 key takes now hold an art PASS at the TAKE gate.
