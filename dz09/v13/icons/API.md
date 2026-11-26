# v13/icons: DEAD ZONE 09 EP.1, flat status strip

PROJ = `/tmp/claude-0/-home-user-github-commit-quest-v2/94b8b382-ecfe-5ec4-8832-97f03dd08322/scratchpad/dz09`. Folder: `PROJ/v13/icons/`. Nothing outside this folder was edited.
Replaces the v12 gauge tubes. Drawn by code as SVG, rasterised by one headless Chromium page (Kanit Black from `PROJ/fonts`), no network, no image generation.

## Look

- Flat only: solid fills, one thick ink outline (`#1d1b24`, 6 units on a 100-unit icon), a thin flat light keyline (2 px at 720 wide) outside the ink so it reads on the night sky and on bright cars. No gradients, shadows, highlights, gloss or backing panel.
- One horizontal row from the top-left (9:16: x from 36, centre line y 172 of 720x1280; 16:9: x from 64, y 106 of 1280x720). Icons join in story order and stay as small quiet status items (0.78 px per unit, 92 % opacity; 0.50 once two newer icons have joined); the icon whose beat is playing is 1.43x (1.12 px per unit, about 112 px = 8.8 % of the 9:16 height) and carries its value horizontally to its right.
- Each icon is the thing itself and changes state: radio (arcs follow the voice, jitter, flat line + red cut mark, grey), battery (3 cells), phone (buzz, badge 1-4, name tag น้ำเหนือ), heart (level inside the heart + bar; crack; grey; splits), heartbeat badge (trace speeds up, green to amber, bar) that squeezes into a lid and snaps open as a red eye (lunge: one flat red flash), stopwatch (hand sweeps once a second, ring and bar empty, 60-59-58-57) that flies to the title spot and becomes the flat biohazard title mark.
- Motion on ones, eased, with springs on arrivals; value changes get a squash, a colour change and one flat burst.

## Calling it

```python
import sys; sys.path.insert(0, PROJ + "/v13/icons")
import icons13 as IC
rgba = IC.overlay(g, W, H, aspect="916")     # film frame g 0..1279 -> uint8 RGBA (H, W, 4), straight alpha; aspect "916" | "169"
rgb  = IC.over(rgb_uint8, g)                 # composite over an RGB frame (aspect from its shape)
IC.cue_table()                               # [(icon, joins, settles, [(film s, event), ...]), ...]
IC.close()                                   # stops Chromium (also at exit)
```

- Pure function of `g`; rasters are cached in `cache/<md5 of the SVG>.png`, so parallel workers can share it. Cold: about 0.1 s per frame per process (1280 frames at 720x1280 in about 40 s with 4 processes); cached: 2 ms per frame.
- Word-synced cues are read from `PROJ/audio/narr_ohm/captions_timing.json` (+0.30 s). Set `DZ09_NARR=narr_v1` in the environment to follow the v1 take instead. Picture cues are fixed: battery cells 16.30 / 16.50 / 16.70, radio cut 3.243, screen dark 31.75, driver lifts head 41.657, lunge 43.445, title 50.72.
- `LAYOUT` holds both placement tables; `shift = {shot: x0}` moves the row start for a shot where a head reaches into the strip.

## Wiring into `v10/film/finish.py` (not done here)

1. In `gauge_setup` / `comp_frame` drop the v12 layer (`_GA["L"].over(im, t)`); that also removes the v12 phone-voice badge and the v12 title mark, which v13 replaces (the mark) or does not use (the voice badge).
2. After the title plate block, composite v13 last, at the output size:
   ```python
   sys.path.insert(0, os.path.join(PROJ, "v13", "icons")); import icons13 as IC
   rgb = np.asarray(im.convert("RGB")); im = Image.fromarray(IC.over(rgb, g, "916" if H > W else "169"))
   ```
3. `cues.py`: `GAUGES`, `VOICE`, `TITLE_MARK` are no longer read; `STATIC`, `BITE`, `TITLE`, `HARD_CUTS` stay.
4. The title text in the `.ass` stays as it is (mark centre 360, 372, radius 92; text at y 600).

## Placement

