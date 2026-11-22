# Film 18 v2 (oxclerk_v2.mp4): client fix "มุมกล้องของลอย / มุมกล้องมันสั่น" (2026-11-22)

## What changed vs v1
- 13 shots re-rendered: s03 s05 s06 s19 s20 s23 (team 5) and s11 s13 s14 s15 s21 s22 s24 (team 4). The other 12 takes, the narration, music, SFX and captions are unchanged. No fal calls were made.
- Floating fixes:
  - s03 (0:06): hovering siege-tent discs removed; 14 pennant poles lowered onto the ground.
  - s11 (0:29): soldiers planted, with contact shadows and props on the ground.
  - s20 (0:51.5): the detached warm pool is replaced by a contact shadow under the hooves; the hovering bundles now rest on the ground.
  - s21 (0:54): silhouettes stand on the ground, with contact shadows and light pools.
- Shake fixes: all camera sway and handheld noise removed (SHAKE=None, shk 0). Each shot has one eased dolly/truck, held punch-ins eased over 10 frames or more, and character bounce of 0.02 D at 1.8 Hz or less.
- Every re-rendered take passes ground_check (exit 0 / 0 FAIL); the reports are in qa/<shot>/QA_v2.md.
- Grade: COLOUR_SPEC v1.1 (grade.py DEFAULT settings, as film_mini.py grade). Captions are Kanit Black 88, outline 4, shadow 1.5, at \pos(360,900).

## qa_jitter on the whole film (film/qa_jitter.py release18/oxclerk_v2.mp4)
```
 50s shake   2.7px
overall median jitter px 0.39
```
v1 had 22 shake seconds (13-17 s, 33-39 s up to 7.4 px, 48-50 s, 54-62 s) and an overall median of 1.05 px.
The one remaining flagged second, 50 s (2.7 px), is the planned whip pan between s19 and s20 (whip-out at the end of s19, whip-in at the start of s20): a planned fast move, not camera shake.

## Audio (unchanged mix)
-12.2 LUFS, true peak -1.1 dBTP, 70.40 s.

## COLOUR_SPEC section 3 bands (graded frames, every 10th frame per shot)
shot     red  orange blue purple mag  sat  val  dark%
s01   33.5  20.7  41.7   1.9   2.0  0.49  0.64   2.6
s03    7.7  68.9   2.1   1.4   1.6  0.55  0.63   0.5
s04    7.7  70.9   1.0   0.9   1.1  0.61  0.65   0.6
s05   42.2  36.0   4.6  10.0   5.6  0.42  0.51  18.2
s06   12.5  26.2  51.3   5.0   4.8  0.41  0.57  11.7
s07   34.9  58.4   4.2   0.8   1.5  0.63  0.58  10.1
s08   38.4  21.1  20.9  10.6   8.8  0.45  0.56  25.6
s09   30.1  18.4  43.3   3.9   4.2  0.40  0.58  11.2
s10   37.6  18.2  35.2   4.1   4.8  0.44  0.48  17.3
s11   24.8  22.4  41.9   4.6   5.9  0.41  0.63  19.3
s12   31.2  16.9  46.4   1.9   3.2  0.45  0.62  16.3
s13   28.8  11.8  46.4   6.3   6.6  0.45  0.60   2.7
s14   22.7   9.6  55.5   4.6   7.6  0.56  0.58   9.0
s15   23.7  14.4  53.8   3.1   5.0  0.61  0.57  13.2
s16   39.8   7.9  37.9   6.0   8.4  0.49  0.51  10.6
s17   40.7  13.7  27.7   8.0   9.9  0.43  0.46  12.2
s18   12.8   4.7  74.6   4.0   3.9  0.56  0.45   4.9
s19   24.0   7.4  52.6   8.0   7.9  0.41  0.52   4.9
s20    4.7   2.1  90.7   1.2   1.1  0.56  0.52   2.9
s21   24.3  14.5  52.5   4.1   4.5  0.68  0.43  38.1
s22   44.0  18.0  32.5   2.2   3.1  0.55  0.68   3.6
s23   10.7   6.8  73.2   3.3   5.2  0.48  0.45  15.6
s24   17.2   8.6  65.5   4.3   4.4  0.51  0.61   2.3
s25    8.1  63.0   3.1   0.8   1.3  0.51  0.64   1.1
s26   34.8  40.6  17.2   3.8   3.4  0.49  0.59  10.4
FILM  25.8  25.9  36.8   4.1   4.2  0.50  0.57  10.5
target: red 30-41, orange 22-38, blue 14-30, purple 0-5, magenta 0-10, sat 0.38-0.48, val 0.45-0.63, dark 8-15

Why the film falls outside the band:
- Blue is high (film 36.8 %) and red is low (25.8 %). Film 18 is mostly NIGHT EXTERIORS (moonlit camp and wall, s09-s24), plus the DUSK and DAWN vista shots s03, s04 and s25, which run orange at 63-71 %. COLOUR_SPEC section 3 allows exteriors, map-like vistas and night shots to fall outside the bands when the reason is written in QA.md; this is that note.
- The interior-like shots (s01 yard, s05 market, s07, s08, s16, s17, s22, s26) sit at or near the red 30-41 % band.
- Saturation 0.50 is just above 0.48: it comes from the night-blue skies and fire (s14, s15, s21).
- Brightness 0.57 and dark share 10.5 % are inside the band.
