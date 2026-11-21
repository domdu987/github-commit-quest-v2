# QA sD1 (g542-642, CUT in, whip right out), re-render of team 7's first version
Fixes per director note:
1. KING'S TREASURY sign: camera starts due south of the chest at table-top height and pushes in with the board kept centred; both lines fully readable g542-~580, then the camera glides over the table front toward him (the board crops at about g584 as it leaves).
2. Counting visible: camera at table height, the counting hand is raised so the pinched coin shows (kept until the look-up at g602); stacks and loose coins on the table recoloured GOLD (silver material swapped to the set's gold at runtime).
3. Composition: table slab share reduced to about 25-30 % of the frame, no underside after g584. Head about 20-25 % of frame height while counting, bigger at the laugh push-in (about 280 px).
4. Look-up beat g602-612 (head and eyes up toward the river, 7-frame ease), then the laugh drawing with bounce at g612 (narration 20.29), no lip-sync (no speak call).
5. Lantern, arc and whip kept. Whip-right in g637-642 (6 frames, horizontal motion blur).
Set: film21/main set3d21 + cast21 as of e07ceb1 (crimson/gold canopy). K.with_rim on Cressingham. 32 samples OIDN, no post-gamma (colour normalised at conform per director).
Fix v3 (director gate item): g562-582 head cut by the right edge. The aim now eases ~0.34 m toward him from g548 and the glide to him starts 10 frames earlier (g564, ends g598 as before); only g548-600 re-rendered, other frames kept. His head is fully inside the frame throughout. The sign is read g542-~565 and then leaves frame left as the camera glides (crop at g570-590 remains, a transition).
Fix v4 (director gate item, g622-636): the laugh drift is halved (0.45->0.25) and the aim eases onto his head (x -13.05) from g604, so his head stays inside the frame until the whip. Whole take is on set bb7aa85 (g542-559 and g593-603 kept from the earlier bb7aa85 render with the g548-600 framing fix; g560-592 and g604-642 re-rendered), one consistent set.
GROUND (QA §K, gc_d1.py, frames every 10): PASS, 0 fail, 0 sunk (GROUND.md). Cressingham's card uses foot_offset -0.31 m (transparent padding under the soles, measured as the SUNK gap); canopy roof excluded as overhead on poles. During the laugh bounce (g612+) the card is listed airborne by design. Table, chest and stool are batched set meshes that pass. Contact shadow: contact=True on the actor.
qa_jitter: overall median jitter 1.28 px, one 7.5 px shake reading in second 2 (the planned glide/laugh push; no shake added).
Numbers (info only): qa_stats2 sat 0.591, vivid 59.7 %, luma 116.2 (above 110, left to conform); rhythm in-shot median 15.82, p90 27.41 (needs 4/12); still 0 %.
qa_auto: one FAIL, suspected blur on g637-642 = the planned whip pan.
Not covered: mouth is closed all segment (no speech in this window); the sign is partly cropped at g584 as the camera leaves it.
