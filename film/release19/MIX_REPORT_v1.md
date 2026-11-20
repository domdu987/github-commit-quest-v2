# Mix report harrison_v1.mp4

- Integrated loudness: **-12.2 LUFS** (target -14..-11): PASS; LRA 2.3 LU
- True peak: **-1.10 dBTP** (limit -1.0): PASS (limiter 0.850)
- Voice RMS -14.4 dB (target -14.4), music RMS -31.0 dB (target -31.0; music_B trimmed to 72 s, 1.5 s fade-out, -3 dB duck under speech), SFX stem RMS -42.7 dB
- Point effects: 18 placed, 24 dropped for spacing (>= 2.0 s apart); min gap 2.07 s
- Beds: 14, prop loops: 6; SFX under speech ducked 6 dB (3 dB if >= 3 s; laugh/gasp/cheer a further 4 dB)
- In-shot frame-diff (90x160 grey, deliver.py method): median 4.69, p90 12.26 over 2134 pairs (target 4 / 12)
- Frames: 2160, dissolve blends 141, missing 0; planned cuts g [57, 110, 262, 466, 545, 661, 773, 986, 1190, 1280, 1581, 1933, 2028, 2086]

## Point effects
| t | file | peak dB | take |
|---|---|---|---|
| 1.33 | glint_shimmer | -27 | s01 |
| 3.73 | timber_creak | -33 | s03 |
| 8.93 | water_bail | -28 | s05 |
| 11.00 | wave_crash | -22 | s05 |
| 14.63 | whoosh_fast | -31 | s06 |
| 20.10 | belly_laugh | -27 | s08 |
| 25.77 | hall_laugh | -25 | s10 |
| 28.73 | file_rasp | -28 | s11 |
| 31.73 | whoosh_fast | -31 | s12 |
| 35.80 | glint_shimmer | -27 | s14 |
| 39.03 | glint_shimmer | -27 | s15 |
| 45.60 | whoosh_fast | -31 | s17 |
| 49.03 | crowd_cheer | -30 | s19 |
| 55.65 | quadrant_clank | -29 | s21 |
| 59.00 | coins_half | -25 | s22 |
| 62.80 | door_creak | -24 | s23 |
| 67.60 | sweat_pop | -26 | s25 |
| 70.23 | coins_bag | -23 | s26 |
