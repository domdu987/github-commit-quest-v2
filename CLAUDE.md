# นับวัน (@nabwan.th) — reel production playbook

Thai story reels for IG/FB about everyday life and love. The user's standard is **professional, with depth**:
icons, motion, effects, storytelling, camera angles, sets, graphics, animation and shadows all at the level of the
"52 ปีกับกระทงสองใบ" / "39 บาทที่แม่ไม่กล้ากด" / "312 ชาม" set (Oct 2026). Never ship below it. The source code
lives in `nabwan/` (copy it to the scratchpad to work; renders, voice and music stay out of git).

## Format (fixed)
- 1080×1920, ≤ 60 s, 30 fps. Narration: Gemini 3.1 Flash TTS voice **Puck**, conversational, sped up **1.2×**.
- Every clip opens with the hook "ถ้า… คุณ…, ถ้า… เขา…". Kinetic captions at top 1640 (each part of a cue needs its
  own word anchor in `placeN.py`; two parts on one anchor reveal at the same time). Title card mid-clip, end card
  with avatars + number title + one-line lesson + CTA chip + นับวัน brand.
- Look: the chibi "story2" rig (`story2/puppet2.js`), warm palettes, INK outlines. No cold teal/grey rooms.

## Look and sets
- Rooms must be **full** like the first clips (47 ครั้ง / 1,095): windows with moon or garden, fairy lights,
  shelves, posters, plants, rugs, a pet or a story prop. Use `story8/props8.js` helpers. Never an empty wall.
- **Every room gets its own palette** (navy bedroom, olive living room, rose room, cream-and-mint provincial
  house, teak veranda…). Never reuse a character design or a house from an earlier clip (e.g. a new mom per story).
- Dark rugs or floors under the caption band (y ≈ 1600–1700); light cream or yellow rugs make white captions unreadable.
  Light set pieces there too (an open cardboard flap, paper): lay a dark gradient band over y ≈ 1440–1920.
- Weather and streets: `story11/rain11.js` has the following:
  - rain streaks per layer, splashes, puddles, drips and lens drops;
  - an umbrella that opens and tilts, and a rain-shadow mask that keeps whoever is under it dry;
  - a wet-shirt patch, and mirrored reflections on wet ground.
  For a long street the camera can track, draw the vignette in screen space (`S.fx`) instead of the mid layer.

## Depth and light (`pro/pro.js`, load it before the sets)
- Shots use 3 layers: `['far', 0.35, 1.5], ['mid', 1, 0], ['fore', 1.8, 12–14]`; put bokeh and blurred
  foreground in `fore`. Foreground props must be recognisable or not there at all; unreadable blurred blocks look like dirt.
