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

## Numbers (take as delivered, 114 frames)
| measure | value | target |
|---|---|---|
| mean saturation | 0.58 | >= 0.50 |
| vivid share | 55.4 % | >= 45 % |
| mean luma | 98.9 | 85-110 |
| top-third luma | 90 | <= 115 |
| shade hue in 240-260 | 89 % of frames (median 257) | >= 80 % |
| magenta (qa_auto strict) | 0.0 % | <= 10 % |
| in-shot frame diff (90x160 grey) | median **10.00**, p90 **32.56**, min 2.06 | median >= 4, p90 >= 12 |
`qa_auto.py` PASS; one soft frame (g 89, window frame at speed).
The first take showed 15 "suspected blur" frames (g 82-100: the flat red curtain, navy sky and glow of the window). Fixed without any blur filter: a wider lens (30 -> 24 mm) while the camera crosses the room (more wallpaper and window frame in view), back to exactly 30 mm at the pane, plus a slightly brighter street card in mid-swing that eases to 1.0 at the pane.

## Camera
Low hero 3/4 from the front-left: g 0-56 pushes in about 6 %/s and arcs left past the ink bottles (1-4 D/s), g 56-107 swings right (smooth-step path, peak about 14 D/s) past the lamp to the window, lens 36 -> 30. No frame is parked: the slowest frame pair has diff 2.06 (g 0-1, start of an eased move). No depth of field, no blur.

## Known issues (for the director)
- The street beyond the window contains the lodging house's own window-box flowers (red/yellow/pink lumps) in the lower third: this is the real london geometry (same in s02), not a card artefact.
- The pendant lamp bulb enters the top edge at g 54-70 as a flat yellow disc (about 1.4 % of pixels); not dimmed.
- Mouths are closed in the whole take (no quote).
