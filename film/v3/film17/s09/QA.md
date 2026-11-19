# QA s09 (film 17, shots 22-23, narration 39.76-44.65 s)
Take g 1190..1348 (159 frames; g0 1196, g1 1342, 6 handle frames each side), 720x1280, 12 samples + OIDN. take.mkv is split (cat take.mkv.part* > take.mkv).
Set: measure / DAY_INT, one process. Shot 22 g1190-1274 (measure_door camera): two gendarmes escort dupont (dupont_held) in, the inspector (smirk, arms crossed) follows on the right. Shot 23 g1275-1348 (measure_chair camera): dupont seated in the chair (innocent shrug, head shakes from g1290, mouth closed), inspector grins, Bertillon calm behind.

## Numbers
- rhythm.py take.mkv --first_g 1190 --cuts 1275: in-shot median **6.07**, p90 **15.03** (target >= 4 / >= 12).
- qa_auto.py: **PASS** (QA_AUTO.md, phone_sheet.jpg), magenta 0.0 %.
- Camera: shot 22 push + slide + snaps at g1215 / g1236 / g1258; shot 23 push + snaps at g1290 / g1311 / g1331; 0.05 m handheld sway.

## Self-check (frames at 6 fps + both cuts +-3)
- Heads/chins above y 880: yes; the largest head (dupont, g1348) chin is at about y 640.
- Director's lessons applied: light shafts (beam_fx) hidden, dust 0.5 (no stray white discs), no props needed in this take.
- Headrest bar of the chair drew over dupont's face: fixed by moving his card 0.2 m toward the camera (re-rendered).
- Inspector was hidden behind the gendarmes in shot 22: moved to the right of gendarme_b, visible from g1215.
- Mouths: all closed, static (no quote window inside this take); blinks and sway only.
- Known: a few thin stray rods near the calipers table in shot 23 are the set's own calipers props; the first frames of shot 22 show the group small (about 280 px tall).
