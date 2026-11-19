# QA-tech, SET gate, film 12 (set3d12 street + cast12)

Verdict: FAIL

Scripts: `street_work/t_anim.py` printed "checks 105 / ALL OK". `cast12/test_cast12.py` printed "sheets in 5.6 s / ALL OK".
Note: running test_cast12.py left an untracked `film/v3/cast12/tmp/` folder (sec_*.png); delete it before any commit.
Tile order = file number (no contact_order.txt exists; the API.md section 9 table is the order). All 20 tiles opened at full size.
No text or letters were found in any tile. No tile has a head above-to-below 880 conflict among the staged cards (all card heads 446-764, below the line only for crowd placeholders, see 9).

## Issues
1. Tiles 03, 14 (also 05, 08, 16, 17, 19, 02, 10): grain/speckle. Foreground puddles and setts (y 1000-1280) show white salt-and-pepper speckle with visible grain (high-pass std 6.2-7.9 on 02/03/05/08/10/14/16/19 vs 3-4.5 on 06/09/15). Worst: 03 and 14 lower-left puddle rings, 07 and 18 puddle film. Fix: more samples (>= 24) or stronger OIDN/clamp indirect/glossy on the puddle decals, or median-filter the fireflies; re-render.
2. Tiles 07, 18: speckle in the deep-puddle reflection (dark region lower half) at 14 samples. Same fix as 1.
3. Tiles 08, 16 (and faintly 03/14 left): a hard-edged pale rectangular patch on the roadway (x 50-330, y 860-1060). It reads as a broken, cut-off reflection of the sky or a window. Fix: soften or remove the reflection decal or raise puddle roughness there.
4. Tiles 01, 09, 19: a floating bright glowing blob on the road (01/09 at about (180, 767) as a lit rectangle; 19 at about (550, 905) as a round orb). Not attached to any lamp or object. Fix: it is a lamp or halo reflection or a stray halo plane; hide it or attach it to a lantern.
5. Tile 18 (mud): the mud wave is a flat, untextured tan polygon fan with no shading, it covers Hanway's body (only head and coat top show) and intersects the coach rear and front wheel; reads as a broken shape and as a flat sticker, and the colour is out of palette. Fix: shade it (mud brown, glossy), keep it in front of Hanway as a splash, and split the coach/wave overlap with a lower t or later wave start; check t 0.2-0.6.
6. Tiles 08, 16, 17, 20 (rush): the 3D rush placeholders are headless-looking cylinders (black hat plate on a pale tube, no face), they stack in a line along the coach, and the nearest ones interpenetrate the front coach wheel (17 at x 400-520, y 680-900; 20 at x 380-470). They also read as clones. Fix: replace with cast cards (crowd_man_*, crowd_woman_*) and offset the `end` points by >= 1.2 units from the wheel and door; vary their `start` rows.
7. Tile 17 ("rush_wide"): not wide. It is rank_rush pose B, a close view of coach_0 filling the right half; no horse or coaches rolling and few coaches visible. Shot 17 (every coach full and rolling) has no wide preset; the coaches are parked on the rank and `run_coach` only drives `coach_run`. Fix: add a wider/higher rank pose (for example loc (-3.4, -4, 3.4) -> (3.4, 40, 3.4)) and a way to roll coaches 0..3.
8. Tile 15 (pink): the pink umbrella pole passes straight across the coachman's face and chest (x about 395, y 590-720) instead of beside the body, the hand holding it is not visible (the pole foot at (3.75, 18.45, 6.0) is beside the body, but the camera sees it in front of the face). The canopy is flat-coloured with red-orange leaning edge pieces and its rosettes are grey blocks (broken lace look). Fix: move the pole foot behind the shoulder (x 3.5, y 18.9) or tilt the canopy, keep the canopy centred over the head, and colour rosettes pink/cream.
9. Tiles 12 and 13 (umbrellas 0.5 / 1.0): close-slot umbrellas and a placeholder man are cropped at the bottom/left/right edges and sit BELOW y 880: black umbrella disc cut off at the left edge (x 0-55, y 1085-1260), a man with tricorn at the bottom right (head y about 1200), two men at y 920-1100, and at 13 a grey umbrella canopy cut off at (510-720, 1090-1280) and a canopy at the bottom edge (260-470, 1210-1280). Key content under the caption line and clipped by the frame. Fix: drop the slots nearest the camera (every slot whose feet project below y 880 at pose B) from `umbrella_slots`.
10. Tile 02/10 (street_high A) and 12/13 (B): a black umbrella disc lies on the road at about (355, 760) as an unattached flat ellipse; it belongs to the `hanway_crowd` stand point but with placeholders=False it floats with no person. In 12 there is a lone lit green item (340, 795) on the road. Fix: tie the umbrella to the hero card only; remove the loose green prop.
11. Tile 11 (box_dusk) and 20: DUSK colour. The coach body, wheels and the horse are saturated purple/magenta (wheels at x 100-220, y 900-1280 in 11 are pure magenta spokes, horse flank purple), which breaks the colour rule (reds orange-leaning, magenta <= 10 %). The hue report in API.md says ok (3.8 %), but the wheel and horse read as magenta on the phone. Fix: shift the coach wheel red and the horse tint toward orange in DUSK_RAIN (apply the hue guard to saturation, or warm up the wheel paint).
12. Tile 03 (and 14): scale: Hanway placeholder (card 3.1 units, head at 563) is bigger than the coach box coachman and his legs are two thin sticks, the umbrella is 10-12 units wide, wider than the box and horse. Adults should be about 3.2 head units: the placeholder umbrella (canopy ~ 9 units wide vs a 3-unit man) is oversized in 01, 03, 04, 06, 07, 19, so with the cast sprites (umbrella ~ 2 D wide in the sheet) the black umbrella canopy will not match. Fix: confirm the umbrella prop radius at the stand points; scale the canopy to about 2.6 units radius (not larger than the pink one, 2.45) or leave the card prop out.
13. Tile 02, 10 (street_high A) and 01, 09: the sky above the horizon shows hard concentric dark-blue arcs (cloud shadow bands, tile 01 y 0-60 and 330; tile 05 top arc; tile 15 and 11) that look like broken cloud geometry (arcs with no cloud). They read as ring-shaped artefacts through the whole sky. Fix: remove the dark under-band from the cloud billboard or paint it as a cloud base with soft falloff.
14. Tile 14 (busy_0): almost identical to tile 03; the "empty rank" state differs only by a dark lantern at (460, 555) and fewer passengers. The coachman (box_a) and one horse stand in it; nothing says "empty and bored". Shot 22 (empty rank, horses bored) needs a pose with several coaches and no passengers (3 coaches visible) or horses' heads down. Fix: add a coach_low variant pose that shows coaches 0-2 and a drooping horse state, or note that the empty rank will be sold by the cast cards.
15. Cast sheet `cast12/sheet.jpg` (3270x9344, row 1): coachman and coachman_b stand pairs overlap (hats and shoulders touch) and the 3.28 D label for hanway collides with the hat; cosmetic only, but the sheet cannot be used as a reference without cropping.
16. Cast: `coachman_sulk_under_pink_umbrella`: the pink umbrella pole ends at the chest/hat with no hand on it (hand hidden behind the hat), so the prop reads as detached. `coachman_count_coins` and `coachman_count_coins_sky`: the purse is only a few pixels (belly level), the coins are not readable at phone size. Fix: put a visible hand on the umbrella shaft; enlarge the purse and add a gold coin glint.
17. Cast: `hanway_egg_tilt`: the umbrella is tilted far from the hand (handle at the hip, shaft about 3 D long to the canopy), the yolk blob sits on the canopy edge and the canopy is cropped by the cell border; the pole reads as bent. `hanway_cabbage_flinch`: cabbage leaf stuck on the canopy top, no hit squash on the umbrella. Minor, check at the take gate.
18. Stale files: `street_work/final/*_RAIN_final.png` (8 files: box_seat, coach_low, hero_track, market, puddle_low, rank_rush, street_high, street_wide) duplicate tiles 01-08 from an older render and are not in the contact order. Remove or move them so nobody grabs a stale image.

