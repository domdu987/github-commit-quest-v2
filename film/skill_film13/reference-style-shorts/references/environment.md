# Environment

Tested in a cloud container with 4 CPU cores, 15 GB RAM, no GPU, outbound network limited to package registries.

## Tools

| Need | How |
|---|---|
| Blender | `pip install bpy` (Blender as a Python module, 5.x). Cycles renders headless on CPU. No Freestyle (a render with it aborts the process without a display), no EEVEE or Workbench without a display. |
| SVG to PNG | Headless Chromium through Playwright. Where a browser is preinstalled do not run `playwright install`. Wait for fonts before a screenshot; embed fonts as base64 `@font-face` or use system fonts. |
| Video and audio | ffmpeg with libass (captions), `atempo`, `alimiter`. |
| Measuring | numpy, Pillow, OpenCV. `rapidocr-onnxruntime` reads burned-in captions offline. |
| Fonts | npm: `@expo-google-fonts/<family>` carries full TTF files (Kanit, Prompt, Noto Sans Thai, Work Sans). |
| Thai text tools | `pip install pythainlp` (dictionary engines work offline) for syllable counts and word boundaries. |

Model hubs were blocked, so local speech recognition models could not be downloaded; speech recognition and stem separation go through fal.ai instead.

## fal.ai from a restricted container

- Ask the user for the key through the environment's secure credential form for host `fal.run`, header `Authorization`, prefix `Key`. Never ask them to paste a key into the chat. The session's proxy injects it; code must not add the header.
- Allow the result hosts `v3.fal.media` and `v3b.fal.media`. In a session on the default environment, propose a new personal environment with those hosts and move the session's network onto it; a running session cannot join an environment with unrestricted network.
- Test access at no cost: a request with wrong field types returns HTTP 422 when the key and network are right.
- Endpoints used: `fal-ai/elevenlabs/tts/eleven-v3` (speech with timestamps), `fal-ai/elevenlabs/speech-to-text`, `fal-ai/elevenlabs/sound-effects/v2`, `fal-ai/demucs`, `fal-ai/gemini-3.1-flash-tts` (alternative voice). Spending for a 65 s film's narration, checks, effects and stem analysis was well under one US dollar; report it as an estimate unless you can read the balance.

## Blender 5.x traps already hit

`pipeline/spec/verify_blender_api.md` and `pipeline/v3/stage/REVIEW.md` have the evidence. In short: `Action.fcurves` is gone and the keyframe-interpolation preference does not apply to inserted keys, so set easing per keyframe point through the channelbag helper; Diffuse roughness must be 0 for the light model to be predictable; set emission sampling to NONE on lit materials; inverted-hull ink needs even offset and must be visible to camera rays only; persistent render data keeps stale sprite textures after a re-pose, so keep it off; create a UV layer before generating primitive UVs with bmesh; Cycles does not mip-map, so a texture far finer than the screen shimmers.

## Render budget

A final 720x1280 frame at 12 samples: about 18 CPU seconds (4.5 to 5 s on 4 threads with the machine to itself). Drafts at 360x640 and 6 samples: about 1 s. A rented GPU box that can only be driven through short remote commands is not worth it: moving the project there and thousands of frames back costs more than it saves.
