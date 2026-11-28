# QA s51 (film 25, g 1526-1557)

## Render
- 44 frames g 1520-1563 (row g 1526-1557 + handles), 59.8 s wall / frame mean (min 55.2, max 87.2), 116.4 s CPU, samples 24 thr 0.02 scale 0.75, OIDN, 2 procs x 2 threads
- post: t2lib.post_take (set sharpen + clarity, gentle grade, exposure/WB smoothed over the take)

## light_metrics
```
take.mkv (1 fr)                        luma 0.499 p1 0.116 p99 0.919 lc 0.0325 sat 0.429 chroma 28.9 a +2.0 b +3.9 p98 0.87 blue 0.37 warm 0.36 neut 0.11 M 71  PASS  (guides off: p1,lc,warm_frac)
```

## qa_jitter
```
0s shake   2.3px
overall median jitter px 1.62
```

## qa_auto
PASS

## Camera
- camera: first -> last frame of the row: subject distance 19.1 -> 17.6 D (scale +8.5 %), lateral camera travel 9.5 D = 57 % of the frame width per second (frame width 16.1 D at the subject)
