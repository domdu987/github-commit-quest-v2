# QA: take s11 (shot 11, office, office_day = INTERIOR_DAY)

- **Frames.** Film frames g 694..791 are the shot; rendered g 687..799 (handles 7 in, 8 out for the dissolves), 113 final frames `frames/g_%04d.png`, 720x1280, Cycles 12 samples, 2 threads, one process.
- **Source.** `shot.py` (this take) on the shared runner `../s10/otake.py` (set `office3d` + `office_props`, stage actors, resumable render, streak post as `shots/post.py`). Numbers below: `python3 shot.py qa` -> `work/qa.json`.
- **Transition in.** {"type": "dissolve", "frames": 9, "note": "the chief's hand already swinging in"}

## What the take does

Take s11 = shot 11 (23.129-26.406, film g 694..791, handles 7 + 8): office, office_day. The erase-and-redraw running gag as
ONE stepped pull-out (persist_steps).
(a) insert_rake_ny on the N.Y. end: the chief's hand rubs three times (erase 0 -> 0.6), the smudge halo grows;
(b) same framing, the camera slides down 0.4 D and back up with the pencil: the hero's hand redraws the same bold stroke
    freehand along the hand-drawn track (erase 0.6 -> 0); no ruler (client change);
(c) snap out 24.35-24.82 to the low two-shot at the wall (low_two_wall): the chief rubs with big strokes (erase 0.8), steam,
    reddening; 'ลากอีก' the hero redraws in one 8-frame swipe with a pencil stub; the chief freezes, purple, eye twitching;
(d) snap out and up 25.33-25.80 to high_two_shot: bold red line in a halo of pink smudges, crumbs on the ledge, the chief pants
    with a worn nub, the hero at ease, chin up, the pencil stub in his hand; near still 26.0-26.27, then drift.
Hands in the insert are hand cards (the take-A method: a card facing the lens, standing just in front of the contact point,
scaled x1.8 so the elbow and the body are outside the frame); the bodies appear in the snap of (c).
    python3 shot.py probe|stills|draft|render|post|contact|qa [a:b[:s]]

## Camera (true 3D camera, corner speed in px per frame)

- move g 705-713 (film 23.50-23.80 s), peak g 708 at 17 px/frame
- move g 723-730 (film 24.10-24.37 s), peak g 725 at 14 px/frame
- move g 735-735 (film 24.50-24.53 s), peak g 735 at 12 px/frame
- move g 737-746 (film 24.57-24.90 s), peak g 740 at 148 px/frame
- move g 765-775 (film 25.50-25.87 s), peak g 770 at 157 px/frame
- static runs (< 0.25 px/frame): [[748, 748]]
- constant-speed (linear) runs: [[687, 696], [697, 700], [708, 710], [726, 727], [752, 757]]
- streaked frames (camera faster than 60 px/frame at the corners): [738, 739, 740, 741, 742, 743, 744, 767, 768, 769, 770, 771, 772]; plate under sharp actors: [744, 767, 768, 769, 770, 771, 772]; whole frame: [738, 739, 740, 741, 742, 743]

## Heads (720x1280 px, from the projected sprite anchors of every final frame)

| actor | frames | head width px | head centre y (px) | lowest head bottom y |
|---|---|---|---|---|
| bossH11 | 34 | 738-825 | 6-299 (0.00-0.23 H) | 623 |
| heroH11 | 32 | 659-820 | -690-456 (-0.54-0.36 H) | 817 |
| boss11 | 60 | 143-338 | 422-500 (0.33-0.39 H) | 650 |
| hero11 | 60 | 137-514 | 497-580 (0.39-0.45 H) | 719 |

Hand cards (names ending in H) are scaled hand cards whose heads lie outside the frame by construction.

## Pinned props (registration: rendered tip against the projected world target)

- bossH11.l: max 0.00 px
- heroH11.l: max 56.29 px
- boss11.l: max 29.18 px
- hero11.r: max 0.00 px

## Popcheck (mean absolute change of consecutive final frames, 180x320)

- pops (change > 1.8 x both neighbours and > 1 level): none
- median change 7.95, largest 48.10
- black or magenta cards retried: none; still wrong: none

