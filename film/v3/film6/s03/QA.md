# s03 QA: film 6, shot 3 (the empty pillory), market AFTERNOON

Delivered: `take.mkv` (libx264rgb crf 6, 30 fps) = `frames/g_0102.png .. g_0185.png` (84 frames, 720x1280, 12 samples, 2 threads,
denoise FAST, no captions, no audio), `meta.json` (first_g 102, n_frames 84), `cues.json`, `contact.jpg`, `compare.jpg`.
Shot 3 = g 108..179 (plan 3.60-6.00 s); handles g 102..107 and g 180..185 rendered in 3D. Transition in / out: cut (plan).
Scripts: `shot.py` (two framings = sid 1 / sid 2, each its own Blender build: `python3 shot.py final <sid> a:b`), `mk.py` (crow drawing,
splats, extra bakers, sharp sky, the per-framing take class; identical copies in s05 / s12), `deliver.py` + `take_cfg.py`
(frames, meta, cues, sheets, mkv, `work/qa.txt`). Raw renders + per-frame json in `raw/s1`, `raw/s2` (git-ignored).

## Client rules
- **No depth of field / sharp image**: DOF off at build and before every render (common.Take). The set's sky dome draws its clouds through
  an SVG Gaussian blur at 11 px/deg, which read soft in the market; `mk.sharp_sky()` redraws the same sky (same seed and clouds) without the
  blur at 34 px/deg and swaps it into the sky material at runtime (set module untouched). No motion streaks.
- **Heads above the caption band**: no people in this shot. The crows sit well above y 880.
- **Mouths**: nobody speaks. The crows' "caw" is a beak drawing, not a cast mouth.
- **Comic, not cruel**: the pillory is empty; the set's dried veg splats on the platform only.

## Framing / timing
| g | framing | action |
|---|---|---|
| 102..143 | sid 1: low among the crowd space, up at the empty pillory against the north row and sky, 24 mm, slow push (pitch ~+18 deg) | crow A on the post top looks about; crow B pecks at the left end of the board; crow C (right end) CAWS g 118..125; a fourth crow flaps across the sky right -> left |
| 144..185 | sid 2: punch-in at 1.2 s, closer along the board from the right, 26 mm, slow push | crow B hops to the neck hole g 150..157 and pecks; crow C caws g 160..166; crow A takes off g 168 and flaps out of frame up-left (gone by g 181) |
Framing change at g 144 (shot 1.2 s + 1.2 s); every frame moves (push + crows): no near-still frame pairs, no pops apart from the cut.

## Numbers (`work/qa.txt`)
- render: 15.5 s wall / 27.0 s CPU per frame (two 2-thread processes at once on 4 cores).
- magenta / black frames: none; retried frames: none.
- hue (shot 3): red 30, orange 8, blue 42, violet 9, magenta 8.5, sat 0.46, val 0.64, dark 0.06 (ref a exteriors: red 6, orange 24,
  blue 55). The red is the oak pillory + platform filling the lower half at this low angle; the shade stays blue-violet (no magenta cast).
  Not graded here (set look).

## Differences from the plan / notes
- Shot 3 is two framings (push, then a punch-in at g 144) to keep a framing change within 1.0-2.0 s; the plan's "slow push" is kept in both.
- Crows are new 2D drawings (`mk.crow_svg`, plum ink, blue-black) on PropCards: the set and cast have no crows.
