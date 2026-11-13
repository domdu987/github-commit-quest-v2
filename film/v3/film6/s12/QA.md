# s12 QA: film 6, shots 12-15 (the nickname + the pillory count), market MORNING then AFTERNOON

Delivered: `take.mkv` (libx264rgb crf 6) = `frames/g_0927.png .. g_1244.png` (318 frames, 720x1280, 12 samples, 2 threads, denoise FAST,
no captions, no audio), `meta.json` (first_g 927, n_frames 318), `cues.json`, `contact.jpg`, `compare.jpg`. Shots 12-15 = g 933..1238
(plan 31.09-41.29 s); handles g 927..932 (dissolve-in, 3D) and g 1239..1244 (3D). Transition in: DISSOLVE from shot 11; out: cut to shot 16.
Eight framings, each its own Blender build (`python3 shot.py final <sid> a:b`). Scripts: `shot.py`, `mk.py` (shared, identical copy in
s03 / s05), `deliver.py` + `take_cfg.py`. Raw + json in `raw/s1..s8` (git-ignored).

## Client rules
- **No depth of field / sharp**: DOF off at build and before every render; the set's blurred sky replaced by `mk.sharp_sky()`. No streaks.
- **Heads above the caption band**: every head centre 0.48-0.60 H and every head bottom above y 880 on all 318 frames (`work/qa.txt`).
- **Mouths only where allowed**: shot 12 is the one place townsfolk laugh: woman1 / man1 alternate their laughing mouth with `talk_o`
  every 3 frames (g 927..1004). Kit (shot 12) and all bakers (13-15) keep the static mouth of their expression; no quoted line.
- **Comic, not cruel**: the pilloried bakers are sad / worried, shaking their heads; no veg thrown in these shots.
- **Continuity**: kit = flour-dusted boy with the 13-loaf basket (cast6 `basket` loaves=13). The pillory count accumulates: week 1 baker2;
  week 2 baker2 + baker3; week 3 baker2..baker5. baker3/4/5 are runtime copies of cast6 baker2 with other tunics (brown / blue / plum),
  caps, hair, moustache or beard (`mk.register_bakers`; cast6 not edited). The set's 3D pillory board is cut away at runtime; each baker
  wears the cast6 pillory board, so the row reads as four pillories side by side on the platform. A crow sits on the post (as in s03).

## Framings / timing
| g | framing | action |
|---|---|---|
| 927..968 | sid 1 square MORNING, 28 mm two-shot, slow push | woman1 + man1 laugh (mouths) and point screen-right |
| 969..1004 | sid 2 26 mm, pan with kit | kit walks past with the basket of 13, glances back at the laughers (g 978..994) and grins; they laugh behind |
| 1005..1043 | sid 3 pillory AFTERNOON, frontal-low 24 mm push | week 1: baker2 alone, sad; crow on the post |
| 1044..1079 | sid 4 punch-in 30 mm | baker2 sighs, head droops (g 1050..1072) |
| 1080..1115 | sid 5 frontal-low 24 mm | week 2: two heads |
| 1116..1151 | sid 6 28 mm from the right | the two look at each other and back |
| 1152..1197 | sid 7 frontal 24 mm | week 3: four heads in a row, all shaking "no, I weighed exactly" |
| 1198..1244 | sid 8 30 mm track left -> right along the row | heads shaking out of phase; the crow caws (g 1212..1219, 1232..1238) |
Framing changes every 1.2-1.5 s. Popcheck (excluding the 7 cuts): none. One near-still pair (g 1041->1042, end of the sid 3 push).

## Numbers (`work/qa.txt`)
- render 15.5 s wall / 29.6 s CPU per frame (two 2-thread processes on 4 cores). Magenta / black frames: none; retried: none.
- hue shot 12 (MORNING) orange 27 red 25 blue 34 sat 0.34; shots 13-15 (AFTERNOON) orange 29 red 19 blue 37 sat 0.40 val 0.68
  (ref a exteriors orange 24 blue 55). Red is the oak pillory boards / timber; the shade is blue-violet, no magenta cast.

## Differences from the plan / notes
- Shot 12 is morning (kit's delivery round); shots 13-15 afternoon (busts in the afternoon sun, paid off in shot 20).
- Each plan shot is two framings, to hold a framing change every 1.0-2.0 s.
- The plan names one "baker2" cast member; the extra bakers of weeks 2-3 are runtime colour / feature variants of baker2.
