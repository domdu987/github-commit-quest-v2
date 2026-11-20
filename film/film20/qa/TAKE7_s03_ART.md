# TAKE7 QA-art: T03 = s03, BIGZOOM 1 + crane (g 170-411), round 5

**Verdict: PASS with notes.** All four round-4 blockers are fixed or reduced to minor items. The take now works as a hook, a find, a landing and a payoff. Two small leftovers are listed below. They do not block conform. If anyone re-renders part of the take, fix them in a partial re-render (g 190-215 and g 362-385, about 50 frames).

## Inputs
- All 242 frames.
  - Contact sheets every 4-6 frames.
  - Full-size frames at g 172, 190, 206, 296, 324, 374, 392 and 411.
  - 2x crops of g 198, 206, 372 and 380.
  - Phone sheet at 360x640.
- Joins: s02 g 185 into s03 g 170, and s03 g 411 into s06 g 396.
- Team stats: saturation 0.556 and luma 98.4, so §G-1 passes.

## Scores (1-10)
| Opening wide | Eiffel find | Landing | Crane to workers | Light/colour | Set richness | Defects | Overall |
|---|---|---|---|---|---|---|---|
| 8 | 7 | 8 | 6 | 8 | 8 | 7 | 7.5 |

## Round-4 items
1. **White dome with floating dots, bottom-left (g 188-210): reduced, still visible.**
   - The black dots are gone, and nothing floats any more.
   - The pale lavender-white low-poly disc is still there, with a small tool lying on it.
     - It is about 180 px wide at g 206 (from g 196 to g 212).
     - It is the brightest shape in the empty bottom-left of the frame.
     - On the phone it reads as a white sheet or umbrella, not as gravel.
   - The QA.md note calls it a gravel patch at about 3 %. The area is right, but the colour is not gravel.
   - **Fix (cheap, optional):** tint pn_gravelp to sand-grey (the ground colour, about 20 % darker) or hide it.
2. **Black deck underside and floating white bulb (g 346-411): fixed.**
   - The deck underside is now warm brown wood with up-light, and it reads as a plank platform, not a black slab.
     - The dark share is still high: luma below 60 covers 54 % of g 378 (deck, shadowed lattice and worker coats together).
     - It works because the warm lattice and the deep blue sky carry the frame.
   - The "bulb" now reads as a small smoke column (stacked translucent puffs) above the top rail, g 366-382.
     - That is acceptable as forge smoke, but it has no visible source.
     - **Optional:** add a small forge or brazier under it, or drop it.
3. **Bare white flag pole (g 186-240): fixed (removed).**
   - Only the thin wooden tent pole through the canopy roof remains (g 206-300). It is wood-toned and harmless.
4. **Wheelbarrow scribble and dark scatter: fixed.**
   - The wheelbarrow is gone, and the ground in front of Eiffel is clean (g 250-310).
   - The opening yard (g 170-182) still has small scatter between the huts. At phone size it reads as yard life (timber, carts, horses), not as black debris. Acceptable.

## Whole take as a viewer
- **Opening (g 170-182): reads well.**
  - The sky and clouds, the Trocadéro with its dome and towers, the Paris blocks, the blue Seine with bridges, the two orange legs on their piers with cranes, and the yard with long blue shadows are all in frame.
  - The longer hold helps: the place registers before the drop.
  - The far bank is still a flat grey-lavender plane (non-blocking, carried over).
- **Eiffel marker (g 170-198): works as a finder, but slightly odd.**
  - It is a white glowing ball on a pale-yellow vertical shaft. At 360x640 the eye goes straight to it, so it does its job.
  - It looks like a map pin or lollipop rather than a light from the world. By g 194-198 it is a large white ball on a stick beside the tent, close enough to look like a strange prop.
  - **Note:** warm it (yellow-orange, not white) and give it a dark post to the ground so it reads as a work lamp, or fade it out by about g 190. It is not blocking.
- **Descent (g 182-234):**
  - One continuous move that passes the crane, the leg diagonal, the pier, the huts, barrels, the drafting table and the tent.
  - Eiffel is findable from about g 194: a small figure with a raised arm near the tent.
- **Landing (g 258-312): strong.**
  - A low hero angle under the lattice. Eiffel stands full-body, grounded with a contact shadow, smiling, with one arm up. He is about 40 % of the frame height at g 296, which is inside §H's 35-60 %.
  - His hat and hand overlap the beam behind him, but nothing crosses his face.
- **Crane-up (g 318-365): still the weakest stretch (carried-over note).**
  - The camera passes the wooden scaffold, then tilts into the Trocadéro tower and almost empty blue sky with crane hooks (g 355-365) before it finds the deck.
  - It reads as a drift, not as "up the leg". Acceptable inside one continuous move.
  - **Note:** at g 324 the timber bar with a ghostly smoke puff in the foreground, bottom-left, reads oddly.
- **Payoff (g 380-411): reads as riveters high on the iron against a deep blue sky.**
  - Hot rivets glow, and the warm/cool contrast is good.
  - The riveter cards still stack in pairs: two heads overlap at upper right, and a red bandana head pokes out behind the near worker at g 405-411. No face is clipped.
  - Spreading the cards would be nicer. Non-blocking.
- **Joins:** the warm s02 balcony into the s03 wide, and the s03 deep blue into the warm s06 café, are both clean.

## If re-rendering anything (optional, partial)
- g 190-215: tint or hide pn_gravelp. Warm the marker or put it on a post.
- g 362-385: add a smoke source, or hide the puff.
