# QA-art round 16 s01: PASS
Shot: BIGZOOM A, the hook (g 0-155, v4 patch g 26-116). I extracted all 162 frames (g = n). I judged a 144x256 phone sheet every 5th frame (about 6 fps), a frame-by-frame strip at g 70-93 (240x427), half-size full frames at g 76/80/84/88, and full-res crops of the left edge (x 0-360, y 350-850) at g 72/76/80/84/88/90. Working files: /tmp/claude-0/-home-user-github-commit-quest-v2/64d228e2-e8b3-5935-8909-70298ec15c3e/scratchpad/qa16/ (s01_phone.jpg, s01_70_93.jpg, s01_left.jpg, s01_full4.jpg).

## Round-16 checks
1. **The plaque post no longer crosses a face at g 72-80: DONE.** The dark post is at the extreme left edge at g 70 and leaves the frame by g 71. In g 72-93 no pole or post overlaps any face. The only faces near the left side are Tian Dan's (x about 380) and the background herd's, and all of them are clean.
2. **No rider or ox half-cut at the left edge at g 76-90: MOSTLY DONE (note).**
   - No rider is anywhere in g 60-156. The small basket rider is gone.
   - One dragon-coated herd ox still exits through the left edge during the truck:
     - g 72-76: about 60 % of its body is visible (x 0-110, y 470-640), with the head already out of frame.
     - g 80: only the rump is visible.
     - g 84: a leg-and-tail sliver.
     - g 87: gone.
   - It is a background herd ox wiped out by the eased camera move in about 0.4 s, not a character held half-cut. On the phone it reads as the herd continuing past the frame. Accepted as an exit, but the QA.md claim "nothing is cut at the left edge" is not quite true. If there is a re-render anyway, move this one ox about 1.5 D further from the left edge or remove it.
3. **Nothing regressed.**
   - The move is still one continuous eased crane-down and push from the extreme wide (g 0, Tian Dan about 2-3 %) to the medium (g 108 onward, about 36-42 %).
   - The 即墨 plaque reads at g 36-60.
   - There are no ghost duplicates, and no faces at the bottom edge.
   - The fire-against-moon-blue palette and the rich set hold. The hook ("he dresses oxen in dragon silk and arms their horns") reads by about 2-2.5 s.

## Notes (carried, not blocking)
- The brazier leg left of Tian Dan (g 100-155) is still a bright white bar. Lower its emission.
- The cool rim on Tian Dan himself is faint (the team admits this).
- A pale straw sliver slides across the lower-left ground at g 70-78. It is harmless and reads as straw.

| Beat on phone | Light/colour | Composition | Acting | Camera |
|---|---|---|---|---|
| 8 | 8 | 8 | 7 | 9 |

## Verdict: PASS with notes
