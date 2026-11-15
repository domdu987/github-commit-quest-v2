# s10 QA: film 9, shots 10-11 ("count": month 1 / month 2), wall_site DAY

Delivered: `take.mkv.partaa` + `take.mkv.partab` (= `take.mkv` split -b 40M, 66.0 MB; `cat take.mkv.part* > take.mkv`), libx264rgb crf 6,
30 fps, **first_g 691, 202 frames (g 691..892)**, 720x1280, 12 samples, 2 threads, OIDN (prefilter FAST). Plan range g 697..886
(23.24-29.57 s); in-handle g 691..696, out-handle g 887..892, both rendered in 3D (the camera move and the acting continue).
`meta.json`, `cues.json` (9 cues), `contact.jpg` (16 frames, cyan line = y 880). Scripts: `shot.py` (stills / final), `c9.py` (own
helper module: film8/common.py switched to cast9 + set3d9/wall.py), `take_conf.py`, `deliver.py`, `qa.py` (-> work/qa.txt).
One process per set-up, one build (two_sections, DAY), two custom cameras, cut inside the take at g 792 (plan 10 -> 11).

## Beats
| g | what | caption |
|---|---|---|
| 691-738 | both sections at 18 courses; the general (akimbo, smug) by his grey section, Lin (arms folded, calm smile) at his creamy rice section, two workers with brick stacks | "เดือนแรก" 23.22, "กำแพงแม่ทัพ" 23.73 |
| 733-769 | the general looks up at his section as it rises: course 19 at g 739, 20 at g 747, 21 at g 758 (set_wall_height keyed; banners, hoist and top dressing ride up) | "สูงกว่า" 24.63, "สามชั้น" 25.10 |
| 764-791 | the general puffs up, smug again; Lin keeps his calm look up at it | "เดือนที่สอง" 25.63 |
| 792 | CUT to the top of the general's section, month 2 (lin 20 / general 26) | "สูงกว่าหกชั้น" 26.45 |
| 792-892 | the general on his wall, arms akimbo, head thrown back laughing (body shake), a worker with bricks behind him, banners, crane | "แม่ทัพยืน หัวเราะบนกำแพงตัวเอง" 27.44-29.60 |

Camera: shot 10 low from the site at the seam of the two inner faces (y 22 -> 20.6, z 5.9 -> 5.6, pitch -11, 20 mm, push 1.6 D, small
drift); shot 11 along the general's top (x 17.6 -> 14.9, 20 mm, push 2.7 D). Moves are 0.35 sine + 0.65 linear (no dead ends).

## QA-team rules (work/qa.txt)
- **Wide, dense, lit 3D set**: both sections, scaffold ladders, hoists, banners, cart, brick piles, brazier, trough in shot 10; paved walk,
  crenels, tubs, crane, banners and the plain beyond in shot 11. Warm DAY sun.
- **Sharp, no blur**: no DOF (`dof.use_dof False` + `setup_dof(None)` before every render). Laplacian variance min 347 / median 477.
- **No text signs**: none in frame (banners carry only emblems).
- **Grounded**: every figure stands on the ground / the wall-top paving with the cast contact shadow (sun shadows also cast).
- **Heads above y 880**: max head bottom 754 (shot 10), 603 (shot 11). Head centres 0.53-0.56 H (shot 10 wide), 0.38-0.45 H (shot 11).
- **Mouths still**: no quote in shots 10-11; no lip-sync, fixed expression mouths (the laughing mouth is a held shape).
- Popcheck: the planned cut 791 -> 792, and the three course pops at 738->739, 746->747, 757->758 (intended: courses appear). No
  near-still frames (median change 2.15 levels). No black / magenta frames, no retried frames.

## Hue (hue_report)
```
s10 shot 10 (g 697-791)   red 20.2 orange 53.4 yellow 1.1 blue 21.6 violet 1.9 magenta 1.6  sat 0.46 val 0.58
s10 shot 11 (g 792-886)   red 16.9 orange 13.2 yellow 9.5 blue 56.0 violet 3.1 magenta 1.0  sat 0.37 val 0.65
```
The set's DAY look (warm orange set, blue sky; shot 11 is sky-heavy). hue_report flags these against its film-2 bands; no grade applied.

## Seconds per frame
10.0 s wall / 19.6 s CPU mean (shot 10 ~12 s wall / 23-24 s CPU, shot 11 ~7.7 s wall / 15.7 s CPU), two processes of 2 threads.

## Differences from the plan / notes
- Shot 10 is a custom low camera (the two_sections preset puts figures at ~80 px and Lin's chin near the band); the height step is shown
  as a time-lapse: both sections start at 18 and the general's grows 3 courses on the narration's "สูงกว่าสามชั้น".
- Shot 11 uses a wall_top-like camera (pushed in): Lin's lower section is not in view from here (set API note); the 6-course gap reads
  from the narration and shot 10's growth.
