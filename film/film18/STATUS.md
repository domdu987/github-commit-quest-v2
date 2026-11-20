# Film 18 status (director)
**Client decision 2026-11-19 (typed in this chat):** "เรื่อง 18 ไม่ต้องรอผม OK ให้ QA-art อนุมัติแทนแล้วเรนเดอร์ได้เลย และเพลงไม่ต้องรอผม ให้ทำเองด้วย fal.ai (elevenlabs/music/v2.5 แบบ instrumental) ให้ทีมตรวจเลือก"
-> QA-art (Opus) is the look/SET approval; render without waiting; music = fal-ai/elevenlabs/music/v2.5 force_instrumental, QA picks. Client gets board/sheets FYI only.
- [x] Facts checked (Shiji ch.82 via Wikisource + Wikipedia) -> FACTS.md
- [x] Script; blind test 1 (7/10, 3 rewrites applied), retest PASS (8/10)
- [x] Narration Bankky original (speed 1.15, atempo 1.134), 11 sentences, STT 0.981-1.0, 70.1 s -> audio/narration.wav, script/captions.json
- [x] Suno text -> SUNO.md; queue row 18 WAIT on claude/new-session-73ou27
- [x] Style board built (v3/set3d18/board/style_board.jpg), sent to client; waiting for look OK
- [ ] After look OK: full set + cast (Sonnet) + one Opus QA-art; SET gate; client OK before render
- [ ] BRIEF.md, shot_plan.md (film-2 camera rhythm), WORKER18.md, render teams on Sonnet (render18/teamK)
Fallback check: send_later 60 min, always re-armed.
- [x] Music: 3 candidates m1-m3 (audio/music/), no vocals (STT); audio QA picking
- [ ] Board fix round (QA-art FIX-FIRST) -> QA-art re-check -> full set + cast -> SET gate (QA-art) -> render
- [x] SET gate r2: QA-art PASS (QA_ART_SET_R2.md, set 7/10, cast 8/10); QA-tech 3 BLOCK -> mandatory take fixes (director note in QA_TECH_R2.md)
- [x] Cast round 3 (serpentine dragon, bronze blades)
- [x] Render teams launched 2026-11-19 20:03 UTC (Sonnet, source film18/main @2029c16):
  team1 session_017iwyCvh6JPLpTAYiAjwLak render18/team1 s01 s02 s05 s06 s07
  team2 session_017iwyCx2d5GTyajVkhJFfmY render18/team2 s03 s04 s12 s25 s26
  team3 session_017iwyCur6kmjwPNg9frYYPj render18/team3 s08-s11
  team4 session_017iwyCtawR3srMLUWD2qJ8k render18/team4 s13 s14 s15 s21 s22 s24
  team5 session_017iwyCuMdzWHqsTh3fMcGVY render18/team5 s16-s20 s23
- [ ] TAKE gate per take (qa_auto + QA-tech 6 fps; QA-art key takes), conform18, FINAL gate, release18, queue row stays WAIT
- OVERRIDE s25: QA-tech bare-ground FAIL overridden; QA-art PASS + second Opus AGREE-OVERRIDE (2026-11-20)
