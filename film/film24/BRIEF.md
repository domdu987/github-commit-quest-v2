# Film 24 "ไอ้เรือเต่า" (Korea's turtle ship, Admiral Yi Sun-sin, 1592)
First film of the series "one amazing war weapon per country".
PROJ = /tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/proj (symlink to the repo's film/).

Workflow: film/skill_film13 (films 1-13 skill), colour film/COLOUR_SPEC.md, client complaint list film/CLIENT_CHECKLIST.md.
QA_TEAM.md §G-§M and DETAIL_SPEC.md are VOID for this film.

## Story (narration PROJ/film24/audio/narration.wav, 65.0 s, Bankky original setting)
Script: PROJ/film24/script/script_th.txt; captions PROJ/film24/script/captions.json; timing PROJ/film24/audio/timing.json.
Facts vs inventions: PROJ/film24/FACTS.md.

| line | start s | what |
|---|---|---|
| hook | 0.00 | Admiral covers a ship roof with iron spikes and puts a smoke-breathing dragon head on the bow |
| pivot | 5.02 | 1592, Japan readies hundreds of ships; Yi builds a ship with a closed roof like a turtle shell |
| boss | 14.37 | Japanese commander laughs. Quote 16.1-21.4: "เรือมีกระดองเหรอ! เต่ามันคลานช้า! ถ้าเต่าตัวนั้นทำอะไรเรือข้าได้ ข้าจะคลานกลับบ้านเอง!" |
| nickname | 21.47 | Japanese soldiers call it ไอ้เรือเต่า |
| count | 24.45 | spike row 1 (~26.4), row 2 (~27.6), row 3 (~28.3), full (~29.0), gun ports open (~29.6) |
| false | 30.64 | Hansan: Korean ships turn and flee. Quote 34.8-37.0: "เห็นไหม เต่ากลัวแล้ว! ตามไปให้หมด!" |
| attack | 37.09 | 70+ Japanese ships chase into open sea, soldiers with swords ready to board |
| reveal | 41.91 | They win by boarding; the turtle roof is all spikes, nowhere to step. The "fleeing" Koreans turn and surround in a U, cannons from every side |
| aha | 53.57 | It was built not to be fast but so nobody can board. More than half the Japanese ships broken |
| ending | 58.90 | the commander clings to a plank, crawls ashore, goes home slowly like a turtle. Hard cut on the last word (~64.9) |

## Client hard rules (every shot)
- Nothing floats: props, flags, people, shadows sit on ground/deck/water. Ships sit IN the water with a waterline.
- No camera shake. Camera moves are slow and eased (Bezier), one move per shot.
- Nothing parented to the camera. Foreground props are fixed in the world.
- Anyone who moves steps with the legs (walk cycle); otherwise planted feet. No sliding. People on ships are parented to the ship root.
- No identical duplicate characters in one frame: vary face, colour, pose, size.
- Near figures bigger than far ones (true perspective).
- Every person has a contact shadow.
- Characters sharp. DOF allowed (client 2026-11-26) for the 3 macro inserts and mild background softness; out-of-focus foreground must be world-fixed. No face filling the frame for more than ~1 s.
- Hard cuts only. No dissolves / ghost double exposure.
- Comic and bloodless: no gore, no bodies, no injury; ships broken = smoke, splintered mast, listing. Fire shown only as smoke puffs/cannon flashes.
- Captions sit at y 900: keep whole heads above y 880.
- Mouths move only inside the two quote windows (16.1-21.4 and 34.8-37.0), commander only.

## Look (client 2026-11-26: R9 reference, film/ref_shorts/R9_sheet.jpg; recipe branch qtest/r9 film/qtest/NOTES.md)
Cycles GI, one soft warm sun key from camera-left, gradient sky fill, thin volumetric haze so distant ships/islands fade, bloom on hot spots only (post.py). Render 24 spp adaptive, OIDN, 75 % (540x960) then upscale to 720x1280. Flat unlit 2D puppet cards that cast shadows. Previously: blue-violet shade (hue 240-260), colour bands of COLOUR_SPEC (exteriors may fall outside; say why in QA.md). Rich, dense, period-correct sets, smooth layered water with foam and wakes (as film 10's sea).

## Overlays (client 2026-11-26, second reference R10: motion graphics as at R10 0:26 and 0:48-0:51)
- Shot 13, g about 1575-1607 ("ยิงปืนใหญ่ ใส่จากทุกด้าน"): small red ✗ marks pop on the Japanese ships as each is hit (positions from s13/overlay.json).
- Shot 14, g 1718-1767 ("วันนั้น เรือญี่ปุ่น แตกไปกว่าครึ่ง"): a top-third tally pops in, a red Japanese-ship icon reading "47 ✗" and a green Korean-ship icon reading "0 ✗", as R10's "10 : 1". This is fact: at least 47 Japanese ships were destroyed at Hansan and no Korean ship was lost. Also ✗ marks on the listing ships.
- Composited in conform (PIL), kept above y 860 and clear of heads. Hard pop with a 4-frame scale overshoot, no dissolves.
