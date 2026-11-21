# Film 17 style board (Bertillon). Cycles CPU, 720x1280, 96 spp + OIDN denoise, no DOF.
Kit: ../bertillon.py, scenes: ../styleboard.py (`python3 styleboard.py <1|2|3> final out.png 96`), hue: ../hue_check.py. Light grade: saturation x1.18 only.
| still | render s | red | orange | blue | violet | magenta | sat | val | dark | shade hue |
|---|---|---|---|---|---|---|---|---|---|---|
| still1 measuring room | 131 | 53.5 | 33.2 | 6.4 | 1.1 | 3.1 | 0.43 | 0.48 | 0.15 | 233.5 (out, 240-260) |
| still2 records office | 176 | 54.1 | 31.0 | 13.8 | 0.1 | 0.7 | 0.54 | 0.53 | 0.08 | 241.1 (ok) |
| still3 reveal | 118 | 34.8 | 43.2 | 13.4 | 0.4 | 7.4 | 0.48 | 0.46 | 0.14 | 233.4 (out) |
Magenta <= 10 in all three. Misses: blue low in 1 (6.4), red/orange skew warm, sat a bit high in 2.
Known problems: window exterior and skylights are flat saturated blue; still 3 table cloth strongly blue; flat card people are plain blue silhouettes; no true shaded-pixel majority (direct light only, diffuse bounces 0).
