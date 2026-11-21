# Phase 3: sound first

Cut the picture to the finished narration. Everything here was measured against the references; levels are in dBFS RMS unless stated.

## Narration

Tools: `pipeline/audio/th/tts_fal.py` (speech with character timestamps and caption alignment) and `pipeline/audio/build_narration.py` (the whole narration from a new script):

```
python3 pipeline/audio/build_narration.py <script.json> <voice_id> <out_dir> --dry-run            # groups and characters (= what you pay for)
python3 pipeline/audio/build_narration.py <script.json> <voice_id> <out_dir> --speed 1.2 --target-s <length the user asked, e.g. 60>
```

**What film 1 used (for a cost estimate before you ask the user).** Narration: 21 sentences, 1,057 characters with spaces (971 without), recorded in 9 paragraph chunks, each checked once by speech-to-text; a 60 s Thai script is about the same size. The re-voicing with a second voice: about 1,400 characters of speech in 13 takes plus 13 speech-to-text checks. Voice samples for the choice: one opening line (about 75 characters) per voice. Sound effects: 20 clips, 45.4 s asked in all (`audio/sfx/manifest.json`). The project did not record the provider's prices: read the current price per 1,000 characters (speech), per minute (speech-to-text) and per second (effects) on the provider's pricing page or the account usage before you quote a cost, and multiply by these counts; `--dry-run` prints the exact characters of a new script.

The script file has the format of `pipeline/script_th_v2/script_th.json` (sentences with `beat`, `tts`, `captions`; `caption_number_readings` for the speech-to-text check). It writes `narration.wav`, `narration.chars.json` and `narration_timing.json`, which the shots, `assemble.py` and the mix read. Use `PROJ/audio/th/full_v2` as `<out_dir>`: the re-voicing script (`build_narration_fit.py`) and film 1's briefs read the clock from there. It needs no earlier recording; chunks are cached, so a re-run after a failure pays only for the missing chunks. Tested offline on film 1's cached chunks: 65.41 s for a 65.4 s target, 104 caption phrases aligned at 0.98. `audio/th/build_narration_v2.py` is film 1's own driver (it also reused the opening chunk and tempo of an earlier build from `audio/th/full/`, which is not bundled): read it as the example, do not run it on a new film.

1. Offer the user two or three voice samples of the opening line and let them choose by ear. Speech through fal.ai: `fal-ai/elevenlabs/tts/eleven-v3` with `voice` (a voice id works, including native voices of the target language), `language_code`, `speed`, `timestamps: true`. The answer carries character start and end times.
2. Generate in paragraph chunks of two to four sentences, not the whole script (one 1,000 character request failed with HTTP 502) and not sentence by sentence (delivery varies between calls).
3. Verify every chunk by transcribing it back (`fal-ai/elevenlabs/speech-to-text`) and comparing with the script; regenerate a chunk that mishears a word. Spelled-out numbers come back as digits, so normalise before comparing.
4. Tighten: trim head and tail, shorten silences over about 0.14 s to 0.10 s, match loudness between chunks, join with 0.16 to 0.20 s gaps. The references have no gap longer than 0.3 s.
5. Fit the length with `atempo` (pitch stays). Keep the opening line's take and tempo fixed once the opening is animated, and give the rest its own tempo if needed.
6. Caption timing: map each caption phrase to the timestamp of its first character; hold each phrase until the next begins.

Tell the user the speed-up you applied and offer the natural-speed version; you cannot hear whether it sounds rushed.

For the opening (`pipeline/v3/shots/timing.py`), cut the first sentence's phrases out of `narration_timing.json` into a timing file of the format of `pipeline/audio/th/hook_timing.json` (documented in `pipeline/v3/README.md`) and tag each phrase with the beat (shot) it belongs to.

### Changing the voice after the picture exists

