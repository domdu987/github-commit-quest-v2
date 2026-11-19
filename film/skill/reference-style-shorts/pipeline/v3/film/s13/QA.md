# QA: take s13 (shot 13, office, office_day = INTERIOR_DAY)

- **Frames.** Film frames g 839..867 are the shot; rendered g 839..874 (handles 0 in, 7 out for the dissolves), 36 final frames `frames/g_%04d.png`, 720x1280, Cycles 12 samples, 2 threads, one process.
- **Source.** `shot.py` (this take) on the shared runner `../s10/otake.py` (set `office3d` + `office_props`, stage actors, resumable render, streak post as `shots/post.py`). Numbers below: `python3 shot.py qa` -> `work/qa.json`.
- **Transition in.** {"type": "punch_in", "frames": 0, "note": "punch-in cut with white speed lines over the first 6 frames"}

## What the take does

Take s13 = shot 13 (27.957-28.922, film g 839..867, no handle in (punch-in cut), handle 7 out): office, office_day.
The punch-in on the Thai label 'ทางด่วนพายุ' being pinned above the arrow head of the red line. Camera label_insert (props
extension; on the axis of shot 12, raked 12 deg from below-left): a 4-frame punch-in that lands on the setup with white speed
lines over the first 6 frames, held close, a 2-frame shake (0.45 deg) on the slap, then an eased drift push of about 5 %/s.
The chief's hand (a hand card, the take-A method of s11) slaps the label (nickname_label art of the paper registry, hi-res) onto
the map at 28.00, slides up to its top edge and thumbs the red pin home at 28.25; the label rocks 4 deg for 2 frames and its
lower-right corner curls. No faces. The red line is the hand-drawn track as it is now (line 1, smudge halo 3).
    python3 shot.py probe|stills|draft|render|post|contact|qa [a:b[:s]]

## Camera (true 3D camera, corner speed in px per frame)

- move g 839-842 (film 27.97-28.10 s), peak g 839 at 118 px/frame
- static runs (< 0.25 px/frame): none
- constant-speed (linear) runs: [[857, 858], [859, 874]]
- streaked frames (camera faster than 60 px/frame at the corners): [839, 840]; plate under sharp actors: [839, 840]; whole frame: none

## Heads (720x1280 px, from the projected sprite anchors of every final frame)

| actor | frames | head width px | head centre y (px) | lowest head bottom y |
|---|---|---|---|---|
| bossH13 | 20 | 539-714 | -267-262 (-0.21-0.20 H) | 534 |

Hand cards (names ending in H) are scaled hand cards whose heads lie outside the frame by construction.

## Pinned props (registration: rendered tip against the projected world target)

- bossH13.l: max 2.75 px

## Popcheck (mean absolute change of consecutive final frames, 180x320)

- pops (change > 1.8 x both neighbours and > 1 level): none
- median change 1.66, largest 31.42
- black or magenta cards retried: none; still wrong: none

## Colour (`tools/hue_report.py frames/`)

```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
reference A, whole clip                        33.6   23.1    0.7    0.5    0.5   29.1    2.7    9.7  0.48 0.63 0.08   OUT: sat,val,dark
reference B, whole clip                        24.5   34.1    2.4    0.7    0.2   28.6    4.5    5.0  0.41 0.57 0.08   OUT: red,dark
reference A interiors                          40.1   27.6    0.3    0.4    0.0   21.9    1.1    8.6  0.47 0.55 0.09   all in band
reference B interiors                          36.3   37.7    2.3    0.1    0.0   13.9    4.5    5.1  0.38 0.45 0.15   OUT: blue
target band: red 30-41, orange 22-38, blue 14-30, violet 0-5, magenta 0-10, sat 0.38-0.48, val 0.45-0.63, dark 0.08-0.15  (percent of chroma for hue families)
v3/film/s13/frames                             22.8   38.0    0.0    0.0   11.8   26.0    0.2    1.3  0.44 0.51 0.07   OUT: red,dark
```

## Cost

- CPU seconds per final frame (min / median / max): [19.3, 22.4, 28.3]; wall: [29.4, 34.0, 43.4] (machine shared with other workers' renders)

## Deviations and notes

- Camera: label_insert of the props module, (-0.249, -1.811, 2.887) -> (0.125, -0.05, 2.87), 22 mm: 1.84 D from the label, raked 12 deg from below-left (the module's note: at 1.1 D the 1.15 D label would be about 820 px wide; 1.84 D keeps the planned 480 px). Punch-in: the take opens at 1.30 x the distance and lands on the setup in 4 frames (cubic ease-out); 2-frame shake on the slap (roll 0.45 then -0.30 deg, g 843-844); then a drift push easing in to 5 %/s.
- Speed lines: 46 white radial wedges (2D, deterministic, centred on the label) over the first 6 frames g 839-844, fading out and retreating outward, drawn by this take's post on top of the streaked frames.
- Label: nickname_label of the paper registry at 2400 px (set_label res 'hi'), hung by the props module on label_rect from its pin LB_PIN, tilt 4 deg. It flies in with the hand (0.30 D from the right, 0.22 D off the wall, scale 1.10, accelerating) and slaps flat at g 843 (28.00), rocks +4 / -2 deg for 2 frames, the lower-right corner curls (0 -> 0.55 over g 846-853) and flutters slightly. The red pin appears under the thumb at g 847 and is thumbed home g 849-851 (28.25).
- Registration on the hand-drawn track (set API track_point): the arrow head is track_point(1.0) = (0.0623, 2.6197); its local heading (track_point(0.97) -> track_point(1.0)) leans 5.6 deg east of up. Extended past N.Y., that heading meets the label's bottom edge 0.486 D above the tip at x 0.110, 47 % along the label's width; the label's bottom centre is at x 0.145, so the label sits centred over the end of the line within 0.036 D (about 15 px in this framing). The label keeps the shared label_rect position so that shots 17-25 match.
- The chief's hand is a hand card (s11's take-A method: the chief's puppet at scale 1.5 facing the lens, 0.05 D in front of the target, body and head outside the frame at the right). Its BARE hand is pinned with a world 'hand' target (palm on the label's right half for the slap, then on the pin head for the thumb). The shared runner reports registration only for prop tips, so this take measures the bare hand the same way (projected hand anchor against the projected world target). The card casts no shadow; the chief's body is not in the scene, so his hat does not shadow the label (the props module measured 17 % at boss_mark).
- No faces: the hand card's head lies beyond the right or top edge in every frame (checked on the frames).

## Hand-over
The worker of lane ADVANCE-X staged this take and started the final render, then returned before it finished. The render ended unattended. The main loop ran post, contact, qa and qa_md at 17:35 and looked at contact.jpg: no pops, no stale sprites, no black or magenta cards. Linear (constant-speed) camera runs are listed above; they are slow drifts and were not re-rendered.
