# Reference E: how the flat puppets sit in the 3D world

Source: `ref/e/ref.mp4` (45 s, 720x1280), frames every 0.5 s in `ref/e/frames2`. Looked at full size: f_001, 004, 006, 012, 020, 024,
026, 030, 037, 045, 050, 053, 060, 066, 073, 079, 084, 089 (close-ups, medium shots, wides, night and interior), plus the 90-frame
contact sheets `v8/cast/tmp/flat/refE_all0.png`, `refE_all1.png`. Numbers: `v8/cast/refE_measure.py` -> `v8/cast/out/refE_measure.json`
(sample windows drawn in `v8/cast/tmp/flat/refE_marks.png`). Nothing of the reference's characters, text or subject is copied.

## 1. Facing and distortion

- Every character is one flat drawing. It always faces the lens squarely and stays upright. There is no perspective skew of the
  drawing, no yaw foreshortening and no rounded shading, in any shot.
- Low camera (f_030, lens at knee height looking up) and high camera (f_012, f_020, looking down an aisle): the heads stay perfect
  circles and the bodies keep their proportions. The cards are turned to the camera in pitch as well as yaw.
- Depth comes from the 3D set, camera moves, lens blur (f_066 to f_073: foreground cat and crates blurred, character sharp) and
  parallax between characters and set. Characters overlap each other as whole flat shapes (f_012, f_089).

## 2. Turning and moving

- Turns are drawing swaps: front (f_045), 3/4 (f_037, f_060), profile-ish 3/4 for seated players (f_012), back (f_053, f_066 to
  f_073: hair cap only, no face). Within a view only the face features slide a little on the head.
- Acting: blinks and eye shapes, mouth shapes, stick arms that bend at an elbow, a hand prop (bottle, token). Walks are a 2-leg
  cycle with the body bobbing (f_024, f_026, f_053).
- No drawing rotates in depth. A character seen from above is still the same upright drawing.

## 3. Light on the characters (measured)

| Frame | Situation | White face | Costume | Surround |
|---|---|---|---|---|
| f_060 | night alley, in shade | L 0.40, hue 225, sat 0.55 (78,103,175) | orange L 0.21, sat 0.79 | wall L 0.24, hue 229, sat 0.58 |
| f_089 | night alley, in shade | L 0.34, hue 224, sat 0.57 | blue L 0.11 | wall L 0.21, hue 227 |
| f_026 | night, half in door light | lit half L 0.99 sat 0.01; shade half L 0.40, hue 225, sat 0.55 | blue L 0.31 | wall L 0.12 |
| f_001 | night, foreground, lamp pool | L 0.87, sat 0.04 | orange L 0.53, sat 0.90 | wall L 0.17 |
| f_084 | night, beside a warm window | L 0.79, sat 0.16, hue 355 | violet L 0.16 | wall L 0.19 |
| f_037 | interior | L 0.79, hue 26, sat 0.22 | orange L 0.56, sat 0.95 | wall L 0.75 |
| f_045 | interior close-up | L 0.76, hue 32 (warm) | orange L 0.55, sat 0.96 | wall L 0.59 |
| f_050 | interior | L 0.72, hue 12, sat 0.21 | orange L 0.49 | wall L 0.85 |
| f_030 | interior, low angle | L 0.97, sat 0.09 | orange L 0.37 | wall L 0.51 |

Reading:
- In night shade the white face takes the scene's shade colour: same hue as the walls (224 to 226), saturation about 0.55, and
  1.6 to 2.9 times the wall luma. As a multiplier on the drawn colour that is about (0.31, 0.40, 0.69) in sRGB. Costume colours
  are multiplied the same way (orange 221,122,22 lit -> 81,49,17 in shade).
- Inside a light pool the face goes to near white (L 0.79 to 0.99, saturation under 0.16), slightly warm near warm lamps.
- Interiors: face L 0.72 to 0.79 with a warm cast (hue 12 to 32, sat about 0.2). Costumes stay at nearly full drawn saturation.
- Scene light and set shadows fall across a character as on a flat plane: f_026 and f_001 have a hard vertical light/shadow split
  across the head. There is no terminator, no rounded falloff.
- A character with a bright light behind it (f_066 to f_073) is not blacked out: the body keeps its colour (violet L 0.33 against a
  wall at 0.14).

## 4. Outline, glow, shadow

- Outline: black, even weight, about 0.03 of the head width. It stays black in every light.
- Glow: a soft halo around the figure when a light is behind or beside it (warm halo in f_066 to f_073 and f_084, cool in f_060).
  Width about 0.1 to 0.2 head widths. The lit edge of the head also gets a thin bright rim.
- Ground shadow: a soft dark pool right under the feet (contact), plus a cast shadow away from the main light where the floor is
  bright enough to show it (f_004 stool shadows, f_053 long shadows across the carpet from the door). The shadow starts at the feet.
- Wet street floors also carry a blurred reflection streak of the nearby lights, not of the character.

## 5. Scale in frame

- Wide (f_006, f_079): figure height 0.10 to 0.20 of frame height.
- Medium (f_037, f_050, f_060): 0.45 to 0.60 of frame height, head 0.10 to 0.14.
- Close-up (f_045, f_084): head 0.25 to 0.35 of frame height, the figure cut at the hips or knees.
- Foreground over-shoulder figures are cropped by the frame edge and stay sharp or go slightly soft (f_001, f_060).

## 6. What v8 flat mode does with this (`v8/cast/stage8.py`)

- Cards face the camera in yaw and are pitched parallel to the sensor (clamped to 40 degrees), turning about the sole line. Measured on
  the neutral stage, camera 35 degrees down: keystone 1.000 and aspect error 0.000 in flat mode, 1.32 and +17.6 % in the old mode
  (`v8/cast/out/flat_test.json`).
- Shader `DZ8_flat`: colour = drawn colour x (AMB x TINT even fill + DIR x scene light on the flat card + BACK x light from behind).
  No normal map (NSTR 0). Ink guard keeps the outline black.
- Defaults: AMB 0.23 (divided by the shot exposure, `EXPO`), TINT (0.30, 0.45, 1.0) linear, DIR 0.20, BACK 0.10, GLOW 0.20 with radius
  0.16 D, card gap 0.03 D.
- Measured in the v9 set (`v8/cast/out/flat9/measure.json`): Kong's face in moon shade with the work lamp off L 0.60, hue 231,
  sat 0.18 against a road at L 0.16; in the work-lamp pool L 0.73 (S06) and 0.92 (S13), saturation 0.07 to 0.10; the driver in
  the cabin L 0.36 (per-shot AMB 0.40, TINT 0.72, 0.84, 1.0).
- Difference kept on purpose: our shade face is brighter and less saturated than the reference's (0.60 / 0.18 against 0.34 to 0.46
  / 0.55), so faces read on a phone in the rain. The set's sky fill, not the emissive fill, sets most of that level; lowering
  DIR toward 0.08 and AMB toward 0.15 moves it to the reference's numbers.
