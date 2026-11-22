# QA-art (strict): film 18 style board (Jimo, 279 BC, fire oxen)

Reviewer: QA-art (opus). Looked at board_1-3 at full size (720x1280) next to set3d10 and set3d9 contact sheets (used for level of finish only).
Checked against bible colour-light.md (1.1, 1.3, 1.5 night, 5.4) and sets.md 9.2. Own measurements are median colour of the named area (PIL), on top of NOTES.md / numbers.json.

## Measurements behind the scores

| item | board_1 | board_2 | board_3 | target |
|---|---|---|---|---|
| sky (y 100-300) | `#100085` H247 S1.00 V0.52 | `#0b007f` H245 S1.00 V0.50 | `#350b8b` H260 S0.92 (top) | night ref `#1e2e7b` -> `#1748ae` -> `#204c8f`, H 221-230, S 0.75-0.87 |
| top eighth luma | 17 | 15 | 64 | 40-90 |
| earth wall, lit | `#d58484` H0 S0.38 V0.84 (salmon) | far wall, small | `#e5967a` H16 V0.90 | ochre H 28-40, S 0.45-0.65, V <= 0.75 |
| earth wall, shade | (whole wall lit pink) | - | `#8d687c` H328 (magenta) | H 240-260, never magenta |
| flame core / body | - | `#ffff00` flat | `#ffff00` flat | only the core clips to `#fffeec`; body H 20-45 |
| luma p50 / p1 | 0.31 / 0.055 | 0.32 / 0.055 | 0.48 / 0.078 | night ref mid-luma 0.32; p1 0.08-0.12 |
| violet % / magenta % | 15.4 / 5.0 | 12.7 / 6.1 | 8.3 / 14.0 | violet 0-5 (night allows some), magenta <= 10 |
| caption band y 880-950 | bridge foot + 2 lit lanterns + water edge | fire-bowl base + flame root + cups | ox hooves + mallet head | no head, no text; keep it calm and mid-dark |

## Scores (1-10)

| still | density & ornament | light & colour | composition & phone | period | key moment | mean |
|---|---|---|---|---|---|---|
| board_1 jimo_wall_night | 6 | 4 | 6 | 5 | 5 | 5.2 |
| board_2 yan_camp_night | 7 | 5 | 6 | 6 | 5 | 5.8 |
| board_3 wall_holes_oxen | 4 | 3 | 4 | 4 | 3 | 3.6 |

### board_1, the wall at night
- Good: strong, readable silhouette (gate tower centre, moon right); square putlog holes and horizontal tamping courses are right for rammed earth; moat, bridge, wheel foreground in shade gives depth; sharp, no DOF, no text.
- Bad: the wall is a pale salmon-pink slab (`#d58484`, V 0.84) lit evenly from end to end, so it reads as pink brick, not ochre earth, and there is no blue moon-shade on it at all: the "warm fire against blue-violet shade" idea is missing on the biggest surface. Sky is a fully saturated `#100085` electric indigo, darker and more violet than the reference night; it looks like a screen-saver, not a period night. Clouds are pink-white streaks. The tower is a two-storey red-pillared hall with curled ridge horns and rows of round yellow paper lanterns: Ming/Qing festival vocabulary, not Warring States. Lamp flames on the parapet are flat yellow cones. The caption band holds the two brightest lanterns (`y ~ 900-940`), which will fight the caption.
- Versus set3d9/10: those walls have texture variety, stains, scaffolds, banners, people-scale props and warm/cool separation on the same wall; here the wall is one repeated texture.

### board_2, the Yan camp
- Good: the densest of the three (jars, cups, table, spear racks, shields/drums, tents, chariot wheel, banners, palisade, far lit city); fire pools on the ground are the nicest light in the board; strong one-point perspective to the city gate.
- Bad: same over-saturated indigo sky (top eighth luma 15). Fires are flat `#ffff00` cones with no colour gradient; the near fire sits in a red disc that reads as a drum lid, not a fire pit. The near fire base and cups are in the caption band. The tents are cut off at both edges so the "camp" reads as a street. The story beat (Yan soldiers off guard, celebrating/asleep) cannot read without people; even stand-in cards are missing, so key-moment clarity is unproven.

