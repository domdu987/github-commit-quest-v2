# Film 15 music pick (provisional winner: C)

Nobody on the team can hear audio. Everything below is a measurement, not a listening judgement. A human ear check is still needed.

STT masking test NOT RUN: fal returned "User is locked. Reason: Exhausted balance." partway through the first (clean narration) pass. The clean-narration sentences that did return scored s1 1.00, s3 0.99, s4 1.00, s5 1.00, s8 0.987, s9 1.00; every other call, and all mix calls, returned the billing error. All-zero scores in the run were API errors, not real scores. Voice masking (rank criterion 1) is therefore unmeasured. Re-run after topping up fal at https://fal.ai/dashboard/billing. Each mix is film/release15/film15_v4_{A,B,C}.mp4 and per-sentence cuts use timing.json + 0.10 s.

## Conform (all three)
music_used true, 2095 frames, 0 placeholder ranges, 0 handle-fallback frames, 55 dissolve blends, pass true. All candidates are longer than the film (A 88 s, B 74 s, C 92 s); conform's mixer truncates the file to the film length and applies a 0.3 s fade in and 0.6 s fade out. It never loops. Note: the work dir /tmp/conform15_work/film15_v3 did not exist, so conform decoded the take frames itself on the first run (--keep used so B and C reused them).

## Table
| | A (jazz) | B (marching band) | C (pizzicato) |
|---|---|---|---|
| length | 88 s | 74 s | 92 s |
| LUFS / TP (final mp4) | -12.2 / -2.4 | -12.2 / -2.4 | -12.2 / -2.2 |
| LUFS/TP in range (-14..-11, <= -1) | yes | yes | yes |
| STT min sentence vs clean | not run | not run | not run |
| music vs voice during speech (target -15..-17) | -16.4 | -16.3 (avg) | -16.2 |
| music vs voice by beat: hook / mock / fail / hush / reveal / triumph / ending | -16.3 / -16.1 / -16.1 / -16.3 / -16.5 / -16.6 / -17.3 | -23.1 / -18.5 / -17.8 / -14.4 / -14.2 / -14.4 / -13.0 | -15.7 / -15.7 / -15.3 / -16.1 / -15.4 / -17.2 / -26.0 |

Level is relative to voice RMS during speech (-11.5 dB in the pre-normalisation mix), music-only render with the conform gain.

## Beat fit, raw candidate (RMS dB vs whole-file RMS / spectral centroid Hz)
| beat | A | B | C |
|---|---|---|---|
| hook 0-6 | +0.5 / 2159 | -6.6 / 1100 | +1.0 / 650 |
| mocking 16-24 | +0.4 / 2251 | -1.9 / 2581 | +0.8 / 2242 |
| failed 35-42 | +0.5 / 2231 | -1.3 / 2435 | +1.3 / 2120 |
| hush 42.4-44.4 (want quiet) | +0.2 / 2504 | +2.2 / 1253 | +0.4 / 3154 |
| reveal 44.5-55 | 0.0 / 2351 | +2.3 / 1796 | +1.1 / 1754 |
| triumph 55-60 (want louder/brighter) | -0.1 / 2256 | +2.1 / 1657 | -0.7 / 2227 |
| comic end 60-69.8 | -0.6 / 2051 | +3.6 / 2800 | -9.3 / 2654 |

None of the tracks follows the prompted dynamics: no candidate gets quieter in the hush and none gets clearly louder in the triumph. A and C are flat (within about 1.5 dB); B has a quiet hook and a loud rest, so the hush is the loudest part. C is slightly brighter in the triumph than in the reveal (2227 vs 1754 Hz).

## Ends and transients
- A: 1 s dip of -11 dB at about 63 s; loud transient (+13 dB over file RMS) at 68.67 s, inside the last sentence, about 1.2 s before the hard cut at 69.84 s.
- B: cuts to near-silence at about 70 s, so it ends cleanly at the film end; but a +19 dB hit at 69.21 s lands in the last word, and its level sits 13-14 dB under the voice from the hush on (too loud for the 15-17 target).
- C: a near-silent second at about 61 s right after the triumph; the comic ending is -9 dB (about -26 dB under voice in the mix), so the bed nearly drops out; no hard transient near the cut (+5.7 dB peak at 69.42 s).
- None loops or ends early (all >= 74 s).

## Choice: C (provisional, pending the STT run)
Ranking used: STT (unmeasured, so a tie), then LUFS/TP (all pass, equal), then beat fit, then defects.
- B is out: its level swings from -23 to -13 dB under the voice (the hush and reveal are loudest, the opposite of the story) and it has a loud hit in the last word.
- A vs C: both sit about 16 dB under the voice and are flat across the beats. C is brighter at the triumph, has no loud transient near the hard cut, and has a lower peak than A. A has a +13 dB hit in the last sentence and a dip at 63 s. C's weakness is the quiet comic ending and the gap at 61 s.
- Runner-up: A. Swap if the ear check dislikes C's quiet ending. The STT run is the deciding test either way: any sentence below 0.93, or more than 0.02 below the clean narration, is a veto.
- music_suno.wav is set to C.wav.
