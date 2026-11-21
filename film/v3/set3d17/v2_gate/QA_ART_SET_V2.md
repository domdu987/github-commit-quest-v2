# QA-art: SET gate, film 17 v2 "ไอ้ช่างวัดหู" (client-delegated)

Reviewer: QA-art (opus), 2026-11-20. Rules: `film/QA_TEAM.md` §G, §H, §I on `origin/claude/new-session-73ou27`.

**What I looked at:**
- `contact_v2.jpg` (24 stills), every still at 360x640, the 6 `full720_*.jpg`, `stats.md`, API.md §v2 and PLAN_V2 §2-§6.
- The reference sheets R3, R4, R5 and R6, plus a 1-frame-per-8-s strip of film 2 (`sky_poker_v3.mp4`).
- I also ran the take paths in `prefecture17.py` (`path_take`, `anchor_frac`, `cast_pos`) at every frame. This found camera speed peaks and cast anchors that come too close to the lens. The numbers below come from that run, not from guesses.

The placeholder look of the cards is ignored. Their **positions** are judged, because the real cast17 puppets will stand on the same anchors.

## Verdict: **FIX-FIRST**

The world is a real step up from v1, and the colour targets are met. Cobalt and amber with red accents reads at once as a signature. The measuring room and the archive hall are dense and layered, and the signs work. Both BIGZOOMs pass on numbers.

Rendering should still not start yet, for three reasons:
1. Several cast anchors sit on the camera line, so the real puppets would fill or slice the frame. The worst case is BIGZOOM 2's end frame, the most important frame of the film.
2. Two paths jump or pass through cards.
3. The hook frame of BIGZOOM 1 is not yet "rich and detailed" (§H.3). It is flat cobalt slabs over an amber void, with no sky.

All fixes are anchor, camera-key or set-dressing changes, each well under a day. Re-gate only the stills listed at the end.

## Scores (1-10)

| item | score | one-line reason |
|---|---|---|
| Set density and richness (§H.3) | **7** | Interiors 8-9: the measuring room has chart, clock, toise, tripod, rug, gasoliers and books, and the archive has a 2-storey drawer canyon, gallery, banners and runner. Street 6: big empty puddle and setts. Night archive vault 5: a black void. Rooftop BIGZOOM start 4: flat untextured slabs. **"Rich and detailed?" = YES for the interiors, NO for the T1 hook frame.** |
| Lighting: motivated key, rim, warm/cool split (§I.2) | **6** | Warm/cool split is in every frame (amber practicals against cobalt), the window and lamp keys are motivated, and the cards carry a rim. Missing: no visible light shafts in the archive (T4 g1051, T6 g1377, T7 g1874), though the plan and R3/R6 rely on them. The night vault is crushed to flat navy. The T2 g0330 transom is blown. The light is mostly ambient-flat, with little falloff. |
| Signature colour (§I.3) | **8** | Préfecture cobalt and gaslight amber with kepi red reads clearly. Sat 0.642 and vivid 82 % pass easily. But it is hotter than every reference: vivid 82 % against R5's 75 % and R2/R4's 54-55 %. Do NOT push the grade further. |
| Readable signs (§I.4) | **7** | PETIT, GRAND, ARCHIVES, 11 MESURES, PRÉFECTURE DE POLICE, MARTIN and GRAND 2761-2820 are sharp on the phone sheet. SERVICE D'IDENTIFICATION is about 10 px cap height at 360 px and is clipped by the frame edge in T3 g0750 and full720_corridor. PETIT reads upside-down in the T7 top-down. |
| Camera: wide/medium, BIGZOOMs, ≥ 4 angle types (§G.3, §H) | **6** | All 7 angle types appear: HI (T5 g1039), TD (T3 g0645, T7 g1874), LO (T7 g1689), OTS (T2 g0657, T8 g1957), FG (T6 g1377), TRK and CR. The `report` BIGZOOMs pass: 1.2 → 36.4 %H and 4.4 → 48 %H. But the path checks find a teleport, three pass-throughs, a whip and an occluded BIGZOOM end (see B1-B3). |
| Floating / placeholder-too-close risk (§G.2-3) | **4** | Contact shadows are there and nobody hangs in the sky. Anchors above 75 %H appear in 7 of 8 takes, outside planned OTS shoulders, up to 240 %H (T6 inspector). `stage_cast` v2 does not exist yet (yaw clamp, walk_path, step decals; API §v2.9). The night-archive gasolier globes hang in a black void. |
| Same channel as the references | **6** | The palette, signs, push-through doors and drawer canyon are very much R2/R3/R5/R6. It is less like the channel in two ways. First, almost no frame shows sky or a horizon, while R5, R6, R7 and film 2 always give the aerials a sky gradient. Second, big surfaces such as roofs, ceilings and cobalt walls are flat fills, where the references have soft gradients and texture. |

