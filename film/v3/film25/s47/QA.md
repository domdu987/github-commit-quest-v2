# QA s47 (film 25, g 1424-1492)

## Render
- 81 frames g 1418-1498 (row g 1424-1492 + handles), 58.4 s wall / frame mean (min 52.6, max 66.2), 115.3 s CPU, samples 24 thr 0.02 scale 0.75, OIDN, 2 procs x 2 threads
- post: t2lib.post_take (set sharpen + clarity, gentle grade, exposure/WB smoothed over the take)

## light_metrics
```
take.mkv (3 fr)                        luma 0.473 p1 0.077 p99 0.848 lc 0.0332 sat 0.438 chroma 24.8 a +3.2 b +5.8 p98 1.00 blue 0.38 warm 0.52 neut 0.08 M 69  PASS  (guides off: p99,lc,chroma)
```

## qa_jitter
```
overall median jitter px 0.36
```

## qa_auto
PASS

## Camera
- camera: first -> last frame of the row: subject distance 28.8 -> 26.3 D (scale +9.2 %), lateral camera travel 8.8 D = 16 % of the frame width per second (frame width 24.3 D at the subject)
