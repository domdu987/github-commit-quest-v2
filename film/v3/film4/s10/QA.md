# s10 QA: film 4, shot 10 (the nickname "เจดีย์เมา"), pagoda set v2, DAY

Delivered: `take.mkv` = `frames/g_0703.png .. g_0788.png` (86 frames, 720x1280, 12 samples, 2 threads, no captions / audio).
g 710..781 = shot 10 ([g0, g1) = [710, 782)); g 703..709 = 7-frame in-handle, g 782..788 = 7-frame out-handle, both rendered in 3D
(the shot's camera keeps moving). meta.json: first_g 703, n_frames 86, transition_in cut (handle there for a dissolve if wanted),
transition_out 10-frame dissolve. Also cues.json, contact.jpg, compare.jpg (two frames beside ref a t0047).
Scripts: `shot.py` loads the engine `../s09/shot.py` (one engine for shots 9-12: cameras, quake clock, sway, set state);
`../s09/deliver.py s10`, `../s09/qa.py s10` (-> `work/qa.txt`).

## Timing (captions_bankky.json, g = round((t + 0.1) * 30))
| g | event |
|---|---|
| 710 | shot starts ("ทั้งเมือง" 712): merchant, farmer, woman2 in the courtyard on the runner, the pagoda behind them still rocking after quake 1 (sway amp 0.5 -> 0.12 D, decaying, at 1.1 Hz) |
| 716-726 | the three burst out laughing one after another (3-frame offsets) and fling a pointing arm up at the pagoda ("หัวเราะลั่น" 726); belly-laugh bounce on squash / head roll / lean |
| 752-759 | snap punch-in onto merchant + woman2 (quint ease), framing change 1.4 s after the start |
| 762-774 | pointing jab on "เจดีย์เมา" (766) |
| 778-785 | the pagoda's sway settles to rest |

## Staging (`work/qa.txt`)
| actor | head w px | centre x | centre y (H) | below 880 | edge |
|---|---|---|---|---|---|
| merchant | 117 -> 178 | 302-413 | 0.56-0.58 | none | none |
| woman2 | 129 -> 205 | 575-602 | 0.57-0.59 | none | none |
| farmer | 102 -> 146 | 126-278 | 0.56-0.57 | none | none |
DOF: focus on the merchant's card, f 2.5 (pagoda soft behind). head_flip False (DAY key from the south-west = screen-left).
Mouths: the cast4 "laughing" expression (fixed open grin with tears) from g ~716; it never animates open / close
(no lip sync: the narrator speaks). Before the laugh: "smirk", mouth closed. No pinned hands. Nobody's back to camera.
Popcheck: no pops; no near-still transitions; no black / magenta frames; no retried frames; no clipped sprites.

## Colour (hue_report.row)
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s10 10 (g 710-781)                             16.7   17.2    0.3    0.0    0.0   56.1    3.4    6.3  0.45 0.63 0.03
ref a t0047                                    33.9   48.0    5.6    0.4    0.0    0.5    7.4    4.3  0.37 0.45 0.16
```
Bluer / brighter than t0047 (an indoor feast): this is an exterior with sky behind the pagoda. Shade blue-violet, magenta 6.3.

## Seconds per frame
10.3 s wall / 19.9 s CPU mean (2 threads, two render processes in parallel on 4 cores).

## Differences from the plan / the reference
- Plan says street_eye; I staged it in the courtyard on the runner with the pagoda behind the laughing group so the "drunk" pagoda
  they mock is in the same frame (street_eye looks at the gate and shows the pagoda small). Camera between the toro and banner
  keep-out zones.
- The pagoda's residual sway is soft (in the DOF blur) and small (0.12-0.3 D) in this shot.
