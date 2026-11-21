# QA s09 (team 4): the ticket hall, g 1005-1196 (+6 handle frames each side, file g 999-1202, 204 frames)
take.mkv is split (`cat take.mkv.part* > take.mkv`, libx264rgb crf 6, 30 fps, 720x1280).

## What is in it
- Crane DOWN from the ceiling lamps (2,-8,12.5) to the leaflet stand, then low through the hall toward the pillar; dissolve 11 in (handles 6 + 5 included).
- 33.55 s porter sets the SMALL stack of pocket maps (setter set_trial_stack 1 stack, then 2), 35.03 s hands a few maps out (porter, pass_woman, pass_child, pass_man-less foreground), 36.19 s (local 84) the official slides out from behind the pillar and peeks (smug), from local 117 he rubs his hands: Q2 lip-sync 37.38-39.90 (g 1122..1197, the file keeps lip-sync to the handle) with four mouth cards (flat / talk_a / talk_b / talk_o from cast22.talk_mouth, new drawing every 2 frames) x two hand-rub phases.
- Crowd: the static hall crowd near the camera path and the camera-to-pillar sight line is hidden; six cast22 crowd walkers (walk-cycle cards, shadows attached) cross the hall at the back and sides.
- Set gate item 20: the official is visible from 36.19 s to the end, face and mouth readable (head about 22 % of the frame at the end); pass_man moved off the line (x <= -3 is out of frame, he is not in the take any more), pass_woman inside the frame edges; the floor share drops under 25 % after the crane (the crane frames at the very start are mostly checker floor by design).

## Numbers (take.mkv)
```
STATS
take.mkv       dur   6.8s shots   1 mean 6.80s med 6.80s <1s  0 >4s  1 | sat 0.649 vivid% 68.7 luma  94.3 contrast 46.2 detail 10.08 warm  6.8% cool 80.2% | motion med 8.59 p90 14.43 still%  0.0
JITTER
overall median jitter px 0.27
AUTO
# QA_AUTO PASS  (take.mkv, 204 frames, 30.00 fps, g 999-1202)

## Notes
- magenta share 0.0 %

Phone sheet: phone_sheet.jpg (cyan line = caption band y 880). Judge legibility on it.
GROUND RESULT: PASS (0 failures)

```
- Required: sat >= 0.50 (0.65), vivid >= 45 % (68.7), luma 85-110 (94.3): PASS. Frame diff median >= 4 / p90 >= 12: PASS (8.6 / 14.4).
- qa_auto PASS. qa_jitter: no second above 2 px (overall median 0.27 px). The camera is Hermite-eased between 6 keys, no noise.
- Section K: GROUND.md = PASS. Fixes made for it: pendant globes marked mounted (rods run to the ceiling), the entrance WAY OUT sign hidden (behind the camera, it hovered above the door frame), floor light pools lowered 4 cm onto the floor, and the TRIAL sign got real struts into the stand cap (the sign used to float 2 D in front of the stand top). Every card has a contact shadow.
- Heads above y 880 in every frame (phone sheet checked at 0.5 s).
- Known minor item: while the camera pans left (g 1104-1134) the porter leaves the frame at the right edge, so he is cut by the edge for about 1 s on his way out. The official's pillar covers about a third of the frame at the end (he peeks, it is the plan).

## Joins
- In: dissolve 11 from s08 (corridor). Out: s09 -> s10 is the hard CUT on "แต่วันนั้น" (the take ends in the official's Q2 line; s10 starts at 39.90 s).

## Colour (film/COLOUR_SPEC.md, film/v3/tools/hue_report.py `stats` on every 3rd final frame, caption band excluded)
```
set     red orange yellow  green   cyan   blue violet magent   sat  val dark | target red 30-41, orange 22-38, blue 14-30, violet 0-5, magenta 0-10, sat 0.38-0.48, val 0.45-0.63, dark 0.08-0.15
s03     12.6    8.2    2.3    1.0    0.6   61.9    4.6    8.8  0.73 0.68 0.00   OUT: red,orange,blue,sat,val,dark
s09      1.8    3.1    1.0    0.1    0.7   71.4    9.9   11.8  0.66 0.57 0.00   OUT: red,orange,blue,violet,magenta,sat,dark
s10      6.2    7.9    1.8    1.2    0.2   58.5    6.5   17.8  0.68 0.59 0.01   OUT: red,orange,blue,violet,magenta,sat,dark
```
Ticket hall interior lit by warm globes under a violet-blue shade tint (set preset HALL). Blue 71 %, red 1.8 %, orange 3 %, violet 9.9 %, magenta 11.8 %: clearly outside the new bands (too blue/magenta, too little red/orange). I did not grade. Not graded by team 4 (the director applies the v1.1 grade). The set light presets (UNDER/HALL) are the cause; a per-take re-light (more warm key, less blue shade) would be needed to reach the bands and was not done. The tool itself could not run its reference rows here (the reference clips are not in this container).
