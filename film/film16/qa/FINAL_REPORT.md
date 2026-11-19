# Film 16 "ไอ้บ้าลวด" — FINAL gate report (2026-11-19)
Release: film/release16/wire_v1.mp4 (69.9 s, 720x1280, 30 fps). Music: NOT yet (client's Suno file pending); voice + 61 SFX cues.
1. Scripts (qa_auto, every frame): PASS — 2096 frames, 0 black/frozen, magenta 0.0 %, cuts at plan (hard cuts diff 44-94, dissolves 10-14).
   Camera motion (90x160 grey, in-shot): film 16 median 7.78 / p90 18.82 vs film 2 median 5.28 / p90 19.40 (target >= 4 / >= 12).
2. Audio: PASS — per-sentence STT on the final mix vs script 0.941-1.000 (target >= 0.93); integrated -13.2 LUFS (target -14..-11); true peak -1.6 dBTP (target <= -1, limiter added); captions from the narration timing (same text as script_th.txt, checked by QA-art).
3. QA-art (Opus): v1 FIX-FIRST (shot 28 sacks read as money) -> shot 28 re-rendered -> v2 SHIP. Scores 7-8 (hook 9, false payoff 8, ending 8).
4. Blind viewer (Sonnet, phone sheet + timed narration): PASS — hook, mocker + promise, mechanism (leak into soil / wet poles / glass insulates) and ending irony all answered correctly. Clarity 7, entertainment 8.
Overrides: none. TAKE gate: all 30 shots passed (rounds 1-5; reports in this folder).
Open non-blocking notes: backstory wife not visual; bottle green vs turquoise neck; s07 magnet spark small; s30 Morse small on phone; countryside set sparser than film 10; s17 p90 10.3 (film-level passes).

## v2 (music added, 2026-11-19)
Music: fal ElevenLabs Music v2.5, 3 beat-timed instrumental variants (A Americana folk, B cartoon woodwinds, C ragtime). QA music reviewer (Opus, from measurements) chose A (ranking A > C > B: A follows the beats incl. the stop on "เงียบกริบ"; C is anachronistic and ignores the stop; B has a 17-s hole).
Repairs on A (film16/audio/music/fix_A.py): section gains, rain bars looped over the 40-46 s hole, A's own plucks spliced as the 46-53 s reveal build, -2 dB at 3 kHz under the aha line, 0.4 s tail fade; rain_heavy bed extended to 40.6-46.4 s.
Bed after normalising to -31 dB RMS: sections -29.3 to -30.5, silence beat -35.5 (deliberate), rain -36.5, reveal -35.9 rising into the triumph -29.3; no 1-s window below -43.
Final mix: -13.3 LUFS, true peak -2.1 dBTP. Per-sentence STT (local faster-whisper large-v3-turbo, because the fal balance is exhausted): mix vs clean narration within -3.7 % on every sentence (limit -5 %). Picture identical to v1 (FINAL QA-art SHIP stands).
Not verified: no automatic vocal-content check of the music (fal locked) — a human should listen for hummed/sung vocals or shouts.
