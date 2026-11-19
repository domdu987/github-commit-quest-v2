# QA_TECH s22 (film 12, shots 22-23, g 1573-1784) - TAKE gate
Method: all 42 f6 frames + cut n_01..n_10 (n 80-89) read at full size, phone_sheet.jpg, plus per-frame numeric checks (frame diff, Laplacian).
f_NNN = f6 frame, n = take frame (n = (f-1)*5), g = 1573 + n.

## VERDICT: FAIL (5 blocking issues, 4 minor)

## Verified OK
- Cut: real hard cut at n 83 (g 1656). Frame diff n82->n83 = 43.2 vs median 6.9; n_03 (wide rank) -> n_04 (box_seat close, pink umbrella). qa_auto's "no visible change" is a false negative (shared sky/palette/coach). Cut is on plan.
- No black/blank/magenta frames; no frozen run (rain and camera move every frame); no sharpness drop (no frame < 60 % of median Laplacian); no DOF blur; no text in picture.
- Heads never cross y 880 (max head y about 640 in f_001-f_017; about 535-590 in shot 23).
- Mouth: coachman mouth closed/straight in every frame f_001-f_042 (shot 23 f_018-f_042 checked at full size). No quote after 34.95 s -> correct.
- Rain continuous across the cut; coach colours (red/yellow body, red wheels) and lamp post consistent across the cut. Pink canopy is salmon-pink (known, accepted).

## Blocking issues
1. Pink umbrella NOT held in his hand - f_018-f_042 (n 85-205), cut frames n_04-n_10. His arms are crossed/tucked; the pole ends at his right shoulder/upper chest (about x 470, y 720 in f_042, x 430, y 690 in f_018), behind/over the arm, with no hand on it. It reads as an umbrella stuck on his shoulder. Fix: give the card a pose/hand sprite with one fist gripping the pole where it ends (pole bottom inside the fist), the other arm crossed or on the knee; keep the sulk.
2. Umbrella canopy clipped by the right frame edge - f_033-f_042 (n 160-205), worsening to about 20-25 % of the canopy and 2-3 pompons out of frame at f_042 (pompons at x>700 cut). Also the right lamp post clipped from f_018 on. Fix: shorten the push or offset the camera target left/lower so the whole canopy stays inside with a margin of about 30 px through g 1784.
3. Shot 22 subject clipped at the right edge - f_013-f_017 (n 60-82): the lead horse's head/muzzles run out of frame (x=720), plus the right lamp post cut at f_016-f_017. The "bored horses" (hanging heads) are exactly the cropped part. Fix: end the push with the full horse heads inside the frame (pan camera 0.5-1 m right or stop the push earlier).
4. Plan coverage shot 22 (empty bored rank) not clearly readable on the phone sheet (g 1573-1648 thumbnails): only one coach with a coachman is readable, the other coaches are tiny/occluded behind the lamp, and the other two coachmen are indistinguishable specks (f_001-f_017, x 300-360, y 570-600: floating small faces over the roof). The bottom 40-45 % of every frame (y 800-1280) is empty cobbles/puddle. Nothing says "rank". Fix: tilt up/dolly so 3-4 coaches in a row are in frame, horses with hanging heads side-on and visible, less cobble foreground; check that the two other coachmen read as bored/glaring at phone size.
5. Plan coverage shot 23 (empty coach) not readable - f_018-f_042: the cabin shows only a sliver on the left (x 0-250) with dark windows, the interior/empty seats are never seen; the bottom 25-30 % (y 1000-1280) is a muddy dark orange/purple horse rump and shafts, unreadable shapes that eat the frame; from f_033 the red box front fills the bottom. The "empty coach" beat is not communicated, only "man under umbrella". Fix: reframe so the cab door/window with empty seats is in frame (camera left/back), drop the horse rump from the frame or lower the camera angle so it does not dominate.

## Minor
6. Grain/noise - f_001-f_017 (shot 22): visible speckle noise in the cobbles and puddle reflections in the lower half (clear in f_001, f_002, f_008). Fix: more samples or stronger denoise on shot 22, or crop the empty lower half (see 4).
7. Contact - shot 22 f_013-f_017: horse hooves/fetlocks have no visible contact shadow on the cobbles (lit cobbles directly under the hooves). Shot 23 f_036-f_042: boots on the box deck have no shadow, a thin light grey strip under the boots makes him look slightly hovering over the dark deck. Fix: add a blob shadow under hooves/boots.
8. Shot 22 -> 23 reads as a jump-zoom, not a new shot: same coach in the right half, same lamp, same direction (n_03 vs n_04); the umbrella pops in at the cut with no cue in shot 22 (he stands bare-headed in the rain). Non-blocking, but a bigger angle change (different side/height) would make the cut clearer.
9. Coachman b/c card heads in shot 22 (f_001-f_018) are bodiless faces sticking out over the coach roof; at f_016-f_018 the face turns into a 25 px red/white mask. Fix: show their torsos or remove the extra cards and keep one clear glare.

## Not verifiable
- Breathing sway on the shot 23 card: region diffs are non-zero but include camera motion, so a separate sway cannot be confirmed. The take is not frozen.
