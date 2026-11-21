# v3/set3d_ext/beach: what the shot plan asks of the beach set (shots 8, 16, 23, 24)

Files:
- `beach_ext.py`: the extension module.
- `bshot.py`: the runner shared by the beach takes, with actors.
- `bqa.py`: the QA, meta, cues and contact sheet of a take.
- `tex/`: the cobweb, spider and boater cards, rasterised once by `v3/set3d/raster.js`.

The extension imports `v3/set3d_beach/beach3d.py` (as `BX.B`) and never edits it. The set's `API.md` and `REVIEW.md` still apply.

The worked examples are `v3/film/s16/shot.py` and `v3/film/s23/shot.py`.

```python
import sys; sys.path.insert(0, PROJ + "/v3/set3d_ext/beach")
import beach_ext as BX                       # registers the preset STORM_APPROACH in beach3d.PRESETS on import
A = BX.build("storm_approach")               # plan light names: beach_sunny | grey_drizzle | storm_approach | storm
                                             # -> beach3d anchors + A["ext"] (dressing anchors), A["cams"] gains the three new cameras
cam = BX.B.make_camera(BX.cam_pose("beach_shore_eye"))
BX.B.set_fog_bank(0.6, frame=1); BX.set_fog_near(0.55, frame=40)       # the fog band grows and slides in toward the shore
BX.set_windows(0.8, frame=40); BX.set_sign_swing(0.08, frame=40)
```

`build(light, clear=True, dressing=True, boater=False)` calls `beach3d.build(<preset>)` and then adds the dressing below into a collection named `BEACH_EXT`. Pass `boater=True` for shot 24.

## 1. Light presets

| plan name | beach3d preset | notes |
|---|---|---|
| `beach_sunny` | `SUMMER_SUN` | unchanged |
| `grey_drizzle` | `GREY_DRIZZLE` | unchanged; the takes use `set_rain(0.35)`, `set_fog_bank(0.25)`, `set_wind(0.3)` |
| `storm_approach` | `STORM_APPROACH` (**new**) | see below |
| `storm` | `STORM` | unchanged |

