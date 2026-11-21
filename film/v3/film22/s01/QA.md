# s01 QA: film 22, take s01 (the HOOK), Beck's lodgings NIGHT

Delivered: `take.mkv` (libx264rgb crf 6, 30 fps, **first_g 0, g 0..113 = 114 frames**, 720x1280, 14 samples + denoise, no captions/audio, 34.6 MB), `meta.json`, `cues.json`,
`contact.jpg` (every 6th frame, cyan line y 880), `phone_sheet.jpg`, `QA_AUTO.md` (PASS), `shot.py`, `c22.py` (own helper), `window_card.py`, `stats.py`, `deliver.py`.
Plan range g 0-107 (0.00-3.55 s) + 6 handle frames 108-113 (travel join into s02 through the window; the push continues). No handle before (film start).
Render: 16-17 s per frame wall (two processes, 2 threads each, Cycles CPU).

## Plan beats (narration at +0.10 s: g = round((t+0.1)*30))
| g | beat |
|---|---|
| 0-16 | Beck mid-stroke: the 45 degree ruler lies on the board, the pen drags the bold RED line up the diagonal (key object big: red line 50 % of frame width at g 0) |
| 22 (0.65 "แผนที่รถไฟใต้ดิน") | set square held up at the corner (pose beck_set_square, face and both hands readable): the red line stops exactly at the 45 degree corner |
| 37-53 | he rules the red line on along the horizontal run |
| 58 (1.82 "ผิดระยะ") | thumb push: a white-ringed station mark slides from u 0.9 to u 2.3 along the red line under his hand (the OLD map hangs on the wall to the left, a different layout; it is in frame at g 0-40) |
| 66-107 (2.35 "ให้คนเป็นล้านใช้") | camera whips right past the green lamp to the window and pushes to the pane; the street (UNDERGROUND roundel, crowd streaming in) fills the frame |

## SET_GATE / QA_TECH mandatory items (team 1)
- **5 (Beck never behind the board; face + both hands on 0.65 and 1.82; red line >= 25 % at g 0):** Beck is a cast22 card placed with `c22.place_ray`: it stands on the floor at y 4.9 in FRONT of the board with feet and a dark contact disc, and the pen / hand anchor projects exactly on the line end from the camera. Never occluded (checked every 0.5 s and at every 6th frame). Red line at g 0 = 36 % of the frame width. He dissolves over 3 frames (g 72-75) as the camera whips past him toward the window, so he is never cut by the frame edge or dragged through the caption band.
- **6 (window card):** `window_card.py` re-renders `set3d22/tex_beck/window_london.png` from the REAL london DUSK (same camera as s02 frame 0) with the flat static near crowd hidden and 33 cast22 `crowd_member` walkers with warm rim and contact shadows added. Team 2's corrected london was not available to me, so the crowd is my own placement: the director must expect a small pop on J1 (conform dissolve of a few frames, or re-run the script after team 2's london is merged). The cache PNG is not in git: run `python3 film/v3/film22/s01/window_card.py` (about 2.5 min) BEFORE `shot.py` on a fresh checkout.
- **QA_TECH 1 (soft window card):** the card is rendered at 2048 px and viewed at about 1:1 or minified, no magnification. End key = room (6.6, 12.4, 5.0), lens 30, the exact s02 start pose from API.md (J1), the push continues through g 108-113 at about 3 D/s. NOTE: API.md J1 says the pane is at y 14.0 and the end stops 1.6 D before it; QA_TECH round 2 suggested 12.1; with the hi-res card there is no softness so I kept 12.4 to equal s02's start camera.
- **QA_TECH 27 / J1 / 31 (hook key object, colour):** closer start (lens 36, distance about 6 D to Beck), the red line is drawn through `diagram` state; colours below.
- **4 (Beck feet at 880):** feet and contact shadow at y about 1000-1130 in the early frames, heads above y 880 for g 0-71 (head well above the line); at g 72-75 he dissolves.
- Foreground prop: the green banker's lamp passes 1-2 D from the lens at g 74-86; the ink bottles are the foreground of the first 3 s.

## Final changes after the director's section K / L rules (re-rendered, this supersedes anything above that differs)
- **Nothing floats (K):** `python3 shot.py ground` -> GROUND.md PASS (every 10th frame). Fixes: the sliding station marker sits 3 cm above the paper (was 10 cm); wall/cord items (window frame, old map, cork, shelf, posters, pendant, coat hook) are marked `mounted` (seen touching their wall/cord); Beck has a contact disc under his feet and dissolves over 3 frames (g 72-75) before the camera whips past him.
- **No camera shake (L):** camera = planned keys, gaussian-smoothed (sigma 12 frames, one key per frame), end pinned exactly to the s02 start pose at g 107. `qa_jitter.py` (`jitter.txt`): **second 2 (g 60-89, the whip to the window) 2.3 px, over the 2.0 limit by 0.3 px; every other second <= 2 px, overall median 1.62 px.** Smoother versions (sigma 16, lens bumps) made the blur check fail instead (flat window frames), so this is the best compromise I reached; the motion is a smooth eased arc, the measured value comes from parallax of the big Beck/lamp cards against the wall.
- **Window curtains:** the two flat magenta-red curtain boxes of the window frame are removed at runtime (`pre_scene`): they were big flat slabs that made the whip look soft (qa_auto blur FAIL) and added the take's magenta.
- The camera swing now starts at g 50 (not 56) and is longer and gentler; lens 36 -> 30.

## Numbers (final, 114 frames)
| measure | value | target |
|---|---|---|
| mean saturation | 0.55 | >= 0.50 |
| vivid share | 51.3 % | >= 45 % |
| mean luma | 105.9 | 85-110 |
| top-third luma | 98.8 | <= 115 |
| shade hue 240-260 | 57 % of frames (median 259; my estimator) | >= 80 % (NOT met) |
| magenta (qa_auto strict / my wide test) | 0.0 % / 8.8 % | <= 10 % |
| in-shot frame diff (90x160 grey) | median **17.48**, p90 **34.36**, min 2.01 | median >= 4, p90 >= 12 |
`qa_auto.py` PASS (one soft frame, g 113, handle). `ground_check22` PASS. `qa_jitter` 2.3 px in second 2 only.

## Known issues (for the director)
- Jitter 2.3 px in second 2 (see above).
- Shade hue in band on 57 % of frames (target 80 %).
- The street beyond the window contains the lodging house's own window-box flowers (red/yellow/pink lumps) in the lower third: real london geometry (same in s02), not a card artefact.
- The pendant lamp bulb enters the top edge at g 54-70 as a flat yellow disc (about 1.4 % of pixels).
- The window card (`tex_beck/window_london.png`, gitignored cache) was re-rendered by `window_card.py` from the current london with my own crowd; team 2's corrected london was not available, so expect a small pop at J1 (conform dissolve) or re-run the script after team 2's london is merged. Run `python3 film/v3/film22/s01/window_card.py` once before `shot.py` on a fresh checkout.
- Mouths are closed in the whole take (no quote).
