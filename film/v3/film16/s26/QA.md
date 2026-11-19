# s26 QA: film 16, shot 26 (CHAMBER chamber_table, DAY)
## Delivered
- `take.mkv` (libx264rgb crf 6, 30 fps): first_g 1698, 78 frames (g 1698..1775). Shot 26 = g 1707..1766 (56.90-58.89 s); 9 handle frames each side, rendered in 3D. Transition in: hard cut.
- 720x1280, 6 spp (TG.FINAL_SAMPLES chamber), 2 threads x 2 processes. **9.32 s/frame wall, 18.12 s CPU.**
- QA_AUTO.md PASS (no black/blank/magenta/frozen frames; its note "planned cut has no visible change" is expected: the cut is made in the conform, the handles are the same shot).
## Shot
| g | beat |
|---|---|
| 1707-1730 | camera above the front table drifting in (push 7 %/s + slide + arc); the tape runs from the register over the table edge to the floor; Morse (right) reads, Congressmen A, B, C crowd round amazed, the mocker (sour, arms folded) behind the instrument |
| 1733 | click 1 "ติ๊ด" (57.66 s): lever down 3 f, tape jumps out, **SNAP push x2.1 / 13 f** toward the register |
| 1742 | click 2 "ติ๊ด" (57.97 s): tape jumps again; the camera travels to the mocker |
| 1745 | mocker swaps sour -> **JAW DROP** (ring eyes, sweat) on the closed frame of a blink |
| 1746-1766 | push on the face (mocker head 238 px), Morse grinning at the right edge, tape paper in his hand |
## Checks
- Mouths: nobody speaks. The jaw drop is a held expression mouth, not lip-sync.
- Heads: mocker 87 -> 240 px, centre y 460-690, bottom <= 811 (< 880). Morse's head is only visible at the right edge in the last frames (centre y < 500).
- No text: the tape is dots and dashes only. No DOF. Contact decals on, actors stand on the floor behind the front table.
- Camera never parked (camreport: min 2.1 px/frame); characters have a squash tremble / lean / head roll / blink (nobody frozen).
## Frame-diff (90x160 grey, in-shot pairs g 1707..1766)
median **4.38**, p90 **27.14** (target >= 4 / >= 12). The p90 comes from the snap (g 1733-1745).
## Differs from the plan / notes
- The front-table instrument is 3x scale and occludes the people behind it from the preset camera, so the camera is above it (z 4.3) and the cast stands behind the table; the foreground lever knob and the register drum pass close to the lens during the snap.
- The mocker's jaw drops on the second click (g 1745), not the first, so the two clicks read as build then pay-off.
- The tape's far end (floor loops round the stool) stays out of frame.
- No eye glint (night close only).

---
# Revision 2 (after the director's TAKE gate) -- re-rendered, take.mkv replaced
Frame-diff now median 4.27 / p90 26.37; 78 frames, 9.39 s/frame; heads 76-233 px, lowest head bottom y 811.
- **Gate 1 (tape does not spool): fixed.** `set_tape` length now starts at 0.04 (nothing on the table), jumps to 0.30 on click 1 (g 1733), 0.60 on click 2 (g 1742) and eases to 0.94 by g 1772. The tape visibly grows out of the register on each click.
- **Gate 2 (crowd): fixed.** Congressmen A, B, C are staged round the mocker (A at 2.4/12.3, B at -2.6/11.3, C at -0.5/12.8, mirrored toward the register): four faces in the opening frame, and in the closing frame the mocker, congressman A, congressman C and Morse are in shot (A and C are 170-180 px).
- **Gate 3 (Morse's eye-line): partly.** His gaze is set toward the tape (-0.6, 0.9); the pose still grins and the sheet in his hand stays a loose paper.
- Morse stays out of the caption band (his head bottom was 893 in the first re-render, now 796).

---
# Revision 3 (after the director's FINAL gate)
Re-rendered, take.mkv replaced (31.5 MB). Frame-diff median 4.28 / p90 22.46; heads 76-233 px, lowest head bottom y 811. QA_AUTO PASS.
- **Foreground spool:** the register's cream paper drum (the "log") and the big brass roller beside it are cut out of the table mesh at run time (bmesh, inside the instrument box); the tape still comes out of the slot. In the snap frames (g 1736-1750) the foreground is now the baize, the instrument's stepped base and the tape.
- A small yellow disc remains at the far left edge at g 1740 (another part of the instrument's coil); it is out of the way.
