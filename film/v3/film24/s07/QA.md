# s07 QA: film 24, shot 7 (sea flag_deck_crew): the crew laughs and points

Delivered: `take.mkv` (libx264rgb crf 6, 30 fps, first_g 638, 102 frames g 638..739, 29.9 MB), `meta.json` (g0 644, g1 734 exclusive), `cues.json`,
`contact.jpg`, `QA_AUTO.md` + `phone_sheet.jpg` (qa_auto PASS), `shot.py`, `deliver.py`. g 644..733 = shot 7 (21.47-24.45 s), 6 in + 6 out handle frames in 3D. Hard cuts at both ends.

| rule | how / measured |
|---|---|
| nothing floats, contact shadow | 3 cards Child-Of the jflag ride on the open upper deck, decal on the deck, sun shadow; checked on the sheet |
| no shake, one eased move | preset flag_deck_crew camera, one slow lateral slide 0.9 D (0.35 sine + 0.65 linear), travelling with the fleet; qa_jitter prints no shaky second (median 0.49 px: the big bouncing figures move the phase correlation) |
| never static > 6 frames | qa_auto: none |
| nothing parented to camera | unparented |
| feet planted | hips bounce = legs crouch oscillation 0.03-0.12, soles stay on the deck points; screen steps max 2.25 / 2.55 / 1.72 px per frame (camera slide only) |
| no identical duplicates | ashi_a24, ashi_c24 (mirrored, pale cone hat), ashi_d24 (black cone): different members, sizes, laugh phases |
| near bigger than far | head w a 99-100, b 93-95 (front row) > c 71-72 (back row) |
| heads above y 880 | head bottoms max 728 px |
| sharp | DOF off |
| mouths | no quote: fixed laughing mouths |
| tone | tears and laughter only |

Set state keyed each frame: set_fleet_chase (g-638)/30, korean_turn 0, spikes 3, ports 0, damage 0, cannon smoke 0.
Deviations: THREE soldiers, not four. The preset's anchors a/b are the only two inside the 9:16 frame; a fourth soldier at the deck edge stood beside the
rail with water below him (floating look) and every other spot overlapped a neighbour, so he was dropped (plan: 3-4). The back-row soldier c was
added between the front pair. A first render with four soldiers was thrown away. Render 32.8 s wall / 62.9 s cpu per frame.
