# GRADE v1.1 (BRIEF_POLISH.md, "How v1.1 is built", step 2)

Sharp picture: no depth-of-field blur (client decision). The delivered v1.1 (`deliver/film_v1_1_sharp_thai.mp4`) is this grade applied to the sharp v1 conform frames by `make_sharp.py` in this folder, which grades, burns the captions and encodes in one pass.

`PROJ/v3/film/out_v11/grade.py`, entry point `grade_frame(img, g) -> img` (PIL RGB 720x1280 in and out, g = film frame 0..1964).
PROJ = `__PROJ__`.
I built and measured it on the v1 conform (`PROJ/v3/film/out/frames/g_%04d.png`, no captions). Nothing outside `out_v11/` was written.

## How to run it (1965 frames)
The function has no state, so frames can be graded in any order and in any number of processes. Each process uses one OpenCV thread (`cv2.setNumThreads(1)`).
```
cd PROJ/v3/film/out_v11
nohup python3 grade.py frames graded 0 1964 3 > grade0.log 2>&1 &
nohup python3 grade.py frames graded 1 1964 3 > grade1.log 2>&1 &
nohup python3 grade.py frames graded 2 1964 3 > grade2.log 2>&1 &
```
The arguments are SRC DST first last step. The run can be resumed: a frame whose output file exists is skipped, and each file is written to a temp name and then renamed. Use 3 processes, which leaves a core for the other worker.
- **Time per frame:** 0.21-0.44 s for one process alone on this machine, plus about 0.25 s to save a default PNG. With 3 processes in parallel, the 448-frame test sample took 69 s wall clock, about 0.47 s per frame per process with fast PNG saving. **All 1965 frames should take about 5-7 minutes with 3 processes.**
- **Dependencies:** numpy, opencv (cv2) and PIL only. There are no external files at run time; the take and join table is copied into the script.

## Stages and parameters
All settings are at the top of grade.py.

| # | Stage | What it does | Parameters |
|---|---|---|---|
| 1 | Per-shot correction | Per take: gain, black lift, gamma, contrast around luma 0.42, saturation, white balance (near-white fills are excluded), a warm key on pale lavender walls (hue 185-300, S < 0.4, V > 0.35; shaded sides stay cool), a darker lower frame. The settings **cross-fade over every dissolve with the conform's own weight** (smoothstep((g-a+1)/(L+1)), the same ranges as joins.json), and linearly over the s24>s25 wipe (1785-1790) and the s25>s26 flash (1868-1876). Hard cuts switch on the cut. | `SHOT` dict; see the table below |
| 2 | Tone curve | One S-curve on luma for the whole film. It preserves hue: the pixel is scaled by Y'/Y, and a pixel that would go over 1 is scaled down rather than having one channel clipped. | knots (0,0) (0.06,0.052) (0.15,0.118) (0.35,0.40) (0.65,0.785) (0.85,0.938) (1,0.985), monotone cubic |
| 3 | Saturation | Global saturation around luma, vibrance style: the boost is multiplied by (1-0.65 S), and near-white fills get none. | `SAT_GLOBAL` 1.18 |
| 4 | Haze | Exteriors only. Warm airlight (1, 0.90, 0.76) is blended onto "far" pixels: pixels close to their row's median colour (sky, sea, horizon, distant hills; characters and props differ from it). The blend follows a vertical profile around the horizon height (sigma 0.16 H above, 0.07 H below). | s08 0.16 at y 0.40 H, s16 0.10 at 0.38 H, s23 0.10 at 0.44 H |
| 5 | Bloom | **Hot sources:** pixels with max channel 0.955-0.985 in the input. They are grouped into blobs (pale regions, max > 0.80). Each blob's 4-px rim is tested for dark ink (luma < 0.30). A blob ringed by ink (a face or a hand) keeps 15 % of its glow (`BLOOM_FACE`); a lamp globe, window or sun patch keeps all of it. **Fix round:** this was not enough (see the last section): the glow is now also gated by saturation and removed inside near-white fills. Glow radii are sigma 8 / 26 / 80 px with gains 0.80 / 0.70 / 0.30, and the glow fades out deep inside large hot areas (density 0.60-0.92). **Bright areas:** max 0.78-0.97 after the curve, a weak glow at sigma 40 / 130 px with gains 0.07 / 0.07. It is suppressed where the bright density within 18 px is 0.42-0.78, so print on white paper and signs is not lifted. Both glows are computed at quarter size, tinted warm (1, 0.94, 0.84) and added with a screen blend. **There is no frame-adaptive normalisation of any kind**, so the bloom cannot pump. | per-shot gain `bloom`: s08 0.55, s16 0.7, s24 0.8, others 1 |
| 6 | Fog bank (s23) | A pale #c9bfd0 band on the horizon (y 600->612 as the camera pushes). It grows from 40 to 120 px tall over g1677-1719 (55.9-57.3 s) with a smoothstep, fades in over g1671-1681, has a soft top, peaks at alpha 0.80, and has a slow, faint x-modulation (plus or minus 16 %) so it is not a ruled stripe. A colour matte puts it behind near objects. The fog covers violet sky, the horizon glow, hills and sea. Near objects stay in front: ink, poles and houses (V < 0.36), the face (V > 0.87), the hat and hair (warm, S > 0.45), the navy stripes (S > 0.6). Dark and bright objects are grown by 2 px. | `FOG_*`, `_fog_matte` |
| 7 | Red protect | Strong reds (hue within 10-22 deg of red, S > 0.45-0.65, V > 0.15-0.35) keep their v1 hue and saturation and take the graded luminance. | `red` 0.8 |
| 8 | White protect | Flat near-white fills (max > 0.74-0.86, S below `wsat`): faces, hands, paper, lamp globes, the clock dial. They keep their v1 colour and value (glow from outside is allowed up to +0.02). This stops tint and saturation landing on them and keeps paper under the captions from getting brighter. It is off in s19-s21, which have no faces, so the pale walls can be warmed. | `wprot` 1 (0 in s19-s21), `wsat` 0.30 (0.13 in s16 so its lavender sky is still corrected) |
| 9 | Soft ceiling | Per pixel and hue preserving: a max channel above 0.965 is rolled into 0.965..0.993, so 1.0 maps to 0.985. | `CEIL_KNEE` 0.965, `CEIL_MAX` 0.993 |

