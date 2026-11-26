# v12/gauge: DEAD ZONE 09 gauge tubes

PROJ = `/tmp/claude-0/-home-user-github-commit-quest-v2/94b8b382-ecfe-5ec4-8832-97f03dd08322/scratchpad/dz09`. Folder: `PROJ/v12/gauge/`.
Glossy glass meter tubes that replace the v1 icon pops (`v4/iconfx`). They are drawn by code as SVG, rasterised by one headless Chromium page at the output resolution, and laid over the finished frame after every blur, so they are crisp at any size and in 9:16 or 16:9. Every gauge is a pure function of film time. No network, no image generation.
Edited outside this folder: only `v10/film/cues.py` (cue table) and `v10/film/finish.py` (compositing). The v1 versions are kept in `tmp/cues_v1_backup.py` and `tmp/finish_v1_backup.py`.

| File | What |
|---|---|
| `gauge.py` | `Track` (value over time), `Gauge` (one tube / badge), pictograms, `gauge_svg`, `frame_svg`. Pure Python, no bpy |
| `layer.py` | `Layer(gauges, W, H)`: SVG to RGBA through Chromium, `image(t)`, `over(frame, t)`, `safe_report()` |
| `film.py` | `build(Q, W, H, level, avatar_png)`: the film's gauges from `v10/film/cues.py`, picks the 9:16 or 16:9 table |
| `raster.py`, `raster_page.js`, `page.html` | copy of the v4 Chromium rasteriser (Kanit Black and Work Sans Black from `PROJ/fonts`) |
| `sheet.py` | writes `gauge_sheet.png` |
| `demo.py` | writes `gauge_demo.mp4` |
| `gauge_sheet.png` | every gauge at 6 values / states at 1.5x film size; left half on a dark film frame, right half on a bright one |
| `gauge_demo.mp4` | 720x1280, the gauges over the real draft frames (360x640 picture scaled up, gauges drawn at 720x1280), captions on |

## Look

