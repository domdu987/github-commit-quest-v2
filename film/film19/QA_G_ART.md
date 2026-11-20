# Film 19 — QA-art, client rules G2 (nothing floats) and G3 (camera distance)

Reviewer: QA-art (Opus), 2026-11-20. Colour (G1) and section H are out of scope here.

## Source and method
- Section G is **not** in the checked-out `film/QA_TEAM.md`. It exists only on `origin/claude/new-session-73ou27:film/QA_TEAM.md`, and I judged against that text. That branch should be merged so the rule is on the working branch.
- `release19/sheet_1fps_v1.jpg` has 72 tiles, **1 tile per 1 s** (0-71 s).
- `release19/sheet_phone_360x640_v1.jpg` has only 24 tiles, **1 tile per 3 s** (labelled 0, 3 … 69 s). Its labels also run about 1 s early against the 1 fps sheet: the "0s" tile shows the 1 s caption "บอกว่านาฬิกา", and the "3s" tile shows the 4 s caption "ทะเล". **It is not the 0.5 s phone sheet that rules A5 and G2 require. Regenerate it before the FINAL gate.**
- To cover G2 anyway, I checked all 26 `v3/film19/sNN/contact.jpg` sheets, 16 tiles per shot at about 0.2-0.27 s apart, which is denser than 0.5 s. I also took 46 extra frames from `release19/harrison_v1.mp4` and measured them with a 10 % height grid. The frames are in `/tmp/qa19g/`.
- **Face height** is the white head disc, from brow to chin, without the wig or hat, as a share of the 1280 px frame height. The limit is 35 %.

## Shot table

| shot | distance class | max face height % | floating / intersect issues | half-cut | verdict |
|---|---|---|---|---|---|
| 01 | MEDIUM (waist-up behind bench, room visible) | ~22 | none; body rests behind the bench, plane and shavings on surfaces | no | PASS |
| 02 | WIDE (aerial ship) | n/a | none | no | PASS |
| 03 | MEDIUM-WIDE | ~20 | telescope tube passes just *behind* astro19's head (4.0 s, 5.9 s), reads as behind, note only; feet on carpet | no | PASS |
| 04 | MEDIUM-WIDE (pushes to medium at 8.0 s) | ~20 | captain grounded with shadow; lantern hangs on a visible rope and swings (motion) | no | PASS |
| 05 | MEDIUM-WIDE | ~12 | sailors on deck; hatch and spar in FG rest on the deck | no | PASS |
| 06 | MEDIUM-WIDE | ~17 | money bag in the air only while falling (12.5-12.7 s, motion) | no | PASS |
| 07 | MEDIUM-WIDE | ~12 | three figures on carpet with shoe shadows; chair in front of astro19_c is plain occlusion | no | PASS |
| 08 | MEDIUM (full body, pushes to knees) | ~26 | telescope tube runs behind wig at 21.4-22.0 s (behind, note) | no | PASS |
| 09 | CLOSE | **~44** (over 35 % from about 24.9 s to the cut at 25.78; 39 % at 25.2, 44 % at 25.5) | none | legs and body cut by bottom edge (close framing) | **FIX** |
| 10 | WIDE | ~12 | figures behind table, Harrison grounded at door | **YES**: at the snap to Harrison, 28.10-28.74 s, an astronomer is halved by the left edge and another is cut about 30 % at the right edge (frame 28.2 s) | **FIX** |
| 11 | MEDIUM-WIDE | ~24 | file held in hand; FG bench is occlusion | no | PASS |
| 12 | MEDIUM, ends CLOSE | **~40** (over 35 % from about 32.25 s to 32.85 s; 37 % at 32.3, 40 % at 32.6) | none | no | **FIX** |
| 13 | MEDIUM | ~18 | only head and shoulders show above the bench and H3 case, but the bench reads as the surface (OK); two small white marks under the bench at 32.9-33.0 s move with the set (drawer knobs), not debris | no | PASS |
| 14 | MEDIUM (MW opening, push to H4 insert) | ~20 | H4 rests on the red cloth on the bench | Harrison's head about 40 % out of the **right edge** at 36.10-36.50 s (frames 36.17, 36.2, 36.37) | **FIX** (minor) |
| 15 | MEDIUM-WIDE | ~16 | strong deck shadows, grounded | no | PASS |
| 16 | MEDIUM (wide first 1.2 s) | ~25 | grounded | no | PASS |
| 17 | WIDE | n/a | none | no | PASS |
| 18 | WIDE | n/a | none | no | PASS |
| 19 | MEDIUM-WIDE | ~14 | sailors on sand with blue shadows; tricorne held in hand; shell rests on sand | no | PASS |
| 20 | MEDIUM (MW start, push to close) | ~36 (54.9-55.49 s, borderline) | none | no | **FIX** (minor) |
| 21 | MEDIUM-WIDE | ~14 | **quadrant swings across William's face**, 57.9-58.2 s (frame 58.07); it also overlaps astro19_c's own head at 55.9-56.2 s | no | **FIX** (minor) |
| 22 | MEDIUM-WIDE (ends MEDIUM on astro19) | ~30 | tall chair back in front of astro19 at 61.0-61.86 s is 3D occlusion, not slicing (note) | Harrison half out of the **left edge** at 60.8-61.0 s during the push | **FIX** (minor) |
| 23 | MEDIUM-WIDE | ~14 | Harrison on the floor with shoe shadow; the door covering him at 61.8-62.0 s is occlusion | no | PASS |
| 24 | MEDIUM-WIDE (ends MEDIUM) | ~22 | king behind table and cabinet; candle stubs rest on the table | no | PASS |
| 25 | MEDIUM (MW start, snap to close) | **~40** (over 35 % from about 69.25 s to the cut at 69.55; 37 % at 69.3, 40 % at 69.45) | none | no | **FIX** |
| 26 | MEDIUM | ~20 | bag only airborne while landing at 70.1-70.3 s | **YES** on the ending: the king is about 40 % out of the right edge at 71.6 s, then Harrison is about 30 % out of the left edge at 71.8-71.9 s (the last frames of the film) | **FIX** |

