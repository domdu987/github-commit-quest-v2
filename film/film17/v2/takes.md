# Film 17 v2: take sheet for the render teams

Source: PLAN_V2.md §4/§5, `film/v3/set3d17/prefecture17.py` (`TAKES`, `path_T1()`..`path_T8()`), QA_ART_SET_V2b.md render notes.
Recipe and checks: `film/v3/set3d17/API.md` §v2 ("v2 render recipe").

**Frame rule:** g = round((t + 0.10) × 30), where t is narration time. The Blender frame is g + 1. End frame g 2052 = 68.40 s, a hard cut on "ตัวเอง".

**Hard cuts (8):** g 336, 651, 850, 1045, 1377, 1675, 1695, 1868. Run `qa_auto.py --cuts 336,651,850,1045,1377,1675,1695,1868 --first_g 0`. (g1675 was added 2026-11-20 17:45. It replaces the 6d→P2 whip, which swept cast across the frame edges.)

**Quote windows (lip-sync only here, ±0.15 s):**
- 16.32-21.59 s = g 493-651: the inspector, T2.
- 37.48-39.74 s = g 1128-1196: the inspector, T5.
- The laugh at 15.46-16.32 s (g 467-493) has no lip-sync.
- Every other mouth stays closed (cast17 story poses), except the planned held shapes: the laugh, and the P2 jaw-drop `inspector_shocked`.

**BIGZOOMs:**
- BIGZOOM 1: T1 g 0-105, Bertillon 1.6 → 36.4 %H.
- BIGZOOM 2: T6 g 1377-1515, Bertillon 4.4 → 48.0 %H.
- `python3 prefecture17.py report T1 T6` must print PASS.

**Punctuation pushes:**
- P1: T6 g 1515-1545, the MARTIN card at about 74 % of the frame width.
- P2: T6 g 1675-1695 (hard cut in at 1675), the inspector's jaw-drop, front-on. 6d holds through g1674.
- P3: T8 g 2018-2052, calipers on the inspector's ear and his red face.

**Every team:** 16 samples + OIDN at 720x1280, 2 threads, adaptive 0.03 (`setup_render2`).

