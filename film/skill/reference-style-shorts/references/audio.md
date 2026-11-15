# Phase 3: sound first

Cut the picture to the finished narration. Everything here was measured against the references; levels are in dBFS RMS unless stated.

## Narration

Tools: `pipeline/audio/th/tts_fal.py` (speech with character timestamps and caption alignment) and `build_narration_v2.py` (the whole narration).

1. Offer the user two or three voice samples of the opening line and let them choose by ear. Speech through fal.ai: `fal-ai/elevenlabs/tts/eleven-v3` with `voice` (a voice id works, including native voices of the target language), `language_code`, `speed`, `timestamps: true`. The answer carries character start and end times.
2. Generate in paragraph chunks of two to four sentences, not the whole script (one 1,000 character request failed with HTTP 502) and not sentence by sentence (delivery varies between calls).
3. Verify every chunk by transcribing it back (`fal-ai/elevenlabs/speech-to-text`) and comparing with the script; regenerate a chunk that mishears a word. Spelled-out numbers come back as digits, so normalise before comparing.
4. Tighten: trim head and tail, shorten silences over about 0.14 s to 0.10 s, match loudness between chunks, join with 0.16 to 0.20 s gaps. The references have no gap longer than 0.3 s.
5. Fit the length with `atempo` (pitch stays). Keep the opening line's take and tempo fixed once the opening is animated, and give the rest its own tempo if needed.
6. Caption timing: map each caption phrase to the timestamp of its first character; hold each phrase until the next begins.

Tell the user the speed-up you applied and offer the natural-speed version; you cannot hear whether it sounds rushed.

## Captions

Burn captions last with `pipeline/assemble.py` (libass). English: Work Sans Black, white, 4 px black stroke, centred at x 360, y 900 on a 720x1280 frame, no animation; libass sizes run small, so use the override `{\fs70}` to get a 34 to 36 px cap height. Thai: Kanit Black with `{\fnKanit Black\fs88}`; check tone-mark stacking on a rendered frame and keep about 80 px of height clear. Full fonts with Thai and Latin glyphs come from the npm packages `@expo-google-fonts/<family>`; the `@fontsource` packages only ship per-script subsets.

## Music

Measure the reference bed first (see analysis.md). The first references: no drums, no clear beat, steady level, mid and low spectrum, about 20 dB under the voice.

If the user makes the music (for example with Suno), give them a style line and the settings:
- Instrumental on, lyrics empty.
- Put positives in the style box ("light whimsical documentary underscore, soft pizzicato strings, marimba, very sparse, calm, curious, steady, minimal, background music, 80 bpm") and negatives in the exclude box ("drums, percussion, vocals, choir, electric guitar, bass drop, loud"); words after "no" in the style box tend to be added, not removed.
- Lower weirdness, raise style influence.

When the track arrives: check it has no drums or vocals by separating stems, find the tempo, and if it is shorter than the film extend it with one beat-aligned loop at the pair of points whose following bars match best, then stretch a few percent so its own ending lands on the last word. Offer the user two levels to choose by ear: the measured one (about -38) and 6 dB louder.

## Sound effects

Build a small library through fal.ai (`fal-ai/elevenlabs/sound-effects/v2`: `text`, `duration_seconds`, `prompt_influence`) with `pipeline/audio/sfx/make_sfx.py`, and measure each result: some come back nearly silent and must be regenerated or replaced. Shot workers export a cue list (time, duration, label) for every visible action and camera snap; place effects from that list.

## The mix

`pipeline/audio/mixer.py <spec.json>`: voice with a gain that brings it to about -17.4, music by target RMS, each effect by target peak or RMS, optional alignment of the effect's onset to the cue, a limiter, then mux into the video without re-encoding the picture. Levels that matched the references: voice -17.4; bed -38; whooshes peaking -19 to -10; impacts peaking about -9; scratches and rubs at -27 to -24 RMS. Limit after summing in floating point; clipping the sum first distorts the voice.

## Learning a fal.ai endpoint without docs or spending

Send a request with wrong types for the fields you suspect (`{"text": 5, "voice": 5, "timestamps": "x"}`). The 422 validation answer lists every real field, its type and allowed values, and costs nothing. Audio input can be sent as a base64 data URI in `audio_url`. Result files come from `v3.fal.media` or `v3b.fal.media`.
