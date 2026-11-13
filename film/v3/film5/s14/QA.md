# s14 QA: film 5, shot 14 (the lamp flame flares blue, the gas lights, the fireball races behind the running group), mine tunnel LAMP

Delivered: `take.mkv` = `frames/g_1357.png .. g_1509.png` (153 frames, 720x1280, 12 samples, 2 threads, no captions, no audio).
g 1365..1501 = shot 14 ([45.49, 50.08) s -> [1365, 1502)); handles g 1357..1364 and g 1502..1509 rendered in 3D (the blast keeps going).
`meta.json` (first_g 1357, n_frames 153), `cues.json`, `contact.jpg`, `compare.jpg` (14a / 14b / 14d beside ref a t0093 / t0095 / t0097), `work/qa.txt`.
Scripts: `shot.py` + `../s12/base.py`, `../s12/deliver_lib.py`, `deliver.py`. Drafts `work/d1..d3.jpg`.

## Client rules
- **No DOF / no blur**: `M.setup_dof(scene, None, None, cam=...)` (the lamp_insert default never applied); the blast has no motion streaks.
- **Bird inside the cage**: alfie holds it in 14c/14d -> cast 2D held cage, bird (fallen, eyes closed) behind the drawn bars; set 3D cage hidden.
- **No casualties**: every runner (the gaffer last, 3.3 D behind alfie) is outbye of the fire front in every frame (front y = `M.blast_front(u)`:
  14c 22 -> 14, 14d 14 -> ~10.6 at g 1509; gaffer 11.9 -> 8.4 -> 5.5). Flying embers / coal ahead of the front pass among them, no one is hit.
- **Mouths**: none move (no quoted line). Gaffer / miners hold a static shocked "o".

## Timing
| framing | g | what | ref a |
|---|---|---|---|
| 14a | 1365-1404 (handle from 1357) | lamp_insert ECU: the foreman's hanging safety lamp; flame normal, then tall (`set_flame` 1 -> 2, g 1378-1396) and pale blue (insert-flame emission colours + lamp light keyed warm -> blue at runtime, "flame_blue" look) on "แล้วเปลวไฟในตะเกียงของหัวหน้า"; gas haze 2.4 drifting | t0093 |
| 14b | 1405-1440 (cut) | low angle: the gaffer under the lamp looks up, hands rising, shocked; on "ก็จุดแก๊ส" (g 1422) the flame bursts (k 3.2) with an orange flash (keyed lamp_ign); from g 1426 he runs outbye | t0095 |
| 14c | 1441-1475 (cut) | from the pit-bottom end down the roadway: alfie with the cage, miner1-3 and the gaffer run at the camera; `set_blast` 0.35 -> 0.55, the fireball comes round the bend behind them ("ทั้งอุโมงค์ระเบิด" g 1464) | t0097 |
| 14d | 1476-1501 (cut, handle to 1509) | low and close from the right, the camera backing off: runners big in front, the fireball filling the roadway right behind (u 0.55 -> 0.66), debris flying past | |
Framing changes 1365, 1405, 1441, 1476: 1.33 / 1.20 / 1.17 / 0.87 s (+ handle).

## Staging (`work/qa.txt`)
14b gaffer head 148-185 px (0.49-0.57 H). 14c alfie 95 -> 176, miners 76-153, gaffer 68-102. 14d alfie 192-254 (leaves the frame left at the end, x -10),
miner1 166-212, miner2 / miner3 133-162, gaffer 107-124. All heads above y 880.
Pops: the cuts 1404/1405, 1440/1441, 1475/1476; 1422/1423 and 1425/1426 = the ignition flash on and off (on purpose). No black / magenta / retried frames.

## Colour
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s14 14a (g 1357-1404)                           3.9   22.8    1.3    0.1    0.0   66.6    3.9    1.3  0.32 0.49 0.01   OUT: red,blue,sat,dark
s14 14b (g 1405-1440)                           8.3   11.8    2.6    0.1    0.0   69.2    4.8    3.1  0.43 0.41 0.07   OUT: red,orange,blue,val,dark
s14 14c (g 1441-1475)                           6.8   10.0    2.1    0.0    0.0   63.4   11.7    5.9  0.35 0.44 0.03   OUT: red,orange,blue,violet,sat,val,dark
s14 14d (g 1476-1509)                          19.2   26.5    7.0    0.1    0.0   25.9    9.8   11.5  0.31 0.51 0.04   OUT: red,violet,magenta,sat,dark
s14 all (g 1357-1509)                           8.9   18.1    3.0    0.1    0.0   57.8    7.0    4.9  0.35 0.46 0.04   OUT: red,orange,blue,violet,sat,dark
```
14a-14c blue-dominant (LAMP underground; the flame turns blue). 14d is the fire: red 19 / orange 27, magenta 11.5 (orange-red fire blobs against the
blue shade: the mixed edges count as magenta); shade stays blue.

## Seconds per frame
11.6 s wall / 22.6 s CPU mean (2 threads).

## Differences from the plan / known issues
- The lamp that flares is the set's insert lamp on its chain (the gaffer's lamp hangs above him in s13); `set_flame` has no blue, so the blue is a
  runtime key of the set's insert-flame emission colours (set file untouched). The 2D `flame_blue` pose key is not used (no held lamp).
- 14b: the lamp itself is above the frame; the ignition reads as the orange flash on the gaffer and the timbers.
- The ignition point (the lamp, y 8.75) and the fireball's origin (the set blast forms at the face, y 40) differ; 14c/14d show it racing outbye.
- 14d: alfie runs out of the frame left in the last frames (out-handle).