## Blocking problems and fixes (priority order)

### B1. T6: the inspector card covers BIGZOOM 2's end, P1 and the OTS (g 1509-1701)
- **Problem:** the inspector anchor `(15.75, hy-1.0)` stands on the line from the camera to Bertillon. It measures 240 %H at its peak, 1.4 m from the lens, and is in frame on 50 % of the frames from g1509 to g1694.
- **Effect:** the big blue slab with the red kepi band in T6 g1515 and g1536 is him. The BIGZOOM end, "medium two-shot 45 %H on Bertillon", becomes a wall of uniform.
- **Fix:** move the T6 inspector to **(15.2, hy-1.9) = (15.2, 24.35, FZ)**.
  - Measured: at most 55 %H from g1509 to g1694, and still in frame for the whole three-shot (g1640-1671).
  - Re-aim the P2 key (g1695/1701 look) at the new head position.
  - T5's end anchor (g1274) must land on the same spot, so T5 and T6 still match across the cut.
- **P1 framing:** T6 g1536 shows the MARTIN card at only about 25 % of frame width, off-centre at the upper right. The keys g1530-1545 look at (14.29, 26.14, 2.86), which is not where the lifted card actually is.
  - Read the card's world position at g1530-1545 after `set_card_lift`.
  - Aim the camera at the card's centre and fill ≥ 60 % of the frame width, so "ตรงกันทุกช่อง" reads on a phone.

### B2. Pass-throughs, a teleport and a whip inside takes

| take | g | problem | fix |
|---|---|---|---|
| T3 | 792 → 800 | Two `hold` keys 6.8 m apart in 8 frames: peak 37 m/s, eye-level wide to under the table. On screen it is a jump cut that is not on the cut list. | Delete the hold on 792. Put the low key at g812, so the move takes ≥ 20 frames, via `ML(0.6, -1.6, 1.0)`. Or make 3c a planned cut at g792 and add it to `qa_auto --cuts`: 8 cuts is still inside 4-10. |
| T3 | 817-825 | The camera rises through the **prankster** card (342 %H). | After pinning the sign (g725), walk the prankster to `ML(-0.6, 3.3)` by g790. |
| T1 | 174-182 | The crane-out passes through **prisoner_b** (233 %H) and Bertillon (83 %H). Peak camera speed is 44 m/s at g200. | Raise key g168 to z `FZ+1.7` (`ML(-0.7, 0.45, 2.9)`) so it clears the seated heads. Spread the crane: key 186 → g182, and allow 6 frames of motion blur (shutter 0.5) on T1 g175-215. |
| T5 | 1196-1228 | The escort walks past the held camera at (15.9, 13.4): Dupont 0.3 m off the lens (103 %H), gendarmes 76-85 %H. | Move the escort lane to x 17.3 for g1196-1274, or move key 1196 to (14.6, 13.4, 2.5). |
| T5 | 1111 → 1125 | A 180° swing in 14 frames (17 m/s) reads as a whip-pan, which §I.1 allows only where travel is impossible. | Start the swing at g1100 (no hold on 1111) and land by g1127, before the lip-sync at g1128. |
| T7 | 1689-1751 | The inspector, 1.0 m from the lens at 95 %H, is the blue slab cut in half by the right edge in g1689 and g1781 (§G.3: no one cut in half). | Use the T6 fix position (15.2, 24.35). If it is still > 60 %H, move it to (15.5, 27.4), behind Dupont. Re-run the check. |

### B3. T1 BIGZOOM 1 start is not rich and has no sky (g 0-40, hook, key shot)
Evidence: `full720_roofs_bigzoom.jpg` and T1 g0000.
- **Problems:**
  - About 40 % of the frame is flat, untextured cobalt roof slab.
  - Amber void shows at the right and bottom edges, between the blocks.
  - No sky or horizon, so the Seine and Notre-Dame are out of frame.
  - The target window is not the brightest pool.
- **Fixes:**
  1. Lower the start key from (-30, 2, 46) to about (-34, -6, 34). Raise the look point so the horizon sits in the top 15-20 %: dome gradient (zenith `#1A3FB8`), a thin amber horizon, the Notre-Dame silhouette and the Seine reflections. Re-run `report T1`: the start must stay < 5 %H.
  2. Give the near roofs (the 30 blocks inside 60 m) zinc seam texture, mansard slopes, dormers and a lit window or two. They are flat boxes now.
  3. Fill the amber void: street canyons with setts colour and lamp dots, or extend the block field. No bare ground plane may show.
  4. Make the measuring-room French window the single brightest amber pool (window key ×1.5, with geraniums and a red awning nearby), so the blind viewer finds Bertillon by 2.2 s.

