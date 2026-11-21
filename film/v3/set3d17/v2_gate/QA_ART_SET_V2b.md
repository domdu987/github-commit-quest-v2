# QA-art: SET gate re-check v2b, film 17 v2 "ไอ้ช่างวัดหู" (client-delegated)

Reviewer: QA-art (opus), 2026-11-20. This answers the set team's v2b (commits 917900e, 007c300), which responds to `QA_ART_SET_V2.md` B1-B6.

**What I looked at:**
- `contact_v2b.jpg` (18 stills) and every `*b.jpg` at 360x640
- `full720_roofs_bigzoom_v2b.jpg`, `full720_archive_night_v2b.jpg` and `AB_archive_night_16_vs_32.jpg`
- `stats_v2b.md`, `anchors_v2b.md` and API.md §v2.10

I also re-ran the paths myself:
- **Frame sizes:** `path_take`, `anchor_frac` and `cast_pos` at every frame. These confirm the set team's table.
- **Card facing (new):** for every frame of every take, I compared each card's story facing from `cast_face()`, the facing `stage_cast2` will clamp to, against the direction of the camera.

## Verdict: **FIX-FIRST, one item (B7: card facings).**

Everything I asked for in B1-B6 is fixed, and the set itself, its light and its paths are **approved**. Once B7 passes its check, rendering may start with the render notes below, and no further QA-art sheet is needed. B7 is a data table plus a check, which should take a few hours.

**Why B7 blocks:**
- No anchor in `TAKES` has an explicit `face`. So `cast_face()` falls back to one of two directions: where the card is walking, or toward the **take's first camera**.
- With the travelling paths, that turns the main characters' backs, or their edges at the ±35° clamp, to the camera on key beats. Neither the placeholder check nor `check_take` measures this.
- You can already see it on the sheet. In T1 g0105b, the BIGZOOM 1 end, Bertillon and the bench prisoners are thin edge-on slivers with nothing readable at 36 %H. In T3 g0796b, Bertillon is a sliver too.
- With the real cast17 cards, `stage_cast2` would show a mirrored pose with a dark back-of-head disc. That would put it on the inspector's lip-sync, the reveal and the P2 jaw-drop.

Measured: frames in which a card is in frame at more than 15 %H, is not on `BACK_VIEW`, and its story facing is more than 110° away from the camera (back view) or more than 60° away (edge-on):

| take | anchor | frames > 60° (of in-frame) | of which > 110° (back) | where | beat it breaks |
|---|---|---|---|---|---|
| T1 | bertillon | 62 / 91 | 55 | g100-161 | **BIGZOOM 1 end + 1b side track (hook, key shot)** |
| T1 | prisoner_a / _b / _q | 41-63 | 40-60 | g100-162 | the ear-clamping row in the hook |
| T1 | prisoner_c | 58 / 70 | 58 | g273-330 | the smirk and calling card on the steps (1d-1e) |
| T2 | inspector | 116 / 198 | 87 | g482-657 | **the laugh and lip-sync 2c-2e** |
| T2 | thief | 130 / 130 | 130 | g330-459 | 2a behind him is fine. In 2b he must turn to find his photo and put on the moustache |
| T2 | gend_room, prisoner_b | 106-148 | 32-117 | g472-657 | room reaction |
| T3 | bertillon, prisoner_chair | 33-34 | 19-34 | g779-823 | 3c low angle: pince-nez and calipers |
| T4 | bertillon | 155 / 172 | 80 | g872-1051 | measuring montage, writing the card |
| T4 | prisoner_s | 124 / 124 | 0 | g870-993 | the measured prisoner, edge-on throughout |
| T5 | inspector | 129 / 187 | 54 | g1190-1318 | the end of the lip-sync (to g1196), then the smirk |
| T5 | bertillon, dupont | 101-106 | 17-30 | g1256-1383 | three-shot, Dupont's innocent shrug |
| T6 | bertillon | 138 / 175 | 122 | g1524-1684 | **reveal: card turn on "มาร์แตง", three-shot** |
| T6 | inspector | 130 / 151 | 130 | g1572-1701 | **P2 jaw-drop push (g1671-1695)** |
| T8 | bertillon | 111 / 139 | 0 | g1931-2041 | the ending: calipers on the ear (edge-on) |
| T8 | crowd2, gend_a | 21-59 | 21-49 | g1920-1978 | grinning crowd |
T7 is clean.

### B7 fix (set team, once, centrally, before any team renders)
1. **Add an explicit `face` to every anchor in `TAKES`.**
   - Use per-segment keys `(g, deg)`, not one value per take.
   - Point each at the camera position in the middle of the beat where the character must read, adjusted for the story's eye-line.
   - T1 example: Bertillon and the bench prisoners face **+x (0°), into the room**. The BIGZOOM 1 start sees Bertillon from behind through the window at 1.6 %H, which is fine and is how the plan describes it, and the end and the track see him from the front.
   - Walkers keep their walking direction only while moving faster than 0.3 m/s. When they stop, they turn to their story `face`.
