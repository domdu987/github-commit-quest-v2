# QA FINAL-fix2 s16: PASS

Reviewer: QA-tech, FINAL-fix2, 2026-11-20. Take `take.mkv`: 720x1280, 30 fps, 120 frames, g1195-1314 (in-film g1205-1308). All 120 frames extracted.
Evidence is in `/tmp/claude-0/-home-user-github-commit-quest-v2/64d228e2-e8b3-5935-8909-70298ec15c3e/scratchpad/qafix2/`: `f/` (new frames), `p/` (passed round-4 frames), `girl_oldnew.png`, `stripA.png`, `stripB.png` (y 740-980 every 3 frames, g1205-1314, with lines at 860/880/950), `sheetA.png`, `sheetB.png`, `ladder.png`, `z1292.png`.

## Blocker B3 (girl's face in the caption band): FIXED
- I diffed every frame g1195-1314 against the failed FINAL-fix take (`qafin3/s16`). On every frame, the only change is a small box where the girl stood. It is about 20-50 px wide, moves from x ~690 (g1195) to x 0 (g1310), and sits at y ~806-905. Elsewhere the mean difference is about 1 grey level, which is render noise. On g1251, g1261 and g1292 there are also a few stray pixels and the soft contact shadow she left on the ground. That shadow is gone now too, so no orphan shadow is left behind.
- She is missing from all 120 frames, including both handles, so nothing pops in or out.
- In 2x crops at 12 frames (g1207-1309, `girl_oldnew.png`), the area behind her is clean: the basket, the rubble, the wall and the ladder are complete, with no hole, no see-through and no leftover buns or eyes.
- Compared with the passed round-4 take, the only differences are in the region of the original girl, and from g1300 on there are none. The holes, glow, camera, lighting and the six diggers are unchanged.

## Faces at y > 860: none on any frame
- Checked in the y 740-980 strips every 3 frames across the whole take. Every digger's face (eyes and mouth) is above y ~840.
- The elder's beard reaches the band from about g1300, as in the passed take and as already accepted (it is a beard, not a face).
- An automatic scan for pale, low-saturation blobs in y 860-950 on every frame found only the two glowing ground props: the lit plank by the ladder foot (g1233-1248) and the white-yellow ground quad (g1299-1314). It found no face.

## Frame-diff
- The team reports median 8.22 and p90 9.52 (n=103). That matches the previous takes (8.52/9.53 and 8.24/9.55) within render noise.
- With my own 90x160 metric, this take measures median 7.15 / p90 8.48 and the passed round-4 take measures 7.41 / 8.49, so the two are on a par.
- The largest single steps are g1212 (the lighting step at the dissolve) and g1252 (a hole opening). They are the same as before, not pulses.
- The team's QA_AUTO reports PASS.

## Other checks
- Pop-in/out: none.
- See-through: none.
- Floating: none. The small dark dirt chips near the right digger's feet at g1284-1296 are flying spoil and were already in the passed take.
- Half-cut main character: none. Only extras touch the frame edge.
- Pole through a face: none. The ladder at g1238-1253 is behind or beside the black-haired digger's head, and the pick handles stay clear of faces.

## Notes (non-blocking, unchanged from v1)
- The pale needle streaks on the ground and the flat white-yellow glow quad on the ground (about y 936-951, g1299-1314) are still there.
