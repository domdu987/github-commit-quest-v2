# s03 QA: film 9, shots 3-4 (the pivot): wall_site, DAY crane + DUSK gate

Delivered: `take.mkv` split into `take.mkv.partaa` + `take.mkv.partab` (80.8 MB > 45 MB; `cat take.mkv.part* > take.mkv`). It holds 173 frames,
g 103..275 at 720x1280, 12 samples, 2 threads, OIDN FAST, libx264rgb crf 6, 30 fps, first_g 103, with no captions and no audio.
- g 103..108 = in-handle (shot 3's crane continued, rendered in 3D).
- g 109..194 = shot 3 (plan 3.62-6.50 s).
- g 195..269 = shot 4 (plan 6.50-9.01 s).
- g 270..275 = out-handle.
- transition_in: cut.

Also delivered: `meta.json`, `cues.json` (8 cues), `contact.jpg` (the cyan line is y 880), and the scripts `shot.py`, `c9.py`, `deliver.py` + `TAKE.json`, `qa.py` (-> work/qa.txt), and `sheet.py`. Each light gets its own build/process (final_loop rebuilds on the change).

## Set-ups
| id | g | camera | action |
|---|---|---|---|
| 1 | 103-194 | site_wide DAY, crane: (-19.4,33,20.6)->(-17,29.8,16.6), look (-2.6,7,1)->(-3.4,7.6,1.6), 20 mm | the camera sinks 4 D and pushes in over the whole site: the steaming cauldron, Lin stirring, three workers carrying brick stacks (one up the plank ramp of the general's scaffold), both sections, scaffolds, banners, gate tower, river plain, mountains |
| 2 | 195-275 | gate_dusk DUSK preset camera, push (14,26,21)->(15.4,24.2,20.3) with the look-at tilted 1.1-2.1 D higher than the preset | the gate tower at dusk, lanterns lit; the enemy host's black/red banners and dust bank on the horizon left and right of the tower; battlefield smoke 0.6 |

## Client / QA rules
- **Sharp, no DOF:** DOF is switched off at build and before every render. Laplacian variance: min 255, median 509.
- **Wide, dense, lit 3D set; no text signs.** The banners carry emblems, not text.
- **Heads above y 880:**
  - Lin: head centre y 746-759, 29-37 px. This is lower than the preset (QA note "lower camera ~1 D": the end of the crane is 0.9 D lower than site_wide) and panned west, so his chin stays at ~775.
  - Workers: y 493-704.
  - Shot 4 has no figures. From this high camera, every ground position near the gate put a figure's head at y 915-1135 (probed), so I left the worker out.
- **Grounded:** cast contact shadows. Lin is on the platform (z 1.5). worker_c's feet follow the ramp slope (z = (x-3.5)/7.8*6).
- **Mouths:** there is no quote, so no lip-sync.
- **Motion:** the only pop is the planned cut 194->195. There are 0 near-still transitions (median change 1.6 levels).
- **Frame checks:** no black or magenta frames, and no retried frames.
- **Continuity:** wall heights are lin 18 / general 21 in both shots, the same as s01. The general is not shown before shot 5.

## Colour (hue_report)
```
s03 shot 3 (g 109-194)  red 21.8 orange 58.0 yellow 1.7 green 1.6 blue 15.0 violet 1.3 magenta 0.6   sat 0.43 val 0.63
s03 shot 4 (g 195-269)  red 30.4 orange 30.6 yellow 0.1 green 0.0 blue 11.6 violet 4.5 magenta 22.8  sat 0.33 val 0.52
```
Shot 4's magenta share (22.8) is the set's DUSK grade on the lower half: the dusk-lit dirt reads mauve, exactly as in the approved `gate_dusk` contact tile. I did not regrade it in the take. If the conform wants it bluer, a hue shift of the lower half toward blue-violet would do it.

## Seconds per frame
13.86 s wall / 27.3 s CPU mean (2 threads, two processes at once).

## Differences from the plan / known issues
- Shot 3: the crane is a descending push rather than a rising one. It is panned west of the preset to keep Lin inside the frame, so the gate tower is cut at the left edge.
- Shot 4 runtime change from shot.py (allowed: no set file edited): `army_horizon` is scaled 1.7x in z, so the host's banners and dust read at phone size (QA_TECH set note B). The banners stand ~25-40 px tall.
- Shot 4 has no characters, and its bottom ~30 % is dusk-lit dirt with a lantern post. QA-art had already noted this dirt as sparse.
