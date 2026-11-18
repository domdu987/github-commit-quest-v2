# QA-art, SET gate, film 12 (set3d12 street): FIX-FIRST

Reviewed: contact.jpg (20 tiles), full-size finals 01, 03, 05, 07, 13, 15, 16, 18 (plus crops of the road in 07 and 16), styleboard/board.jpg,
cast12/sheet.jpg (cropped), set3d10/contact_small.jpg, and the reference sheets window_0 and rail_0. Code read: street.py, street_tex.py, street_parts.py.
Note: API.md has no "weak points" section. The weak spots are in STYLEBOARD.md, and #1 (chunky horse) and #2 (noisy puddles with ghost cobbles) are still open.

## Scores (1-10)
| criterion | score | why |
|---|---|---|
| Set density / ornament | 7 | Dense terraces, shops, market, rank and chimneys hold up in 02, 09, 10, 12 and 13. But 35-45 % of the frame in 01, 03, 06, 08, 16 and 17 is bare oversized setts with nothing on them. |
| Lighting & colour | 5 | Warm windows against blue-violet shade still work and the hue numbers pass. But the day sky is washed out to near white-lavender (01, 13, 16), which loses the board's peach/mauve warmth. A zenith band artifact shows in every low-angle tile. The hammercloth reads magenta. Lanterns are lemon yellow, not amber. White speckle noise covers the wet road at 14 samples. |
| Composition / framing | 5 | The 22 mm lens with the horizon at mid-frame puts the subjects small and high: Hanway's head is about 40 px in 01, about 20 px on the phone sheet. The ending framing (15) is mostly horse polygons. |
| Character acting | 7 (cast sheet only) | The poses read well on the sheet (laugh, point_mock, count_coins_sky, sulk_under_pink_umbrella). The set tiles only have placeholders. |
| Key moments | 3 | Hook (01) 6. Reveal (16/17) 3: the rush is a row of identical dark cones behind coach_0, with no rush, fight or coins. False payoff / mud (18) 3: flat beige cut-outs. Ending (15) 4. |
| Water | 3 | The big puddle in 07/18 is a smeared double image of setts under a noisy mirror, with no smooth surface and no readable shore. A pale straight-edged reflection slab sits in 16's foreground. This is not "smooth and layered". |
| Overall match to board / references | 5 | Below the approved board. The board's road was a coloured wet mirror with a soft painted sky. Here the road is matte, pillowy and grey-violet, and the sky is a pale cartoon ceiling. The references (window, rail) keep the subject at mid-frame size with rich, deep colour. |

## Fixes that matter before the client sees it (in order)

1. **Sky zenith arcs and pale sky (tiles 01, 03, 05, 07, 15, 16, 18).** The huge concentric arcs at the top of low-angle frames are the painted cumulus of the top layer, pinched at the dome pole. In `street_tex.sky_rain`, drop the `((46.0, 72.0), 8, (40, 70), 2)` layer, or cap it at e <= 40. Fade the cloud stamping to zero above about el 50 so the zenith is a plain gradient. Then bump `TEX_V`. Bring back some of the board's warmth: lower `P_RAIN['sky_k']` to about 0.85 so the horizon (`(0,'#f0c49c')`, `(7,'#e6b8a8')`) is no longer graded to near white, and add a little peach to the cloud rims. 15 (the ending) is unshowable until this is fixed.

2. **Water: smooth, layered puddles and no speckle (07, 18, 01, 03, 16).**
   - In `_mat_pud`, the 'core' layer must not resample the cobble texture. Give it a flat dark water base like `_mat_water('#1d2a58', rough 0.02)` with no bump, so the deep part is a smooth mirror and only the shallow and halo layers show setts. Then the big puddle at (-1.7, 12.4, r 3.3) reads as water with a pale shore line. Raise the G-rim emission (`0.12*strength`) slightly so the shore shows at phone size.
   - Kill the white speckle: set `SAMPLES` to at least 24 on puddle shots, or clamp indirect light / `filter_glossy` about 1.0 and disable caustics in `setup_render`.
   - The setts read as giant pillows in the foreground of every low camera. Shrink them (`ROAD_TILE` 3.2 -> about 2.4) and lower the bump dome so the road reads wet-flat like the board, not quilted.

