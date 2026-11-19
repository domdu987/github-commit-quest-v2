# QA AUDIO - film 12 v1 (FINAL gate, reviewer 2)
File: film/release12/film12_v1.mp4 (59.5 s). No music bed in this version (Suno track pending): rain bed + SFX only.
Method: faster-whisper medium (int8, CPU, numpy audio, language th, beam 5). Mix cut at sentence window +0.10 s (measured lag by cross-correlation 0.105 s, constant at 0-10, 20-30, 45-55 s).

## 1. Per-sentence STT, mix vs clean (>= 0.93): PASS
Name Hanway normalised. Raw ratio / ratio after digit-to-Thai-word normalisation:
| s | raw | digits normalised |
|---|-----|------|
| 0 | 0.973 | 0.973 |
| 1 | 1.000 | 1.000 |
| 2 | 0.981 | 0.981 |
| 3 | 1.000 | 1.000 |
| 4 | 0.937 | 0.983 |
| 5 | 0.968 | 0.969 |
| 6 | 1.000 | 1.000 |
| 7 | 0.995 | 0.995 |
| 8 | 1.000 | 1.000 |
Minimum 0.937 (s4, the lowest value; the only difference is whisper writing "2"/"3" in the clean take and "สอง"/"สาม" in the mix, plus one vowel). Mix is as intelligible as the clean narration everywhere. Details: scratchpad/final_qa/stt.json.

## 2. Loudness / true peak: PASS
Integrated -12.2 LUFS (target -14..-11), LRA 2.8 LU, true peak -1.4 dBTP (limit <= -1).

## 3. No SFX louder than the voice: PASS
555 windows of 0.4 s (hop 0.1 s) inside the nine sentence windows. The mix is uniformly +6.07 dB over the clean narration (mastering gain; the raw difference alone is not meaningful). After removing that gain: max excess of mix over narration +1.50 dB, 0 windows above +3 dB.
Cross-check: subtracting the gain-matched clean narration from the mix leaves the non-voice residual (rain + SFX); in 0 of 555 windows is it as loud as the voice (closest: s7 t=50.8 s, residual 5.1 dB below the voice; s2 12.9 s, 4.5 dB below).

## 4. Caption timing within +-0.15 s: FAIL
Reference: whisper word timestamps per sentence on the clean narration, aligned to the script characters (82 of 86 caption starts anchored directly, 4 interpolated). Offset = caption on-screen (t+0.10) minus spoken onset (narration + 0.10); positive = caption late.
- No global offset: median +0.001 s, mean -0.005 s.
- But 30 of 82 anchored captions are outside +-0.15 s (33 of 86 overall), 5 outside +-0.30 s, p90 |offset| 0.25 s.
- Worst: s2 "ผู้ชายกางร่ม" -0.58 s (caption film 12.76, spoken 13.34), s2 "ลั่น" -0.49, s7 "ทีละคน" +0.46 (film 48.15, spoken 47.69), s7 "เริ่มกางตามกัน" +0.37, s2 "เหรอ!" -0.32, s5 "ทั้งเมือง" -0.31, s4 "รถม้าพุ่งลุย" -0.30.
- Independent energy check of s2: narration has a pause 13.0-13.15 s and speech restarts at ~13.2 s, i.e. caption "ผู้ชายกางร่ม" shows about 0.5 s before it is spoken (laugh/pause in sentence 2 pushes the proportional-by-voiced-frames caption placement early).
- Caveat: Thai whisper word timestamps are noisy (about +-0.1 to 0.15 s), so the 0.15-0.3 s cases are borderline; the s2 (two phrases) and s7 (two phrases) cases at 0.37-0.58 s are beyond that noise.
- Cause: captions.json is built by distributing phrase starts proportionally over voiced frames per sentence (build_bk0.py), not from true word times. Sentences 2 (laugh) and 7 are worst. Fix: re-time those sentences' phrases from forced alignment / bk0 char timestamps.

## 5. Caption text == script text: PASS
All 9 sentences: concatenated captions (spaces removed) are identical to the script sentence (spaces removed); 86 phrases, sentence indices 0-8 all covered.

## Overall: FAIL (item 4 only)
Items 1, 2, 3, 5 pass. Item 4 fails on caption timing in sentences 2 and 7 (worst -0.58 / +0.46 s), plus many 0.15-0.3 s deviations. Audio mix itself (intelligibility, loudness, peak, SFX balance) is clean. Scripts used: scratchpad/final_qa/{stt,sfx,res,words2,cap2}.py.
