# QA-art, film 17 take s01 (HOOK, shots 1-3), ROUND 2: FIX-FIRST (shot 1 only)

Reviewer: QA-art (opus). The client delegated approval to QA, so this verdict decides the take.
Material reviewed: phone_sheet.jpg, full/g15 g40 g70 g105 g135, and f6 frames g0, g25, g45, g60, g110, g125, g140, g145 (downscaled to 360 px for the phone check).
Numbers: rhythm 6.22 / 14.31 (target >= 4 / >= 12). qa_auto: PASS.

## Round-1 fixes, checked
| R1 item | Status | Evidence |
|---|---|---|
| Shot 1: calipers ON the near ear, jaws closing | **NOT MET** | g15/g40: the calipers are a diagonal grey bar from Bertillon's hip (x~140, y~880) up to the underside of prisoner_a's near ear (x~270, y~720). The jaws sit behind the ear and head, so no tips are visible. The bar sits on Bertillon's dark coat and reads as "a rod held across his chest". |
| Shot 1: headrest no longer stabs forehead | MET | g0-g45: clean head silhouette. |
| Shot 1: see-through coat skirt | MET | Solid in g15/g40. |
| Shot 2: queue, gendarme, closer on Bertillon, ledger stool, dust | MET (mostly) | g60 shows the bench queue and the gendarme. The snap-in at g60-73 gives the Bertillon + sitter framing. The gendarme stands mid-room, not at a door: accepted, because nobody reads "door" at 2 s. Minor: at g70 the caliper bar crosses the sitter's forehead. That is acceptable at this size, but don't copy it. |
| Shot 3: near-profile ear insert | MET | g105/g110 is the best frame in the take. The ear sits big at centre, the beam is horizontal, the jaws visibly bracket the ear, the stiff sideways eye plays, and the hand is in. The front/back straddle is fine: at phone size it reads as "measuring the ear". |
| Shot 3: same framing on the next ear after the snap | PARTIAL | g135-145: the prisoner_c ear framing is good, but the calipers are gone. The "ทีละหู" (ear by ear) beat lands on a bare ear. |

## Scores (1-10, R1 in brackets)
| Area | Score | Notes |
|---|---|---|
| Hook clarity | **5** (3) | Shot 3 now reads clearly. Shot 1 still does not, and the timing makes that worse (see below). |
| Set density | 8 (7) | Queue, gendarme, lamp, clock and shelves are all there. |
| Light / colour | 7 (7) | Unchanged. Shot 3 is warmer than in R1. |
| Composition | 6 (4) | Shots 2 and 3 are fixed. Shot 1 has its best element (the calipers) hidden behind the sitter's head. |
| Acting | 6 (4) | The sitter's deadpan works. Bertillon in shot 1 is still static, with no visible reach-and-close. |
| Camera energy vs film 2 | 8 (7) | The snap in shot 2 and the whip in shot 3 are both good. |

## Can shot 3 carry the hook alone?
No, and the reason is timing:
- The words that carry the image, "เอาคีมเหล็ก ไปวัดหูโจร" ("takes steel calipers, measures a thief's ear"), are spoken at 0.72-2.49 s narration time. That is all inside shot 1 plus the start of the shot-2 wide.
- Shot 3 (3.2-4.8 s film time) plays under "ถูกจับมา ทีละคน ทีละหู" ("brought in, one by one, ear by ear").
- So the picture that explains the line shows up about 2 s after the line. That is also past the 1-2 s window in which a phone viewer decides whether to keep watching.
- The first frames are the thumb-stop. At 360 px, g0-g45 read as "a stern man with a stick behind a bored man". That is pleasant, but it is not the strange act.

Everything else in the take is ship-quality, so this is a narrow, shot-1-only re-render (48 frames).

## Verdict: FIX-FIRST
### Fixes (max 2)
1. **Shot 1 (g0-47): reuse the shot-3 caliper rig and stop relying on the hand IK.**
   - Pin the calipers to prisoner_a's near (camera-left) ear, exactly as shot 3 does. Run the beam roughly horizontal at ear height, in front of Bertillon's chest, and take the hand to the beam end. The hand follows the tool. Do not solve the tool to the hand; that path carries the ~0.4 D error.
   - Both jaw tips must be visible in front of the ear and must not disappear behind the head. Swing the camera about 15-25° toward camera-left so the ear and jaws are silhouetted against the light wall, not against the dark coat.
   - Frame about 1.3x tighter than the current g40 so the ear is at least ~70 px wide at 720 px by g20.
   - Keep the sliding jaw closing over g14-40 and keep the planned push and slide.
   - Phone test: at 360 px, a frame between g10 and g20 must read as "calipers on ear" with no narration.
2. **Shot 3 (g127-145), cheap: keep the calipers on prisoner_c's ear after the whip.**
   - Re-anchor the same rig to prisoner_c's ear at the swap frame, so "ทีละหู" lands on a second measured ear.
   - This is recommended, but it does not block shipping. If the render budget is tight, ship with only fix 1 done.

To re-check: send the phone sheet plus full-res g10, g20 and g40 of shot 1 (and g140 if fix 2 is done). If those frames read as calipers on the ear at 360 px, the take ships without another full review.