| take | segments | g core | render range (handles) | frames | locations / light | cuts at | quote / lip-sync | BIGZOOM / P-shots | key still (real cast) | luma target | motion blur 0.5 | est. render at 16 samples |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| T1 hook + Paris | 1a-1e | 0-336 | 0-342 | 343 | roofs + street + façade (BLUE_HOUR_EXT), measuring room (SUNSET_INT) | out at 336 | none | BIGZOOM 1 g0-105 | g105 | 95-112 | g152-278 | ~460 min |
| T2 corridor + mockery | 2a-2e | 336-651 | 330-657 | 328 | street, façade, corridor (GASLIGHT_INT), measuring room | in 336, out 651 | g493-651 (inspector), laugh g467-493 | - | g560 | 95-110 | none | ~465 min |
| T3 nickname + prefect | 3a-3c | 651-850 | 645-856 | 212 | measuring room (cutaway while the camera is above the ceiling) | in 651, out 850 | none | - | g800 | 95-110 | none | ~265 min |
| T4 montage + drawers | 4a-4d | 850-1045 | 844-1051 | 208 | measuring room, ARCHIVES (ARCHIVE_DAY) | in 850 (clock match), out 1045 | none | - | g930 | 95-110 | optional g1035-1038 | ~245 min |
| T5 false payoff + crisis | 5a-5e | 1045-1377 | 1039-1383 | 345 | ARCHIVES night → day (`set_light_mix` g1196-1211) | in 1045, out 1377 | g1128-1196 (inspector) | - | g1150 | 90-108 | optional g1141-1150 | ~490 min |
| T6 reveal | 6a-6e | 1377-1695 | 1371-1701 | 331 | ARCHIVES day (T6 overrides) | in 1377, out 1695 | none ("มาร์แตง" 53.25 s = g1601: card turn) | BIGZOOM 2 g1377-1515, P1 g1515-1545, P2 g1671-1695 | g1515 | 95-112 (P1 excluded) | none | ~360 min |
| T7 aha + 200 | 7a-7b | 1695-1868 | 1689-1874 | 186 | ARCHIVES day (vault cut away on the crane top) | in 1695, out 1868 | none | - | g1730 | 88-105 | g1800-1867 | ~185 min |
| T8 ending | 8a-8c | 1868-2052 | 1862-2052 | 191 | measuring room (cutaway on the bird's-eye start) | in 1868, end 2052 | none | P3 g2018-2052 | g2018 | 95-110 | none | ~240 min |
| **total** | | 2052 | | **2144** | | 7 | | | | | | **~2,700 min ≈ 45 CPU-h (2-thread)** |

**How the render estimate is built** (rough):
- World alone at 16 samples, 720x1280, 2 threads, measured:
  - rooftops 36 s
  - street about 58 s
  - corridor 62 s
  - measuring room about 42 s
  - archive by day about 28 s
  - archive at night 73 s
- The real cast17 sprites add about 30-40 s per frame for 4-6 cards: the 4 real-cast stills took 50-87 s each in total.
- Per-take means used: T1 80, T2 85, T3 75, T4 70, T5 85, T6 65, T7 60, T8 75 s/frame.
- With 8 teams that is about 8 h wall time. Split T1, T2 and T5 at a mid frame to cut it to about 4-5 h.

**Before the full render, every team:**
1. Run `check_take(take)` and `check_face(take)` (both PASS today).
2. Render one full-res 720x1280 still with the real cards at the key frame above. It must be committed and get the director's OK.
3. After the first 30 frames:
   - Check qa_stats2 luma against the target. Fix it by light only (`TAKE_OVER` / preset), never by haze or by lowering saturation.
   - Check for OIDN shimmer on flat walls. If it shimmers, use 24 samples for that take.

**Per-take notes (QA-art):**
- **T1:**
  - Window key 300 W for g0-95, about 220 W for g96-200.
  - Façade-sign rule: PRÉFECTURE DE POLICE whole and readable (≥ 28 px cap height) for ≥ 20 consecutive frames between g200 and g300. The g218 crane top does not show it whole today, so re-aim that look-at or hold the band through the swoop.
- **T2:**
  - Drop the door lanterns and the fanlight by 20 % for g330-360.
  - The corridor gendarme passes 0.98 m from the lens at g403-451; his head must not be cut by the left edge for more than 10 frames.
  - The thief is seen from behind only in 2a (g330-386).
  - 2e is a 22 → 28 mm push-in that continues the OTS.
- **T3:**
  - The gasolier crossing the room sign at g796 is accepted.
  - The dark foreground block in g792-812 may cover at most 30 % of the frame for at most 8 frames.
  - The clock push g828-856 lasts ≤ 1 s.
- **T4:** match the clock face and its screen position with T3 g856.
- **T5:** do not move the escort lanes (x 15.9 / 16.6 / 17.3).
- **T6:** if the take mean is above 112, tone the card paper to cream (#F2E6C8). The P2 face may fill at most 35 % of the frame height.
- **T7:** if the first 30 frames are below 88, add +5 % to the `TAKE_OVER` shade.
- **T8:** P3 lasts about 1.1 s. The crowd faces the chair (face keys). The OTS gendarme's head must not be cut by the top edge.

## Luma trim at conform (director decision 2026-11-20 16:50)
- The binding metric is the RGB mean at 90x160, as in qa_stats2. Several parts measured on it run 5-9 above their target: T3b's ramp half, T5b and T5b2, and T6b's stills. This happened because the earlier reports used PIL L.
- These parts are NOT re-lit or re-rendered for luma. At conform each take gets an exposure trim, a pure RGB multiply k between 0.85 and 1.12 (T6 6c/6d down to 0.82: the bright floor measures 125-133). It can be keyed per frame as a smooth curve, eased over 10 frames or more, both at part joins and inside a take with uneven sections (T4: macro clock 116-127 vs the desk side 80-92). Above k = 1.0, check highlight clipping.
- The trim brings the take mean to its target. Multiplying by k leaves the qa_stats2 saturation and vivid values unchanged (checked on T6b g1600: sat 0.593 → 0.593, vivid 84.1 % → 84.1 %, luma 115.6 → 106.3 at k 0.92). It is not haze and it does not touch saturation.
- Teams keep rendering their approved setups unchanged. Re-renders are only for real defects: slabs, shafts, edge cuts, staging.

## ARCHIVES day skylight beam fx OFF (director decision 2026-11-20 19:05)
- The beam_fx volume puts a milky veil over the whole frame whenever the camera's view passes through the beams. Measured effect:
  - T5b2: beam on 114, beam off 90.
  - T6a: mean abs diff 4-7.5/255, saturation +0.03-0.06 with the beam off.
  - This is haze, which the client rules forbid.
- From now on, ARCHIVES day renders force the beam_fx Emission strength node to 0, or hide arch_beam_fx. Setting beam_k through TAKE_OVER alone does not always reach the node (T7).
- Per take:
  - T5: the beam fades out over g1211-1218 (T5b beam_scale, 6cdc298), then stays off.
  - T6a and T6a2: re-rendered beam-off.
  - T6b: no measurable contribution (0.56/255), so it stays as rendered.
  - T7: the crane frames g1800+ are tested and switched off if the diff is above 3/255.
