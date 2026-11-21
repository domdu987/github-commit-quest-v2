# small_REVIEW.md : vault.py and room.py against the reference

Self-review by the builder (not independent). Pictures: `small_contact.jpg` (every camera x preset at 360x640 with placeholder actors, plus ref a/t0010, t0080, t0088 and ref b frames), finals in `small_work/final_*.png`.

## Numbers (hue_report band, `small_work/hue.py`, rows in `small_work/hue_rows.txt`)
| set | red | orange | blue | violet | magenta | sat | val | dark | verdict |
|---|---|---|---|---|---|---|---|---|---|
| vault LANTERN | 40.6 | 34.3 | 16.3 | 1.5 | 5.3 | 0.42 | 0.45 | 0.09 | in band |
| room DAWN | 36.8 | 31.7 | 27.8 | 0.5 | 3.2 | 0.44 | 0.45 | 0.08 | in band |
| vault BURN | 89.8 | 0.9 | 0.1 | 0.9 | 7.6 | 0.57 | 0.58 | 0.11 | special light: the vault is lit by fire only, so no cool light; no magenta cast |
| room NIGHT | 1.9 | 4.0 | 89.2 | 1.2 | 3.6 | 0.42 | 0.43 | 0.01 | special light: moonlight, blue-dominant like ref a night (74.8 blue); candle is a small warm accent |
| ref a t0010 | 26.3 | 28.6 | 31.2 | 3.9 | 7.6 | 0.27 | 0.51 | 0.07 | |
Note: `v3/tools/hue_report.py` crashes on its own "interiors" reference rows (it asks for ref/a/t27.0.jpg; the files are tNNNN.jpg); `small_work/hue.py` imports its stats and band unchanged and skips those rows.
Several values sit within 1 point of a band edge (LANTERN red 40.6, val 0.45; DAWN val 0.45, dark 0.08): one brick colour moves red/orange by 5 points, so a re-tune of the brick palette must re-run the row.

Shade/lit on one lit surface (key on vs off, same pixels, `small_work/measure.py`): vault floor 0.168 (hue 20 -> 232), room floor patch 0.29 (hue 10 -> 243). Final 720x1280 x 12 samples: 14.1-15.7 CPU s per frame (2 threads, 7.2-7.9 s wall). Builds are deterministic (same digest, identical pixels in two processes).

## What was fixed after comparing with the references
- First vault pass was 76 % red, lit brick hue 9 and pink (blue ambient added under a warm key). Fixed by a yellow key, orange-leaning bricks and shade computed on the artwork pulled 85 % to grey: lit brick 20-30, shade 230-245.
- Vault evenly lit, no darks (dark 0.04): ambient now falls off 94 % over 4.5 D from the lantern and toward the crown and shaft.
- Brick texture read noisy next to the quiet stone of a/t0010: value spread of the bricks reduced.
- Room first pass was violet/magenta and murky: walls and wood keep a warm dusky shade (office-style per-surface shade multipliers), the floor alone goes blue-violet; dawn bounce pool around the patch.
- Moonlit patches were red (red floor x blue moon): the NIGHT key sees the artwork 80 % grey, so patches read pale lavender as in a/t0088.
- Crack glow clipped to yellow: emission lowered to 1.6 of `#ff5a10`, it now blooms orange.

## What still differs
- Reference interiors (a/t0010) have a painted, soft far layer and much more ornament (pillars, drapes, rose window); our vault is clean geometry with one repeating brick tile, and the back of the stair_high view is a plain door. A painted far card or more props (racks, ropes, a powder scale) would add density.
- The vault's lit surfaces are a little desaturated beige-orange; the reference warm lights are golden and more saturated. Pushing saturation broke the band (orange share) so it stays at 0.42.
- The lantern is the key but its glow on the near ceiling is a painted pool, not a visible light cone; no dust or smoke.
- Room: geometry is boxy (blanket is a box, mattress a box); the reference would drape it. Plaster tile repeats (the brick patch shows 3 times in room_wide).
- The DAWN light patch is small (one small window, by design); in push_rod the rod is lit only on its lower half.
- Placeholder actors stand on plain cards with no contact shadow decal (the stage module adds those); the boy uses the v2 hero at 0.8 scale until `nico` exists.
- BURN is uniformly orange; for the disaster shots the darker plum shade could be pushed further, and there is no smoke/fire geometry, only the crack glow, pools and the pulsing light.
- Raking hard light like ref b: our edges are crisp (sun 0.45 deg, lantern radius 0.025) but the vault key is a point, so shadows fan out rather than rake in parallel.
