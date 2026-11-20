# QA-art FINAL-fix s16: FIX-FIRST

- Reviewer: QA-art, last FINAL-fix check, 2026-11-20. Take `take.mkv`, 120 frames, g1195-1314 (in-shot g1205-1308).
- What I checked:
  - every 6th frame on a phone sheet with the band marked (magenta y 860, cyan 880/950);
  - full-res frames g1240, 1268, 1280, 1292, 1300 and 1308;
  - a y 780-930 strip every 4 frames from g1236 to g1308;
  - 4x zooms on the girl;
  - a per-frame measurement of the girl's visible face;
  - old (release v1) against new at g1268, 1292 and 1300.
- Evidence is in `scratchpad/qafin3/`: `s16_sheet.jpg`, `s16_fullA.jpg`, `s16_fullB.jpg`, `s16_band_a.png`, `s16_band_b.png`, `s16_girl_zoom.png`, `s16_girl_tail.png`, `s16_oldnew.jpg`.

## Blocker B3 (the girl's face in the caption band): NOT GONE. It has moved later in the shot.
- The g1268-1292 window is fixed. She is small and behind the baskets, and her visible face (eyes) sits at y ~840-875, so it never reaches 880 there.
- **But the camera keeps dollying, and she drifts down and left.** Her visible face (the white strip with both eyes, above the basket or rubble rim) is at:

  | Frames | Visible face, y |
  |---|---|
  | g1296 | ~872-880 |
  | g1300 | ~877-887 |
  | g1304 | ~882-895 |
  | g1306-1308 | ~885-900 |

  Her eyes are at about y 887 on g1306. Her bun tops are at about y 855-865 from g1300, not at 835 or less as the team note says.
- This is inside y 880-950 for about g1298-1308 plus the handle, during the caption "รูหลายสิบรู" (42.54-43.80 s = g1276-1314).
- The caption text (x ~230-490) does not physically cover her (x ~0-170). But the hard rule is "no face in y 880-950", and the brief for this fix was "face above y 860". It breaks both.
- **Fix (cheap, only the girl):** take the girl out of s16 for the whole take, and re-render the 120 frames.
  - She is hidden behind the baskets anyway and adds nothing to the digging beat.
  - Removing her for the whole take means there is no pop.
  - Otherwise, push her at least 2 D further back or up the wall, so her face stays at y ≤ 850 through g1314. Verify on g1295-1314, not just g1250-1300.

## Beat on phone (holes dug in the wall at night): READS
- Diggers swing picks at the lit wall base, and breaches open one after another with warm light. The holes stay in frame through the end.
- Apart from the girl's position, the picture matches the release v1 (compared at g1268, 1292 and 1300).

## Other hard rules
- **Pole through a face:** none. The ladder passes beside the left digger at g1236-1248 and does not cross his face. The pick handles are clear of faces.
- **Half-cut main character:** none. The edge-clipped diggers are extras.
- **Floating:** none.
- **See-through:** none.
- **Old man (foreground digger):** his face is above y ~860 and only his beard reaches the band. That matches the s17 elder precedent and is unchanged from v1.

## Notes (non-blocking, already present in v1 at FINAL)
- **N-s16-1:** There are pale thin "needle" shards on the ground (for example g1292 at x~550, y~1090, and g1300 at x~410, y~1190). There is also a flat white-yellow glow quad on the ground at y ~940-960 from about g1295. Both were in the release v1 and were not flagged at FINAL. Clean them up if the re-render pass is cheap.
