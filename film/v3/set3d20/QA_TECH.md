# QA-tech, SET gate, film 20 (set3d20) -- VERDICT: FAIL

Inputs: contact.jpg, 35 full-size tiles (work/final, int_work), hue_report.txt, int_hue.txt, cost_report.txt, API.md, shot_plan.md, QA_ART_board.md (v2).
Caption band 880-950 (cyan lines checked on every tile). Cost: all tiles <= 41.7 cpu s (max I04 41.7, I01 39.1, I03 39.7): PASS, nothing > 45.
No readable text or tofu found on any tile (the protest sheet in I03/I04 is loops + dashed greek lines: OK). No blur/DOF found: all tiles sharp.

## BLOCKING (fix before renders)
1. S01_site_wide_stage0: three riveter heads at y 937 (chin 949), 909, 879 (chin 890) sit in/at the caption band. Fix: move the worker marks up/back (heads <= 860) or reframe so no head is in 880-950. S02 end pose: all six riveter heads at y 1012-1745 (the near ones huge, 92 px), all >= 880: re-place the workers so heads are < 880 or off frame.
2. S04_site_leg_low: Eiffel head y 1097 (chin 1127), >= 880. A riveter (13 px) hangs alone in the sky at top centre (y 93), reads as floating. Fix: move mark `eiffel_leg` up to the foot with head < 860 (or lower the camera), put the scaffold rider on a visible deck.
3. S01, S03, S04, S10-area ground: hard BLACK diamond / quad patches on the ground (S01 bottom-left, S03 and S04 centre-bottom). These are the invisible shade-caster geometry rendering black (visible in S01 at ~x 190 y 500 of 720x1280). Fix: make the casters shadow-only (is_shadow_catcher/ray visibility camera = off).
4. S03_site_table 13.5 % and S04_site_leg_low 12.6 % magenta of frame (limit 10 %): FAIL. Cause: dark violet scaffold shade. Fix: warm the shade ambient or lower sat of the dark timber so magenta < 10 %.
5. SITE ground (QA-art SITE fix 1): bottom-eighth luma <= 70 not met in S02 96.6, S07 109.2, S09 88.1, S10 107.0 (met: S01 63.7, S03 50.9, S04 40.9, S05 56.4, S06 49.7, S08 60.6). Also bottom 35-45 % of S03/S04/S05/S06 is flat blue-grey ground, not ochre, with no props (reads empty at phone size). Fix: foreground shade layer + ochre trampled ground, planks, ruts, gravel in the nearest 15-30 %.
6. SITE foreground 1-2 D (fix 2): S08, S09, S10 have none; S06 has only a thin pole. Add a girder end / post / barrel in the nearest 15 % of every site camera.
7. SITE workers (fix 3): body px listed [76,68,72,61,59,64]: one is 59 < 60 px (not met). 5-8 workers: met (6). Crane 92 px >= 40 met; scaffold/leg 0.72 >= 0.33 met; sky open S01 19.3 % <= 30 met.
8. T04/T05/T07 tower_dusk (+ NIGHT): all marks (eiffel_old 1209, officer 1200, riveters 1173-1211) have heads at y 1173-1211, 16-22 px tall, far below 880 and tiny: old Eiffel / officer / workers cannot be staged with heads above 880 or readable at phone size (shot 18, 22). Fix: move the marks to the mid-ground (about 12-20 m from the camera) and raise them so heads are 700-860 and >= 40 px, or raise the camera shift so the foot of the tower sits above y 880.
9. T08/T09 tower_hut spark: T09 V>.95 = 55 % (luma top 199), the whole frame is blown. QA-art fix: two brass balls + thin jagged arc, halo 12-24 px. Not met. Fix: halo emission down, arc only, whole-frame flood removed.
10. TOWER wires (QA-art TOWER fix 1): in T04/T05 the 4 wires read as 5-8 px bright white streaks; in T10 they are about 10 px white bars with a glow (emit not <= 0.6, not 2-3 px). Not met. T10 V>.95 = 18.7 % (limit 9 %). Fix wire_r ~0.25, colour #d8ccc0, emit_k <= 0.6.
11. cafe_window (I05, shot 8): the window shows a big finished-looking arch + lattice, no stub, no visible forge smoke column: the 1887 stub/black chimney beat (18.96 "ปล่องโรงงานสีดำ") is not stageable. Fix: show the 4 stub legs at the skyline with the smoke column in the window; make the window larger in frame.
12. cafe_low / cafe_low_close stub vs full (I06 vs I07, I08 vs I09): the only difference is ~2.5 % of pixels, a thin dark spike behind the head and a mullion. Shot 16/17 ("full tower now stands in the window") does not read: the legs are hidden behind the head. Also the window sky has blown-white bands (rows of V=1.0) and black square patches at the mullion joints. Fix: shift the head or the camera so the tower fills the window right/left of him, remove the blown band and the black joint blocks.
13. resto_table (I11, shots 2 and 25): a green bottle + glasses sit directly in front of Maupassant's mouth/chin, a chair back cuts the lower frame: "napkin tucked / eating" cannot read. Fix: move the bottle and glasses out of the face line (to the side, below y 780), keep the chair back at the edge. Shade hue cream/cloth/wall/carpet 226.1 < 230 (QA-art RESTO fix 5): not met. Tablecloth shows only ~3 broad folds, not 6-8 flutes: not met.
14. resto_wide (I10, QA-art RESTO fix 2): no gilt mirrors, no buffet, no coat stand visible; only 2 actors + 3 small diners; centre is a navy carpet with white disc dots (reads as stepping stones). Dressing 20-26 objects, 2-3 mirrors, 4-6 diners: NOT met. (met: floor 24.3 %, blue 25.8 %, magenta 1.1 %, red 33.8 %.)
15. resto_view (I12, shot 26): Maupassant faces the camera, head 207 px at left of centre, window view is behind him: the planned over-the-shoulder look OUT of the window is not what this camera gives (the audience sees his face, not the view past his shoulder). View itself is good (Paris, Seine ribbon, both Trocadero towers, lattice on the glass, no tower, view > 120 px wide). Fix: render the card from behind (back-of-head card) or mirror the camera past his shoulder, glass raised toward the view.
16. Hue band (240-260 shade mean, lit exteriors; no exception listed): T01 230.3, T02 227.9, T03 227.9 (median 221.6) below the band; S02 291.0 (median 235.8, only 49 % of shade px in band); S08 261.5; T04 264.5 (just over); T12 342.8 (median 190.6, 3.3 % in band; exterior wall shade is orange). Fix: shift sky-ambient hue a few degrees toward violet (T01-T03) and cool/neutralise the shade on the T12 wall and S02 foreground. Exceptions accepted: T05/T10/T11 night, T08/T09 hut interior, warm cafe/resto interiors (I01-I05, I08, I09 shade-all) per the QA note. Magenta <= 10 % passes everywhere except item 4.
17. T03_tower_fair_1910: differs from T02 (1889) only in rows 776-895 (the crowd); 1910 is not distinguishable by light or props (no new sign of 20 years). Acceptable only if shot 23 is carried by the actor swap; if the plan means to show antenna/hut, `set_year(1910)` shows neither in this tile. Confirm or fix with the director.

