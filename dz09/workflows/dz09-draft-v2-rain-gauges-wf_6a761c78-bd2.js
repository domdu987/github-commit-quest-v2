export const meta = {
  name: 'dz09-draft-v2-rain-gauges',
  description: 'Lighter rain and sharper picture, quieter rain sound, gauge-tube icons, then a full draft v2 of the EP.1 hook',
  phases: [
    { title: 'Fix', detail: 'rain/clarity, gauge icons, audio mix in parallel' },
    { title: 'Draft', detail: 'shot fixes, full 360x640 draft v2 with sound' },
    { title: 'Review', detail: 'independent watch-through and repair' },
  ],
}
const P = '/tmp/claude-0/-home-user-github-commit-quest-v2/94b8b382-ecfe-5ec4-8832-97f03dd08322/scratchpad/dz09'
const COMMON = `Project root ${P}. DEAD ZONE 09, Thai zombie series, EP.1 hook film (53.32 s, 24 fps, 9:16). Read ${P}/v10/film/README.md first (shot scripts, runner, finish), then ${P}/v11/set/API.md (set, light, post), ${P}/v8/cast/API.md (flat 2.5D SVG puppets), ${P}/v4/iconfx/API.md (old icons). Current draft: ${P}/v10/film/draft_v1.mp4 and draft_sheet.png. bpy 5.3 Cycles CPU, 4 cores, numpy, PIL, cv2, ffmpeg, Chromium/Playwright available. Never call paid APIs or any network service; no AI image generation: everything is drawn or built by code. Do not copy characters, text or logos from the reference clips. Kill any render processes you start before you return. Look at your own output images at full size before reporting, and report honestly what is still weak.
USER FEEDBACK ON DRAFT V1 (Thai user, verbatim meaning): "Make the rain less, it makes the scene look blurry. The rain sound too. Make the icons prettier: make them gauge tubes (meter bars) whose value goes up or down."`

phase('Fix')
const [rain, gauge, audio] = await parallel([
  () => agent(`${COMMON}

YOUR JOB: rain and clarity. You own ${P}/v11/set (post11.py, look11.py, render11.py, beauty.py ...) and in ${P}/v10/film only common.py, stage.py, run.py and shots/*.py post options. Do not touch finish.py or cues.py.
Find everything that makes the picture soft or veiled: rain streak layers (count, length, opacity, near-lens streaks), mist/fog/atmosphere, light shafts, bloom/glow radius, depth-of-field strength, motion blur, lens droplets, grain, the 75 % render scale of the final tier. Reduce: rain streaks to roughly 35-45 % of the current density and lower opacity, visible mainly where they cross headlights, lamps and neon (back-lit), almost invisible over faces and dark areas; no near-lens streak sheet over characters; fog/haze cut so far cars and signs keep contrast; bloom tighter; DOF kept only as a gentle background falloff with principals and their surroundings sharp. KEEP the wet look: glossy wet asphalt, puddle reflections, ripple rings, small splashes, drips on car edges. Keep the approved blue night grade (shade hue 222-238, no magenta cast) and the practical lights.
Expose the levels as named parameters with the new values as defaults (e.g. RAIN, HAZE, BLOOM, DOF) so they can be tuned later; document them in API.md/README.
Measure sharpness before/after (e.g. Laplacian variance and local contrast on mid/background regions) on the same frames. Prove with ${P}/v12/rain_before_after.png: 6 shots (S03, S06, S10, S13, S19, S24), each before | after at 720x1280 final tier (single stills via run.py --at), labelled, plus the measured numbers. Return: what was changed (file, parameter, old -> new), measurements, CPU s per frame after the change, what still looks soft.`, { label: 'fix:rain', phase: 'Fix' }),
  () => agent(`${COMMON}

YOUR JOB: replace the on-screen icons with good-looking animated GAUGE TUBES. You own ${P}/v12/gauge (create it) and in ${P}/v10/film only cues.py and finish.py. Do not touch other film files.
Design a small gauge library drawn by code (SVG via Chromium, or PIL/cairo with supersampling) rendered as RGBA overlays per frame, composited after all blur so they stay crisp, at any resolution and for 9:16 and 16:9:
- A glossy rounded glass tube (vertical by default, horizontal variant) with dark translucent body, bright gradient liquid fill, soft inner glow, highlight streak, fine tick marks, thick dark outline matching the cartoon line weight of the cast, a round badge on top or at the left with a clean simple pictogram, and an optional short Thai label or number (font ${P}/fonts/Kanit_900Black.ttf; verify Thai glyph shaping, vowels and tone marks must not collide).
- The value ANIMATES: eased fill moving up or down, a small overshoot and settle, a flash and little particles or a shake when it changes, a small up or down arrow and delta number while changing, colour moving with the value (green -> amber -> red), a pulsing warning state when critical, pop-in and pop-out. Segmented mode for discrete values.
- Gauges for this film (times from ${P}/audio/narr_v1/cue_times_v2.json and ${P}/v10/film/cues.py; film time = caption time + 0.30 s): (1) cutter battery, 3 segments, full at 16.30-16.70, stays quietly visible in later cutter shots; (2) missed calls / daughter's trust: shows 4 missed calls, then a heart-topped trust tube that drains while Kong says he will call back and drops hard when the call ends (around 28.25-28.95 and the hang-up shot S16); (3) danger: rises slowly while Kong walks to the car (S17-S19), jumps to full red and pulses when the driver lifts his head (41.66) and at the lunge (43.45); (4) the 60 second countdown as a draining tube with the number (46.43-50.37). Remove or restyle remaining old icons so everything is one family; keep the phone-voice bubble and title if they fit, restyle if they clash.
- Placement: never over a face, never over the caption band (captions at y about 900/1280), inside the safe area for Shorts UI (keep clear of the right edge buttons zone and bottom 20 %), about 9-12 % of frame width for a tube; provide a 16:9 placement table too. At most two gauges on screen at once.
Prove with ${P}/v12/gauge/gauge_sheet.png (each gauge at 6 values and states, large, on dark and on bright backgrounds), ${P}/v12/gauge/gauge_demo.mp4 (each gauge animating over a real draft frame from ${P}/v10/film/out/draft_360x640/comp, upscaled to 720x1280, 10-15 s total), and wire them into finish.py/cues.py so the next film conform uses them. Write API.md. Return the API, cue table, files, and gaps.`, { label: 'fix:gauges', phase: 'Fix' }),
  () => agent(`${COMMON}

YOUR JOB: the sound mix. You own ${P}/audio/narr_v1 but must NOT overwrite mix.wav, narr_final.wav or any timing json; write mix_v3.py -> mix_v3.wav (same length 53.32 s, same cue times). Read mix_v2.py. The user finds the rain too loud. Lower the rain ambience bed by about 10-12 dB (it was normalised to -21 dBFS RMS: aim near -32, and duck it a further 3-4 dB under narration), soften its high frequencies a little so it is a soft bed instead of hiss, lower rain_on_hood likewise, keep sirens faint, keep all story effects (radio static, battery beeps, phone vibrate, heartbeat, scream, stopwatch, title hit) clearly audible, narration on top and intelligible. Final loudness about -14 LUFS integrated, true peak <= -1 dBTP (measure with ffmpeg ebur128/loudnorm analysis). Also write a 20 s A/B file ${P}/audio/narr_v1/ab_rain.mp3 (10 s old mix then the same 10 s new mix, from 8 s). Return measured levels old vs new (rain bed RMS, narration-to-bed ratio, LUFS, peak) and the files.`, { label: 'fix:audio', phase: 'Fix' }),
])

