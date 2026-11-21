# QA s15 (film 22, team 2): BIGZOOM 2 and the ENDING, london NIGHT -> publicity room
Film frames 1752-1889 (138) + 10 in-handles g 1742-1751 (match dissolve 15) = g 1742-1889 in `take.mkv.part00..01` (`cat take.mkv.part* > take.mkv`; crf 6, 720x1280, 13 samples). No out handle (hard end on the last word). Script `shot.py` + `c22.py`.

## What the take does
Extreme wide over night London (HQ, dome, clock tower, river, stations glowing, walking crowd) -> dive past roofs and the red bus to the lit PUBLICITY DEPT window (59.84 s) -> glide through the window opening (60.35 s) -> official at his desk, napkin, knife and fork with a map, cheeks puffed, sweating, mouth closed, towers of pocket maps to the ceiling -> a crate of maps lands on his desk at frame 1856 (61.72 s) with contact shadow and a small bounce, he gulps (puff pulse) -> ends MEDIUM, official 42 % of frame height (head to desk line), face about 26 %.

## Fixes of the weakest tile (SET_GATE 12)
- End key re-done: camera (0.2, 39.0, 10.5) lens 33 looking at the official; ceiling 0-5 % of frame, desk front and floor 15 %.
- Card was leaning back 47 deg toward the far build camera and hid behind the chair: now re-created per frame with the real elevation tilt (own `off_card15`), so face, napkin, fork+map and knife read.
- Own towers (14 stacks, gain lowered, reaching the ceiling), crate lands on the desk at 1856 (contact + shadow), warm desk lamp x1.6, cool painted rim on the card, pendant lamps x0.4, clock glow x0.35; NIGHT ambient raised ~1.35x so the start reaches luma 85+.
- Ink hulls: one build per distance range (builds at k 12, 54, 100) so the close-ups do not get thick outlines.
- Fill blocks for the bare ground, walkers replace the static crowd cards (heads in the caption band), crop via shift_y.

## Numbers (in-shot g 1752-1889)
sat 0.63, vivid 59 %, luma 104.9 (qa_stats2 105.5), shade hue 240-260 on 90 % of frames, top-third luma mean 100 (max 128). Motion median 13.0, p90 37.1, still 0 %. qa_auto PASS (soft notes g 1820-1824: the window frame crossing). Magenta 0 %.
Last frame (g 1889): sat 0.61, luma 100, hue 255.

## qa_jitter (QA_TEAM section L) output
```
  2s shake  17.5px
overall median jitter px 0.75
```
One second (the fast glide through the window, a zoom) exceeds 2 px on this translation-only estimator; the rest of the take is 0.75 px median. Camera is an eased Hermite path, no noise keys. Not re-eased further because the through-window move is the planned push-through.

## Ground check (section K)
GROUND.md: PASS (0 failures). Strict for walkers, shadows, towers, crate (airborne only while falling), filler blocks; the seated official is mounted (seated on his chair, legs hidden by the desk); set3d22 geometry exempt.

## Differences from the plan
Official is seen from slightly right of centre and the crate is only partly in frame at the very end (it is fully visible at 1856-1870 when it lands); signs: PUBLICITY DEPT reads at 360x640.

## COLOUR_SPEC measurement (hue_report.py stats, every 4th in-shot frame; reference clips absent in this container so only the take's own shares)
```

```
Shares are percent by hue family; then mean saturation, mean value, dark share. Outside the target bands (red 30-41, orange 22-38, blue 14-30, violet 0-5): blue and violet dominate, red/orange are low, saturation is above 0.48. Reason: this take is a London exterior at dusk/night (s02) or a night city dive into a blue-lit office (s15), where the set's own night light (blue key, blue-violet shade, lit windows as the only warm spots) sets the palette; I did not grade (the director applies the v1.1 grade). Characters are cast22 cards with a painted rim and a contact shadow each; no extra bloom on them.
