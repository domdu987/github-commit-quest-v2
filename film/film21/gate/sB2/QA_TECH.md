# QA-tech sB2 (team5 9fa3189)

**Verdict: FAIL** (2 blocking, both about the Scots payoff; the travel itself is good).

Checked: every 5th frame g295-415 (f6), full-size frames g295/298/405/413/418, handles, team QA.md, meta.json. qa_auto PASS, rhythm 21.3 / 27.3 (fine).

## Beat table
| g | beat | read at phone size | verdict |
|---|---|---|---|
| 295-298 | handles + P_CAMP: parade of red/gold knights and footmen, ENGLISH CAMP sign, tents, light shafts | Camp readable, soldiers tiny (about 40-60 px) but a wide shot; g295 to g298 differ only slightly, a correct continuation of B1 (the move runs backwards, fine for the D6) | OK |
| 298-325 | crane up over the pavilions, striped canopies fill the lower frame, parade falls away | Moves, rich set, no floating | OK |
| 325-350 | fly NE over the river, bridge on the left, glitter | Moves clearly; river is saturated turquoise with white shore line and fills about 40 % of the frame (see issue 3) | OK, see 3 |
| 350-376 | meadow bank, trees with shadows, Abbey Craig ahead with light shafts | Clear, pines visible; empty of characters for about 2 s | OK, see 4 |
| 376-398 | climb to the foot of the crag, pines, shafts | Good; shaft glare at right g385-405 is bright but not covering the subject | OK |
| 398-418 | land and arrive on the Scots: five blue-tunic spearmen on the slope | Scots appear only from about g392 (about 0.9 s), 130-190 px tall (10-15 % of the frame), heads y 600-800 (OK) | FAIL, see 1, 2 |

## Checks
- Heads above y 880: pass (Scots y 600-800, English parade far up the frame).
- Nothing floats: pass. Scots have contact shadows; the Scot behind the brown rock/boar shape at the bottom centre is covered to the knees, reads as standing behind a boulder (ok).
- Nobody cut by the frame edge: pass. Face over 35 %: pass (max about 6 %).
- Characters acting: English parade walks the whole time g295-330. Scots shift in the last 25 frames; nobody still over 1.5 s on the visible figures. The spear shift and "one leans on his" cannot be read at this size (issue 2).
- Camera clearance: pass, no pine, crag or banner clipping the lens seen; left-edge pine trunk g405-418 is close but clear. Hidden banners: none near the lens.
- Smoke/banners near the lens: none.
- Bloodless: pass. Mouths: Scots mouths closed (checked at g413-418).
- Join: g418 is exactly P_HILL raised 0.8 m, the camera is still moving at the cut, which is good for the cut to C.

## Issues
1. **BLOCKING, g395-418: the landing is not the plan's "LOW hero angle looking up at the Scots against the sky".** The camera ends above the Scots looking down the slope; the hill's grass slope is behind them, the sky and pines are above them. They are not silhouetted against the sky and there is no hero feeling. The team notes it as "P_HILL is a fixed pose". Fix: lower the end pose (about 1.0-1.5 m, below the Scots' hip height) and tilt up, or lift the Scots' stand points to the crest line so they read against the sky; the 0.8 m raise of hill_low is what makes it look down. Keep the same trajectory, only change the last 30 frames; P_HILL is not tied to any neighbouring segment (C is a cut), so the change is free.
2. **BLOCKING, g392-418: the narration is about the Scots ("ส่วนฝั่งสกอต" from g298) but they are on screen for only about 25 frames, small, and their action cannot be read.** Fix: make them larger (end closer, about 4-5 m instead of 8-10 m, so figures are 25-35 % of the frame height, heads still below y 880) and start them entering the frame earlier (about g380), with the lean on the spear a big readable swing (about 0.15 D) and spear shifts at 1-2 Hz.
3. **Non-blocking, g330-375: river colour.** The turquoise water with the white shore line is a neon-like field filling about 40 % of the frame. The set palette is content. Fix if a re-render happens anyway: pull the river toward a deeper blue-green, or frame the meadow bank more than the water.
4. **Non-blocking, g350-392: about 1.3 s with no character in frame.** The rule is "characters acting", and the plan has glitter and the bridge here. Fix: add a few distant English soldiers on the bridge or bank, or Scots scouts on the crag foot.
5. **Non-blocking, g298-310: soldiers of the parade tiny.** The crane-up leaves them at about 40 px quickly. Optional: slow the first 12 frames of the crane so the parade stays readable through the D6.
6. **Non-blocking: take.mkv is split in two parts (partaa/partab, 40 MB) and the full take.mkv is also present.** Make sure only one form goes to the conform.

## Re-render scope
Only the last about 40 frames (g378-418) need re-rendering for issues 1 and 2; the rest can be kept.
