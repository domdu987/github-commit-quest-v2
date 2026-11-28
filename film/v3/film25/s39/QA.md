# QA s39 (film 25, g 1135-1183)

## Render
- 61 frames g 1129-1189 (row g 1135-1183 + handles), 84.9 s wall / frame mean (min 60.8, max 138.4), 128.9 s CPU, samples 20 thr 0.02 scale 0.75, OIDN, 2 procs x 2 threads
- post: t2lib.post_take (set sharpen + clarity, gentle grade, exposure/WB smoothed over the take)

## light_metrics
```
take.mkv (2 fr)                        luma 0.470 p1 0.070 p99 0.812 lc 0.0186 sat 0.435 chroma 23.3 a +0.6 b +1.9 p98 1.00 blue 0.46 warm 0.32 neut 0.01 M 57  PASS  (guides off: p99,lc,chroma,blue_frac,warm_frac,M)
```

## qa_jitter
```
overall median jitter px 0.39
```

## qa_auto
PASS

## Camera
- camera: first -> last frame of the row: subject distance 47.5 -> 43.2 D (scale +10.0 %), lateral camera travel 0.6 D = 1 % of the frame width per second (frame width 34.3 D at the subject)
