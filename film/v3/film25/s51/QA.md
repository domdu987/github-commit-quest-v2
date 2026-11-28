# QA s51 (film 25, g 1526-1557)

## Render
- 43 frames g 1520-1562 (row g 1526-1557 + handles), 60.6 s wall / frame mean (min 46.9, max 90.3), 113.3 s CPU, samples 20 thr 0.02 scale 0.75, OIDN, 2 procs x 2 threads
- post: t2lib.post_take (set sharpen + clarity, gentle grade, exposure/WB smoothed over the take)

## light_metrics
```
take.mkv (1 fr)                        luma 0.469 p1 0.056 p99 0.796 lc 0.0233 sat 0.414 chroma 23.2 a +3.3 b +2.0 p98 0.95 blue 0.47 warm 0.40 neut 0.02 M 57  PASS  (guides off: p99,lc,chroma,blue_frac,warm_frac,M)
```

## qa_jitter
```
overall median jitter px 2.0
```

## qa_auto
PASS

## Camera
- camera: first -> last frame of the row: subject distance 19.2 -> 14.3 D (scale +34.8 %), lateral camera travel 2.0 D = 12 % of the frame width per second (frame width 16.2 D at the subject)