### B4. Empty floors and lower halves (§H.3 "no empty flat ground planes")
Each of these frames has ≥ 40 % bare floor in its lower half:

| frame | add |
|---|---|
| T1 g0105 / g0170 (inside the window) | ledger stack, kepi on the floor, spittoon, the open calipers case, a dropped card (1-2 m fg) |
| T2 g0493 (low drift into the room) | rug edge, crate, umbrella stand, or tilt the drift up 5° |
| T4 g1051 (archive entry) | a card trolley plus an overflow pile in the lower third |
| full720_corridor (T2 g400) | the plan's fg layer: bench end, photo pile, runner |
| full720_street (T1 g287) | the planned flower cart or barrels as fg, the horse, the crowd cards; shrink the giant puddle or break it with setts |

### B5. Light fixes
- **Archive day shafts:** none are visible in T4 g1051, T6 g1377 or T7 g1874. Raise `beam_k` and the dust in `ARCHIVE_DAY` until at least 2 skylight shafts read on the phone sheet (R6/R3). It also helps the T6 BIGZOOM depth.
- **Night archive vault** (T5 g1039, full720_archive_night): the upper half is flat black-navy, and the gasolier globes float in it. Light the vault ribs with the moon skylight shafts (cool), and lift the vault ambient to read as cobalt, not void.
- **T2 g0330 (luma 130):** the transom/fanlight above the main door is blown to white across the top of the frame. Cut `glow_door` emission there by about 50 %, or tilt the start key down.
- **T6 take luma 121** (target 85-110): lower `ARCHIVE_DAY` strip fills and AMB_K for T6 only, by about 12 %. Watch g1377 (133) and g1536 (128).
- **T7 luma 84:** lift by about 5 %.

### B6. Prerequisite before T5/T6/T8 render: `stage_cast` v2
API §v2.9 says the yaw clamp, `walk_path` with foot-lock and step contact decals are not built. T5 (arcs), T6 (OTS and three-shot drift), T8 (OTS arc) and T2 (thief climbing the steps) depend on them for §G.2. Teams for T1, T3, T4 and T7 may start once B1-B5 pass. T2, T5, T6 and T8 need `stage_cast` v2 merged first.

## Non-blocking notes for the render teams
- **Clock push (T3 g828 → T4 g902):** the clock fills > 50 % of the frame for about 1.3 s, which is fine as a push-through (R3 does the same). Do not let it grow. Drop the `hold` on T4 g902 so the pull-out keeps moving.
- **PETIT upside-down** in the T7 top-down (g1874): make the banner double-sided, or give it a second face toward the north.
- **SERVICE D'IDENTIFICATION:** enlarge the cap height to ≥ 0.3 m, or shorten the corridor-side sign to "IDENTIFICATION". Keep it fully in frame in T2 g445-493 and T3 g725-760.
- **PRÉFECTURE DE POLICE** must be whole in the T1 crane-up (g200-230), not clipped as in full720_street.
- **Colour:** keep `grade2` as is. Vivid 82 % is already above every reference, so do not add sat. If a take tests above 0.70 sat, take 0.05 off rather than adding haze.
- **OTS shoulders** (T2 g560-611 Bertillon 140 %H, T8 g1996-2006 gendarme 113 %H, g2031-2041 Bertillon 119 %H) are planned. They must be back-view puppets or dark coat silhouettes, and the head must not be cut by the top edge.
- **Top-down cutaways** (T3 g0645, T8 g1862): the gasolier arms and wall brackets read as scattered debris from above. Hide the gasolier nearest the lens for those frames.
- **QA at the TAKE gate:** run the same anchor check on every take: no anchor > 75 %H outside the planned OTS frames and P1-P3, and camera speed ≤ 15 m/s except during BIGZOOM/crane frames with blur.

## Re-gate (small)
Re-render only these stills at 360x640, 16 samples:
- T1 g0000, g0105, g0170, g0180
- T2 g0330, g0493
- T3 g0796, g0820
- T4 g1051
- T5 g1039, g1215
- T6 g1515, g1536
- T7 g1689

Also send:
- full720_roofs_bigzoom and full720_archive_night
- the per-frame anchor table (zero hits > 75 %H outside planned OTS/P1-P3)
- `report T1 T6` (BIGZOOM still PASS)

If those are clean, QA-art approves without a full re-sheet.
