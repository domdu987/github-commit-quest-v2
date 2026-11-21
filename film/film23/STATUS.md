# Film 23 status (director): "ไอ้กองทัพลูกโป่ง" (Ghost Army, 23rd HQ Special Troops)
Branch film23/main. Set film/v3/set3d23, cast film/v3/cast23. Render teams: outcome render23/teamK, source film23/main, Sonnet.
Client rules: QA-art approves the look (no waiting for the client); music fal elevenlabs/music/v2.5 instrumental, 2-3 takes, QA picks, -31 dB;
queue row WAIT; voice Bankky original (speed 1.15, atempo ~1.134); stricter QA; FINAL gate vs film 2 + ref sheets.
Fallback check: send_later 60 min, always re-armed.

- [x] Facts web-checked -> FACTS.md (1,100 men; Viersen 18-24 Mar 1945; 600 dummies; 2 divisions; sound ~15 mi; 93 lb decoy; cyclist anecdote)
- [x] Script v1, blind test 1: 7.5/10, 3 rewrites applied -> script/script_th.txt (v2), TTS text script/tts_bankky_orig.json
- [x] Blind retest PASS 8/10; 2 small rewrites applied (hook stake shortened, nickname line "ทั้งหน่วยเลยโดนเรียกว่า")
- [ ] BLOCKED 2026-11-20 23:55 UTC: fal.ai "User is locked. Reason: Exhausted balance." Narration + music cannot be generated. Client told.
      Resume: cd film/film23 && python3 audio/gen.py && python3 audio/build_bk0.py --stt  (then python3 audio/build_bk0.py)
- [x] Style board r1 (v3/set3d23/board) -> QA-art FIX-FIRST (board/QA_ART.md: overall 5/10, still 2 recompose, shadows, night tanks, caption band)
- [ ] Board r2 (builder fixing all 8 QA-art items) -> QA-art re-check
- [ ] Set + cast -> SET gate -> shot plan (≤12 cuts, 2 BIGZOOM) -> WORKER23.md -> render teams
- [x] QA §K adopted (producer 2026-11-21): ground_check before every render, contact shadow on every card/prop, independent float hunter at TAKE+FINAL. Tanks sit on the ground except in the lift gag.
- [x] QA §L adopted (producer 17bbec1): no random shake; shake() only on real impact (amp ≤0.15 deg, ≤0.6 s); qa_jitter.py ≤2 px/s. Max 3 render teams at once.
- STOPPED 2026-11-21 by client order (via producer): no renders, no agents, no send_later. Board r3 builder killed mid-work; its WIP is committed. Resume only when the producer says continue.

## RESUMED 2026-11-21 ~02:30 UTC (client in this chat: "ทำต่อได้ ใช้สกิลใน film/skill_film13 ทำให้เสร็จ")
Process = film/skill_film13 (skill as of films 1-13) + standing decisions: music on fal (elevenlabs/music/v2.5), QA-art approves the look,
text signs allowed, queue row WAIT, max 3 render teams, free automatic checks on every take (qa_auto, v3/tools/ground_check.py, qa_jitter).
No extra review layers (§G-§L multi-reviewer gates dropped). fal still exhausted -> picture first on ESTIMATED timing, narration/music later.
- [x] Board r3 (Opus, partial) re-rendered: still 2 now hero tank; numbers sat 0.53-0.58, luma 95-107, shade hue 245/252/223(night). Look accepted as base; final look check at SET gate.
- [x] Estimated timing audio/timing_EST.json (70.3 s); shot_plan.md v1 (19 shots, BIGZOOM S01+S12, takes render x1.25 length for retiming)
- [ ] Full set (Opus builder, running) + cast23 (Opus builder, running) -> one QA-art SET check -> WORKER23.md -> 3 render teams
- [x] Cast23 (Opus) committed; full set v1 committed; SET gate QA-art (QA_ART_SET.md): LANE PASS, CAMP PASS, FIELDS FIX (S01), RHINE FIX (S14-S18)
- [x] Render teams launched 2026-11-21 04:13 UTC (Sonnet, source film23/main @2cdcb73):
  team1 session_017iwyCtvhJgyg3a8pwiDW3V render23/team1 S02-S08
  team2 session_017iwyCwdz3vZPczGX7PPrA4 render23/team2 S09 S10 S11 S12 S13 S19
- [x] FIELDS + RHINE fixed (director accepted, notes in QA_ART_SET.md)
  team3 session_017iwyCtMyJ4HG42ELGQD298 render23/team3 S01 S14-S18 (launched 04:44 UTC from a29598b)
- [ ] fal top-up -> narration (gen.py, build_bk0.py --stt), music 2-3 takes -> retime conform -> release23
