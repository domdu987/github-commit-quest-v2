# Ref D: how the characters are built and lit, and a Kong recipe in that construction

Source: `ref/d/ref.mp4` (720x1280). Frame ids: `f_NNN` is from `frames/` (every 3 s, t=(n-1)*3), `f2_NNN` is from `frames2/` (every 0.5 s, t=(n-1)*0.5). All px values are in 720x1280 source pixels unless marked "2x crop".
Evidence crops are in `spec/refD_evidence/`: `contact_3s.png`, `cs_A_29-52.png`, `cs_B_53-76.png`, `cs_C_85-108.png`, `cs_D_109-132.png`, `head_officer_f2_042.png`, `head_capgeneral_f2_087.png`, `hat_soldier_f2_104.png`, `prone_3q_f2_098.png`, `fallen_f2_066.png`, `march_f2_062.png`, `walk_f2_100.png`, `cabin_f2_032.png`, `faces_turns.png`.
We copy the construction and finish only. We do not copy the reference's uniforms, hats, insignia, logo, text or WW2 subject.

## 1. Verdict: what kind of puppet this is

These are **real 3D volumes with a toon ink silhouette, rendered in a fully lit, physically shaded 3D world.** They are not cards. The flat look comes from three choices: heads that are almost unshaded, a uniform ink outline, and stick limbs. It does not come from flat geometry.

Proof from the frames:
- **Bodies are capsule volumes ("beans").** `f2_065`–`f2_068` (`fallen_f2_066.png`): soldiers fall over and their bodies show as horizontal cylinders with round end caps, foreshortened in depth, sliding through snow puffs. `f2_098` (`prone_3q_f2_098.png`): the prone bean is seen 3/4 from behind. The belt band wraps around the cylinder, and a patch decal follows the curve.
- **Heads are spheres with a face decal.** In `f2_066` the fallen heads lie at 90° and the outline is still a perfect circle, while the face decal rotates with the head. In `f2_098` and `f2_031` (left soldier) the head is at 3/4: the features slide toward the facing side and get foreshortened (eye spacing compresses), so the face is a decal on a curved surface, not a flat drawing. In `f2_057` the hood is a shell around the sphere and the face shows through its opening.
- **Hats and hair are separate 3D shells with painted textures** (`hat_soldier_f2_104.png`, `head_officer_f2_042.png`). Fur hats are scalloped volumes with hand-painted hatch strokes. Hair is **flat, jagged, cookie-cutter tufts** (the blonde officer, `f2_042`): thin plates peeking out under the hat at the sides, each inked, sticking out no more than about 0.12 D. There are no conical spikes.
- **Props are NOT inked** (rifles, scope, map, binoculars in `f2_032`, `f2_042`, `f2_085`). Only the characters (head, body, hat, hair, ear flaps, hood) carry the black silhouette line. Props are plain PBR models in the same world.

## 2. Measurements (D = head diameter in px of that frame)

