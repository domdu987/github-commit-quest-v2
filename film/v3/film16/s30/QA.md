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

---
# Revision 3 (after QA-art round 2) -- re-rendered, take.mkv replaced (42.8 MB, one file)
Frame-diff median 5.02 / p90 12.39; 129 frames, 8.6 s/frame; heads 82-398 px, centre y 597-721, lowest head bottom y 849 (< 880). QA_AUTO PASS. Hard cut on "เอง" (g 2096) kept.
1. **Register at his elbow: done.** A small walnut table with a copy of the set's instrument (scale 1.1, built with `tg_arm_parts`) stands at his right elbow on his depth; ONE continuous paper ribbon (the set's own dot-dash tape material) runs from its slot over the table edge into a heap of 12 curled ribbons (dots and dashes visible) and 5 loose strips at his boots. The tan wooden slats are gone.
2. **Gold sack removed: done.** It was not the money bag (hidden already): it was a brass urn of the set's room mesh (`room_brass`) standing at the stool; its vertices near the stool are cut out at run time (found by hiding objects one at a time and comparing the crop).
3. **Night contrast: done.** Walls and ceiling material 40 % darker (colour ramp x 0.6), window fill and ambient kept low, windows deep blue. The candle light moves to chest height between his hand and the register (energy x 2.6 over round 2).
4. **Morse: partly.** He stays on his mark in the doorway, drawn 15 % bigger (head 82-104 px at full size, was 71-85) and the camera look is shifted 0.15 D left so he sits further from the left frame edge. He is not moved deeper into the opening: shifting him 0.9 D put him behind the wall wing and out of sight.
Frame-diff and heads were measured on the final frames. I did not re-scrub the whole take at 6 fps; I looked at stills (g 1990, 2030, 2060, 2095) and the contact sheet.

---
# Revision 4 (after TAKE gate round 3) -- re-rendered, take.mkv replaced (42.6 MB, one file)
Frame-diff median 5.07 / p90 12.76; 129 frames, 8.6 s/frame; heads 78-398 px, lowest head bottom y 849. QA_AUTO PASS. Hard cut on "เอง" (g 2096) kept.
- **Morse (blocking item): fixed.** He stands 0.35 D screen-left of his old mark (the four directions were compared on stills at g 2095; this one clears the jamb best), so his whole face shows beside the door frame: head 78-90 px at full size (g 2065-2095), doorway at x 90-180. The camera look in the snap-out moves 0.5 D left (was 0.2 right) so the doorway sits in the left third. Grin pop: a blink at g 2084, expression "laughing" from g 2085.
- **Optional notes:** ceiling and walls a further 25 % darker (colour ramp x 0.45 of the original); the register's candle light x 1.4 brighter (total x 3.6 of the set's). The red rectangle on his vest (the mail bag of the sash costume, drawn in the sprite) is NOT removed: it belongs to cast16's costume and would need a pose key that does not exist.
- The snap-out is now x 1.67 (k 0.6) to keep the p90 above 12 after the pan change.
- Checked on the frames: g 2040, 2065, 2085, 2095 (contact strip); I did not re-scrub the whole take at 6 fps.
