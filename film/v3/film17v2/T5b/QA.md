# QA self-check: T5b (T5 part b), g1211-1296, 86 frames, 720x1280, 30 fps

Scope: this part covers g1211-1296 only. g1297-1383 is rendered by T5b2. I did not compare g1211-1215 against T5a's g1210, because T5a's frames were not available to me (only scripts on its branch).

## Numbers
- Luma (RGB mean, 90x160 bilinear): part mean **93.3**, min 89.3, max 102.4. Target 90-108: inside. Largest step between neighbouring frames 2.4.
- `qa_auto.py`: PASS, 0 hard cuts, magenta 0.0 % (QA_AUTO.md, phone_sheet.jpg).
- `rhythm.py`: 86 frames, in-shot median 16.67, p90 20.82.
- check_take(T5) hits=[] and check_face(T5) ok: both PASS before rendering.

## What changed from the prepared recipe (all director-approved)
- Camera override from g1250 (eased in by g1274), raised to about 1.5 m above floor (override.json).
- Day lights scaled to 0.78 (eased in over g1211-1241). Night values copied from T5a.
- Skylight beam fx OFF for the whole part (beam_scale = 0 on every frame, incl. g1211-1218, re-rendered after the director's follow-up because T5a is beam-off too), because the beam veiled the whole frame. Verified: g1240 via beam_k=0 equals a direct strength-0 render (diff 0.000). Re-measured after the g1211-1218 re-render: luma unchanged (mean 93.3, max step 2.4); g1211 viewed at 360x640 and clean.
- Cast-leak fix: stale c2_/back_* actors cleared before every stage_cast2. Frames g1212-1264 and g1265-1296 were re-rendered after fixes; g1211-1218 were re-rendered last, beam-off, in their own process after a warm-up frame.
- Mouths closed on every frame (no talk option used). Mid-take acting follows the plan: escort held, Dupont shrug in the second half.

## Frames viewed at FULL size (720x1280) and at phone size (360x640 strip)
- **g1211**: one gendarme standing arms folded, centre; ladder and drawer wall behind; a trolley with boxes at right edge, partly cut by the right edge; blue/red runner in the lower third; feet on the floor with a contact shadow. No veil, no shaft. The inspector is not visible here and Dupont is not visible.
- **g1240**: the camera is low at the left; an escort gendarme's arm and body are CUT by the left frame edge (only the sleeve and part of the coat show); another gendarme sits behind a desk with books and a lamp; stool visible; floor tiles large in the lower third. No veil, no shaft. Edge-cut: yes, at the left.
- **g1264**: a foreground gendarme is CUT by the left edge (half head, arm, coat); a second gendarme stands mid-frame, a bearded figure with glasses (Bertillon) is at the desk at right, gallery rail above. No veil; clean. Edge-cut: yes, at the left.
- **g1275**: a large foreground gendarme at the left, head and torso fully readable but his left side is cut by the left edge slightly; the inspector (moustache, arms folded) and Bertillon behind at centre-right; GRAND plates visible. No veil, no shaft over any card.
- **g1285**: Dupont (brown coat, cap), a blue gendarme and a green-uniformed gendarme in a bunched row, plus a dark blue figure partly hidden behind Dupont; all heads readable, none cut; feet on floor. No veil.
- **g1296**: left to right the inspector (smirk, arms folded), Bertillon, Dupont with the shrug, and a gendarme; all fully inside the frame with margin; no veil.
The 6-frame phone strip shows the same: faces readable at 360x640, runner at the bottom 15-25 %.

## Known issues (for the director)
1. Foreground escort gendarme cut by the left frame edge in about g1235-1275 (seen in g1240, g1264, g1275). This is on the prepared side-track path, which I did not change before the override starts at g1250. It breaks the "no character cut by the frame edge" rule.
2. A dark blue figure is half-hidden behind Dupont at g1285 (cards overlap in the escort row).
3. g1211-1215 not compared against T5a's g1210 (no T5a frames available).
4. I viewed 6 frames at full size and a strip; I did not view every frame. Black slabs or ghosts in unviewed frames are ruled out only by the luma step check (max 2.4) and the cast-leak fix.
