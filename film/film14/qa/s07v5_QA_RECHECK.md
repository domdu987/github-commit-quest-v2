# s07 v5 TAKE-gate re-check (shot 10 only, g664-758), round 5   VERDICT: FAIL (2 blockers)

Checked: all 362 frames extracted (g403-764); every 3rd frame g655-764 at full size (720x1280) and phone size (180x320 sheet, cyan line = y 880);
2x crops of uncle/old man g667/685/700/715/730/748/758; farmer crops g670/715/755; kid every frame g700-723; per-frame mean abs diff g640-764 plus regional diff at g715.
Working files: scratchpad/takes/qa5/ (phone_sheet.jpg, crop_mid.png, farmer.png, kid_700_723.png, pop714_715.png, all/, ev3/).
Narration: "คนทั้งหมู่บ้านหัวเราะตาม แล้วเรียกเขาว่า ไอ้บ้าผึ้ง"

## Tech: PASS
- Cut at g664 (diff 63.2) only. Elsewhere 1-4.3. g715 (4.3) is a small whole-body bob of uncle/old man (a few px, same pose), not a pop.
- Heads: all heads y ~440-640 (log 466-640), chins well above y 880 in every frame. Nobody clipped except the farmer's straw-hat brim/veil touching the left edge x 0 (non-blocking).

## Acting checks
| check | status | evidence |
|---|---|---|
| Farmer = worried target with hive | PASS | Wide round eyes, 'o' mouth, sweat drop, both hands on the hive box at his chest, all shot. Reads worried at phone size. Smirk gone. |
| Uncle points at him while laughing | FAIL (weak) | Uncle laughs (eyes shut, open mouth), but his screen-left teal arm ends as a blunt mitt resting on the hive lid; the "finger" is a thin dark line that runs up to the farmer's cheek, so it still reads as touching/poking or reaching for the hive, not a point. Not readable at phone size. |
| Old man cackles | PARTLY | Eyes shut, tear drops, open mouth, hand on hip = laughing. But see next row. |
| Kid bangs the pot | FAIL | g700-723 frame by frame: pot held flat to his chest by both green hands, no spoon/stick visible (only a dark stub at his right hand), no hit motion, only a 1-2 px bob. Identical to v4. |
| No arm covering a face | FAIL | Uncle's screen-right teal arm still crosses onto the OLD MAN's face and covers his mouth/beard in every frame g664-758 (crop_mid.png). Same as the v4 blocker. |

## Blockers (round 5)
1. **Uncle's screen-right arm covers the old man's mouth/beard all shot (g664-758).** Put that arm down / on his own belly, or move the old man 40+ px right so nothing overlaps his face.
2. **Kid does not bang the pot.** Needs a visible spoon/stick (>=6 px thick, contrasting colour) held clear of the body and 2-3 clear up/down hits (>=15 px travel) onto a pot held low. The current bob is invisible.
Should fix with these (also blocking the "laughs AT him" read): uncle's pointing hand must show an index finger stopping ~40-60 px short of the farmer, not a blunt hand on the hive plus a line to his cheek.

## Non-blocking
- Farmer's hat brim/veil touches the left frame edge.
- Crowd sits small in the frame (heads ~135 px) with ~350 px of empty ground below; fine for captions.
- Shot 8 pinch claw, grey foreground twigs (unchanged).
