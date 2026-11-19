# QA s21 (film 18, render team 4)
Range g 1596-1682, take.mkv frames 1590..1688 (99 frames), transition in: cut.
Render: 720x1280, 12 samples, OIDN, 2 threads, 31.8 s/frame wall (two renders at once).

## Frame diff (90x160 grey, in-shot frames only)
median 7.12, p90 13.5, min 2.12, max 22.38, frames < 1: 0 (rule: median >= 4, p90 >= 12)

## Max chin y per head (rule < 880)
{"soldier_stand_a": 714, "soldier_cheer_cup_b": 722, "soldier_stand_c": 714, "soldier_freeze_a": 757, "soldier_freeze_c": 763, "soldier_freeze_b": 785}

## Notes
- 60 front-3/4 gallop dragon oxen (8 phases x 3 flame drawings, flicker every 2 frames) marching 3.8 D/s toward the camera through the palisade gap; >= 3 tail flames visible through the shot (checked g 1635-1665).
- The 3 soldier silhouettes are carried 4.4-5.9 D ahead of the lens (head chin 714-785), freeze at the word (g 1646, 54.76 s); the right soldier's cup (3D) falls from his hand's anchor.
- Purple band cause found: Cycles transparent bounces (default 8) ended rays through stacked ox cards; set to 64. Moat/banks darkened, cityglow ball hidden, soft dark decal over the strip.
- Snap x1.5 (lens) on the word, extra punch-ins, sway 0.5 deg. Mouths do not move.
- Deviation: soldiers drawn facing the lens (no back views in cast18).

See QA_AUTO.md and phone_sheet.jpg.