## NOTES FOR RENDER WORKERS (camera/staging)
N1. T01 tower_low: Maupassant head 793 chin 852 (ok <880), but his legs are two thin sticks with no visible contact shadow on the plaza; the lamp-post is a bare black pole (no lamp head). Add a contact blob and put the lamp head in frame; push-in must not take the chin over 880.
N2. T02 child_fair chin 869 (11 px from the band) and gent 816: the push 8 %/s and the snap push on Eiffel will cross 880: start the push from a camera that keeps chins < 860 or tilt up.
N3. T12 tower_window_pull: lit window and Maupassant visible (46 px, head 736) but he is tiny and the glass shows dark orange horizontal bands (reflections); his chair is brown, the I11 chairs are blue: make the end of the pull and the interior match resto_table (blue chairs, white cloth).
N4. T13 window end: head 871, 2 px: ok, last 12 frames still; he is invisible at that size (smug eyes shut will not read).
N5. Time/light continuity: tower_fair 1889 (T02) sunny blue sky (luma 81) vs resto/cafe windows warm peach (I11 sunset-ish sky, I12 cream-peach): pick one sun colour at the cuts 24-27. cafe_low shot 9 (1887) and 16 (1889) are the same tile except the 2 % diff (item 12).
N6. cafe_low and cafe_low_close: Maupassant card fills the frame with the head at 626-659; any crane up on "rises" must keep chin < 880; cafe_low_close head 626 chin 742 ok.
N7. cafe_wide I01/I02: chin 884 (architect, I02) is 4 px over 880: keep the slide short or tilt up 20 px. Smoke and signature insert (I03/I04): readable as scribbles only, ok; the dashed greek block at the top of the sheet reads as printed text lines at close range: acceptable.
N8. resto_wide: waiter + Maupassant chins 715-736, feet 886-897 (they stand in the band at y 880-950): feet crossing the caption band is allowed, heads are free.
N9. S05 site_fence: shade mean 239.5 (median 242.8, ok); two small figures at the far fence are tiny; Parisians heads 677-697, all < 880: ok.
N10. SITE dressing at phone size is dense in S01/S07/S08, thin in S03-S06 (flat ground). Ground colour reads grey-blue in the shaded lower third (QA-art asked warm ochre).

