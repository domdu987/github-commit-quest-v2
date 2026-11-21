# Visual + story breakdown of a hit YouTube Short (channel with 9-33M views per clip)
Base dir: /tmp/claude-0/-home-user-github-commit-quest-v2/e8b79665-ba86-5bba-9861-f4e29c068ae7/scratchpad/ana
For your clip NAME: video clips/NAME.mp4 (look only at extracted images — do not play video), frames f2/NAME/t_%03d.jpg at 2 fps
(t_001 = 0.0 s, t_00k = (k-1)/2 s), transcript with timestamps tx/NAME.txt, word timings tx/NAME.words.json, measurements meas/NAME.json.
Look at EVERY frame (build contact sheets with PIL, e.g. 4x4 grids of 360px frames, and view them; zoom into single frames where needed).

Write NAME.md in the base dir (in English, concise but specific, numbers wherever possible):
1. Beat sheet: table second-by-second ranges -> narration line -> what is on screen -> story function (hook / context / hero / antagonist
   mock / escalation step N / twist / reveal mechanism / ending). Note where the narrator says "You see," and other recurring phrases.
2. Story mechanics: hook sentence structure (first 3 s), how the reason is withheld, who mocks, the countable escalation, the false
   payoff, the reveal (is it one visual mechanism?), the ending image, any second-person "you" address. Word count, sentences.
3. Camera: list every framing change with time (cut, whip, push, pull, crane, orbit, rack), shot sizes (ECU/CU/MCU/MS/WS/EWS), angles
   (low/high/eye/top-down/dutch), average seconds per framing, how continuous movement is (is the camera ever static?), transitions used
   (hard cut, whip pan, match cut, zoom-through, morph). Where the camera goes at the reveal and at the ending.
4. Light, colour, depth: palette per scene (name the dominant hues), key light direction, rim light, practical light sources in frame
   (lamps, windows, fire), time of day, contrast, fog/haze/god rays, depth layering (foreground objects, background blur or not — be exact:
   is the background sharp or blurred?), vignette, colour grading shifts between story phases (e.g. warm happy -> cold danger).
5. Characters: design (head shape, eyes, mouths, body proportion, outlines), how many characters per frame, expressions used and WHEN
   (list them with times), gestures/poses, lip-sync (does the mouth move with dialogue? only for quotes?), eye direction, exaggeration
   (squash/stretch, sweat drops, anger marks), crowd treatment, how the hero vs. antagonist are distinguished.
6. On-screen text/captions: font, size, position, colour, outline, how many words per caption, emphasis words, any graphics/diagrams/arrows.
7. Sound (from transcript and measurements only): narration speed (words per minute given in meas or compute), pauses, character voices in
   quotes, sound effects that are implied.
8. The 5 things this clip does that make it work, ranked.
Final message: a 10-line summary of the most important findings.
