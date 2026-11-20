# QA-art round 14 s01: FIX-FIRST
Shot: BIGZOOM A, the hook (g 0-156, new key take). I extracted all 162 frames (g = n). I judged them on a 180x320 phone sheet every 5th frame (about 6 fps), at full size at g 0/30/60/72/90/108/130/155, frame by frame at g 54-89 (pop-in and plaque post), on a 2x crop of Tian Dan at g 108 and g 130, and with a per-frame 90x160 frame-diff. I compared it with the R4 and R5 reference sheets.

## Checks
1. **One continuous eased move: YES.** Frame-diff rises smoothly from 4 to 19 (g 0-36), holds 11-13 through the descent, peaks at 20 when the plaque post passes (g 78-80), then settles at 8-10 (g 82-108) and 3-6 in the slow push. There are no spikes, no cut and no pulse.
2. **Extreme wide to medium: YES.**
   - **g 0:** Tian Dan is about 25-30 px tall (about 2 %), beside the coated ox at x 370, y 625. He is small but findable on the full frame. On the phone he is about 12 px.
   - **g 108:** from the hat top to the feet he measures about 41 % (y 430-955). That is in the 35-60 % band.
3. **Rich set at every stage: YES, the best set in the film.** The move passes over tiled roofs with lit windows, a pagoda, ox pens and fences, dozens of dragon-coated oxen, braziers on the wall walk, the gate-house roof, the 即墨 plaque, rows of oxen with horn blades and the wall with torches. It ends on a lit yard with houses behind. This matches the density of R4 and R5.
4. **Reads as the hook: YES.**
   - g 55-90: he tugs the red-and-gold coat over an ox.
   - g 100-155: he lifts the blade bundle to the horn, with the dressed herd behind him.
   - On the phone, "a man dressing oxen in dragon silk and tying blades to their horns" reads by about 2 s.
5. **即墨 plaque readable: YES.** Both characters are clear at about g 30-62 (about 1.1 s), largest at g 50-60. The first character leaves the frame at g 63.
6. **Rim light and warm/cool: PARTLY.**
   - **Warm/cool: YES.** Warm brazier and lantern pools sit against the moon-blue roofs and sky in every frame.
   - **Rim: NO.** The "rim" is a misregistered backing copy, not a rim (blocker 1).
7. **Pop-ins (team's admissions):**
   - **Basket carriers at g 60: ACCEPTED.** They do not pop in mid-frame. They rise in through the bottom edge as the crane comes down (g 64-70), which reads as a reveal. But see blocker 2 for where their faces sit.
   - **Plaque post at g 62-80: ACCEPTED as a foreground wipe, with a note.** It is a dark post 1-2 D from the lens that slides across the frame, which is good parallax. At g 79-80 it crosses the left carrier's face and body for about 2 frames.
8. **Heads above y 860: NO** (blocker 2).

## Blockers
- **Blocker 1: the rim backing copies render as dark ghost duplicates.**
  - On the 2x crop at g 108 and g 130, Tian Dan's backing copy sits about 50 px ABOVE his card. The result is a second complete cap stacked on his cap, with two hairpins (y about 400-520). The copy also shows as a dark extra leg beside his left leg (x about 250-290, y 780-960 at g 130).
  - The hero ox shows a second set of dark legs offset left (x about 480-620).
  - Only a thin pale line reads as rim, at the hat edge.
  - This is on the hero's face in the held medium, the hook's main frame (g 100-156). On the phone it reads as a tall double hat.
- **Blocker 2: carrier faces in the caption band.**
  - The left basket carrier's face rises through the bottom of the frame. Her face bottom, measured from face-colour pixels, is at 1253 (g 68), 1128 (g 72), 1037 (g 76), 949 (g 80), 901 (g 84) and 879 (g 86). It is ≤860 only from g 88.
  - That is 22 frames (about 0.7 s) of a face under the hook caption.

| Beat on phone | Light/colour | Composition | Acting | Camera |
|---|---|---|---|---|
| 8 | 8 | 7 | 7 | 9 |

## Verdict: FIX-FIRST (2 blockers, each measurable)
1. **Rim copies:**
   - Scale each backing copy (Tian Dan, hero ox, carriers) about its own card centre with an offset of ≤3 px, so the rim shows as an even 3-6 px edge on the moon side only.
   - Make it brighter than the card's edge, not darker (moon blue, about RGB 150,190,255). If that cannot be drawn, remove the copies and leave the warm key.
   - Pass check on rendered g 108, 130 and 155: one cap and one hairpin on Tian Dan, two legs on him and four on the ox, with no dark silhouette outside any card wider than 6 px.
2. **Carrier faces ≤860:**
   - Keep the carriers' heads out of frame until their face bottom is ≤860. You can start them about 0.5 D farther from the lens, bring them in from the left edge, or delay them to g 88.
   - Pass check: on every frame in g 60-156, any visible face has its bottom at ≤860.

## Notes (not blocking)
- **Plaque post:** Nudge it about 0.3 D right, or lower it, so it does not cross the carrier's face at g 79-80.
- **Brazier leg:** A bright white-yellow vertical bar (the leg of the left brazier, x about 130-165, y 590-800, g 105-156) glows like a light-saber next to the carrier's head. Lower its emission or darken it.
- **Edge-cut carriers:** In the medium (g 85-156) the carriers are cut by the frame edges: the left one is about 60 % visible and the right one is a sliver of face and basket. They are acceptable as foreground framing. A whole-or-nothing framing would be cleaner.
- **Start frame:** Plain dark ground outside the wall fills the bottom-right triangle at g 0-20 (about 20-25 %). A lit patch or a warm lamp near Tian Dan at g 0 would make him easier to find on the phone.
- **Keep:** the move, the set density, the plaque and the warm/cool grade are client-reference level.