phase('Draft')
const draft = await agent(`${COMMON}

Three fixes were just made. Rain/clarity: ${rain}
Gauge icons: ${gauge}
Audio: ${audio}

YOUR JOB: make the full draft v2. You own ${P}/v10/film (all of it now) and may adjust ${P}/v12. First fix these shot problems seen in draft v1 (check each on stills with run.py --at before the full render):
- S04: a background extra in yellow pops up huge and cropped near the lens; restage so extras are at readable distance and nothing unreadable blocks the lens.
- S18 (POV through the cracked windscreen): the driver reads as a teal blob; make his slumped face and shirt readable through the glass (interior fill light, fewer cracks over the face).
- S20: the back of Kong's head covers almost the whole frame; reframe as a clean over-the-shoulder so the driver lifting his head and the red eye are the subject (the gauge agent's danger tube replaces the old eye icon if it clashes).
- S15 close-up of Kong: line quality must hold at this size (re-raster the puppet at higher resolution for close shots).
- S06/S07: the cutter must sit properly in his hands.
Then re-render ALL 1280 frames at 360x640 draft tier with the new rain/clarity settings (4 workers x 1 thread, --force or a new tier folder so old frames are not reused), conform with the gauges and ${P}/audio/narr_v1/mix_v3.wav into ${P}/v10/film/draft_v2.mp4 and ${P}/v10/film/draft_v2_sheet.png (same layout as draft_sheet.png). Also render 6 stills at 720x1280 final tier (S03, S06, S13, S18, S20, S23) with gauges and captions composited, as ${P}/v10/film/v2_stills_720.png (2 rows x 3), so the user can judge sharpness. Update README. Return what changed per shot, files, timings, CPU cost per final frame, and what is still weak.`, { label: 'draft:v2', phase: 'Draft' })

phase('Review')
const review = await agent(`${COMMON}

Draft v2 was just built. Builder report: ${draft}
YOUR JOB: independent strict review as the user would see it on a phone, then repair. You own ${P}/v10/film and ${P}/v12. Extract frames from ${P}/v10/film/draft_v2.mp4 every 0.5 s and look at all of them, and look at v2_stills_720.png at full size. Check: (1) rain is light and the scene is clear, not veiled or blurry, yet still reads as a wet rainy night; (2) gauges are attractive, crisp, readable in under a second, animate up/down at the right cues, never cover faces or captions, one visual family; (3) the five shot fixes (S04, S18, S20, S15, S06/S07) really work; (4) characters stay flat, upright, camera-facing, costume colours match ${P}/uploads/character_sheet.webp; (5) captions in sync and never overlapped; (6) audio: rain quiet, narration clear (measure). Fix what fails (re-render only the affected frames, re-conform to the same file names), and return: defects found, fixes made, and an honest list of what still differs from a professional result.`, { label: 'review:v2', phase: 'Review' })
return { rain, gauge, audio, draft, review }