# QA s53 (film 25, g 1592-1635)

## Render
- 56 frames g 1586-1641 (row g 1592-1635 + handles), 66.8 s wall / frame mean (min 55.7, max 128.6), 121.9 s CPU, samples 20 thr 0.02 scale 0.75, OIDN, 2 procs x 2 threads
- post: t2lib.post_take (set sharpen + clarity, gentle grade, exposure/WB smoothed over the take)

## light_metrics
```
take.mkv (2 fr)                        luma 0.504 p1 0.099 p99 0.931 lc 0.0318 sat 0.428 chroma 27.4 a +1.3 b +4.4 p98 0.85 blue 0.35 warm 0.41 neut 0.04 M 71  PASS  (guides off: p1,lc,chroma,sat_p98)
```

## qa_jitter
```
overall median jitter px 0.28
```

## qa_auto
PASS

## Camera
- camera: first -> last frame of the row: subject distance 8.0 -> 7.3 D (scale +9.9 %), lateral camera travel 4.2 D = 47 % of the frame width per second (frame width 6.2 D at the subject)
