# Shot plan, film 17 (ไอ้ช่างวัดหู — Bertillon, Paris 1882-83)
Narration film/film17/audio/narration.wav (67.94 s), placed at +0.10 s. g = round(t*30) with t = film time. N = 2052 (68.40 s, hard cut on the last word "ตัวเอง").
Captions film/film17/script/captions.json (narration time; add 0.10 s for film time). Timing film/film17/audio/timing.json.
Set film/v3/set3d17 (bertillon.py + API.md; presets named below — use the closest preset in API.md if a name differs). Cast film/v3/cast17.

## Sentence starts (narration time)
| line | start (s) |
|---|---|
| hook | 0.00 |
| pivot | 4.71 |
| setup | 11.10 |
| boss | 14.72 |
| nickname | 21.61 |
| deadline | 24.08 |
| count | 28.25 |
| false | 34.74 |
| crisis | 39.76 |
| reveal | 44.65 |
| aha | 56.40 |
| ending | 62.19 |
| end | 67.94 |

## Quote windows (mouths move ONLY here, +-0.15 s)
- inspector: 16.32-21.59 ("วัดหูโจรเนี่ยนะ! ... วัดหูข้าเองเลย!") and 37.48-39.74 ("เหลืออีกอาทิตย์เดียวนะ ไอ้ช่างวัดหู!"). Laugh (no lip-sync, laughing pose + bounce) 15.46-16.32.
- No other character speaks (dupont's "never arrested" is narrated; he may shrug/shake head, mouth closed).

## Camera rules (production-lessons §10 + bible camera.md) — MANDATORY in every shot
- 22 mm, roll 0. Every shot has a clear eased move: drift push/pull 6-10 %/s with a 20-60 px/s lateral slide, or a snap (13-25 frames, x1.3-x3). Never more than 6 frames under 0.25 px/frame. No near-static hold > 1 s.
- Framing changes every 1.3-1.4 s on average (cuts + dissolves + snaps). Quick push-in on punch lines; a whip/snap on the reveal steps.
- Foreground prop 1-2 D from the lens in most shots (gas lamp, ledger stack, calipers, kepi on rack, drawer edge, cobble bollard).
- Transitions: 11-frame dissolve between locations/time jumps (marked D11); hard cut elsewhere (C).
- Heads: centre y 450-760, all heads above y 880. Laughing characters bounce ~0.06 D at ~3 Hz. Nobody frozen: idle sway/blink.
- Shot mix target: eye 35-40 %, establishing 15-25 %, inserts 15-25 % (warm 3D props, never flat diagrams), low 5-10 %, high 7-10 %.
- Acceptance: median in-shot frame-diff >= 4, p90 >= 12 (90x160 grey), shown next to film 2 at the FINAL gate.

## Shots (film time = narration time + 0.10; t below is NARRATION time)
| # | t0-t1 | in | preset / light | action + camera move |
|---|---|---|---|---|
| 1 | 0.00-1.60 | — | measure_chair / DAY_INT | HOOK image: Bertillon, calm, lifts big steel calipers and closes them on a seated prisoner's ear (prisoner_a stiff, eyes sideways). Drift push-in 8 %/s, slide left 30 px/s; calipers fg. |
| 2 | 1.60-3.10 | C | measure_wide / DAY_INT | the room: queue of prisoners on the bench, gendarme at the door, Bertillon at the chair; next prisoner sits. Pull-out 7 %/s + slide right; gas lamp fg. |
| 3 | 3.10-4.71 | C | measure_low (insert on ear) | close raking insert: caliper tips on an ear, then snap (15 f, x1.6) to the next ear (prisoner_b) on "ทีละหู". |
| 4 | 4.71-7.30 | D11 | street_wide / DUSK_EXT | Paris at dusk: mansard roofs, gas lamps lighting, police wagon arrives at the station. Crane-down/push 6 %/s; lamp post fg. |
| 5 | 7.30-9.40 | C | street_wagon / DUSK_EXT | gendarmes pull a thief (prisoner_c) from the wagon; he tips his cap and smirks (fake name). Slide 40 px/s + push. |
| 6 | 9.40-11.10 | C | measure_door / DAY_INT (front desk side) | the same thief at the desk shrugging innocently; a gendarme shrugs and waves him through (light sentence). Push-in 9 %/s on the shrug. |
| 7 | 11.10-12.90 | D11 | records_aisle / DAY_INT | endless photo/card cabinets, piles of photo cards spilling; clerks lost among them. High angle, pull-out 7 %/s + slide; cards stack fg. |
| 8 | 12.90-14.72 | C | records_desk / DAY_INT | insert: two photo cards side by side on the desk — the same face, one with a big moustache (drawn, no text); a clerk scratches his head. Drift across, push 8 %/s. |
| 9 | 14.72-16.32 | C | measure_wide / DAY_INT | the inspector strides in, sees Bertillon measuring an ear, bursts out laughing (bounce, gendarmes join). Push-in 8 %/s; kepi rack fg. |
| 10 | 16.32-17.91 | C | measure_low (two-shot, inspector near) | inspector mocks with lip-sync "วัดหูโจรเนี่ยนะ!", pointing at the calipers; Bertillon behind, unmoved. Low 1.2 D, slight push. |
| 11 | 17.91-19.64 | C | measure_chair (eye, two-shot staged in depth) | "ถ้าเอ็งใช้คีมนั่นจับโจรเก่าได้สักคน" lip-sync, inspector flicks the calipers; slide 40 px/s. |
| 12 | 19.64-21.61 | C | measure_chair | QUICK PUSH-IN (snap 20 f, x1.5) on the inspector tapping his own ear: "ข้าจะนั่งให้เอ็งวัดหูข้าเองเลย!" (lip-sync), chest out. |
| 13 | 21.61-24.08 | C | measure_high / DAY_INT | the whole room laughs: gendarmes and prisoners point at Bertillon, one mimics calipers on his own ear (bounce 3 Hz). High angle, pull-out 7 %/s. |
| 14 | 24.08-26.10 | D11 | records_desk / EVENING_INT | the prefect (top hat, sash) at Bertillon's desk, holds up three fingers on "สามเดือน". Push 8 %/s; green lamp fg. |
| 15 | 26.10-28.25 | C | records_low | prefect turns away; Bertillon alone below the towering cabinets, tightens his pince-nez. Low angle, slow pull-out + slide. |
| 16 | 28.25-29.90 | D11 | measure_chair / DAY_INT | montage 1: calipers on a head (length), Bertillon reads, a gendarme writes. Push 9 %/s. |
| 17 | 29.90-31.50 | C | measure_low (insert) | montage 2 quick: middle finger on the gauge -> snap to foot on the foot board (snap 14 f). |
| 18 | 31.50-33.10 | C | measure_wide | montage 3: arm-span scale and ear; Bertillon writes on a card (pen) — slide 50 px/s past the height gauge fg. |
| 19 | 33.10-34.74 | C | records_aisle | Bertillon slides the card into a drawer marked by size (no text, three drawer sizes small/medium/large); drawers fill up. Push + slide. |
| 20 | 34.74-37.48 | D11 | records_desk / EVENING_INT | two months later: drawers overflowing, candle low, Bertillon tired (slumped) comparing cards, no match. Slow pull-out 6 %/s + slide. |
| 21 | 37.48-39.74 | C | records_aisle (inspector in doorway, Bertillon near) | inspector shouts from the doorway, cupped hand: "เหลืออีกอาทิตย์เดียวนะ ไอ้ช่างวัดหู!" (lip-sync), gendarmes snicker. Push-in 9 %/s on the shout. |
| 22 | 39.76-42.40 | D11 | measure_door / DAY_INT | last week: two gendarmes escort dupont in (held pose); the inspector follows, smirking. Push 8 %/s, door frame fg. |
| 23 | 42.40-44.65 | C | measure_chair | dupont in the chair, innocent shrug, shakes head "never arrested"; inspector grins at Bertillon. Push-in 9 %/s on dupont. |
| 24 | 44.65-46.78 | C | measure_chair -> drawer_big | REVEAL step 1: calipers on dupont's head (insert 0.8 s) then SNAP to records: Bertillon yanks the "long-head" big drawer out (set_drawer open 0->1). Whip/snap 16 f. |
| 25 | 46.78-48.60 | C | drawer_box | step 2: finger measured (quick insert) -> inside the big drawer only one box remains lit; he lifts the box out (set_drawer). Snap push x1.5. |
| 26 | 48.60-50.41 | C | card_hero | step 3: ear -> one single card rises from the box (set_card_lift 0->1) into the lamplight. Push-in 9 %/s; calipers fg. |
| 27 | 50.41-52.52 | C | card_hero (Bertillon OTS) | the card held next to dupont's face in the background; the drawn profile on the card = dupont's profile; numbers rows glow one by one (all match). Slide 40 px/s + push. |
| 28 | 52.52-56.40 | C | measure_chair (two-shot) | the card turned toward dupont: the name panel shows a drawn empty bottle icon (no text); dupont's eyes go wide (caught), the inspector's jaw drops (shocked). Push-in, then snap (18 f) to the inspector on "ขวดเปล่า". |
| 29 | 56.40-59.62 | D11 | records_low / DAY_INT | Bertillon holds the card up (triumphant) under the cabinets; behind him dupont in a fake beard dissolves to clean-shaven — the card does not change (bones stay). Slow push 7 %/s. |
| 30 | 59.62-62.15 | C | records_aisle / DAY_INT | drawers fill, gendarmes bring more thieves, cards found one after another (cards popping up along the aisle, 200+). High angle crane pull-out 8 %/s. |
| 31 | 62.15-64.91 | D11 | measure_wide / DAY_INT | the ending: the inspector, red-faced, sits stiff in the measuring chair (seated_stiff); gendarmes and prisoners watch, grinning. Push-in 8 %/s; kepi rack fg. |
| 32 | 64.91-67.13 | C | measure_chair | Bertillon calmly closes the calipers on the inspector's ear; inspector's moustache twitches, eyes sideways. Push-in 9 %/s. |
| 33 | 67.13-68.30 | C | measure_low (insert on ear) | final punch: caliper tips on the inspector's ear (same framing as shot 3 = callback), quick push-in x1.4; HARD CUT on "ตัวเอง" (film end g 2052). |

Shot count 33, mean 2.06 s; with planned snaps (3, 12, 17, 24, 25, 28) the framing changes ~40 -> ~1.7 s; each take adds at least one extra snap or reframe inside shots longer than 2.2 s to reach the 1.3-1.4 s target (bible camera rule 6).
Angle mix (approx): eye 14 shots, establishing/wide 6, insert 7, low 4, high 3.

## Sound cues (for conform)
calipers click (1, 3, 16-18, 24-26, 32-33), crowd laughter (9, 13, 21), wagon wheels + horse (4-5), drawer slide (19, 24-25), paper flutter (26-27, 30), gasp (28), clock tick bed under 20-21, sting on "มาร์แตง" (28).

## Takes for render teams (one take per row group; 6 handle frames each side)
| take | shots | t0-t1 (narration) |
|---|---|---|
| s01 | 1-3 | 0.00-4.71 |
| s02 | 4-6 | 4.71-11.10 |
| s03 | 7-8 | 11.10-14.72 |
| s04 | 9-12 | 14.72-21.61 |
| s05 | 13 | 21.61-24.08 |
| s06 | 14-15 | 24.08-28.25 |
| s07 | 16-19 | 28.25-34.74 |
| s08 | 20-21 | 34.74-39.76 |
| s09 | 22-23 | 39.76-44.65 |
| s10 | 24-26 | 44.65-50.41 |
| s11 | 27-28 | 50.41-56.40 |
| s12 | 29-30 | 56.40-62.15 |
| s13 | 31-33 | 62.15-68.30 |
