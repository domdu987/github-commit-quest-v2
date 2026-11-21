# AUDIO FINAL gate, film 19 v3 (film-13 rules, QA_TEAM_film13 §D.2)

Final mix: release19/harrison_v3.mp4 (built with hall_laugh lowered 4 dB, -18 -> -22, because it sat on sentence 3).

| check | result | rule |
|---|---|---|
| integrated loudness | -12.2 LUFS | -14..-11 PASS |
| true peak | -1.10 dBTP | <= -1.0 PASS |
| caption text vs script | 10/10 sentences identical | == script PASS |
| caption sync | max 0.032 s from the spoken sentence start | +-0.15 s PASS |
| overlapping captions | 0 | PASS |
| per-sentence STT, final mix vs clean narration | min 0.950 | >= 0.93 every sentence PASS |

STT method (film19/qa_tools/stt_med.py): faster-whisper large-v3-turbo on numpy audio, each sentence cut from the clean narration and from the mix (+0.10 s picture offset) with three window paddings 0 / 0.1 / 0.2 s; the score is the MEDIAN of the three (not the best). A single unpadded window clips the first consonant and swings the ratio by +-0.05 (e.g. sentence 7: 0.878 / 0.976 / 0.951); a whole-film transcript hallucinated on the clean narration too and was rejected.

| sentence | t (s) | ratios pad 0 / 0.1 / 0.2 | median |
|---|---|---|---|
| 0 | 0.00-6.32 | 0.99 / 0.99 / 0.975 | 0.99 |
| 1 | 6.37-15.49 | 0.915 / 0.975 / 0.95 | 0.95 |
| 2 | 15.54-25.72 | 0.974 / 0.97 / 0.924 | 0.97 |
| 3 | 25.78-28.69 | 0.966 / 0.966 / 0.921 | 0.966 |
| 4 | 28.74-33.81 | 0.964 / 0.964 / 0.978 | 0.964 |
| 5 | 33.86-46.07 | 0.975 / 0.983 / 0.966 | 0.975 |
| 6 | 46.12-52.66 | 0.967 / 0.962 / 0.972 | 0.967 |
| 7 | 52.71-55.44 | 0.878 / 0.976 / 0.951 | 0.951 |
| 8 | 55.49-61.81 | 1.0 / 1.0 / 0.979 | 1.0 |
| 9 | 61.86-71.89 | 0.963 / 0.963 / 0.976 | 0.963 |
