# H2b (BIGZOOM 2), g 1392-1519 (render g 1389-1522), team 10
Delivered: take.mkv (split in parts, `cat take.mkv.part* > take.mkv`), meta.json, cues.json, contact.jpg, phone_sheet.jpg, QA_AUTO.md, path_draft.mp4.
Camera: P_TOP (new, -10,-115,115 -> 0,70,0) held about 1 s (slight drift), then one Catmull-Rom swoop over the camp to a medium shot of Cressingham + Surrey (reached g1495, 3.4 s after the start), then the CU3 push into Cressingham's face g1495-1519 (cut at g1519). 32 samples + OIDN.
Acting: worried -> shocked behind a blink (Cressingham g1486-88, Surrey g1488-90), sweat drops; 5 English on tiptoe (bobbing ~2 Hz); Cressingham does not speak. Rim light gold on every card, contact shadows on, feet on terrain. Cork image: crimson English, 5-rank blue spear wall, 6 saltire banners.
## Numbers (qa_stats2 on take.mkv)
sat 0.711, vivid 81 % (first render on the pre-palette-fix set; a palette re-render was started and stopped on the director's policy), luma 132 (raw set grade, no post pass; the director normalises brightness at the conform). rhythm: in-shot median 17.0, p90 27.8.
## Open notes
- qa_auto flags 25 frames as "suspected blur" (g1389-1400 top view, g1462-1470 swoop): the metric compares against the take median and this take goes from a far aerial to a close-up; no blur or DOF is used anywhere. Judge on the phone sheet.
- The bridge deck still runs past the spear wall into the loop (merged bridge mesh, not editable from the shot script).
- Mid-swoop frames (g1430-1470) are lemon-yellow (VIVID easing P_TOP -> camp_bank).
- During the CU3 push Surrey is cut by the right frame edge (unavoidable with a 2-shot pushing in on one face); heads are above y 880 throughout.
- Join: P_TOP start matches K.POSES['P_TOP']; the 3 handle frames before g1392 are a continuation of the drift (cam_path extrapolated). Team 3's H2a drift should be compared by the director.
