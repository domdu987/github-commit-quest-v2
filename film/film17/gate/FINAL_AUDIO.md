# FINAL AUDIO gate, film 17 (ear_v1.mp4, 68.4 s)

## VERDICT: FAIL (captions out of sync beyond +-0.15 s; everything else passes)

## 1. Per-sentence STT (fal elevenlabs/speech-to-text, tha), mix window vs clean narration window, norm + difflib ratio. Threshold 0.93

| # | beat | mix vs clean | mix vs script | clean vs script | result |
|--|--|--|--|--|--|
| 0 | hook | 1.000 | 1.000 | 1.000 | PASS |
| 1 | pivot | 1.000 | 0.990 | 0.990 | PASS |
| 2 | setup | 1.000 | 1.000 | 1.000 | PASS |
| 3 | boss | 0.995 | 1.000 | 0.995 | PASS |
| 4 | nickname | 1.000 | 1.000 | 1.000 | PASS |
| 5 | deadline | 1.000 | 1.000 | 1.000 | PASS |
| 6 | count | 1.000 | 1.000 | 1.000 | PASS |
| 7 | false | 1.000 | 1.000 | 1.000 | PASS |
| 8 | crisis | 1.000 | 0.987 | 0.987 | PASS |
| 9 | reveal | 1.000 | 0.991 | 0.991 | PASS |
| 10 | aha | 1.000 | 1.000 | 1.000 | PASS |
| 11 | ending | 1.000 | 1.000 | 1.000 | PASS |

Min mix-vs-clean = 0.995. PASS.

## 2. Loudness (ffmpeg ebur128 peak=true, whole mp4 audio)

- Integrated: -12.2 LUFS (target -14..-11) PASS
- True peak: -1.5 dBTP (target <= -1) PASS
- LRA 1.9 LU

## 3. SFX vs voice inside sentences

Stems rendered with the project mixer from ear_v1_mix.json (voice only, sfx only, music only, pre-limiter). Levels are over each cue window (dBFS). Margin = voice RMS minus SFX RMS.

| cue | at (s, film) | sent | SFX peak | SFX RMS | voice RMS | margin | SFX peak vs voice peak |
|--|--|--|--|--|--|--|--|
| caliper_click.mp3 | 1.05 | 0 | -26.0 | -56.0 | -14.2 | 41.8 dB | 25.0 dB below |
| caliper_click2.mp3 | 3.45 | 0 | -27.0 | -53.0 | -15.2 | 37.8 dB | 24.9 dB below |
| caliper_click.mp3 | 4.35 | 1 | -27.1 | -49.2 | -14.7 | 34.5 dB | 26.1 dB below |
| caliper_click2.mp3 | 28.9 | 6 | -27.0 | -55.8 | -14.7 | 41.1 dB | 26.0 dB below |
| caliper_click.mp3 | 30.5 | 6 | -28.0 | -57.2 | -14.6 | 42.6 dB | 26.2 dB below |
| caliper_click2.mp3 | 32.3 | 6 | -28.0 | -56.8 | -15.0 | 41.8 dB | 27.0 dB below |
| caliper_click.mp3 | 45.35 | 9 | -24.0 | -45.7 | -13.6 | 32.1 dB | 23.0 dB below |
| caliper_click2.mp3 | 47.4 | 9 | -24.5 | -43.0 | -15.4 | 27.6 dB | 23.5 dB below |
| caliper_click.mp3 | 49.3 | 9 | -27.0 | -56.0 | -14.0 | 42.0 dB | 26.0 dB below |
| caliper_click2.mp3 | 65.8 | 11 | -26.0 | -54.6 | -14.6 | 40.0 dB | 25.0 dB below |
| caliper_click.mp3 | 67.5 | 11 | -24.0 | -52.7 | -18.8 | 33.9 dB | 19.3 dB below |
| crowd_laugh.mp3 | 15.0 | 3 | -29.0 | -43.1 | -14.6 | 28.5 dB | 28.0 dB below |
| crowd_laugh.mp3 | 21.8 | 5 | -29.0 | -44.1 | -14.9 | 29.2 dB | 28.0 dB below |
| crowd_laugh.mp3 | 38.6 | 8 | -33.0 | -47.0 | -13.9 | 33.1 dB | 32.0 dB below |
| wagon_horse.mp3 | 4.9 | 1 | -30.0 | -48.4 | -13.7 | 34.7 dB | 29.0 dB below |
| wagon_horse.mp3 | 9.0 | 1 | -39.1 | -56.8 | -15.0 | 41.8 dB | 38.1 dB below |
| drawer_slide.mp3 | 33.7 | 7 | -25.0 | -49.5 | -15.6 | 33.9 dB | 24.0 dB below |
| drawer_slide.mp3 | 45.8 | 9 | -24.0 | -43.1 | -13.5 | 29.6 dB | 23.0 dB below |
| drawer_slide.mp3 | 47.1 | 9 | -24.5 | -38.5 | -13.9 | 24.6 dB | 23.5 dB below |
| paper_flutter.mp3 | 49.7 | 9 | -32.0 | -58.0 | -14.1 | 43.9 dB | 31.0 dB below |
| paper_flutter.mp3 | 51.3 | 9 | -35.0 | -59.7 | -16.2 | 43.5 dB | 32.5 dB below |
| paper_flutter.mp3 | 60.1 | 10 | -32.0 | -59.6 | -15.3 | 44.3 dB | 31.0 dB below |
| gasp.mp3 | 54.05 | 9 | -26.5 | -40.6 | -14.0 | 26.6 dB | 25.5 dB below |
| sting.mp3 | 53.46 | 9 | -16.0 | -30.5 | -14.2 | 16.3 dB | 15.0 dB below |
| whoosh.mp3 | 44.72 | 9 | -33.0 | -50.3 | -12.0 | 38.3 dB | 32.0 dB below |
| whoosh.mp3 | 55.15 | 9 | -33.3 | -50.1 | -15.1 | 35.0 dB | 32.3 dB below |
| clock_tick.mp3 | 35.0 | 7 | -33.0 | -55.5 | -14.9 | 40.6 dB | 32.0 dB below |
| clock_tick.mp3 | 38.9 | 8 | -33.0 | -47.0 | -13.8 | 33.2 dB | 32.0 dB below |

