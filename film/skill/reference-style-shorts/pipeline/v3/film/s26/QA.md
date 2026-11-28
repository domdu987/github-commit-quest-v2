# QA: take s26 (shot 26, kitchen_storm): the last image of the film

- **Frames.** Film frames g 1873 to 1964 (the end of the film). No handles: the way in is the white flash, which the conform makes over the first 4 frames, and the way out is the end of the film. That is 92 final frames in `frames/g_%04d.png` at 720x1280.
- **Sources.** The set is `v3/set3d_kitchen/kitchen3d.py`, the take is `shot.py`, and the numbers come from `set3d_kitchen/kqa.py` (stored in `work/qa.json`).

## Approval of the last frame
Before animating, I rendered and checked the last frame of the film (g 1964) as a still, then rendered it again as the final frame `frames/g_1964.png`.
- **Weather box.** It is centred at x 360. The header top is at y 247 and the bottom of the Thai at y 573, all above y 600 and clear of the caption band at y 848-960.
- **Size of ฝนตก.** The full glyph, with the tail of ฝ, is 99.5 px tall. The x-height of น ต ก is about 71 px, so the 70 px rule is met either way.
- **Bleed.** The drop has landed on ฝนตก, and the ink bleeds blue-brown into a wet ring (`newspaper_bleed` frame f_11, held).
- **Around it.** The cup, crept toward the near table edge, stands at lower right. Above the paper, dark water and rain run down the four panes, and the lower-right pane is cracked.
- **Approved.** All of the above matches the plan's final frame.

## Timing (narration clock + 0.1 s = film time)
| event | clock | film frame |
|---|---|---|
| cut-in out of the white flash (window lit by lightning) | 62.442 | 1873-1876 |
| chair shoved back, cup rattling | 62.45-63.5 | 1876-1908 |
| lightning and thunder | 62.90 | 1889-1894 |
| snap pull-back and tilt down | 63.28-63.82 | 1901-1918 (16 frames) |
| Thai readable (≥ 70 px, above y 600) | from 63.82 (plan: 63.9) | 1918 on |
| newspaper flutter | 63.90-64.60 | 1920-1941 |
| pane cracks | 64.00 | 1923 (grows over 4 frames) |
| push onto the weather box | 64.2-65.0 | 1929-1953 |
| shake gone | 64.6 | 1941 |
| still hold | | 1953-1964 (12 frames) |
| drop falls / lands, bleed f_00 | 64.82 / 64.95 | 1948-1951 / 1952; bleed f_00-f_11 over g 1952-1963, f_11 held on g 1964 |

## Camera (from the true 3D camera, corner speed in px per frame)
- **g 1873-1900, tight on the window.** The four panes fill the frame. The camera drifts in at 2 %/s under a 5 Hz shake, at 20-35 px per frame.
- **g 1901-1917, snap.** The camera pulls back from 1.05 D to the table framing (2.42 D, so x0.43) with the tilt trailing. Speed peaks at 223 px per frame. Frames g 1905-1914 are streaked whole with `post.py`'s method: there are no actors, so no plate or matte is needed.
- **g 1918-1928, settle.** The camera holds the table framing with a 0.6 %/s creep while the shake decays, at 0.7-2 px per frame.
- **g 1929-1953, push.** The camera pushes 15 % of the way to the weather-box centre. It starts at about 26 %/s and eases out to zero at 65.0, with a tilt down of 0.05 D so the words rise clear of y 600.
- **g 1953-1964, still.** The camera stops (the 12-frame hold).
- **Framing-change times (film).** 62.44 (in, drifting), 63.38-63.93 (snap), 64.30-65.10 (push), 65.10 (hold).
- **Static runs over 6 frames.** One, from g 1954: the planned 12-frame final hold.
- **Linear runs.** None.
- **Popcheck.** No pops. The lightning frames g 1873-1876 and g 1889-1894 are deliberate light changes.

## Text on the newspaper (projected page points)
| g | header top y | Thai bottom y | height of ฝนตก (full glyph) | weather-box centre x |
|---|---|---|---|---|
| 1918 (snap lands) | 299 | 573 | 83.5 px | 362 |
| 1929 (push starts) | 298 | 572 | 83.8 px | 360 |
| 1941 | 266 | 572 | 93.7 px | 360 |
| 1952 (drop lands) | 247 | 573 | 99.4 px | 360 |
| 1964 (last frame) | 247 | 573 | 99.5 px | 360 |