## Colour (`tools/hue_report.py frames/`)

```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
reference A, whole clip                        33.6   23.1    0.7    0.5    0.5   29.1    2.7    9.7  0.48 0.63 0.08   OUT: sat,val,dark
reference B, whole clip                        24.5   34.1    2.4    0.7    0.2   28.6    4.5    5.0  0.41 0.57 0.08   OUT: red,dark
reference A interiors                          40.1   27.6    0.3    0.4    0.0   21.9    1.1    8.6  0.47 0.55 0.09   all in band
reference B interiors                          36.3   37.7    2.3    0.1    0.0   13.9    4.5    5.1  0.38 0.45 0.15   OUT: blue
target band: red 30-41, orange 22-38, blue 14-30, violet 0-5, magenta 0-10, sat 0.38-0.48, val 0.45-0.63, dark 0.08-0.15  (percent of chroma for hue families)
v3/film/s11/frames                             33.0   37.4    0.1    2.2    4.0   17.6    2.2    3.6  0.44 0.49 0.14   all in band
```

## Cost

- CPU seconds per final frame (min / median / max): [20.5, 21.9, 26.6]; wall: [15.4, 26.5, 33.6] (machine shared with other workers' renders)

## Deviations and notes

- Hands in the insert (a, b) are hand cards, the take-A method: the chief's and the hero's puppets at scale 1.5, facing the lens, standing 0.05 D in front of the contact point, so the drawn eraser face and pencil point register on the map. Their heads and bodies lie outside the frame and the elbows leave it at the right edge. These cards cast no shadow, because their scaled bodies would darken the map. Both hands enter from the room side (screen right): the insert lens stands where the hero's body is (hero_mark is 0.8 D in front of it).
- The full bodies are hidden in (a, b) and enter inside the snap of (c) at g 739, while the camera moves 100-200 px per frame; g 736-742 are streaked as whole frames so the entry does not pop. Physically the chief at boss_mark would stand in the insert's background at x of about 560: an accepted deviation.
- Erase states: 0 -> 0.6 in three 4-frame bites (g 698-711), 0.6 -> 0 with the pencil (g 716-732), 0 -> 0.8 in four frantic rubs (g 746-756), 0.8 -> 0 in one 8-frame swipe with the pencil stub (g 761-769). The smudge halo grows 0 -> 1 -> 2 -> 3; crumbs 0 -> 0.45 -> 1 on the ledge. No ruler (client change): the hero redraws the same bold stroke freehand, his pencil point pinned on the hand-drawn track (track_point).
- The chief stays 'frozen purple' through the start of the snap (d) and swaps to the panting drawing (worn eraser nub, prop scale 0.6) at g 771 inside the snap. In (d) the hero stands at ease, chin up, the pencil stub in his near hand (no ruler).
- In (d) the heads are 138-148 px (the reviewed high_two_shot, wide, as planned). The hero stands at x of about 100.
- Red line: the client's hand-drawn track (office3d TRACK_STYLE 'hand'); every frame of this take was rendered after 18 Nov 14:40 (version 3), no ruler anywhere. Everything that touches the line (eraser, pencil points, smudge halo, camera look-at points) is placed with S.track_point(u) of the hand-drawn track.
- Colour: the ungraded render sits inside the office_day band (red 33.0, orange 37.4, dark 0.14), so this take is delivered ungraded. (s10 and s09 carry the mild band grade ../s10/grade.py because their framings hold more red wallpaper; a test of that grade here pushed red to 29 and orange to 41, out of band.)
- Registration: the hand cards and the chief's eraser are pinned on the erase front of the hand-drawn track (0.0 px in the inserts). In the four frantic rubs of (c) the chief's arm reaches its limit at the end of strokes: 4.7-10.3 px on g 751-754, 29 px on g 756 and 21 px on g 759 (the release stroke, the eraser leaving the paper); g 740 (heroH11 56 px) is a whole-streaked snap frame in which the hand card leaves.
- Head bottoms: the hand cards (bossH11, heroH11) are scaled hand cards whose heads lie outside the frame by construction; hero11 and boss11 are whole, bottoms at most 719.
