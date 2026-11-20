# QA-art round 15 s01: PASS
Shot: BIGZOOM A, the hook (g 0-155, v3 take). I extracted all 162 frames (g = n) and judged them on a 180x320 phone sheet every 5th frame (about 6 fps). I also looked at every 8th frame in g 100-155 at 360x640, at full size at g 0/60/108/155, on 2x crops of Tian Dan at g 108 and g 140, frame by frame at g 70-80 (plaque post), and on a per-frame 90x160 frame-diff. I compared it with the R4 and R5 reference sheets. Working files: /tmp/claude-0/-home-user-github-commit-quest-v2/64d228e2-e8b3-5935-8909-70298ec15c3e/scratchpad/qa15_s01/

## Round-14 blockers
1. **Ghost duplicates: GONE.** On the 2x crops at g 108 and g 140, and on every 8th frame in g 100-155:
   - Tian Dan has one cap, one hairpin and two legs.
   - The hero ox has its own legs only, with no offset dark set.
   - No dark silhouette sits outside any card.
2. **Basket carriers: GONE.** No face enters through the bottom edge anywhere in g 60-156. The yard pair (a woman and an old man) stand far back, with their heads at about y 600-700. All heads are above y 860.

## Re-confirmed
- **One continuous eased move: YES.** Frame-diff (in-shot) has a median of 7.4, a p90 of 11.7 and a max of 17.4 at g 36. It rises smoothly from 3 to 17, holds 9-12 through the descent, and settles to 2-4 in the slow push. There is no jump, cut or pulse.
- **Extreme wide to medium: YES.**
  - g 0: Tian Dan is about 20-30 px tall (under 3 %) beside the lantern near the coated ox, x about 370, y about 630.
  - g 108: he spans hat top to feet at about y 430-955 (about 41 %), inside the 35-60 % band.
- **Rich set: YES.** The move passes roofs with lit windows, the pagoda, ox pens, about 70 dragon-coated oxen, braziers on the wall walk, the gate-house, the plaque, horn-blade rows and the wall torches. It ends on a lit yard with houses and a lit tower behind. This matches R4 and R5 density.
- **Hook by about 2 s: YES.** From g 55 he tugs a coat over an ox in a dressed herd. From g 100 he lifts the blade bundle to the horn. "A man dressing oxen in dragon silk and arming their horns" reads on the phone by about 2-2.5 s.
- **即墨 plaque: YES.** Both characters are clear from g 36 to about g 60 (about 0.8 s), largest at g 54-60.
- **Warm/cool: YES.** Brazier and lantern pools sit against the moon-blue sky, roofs and wall in every frame.
- **Plain ground in the medium: OK.** The ground below the lowest figure is 25 % at g 108, 24 % at g 130 and 21 % at g 155. The ground is lit and textured, with pebbles and straw.

## Rim on Tian Dan (team's admission): NOTE, not a blocker
The cool light shows on the wall, sky, background figures and ground edges. On Tian Dan and the hero ox themselves it is barely visible, so they read warm-key only. The reference puppets (R4 and R5) also read mainly by their ink outline against a glow behind them. Here, the bright sky-glow halo behind his head already separates him. If the team has time, add a 3-6 px moon-blue (about RGB 150,190,255) edge line on the moon side of his card and the hero ox's card, in texture or as a compositing pass. Do not add backing geometry again.

## Notes (not blocking)
- **Plaque post, g 75-76:** The post still crosses the left half of the blue-robed villager's face for about 2 frames. It is a fast foreground wipe, so this is acceptable. QA.md's claim that "no post crosses a face" is not quite true.
- **Brazier leg, g 100-155:** It is still a bright white "light-saber" bar at x about 130-165, y about 590-800, left of Tian Dan. Lower its emission.
- **Old man behind the hero ox, g 100-155:** His grey-green robe and two dark legs show through the gap under the ox's head and chest. On the phone this can read as extra legs under the ox. Move him about 0.5 D sideways so he is clear of the ox, or behind it.
- **g 86-96, mid-move:** The bare ground is about 35 % below the figures. It is transient during the descent, so this is acceptable.
- **Caption band at g 155:** The mean is 118 (lit ground), with no bright pixels. This is fine for white captions with an outline.

| Beat on phone | Light/colour | Composition | Acting | Camera |
|---|---|---|---|---|
| 8 | 8 | 8 | 7 | 9 |

## Verdict: PASS with notes
Both round-14 blockers are fixed. Everything I passed in round 14 still holds. The faint rim on Tian Dan is a note.
