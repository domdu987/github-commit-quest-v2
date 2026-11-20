# QA_TECH s04 (take g295-391; in-shot g297-383) - FAIL
Checked: 6 fps frames + first/last 3; frame-diff re-measured (86 in-shot pairs): median 8.92, p90 19.78 (min 2.46, max 21.11). Caption band y880-950 mean 59-96; bright (luma>200) share max 1.10 %, mean 0.29 %.
## Issues
1. mandatory "Ju is lit": NOT MET. Ju is not visible anywhere in the frame (QA.md itself says so). No second lit town in view; the shot shows Jimo only. Fix: a camera or set change that shows a second warm town.
2. whole shot - rule 1 (zoom pulsing): "push punches every 13 frames" (QA.md); the frame-diff is a repeating burst of 13 frames (4.8 -> 13 -> 20 -> 14 -> 9 -> 18 -> 17 -> 8 -> 4.8). The 90x160 numbers pass only because of the pulses; steady motion between bursts is about 4. Fix: remove the punches, keep the orbit and push, at most one held punch on "จี๋โม่".
3. g~350-391 - mandatory caption-band bright share <= 1 %: max measured 1.10 % (over the limit by a hair; the bright tent faces and flag edge). Fix: dim the tent faces a bit more.
4. g297-330 - composition: the plan says "two towns stay warm-lit"; the foreground is a field of orange-lit tents and the lit Jimo is small on the horizon in the first half. Reads as a tent camp, not a siege view of Jimo (note).
5. delivered as a CUT in (meta transition_in cut) while the plan says "same take, snap" from s03 (note; the director must decide).
## Pass items
Flag opaque crimson cloth, no bloom, no halo card, no blown glow. No text. No characters. DUSK matches. g range 297-383 (+2 handle) matches the plan. Sky about 20 % at the end.
