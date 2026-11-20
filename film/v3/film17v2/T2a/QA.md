# T2a QA self-check (film 17 v2, take T2, g330-493, 164 frames)

Render: `render_T2a.py` (`check_take('T2')` hits [] PASS, `check_face('T2')` ok PASS), 720x1280, 16 samples + OIDN, adaptive 0.03, 2 threads, `stage_cast2` on every frame, no motion blur, mouths closed except the held laugh g467-493 (no lip-sync, no `talk`).
Commit that carries the take: see the message sent to the director.

## Numbers (qa_stats2-style: 90x160, luma = mean of R, G, B)
- Part: mean **100.1**, min 86.1 (g380), max 118.7 (g332), saturation 0.646, vivid 70.0 %.
- By range: g330-360 107.6 (façade, trimmed at conform per the director), g361-386 93.0, g387-466 101.2, g467-493 94.8.
- Key still g450: 99.2 (film/v3/film17v2/T2a/key_g450.png).
- Rhythm (`film17/rhythm.py`): median 13.82, p90 22.07 (targets >= 4 / >= 12). No hard cuts inside the range.
- First-30-frame check on g387-416 at the final light: 104.6-106.5 (taken from the paused 10-frame measurement, g387-396).
- OIDN shimmer: I did NOT study the 30 frames as a clip, and I did not measure shimmer on flat walls. I only compared two consecutive frames (g410/g411) of the first, over-lit run (not these frames), and that crop was not examined by eye. Status: unchecked.

## qa_auto.py: FAIL (one item)
- "suspected blur on 31 frames, e.g. g330-344". Its Laplacian test uses 0.6 x the take median. Recomputed with the same formula on the final frames: median 1236, 32 frames below 0.6 x median (g330-360 and g482).
- I believe this is a false positive from flat stone façade frames (few edges against the dense photo-wall corridor that sets the median), not blur: motion blur is off (`use_motion_blur = False`) and g358, g380 at full size have crisp ink outlines. I have not shown that with a numerical edge-density comparison. The director should judge.
- Notes: magenta 0.0 %. No black / blank / frozen / pop failures listed.

## Frames viewed (full 720x1280, then phone size)
Phone size = `qa_auto_out/phone_sheet.jpg` (360x640 tiles at g330, 345, 360, 375, 390, 405, 420, 435, 450, 465, 480) and `contact.jpg` (240x427 tiles, 13 frames). Full size was viewed for g358, g380, g450 (key), g470, g485, g493. Earlier (before the last relight) I also viewed g330, g345 and g407 at full size.

- **g330 (phone sheet) / earlier full view:** back view of the thief at the open main doors: olive flat cap with a button and seam, ginger hair with ears and a nape, red neckerchief, brown jacket with seam and blue and ochre patches, dark ink outlines. It reads as cap, hair and jacket, not a black slab. His feet are on the steps with a contact shadow. Doors and stone are orange/cobalt, bright. "ARCHIVES" sign is far inside.
- **g358 (full):** thief on the corridor steps, same cover, small in frame. The clerk on the ladder at left has a hat, moustache, and his body is on the ladder. A gendarme at right behind the rail, and a seated prisoner far end. Feet of the thief on the stone step.
- **g380 (full):** the thief is a very large back view at left, about 60-65 % of the frame width, head and cap partly cut by the left edge. The cap highlight has a small notch in the top seam. The ARCHIVES door and a green gendarme are behind. The thief at this size is bigger than the 2b "30 %H" in PLAN_V2; I used the prepared camera path unchanged, so this follows from it. Flag for the director.
- **g405 / g420 (phone sheet):** the thief now front-facing with a smirk, patched jacket, shrug, feet on the tiled floor with a runner; clerk on the ladder; green gendarme standing at the ARCHIVES door. IDENTIFICATION sign visible, partly cut by the frame at g405, whole at g435-450 in the sheet.
- **g450 (full, key):** IDENTIFICATION whole and readable; thief in front of the door; clerk on the ladder with his feet at rung level. Photo walls dense.
- **g470 (full):** looking through the ID door into the measuring room: gasolier, shelf of books, tripod camera, Bertillon and a prisoner, a gendarme at the right edge. No sprites float; feet on the floor.
- **g485 (full) and g493 (full):** the laugh. A gendarme (left) with eyes shut and tears, open mouth; the inspector (stout, curled moustache, tears, hands on hips, open mouth) beside him; stacked books on stools; Bertillon at right with his pince-nez beside the chair with a prisoner and the tripod. Mouths are held shapes, nothing is lip-synced. Floor rug visible at the bottom. Cards stand on the floor with soft contact shadows. The second laughing gendarme (grey-green kepi) is not visible in either frame.

## Specific checks
- **Thief back view (director's request):** reads as cap, hair and jacket at full size and at 360x640 (phone sheet g330-375). Built from T6b's approved code (`t2a_back.py`).
- **Corridor gendarme head, g403-451:** I looked at every 6th frame (g403, 409, ..., 451) as a strip. The green gendarme is not cut by the LEFT edge in any of them. From about g439 to 451 he is partly cut by the RIGHT edge. I did NOT check every frame and did not measure it in pixels.
- **IDENTIFICATION whole g445-458:** seen whole in the g450 key and in the g435-450 phone tiles. Not measured per frame.
- **Black slabs / leaked actors:** the loop clears `c2_*`, `back_*`, `bk2_*`, `bk_*` before each `stage_cast2`. Luma over the final run is smooth, and no slab was seen in the frames viewed. Not exhaustively checked on all 164.
- **Arch fix (T1b):** `prefecture17.py` main-door arch stones radius 1.25 / height 0.42 (commit 17f4dcd). I did not compare the arch against the PRÉFECTURE band in the g330-360 frames, which show the doors from the steps and do not include the band.

## Discarded frames (history)
50 frames of an over-lit first run (RGB-mean about 121), 11 frames with the stale flat-black back cover, and 11 frames of a middle lighting run were deleted and re-rendered.
