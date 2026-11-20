# QA s09 (film 17, shots 22-23, narration 39.76-44.65 s) - round 2
Take g 1190..1348 (159 frames; g0 1196, g1 1342, 6 handle frames each side), 720x1280, 12 samples + OIDN. take.mkv is split: `cat take.mkv.part* > take.mkv`.
Set measure / DAY_INT, one process. Shot 22 g1190-1274 (measure_door): the two gendarmes walk dupont in (march cycles, hands on his arms all the way), the inspector follows a beat behind on the right with a closed-mouth smirk. Shot 23 g1275-1348 (measure_chair, camera raised to z 1.95): dupont in the chair with a shrug and two head-shake bursts (g1290-1321, g1328-1345, yaw 0.1 +-0.5 at 2 Hz, mouth locked flat), the inspector turns head and eyes to Bertillon with a grin, Bertillon calm at the right, fully in frame to g1348.

## Numbers
- rhythm.py --first_g 1190 --cuts 1275: in-shot median **5.89**, p90 **12.51** (>= 4 / >= 12).
- qa_auto: **PASS** (QA_AUTO.md, phone_sheet.jpg), magenta 0.0 %.

## Gate round 1 fixes (QA_TECH s09)
1. entrance animated: group walks from the door, positions change every frame, march cycles + bob. 2. inspector visible right of gendarme_b the whole time, expression `proud`. 3. shot 23 inspector yaw 0.7 + gaze toward Bertillon. 4. the floating white rods were the quill in the ink pot and the loose spreading calipers on the small table: their geometry is deleted at runtime. 5. camera raised so the foreground table no longer covers dupont's lap; both legs read (seated leg preset). 6. head shake yaw +-0.5. 7. mouths locked (silent + flat). 8. camera now pulls back and tracks the group: both gendarmes stay in frame. 9. dust 0.2, shafts hidden. 10. Bertillon framed fully (tail frames re-rendered, camera slide fixed). 11. satchel: no cast pose has a satchel in cast17 (dupont_held / dupont_innocent are the approved poses), so none in either shot.

## Self-check
Frames viewed on contact sheets at 12 + 5 sample frames across both shots, both cut neighbourhoods (g1196, g1275 +-3) and the tail g1331-1348; all PNGs decode (one truncated frame g1331 was found and re-rendered). Heads above y 880 everywhere (largest chin about y 640). Not every frame was inspected at 6 fps.
