# QA-art FINAL-fix s21: PASS

- Reviewer: QA-art, FINAL-gate fix check, 2026-11-20.
- Take: `take.mkv`, 99 frames, g1590-1688 (in-shot g1596-1682).
- What I checked:
  - every 6th frame on a phone sheet;
  - full-res frames at g1600, 1640, 1646, 1658, 1668 and 1682;
  - per-frame difference;
  - a side-by-side with s22 from the conformed v1 at 56.5 s and 57.3 s.
- Evidence is in `scratchpad/qa18fix/`: `s21_sheet.jpg`, `s21_vs_s22.jpg` and `s21_tail.jpg`.

## Blocker B4: GONE (all three parts)
- **(a) See-through glowing pots: fixed.**
  - The foreground row (jars, helmet with plume, bowl, pots) is now solid and opaque.
  - It has outlines and a lit clay/bronze shade.
  - There is no x-ray overlap of bodies or handles and no orange glow.
- **(b) Beige-block cups: fixed.**
  - The raised and dropped cup is now a lit gold bronze cup (round gold read at g1658 above the right soldier).
  - At g1668 it is a small gold shape falling at lower right.
  - No untextured beige polyhedra remain.
- **(c) Grey-mauve palette: fixed.**
  - The sky is now moon-blue: top-of-frame mean RGB 0/53/176 at g1600.
  - The ground is blue-navy.
  - Whole-frame saturation is 0.59-0.67, against the target of 0.48 or more.

## s21 vs s22 night palette (`s21_vs_s22.jpg`): MATCH, with notes
| | sky (top) | sat | luma | lower-frame ground |
|---|---|---|---|---|
| s21 g1600 / g1646 | 0/53/176 | 0.59 / 0.66 | 63 / 60 | navy 38/43/81 |
| s22 56.5 s / 57.3 s | 48/86/165 to 62/100/178 | 0.55 / 0.56 | 98 / 101 | warm fire-lit 160/98/75 |

- Both shots now have the same hue family: a saturated moonlit blue sky with warm fire accents.
- The colour jump that made s21 read as another place is gone. Across the whip the cut now reads as the same night.
- Remaining differences, none of them blocking:
  - s21 is darker overall (luma about 60 against about 100).
  - s21's sky is a flat, purer blue: R is 0 at the top, with no moon or clouds.
  - s22's ground is warm orange (fire-lit), while s21's is navy.

## Beat on phone (Yan camp terror as the fire-ox wall arrives): READS
- Black Yan silhouettes stand with a warm rim (g1596-1640).
- The wall of red dragon oxen with tail flames rises behind them, followed by the snap at g1644 and the shock poses.
- The cup flies up, then the hero ox charges into the lens (g1660-1682).

## Hard rules
- **Caption band:** no human face.
  - The hero ox's lower jaw outline reaches about y 900 on the last in-shot frames (g1680-1682). The mouth interior stays at or above y 840, per the director's rule for this shot.
  - The animation is unchanged from the version passed at FINAL, and ox muzzles are allowed. Note only.
- **Pole through a face:** none. The soldiers' spears are beside their silhouettes.
- **Half-cut main character:** none. The hero ox fills the frame by design at the tail.
- **Glitches or see-through:** none.
  - The white glint at about g1650 is the snap sparkle.
  - Frame diff has no single-frame spikes. It rises with the charge after g1644.
- **Floating:** none.
  - The pots sit on the dark foreground floor.
  - The soldiers' feet are on the ground.
  - The cup is in flight by design.

## Notes (non-blocking)
- **N-s21-1:** For a closer match to s22, lift the top sky slightly toward about 50/90/170 so it does not clip R to 0. Adding a moon upper left would help, if that is cheap.
- **N-s21-2:** The empty dark band between the soldiers' feet and the pots (about y 830-960) is large but sits under the captions. Fine.
- **N-s21-3:** The pots read slightly lilac in the moon fill. That is acceptable.
