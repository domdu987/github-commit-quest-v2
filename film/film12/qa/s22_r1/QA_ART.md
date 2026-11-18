# QA-art, film 12, take s22 (ENDING: shots 22-23), TAKE gate (Stricter QA C)
Reviewed: f6/ at full size (f_001, f_016, f_020, f_030, f_042), cut/n_05-06, phone_sheet.jpg (360x640), against approved set tiles 16 (rank_idle) and 22 (box_seat pink umbrella).

## Verdict: FIX-FIRST (shot 23 only; shot 22 can ship as is)
The joke reads. The problem is the last image of the film. It ends tighter than approved tile 22: the canopy is cropped at the right edge,
and two pure-black lantern boxes are the strongest dark shapes in the frame. Fix 1 alone costs one shot-23 re-render
(129 frames x ~26 s, about 1 h at 2 threads) and fixes the final hold. Fixes 2-3 can go in the same render.

## Scores (1-10)
| criterion | s22 rank | s23 box seat | note |
|---|---|---|---|
| set density / ornament | 8 | 8 | street, lamps and coaches match the approved set |
| light & colour | 7 | 6 | warm windows against the blue-violet rain sky work; canopy reads salmon/coral, not pink; black lantern boxes have no value |
| composition / phone legibility | 7 | 5 | s22: low-angle street, bottom ~40 % is empty wet cobbles (as in tile 16, acceptable). s23 end: canopy cropped right, lower third is muddy orange shafts/horse-back clutter |
| acting | 6 | 8 | s23: droopy brows, frown and red nose, hand clutching the pole at the chin: clear sulk. s22: coachman sits upright and the horses' heads barely read as "bored" on the phone |
| key-moment clarity | 7 | 7 | umbrella pops at the cut; "empty coach / nobody waiting" comes only from s22 |
| match to approved tiles | 8 (tile 16) | 6 (tile 22) | tile 22 shows the whole canopy with sky margin; the take pushes past it |
| **overall** | **7** | **6.5** | |

## Is the joke readable on a phone in under 2 s?
- Frilly umbrella: YES. It reads in the first phone frame after the cut (g1663, 3.0 s): big, central, scalloped edge with white tip-balls, unmistakably a lady's parasol.
- Pink: PARTLY. On the phone it reads coral/salmon-orange (known hue-guard compromise). The narration says "pink" at the same moment, so the joke survives, but the picture alone does not say pink.
- Sulking face: YES. Readable at 360 px from about 4.0 s as the push closes in. At 3.0 s the face is small but the frown and red nose still carry it.
- Empty coach / nobody waiting: WEAK in s23 by itself, because no passenger compartment or pavement is visible. It is carried by s22, where the street is empty of people and the lanterns are dark. Across the 7 s ending it reads; inside the 2 s after the cut it reads only as "sad man under girly umbrella".
  Overall: the punchline (man + girly umbrella + sulk) lands in under 2 s. The "no customers" half relies on s22 plus the narration.

## Changes (in priority order)
1. **Shot 23: end the push earlier, matching tile 22.** Stop the A->B push about 15-20 % short, or pull pose B back 0.3-0.4 m along the view axis, so the whole canopy,
   including the right-hand tip-balls, sits inside frame with about 5 % margin and a band of sky above it. Keep the head near 0.42 H (it will be about 0.45 H, still clear of the caption band).
   This is the film's final hold (g1770-1784), so it must be the complete approved picture, not a crop.
2. **Shot 23: replace the pure-black lantern boxes** (left foreground, and right at the coach box) with unlit glass: dark slate blue (#2a2f4a) with a thin rim highlight,
   or hide the left one. At phone size they read as holes and pull the eye away from the face. They stay "dark lanterns" (idle rank) without being black voids.
3. **Shot 23: push the canopy toward true pink** if the hue guard allows. Use a lighter, less saturated rose, for example base around #F29BB8 (hue about 340) with the lace holes kept,
   instead of the current coral. Run hue_report on the result: the canopy is about 12-15 % of the frame, so check the magenta share stays at or below 10 %. If it fails, keep the current colour
   (client-accepted) and skip this item. Do not block on it.
4. **Shot 23 (cheap, same render): calm the lower third.** Add a light darkening/desaturation gradient on the bottom ~30 % (the orange shaft and horse-back shapes).
   The caption sits there anyway, and the eye goes up to the face and umbrella. Alternatively tilt the camera up 2-3 degrees at pose B, which also helps fix 1.
5. **Shot 22 (optional, non-blocking, no re-render requested):** for the next pass, a glance from box_a toward the empty kerb, or drooped horse heads more visible, would make
   "nobody waiting" read without narration. Not worth a re-render now. Ship s22.

## Not issues
Cut at g1656 is clean and readable (wide rank -> box seat close). Rain is continuous, palette is continuous across the cut, nothing is frozen, and the mouth stays shut (no quote).
