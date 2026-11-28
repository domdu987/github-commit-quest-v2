# v15/picto: DEAD ZONE 09 EP.1, animated pictograms

PROJ = `/tmp/claude-0/-home-user-github-commit-quest-v2/94b8b382-ecfe-5ec4-8832-97f03dd08322/scratchpad/dz09`. Folder: `PROJ/v15/picto/`. Nothing outside this folder was edited.
Drop-in replacement for `v13/icons/icons13.py` and `v14/cards/cards14.py`, after the user's note on v14: "icons: less text, more picture, more movement, no background, easy on the eyes, prettier than this". Drawn by code as SVG, rasterised by one headless Chromium page, no network, no image generation.

## Look

- No panel, card, box, tab or bar. One HERO pictogram at the top-left (left edge x 36, centre line y 186 of 720x1280, about 150-175 px tall; v13's active icon was about 90), plus at most one small companion to its right.
- Flat: solid fills, ink outline, one off-white keyline (2.6 px at 720 wide) round the silhouette so it reads on night sky and on white cars. No shadow, gradient, glow or texture. Loose particles (flecks, shards, arc fragments) are drawn without the keyline so they stay crisp.
- Three stroke weights (4.6 / 3.0 / 1.9 units, round joins). Palette: icons13's PAPER, INK, ORANGE (Kong's vest), AMBER, RED, GREEN, BLUE (phone screen), plus `SICK` `#9fd356` (the driver's green, heartbeat trace), `SCREEN` `#232a40` (dark glass) and `DEEP` `#b3202f` (red one step down).
- No words anywhere. Two numbers only: the red badge on the phone (1-4) and the amber number beside the stopwatch (60-57), Kanit Black digits.
- Every pictogram moves on every frame it is up (idle breathing / sway of 1-1.5 %, the heart's beat, the monitor's sweep); the large moves sit on the story cues.

## Calling it (same as icons13 / cards14)

```python
import sys; sys.path.insert(0, PROJ + "/v15/picto")
import picto15 as IC
rgba = IC.overlay(g, W, H, aspect="916")     # film frame g 0..1279 -> uint8 RGBA (H, W, 4), straight alpha; "916" | "169"
rgb  = IC.over(rgb_uint8, g)                 # composite over an RGB frame (aspect from its shape, or pass it)
IC.cue_table()                               # [(pictogram, joins, leaves, [(film s, event), ...]), ...]
IC.close()                                   # stops Chromium (also at exit)
IC.LAYOUT["916"], IC.LAYOUT["169"]           # x0, y, s, shift {shot: (x0, y)}, dodge [(t0, t1, dx, dy)], fade, out, title
IC.T                                         # the cue-time class of icons13 (same object)
```

- `DZ09_NARR` (default `narr_ohm`) is read by icons13 on import, as before.
- Pure function of `g`. Rasters are cached in `cache/<md5 of the SVG>.png` (safe to delete; parallel workers can share it).
- Cost at 720x1280, one process at nice 15 while the final render held all 4 cores: cold 0.042 s per frame on average, 0.105 s worst; cached 0.006 s (256 frames, `check.py`).

## Switching `v10/film/finish.py` (not done here)

In `icons()` replace the two lines

```python
        sys.path.insert(0, os.path.join(PROJ, "v14", "cards"))   # user: themed info cards (v14) replace the bare v13 row
        import cards14
        _IC["m"] = cards14
```

with

```python
        sys.path.insert(0, os.path.join(PROJ, "v15", "picto")); import picto15 as cards14
        _IC["m"] = cards14
```

(i.e. one import line changes; the `v13/icons` path line above it can stay, picto15 adds it itself.) `icons_over()` calls `.over(rgb, g, aspect)` and `comp()` calls `.close()`; both exist. Without editing the file: `import finish, picto15; finish._IC["m"] = picto15` (how `demo.py`, `on_film.py`, `facecheck.py` ran finish.py's own `comp_frame`).

## Pictograms (film seconds, narr_ohm take)

| Pictogram | In | Leaves | What it does |
|---|---|---|---|
| radio | 0.10 | 6.40 | Orange walkie-talkie pops in with a bounce, antenna whips. Three arcs and five display bars follow the narration level (the voice travels outward through the arcs). 2.15 arcs jitter, amber; 2.62 harder, red. 3.243 arcs shatter into 12 fragments that tumble, fall and shrink away; 3.33 a red slash snaps across the body; 3.8-4.6 the colour drains to grey from the top, the body droops, the antenna hangs. From 4.7 one small grey arc tries to get out every 1.25 s and dies. 6.40 sinks and fades. |
| battery | 15.92 | 19.30 | Upright empty shell drops in and squashes. 16.30 / 16.50 / 16.70 a green cell slams in from the right with a squash, the shell jolts, green flecks fly. 16.78 amber bolt pops (one blink at 17.08), 16.92 hop. 17.55 (cut to S10) hops aside and becomes the small companion beside the phone; 19.30 slides off right and fades. |
| calls | 17.55 | 33.00 | Phone with an incoming call on its screen pops in buzzing (rotation shake, vibration ticks). Red badge 1 / 2 / 3 / 4 at 17.81 / 18.25 / 18.69 / 19.13: pop, the digit flips, a red ring wave goes out, flecks on the 4th. Then one short buzz every 1.3 s. 22.00 hops aside and becomes the companion beside the heart (badge 4 stays); 31.75 its screen goes dark; 33.00 sinks and fades. |
| trust | 22.00 | 33.00 | Glass heart with red liquid at 82 %. It beats all the time (1.33 beats/s at 82 %, 0.79 at 7 %, stops at 31.75); the liquid has two wave layers and bubbles, and sloshes on every fall. Levels are `icons13.trust_level`: 24.94 -> 60, 26.34 -> 52, 27.34 -> 28, 28.96 -> 17, 30.35 -> 7, 31.75 -> 0; droplets fall from the tip each time. 27.96 crack, grows at 28.96, 30.35, 31.75. 31.75 empty and grey. 32.05 splits, halves swing apart about the tip; 32.21-32.70 whole layer at 35 %; 32.74 halves drop. |
| danger | 33.62 | 45.90 | Round heart monitor (paper bezel, dark glass, graticule, two screws, a knob). A head runs left to right every 1.6 s and draws the trace. Beats at 34.24, 35.39, 36.53, 37.68, 38.83, 40.83 with strength 1, 1, 0.9, 0.76, 0.58, 0.30 (the last two are on the heartbeat thumps of the mix); a small heart blinks with each. Green to amber between 37.8 and 40.3; flat after 41.1. 41.45 the disc squeezes shut into a closed eyelid with lashes. 41.657 the eye snaps open: red iris, slit pupil, shards; pupil darts left / right / left and locks forward by 42.6; veins creep in until 43.4; slight tremble. 43.28 squint; 43.445 pupil dilates and the eye lunges (scale 1.36 at g 1045); g 1045 only: inverted frame (red sclera, white iris), on the film's own flash frame (`cues.LUNGE_FLASH`). 43.9-45.2 four drips. 45.90 fades. |
| countdown | 46.43 | title | Stopwatch pops in, amber 60 slides out beside it. From 46.78 the hand turns once a second, continuously; the amber ring steps down. 47.78 / 48.78 / 49.78: 59 / 58 / 57 flip in (old digit leaves upward, new one overshoots), the watch kicks, the crown clicks with two tick marks. 50.22 the number folds away and the watch flies along icons13's path to the title spot, details retract, face floods amber, biohazard mark grows in. 50.72 title mark lands + burst. |

Nothing on screen: 0.00-0.08, 6.67-15.92, 33.29-33.58, 46.17-46.42 s.

## Placement (9:16, measured on every frame 0-1204 by `check.py`, alpha > 24)

- Ink stays inside x <= 396 (55 %) and y 90-290 except: g 6-9 radio pop-in (y 84), g 37 (y 89), g 82-159 dead radio (y to 294), g 383-420 battery at its shifted place (x to 450 = 62 %: the flying cells and flecks), g 531-534 phone hop to companion (y 79), g 797-798 falling heart halves (y 295, nearly faded), g 1045-1046 lunge (y 83), g 1117-1120 stopwatch pop-in (y 86).
- `shift = {"S08": (292, 186), "S09": (292, 186)}`: Kong's large foreground face fills the top-left of S09 (x 0-290), so the battery plays at x 292 on the dark sky beside him; S08 has the same shift so the battery does not jump at the cut.
- `dodge` is empty; it is there for a glide of a few frames inside a shot (`(t0, t1, dx, dy)` in reference px).
- `fade = [(32.21, 32.70, 0.35)]` (from icons13).
- 16:9: `x0 64, y 120, s 0.64`; renders, never looked at over a picture.

## Differences from v13 and v14

- v13: a row of small icons with value bars / name tag. v15: one large pictogram, no bars, no tag, no row; redrawn (radio with display and two-tone body, upright battery, phone with call screen, liquid heart, sweep monitor that becomes an eye with veins and lashes, stopwatch with crown, pusher and minute marks).
- v14: navy cards with labels, values, sub-lines, chips, zone tab. v15 has none of that and no Thai text.
- Same as both: cue times (`icons13.T`), leave times, the 32.21-32.70 fade, trust levels, the title mark. Frames g 1217-1279 are pixel-identical to `icons13.overlay` (checked by `check.py`; T.TITLE is g 1218). During the flight (g 1206-1216) the path formula is icons13's, starting from the hero position.
- The danger trace weakens and slows to a flat line (v13's sped up); the lunge flash moved to g 1045 to coincide with the film's (v14 had g 1043).
- `LAYOUT` keys: `x0, y, s, shift {shot: (x0, y)}, dodge, fade, out, title` (no `q / a / m / gap / band / keep`).

## Files

| File | What |
|---|---|
| `picto15.py` | everything: layout, drawings, raster, `overlay`, `over`, `cue_table` |
| `raster_page.js`, `page.html` | the Chromium rasteriser page (copies of v13's) |
| `sheet.py` -> `sheet.png` | key states of each pictogram at 1.2x film size, dark and light background |
| `motion_strips.py` -> `motion_strips.png` | 10 consecutive frames of 8 events, 1:1 |
| `on_film.py` -> `on_film.png` | 12 moments over clean draft frames (finish.py's `comp_frame`, no captions) |
| `demo.py` -> `demo.mp4` | 53.33 s, 720x1280, pictograms over the draft frames, film captions, `mix_ohm_v2.wav`, CRF 20 |
| `facecheck.py`, `check.py` | face-check sheets in `tmp/`; title equality, cost, ink extent, empty stretches |
| `cache/`, `tmp/` | raster cache and working files (safe to delete) |
