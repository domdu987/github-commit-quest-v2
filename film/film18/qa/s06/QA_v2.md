# QA s06 (film 18, team 1) — "สิบตัว" (FINAL-gate fix 2)
Take: g 459-530 (72 frames), first_g 459, jimo_in DUSK, 720x1280, 12 samples, ~17 s/frame. transition_in: CUT.
Round-4 changes: the 10 plain oxen (no coats, no blades) were moved nearer the lens (y 15-17) so they and Tian Dan fill the frame, camera look-at raised, a child and an old man carrying baskets added at the right foreground from g 459, so bare ground is about 30 % at g 459-510 (was 40 %); dolly + 2.4 D truck + one held punch at g 497 as in round 3, no pulses; Tian Dan inside the frame all take.
FINAL-gate fix (Tian Dan cut by the left edge at g500-530): Tian Dan is now locked to the keyed camera (5.2 D in front of it, 0.55 D to the right of the axis, walk bounce kept), so his cap and body stay fully inside the frame (60+ px margin) for the whole take and nothing stands in front of him; the child and old man carriers stay lower left. cycles.transparent_max_bounces = 64. Everything else as before: 10 plain oxen (no coats, no blades), dolly + 2.4 D truck + one held punch at g 497.
Second FINAL fix (carrier regression): the world-fixed carrier child, old man and woman are gone from the lower left. One child (1.9 D) and one woman are now locked to the camera 6.9 D / 8.8 D ahead, 1.5 / 2.0 D to the left, so both are fully inside the frame with chins at about y 560-640 (far above y 850) on every frame g500-530 (phone strip checked at g500, 510, 520, 523, 527, 530). Camera look-at raised (z 1.6 -> 2.5) so plain ground is 0.23-0.30 (J.ground_share at g459 / 490 / 510 / 530: 0.29 / 0.30 / 0.28 / 0.23). Tian Dan as in fix 1 (fully in frame, nothing in front of him).
## Frame-diff (90x160 grey, in-shot)
median 5.87 (>= 4 OK), p90 8.64 (under 12: the tilt-up and the removal of the drifting carriers cost motion), min 1.97, max 11.02.
## Checks
qa_auto PASS. Heads above y 880, no mouths, no flames, no blades, no text.

## V2 fix (client: "camera shakes", 0:15-0:17) - 2026-11-22, render team 5
Base: s06 (render18/team1 c9258d107), rendered with film18/main's set3d18 (f7be8e4). Cause: `shk=0.016` hand-held noise, a 5-frame punch-in, 2 Hz walk/hop bounces. Fix: `shk=0.0`; punch-in eased over 14 frames (+10 %); bounces capped at 0.018 D / 1.5 Hz; the eased slide grew from -2.4 to -7.5 D (camera end (77, 13.8)) so frame-diff stays >= 4 with Tian Dan locked in frame. `transparent_max_bounces = 64`; crf 20.
- ground_check (`GCHECK=1 python3 shot.py draft`, every 10th frame, 0.05 D): **exit 0 / PASS** - 160 rows, 0 FAIL (GROUND.md).
- qa_jitter.py take.mkv: **no "shake" line**, overall median jitter 0.37 px.
- Frame-diff in-shot (n=71): median **4.62**, p90 5.58. qa_auto PASS. A scaffold ladder crosses the top-left corner in the last ~25 frames (set object passed by the truck).