3. **Mud splash (18, plan shot 12).** `M['mud']` and `M['mud_hi']` are `mat_emit` flat colours (`#8a6840` / `#dcc490`), so the wave renders as unshaded beige cardboard. These are exactly the "flat triangles" the client rejects.
   - Make them lit toon materials: wet dark brown about `#5a3e24`, with `_wetgloss` highlights and a lighter `mud_hi` only on the bulb tips.
   - Raise `PT.tube(..., seg=6)` to 10 so the fins are rounded.
   - Add a translucent muddy-water spray layer so it reads as a splash, not a fan of paper.

4. **Reveal readability (16/17/20, plan shots 16-17).**
   - The rush crowd (`crowd_figures('rush')`) is a single file of identical near-black cones hidden behind coach_0's wheel, and the lower 40 % is empty road.
   - Re-aim `CAMS['rank_rush']` closer and lower so the doors and the crowd fill the middle band, for example A `(-1.6, 12.0, 2.6) -> (3.0, 24.0, 3.3)`, keeping heads < 880 (`project_px`).
   - Spread the `_rush_slots` ends across the doors of coaches 0 and 1 (not queued along x), and give the placeholder figures the cast's warm coat colours instead of dark cones.
   - Use `set_rank_busy(1)` with lit coach windows.
   - The set-gate tile must show the reveal image the plan describes (crowd fighting for coaches, a grinning coachman), not a queue.

