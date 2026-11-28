# v14/cards: DEAD ZONE 09 EP.1, info cards

PROJ = `/tmp/claude-0/-home-user-github-commit-quest-v2/94b8b382-ecfe-5ec4-8832-97f03dd08322/scratchpad/dz09`. Folder: `PROJ/v14/cards/`. Nothing outside this folder was edited.
Drop-in replacement for the v13 icon row (`v13/icons/icons13.py`), after the user's reference clip: one INFO CARD (a navy quarantine field tag) at the top-left that arrives with its subject, changes its value with the story and leaves when the subject is over; within a subject the older card shrinks to a chip above the current one. Drawn by code as SVG, rasterised by one headless Chromium page, no network, no image generation.

## Look (second user note: "fit the theme of OUR story": a quarantine / rescue field tag, not a cream note)

- Panel: flat night navy `#141a2b`, 5 px outline in our PAPER off-white (`#f6f1e7`) so it reads on the dark shots, plus a 2 px ink keyline outside it for the bright ones. Text in PAPER; the value in the state colour (paper = neutral, green = OK, amber, red = critical, grey = hung up).
- Left bar: diagonal hazard stripes, rescue orange (`#f26a1b`, the vest) on ink. Solid red when critical (signal lost, missed calls from the first one, trust at 28 % and below, infected), solid green when the battery is full, grey after the hang-up.
- Zone tab: a small stencil tab on the top edge (right end; left end on the radio card) with the title's biohazard mark from icons13 at 17 px and "เขต 09", so every card belongs to the series.
- Medallion: ink disc with a 3.5 px ring in the state colour, the v13 animated icon inside with its light keyline.
- Critical moments: 3.243 s three frames of offset slices on the value (signal glitch, on the film's three static frames) and a shake; 41.657 s the outline, bar and tab snap to red with the eye burst; 43.445 s ONE frame (g 1043) of white card with red outline and text, then a shake (the film's own white / red frame is g 1045, `cues.LUNGE_FLASH`; set the card's to that if they should coincide); countdown: outline pulses amber and the card swells 2.5 % on each second (46.78, 47.78, 48.78, 49.78).
- Chips: the same navy tag, 44 px high, icon + final value in its state colour.
- Two panel alternatives are on `sheet.png` (bottom) over the same film frames: A = the above (default, used in `demo.mp4`), B = a rescue-orange header band with the mark, "เขต 09" and "DEAD ZONE" on the navy panel (card 28 px taller, grows upward, no tab). Switch with `DZ09_CARD=B` in the environment or `cards14.STYLE = "B"`.
- The icons, every cue time, the palette and the easing are imported from `icons13` (not copied). The strip extras of v13 (value bar, name tag, number beside the stopwatch, count in the phone badge) are switched off for the length of each draw call, because the card carries them as text.
- Font: Kanit Black only (`PROJ/fonts/Kanit_900Black.ttf`), the one Kanit file in the project (finish.py and the captions use the same). There is no Kanit SemiBold on the machine and no network, so label, unit and sub-line are Kanit Black in a dimmer paper (`#c3c2c6`) with a thin navy stroke over the glyph edges, which reads as a lighter weight. With a SemiBold file: add an `@font-face` to `page.html` and a weight to `txt()`.
- Sizes at 720 wide: card 132 px high, 290-439 px wide (61 % of the frame at most), top-left (36, 110), tab reaches 22 px above the top edge; chips 44 px high at y 58-102. Label 25 px, text value 54 px, number value 60 px (countdown 68 px), unit 28 px, sub-line 23 px. Ink of the whole layer stays inside y 52-274 and left of x 495 (the widest card for a few frames of pop-in overshoot and shake; at rest x 480). Captions are at y 900.
- Motion: spring pop-in from the left edge; value change = old value lifts and fades, new one comes up (5 frames, not clipped, so no Thai mark is cut); leave = 7-frame fade + slide left; card to chip = 9-frame shrink toward the chip row.
- Flat only: no shadow, gradient, glow, texture or grain.

## Calling it (same as icons13)

```python
import sys; sys.path.insert(0, PROJ + "/v14/cards")
import cards14 as IC
rgba = IC.overlay(g, W, H, aspect="916")     # film frame g 0..1279 -> uint8 RGBA (H, W, 4), straight alpha; "916" | "169"
rgb  = IC.over(rgb_uint8, g)                 # composite over an RGB frame (aspect from its shape, or pass it)
IC.cue_table()                               # [(card, joins, leaves, [(film s, event), ...]), ...]
IC.close()                                   # stops Chromium (also at exit)
IC.LAYOUT["916"], IC.LAYOUT["169"]           # x0, y, s (scale), shift {shot: (x0, y)}, fade, out (leave times), title
IC.T                                         # the cue-time class of icons13 (same object)
```

- `DZ09_NARR` (default `narr_ohm`) is read by icons13 on import, as before.
- Pure function of `g`. Rasters are cached in `cache/<md5 of the SVG>.png` (safe to delete; parallel workers can share it).
- Cost at 720x1280, one process, while the final render held all 4 cores: cold 0.038 s per frame on average, 0.09 s worst; cached 0.006 s. No static-part cache was needed.

## Switching `v10/film/finish.py` (not done here)

In `icons()` (line 77) replace the line `        import icons13` with:

```python
        sys.path.insert(0, os.path.join(PROJ, "v14", "cards")); import cards14 as icons13
```

(the `sys.path` line above it can stay: cards14 imports icons13 from `v13/icons` itself.)

Nothing else changes: `icons_over()` calls `.over(rgb, g, aspect)` and `comp()` calls `.close()`, both exist here. Without editing the file the same switch works from outside: `import finish; import cards14; finish._IC["m"] = cards14` (this is how `demo.py` and `on_film.py` ran finish.py's own `comp_frame`).

## Cards (film seconds, narr_ohm take)

| Card | In | Leaves | Label | Value and events |
|---|---|---|---|---|
| radio | 0.10 | 6.40 | วิทยุกู้ภัย | กำลังติดต่อ in paper (arcs follow the voice, hazard bar) -> 3.243 three glitch frames, then สัญญาณขาด in red, bar red, card shakes, flat line + cut mark; 4.09 radio goes grey |
| battery | 15.92 | 19.30 (as a chip from 17.27) | เครื่องตัดไร้สาย | 0/3 ขีด -> 16.30 1/3 -> 16.50 2/3 -> 16.70 3/3 in green, bar green + sub-line แบตเต็ม; 17.27-17.64 shrinks into the chip [battery 3/3] |
| calls | 17.56 | 33.00 (as a chip from 21.71) | สายที่ไม่ได้รับ | 0 สาย -> 17.81 1 (red from here, bar red) -> 18.25 2 -> 18.69 3 -> 19.13 4; 20.49 sub-line ลูกสาว; 21.08 sub-line ลูกสาว · น้ำเหนือ; 21.71-22.08 shrinks into the chip [phone 4] |
| trust | 22.00 | 33.00 | ความเชื่อใจของลูก | 82 % + level bar; follows `icons13.trust_level`: 24.94 -> 60, 26.34 -> 52, 27.34 -> 28 (crack 27.96), 28.96 -> 17, 30.35 -> 7 (number and bar red from 28 % down), 31.75 -> 0 and the value becomes วางสาย in grey, bar and heart grey; 32.05 heart splits; 32.21-32.70 whole layer at 35 % |
| danger | 33.62 | 45.90 | คนขับ | ชีพจรอ่อน in green (green heartbeat) -> 37.62 ไม่ตอบสนอง, value, ring and badge go amber by 40.28 -> 41.657 ติดเชื้อ! in red, outline and bar red, red eye + burst -> 43.445 one white / red frame, shake |
| countdown | 46.43 | 50.22 | เหลือเวลา | 60 วินาที in amber -> 47.78 59 -> 48.78 58 -> 49.78 57, amber outline pulse on each second; 50.22 the card dissolves and the stopwatch flies to the title spot; 50.72 biohazard mark lands + burst, holds to the end |

No card: 6.7-15.9 s, 33.3-33.6 s, 46.2-46.4 s.

Wording against the film: วิทยุ / ก็เงียบไป, เครื่องตัดไร้สาย, แบตเต็ม 3 ขีด, 4 สาย ที่ไม่ได้รับ, จากลูกสาว น้ำเหนือ, วางสาย, คนขับ, 60 วินาที are all in the captions. The sub-line order is ลูกสาว · น้ำเหนือ (not น้ำเหนือ · ลูกสาว), because the narration says "จากลูกสาว" (20.49) before the name (21.25) and each word appears as it is said. ชีพจรอ่อน, ไม่ตอบสนอง (the film says it about the injured in the first line, and "นั่งนิ่ง ไม่ขยับเลยสักนิด" about the driver), ติดเชื้อ! and ความเชื่อใจของลูก are not spoken in the film; they are the card's own words.

## What differs from v13

- A card with label + value + sub-line instead of a bare icon with a bar beside it; one card at a time (plus at most one chip), not a row.
- Values are text: connection state, 0/3-3/3, 0-4 calls, trust in percent, driver state, seconds. v13's bar, name tag and the number beside the stopwatch are not drawn.
- New: navy tag panel, hazard bar by state, the zone tab, the chip row, signal glitch, red outline at the eye, one-frame flash at the lunge, amber pulse, the calls sub-line in two steps.
- Same: cue times (`icons13.T`), leave times, the 32.21-32.70 fade, the title mark. From frame 1216 (50.67 s) to the end the layer is pixel-identical to icons13 (checked on every frame 1216-1279); during the flight (frames 1205-1215) the stopwatch starts from the card's medallion (centre 100, 175) instead of the row, same path formula and same end.
- `LAYOUT` keys differ (`s`, `shift` as `{shot: (x0, y)}`; no `q / a / m / gap / band / keep`). 9:16 has one shift: S01 at y 136 instead of 110. New module names: `STYLE`, `TAB_LEFT`.
- 16:9 is laid out (x 64, y 86, scale 0.80) and renders, but was only looked at on a flat background.

## Faces (9:16, checked every 0.5 s on the 360x640 draft scaled to 720x1280)

- S01, 2.4-3.3 s: Kong's face rises behind the right end of the radio card. With the S01 shift (y 136) and the tab at the left end, eyes and mouth are clear; the card's top edge covers his chin and collar.
- S09, 16.5-17.5 s: the out-of-focus foreground face at the top-left edge: the battery card covers its mouth and chin (v13 covered it too, by choice).
- S16, 30.5-32.2 s: Kong's chin is at the top edge of the frame above the card; the card covers his collar and vest, not the face. 32.3-32.6 s: his head sweeps through the card, layer at 35 % (as in v13).
- No other shot has a face under the card. S10 (18-19 s): hair tips are about 20 px under the card.

## Files

| File | What |
|---|---|
| `cards14.py` | everything: layout, card states, drawing, raster, `overlay`, `over`, `cue_table` |
| `raster_page.js`, `page.html` | the Chromium rasteriser page (copies of v13's) |
| `sheet.py` -> `sheet.png`, `contrast.png` | every card state 1:1 (720-wide scale) on a dark background, some on light, with chips; alternatives A / B over two film frames. `contrast.png`: the cards on S02, S04, S18, S19 (darkest) and S08, S14, S09, S16, S24 |
| `on_film.py` -> `on_film.png` | 12 moments over clean draft frames (finish.py's `comp_frame`, no captions) |
| `demo.py` -> `demo.mp4` | 53.33 s, 720x1280, cards over the draft frames, film captions, `mix_ohm_v2.wav`, CRF 20 |
| `facecheck.py`, `check.py` | face-check sheets in `tmp/`; title-mark equality and timing |
| `cache/`, `tmp/` | raster cache and working files (safe to delete); `tmp/cards14_paper.py` is the first, paper-coloured version |
