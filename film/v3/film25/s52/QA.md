# QA s52 (film 25, g 1558-1591)

## Render
- 46 frames g 1552-1597 (row g 1558-1591 + handles), 91.4 s wall / frame mean (min 74.0, max 125.9), 162.6 s CPU, samples 20 thr 0.02 scale 0.75, OIDN, 2 procs x 2 threads
- post: t2lib.post_take (set sharpen + clarity, gentle grade, exposure/WB smoothed over the take)

## light_metrics
```
take.mkv (2 fr)                        luma 0.483 p1 0.075 p99 0.832 lc 0.0407 sat 0.434 chroma 31.2 a +1.3 b +4.8 p98 0.99 blue 0.40 warm 0.28 neut 0.03 M 83  PASS  (guides off: p99,warm_frac)
```

## qa_jitter
```
overall median jitter px 0.3
```

## qa_auto
PASS

## Camera
- camera: first -> last frame of the row: subject distance 5.9 -> 4.3 D (scale +38.0 %), lateral camera travel 6.0 D = 109 % of the frame width per second (frame width 5.0 D at the subject)
