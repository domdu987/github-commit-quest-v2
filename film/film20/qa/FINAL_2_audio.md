# FINAL gate 2 - audio + captions, film20_rc2.mp4

**Verdict: FAIL** (check 4 caption sync; checks 1, 2, 3, 5 PASS)

## Check 1 - per-sentence STT, final mix vs clean narration (fal-ai/elevenlabs/speech-to-text, tha)

| # | window (s) | final-vs-clean ratio | clean-vs-script (info) | loudest SFX (peak dB) vs voice voiced RMS -14 dB | caption phrases >0.15 s off | worst dev (s) |
|---|---|---|---|---|---|---|
| 1 | 0.1-6.03 | 1.000 PASS | 1.000 | hmph -24 | 3/9 | -0.23 |
| 2 | 6.03-13.57 | 1.000 PASS | 0.866 | rivet_hammer -26 | 4/9 | +0.42 |
| 3 | 13.57-25.19 | 1.000 PASS | 0.987 | chair_scrape -24 | 3/17 | +0.27 |
| 4 | 25.19-27.51 | 1.000 PASS | 1.000 | whoosh_punch -24 | 1/3 | -0.18 |
| 5 | 27.51-33.31 | 1.000 PASS | 1.000 | rivet_catch -22 | 4/8 | +0.35 |
| 6 | 33.31-40.8 | 1.000 PASS | 0.957 | seal_stamp -22 | 6/11 | -0.63 |
| 7 | 40.8-43.49 | 1.000 PASS | 1.000 | crowbar_clank -26 | 1/3 | -0.20 |
| 8 | 43.49-52.12 | 1.000 PASS | 1.000 | wire_twang -24 | 6/12 | -0.52 |
| 9 | 52.12-57.85 | 1.000 PASS | 1.000 | tools_drop -22 | 3/8 | -0.23 |
| 10 | 57.85-67.9 | 1.000 PASS | 0.994 | cutlery_clink -24 | 7/16 | +0.33 |

Final and clean STT transcripts were character-identical in every sentence (ratio 1.000, threshold 0.93). The lower clean-vs-script ratios (S2 0.866, S6 0.957) are only STT writing digits / number words differently from the script, not audio damage.

## Check 2 - loudness (ffmpeg ebur128 peak=true on mp4)
Integrated -12.6 LUFS (range -14..-11) PASS; true peak -1.2 dBTP (limit -1) PASS; LRA 1.7 LU.

## Check 3 - SFX vs voice
Voice pre-limiter (gain 1.396): voiced RMS about -14 dBFS in every sentence, peaks about 0 dBFS. Loudest one-shot SFX per sentence peaks -22..-26 dBFS (table above), i.e. at least 8 dB under voice RMS and over 20 dB under voice peaks; beds -35..-38, music -31 RMS. No SFX louder than voice. PASS.

## Check 4 - caption sync (STT char timestamps on clean narration +0.10 s vs ASS start)
96 phrases; **38 exceed +-0.15 s** (mean offset -0.06 s, range -0.63..+0.42; negative = caption earlier than STT time). Worst: S6 'เห็นมั้ย' 37.67 vs spoken 38.30 (-0.63), 'หอของ' -0.51, 'ไอ้ช่างหมุด' -0.51, S8 'หอทั้งต้น' -0.51, 'เลยกลายเป็น' -0.52, 'สัญญาณ' -0.48; late captions: S2 'วิศวกรไอเฟล' +0.42, S5 'หมุด' +0.35, 'สองล้านครึ่งตัว' +0.33, 'สูง 300 เมตร' +0.32, S10 'หอไอเฟล' +0.33. Clusters: S2 (8.9-12.4 late), S5 (30.3-32.3 late), S6 end (37.7-40 early), S8 (47.8-51.3 early), S10 (59-65 mixed). Captions are proportionally timed per sentence, not word-aligned. Caveat: Thai STT char timestamps are noisy; an independent energy-onset check agrees in direction for the S6 and S8 clusters at smaller magnitude (captions about 0.1-0.4 s ahead of nearest voiced onset). Sentence-level sync is fine (every caption within its sentence). Per the +-0.15 rule: FAIL.

Full list of 38 offenders: scratchpad conf/f2/sync.json (start, text, stt_time, delta).

## Check 5 - caption text vs script
Caption ASS == captions.json == caption_split.txt (96 phrases, identical). Versus script_th.txt the only differences are the intended digit forms (ปี 1887, 300 เมตร, 18,000 ชิ้น, 20 ปี, 70 ปี); one script phrase ยี่สิบปี appears as 'ยี่สิบปีผ่านไป' in the crisis sentence (spelled out, matches script) while 'ได้แค่ 20 ปี' is digits as intended. No spelling differences. PASS.
