# set3d17 fix round 1 (answers QA_ART_SET.md, P1 + P2; P3 horse not done)

Re-rendered at 720x1280, 64 samples, OIDN denoise, with the REAL cast17 cards (stage Actor cards) on the stand points: measure_low, measure_door, measure_high, drawer_box, card_hero, records_aisle, measure_wide, records_desk, drawer_big, records_ladder (DAY_INT) and measure_wide, measure_chair, records_aisle, records_desk, card_hero (EVENING_INT). The other 5 finals are the old ones. `contact.jpg`, `contact_small.jpg`, `hue.md` rebuilt (all 20 tiles; hue.md ring numbers for the old tiles are the old placeholder numbers). Placeholder numbers below come from `stand_report.py`; real cards lean toward a low or high camera, so near heads sit up to 130 px further out (measure_low clerk, `dx -0.3` applied).

## P1
| # | before | after | number |
|---|---|---|---|
| 1 hood | cam (-0.45,-0.3,0.5): hood over `clerk`; measure_door look (3.2,-2.4,1.3): slab over left 25 % | measure_low cam (0.3,0.55,0.5); measure_door look (3.2,-2.9,1.3); tripod unmoved; its cloth drape shortened (0.95 to 0.72 m) because at the QA camera the old hem still covered 16 % of the frame | hood (magenta repaint) 4.3 % of measure_low, 1.3 % of measure_door; 0 % of every staged head disc; foreground ledgers/crate moved 1-1.5 m ahead of the lens |
| 2 drawer_box | dim brown box low in the drawer, about 190 px | light-ochre box (`box_ochre`) 0.28 tall, on a ledger block so its top is flush with the drawer rim, own warm spot `box_lamp`, sun 0.5x, window 200 W, camera (0.09,0.99,1.68) | box 341 px wide at 720 (47 % of the frame); box luma 154 vs 80 for the drawer interior = 1.9x |
| 3 hero card | two grey generic faces + squiggle name | both portraits Dupont bare-headed (ginger hair, stubble, ruddy cheeks, red neckerchief): front + true profile with an ear; empty glass bottle in a framed name panel; no letters or digits; same art in `cast17.card_svg` (`card_match.jpg`) | ginger and bottle read in card_hero at 360x640 (see contact) |
| 4 measure_high | globes at head height among the bench heads, blown bracket globe at y 990+ | second gasolier hung 0.85 m higher (`lamps_up`); foreground bracket unlit; look-at z 0.5 to 1.1 | nearest globe to a staged head 6.3 head radii (needed 1.2); frame pixels at y 880-950: max luma 164, 0 px >= 250 |

## P2
5. Stand points (placeholder heads, 720x1280). All staged heads: cy 450-760, chin < 880, inside the frame, no head overlaps below 1.0 head-D except where noted.
   - measure_wide: bench0 (111,642) queue0 (239,650) chair (357,651) clerk (411,609) door_mid (613,642).
   - measure_high: bench0 (184,616) bench2 (251,542) queue0 (152,745) chair (435,616) tripod (339,691).
   - measure_door: door_out (339,586) door_r (531,637) door_x (668,581) (new marks door_r, door_x; door_in/door_mid dropped).
   - measure_low: chair (324,714) clerk (509,555).
   - records_aisle: aisle1 (321,758, moved to (-0.9,5.4)) aisle2 (389,746) ladder_foot (386,685) aisle_far (377,635); aisle0 dropped.
   - records_desk (look z 1.0 to 1.4): desk_clerk (419,586, moved to (-0.9,3.4)) desk_stand (611,636, moved to (0.3,3.8)).
   - records_ladder (look z 3.2): ladder_up (349,598); ladder_foot dropped.
   - drawer_big: new marks drawer_r (583,476) drawer_l (190,660); the old clerk/inspector were off-frame.
6. EVENING_INT: sun 0.25x, skylights `#2f3270`, sky `#12143a/#26295a/#3a3878`, gain 0.5, lamp_k 1.4 (not 2.5: 2.5 made the frame brighter than day), window 40 W. Mean luma evening/day: measure_wide 0.80, records_aisle 0.72, records_desk 0.79, card_hero 0.86 (target 0.80-0.85).
7. measure_wide near floor: second small rug, crate stack (3 crates), coal scuttle, stool with a kepi, added to the existing stool and gas standard (y -3.5..-1.5, path to the chair kept clear).
8. Cast: `inspector17` `tache_scale` 1.3. `test_cast17.py canvas / robust / sheet`: 3 073 575 checks, 0 failed.

## Remaining issues
- P3 horse not done: the police wagon still has shafts and no horse (keep it parked, as QA advised).
- drawer_box and card_hero keep a warm bloom on the drawer front and the card centre (the box is still the brightest object, but the card is near white).
- EVENING_INT gas lamps are 1.4x (day 0.75x); the evening look is dark ceilings and navy skylights with warm pools, not a full night.
- The seated inspector is a frontal sprite floating over the 3D chair (feet hidden); the measure_low tile shows the tripod hem at the top right (4 %).
- measure_chair EVENING and street tiles other than the listed ones were not re-checked beyond the render.
