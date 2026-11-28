# LIGHT SPEC v2: match R9/R10 (client 2026-11-27, after turtle_C)
v1 of this spec produced turtle_C, which the client judged "สีกับแสงยังไม่ดีเท่าคลิปที่ผมส่งให้ดู". Measured on 1 fps frames:

| | R9/R10 | turtle_C |
|---|---|---|
| mean luma | 0.50-0.53 | 0.37 (too dark) |
| local contrast (mean abs neighbour luma diff) | 0.040-0.042 | 0.030 (soft, flat) |
| saturation | 0.29-0.30 | 0.34 |

Comparison image: film/ref_shorts/compare_R9_R10_vs_turtleC.jpg.

## Targets (measure every take; a take misses if any value is out of range)
- Mean luma 0.48-0.55, p1 0.02-0.08, p99 0.90-0.95.
- Local contrast 0.038 or more, measured at 90x160 like qa.
- Saturation 0.45-0.50, Lab chroma >= 28 (client 2026-11-28: R2-R7 are more vivid than R9/R10).

## How to get there
1. **Bright key, not dusk backlight.** Use a late-afternoon or golden-hour sun at 20-35°, strong and warm (about 3-5x the old KEY), coming from the side or 3/4 front so faces and props are lit. Backlit dusk only for 1-2 hero moments.
2. **Bounce fill.** Use 4 or more GI bounces, a bright sky fill, and light-coloured ground bounce, so shadows keep colour and detail. Shadows are cool blue, never murky grey-purple.
3. **Little haze.** Use volume only at long distance (more than 150 m) and thin. No fog in the near or mid ground.
4. **Textured materials everywhere.** Use real CC0 PBR textures (Poly Haven / ambientCG) where the network allows; otherwise procedural textures. Include wood grain and plank seams, brick, stone, fabric weave and rope, with normal or bump maps, so the frame has crisp surface detail.
5. **Crisp image.** Render at native resolution. Keep the denoiser from smearing texture (use prefilter Accurate and enough samples). Apply mild sharpening in post. Use DOF only on macro inserts.
6. **Warm-cool contrast** stays: warm sunlit faces against cool sky and shadow. Add a bright pastel sky with a gradient and clouds.
7. **Practical lights** (lanterns, fires) add warm pools in interiors. Interiors still read bright, like R9's cabin.

## Gate
Before the set is locked, render ONE test shot at final settings, measure it against these targets, and put it side by side with an R9 or R10 frame. Only then build out the film.
