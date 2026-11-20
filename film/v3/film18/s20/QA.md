# QA s20 (render team 5, film 18) round 2 - frames g1515-1595 (+6 handles: take.mkv g1509-1601, 93 frames), jimo_out NIGHT
Frame-diff in-shot (n=80): median **4.00**, p90 **7.35** (target 4 / 12: median met on the limit, p90 NOT met; no pulses).
qa_auto PASS.
- The camera now rides ALONGSIDE the herd at herd speed (11 D/s, lateral 7.5 -> 6.7 D, slow push), so the herd never recedes after g1585; a lead ox in clean profile at the left-centre of frame (about 35-45 % of frame height) with its flame trailing behind it; all 27 oxen run the same way (-y), none turns back. Short whip-in at the start (30 D look offset unwinding over 7 frames).
- 3 or more tail flames visible throughout (3-6 counted every 15 frames), each on a tail-tip anchor, leaning back, with sparks and a warm light; no flame card touches a head.
- Ground: the dark diagonal furrow bands are gone (POST of the set replaced by two torch stakes only); ground is plain lit earth, about 30 % of the frame; caption band is mid-dark earth with soft warm pools.

## Round 2 (TAKE-gate notes from the director, QA_TECH / QA_ART)
Shared fixes (c18.py): every flame is a painted card placed on the ox's tail-tip anchor (cast18 `tail_tip`), leaning backward against the run, size capped (~1 D), with 6 spark cards streaming behind and one warm point light per lit tail (nearest 5) plus a small ground pool. The cast's own flame drawing is no longer used (cards are rendered with the unlit reed bundle). Placeholder/low-poly junk hidden at runtime (rubble/dig heaps, rain streaks, jars/reeds near the lens). No zoom pulses: motion is the eased push + slide, tracking and actor motion, with at most one held punch-in.
