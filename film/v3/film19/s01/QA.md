# s01 QA: film 19, shot 1 (the hook) -- WORKSHOP shop_bench, DAY

**This is the worked example for every film-19 render team.** Copy `c19.py` into your take folder and read its docstring ("API DIFFERENCES" and "GOTCHAS") first. Then use `shot.py` and `deliver.py` as templates.

## Delivered
- `frames/g_0000.png .. g_0065.png`: 66 frames, 720x1280, 8 spp (H.STATE['samples'] of the WORKSHOP), 2 threads, OIDN. No captions, no audio. (Not in git.)
- `take.mkv`: libx264rgb crf 6, 30 fps, first_g 0, 66 frames, 21.8 MB (no split needed).
- Frame ranges:
  - g 0..56 = shot 1 (plan 0.00-1.91 s).
  - g 57..65 = 9-frame out-handle (WORKER19), rendered in 3D: the push, the arc, the rocking bars and his idle continue.
  - No handle before g 0 (the film opens here).
- `meta.json`: g0 0, g1 57 (exclusive: hard cut to shot 2 at g 57), first_g 0, n_frames 66, transition_in {"type":"cut","frames":0}; also transition_out, events, camera, s/frame, head numbers, frame-diff.
- `cues.json`: 6 cues (film seconds): workshop ambience; the H1's slow brass tick-tock under the whole shot; apron rustle as his arms rise (g 0-11); snap whoosh (g 36-50); a brass "ta-da" chime sparkle (g 37-44); the cut to shot 2.
- `contact.jpg` (16 frames, cyan line = y 880), `QA_AUTO.md` (PASS) + `phone_sheet.jpg`, `framediff.json` (per-pair numbers).
- Scripts: `c19.py` (the film-19 helper), `shot.py` (`probe`, `camreport`, `stills`, `final`; draft and final share one loop), `deliver.py` (final, or `deliver.py draft`). `.gitignore` keeps `raw/ frames/ work/` out of git.

## Shot (what the viewer sees)
| g | beat | caption (event g = round((t+0.10)*30)) |
|---|---|---|
| 0-11 | Harrison (harrison19 default: greying hair tied back, apron with shavings) stands behind the bench right of the big brass H1. Both arms swing up into an open-palm presentation toward the clock; proud grin. Camera already moving; the plane and shavings on the sawhorse pass through the bottom-left foreground. | "ช่างไม้" -0.01 = g 3 |
| 12-35 | He holds the presentation with a 2 Hz proud bob. The H1's crossed dumbbell bars rock (set_balance, every frame), gears turn, the candle flickers. Blink g 20. The arc swings the H1 across the back wall (parallax). | "บ้านนอกคนนี้" 0.39 = g 15 |
| 36-49 | SNAP push x1.35 with a pan (13 f, peak 1.9). His palms thrust out a second time (ta-da, rise on the toes) and his eyes go to the clock. | "บอกว่านาฬิกา" 1.12 = g 37; the word นาฬิกา is heard about g 44 |
| 50-65 | Holds the ta-da, eyes back to the lens, grin; blink g 55. Hard cut at g 57; the handle keeps moving. | |

## Checked (all 66 frames at full size, scrubbed at 6 fps, g 34-52 and the cut g 54-60 frame by frame)

### Heads and staging
- Head 121 -> 213 px wide; head centre y 622-666; the lowest head bottom is y 771. No head reaches the caption band (y 880).
- Below y 880: bench front, the sawhorse plane (first 0.5 s), the lantern on the chest, the floor shavings, then the bench top and the tool rack after the snap.
- **In the world:** the feet point is on mark harrison_bench (floor z 0) with the contact decal; his stockings show under the bench at g 0-35 (feet on the floor, not floating); the shadow proxy casts on the wall behind. Scale is cast19's true 3.16 D.
- **H1 rocking:** set_balance(g / 30) keyed on every frame (bars +-24 deg, 1.3 s period, gears at their own rates): visible on the contact sheet as different bar angles in every tile.