## Props in motion
- **Rings on the coffee.** A ring texture runs outward at 0.9 rad per frame at amplitude 0.85 until the shake ends, then eases to 0.25. These are the ripple that shot 15 did not have.
- **Cup and saucer.** They creep 0.05 D right and 0.17 D toward the lens, in jerks plus a slow slide, with hops of up to 0.01 D and ±3 degrees of rotation while rattling.
- **Paper.** It flutters, a wave across the leaning page plus the free top-left corner lifting. The amplitude is 0.006 D throughout and 0.036 D from 63.9 to 64.6. The saucer stands on its bottom-right corner.
- **No characters.** No heads and no hands appear in this shot.

## Light and colour: `kitchen_storm` (special light)
**hue_report row (frames/):**

| red | orange | yellow | green | cyan | blue | violet | magenta | sat | val | dark |
|---|---|---|---|---|---|---|---|---|---|---|
| 46.1 | 18.9 | 0.0 | 0.0 | 4.6 | 24.3 | 0.4 | 5.7 | 0.51 | 0.36 | 0.22 |

**Why it is out of band (red, orange, sat, val, dark).** This is the storm and the end of the film. The plan asks for "dark, the window filled by the wall of water, lightning".
- **Value and dark share.** Value 0.36 and a dark share of 22 % are deliberate. These are the real deep darks the colour section asks for: the room is lit only by a weak warm key and a deep-blue ambient.
- **Blue.** Blue (24.3, in band) and cyan (4.6) come from the wave in the window.
- **Red.** Red is high because the oilcloth fills the lower half of the frame.
- **Shade.** Shade reads blue-violet. Violet is 0.4 and magenta 5.7, inside 0-10.

**The magenta pass.**
- **Before:** an earlier storm build measured 12-27 % magenta. The red cloth, the red wood and the paper's ink were going magenta under the blue ambient and the office grade's plum offset.
- **Repairs:**
  - warm, low-blue shade multipliers on the cloth, wall and wood: (2.2, 1.3, 0.55), (2.6, 1.5, 0.55) and (1.8, 1.15, 0.55);
  - a warm key, (0.28, 0.20, 0.125);
  - a neutral-blue grade offset, (0.0, 0.002, 0.007).

**Light numbers.**
- Ambient: (0.050, 0.072, 0.20), falling by 1.2 x y / 9 toward the lens.
- Key: one sun, (0.28, 0.20, 0.125), angle 2 degrees.
- Lightning: a second sun through the window, at (π x 3.2) x strength, with the window card brightened x1.6 for the same frames. Strength by frame:
  - g 1873-1876: 1.0, 0.75, 0.45, 0.2 (out of the white flash)
  - g 1889-1894: 0.35, 1.0, 0.8, 0.25, 0.6, 0.15
  - g 1935-1936: 0.7, 0.3
- Window: the wave sequence (92 frames, one per film frame) at emission 0.85.
- Grade: saturation 1.15.

## Cost
- 8 samples, 720x1280, 2 threads, one process.
- Median 5.77 s and maximum 6.46 s per frame, measured while other agents were rendering.
- 12 samples cost 8.5 s and gave the same picture (mean difference 0.25 of 255), which is why 8 samples were used. `meta.json` says so.

## What differs from the plan, and why
1. **The pull-back is x0.43, not x0.37.** It runs from 1.05 D in front of the window to the table framing at 2.42 D, because the table framing is the fixed end point shared with shot 15. Timing, the tilt down and the easing follow the plan.
2. **The masthead is not in frame.** The page is folded; see `s15/QA.md` item 1. The calendar leaf 21 hangs left of the window. It is in the table framing of shot 15, but here it falls just outside the pushed-in framing.
3. **The chair is shoved back off the right edge.** It is not visible in this framing. The shove is in `cues.json` as a sound only.
4. **The wall of water is the window's exterior texture sequence.** Behind the panes, the dark water face rises with a boiling foam crest that climbs out of the top of the window by about g 1903, with spray, rain and water sheeting down the glass. It reads as heavy water against the window more than as a single towering curl.
5. **The drop falls for 4 frames.** It is a small light-blue drop falling onto ฝนตก (g 1948-1951) before the bleed sequence starts. Where it falls from (a leak in the sash) is not shown.
