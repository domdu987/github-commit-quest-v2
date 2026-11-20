# QA-art review: film 21 shot plan v3 (camera travel), 2026-11-20

Reviewed: shot_plan.md (v3) against QA_TEAM.md §G/§H/§I, ref_shorts (README, R5 sheet, R3 transition detail), set3d21 contact.jpg + API.md. Plan only, no renders.

## Verdict: GO-WITH-CHANGES

The spine is right and reads as the reference channel: one connected valley, camera that flies instead of cutting (R5 crane-out/swoop, R3 follow, R7 ride-along), characters busy in every beat, three punctuation CUs, two BIGZOOMs, signs. The story reads with the sound off: hook (tiny Scots, bridge below), mocker (laughing Cressingham + CU1/CU2), mechanism (count E2, cork H2, jam I), ending (empty table, jump). The changes below are about physical sense in this set, render budget, and making the bottle image and the colour identity actually land.

## Checks
- **Cuts/whips:** 9 hard cuts + 3 whips = 12 discontinuities. Inside §I (<= 12 cuts, target 4-10) but whips are "only where travel is impossible"; G1 spends 2 of them on 1.75 s. After change 4: 8 cuts + 2 whips.
- **BIGZOOM (§H):** A passes (g 0-125, ~4.2 s, valley_wide 361 m up -> shelf). H2 does NOT pass as timed: the wide-to-character part (swoop at 47.50 -> medium at ~49.6) is about 2.1 s, under the 3 s minimum (change 3).
- **§G wides / floating:** majority wide/medium-wide, good. Risk points: H1 ride-along of running cards (feet/contact shadow at speed), J2 jumpers lifted 0.5-0.8 D (allowed only as a visible jump arc with motion, never a held hang), E2/H2 meadow troops at 229 m are placeholder dots (fine, but they must sit on the ground).
- **Missing tools:** `build_world`, `cam_path`, the text signs and the money-canopy lantern do NOT exist in stirling.py; API.md still says "no readable text" (change 1).
- **Render cost:** final frames are 70-175 s each on 4 cores. Segments of 100-175 frames are 3-8 h per team at 64 samples: over the 2-3 h budget (change 2).

## Changes (max 8)

1. **ALL / set, before any team starts.** Add to set3d21 and document in API.md: `build_world(presets)` (union build of two locations, built once per process), `cam_path(keys, eases)` (camera keys + VIVID-preset lerp), `sign(text, loc, rot, size)` (three signs placed: south bridge gate, chest front, camp road), a warm lantern point light under the canopy, and a rim-on default for cast cards. Delete "no readable text" from API.md. *Why:* every segment depends on these; 16 teams inventing their own path/sign code gives 16 looks and broken D6 joins.

2. **A, H2, B2, E1, H1 (render budget).** Render travel frames at 32 samples + OIDN (fast motion hides noise), keep 64 only for CU and held frames; split A and H2 each between two teams at a mid-path pose with a D6 join (A at g 80, H2 at the top of the crane, g ~1380). Every team renders a 10 fps draft of the whole path first (~10 min) for a director check before finals. *Why:* 160-175 frames x 105-140 s is 5-7 h per team; the brief is 2-3 h.

3. **H2 (BIGZOOM 2 timing + legibility).** Crane from P_NECK to the top in about 1.0 s (44.73-45.8), hold/drift 0.5 s, start the swoop at 46.3 so wide -> medium on Cressingham/Surrey takes >= 3.3 s, then CU3 at 49.73. Top pose: ~110-130 m up, pitched ~60 deg, framing ONLY the loop + neck + south bank strip (not the 229 m valley_loop frame: at that height a man is ~5 px and the 18 m spear wall ~60 px). Give the Scots wall saturated blue (saltire banners on poles) and the trapped English red/white, so the cork reads as a blue plug in a red bottle with the sound off. *Why:* §H 3-6 s rule; the mechanism is the whole film and must read on a phone.

4. **G1 + G2 (merge, -1 whip, -1 cut).** Drop G1 as its own segment. F whips (or cuts) to the Scots from BEHIND on the hill (hill_over pose, 32 mm): the calm column crossing two by two far below (the 280 px bridge is already in that preset), a knight yawning is replaced by the Scot chewing his grass stalk; then the camera arcs round and down to the hill_low hero angle as the horn is raised and blown (39.7-41.1). *Why:* G1 is 1.75 s costing two transitions and repeats E2's bridge_end_north view; the over-the-shoulder look at the trap from the Scots' side gives cause -> effect (they wait, THEN blow).

5. **A (end pose).** End the BIGZOOM on a pose UP-slope of the shelf looking SW over the Scots toward the bridge (hill_over family, camera ~ (150, 145, ground + 3) -> (131, 131, 15) and on to the bridge), not hill_eye. *Why:* hill_eye looks NE, away from the river: "the bridge still visible far below behind them" is impossible there. The valley_wide start is NE of the hill looking SW, so this end keeps one direction of travel (no 180 deg turn mid-swoop). Cards are billboards, so Wallace and the grass-chewer still face the lens.

6. **H1 (ride-along speed).** hill_over (160, 150, z ~47) to P_NECK (-2, 50, 4.6) is ~195 m in 3.5 s (~55 m/s): no running card can stay in front of that lens. Make it two legs: 0-1.2 s true ride-along behind 4-5 runners on the slope (5-7 m/s, gorse whipping past), then the camera OVERTAKES them and swoops ahead to the bridge mouth, where a second, pre-placed group of Scots slams the wall at 43.78. Runners always grounded with contact shadows. *Why:* physical sense + §G nothing floats (fast-slid cards look like they hover).

7. **E2 (do not pre-spend the reveal).** Cap the crane at ~35-45 m, angled back toward the hill so the Scots line and the filling meadow share the frame; do not reach the top-down loop view. *Why:* as written E2 and H2 both crane straight up from the bridge north end over the loop, 12 s apart; the repeat flattens the H2 reveal and breaks "no more than 2 shots at the same angle".

8. **ALL (signature colour, §I 3).** State it in the plan: **English crimson + gold** (Cressingham, caparisons, pavilions) against **Scots saltire blue** on a teal river; everything else (meadow, crag, sky) stays secondary. Add 2-3 blue saltire banners on the hill (A, B2, E1, G2, H1, H2) and keep the money canopy crimson/gold under the lantern (D1, J1). E1 flight camp -> hill (~265 m in ~2 s after the laughing beat) should use the same red-to-blue colour hand-off as the eye's guide. *Why:* the references own one bold colour each (R5 storm blue, R6 pink); the plan names none, and the contact sheet's dominant tones are sand/olive, which reads as "any valley".

## Minor (no change count)
- D2: Cressingham's mark in camp_bank is ~80 m west of the money table; the whip hides this, but keep his walk to a few metres along the bank, not "from the table".
- C: the two knights' horses fill the 2.6 m deck; keep the camera above rail height (no rail through a face, §G).
- J2: the "camera DROPS to water level" ends at river_low 0.55 m over water with splash crowns: good, keep crowns emission white (no grey).
