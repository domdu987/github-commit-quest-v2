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
