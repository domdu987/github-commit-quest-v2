# Scene tricks: transitions, overlays, gags, effects

The rules in brief:

1. Join shots with smoothstep cross-dissolves (four of five joins, 11 frames by default, 9 for quick continuity, 13 to 17 for a change of place or time). Spend each special join once: 2 or 3 hard cuts on a punch line, 1 or 2 whips, 1 object wipe, 1 white flash, 1 punch-in with speed lines.
2. Characters never streak or blur. Only the set streaks, and only on frames where the camera moves more than 60 px per frame at the frame corners (`STREAK_MIN`).
3. Every change of face is a swap on the closed frame of a 3-frame blink, with an optional 2-frame squash of 0.03 D. Never tween two face drawings.
4. The cartoon overlays are few and fixed: sweat drop, purple face with steam, laugh tears with blush, sleep Z, hair on end, focus lines, stubble with a cobweb, eye glint, a brightness dip. Each appears in one to four places per clip. Never draw impact stars, speech bubbles, vein marks, question marks or exclamation marks.
5. The story is told by props that change state on the beat word: a line that grows and is rubbed out, a label slapped on and pinned, a sign that spins, a paper that is stamped. Each prop event gets one sound.
6. Explain a mechanism by turning the familiar object into a small machine (the map becomes terrain, the storm a spinning disc). Keep it warm, close and short: the reference never holds a flat chart.
7. Plan callbacks at plan time as named framings: the same camera and marks, the same place in frame, with only the light or one prop changed.
8. A device must be big enough to read on a phone: text 180 px wide to be recognised and 400 px or more to be read, a reacting face 250 px or more, an effect at least 0.1 D on a head of 300 px or more.
9. Time every accent at least 6 frames before the outgoing dissolve starts. An accent inside a dissolve is lost.
10. One gesture per shot, about one snap per shot (18-24 in 65 s; A 36, B 22), a framing change every 1.2 to 1.5 s. A reaction gets its own frame (0.4 to 1 s), not a corner of a wide.

Pictures (all from film 1: the sharp v1.1 graded frames without captions, the picture of the delivered `film_v1_1_sharp_thai.mp4`; each tile names the device, the film frame and the take). Any softness in a tile is the motion streak of a fast camera move (section 2.5), never a depth-of-field blur:
- `../../assets/bible/scene_tricks_transitions.jpg`: every special transition and the 2D overlays.
- `../../assets/bible/scene_tricks_characters.jpg`: character effects.
- `../../assets/bible/scene_tricks_set_gimmicks.jpg`: props and set gimmicks that carry the story.

Units: px at 720x1280, y from the top. D = head diameter = 1 scene unit. Frames at 30 fps. "g" = 0-based film frame. "Clock" = narration clock; film time = clock + 0.100 s, so an event at clock x is on g = round((x + 0.1) x 30). "Corner speed" = the largest displacement the camera gives a frame corner in one frame. Paths are relative to the skill's `pipeline/` folder unless they start with `__PROJ__` (the project, not bundled).

---

## 1. Reference (measured)

Clip A has 16 shots in 65.2 s and clip B 22 shots in 64.9 s. Both are 720x1280 at 30 fps. Frame names: `a/t16.0` = clip A at 16.0 s; `a f1322` = clip A frame 1322.

### 1.1 Transitions