### board_3, the oxen through the wall (the key image of the film)
- Bad, and the main reason for FIX-FIRST:
  - The ox is a placeholder: box body, four post legs, a red pillow for the silk with a row of multicoloured LED-like squares, white narwhal-cone "horns". It does not read as an ox, the silk does not read as red silk painted with dragons (the brief: 绛缯衣, 画以五彩龙文), and the blades do not read as bronze blades lashed to horns.
  - The tail fire is two flat yellow cones standing beside the ox on what looks like a separate bundle; it does not read as a burning reed tail attached to the ox. Next to it, the rolled mats read as a second unrelated prop.
  - The "holes in the wall" are red-lintel, cream-capped timber frames: they read as Japanese torii / shrine gates, not breaches dug through rammed earth.
  - The whole frame is too bright for night (p50 0.48, mid-band 145) and the earth wall is pink in light and magenta in shade (H328); magenta 14 %. There is no blue night anywhere except a strip of sky.
  - Sparse: about 8 objects; a mallet lies across the lower centre and into the caption band; ox hooves in the band.
  - Camera: ox seen side-on, half hidden by the mallet and shields, walking out of frame left. For a hook/reveal it needs to come at the camera.

## Fixes, in order of impact on the lowest scores (board_3 light/key-moment, then board_1 light/period)

