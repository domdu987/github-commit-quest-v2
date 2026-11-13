# s11 QA: film 4, shots 11 + 12 (years 2 and 3: crack, plaster, crack, plaster), pagoda set v2, DAY -> SUNSET

Delivered: `take.mkv` = `frames/g_0775.png .. g_1061.png` (287 frames, 720x1280, 12 samples, 2 threads, no captions / audio).
g 782..1054 = shots 11-12 ([g0, g1) = [782, 1055)); g 775..781 in-handle, g 1055..1061 out-handle, rendered in 3D.
Inside: 10-frame dissolve 11 -> 12 (DAY -> SUNSET, time passing), mixed g 915..924 (raw 11c to g 926, 12a from g 913).
meta.json: first_g 775, n_frames 287, transition_in 10-frame dissolve, transition_out 10-frame dissolve, sub_ranges, frame_source.
Also cues.json, contact.jpg, compare.jpg (one frame per sub-shot beside ref a t0049 / t0051 / t0053 / t0061 / t0063 / t0065).
Scripts: `shot.py` loads the engine `../s09/shot.py`; `../s09/deliver.py s11`, `../s09/qa.py s11` (-> `work/qa.txt`).
Render: DAY sub-shots in one process, SUNSET sub-shots in another (one preset per Take build).

## Timing (captions_bankky.json, g = round((t + 0.1) * 30))
| sub | g | what | ref a |
|---|---|---|---|
| 11a | 782-835 | DAY low wide on both buildings; quake 2 from g 784 ("ปีที่สอง" 786), strength 0.75, camera shake; pagoda sways two spans (0.85 D by g 810, "เจดีย์เมาโยก" 800); snap toward the pagoda g 816-824, lands on "สองคืบ" 825 | t0049 |
| 11b | 836-876 (cut) | crack insert at the tower's nailed joint (iron plate), muffled shake; the hairline crack appears g 856 ("ร้าวเป็น" 856) with a small camera jolt g 855-864 | t0051 |
| 11c | 877-919 (cut) | medium from below: the master on a plank scaffold (added by the take) plasters the joint, trowel tip pinned to the crack (strokes every 12 f); patch 1 appears g 897 ("ฉาบปูนปิด" 889); expression determined -> smug | t0053 |
| 12a | 920-971 (dissolve 915-924) | SUNSET wide between the courtyard banners: quake 3 ("ปีที่สาม" 922), strength 1.0, strongest shake; three spans (1.2 D, the cap); snap g 952-959 onto the pagoda, lands on "สามคืบ" 960 | t0061 / t0063 |
| 12b | 972-1015 (cut) | close: the crack now finger-wide through the old patch ("รอยร้าวกว้าง" 973); the master (worried, sweat) reaches in, his pointing finger pinned to the crack, pokes in g 994-1003 ("จนยัดนิ้วได้" 996), pulls back | t0063 |
| 12c | 1016-1054 (cut) | medium low against the sunset sky: he plasters over it again ("เขาก็ฉาบทับ" 1018); patch 2 lands g 1036, "อีกชั้น" 1041; smug | t0065 |
Framing changes: 782, 816-824, 836, 877, 915-924, 952-959, 972, 1016: gaps 1.1-1.5 s.

## Staging / checks (`work/qa.txt`)
| sub | master head w px | centre x | centre y (H) | below 880 | edge | pin error |
|---|---|---|---|---|---|---|
| 11c | 116-132 | 336-350 | 0.40-0.42 | none | none | 0.000 D (trowel tip) |
| 12b | 198-240 | 287-315 | 0.42-0.44 | none | none | 0.000 D (finger) |
| 12c | 130-143 | 294-304 | 0.40-0.42 | none | none | 0.000 D (trowel tip) |
11a / 11b / 12a: no actors. Mouth closed in every frame (determined / smug / worried). head_flip False (DAY south-west key,
SUNSET west key: screen-left in all these views).
Popcheck: cuts 835->836, 876->877, 971->972, 1015->1016; inside shots: g 803 (quake-2 shake peak), 855-860 (the crack jolt, intended),
870 (shake), 981 (12b shake). Near-still: g 877, 1014, 1016 (single frames). No black / magenta frames, no retried frames,
no warnings in `work/finalA_s11.log` / `work/finalB_s11.log`.
Crack / plaster continuity: crack 0 -> 1 at g 856, patch 1 from g 897; from g 920 crack 2 runs through patch 1; patch 2 from g 1036.

## Colour (hue_report.row)
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s11 11a (g 782-835)                             5.7   18.3    0.1    0.0    0.0   69.2    1.8    4.8  0.55 0.66 0.05
s11 11b (g 836-876)                            10.1   43.8    0.0    0.0    0.0   39.7    0.8    5.6  0.37 0.51 0.30
s11 11c (g 877-919)                            11.3   25.9    0.1    0.4    0.0   52.4    2.8    7.1  0.38 0.50 0.25
s11 12a (g 920-971)                            62.1   12.6    0.1    0.0    0.0    1.8    6.3   17.1  0.54 0.72 0.02
s11 12b (g 972-1015)                           59.2    5.4    0.0    0.0    0.0    7.3   10.5   17.5  0.38 0.57 0.11
s11 12c (g 1016-1054)                          55.9   10.7    0.0    0.0    0.0    2.5   20.7   10.2  0.44 0.55 0.24
s11 all (g 775-1061)                           34.9   17.3    0.1    0.0    0.0   30.5    6.6   10.6  0.45 0.59 0.15
ref a t0049 t0051 t0053 t0061 t0063 t0065      52.3   35.4    1.5    0.0    0.0    3.0    1.7    6.2  0.52 0.56 0.18
```
SUNSET magenta 10-17 comes from the set's pink-orange sunset sky and the sunlit plaster (the set's SUNSET crack_insert still is
19.5; ref t0061 / t0063 have the same pink sky); the shade stays blue-violet (see compare.jpg). DAY shots are sky-blue exteriors.

## Seconds per frame
10.7 s wall / 20.7 s CPU mean (11a 7.3, 11b 11.6, 11c 10.8, 12a 9.7, 12b 14.4, 12c 11.8 wall), two processes x 2 threads.

## Differences from the plan / the reference
- The scaffold (poles, ledgers, plank, guard rail, plaster bucket) in front of the joint is added by the take (no scaffold in
  the set); the master stands on it at z 9.1 for 11c, 12b, 12c.
- 11a / 12a are custom low wides (not the exact two_buildings camera) so they differ from 9a; the snap-ins go to the pagoda.
- No visible sun disc in 12a (the set's sunset sun sits at azimuth 200, west-south-west, outside these north-facing views).
- 12b: the finger is the master's (pinned hand, pointing shape), the plan's "finger poked into the wide crack".
