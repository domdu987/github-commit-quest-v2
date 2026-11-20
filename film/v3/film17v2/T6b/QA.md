# T6b self-check (film 17 v2, T6 reveal payoff, g1536-1701, 166 frames)

Render: `render_t6b.py` (+ `t6b_stage.py` staging), `world_build('T6')` + `key_take` + `stage_cast2` on every frame, 720x1280, 16 samples + OIDN, 2 threads, `grade2`.
Chunks of 30 frames, one Blender process per chunk; `clear_cast()` before every `stage_cast2` (cast leak fix, plus per-frame material/image/action cleanup).
`check_take('T6')` hits = [] and `check_face('T6')` PASS (re-run after the camera edits). `qa_auto.py --cuts 1675 --first_g 1536`: PASS.
`rhythm.py`: 166 frames, 1 cut detected, in-shot median 9.26, p90 19.50.
Hard cut inside the range: **g1675** (6d framing held through g1674, g1675 opens on the P2 framing; director, takes.md 06657cb). `qa_auto` lists it as "no visible change within +-2 frames" only because its spike threshold is 8x the median diff; the actual diff g1674->g1675 is 44.5 (mean abs, 90x160 grey).

## Staging changes (all in `film/v3/film17v2/T6b/`, shared files untouched)
- Dupont's OTS back view = ginger hair dome, ears, nape, red neckerchief, patched brown jacket, with ink outlines (not a black slab).
- 6c (g1550-1616): held MARTIN card (3D plane beside Bertillon's raised hand, ~29 % of the frame width), turn g1594-1602, MARTIN almost face-on at g1601; the lifted hero card in the drawer box is hidden from g1550.
- 6d (g1616-1674): row of Bertillon, Dupont and the gendarme at equal depth; card above Dupont's head, empty bottle (3D plane) held by the gendarme's raised hand from g1646; camera look rotated and raised, floor about 25 %.
- Inspector: not rendered g1546-1639 (out of frame); out of frame left in 6d; on his mark for P2. P2 (g1675-1701): front-on jaw-drop, head + kepi about 24-30 % of the frame height.
- The foreground desk and a stool were deleted from the batched archive meshes (bmesh faces) for T6b only.
- Lights: T6 `TAKE_OVER` raised (shade_mul 1.4, fill_w 600, gain 1.15). Luma stays high; the director trims at conform.

## Luma (RGB-mean, 90x160 bilinear, binding metric)
All 166 frames: see `luma.txt`. Mean 124.4, min 111.9, max 134.3. Ranges: g1536-1547 (P1 join) 132.9; g1548-1575 126.1; g1576-1600 125.5; g1601-1674 126.1; g1675-1701 113.1.
Largest consecutive step in the take: 8.8 at g1675 (the planned hard cut); in g1536-1580 the largest step is 3.9 (g1563), none above 5.

## Join with T6a2 (luma seam fix, director 21:15/21:35)
- g1536-1575 were re-rendered (40 frames, one fresh process per frame, `join_one.sh`): T6a2's light setup (shade_mul 0.8, fill_w 220, gain 0.65, beam hidden) up to g1547, then a smoothstep to T6b's override (1.4 / 600 / 1.15) over g1548-1575 (beam stays hidden in g1536-1575; it is on from g1576, diff to beam-off 0.2-0.6/255).
- T6a2 g1535 (extracted from its take.mkv) luma 133.0 vs T6b g1536 133.6; mean abs diff (grey, 90x160) 7.11 vs T6a2's own neighbour median 21.6.
- T6b neighbour mean abs diff median over g1536-1580: 16.99.

## Frames viewed at FULL size (720x1280) and at phone size (360x640, `qa_phone_sheet.jpg`)
1. **g1550** (full viewed before the re-light; phone sheet viewed after it, same composition, slightly darker): sweep out of the P1 close-up. Bertillon's face is large at the left edge and its left side is CUT by the frame edge; the open drawer front crosses his chest and beard; the blank card back fills the right. **Known fault, see below.**
2. **g1561** (full: `key/frame_g1561.png`; phone sheet): Bertillon fully inside the frame, face about 140 px clear of the left edge, glasses, goatee, raised fist, the blank card back beside him, drawer at his right, nothing across his face.
3. **g1601** (full + phone): MARTIN card almost face-on to the right of his head, name panel with MARTIN in red and the bottle sketch, two portraits, hand print. Legible at phone size but small (the word is about 30 px wide at 360 px). Dupont's back (hair, neckerchief, jacket with blue patch) at the right edge, partly cropped; red stool top gone.
4. **g1650** (full + phone): Bertillon (left, raised fist), Dupont (centre, wide eyes, mouth 'o', sweat drops), gendarme (right) with the empty bottle held in his raised hand and sleeve beside the card; card above Dupont's head. Nobody hides anybody. Floor about 25 %. A tiny dark dot on the floor at lower right (an existing floor mark).
5. **g1675** (full + phone): first frame of the cut. Inspector front-on and centred, kepi, moustache, wide eyes with sweat, mouth open; his desk with the lamp at right; head + kepi about 24 % of the frame height.
6. **g1695** (full + phone): same shot after the push, head + kepi about 30 % of the frame height, jaw-drop held. Wall detail looks slightly soft from OIDN, no shimmer seen in the 8-frame samples.

Additional frames looked at in contact sheets or key stills: g1559, g1600, g1606, g1640, g1660, g1674, g1678, g1685, g1690.

## Known faults (not fixed)
- **g1549-1551**: Bertillon's face touches / is cut by the left edge. **g1550-1554**: the open drawer front crosses his chest and beard. Cause: the camera sweep out of T6a's P1 close-up passes close to the drawer with Bertillon behind it; the 3D card is near the lens. A faster offset ramp made it worse, so I left it. Frames g1556 onwards: no face on any edge in the frames I looked at.
- The MARTIN word at phone size is small (card about 29 % of the width), but readable.
- No black slabs, veil or shaft wedges seen. beam_k 0 and beam_fx forced to 0 tests at g1600/g1640 differ by 0.2-0.56/255 (`beam_test/`).
