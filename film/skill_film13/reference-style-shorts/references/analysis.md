# Phase 1: analysing the reference clips

The goal is a build specification made of numbers with a frame cited for each one. Everything later is checked against it, which is also what lets cheaper models do the building.

## Extract the evidence

```
ffprobe -v error -show_entries stream=codec_name,width,height,r_frame_rate,nb_frames -of default=nw=1 clip.mp4
ffmpeg -i clip.mp4 -vf fps=2 -q:v 2 ref/a/t%04d.jpg          # a full-resolution still every 0.5 s (rename to tSS.S.jpg)
ffmpeg -ss 12 -t 1.5 -i clip.mp4 burst/f_%03d.png            # consecutive frames: how things move, blink, cut
ffmpeg -i clip.mp4 -ac 2 -ar 44100 audio.wav
```

- Captions: OCR the burned-in captions at 8 fps (rapidocr works offline) to get the transcript and the caption style. Speech recognition through fal.ai (`fal-ai/elevenlabs/speech-to-text`) gives word times.
- Cuts: scene scores on the top 60 percent of the frame, because captions and soft transitions hide cuts from a whole-frame detector. Most transitions in the first references were 9 to 23 frame dissolves, not cuts.
- Look at a dozen stills at full size yourself before briefing anyone. Thumbnails hid that the characters were flat drawings.

## Measure through lenses

One analyst per lens, each returning observations, measurements with evidence frames, a reproduction recipe and a ranked list of differences from the current attempt. Then one synthesiser reconciles contradictions into a single spec, and two verifiers re-measure a sample and test every tool call the spec relies on. Template: `workflows/01_study_reference_look.js`.

| Lens | What to pin down |
|---|---|
| Character anatomy | proportions in head diameters, outline widths and colour, limbs, hats, costume construction, views used |
| Faces and expressions | eye and mouth vocabulary, feature positions, how a turn is drawn, blink and expression timing |
| Colour, light, post | palette by scene, lit against shade on the same surface, shadow hue and edge, bloom, grain, black point |
| Environments | 3D or painted, outline use, texture, prop density, where the light sits in the frame |
| Camera and edit | shot count and length, interval between framing changes, move types and easing, transitions, lens, camera heights, staging in depth |
| Captions | font match, size, stroke, position, words per caption, animation or none |
| Sound | narration pacing and gaps, music bed level and character, effect count and level |
| Production forensics | conventional render, 2D rig or generated video; test it, do not assume |

Lessons from the first production:
- Give analysts the current attempt to compare against; "differences ranked by visual impact" was the most useful field.
- Analysts disagree (22 contradictions were reconciled). Keep the synthesis and the verification steps; do not hand single-lens specs straight to builders.
- Forensics matters: early guesses went back and forth between "3D", "AI video" and "2D". Evidence settled it: typeset text with correct real data that never changes between frames, and sub-pixel rigid geometry under a moving camera, mean a conventional 3D render.
- Add the sound lens from the start. In the first production it was forgotten until the user asked about music.

## Sound analysis without ears

You cannot listen, but you can measure:
- Word times from speech recognition give the gaps between words. In the references the voice ran wall to wall (first word at 0.12 s, longest gap 0.3 s).
- Level inside the gaps against level of the words shows whether something else is playing. Gaps louder than the bed are sound effects (21 and 25 per 65 s clip).
- Separate stems on fal.ai (`fal-ai/demucs`, model `htdemucs_ft`): drums stem silent means no beat; the remainder gives the bed level (about 20 dB under the voice), its steadiness and its spectrum.
- Say plainly what you cannot tell (the instruments, whether the music fits the mood) and ask the user to listen.

## What the first two references measured (bundled in pipeline/spec/)

Characters: flat unlit ink-and-fill puppets, plum ink `#3a2832`, head outline thin on the lit side and thick away from the key light, half-lid default eyes, torso one rounded shape with a drawn costume, constant-width rubber-hose limbs, total height about 3 head diameters, hats drawn over the top of the head.
World: real 3D (clip A) or illustrated plates with 3D inserts (clip B), one hard key light, shade at 0.11 to 0.33 of lit and blue-violet, bloom only on emitters, no grain, no vignette.
Colour make-up by share of chroma: red 25 to 40, orange 23 to 38, blue 14 to 29, violet 1 to 5, magenta 5 to 10 percent; 8 to 15 percent of pixels darker than value 0.25.
Camera: 22 mm lens, almost never static, a framing change every 1.2 to 1.5 s, 16 to 22 shots per 65 s, 81 percent dissolves of 9 to 23 frames, low, eye and high angles, two-shots staged in depth with the near head 1.36 to 1.46 times the far one.
Captions: Work Sans Black, white with a 4 px black stroke, centred at 70 percent of the height, 1 to 3 words, hard swaps.
Sound: voice about -17 dBFS RMS, bed about -38 dBFS with no drums, effects every 2.5 to 3 s peaking between -24 and -12 dBFS.
