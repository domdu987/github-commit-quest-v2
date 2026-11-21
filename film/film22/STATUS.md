# Film 22 status (director) — "ไอ้ช่างวงจร" (Harry Beck's Tube diagram, 1931-33)
Client rules: HANDOFF §3, §7b-7d; QA_TEAM §G-§J. QA-art approves the look (no client wait). Music fal elevenlabs/music/v2.5, QA picks, -31 dB. Queue row WAIT.
Fallback check: send_later 60 min, always re-armed.
- [x] Facts web-checked -> FACTS.md (print run and pay figures conflict between sources: not spoken)
- [x] Script; blind test 1 = 7/10 (3 rewrites applied), retest = 8/10 PASS -> script/script_th.txt
- [x] Hook ≤ 3.5 s: 3.51 s (variant tests in audio/hooktest)
- [x] Narration Bankky original (speed 1.15, atempo 1.134), 12 sentences, STT 0.946-1.0 (s05 0.946 only because STT wrote "Beck" in Latin), 62.66 s -> audio/narration.wav, script/captions.json (76 phrases)
- [x] Music 3 takes (fal elevenlabs/music/v2.5, 68 s) -> audio QA pick m2 (runner-up m3), audio/music/PICK.md; vocals STT open (fal locked) -> local check
- !! 2026-11-20 21:55 UTC fal.ai returns "User is locked. Reason: Exhausted balance." Client told. Narration and music were done before; SFX + fal STT need a top-up (fallback: older films' SFX libraries, local whisper)
- [x] Style board r1 (v3/set3d22/board) -> QA-art FIX-FIRST (board/QA_ART.md: period skyline, sky magenta, tunnel not dark blue, still 2 framing)
- [x] Board r2 -> QA-art SHIP (board/QA_ART.md Round 2; 8 carry-forward look rules)
- [x] cast22 built (10 members + 16 crowd, 51 poses, test ALL OK)
- [x] Full set: builder A (london + hq, 2 revisions), builder B (under + mapworld, 1 revision) -> contact_sheet.jpg / contact_sheet_B.jpg
- [x] SET gate: QA-art PASS (SET_GATE.md, 27 team items); QA-tech FAIL r1 -> builders' SET-fix round -> QA-tech PASS r2 (QA_TECH.md); no overrides
- [x] WORKER22.md drafted (5 teams)
- [ ] Set + cast -> SET gate (QA-art + QA-tech)
- [x] shot_plan.md, WORKER22.md, TEAMS.md; render teams launched 23:59 UTC (see TEAMS.md)
- [ ] TAKE gates, conform22, FINAL gate (4 reviewers + film 2 side-by-side + ref sheets), release22, queue WAIT
- 2026-11-21 00:44 UTC check: all 5 teams running (team4 s03 81/144; team1 s01 rerender + s05; team2 s02/s15 camera previews; team3, team5 scripts pushed, renders in progress). conform22.py + SFX library ready.
- 2026-11-21 01:20 UTC: producer relayed client rule QA_TEAM §K (nothing floats). Verified on claude/new-session-73ou27 a663493, merged; fallback ground_check22.py; WORKER22 §7; all teams messaged. Float hunter added to TAKE + FINAL gates.
- 2026-11-21 01:25 UTC: producer relayed §L (no camera shake, qa_jitter ≤ 2 px/s); verified 17bbec1, merged, WORKER22 §8, teams told. Usage limit: no new teams; reuse finished teams for re-renders; archive on acceptance.
- 2026-11-21 01:30 UTC: STOPPED. Producer relayed the client's full stop ("หยุดทุกอย่างเลย"). Director halted: no spawn, no messages, no renders, 60-min self-check cancelled. Render teams 1-5 were NOT messaged (producer said not to); their sessions may still be running. Resume only when the producer/client says continue.
- 2026-11-21 04:32 UTC: producer relayed client: finish with the film-13 skill (claude/new-session-73ou27 0c95e6c film/skill_film13/, QA_TEAM_film13.md; not v3 skill, not QA §G-§L; keep: fal music, QA-art look, text signs, WAIT row, ≤3 teams, qa_auto + ground check + qa_jitter). Verified. Resume of teams 2+4 blocked by the permission check (unsanctioned communication); team1 resumed. Waiting for the user's own go.
- 2026-11-21 07:50 UTC: producer relayed 'finish all films, fal works'. Team1 done: s01 s04 s05 PASSED (film22/qa/sNN/PASSED). Remaining: s02 s15 (team2), s03 s09 s10 (team4), s07 + s06 re-render (team3), s11 s13 + s12 fix (team5). Teams 2-5 idle; resuming them needs send_message, which the permission check blocks without the user's own OK. GitHub warns the repo is approaching its size quota.
- 10:23 UTC: USER approved resume ("ทำต่อได้"). Resumed team2 (s02 s15), team4 (s03 s09 s10), team3 (s06 re-render, s07); team1 archived (done). Team5 waits (≤3 running). Workflow: film-13 skill; checks = free scripts. 60-min check re-armed.
