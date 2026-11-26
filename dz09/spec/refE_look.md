# Reference E look: set, light, shadow, camera (measured)

Source: `ref/e/ref.mp4` (720x1280, 30 fps, 45.03 s), frames every 0.5 s in `ref/e/frames2`. Scripts and raw numbers: `v11/set/analysis/` (`cuts.py`, `an2.py` -> `shots_motion.json`; `meas.py` -> `frame_stats.json`). Luma is Rec.709 on display values, hue/sat/value are HSV. Do not copy the reference's characters, text or subject; this is finish and grammar only.

## 1. Set construction

- **Real 3D boxes, drawn surfaces.** Streets, alley walls and the hall are simple 3D geometry (parallax and perspective are true under the moving camera). Surfaces are flat colour fields with a slow gradient, not photographic materials. No noise texture, no grime maps.
- **Ink outlines on set objects.** Every object edge and many interior details (vents, pipes, window grids, cables) carry a thin dark line, 1.5-2.5 px at 720 wide, dark navy in night scenes. Thin-dark-line density (black-hat 5 px > 28): 1.6-2.8 % of pixels at night, 4.7-5.5 % in the bright interiors. Canny edge density 3.5-5 % night, 6.5-9 % interiors.
- **Detail density.** High in the lit mid-ground (signs, crates, bottles, vending machine, lantern, posters), sparse in the dark surround. Every frame has 3-6 distinct props near the action.
- **Sky.** A clean vertical gradient: top hue 222, S 0.89, V 0.29; horizon hue 219, S 0.75, V 0.51. No clouds, no moon.

## 2. Light

Measured on night-street frames (f_002-008, 055-089) and interiors (f_010-052).

| | night street / alley | interior |
|---|---|---|
| luma mean | 0.20-0.30 | 0.33-0.55 |
| luma p5 / p50 / p95 | 0.04-0.09 / 0.16-0.20 / 0.43-0.93 | 0.04-0.16 / 0.26-0.60 / 0.85-0.93 |
| share below luma 0.05 | 0.5-8 % (shadows are never black) | 0-6 % |
| mean saturation | 0.58-0.64 | 0.44-0.50 |
| shadow hue (V < 0.35) | 230-271 (blue to violet), S 0.60-0.70 | 350-18 (warm brown), S 0.5-0.77 |
| lit hue (V > 0.75) | 25-30 (amber windows) or 295-350 (magenta neon), S 0.27-0.63 | 23-33, S 0.27-0.40 |
| hue share | blue 32-78 %, violet 4-31 %, magenta 2-15 %, red+orange 5-30 % | red+orange 62-80 % |

- **Practicals are the only light sources.** Neon sign (hue 331, S 0.74, V 1.0), amber windows (hue 28, S 0.55, V 0.94), a lit doorway (hue 19, V 1.0), a red paper lantern (hue 12, S 0.88, V 0.85), a blue vending machine, a warm service window (V 1.0). No visible key from outside the frame.
- **Each practical owns a coloured pool** on the wall and the ground next to it: wall beside the neon hue 320, S 0.60, V 0.78; ground pools hue 282 (magenta, V 0.76) and hue 234 (blue, V 0.91) against a road of hue 240, S 0.70, V 0.29. Lit to surround ratio in value: 2.6-3.1 : 1.
- **Glow / bloom.** The service window (half-width about 80-130 px) carries a halo whose luma falls 0.85 -> 0.51 at the source edge, 0.38 at +70 px, 0.25 at +150 px and reaches the wall level (0.23) at about +200 px: bloom reach about 0.28 of the frame width beyond the source. The halo keeps the source colour.
- **Light shafts.** Soft cones only as glow gradients (no hard volumetric beams). Ceiling tubes in the hall bloom into the ceiling.
- **Wet ground reflections.** Every light drags a vertical streak down the ground: under the lit door the reflection holds luma 0.76 -> 0.50 over 160 px and fades to the road level (0.22) at about 200 px, i.e. 1.3-1.5 x the door height; the neon sign's streak runs about 500 px (to the frame edge). Streaks are soft-edged, straight, slightly broken.
- **Vignette.** Corner / centre luma: 0.25-0.40 in close and medium night shots, 0.58-0.69 in wide night shots, 0.72-0.77 in interiors.

## 3. Shadows

- Characters cast a **soft dark ellipse on the ground** under and slightly behind the feet (f_060: shadow V 0.35 against 0.29-0.71 ground; hue 267). No long projected shadows.
- Shadow colour is the surround colour (blue-violet), never grey or black.
- Characters with their back to a light are **dark silhouettes with a thin rim** (f_057, f_066: hair V 0.11, body rim S 0.72, V 0.78). Characters facing a light stay evenly bright with a tint.

## 4. Depth

