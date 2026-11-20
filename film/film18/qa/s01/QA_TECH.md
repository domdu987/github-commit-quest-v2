# QA-tech round 15 s01: FAIL
Checked: all 162 frames extracted; 6 fps sheet, every frame g60-90 and g100-155 (4-frame steps on the sheet, 1:1 crops at g72/76/78/82, g76/80/84 full width, g110 and g150 hero pair). Frame-diff re-measured (90x160 grey, in-shot g1-155): median 8.20, p90 12.96, min 2.27 (g153), max 18.6. This matches the director's 8.20 / 12.95 (the team's QA.md 7.93 / 12.42 is stale).

## Blockers
1. g72-g80, the plaque post and the left edge (rider on the foreground ox, plus the ox itself).
   - A small rider in a blue robe sits on the left foreground dragon-coated ox. At g75-77 the black plaque post (x ~30-80) covers her face, so the post still crosses a face. The round-14 fix only moved it off the carrier.
   - At g77-80 the same rider's face is half cut by the left frame edge (about 50 px of a 90 px head). The foreground ox is cut roughly in half by the left edge for g76-90.
   - This breaks "post crosses no face" and "no half-cut characters" (§G).
   - Fix: delete or move the rider so her face is clear of the post and fully in frame at g72-82, for example by moving the foreground ox about 1 D right or removing the rider. Or shift the post so it passes through no face. Also keep the foreground ox whole in frame, or have it exit the frame completely by g82.

## Round-14 blockers: verified gone
- Ghost duplicates: at 1:1 on g110 and g150 Tian Dan has one cap and one hairpin, two legs, and the ox has two front legs and a single set of hooves. No dark offset silhouette. The rim now only tints the hat edge faintly. OK.
- Basket carriers: gone from the foreground. The only people in g60-156 are the small rider(s), an old man with a basket and a woman farther back in the yard, with heads far above y 860. No face is below 860 at any frame. OK.

## Checks passed
- Zoom: one continuous move g0-108 (frame-diff rises 4 to 18.6, then 10-13), no cut, no pulse, no stall inside the move. Tian Dan is 2.3 % at g0 (< 5 %), about 41 % at g108 and about 42 % at g155 (35-60 % OK).
- Blades: he lifts and ties the blade bundle at the ox horn from g90 to g108 and holds it through g155 (cue 97 OK).
- Plaque 即墨: gold on dark red, legible g36-g66 (about 1 s). Readable on the phone sheet. OK.
- Heads above y 860: yes, in every frame (hero face bottom about 600).
- Pop-ins: none seen. The crane reveals the same pre-placed people and oxen.
- Contact shadows: a soft shadow is present under Tian Dan and under the near oxen at g76-84 and g110-150. The ox-foot shadow is faint but present.
- Ground at the end: sand mask 0.30 at g155 (0.29 at g130, 0.24 at g108). Team says 0.20; I measure 0.28-0.30, which is at the limit and not over it. Note.

## Notes (not blocking)
- Frame-diff falls from 10.0 (g107) to 3.2 (g108): the move ends with a hard speed step instead of an eased stop. Ease the last 8-10 frames of the crane so the stop is not a visible snap. The slow push g108-155 then runs at 2.3-4.9, which is a bit static but acceptable.
- Ground fraction is on the 30 % line; a dark prop or fence low in the frame at g130-155 would give margin.
- The brazier leg (x ~30-45 at g110-155) still glows as a white vertical bar, like a light-saber. Lower its emission.
- g0-20: Tian Dan is about 25 px tall and findable only by the brazier. Marginal but acceptable.
- Hero face: his eyes look at the lens. Rule 7 is a note only.
- QA.md measured figures (frame-diff, ground 0.20) are out of date. Refresh them for the next round.