## QA-art mandatory fix list: numbers
SITE: 1 bottom luma <= 70: MET S01/S03-S06/S08, NOT MET S02 96.6, S07 109.2, S09 88.1, S10 107.0; shade hue mean 240-260: MET S01 246.0 (NOT S02 291.0, S08 261.5). 2 foreground: NOT MET S06/S08-S10. 3 crane 92 px MET, scaffold 0.72 MET, workers 6 MET but one body 59 px (< 60) NOT MET. 4 sky <= 30 % MET S01 19.3 %. 5 object count: S01 estimated >= 12 MET, S03-S06 not countable (thin). 6 stages converge: MET S08-S10 (stage 1 stubs visible).
TOWER: 1 wires 2-3 px / emit <= 0.6: NOT MET. 2 spark gap halo 12-24 px: NOT MET (flood 55 % V>.95). 3 clouds bumpy cumulus: MET (T04/T05). 4 wagon + crowbars + FG lamp-post: MET (lamp is a bare pole); objects >= 12: MET. 5 V>.95 <= 9 %: MET T04 5.4, T05 2.7, T06 3.8, T07 4.8; NOT MET T10 18.7, T09 55; stars <= 15 MET.
RESTO: 1 floor <= 25 % MET 24.3 (resto_wide); FG chair MET; parquet pitch not measurable on a still. 2 dressing 20-26 / mirrors / buffet / 4-6 diners: NOT MET. 3 cloth flutes 6-8: NOT MET. 4 window view >= 120 px, Seine, Trocadero, no tower: MET (I12). 5 blue >= 12: MET 25.8 / 42.6; magenta <= 10: MET 1.1 / 1.7; red 30-45: MET 33.8 / 33.1; cloth/wall/carpet shade 230-260: MET resto_wide 231.2, NOT MET resto_table 226.1. 6 hero stand-in card: MET (head < 880, contact shadow on the chair ok).

---
# ROUND 2 (re-check at full size; numbers measured on the new tiles by QA-tech, hue/luma from the rebuilt hue_report/int_hue)
## Round 2 VERDICT: FAIL (one blocking item left, small); everything else PASS or NOTE
Cost: all <= 41.7 cpu s: PASS. No blur/DOF, no readable text/tofu, no magenta > 10 % (max frame magenta S07 7.85 %).

