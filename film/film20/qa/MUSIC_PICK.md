# Film 20 - music pick (QA-audio)

**PICK: C** (music_C.mp3). Method: numpy/ffmpeg measurement only (no listening). Windows = film time, music cut to 0-68.2 s. Scripts were in the scratchpad, takes untouched.

## Numbers

| Metric | A | B | C |
|---|---|---|---|
| Length | 73.2 s | 82.2 s | 73.2 s |
| Silent holes < -45 dB inside 0-68.2 s (excl. lead-in) | **38.07-41.03 s (3.0 s), plus 2 s fade-down either side** | 38.22-38.67 (0.45 s) with 36.5-40 s sag to -34..-49 dB | none (one 0.5 s frame -32 dB at 36.5 s) |
| Lead-in silence at 0 s | 0.53 s | none | 0.72 s |
| Level 0-68.2 s (RMS / peak / crest) | -17.4 / -1.3 / 16.1 dB | -18.1 / -2.1 / 16.0 | -19.2 / -2.1 / 17.2 |
| Section RMS dB: hook / pivot / boss / nick+count | -14.7* / -14.4 / -13.9 / -14.6 (analysis.txt; flat) | -16.5 / -15.5 / -15.4 / -14.9 (flat) | **-21.5 / -19.7 / -16.2 / -15.7 (rises ~6 dB = build)** |
| false / crisis (dip) / reveal / aha / ending | -20.0 / **-11.4 (loudest, opposite of dip)** / -14.0 / -14.2 / -13.7 | -16.5 / -14.4 (no dip) / -14.0 / -13.6 / -15.0 | -17.4 / **-18.5 (dip)** / -15.6 / **-14.0 (lift)** / -14.6 |
| Dip depth (crisis vs mean of false and reveal) | +5 dB louder (wrong) | ~0 dB | -2.0 dB (mild, right direction) |
| Spectral centroid, mean per section / max 0.5 s frame | 226-652 Hz / 2829 Hz at 39 s (hole edge) | 288-469 / 910 | 314-754 / 1120 |
| Frames with centroid > 3 kHz | 0 | 0 | 0 |
| Max 0.5 s crest (pk-rms) | 16.3 | 16.2 | 20.2 (pivot), else <= 19.4 |
| 1-4 kHz band crest, mean per section | 12.6-18.8 | 11.8-18.7 | 13.1-17.0 |
| Onsets/s (build 5.9-33) | 0.9-3.5 | 0.9-1.6 | 1.5-2.8 |
| Short-term pumping: sd of 0.5 s RMS, 10-33 s | 3.18 | 4.98 | **2.35** |
| Sd of 100 ms RMS, 5.9-33 s / 43.4-68 s | 4.96 / 3.55 | 6.82 / 3.97 | 6.89 / 4.88 |
| Frame-to-frame jumps > 6 dB (0.5 s), 0-68.2 | 25 | 37 | **12** |
| Narration/music ratio, per sentence, music at -31 dB RMS, narration as-is (active speech -17.3 dB): min / which | 10.6 (S7 40.8-43.4) | 12.4 (S9) | 11.7 (S9) |
| Same, narration re-levelled to -14.4 dB (+2.9 dB) | **13.5 (S7)**; S6 only passes because of the hole | 15.3 | 14.6 |
| 1-4 kHz band ratio, min per sentence (as-is -> +2.9) | 13.5 -> 16.4 | 11.6 -> 14.5 | 10.1 -> 13.0 (S9) |
| Worst 0.5 s window ratio, as-is | 4.2 dB (12.5 s) | 4.3 dB | 5.4 dB |
| Ending at 68.2 s | RMS -14.0, natural button at ~72.2 s lost | RMS -12.2, **mid-phrase, natural end at ~80.2 s** | RMS -14.5, button at ~72.2 s lost |
| Vocals | none (STT) | none | none |

