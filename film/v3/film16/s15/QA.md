# s15 QA: film 16, shot 15 (LINE line_trench_end, DUSK) -- the silent test key (re-shot after the director's TAKE gate)
- take.mkv: g 949..1015 (67 f; shot = g 958..1006, handles 9 each side), 720x1280, 7 spp, libx264rgb crf 6. Dissolve in 13 f, hard cut out (g 1007).
- Staging: the whole crew is BEHIND the crate (Cornell, both workers lean in toward the register, 120-150 px heads); Morse stands behind the key knob and his right hand is PINNED to it (hand error 0). The set's static lever + knob were replaced at runtime by an animated copy that pivots 16 deg down: press g 975-981 ("ส่งข่าว") and again g 982-987; the register (paper roll, copper coils, tape strip) is in frame next to the key and does not move. Morse: determined before, worried from g 982.
- "เงียบกริบ" (g 988): brightness dip to x0.58 over g 986-998 (exposure keyed) and an eased x2.2 push-in snap (13 f, peak 1.8) that lands on Morse's worried face at the key; the final 0.7 s is a close on Morse + key + lever.
- Camera: custom 22 mm, 6 D from the crate, push 12 %/s + slide 45 px/s + arc 15 deg/s, one snap. Frame-diff (in-shot): median 4.30, p90 13.77 (targets 4 / 12 met). qa_auto PASS. s/frame 11.2 wall.
- Known: the eye-lines still look mostly toward the camera (cast16 gaze keys had little effect); Morse's face is large in the last frames (head ~300 px, bottom stays above y 880); no lantern was added.
- Update: Morse now faces left toward the key (mirror, pitch 0.6, gaze 1.0/0.9), the crew's gaze is shifted toward the register (1.0/0.7); frame-diff now median 4.36 / p90 14.18.

## Round 2 (director QA-art r2) -- final state
- Press readable: Morse now stands beside the key (crate end), faces it, and his right hand (layer front) is pinned just above the knob; the set's lever is replaced by an animated copy pressing 16 deg at g 975-981, 982-987 and again g 996-1002 inside the end close, where knob, hand and lever are all in frame. (The first press had been missing in the earlier deliveries: cap_g("ส่งข่าว") matched the hook's caption at g 422; G_TRY is now g_of(32.41) = 975.)
- Crew: arms down, bent toward the register (lean +11, yaw 0.95, pitch 0.35, gaze toward it); no folded arms.
- Register + lantern: brass collars on the coils, brass top on the register box and flange on the paper drum, a still white tape strip hanging over the box edge; a brass lantern with a glowing glass and a warm point light (600 W, 0.25 D) at the crate's near end gives the warm pool.
- Frame-diff in-shot: median 4.63, p90 16.26. qa_auto PASS. s/frame 10.7 wall.