### Hands, eye-lines, mouths
- No hand pins (no hand props): the presentation is a drawn pose. Mirror=True (the H1 is screen-left of him); arm keys stay arm_r / arm_l of the unmirrored figure.
- **Known limit:** he stands 1.6 D BEHIND the H1, so in the early wide frames his reaching hands are partly hidden by the clock's right post, and the near arm crosses his chest. It reads as "reaching toward / presenting the clock" at phone size; after the snap both palms are clear. Teams staging a character beside a set prop: keep the gesture on the camera side of the prop or move the mark.
- Eye-lines: at the lens (proud) except g 37-51, a glance at the clock.
- **Mouths:** no quote in this shot. Fixed grinning expression mouth, no lip-sync.

### Rules
- **No DOF:** dof off at camera creation (H.make_camera) and before every render; `dof: false` in every raw/g_*.json. **No text** anywhere (the H1 has gears and balls only).
- **No caption_shade:** c19.Take deletes it before and after making the camera and before every render; `caption_shade: false` in every raw/g_*.json.
- **Plan coverage:** shop_bench DAY, set_clock(1), balance rocking, Harrison default with apron + shavings presenting with both arms and grinning, low-ish camera already moving on frame 0, push 8 %/s + slide, plane and shavings in FG, snap on "นาฬิกา".
- **Continuity into shot 2** (SHIP ship_aerial NOON): a hard cut to another place, nothing to match.

### Automatic checks
- `qa_auto.py take.mkv --first_g 0 --cuts 57`: **PASS**. No black, blank, magenta or frozen frames; magenta 0.0 %. Its only note, "planned cut g 57 has no visible change", is expected: g 57-65 is the handle, the real cut happens in the conform.
- Sprite 'clipped' warnings: 0. Retried frames: 0.
- Colour: indoor WORKSHOP shade is warm by design (approved indoor exception, set3d19/hue_report.txt); magenta 0.0 %.

## Frame-diff (production-lessons §10)
Method (`deliver.py framediff`, also `c19.framediff`): grey = mean of R, G, B, resized to 90x160 bilinear; mean absolute difference to the previous frame in 0-255 levels; in-shot pairs only (g 1..56, no handle).

| | median | p90 | min | max |
|---|---|---|---|---|
| **final s01** | **4.38** | **14.40** | 3.89 | 20.98 |
| target | >= 4 | >= 12 | | |
| film 2 (reference) | 5.3 | 19.1 | | |

The 360x640 draft gave 4.38 / 14.17. **Tune on drafts.** The p90 comes from the snap (pairs g 40-46: 13.7-21.0); the median from the drift. The median has little margin: the warm, soft, low-contrast workshop moves the grey frames less than film 16's sky and trees did.

How the camera got there (draft numbers):

| camera | median | p90 | note |
|---|---|---|---|
| low (z 1.95), push 8 + slide 50 + arc 6, snap x2 | - | - | the sawhorse plank filled 40 % of the frame; the snap ended inside the H1 |
| preset height, look between H1 and Harrison, arc 9, snap x1.4 | 3.01 | 13.97 | median low |
| + slide -50, arc 15 | 3.53 | 14.81 | |
| + window-shaft volume hidden (the haze NOTE) | 3.78 | 15.07 | more contrast |
| + crane 35 px/s, snap shift down | 4.49 | 14.41 | but the arc ended on the H1 side-on (an empty brass frame) |
| final: start x 2.10, look x 2.85, push 8, slide -45, crane 35, arc 15, decay 0.1, snap x1.35/13 f peak 1.9 shift (0.30, -0.30) | 4.38 | 14.17 | |

## Seconds per frame
**13.16 s wall / 25.8 s CPU** mean at final (720x1280, 8 spp, 2 threads, two processes at once on 4 cores). The take took about 7.5 min wall. Build about 4.5 s per process. The draft (360x640, 6 spp) runs at about 3 s wall per frame (about 100 s for the take on two processes).

