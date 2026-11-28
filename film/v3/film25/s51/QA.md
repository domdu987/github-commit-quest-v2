# QA s51 (film 25, g 1526-1557)

## Render
- 43 frames g 1520-1562 (row g 1526-1557 + handles), 55.2 s wall / frame mean (min 50.0, max 75.5), 104.2 s CPU, samples 20 thr 0.02 scale 0.75, OIDN, 2 procs x 2 threads
- post: t2lib.post_take (set sharpen + clarity, gentle grade, exposure/WB smoothed over the take)

## light_metrics
```
take.mkv (1 fr)                        luma 0.480 p1 0.103 p99 0.912 lc 0.0284 sat 0.453 chroma 31.4 a +1.7 b +3.3 p98 0.89 blue 0.36 warm 0.30 neut 0.07 M 70  PASS  (guides off: p1,lc,warm_frac)
```

## qa_jitter
```
overall median jitter px 0.67
```

## qa_auto
PASS

## Camera
- camera: first -> last frame of the row: subject distance 19.0 -> 17.5 D (scale +8.6 %), lateral camera travel 12.3 D = 74 % of the frame width per second (frame width 16.0 D at the subject)
