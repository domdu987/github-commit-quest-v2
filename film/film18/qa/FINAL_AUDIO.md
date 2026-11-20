# FINAL audio gate - film 18 (oxclerk_v1.mp4)

Method: fal ElevenLabs STT (tha). Sentence windows cut from the final mix at +0.10 s and from the clean narration at 0 s (each -0.05/+0.15 s padding), compared with difflib after stripping spaces, punctuation and [sound tags]. Caption sync = ASS Dialogue start minus the STT character-level start time of the caption's first character in the full final mix (STT of mix equals STT of narration +0.10 s, median 0.100, p1-p99 0.06-0.14, so the offset is solid). Offsets were spot-checked against the audio envelope.

## Whole-film numbers
| Check | Result | Limit | Status |
|---|---|---|---|
| Integrated loudness | -12.2 LUFS (LRA 2.5 LU) | -14..-11 | PASS |
| True peak | -1.1 dBTP | <= -1.0 | PASS |
| Duration video / audio / container | 70.400 / 70.400 / 70.400 s | 70.40 | PASS |
| Caption text vs script (109 captions, ignoring spaces/!/?) | 0 diffs; ASS text == captions.json text == script_th.txt | 0 | PASS |
| SFX louder than voice (0.4 s windows, mix vs voice, master gain +6.1 dB removed) | worst +1.3 dB (s8 at 51.2 s); no window > +3 dB | <= +3 dB | PASS |

## Per sentence
| # | Beat | STT ratio (mix vs clean) | Mix-vs-voice level, sentence avg / worst 0.4 s window (dB, gain-normalised) | Caption-sync worst offset (s) | Spelling diffs |
|---|---|---|---|---|---|
| 0 | hook | 1.000 | -0.1 / +0.5 | -0.22 (c2 ใส่ชุดผ้าแดง) | 0 |
| 1 | pivot | 1.000 | -0.2 / +0.3 | +0.44 (c17 ไม่แตก); also +0.33 c18, +0.23 c19 | 0 |
| 2 | count | 1.000 | -0.1 / +0.3 | +0.13 | 0 |
| 3 | boss | 1.000 | -0.1 / +0.7 | -0.63 (c34 จะเอาวัวมา); c35 -0.34, c36 -0.31, c33 +0.34 | 0 |
| 4 | nickname | 1.000 | -0.6 / +0.1 | +0.16 (c46) | 0 |
| 5 | false | 0.983 (window padding catches next sentence's "แต่") | 0.0 / +0.4 | -0.58 (c55 หัวเราะ); c51-c58 all -0.33..-0.51 | 0 |
| 6 | turn | 1.000 | -0.3 / +0.1 | -0.19 (c62) | 0 |
| 7 | attack | 1.000 | -0.1 / +0.9 | -0.18 (c69) | 0 |
| 8 | reveal | 1.000 | -0.2 / +1.3 | +0.29 (c83 ลายมังกร) | 0 |
| 9 | aha | 1.000 | -0.2 / +1.0 | -0.14 | 0 |
| 10 | ending | 1.000 | -0.6 / +0.6 | +0.19 (c105 ลั่นวาจาไว้) | 0 |

STT minimum 0.983 (threshold 0.93). Integrated LUFS / true peak are film-level (-12.2 / -1.1); per-sentence loudness is shown as relative level above.

## Caption sync detail (FAIL)
31 of 109 captions are outside +-0.15 s (13 outside +-0.30 s). Median |offset| 0.08 s, p90 0.33 s, max 0.63 s. Negative = caption appears before the voice.
- Sentence 3 (boss): the narrator laughs ("[เสียงหัวเราะ]" 22.06-22.7 s), then pauses until 23.18 s (envelope near -30 dB 22.75-23.1 s). Captions c34-c36 ("จะเอาวัวมา / สู้ทัพข้า / งั้นเหรอ!") start 0.63 / 0.34 / 0.31 s before the voice; c33 "ลั่น" is 0.34 late. The caption timeline does not include the laugh/pause.
- Sentence 5 (false): captions c51-c58 (33.51-38.5 s, "ทหารเยียน" ... "พรุ่งนี้กิน") run 0.33-0.58 s ahead of the voice, then re-sync by c60 (e.g. c51 ass 33.51 vs speech 33.84; c55 ass 36.50 vs speech 37.08).
- Sentence 1: c17 "ไม่แตก" +0.44, c18 "หนึ่งคือจี๋โม่" +0.33, c19 +0.23 (late); c10/c11/c13 are 0.17-0.28 early.
- Minor: c2, c9, c35.. c46, c62, c63, c65, c69, c76, c83, c103, c105 are 0.16-0.29 off.

Suggested fix: re-time captions.json from the STT character times of the mix (minus 0.10 s) per phrase, or at least for sentences 1, 3 and 5, then re-burn the ASS. Audio itself needs no change.

## Verdict
First-pass verdict (superseded by Re-check below): FAIL

Reason: caption sync is outside the +-0.15 s rule (31/109 captions, worst 0.63 s in sentence 3, sustained 0.3-0.58 s early in sentence 5). Everything else passes: STT >= 0.983 on all 11 sentences, -12.2 LUFS, -1.1 dBTP, no SFX above voice (worst +1.3 dB), spelling identical to script, duration 70.40 s with audio = video.

## Re-check (captions re-timed from clean-narration STT; new oxclerk_v1.mp4 / .ass)
- Caption sync vs final-mix STT (re-run STT on the new mix, same method): 109/109 captions within +-0.15 s; max |offset| 0.06 s (c34), median 0.00 s, p90 0.02 s. The earlier offenders (s1 c17-19, s3 c33-36, s5 c51-58) are now 0.00..-0.06 s. PASS.
- Spelling: 109 ASS captions == captions.json == script_th.txt (ignoring spaces/!/?), 0 diffs. PASS.
- Loudness unchanged: -12.2 LUFS, true peak -1.1 dBTP; video and audio both 70.400 s; SFX-vs-voice re-run: 0 windows above +3 dB. PASS.
- Note: captions now derive from the same STT family as the check, so sync is self-consistent; the earlier envelope spot checks (pause at 22.7-23.1 s, 33.75 s) agree with the new times.

FINAL audio: PASS