2. **Add `check_face(take)` to `check_take`.** It should fail when:
   - a card in frame at more than 15 %H, and not on `BACK_VIEW`, is more than 60° off the camera
   - on lip-sync windows (g493-651, g1128-1196), BIGZOOM ends (g90-148, g1500-1530), P1-P3, and 6c "MARTIN" (g1545-1616), the speaker or hero is more than 35° off the camera, i.e. past the card clamp
3. **Re-send:** the `check_face` table for T1-T8, plus a **full-res 720x1280 still with the real cast17 cards through `stage_cast2`** at T1 g105, T2 g560, T6 g1600 and T6 g1690.
   - That means the ends of BIGZOOM 1 and 2 and P2 are seen with real art, and `stage_cast2` is proven on real cards. That is the other open item.
   - If the table is clean and the 4 stills read (front-facing faces, feet on the floor, no thin card), the director may start the teams. QA-art checks those 4 stills only.

## B1-B6 re-check: all fixed

| item | result | evidence |
|---|---|---|
| B1 T6 inspector / P1 | **fixed** | My own re-run puts no unplanned anchor above 75 %H anywhere. T6 g1515b is a clean medium two-shot (Bertillon and Dupont), with the inspector small at the right. In T6 g1536b the MARTIN card fills about 74 % of the frame width and reads on the phone. |
| B2 jumps and pass-throughs | **fixed** | T3 has no teleport (g792→812 at ≤ 5.7 m/s). The T1, T3 and T5 pass-throughs are gone. There is no T5 whip. T7 ends on a high bird's-eye with the banners upright. Speeds above 6 m/s occur only on the planned cranes (≤ 15.5 m/s). |
| B3 T1 hook frame | **fixed** | T1 g0000b and full720_roofs_v2b: cobalt-to-amber sunset sky, Notre-Dame with lit windows, seamed zinc roofs with dormers and smoke, lit windows, no amber void. Now as good as the R5/R6 aerials and film 2's towers. |
| B4 empty floors | **fixed** | Calipers case, kepi, cards and spittoon (T1 g0105b), crates and stools (T2 g0493b), trolley and pile (T4 g1051b), runner (T5 g1215b), refuge island and lamp (T1 g0180b). |
| B5 light | **fixed** | Skylight shafts read (T5 g1039b, T6 g1377b, T4 g1051b). The night archive is a violet/moon-blue R4-style night, no longer a void. No white transom in T2 g0330b. The T6 BIGZOOM start falls from 133 to 121. |
| B6 stage_cast2 | **built, not proven** | `floor_z`, yaw clamp, `walk_path` and `BACK_VIEW` with back covers are all in. Facing data is missing (B7), and nothing has run with real cards yet (B7.3). |

## Scores now (1-10)

| item | v2 | v2b |
|---|---|---|
| Set density and richness (§H.3), **"rich and detailed?" = YES** | 7 | **8** |
| Lighting: motivated key, rim, warm/cool split (§I.2) | 6 | **8** |
| Signature colour (§I.3): sat 0.628, vivid 75.8 %, now matching R5 rather than overshooting | 8 | **9** |
| Readable signs (§I.4) | 7 | **8** |
| Camera: wide/medium, BIGZOOMs 1.6→36.4 and 4.4→48 %H, 7 angle types (§G.3, §H) | 6 | **8** |
| Floating / too close to the lens (§G.2-3) | 4 | **8** (0 unplanned > 75 %H; one 0.98 m wall-side gendarme in T2) |
| Card facing / readability of the cast (§I.5, §G.2), new check | - | **3** until B7 |
| Same channel as the references | 6 | **8** (sky, signs, shafts, push-throughs: reads as R3/R5/R6) |

## The set team's open items: all are render notes or TAKE-gate checks, none blocks the SET

| open item | ruling |
|---|---|
| T1 luma 120 (bright window interiors) | TAKE gate. Target in the notes below. |
| T6 luma 121 (P1 white card) | TAKE gate. Accepted for the 1 s P1. The rest of T6 must meet its target. |
| T1 g218 sign not whole | Render-team rule (T1 notes). |
| Cranes up to 15.5 m/s | Accepted with motion blur at shutter 0.5 on those ranges only. |
| Gasolier crossing the room sign at T3 g796 | Accepted: the sign is whole in g736-760. Note only. |
| `stage_cast2` not run with real cards | Becomes **B7.3** (4 real-cast stills), then the per-take still below. |
| 16 samples | **Approved** (A/B: identical numbers, no visible noise). Temporal check at the TAKE gate (see notes). |

## Render-team notes (apply once B7 has passed)

