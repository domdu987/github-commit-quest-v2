# QA-art: film 23 style board (Ghost Army)
Looked at: board_1-3 at full size, a 360x640 phone sheet, caption-band crops and tank close crops, against refs R2/R4/R5/R7.

## Scores
| | 1 dawn | 2 lane | 3 night | overall |
|---|---|---|---|---|
| Rich and detailed? | 8 yes | 4 NO | 5 NO | **5, NO** |
| Lighting & colour | 7 | 6 | 7 | **6** |
| Composition / phone | 7 | 3 | 6 | **5** |
| Hero tank (afar / up close) | 7 | 3, hidden | 3, white lumps | **4** |
| Match to refs | 6 | 4 | 6 | **5** |

What works: still 1 has the right layout: green patchwork, hedgerows, red roofs, village, river, gold horizon, findable soldiers and cows. Still 3 has good warm-against-cool contrast and a good moon key.

## Blocking findings
- **Overlap:** in still 3 a lantern pole runs through the left soldier's body. In still 2 the bike basket crosses a soldier's helmet.
- **Caption band 880-950 not clear:** a tank and a soldier sit in it in still 1, and the left soldier's body in still 3.
- **Haze:** in still 3 the lantern halos fog the middle of the frame, and the bottom 30 % is an empty, grainy plane.
- **Shadows:** flat, saturated indigo-violet slabs (about 35 % of still 1) read as paint, not shade.
- **Cheap backdrop:** hard half-dome clouds with purple slab undersides and faceted low-poly hills.

## Fixes, ordered by impact
1. **Rebuild still 2 around the tank** (`build_morning` stage). Put the half-inflated tank centre frame, fully visible at about 55 % of frame width, barrel sagging over the lane, star, seams and valve facing camera. Place soldiers beside it, not in front, and run the pump hose into the valve. Move the bike to the right foreground edge. Leave room for the 4-man lift and the two cycling Frenchmen. The barrel currently reads as a cucumber.
2. **Fill the bottom 40 % of still 2.** Replace the plain orange dirt and grey rocks with ruts, a puddle reflecting sky, a flat deflated rubber sheet, a coiled hose, a toolbox, straw from an open crate and chickens, kept low-contrast inside y 880-950. Keep the full sign words in frame ("SPECIAL TROOPS", "DECOY M4", "HANDLE WITH CARE"). Make the lavender smoke white-grey.
3. **Fix the shade colour** (`mat_g` shade_mix / grade). Target hue 242-250, saturation about 0.45, value raised about 15 %, with soft contact AO under tanks, hedges and feet. This also fixes the shade-hue misses on stills 1 and 3.
4. **Night rows** (`build_night`). Give the tanks real silhouettes (turret, barrel), dark olive with a cool moon rim on top, not pale marshmallows. Cut lantern `halo_r` from 3.4 to about 1.6 and remove the fog spread. Fill the ground with ruts, cables from truck to tent, crates and grass, and raise the denoise.
5. **Sound truck.** Mount a deep flared metal horn (bell) on an olive truck. The flat ring reads as a mirror.
6. **Blocking and band.** Move the night soldier 1.5 m off the pole with his feet above y 870. In still 1, shift the camera or the column so a hedge or field fills the band.
7. **Sky and hills.** Use soft painted cumulus with graded undersides, and smooth, textured hills with far treelines.
8. **Rubber up close.** Raise the rubber spec to about 0.22 and draw a seam ink line on the hull.

## Verdict: **FIX-FIRST**
Still 1 can be kept for the BIGZOOM after fixes 3, 6 and 7. Stills 2 and 3 need to be recomposed, and the board must come back to QA-art before the full set is built.
