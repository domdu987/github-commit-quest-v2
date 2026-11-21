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