\* A's first 0.5 s is digital silence; its hook figure from analysis.txt includes that. Note: narration file measures -17.7 dB whole / -17.3 dB active, not -14.4 dB; ratios are shown both ways. A 0.5 s window ratio below 14 dB happens on every take on loud beats (accordion/piano hits) and does not separate them.

## Why C

- **A: reject.** 3.0 s dead silence at 38.1-41.0 s (the whole 33.2-40.7 section averages 6 dB below the rest), then the music slams back in at -13 dB exactly when the tension dip (40.7-43.4) should be quiet: the crisis section is the loudest of the film (-11.4 dB), the reverse of the brief. Narration/music ratio there is the lowest (10.6 dB). It also has 25 jumps > 6 dB (vs 12 for C) and a centroid spike (2.8 kHz) at the hole edge. Cannot be patched with a duck.
- **B: second.** No silent hole (a 0.45 s gap at 38.2 s plus a 3 s sag 36.5-40 s is a drop-out of the bed, early by ~3 s relative to the dip at 40.7). Energy is flat across sections (-13.6 to -16.5 dB), so the hook/build/lift do not follow the story, and the crisis is not a dip. Most pumping of the three (sd 4.98 dB 10-33 s, 100 ms sd 7.0, a 25 dB jump at 16.0 s, 37 jumps > 6 dB). First 68.2 s are usable (no vocals, quiet spectrum) but it is cut mid-phrase at -12.2 dB, so it needs the full fade and never gets its ending. Best narration ratios though.
- **C: pick.** The only take whose levels follow the story: quiet hook (-21.5), monotonic build to -15.7 by 33 s, shallow dip at the crisis (-18.5), lift into the reveal (-15.6) and loudest at the aha (-14.0), playful ending steady (-14.6). Steadiest bed (sd 2.35 dB, fewest jumps), no holes, centroid never above 1.1 kHz (no harshness), narration ratio >= 14.6 dB per sentence at the -14.4 dB narration level.
- Caveats: the dip is only ~2-3 dB deep; the piano/accordion has the most 1-4 kHz energy in the last three sentences (S8-S10 band ratio 10-13 dB vs 14-17 elsewhere); max crest of 20.2 dB in the pivot.

## Conform instructions (for C)

1. Music at -31 dB RMS: gain -11.8 dB on the 0-68.2 s span (C is -19.2 dB there). Do not normalise on the full 73.2 s file.
2. Fade out: `afade=t=out:st=67.2:d=1.0` (ends at 68.2). The natural button at ~72.2 s is cut off, so do not rely on it. Narration ends at 67.9 s, so the fade runs under the last word only; if the last word gets masked, use st=66.9:d=1.3.
3. Lead-in: the take starts with 0.72 s of silence. Keep it (trimming would move every cue 0.7 s early and shift the dip off 40.7). Add `afade=t=in:st=0.7:d=0.3` only if a click is heard at the entry.
4. Speech-band relief for the ending: apply a broad `equalizer=f=2500:t=o:w=2:g=-3` to the music bus (or only 52-68 s), which lifts the 1-4 kHz ratio in S9-S10 from 10 dB to about 13 dB at the as-is narration level (above 16 dB at -14.4 dB narration).
5. Optional local duck: none required. If S9 (52.1-57.8 s, ratio 11.7 dB as-is) still masks, duck music a further -2 dB over 52.0-57.8 s with 150 ms ramps.
6. If the final narration is NOT re-levelled to -14.4 dB (stays at -17.3 dB active), duck music -3 dB over 52-68 s so all sentences keep >= 14 dB.

## Director: conform bed (applied)
`ffmpeg -i music_C.mp3 -t 68.2 -af "equalizer=f=2500:t=o:w=2:g=-3,afade=t=out:st=67.2:d=1.0" -ar 48000 -ac 2 music_C_mix.wav` (regenerable, not committed); conform20.py mixes it at MUSIC_DB -31 with the narration lifted from -17.3 to -14.4 (VOICE_DB/NARR_DB).
