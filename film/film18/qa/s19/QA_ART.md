# QA-art — film 18 s19 (attack: oxen burst out of the wall, 47.56-50.51 s), TAKE gate
Reviewed: take.mkv at 6 fps (frames in art6/, phone sheet art_phone.jpg 360x640) plus key frames at full size 720x1280. Frame refs = global g (30 fps).

## What reads
- The burst (g 1430-1455) is good. Oxen come out of the breached holes with dust puffs along a lit wall, and it reads on the phone.
- From g ~1450 to 1500, oxen pass right through the lens. The frame fills with a single ox face or coat (g 1450-1500). One giant flat flame card floats in the sky, detached from any tail, with stair-step aliased edges (g ~1456 and ~1496). At g ~1500-1509 the frame holds the empty wall for about 0.3 s before the whip. The flames do not light anything.
- About the qa_auto blur flag (g 1510-1520): I agree it is the low-detail whip landing, not blur. It is not an art issue.

## Scores
| Item | Score |
|---|---|
| Beat clarity (phone) | 6 |
| Light / colour | 6 |
| Composition | 5 |
| Acting (herd) | 6 |
| Camera move | 6 |

## Verdict: FIX-FIRST (reveal)
## Changes
1. **g 1445-1500, near oxen:** Keep the nearest ox at least about 2.5 D from the lens and no more than 50 % of frame height, so the shot stays "a herd pouring out of the wall" rather than "one ox face".
2. **Flames, whole take:** Attach every flame card to its reed tail tip. Cap the card at about one third of the ox body length. Render it at a resolution high enough that the edges do not alias. Lean it backward against the run (streaming).
3. **g ~1498:** Start the whip while the last oxen and Qi runners are still in frame, so there are no empty-wall frames.
4. **Light:** Give each lit tail a small warm point light so the ground and the oxen's flanks pick up orange.
