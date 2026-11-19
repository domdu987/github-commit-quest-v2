# Film 13 "ไอ้แม่แรง" - FINAL gate report (2026-11-19)
File: film/release13/maeraeng_v1.mp4 (66.5 s, 720x1280, 30 fps)
1. Scripts (qa_auto, every frame): 0 frozen / 0 black / 0 missing frames, magenta 0.0 %. FLAG: 'suspected blur' on ~104 frames
   (g 152-161 tea close-up, 594/639-642 suite, ...). OVERRIDE (rule E): QA-art (Opus, independent, saw full-size frames) confirms
   these are false positives from large smooth areas (table, sky, parquet); no DOF/blur anywhere. See FINAL_ART.md.
2. Audio: per-sentence STT on final mix 0.938-1.000 (all >= 0.93); -13.2 LUFS integrated; true peak -2.7 dBTP; no SFX above voice
   at sentence level (music+SFX 9.4-10.4 dB under voice); captions == script text (102/102); caption timing round 2: 102/102 within
   +-0.15 s of the clean-narration word starts (100/102 vs final-mix STT; the 2 outliers are the "Chicago" spelling mapping). FINAL_AUDIO.md.
3. QA-art: SHIP after the s26 shot-28 fix (near-camera townsman with head below y 880 removed, re-rendered, re-conformed, re-checked
   by director on 6 fps frames g 1797-1830). Scores 7-8. Non-blocking notes: s10 dusk light vs s11 day; s07 confetti clouds; s25 ceiling smear.
4. Blind viewer: all four answers correct (hook, mocker + promise, mechanism, ending). Notes: hotel rise subtle on phone in the hook
   and at 48-50 s; purse read as a jug.
TAKE gate: all 17 takes (30 shots) passed QA-tech; key takes passed QA-art. Overrides: only the qa_auto blur flag above.
Music: client Suno "The Curious Mechanism" (no vocals/drums). SFX: reused from earlier films' libraries (fal SFX service was down).
