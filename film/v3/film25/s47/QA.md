# QA s47 (film 25, g 1424-1492)

## Render
- 81 frames g 1418-1498 (row g 1424-1492 + handles), 61.5 s wall / frame mean (min 52.6, max 82.5), 114.4 s CPU, samples 24 thr 0.02 scale 0.75, OIDN, 2 procs x 2 threads
- post: t2lib.post_take (set sharpen + clarity, gentle grade, exposure/WB smoothed over the take)

## light_metrics
```
take.mkv (3 fr)                        luma 0.473 p1 0.068 p99 0.851 lc 0.0354 sat 0.439 chroma 25.8 a +2.3 b +3.1 p98 0.97 blue 0.41 warm 0.48 neut 0.04 M 68  PASS  (guides off: p99,lc,chroma)
```

## qa_jitter
```
overall median jitter px 0.36
```

## qa_auto
PASS

## Camera
- camera: first -> last frame of the row: subject distance 24.8 -> 22.7 D (scale +9.2 %), lateral camera travel 8.8 D = 19 % of the frame width per second (frame width 20.9 D at the subject)
