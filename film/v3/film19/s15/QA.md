# s15 QA: film 19, shot 15 (SHIP ship_deck NOON)

## Delivered
- `take.mkv` (libx264rgb crf 6, 38 MB, 30 fps): g 1086..1198 = 113 frames, `first_g` 1086. Shot 15 = g 1096..1189 (36.52-39.67 s); handle in g 1086..1095 (10 f, DIS 15 in), handle out g 1190..1198 (9 f, cut to shot 16). 720x1280, 11 spp (the set's own), 2 threads, OIDN.
- `meta.json`, `cues.json`, `contact.jpg`, `QA_AUTO.md` (PASS) + `phone_sheet.jpg`, `framediff.json`; scripts `shot.py`, `deliver.py`, `c19.py`.

## Shot
"ความลับคือ เที่ยงวันกลางทะเล ดวงอาทิตย์อยู่ตรงหัว": william19 (blue coat, tricorne) aims the brass quadrant at the sun (the quadrant thrusts up on the snap, glint pulses); captain19 stands beside him at the wheel looking up at the sun, hands behind his back.
`set_sun_overhead` is keyed on EVERY frame 0 -> 1 (g 1086..1176), so the sun climbs to the zenith and the sail / mast shadow swings in under the mast. Camera: slow push 10 %/s + slide + a small arc and crane (ship's rest frame), then a SNAP x1.9 with a pan on "อยู่ตรงหัว" (caption 38.98 = g 1172; snap g 1164..1184, 20 f) onto William and the quadrant.

## Ship riding
- Cards parented to ship_root (`c19.ride_ship`), camera rides the deck (`c19.on_ship`), `set_sea(t)`, `set_roll(t)` and `set_sun_overhead` keyed with the same t on every frame.
- **Gotcha (found here): the parent inverse must be taken with the ship level.** `ride_ship` inverts ship_root's matrix_world at the CURRENT frame; if `set_roll(t != 0)` is keyed on the first rendered frame the inverse carries 2-3 deg of roll and the cards sit up to 1.4 D off the deck (shot 16's first test showed the figures sunk to the chest). shot.py keys `H.set_roll(0, frame=1)` and `scene.frame_set(1)` before `ride_ship`. c19.py is unchanged.

## Checks
- Heads: centre y 591-670 in shot, widths 93-270 px, lowest head bottom < 800; no head above the caption band. Captain (mark captain_wheel offset +0.8, +1.7 D so he sits beside William) leaves frame left during the snap (he is background to the sun business); William's head touches the left edge only in the last in-shot frames of the push.
- No DOF, no text, no caption_shade (false in every raw json). Feet and contact shadows on the deck in every frame.
- Frame-diff (90x160 grey, in-shot pairs g 1097..1189): **median 5.08, p90 13.96** (draft 5.01 / 13.72). Target >= 4 / >= 12.
- s/frame: 18.6 wall / 36.5 cpu (final, two processes, 2 threads each).

## Differs from plan
- "crane up toward the sun": the camera cranes (rise 15 px/s) and pushes in; it does not tilt up to the sky because heads must stay in y 450-760.
- Captain exits the frame in the snap; William is the subject.
- Mouths: nobody speaks. Mast shadow = the main sail shadow (the deck's mast shadow moves under the mast as the sun reaches the zenith).