- **Three layers in every shot.** Foreground: a dark, blurred silhouette (a character's shoulder / head at a frame edge, a plant, crates, a cat) covering 10-30 % of the frame. Mid-ground: the action in the brightest pool. Background: glowing signs and windows, blurred.
- **Tilt-shift depth of field.** Laplacian sharpness by fifths of frame height (top to bottom), night: 3-19 / 13-43 / 33-57 / 13-37 / 2-7. The bottom fifth is 8-20 x softer than the middle; the top fifth 2-10 x softer.
- Lens blur on the foreground layer: 6-14 px radius at 720 wide.

## 5. Camera

No hard cuts: 10 of the 11 shot changes are 0.15-0.5 s motion-blurred whip / push transitions. The camera never stops. Median shot length 2.9 s (1.4-10.2 s).

| # | time (s) | angle, height | lens (est.) | move, speed (% of frame per s) | character size |
|---|---|---|---|---|---|
| 1 | 0.0-2.25 | eye level, OTS past a foreground figure | 28 mm | fast push-in, zoom +44 %/s | head 0.10 -> 0.20 W |
| 2 | 2.25-4.8 | starts low at street level, cranes up to a 50 deg high aerial, roll +18 deg | 24 mm | pull-back -53 %/s | figures 0.10 H -> specks |
| 3 | 4.8-10.5 | eye level, one-point perspective down an aisle | 22 mm | fly-through, +109 %/s easing to +43 %/s | passing heads 0.12-0.25 W |
| 4 | 10.5-13.85 | low angle (about 15 deg up), 3/4 | 28 mm | lateral track 8 %/s | head 0.20 W |
| 5 | 13.85-16.45 | slightly low, side-on along a row | 24 mm | lateral track 14.5 %/s, zoom -5 %/s | head 0.28 W |
| 6 | 16.45-24.05 | eye level two-shot | 35 mm | push-in +26 %/s easing to +7 %/s (mean 13) | head 0.14 -> 0.30 W |
| 7 | 24.05-26.95 | eye level, full figures | 30 mm | push +10 %/s with a 5 %/s pan | figure 0.45 H |
| 8 | 26.95-37.1 | eye level, OTS; ends behind the subject's back | 28 mm | one long push +19 %/s easing to +6 %/s, drifts 2.4 %/s | figure 0.30 -> 0.55 H |
| 9 | 37.1-40.8 | high angle about 35 deg down | 35 mm | slow push +7 %/s, pan 3 %/s | figures 0.15-0.20 H |
| 10 | 40.8-43.6 | eye level MCU, 3/4 | 45 mm | push +9 %/s | head 0.38 W |
| 11 | 43.6-45.0 | low three-shot | 30 mm | pull-out -5 %/s | heads 0.20 W |

Holds drift at 5-13 %/s (push) or 3-8 %/s (pan). Entrances and transitions run at 40-110 %/s and always ease out.

## 6. Numeric targets for DEAD ZONE 09 (night expressway)

| quantity | target | v9 | v11 (look stills) |
|---|---|---|---|
| luma p5 | 0.04-0.09 | 0.01-0.03 | 0.06-0.10 |
| luma p50 | 0.16-0.22 | 0.16-0.33 | 0.22-0.28 |
| share below luma 0.05 | under 8 % | 8-16 % | 0 % |
| mean saturation | 0.55-0.64 | 0.38-0.56 | 0.33-0.47 |
| shadow hue | 230-250 (our blue; no violet drift past 255) | 224-261 | 230-260 |
| corner / centre luma | 0.25-0.65 | 0.28-1.2 | 0.40-1.2 |
| bloom reach | 0.28 W past the source, source colour | 60 px, blue-tinted | 95 px sigma, source colour |
| ground streak length | 1.3-1.5 x source height | physical only | physical + 240 px smear |
| ink line density | 1.6-2.8 % | 0.3-1.0 % | 0.3-0.7 % |
| bottom-fifth blur | 8-20 x softer than the middle | lens DOF only | tilt-shift 3-8 px |
| pools | every practical has one, lit : surround = 2.6-3.1 : 1 in value | sodium, work lamp | + red / blue throws, amber, green sign |

## 7. Eight camera templates (aspect-parametric; H = frame height, W = width; 9:16 values, 16:9 in brackets)

| id | name (ref shot) | height, angle | lens | subject size | move | depth of field | use in EP.1 |
|---|---|---|---|---|---|---|---|
| E1 | OTS push (1, 8) | eye level 2.4 D, foreground shoulder covers 15-25 % at one edge | 28 (24) | head 0.12 -> 0.22 W | push-in 17 %/s easing to 6 %/s | foreground blur 10 px, tilt-shift on | S13, S16 |
| E2 | Crane reveal (2) | start 1 D above the deck, end 14 D up looking 45-50 deg down, roll up to 12 deg | 24 (20) | figures 0.10 H -> 0.04 H | pull-back 40-50 %/s for 2.5 s, ease out | deep; tilt-shift on | S01, S24 |
| E3 | Lane fly-through (3) | eye level, one-point perspective between the car rows | 22 (18) | passing heads 0.12-0.25 W | dolly forward 100 %/s easing to 40 %/s | near objects streak past, blur 8 px | S02-S04 |
| E4 | Low lateral track (4, 5) | 1.0-1.3 D, 10-15 deg up, subject 3/4 or side | 28 (24) | head 0.20-0.28 W | track 8-14 %/s, no zoom | background blur 6 px | S06, S10 |
| E5 | Two-shot settle (6) | eye level | 35 (30) | heads 0.14 -> 0.30 W | push 26 %/s easing to 7 %/s over 3 s, then drift | background blur 5 px | S07, S12 |
| E6 | High tilt-shift wide (9) | 10-14 D up, 30-35 deg down | 35 (30) | figures 0.15-0.20 H | push 7 %/s with a 3 %/s pan | top 10 % and bottom 20 % blurred | S24, S05 |
| E7 | MCU push (10) | eye level, 3/4 | 45 (40) | head 0.35-0.40 W | push 9 %/s | background blur 10 px | S13, S20, S22 |
| E8 | Low group pull-out (11) | 1.2 D, 8 deg up | 30 (26) | heads 0.20 W | pull-out 5 %/s | mild | S23, title lead-in |

Rules for all templates: never lock the camera (minimum drift 3 %/s); join shots with a 4-8 frame motion-blurred push or whip in the direction of the next move; keep a dark foreground element in at least two of every three shots; keep the brightest pool on the subject and no lamp lens within 0.16 W of a head.
