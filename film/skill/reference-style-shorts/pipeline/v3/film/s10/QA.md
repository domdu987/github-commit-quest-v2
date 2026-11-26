# QA: take s10 (shot 10, office, office_day = INTERIOR_DAY)

- **Frames.** Film frames g 610..693 are the shot; rendered g 603..700 (handles 7 in, 7 out for the dissolves), 98 final frames `frames/g_%04d.png`, 720x1280, Cycles 12 samples, 2 threads, one process.
- **Source.** `shot.py` (this take) on the shared runner `../s10/otake.py` (set `office3d` + `office_props`, stage actors, resumable render, streak post as `shots/post.py`). Numbers below: `python3 shot.py qa` -> `work/qa.json`.
- **Transition in.** {"type": "dissolve", "frames": 9, "note": "quick continuity from s09 (corridor view) into the low angle on the chief"}

## What the take does

Take s10 = shot 10 (20.317-23.129, film g 610..693, handles 7 + 7): office, office_day (INTERIOR_DAY).

(1) low angle on the chief alone at boss_mark (camera 1.2 D up, about 4 D away, looking up past him at the map), he bounces the
eraser in his palm; (2) snap 20.82-21.35 on '"ไอ้หนู': pull back, rise to 2.85 D and pan right into G, THE GLOAT FRAMING (chief far
at boss_mark, hero near at gloat_near, red line at screen left); (3) eased push through the quote, 30 -> 0 %/s, x1.3 (a zoom from
G's pose with a small truck right, so the near/far ratio of G is kept). The chief's mouth moves with the narration loudness only
inside the quote 21.07-23.13; 'เฮอริเคน' he drives the eraser up the red line (pinned), 'มันไม่ขึ้น' finger wag, 'ทางด่วนหรอก' lean
toward the hero and a held wink. The hero listens, frozen, unimpressed, blinks, one gaze shift; his mouth never moves.
    python3 shot.py probe|stills|draft|render|post|contact|qa [a:b[:s]]

## Camera (true 3D camera, corner speed in px per frame)

- move g 632-641 (film 21.07-21.40 s), peak g 636 at 40 px/frame
- static runs (< 0.25 px/frame): [[697, 700]]
- constant-speed (linear) runs: [[637, 638]]
- streaked frames (camera faster than 60 px/frame at the corners): none; plate under sharp actors: none; whole frame: none

## Heads (720x1280 px, from the projected sprite anchors of every final frame)

| actor | frames | head width px | head centre y (px) | lowest head bottom y |
|---|---|---|---|---|
| boss10 | 98 | 173-223 | 511-608 (0.40-0.47 H) | 720 |
| hero10 | 98 | 244-317 | 478-711 (0.37-0.56 H) | 870 |

Hand cards (names ending in H) are scaled hand cards whose heads lie outside the frame by construction.

## Pinned props (registration: rendered tip against the projected world target)

- boss10.l: max 0.00 px

## Popcheck (mean absolute change of consecutive final frames, 180x320)

- pops (change > 1.8 x both neighbours and > 1 level): none
- median change 4.78, largest 26.84
- black or magenta cards retried: none; still wrong: none

## Colour (`tools/hue_report.py frames/`)

```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
reference A, whole clip                        33.6   23.1    0.7    0.5    0.5   29.1    2.7    9.7  0.48 0.63 0.08   OUT: sat,val,dark
reference B, whole clip                        24.5   34.1    2.4    0.7    0.2   28.6    4.5    5.0  0.41 0.57 0.08   OUT: red,dark
reference A interiors                          40.1   27.6    0.3    0.4    0.0   21.9    1.1    8.6  0.47 0.55 0.09   all in band
reference B interiors                          36.3   37.7    2.3    0.1    0.0   13.9    4.5    5.1  0.38 0.45 0.15   OUT: blue
target band: red 30-41, orange 22-38, blue 14-30, violet 0-5, magenta 0-10, sat 0.38-0.48, val 0.45-0.63, dark 0.08-0.15  (percent of chroma for hue families)
v3/film/s10/frames                             39.3   32.4    0.1    4.2    2.5   15.7    1.3    4.5  0.44 0.50 0.13   all in band
```

## Cost

- CPU seconds per final frame (min / median / max): [24.7, 26.7, 29.3]; wall: [13.2, 21.3, 39.5] (machine shared with other workers' renders)

## Deviations and notes

- Framing 1 is a low single from (0.30, -4.10, 1.20) looking at (0.70, -0.42, 2.30), 1.2 D up, +16.5 deg, not the props module's low_boss: from low_boss the near hero at gloat_near is in frame (x 577, head 273 px), so the chief would not be alone. Here the chief is alone (head 190 px at x 474, centre 0.40 H), with the map and the red line at screen left and the ceiling boards above. The snap then pulls back, rises 1.6 D and pans right into G as planned.
- The x1.3 push is a zoom (22 -> 28.6 mm) plus a 0.3 D truck right. A dolly alone would grow the near hero x1.47 and break the 1.36-1.46 near/far ratio. G at the snap end: chief 173 px (397, 594), hero 244 px (620, 694), ratio 1.41. At the end of the push: chief 223 px, hero 317 px, ratio 1.42; the right frame edge crops about 20 % of the hero's head at the end (under 10 % in G itself).
- The chief's mouth is driven by acting.loudness(21.07, 23.13) through boss_talk on g 635-696 only; before and after it holds the smirk / flat drawing. The hero's mouth never moves.
- The chief faces the map (yaw -0.35) for the eraser bounce and the 'vroom' up the line (eraser pinned on the track, u 0.50 -> 0.92, g 644-667), then turns to the hero (yaw +0.40) over 7 frames at the start of 'มันไม่ขึ้น'; finger wag with the near hand, then lean 0.12 D + held wink g 692-695.
- The hero has no pencil behind his ear: the acting library's hero_listener draws none, and no ear-pencil drawing exists.
- Red line: the client's hand-drawn track (office3d TRACK_STYLE 'hand'); every frame of this take was rendered after 18 Nov 14:40 (version 3), no ruler anywhere. Everything that touches the line (eraser, pencil points, smudge halo, camera look-at points) is placed with S.track_point(u) of the hand-drawn track.
- Colour: the raw render measured red 43-44 % and dark 0.16 (the red wallpaper fills more of these framings). The delivered frames carry the mild band grade ../s10/grade.py (red family rotated 8 deg toward orange, tapered, the pure track red spared; shadows under V 0.28 lifted by up to 0.07), the same grade on s10, s11 and s09; the change is not visible side by side (work/raw keeps the ungraded render).
- Static run g 697-700: the end of the eased push (30 -> 0 %/s, as the plan asks) falls in the last 4 frames of the out handle, under the 9-frame dissolve into s11; inside the shot [610, 694) the camera never stops.