- `lightCast(S, set, pups)` on every lit set. It adds the rim light and core shade from `charLight`, plus a wall cast
  shadow per puppet. Each set returns `shadowL` (a group placed before the furniture) and
  `light: {ux, uy, lx}` pointing at its real key light.
  - Lamp key light: shadow op 0.2–0.24.
  - Overhead tube or bulb: soft, op ≈ 0.13, blur ≈ 11 (otherwise the shadow reads as a dark blob in close-ups).
  - Window/sun light: shadows fall *away* from the light (positive k with lx on the light's side).
- Every room: `wallAO` at the floor line, `lightPool` / `lampCone` at the lamps, `lightShaft` with dust for window
  light, `ktReflection` for lights on water. Keep `.layer { will-change: auto }` (pro.js sets it) or the lit
  characters render soft.

## Camera and storytelling
- Every scene is a **shot list** (`shotCam` + `applyCam`) cut on narration beats, usually 2–5 shots:
  wide z≈1.1–1.2 → medium 1.3–1.6 → close-up 1.9–2.3 → **insert** 3–5.5 on the story object (coriander in the
  bowl, wired slippers at the door, candles being lit, feet in new slippers). Use `frameAt(worldX, worldY, z, screenX,
  screenY)` with head positions from `HW()`; handheld stays on; depth of field follows zoom.
- Each narration beat needs an on-screen *action* or insert, not only a card:
  - contrast cuts (her cart fills / mom hesitates);
  - entrances (walk cycle into sit);
  - reactions in close-up;
  - time-lapse (clock chip + faster motion);
  - a sepia flashback that dissolves to the present;
  - endings with a wide shot or crane-up, hearts, light leak.
- Keep the camera **inside the set**:
  - The visible world x must stay within 0…1080, otherwise the vignette edge shows as a vertical seam.
  - The camera y offset must stay ≥ 0, otherwise a dark band shows at the top.
  - Faces must never be cut by the frame edge or covered by UI cards (cards sit in y ≈ 100–800, faces below).
- Chibi heads sit right above the hands, so a hands-only insert always cuts faces.
  - Frame hand actions (a hand-off, a push) as a close two-shot, z ≈ 2.2, with both faces whole.
  - Frame a back or shoulder insert so the other character is out of frame, or shows only the back of the head.
  - Keep raised props off faces: an umbrella goes up between the heads and opens above them, then comes down.
  - Raised arms ("ta-da"): spread them out and up (`aF ≈ [-24, -48]`, `aB ≈ [214, 236]`); an arm raised forward
    goes over the head and across the face.
  - A standing chibi can't reach a seated one's neck (arm ≈ 178 px at s 1.2): the IK tops out at face height. Sit or
    kneel beside them to wrap a scarf or touch a shoulder, and keep the heads ≥ 2 head radii (≈ 150 px) apart so one
    face never covers the other.
  - In a close-up next to a character who stands nearby, look for a sliver of the other head at the frame edge (a cut
    face); move the framing or the character.
- Tears on the 3/4 face: one stream per eye from its outer corner, drifting outward (`tears(…, {drift: ±1})` in
  `story12/icons12.js`). Streams that split both ways run across the nose and read as a runny nose.
- Phones are always seen **from the back** (`phoneProp`: case, camera, sliver of screen light).
- A hand mic stays at the collar, below the chin (`torsoW(pup, p, 66, -RIG.T + 6)`, `propRot ≈ -34`); an open-hand
  "this is my daughter" gesture stays low (`torsoW(pup, p, 104, -44)`), never at the other person's face.
- Seated characters with big forward heads clap with their hands at the chest (`torsoW(pup, p, 72, -RIG.T + 66)`);
  raised arms on a seated chibi cross the chin.
- Match cut across years (child → adult): the same head screen position and size (adult zoom = child zoom × child
  scale) and a 0.45 s dissolve (`S.fadeIn`).
- `shotCamF` clamps the camera y to ≥ 2 unless you pass `minY`. Sets that extend above y = 0 (a bus ceiling, a terminal
  roof, the sky) need a negative `minY`, or every close-up is pushed down by hundreds of pixels.
- Moving vehicles (`story13/sets13.js`): the outside rushes past in the far layer (`nightOutside13`: lamps, trees, warm
  traffic bokeh), a street-lamp `lightSweep13` crosses the cabin and the cast, the camera gets a small `bump`.
  Fireworks (`fireworks13` + `burstPlan`) flash the whole set.
  - Feed fireworks the shot clock: `set.update(lt)`, never `lt + offset`, or every burst is already over.
  - Put window bursts at window height.
- CSS `zoom` on a card also scales its `left` / `top`.

## Graphics
- Cards get the layered pro shadow, a top gloss and a shine sweep; they enter with `enter3d` / springs.
- Prefer **animated metaphors** over static numbers:
  - a balance scale that tips;
  - a Buddhist-era (พ.ศ.) year odometer (hide the leading-zero column once the value drops under 10: "9", not "09");
  - a red marker circling a date;
  - items flying into a cart;
  - a LINE banner that buzzes with a ripple;
  - a time-lapse clock;
  - a glowing "?".

## Audio
- TTS through fal.run `fal-ai/gemini-3.1-flash-tts`, with retries.
  - The content filter blocks some lines about death or loss; reword them (e.g. "ปีนี้ยายไม่อยู่แล้ว" passes).
  - Transcribe every take with Whisper large-v3, run plain (no prompt); regenerate if a word reads wrong.
- Music: fal `elevenlabs/music` composition plan with every section ≥ 3000 ms; use `extend.py` if it is short.
- Sound effects: generate real ones with fal `fal-ai/elevenlabs/sound-effects/v2` (`{text, duration_seconds,
  prompt_influence}`; about 23 per story) into `storyN/sfx/`.
  - In `audio.py` (`story13`), use `put` / `loop_bed` and `muffle` (low-pass) for anything heard through a bus window or a wall.
  - Synthesise only small accents (ticks, sparkles).
- A character's own line (the mom's PA announcement) can use a second Gemini voice (female: Gacrux, at 1.1×) with the
  bus-PA filter `pa()` (band-limit, drive, short cabin echo) and caption style `p`. Whisper-check it like the narration.
- Mix with the per-story `audio.py` numpy mixer:
  - ducking with a 0.4 s hold; SFX for every on-screen action (steps, taps, plops, lighter, buzz);
  - master with `volume=1.5dB,alimiter=limit=0.75:attack=4:release=80:level=false` to about −14 LUFS.
  - **Transcribe the final mix**; where a word gets masked (e.g. "จากไป" → "จะไป"), add a music `ramp` down under that line.
  - Before adding a ramp, transcribe the voice stem alone (`audio.py` writes `<out>.stems.npy`).
    - If the stem also misreads, the music is not the cause, so regenerate the take.
    - If new takes misread the same way, Whisper is confusing the tone (หนัก → นัก). Flag the word to the user for a listen.

## QA (non-negotiable before delivery)
1. Stills of every shot before the full render (`node render.js stills dir t…`, grid with `scripts/grid.sh`), fix framing first.
2. Full render (`PAGE=../storyN/index.html node render.js video out.mp4 30 [t0 tEnd]` — the 3rd number is the END
   time). About 1 fps, so run at most 2 renders at once on 4 cores. Never run Whisper during a render: the CPU contention
   makes a frame screenshot time out (`render.js` now allows 180 s).
3. Contact sheets every 0.6 s (`fps=1/0.6,scale=432:768,drawtext,tile=4x2`) and read **all** of them; their time
   labels can run about 0.3 s ahead, so pin exact times with stills. Check:
   - cut faces;
   - UI over faces;
   - edge seams or bands;
   - shadow blobs or wrong shadow direction;
   - unreadable captions;
   - hands through tables;
   - phones facing the viewer;
   - unclear props.
4. Fix by re-rendering only the affected segment and splicing by frame index (ffmpeg trim + concat), then re-check
   those frames.

## Delivery
- Full-quality copy: `deliver/<Thai title>.mp4`.
- Phone copy: `deliver/phone/<ascii-name>.mp4` with
  `-profile:v high -level:v 4.0 -crf 24 -maxrate 2500k -bufsize 5000k -preset slow -c:a aac -b:a 160k -movflags +faststart`.
- Cover `deliver/covers/cover-<name>.jpg` via `cover/grab.js` (HIDE selectors) + `cover/cover.html` + `cover/shoot.js`.
  The title sits in the 3:4 safe area; the subject goes below it and is not covered by the brand badge.
- Append the post caption (hook, story, lesson, 📌 CTA, hashtags) to `deliver/แคปชั่น-ทุกคลิป.txt` and give it in chat.
- Report API cost (≈ $1 per story for voice + music).
- No model identifiers in any file or commit.
