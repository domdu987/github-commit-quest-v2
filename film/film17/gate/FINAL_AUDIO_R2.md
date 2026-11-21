# FINAL AUDIO gate R2, film 17 (final2/ear_v1.mp4, 68.4 s)

## VERDICT: PASS

| check | result | threshold | status |
|--|--|--|--|
| Caption start vs spoken onset (102 captions, same char-level STT method, film = narration + 0.10) | 0 outside +-0.15 s; max abs offset 0.05 s; mean +0.045 s (sd 0.018) | within +-0.15 | PASS |
| Caption text vs script_th.txt | all 12 sentences EXACT (1.000); captions.json = 102 = ASS Dialogue lines, 0 time/text mismatches | exact | PASS |
| Integrated loudness | -12.2 LUFS (LRA 1.9 LU) | -14..-11 | PASS |
| True peak | -1.5 dBTP | <= -1 | PASS |
| STT spot-check on new mp4 (sentences 0, 6, 9) | vs clean narration 1.000 / 1.000 / 1.000; vs script 1.000 / 1.000 / 0.991 | >= 0.93 | PASS |
| Sting placement and level | see below | under "มาร์แตง", below voice | PASS |

## Notes
- Previous result: 34/102 outside, max 0.78 s. Now 0/102, max 0.05 s. Captions run uniformly about 0.045 s after the spoken onset, which is well inside tolerance.
- Sentence-first captions vs timing.json sentence_start: max +0.20 s (sentence 3), but these are measured against the sentence boundary, not the spoken onset (STT places the first word later), so this does not count against the criterion.
- Voice mix unchanged: sample-level difference vs the previous mp4 is digital silence (-240 dBFS) for 0-53 s, -29 dBFS during 53-56 s (the moved sting), and -49 dBFS for 56-68 s (limiter interaction with the sting tail). Previous full 12-sentence STT therefore still stands (min mix-vs-clean 0.995).
- Sting: mix spec has sting.mp3 at 53.35 s film (= 53.25 narration), peak -16 dBFS, 2.2 s, fade 0.4 s. STT onset of "มาร์แตง" is 53.20 s narration = 53.30 s film, so the sting lands 0.05 s after the word onset and plays under the word. Level unchanged from the previous gate: SFX RMS about -30.5 dBFS vs voice RMS about -14.2 dBFS, 16.3 dB below voice RMS; peak -16 vs voice peak about -1 (15 dB below). Not louder than the voice.
- Listen-proxy only; no human listening done.
