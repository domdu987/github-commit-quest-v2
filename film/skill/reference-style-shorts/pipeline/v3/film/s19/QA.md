# QA: take s19 (shot 19, the mechanism on the wall map), hand-drawn red line

- **Frames.** Film g 1189-1418 (230 f) plus handles 8 in (g 1181-1188, match dissolve 12 f) and 7 out (g 1419-1425, dissolve 9 f):
  245 final frames `frames/g_%04d.png`, 720x1280, 12 samples, office_grey. All rendered after 14:52 on 18 Nov with the
  HAND-DRAWN line (no frame of the straight version is left; the straight work is kept only as `work/shot_straight.py.bak`).
- **No characters.** No mouths, no backs, no pinned hand props (no registration needed).
- **Mechanism.** `v3/set3d_ext/mech/office_mech.py` (API.md section 0-2): lane, both corridor faces, face H, pictograms, wind,
  sign, wake and every spinner position follow `S.track_point(u)`; the corridor bends with the line (0.154 D west of the chord at u 0.5).

## Gate (build step 2) on the hand-drawn corridor
`set3d_ext/mech/gate_hand/sheet.jpg`: lens 0.35 D above the paper, 6000 px map, walls 0.50 D. Lens ON the line behind the storm: the
inside of the bend hides N.Y. (fail). Lens 0.155 D west of the chord (`M.clear_lateral`): N.Y. arrow head visible down the bent
lane, clearance 0.027 D, walls leave the top of the frame: PASS, no fallback. No shimmer seen on the 6000 px map in the corridor creep.

## Framing changes (film frames; probe numbers in work/probe.txt)
| phase | frames | camera | numbers |
|---|---|---|---|
| (0) crash push x6 | 1188-1205 | far room -> 30 deg rake from below-left, 0.8 D | spinner 29 -> 112 px at (393, 753) |
| drift | 1205-1225 | creep + orbit | spinner 112-119 px |
| (1) snap | 1225-1238 | x0.45 back, 35 deg rake north | both walls in frame, N.Y. y 516 |
| drift push | 1238-1292 | 10 %/s push, accelerating orbit | spinner 92 -> 117 px |
| (2) snap | 1292-1308 | corridor view (lens 0.345 D, 0.155 D west of the chord) | N.Y. at (379, 652); spinner 410-440 px at the bottom right |
| creep | 1308-1328 | u_lens -0.17 -> -0.13 | |
| (3) snap | 1328-1345 | plan view, roll -12 -> 0 by 1374 | |
| truck north 0.6 D | 1345-1372 | follows the line | N.Y. y 28 -> 363 (upper third) |
| (4) snap | 1372-1385 | truck back, push x2 onto the spinner (52 deg rake) | spinner 191 -> 200 px |
| bonks, shakes | 1396, 1408 (6 f each) | | creep decays, near still from 1413 |

- Corner speed (work/motion.json): peaks 160-358 px/frame in the snaps; static runs over 6 frames: none; linear runs: g 1183-1188
  (handle, shot 18's slow push) and g 1387-1396 (10 f creep at 1.8-1.9 px/f, slowly accelerating) only.
- **Popcheck** (post.py): 245/245 frames, none missing, no black or magenta frames. One flag g 1255 (diff 5.8 vs 1.9): the first
  terrace of the land wall swelling out of the paper on its thud (41.70), the same planned event as the east wall at g 1233. Largest
  diff g 1336 (snap 3).
- **Events** (cues.json): terraces E 1233-1251, W 1254-1269; squeeze 1272-1293; locks W 1299, E 1311; chalk crumble 1314; lane
  1335-1356; compass ping 1358; bonks 1396 (E) / 1408 (W) with the pictograms (W card turned yaw 60 / tilt 35 to face the camera).
- **Hand-drawn line vs the chalk curve.** Phases 0-1 show the red stroke wandering north beside the white dashed chalk curve that
  bends out to sea; once the east wall rises the chalk lies under it (crumbled at 43.70, as planned).

## Colour (hue_report.py frames)
`frames  red 28.1 orange 22.3 yellow 0.0 green 0.1 cyan 0.4 blue 45.5 violet 0.4 magenta 3.2 sat 0.37 val 0.47 dark 0.12  OUT: red,blue,sat`
A map-only office_grey shot: the pale blue-grey pressure walls fill most of the close views, so blue runs above the band and red a
little under it; violet 0.4 and magenta 3.2 stay low (shade reads blue, never magenta); value and dark share are inside the band.

## Cost
Wall time per final frame 11-46 s (median 23.1 s), CPU 19-35 s (median 27.8 s), 2 threads, machine load 7-10.

## Known
- In the rakes of phases 0-1 the far Thai label is seen rotated by the rake's dutch angle (it is small and far; the plan reads it in 18 and 22).