Per-shot settings (all others are at the defaults):

| Take | Settings | Why |
|---|---|---|
| s08 | gain 0.93, sat 0.94, bloom 0.55, haze 0.16 | the sunny sand was already bright (val 0.71); keep its texture |
| s15 | sat 0.93 | the kitchen is already all warm |
| s16 | gain 0.88, contrast 1.30, gamma 1.08, sat 1.60, wb R 1.04 / B 0.95, lower frame -22 %, haze 0.10 | washed out |
| s19 | walls 0.80, sat 1.12, wb R 1.03 / B 0.95, white protect off | cold diagram |
| s20 | walls 0.85, sat 1.32, wb R 1.05 / B 0.93, white protect off | cold diagram |
| s21 | walls 0.75 (lamp colour 1 / 0.87 / 0.69), sat 1.60, wb R 1.05 / B 0.92, contrast 1.06, white protect off | coldest shot |
| s23 | haze 0.10, plus the fog bank | fog bank not readable |
| s24 | bloom 0.8 | night |
| s25 | lift 0.06, gamma 0.88, gain 1.04, sat 1.40 | too dark to read |

## Numbers (v1 against graded)
**Sample:** 448 frames. These are the 131 half-second stills g = 6 + 15k (the frames score.py samples), every 2nd frame of s16, s19, s20, s21, s23 and s25 (the review's hue rows), 10-frame strips at 300-309, 735-744, 1040-1049, 1460-1469 and 1885-1894, the dissolves 1007-1019 and 1415-1423, and every 3rd frame of the fog.
**Tools:** score.py's own `picture_stats` and `heads.detect_heads` (heads with eyes, as in score.py) on the 131 stills, which gives medians like the scorecard. I measured the v1 PNGs the same way, so both columns are captionless PNGs. The review measured the MP4 with captions: contrast 0.498, V>0.95 0.012, top 82, middle 103, sat 0.395, head V 0.996. The hue rows use `PROJ/v3/tools/hue_report.py`'s `stats`.

| Metric | Target | v1 | **graded** |
|---|---|---|---|
| Contrast, luma p95-p5 | 0.60-0.75 | 0.497 | **0.623** |
| Share of pixels with V > 0.95 | 0.02-0.09 | 0.012 | **0.036** |
| Top-third mean luma | 85-135 | 83.7 | **93.3** |
| Middle-third mean luma | 105-150 | 104.4 | **118.2** |
| Saturation mean | 0.40-0.60 | 0.392 | **0.410** |
| Head fill V | <= 0.995 | 1.000 (0.996 on the MP4) | **0.984** |
| Head fill S | <= 0.055 | 0.043 | 0.036 |
| Black point, luma p1 | 0.08-0.12 | 0.125 | 0.101 |
| Colourfulness | 55-100 | 55.3 | 66.4 |
| Canny edge density | 0.050-0.110 | 0.0525 | 0.0613 |
| Thin dark lines | 0.03-0.20 | 0.0513 | 0.0647 |
| Bottom-third luma | 60-105 | 81.6 | 90.9 |

Hue rows (share of chroma, %; band red 30-41, orange 22-38, blue 14-30, violet 0-5, magenta 0-10, sat 0.38-0.48, val 0.45-0.63, dark 0.08-0.15):

| Set | | red | orange | blue | violet | magenta | sat | val | dark | out of band |
|---|---|---|---|---|---|---|---|---|---|---|
| s16 | v1 | 24.4 | 4.1 | 64.8 | 1.2 | 5.4 | 0.24 | 0.65 | 0.01 | red, orange, blue, sat, val, dark |
| | graded | 33.3 | 6.2 | 57.0 | 1.3 | 1.9 | 0.31 | 0.67 | 0.07 | orange, blue, sat, val, dark |
| s19 | v1 | 27.7 | 22.5 | 46.0 | 0.4 | 3.0 | 0.36 | 0.47 | 0.12 | red, blue, sat |
| | graded | 31.6 | 39.3 | 27.4 | 0.4 | 0.9 | 0.38 | 0.53 | 0.12 | orange (39.3) |
| s20 | v1 | 11.7 | 18.8 | 62.1 | 0.9 | 6.3 | 0.35 | 0.49 | 0.10 | red, orange, blue, sat |
| | graded | 27.5 | 33.7 | 31.3 | 1.2 | 6.2 | 0.35 | 0.55 | 0.10 | red (27.5), blue (31.3), sat |
| s21 | v1 | 15.5 | 8.9 | 66.7 | 1.4 | 6.8 | 0.29 | 0.52 | 0.12 | red, orange, blue, sat |
| | graded | 38.6 | 37.4 | 19.3 | 1.1 | 2.2 | 0.34 | 0.60 | 0.12 | sat (0.34) |
| s23 | v1 | 21.9 | 7.9 | 3.9 | 55.5 | 10.7 | 0.31 | 0.49 | 0.01 | 7 of 8 |
| | graded | 23.7 | 5.8 | 3.1 | 56.8 | 10.5 | 0.32 | 0.58 | 0.01 | 7 of 8 (the violet sky is kept) |
| s25 | v1 | 29.2 | 16.2 | 45.2 | 1.7 | 4.7 | 0.34 | 0.33 | 0.33 | red, orange, blue, sat, val, dark |
| | graded | 27.8 | 16.7 | 43.8 | 2.5 | 6.2 | 0.33 | 0.49 | 0.08 | red, orange, blue, sat |
| Office shots (1-7, 9-14, 17-18), 0.5 s | v1 | 36.6 | 28.4 | 21.0 | 1.1 | 4.4 | 0.41 | 0.49 | 0.13 | in band |
| | graded | 35.6 | 31.6 | 18.6 | 0.9 | 3.7 | 0.43 | 0.54 | 0.15 | **in band** |
| Whole film, 0.5 s | v1 | 32.7 | 24.5 | 31.0 | 2.4 | 4.3 | 0.39 | 0.49 | 0.12 | blue |
| | graded | 33.8 | 29.9 | 24.9 | 2.4 | 3.3 | 0.41 | 0.55 | 0.13 | **in band** |

**Caption band** (rows 850-960, 0.5 s sample; `grade_test/capband.txt`):
- **Mean luma:** v1 0.346, graded 0.385.
- **Share of pixels with luma > 0.85:** v1 0.4 %, graded 0.7 %.
- **Worst single frame:** g936, the s14 forecast sheet (warm paper, S 0.2), where 12 % of the band rises above luma 0.85.
- The white-protect stage keeps white paper at its v1 value. I did not use a band-shaped limit, because it would show as a stripe on paper and sky.

**Stability** (`grade_test/flicker.py`, `run_final.log`). The grade's gain (graded/v1 frame mean) moves smoothly in every strip, and the frame-to-frame change of the grade itself is about 0.3-0.45 of the change of the picture:
- **300-309, lamps in shot:** gain 1.059-1.064.
- **735-744:** a bright object enters at g740 (hot pixels 0.01 % -> 4.95 %). The graded mean goes 111.4 -> 111.3 -> 110.9 while v1 goes 97.8 -> 101.2 -> 100.4. The grade does not react against the content, so there is no pumping.
- **1040-1049, s16:** gain 0.959-0.990.
- **1460-1469, s20 speed lines:** gain 1.130-1.146.
- **Dissolve s15 > s16 (1007-1019):** the gain crosses smoothly from 1.097 to 0.971.
- **Dissolve s19 > s20 (1415-1423):** gain 1.125-1.145.

## What I looked at (full size)
- **Before/after:** `grade_test/pairs/pair_gNNNN.jpg` puts v1, graded and the nearest reference still side by side for 17 shots: g42 (shot 2), 84 (3), 167 (4), 291 (6), 418 (8), 627 (10), 828 (12), 966 (15), 1045 (16), 1170 (18), 1300 (19), 1480 (20), 1546 (21), 1719 (23), 1755 (24), 1840 (25), 1922 (26).
- **Strips:**
  - `strip_0735_0744.jpg` (v1 over graded)
  - `strip_0300_0309_graded.jpg`, `strip_1040_1049_graded.jpg`, `strip_1460_1469_graded.jpg`
  - `dissolve_s15_s16_graded.jpg`, `dissolve_s19_s20_graded.jpg`
  - `fog_s23_graded.jpg`
- **Faces and hands:** they stay flat and neutral (head fill 0.984, S 0.036). The lavender and cream casts that showed in early tries on s16 and the office faces are gone.
- **Lamps:** the globes now glow onto the shade and ceiling.
- **Text:** the forecast sheet, the label ทางด่วนพายุ, the LONG ISLAND sign, the 100 km/h sign and the WEATHER BUREAU board all stay readable.
- **The red line** keeps its hue.
- **The s23 fog bank** reads as a pale bank on the horizon, behind the man's head, the umbrella and the poles.

## What is still wrong or left at v1
- **Larger ghost storms in s21:** not done. They need sprites that track the corridor through the whip pull-out, which is not cheap; the shot stays as in v1 apart from the grade.
- **Grain:** not added. The edge-density measure is already in range (0.061). A static grain reads as dirt on the lens, an animated one shimmers, and at 2-3 % opacity it would not cross score.py's Canny thresholds (60/140) anyway.
- **Hue rows outside the band:**
  - s16 is still blue (57 %) and sat 0.31: it is a grey drizzle exterior. More warming turns the sky brown.
  - s19 orange 39 is just over 38.
  - s20 red 27.5 and blue 31 are just outside the band.
  - s25 blue 44 is the night-storm light; it is now readable (val 0.49, dark 8 % against 33 %).
  - s23 stays violet, as planned.
- **Margins on two targets are small:** contrast 0.623 and saturation 0.410. Re-measure the delivered film with score.py and, if needed, raise the 0.65 knot of `CURVE` or `SAT_GLOBAL`.
- (Fixed in the fix round, see below: bloom on characters, which had turned the ink inside every face grey.)
- **Fog bank fringe:** it leaves a thin yellow fringe (2-4 px) of the original horizon glow round the house roofs right of the sign.

## Fix round (after the two reviews; the bundled `grade.py` is this version)

This file was written before the fix round; the section below records what changed. The bundled `grade.py` reproduces the delivered graded frames bit for bit.

| Fault (found by) | Change in `grade.py` | Parameters |
|---|---|---|
| Bloom turned the black ink inside every face grey: face-ink luma +0.07 to +0.10 in every take with faces except s16 (artifact hunter); the 4-frame ghost face in s11 g740-743 was the worst case (look reviewer) | `_fill_inner(x0)`: the inside of near-white flat fills (faces, hands, paper, globes), closed over their dark features, gets no glow at all: `stage_bloom` returns `x + (y - x) * (1 - fill_inner)` | `FILL_V, FILL_S = 0.85, 0.15` (fill = max > 0.85 and saturation < 0.15 in the input frame); `FILL_CLOSE = 61` px (closes over smeared eyes and mouths), `FILL_HOLE = 20000` px (larger enclosed features such as a close-up eye, 70 x 90 px, count as inside), `FILL_ERODE = 5`, `FILL_BLUR = 2.0` |
| The sunlit orange floor flickered (s11 g774-788, opening g86-90): it sits on the hot threshold and its per-frame blob test switched on and off (artifact hunter) | hot-source weight multiplied by `1 - smoothstep(HOT_SAT, saturation)`: only pale sources are hot | `HOT_SAT = (0.20, 0.35)` |

`BLOOM_FACE` (15 %) still applies outside the fills.

## Files
- `grade.py`: the grade. As a script it grades a folder (see above).
- `grade_test/`:
  - `measure.py` (score.py picture stats on the sample), `hue_rows.py`, `capband.py`, `flicker.py`
  - `run_sample.py` (grades the sample with 3 processes), `some.py`, `pair.py`, `strip.py`
  - `run_final.log` (all final numbers), `m_v1.json`, `m_graded.json`
  - `sample/` (the 448 graded test frames), `pairs/`, strips