Smallest RMS margin: 16.3 dB (sting at 53.46 s, deliberately un-ducked, SFX peak -16 dBFS vs voice peak about -1). No SFX dominates any sentence. PASS.

### SFX source files (film/film17/audio/sfx/), peak and STT

| file | dur s | peak dBFS | STT text |
|--|--|--|--|
| caliper_click.mp3 | 1.52 | 0.0 | (empty, no words) |
| caliper_click2.mp3 | 1.52 | -6.8 | (empty, no words) |
| clock_tick.mp3 | 4.05 | -10.1 | (empty, no words) |
| crowd_laugh.mp3 | 4.05 | -0.3 | (empty, no words) |
| drawer_slide.mp3 | 2.51 | -6.1 | (empty, no words) |
| gasp.mp3 | 2.04 | 0.0 | (empty, no words) |
| paper_flutter.mp3 | 2.04 | -10.2 | (empty, no words) |
| sting.mp3 | 2.51 | 0.0 | (empty, no words) |
| wagon_horse.mp3 | 4.05 | -5.5 | (empty, no words) |
| whoosh.mp3 | 4.05 | 0.0 | (empty, no words) |

None silent, none contain intelligible words. PASS. (Listen-proxy only; no human listening done.)

## 4. Captions

### Text vs script (concatenate per sentence, strip spaces/punct)

All 12 sentences EXACT match (ratio 1.000). captions.json (102 captions) and ear_v1.ass (102 Dialogue lines) agree on time (+0.10 s) and text, 0 mismatches. PASS.

### Start time vs spoken phrase (char-level word timings from STT on the clean narration, caption t compared at same narration clock; film offset +0.10 applies to both)

- First caption of every sentence: within 0.07 s of timing.json sentence start. OK.
- Over all 102 captions: mean offset -0.021 s, max |offset| 0.78 s, 34 captions outside +-0.15 s, 8 outside +-0.30 s. FAIL.

Positive = caption appears after the phrase is spoken; negative = caption appears before.

