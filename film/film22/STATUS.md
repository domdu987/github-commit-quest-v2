# Film 22 status (director) — "ไอ้ช่างวงจร" (Harry Beck's Tube diagram, 1931-33)
Client rules: HANDOFF §3, §7b-7d; QA_TEAM §G-§J. QA-art approves the look (no client wait). Music fal elevenlabs/music/v2.5, QA picks, -31 dB. Queue row WAIT.
Fallback check: send_later 60 min, always re-armed.
- [x] Facts web-checked -> FACTS.md (print run and pay figures conflict between sources: not spoken)
- [x] Script; blind test 1 = 7/10 (3 rewrites applied), retest = 8/10 PASS -> script/script_th.txt
- [x] Hook ≤ 3.5 s: 3.51 s (variant tests in audio/hooktest)
- [x] Narration Bankky original (speed 1.15, atempo 1.134), 12 sentences, STT 0.946-1.0 (s05 0.946 only because STT wrote "Beck" in Latin), 62.66 s -> audio/narration.wav, script/captions.json (76 phrases)
- [x] Music 3 takes (fal elevenlabs/music/v2.5, 68 s) -> audio QA pick m2 (runner-up m3), audio/music/PICK.md; vocals STT open (fal locked) -> local check
- !! 2026-11-20 21:55 UTC fal.ai returns "User is locked. Reason: Exhausted balance." Client told. Narration and music were done before; SFX + fal STT need a top-up (fallback: older films' SFX libraries, local whisper)
- [ ] Style board (3 stills, Sonnet builder running) -> QA-art   (WORLD.md = the connected world)
- [ ] Set + cast -> SET gate (QA-art + QA-tech)
- [ ] shot_plan.md (≤12 hard cuts, 2 BIGZOOM), WORKER22.md, render teams (Sonnet, render22/teamK)
- [ ] TAKE gates, conform22, FINAL gate (4 reviewers + film 2 side-by-side + ref sheets), release22, queue WAIT
