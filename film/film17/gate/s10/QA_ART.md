# QA-art, film 17 take s10 (THE REVEAL, shots 24-26, g1336-1520, narration 44.65-50.41): FIX-FIRST

Reviewer: QA-art (opus), TAKE gate for a key shot (QA_TEAM.md, Stricter QA C). The client delegated approval to QA, so this verdict decides the take.
Material reviewed: phone_sheet.jpg (360x640) first, then contact.jpg, then the full-res f6 frames. I looked closely at g1366, 1371-1386 (whip), 1401, 1404, 1408, 1411, 1436, 1459-1466 (snap), 1481 and 1511.
Numbers: rhythm in-shot median 4.90 / p90 15.14 (target >= 4 / >= 12), so it passes. qa_auto: 39 "soft" frames (judged by eye below).
Narration: "หัวยาวระดับนี้ เปิดลิ้นชักหัวยาว / นิ้วขนาดนี้ เหลือกล่องเดียว / หูขนาดนี้ เหลือการ์ดใบเดียว". This line explains the mechanism: measure, then narrow to a drawer, then a box, then one card.

## What a first-time phone viewer gets now
| Beat | Reads at 360x640? | Why |
|---|---|---|
| Head measured | **No** | At g1342-1366 the calipers are a horizontal bar at Dupont's chin and chest height (g1366: bar at y~860 full-res, below his face). They point AT him; they do not span his head. QA.md says the calipers "settle ON Dupont's head", but the frames do not show that. The words say "head this long", and the picture shows nothing being measured. |
| Long-head drawer yanked | **Weak until g1411** | During g1381-1404 Bertillon's large head and body fill the centre. The drawer is a sliver at the left edge behind his arm, and the yank happens behind him. At g1411 the open double-height drawer reads clearly, but only after he leaves. |
| Finger -> one box | **Partly** | There is no finger image (not rendered). The lit box inside the big drawer (g1420-1460) is a clear, warm, single object, and the dim card rows beside it suggest "the rest". You never see many boxes become one. |
| Ear -> one card | **Mostly yes** | There is no ear image (not rendered). But the card rising out of the box into the light (g1481-1516) is the best image in the take: sharp, readable portraits, hand, fingerprint and table. "One card" lands. |

Overall: the drawer -> box -> card zoom-down does read as "narrowing to one" at phone size, because each step is a smaller lit object inside the previous one. **The measuring half of the mechanism is not visible at all.** None of the three body parts is shown being measured, including the head, which the team believes is covered. A blind viewer will get "they searched the files and found his card", not "the body measurements pick the drawer". The measurements are what make this a system rather than a search, so this matters.

## Blur (client hates blur)
- **Whip g1370-1378 is too long.** Nine consecutive frames are fully smeared: g1371, 1373, 1375 and 1377 are unreadable mush, and g1378 is still heavily streaked with a ghosted Bertillon. That is 0.3 s of blur, three times the 1-3 frame allowance. The location change does not need that many smeared frames to hide.
- Snap g1406-1415: g1408 and g1411 are sharp. The streak frames are short and within the allowance.
- Snap g1461-1467: the frames are sharp.
- Card_hero g1470-1516: the frames are sharp at full res (g1481, g1511 checked). The low Laplacian score comes from the flat wall and wood, not from blur. No action needed.

## Scores (1-10)
| Area | Score | Notes |
|---|---|---|
| Mechanism clarity (phone) | **4** | Narrowing 7, measuring 1. Head, finger and ear are never visibly measured. |
| Beauty / key image | 7 | Card rising into the lamplight (g1481-1516) and the lit box in the dark drawer (g1436) are lovely. The whip mush pulls it down. |
| Acting | 5 | Dupont's smug-worried face and Bertillon's frown in 24 are good. In 24 the calipers are not on the head. In 25 Bertillon "yanks" by standing with an arm out while facing the camera, so the effort does not read. |
| Set density | 8 | Clock, shelves, measuring furniture; a towering card-drawer wall with lamps and a desk. Rich and in character. |
| Light / colour | 8 | Warm practicals against blue-violet shadow, and a warm pool on the box and card. No blown bloom on the card. |
| Camera | 6 | Moves and snaps follow the plan and the rhythm passes, but the whip blur is 9 frames, and the drawer shot frames Bertillon instead of the drawer. |

## Verdict: FIX-FIRST
The narrowing images and the lighting are shippable. The take fails on the film's central idea (measurement) and on the client's hard rule against blur. Three fixes, cheapest first:

1. **Trim the whip blur to 3 frames (post only, no render).**
   - Keep the motion streak only on g1373-1375.
   - For g1370-1372, hold or ease the last sharp measure-room frames (camera accelerating, kernel at most 1/3).
   - For g1376-1378, use sharp drawer-room frames (or kernel at most 1/3).
   - Re-run qa_auto: the blur list must drop to 3 whip frames plus at most 2 frames for each snap.
2. **Put the calipers ON the head in shot 24 (re-render g1336-1373 only, same set and camera).**
   - Open the caliper arms so one tip touches Dupont's forehead and the other the back of his skull (front-to-back head length), at head height (y ~430-600 full-res at g1366), not chin height.
   - Bertillon's eyeline goes to the caliper scale.
   - Hold the tips in contact from g1350 to the whip. Add a 2-3 frame "tighten" nudge on "ระดับนี้" (about 45.5 s) as the measuring gesture.
   - This alone turns "search" into "measure -> drawer".
3. **Show the finger and ear beats with two 12-15-frame inserts from the existing measure_chair set (no new location).**
   - Finger: cut in at g1406, before the snap to drawer_box, ending on the box. Calipers close on Dupont's raised middle finger, framed close but with the chair and clock behind (no flat panel, no text).
   - Ear: cut in at g1459-1461, before the snap to card_hero. Calipers on his ear, head turned in profile.
   - Hard cut in and out on the words "นิ้ว" (~46.8 s) and "หู" (~48.6 s). Each is 0.4-0.5 s, so the box and card shots lose only their first beats, which are their least important frames.
   - Fallback if inserts are not possible: in drawer_box, light about 6 boxes at g1406, then turn off all but one by g1430. In card_hero, show a fan of cards that drop back as the single card rises. This makes "เหลือ (only one left)" visible. It still leaves finger and ear unshown, so treat it as the weaker option.

Non-blocking:
- Shot 24-25: drawer framing. Slide the camera or move Bertillon about 0.5 D to the right, so the yanked drawer sits at frame centre-left and is not covered by his head during g1386-1404. Turn his torso toward the drawer, with a lean-back pull pose.
- g1420-1460: the card with the bottle already stands visible in the box before the lid "opens", so the bottle is shown early. Keep the card below the box rim until g1466.
- Heads are clear of the caption band (Bertillon chin ~800 at g1404-1408). No mouths move. Thai text: none in the picture. Pass.