| quantity | value | frames |
|---|---|---|
| head D (full figure, MS) | 150–166 px | f2_032 left soldier 150, f2_115 = f_020 166 |
| head D (close) | 225–234 px | f2_087 225, f2_042 234 |
| **head width / body width** | **0.83–0.92** (head is narrower than the bean) | f2_032 150/180 = 0.83, f2_115 166/190 = 0.87, f2_085 225/245 = 0.92 |
| body (bean) height | 1.40–1.48 D | f2_115 245/166, f2_085 315/225 |
| body depth | about 0.8 of its width (from the 3/4 views) | f2_098, f2_066 |
| leg length (hip to sole) | 1.0–1.2 D | f2_115 195/166 = 1.17, f2_087 ~220/225 = 1.0 |
| arm length | about 0.9–1.0 D | f2_032, f2_100 |
| total figure height (crown to sole, no hat) | 3.4–3.6 D | f2_115: y 575 to 1150 = 3.5 D |
| head–body join | the head sits directly on the bean top, overlapping about 0.05 D. No neck, no collar ring. | f2_032, f2_087 |
| limb thickness | 9–11 px when D = 166–225, so **0.045–0.06 D** (4.5% of body width) | runs at f2_100 y1000: 11, 11 px; f2_087 y1150: 10, 10 px |
| limb colour | near black, median L 24–26, p95 66 (edge antialias only), **no specular highlight** | f2_087 legs RGB (28,25,32) |
| hands | a small black ball cap, about 1.5x limb thickness (0.07–0.09 D). No fingers, except when gripping. | f2_032, f2_066 |
| feet | a dark rounded oval blob, about 0.20 x 0.12 D, slightly navy (≈ #1c1f2a) | f_020 (f2_115), f2_066, f2_032 |
| **ink outline** | **2.3–2.5% of D**: 5–6 px at D 234 (f2_042 y760: 5 px left, 12 px where it doubles with the hair edge), 3–4 px at D 166 (f2_115 head 335:4 px, 498:3 px) | f2_042, f2_115 |
| outline on body | the same world weight as on the head, or slightly thinner (3–5 px at MS) | f2_032 body runs 2–7 px |
| inner lines (seams, button lines, hat band, hood edge) | about half the silhouette weight: 1.5–3 px | f2_063, f2_098 |
| outline colour | warm near black (≈ #160f12), slightly soft (antialiased, video compressed) | f2_042 |

So the outline is a **world-space thickness** (it scales with the object), not a constant pixel width.

## 3. Shading

| surface | lit side | shadow side | drop | notes |
|---|---|---|---|---|
| **head** (white) | (250,236,220) warm | (206,196,216) lavender at the far edge | **8–18% in L** | f2_042 y760; f2_115 y640: 249 to 229; f2_087 y650: 251 (lit right) to 212 (left edge). Heads are nearly self-lit: a broad, very soft gradient, no visible terminator, a warm-to-cool hue shift. |
| contact shadow / AO under the hat brim or hood | (225,204,200) | | about 10% | f2_042 (the band under the fur hat), f2_104 (a lavender band under the hat). This is the 3D cue that sells the volume. |
| **body** (brown coat) | (180,117,45) | (120,81,42) at the rim, (51,36,25) at the ink | **30–40% in L** | f2_115 y800. A soft terminator about 40% of the body width wide. Bodies take the full scene light. |
| body (white coat, warm lamp) | (253,214,155) on the lamp side | (153,143,142) cool on the far side | about 40% | f2_032: the lamp warms the near side, the far side goes neutral grey-blue. |
| fabric texture | subtle painted noise and fold lines at about 10% contrast, buttons as decals, belt as a raised band | | | f2_063, f2_100 |
| specular | none on heads, limbs or cloth. Only props (rifle varnish, scope glass) get highlights. | | | f2_042 |
| rim | no hard rim. Backlight in snow scenes gives a soft bright edge just inside the ink on the bean. | | | f2_085, f2_100 |
| shadows cast | soft blue cast shadows on the ground (sun) and contact darkening at the feet | | | f2_061–f2_064, f_020 |

## 4. Faces and animation

- Face features are black, matte, flat-ink decals. Brows are a bar 0.16–0.2 D long and 0.035 D thick (f2_042, f2_104). Default eyes are **heavy-lidded half ovals**: a straight lid line on top and a black semi-oval below it, 0.08 x 0.05 D (f2_042, f2_104, f2_031). The mouth is a single arc line 0.12 D (f2_104), a wavy "nervous" squiggle (f2_085), or open D-shapes with a dark-red interior and a pink tongue (f2_042, f2_088). Shock eyes are white circles with a ring and a dot pupil (f2_087). The sweat drop is a separate light-blue teardrop with an ink outline beside the head (f2_085–f2_087). Blush is soft pink discs (f2_058, f_010).
- Features sit inside about ±40° of the face normal. At 3/4 the decal slides with the sphere (f2_098, f2_031). No profile drawing is swapped in: the head simply rotates.
- Expression changes are decal swaps on held poses, about 1 swap per caption phrase (f2_085 to f2_087 to f2_088 within 1.5 s). The head shakes are whole-sphere rotations with motion blur (f2_088). The laugh is a head tilt plus a blur (f2_040, `f_007`).
- Walking: the legs are **noodle tubes with a smooth knee arc**, not hinged sticks. Small steps, the bean bobs about 0.05 D, the arms swing as soft curves (f2_100 `walk_f2_100.png`, f2_061–f2_064 march). Arms bend in one smooth curve and can pass in front of the bean (f2_032 right officer, f2_100).

## 5. Kong recipe (Blender 5.3, Cycles, units D = head diameter)

Keep the character-sheet identity: round white head, simple black-line face, spiky black hair, orange RESCUE jacket with silver bands and a Thai flag, black trousers, boots, backpack. Build and light it the way ref D does.

1. **Head**: a UV sphere, D = 1.0, 64x32, scale (1, 0.97, 0.98). It sits on the bean with 0.05 D overlap. No neck and no collar ring (or a flat collar decal only).
   Shader: Mix(Diffuse 0.78, Emission 0.22) of base `#F7F2EA`. Tint the diffuse shadow with a lavender ramp (Shader-to-RGB, then a ColorRamp from `#CFC7DB` at 0.0 to white at 0.45), so the lit-to-shadow drop is **≤ 18% L** even under a hard sodium key. Specular 0, roughness 1. Add an AO node (distance 0.08 D) multiplying 0.88 so that the hair, the collar and an arm crossing the face leave contact shadows.
2. **Face decal**: in angular sphere coordinates, front ±40°. Brows 0.17 x 0.035 D at the "determined" angle. Lidded half-oval eyes 0.08 x 0.05 D. Mouth arc 0.12 D wide, line 0.03 D. Stubble: about 25 dots of 0.01 D on the jaw only, at 50% grey (not 70 dots).
   Expression set: determined, tired (lids lower), alarmed (white ring eyes with dot pupils, as in f2_087), shouting (open D 0.16 x 0.11 D, interior `#8E2430`, tongue `#E9868F`), plus a sweat-drop card beside the head.
3. **Hair (the main fix)**: a matte black shell plus **flat, jagged cookie-cutter tufts**, not cones.
   - Draw the sheet's spiky silhouette as one 2D outline: 7–9 points, each 0.10–0.18 D tall, plus 2 side flares of 0.08 D and 3 short fringe points over the forehead that stay above the brows.
   - Extrude it 0.04 D, bend it to follow the scalp at an offset of 0.01 D, and add a second shell layer behind it rotated 90° so the hair holds up at 3/4.
   - **Max height above the crown: 0.22 D** (v5 had 0.54 D).
   - Material `#141418`: roughness 1, specular 0, plus 4–6 painted dark-grey strand strokes (like the hat hatching in f2_104) at about 10% contrast. Wet: a single thin sheen strip only (coat 0.15, coat roughness 0.35).
   - The hair carries the ink outline.
4. **Body bean**:
   - A capsule 1.12 D wide (head/body = 0.89), 1.45 D tall, depth 0.85 of its width.
   - **The whole bean is the jacket** in orange `#E8732A`, dry or wet. Do not split off a black lower half.
   - The black trousers read as a 0.12 D black hem band at the bottom of the bean plus the black legs.
   - Fabric shader: Principled with roughness 0.85, specular 0.15, sheen 0.25, and a painted fold/noise texture at 8–10% contrast.
   - The two silver bands are raised 0.012 D, `#C8CCD3`, roughness 0.5, specular 0.3. That is retro-reflective but **not chrome**.
   - RESCUE patch, Thai flag (screen-left upper side), zip line, pockets and seams are decals at half ink weight (0.012 D).
   - Radio: a small inked box on the chest strap.
   - Backpack: a rounded box 0.75 x 0.85 x 0.32 D behind the bean, matte `#33343B`, inked. The straps are raised bands.
5. **Limbs**:
   - Bezier tubes, **radius 0.028 D** (thickness 0.056 D), black `#18171C`, roughness 0.9, specular 0.05, no coat (wet: coat 0.08, coat roughness 0.5).
   - Legs 1.1 D from the bean bottom, arms 0.95 D from the upper side of the bean.
   - Bend them as one smooth arc (3 control points, handles 0.3 D, the knee/elbow never a sharp angle).
   - Hands are black ball caps r = 0.04 D (gloves). Only the hand that grips the cutter gets a simple mitten form.
   - Boots: a rounded oval 0.22 x 0.13 x 0.11 D, `#1B1D26`, roughness 0.8, with a 0.02 D grey sole line.
   - Limbs need no outline (they are already ink black).
6. **Outline**:
   - An inverted hull on the head, hair, bean and backpack: Solidify with thickness **0.024 D** (head) / 0.020 D (bean, hair, pack), flipped normals, emission `#150F13`, holdout on the back faces toward the camera. Alternatively a Line Art modifier with silhouette plus border only.
   - Check: the outline must measure **2.3–2.5% of the head's pixel diameter, never under 2 px**.
   - Add a pale 1 px separator (L ≥ 140) outside the ink when the background is darker than the ink (night sky), so the silhouette still reads, the way the snow does for ref D.
   - The cutter, the cars and the other props get **no** ink.
7. **Proportions check** (in a front ortho at the feet):
   - head D 1.0
   - bean 1.12 x 1.45 D
   - legs 1.1 D
   - total height crown to sole **3.5 D**, plus hair 0.22 D
   - head/body width 0.89
   - limb 0.056 D
8. **Lighting**:
   - The heads keep ≤ 18% falloff, while the bean takes the full scene key. Aim for a 30–40% lit-to-shadow drop with a cool-shifted shadow side: the sodium key warms the lit side, the moon/sky fill sets the shadow side to blue-grey.
   - World/bounce fill must keep the shadow side ≥ 60% of the lit side. Put a contact-shadow decal under the boots.
   - No specular highlights on character surfaces except the wet hair strip and the reflective bands. Specular reads stay on the props (cutter, wet asphalt).
9. **Animation**:
   - Rotate the head as a sphere and the face decal turns with it. There is no view-bin swap like in v4.
   - Swap expressions per phrase.
   - Head shakes use motion blur (shutter 0.5).
   - Walking uses the noodle-leg cycle with a 0.05 D bean bob.

## 6. Why v5/kong3d looked toy-like (measured on `v5/kong3d/out/mcu.png` and `low.png`)

| problem | v5 kong3d | ref D |
|---|---|---|
| **Hair** | 3D cone spikes (`_spike`, `kong3d.py` l.290–590) rise **205 px above a 380 px head = 0.54 D**. Colour reads brown (62,52,51), median L 53, p95 106 with a specular sheen. No ink outline on the hair. The hair+head mass is 1.5 D tall, so it reads as a spiky helmet. | Hair/hat elements are flat, inked tufts that stick out at most 0.12–0.22 D. They are matte, with painted strokes (f2_042, f2_104). |
| **Limb gloss** | Limb roughness 0.45, specular 0.45; wet it becomes roughness 0.225 + coat 0.4 (`m_plain`, l.88–95, 596). The hand ball reaches **L 255** (blown highlight), leg p95 **L 118**. Boots roughness 0.35 / specular 0.5. That reads as glossy black plastic tubing. | Limbs median L 24–26, p95 66, with no highlight at all (f2_087). |
| **Head size ratio** | Head D 1.0 on a bean 0.94 D wide = **1.06** (1.2 on screen in the MCU). Legs **0.72 D**. Total about 3.0 D + 0.54 D of hair, so the head and hair take about 43% of the height: a bobblehead. | Head/body width **0.83–0.92**, legs **1.0–1.2 D**, total **3.4–3.6 D**. The head is about 29% of the height. |
| **Head shading** | Principled roughness 0.55: lit 246–255 (clipped), shadow cheek **L 80** = a **67% drop** with a hard terminator (mcu y600, x 140 to 410). That makes it a plastic ball. | 8–18% drop, lavender shadow, no terminator. |
| **Outline** | Hull 0.016 D on the bean and 0.018 D on the head (l.433) = **1.6–1.8% D**, about 2 px and dark-on-dark against the night sky. None on the hair. | **2.3–2.5% D** (3–6 px), on the head, body, hat and hair; always contrasting. |
| **Bean split** | The lower about 40% of the bean is glossy black trousers, so the figure reads as a black bomb with an orange top (low.png). | The bean is one cloth colour; only the stick legs are black. |
| **Extras** | A collar ring as a neck, chrome-like band and strap highlights, 70 stubble dots. | Head on the bean directly, matte bands, minimal face marks. |

Fix order by visual impact: (1) hair → flat inked tufts ≤ 0.22 D; (2) head shader → ≤ 18% falloff; (3) proportions (head/body 0.89, legs 1.1 D); (4) limbs and boots matte; (5) outline 2.4% D plus a separator; (6) one-colour jacket bean.
