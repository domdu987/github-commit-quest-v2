# s13 QA: film 5, shot 13 (alfie grabs the cage and drags the miners toward the exit; miner3 mocks; the gaffer stays), mine tunnel LAMP

Delivered: `take.mkv` = `frames/g_1196.png .. g_1372.png` (177 frames, 720x1280, 12 samples, 2 threads, no captions, no audio).
g 1204..1364 = shot 13 ([40.14, 45.49) s -> [1204, 1365)); handles g 1196..1203 and g 1365..1372 rendered in 3D.
`meta.json` (first_g 1196, n_frames 177), `cues.json`, `contact.jpg`, `compare.jpg` (13a / 13c / 13d beside ref a t0079 / t0077 / t0081), `work/qa.txt`.
Scripts: `shot.py` + the shared engine `../s12/base.py`, `../s12/deliver_lib.py`, `deliver.py`. Drafts `work/d1..d4.jpg`.

## Client rules
- **No DOF / no blur**: `M.setup_dof(scene, None, None, cam=...)` at build and before every render. No streaks (the snatch is a plain 3-frame arm move).
- **Bird inside the cage**: up to g 1207 the cage hangs on its nail (set 3D cage, the canary sprite lying on its floor, inside); from g 1208 alfie
  HOLDS it, so it is the cast's 2D held cage (`prop_r="cage"`, pose key `bird` = fallen, bars drawn over the bird) and the set's 3D cage is hidden
  (per-frame `hide_render`). Swing keyed (yank 34 deg decaying, then +-14 deg at the run).
- **Gentle bird**: fallen, eyes closed (`eyes` 0), faint breathing.
- **Mouths**: only miner3, on the quoted line g ..1367 ("ไอ้เด็กเลี้ยงนก ตื่นตูมอีกแล้ว"), lip-sync drawing every 2 frames (talk_a/b/o, flat);
  everyone else closed (frown / smirk). In 13c before g 1304 miner3 holds a closed smirk with his hands cupped.

## Timing
| framing | g | what | ref a |
|---|---|---|---|
| 13a | 1204-1245 (handle from 1196) | alfie beside the cage on its nail, looks at the fallen bird; reaches g 1203-1207 and snatches it (cage in his hand from 1208, "เขาคว้ากรง" g 1206); turns 1219-1227 and starts to run at the camera; miner1 / miner3 watch from inbye, smug | t0075-79 |
| 13b | 1246-1287 (cut) | low, from outbye: alfie runs at the camera with the cage, pulling miner1 by the hand (both hands pinned to one world point); miner2 / miner3 follow at a walk | |
| 13c | 1288-1329 (cut) | medium, camera tracking back: miner3 walks with his hands cupped at his mouth, mocking (mouth from g 1304); miner2 behind | t0077 |
| 13d | 1330-1364 (cut, handle to 1372) | high wide from outbye: alfie + miner1 run toward the camera / exit, miner3 still mocking, the gaffer stays smug, arms crossed, under his hanging lamp | t0081 |
Framing changes 1204, 1246, 1288, 1330: 1.40 / 1.40 / 1.40 / 1.17 s (+ handle).

## Staging (`work/qa.txt`)
| framing | heads (width px, centre y H) |
|---|---|
| 13a | alfie 189-284 (0.51-0.53); miner1 100-105 / miner3 82-86 in depth; bird in the 3D cage 31-34 px (until 1207) |
| 13b | alfie 155 -> 248 (0.46-0.53), miner1 124-176, miner2 101-133, miner3 95-123 |
| 13c | miner3 278 (0.45), miner2 177 |
| 13d | alfie 119 -> 196, miner1 106-163, miner3 94-103, miner2 80-86, gaffer 99-103 (0.40) |
All heads above y 880. Pops: the cuts 1245/1246, 1287/1288, 1329/1330; 1211/1212 (4.1, the cage yank); 1294/1295 (13.1: the tracking camera passes
under the cap bar of the set at y 8.75, the bar leaves the top of frame). No black / magenta / retried frames.

## Colour
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s13 13a (g 1196-1245)                           5.3    5.2    0.1    0.0    0.0   78.7    8.5    2.2  0.31 0.44 0.02   OUT: red,orange,blue,violet,sat,val,dark
s13 13b (g 1246-1287)                           7.1    6.8    0.5    0.0    0.0   68.0   14.1    3.5  0.35 0.42 0.04   OUT: red,orange,blue,violet,sat,val,dark
s13 13c (g 1288-1329)                           2.9   10.0    0.6    1.0    0.0   71.4   10.8    3.3  0.34 0.44 0.02   OUT: red,orange,blue,violet,sat,val,dark
s13 13d (g 1330-1372)                           7.8   11.8    0.3    0.2    0.0   64.8   12.7    2.4  0.25 0.48 0.01   OUT: red,orange,blue,violet,sat,dark
s13 all (g 1196-1372)                           5.7    8.3    0.4    0.3    0.0   71.1   11.4    2.9  0.31 0.45 0.02   OUT: red,orange,blue,violet,sat,val,dark
```
Underground, blue-dominant by the set's LAMP design (as s01 shots 3 / 4b-4d: blue 59-72); magenta 2-3.5, shade blue, never magenta.

## Seconds per frame
13.1 s wall / 25.4 s CPU mean (2 threads), run beside s12 / s14.

## Differences from the plan / known issues
- Camera: the plan names tunnel_run (inbye looking outbye, runners' backs); I shot 13b / 13d from outbye so the runners face the camera (the puppets
  have no back view) and the gaffer can stay in frame under his lamp.
- Runtime set change: the nail and the 3D cage sit 0.55 D lower in this take (`shot.setup`), so the boy can reach it; s12 (ECU) shows it at the set height
  (not readable in the ECU).
- The snatch: his hand gets to the side of the cage (the arm is short); the cage appears in his hand on g 1208 during the fast reach + hard swing.
- The gaffer holds no lamp here: his flame safety lamp hangs on its chain above him (the set's insert lamp, used again in s14).
- The drag reads as alfie's hand and miner1's hand meeting between them (pinned to one point); at the 13d size it reads as a pull, not as a clear grip.