### All takes
- **Samples:** `setup_render2((720, 1280), samples=16, threads=2)` + OIDN, adaptive 0.03. Do not raise saturation in `grade2`.
- **Shutter:**
  - Motion blur on, shutter **0.5**, only on T1 g152-278 and T7 g1800-1867.
  - Optionally the 6.1 m/s moments: T4 g1035-1038 and T5 g1141-1150.
  - Everything else renders sharp (shutter off), so qa_auto's blur check is not tripped.
- **Cast:**
  - Use the real cast17 cards only, via **`stage_cast2(take, g, assign)` on every frame**, with the B7 `face` keys.
  - Never use `bertillon.stage_cast` or placeholders.
  - The cards' feet stand on `floor_z`, with contact shadows.
- **Pre-render check, every team:**
  - Before the full render, render **one full-res 720x1280 still per take**, with the real cards, at the take's key frame (table below).
  - Run `check_take(take)` and `check_face(take)`.
  - Commit the still and both outputs, and wait for the director's OK. QA-art at the TAKE gate will ask for them.
- **Temporal noise:** after the first 30 frames, look at them as a clip, specifically for OIDN shimmer on flat walls at 16 samples. T5 night and the T1 roofs are the weak spots. If it shimmers, use 24 samples for that take only.
- **Luma:** check qa_stats2 per take on the first 30 frames. Targets are below. Fix by light only (a preset or `TAKE_OVER`), never by haze or lowering saturation.

### Per take

| take | key-frame still (real cast) | luma target (take mean) | notes |
|---|---|---|---|
| T1 | g105 (BIGZOOM 1 end) | 95-112 | The g100-200 interior currently runs 127-133. Lower the T1 window key (300 W) to about 220 W for g96-200 only, and keep it at 300 W for g0-95, so the French window stays the brightest pool in the BIGZOOM start. **Façade sign rule:** the whole band PRÉFECTURE DE POLICE must be in frame and readable (≥ 28 px cap height at 720x1280) for **at least 20 consecutive frames** between g200 and g300. Today's crane top at g218 does not show it whole. Re-aim the g218 look-at up and toward the band, or hold the band whole through the swoop (g227-287). Motion blur g152-278. Keep the BIGZOOM 1 report PASS (start < 5 %H, end 35-60 %H). |
| T2 | g560 (inspector lip-sync, OTS) | 95-110 | The g330 start runs 125: drop the door lanterns and fanlight by another 20 % for g330-360. The T2 corridor gendarme passes 0.98 m from the lens at g403-451: his head must not be cut by the left edge for more than 10 frames. Lip-sync only inside 16.32-21.59 s. The thief's back view applies only in 2a (g336-386). |
| T3 | g800 (3c low angle) | 95-110 | The gasolier crosses the room sign at g796 (accepted). In the low move g792-812, the dark foreground block (right side in g0796b) may cover at most 30 % of the frame for at most 8 frames. Clock push g828-856 is ≤ 1 s full-frame. |
| T4 | g930 (station track) | 95-110 | Match the clock face and its screen position with T3 g856. Drop the `hold` on g902 so the pull-out keeps moving. |
| T5 | g1150 (lip-sync OTS) | 90-108 | Night → day `set_light_mix` g1196-1211. Lip-sync 37.48-39.74 s. The escort lanes are fixed (x 15.9/16.6/17.3). Do not move them. |
| T6 | g1515 (BIGZOOM 2 end) | 95-112, excluding P1 g1515-1545 | P1 may run brighter (white card). If the take mean is still above 112, tone the card paper from near-white to cream (about `#F2E6C8`). Keep the BIGZOOM 2 report PASS. P2 g1671-1695: the inspector's face front-on (B7), at most 35 % of the frame height for his face. |
| T7 | g1730 (low hero) | 88-105 | Currently 88, at the lower bound: lift `TAKE_OVER` shade a further 5 % if the first 30 frames are below 88. Motion blur g1800-1867. |
| T8 | g2018 (OTS behind the crowd) | 95-110 | P3 g2018-2052 is about 1.1 s, with the face at most 35 % except for the punch-in. The crowd faces the chair (B7). The OTS gendarme back view g1958-2052 must not cut the head by the top edge. |

## TAKE-gate items QA-art will check (carried forward)
- 0.5 s phone tiles for grounding (feet on `floor_z`, contact shadow) and for no thin or edge-on cards.
- Sign readability:
  - IDENTIFICATION, whole in T2 g445-458
  - SERVICE D'IDENTIFICATION, whole in T3 g736-760
  - PRÉFECTURE DE POLICE, per the T1 rule
  - MARTIN at P1
  - PETIT / MOYEN / GRAND
- BIGZOOM timecodes: T1 g0-105, T6 g1377-1515.
- Cut list: 336, 651, 850, 1045, 1377, 1695, 1868.
