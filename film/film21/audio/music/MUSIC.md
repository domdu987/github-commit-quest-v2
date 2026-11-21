# Film 21 music QA (Stirling Bridge)

Pick: **m1**. Measured with ffmpeg/numpy (RMS, spectral flux, onset density) plus a read of the three spectrograms. Ear checks are left to the client.

Timings are against the 67 s files. Narration runs to ~62 s with a hard cut there, so everything after 62 s is irrelevant, and the 64-66 s tails are fine on all three takes.

## m1 (playful chanter/fiddle/whistle, 112 bpm, jig finale)

| Check | Result |
|---|---|
| Vocals | None. STT only returned "[outro jingle]"; the prompt says instrumental. |
| RMS profile | -20 to -17 dB over 0-16 s, a gradual rise from 16-24 s, then a flat plateau at -12 to -13 dB from ~24 s to 64 s, then a tail. |
| 41-62 s | No dropout. Minimum 0.5 s RMS -19.1, max -13.8, std 1.4 dB. Flux is flat (144 over 41-50 s, 145 over 50-62 s). Onset density 4.0/s. |
| Problems | The intro is thin and quieter, with a texture change at ~17 s (mid set-up, harmless under narration). No hush at the 29-34 s suspense count, since the bed is already at full level. The whole bed runs ~7 dB hotter than the intro, so check the -31 dB mix level against narration at the plateau. |

## m2 (Celtic folk, pizzicato/tremolo, 108 bpm, reel ending)

| Check | Result |
|---|---|
| Vocals | None. STT returned "[outro jingle]". |
| RMS profile | Pulses of -20 to -24 dB over 0-16 s. A 2 s alternation (-20, -15, -20, -15...) from ~22-34 s, then -14 to -17 dB from ~36 s onward. |
| 41-62 s | No dropout, but 0.5 s RMS ranges -22.0 to -14.4 dB (std 1.9), the least steady of the three. Highest flux (154) and onset density 3.8/s. |
| Problems | The tiptoe pulsing and tremolo is not a clean, steady bed, and it wobbles under narration. There is a visible texture step at ~17 s and another at ~34 s. Fades out earliest (-40 dB at 64 s). |

## m3 (recorder/lute, woodblock steps, 115 bpm, crescendo, pause, reel)

| Check | Result |
|---|---|
| Vocals | None. STT returned "[on-hold music]". |
| RMS profile | -20 to -22 dB over 0-26 s, a gap to -32 dB at 26-28 s, then -14 to -16 dB from ~28 s, ending at -13 to -14 dB. |
| 41-62 s | Steady apart from slow swells: min 0.5 s RMS -20.2, max -15.0, std 1.3. Highest flux (177) and a busy, dense reel. |
| Problems | The deliberate "brief pause" is a ~2 s hole at ~26-28 s (-32 dB), a dropout in the middle of the narration. The reel then starts at ~28 s, before the suspense count (29-34 s) rather than at the reveal at 41 s. The payoff is not marked, because the loud reel has already run for ~13 s. It is the busiest and brightest take, so it competes most with narration. |

## Pick: m1, with m3 as the fallback

- It is the only take with no pulsing and no dropout anywhere in 24-64 s.
- It has the flattest, steadiest level through 41-62 s (std 1.4 dB, flux flat before and after the 50 s aha).
- Its instrumentation fits the comic Scottish mood, and the jig covers the splash finale.
- m2 pulses, and m3 has a ~2 s hole at ~26-28 s and a reel that starts too early. Neither marks the payoff either.

## Not verified

The ear checks are left to the client. Nothing here was listened to. These are still to be confirmed by ear:
- mood and instrument taste
- melodic clashes with the Thai narration
- whether the 17 s texture change is audible under the voice
- final -31 dB level against the narration

## 2026-11-21: CLIENT'S OWN MUSIC replaces m1
The client made "The Sneaky Jig" on Suno (74.0 s, 48 kHz stereo), pushed by the producer at 23b0159 (film/suno/film21_the_sneaky_jig.mp3).
It is now audio/music.mp3; the old pick m1 is kept as music/m1_fal_previous.mp3. It is mixed the same way (music bed at -31 dB RMS under the
narration, ducked under the voice, 0.3 s fade-in), trimmed at the film's hard cut (61.6 s) with the 0.6 s fade-out.
