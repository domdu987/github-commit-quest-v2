# QA-tech, film 21 take A1 (BIGZOOM 1, first half, HOOK): g0-80 + handles g81-83

**Verdict: FAIL** (plan coverage of the hook: the Scots are not findable and the two-by-two knights do not read on a phone. Otherwise the take is technically clean.)

Inputs: take.mkv (720x1280, 30 fps, 84 frames g0-83), meta.json, QA.md, QA_AUTO.md, contact.jpg, phone_sheet.jpg, shot.py; shot_plan.md v3 segment A + P_A; RENDER_TEAMS.md; QA_TEAM.md checklist + Stricter QA B/C + §G/§H/§I.
Frames: all 84 frames extracted (a superset of 6 fps + every handle frame) to scratchpad gate/sA1/frames/all_NNN.png (NNN = g+1). Viewed at full size: g0, g40, g80; 3x crops of bridge (g0, g80), hill crest (g0, g60, g80).

## Measured here (numpy, every frame)
- Sharpness (Laplacian var): 620-755; min/median = 0.94. **No blur frame**; no DOF anywhere. The bottom-band variance drops from 261 to 164 as the smooth hill face fills the bottom; that is content, not defocus.
- Frame diff g->g+1: 5.7 at g1 rising smoothly to 13.4 at g64, easing to 12.15 at g80, then 12.2 / 12.5 / 12.8 at g81-83. **No pops, no frozen run, no black/blank/magenta frames.** Move is monotone and continuous.
- Saturation (max-min)/max: 0.83 at g0 falling to 0.73 at g83 (mean ~0.78; take report 0.773). Luma 99-102. §G (>= 0.47, luma 85-110) and §I 3 (>= 0.50, vivid >= 45 %) met numerically.
- End pose: `keys()` in shot.py puts the key `(80,) + K.POSES["P_A"]` exactly at g80, and meta.json `cam_out` states P_A (290,205,170)->(120,110,10) 22 mm at g80. **P_A match: OK by construction.** Handles g81-83 continue toward the hill_over key (g159): same move, correct for D6.

## Issues
1. **g0-83, plan coverage (hook), BLOCKING.** The Scots on Abbey Craig are not visible in any frame. 3x crops of the crest/slope at g0, g60 and g80 show only pines, red rock dots and pale rock; no blue line, no saltire banner. §H 1 requires the character "tiny (under 5 %) but **findable**"; the narration opens on "ทหารพวกนี้" (these soldiers) with no soldiers on screen. Fix: place the Scots line + 2-3 saltire banners (oversized is fine at this distance) on the open shelf on the camera side of the crest, clear of the pine canopy, so they read as a blue-and-white line on the 360x640 phone sheet from g0.
2. **g0-50, plan coverage (hook), BLOCKING.** The bridge column ("knights crossing two by two") is about 6 riders, each ~2-3 px wide at g0 and ~4 px at g80; on phone_sheet.jpg the bridge is a brown hairline and the riders are not visible at all. The "two by two" idea does not read before g60 even at full size. Fix: fill the deck end-to-end with pairs and continue the column onto both causeways; give them high-contrast crimson/white caparisons and a gold pennon per pair so the column reads as a red double-dotted line crossing the teal river.
3. **g0-83, artefact (non-blocking but visible at full size).** The "light shaft on the crag" renders as flat horizontal yellow slabs at the NW edge of the crest (full-frame approx. x 200-420, y 640-700 at g80; present from g0). It reads as a smear/glitch, not a sun shaft (no diagonal, no source direction). Fix: angle it from the sun direction as a soft volumetric cone, or drop it from A1.
4. **g75-83, join note (non-blocking).** Camera speed dips about 9 % into the P_A key (diff 13.3 at g70 -> 12.15 at g80) and re-accelerates in the handles (12.8 at g83). A2 (team 5) must start from P_A with the same velocity (match the handle frames g81-83, not a fresh ease-in) or the D6 will show a stall.
5. **g0-30, motion (non-blocking).** The first second is the slowest part of the take (diff 5.7-10.4 vs 13+ later): the ease-in still shows inside the hook. p90 8.15 is acceptable for an extreme-wide high swoop (parallax is low at 360 m), but moving the pre-roll key earlier (e.g. g-40) would put the cruise speed on screen from g0.
6. **Rim light (known film-wide limitation, not failed):** no character is large enough here for a rim to matter; noted only.

Not applicable in this take: heads vs y 880 (no cast cards), lip-sync (no quote), Thai text (none rendered), floating feet (riders too small to judge; horses on deck at g80 crop look seated on the planks), neighbouring take continuity (A1 is the film start; A2 not delivered yet).
