# s04 QA: film 7, shots 4-6 (the crowded salon; the small Mona Lisa; the director's boast)

Delivered: `frames/` (g 228..604, 377 frames, 720x1280, 12 samples, 2 threads, denoise FAST) and `take.mkv` (libx264rgb crf 6, 30 fps,
**first_g 228, n_frames 377**). Shots: 4 = g 234..335, 5 = g 336..440, 6 = g 441..598 (plan 7.80-19.96 s). In-handle g 228..233 and
out-handle g 599..604, both rendered in 3D. **transition_in = dissolve** (from shot 3's kiosk; s03 also carries a 6-frame out-handle),
out = cut. Also `meta.json`, `cues.json` (13 cues), `contact.jpg` (cyan line y 880), `compare.jpg` (g 260 / ref a t0016 wide hall; g 412 /
t0046 people in a hall; g 520 / t0051 big figure from below; g 555 / t0003 ECU object). Scripts `shot.py`, `deliver.py`, `qa.py`;
`../common.py` untouched. Drafts `work/d1a/d1b/d2/d3/d4.jpg`, `work/f1/f2.jpg`.

## Set-ups (all louvre Salon Carre, GALLERY_DAY, `set_mona(True)` + `set_flames` keyed every frame)
| id | g | shot | what |
|---|---|---|---|
| 1 | 228..285 | 4 | establishing wide from the service-door corner: three hung walls, skylight, divan, torcheres; 2 ladies, 2 gentlemen and a boy stroll across (walk cycles), the guard at ease; slow crane drift |
| 2 | 286..335 | 4 | mid-room toward the back wall: she is a small picture in the middle of the hang; a lady and two gentlemen cross in front without a look; slow push ("โมนาลิซ่า เป็นแค่ภาพเล็ก ๆ" 9.91 s = g 300) |
| 3 | 336..389 | 5 | close on the Mona Lisa (frame, glass glare) pulling back 46 -> 24 mm until the big pictures crowd round her ("แขวนปนกับภาพอีกเป็นร้อย") |
| 4 | 390..440 | 5 | eye level at the rope: a lady strolls in, slows (402-408), glances up at her (408-418), walks on bored; the guard by the wall ("คนเดินผ่าน แทบไม่หยุดดู" 13.3 s = g 402) |
| 5 | 441..499 | 6 | low angle (camera z 1.35): the director (top hat, monocle) proud beside her, hand on hip, chin up before the boast; rising push. Mouth closed (narrator: "ผู้อำนวยการลูฟวร์ประกาศว่า") |
| 6 | 500..539 | 6 | lower (z 0.95) and closer, huge from below: the finger goes up (500-506) and the boast -- lip-sync |
| 7 | 540..569 | 6 | ECU cut-in on the painting at 18.0 s: her face and smile behind the glass, slow push 50 -> 52 mm (his voice off screen) |
| 8 | 570..604 | 6 | extreme low angle (z 0.65), the skylight above him, finger to the sky, lip-sync to the end of the quote (19.95 s = g 602), smug closed mouth on the handle |
Framing changes at g 286, 336, 390, 441, 500, 540, 570 (1.0-2.0 s apart; id 1 incl. the in-handle 1.9 s).

## Client rules
- **No depth of field** (C.Take): the far hang, the skylight bars and the coffers are sharp in every set-up.
- **Mouths**: ONLY the director, ONLY inside the quote 16.57-19.95 s (g 500..602): `cast7.talk_mouth(g, level, seed 7, hold 2)` with the
  level from the narration RMS (at +0.10 s, normalised to its 90th percentile); level < 0.12 -> the expression mouth (pauses at g 510-511,
  530-531, 600-601). Before g 500 (id 5) and after g 602: closed smug mouth. Nobody else's mouth moves.
- **Heads** (`work/qa.txt`): no head bottom below y 880 in any frame. Main head centres: id 4 lady 0.57-0.58 H, guard 0.53; id 5 director
  0.49; id 6 0.43-0.45; id 8 0.37-0.40 (the extreme low angle, still inside 0.35-0.59). Wides id 1 (heads 0.56-0.63 H, 49-78 px) and id 2
  (0.55-0.61 H) are the exempt establishing set-ups.
- **Dense set**: the 155-picture salon hang, damask, gilt frames, torcheres, rope and stanchions, divan, parquet in every frame.

## Checks
Popcheck: exactly the 7 planned framing changes. Near-still single pairs at g 498 (the director's breath before the boast), 540 and 568
(eased ECU push) -- none longer than 1 frame. No black / magenta frames, no retried frames, no clipped sprites in the finals (the director
uses a wider card canvas `DIR_CANVAS`: the finger to the sky clipped in the draft).

## Colour (hue_report rows, `work/qa.txt`)
```
s04 id 1 wide          red 52.6 orange 37.5 blue 2.0 violet 0.9 magenta 4.2   sat 0.35 val 0.53 dark 0.05
s04 id 3 Mona close    red 73.4 orange 22.9                     magenta 0.7   sat 0.62
s04 id 7 ECU painting  red 9.9  orange 73.7 yellow 10.8         magenta 0.2   sat 0.19 (her painted ochres + the glass glare)
s04 id 8 extreme low   red 32.9 orange 44.0 blue 4.3 violet 12.7 magenta 4.8  sat 0.26 dark 0.19 (black frock coat + coffered ceiling)
s04 all                red 52.3 orange 39.4 blue 1.1 violet 1.8 magenta 2.7   sat 0.42 val 0.57 dark 0.07
```
Warm gaslit/daylit gallery, red damask dominant (the set's walls); magenta <= 4.8 everywhere; violet 12.7 in id 8 is the shade on the black
coat (hue ~225 by design, not magenta). Not graded here.

## Seconds per frame
14.2 s wall / 27.6 s CPU mean (2 threads, two render processes at once).

## Fixed after looking
- id 4 first final had the lady's head at 0.60-0.62 H and its bottom below y 880 on g 436-440: camera look lowered (z 3.35 -> 3.0), re-rendered
  (old frames in `work/old_s4`).
- Drafts: director moved to x 2.0 so the Mona Lisa shows beside him (id 5); finger-to-the-sky hand raised clear of the head + wider canvas;
  the guard in id 1 moved back off the lens; the lady's path in id 4 moved so she glances while passing under the painting.

## Differences from the plan
- Shot 6's lip-sync covers the quote only (from 16.57 s), not the narrator's "ผู้อำนวยการลูฟวร์ประกาศว่า" before it.
- In id 1 some walkers pass behind the divan's urn (partly hidden for a few frames).

## take.mkv is split (GitHub 100 MB limit)
The crf-6 encode of 377 frames is 115992611 bytes, over GitHub's 100 MB per-file limit (the push was refused). It is stored unchanged,
byte-split: `take.mkv.part00` + `take.mkv.part01`. Rebuild: `cat take.mkv.part00 take.mkv.part01 > take.mkv`
(sha256 1f834719ae56debe0dfbe4ca167bbcbc01403de7cf1f80ff539604d42e43d421, also in meta.json "take_file").
