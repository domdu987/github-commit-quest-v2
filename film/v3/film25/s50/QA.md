# QA s50 (film 25, g 1493-1525)

## Render
- 45 frames g 1487-1531 (row g 1493-1525 + handles), 64.0 s wall / frame mean (min 59.8, max 69.3), 126.2 s CPU, samples 24 thr 0.02 scale 0.75, OIDN, 2 procs x 2 threads
- post: t2lib.post_take (set sharpen + clarity, gentle grade, exposure/WB smoothed over the take)

## light_metrics
```
take.mkv (2 fr)                        luma 0.466 p1 0.075 p99 0.823 lc 0.0444 sat 0.426 chroma 29.4 a +2.0 b +2.7 p98 1.00 blue 0.40 warm 0.39 neut 0.06 M 78  PASS  (guides off: p99,warm_frac)
```

## qa_jitter
```
overall median jitter px 0.7
```

## qa_auto
PASS

## Camera
- camera: first -> last frame of the row: subject distance 14.3 -> 12.8 D (scale +11.4 %), lateral camera travel 1.8 D = 17 % of the frame width per second (frame width 9.6 D at the subject)
