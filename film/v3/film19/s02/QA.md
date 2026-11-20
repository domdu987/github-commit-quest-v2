# s02 QA: film 19, shot 2 (the lone ship) -- SHIP ship_aerial, NOON

## Delivered
- `take.mkv` (libx264rgb crf 6, 30 fps, 16 MB): first_g 48, 71 frames, 720x1280, 10 spp (H.STATE['samples'] of ship_aerial), 2 threads. No captions, no audio.
- g 48..56 = in-handle, **g 57..109 = shot 2 (1.91-3.65 s)**, g 110..118 = out-handle. Both joins are hard cuts (shot 1 -> 2 at g 57, 2 -> 3 at g 110); the handles are real 3D continuation.
- `meta.json`, `cues.json`, `contact.jpg`, `QA_AUTO.md` (PASS), `phone_sheet.jpg`, `framediff.json`, scripts `shot.py` / `deliver.py` / `c19.py`.

## Shot
The lone ship at the origin on the endless glittering sea (one narrow glitter path, clouds at the horizon, gulls). No actors. The camera pulls back and sinks the ship down the frame (pull 10 %/s, crane 140 px/s, orbit -8 deg/s, slide 60 px/s, decay 0.1: moving on frame 0 and on the last frame; no snap, shot < 2 s). `set_sea(g/30)` and `set_roll(g/30)` keyed on every frame (swell, wake foam, the ship pitching).

## Checked
- DOF off, no text, no caption_shade (`dof:false`, `caption_shade:false` in every raw json). camreport: never parked (0 frames under 0.25 px/f).
- No characters, so no heads / mouths / contact shadows to check. Ship stays clear of the caption band until the last handle frames (hull reaches y ~860 at g 118).
- **Sea edge:** the set fits ONE sea grid to the preset camera, so any pull-back shows its edge. Fixed at runtime in shot.py (`widen_sea`: the grid is fitted to a virtual camera 4.5x farther on the same axis, 700x1000 vertices). No set module edited. Checked at g 48, 82, 118: no edge.
- qa_auto: PASS; the planned cuts have "no visible change" only because the neighbours are other takes.

## Frame-diff (90x160 grey, in-shot g 58..109)
median **2.04**, p90 **2.33** (draft 2.03 / 2.30). **Below the 4 / 12 target.** Deviation: a calm high aerial over smooth low-contrast sea changes very little per frame; every camera variant tried (pull up to 12 %/s, crane 250 px/s, orbit 10 deg/s) gave 0.5-3.4 on a single pair, and bigger moves leave the 6-10 %/s / 20-60 px/s drift rule or expose the sea edge. I kept the strongest move that keeps the ship framed and clear of the caption band.
