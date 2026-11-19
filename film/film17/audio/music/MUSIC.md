# Film 17 music (client decision 2026-11-19: generate with fal ElevenLabs music, instrumental, QA team picks)
Endpoint fal-ai/elevenlabs/music, force_instrumental true, 74 s, 3 candidates (prompts in gen_music.py).
| cand | vocals (STT) | RMS per 2 s (dB) | problem |
|---|---|---|---|
| m1 | none ("[on-hold music]") | -18..-15, then a 10 s near-silence at 52-64 s | gap lands on the reveal/aha/ending (44.6-62 s): music drops out at the payoff |
| m2 | none | -17..-13 steady for 72 s, ends at 72 s | none; steady bed, ducks cleanly under voice |
| m3 | none | 12 s near-silence at 40-54 s | gap covers crisis + reveal |
**Pick: m2** -> audio/music.mp3 (mix at -31 dB RMS under voice -14.4 dB per client rule). Ear checks (fit, mood) left to the client; can be swapped later.
