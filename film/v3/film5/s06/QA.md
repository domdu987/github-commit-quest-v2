# s06 QA: film 5, shot 6 (plan t 14.38-17.63, g 431..528), mine set (tunnel LAMP)

Delivered: `take.mkv` = frames g 424..535 (112 frames, 720x1280, 12 samples, 2 threads, denoise FAST), first_g 424.
g 424..430 in-handle, g 529..535 out-handle (both rendered in 3D, the camera keeps moving), so the conform can cut or dissolve (10 f).
Also `meta.json`, `cues.json` (6 cues), `contact.jpg`, `compare.jpg`, `work/qa.txt`. Scripts: `shot.py`, `lib5.py`, `deliver5.py`.

## Client rules
- No depth of field (`M.setup_dof(..., None, None, cam)` at build and before every render), no motion streaks.
- The cage alfie holds is ALWAYS the cast's 2D held cage: pose `prop_r="cage"` + `bird` (perch_sing, 3 notes, beak moving), bars drawn
  over the bird, so the canary is visibly inside the cage on its perch in every frame (alfie sprite 448-640 px/D). The set's 3D cage is hidden.

## Timing
| sub | g | what | ref a |
|---|---|---|---|
| 6a | 424-465 | eye level just below alfie's eyes (cam z 1.3): alfie (2.48 D) in a row with miner1 (3.32), miner3 (3.38) and the gaffer (3.31) behind; he glances up at the big men (g 440-456); slow push | t0037 |
| 6b | 466-497 (cut) | the height gag: opens on miner3's grinning face, tilt + pan down (g 470-488) to alfie looking up at him, determined, on "น้อยที่สุด" (g 478) | t0037 |
| 6c | 498-535 (cut) | medium on alfie and the cage side by side; he lifts the cage up beside his torso on "กับกรงนก" (g 510-519), cage swings, bird singing; push in | t0037 |
Framing changes g 431, 466, 498, out 529: 1.17, 1.07, 1.03 s.

## Staging (`work/qa.txt`)
| sub | head | width px | centre y (H) |
|---|---|---|---|
| 6a | alfie / miner1 / miner3 / gaffer | 155-180 / 147-168 / 152-175 / 119-132 | 0.52 / 0.42 / 0.40 / 0.46 |
| 6b | miner3 -> alfie (tilt) | 296-355 / 283-343 | 0.52 -> 0.23 / 0.76 -> 0.44 |
| 6c | alfie | 315-394 | 0.41-0.42 |
Heads above y 880 everywhere except 6b g 474-479: during the fast tilt down alfie's head enters from the bottom-left corner (6 frames).
Mouths closed (happy / determined / smirk / grinning, static). Lamps: alfie's belt lamp (hip), two miner lamps (keyed lamp_light).
Popcheck: pops only at the cuts 465/466, 497/498. No static runs, no black / magenta frames, no retried frames.

## Colour
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s06 shot 6a (g 424-465)                        11.3   12.7    0.8    0.2    0.0   54.6    9.1   11.4  0.34 0.43 0.05
s06 shot 6b (g 466-497)                         8.6   20.4    2.8    0.8    0.0   39.8   13.2   14.3  0.32 0.46 0.09
s06 shot 6c (g 498-535)                        13.6   14.4    0.7    0.0    0.0   53.9    9.0    8.5  0.35 0.45 0.07
s06 all (g 424-535)                            11.3   15.4    1.3    0.3    0.0   50.3   10.2   11.2  0.34 0.45 0.07
```
Blue-dominant tunnel (as s01); the magenta share (8-14) comes from the red tubs "37" and alfie's brick-red waistcoat, not from the shade.

## Seconds per frame
18.7 s wall / 35.5 s CPU mean (two processes x 2 threads); 6b is 40 CPU s (large close sprites).

## Differences from the plan
- Plan says tunnel_eye; I used custom eye-level cameras on the walkway (y 6-9) so the four actors stand in one row for the height comparison.
- 6b re-rendered once (start framing moved so miner3's face and alfie stay above the caption line except the 6-frame tilt pass).
