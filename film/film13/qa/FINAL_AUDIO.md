# FINAL AUDIO gate, film 13 (release13/raeng.mp4)  -- OVERALL: FAIL (caption timing)

| Check | Result |
|---|---|
| 1 STT per sentence, final mix vs script (>=0.93) | PASS, min 0.938 (s1) |
| 2 Loudness / true peak | PASS, I = -13.2 LUFS, TP = -2.7 dBTP, LRA 2.4 LU |
| 3 SFX not louder than voice | PASS at sentence/peak level, with notes |
| 4a caption text == script | PASS (all 10 sentences, 102 phrases; .ass text == captions.json text) |
| 4b caption timing within +-0.15 s | FAIL |

## 1. STT (fal ElevenLabs, difflib ratio, norm = strip whitespace . , ! ? quotes and ๆ)
Final mix, cut S+0.10..E+0.10 from mp4:  s0 1.000, s1 0.938, s2 1.000, s3 1.000, s4 0.986, s5 1.000, s6 0.974, s7 1.000, s8 1.000, s9 1.000.
Clean narration (reference):             s0 1.000, s1 1.000, s2 1.000, s3 1.000, s4 0.986, s5 1.000, s6 0.974, s7 1.000, s8 1.000, s9 0.994.
s1 on the mix: STT wrote "Chicago" for ชิคาโก and dropped a space after นะ/ก่อน (a spelling variant, not a mispronunciation; clean narration scores 1.000). Margin 0.008 over the 0.93 limit.

## 2. Loudness
ebur128 on the mp4: integrated -13.2 LUFS (window -14..-11), true peak -2.7 dBTP (<= -1), LRA 2.4 LU. Duration video 66.500 s / audio 66.517 s.

## 3. SFX vs voice
Method: aligned narration x fitted gain (k=1.21, lag 0.103 s incl. AAC delay, xcorr 0.95) = voice-only; residual = mix - voice (music + SFX).
- Per sentence: voice RMS -13.2 dBFS, residual (music+SFX) -22.6..-23.6 dBFS, i.e. 9.4-10.4 dB under the voice in every sentence.
- Loudest 50 ms residual in any SFX window: -15.8 dBFS (murmur+rattle/whistle region 43-47 s; thud 32-34 s -16.5), still 2.6 dB below the voice sentence RMS. No SFX window exceeds the voice level. The mix spec already ducks SFX that overlap speech (conform13 _talk rule).
- Literal 50 ms test (mix > voice-only + 3 dB while voice window > -26 dBFS): 23 of 1106 speech windows (2%), max +5.6 dB at 33.3 s (thud). Every one sits in a micro-pause/consonant dip where the voice window is -19..-26 dBFS (7-12 dB under the word peaks); 12 of the 23 have no listed SFX (music bed only). Windows with a listed SFX: 7.75 rain; 16.55-17.9 street; 31.3 rattle/murmur; 33.3, 34.3 thud+murmur; 45.45 whistle/rattle/murmur; 52.85 street; 56.0 street; 58.3, 59.9 street; 62.55 whoosh; 63.25, 63.9 splat/chirp. Judged not masking (words intact: STT >= 0.938), flagged for information only. Optional trim if wanted: -2 dB on the 33.2 thud, 44.75 whistle and the street bed at 16-18 s.

## 4. Captions
Text: concatenated phrases per sentence == script line (spaces ignored) for all 10 sentences. .ass has 102 Dialogue lines, equal to captions.json, text identical, start = t + 0.10 exactly (max deviation 0.000 s). So the .ass faithfully carries the caption file.
Timing vs speech: FAIL. Captions are placed by proportional voiced-frame timing, which drifts from the actual words. Compared each phrase start with the STT word-start time (ElevenLabs char timestamps, mapped by cumulative character index): 55 of 102 phrases are off by more than 0.15 s (48 if s1 is excluded, where the "Chicago" spelling shifts the index mapping). Typical error: caption appears 0.2-0.4 s BEFORE the phrase is spoken (up to -0.58 s). Independent energy check confirms it: s0 caption "ทำให้โรงแรม" shows at 0.57 s but the preceding word "ชายคนนี้" is still voiced until ~0.80 s (the next word starts ~0.90 s) -> 0.3 s early.
Worst examples (caption shown / word spoken): s3 "ตึกอิฐทั้ง" 21.78 / 22.36 (-0.58); s0 "ขึ้นจากพื้น" 2.12 / 2.54 (-0.42); s9 "ขึ้นเกือบสอง" 59.78 / 60.15 (-0.37); s6 "เศรษฐีมองออก" 37.74 / 38.08 (-0.34); s7 "ทุกครั้งที่" 44.04 / 44.39 (-0.35). Some late the other way: s2 "กว่า" +0.24, s8 "ยกตึกได้" +0.23.
Sentences with the worst drift: s0, s2, s3, s6, s7, s9. s4 and s5 are within tolerance.
Fix: re-time captions.json from per-word STT timestamps of narration.wav (or forced alignment) instead of proportional frames, regenerate raeng.ass (t+0.10), re-burn; no re-mix needed.

---
# ROUND 2 (captions re-timed, raeng.ass / raeng.mp4 re-burned) -- caption checks: PASS
- Text: 102 phrases; per-sentence concatenation == script line for all 10 sentences; .ass text identical to captions.json; .ass start = t + 0.10 exactly (max dev 0.000 s).
- Timing, same method (caption start vs STT word-start of the phrase's first character, cumulative-char mapping):
  - vs STT of clean narration (+0.10): 102/102 within +-0.15 s, mean -0.030 s, max |dev| 0.07 s.
  - vs STT of the final mix: 100/102 within +-0.15 s, mean -0.023 s; the 2 outliers are both in s1 ("ถนนกลายเป็นบึง" +0.33, "น้ำเสียไหลไป" +0.17) and are the known "Chicago" spelling index-shift artifact of the mix STT (same phrases measure within 0.07 s against the clean-narration STT).
  - Round 1 had 55/102 outside tolerance (up to -0.58 s); now none.
- Audio checks 1-3 unchanged (mix unchanged: -13.2 LUFS, TP -2.7 dBTP). OVERALL AUDIO GATE: PASS.