## G3 summary
- **WIDE or MEDIUM-WIDE: 16 of 26 shots = 62 %** (WIDE: 2, 10, 17, 18; MEDIUM-WIDE: 3, 4, 5, 6, 7, 11, 15, 19, 21, 22, 23, 24). The limit is 50 % or more. **PASS.**
- **Face over 35 %:** shots 9, 12 and 25 (about 40-44 %) and shot 20 (borderline, about 36 %). Every one comes from the end-of-shot snap or push-in. **FIX.**
- **Half-cut by a frame edge:** shot 10 (blocking), shot 26 (blocking, because it is the ending), and shots 14 and 22 (minor, transient).
- **Room angle repeats:** the longest run is 2 (4-5 ship_rocks, 8-9 hall_low, 15-16 ship_deck). Shots 6 and 7 both face the arched window, a run of 2. **PASS.**

## G2 summary
- Every character stands on deck, floor, carpet or sand, or behind a bench or table, and shows a contact shadow. Hall shots have small shoe shadows (checked at 17.0, 19.0, 53.3 and 67.9 s); deck and beach shadows are strong.
- No heads or bodies hang in the sky.
- No grey slabs slice a character.
- Nothing hangs static in mid-air: the money bags (shots 6 and 26) and the lantern (shots 4 and 5) are always moving.
- The only prop-across-face hit is shot 21 (the quadrant over William's face).
- The telescope tube passing behind heads in shots 3 and 8 is a note, not a fail.

## Overall verdict
**FIX: not yet passing G2/G3.** The distance mix is good at 62 % wide. 7 shots need fixes: shots 9, 10, 12, 25 and 26 must be fixed, and shots 14, 20, 21 and 22 should be fixed. Shot 20 is borderline. The phone sheet also has to be regenerated at 0.5 s before the FINAL gate.

## Fixes
- **s09:** cap the "จับเวลาเอง" push-in at about 30 % face. Stop the push about 12-15 % earlier, or end at the 24.9 s framing, so the face stays at or under 35 % through 25.78 s.
- **s10:** reframe the snap to Harrison (28.10-28.74 s) so no astronomer sits halved on the left or right edge. Either slide further so the two edge figures leave frame completely, or widen until they are fully inside. Harrison at the door stays the subject.
- **s12:** shorten the push. At 32.0 s the face is about 23 %, which is good; hold near 30 % at most through 32.85 s.
- **s14:** in the final 0.4 s (36.1-36.5 s), keep Harrison's whole head inside the right edge by slowing the slide, or keep him fully out.
- **s20:** trim the end push by about 10 % so the face is about 32 % at 55.2-55.49 s.
- **s21:** keep astro19_c's quadrant swing clear of William's head at 57.9-58.2 s. Either move astro19_c about 0.3 D left or lower the swing arc. Also avoid the quadrant covering astro19_c's own face at about 56 s.
- **s22:** on the push at 60.8-61.0 s, either keep Harrison fully in frame or let him clear the left edge sooner. Do not leave half a face on the edge.
- **s25:** cap the "เป๊ะ" snap at about 30-33 % face (it is 37-40 % at 69.3-69.55 s). The comic shock pose reads at medium.
- **s26:** recompose the end move (71.5-71.9 s) so that both old Harrison (grinning) and the King are entirely in frame on the last frame of the film. The push-in should end centred on Harrison with the bag, without swinging him onto the left edge.
