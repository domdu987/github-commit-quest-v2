# QA s05 (film 18, team 1) — Tian Dan receives the sash (round 7)
Take: g 384-458 in-shot (75 frames) + 8 handle frames before (g 376-383); first_g 376, n_frames 83. jimo_in DUSK, 720x1280, 12 samples, ~17 s/frame. transition_in: dissolve 11.
Round-7 changes: v1 ground lumps removed (no dress_ground output kept: v2 with actor clearance placed only ~9 stones, so it is not used here); the sky texture is replaced by a cloudless gradient (cloud / sun sticker gone for the whole take); camera end framing pulled back / left so the old man and the sash stay inside the frame to g 458; four camera-locked basket carriers (child, old man, child, woman) fill the lower third with all heads above y 880; dolly + truck + one held +10 % punch, staged hand-over as before.
## Frame-diff (90x160 grey, in-shot g 384-458)
median 7.19 (>= 4 OK), p90 11.18 (target >= 12: just short), min 1.83, max 14.20.
## Checks
qa_auto PASS. Heads above y 880, no mouths, no text, no oxen.
Known: bare ground at the bottom is about 28-32 % (violet dirt with a few stones); the sky is a plain gradient; fg cards are flat 2D cards so they overlap Tian Dan slightly in the last second.

## V2 fix (client: "camera shakes", 0:13-0:15) - 2026-11-22, render team 5
Base: s05 round 7 (render18/team1 ddea3b2a2), rendered with film18/main's set3d18 (f7be8e4). Cause of the shake: `shk=0.016` hand-held rotation noise on the keyed camera (2.3 + 4.1 Hz sinusoids), a 4-frame punch-in, and 2-3 Hz hops of the children. Fix: `shk=0.0`; the punch-in eased over 13 frames (+10 %); every bounce capped at 0.018 D and 1.5 Hz, sway <= 1.5 deg at <= 0.8 Hz; to keep frame-diff >= 4 the eased push/slide is larger (camera end (-70.3, 18.8), slide -1.9 D). `transparent_max_bounces = 64`; crf 20; meta transition unchanged (dissolve 11). One ground-dressing haystack with no ground under it (`dg_hay_0003`) is removed.
- ground_check (`GCHECK=1 python3 shot.py draft`, every 10th frame, 0.05 D): **exit 0 / PASS** - 171 rows, 0 FAIL (GROUND.md).
- qa_jitter.py take.mkv: **no "shake" line**, overall median jitter 0.24 px.
- Frame-diff in-shot (n=74): median **4.53**, p90 7.55. qa_auto PASS.
