# s14 QA: film 2, shot 14 (the morning after: padre hands the rod back), tower set DAY

Delivered: `take.mkv` = frames g 1018..1158 (141 frames, first_g 1018, 720x1280, 12 samples, 2 threads, libx264rgb crf 6), `meta.json`, `cues.json`,
`contact.jpg` (16 frames; label shows padre's mouth drawing), take script `shot.py`, delivery `deliver.py` (uses `../s12/deliver_lib.py`).
Raw renders + per-frame json in `raw/`, numbers in `work/qa.txt` (not in git).

## Timing
| event | g |
|---|---|
| in-handle (12-frame dissolve from shot 13) | 1018-1025 |
| shot 14: two-shot in the square, padre (smug) holds the rod out; pushes it out a little on "บาทหลวงยื่น" (1028) | 1026 |
| nico reaches up (12 f, cubic) and grips the rod on "คืนให้เขา" | 1041-1053 |
| padre's mouth moves (the quote "เห็นไหม ... ไปเถอะ"), a new drawing every 2 frames from the narration envelope (flat / talk_a / talk_o / talk_b); closed smirk outside | 1071-1155 |
| snap reframe onto padre (plan 35.9 s = g 1080) | 1076-1084 |
| snap reframe onto nico + rod on "เก็บไม้จิ้มฟ้า" (1115); padre lets go mid-snap (1116) and puts both hands on his hips; nico holds the rod himself | 1112-1120 |
| speed change before the out-dissolve (plan 38.3 s) | 1146 |
| out-handle (12-frame dissolve into shot 15) | 1151-1158 |
Framing changes: 1018-1048 drift, 1048 speed change, 1076-1084, 1112-1120, 1146: gaps 1.0-1.3 s.

## Camera (fastest of 9 screen points at 5 D, px/frame)
min 0.32, median 2.2, peak 104 (g 1079, snap onto padre); static runs none; one constant-speed run 1030-1035 (6 f).

## Staging (raw json, g 1026-1150)
| head | width px | centre y (H) | below y 880 |
|---|---|---|---|
| nico (main in the two-shot and at the end) | 173-278 | 0.52-0.58 | none |
| padre (main in the close, 1084-1112) | 149-229 | 0.40-0.46 | none |
During the padre close (1084-1112) nico is off frame left (centre x < -120; only his arm on the rod stays in frame).
Hand pin: nico's right hand on padre's rod (0.30 D below padre's fist), solve error 0.000 D on every frame from the grip on.
head_flip False (key from screen-left), padre mirrored so that he faces nico; nobody's back to the camera. Mouth movement only in g 1071-1155
(checked: no mouth drawing outside the quote). Popcheck: no pops, no near-still transitions, no black / magenta cards, no retried frames.

## Colour
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s14 shot 14 (g 1026-1150)                      29.2   37.2    0.0    0.2    0.0   28.4    3.3    1.6  0.46 0.62 0.11   OUT: red
s14 all (g 1018-1158)                          29.2   37.2    0.0    0.3    0.0   28.5    3.3    1.5  0.46 0.62 0.11   OUT: red
ref a t0062 t0040 t0072                        23.3   15.0    1.3    0.1    0.0   51.4    3.4    5.5  0.49 0.59 0.12
```
Everything in band except red 29.2 (band 30-41). Shade blue-violet (actor shadows on the cobbles). Seconds per frame: 11.8 s wall / 23.1 s CPU.

## Differences from the plan
- "padre_smug_hand_rod": his rod arm is pushed further out (hand (1.06, 0.42), stretch 1.3) so the rod stands against the brick of the tower,
  not against his black cassock; nico grips it 0.30 D below padre's fist.
- When padre lets go (g 1116, during the snap) the rod becomes nico's own prop (gripped 0.9 D from its base): it moves about 0.3 D in the
  frame, hidden by the 104 px/frame snap.
- DAY preset as "morning" (no separate morning light exists in the set). Tower bare (set_rod(0)). Market stall hidden.
- First version of this take had nico's head dipping below y 880 during the snaps; re-rendered with all cameras aimed 0.3-0.5 D lower.
- At the end padre's hat brim touches the right frame edge (head inside).