## Shot-plan coverage (23 shots)
Present: street_wide (01/09), street_high (02/10, crane A/B, umbrellas 0.5/1.0 in 12/13), coach_low (03/14), hero_track (04), box_seat (05/11/15 pink), market (06/19 throw), puddle_low (07/18 mud), rank_rush (08/16/17/20), DUSK_RAIN lights, set_rush, set_rank_busy, pink umbrella, throw (cabbage, egg), mud splash.
Missing or insufficient:
- Shot 20 (street_wide reverse, umbrellas popping along the pavement): no preset and no tile. API.md says build it by hand; the reverse looks at the open far end (y -56 row ends open) and the dome with the warm rift behind. Add `street_wide_rev` (for example loc (-0.5, 60, 3.4) -> (0.3, -10, 3.4)) and render a tile; check the open end.
- Shot 9 (street_wide, "low"): `street_wide` is at eye level 3.4; no low variant.
- Shot 7 (coach_low two-shot with Hanway passing below) and shot 15 (close-ish on the coachman with his purse): `coach_low` frames the head coachman at about 455 px y at small size; no close preset for shot 15.
- Shot 2: three coachmen on their boxes: tile 03 shows only box_a and box_b; box_c is not in frame at either pose.
- Shot 14: other coachmen nodding: box_seat only frames box_a; box_b/c are not in frame at 05/11.
- Shot 13 (dusk, street_high, ONE umbrella among many bare heads): tile 10 has no crowd; there is no bare-head crowd state, only umbrella slots (set_crowd_umbrellas) and placeholders; the dusk variant with umbrellas 0 + a crowd of cards must be staged by the cast team.
- Shot 17: see issue 7. Shot 18 (queue at the rank, grin drops): no queue states in the contact set (queue_a stand only).
- Shots 3, 10, 11 (cabbage/egg throws on hero_track/market): throws exist for market (tile 19), but no tile for hero_track with a cabbage or egg splat decal; no tile for the splat decals themselves (egg yolk on the canopy).
- Shot 16 (REVEAL image: rain pours, crowd rushes and fights): tile 16 and 20 show a single row of identical headless placeholders; the hero image of the film is not yet convincing (issue 6).

