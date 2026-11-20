# QA_TECH s13 - PASS (non-blocking notes)
Checked: qa_auto PASS (note: planned cut g986 has no visible change; expected, handle is continuous 3D), 6 fps + cut +-3 sheet g977-1022, meta g0 986 / g1 1015 (plan 32.85-33.86 -> 986/1015 OK), cut in OK, out-handle 9 for DIS 11 OK, framediff median 5.31 / p90 14.68 OK. Old look (white hair, spectacles, brown coat) OK, NIGHT bench OK, candle lower (0.30 -> 0.18) visible, rub + blink + sweat drop visible g1003-1022, no text/blur, head centre y 603-638, bottom <= 758, mouth fixed (wavy), no lip movement, snap/push g986-1002 visible.
Issues (non-blocking):
1. g993-1003: "leans back" is not distinct; he only moves toward lens with the push and the hand goes to the face. Fix: add a 2-3 deg head-back + torso lean before the rub.
2. g977-1022: torso is cut by the bench top (he stands behind it); no feet seen. Acceptable occlusion, note only.

## Round 2 - FAIL
Checked: qa_auto PASS, meta g0 986/g1 1015 OK, handles OK, framediff 5.21 / 14.74 OK, old look OK, NIGHT bench OK, mouth fixed, snap OK.
1. g1000-1015 (new): head is half hidden behind the foreground plank at right and cut by the right frame edge (x ~ 720) during the rub / sweat-drop payoff. Fix: slide the camera left or move the mark left ~0.3 m so the face clears the plank and the edge.
2. Earlier 1 (lean back not distinct) NOT fixed, g993-1003; now also lost to the occlusion. Fix: head-back lean before the rub.
3. Earlier 2 (torso cut by bench): note only.

## Round 3: PASS
Checked 6 fps + cut g986 +-3 (take g977-1024), qa_auto PASS (g986 "no visible change" = handle). No text, no black/magenta, no frozen, no blur. Mouth fixed (wavy). Head centre y ~ 600-660, bottom < 760. Frame-diff (take.mkv, g987-1015): median 4.80, p90 12.68: OK. Old look (white hair, spectacles, brown coat) and NIGHT bench OK; rub + blink + sweat drop visible g1003-1022.
Earlier issues: R2-1 head hidden by plank / cut by right edge: FIXED (head x ~ 370-460 of 720, clear of plank and edge through g1024). R2-2 lean-back: still subtle, NOTE (he straightens g992-997, then rubs). R2-3 torso cut by bench: note.
Notes: very dark frame; faces still read at phone size; candle at the right edge in the handle (g1022+).
