# s02 QA: film 7, shot 2 (the empty wall: four hooks, the guard yawning)

Delivered: `frames/` (g 66..143, 78 frames, 720x1280, 12 samples, 2 threads, denoise FAST, no captions, no audio) and `take.mkv`
(libx264rgb crf 6, 30 fps, **first_g 66, n_frames 78**). g 72..137 = shot 2 (plan 2.40-4.60 s); g 66..71 in-handle and g 138..143
out-handle, both rendered in 3D (camera move and acting continue). transition_in = cut, out = cut (plan).
Also `meta.json`, `cues.json` (7 cues), `contact.jpg` (16 frames, cyan line = y 880), `compare.jpg` (g 80 beside ref a t0003, an ECU
object insert; g 116 beside ref a t0013, a character with a wide-open mouth). Scripts: `shot.py` (probe / stills / final), `deliver.py`,
`qa.py` (-> `work/qa.txt`); shared helpers `../common.py` (untouched). Drafts `work/d1.jpg`, `work/d2.jpg`.

## Set-ups (framing change at g 102 = 3.40 s; 1.0 s and 1.2 s + handles)
| id | g | what |
|---|---|---|
| 1 | 66..101 | ECU of the empty spot: the four iron hooks, the unfaded damask patch with its dust line, the brass plaque "LEONARD DE VINCI / La Joconde"; slow pull back (34 -> 29.5 mm), the guard kept out of frame |
| 2 | 102..143 | medium at eye level outside the rope: the guard (bottle-green kepi) beside the empty spot, sleepy; huge yawn and stretch g 104..130 (open 104-112, hold 112-122, close 122-130), sags back; slow push 26 mm |
`set_mona(False)` and `set_flames` keyed on every frame (common.py keys gotcha). Captions: "โดยไม่มีใคร" 2.52 s (g 79), "สังเกตเลย"
3.28 s (g 101: the cut to the guard), "ทั้งวัน" 3.83 s (g 118: mid-yawn).

## Client rules
- **No depth of field**: C.Take turns it off at build and before every render. Hooks, damask pattern, plaque text, the hang behind: sharp.
- **Heads**: id 2 guard head centre y 698..708 (0.55 H), 165..191 px, bottom <= 804 (none below 880). id 1: no head on screen.
- **Mouths**: no quoted line -> no lip-sync. The yawn is one slow open / hold / close of the expression mouth (`("open", w, h)`), no speech.
- **Dense set**: id 2 shows the salon hang (gilt frames, portraits), rope and stanchions, marble dado, parquet. id 1 is an insert (the motif).

## Checks (`work/qa.txt`)
Popcheck: one jump, the planned framing change 101 -> 102. Near-still pairs only at the eased ends g 66 and g 142 (single pairs, < 6 frames).
No black / magenta frames, no retried frames, no clipped sprites.

## Colour (hue_report rows)
```
s02 id 1 (g 66-101)    red 97.8 orange 1.8 ... magenta 0.2  sat 0.92 val 0.66 dark 0.04
s02 id 2 (g 102-143)   red 71.2 orange 25.3 ... magenta 1.3 sat 0.65 val 0.61 dark 0.05
```
The set's red silk damask fills the frame (id 1 is almost all damask): red and saturation are far above the film-wide band; this is the
set's wall colour, not graded here (do it in the conform if wanted). No magenta / violet shade.

## Seconds per frame
15.4 s wall / 25.6 s CPU mean (2 threads, two render processes at once; some frames ran while a 2-thread draft paused the other).

## Differences from the plan
- None in content. The ECU-then-medium order (hooks first, then the guard) is a choice for the framing-change rule.
