# Music pick, film22

**Pick: m2** (1930s jazz-age orchestral comedy; muted trumpet, clarinet, walking bass, celesta).
**Runner-up: m3.** Rejected m1 (flat, never calms).

Copied to `audio/music_pick.mp3`; preview mix `audio/music_pick_preview.mp3` (narration at +0.10 s, music RMS -31 dBFS, fade 60.5-63.0 s).

| | m1 | m2 | m3 |
|---|---|---|---|
| Vocals (fal STT) | none ("[on-hold music]", 0 words) | NOT RUN (fal balance exhausted) | NOT RUN (same) |
| Integrated LUFS | -15.5 | -16.6 | -16.0 |
| LRA (LU) | 3.7 | 11.0 | 6.4 |
| RMS 0-40 s (dB) | -16.8 | -20.6 | -17.5 |
| RMS 40-58 s (dB) | -15.8 | -17.4 | -15.1 |
| Lift 40+ vs before | +1.0 | +3.2 (peaks -13 to -14 at 58-62 s) | +2.4 |
| Centroid 0-40 / 40-60 s (Hz) | ~900 / ~1550 | ~650 / ~1300-2000 | ~870 / ~1300 |
| Energy >4 kHz | 0.14% | 0.17% | 0.12% |
| Transients (flux 0-40 s, lower = softer) | 83 | 53 | 72 |
| Ending | music runs to ~66 s, hard cut at 68 s | same, ~66 s | same, ~66 s; dips to -31/-27 dB at 58.5-60 s |

No take has harsh highs (centroid under 2 kHz everywhere, under 0.2% energy above 4 kHz) or strong drums. m2 is the softest and has the clearest calm-then-lift shape. m2 is bass-heavy (46% of energy under 150 Hz, walking bass), so high-pass the music at about 80-100 Hz under the voice.

## Conform notes
- Level: gain -12.7 dB on the 0-63 s window of m2 gives music RMS -31 dBFS (voice -14.4 dBFS).
- Fade: start 60.5 s, end 63.0 s (2.5 s), music trimmed to 63 s. All takes' natural ending is ~66 s, so the fade lands mid-phrase; that is expected and masked by the fade. The final sentence runs to 62.75 s, so keep the fade as is.
- Calm 0-40 s needs no duck: m2 sits around -20 to -25 dB raw. Mocking-quote beats (19.3-27.4 s and 36.2-39.9 s) are fine; optionally -1.5 dB on 26-28 s where a brighter phrase (centroid 1500 Hz) appears.
- Lift after 40 s is real (+3 dB, brighter). Let it push, but if the reveal and aha lines (43.4-58.4 s) feel masked, duck -1.5 to -2 dB over 43-58 s with 0.5 s ramps. Do not duck at the turn at 39.96 s; let the music open up there.
- Open item: vocals check on m2 and m3 was not completed (fal returned "Exhausted balance"). m2's prompt asked for no vocals and its spectrum shows no sibilance bursts, but re-run STT on m2.json audio url after a top-up before locking.
