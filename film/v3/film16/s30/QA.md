# s30 QA: film 16, shot 30 (CHAMBER chamber_table / NIGHT, candles): the ENDING
## Delivered
- `take.mkv` split in two parts (`take.mkv.partaa` + `partab`, `cat` them to rebuild; libx264rgb crf 6, 30 fps, 45.7 MB): first_g 1971, 129 frames (g 1971..2099). Shot 30 = g 1980..2095 (66.01-69.85 s). Transition in: **dissolve 17 f** from shot 29 (the longest of the film), centred on g 1980, 9 handle frames before it. Out: hard cut on "เอง" at g 2096; 4 handle frames g 2096..2099.
- 720x1280, 6 spp, 2 threads x 2 processes: **8.68 s/frame wall, 16.89 s CPU**. QA_AUTO.md PASS (its cut note is the handle).
## Shot
| g | beat |
|---|---|
| 1980-2023 | the mocker (bald, sash, key ring) alone on the stool beside the register, candle in his hand, YAWNING (held wide mouth) with the sleep Z drifting up; the tape piled round the stool and his boots; Morse grins out of the lit side doorway (far left); the camera sways about him with a 14 deg heading swing and slowly pulls back |
| 2024-2037 | **SNAP** push x1.4 / 14 f on "นั่งเฝ้าลวด" (67.44 s = g 2026) |
| 1992-2004, 2030-2044, 2062-2078 | head-nod windows (mocker_stool_candle_nod), blink on each swap |
| 2056-2070 | **SNAP-OUT** x2.5 / 15 f (pull-back reveal) on "ของไอ้บ้าลวด": the wide empty night chamber, candle pools, the register on the table clicking, the tape spilling over the carpet |
| 2070-2095 | wide: he is small on his stool at the right third, Morse peeking at the left |
| 2096 | hard cut (end) |
## Checks
- Mouths: nobody speaks; the yawn is a held expression mouth. Morse's grin is an expression, not lip-sync.
- Heads: mocker 90 -> 341 px, Morse 49-113 px; head centre y 636-680; lowest head bottom y 819 (< 880). No text, no DOF.
- The set's own leather stool is hidden behind the puppet's drawn stool (the mocker is placed 0.5 D toward the lens).
- Register clicks: the lever is keyed down 3 f every 9 f (set_click); the register is out of frame until the pull-back, so the clicks show in the wide end only.
- Callback: the NIGHT chamber_table axis of shot 26 is the final wide direction (approximately; the camera orbits about the mocker).
## Frame-diff (90x160 grey, pairs g 1980..2095)
median **4.66**, p90 **14.04** (targets >= 4 / >= 12). The median comes from the heading swing (parallax in the night room) and the p90 from the two snaps.
## Differs from the plan / notes
- Two snaps (push and snap-out), the bible asks for one: the push alone gave p90 8-10, the snap-out is the "pull back to the wide empty chamber" of the plan, delivered as a fast reveal rather than a steady 8 %/s pull (the drift itself is 8 %/s).
- Morse in the doorway is small (49-113 px) and partly behind the door-wing at the start; there is no eye glint.
- The 3D register does not click visibly before the pull-back.

---
# Revision 2 (after the director's TAKE gate and QA-art) -- re-rendered, take.mkv replaced (42.3 MB, one file)
Frame-diff now median 4.56 / p90 13.02; 129 frames, 8.5 s/frame; heads 71-398 px, centre y 635-721, lowest head bottom y 849 (< 880). QA_AUTO PASS.
- **Gate 1 (no hat): fixed.** `hat_off` = 0: the black stovepipe is on his head for the whole take (continuity with 26-29).
- **Gate 2 (candle): fixed.** The two translucent glow discs of cast16's candle (the un-composited sprite at his cuff) are removed at run time (`cast16._candle_body` is wrapped in shot.py, cast16 untouched): the candle is a solid brass chamberstick with its flame, visible in his hand and in the wide.
- **Note 3 (callback axis): restored.** The camera is on the set's night axis again (register on the table to the right, lit doorway left), as the chamber_table_night preset.
- **QA-art fixes:**
  - End framing: the pull-back stops at a medium (mocker head 190-230 px at the end of the shot, was 80), the register and the table with the coils are in frame at his right, Morse in the doorway is 71-85 px. The two snaps are a push on "นั่งเฝ้าลวด" (x1.5) and a pull-back accent (x1.47) at g 2058-2070.
  - Night light: the window fill is at 35 %, the world ambient at 35 %, exposure -0.4 EV, candle / lamp pools kept: the room is dark between the pools.
  - Tape: the set's even floor loops (they read as rails) are hidden (tape clip 0.27: only the table part shows); a heap of 46 crumpled paper strips and a ribbon of paper lie round his boots, higher at the centre.
  - Sleep Z: it floats above his head for the whole yawn (kept from the first version).
- Still open: the heap is plain paper (no dots / dashes); the vest shows a small red rectangle (the mail bag seen from the front); Morse's grin is small.
