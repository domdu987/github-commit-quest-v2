# QA s18 (render team 5, film 18) round 2 - frames g1388-1426 (+6 handles: take.mkv g1382-1432, 51 frames), jimo_in NIGHT
Frame-diff in-shot (90x160 grey, area downscale, n=38): median **4.33**, p90 **7.22** (target 4 / 12: median met, p90 NOT met; no pulses were used, and the wide static framing carries little motion). qa_auto PASS.
- Ripple: 6 oxen, one tail lit every 3 frames from g1417 (nearest to the camera first), all six in frame in a lateral row (x -37..-14 spaced 4.6 D) so no tail is hidden; no tail lit before g1417 (checked every frame).
- Tian Dan stays in frame (placed at (-21.5, 13.2), torch unlit until g1413 then lit), push 0.17/s + slide, one held 10 % punch on "จุดไฟ".
- Pink V decals and navy lumps: rain streaks, rubble and dig heaps hidden; foreground dressing removed. Ground bottom is dark with the warm pools only under the lit tails; flame lights limited (420 W x scale).
- Not fixed: ground is still about 40 % of the frame (a lower camera was needed to keep six tails in view); the old navy-outlined basket at the left edge in the first frames.

## Round 2 (TAKE-gate notes from the director, QA_TECH / QA_ART)
Shared fixes (c18.py): every flame is a painted card placed on the ox's tail-tip anchor (cast18 `tail_tip`), leaning backward against the run, size capped (~1 D), with 6 spark cards streaming behind and one warm point light per lit tail (nearest 5) plus a small ground pool. The cast's own flame drawing is no longer used (cards are rendered with the unlit reed bundle). Placeholder/low-poly junk hidden at runtime (rubble/dig heaps, rain streaks, jars/reeds near the lens). No zoom pulses: motion is the eased push + slide, tracking and actor motion, with at most one held punch-in.
