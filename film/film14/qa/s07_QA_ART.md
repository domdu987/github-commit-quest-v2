# QA-art, TAKE gate: film 14, s07 (shots 7-10, g403-764): FIX-FIRST (2 small blockers, shots 8-9 only)
Reviewed: take.mkv every 7th frame (~4 fps, 52 frames) at full 720x1280 and in 360x640 grids; extra full frames g410/500/620-638/700; every-4-frame strip g600-660 and every-6-frame strip g461-563; phone_sheet.jpg.

## What works
- Shot 7: the uncle's big laugh (eyes shut, mouth wide, tears) reads well on a phone; the farmer holding his hive with a calm smile is a clear two-shot. Warm DAY key, blue-violet contact shadows, sharp, no DOF.
- Lip-sync only inside shots 8-9 (as the plan says). The push-in from 7 to 8 to 9 is calm and always moving. Heads stay well above y 880.
- Shot 10: the uncle laughs inside the crowd, the woman and the old man laugh. The DUSK sky is warm and complementary.

## Scores (1-10)
| area | score | note |
|---|---|---|
| Set density | 5 | shots 7-9 have only the maize wall and two posts (a director choice after s01); shot 10 adds the shade roof and a hut |
| Light and colour | 7 | warm and clean; shot 10 is flat (soft, even light on the crowd); the dusk sky has a curved "dome" band |
| Composition | 6 | 7-9 OK; shot 10 is a thin strip of small people with ~33 % plain sky above and ~30 % bare soil below |
| Character acting | 5 | the laugh is good; the two planned gestures that set up the payoff are missing or wrong (see 1-2) |
| Key-moment clarity (boss / nickname) | 6 | the audio carries it; the picture does not show the nose bet |
| Match to references / client taste | 6 | right look, slightly sparse |

## Blocking (fix before conform)
1. **Shot 9, the nose tap is missing (g624-640).** cues.json says nose_tap g624-634 (21.04 s, "...ต่อยจมูกข้าเลย!"), but on every frame g600-663 his raised hand stops at shoulder or collar height, never near the face. This is the line the ending pays off (sting -> trunk nose), so it must be seen. Fix: in shot 9 only, bring the hand up so the index finger touches the nose tip by g630 and holds it there to g640, with chin up and chest out. Re-render ~40 frames.
2. **Shot 8, he points away from the farmer (g466-512).** The farmer stands at screen left, but the uncle's mocking arm points to screen right, out of the frame. With no sound, this does not read as "mocking him". Fix: make the point_mock arm the screen-left arm (or mirror the uncle card for shot 8 only), so the finger aims at the farmer or his hive. The raised-finger "bean" beat (g513-540) can stay as it is.

## Nice-to-have (do only if a re-render is happening anyway)
3. Shot 10 (g664-758): the kid (yellow cap, green shirt) has round, wide eyes, so he reads as scared, not laughing. Swap to his laugh face. Turn two or three of the arms that stick out sideways into points toward screen left (the farmer). Push in about 15 % so the crowd fills more of the frame and there is less plain sky.
4. Shot 7, g403-452: a hard-edged, softer and lighter band of ground at y ~1090-1280 (the ground texture edge). It sits under the caption, so it is low priority.