- Tube: off-white sticker rim, thick ink outline (`#1f1d24`, 6 px on a 72 px tube at 720 wide, the cast's line weight), dark translucent glass, liquid with a cylinder gradient, a lighter meniscus, rising bubbles, a soft glow of the liquid colour inside and around the glass, fine tick marks every 10 % (long at 0 / 50 / 100), a highlight streak, a drop shadow.
- Badge: round glass button on the open end (vertical) or the left end (horizontal), same rim and outline, white pictogram with an ink line: `bolt`, `heart` (breaks when critical), `phone`, `warn`, `stopwatch`, `signal` (struck through when critical), `biohazard`.
- Colour follows the value: green, lime, amber, orange, red. `polarity="good"` means full is green; `"bad"` means full is red; a function `v -> badness` is allowed.
- Text is Kanit Black, shaped by Chromium (HarfBuzz). Checked by eye at 3x: `เชื่อใจ`, `สัญญาณ`, `อันตราย`, `น้ำเหนือ`, `แบต`, `สาย`: vowels and tone marks stack without collisions.

## Animation (all from `Track` keys)

| What | When | How |
|---|---|---|
| pop-in / pop-out | `t_in`, `t_out` | 7 frames in with overshoot and a small roll, 5 frames out |
| glide | key `"ramp"` | linear to the value, arriving at the key time; a small arrow pulses beside the surface while it moves |
| change | key `"hit"` | spring to the new value (about 15 % overshoot, settled in 0.4 s), white flash, shake, badge bump, a ring burst and droplets from the surface, an arrow and the delta number for 1 s |
| warning | badness >= `crit` | rim and glow pulse red at 3 Hz, badge wobbles, the tube trembles |
| cells | `segments=n` | discrete cells; a cell pops and flashes when it lights |
| quiet | `quiet=[(t, scale, opacity)]` | sits back smaller and dimmer |
| re-place | `moves=[(t, dict(...))]` | new position / orientation from t on (use on a cut) |

## Calling it

```python
import sys; sys.path.insert(0, PROJ + "/v12/gauge")
import gauge as G, layer as LY

tr = G.Track(0.62, [(24.9, 0.56, "ramp"), (28.25, 0.24, "hit"), (31.75, 0.02, "hit", 1.0)])   # (t, value, kind[, kick])
g = G.Gauge("trust", tr, t_in=22.3, t_out=33.25, x=100, y=470, w=72, length=330,
            picto="heart", label="เชื่อใจ", polarity="good", crit=0.9)
L = LY.Layer([g], 720, 1280)                 # any output size; the aspect is read from it
rgba = L.image(28.4)                         # PIL RGBA or None
out = L.over(frame_pil, 28.4)                # composite
print(L.safe_report())                       # {"problems": [(id, frame, "safe area" | "caption band", box)], "max_tubes_at_once": n}
LY.close()
```

`Gauge(id, track, t_in, t_out, x, y, w=72, length=330, orient="v", kind="tube", segments=0, polarity="good", crit=0.9, picto, label, number, side=1, quiet, delta_scale=100, moves, r, color, image, level, pop_out=True)`

- Positions and sizes are pixels of a frame whose SHORT side is 720 (720x1280 or 1280x720) and are scaled to the output.
- `orient="v"`: `x` = tube axis, `y` = top of the glass; the badge sits above `y`, the label below `y + length`. `orient="h"`: `x` = left end of the glass, `y` = axis; badge at the left, number or label at the right.
- `number`: function `t -> text`. On a vertical tube it is put before the label (`4 สาย`); on a horizontal tube it is the big figure at the right end.
- `side`: +1 or -1, the side the arrow and delta appear on. `delta_scale`: the delta number is `|dv| * delta_scale` (100 = percent, n = cells).
- `kind="badge"`: a badge alone (`r`, `picto`, `color`). `kind="avatar"`: picture badge (`image` = data URI from `G.data_uri(png)`) with sound arcs driven by `level(t)` 0..1, and a label.
- `Gauge.bbox(t)` returns the box in reference pixels (rim, badge, label; not the droplets or the delta number).

## In the film

`finish.py` builds the layer once (`gauge_setup`) and composites it last in `comp_frame`. `finish.py comp` prints the safe report and writes `out/<tier>_<size>/gauge_safe_report.json`. New options: `--base-size 360x640` finishes a small render at a larger `--size` (written to `out/<tier>_from360x640_<size>/`), `--name` names the finished-frames folder.

Safe area used by `safe_report`: 9:16 x 5-85 %, y 10-80 %, caption band y 860-1010 of 1280; 16:9 x 4-96 %, y 6-90 %, caption band y 484-568 of 720.

### Cue table (`v10/film/cues.py`, film seconds)

| Gauge | On screen | Values | 9:16 place (720x1280) | 16:9 place (1280x720) |
|---|---|---|---|---|
| `signal` (4 cells, new: replaces the radio rings) | 0.40-5.20 | 4/4; 2/4 at 2.06; 1/4 at 2.50; 0 at 3.24 (static), warning | left: x 100, glass y 470-800 | left: x 120, glass y 150-380 |
| `battery` (3 cells) | 16.22-19.00 | 0; 1 at 16.30; 2 at 16.50; 3 at 16.70; quiet (74 %, 82 % opacity) from 17.55 through S10 | right: x 556, y 470-800 | right: x 1160, y 150-380 |
| `calls` (4 cells, `N สาย`) | 19.05-22.05 | 1 at 19.20, 2 at 19.36, 3 at 19.52, 4 at 19.68, warning at 4 | left | left |
| `trust` (heart) | 22.30-33.25 | 62 %; glides to 56 by 24.94 and 38 by 27.34; drops to 24 at 28.25; glides to 14 by 30.35; drops to 2 at 31.75 (screen goes dark), heart breaks, warning | left; lies down at x 96-426, y 166 during S15 (28.96-30.35) because the close-up face fills the frame | right: x 1160 |
| `danger` (warning sign) | 33.50-45.22 | 10 %; glides to 20 by 34.61, 36 by 37.62, 54 by 40.28, 60 by 41.66; jumps to 100 at 41.66, warning; kicks at 43.45 (lunge) and 43.80 (bite) | left | left |
| `count60` (horizontal, stopwatch) | 46.43-50.37 | number 60, 59, 58, 57 in real seconds from 46.78; the tube loses 4.5 % per second | x 96-426, y 180, figure at the right | x 120-450, y 96 |
| voice badge `น้ำเหนือ` (restyled bubble) | 22.17-24.94, 27.34-28.96 | arcs follow the narration level | centre 112, 222, r 62 | centre 120, 130, r 50 |
| title mark (restyled) | 50.72-end | biohazard badge, amber, pops in | centre 360, 372, r 92 | centre 640, 190, r 70 |

Removed: the eye (41.66) and the shout rings (33.40): the danger tube carries both beats. At most one tube is on screen at a time, plus the voice badge during S12 and S14.

## Known gaps

- 16:9 has no rendered film frames, so its table is checked only against the safe area and the caption band, not against faces.
- The countdown tube is stylised: 4.5 % per second, not 1/60.
- `bbox` does not include droplets, the delta number or the exact label width (it estimates the label).
- One Chromium screenshot per frame: about 0.1-0.2 s at 720x1280.
