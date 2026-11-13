# s05 QA: film 5, shot 5 (plan t 10.50-14.38, g 315..430), mine set (tunnel LAMP)

Delivered: `take.mkv` = frames g 308..437 (130 frames, 720x1280, 12 samples, 2 threads, denoise FAST, no captions, no audio),
first_g 308. g 308..314 = in-handle for the 10-f dissolve from s01's 4d (mixed g 310..319; s01's out-handle covers 315..321);
g 431..437 = out-handle (5c push keeps moving). Also `meta.json`, `cues.json` (8 cues), `contact.jpg`, `compare.jpg`, `work/qa.txt`.
Scripts: `shot.py` (the shot), `lib5.py` (shared take machinery, same in s05/s06/s07), `deliver5.py` (frames, mkv, meta, cues, sheets, QA numbers).

## Client rules
- No depth of field: `M.setup_dof(scene, None, None, cam=...)` at build and before every render; no motion streaks (no whips). The ECU is
  sharp by framing (the lamp is a 1536 px/D sprite) not by blur.
- No cage in this shot (the set's 3D cage is hidden in all my takes; alfie carries the cast's 2D held cage in s06/s07).

## Timing (captions.json, narration at +0.10 s)
| sub | g | what | ref a |
|---|---|---|---|
| 5a | 308-354 | low angle (cam z 0.6-0.8, pitch 32-35 deg) looking inbye at the gaffer, lamp hanging in his right fist, left fist on hip; he hoists the lamp beside his helmet on "แค่ตะเกียง" (g 339-350, back_out); slow crane up; faint gas 1.2 (continuity from 4d) | t0013 |
| 5b | 355-397 (cut) | ECU of the raised lamp in his fist (his sleeve on the left): the flame flares from 1.15 to 2.0 on "ไฟยังสว่าง" (g 372-381), push in | t0045 / plan lamp_insert |
| 5c | 398-437 (cut) | low reverse angle looking outbye (bright pit bottom behind): the gaffer holds the bright lamp high, smug nod on "ปลอดภัย" (g 410-422), miner2 digging behind him; slow push | t0013 |
Framing changes g 315 (dissolve), 355, 398, out 431: 1.33, 1.43, 1.10 s.

## Staging (`work/qa.txt`)
| sub | head | width px | centre y (H) |
|---|---|---|---|
| 5a | gaffer | 196-209 | 0.42-0.46 |
| 5b | gaffer (ECU, face off-frame left, only the sleeve + fist) | - | - |
| 5c | gaffer / miner2 | 175-198 / 133-149 | 0.43-0.44 / 0.59-0.63 |
All heads above y 880. Mouths closed (smug flat bar; no quote in this shot). Lamps: keyed `lamp_light` at the held lamp's flame
(`prop_tip_r`, strength follows the flame), a soft key in 5b, miner2's lamp in 5c.
Popcheck: pops only at the cuts 354/355, 397/398. No static runs, no black / magenta frames, no retried frames, no clipped sprites.

## Colour (`hue_report.row`)
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s05 shot 5a (g 308-354)                        10.3    9.2    0.0    0.0    0.0   62.0   12.7    5.7  0.44 0.36 0.09
s05 shot 5b (g 355-397)                        14.6   27.1    0.0    0.0    0.0   42.7    6.9    8.7  0.38 0.41 0.06
s05 shot 5c (g 398-437)                        17.0   12.8    2.0    0.0    0.0   51.4    9.1    7.6  0.39 0.41 0.07
s05 all (g 308-437)                            13.8   16.4    0.6    0.0    0.0   52.2    9.6    7.3  0.41 0.39 0.07
```
Blue-dominant underground by the set's design (same as s01's tunnel shots, blue 38-72); shade blue, magenta 5.7-8.7 (never a magenta cast).
The ref (a red throne room) is warmer; the set's LAMP look is kept for continuity with s01.

## Seconds per frame
16.5 s wall / 31.8 s CPU mean (two render processes of 2 threads sharing 4 cores).

## Differences from the plan
- The ECU uses the gaffer's own 2D `flame_lamp` (the lamp he holds) at 1536 px/D, not the set's 3D insert lamp on its chain, so the lamp
  he lifts in 5a is the same one in the ECU.
- 5c re-rendered once: miner2 moved (y 6.4 -> 10.1) and stands more upright so his head stays above the caption line.