| sent | captions | outside 0.15 | max abs offset |
|--|--|--|--|
| 0 | 7 | 5 | 0.56 |
| 1 | 10 | 2 | 0.27 |
| 2 | 5 | 0 | 0.12 |
| 3 | 11 | 3 | 0.21 |
| 4 | 3 | 0 | 0.07 |
| 5 | 6 | 1 | 0.25 |
| 6 | 9 | 4 | 0.78 |
| 7 | 6 | 3 | 0.30 |
| 8 | 8 | 2 | 0.20 |
| 9 | 18 | 8 | 0.38 |
| 10 | 9 | 2 | 0.33 |
| 11 | 10 | 4 | 0.24 |

All captions outside tolerance (narration clock):

| sent | caption | caption t | spoken t (STT) | offset |
|--|--|--|--|--|
| 0 | ไปวัดหูโจร | 1.59 | 1.35 | +0.24 |
| 0 | ทุกคนที่ | 2.49 | 2.11 | +0.38 |
| 0 | ถูกจับมา | 3.15 | 2.59 | +0.56 |
| 0 | ทีละคน | 3.73 | 3.37 | +0.36 |
| 0 | ทีละหู | 4.17 | 3.97 | +0.20 |
| 1 | ปีก่อน | 6.85 | 6.58 | +0.27 |
| 1 | เหมือนมือใหม่ | 10.18 | 10.34 | -0.16 |
| 3 | สารวัตรใหญ่ | 14.71 | 14.87 | -0.16 |
| 3 | วัดหูโจร | 16.32 | 16.11 | +0.21 |
| 3 | สักคน | 19.29 | 19.11 | +0.18 |
| 5 | จับโจรเก่า | 26.0 | 26.25 | -0.25 |
| 6 | วัดสิบเอ็ดจุด | 28.93 | 29.16 | -0.23 |
| 6 | หัว | 30.14 | 29.92 | +0.22 |
| 6 | จดลงการ์ด | 31.44 | 32.22 | -0.78 |
| 6 | แล้วเก็บเข้า | 32.21 | 32.88 | -0.67 |
| 7 | ไม่เจอซ้ำสักคน | 35.6 | 35.81 | -0.21 |
| 7 | สารวัตรตะโกน | 36.57 | 36.87 | -0.30 |
| 7 | เหลืออีก | 37.48 | 37.67 | -0.19 |
| 8 | สุดท้าย | 40.24 | 40.07 | +0.17 |
| 8 | เข้ามา | 41.99 | 41.79 | +0.20 |
| 9 | นิ้วขนาดนี้ | 46.78 | 47.02 | -0.24 |
| 9 | เหลือกล่อง | 47.58 | 47.84 | -0.26 |
| 9 | เหลือการ์ดใบ | 49.2 | 49.58 | -0.38 |
| 9 | ตัวเลขตรงกัน | 50.41 | 50.58 | -0.17 |
| 9 | นั้นเขียนว่า | 52.52 | 52.3 | +0.22 |
| 9 | มาร์แตง | 53.36 | 53.2 | +0.16 |
| 9 | เดือนก่อน | 54.52 | 54.2 | +0.32 |
| 9 | ข้อหาขโมยขวด | 55.14 | 54.86 | +0.28 |
| 10 | แต่กระดูก | 57.88 | 58.21 | -0.33 |
| 10 | ผู้ใหญ่ไม่ | 58.5 | 58.69 | -0.19 |
| 11 | ที่มานั่งให้ | 62.64 | 62.88 | -0.24 |
| 11 | ก็คือสารวัตร | 63.78 | 64.02 | -0.24 |
| 11 | ที่ต้องนั่ง | 64.91 | 65.12 | -0.21 |
| 11 | วัดหู | 66.77 | 66.54 | +0.23 |

Worst cases, confirmed independently by narration energy envelope: sentence 6 (count) captions "จดลงการ์ด" at 31.44 s and "แล้วเก็บเข้า" at 32.21 s, but the voice says them at 32.22 s and 32.88 s (there is a speech gap at 32.14-32.20 s). Sentence 0 (hook) captions run 0.2-0.56 s late from "ไปวัดหูโจร" onward. Sentence 9 (reveal) captions run 0.2-0.4 s late then early. Pattern: caption times look like a uniform/proportional split within each sentence rather than the actual delivery, so errors are zero at sentence start and wander mid-sentence.

Fix: rebuild captions.json phrase times from STT char/word timings on narration.wav (stt.json words, available in the scratchpad aud dir), keep first-phrase times, then re-burn ear_v1.ass. Audio mix itself needs no change.