`STORM_APPROACH` starts from `GREY_DRIZZLE` and changes the following:
- **Light.** Key K, ambient A and A_pale are each multiplied by 0.75. The shade tint is (0.36, 0.36, 0.56).
- **Sky.** A bruise-violet sky runs from `#3a3466` at the zenith through `#6a5f8e` to `#8e7f98`. One sick yellow band (`#c2b27c`) sits at elevation t of about 0.11, just above the fog band, over a greyish horizon. Clouds are violet-grey (`#4d4672` and `#7d7398`).
- **Sea.** It is like glass. Streaks are almost gone (0.04). The sea is dark (`#2e3658` near, `#4c5076` far) with a pale `#a69fae` horizon band.
- **Fog.** `#d4cac6` at the top and `#b2a8ad` at the foot (the plan's pale card is `#c9bfbd`).
- **Sand.** The drizzle tones are multiplied by 0.8.
- **Grade.** Grade saturation is 1.22 and object saturation 0.95.

The preset is meant to be used with fog 0.06 to 0.9, rain 0 and wind 0.04 to 0.6.

hue_report on s23's frames: see `film/s23/QA.md`. The sky reads violet and blue by design, so violet runs above the office band.

## 2. Cameras (`CAMS`, `cam_pose(name)`, also in `A["cams"]`; 22 mm)

| name | loc | look_at | what it shows |
|---|---|---|---|
| `beach_shore_eye` | (-7.4, 7.0, 2.6) | (22, 5.0, 1.054) | **THE BEACH FRAMING** (shots 16 and 23). It looks along the shore toward +x, azimuth -3.9 deg, pitch -3 deg, horizon at 0.47 H. Layout: the sea, surf, umbrella and deck chair at left; the LONG ISLAND sign mid-right (x about 405-555); the boardwalk and fence; cottage_07 with its vane and chimney and the poles at right; the fence-gap landing in the right foreground. The man's mark is about 5 D ahead. |
| `beach_high` | (-2.4, 10.0, 5.0) | (9.6, 8.6, 1.30) | shot 8 start. It is the vista_high axis, lower: 5 D up, -17 deg, 12 D from the deck chair, horizon at about 0.31 H. The sea is at left and the cottages and poles recede at right. The deck chair and umbrella are centred. The crash push x3 goes onto the chair. |
| `beach_low_wave` | (-6.0, 7.0, 0.7) | 20 D ahead at azimuth +11 deg (the beach framing's axis turned 15 deg toward the sea), pitch +8 | shot 24 start pose: 0.7 D above the sand, clear of the boat |

Probe stills: `film/s16/work/probe/*.png`.

## 3. Dressing (`EXT` holds the positions; each builder returns its anchors in `A["ext"]`)

| item | where | controls |
|---|---|---|
| **LONG ISLAND sign** (`li_sign_*`) | `EXT["sign"]` = (2.0, 4.9), between the boardwalk and the fence, face yawed 65 deg toward -x | `set_sign_swing(amp_rad)`, plus 0.10 x wind of lean |

The sign has two posts 2.95 D high with a crossbar. The board, 2.3 x 0.98 D, hangs on two chains from a pivot at z 2.85. Its face is the paper registry's `beach_sign` (LONG ISLAND large, BATHING BEACH - SUFFOLK COUNTY 1938 small, English). The set's BATHING BEACH sign (`sign`, `sign_face`) is hidden. The face reads in the beach framing (about 150 px wide) and from `beach_high`.

| item | where | controls |
|---|---|---|
| landing + step (`landing`) | the fence gap, x -3.2..-1.4: deck from the boardwalk edge y 4.6 to 5.95 at z 0.36, then one step y 5.95..6.25 at z 0.18 | none |
| weather vane and brick chimney | vane and chimney on `cottage_07` (`EXT["vane_cottage"]`), a second chimney on `cottage_06` | `set_vane(deg)` |
| towel line (`li_towel_line`, `li_towel`, `li_pegs`) | the porch front of `cottage_06` | `set_towel(0/1)`; flaps with wind |
| lit windows (`li_windows`) | every cottage front | `set_windows(0..1)` |
| banging shutters (`li_shutter_*`) | every cottage front | `set_shutters(0..1)` |
| cobweb + spider (`li_cobweb`, `li_spider`) | between the umbrella pole (7.2, 9.4) and the deck-chair arm (9.6, 8.6), z 0.4-1.2 | `set_spider(0..1)` |
| fog ring radius | the set's `fog_bank` | `set_fog_near(k)` |
| flying boater (`li_boater`, `build(boater=True)`) | anywhere | `set_boater(frame, loc, spin_deg, scale, visible, cam)` |

More on each:
- **Landing.** It is where beach_man "steps off the porch" in shot 16. The set has no porch on the sea side of the fence.
- **Weather vane and brick chimney.**
  - The vane: an iron post with compass arms, an arrow and a rooster silhouette, on the ridge over the porch end.
  - The vane swings with the wind.
  - The chimney: brick with a cap, on the roof near the back.
  - Both sit at the bottom edge of shot 16's tilt to the sky.
- **Towel line.**
  - A sagging line between the porch posts, with a red and cream striped towel 0.7 x 0.78 D and two pegs.
  - The towel is hidden while `towel_on` < 0.5; key it to 1 on the frame the woman pegs it (shot 8, 14.0).
- **Lit windows.**
  - Emissive panes 0.40 x 0.60 D on both front windows of each cottage, camera rays only.
  - `set_windows` blends them from dark `#2b3150` to `#ffd995` at strength 1.9, hazed with distance.
- **Banging shutters.**
  - Two hinged boards per front window, painted `#3d5a6e` with ink.
  - Each swings out to 75 deg at `shutters` = 1, on its own phase: `1.31 x shutters x sqrt(abs(sin(0.37 f + phase)))` rad.
- **Cobweb and spider.**
  - The cobweb is a 0.9 D card of white silk.
  - The spider is a card on its thread. `set_spider(1)` lowers it 0.35 D (shot 8, from 15.70).
- **Fog ring radius.** `set_fog_near(k)` sets the ring radius to 300 x k by keying the x and y scale. The set's driver keeps the height (`set_fog_bank`). Shot 23 uses k 1 -> 0.55 so that the band "slides toward the shore".
- **Flying boater.**
  - A card drawn with `acting.flying_hat_svg('beach_man')`, 2 x 1 D, self-coloured, turned to face the camera you pass.
  - Hide the boater on the puppet with `hat_off` (acting `beach_shocked`).

## 4. Runner (`bshot.py`)

A take module defines the following and ends with `BS.run(sys.modules[__name__], sys.argv[1:])`:

| name | meaning |
|---|---|
| `TAKE`, `SHOTS`, `LIGHT` | take id, shot numbers, plan light name |
| `G0`, `G1`, `H_IN`, `H_OUT`, `R0`, `R1` | film frame range, handles, rendered range |
| `TRANSITION_IN`, `VERSION` | transition in; version stamp of the render |
| `cam(g)` | returns `(loc, look)` |
| `state(g)` | dict with the keys fog, fog_r, rain, wind, sea, wave, sign_sw, windows, shutters, spider, towel_on, vane |
| `ACTORS` | list of `dict(name, cast, ppd, shadow, contact)` |
| `actors(g)` | returns `{name: None or dict(feet, pose, hands=None, flip=False)}` |
| `CUES` | sound cues |

| command | what it does |
|---|---|
| `probe [a:b:step]` | head x, y and width and the camera pitch, without rendering; written to `work/probe.json` |
| `still g [scale samples]` | one frame to `work/still_g.png` |
| `draft [a:b:step]` | 360x640 at 6 samples to `work/draft/`, plus `work/draft_contact.jpg` |
| `render [a:b]` | final 720x1280 at 12 samples on 2 threads to `raw/`. Resumable: a frame is done when its PNG and `raw/meta/g.json` (same VERSION) both exist. On frames whose camera moves faster than `post.STREAK_MIN` and that have actors, it also renders the `plate/` (no actor cards) and `matte/` (actor cards over a holdout set, rain hidden) |
| `post` | camera streak by `shots/post.py`'s method; actors stay sharp over the streaked plate |
| `qa` | `meta.json`, `cues.json`, `contact.jpg`, `work/qa.json` |

Details:
- Every frame keys the camera, the set controls (LINEAR) and the actor placement.
- Actors are `stage.actors.Actor` cards.
- `head_flip` is set from the key's screen side per frame.
- Sprites are rasterised per frame. Puppet poses come from `v3/acting` (keys starting with `_` are stripped by the takes).
- Set `shadow=None` for no cast shadows (drizzle).

## 5. Limits

- **Sign placement.** The sign stands between the boardwalk and the fence, not by the fence gap. At the gap it was always behind the near man in the beach framing. One of its posts stands on the boardwalk deck.
- **Fog ring.** It is the set's ring brought in by scaling, so its billowing top scales too. At k 0.55 its height is still 30 x a^0.75 D.
- **Windows and shutters.** They exist on the cottage fronts only, not the sides or backs.
- **Towel.** It is one rigid striped card that flaps by rotation, not cloth.
- **Woman's porch mark.** The porch of cottage_07 is at x 9.15, y 1.05, z = 0.6 x the cottage scale. In the beach framing she is about 46-51 px, at x about 580-610, just right of the sign.
