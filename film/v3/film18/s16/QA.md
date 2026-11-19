# QA s16 (render team 5, film 18) — frames g1205-1308 (+10 handle in for the 15-frame dissolve, +6 out: take.mkv g1195-1314, 120 frames), jimo_in NIGHT
Render: Cycles 12 samples 720x1280, 2 threads, 15.9 s/frame alone, ~25-35 s with four renders sharing the 4 cores. Per-frame animated cards (c18.py), all setters keyed by direct setting on every rendered frame.

## Frame-diff (90x160 grey, in-shot g1205-1308, n=103)
median **4.65**, p90 **13.71** (min 0.44, max 19.23). Target >= 4 / >= 12: met.
Camera: slide -55 px/s along the wall (x 50 -> 30), push 0, six quick swings (+-6 deg pans, 0.95 / 1.05 snaps). Diggers swing the pick through 4 lean/angle drawings every 3 frames and bob 0.07 D; the child bobs.

## qa_auto
PASS (QA_AUTO.md, phone_sheet.jpg).

## Brief items
- Breach glow doubled: every breach gets a real warm point light (2600 W) once it opens, on top of the set's dark opening + warm interior; the openings read dark with a warm rim and glow on the ground at phone scale.
- Holes open one after another 0 -> 12 (hole x 41 first) across the shot; diggers (6 townsfolk + 1 child with basket) between the holes, comic, nobody hurt.
- Foreground: set's pick-and-baskets prop (left) plus dark ground props (baskets, rope, pots) in the lower part to fill the bare ground.
- Cast cards re-baked from the current cast18 (set_work/cards deleted before rendering).

## Checks (6 fps look)
heads above y 880 (head tops y 300-680 px of 1280); hooves/feet on the ground with contact shadows; picks held; mouths still; continuity with s17 (same wall, holes = 12 at the end of the shot).

## Deviations / history
- First finals ended with a close-up of an empty wall and tripped the blur check; the camera move was softened (no push) and the whole take re-rendered.
- Frame-diff of the plan's 6-10 %/s push could not be kept: it ran the camera into the wall; swings and slide give the frame-diff instead.