1. **Earth wall: ochre, and shaded blue (all three boards).** Change the rammed-earth albedo from the pink to ochre-loess, about `#b8874e` (H 32, S 0.58), tamping courses 0.10-0.15 D tall in a darker `#8e6438`, plus irregular wash stains and a few erosion runnels. Give the wall a `shade_mul` that keeps its shade at H 240-255 (bible rule 3; currently H 328). Displayed targets: fire-lit wall `#c07a3c`-`#a86a38` (V 0.65-0.75, never above 0.80), moon-lit `#6a6488`-`#57608f`, unlit `#3b3a5e`. On board_1 the wall must be blue moon-shade overall with only warm pools 1-1.5 D around each torch/lamp (pool falloff, not a flat wash); goal on the wall: >= 55 % of its area at H 230-255.
2. **Sky: back to the reference night (board_1, 2, 3).** Gradient top `#1e2e7b` -> 60 % `#1748ae` -> horizon `#204c8f` (bible 5.4, `lightkit_clp` NIGHT), S <= 0.85, H 220-232. Top-eighth luma 40-60 (now 15-17). Cloud streaks lit cool `#8fa0d8` with a faint warm underside only near the city glow, not pink-white. Moon halo blue `#5a8af5` to 84 px (bloom size 0.20, strength 1.0). Target violet share <= 6 %.
3. **Real flames (every fire, torch and tail).** Replace the flat yellow cones with 3-5 overlapping tongue meshes (or one displaced, noise-animated mesh) graded core `#fffeec` (the only clipped part, emission > 1.0) -> mid `#ffb238` -> edges `#e8561c` -> tips `#b8301a` with alpha, leaning with motion; add a warm halo 12-24 px beyond the core and a few embers (board 2 embers are good, keep). No pixel of flame body at `#ffff00`; flame body hue 20-45. Light colour of the matching point lights (1.0, 0.50, 0.18).
4. **Board_3 brightness and colour.** Drop overall exposure so p50 luma <= 0.34 and mid-band luma 100-120 (now 145); bring back blue night: moon key on the wall top and ground away from the fire, fire light only within about 2 D of the tail. Targets: red+orange 45-55 %, blue+violet >= 30 %, magenta <= 8 %, p1 0.08-0.10. Push the sky band to the board_1 values.
5. **Hero ox (board_3, also needed for every later fire-ox shot).** Build a proper stylised ox: deep chest, hump, dewlap, short legs with hooves, head low with ears; silk blanket as a draped cloth mesh over the back and flanks, crimson `#a8142a`-`#c42a2a` with painted five-colour dragon scrolls (gold `#e0b04a`, green-teal `#3e8f7a`, white `#f0e6d0` accents) in 2-3 large readable motifs, not the LED square row; blades = flat bronze dagger blades (`#8a6a3a`, edge highlight) lashed to the horn bases with cord, about 0.5 D long, pointing forward; tail = a thick reed bundle tied to the tail and soaked in fat, flame streaming back from it (fix 3). Silhouette test: at 360x640 the ox must read as an ox with fire at its back in < 1 s.
6. **Board_3 restage the key image.** Turn it into the money shot: low camera (0.9-1.2 D, +14-20 deg) in front of a breach in the wall, 2-3 oxen bursting through toward camera at a 30-45 deg angle, the lead ox filling 35-45 % of frame height, horn blades catching fire light, tail flames behind lighting the breach and the next ox. Holes = ragged breaches in rammed earth with packed-earth rubble, broken courses and rough timber props (unpainted, no red lintels / cream caps). Add density to 12-18 objects: rubble, dropped baskets of earth, spades, a fallen ladder, drums of Qi soldiers behind, more oxen and torches through the other breaches. Remove the mallet across the frame.
7. **Caption band y 880-950 (all boards).** Keep it calm, mid-dark (luma 60-110) and free of bright emitters and small busy props. Board_1: move the bridge lanterns up the bridge to y <= 840 or out of frame, or raise the camera so the bridge foot sits below 960; water edge may pass under the band if dark. Board_2: lift the near fire pit so its flame root is at y <= 850 (or move it to y >= 980 with the flame fully below), clear the cups. Board_3: hooves at y <= 860 or >= 960; no mallet.
8. **Period dress for the city (board_1, also the far city in 2).** Warring States Qi: single-storey or two-stage gate hall on the rammed-earth wall with a plain hipped/gabled grey tile roof, near-straight eaves, half-round eaves tiles (wadang) along the edge, no curled ridge horns; timber posts dark lacquer red/black with simple brackets, not a Ming festival hall. Replace round yellow paper lanterns with bronze standing oil lamps and torches in iron/bronze braziers on the parapet; add Qi banners (plain dyed, no text) and crenels with wooden shields. Wall faces slightly battered (inward-sloping) as rammed earth is, with a wooden walkway and ramp. Keep the moat and the plank bridge; make the gate leaves heavy plank with bronze studs (already close).
9. **Board_2 legibility of the camp beat.** Widen 10-15 % or step back so at least one whole tent is framed each side; put the stand-in Yan soldiers in (asleep / drinking around the near fire) so the beat reads on the phone sheet; make the near fire a ground pit ringed with stones, no red disc. Keep the existing table, jars, racks, drums; add a sleeping soldier silhouette and a dropped spear in the foreground shade (within the nearest 15 %).
10. **Board_1 ornament.** Break up the single wall texture: stains, darker rain streaks under the parapet, repaired patches, a few hanging ropes/ladders, banners on the parapet, guards (stand-in cards) on the wall walk, a few far roofs of the city behind the tower with lit windows. Target Canny edge density >= 0.05 on the wall area and no featureless 40 px block share above 0.30.

## Verdict: FIX-FIRST

Board_2 is close to buildable; board_1 needs the wall/sky/period fixes; board_3, the film's key image, does not yet show a fire ox at all (placeholder ox, flat cone fire, torii-like holes, pink wall, too bright). Do not build the full set until fixes 1-6 are in and the three stills are re-rendered and re-measured (sky and wall hex, p50, magenta, caption band) against the targets above. Fixes 7-10 can land in the same pass.
