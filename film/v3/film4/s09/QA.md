# s09 QA: film 4, shot 9 (year 1: the small quake), pagoda set v2, DAY

Delivered: `take.mkv` = `frames/g_0586.png .. g_0716.png` (131 frames, 720x1280, 12 samples, 2 threads, no captions / audio).
g 593..709 = shot 9 ([g0, g1) = [593, 710)); g 586..592 in-handle and g 710..716 out-handle rendered in 3D (cameras continue).
meta.json: first_g 586, n_frames 131, transition_in 10-frame dissolve, transition_out 10-frame dissolve, sub_ranges, frame_source.
Also cues.json, contact.jpg, compare.jpg (9a / 9b / 9c beside ref a t0039 / t0043 / t0041).
Scripts: `shot.py` = the engine of shots 9-12 (s10 / s11 shot.py load it): cameras per sub-shot, the quake clock `quake(g)`,
sway amplitude `sway_amp(g)` (G.set_sway, 1.1 Hz, storeys opposite ways, pillar the other way), `G.set_quake` (lanterns, wind
bells, loose tiles), crack / plaster levels, the take-only props. `deliver.py <take>`, `qa.py <take>` (-> `work/qa.txt`).

## Timing (captions_bankky.json, g = round((t + 0.1) * 30))
| sub | g | what | ref a |
|---|---|---|---|
| 9a | 593-628 | the set's two_buildings wide (slow push): pagoda left, master's tower right, the master small before it, arms crossed. Quake 1 from g 600 ("แผ่นดินไหว" 603), strength 0.45: lanterns / bells swing, slight camera shake; the pagoda starts to sway (0 -> 0.5 D by g 625), the tower does not move | t0039 |
| 9b | 629-661 (cut) | insert: a celadon-rimmed tea cup on a wooden sill of the master's tower, the tea dead flat with a still highlight, no ripple, no shake ("หอของช่างใหญ่นิ่งสนิท" 629-661, "นิ่งสนิท" ~644); slow push, DOF on the cup f 2.2 | t0043 (wine cup) |
| 9c | 662-709 (cut) | low up-shot of the pagoda ("แต่เจดีย์ของเขา" 662): storeys swaying opposite ways, one hand-span (0.5 D at the top); snap punch-in g 688-696 to the upper storeys, lands on "หนึ่งคืบ" 696; quake fades from g 700 | t0041 (insert rhythm) |
Framing changes: g 593, 629, 662, 688-696: gaps 1.2, 1.1, 0.9-1.1 s; then the out-handle.

## Staging / checks (`work/qa.txt`)
- 9a: master head 39-42 px (wide extra), y 0.64-0.65 H, above 880. kenta is NOT in the take (at his mark he fell half outside the wide; removed).
- No actors in 9b / 9c. Mouths: the master's never moves (arms_crossed, smug, closed).
- Popcheck: pops only at the two cuts (628->629, 661->662). Near-still transitions g 586-587 (in-handle, quake not started),
  629-631 and 659-660 (the cup insert's slow push, the tower is meant to be still); never more than 3 in a row.
- No black / magenta frames, no retried frames, no warnings in the final logs.
- Camera shake in 9a is deliberately small (0.012 x strength) so the tower reads still; the first render had 0.05 and jumped
  ~12 levels per frame (re-rendered).

## Colour (hue_report.row)
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s09 9a (g 593-628)                              3.2   26.6    0.1    0.0    0.0   67.3    1.5    1.4  0.48 0.71 0.04
s09 9b (g 629-661)                             23.8   10.8    0.0    0.0    0.0   52.1    1.2   12.0  0.45 0.39 0.35
s09 9c (g 662-709)                             10.8   12.3    0.4    0.0    0.0   68.9    4.6    2.9  0.64 0.56 0.08
s09 all (g 586-716)                             9.9   17.1    0.2    0.0    0.0   66.3    3.1    3.5  0.54 0.56 0.13
ref a t0039 t0041 t0043                        37.5   20.7    0.9    0.2    0.0   23.1   10.1    7.6  0.33 0.46 0.11
```
Exterior DAY sky makes 9a / 9c blue-heavy (ref is an interior). 9b magenta 12: the brown sill's shaded faces under the tower's skirt
roof read mauve (the set's own crack_insert stills are 9.5-19.5 for the same reason: plaster / wood in shade).

## Seconds per frame
8.5 s wall / 16.7 s CPU mean (9a 7.4 / 14.4, 9b 10.5 / 20.7, 9c 8.2 / 16.1), two render processes with 2 threads each.

## Differences from the plan / the reference
- The cup sits on a sill the take adds on the tower's south face (x 11.6-12.4, z 3.2, under the first skirt roof); the camera looks
  east along the wall, so the background is the tower itself (still), not the swaying pagoda: from the side where the pagoda is
  behind the cup, the cup was in its own shade and unreadable.
- 9c is our "insert" between the wides (ref t0041 is a frog insert); no characters.
- Sway: one span = 0.5 D at the top storey (two = 0.85, three = 1.2, the cap).
