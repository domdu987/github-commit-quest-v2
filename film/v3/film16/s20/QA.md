# s20 QA: film 16, shot 20 (LINE line_close, RAIN)
- Delivered: g 1259..1354 (96 f): shot g 1268..1345, 9-f handles each side (hard cuts). 720x1280, 7 spp, 2 threads, ~10.7 s/frame wall (20.8 cpu). take.mkv libx264rgb crf 6. QA_AUTO PASS.
- Content: bare poles + wire, rain pours, 12 cyan spark beads (set_leak 'pole', keyed every frame) crawl down the wet pole into the puddle; camera tilts down the pole (look z 7.2 -> 1.3 D) with push + slide; snap x1.9 g 1316..1331 on "ไฟรั่วลงดินหมด" (event g 1319).
- Set notes handled at runtime (c16.rain_look): rain streak opacity cut to ~22 % (QA_ART asks 50-60 % visual), puddle dark matte navy (RGB node + no spec), ladder hidden, beads x2.2 so they read on a phone.
- No cast, no mouths, no text, no DOF. Frame-diff (90x160 grey, in-shot): median 9.38, p90 12.10 (target >= 4 / >= 12).
- Checked at 6 fps + cut +-3 frames: no heads, no props; the wire from pole 0 runs top of frame (not a thick bar); caption band calm except rain. Notes: puddle is still a deep blue (dark) disc; the haze on the ground at the lower right is the set's wet gloss.
