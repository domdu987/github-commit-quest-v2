# v4/iconfx: DEAD ZONE 09 icon effects

This folder holds flat 2D icons in the puppets' ink style and in the finish of the new reference (`ref/c`). They come out of Python as SVG and Chromium turns them into PNG. Every icon has a pop-in, hold and pop-out that is a pure function of the film frame g. You can use an icon in two ways:

- **as an emission-only card inside the lit Blender world.** It is never lit and casts no shadow, but it still gets depth of field and motion blur and is hidden by anything in front of it.
- **as a screen-space overlay laid on the finished frames.** Use this for icons that explain a rule.

Everything is deterministic. No paid API or network call is used. Nothing outside this folder is edited: the code only reads `PROJ/fonts`, the reference frames and `v3/tools/hue_report.py`.

| File | What |
|---|---|
| `icons.py` | the SVG generators: palette, wobble, ink outline, rim and shadow filters, 19 icons, `make`, `placed`, `to_svg`, `META` (meaning and suggested sound accent) |
| `anim.py` | `Cue`, `pop_state(cue, g)`, the pop profiles, `overlap(cues)`, easing |
| `raster.py` + `raster_page.js` + `page.html` | one persistent headless Chromium page (Playwright). SVG goes in, straight-alpha PNG comes out. Work Sans Black (`WS`) and Kanit Black (`Kanit`, which shapes Thai) are loaded from `PROJ/fonts` |
| `overlay.py` | screen-space placements, one full-frame transparent layer per g, PIL composite, caption-band and edge check |
| `blender_card.py` | `bake` (a PNG sequence of the icon's own animation), `add_card` (an emission card), `key_pop` (scale, roll and hide keyed per frame), `project` (world point to pixel) |
| `sheet.py` | contact sheets |
| `test_pop.py` | the 2D overlay test MP4 and its pixel measurements |
| `demo_blender.py` | a 3D night-expressway stand-in with world cards and one overlay; renders the test MP4 |
| `measure_card.py` | Cycles checks: colour exactness, sequence frame mapping, pop widths |
| `study/` | crops and 30 fps frames of the reference graphics used to match the finish |

## 1. Calling it

```python
import sys; sys.path.insert(0, "PROJ/v4/iconfx")
import icons as I, raster
from anim import Cue, pop_state

ic = I.make("stopwatch", t=0.8, speed=20)            # Icon(body, w, h, anchor), design units (100 x 100 box)
svg, W, H, anchor_px = I.to_svg(ic, px=256, name="stopwatch")   # transparent SVG; 100 units = 256 px
raster.render([{"svg": svg, "w": W, "h": H, "out": "/abs/sw.png"}])

cue = Cue(g_in=120, hold=45)                         # profile "brief" by default
st = pop_state(cue, g)                               # visible, scale, opacity, rot_deg, t (icon clock), phase
```

### Screen-space overlay (9:16, 720x1280)

```python
import overlay as OV
P = [OV.Placement("stopwatch", Cue(300, hold=90), x=560, y=230, px=190, kw={"speed": 20}),
     OV.Placement("sound_rings", Cue(310, hold=40), x=lambda g: track_x(g), y=520, px=260, kw={"mode": "arcs"})]
lay = OV.render_layer(P, g, "/abs/ovl/o_%04d.png" % g)     # None when nothing is visible
OV.composite(frame_png, lay, out_png)                       # scaled to a same-aspect frame (360x640); other aspects raise
print(OV.safe_report(P))                                    # [(icon, g_first, g_last, "caption band"|"edge", box)]
```

- `x`, `y` and `px` can be functions of g. To follow a world point, use `blender_card.project(scene, cam, xyz)` per frame.
- The caption band is y 860 to 1010 (captions sit at y 900 of 1280). The side gutter is 16 px. `safe_report` uses the 115 % overshoot box with the rim and shadow included.

### 16:9 (review fix)

Every shot also has a 16:9 framing. Pass `frame="16:9"` (1280x720; presets in `OV.FRAMES`, or a `(w, h)` tuple) to `render_layer` and `safe_report`, and give `x`, `y`, `px` in pixels of that frame. The caption band keeps the same fraction of the frame height (y 484 to 568 of 720). `composite` scales a layer only to a frame of the same aspect; a 9:16 layer on a 16:9 frame now raises an error instead of being stretched. `blender_card.project` uses the scene's `resolution_x/_y` unless `w, h` are given (it used to assume 720x1280, which misplaced 16:9 overlays that follow a world point). `demo_blender.py ... --aspect 16:9` renders the same set and camera path in 16:9 (`out/demo3d_16x9/`).

### Phone readability (review fix)

Size world cards in screen pixels, not metres: `BC.height_for_px(scene, cam, location, px)` returns the `height` that makes 100 design units `px` pixels tall on a 720-short-side frame at that spot. `BC.readability_report(scene, cam, [(ob, "symbol"|"text_cap")], frames)` lists frames where a held card is smaller than `BC.MIN_PX` (symbol 64 px, text cap 22 px; for a label set `ob["iconfx_cap"]` to the text height per 100 units, about 0.17 for `tape_label` at size 24). Reference sizes on 720x1280: X marks about 90-110 px, check about 140 px. For a row of X marks use ONE world height (nearest X at about 110 px) so the row shrinks with depth like the reference.

### In the 3D world (inside a bpy process)

```python
import blender_card as BC
cue = Cue(g_in=40, hold=60)
bk = BC.bake("rings", "sound_rings", {"mode": "arcs"}, cue, "/abs/tex", px=256)      # animated=False: one PNG
ob = BC.add_card(bk, height=2.8, location=(2, 9, 3.9), facing="camera", camera=scene.camera)
BC.key_pop(ob, cue)      # Blender frame = g + 1 (convention); CONSTANT keys on scale, Z roll, hide_render
```

- **Card origin and size.** The origin of the card is the icon's anchor, so the pop scales about it. `height` is the world size of 100 design units.
- **`facing` options:**
  - `"camera"`: a Copy Rotation constraint from the camera keeps the card parallel to the image plane. The constraint's mix mode is BEFORE, so the pop's roll kick turns the card in screen space.
  - `"flat"`: the card lies on the ground, `yaw` turns it. This is how the reference's tape lies on the road.
  - `"fixed"`: uses the `rotation` you give.
- **Material.** Emission at strength 1, mixed with Transparent by the PNG alpha. `emission_sampling = NONE`, so the card lights nothing.
- **Visibility.** The card is seen by camera rays only. `reflect=True` lets the wet road mirror it.
- **Animated textures** are an image SEQUENCE with `name_%04d.png` numbered by Blender frame. `bake` also writes frame `first - 1`, because Blender asks for that frame while the card is still hidden. Cycles reads a new file every frame, so the stale-texture trap in `v3/stage/REVIEW.md` (one path rewritten while persistent data is on) cannot happen.
- **Pop resolution.** The pop is the object's scale. The texture is baked at 100 % inside a canvas padded 25 %, so the overshoot stays sharp.
- **View transform.** Colours come out exact under the `Standard` view transform. Any later grade or compositor applies to the cards as well.

### Sheets and tests

```
python3 sheet.py                 # out/sheet_night.png, out/sheet_light.png, out/strips_night.png
python3 test_pop.py              # out/poptest/pop_test.mp4, pop_contact.png, pop_measure.json
python3 demo_blender.py out/demo3d --frames 0:48 --scale 0.5 --samples 10   # out/demo3d/demo_3d.mp4
python3 measure_card.py          # out/measure/measure_card.json
```

## 2. Icons (`icons.ICONS`), all taking `t` (seconds on the icon's own clock) plus these options

| Name | Options | Inner animation |
|---|---|---|
| `battery` | `level` 3/2/1/0 (an int, or a function of t), `blink_hz` | 3 green, 2 yellow, 1 red. Levels 1 and 0 blink at 2.5 Hz; level 0 adds a yellow bolt |
| `phone` | `n` (badge number, default 4), `buzz` | rotates ±6° at 14 Hz for 0.45 s of every 0.8 s, with buzz arcs |
| `heart` | `crack_at` 0.15, `split_dur` 0.25 | the zigzag crack draws on, then the two halves split and tilt ±12° |
| `pinky` | `split_at` 0.3, `split_dur` | two hooked little fingers pull apart; red crack ticks fly out |
| `sound_rings` | `mode` "arcs" or "circle", `period` 0.9, `n` 3, `span`, `dot` | a ring is born every period/n; it grows 10 to 48 units (ease-out), thins and fades |
| `eye` | `open_t` 0.12, `ticks` | the lid opens, the red pupil contracts from 10 to 6 between 0.25 and 0.45 s, alert ticks appear |
| `stopwatch` | `total` 60, `elapsed` or `speed` | a red wedge and hand sweep from 12 o'clock while the number counts down |
| `biohazard` | `disc` (yellow sticker), `spin`, `color` | optional spin |
| `warning` | `symbol` "!" or "bio", `color` YELLOW or RED | pulses ±4 % at 2 Hz |
| `exclaim_sparks` | `spread`, `bang` | the 3 yellow strokes shoot out in 0.12 s, then breathe; ±1.2 shake for the first 0.4 s. The anchor goes on the top of the head |
| `question` | — | the scribble swirl turns −200°/s; the "?" rocks ±8° |
| `sweat` | `slide` 8, `period` 1.2 | slides down and stretches (LOOK_SPEC 2.9 colours) |
| `light_rays` | `n` 12, `hz` 2, `spin` 25, `beacon` | turns and pulses (opacity 0.55 to 1) |
| `x_mark` | `outline` 0, `strike` | reference: flat red, no outline. `strike` draws one bar, then the other, 4 frames each |
| `check` | `draw` | reference: green, ink outline, round caps. `draw` strokes it on in 0.2 s |
| `tape_label` | `label`, `family` "WS" or "Kanit", `size` | the box width comes from the real font metrics (PIL with raqm) |
| `tape` | `length`, `grow` 0.5, `unit`, `start_num` | rolls out; ticks every unit/5, numbers every unit, red start diamond |
| `swoosh` | `r`, `a0`, `a1`, `dur` 0.22, `lag` 0.14, `width` | reference: white glowing tapered arc round a character; the head runs, the tail follows, then it fades |
| `arc_fan` | `n`, `src`, `dur`, `stagger` | reference: thin yellow trajectory arcs drawn on one after the other |

**Palette.** Red `#e2453b`, yellow `#ffd23f`, infected green-grey `#8fa37a`, white `#f4f1ea`, ink `#1f1d24`. The brief has no green, so the check and the full battery use `#2fbf3f`; the reference check measured `#24c434`.

**Finish**, from the `ifx_fin` filter in `I.defs()`:
- a pale rim at a 1.4-unit dilate, 90 % opacity
- a drop shadow offset (1.6, 2.6) units, blur 1.6, ink-black at 40 %
- ink outline 4 units (4 % of the icon)
- wobble seeded per icon, amplitude 0.5 to 0.8 units, baked into the outline (no filter noise)

**Finish overrides.** `rim=False` and `shadow=False` can be passed per placement. Rings, rays, tape, swoosh and arc fan have the rim off by default (`META`).

## 3. Pop profiles (`anim.PROFILES`; scale per frame from `g_in`)

| Profile | Pop-in | Pop-out |
|---|---|---|
| `brief` (default) | 0, 0.62, 1.15, 1.06, 1.00, with a roll kick of −8, −5, +3, +1, 0° | 1.08, 0.55, 0 (opacity 1, 0.6, 0) |
| `snap` | 0.65, 1.00 | cut |
| `soft` | 0, 0.35, 0.75, 1.04, 1.08, 1.03, 1.00 | as `brief` |

- `snap` matches the reference: its green check at t 50.4 s measured 91, 139, 141, 141 px wide at 30 fps (study/pop).
- `soft` is for large world cards (title, warning).

`Cue(g_in, hold, profile, pop_out=True, rot=True)` exposes `g_hold`, `g_out` and `g_end`. `anim.overlap(cues)` lists the frames where two icons show at once; the brief allows that only in the climax.

## 4. How the reference draws its graphics (`ref/c/frames2`, crops in `study/`)

- **Red X marks** (f_097 to f_104): flat red, about (252, 87, 83) under that grade. They have no ink outline and square-ish ends. They are anchored in the world, one above each tank in a receding row, so perspective and depth of field shrink and soften the far ones. They pile up one after another as the narration counts.
- **Green check** (f_102): green (36, 196, 52) with a dark outline of about 3 px on a 28 px stroke, plus a 1 px pale rim. It has round caps, is screen-placed, and snaps in over 2 frames.
- **Yellow measuring tape and label** (f_052 to f_056): the tape lies flat on the road in 3D, with ticks, numbers and a red start diamond. The label is a yellow (238, 188, 77) rounded box with a dark border and dark capitals, standing in the world and blurred by depth of field.
- **Arc round a character** (f_120 to f_123): a white glowing tapered swoosh about 150° around the figure, one or two frames long. It reads as a motion trail, not a ring.
- **Yellow arcs** (f_115 to f_118): thin pale-yellow trajectory curves fan from one source and draw on. Green checks pop at their ends.

## 5. Measured

- **Raster cost:**
  - one 720x1280 overlay layer: 98 ms mean, 258 ms max (Chromium screenshot route, two to four icons)
  - the sheets: 365 / 207 / 615 ms
  - baking 5 cards (about 160 PNG): 8 s
- **Pop on rendered pixels, 2D overlay** (warning icon alone; width relative to hold): 0, 0.615, 1.159, 1.077, 1.011, 1.0. The expected values are 0, 0.62, 1.15, 1.06, 1.0. The ±3 % during the hold is the icon's own pulse.
- **Pop in Cycles** (stopwatch card): 0, 0.623, 1.146, 1.053, 1.0, 1.0.
- **Card colour in Cycles** (an orange 3000 W point light and a red 2000 W point light right beside the card):
  - flat interior pixels against the baked PNG: max difference 1 level, mean 0.17
  - `#e2453b` renders as (226, 69, 59) and `#f4f1ea` as (244, 241, 234)
  - edge pixels differ through the texture filter and pixel filter: mean 6.5 levels over opaque pixels, p99 58 at 1-px edges
- **Image sequence:** 4 of 4 frames rendered the PNG of their own frame.
- **3D demo** (360x640, 10 samples, OIDN, 2 threads): 5.5 s/frame mean, 6.7 s max.

## 6. Known gaps

- `demo_blender.py` is a crude stand-in for the expressway, there only to prove the cards. It has no rain, fog or motion blur and no grade. Its hue row (blue 74 %) is far from the EP.1 band, and it is not a film shot.
- The Thai label and badge text depend on the two fonts in `PROJ/fonts`. In Kanit Black, "ม." reads heavy at small sizes, so keep `size` at 24 or more.
- `pinky` is the weakest drawing: the hooked fingers read as an S at small size. Prefer `heart` for the promise.
- Overlay layers go through the DOM-screenshot route (about 100 ms a frame). A 55 s film costs about 3 min of overlay rastering.
- An overlay that must sit behind a foreground object needs a world card instead; overlays always sit on top.
- Sound accents in `META` are labels only. No SFX is generated here.
