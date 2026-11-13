# s05 QA: film 6, shots 5-6 (market establishing + the pilloried baker), market MORNING then AFTERNOON

Delivered: `take.mkv` (libx264rgb crf 6) = `frames/g_0253.png .. g_0465.png` (213 frames, 720x1280, 12 samples, 2 threads, denoise FAST,
no captions, no audio), `meta.json` (first_g 253, n_frames 213), `cues.json`, `contact.jpg`, `compare.jpg`. Shots 5-6 = g 259..459
(plan 8.62-15.34 s); handles g 253..258 (the dissolve-in, 3D) and g 460..465 (3D). Transition in: DISSOLVE from shot 4; out: cut to shot 7.
Four framings, each its own Blender build: `python3 shot.py final <sid> a:b` (sid 1 market_wide, 2 square_eye, 3 pillory medium, 4 throwers).
Scripts: `shot.py`, `mk.py` (shared; identical copy in s03 / s12), `deliver.py` + `take_cfg.py`. Raw + json in `raw/s1..s4` (git-ignored).

## Client rules
- **No depth of field / sharp**: DOF off at build and before every render. The set's blurred sky dome is replaced by `mk.sharp_sky()`
  (same clouds, no blur, 34 px/deg). The one motion event (man1's cabbage throw) is a 2-frame pose change, not a streak.
- **Heads above the caption band (y 880)**: every in-frame head centre 0.45-0.60 H, head bottom above 880 on every frame (`work/qa.txt`).
  The shot-5 crowd heads are small (25-145 px) and high; shot 6 baker2 0.45 H, woman1 / man1 (foreground) 0.58-0.60 H, tops above the band.
- **Mouths only on quoted lines**: no quoted line in shots 5-6. Every mouth is the static mouth of its expression; the foreground townsfolk
  in sid 4 laugh with the static `laughing` drawing (no lip-sync).
- **Comic, not cruel**: the rotten veg are cartoon drawings; the tomato (g 392) and cabbage (g 446) SPLAT on the board / cap beside baker2,
  never on his face; he flinches (eyes shut, a little sweat), no injury.
- **Continuity**: baker2 = the thin sad neighbour baker (cast6), locked in the cast6 pillory board; the set's 3D board is cut away at
  runtime (`mk.cut_pillory_board`) so only the drawn board shows. Shot 6 is the afternoon sun (the busts happen in the afternoon, shot 20).

## Framings / timing
| g | framing | action |
|---|---|---|
| 253..312 | sid 1 market_wide MORNING, 22 mm, slow crane down + push | the square: timber houses, stalls, bunting, balance, empty pillory; ~12 townsfolk strolling (walk cycles) + two laughing groups + two guards |
| 313..359 | sid 2 square_eye MORNING, 22 mm, lateral drift | eye level: two townsfolk cross, a pointing/laughing pair, guards; bunting overhead |
| 360..414 | sid 3 pillory AFTERNOON, 26 mm, slow push (cut in) | baker2 in the pillory, sad; a rotten tomato flies in from screen-left (g 383..391) and SPLATS on the board by his head (g 392); he flinches |
| 415..465 | sid 4 AFTERNOON, 24 mm, from behind the throwers (cut in) | woman1 laughs + points, man1 raises a cabbage (g 415..432), throws (g 433..436) -> it splats (g 446); baker2 flinches; man1 laughs |
Framing changes at g 313 / 360 / 415 (every 1.6-3.1 s, within the shots' own cuts). No near-still frame pairs. The two popcheck hits
(g 432->433, 436->437) are man1's raise->throw->laugh pose change (a real whip move), not errors.

## Numbers (`work/qa.txt`)
- render 14.4 s wall / 27.6 s CPU per frame (two 2-thread processes on 4 cores). Magenta / black frames: none; retried: none.
- hue shot 5 (MORNING) blue 48 red 24 orange 14 sat 0.32 (the blue-grey morning market); shot 6 (AFTERNOON) orange 21 red 21 blue 43
  sat 0.43 val 0.68 (ref a exteriors orange 24 blue 55 val 0.68). The red is the oak pillory close in sid 3-4; shade stays blue-violet.

## Differences from the plan / notes
- Each plan shot is split into two framings (wide->eye in shot 5, the hit->the throwers in shot 6) to hold a framing change every 1.0-2.0 s.
- The set has no crowd (placeholders only); the crowd is cast6 woman1/man1/guard copies on walk cycles and in `town_point` / `town_laugh`
  poses. baker3/4/5 are not used here (only baker2).
- Shot 6's two throws (a tomato already stuck on the board from an earlier pelt, then man1's cabbage) both read as comic splats.
