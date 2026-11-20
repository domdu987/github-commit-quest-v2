# s16 QA: film 19, shot 16 (SHIP ship_deck NOON)

## Delivered
- `take.mkv` (libx264rgb crf 6, 30.5 MB, 30 fps): g 1181..1288 = 108 frames, `first_g` 1181. Shot 16 = g 1190..1279 (39.67-42.65 s); handle in g 1181..1189 (9 f, CUT in), handle out g 1280..1288 (9 f, cut to shot 17). 720x1280, 11 spp, 2 threads.
- `meta.json`, `cues.json`, `contact.jpg`, `QA_AUTO.md` (PASS) + `phone_sheet.jpg`, `framediff.json`; scripts `shot.py`, `deliver.py`, `c19.py`.

## Shot
"แต่นาฬิกายังบอกเวลาที่บ้าน": william19 (happy, eyes closed smile) holds the silver H4 out on his open palm toward the lens; captain19 stands beside him and looks at the watch (gaze to William's hand), then drifts out of frame left as the camera pushes. Sun at the zenith (`set_sun_overhead(1)` keyed every frame, continuity with shot 15). Camera: push 10 %/s + slide + arc (-9 deg/s) in the ship's rest frame, deck-ridden; SNAP x2.3 with a pan on "บอกเวลาที่" (caption 40.5 = g 1218; snap g 1212..1228, 16 f) onto William and the watch, with the starboard bulwark / deck in the foreground.
Cards ride the ship (c19.ride_ship with the parent inverse taken at t = 0, see s15/QA.md gotcha), camera rides the deck (c19.on_ship); set_sea / set_roll / set_sun_overhead keyed with the same t every frame.

## Checks
- Heads: centre y 540-600, widths 100-345 px, nothing near the caption band (y 880). Contact shadows and feet on the deck. No DOF, no text, no caption_shade; mouths still (no quote).
- Known: William's head slides to the left edge on the last in-shot frames of the push (hat edge may touch x 0 around g 1275-1279); the H4 is small (0.24 D) but shows tick marks and hands from g ~1225 on.
- qa_auto: PASS. Soft frames g 1285-1288 are handle frames beyond the cut (William half off-frame at x2.3 zoom); the first delivery had those flagged as blur FAIL with a 256 px/D sprite; re-rendered g 1210-1288 with PPD 384 for William.
- Frame-diff (in-shot pairs g 1191..1279): **median 6.12, p90 12.48** (draft 6.02 / 12.22). Target >= 4 / >= 12 (p90 has little margin).
- s/frame: 17.8 wall / 34.3 cpu.

## Differs from plan
- The captain looks on only for the first ~1.5 s, then the push leaves him out of frame. "Wheel / rail in the foreground": the bulwark and deck fill the right of the frame; the wheel is out of frame (camera is at the stern mark, offset).
- The watch is held to the side of William's body (cast pose show_h4), not straight into the lens.
