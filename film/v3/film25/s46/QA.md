# QA s46 (film 25, g 1396-1423)

## Render
- 34 frames g 1396-1429 (row g 1396-1423 + handles), 75.8 s wall / frame mean (min 62.8, max 130.8), 127.8 s CPU, samples 20 thr 0.02 scale 0.75, OIDN, 2 procs x 2 threads
- post: t2lib.post_take (set sharpen + clarity, gentle grade, exposure/WB smoothed over the take)

## light_metrics
```
take.mkv (1 fr)                        luma 0.468 p1 0.049 p99 0.828 lc 0.0272 sat 0.451 chroma 23.7 a +2.4 b +2.9 p98 0.86 blue 0.45 warm 0.53 neut 0.02 M 64  PASS  (guides off: p99,lc,chroma,M)
```

## qa_jitter
```
overall median jitter px 0.61
```

## qa_auto
PASS

## Camera
- camera: first -> last frame of the row: subject distance 23.1 -> 16.1 D (scale +43.4 %), lateral camera travel 1.5 D = 9 % of the frame width per second (frame width 19.5 D at the subject)
