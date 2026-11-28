# QA s47 (film 25, g 1424-1492)

## Render
- 81 frames g 1418-1498 (row g 1424-1492 + handles), 57.4 s wall / frame mean (min 48.0, max 73.7), 102.6 s CPU, samples 20 thr 0.02 scale 0.75, OIDN, 2 procs x 2 threads
- post: t2lib.post_take (set sharpen + clarity, gentle grade, exposure/WB smoothed over the take)

## light_metrics
```
take.mkv (3 fr)                        luma 0.470 p1 0.067 p99 0.869 lc 0.0302 sat 0.442 chroma 28.1 a +2.3 b +3.2 p98 0.92 blue 0.43 warm 0.34 neut 0.03 M 68  PASS  (guides off: p99,lc,warm_frac)
```

## qa_jitter
```
overall median jitter px 0.38
```

## qa_auto
PASS

## Camera
- camera: first -> last frame of the row: subject distance 24.8 -> 22.7 D (scale +9.2 %), lateral camera travel 8.6 D = 18 % of the frame width per second (frame width 20.9 D at the subject)