## Counts
Heads above 880: all staged cards (446-764), PASS. Heads/key content below 880: tiles 12, 13 (issue 9) FAIL. DOF/blur: none seen, PASS. Black/magenta/blank areas: none, except issue 11 (magenta-leaning coach wheels in 11). Text/letters: none, PASS. Interpenetration: issue 5, 6.

## Re-check r1

Verdict: FAIL (one blocking item: the floating glow orb on the road, item 4). Everything else is FIXED or a non-blocking note.
`cd street_work && python3 t_anim.py | tail -2` -> "checks 152 / ALL OK". All 25 tiles in `street_work/final/` opened at 720x1280 (numbers = API.md section 9 table; `contact.jpg` is the same order). No text or letters in any tile. No blur / DOF. No tile has a staged card head below y 880 (heads 420-760). No stray `cast12/tmp`; `git status` shows only QA_ART.md modified (not mine).

### Earlier issues
1. Grain/speckle (puddles, setts): FIXED in 01, 03, 05, 07, 08, 10, 14; PARTLY in 12 and 23 (faint grain in the deep puddle, y 1000-1200, x 100-500) and 16 (y 900-1000). Non-blocking.
2. Deep-puddle speckle 07/18: FIXED (07 clean; 18 bottom puddle y 1100-1280 clean).
3. Hard pale rectangle on road 08/16: FIXED (08 x 50-330, y 860-1060 now a normal puddle sheen).
4. Floating glow blob: OPEN, BLOCKING. A round white orb sits on the road with no lamp or object: 01 and 18 at (180, 815), 24 at (558, 1022) right beside the hero's feet (reads as a glowing ball), 19/21 at about (610, 970) on the pavement, 11 at (510, 935). API.md section 11 admits it. Fix: hide or lower the lantern/halo reflection for those lamps, or clamp the glossy highlight; then re-render 01, 11, 18, 24.
5. Mud wave (23): PARTLY. It is now a shaded, textured fan with brown balls, Hanway is visible in front of it with mud spots and a clear face; but the wave is pale beige stacked sheets (paper-cut look, hard edges at x 190-440, y 280-800), is cropped by the left frame edge, and still overlaps the coach front wheel (x 360-440, y 600-800). Stills only at t 0.4; check t 0.2-0.6 in the take. Non-blocking.
6. Rush placeholders: FIXED. 13/14 use real cast cards (push pose, angry faces) at the coach door; feet at y 880, heads 690-760; hands meet the wheel/door, no body in the wheel. Note: only 5-6 cards, heavily overlapped, so the mob is thin (non-blocking, add more in the take).
7. Tile 17 not wide: FIXED. 15 (rank_wide) shows coach_0 plus 3 coaches receding with the horse; wheels are static in a still, roll is hook-driven.
8. Pink umbrella: PARTLY. The pole no longer crosses the face; canopy centred over the head in 22, rosettes are now white/cream, canopy coral-salmon with dark ribs. But the shaft ends behind the hat at (395, 540) and no hand holds it, so the canopy reads as stuck on the hat (props detached from hands). Non-blocking; add a visible hand on the shaft or lower the canopy onto the shoulder line.
9. Clipped umbrellas below 880 (old 12/13): FIXED. New 20/21 (street_high B) have no clipped content at the bottom edge.
10. Loose black disc / green prop on the road: FIXED (not seen in 02, 04, 20, 21).
11. Dusk magenta coach/horse: PARTLY. 25 wheels now red-orange and horse brown, good; 14 horse flank and coach body still maroon-purple (x 570-720, y 660-860); 23 (RAIN light) coach is deep purple with magenta spokes (x 400-560, y 690-780). Non-blocking, warm the DUSK/shade tint on coach and horse.
12. Placeholder umbrella scale: FIXED (01, 02, 04, 07, 11: black umbrella is about one body width wider than the head, smaller than the pink one).
13. Sky arcs under clouds: OPEN, non-blocking. Dark thin ledge lines still extend beyond the cloud billboards (01 y 185 and 380, 07 y 360 and 420, 13 y 300 and 380, 16 y 290). Softer than before and read as a stylised cloud shadow.
14. busy_0 vs 03 (empty rank): PARTLY. New 16 (rank_idle, horses bored, box_a/b/c) is distinct from other tiles; the horse head is cropped at the right edge so the drooping head is not seen. Non-blocking.
15. Cast sheet label overlap: NOT RE-CHECKED (cast12 sheet is outside the 25 tiles); remains cosmetic.
16. Cast purse/coins: NOT in any tile; unchanged until a cast12 re-check. Pole-hand see 8.
17. egg_tilt / cabbage_flinch: NOT in any tile; no change to verify.
18. Stale `*_RAIN_final.png`: FIXED (final/ holds exactly 25 files).

