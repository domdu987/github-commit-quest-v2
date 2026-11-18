# Captions and typography (measured by the main session)

## Measurements (720x1280)
| Property | Value | Evidence |
|---|---|---|
| Font | Work Sans Black (weight 900) is the closest free match: 0.9 % mean width error over 4 phrases; double-storey g, square dots | ref/crops/captions/font_candidates.png |
| Font size | 50 px (ascender-height word "called" = 36 px tall fill) | b/t24.5 |
| Fill | pure white #FFFFFF | all |
| Stroke | black, 4 px each side (stem 10 px wide, stroke runs of 4 px) | a/t12.5 row 900 |
| Shadow | soft dark halo about 2-3 px beyond the stroke, low opacity | crops |
| Position | horizontally centred (x = 359-360), vertical centre of the text line at y = 900 (70.3 % of height) | 60 consecutive frames at 11.5 s of clip A |
| Words per caption | 1 to 3 words, one short phrase at a time, sentence case, punctuation kept | OCR pass |
| Animation | NONE: text is at full size on its first frame and is replaced by a hard swap (width constant across every frame of a phrase) | 60 consecutive frames |
| Duration | about 0.2 to 0.6 s per phrase (6 to 18 frames at 30 fps), synced to narration | same |

## How to reproduce
- Font file: proj/fonts/WorkSans-Black.ttf (converted from npm @fontsource/work-sans).
- ASS style: Fontname "Work Sans Black", Fontsize 50 (libass sizes run slightly small, calibrate so that "called" is 36 px tall), white primary, black outline 4, shadow 1.5 with 50 % alpha, alignment 5 with \pos(360,900), no \t animation.
- Group narration word timestamps into 1-3 word phrases; never exceed about 16 characters per caption.

## Differences vs v1
1. v1 used DejaVu Sans Bold 46 with a pop-in scale animation; the reference has no animation and a heavier, wider face.
2. v1 outline 5 px, reference 4 px.
3. v1 centre y 915, reference 900.
