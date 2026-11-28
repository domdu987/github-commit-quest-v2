# QA s40 (film 25, g 1184-1226)

## Render
- 55 frames g 1178-1232 (row g 1184-1226 + handles), 63.4 s wall / frame mean (min 51.9, max 128.2), 110.3 s CPU, samples 20 thr 0.02 scale 0.75, OIDN, 2 procs x 2 threads
- post: t2lib.post_take (set sharpen + clarity, gentle grade, exposure/WB smoothed over the take)

## light_metrics
```
take.mkv (2 fr)                        luma 0.467 p1 0.100 p99 0.797 lc 0.0227 sat 0.432 chroma 26.4 a +0.5 b +2.0 p98 0.99 blue 0.46 warm 0.30 neut 0.01 M 67  PASS  (guides off: p1,p99,lc,chroma,blue_frac,warm_frac)
```

## qa_jitter
```
overall median jitter px 0.32
```

## qa_auto
PASS

## Camera
- camera: first -> last frame of the row: subject distance 52.6 -> 62.1 D (scale -15.3 %), lateral camera travel 26.0 D = 52 % of the frame width per second (frame width 35.5 D at the subject)
