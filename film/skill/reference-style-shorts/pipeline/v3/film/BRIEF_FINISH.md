# Brief for the finishing workers (conform, sound, review)

> **Example from film 1, not a template.** For a new film copy it and rewrite: the input paths, the dated voice section, the expected take list and the film length. The levels and rules are generic. See "Adapting to a new film" in references/production.md of the skill.

PROJ = __PROJ__

The film is 1965 frames (g 0..1964), 30 fps, 720x1280, Thai narration and Thai captions. Read PROJ/v3/film/CONVENTIONS.md and PROJ/plan/shot_plan.md (shot table, transitions, build-order step 12 "Conform") first.

## Inputs
- Takes: PROJ/v3/film/sNN/ (frames/g_%04d.png with handles, meta.json, cues.json). Expected takes: s04 s05 s06 s07 s08 s09 s10 s11 s12 s13 s14 s15 s16 s17 s18 s19 s20 s21 s22 s23 s24 s25 s26.
- The hook (shots 1-3) is not in that layout: its finished picture frames without captions are PROJ/v3/out/frames/f_%04d.png, where f_0001 is film frame g 0 (150 frames, g 0..149); its cue list is PROJ/v3/out/sfx_cues.json. The plan says which of its frames are film frames and which lie under the dissolve into shot 4.
- Narration: PROJ/audio/th/full_v2/narration.wav laid at +0.100 s. Caption phrases and times: PROJ/audio/th/full_v2/narration_timing.json (104 phrases; add 0.100 s). Caption style: Thai, Kanit Black, the libass override {\fnKanit Black\fs88} in front of each phrase, centred at x 360, y 900, hard swaps, burned LAST with PROJ/assemble.py (see how PROJ/v3/shots/finish.py does it for the hook).
- Music: PROJ/audio/music/music_fit.wav (the client's track, already fitted to 65.9 s). Sound effects library: PROJ/audio/sfx/*.wav with manifest.json (20 sounds; label_slap is nearly silent, do not use it). Mixer: PROJ/audio/mixer.py (spec format in its docstring; PROJ/v3/out/mix_opening.json is the approved mix of the hook: reuse its entries and levels for the first 5 seconds). Voice gain: PROJ/audio/music/mix_settings.json ("voice_gain").

## The voice was re-recorded (18 Nov 14:54): the new voice, same clock
The narration PROJ/audio/th/full_v2/narration.wav is now the new voice, fitted sentence by sentence to the clock of the first recording: every sentence starts where it did, the file has the same length, the same loudness. The caption phrase times in narration_timing.json were recomputed from the new voice (they moved by 0.05 s on average, 0.24 s at most), so always read the times from that file, never from an older copy or from a take.
The ONLY voice in the film mix is that file. From PROJ/v3/out/mix_opening.json reuse the effect entries and their levels only, never its voice entry. The old voice is kept in PROJ/audio/th/full_v2_oldvoice/ and must not be used.

## Levels measured on the reference (dBFS)
Voice about -17.4 RMS. Music bed -38 RMS, from the first frame to the end. Effects in the gaps between words every 2.5 to 3 seconds: whooshes peaking -19 to -10, impacts about -9, scratches and rubs -27 to -24 RMS, ambiences (rain, wind, room tone) -34 to -30 RMS. Effects never mask a word: keep peaks at or under -10 while the voice speaks.

## Rules
Write only where your task says. No network, no paid APIs, no MCP or connector tools. To look at an image use the Read tool (downscale to at most 1600 px). Your final message is consumed by a script: return the structured result only, with absolute paths.
