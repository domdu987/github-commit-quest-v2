# QA s23 (render team 5, film 18) — frames g1742-1806 (+6 handles each side: take.mkv g1736-1812, 77 frames), jimo_out NIGHT
Render: Cycles 12 samples 720x1280, 2 threads, ~20-35 s/frame with four renders sharing the 4 cores.

## Frame-diff (90x160 grey, in-shot g1742-1806, n=64)
median **5.18**, p90 **12.96** (min 1.32, max 25.26). Target >= 4 / >= 12: met.
Camera: from the planned high pose to a lower, closer one over the wall walk (cam (-26,3.2,19.2) -> look (-9,0.2,17)), pull-out -0.12/s, slide +70 px/s, eight quick +-7 deg swings and two 1.09 / 0.93 snaps; fg torch right (set prop).

## qa_auto
PASS.

## Brief items
- Townsfolk beating pots, with shout drawings (`old_man_beat`, `woman_beat`, `child_beat`, expr "shouting", mouth open) and NO lip-sync: the mouth drawing is fixed, only the mallet angle (-58/-18 deg, 6-frame period), pot_ring (0.25/1.0) and a 0.06 D bounce animate. 6 townsfolk + 2 kids.
- Sound rings visible round the pots at every strike; nothing blown out, caption band clean (the walk planks and parapet only).
- Heads above y 880: yes (the group is at y 330-700 px of 1280). Eye-lines toward the Yan camp side.

## Deviations
- Camera pose is closer/lower than planned: the planned high pose put the 8 beaters at about 100 px, which did not read; the dark parapet merlon of the near wall frames the bottom left. The pull-out at the end makes the group small again (about 160 px) but still readable.
- The set's walk is lit by one fire; no extra light added.

## V2 fix (client: "camera shakes") - 2026-11-22, render team 5
Base: s23 take 688a39e. Changes: the camera is ONE eased pull-back (push -0.12) + one truck (slide 72 px/s) - the eight +-7 deg pan snaps and the two distance snaps are removed; pot-beat cycle slowed from 5 Hz (3 frames) to 2.5 Hz (6 frames per half cycle) and the per-person hop reduced from 0.06 D to 0.015 D at 1.5 Hz; `transparent_max_bounces = 64`; crf 20; meta transition_in unchanged (dissolve 9).
- ground_check (`python3 shot.py gcheck 1742 1806`, every 10th frame, 0.05 D): **exit 0 / PASS** - 16 objects, 112 rows, 0 FAIL (GROUND.md).
- qa_jitter.py take.mkv: **no "shake" line**, overall median jitter 0.21 px.
- Frame-diff in-shot (n=64): median **4.10**, p90 5.61 (median >= 4 met with the eased dolly + parallax). qa_auto PASS.
