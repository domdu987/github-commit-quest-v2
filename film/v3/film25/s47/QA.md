# QA s47 (film 25, g 1424-1492)

## Render
- 81 frames g 1418-1498 (row g 1424-1492 + handles), 61.7 s wall / frame mean (min 48.9, max 166.5), 106.1 s CPU, samples 20 thr 0.02 scale 0.75, OIDN, 2 procs x 2 threads
- post: t2lib.post_take (set sharpen + clarity, gentle grade, exposure/WB smoothed over the take)

## light_metrics
```
take.mkv (3 fr)                        luma 0.480 p1 0.056 p99 0.885 lc 0.0335 sat 0.434 chroma 26.4 a +2.5 b +3.4 p98 0.78 blue 0.36 warm 0.55 neut 0.02 M 70  PASS  (guides off: p99,lc,chroma,sat_p98)
```

## qa_jitter
```
overall median jitter px 0.35
```

## qa_auto
PASS

## Camera
- camera: first -> last frame of the row: subject distance 19.0 -> 10.4 D (scale +83.0 %), lateral camera travel 5.0 D = 11 % of the frame width per second (frame width 19.2 D at the subject)
