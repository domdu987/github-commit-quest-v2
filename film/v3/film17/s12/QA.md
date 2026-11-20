# s12 QA, round 2 (shots 29-30, g 1695..1868, first_g 1689, 186 frames, 720x1280, 12 samples + OIDN)

take.mkv is stored as take.mkv.partaa/ab (`cat take.mkv.part* > take.mkv`).

## Numbers
- qa_auto: PASS (`QA_AUTO.md`), magenta 0.0 %. Its note "no visible change at g 1789" is a metric quirk: the hard cut 29 -> 30 at g 1789 is plainly visible.
- rhythm (`film17/rhythm.py --first_g 1689 --cuts 1789`): in-shot median **5.70**, p90 **12.95**.

## Round-2 fixes (QA-tech FAIL list)
- 4/5/6 cards: 14 drawers along both aisle walls open one after another (every 5 frames, far to near); each pops 3 true-size mugshot cards (0.17 x 0.114 m, the same hero-card texture as shot 29) out of the drawer. No giant floating cards, no pile: the aisle and the people stay visible to g 1874.
- 3 gendarmes lead thieves: three escort pairs (gendarme's arm out toward the thief, march-cycle legs) enter staggered at g 1789 / 1801 / 1813 from the far end toward the camera and stop at y 3.3 / 4.7 / 6.8; Bertillon (left) points, arm pulsing. Pairs are 100-260 px tall. Thieves have closed, worried faces (no shouting).
- 9 camera: crane pull-out eased at the head (diff after the cut 2.5-5, no jerk); extra snaps at g 1800/1812/1822/1850/1862.
- 1 shot 29: the foreground crates/stool are hidden, nothing crosses the lower third.
- 2 shot 29: card is 2.1x, frontal and mirrored into the screen-left hand (about 130 px wide, portraits and bottle readable); dupont stands right of Bertillon, uncropped, face free. The beard dissolve (g 1722-1756) is kept.
- 7 no mouth moves anywhere.

## Self-check (full-res frames g1720, 1760, 1800, 1830, 1860 viewed, plus the whole take at 3-frame steps on a contact sheet)
- g1720: card + both faces clear, grey false beard still on dupont. g1760: beard gone, card unchanged. g1800: first pair entering mid-ground, Bertillon pointing, drawers open. g1830/1860: two to three pairs, cards visible on drawer rims, floor visible.
- Heads above y 880 everywhere; no black/magenta frames. Cut g 1786-1792 inspected earlier: clean hard cut. Shot 30 far figures at the back of the aisle are small (about 60 px) by design; the escort pairs are the subject.
- Note: cut is at plan boundary g 1789 (round(59.62*30)); narration lands about 3 frames later, within tolerance.
