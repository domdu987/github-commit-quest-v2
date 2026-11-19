# s01 QA: film 16, shot 1 (the hook) -- LINE line_close, DAY

s01 and s23 share one setup (same camera, marks, bottle-hand method, timing differs). Current state after the TAKE gate rounds 1-3.

## Delivered
- take.mkv: 75 frames, g 0..74 (shot g 0..68; no handle before g 0, 6 after), 20.1 MB. Hard cuts out.
- QA_AUTO.md (PASS), phone_sheet.jpg, contact.jpg, cues.json, meta.json, framediff.json.

## Staging (what the viewer sees)
- Morse stands one rung lower along the ladder, holds the bottle out toward the pole top: his head is beside the bottle (head-to-glass distance >= 165 px) and the bottle body stands against sky to the cut.
- The set's glass is tuned at runtime (transmission 0.35, deep bottle-green, more body): the held copy and the pole glass are the same deep green from the first frame (no pale cyan to green switch), no grain.
- Hands: after the cap the free hand comes down the pole side to chest height and takes the wire at the coil; it never reaches his mouth or forehead (hand error <= 0.25 D).
- Wire: lifted in an arc, it falls onto the glass top and settles into a drape hanging on both sides of the glass over 3-4 frames (two thin catenaries that hang ACROSS the view: the real line runs along the sight line and read as a rigid rod up out of the frame). The set's long spans stay off in this take; the wrap ring shows 3 frames after the landing (no 1-frame pop). The sag is carried by the catenary shape, not by a visible bounce.
- Glint: the star flares at the word and at the contact, fades after 10 frames and twinkles once more 30 frames later (no fixed sticker).
- DAY, dry pole.
- Camera: higher (z 5.3, pitch 25 deg) so ground and poles fill the first second; push 10 %/s, slide 60 px/s, arc 18 deg/s; snap x2.5 + pan (13 f) on the word; a short eased truck + crane-up (14 f) while the wire settles.

## Beats
| g | beat |
|---|---|
| 0-21 | bottle held out over the bare pole top |
| 22-35 | SNAP on "คอขวดเบียร์" (24), glint |
| 34-47 | lowered; contact g 47 |
| 51-53 | blink, pose swap, happy |
| 53-56 | hand down the pole side to the coil |
| 56-60 | wire lifted in an arc over the glass |
| 60-67 | the wire falls onto the glass and drapes; ring from 63 |

## Checked
- Heads [95, 308] px wide, centre y [510, 663], lowest head bottom 817: nothing in the caption band. No text, no DOF, mouths still, no magenta.
- qa_auto PASS (its "no visible change at the planned cut" note is a false alarm: the handle renders the same shot).

## Frame-diff (in-shot, 90x160 grey)
median 7.59  p90 17.55  (target >= 4 / >= 12).

## Seconds per frame
8.5 s wall / 16.33 s CPU (720x1280, 7 spp, 2 procs x 2 threads).

## Notes / not done
- The 3-frame forearm-at-chin and the wire end near his cheek at the pick are reduced, not removed.
- The pose swap on the blink still jumps the drawn arm in one frame (diff spike).
- The wrap ring shows at g 63, three frames after the landing.