`pipeline/audio/th/build_narration_fit.py <voice_id> <voice_name> <out_dir> [speed]` (film 1's sentence groups `GROUPS` and number readings `NUM` are written into the file: edit both for a new script) records a new voice in the same paragraph chunks, checks each chunk with speech-to-text, tightens the silences, then time-stretches every sentence into the slot the same sentence has in the old narration. Sentence starts and total length stay the same, so every rendered frame stays valid; caption phrase times are recomputed (0.05 s average shift, 0.24 s at most). Only mouths that follow the narration loudness must be rendered again. Keep the old voice in a backup folder (the script reads its clock from `audio/th/full_v2_oldvoice/` when that folder exists) so the change can be reverted. Details: `references/production.md`.

## Captions

Burn captions last with `pipeline/assemble.py` (libass). English: Work Sans Black, white, 4 px black stroke, centred at x 360, y 900 on a 720x1280 frame, no animation; libass sizes run small, so use the override `{\fnWork Sans Black\fs58}`: 36 px text height by score.py, the reference's 36-37 (measured: fs50 32, fs70 44 px; `film_mini.py captions --style en`). Thai: Kanit Black with `{\fnKanit Black\fs88}`; check tone-mark stacking on a rendered frame and keep about 80 px of height clear. At that size the scoring tool reads 45 px of text height against 36 to 37 px for the reference's Latin captions: Thai at the reference's point size looks about 25 % taller because of the marks above and below. Show two sizes on the opening and let the user choose. Full fonts with Thai and Latin glyphs come from the npm packages `@expo-google-fonts/<family>`; the `@fontsource` packages only ship per-script subsets.

## Music

Measure the reference bed first (see analysis.md). The first references: no drums, no clear beat, steady level, mid and low spectrum, about 20 dB under the voice.

If the user makes the music (for example with Suno), give them a style line and the settings:
- Instrumental on, lyrics empty.
- Put positives in the style box ("light whimsical documentary underscore, soft pizzicato strings, marimba, very sparse, calm, curious, steady, minimal, background music, 80 bpm") and negatives in the exclude box ("drums, percussion, vocals, choir, electric guitar, bass drop, loud"); words after "no" in the style box tend to be added, not removed.
- Lower weirdness, raise style influence.

No track yet, or the user makes no music: send the opening without a bed and say so in the message ("no music yet: the bed goes in when your track arrives"), or use a track the user names. No music-generation endpoint was tested in this pipeline, so do not promise one; if the user wants you to generate music, test the endpoint they have access to on a 10 s sample first and measure it like the reference bed. The mix spec takes the bed as one optional input, so adding it later changes nothing else.

When the track arrives: check it has no drums or vocals by separating stems, find the tempo, and if it is shorter than the film extend it with one beat-aligned loop at the pair of points whose following bars match best, then stretch a few percent so its own ending lands on the last word. Offer the user two levels to choose by ear: the measured one (about -38) and 6 dB louder.

## Sound effects

The skill ships no sound files (no narration, music or effect WAVs): a new film builds its own library. Build it through fal.ai (`fal-ai/elevenlabs/sound-effects/v2`: `text`, `duration_seconds`, `prompt_influence`; paid) with `pipeline/audio/sfx/make_sfx.py`, and measure each result: some come back nearly silent and must be regenerated or replaced. Shot workers export a cue list (time, duration, label) for every visible action and camera snap; place effects from that list.

## The mix

Captions are burned before the mix: `pipeline/assemble.py <frames> <out.mp4> <captions.json> 30`. Always pass 30 (the film's rate). `assemble.py` reads `f_%04d.png`, while the conform and the grade write `g_%04d.png`: burn through a folder of links named `f_%04d` (film 1 used `f_0001` -> `g_0000` and so on); `pipeline/examples/film_mini.py` writes `f_` frames itself.

`pipeline/audio/mixer.py <spec.json>`: voice with a gain that brings it to about -17.4, music by target RMS, each effect by target peak or RMS, optional alignment of the effect's onset to the cue, a limiter, then mux into the video without re-encoding the picture. Levels that matched the references: voice -17.4; bed -38; whooshes peaking -19 to -10; after the opening every point effect capped at -11 peak (only the opening's jab thump peaked at -9, which under a word breaks the rule below); scratches and rubs at -27 to -24 RMS. Ambiences (rain, wind, room tone) -34 to -30 RMS with their peaks limited to about -14; a bed at -41 was inaudible in the first film. Effects never mask a word: nothing but the voice over -10 peak while the voice speaks, measured on effects plus music together (film 1's gust at 48.1 s and wall boom at 43.3 s passed with the effects alone and reached -9.5 and -9.8 dBFS with the music). Measure the finished mix: the first film's voice came out 1 dB hot and was corrected in the polish pass. `pipeline/v3/film/out/sound/build.py`, `measure.py` and `out_v11/sound/build_v11.py` are film 1's scripts with its paths and cue list written in: read them as examples; for a new film use `pipeline/examples/film_mini.py mix` and the mix-check recipe in `references/bible/captions-sound.md` 4.4. Limit after summing in floating point; clipping the sum first distorts the voice.

## Learning a fal.ai endpoint without docs or spending

Send a request with wrong types for the fields you suspect (`{"text": 5, "voice": 5, "timestamps": "x"}`). The 422 validation answer lists every real field, its type and allowed values, and costs nothing. Audio input can be sent as a base64 data URI in `audio_url`. Result files come from `v3.fal.media` or `v3b.fal.media`.
