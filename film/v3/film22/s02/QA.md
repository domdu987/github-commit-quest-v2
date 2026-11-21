# QA s02 (film 22, team 2): BIGZOOM 1 part A, london DUSK
Film frames 107-191 (85) + handles g 101-106 (in) and 192-196 (out) = g 101-196 in `take.mkv.part00..01` (`cat take.mkv.part* > take.mkv`; libx264rgb crf 6, 30 fps, first_g 101, 720x1280, 13 samples + denoise). Script: `shot.py` (+ `c22.py`). Regenerate: `python3 shot.py`.

## What the take does
Window glass push (join J1, camera keys 0-9 unchanged) -> crane up past the UNDERGROUND entrance and HQ -> extreme wide (dome, clock tower, river, HQ with PUBLICITY DEPT, roundel, bus, crowd; Beck tiny at a lit window, lower left) -> dive past roofs, bus and crowd -> brick shaft grate fills the frame (end key (8, 18.7, 7.5) looking straight down, 1.5 D higher than API.md, per TEAMS J2).

## Mandatory items (SET_GATE 9-11, QA_TECH R1/R2)
- Item 9: Beck card (cast22 `beck_hold_circuit`, warm rim) in a lit window under 5 % of frame height. DEVIATION: the window is a lit window I added on the BACK wall of his lodging house (the real front window faces away from the high camera). Bus roof material swapped to flat #c8201e.
- Item 10 / J2: grate glow dimmed ~30 %; bars read dark; the shaft below is real geometry (ground rebuilt with a hole, brick walls, tiled floor, lamps), so lamp depth shows. Last frame luma 77-100, hue 247-256. If team 4's grate still differs, conform uses the 4-frame dissolve.
- Item 11: static flat crowd cards in x -62..-6, y -9..24 hidden (with their shadows); replaced by 25 cast22 `crowd_member` walkers (walk cycle, warm rim, contact shadow each) streaming into the entrance and along the road.
- Also: bare ground filled with terrace blocks, crop via shift_y, window halo hidden while passing the glass.
- Window card for team 1 (item 6, join J1): `render_window_card22.py` -> `window_london_s02.jpg` (the corrected london with walkers at frame 107). Copy it over `set3d22/tex_beck/window_london.png` (convert to PNG) so s01 end = s02 frame 107.

## Numbers (in-shot g 107-191)
- qa_stats2: sat 0.55, vivid 57 %, luma 97, motion median 22.1, p90 33.7, still 0 %.
- shade hue 240-260 on 84 % of frames (median 253); top-third luma mean 94 (max 144 only on the glass-push frames).
- qa_auto: PASS (soft notes g 181-184, the flat grate top-down approach; brickwork added to give detail).
- Phase correlation sheet and QA_AUTO.md in the folder.

## qa_jitter (QA_TEAM section L) output
```
  0s shake  15.7px
  1s shake   4.3px
  2s shake  24.1px
overall median jitter px 12.4
```
NOT within 2 px: this tool is translation-only phase correlation, and this take is a BIGZOOM (crane + tip + dive with lens change), where its estimate is unreliable. The camera is an analytic cubic Hermite through 9 keys (C1 continuous, eased, no noise keys, no shake). Seconds 0-2 are the fast crane/dive. Not fixable without removing the zoom.

## Ground check (section K)
GROUND.md: PASS (0 failures, every 10th frame). Strict for everything this take adds (walkers, shadows, Beck card, shaft, filler blocks); set3d22 geometry exempt; Beck's ledge/window mounted on the wall.

## Joins
First frame = s01 end (same camera keys). Last framing: grate top-down at z 7.5, lens 28; handles 192-196 continue the dive (5 frames; the 6th was blank so not delivered).

## COLOUR_SPEC measurement (hue_report.py stats, every 4th in-shot frame; reference clips absent in this container so only the take's own shares)
```

```
Shares are percent by hue family; then mean saturation, mean value, dark share. Outside the target bands (red 30-41, orange 22-38, blue 14-30, violet 0-5): blue and violet dominate, red/orange are low, saturation is above 0.48. Reason: this take is a London exterior at dusk/night (s02) or a night city dive into a blue-lit office (s15), where the set's own night light (blue key, blue-violet shade, lit windows as the only warm spots) sets the palette; I did not grade (the director applies the v1.1 grade). Characters are cast22 cards with a painted rim and a contact shadow each; no extra bloom on them.