### Coverage gaps
- Shot 20 (street_wide_rev): FIXED, 03. Note the pavement crowd there is faceless blocky placeholders at y 690-760 with a soft look (non-blocking, cards replace them).
- Shot 9 (low wide): FIXED, 02.
- Shots 7/15 close two-shot: FIXED, 06 (Hanway head 695, coachman head 421).
- Shot 2 three coachmen: PARTLY. 10 shows box_a (big, head 423) and box_b (small, about (362, 590)); box_c is not readable in the frame. 
- Shot 14 other coachmen nodding: PARTLY: 25 shows box_b small at (203, 620); box_c still not framed.
- Shot 13 (dusk, bare heads + one umbrella): FIXED, 19 (hero's black umbrella among bare placeholders; placeholders are faceless cylinders from the high angle).
- Shot 17: FIXED, 15. Shot 18 queue: FIXED, 08 (two queue cards at (175-225, 720-830), small but legible). Shot 16 reveal: FIXED in principle, 13 (thin mob, see 6). Shot 22 empty rank: PARTLY, 16.
- Shots 3, 10, 11 throws: PARTLY. 24 shows the cabbage mid-arc (green block at (555, 355), correct, in the air); there is still no tile with a splat decal on the umbrella or a hero_track throw.

### New failures
- None blocking apart from item 4. Hanway card head/umbrella contact in 06, 07, 12, 24 is correct (hand on the handle). Rush cards touch the door, not floating. No interpenetration of cards with the coach except the mud wave and wheel in 23.
- Non-blocking: 23 mud wave is cropped on the left edge (x 0-60, y 250-500); 03 and 19 crowd placeholders look soft.

Re-check fix list for the next round: (1) remove the orb at the 5 positions in item 4, (2) optional: hand on the pink pole, warmer purple coaches, framing of box_c, splat tile.
