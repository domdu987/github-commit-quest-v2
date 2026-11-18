# Film 11 "ไอ้หมอวัว" delivery report (2026-11-18), release11/cowdoc_v1_nomusic.mp4
- Length 62.5 s, 1875 frames, 720x1280, 30 fps. Music: NOT yet (waiting for the client's Suno track).
- SET gate: QA-tech FAIL + QA-art FIX-FIRST -> 1 fix round + polish -> client OK.
- TAKE gate: 28 takes; QA-tech 6 fps + cuts, QA-art on key takes; 4 rounds (s26 queue re-staged twice). No overrides.
- FINAL gate:
  1. qa_auto full film: PASS (0 frozen, 0 black, 0 magenta, 0 pops; soft frames g774-788 = the planned dissolve into s13).
  2. Audio: -12.4 LUFS integrated, true peak -1.6 dBTP. Per-sentence STT mix vs clean narration 0.98-1.03 (absolute 0.90-1.00; s4/s6 at 0.90 equal the clean narration: digits vs Thai words in the ASR). Captions = script text; timing from voiced frames.
  3. QA-art: round 1 FIX (s24 too sparse) -> s24 re-rendered -> round 2 SHIP. Overall 8/10.
  4. Blind viewer (phone sheet + timed narration): all 4 questions answered correctly; 6/10 clarity (hook first 2.5 s, day count, s23 small at phone size rely on narration).
- Overrides: none.

## v1 with the client's Suno music ("The Curious Shepherd's Quest", 92.4 s) -> release11/cowdoc_v1.mp4
- Music bed at -31 dB RMS under the voice (series standard), fades out at the hard cut.
- Loudness -12.3 LUFS integrated, true peak -1.6 dBTP.
- Per-sentence STT, mix with music vs clean narration: ratios 0.96-1.02 (no sentence worse by more than 4 %). Absolute vs script 0.90-0.98; sentences 2, 5, 7, 8 (0.90-0.92) score about the same on the clean narration (ASR digits / Thai spelling), not masking.