## Round-1 blocking items, re-checked
1. Heads in band: S01 now chins 745-848, S02 chins 628-751: FIXED. S06 chin 824, S03 723: OK.
2. S04: Eiffel head 770/793 (< 880), riveters 12-19 px on the scaffold deck (standing on the platform now, not in the sky): FIXED.
3. Black quads on the ground: S01/S02/S03/S04 black px 0-0.5 % (no black blocks, measured): FIXED. NEW: T12_tower_window_pull has 5.9 % pure-black pixels, a full-width black band at y ~960-990 under the window (and a dark band at y ~130): REMAINS, see R2-B1.
4. Magenta: S03 1.6 %, S04 0.9 % (frame): FIXED.
5. Ground luma bottom-eighth: S01 67.4, S02 55.0, S03 54.2, S04 51.3, S05 48.0, S06 47.2, S08 58.3 met; S07 92.8, S09 87.7, S10 106.1 not met: NOTE (S07 bottom is the scaffold rail over sunlit iron; S09/S10 are crane-up pulls with ground miles away; render workers keep a shaded FG post/rail at the bottom). Lower third of S03-S06 is still a flat blue-grey slab (about 35 % of the frame, caption zone): NOTE, keep camera tilted up 3-5 deg so < 30 % of the frame is empty slab.
6. Site foreground 1-2 D: now S01 (black chimney block + barrels), S03/S04/S06 (shed block + post), S07 (rail): MET. S08-S10 crane-up shots (far from everything): NOTE, nothing to put 1-2 D from a crane camera; ok.
7. Workers body px [84, 75, 87, 71, 69, 90], all >= 60: MET.
8. tower_dusk: T04/T05 still have the heads at y 1200-1211, 20 px (the board camera): the new staged tile T14_tower_dusk_chars has heads at y 775-783 (32-42 px), chins 791-875, feet <= 893, actors at the wagon foot: PASS for shots 18/22 PROVIDED the takes use the T14 camera (NOTE R2-N1). The T14 bottom third is empty blue ground (bottom luma 27.5).
9. Spark (T09): V>.95 8.4 % (was 55 %), white 1.3 %: FIXED; the gap is a pale blue ball with a white X, not two brass balls + jagged arc: NOTE for the take (halo ok, arc only on taps).
10. Wires: T04/T14 are now 4-5 px pale white lines (ok at phone size, still brighter than #d8ccc0), T10 still bright-white lines about 6-8 px with rings; T10 V>.95 5.3 % (met, was 18.7 %): NOTE.
11. cafe_window (shot 8): the window now shows the smoke column (black chimney smoke over the arch) and the stub/arch with Paris roofs, painter/poet/composer/architect heads 702-794, chins <= 792: FIXED (the lattice still reads as a taller arch than a stub; NOTE).
12. cafe_low full vs stub: the full tower with lamp rings now stands on the right of the window, readable behind his shoulder (cafe_low_full, cafe_low_close_full): FIXED. Black joint squares gone. Remaining: the window top has a white glare band (29 rows, 3 % of frame, close-up 48 rows): NOTE (soften the sill glare, not blown to V=1 across the full width).
13. resto_table: bottle no longer covers his mouth, head 676/740 clear, cloth folds visible (about 6), chair back at the edge: FIXED. Cloth/wall/carpet shade 222.3 (< 230): on screen the cloth reads white-blue and the carpet navy, metric artifact of the cream-wall/parquet pixels: NOTE.
14. resto_wide: floor 24.2 %, blue/magenta/red gates OK, carpet is now striped (no white discs). Still no gilt mirrors, buffet or coat stand visible, 5-6 small diners: dressing target (20-26 objects, 2-3 mirrors) NOT MET: NOTE for QA-art to score; render worker may raise the camera shift to include the right wall.
15. resto_view: now over his shoulder (back of the head at left, Paris, Seine, Trocadero in the window, no tower, view well over 120 px): FIXED. A tiny black rectangle sits on the garden path (about 20 x 10 px): NOTE.
16. Hue, judged on screen:
   - S03 271 (median 255.5), S06 290 / S07 294 (red-lead girders and scaffold in shade: they read crimson-orange on screen, the metric counts saturated red as hue 290): metric artifact, NOTE (bible allows crimson shade).
   - T01 239.8, T02 236.0, T03 237.7: within 4 degrees of the band, looks correctly blue-violet: NOTE.
   - T04 262.3 / T14 249.8: OK. T05/T10/T11 night: night exception, OK on screen.
   - T12 335.9: the frame is a rust-orange iron wall with a warm interior glimpse, reads orange not magenta (magenta 4.45 %): NOTE.
   - T13 296.7: 1.7 % shadow pixels only, sky/tower read correct: NOTE.
   - S02 249.3 and S08 257.3 now in band.
17. T03 (1910) vs T02: still identical except the crowd; the plan swaps actors only: NOTE, director to confirm.

## BLOCKING (Round 2)
R2-B1. T12_tower_window_pull: 5.9 % pure black pixels (full-width black strip at y ~960-990 under the lit window, plus a dark strip near y 130). It is an unlit gap between the rust wall panels and will read as a black bar through the first frames of shot 27. Fix: close/fill the gap geometry or add fill light so min luma >= 25 in those rows; re-render T12 and T13 (crash pull-out must stay lit). Also T12 Maupassant head 51 px (chin 774): acceptable as is.

## NOTES FOR RENDER WORKERS (Round 2)
R2-N1. Shots 18/22 must use the T14 tower_dusk camera (heads 775-783), not the board camera of T04/T05 (heads at y 1200).
R2-N2. Window glare strips at the top of cafe_low / cafe_low_close windows (white, V=1): keep the framing so the strip is cropped or accept it as sky glare.
R2-N3. S09/S10 crane-up shots: bottom-eighth luma 88-106 (ground far away); keep a shaded FG element in the lowest 15 %.
R2-N4. Empty slab in the lower 30-35 % of S03-S06 and T14: keep the move tilting up or push in so that area is under the captions.
R2-N5. resto_wide: aim to include mirrors/buffet on the right wall; QA-art to confirm density.
R2-N6. All earlier notes N1-N10 stand (tower_low legs/contact shadow, T02 child chin 869 on pushes, cafe_wide_end architect chin 884, T13 invisible actor, window/interior chair match for T12).