| | 9:16 (720x1280) | 16:9 (1280x720) |
|---|---|---|
| row start x | 36 (5 %) | 64 (5 %) |
| row centre y | 172 (strip 116-228 = 9-18 %; nothing above y 102, bursts are clamped) | 106 (strip 54-158) |
| two beats old / quiet / active scale (px per unit) | 0.50 / 0.78 / 1.12 | 0.47 / 0.73 / 1.04 |
| longest row | x 36-561 = 78 % (countdown, 46.6 s) | about x 64-560 |
| shot shifts | none (S08-S09: the row stays top-left over Kong's out-of-focus foreground face) | none set (16:9 was never rendered; check when it is) |
| fades | 32.21-32.70 s: the whole row at 35 % while Kong's head sweeps through the strip (S16) | none set |
| title mark | centre 360, 372, r 92 | centre 640, 190, r 70 |

Checked against the 360x640 draft frames (2 x upscaled). Faces under the strip: S09 (the out-of-focus foreground face, by choice) and S16 32.3-32.6 s (head sweeps through; the row is faded to 35 %). Hair tips come close in S10 and S15.

The heartbeat trace is phase-locked to the mix: `heartbeat_low.wav` starts at 38.68 and 40.68 and its thump is 0.147 s in, so the spike and the badge pulse fall on 38.827 and 40.827 (`HB`).

## Cue table (film seconds, narr_ohm take)

| Icon | Joins | Settles | Events |
|---|---|---|---|
| radio | 0.10 | 5.30 | 0.10 walkie-talkie pops in, arcs follow the voice; 2.15 arcs jitter, amber; 2.62 arcs jitter harder, red; 3.24 arcs collapse to a noisy then flat line, red cut mark; 4.09 body goes grey; 5.30 settles: small grey radio with the cut mark |
| battery | 15.92 | 17.04 | 15.92 empty battery pops in; 16.30 cell 1; 16.50 cell 2; 16.70 cell 3 + burst; 17.04 settles: small full battery, stays to the title |
| calls | 17.55 | 21.95 | 17.55 phone pops in, buzzing; 17.81 badge 1; 18.25 badge 2; 18.69 badge 3; 19.13 badge 4 + burst; 21.08 badge stretches into the name tag น้ำเหนือ; 21.95 tag folds back into the badge, settles: phone with 4 |
| trust | 22.00 | 32.30 | 22.00 heart pops in where the tag was, level 82 %; 24.94 sinks to 60 %; 26.34 sinks to 52 %; 27.34 sinks to 28 %; 27.96 crack; 28.96 sinks to 17 %; 30.35 sinks to 7 %; 31.75 empties, goes grey, crack runs through; 32.05 splits, halves drop apart; 32.30 settles: small grey broken heart |
| danger | 33.62 | 43.70 | 33.62 green heartbeat badge pops in, bar 12 %; 37.62 beat speeds up, green to amber, bar to 55 %; 41.46 trace flattens, badge squeezes into a closed lid; 41.66 red eye snaps open, bar full red + burst; 43.45 one flat red flash + shake; 43.70 settles: small red eye |
| countdown | 46.43 | 50.22 | 46.43 stopwatch pops in with 60; 47.78 59; 48.78 58; 49.78 57; 50.22 row fades, the stopwatch flies to the title spot and turns into the biohazard mark; 50.72 title mark lands + burst, holds to the end |

## Files

| File | What |
|---|---|
| `icons13.py` | everything: cues, drawing, layout, raster, `overlay`, `over`, `cue_table` |
| `raster_page.js`, `page.html` | the Chromium rasteriser page (copy of v12's) |
| `env.npy` | narration level per frame (made from `narr_ohm/narr_final.wav` on first use) |
| `base.py`, `sheet.py`, `strip.py`, `demo.py` | newest draft frame per film frame; builders of `sheet.png`, `strip.png`, `demo.mp4` |
| `sheet.png` | every icon in its key states at 2.1x film size, dark and bright background |
| `strip.png`, `strip_small.jpg` | 43 frames, one per icon change, top 520 px of the 720x1280 frame (4320 px and 2400 px wide) |
| `demo.mp4` | 53.32 s, 720x1280, icons over the newest draft frames (new look where rendered, draft v1 elsewhere), ohm captions, `mix_ohm_v2.wav` |
| `cache/` | raster cache (safe to delete) |

## Film v3 change (made from `v10/film`, on the director's note): `keep`, larger quiet icons, larger title mark

- `LAYOUT[aspect]["keep"] = n` (new, optional): an item fades out and gives up its place in the row once `n + 1` newer items have joined. 9:16 has `keep=2`: the current icon plus at most the two most recent quiet ones. `scene()` got three lines for it; no icon drawing changed. Without the key the row behaves as before (16:9 is untouched).
- 9:16 sizes: `q` 0.78 -> 0.96, `m` 0.50 -> 0.88 px per unit. Narrowest quiet item (radio, 46 units): 44 px wide, 40 px once two newer have joined (was 36 / 23). Active stays 1.12.
- Longest row is now x 36-508 = 71 % of the width (was 78 %); ink rows y 102-241 (measured over every second frame).
- 9:16 title mark: centre (360, 350), radius 118 (was 372, 92); the title text in `v10/film/captions_ohm.ass` is libass size 124, about 485 px wide, centre y 612.
- The tables above describe the state before this change. The copy from before is `v10/film/tmp/v3/icons13_before.py`.

## Leave times (user note with reference clip, after film v3)
9:16 LAYOUT now has `keep=None` and `out={radio 6.40, battery 19.30, calls 33.00, trust 33.00, danger 45.90}`: an icon fades out
(8 frames) once its story beat is done, then its gap closes (5 frames). Nothing stays as a permanent row; 6.7-15.9 s has no icon.
The stopwatch still flies to the title mark. Previous version: icons13_keep2.bak.