## Gotchas for render teams (film 19; details in c19.py)
1. **h19 API differs from film 16's telegraph:** `H.build(preset, light)` (no SET argument); hooks are all `H.set_*` (c19 `key_set(f, balance=..., candles=...)`); final samples are `H.STATE['samples']` after build (WORKSHOP / HALL 8, SHIP 10-12), not a per-location table.
2. **Key every hook on every frame.** Without `set_balance(g/30)` on each frame the H1 bars freeze; without `set_candles(1.0)` the flicker stops.
3. **`matrix_world` is identity right after `H.build`.** `c19.clock_world()` calls `view_layer.update()` first; do the same for any set object's world position (s01's first probe read the H1 at the origin).
4. **Never add caption_shade.** `H.make_camera` would build it if `H.STATE['caption_shade']` were set; c19 deletes the key and the object.
5. **shop_bench DAY haze** (QA_ART NOTE) is the faint window-shaft volume `H.STATE['shafts']` running toward this camera. s01 hides it on every frame (`C.key_vis(H.STATE['shafts'], False, f)`): clearer lower frame, +0.25 median frame-diff. The sun patches stay.
6. **WORKSHOP is small.** The right wall is at x 4.25 D, the front wall at y -5.4 D. A big arc or push drives the camera into the wall or the chest lantern (x 3.7, y 1.3 D): print the camera path (`shot.py probe`) before rendering. A low camera (below z ~2.2) at shop_bench puts the sawhorse plank over the bottom 40 %.
7. **Arcs and near props.** Arc about the subject's depth: the nearer H1 swings across the background (parallax), but more than ~30 deg over the shot turns it side-on (an empty brass frame). s01 uses 15 deg/s over 2.2 s with a slide the other way.
8. **Characters behind set props:** at harrison_bench he is 1.6 D behind the H1; gestures toward it are partly hidden. Plan the gesture or the mark.
9. **SHIP teams:** `c19.ride_ship(actor, A['ship_root'])` before the first `place()`, and the same t for `set_sea` and `set_roll` on every frame. Tested on ship_deck (no render): the card's feet follow mark_captain_wheel to 0.001 D while the deck bobs up to 1.6 D and pitches 2.6 deg in 2 s, so a camera standing on the deck must ride too: `C.on_ship(A['ship_root'], f, loc, look)`.
10. Draft vs final: `shot.py final ... 0.5 6` writes drafts to `work/draft`; run two processes on interleaved frame lists (`0:65:2` and `1:65:2`); the loop resumes and skips frames already rendered at the same scale and samples.

## Differs from the plan / notes
- **Camera height:** "low" is the preset height (z 2.25 D, looking 2 deg up). Lower, the sawhorse plank fills the bottom of the frame; the bench and the H1 still sit above the eye line.
- **Snap size:** x1.35 (bible x1.3-x3) with a pan; shot 1 is 1.91 s (under 2 s), so the snap is the plan's request, not a bible requirement. A larger snap ended inside the H1.
- **Runtime set change:** the window-shaft volume is hidden for the whole take (haze NOTE).


## Round 2 (QA-art FIX-FIRST fixes applied)
- **Staging:** mark moved to (3.45, 2.19) = harrison_bench + (0.12, -2.9): beside the H1's right end, on the camera side (no longer 1.6 D behind it); apron visible from g 0. Pose re-keyed as an open V, palms up: clock-side arm out toward the H1, other arm up and outward, no arm across the chest (DOWN/PRES/TADA hand targets in shot.py).
- **Camera:** CAM_LOC0 (2.00, -1.30, 2.25), CAM_LOOK0 (2.70, 3.20, 2.05): about 0.8 D closer to the old start, pitch -2.5 deg (ceiling beams under 30 % of frame); slide +30 px/s and arc 9 deg/s (was -45 / 15) keep him in frame and avoid the right wall's black void; snap shift x 0.12 (was 0.30): the H1 and its balls stay in frame through g 56.
- **Lantern:** the set fix (caged, dimmer) is on film19/main; it is now a dull orange cage on the stool, clearly dimmer than the yellow floor patches and the white face. It grows in the bottom foreground after the snap; known, accepted.
- **Top-right plank:** the lit diagonal oak plank is deleted from the scene mesh at build time (drop_top_right_plank in shot.py).
- **Numbers (final 720x1280):** head width 214 px at g 0 (to 411 at g 56); head centre y 427-561 (all heads below top, bottom max y 687, above 880); frame-diff median 4.43, p90 13.81 (min 3.54, max 20.49); camreport: never parked (0 frames under 0.25 px/frame); 12.4 s/frame wall; qa_auto PASS; no DOF, no text, no caption_shade; H1 bars rock every frame.
- meta.json camera string corrected.
