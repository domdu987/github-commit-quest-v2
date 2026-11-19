# s24 QA: film 16, shot 24 (the REVEAL macro) -- LINE bottle_macro, AFTER_RAIN

## Delivered
- take.mkv: 93 frames, g 1531..1623 (shot = g 1540..1614; 9 handle frames each side), libx264rgb crf 6, 20.9 MB. Hard cut in at 1540, hard cut out at 1615.
- cues.json, contact.jpg, framediff.json, QA_AUTO.md (PASS), phone_sheet.jpg. No cast, no text, no DOF.

## Beats
| g | beat |
|---|---|
| 1540-1557 | ONE pulse (TG.set_pulse, keyed every frame, cyan tapered comet with a white-hot head) runs along the wire from the left; the camera WHIP-PANS with it (look point on the head, 7 f lag) while the sky sweeps past ("ไฟเลยวิ่ง" 1543) |
| 1558 | head slides over the neck and PARKS inside the glass (pulse_s_at_pole(1)); cyan glow in the glass ("อยู่แต่ในลวด" 1561) |
| 1579-1592 | SNAP push x2.0 with pan (13 f) onto the glowing glass on "ไม่รั่วลงเสา" (1582) |
| 1592-1614 | settle, drift push + slide on the glass ("สักหยด" 1604) |

## Checked
- Pulse is one continuous comet on the wire (not beads), parks inside the glass, cyan glow only in the glass (the pulse light is linked to the glass).
- The pole below the glass carries no cyan; it is sunlit wood (the set's lighting), not black. After the snap the glass fills the frame and the pole is mostly out of it: the "does not leak" read is carried by the cyan staying inside the glass and the wire.
- No magenta; no sprite; no caption-band content issues (glass and sky only).
- First frames g 1531-1537 (handle) show pole 2 / the fence from the whip start; they are the unused handle.

## Frame-diff (in-shot g 1541..1614)
median 4.02  p90 14.28  (target >= 4 / >= 12). The macro frame is mostly smooth sky: the whip (a PAN, not a truck, so the clouds sweep) and the snap carry the p90; the drift (slide 115 px/s, arc 22 deg/s) the median.

## Differs from the plan
- Plan: "whip follow along the wire, then settle on the bottle": done as above; the end framing is tight on the glass (glass about 60 % of the width).
- Foreground blades (set FG) were tried and dropped: the macro camera is 8 D above the ground, nothing at 1-2 D.
- 7.29 s/frame wall, 13.99 s CPU (720x1280, 7 spp, 2 procs x 2 threads).