5. **Ending / box_seat framing and colour (05, 11, 15, plan shots 6, 8, 14, 23).**
   - Pose B `(0.2, 12.4, 2.3)` sits under the horse: the bottom half of 15 is flat orange/magenta horse polygons (the chunky horse from weak spot #1, now seen close), and the coachman's face is about 70 px.
   - Move B back and up, for example `(-0.8, 10.5, 3.4) -> (3.4, 18.6, 5.7)`, or use a 30 mm `lens` for box_seat (still no DOF), so the coachman plus the pink umbrella fill the upper-middle third and the horse is only its head at the edge.
   - Shift `M['cloth']` (hammercloth, `#7a2434`, smix 0.8) to an orange-leaning red, about `#8a3a22`, because in shade it reads magenta-violet in 05, 07, 15 and 18.
   - Take the coach lanterns `e_clamp%d` (`#ffc070`, strength 3.4) down to about 2.2 so they read amber, not clipped lemon.

6. **Empty lower third in the eye-level presets (01, 03, 06, 08, 09, 16, 17).** Raise `look_at` z by about 1.0-1.5 on `street_wide`, `market` and `rank_rush`, so more facade and less road is in frame, and re-check heads with `project_px` (keep below 860). Dress the near road with a few props on the setts: a parked barrow or dray, a mounting block, crates at the kerb, the gutter grating. Puddles there should reflect the amber windows, as in the board.

## Cast colours in this set
- **Hanway** (mid-navy frock coat, black umbrella, white stockings) is close to the shade hue (about 248) and goes dark under the black canopy, most of all in DUSK_RAIN. He will sink into the blue-violet road. Give his cards a warm `rim` (amber, from the key side), keep the buff waistcoat and white stock visible, and consider a slightly lighter, warmer coat value.
- **Head coachman** (drab-olive greatcoat) stands on coach_0, which is `COACH_SPEC[0]` = 'green'. That is olive on dark green, with weak separation in the key shots 05, 11 and 15. Make coach_0 'oxblood' or 'ochre' (swap with `COACH_SPEC[1]` or `[3]`). His red nose and scarf then read too.
- **Pink umbrella:** the cast sheet's `coachman_sulk_under_pink_umbrella` prop is a hot magenta-pink. The `_hue_guard` Hue Correct will pull it toward violet and it fights the 3D lace umbrella (salmon pink). Use only the 3D `set_pink_umbrella` in the ending and drop the sprite prop, or recolour the sprite to the same coral-pink.
- **Seated cast poses** draw their own red and green coach box (`coach_box=1`). Do not use them on the 3D box: stand the cards on the plank (z 4.22) without `coach_box`, or the box is doubled.
- **Crowd** (red, teal, ochre, burgundy, brown) is good warm accent against the blue shade. The purple of `passenger_b` / `crowd_woman` will be shifted by the hue guard, so use the warmer women in the foreground.
- The sprites are flat mid-value against a high-contrast toon-lit set. Use `tint` toward the shade colour on the shaded side, plus a warm rim, so they sit in the light and are not pasted on.

## Verdict: FIX-FIRST
The sky arcs (every low angle, including the ending), the speckled double-image water, and the cardboard mud splash are the client's named dislikes ("water smooth, not flat triangles", "pleasing, not harsh"). The reveal tile does not show the reveal. Fix 1-5, re-render 01, 05, 07, 15, 16 and 18, and run this gate again before showing the client.

## Re-check r1

Reviewed: the new contact.jpg (25 tiles); the full-size finals 01, 06, 09, 13, 15, 16, 22, 23 and 24; styleboard/board.jpg; and a phone strip at 360x640 of tiles 01, 13, 22 and 23 (scratchpad `phone4.png`). Code read: street.py (`_mat_pud`, `_mud_objects`, materials, COACH_SPEC) and API.md sections 9-11.

### Earlier fixes
| # | fix | status | notes |
|---|---|---|---|
| 1 | Sky zenith arcs, pale sky | **done** | The arcs are gone. The sky is warmer, with a peach horizon and peach cloud rims. New but minor: the cel clouds have hard dark straight "under-band" strokes, and small floating triangle shards (01 about (320,320), 15 about (190,240) and (470,170), 16 about (130,300)). |
| 2 | Water smooth and layered, no speckle, smaller setts | **partly** | The deep cores are now flat, smooth mirrors with ripple rings (12, 13, 16, 23 read as water), and the speckle is largely gone. Open: the shore glint (`rim` 0.35*strength) now reads as a thin pale **wire or cable** running across the road (01 y 940-1050, 13, 16 y 960-1060, 23 y 1090-1200, 24). The low-camera setts are still big pillows (16 and 23 foreground). The lamp-reflection orb on the road (QA-tech #4) is still there in 01 (180,815) and 24 (560,1020). |
| 3 | Mud splash | **not** | The fins are now lit brown with seg 10, but the new `mud_spray` sheets (12 overlapping emission tubes, 1.3 wide, opacity 0.3, colour (0.72,0.56,0.36)) stack into one opaque pale-beige cardboard slab behind Hanway. The bulbs are separate brown balls, and the droplets near his face render as grey faceted rocks (seg 6, rings 4). On the phone it reads as "beige paper plus balls", not mud. This is still the client's "flat triangles" dislike. The mud spots on Hanway's card do read well. The coach in 23 is violet-magenta (wheels and body). |
| 4 | Reveal readability | **mostly done** | 13 now shows real cast cards shoving at coach_0's door with angry faces, the coach is lit and busy, and the coachman sits above them. It reads at phone size. It is still a single file along the coach, the lower 30 % is puddle, and the cards repeat. That is fine for the client sheet; fix it at the take gate. |
| 5 | Ending framing and colour | **done** | 22 is the best tile. The coachman and the coral lace umbrella fill the upper-middle, the rosettes are cream, the pole is clear of his face, the hammercloth is orange-red, and the lanterns are amber. Only a small slice of horse shows at the bottom right. |
| 6 | Empty lower third, near-road props | **partly** | 13 and 15 are better (planters and barrels on the pavement, puddles with shores). 01 (hook) and 16 still show about 40 % bare setts, and Hanway's head is about 20 px on the phone in 01. |
| - | Cast colour notes | **done** | coach_0 is now ochre, so the olive coachman separates. Hanway's navy holds against the road. The pink umbrella is 3D only. The box cards stand on the plank with no doubled box. |

### Scores (r0 -> r1)
| criterion | r0 | r1 | why |
|---|---|---|---|
| Set density / ornament | 7 | 7 | Same rich terraces. The near road is still bare in 01 and 16. |
| Lighting & colour | 5 | 7 | Warm sky, amber lanterns and a fixed hammercloth. Cloud under-strokes and shards remain, and the coach in 23 is violet. |
| Composition / framing | 5 | 7 | 06, 09, 13 and 22 are well framed. The hook (01) is still small and high. |
| Character acting (in set) | 7 | 7 | Real cards are now in the set, and the coachman's face reads in 09, 13 and 22. |
| Key moments | 3 | 5 | Hook 6, reveal 6, ending 8, mud 2. |
| Water | 3 | 6 | Smooth cores and ripples. Wire-like shore lines and the floating orb remain. |
| Overall match to board / refs | 5 | 7 | The road's wet mirror and warm sky are now close to the board. The cel clouds are a stylistic step away from the board's soft painted clouds, but they are consistent and acceptable. |

### Phone check (360x640)
- **01 hook:** reads as a rainy street with a little umbrella man. Hanway is legible but small. The orb on the road and the pale wire curve show at this size.
- **13 reveal:** reads. The angry crowd at the coach and the coachman's red nose are clear.
- **22 ending:** excellent. The umbrella, the sulk and the red nose all read instantly.
- **23 mud:** fails. Hanway with his mud spots reads, but the splash reads as a beige sheet with brown balls, and the shore wire crosses the foreground.

### Verdict: FIX-FIRST (small: two items, re-render only 01, 13, 16, 23 and 24; no full gate needed, a look at those five tiles is enough)

**Blocking**

1. **Mud splash (tile 23, shot 12).** This is in `street.py` `_mud_objects`.
   - The spray sheets are the beige slab. In the `PT.tube(sp, ...)` line, cut the width `1.3*(...)` to `0.5*(...)` and build a sheet only for `j % 3 == 0`.
   - In `M['mud_spray']` (line 273), change to `_mat_streak(pre+'mudspray', (0.36, 0.25, 0.14), 1.0, 0.12)`: darker brown and much thinner.
   - Droplets: raise to `seg=10, rings=7`, and use `M['mud']` for all of them except one in four. Skip any drop whose path passes within 0.8 of the face point `(-4.3, 11.0, 2.6)`, or clamp `vz` so the drops fall in front of the chest.
   - Lower the fin height `Hh` by about 25 % (`3.2+0.7*...` -> `2.4+0.6*...`) so the crest breaks at chest height in front of the card instead of a wall behind it.
   - Re-render 23 at t 0.3 and 0.45. The splash must read as glossy dark-brown fins with lighter tips, not as a sheet.
   - At the same time, warm the coach in tile 23 (the violet body and wheels): give the coach that passes in this shot `COACH_SPEC` 'ochre' or 'oxblood' with orange-leaning wheels.

2. **Shore "wire" and floating orb (tiles 01 hook, 13, 16, 23, 24).**
   - In `_mat_pud`, in the 'shallow' rim, take `rm.inputs[1]` from `0.35*strength` to about `0.12*strength`, and soften the G-channel shore band in the mask (blur it 2-3 px in the mask texture, or multiply G by R so the line fades where the film is thin). The shore should be a faint glint, not a line.
   - Orb: in 01 (180,815) and 24 (560,1020) a lamp glass is mirrored in a small puddle or gutter whose outline is not visible. Either set `visible_glossy = False` on the lamp-glass and lantern emission objects (keep the halo light), or drop or move the puddle decal under those pixels from the `_puddles` list for street_wide and market.

**Not blocking (fix in parallel or at the take gates)**
- Cloud under-band strokes and triangle shards (cut the dark under-band or soften it with a gradient alpha, and delete the shard faces).
- 01 and 16 bare lower third: raise `look_at` z, or add a barrow or crates at the near kerb.
- 13 rush: break the single file (stagger the `end` points by ±1.2 on y and add a second row), and vary the cards.
- Big pillow setts under the low cameras.
- Horse faceting.
