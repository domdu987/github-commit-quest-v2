# Film 21: "ไอ้ชาวนาบนเนิน" (Battle of Stirling Bridge, 11 Sept 1297)
Branch film21/main. Set film/v3/set3d21 (NEW), cast film/v3/cast21 (NEW). Facts and sources: FACTS.md. Shot plan: shot_plan.md.
Same style, pipeline and client rules as films 9-17: skill film/skill/reference-style-shorts (SKILL.md, "This client's rules override the style card",
references/production-lessons.md incl. §10 film-2 camera rhythm) and film/QA_TEAM.md (stricter QA).

- Narration audio/narration.wav: Bankky RwilAvCC3o05RLuACpAn, speed 1.15 original setting, atempo 1.134. Per-sentence STT 0.978-1.000. 61.25 s.
- Script script/script_th.txt; TTS text script/tts_bankky_orig.json; captions script/captions.json (phrases hand-split in script/caption_phrases.txt); timing audio/timing.json.
- Blind test (Sonnet): v1 7/10 (hook 7, ending 6) -> 3 rewrites (the ending names the mocker and echoes "เร็วดี ประหยัดดี"; the reveal is split and says the Scots waited on purpose; the aha has a new meaning: "two at a time across, two at a time back") -> retest 8/10 (hook 7, ending 8) -> 2 word fixes (ขาถอย; อ้อมไปเปลืองเงินหลวง).
- Music: fal-ai/elevenlabs/music/v2.5, force_instrumental, 67 s (= film 62 s + 5 s), 3 takes. QA picked m1 (audio/music/MUSIC.md) -> audio/music.mp3, mixed at -31 dB.
- Film length N = 1848 frames (61.60 s), hard cut on the last "ตูม".

## Client rules for this film (2026-11-19/20, mandatory)
- Look approval = Opus QA-art (style board, then SET gate), NOT the client. Do not wait for the client before rendering. The board and set sheet go to the client as FYI.
- Music made by us (above); never ask the client which take.
- POST_QUEUE row = WAIT (client posts himself). Never ask READY/WAIT.
- NEW set. Render teams run on Sonnet. Stricter QA, with the film-2 camera numbers at the final gate.
- Final mp4 committed to film21/main under film/release21/ (verify it is in the commit; watch for ignore rules).
- If fal.ai says "Exhausted balance": stop and tell the client.

## Treatment
Comic and bloodless. Soldiers splash into the river, the bridge jams, nobody dies on screen. Cressingham's fate is never shown. The dramatised quotes are marked in the post caption.
Look: a sunny morning in the Forth valley. A warm low sun, green-gold meadows, heather purple-brown, grey crags, deep teal-blue river with foam and glitter, red/blue/gold English pavilions and surcoats, earthy Scots tunics. Wide, dense and lit, never empty.