| Transition | Clip A | Clip B | Length | How it is made |
|---|---|---|---|---|
| Cross-dissolve | 11 | 18 | A 9 to 17 frames, median 13; B 9 to 23, median 10.5 | Smoothstep mix, not linear. Measured mix per frame at A f346-357: .02 .07 .14 .22 .35 .47 .60 .72 .82 .90 .95 .99 (a 12-frame smoothstep within 0.04). Both shots keep moving through it; the incoming shot is already moving on its first visible frame. |
| Plain hard cut | 1 (f1322, 44.07 s, into the smug two-shot) | 1 (f93, 3.10 s, into the inventor's first line) | 0 | Each lands on a line that hits like a punch. |
| Punch-in cut with speed lines | 0 | 1 (f146-147, then held close 0.40 s) | cut, lines over about 10 frames (f146-156) | A cut to a tighter framing of the same face, thin white radial streaks redrawn every frame. |
| Whip pan | 0 (one whip-off inside shot 5) | 1 (f160-166) | 7 frames | Picture shifts 40 to 190 px per frame; sharpness falls to 0.38 of normal. |
| Object wipe | 1 (the train crosses the lens, f111-113) | 0 | 3 frames | A large foreground object fills the frame. |
| Cut hidden in a fast tilt | 1 (f276-277) | 0 | inside the move | The cut sits on the blurred frames of a tilt. |
| White flash | 1 (f1930-1934, the explosion) | 0 | 5 frames to white | Layered over an unchanged background. |

Totals: 29 of 36 transitions (81 percent) are dissolves. The framing changes every 1.19 s (median) in A and 1.26 s in B when dissolves, cuts and snaps are counted together (means 1.25 and 1.54 s).

The longest dissolve in each clip carries the biggest change of mood: A 17 frames into the calm vista before the catastrophe (shot 14); B 23 frames into the last shot.

### 1.2 Camera-borne devices

| Device | Measured | Where |
|---|---|---|
| Motion blur (streak) | Only on fast camera moves: whip, crash zoom, fly-in. Rule of thumb: the plate streaks when it travels more than about 40 px per frame. Fly-in A f296-312 has radial streaks (horizontal gradient energy 0.47 to 0.54 of vertical). | B f159-166, A f296-312 |
| Characters stay sharp | Sharp while moving about 250 px per frame. | A f1736-1740 |
| Snap | A 36 snaps (median 24.5 frames), B 22 (median 13.5); scale x1.5 to x3 or the inverse, often with 150 to 700 px of pan. Fastest peak corner speed 5851 px/s (A f1740), 6811 px/s (B f26). | throughout |
| Camera shake | One shot: the sweating passenger, about 5 Hz, 12 px per frame standard deviation, 86 px peak to peak, 1 to 1.5 s. | A f894-930 |
| Focus lines | 25 to 35 white wedges 1 to 3 px wide, 60 to 250 px long, pointing at the character, over the background, redrawn every frame, 10 frames. | B f146-156 |
| Brightness dip | Whole frame value x 0.75 for 0.4 s on one dramatic line. | b/t03.3-t03.7 |
| Holds | Fully static frames are 4 to 6 percent of the reference; holds of 6 frames or more total about 1 s per clip. A 0.4 s hold before the crash pull-out in A shot 13 (0.47 s). | A shots 10, 13 |

### 1.3 Drawn effects on characters

Geometry in D of the head, origin at the head centre, y down. Colours as #rrggbb.

| Effect | Geometry | Timing | Seen at | How often |
|---|---|---|---|---|
| Sweat drop | Teardrop 0.075 x 0.115, stroke 0.014, lighter blob on its left half; fill `#b6e3ff`, light half `#def9ff`, outline `#5c647a` (slate, not ink); at (0.33 x sign of yaw, -0.12), straddling the outline, under the hat. | Appears with the expression (shocked, worried). | a29.0, a29.5, a33.5, a37.0, a47.0, a54.0, b04.5, b05.0, b35.5, b39.0 | 10 of the sampled stills: the most common effect |
| Purple face | Radial gradient centred (-0.07, -0.09), r 0.56: `#b769e1` 0, `#a152cd` 0.55, `#7c35a8` 1; arc highlight r 0.40 from 188 to 228 deg, stroke 0.012, `#f0b2ee`. | Rises from the chin like liquid in 8 frames, with a 0.02 wavy surface band `#d49ff9` and three ring bubbles. | a17.0 to a19.5 | once (clip A, the boss) |
| Steam | Puff = 5 overlapping circles r 0.045 to 0.065, `#fffeff` over the same circles 0.014 larger in ink, underside `#e3e3f5`; three per side: (-0.36, -0.11) (-0.49, -0.24) (-0.57, -0.42) and (+0.56, -0.14) (+0.67, -0.29) (+0.75, -0.50). | Spawn the inner puff, move each to the next position over 6 frames, fade the outer one; loop while the anger lasts. | with the purple face | once |
| Laugh tears | Ellipse 0.11 x 0.06, fill `#b8e4dc`, stroke `#383f36` 0.012; chains of 2 or 3 from the outer eye corners, each 0.8 x the last; plus pink blush. | Fade over 4 frames. | b06.0, b06.5, b07.0, b24.0 | 2 places (clip B) |
| Sleep Z | Bold italic Z, fill `#dbd1fa`, outline `#221a3f`; three on screen 0.33 apart, zig-zag +/-0.1. | Rise 0.5 D/s, grow from 0.10 to 0.13, a new one every 0.65 s, fade in at the bottom and out at the top. | b33.0 to b34.0, on a close-up (head 389 px at b33.5) | once |
| Hair on end | 8 or 9 ink strokes 0.25 to 0.3 long, 0.035 thick, fanned over the top half of the head. | Held 10 frames while the body jumps 1 D and lands. | b f1084-1094 (head only 111 px, so +/-20 percent) | once |
| Stubble and cobweb | 60 to 80 dark specks on the lower third of the face plus a cobweb. | A "weeks later" gag. | b18.5, b19.0 | once |
| Eye glint | One 2 px light dot in each pupil. | Dark close-up only, never in daylight. | b42.0 | once |

Not found in either clip: impact stars, speech bubbles, vein or anger marks, question or exclamation marks. The spec adds: the reference has no musical-note glyph, so a whistle is drawn as a mouth shape only.

### 1.4 Character timing devices

| Device | Measured | Where |
|---|---|---|
| Blink | Half (almond 0.22 x 0.08 D), closed (line), half, one frame each, 4 to 5 frames in all. Every 0.7 to 1.2 s in close-ups, about every 2 s otherwise, and at every change of thought. A talker can go 1.8 s without one. | a f1651-1655, a f1669-1673 |
| Expression swap | Hidden behind a blink: the new eyes and mouth are there when the eyes open. During lively speech every 10 to 12 frames (B 3.07 to 4.53 s); in the A close-up every 0.6 to 0.73 s. One to three swaps per second during a reaction. | a f1646, b f98-142 |
| Squash on the swap | Optional 2 to 3 frames of 0.03 D. | spec |
| Jump scare | Squash blink 2 frames, leap 2, hang 2, land 2. | b f1080-1088 |
| Entrance | Pop up or slide in from the frame edge over 4 to 8 frames, then small nods. | spec 5.5.7 |
| Gesture | One per shot (raise, point, wipe), eased over 8 to 10 frames, timed to the caption word. | spec 5.5.8 |
| Listener freeze | The speaker moves (a lean or nod every 1.0 to 1.5 s, head 0.15 to 0.30 D sideways); the listener moves under 0.04 D, blinks only. | a f1380-1435 |
| Lip sync | A new mouth every 1 to 3 frames (about 7 per second, measured 4.9 to 9.8), driven by loudness, biggest shape held up to 4 frames. | a f1399-1402 |

### 1.5 Props, text, gags, metaphors, reactions

- **How props enter.** A prop insert is shown by pushing into the real prop (0.3 x to 1.4 x of frame area in about 12 frames) and whipping back out, or as a full-frame drawing moved with pan and zoom. A paper is held up to the lens until its printed words fill the frame (a/t31.5 to t32.5). Fireball, dust plume and steam are layered effects over an unchanged background (A f1928-1940, B f1400-1456).
- **Text as a joke or a clock.** All text is in clip A and all of it is correct, typeset and never garbled: the newspaper "The Red Mesa Herald" (paper `#fdefd7`, ink `#937c5e`), the nickname banner "THE CLICKETY CLACK LINE!", "FIRST LINE IN GETS IT ALL!", the wall calendar "CALENDAR for the Year 1880 / MAY" with the right day grid (header `#c82928`, page `#faf3f1`, month `#db5d66`), signs ("ALL ABOARD!", cream board, red slab capitals, four corner nails). One or two lines are large and legible, everything else is greeked. A featured banner's cap height is about 11 percent of the frame width. The calendar and the newspaper carry time jumps; the nickname is held up to the lens as the joke. Clip B has almost no text, only pictograms.
- **Running gags and callbacks.** The formula (`references/story-formula.md`) has a mocking nickname used as a running thread and a running object the viewer watches change. Clip A answers its shot 5 boss-and-hero framing with the shot 11 two-shot (the plan's reading). Clip B sets up "not even a ripple in the emperor's wine" (a goblet, crash pull-out x0.10, B shots 7 to 8) and laughs twice ("laughed even harder"). The stubble and cobweb gag marks weeks passing.
- **Visual metaphors.** The mechanism is shown on the thing itself, as a small machine: B shot 19 is one 6.53 s rotating top-down take inside the jar that shows each part as the narrator names it (pendulum, then low and close on the part that acts); A shot 10 tests the rail gap (a coin fits, paper barely, a/t39.0 to t43.0); A shot 12 travels along the rail as a point of view (a/t48.0 to t51.5).
- **Reaction shots.** B shot 3: the inventor shocked in close-up for 0.40 s with speed lines, then a whip pan. B shot 4: the court laughing, 1.80 s, pull back x0.56. A shot 13: the hero's wide eyes, push x1.92, a 0.47 s hold, then a crash pull-out x0.27. A shot 11: the near hero frozen with blinks while the boss talks. Extreme close (390 to 440 px head) is the reaction beat, 0.4 to 1 s.

### 1.6 Sound that goes with the devices

Not measured per device. What is measured (`references/audio.md`): whooshes peak -19 to -10 dBFS, impacts about -9 peak, scratches and rubs -27 to -24 RMS, ambiences -34 to -30 RMS with peaks near -14; nothing but the voice over -10 peak while the voice speaks. Effect cadence target: about one point effect every 2.5 to 3 s.

---

## 2. Our build (film 1)

### 2.1 Transitions of the conform

Code: `v3/film/out/conform.py` (`joins()`, `build()`). Each take's `meta.json` declares `transition_in` as `{"type", "frames"}`; `type` is `dissolve`, `cut`, `hard_cut`, `hidden_cut_in_whip`, `punch_in`, `wipe` (or `object_wipe`) or `flash`. `gb` = first frame of the incoming take.

Exact rules:
- **Dissolve L:** mixed frames `gb - L//2 .. gb - L//2 + L - 1`; weight of the incoming take `smoothstep((g - a + 1) / (L + 1))`, a = the first mixed frame. Both takes render handle frames over that range. Weights for L = 11 (run): .020 .074 .156 .259 .376 .500 .624 .741 .844 .926 .980. A missing handle frame is extended in 2D from the last two frames' fitted camera motion (it ran on 0 frames in film 1).
- **Hard cut, hidden cut, punch-in:** a straight cut on `gb`. The punch-in's speed lines live in the incoming take.
- **Object wipe (6 frames):** `gb - 3 .. gb + 2`; a 2D foam sheet (`foam_wipe`) crosses left to right: leading edge `-0.2 + 1.75 x smooth(u / 0.62)`, trailing edge `-0.75 + 1.95 x smooth((u - 0.38) / 0.62)` (fractions of the width, u = (i + 0.5)/6), both leaning 0.22 W from top to bottom with scalloped sine edges; colour `#c7afde` to `#eef2fe` over cloud noise with bubble rings, a bright crest glow 18 px at the leading edge, a spray trail behind; the outgoing take shows ahead of the sheet, the incoming behind it. Full cover on the two middle frames.
- **White flash:** a lerp to white `0.15, 0.35, 0.60, 0.85, 1.00` on the last 5 frames of the outgoing take (`gb-5 .. gb-1`) and `0.85, 0.55, 0.30, 0.12` on the first 4 of the incoming.
- **Grade across joins** (`v3/film/out_v11/grade.py`): per-take settings cross-fade with the same smoothstep weight over each dissolve, linearly over the wipe and the flash, and switch on hard cuts.

The 23 joins plus the two inside the hook (frames are film frames):

| # | Join | gb | Done | Frames mixed | Why there |
|---|---|---|---|---|---|
| hook | shot 1 > 2 | - | in-take reframe: 14-frame pull-out that swings round the hero | g33-47 | no cut: the insert becomes the low angle |
| hook | shot 2 > 3 | 73 | whip pan: `whip_off` 4 frames (34 deg, quadratic ease-in, g69-72), cut on g73, `whip_on` 7 frames (30 deg, quartic ease-out, g73-79); whole frames streaked | - | the joke turn ("and the boss rubbed it out") |
| 1 | hook > s04 | 129 | dissolve 12 | 123-134 | flash-back |
| 2 | s04 > s05 | 199 | cut hidden in a whip-tilt (both takes carry the streaked whip frames) | - | from the calendar to the map |
| 3 | s05 > s06 | 271 | dissolve 13 | 265-277 | |
| 4 | s06 > s07 | 336 | dissolve 10 | 331-340 | |
| 5 | s07 > s08 | 401 | dissolve 15 | 394-408 | change of place (beach) |
| 6 | s08 > s09 | 505 | dissolve 13 | 499-511 | change of place |
| 7 | s09 > s10 | 610 | dissolve 9 | 606-614 | quick continuity |
| 8 | s10 > s11 | 694 | dissolve 9 | 690-698 | quick continuity |
| 9 | s11 > s12 | 792 | dissolve 11 | 787-797 | |
| 10 | s12 > s13 | 839 | punch-in cut; 46 white speed lines over g839-844 in s13 | - | the nickname lands |
| 11 | s13 > s14 | 868 | dissolve 11 | 863-873 | |
| 12 | s14 > s15 | 956 | match dissolve 13, paper to paper | 950-962 | change of time; the forecast becomes the newspaper |
| 13 | s15 > s16 | 1013 | dissolve 13 | 1007-1019 | change of place |
| 14 | s16 > s17 | 1086 | dissolve 14 | 1079-1092 | change of place |
| 15 | s17 > s18 | 1123 | hard cut, 3 frames before the quote | - | the whistle stops dead on the cut |
| 16 | s18 > s19 | 1189 | match dissolve 12 inside the crash push into the map | 1183-1194 | the map behind the chief becomes the frame |
| 17 | s19 > s20 | 1419 | dissolve 9 | 1415-1423 | |
| 18 | s20 > s21 | 1516 | dissolve 10 with the whip pull-out | 1511-1520 | |
| 19 | s21 > s22 | 1571 | dissolve 14 | 1564-1577 | |
| 20 | s22 > s23 | 1664 | dissolve 17, the longest, matched from the arrow tip on Long Island to the shore | 1656-1672 | calm before the catastrophe (as A's 17) |
| 21 | s23 > s24 | 1720 | hard cut, 3 frames before 'มันคือ' | - | the wave |
| 22 | s24 > s25 | 1788 | object wipe 6: the foam sheet | 1785-1790 | the wave crosses the lens and clears to the map |
| 23 | s25 > s26 | 1873 | white flash 5 in, 4 out (lightning key of s26 decays under it) | 1868-1876 | the impact |

Counts: 17 dissolves (9 to 17 frames, median 12) = 71 percent of the 24 real transitions (reference 81); 2 hard cuts; 1 whip; 1 hidden cut; 1 punch-in; 1 wipe; 1 flash; 1 in-take reframe. Film 1 used every special transition of both clips at once (7 against A's 4 and B's 3). Framing change interval: mean 1.26 s, median 1.22 s by the plan; the review's picture tool read 1.06 s, faster than A (1.39) and B (1.62) on the same tool.

Popcheck rule for joins (`v3/shots/popcheck.py`): mean absolute difference at 180x320 larger than 1.8 x both neighbours. In film 1 it flagged only the two planned hard cuts (g1123, g1720) and one pop inside s19 (g1255, see section 6).

### 2.2 Overlays

| Overlay | Where made | Parameters | Frames | Shot | Sound (plan / placed in the mix) |
|---|---|---|---|---|---|
| Speed lines, punch-in | take post `__PROJ__/v3/film/s13/shot.py` `speed_lines()` (bundled: `v3/film/s13/shot.py`) | 46 white radial wedges centred on the label, alpha `(1 - i/6)^1.3`, retreating outward | g839-844 (6 f) | 13 | punch-in whump / placed: none (the label slap thump_jab at 28.10) |
| Speed lines, launch | conform `speed_lines(img, 360, 470, st, seed=1000+g, n=42, r_in=230, retreat=0.6k)`, k = (g - 1442)/30, st = 0.55 x smooth((g - 1441)/4) x (1 - smooth((k - 0.55)/0.45)) | centre = the corridor vanishing point | g1442-1472 | 20 | cannon thwump and slingshot twang / placed: thump_jab -13 peak at 48.10 |
| Speed lines, crash pull-out | conform, `(330, 520)`, n 40, r_in 300, strength 0.45, retreat 0.5k | | g1730-1748 | 24 | crash whoosh out / placed: covered by wave_roar from 58.10 |
| Focus lines | conform `focus_lines(img, 300, 470, 300, 330, k)`: 70 dark-ink wedges `#181228` from the frame edge to an ellipse 300 x 330 px round the two faces | strength 0.85, 0.70, 0.45 | g1720-1722 | 24 | two gasps / placed: thump_jab -11.1 "orchestra hit" at 57.35 |
| Puppet focus lines | `fx={"type": "focus_lines", "seed": g, "n": 30}` (white streaks 0.85 to 2.7 D round the figure); `acting.beach_shocked(..., focus=True)` gives 3 frames | | 3 f | 24 | - |
| Rain strokes | in the take: beach `B.set_rain(0.35)` | | whole shot | 16 | drizzle bed / placed: rain_drizzle and beach_calm |
| Note glyphs | in the take's sprite overlay: `acting.note_glyphs_svg(pose["_notes"], origin=mouth_anchor, facing=facing)` (signature `note_glyphs_svg(notes, origin=(0.25, -0.1), facing=1, ink="#3a2832", fill="#3a2832")`) | rise 0.9 D, drift 0.5 D ahead over 1.1 s, rocking, fade in the last 0.3 s; ink `#3a2832` | leave the mouth at g1098, 1107, 1116 | 17 | whistled tune / placed: whistle_tune -14 peak |
| Wake streak | in the takes: `M.set_wake(head_u, length_u, alpha)`, red-hot, glowing | s21: 0.24 u long | whole shots | 20, 21 | doppler roar / placed: wind_storm ambience |
| Wake streak, shot 25 | left out (needs a per-frame track of the spinner) | | | 25 | - |
| Ink blot | in the take: a lit map decal (`__PROJ__/v3/film/s25/make_blot.py`, not bundled): blue splat with fingers and droplets east of the N.Y. dot | grows to 0.5 D in 5 frames | from g1862 | 25 | impact boom and ink splat / placed: thump_jab -12 at 62.08 |
| Foam wipe, white flash | conform (2.1) | | g1785-1790, g1868-1876 | 24-26 | wave crash; flash hiss / placed: rain_drizzle "crash" bed at 59.55; flash: none |
| Fog bank (grade) | `v3/film/out_v11/grade.py` stage 6: band `#c9bfd0` on the horizon, y 600 to 612, 40 to 120 px tall over g1677-1719 (smoothstep), fade-in g1671-1681, alpha peak 0.80, x-modulation +/-16 percent, behind near objects by a colour matte | | g1671-1719 | 23 | brass and breath swell / placed: riser_tension -16 at 55.79 |
| Camera streak | `v3/shots/post.py` (2.5) | | fast frames | many | - |

### 2.3 Set gimmicks

Every setter takes `frame=None` (set statically) or `frame=N` (key it). Office props: `X` = `v3/set3d_ext/props/office_props.py`; set: `S` = `v3/set3d/office3d.py`; light: `OL` = `v3/set3d_ext/light/office_light.py`; mechanism: `M` = `v3/set3d_ext/mech/office_mech.py`; beach: `B` = `v3/set3d_beach/beach3d.py`, `BX` = `v3/set3d_ext/beach/beach_ext.py`; kitchen: `K` = `v3/set3d_kitchen/kitchen3d.py`. "Placed" names the library sound the mix actually used (`v3/film/out/SOUND.md`); "none" means the plan wanted a sound the library did not have.

| Gimmick | Call | Parameters and timing | Shots (g) | Sound: plan / placed |
|---|---|---|---|---|
| Window-bar shadows (the reviews call them blind shadows) | `S.build("INTERIOR_DAY")`: one sun `key_sun` through the glazing bars | sun angle 0.45 deg, bars 5 to 8 D from the surfaces they shadow, edge median 5 to 10 px, max 22 px; gone in `office_grey` and `office_storm` (no shell shadow) except on lightning frames | every office_day shot (1-14) | - |
| Lamps that glow | set bulbs; `OL.apply(preset)` | bulb emission 6 (day), 8 (grey), 12 (storm); banker lamp slit 3.6; bloom halo 16 to 24 px beyond the core; the v1.1 grade adds bloom on sources | office | lamp hum in the office bed / office_tone |
| The red line, grown and rubbed out | `S.set_track(line, erase)` | line 0..1 grows from the storm to N.Y. (arrow head over 0.97..1); erase 0..1 removes it from the N.Y. end (arrow head gone at erase 0.06), leaving a faint pink smudge and a pink ghost arrow head. Hand-drawn stroke 0.038 D wide, wandering up to 0.15 D from the chord (`TRACK_STYLE = "hand"`, client decision) | 1-3 (drawn g7-60, erased 3.03-3.97 s in six strokes, one every 5 frames), 9, 10, 11 | pencil scratch / map_marker, pencil_scratch; eraser strokes / eraser_rub |
| Eraser smudge halo | `X.set_smudge(level)` | 0..3: 1 = N.Y. end, 2 = upper half, 3 = whole line | 11, 12 | - |
| Eraser crumbs | `X.set_crumbs(amount)` | 70 pink crumbs on the chalk ledge, revealed in a fixed order | 11d, 12 | crumbs pattering / none |
| Redrawing (the line drawn again) | hand card + `acting.hero_redraw(t, t0, swipe=8, ..., stub=True)`; `S.set_track(1, erase)` back to 0 | one 8-frame sine swipe with a small overshoot; pencil stub at prop scale 0.6 | 11 (23.75-24.30, 25.25) | zip / pencil_scratch -27.5 RMS at 18.40 |
| Calendar leaf | `X.set_calendar(day=20, lift, flutter, tear)` | leaf hinged at its top edge, two shape keys; alternate lift and flutter for the draught at 5.6 s; `day=21` = pad only (WEDNESDAY) from shot 17 | 4 (g171), 17, 18, 25 | date-stamp clunk, leaf flutter / none |
| Teletype feed | `X.set_teletype(feed, stamp, yaw_deg=-45)` | forecast art at half size rising out of the slot (z 1.88); a shader clips below the slot | 14 (28.95-29.80) | teletype clatter / teletype -33.7 RMS |
| Rubber stamp | `X.set_stamp(loc, face_dir)` (0.17 D, scale 2 matches the full sheet); puppet prop `stamp` | ready above, anticipation lift, 4-frame cubic-in drop, contact g898 (29.82) | 14 | stamp thump / none |
| Forecast sheet | `X.set_sheet(..., pop1, pop2, bow)` | 1.08 x 1.40 D quad, 2048 px; each typed word pops 1 -> 0 over 4 frames = scale 1.08 plus ink bloom, as it is spoken (30.85, 31.30); alternate small `bow` values to tremble | 14 | typebar clack and bell / none |
| Storm spinner | `X.set_spinner(u or xz, angle, wobble, squash, fast, pin_out, show)`, `X.spinner_angle(t)` | red spiral disc 0.16 D on a brass pin, 0.022 D proud, hard shadow; 0.5 rev/s with 3 deg wobble; thumb pushes `pin_out` 0.025 -> 0 over 3 frames; `squash` keeps area (0.82 under the pointer whack; 0.7 x 1.25 pinched); `fast` 0..1 blends a rotation-blurred disc (0.95 to 1 at speed) | 5 (pinned g218), 6, 19-22, 25 | pin thunk, ratchet whirr / none |
| Spinner sweat and pulse | `M.set_spinner_fx(ring, ring_pulse, drop, drop_slide)` | isobar ring card scale x(1 + 0.25 pulse); one sweat drop running 0.06 D down the disc | 19 | squeak / none |
| Pointer whack | `acting.boss_pointer_whack(t, t_land, ...)` | raise, 3-frame whack, contact squash, rebound | 6 (lands g319), 18 (two taps make the label swing) | pointer whack / none |
| Chalk curve | `X.set_chalk(grow, crumble, alpha, head)` | white dashed curve 0.020 D wide, dashes 0.055 D; arrow head rides the tip (key every frame while it grows); bends north-east at `CHALK_BEND`; `crumble` 0 -> 1 and alpha 1 -> 0.45 at 43.70 in shot 19 | 7 on | chalk scratch with a slide whistle / pencil_scratch -26.1 RMS |
| Ghost tracks (the fan of old storms) | `X.ghost_fan_keys(f_first, every=3)`, `X.set_ghost(i, grow, alpha)` | six faded grey-blue tracks, one every 3 frames, flash to 0.75 then settle at 0.35; small arrow heads in the last 3 percent | 7 (12.40-13.00) | six fwips as a xylophone run / none |
| Tick stamp | `X.set_tick(alpha, scale)` | 0.20 D impression; scale 1.25 -> 1 = the thunk | 7 (12.95) | rubber-stamp thunk / thump_jab -12 |
| Ruler slap | `X.set_ruler(on)` | 1.30 x 0.11 D maple, no lettering; key 0 -> 1 for the slap-on, 1 -> 0 for the whip-off (lifts 0.45 D, swung and tipped) | planned 9, 11 (film 1 used no ruler in the end: hand-drawn line) | ruler thwack / none |
| The pinned label (nickname) | `X.set_label(show, tilt_deg=4, swing_deg, away, scale, curl, flutter, pin, pin_out, res="hi")` | cream strip 1.15 x 0.34 D, Thai brush 'ทางด่วนพายุ', red pin at `LB_PIN`; `away` + `scale` = the slap (flies in from 0.30 D right, 0.22 D off the wall, scale 1.10); rocks 4 deg for 2 frames; one corner curls; flutter 0.35-0.75 in the storm; whips 16 deg on its pin at the impact, damped | 13 (slap 28.00, pin 28.25), 17, 18, 19-22, 25 | paper slap, pin thunk, wah-wah / thump_jab -12 at 28.10 |
| Pressure walls rising from the map | `M.set_wall(side, rise, slide, lock, fade, pulse)` | four terraces 0.125 D each (wall 0.50 D), key `rise` 0 -> 4 over 18 frames for four thuds; `slide` 0 -> 1 = the squeeze (0.15 D inward); `lock` 0 -> 1 = vertical corridor face with the H stamped on; `pulse` = height x(1 + 0.15 pulse) (lock boom, the reveal at 53.62); `fade` 0..1 sinks them to outlines (shot 22) | 19 (41.0-42.2, lock 43.20 W, 43.60 E), 22 | eight thuds, two wall booms / thump_jab -11 at 43.30 |
| Lane | `M.set_lane(grow, red, fuse, alpha, glow)` | unrolls north 44.4-45.1; glow 0.9 at hum-on, 0.2 after; shot 22 keys `red` 0 -> 1 then `fuse` 0 -> 1 (dashes turn red and fuse into the pencil line) | 19, 22 | road zip, neon hum / none |
| Compass | `M.set_compass(show, ping)` | ping = scale x(1 + 0.35 ping) | 19 (45.15) | ping / none |
| The corridor view | `M.cam('corridor_cam')`, `M.corridor(u_lens, h, look_u, look_h, a='auto')` | lens 0.35 D above the paper, 0.155 D west of the chord (compute `M.clear_lateral` once per shot), up = wall normal; walls tower 0.15 D above the lens | 9c, 19, 20, 22 | engine rev under the swing / none |
| No-turn signs | `M.set_picto(side, show, scale=0.5, s=0.22, h=0.30, yaw_deg, wobble_deg, tilt_deg)` | 'E' no right turn, 'W' no left turn, popped with a 1.25 overshoot and decaying wobble on each bonk | 19 (bonks 46.45, 46.85) | bonk and sign pop / thump_jab -14 at 46.55 |
| Wind arrows | `M.set_wind(progress, amount, span)` | 14 pale arrowhead cards up the corridor; `progress` advances about 0.9 per second in a gust; `amount` 0.33 / 0.66 / 1 = three waves (g1425, 1434, 1443) | 20 | three gusts rising / wind_storm bed, thump_jab on gust 3 |
| Spinner launch | `X.set_spinner(..., squash, wobble, fast)` | third gust squashes it flat (g1440-1443), then it rockets north tall and leaning (squash 1.47 -> 1.12, wobble 16 deg, blurred disc) | 20 | cannon thwump / thump_jab |
| Speed sign that spins | `M.set_speed_sign(show, spin_deg, scale=0.8, u=0.62)` | round '100' with Thai 'กม./ชม.'; spins two turns in the wake (ease-out, 22 f), rocks +/-9 deg, settles on 0 or 360 by 50.30 (g1512); read 49.2-50.3 at 420-435 px | 20 | pass-by vwip, ratchet, ting / none |
| The wake | `M.set_wake(head_u, length_u, alpha)` | red-hot streak on the line, thin and faint at the tail, glowing at the head | 20, 21 | doppler roar / wind_storm |
| Ghost storms | `M.set_ghost_spinner(i, s, angle, show, alpha, scale)`, `M.set_shell(show, which=2)`; brighten tracks with `X.set_ghost(k, 1.0, alpha=0.6)` | three grey spinners crawl at a sixth of the storm's speed, overtaken at 50.9, 51.3, 51.7; one carries a snail shell | 21 | three poofs, plodding tuba / none |
| Lightning | office `OL.lightning(f, pattern=(1.0, 0.35, 0.8))` (keys f, f+1, f+2, 0 on f+3; `office_storm` only unless `OL.set_flash_energy`); kitchen `K.set_state(lightning=k)` | a second sun from the key direction, 3.2 x the day key; the window and bars print on floor and wall while it is on; costs nothing at 0. Key flash 0 on the first frame of the take, or every frame renders lit (a bug hit in s25) | 25 (g1872), 26 (g1873-1876, 1889-1894) | thunder / thunder_low |
| Rain on the office window | `OL.set_rain(drizzle, lash, phase)` | 96-frame seamless loops; drizzle = beads plus 26 stick-slip drops; lash = dense drops plus 170 slanted streaks; grey (1.0, 0) gain 0.9, storm (0.35, 1.0) gain 0.55 | 17, 18, 25 | rain bed / rain_drizzle -41.5 RMS (inaudible: see 6) |
| Beach rain and drizzle | `B.set_rain(a)` | about 1300 streak quads in a camera-parented field, 1 px wide, 1.8 to 11 D from the lens; a = density (0.3 drizzle, 1 storm); slant 0.10 + 0.22 x wind rad | 16 (0.35), 24 | drizzle bed / beach_calm, rain_drizzle |
| Drops on a palm | `acting.beach_palm_out(t, t0, drops_at)` | 1-frame dips per drop | 16 (35.50, 35.65, 35.80) | three plips / none |
| Kitchen window | `K.set_state(window=('drizzle'\|'wave', k), crack=k)` | 24-frame drizzle loop; 92-frame wave sequence (one per film frame g1873-1964); crack card from g1923 over 4 frames | 15, 26 | drizzle; pane crack / none |
| Fog bank | `B.set_fog_bank(a)`, `BX.set_fog_near(k)` | ring of radius 300 D; height 30 x a^0.75 D, opacity min(1, 3a); shot 23: 0.06 -> 0.30 on 'ม่านหมอก', then 1.0 with the radius 300 -> 165 D (k 1 -> 0.45). Plus the grade band (2.2) | 16 (0.25), 23 | fog motif / riser_tension |
| The wave | `B.set_wave(p)`; `B.wave_state(p)` | one sculpted wall: toe at y = 17 + 420 (1 - p)^1.7, height 9 + 8p D, curling lip and foam; sunk below p 0.2; at p 1 the crest is 17.5 D, 4.3 x the cottage ridge | 24 | roar / wave_roar -12 peak |
| Wind on the beach | `B.set_wind(w)`, `BX.set_sign_swing(amp_rad)`, `BX.set_vane(deg)` | grass leans, umbrella tilts 0.22 w rad, flag flaps, rain slants; shot 23: wind 0.04 -> 0.59 from 57.0, sign swing 0.02 -> 0.08 rad, vane 35 -> 60 deg | 23, 24 | sign creak, canvas / none |
| Lit windows, banging shutters | `BX.set_windows(k)` (`#2b3150` -> `#ffd995`, strength 1.9); `BX.set_shutters(k)` (each swings to 75 deg, own phase) | | 23 (0.15 -> 0.90), 24 | shutters x3 / none |
| The flying hat | `BX.build(..., boater=True)`, `BX.set_boater(frame, loc, spin_deg, scale, visible, cam)`; drawing `acting.flying_hat_svg('beach_man')`; puppet `hat_off` | s24: leaves the head at 57.52 (g1729); up = 2.6t + 1.6t^2 D, sideways 1.4t + 2.2t^2 D, spin -25 - 420t deg, scale 0.55 | 24 | hat pop / none (the hit covers it) |
| Cobweb and spider | `BX.set_spider(0..1)` | 0.9 D web card between umbrella pole and chair arm; `set_spider(1)` lowers the spider 0.35 D | 8 (from 15.70) | harp pluck / none |
| Towel line | `BX.set_towel(0/1)` | red and cream towel 0.7 x 0.78 D, hidden under 0.5; flaps with wind; key to 1 on the peg frame | 8 (14.0) | towel flap / none |
| Newspaper and cup | `K.set_state(cup, saucer, ripple=(phase, amp), steam, flutter=(t, amp), bleed=k, drop=(x,y,z), chair)` | shot 15: coffee dead still (no ripple), steam; shot 26: rings run outward at 0.9 rad per frame, amplitude 0.85 until the shake ends then 0.25; cup creeps 0.05 D right and 0.17 D toward the lens in jerks with hops up to 0.01 D and +/-3 deg; page flutter 0.006 D, 0.036 D from 63.9 to 64.6; drop lands g1952 on ฝนตก, bleed frames f_00-f_11 over g1952-1963, f_11 held | 15, 26 | cup clink, rattle; flutter; plip and one piano note / paper_slide -28 RMS; the rest none |

### 2.4 Character effects

Puppet: `P` = `v2/puppet/puppet.py`; acting library: `AC` = `v3/acting/acting.py`. Pose keys: `expr`, `blink` (0 open, 1 half, 2 closed), `squash` (float or (sx, sy)), `fx` (list), `mouth`, `tint`, `hat_off`.

| Effect | Call | Parameters and timing | Shots (g) | Sound: plan / placed |
|---|---|---|---|---|
| Expression swap behind a blink | `AC.blinks(t, starts)`, `AC.closed_at(t, at)`; or by hand: blink 1, 2, 1 on three frames, change `expr` on the 2 | every face change in the film | all | - |
| Blinks | `AC.blinks(t, starts)` | half, closed, half; offset between characters; none inside a line | all | blink cue / none |
| The shocked take | hook: `squash = (1 + 0.014 sq, 1 - 0.014 sq)` pulse over SHOCK-1..SHOCK+5, `expr="shocked"`, `fx=["sweat"]`; library: `AC.boss_shocked(t, t_shock, before="smug", drop_pointer_at)` (3-frame blink, 2-frame squash 0.03 D, head pops back 0.08 D, hands flinch over 5 frames); `AC.beach_shocked(..., hat_pop, focus=True)` | swap on the closed frame | 3 (g108), 24 (57.42), 25 (g1863) | eye-pop boing and gulp / pop_surprise -11 (hook); 25: none (impact covers it) |
| Stunned | `AC.hero_stunned(t, t_swap, close_at)` | swap, then eyes shut and head lowered 0.1 D | 25 | - |
| Sweat drop | `fx=["sweat"]` or `{"type": "sweat", "side", "scale"}` | pale drop, slate outline, tucked under the hat | 3, 18 (38.4), 24, 25 | gulp / none |
| Purple angry face | `fx=[{"type": "anger_fill", "level": k, "t": t}]`, level 0 -> 1 over 8 frames; `AC.boss_rub_furious(t, t0, stroke=0.33, fill_len=0.8)`; `AC.boss_frozen_purple(t, twitch_every=0.4)` | wavy surface and bubbles while rising, specular arc when full; eye twitch every 0.4 s | 11c (g739-771) | kettle whistle / eraser_rub |
| Steam puffs | `fx=[{"type": "steam", "t": loop 0..1}]` | three puffs per side from brim height | 11c | kettle whistle / none |
| Laugh, tears, blush | `AC.senior_laugh(t, cast, phase, hz=3, bounce=0.06, roll=15, thumb_at)`; `AC.boss_laugh_doubled(t, lean=25, bounce_hz=4.5, slap_at, pull_strip_at)`; puppet `expr="laughing"` adds `fx=["blush", "tears"]` | held laughing drawing, never flapping; heads rolled 15 deg; bodies bounce 0.06 D at 3 Hz out of phase (0 and 0.5) | 12 | walla, thigh slap / crowd_chuckle -15 |
| Thigh slap | `AC.boss_laugh_doubled(..., slap_at=(...))` | | 12 (g810) | slap / inside the walla |
| Thumb jerk | `AC.boss_thumb_jerk(t, t0, yaw, expr, cast)`; `senior_laugh(thumb_at=...)` | thumb back over the shoulder, held 0.8 s | 9 (17.0), 12 (g801, g811) | three low brass notes / none |
| Pop-in | `Actor.place(frame, feet, scale=s)` with s = 0.35, 0.80, 1.12, 1.06, 0.97, 1.0 on six frames | one after another, 4 frames apart | 6 (g274, 278, 282) | three pop thumps / none |
| Pointer whack, nods | `AC.boss_pointer_whack`; `AC.senior_nod(t, nods_at, depth=0.6)` (pitch 0.6 + 0.05 D dip in 4 frames, back in 6) | | 6 (whack g319, nods g327, g333) | whack, wood-block knocks / none |
| Talk and accents | `AC.boss_talk(t, AC.loudness(t0, t1), base, accents)`; `boss_finger_wag`, `boss_lean_wink(horn=True)`, `boss_mock_search`, `boss_eraser_bounce` | 8.2 to 8.6 mouth changes per second, holds 3 to 5 frames; a new head target at every phrase start | 10, 18 | wink ting, honk / none |
| Held wink | `AC.boss_lean_wink(t, t0, wink_at, wink_len=0.15)` | | 10 (g692-696), 18 (g1184-1187) | ting / none |
| Whistling | `AC.boss_whistle_stroll(t, notes_at=(0.3, 0.6, 0.9))`: HELD `whistling` drawing (eyes shut, brows up, round pucker) + note glyphs | | 17 | whistled tune / whistle_tune |
| Zzz | `expr="asleep"` or `AC.beach_sleep(t, breath=1.3, z=True)`: `fx=[{"type": "zzz", "t": loop}]` | three Z, a new one every 0.65 s, each 0.095 to 0.14 D tall rising 0.70 to 1.70 D above the head point (`puppet._fx_zzz`; no size parameter), so about 16 to 24 px at a 170 px head: use it on close shots (head 290 px and more) or it reads weakly; chest rise every 1.3 s; boater over the eyes (`hat_dx`, `hat_dy`, `hat_rot`) | 8 | snores / none |
| Jump scare and run | `AC.jump_run(t, t_jump, height=0.55, run_speed)`; `AC.run_cycle` | squash 2, leap 2, hang 2 (0.55 D), land 2, then the walk at double rate | 24 (57.73) | jump / none |
| Hand-only shots | hand cards (`AC.hand_canvas`, 512 px per D) pinned to a world tip | the take-A method: the puppet at scale 1.5 facing the lens, body out of frame | 1, 5, 11a-b, 13, 14, 15 | - |
| Tint for night | puppet `tint` (s24 `#b5b5f0` = 0.71, 0.71, 0.94); `OL.tint_cards()` in `office_storm` (0.86, 0.86, 0.95) | ink is not tinted | 24, 25 | - |

### 2.5 Motion streaks and fast frames

- Code: `v3/shots/post.py` (`STREAK_MIN = 60.0` px per frame at the corners, `SHUTTER = 0.40` frames, up to `MAX_TAPS = 48` sub-frame copies). The streak averages the frame along the similarity (zoom + pan) that the true camera of frames g-1, g, g+1 gives the set's reference points, in linear light (power 2.2).
- With actors in frame, each fast frame also renders a `plate/` (set without actor cards) and a `matte/` (actor cards over a holdout set); the plate is streaked and the actors are laid over it sharp. Without actors, or in a whip, the whole frame is streaked. The takes' runners do this automatically (`v3/set3d_ext/beach/bshot.py render`, `v3/set3d_kitchen/kshot.py`, `v3/film/s10/otake.py`).
- Film 1: about 115 streaked frames with actors. Peak corner speeds in snaps 160 to 458 px per frame.
- A card that would cross the lens is hidden on the fastest streaked frame (s09: the three near figures hidden on g539-541 inside the crash push; s11: the full bodies enter inside the snap on g739).
- Reference rule was 40 px per frame; film 1 used 60 so that a follow move keeps its subject sharp.

### 2.6 Camera shake

The takes shake the look-at point (or pitch and yaw) per frame in Python; no Blender keys needed. `v3/stage/camrig.shake(f0, f1, amp_deg=0.45, every=3, seed)` keys random pan and tilt every 3 frames instead (measured in this chapter's test: 0.45 deg gives an offset of 6 to 7.5 px RMS and 10 to 13 px peak from the unshaken view; 0.9 deg gives 12 to 15 px RMS. The docstring now gives these measured values).

| Shot | Kind | Exact rule | Frames |
|---|---|---|---|
| 13 | slap | roll 0.45 deg, then -0.30 deg | 2 (g843-844, the slap `SLAP` = g843) |
| 19 | bonks and wall locks | look-at offset amp 0.012 D (bonks, 6 f), 0.006 to 0.007 D (locks, 5 f), decaying (1 - k/n)^1.2, phase pi x k x 0.95 | 6 each (g1396, g1408) |
| 20 | launch | look-at offset 0.010 x exp(-k/16) D + 0.0025 x exp(-(g - pass)/10) after the sign pass, 5 Hz | g1443 on |
| 22 | landing whump | small, on the pull-out landing | 53.27 |
| 23 | wind | 0.2 deg, two incommensurate sines on yaw (1.7, 2.9 Hz) and pitch (2.3, 3.7 Hz), swelling at 57.0 | whole shot |
| 24 | wave | pitch 3.15 deg x (0.8 sin(2 pi 5 t) + 0.2 sin(2 pi 7.3 t + 1.1)), yaw 1.2 deg x sin(2 pi 5 t + 1.7), ramp in over 4 frames: 77 px peak to peak and 24 px RMS in pitch (computed here) | g1752 on |
| 25 | impact | look-at offset 0.045 x (1 - k/8) D, 5 Hz, x and 0.7 x z, small location wobble | 8 (g1862-1869) |
| 26 | aftermath | 0.028 D x (1 - smooth)^1.3, 5 Hz, decaying to 0 by 64.6 | g1873-1941 |

Film 1 shakes in 8 shots; the reference shakes in one.

### 2.7 Sound of the devices: what film 1 actually had

The library had 18 sounds (`audio/sfx/`: whoosh_fast, whoosh_whip, thump_jab, pop_surprise, eraser_rub, pencil_scratch, map_marker, label_slap, paper_slide, teletype, crowd_chuckle, whistle_tune, thunder_low, riser_tension, shimmer_reveal, wave_roar, plus the beds office_tone, beach_calm, rain_drizzle, wind_storm). The mix placed 52 entries: 16 in the hook, 26 point effects (one every 2.3 s), 10 ambiences. Every impact, slap, bonk, gust, boom and hit used `thump_jab`. With no fitting sound, the plan's tings, dings, bells, wood blocks, slide whistles, harp, rimshot, horn, snores, gasps, steps, cup clinks, shutters, plips, ratchets and the flash hiss were left out (`v3/film/out/SOUND.md`, "Cues with no fitting sound"). Next time, build the library from the cue kinds of the plan before the mix (section 4 lists the kinds per device).

---

## 3. Callbacks: the pattern

| Callback | Set up | Returns | How it is made | Review verdict |
|---|---|---|---|---|
| G, THE GLOAT FRAMING | 10 (day): chief far at `boss_mark`, hero near at `gloat_near` (2.40, -1.70), map and red line at screen left | 18 (grey light, label now on the map), 25 (storm, impact) | the same named camera: `G` = loc (1.55, -4.95, 2.85), look (1.25, -0.40, 2.62), 22 mm; chief head 173 px at (368, 597), hero 244 px at (619, 696), ratio 1.41; `G_prime` = G's position at 30.36 mm (x1.38). Only the light preset and the map's state change. Shot 25 lands in G, not G', because G' crops the hero's face. | lands |
| The label | 13: slapped on with a punch-in and speed lines, pinned | 17 (in the background), 18 (tapped twice, swings), 19-22 (at the far end of the corridor), 25 (flutters, whips on the impact) | one prop with state controls (`X.set_label`); readable 180 px or more wherever it appears, 400 px or more where it is read | lands (all three readings) |
| THE BEACH FRAMING | 16 (grey drizzle) | 23 (bruise-violet sky, fog) | the same camera `beach_shore_eye` = loc (-7.4, 7.0, 2.6), look (22, 5.0, 1.054), horizon 0.47 H | lands in part: the man moved from the centre to the left third and the camera sat lower, so it is felt, not seen |
| The forecast paper | 14: teletype sheet, stamp 'ทางการ', 'ฝนตก' and 'ลมกระโชก' pop as spoken | 15 (newspaper weather box, the same words at the same size; match dissolve 13 frames paper to paper), 26 (last frame: a drop lands on ฝนตก and the ink bleeds) | one artwork used three times (`forecast` art on the sheet, the quad and the newspaper box) | lands strongly |
| THE TABLE FRAMING | 15: the coffee does not ripple | 26: rings race across it, the cup creeps | the kitchen camera `table` | (not rated separately; the ending lands) |
| Running object | the spinner is the storm in every map shot (5-11, 19-22, 25); the eraser against the pencil (3, 10, 11); the whistled tune returns slowed and in minor in 25 (music) | | | |

What makes a callback land, from these four:
1. Name it in the shot plan before any take is made (G, THE BEACH FRAMING, THE TABLE FRAMING), and give the returning shot the same camera name and the same marks.
2. Put the subject in the same place in frame. The beach callback lost its force when the man moved from the centre to the left third.
3. Change one thing the story needs (light from day to grey to storm; the label added; the paper now wet), and nothing else.
4. Keep the shared element readable every time (label 180 px or more; the Thai words 70 px or more).
5. Join the two halves of a paper callback with a match dissolve, paper to paper, at the same size.

---

## 4. Which device for which beat, and how much

### 4.1 Decision table

Film 1 shot numbers in brackets. Sound kinds are the plan's cue kinds.

| Story beat | Camera / join | Overlay or face | Prop or set device | Sound kinds |
|---|---|---|---|---|
| Cold-open odd act | already moving on frame 0; snap push 0.33 s | none (no face, hand only) | the line grows on real geometry | whoosh, pencil_draw |
| The hero's jab | snap push x1.35 | squash and stretch on the jab (anticipation 3 frames) | arrow head completes | jab_impact (about -9 peak) |
| The joke turns ("and the boss...") | whip pan (4 off, 7 on) or hard cut | - | the rub-out (erase in strokes every 5 frames) | whip_pan, eraser_rub |
| Shock | snap push onto the face, 0.4 to 1 s | swap behind a blink, ring eyes, sweat, 2-frame squash; focus lines 3 to 10 frames on the biggest one only | - | pop / gulp, gasp |
| Flash-back or time jump | dissolve 12 to 15 | - | calendar leaf, newspaper, dateline | soft whoosh, flutter |
| Introduce a thing that will matter | fly-in or crash push into the real prop (x3 to x8 in 14 to 27 frames) | - | pin it on screen (spinner pinned with a thumb) | long whoosh, thunk |
| The doubters' pattern ("they always curve away") | snap pull-out to show many | - | repeat the pattern quickly (six tracks, one every 3 frames) | ascending run |
| Authority pronounces | low angle, crane up | pop-in of the group (6 f, staggered 4 f) | pointer whack on the prop | pop thumps, whack |
| Mockery (quote) | low single, snap back into the gloat two-shot, drift push easing to 0 | talk cycle, finger wag, held wink (end it 6 frames before the dissolve) | eraser driven up the line like a toy car | chuckle, ting |
| Persistence by repetition | one take, stepped pull-out, one snap per count | purple face rising 8 frames, steam, eye twitch | erase / redraw states, smudge halo, crumbs, worn props | squeaks, zip, kettle, pant |
| Everyone laughs | eye level over a foreground, pull back 8 %/s with slide | held laughing drawings, tears, blush, bounce out of phase, thumb jerks, thigh slap | - | walla |
| The nickname | punch-in cut, 6 frames of speed lines, 2-frame shake | - | label slapped and pinned, rocks 4 deg | slap, thunk, wah-wah |
| Official document | crash push x3 onto the paper | words pop x1.08 as spoken | stamp, tear, thrust | clatter, stamp, clack |
| False defeat (nothing happens) | dissolve, gentle drift | shrug | still cup (no ripple), drops on a palm | drizzle, plip, clarinet droop |
| Second mockery | hard cut onto the grin, crash zoom-out into the gloat framing (callback) | whistle (mouth only), mock search, horn mime | label tapped so it swings | rimshot, honk |
| Mechanism | one long true-3D take on the familiar object, 3 to 4 snaps | sweat on the object | the object becomes a machine (walls rise, lock, a lane unrolls, signs pop) | thuds, booms, zip |
| Speed | chase view, 5 Hz shake, speed lines | - | wind arrows, wake, a speed sign that spins and settles | gusts, roar, ratchet |
| Comparison of scale | whip pull-out x0.2 | - | the slow ones overtaken (ghost storms) - make them big | poofs, tuba |
| The reveal | crash pull-out x0.27, hold 12 frames, push onto the end | - | the machine sinks back into the map; the lane fuses into the line | dong, marimba |
| Calm before | longest dissolve (17), push 24 %/s easing to 0, 0.2 deg wind shake | stunned behind a blink | fog bank (make it big) | dead calm, chime, brass swell |
| The catastrophe image | hard cut, crash pull-out with tilt, 5 Hz shake | shocked, hat flies, jump and run | the wave, lit windows under it | hit, roar |
| Impact | object wipe in; 8-frame shake; white flash out | shocked swap close enough to read | ink blot, label whips | boom, splat, flash hiss |
| Ending | pull back to the callback framing; push easing to 0; last 12 frames still | - | the paper that was wrong, now ironic (drop and bleed) | silence on the drip |

### 4.2 Dosage

Reference counts (section 1) and film 1 counts:

| Device | Reference per clip | Film 1 | Next film |
|---|---|---|---|
| Dissolves | 81 percent of joins | 71 percent | 75 to 85 percent; cap the special joins at about four |
| Hard cut | 1 | 2 | 1 to 3 |
| Whip | 0 to 1 | 1 (+ the hidden cut) | 1 |
| Object wipe, flash, punch-in | at most 1 each, in one clip | 1 each | 1 each at most |
| Shake | 1 shot | 8 shots | 1 to 3 shots, on the catastrophe and the impact |
| Speed or focus lines | 1 place (B) | 4 places | 1 or 2 |
| Sweat drop | about 10 stills of the 0.5 s sample | 5 shots | the one recurring effect: use it on every worried or shocked face |
| Purple face, Z, hair on end, tears | once each | purple 1, Z 1, tears 1 | once each, on a close shot |
| Expression swaps | 1 to 3 per second in a reaction | | |
| Gesture | 1 per shot | | |
| Snap | 36 (A), 22 (B) | 26 | about one per shot: 18-24 in 65 s, each 13-25 frames; snaps fill 17-44 % of the time |
| Point sound effects | target one every 2.5 to 3 s | one every 2.3 s | the same, with a sound for every prop event that matters |

Rules of dosage (from the measured rules; the per-shot count is inferred from film 1's shots that read best):
- Per shot: one camera accent (a snap or a special join), one gesture, one face change or effect, one prop event on the beat word. Shot 19 stacked about 15 events in 7.7 s and read as a diagram (inferred from the review's "still a diagram").
- An effect lasts as the reference's do: focus or speed lines 6 to 10 frames, a flash 5 frames, a shake 1 to 1.5 s, a brightness dip 0.4 s.
- What the reference never does: impact stars, speech bubbles, vein marks, question or exclamation marks, note glyphs; motion-blurred characters; a tween between face drawings; boiling ink; a dutch angle (one rotating top-down shot only); a flat chart held for seconds; a parked camera (static frames 4 to 6 percent).

---

## 5. Recipes

Snippets 5.1, 5.2, 5.3, 5.4 and 5.6 were run when this chapter was written, against the bundled `pipeline/` (Python 3 with numpy, PIL, opencv; bpy 5.3 as a module for 5.6b); 5.1 to 5.4 and 5.6a were run again in the fact check (the 5.6a pitch gives 76.8 px peak to peak, 24.2 px RMS at 22 mm). 5.5 was run for its numbers only; its Blender calls were not run here. Set `PIPE` to the `pipeline/` folder.

### 5.1 Joins: dissolve, foam wipe, white flash (the conform's own functions)

```python
import sys, numpy as np
from PIL import Image
sys.path.insert(0, PIPE + "/v3/film/out")
import conform as C                         # importing has no side effects; W, H = 720, 1280

def dissolve(A, B, k, L):                   # k = 0..L-1 inside the mixed range
    w = C.smooth((k + 1) / (L + 1.0))       # L=11: .020 .074 .156 .259 .376 .500 ... .980
    return A * (1 - w) + B * w

wipe = lambda A, B, i: C.foam_wipe(A, B, i)          # i = 0..5, A ahead of the sheet, B behind it
FLASH_IN = [0.15, 0.35, 0.60, 0.85, 1.00]            # last 5 frames of the outgoing shot
FLASH_OUT = [0.85, 0.55, 0.30, 0.12]                  # first 4 frames of the incoming shot
flash = lambda img, w: img * (1 - w) + 255.0 * w

A = np.asarray(Image.open("a.png").convert("RGB"), np.float32)   # 720x1280 frames
B = np.asarray(Image.open("b.png").convert("RGB"), np.float32)
out = np.clip(dissolve(A, B, 5, 11) + 0.5, 0, 255).astype(np.uint8)
```
For a whole film, declare `transition_in` in each take's `meta.json` and run `python3 v3/film/out/conform.py`: it reads every take, checks that the takes tile the film, and writes `frames/g_%04d.png` and `work/joins.json`. Change `TAKES`, `N` and the hard-coded overlay ranges in `build()` for a new film.

### 5.2 Speed lines and focus lines on a frame range

```python
for g in range(g0, g1 + 1):                 # e.g. a crash move of 18 frames
    k = (g - g0) / float(g1 - g0)
    st = 0.45 * C.smooth(min(1, (g - g0 + 1) / 3.0)) * (1 - C.smooth((k - 0.5) / 0.5))   # in over 3 f, out over the 2nd half
    img = C.speed_lines(img, cx, cy, st, seed=2000 + g, n=40, r_in=300, retreat=0.5 * k)  # white, toward (cx, cy)
# focus lines: 3 frames on the shocked faces, dark ink, around an ellipse rx x ry
for i, s in enumerate([0.85, 0.70, 0.45]):
    img_i = C.focus_lines(frame[g_cut + i], 300, 470, 300, 330, s, seed=3000 + g_cut + i)
```
Pass a new seed each frame: the lines are redrawn every frame, as in the reference.

### 5.3 The shocked take: swap behind a blink, squash, sweat

```python
sys.path.insert(0, PIPE + "/v2/puppet"); import puppet
SWAP = 10                                   # closed frame of the blink: the drawing changes here
def hero(f):
    shocked = f >= SWAP
    sq = {SWAP: 1.0, SWAP + 1: 0.5}.get(f, 0.0)            # 2-frame squash of 0.03 D
    return dict(expr="shocked" if shocked else "determined", yaw=0.6,
                blink={SWAP - 1: 1, SWAP: 2, SWAP + 1: 1}.get(f, 0),   # half, closed, half
                squash=(1.0 + 0.03 * sq, 1.0 - 0.03 * sq),
                fx=["sweat"] if shocked else [])
for f in range(8, 14):
    fig = puppet.figure("hero", hero(f), "hero")           # fig["svg"], fig["bbox"], fig["anchors"]
```
Library shortcut for any cast member: `sys.path.insert(0, PIPE + "/v3/acting"); import acting; pose = acting.boss_shocked(t, t_shock=0.2, before="smug", cast="boss")`. In 3D the pose goes to `Actor.pose(frame, pose)` (`v3/stage/actors.py`).

### 5.4 The anger take: purple rising, then steam

```python
F0 = 0                                       # frame the anger starts
def boss(f):
    k = f - F0
    fx = [{"type": "anger_fill", "level": min(1.0, k / 8.0), "t": (k % 30) / 30.0}]   # chin to top in 8 frames
    if k >= 8:
        fx.append({"type": "steam", "t": (k % 18) / 18.0})                          # loop while the anger lasts
    return dict(expr="furious", yaw=-0.4, fx=fx)
for f in range(F0, F0 + 30):
    fig = puppet.figure("boss", boss(f), "boss")
```
Library versions: `acting.boss_rub_furious(t, t0, stroke=0.33, fill_len=0.8)` (rubbing with the fill rising) and `acting.boss_frozen_purple(t, twitch_every=0.4)` (frozen, eye twitch).

### 5.5 Pop-in with overshoot, and a prop slapped on (Blender)

```python
POP = (0.35, 0.80, 1.12, 1.06, 0.97, 1.0)    # six frames (s06)
def pop(g, at):
    k = g - at
    return None if k < 0 else (POP[k] if k < 6 else 1.0)   # None = card hidden
# per frame, for each actor that has appeared:
actor.place(g, feet_xyz, scale=pop(g, at))  # v3/stage/actors.py Actor.place keys location and uniform scale
# the label slap (office props): fly in scaled and away from the wall, land, rock, pin
# away = D off the wall toward the room (s13: 0.22 -> 0), scale = slap pop, swing_deg = rock about the pin
X.set_label(show=1, away=0.22, scale=1.10, frame=g_slap - 3)
X.set_label(show=1, away=0.0, scale=1.0, swing_deg=4, frame=g_slap)
X.set_label(swing_deg=-2, frame=g_slap + 1); X.set_label(swing_deg=0, curl=0.3, frame=g_slap + 2)
X.set_label(pin_out=0.025, frame=g_pin - 3); X.set_label(pin_out=0.0, frame=g_pin)
```
Stagger a group's pop-ins by 4 frames and give each a pop thump. Keys from the setters are LINEAR (visibility CONSTANT); key the label every frame if you need eased motion.

### 5.6 Camera shake (a) as the takes do it, bpy-free; (b) with camrig

```python
import math
def smooth(a, b, g):
    u = min(1.0, max(0.0, (g - a) / float(b - a))); return u * u * (3 - 2 * u)
def storm_shake(g, g_start, amp_deg=3.15, ramp=4):          # shot 24: add to the camera's pitch and yaw (deg)
    if g < g_start: return 0.0, 0.0
    e = smooth(g_start, g_start + ramp, g); t = (g - g_start) / 30.0
    return (e * amp_deg * (0.8 * math.sin(2 * math.pi * 5.0 * t) + 0.2 * math.sin(2 * math.pi * 7.3 * t + 1.1)),
            e * 1.2 * math.sin(2 * math.pi * 5.0 * t + 1.7))     # 77 px peak to peak in pitch at 22 mm
def impact_shake(k, n=8, a0=0.045):                         # shot 25: add (dx, dz) in D to the look-at point
    if not 0 <= k < n: return 0.0, 0.0
    a = a0 * (1 - k / float(n)); ph = 2 * math.pi * 5 * k / 30.0
    return a * math.sin(ph + 0.4), 0.7 * a * math.sin(1.37 * ph + 1.1)
```
(b) With keys in Blender, on top of an existing move: `camrig.drift(1, 60, pose0, pose1); camrig.shake(20, 50, amp_deg=0.9, every=3, seed=7)` (0.9 deg gives about 12 to 15 px RMS of offset; 0.45 deg about 6 to 7.5 px).

---

## 6. What the reviews found weak, and the better choice

Sources: the v1 and v1.1 reviews; items marked "seen here" were found while making this chapter's sheets and are not in the reviews.

| Weakness | Where | Evidence | Better choice next time |
|---|---|---|---|
| Ghost storms too small and grey to read on a phone | s21 | review v1 and v1.1, beat 16 "has no readable picture" | Make the compared objects at least about 120 px (the review's fix), give one overtake its own close framing, and a sound for each pass. A comparison of scale needs both things readable at once. |
| Fog bank barely visible | s23 | v1: a faint strip; v1.1 after the grade band: 40 to 60 px, easy to miss | Make the fog the subject of a frame: a quarter of the frame tall or more, ideally from the sea-facing camera (`sea_view`, where a = 1 is about 80 px) with `set_fog_near` pulled in (inferred from the set's numbers). |
| The climax has little reaction | s25 | "the two men barely react" (v1 and v1.1) | Give the reaction its own beat: snap or cut to a close (300 px or more) for 0.4 to 1 s with the shocked swap on screen, then go on. A reaction in a two-shot at 180 to 250 px reads as no reaction. |
| Empty frame | s16, 35.0-35.3 s | the tilt lands on empty grey sky with half a head at the edge | Every frame needs a subject. Time a reveal so the subject enters as the move lands (palm by 35.1 s), or cut those frames into the dissolve. |
| Hard cut lands on the wrong face | s18 g1123 | planned grin close-up opens on a neutral medium shot | The first frame after a hard cut must show the planned expression at the planned size; check it on the contact sheet before rendering the rest. |
| Picture sharpness | every shot | client decision | Sharp picture: no depth-of-field blur (client decision). Depth comes from real 3D parallax, cast shadows, overlap and light. |
| Caption over picture text | s14 g902-925 | typed Thai 'ลมกระโชก' at y 880-960 under the caption for 0.8 s | Keep picture text above y 600 or out of the band y 880-950. |
| Accents lost inside dissolves (seen here) | s10 wink g692-696 inside the dissolve g690-698; s18 wink g1184-1187 inside g1183-1194 | | End-of-shot accents finish before the outgoing dissolve starts (spec: the outgoing dissolve starts at N-6, the last 12 frames are near still). |
| Sleep Z too small (seen here) | s08 g490 | Z letters about 20 px on a 190 px head in a medium shot | To spec (0.10 to 0.13 D), but the reference shows its Z on a close-up (head 389 px). Put the effect on a close shot. |
| Note glyph on the face (seen here) | s17 g1098-1116 | each note is born on the mouth, about 30 px, over the face | The spec says the reference has no note glyph: hold the whistle mouth and let the whistled tune carry it. If notes are used, start them clear of the head. |
| A wall appears in one frame | s19 g1255 | popcheck flag; the land wall should swell | Key every rise frame (`rise` 0 -> 4 over 18 frames) and run popcheck on each take. |
| Full-frame smear | s05 fly-in | "a full-frame smear" at 6.7 s | Streak only the fastest frames; land the fly-in early enough that the subject reads sharp for at least 10 frames. |
| The explainer is a cold diagram | s19-s21, 14.7 s (22 % of the film) | blue 46 to 67 percent, still "a diagram" after the warm grade | Keep explainer beats warm and rich in material from the build (not the grade), shorter, with fewer stacked devices; the reference's explainer shots keep warm light. |
| The water in the window reads as clouds | s26 | "white puck clouds and rain, not water" | Draw a dark wall of water with a clear surface line in the window sequence. |
| Device sounds missing | whole mix | 26 point effects; tings, bells, plips, steps, snores etc. had no sound | Build the effect library from the plan's cue kinds first (section 2.7), and measure each result. |
| Too much shake and too many speed lines | 8 shaken shots, 4 line overlays | reference 1 and 1 | Spend them on the catastrophe and the impact only. |

---

## Sources

Relative to the project (`__PROJ__`) unless marked "pipeline/":
- `spec/LOOK_SPEC.md` (2.8, 2.9, 4.2 steps 6 and 9, 5.2 to 5.5, 7, 8); `spec/camera_motion.md` (transitions, snaps, shake, motion blur, shot tables); `spec/face_expressions.md` (1.6, 1.7, 2.x effect geometry); `spec/production_forensics.md` (text props, transitions); `spec/environment_materials.md` (1.7 text-bearing props)
- `plan/shot_plan.md` (shot table: transitions, acting, props, sound cues, reference frames; Props; Inserts, textures, overlays; Grammar check)
- `v3/film/out/CONFORM.md`, `v3/film/out/conform.py`, `v3/film/out/SOUND.md`, `v3/film/out/cues_all.json`
- `v3/film/out_v11/GRADE.md`
- `v3/set3d/API.md`; `v3/set3d_ext/props/API.md`; `v3/set3d_ext/mech/API.md`; `v3/set3d_ext/light/API.md`; `v3/set3d_beach/API.md`; `v3/set3d_ext/beach/API.md`; `v3/set3d_kitchen/API.md`
- `v2/puppet/API.md`, `v2/puppet/puppet.py`; `v3/acting/API.md`, `v3/acting/acting.py`; `v3/stage/API.md`, `v3/stage/camrig.py`, `v3/stage/actors.py`; `v3/shots/post.py`, `v3/shots/film.py`; `v3/out/QA.md`
- Takes: `v3/film/s04` to `s26` `QA.md`; `shot.py` of s06, s10, s13, s19, s20, s24, s25, s26 (shake, pop-in, wink, speed lines, boater); `s10/meta.json`
- `deliver/QA_film.md`, `deliver/QA_film_v1_1.md`
- Skill: `references/audio.md`, `references/story-formula.md`
- Frames for the sheets: `v3/film/out_v11/graded/g_%04d.png` (the sharp v1.1 frames)
