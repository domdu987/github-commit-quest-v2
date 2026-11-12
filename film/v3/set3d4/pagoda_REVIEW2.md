# REVIEW 2 of v3/set3d4/pagoda.py (v2: density, depth, warm light, the golden pillar insert)

Pictures: **`compare2.jpg`** (per s01 shot: v2 still | old s01 frame | reference a t0001 / t0003 / t0005 / t0007 / t0031, 360x640, rendered
720x1280 12 samples with the shot.py cameras, staging and cast4 actors by `pagoda_work/v2/s01_v2.py`), `pagoda_contact2.jpg` (all 32 camera x
preset finals, `pagoda_work/final/`), `pagoda_work/stills/` (360x640 contract stills, regenerated), `pagoda_work/tests/` (sway, pillar swing,
cutaway, crack, collapse, quake, all re-run on v2). v1 sources kept as `pagoda_v1_backup.py.txt`, `pagoda_tex_v1_backup.py.txt`, `pagoda_API_v1.md.txt`.

## 1. What changed, by the director's four gaps

1. **Density / ornament** (all in `build()`, `dress=True` default):
   - Ground storey: open base (folded from shot.py), red velvet drapes gathered with gold tie-backs and tassels in the three front bays under a
     swagged gold-fringed pelmet, two big lit lanterns, ban banners at the front eave corners, warm bracket band; inside: dragon murals in
     red-gold frames on six bays, glowing round lattice windows (marumado, the reference's rose window) in the three middle bays, red dado,
     runner + square carpet round the stone, a gilded canopy with chains of gold beads and red tassels (yoraku) round the pillar, two gold
     candelabra, fire bowls (kagaribi) on the platform.
   - Every storey: gold fittings on all posts, 3D bracket blocks (red / green, gold caps, top tier under the soffit), beam ends with gold tips,
     festival bunting on the balcony railings (storeys 1-4), 38 lit paper lanterns under the eaves, ban banners from storey 1's corners.
   - Yard / street / gate: the shot.py carpenter's yard folded in and extended (plank stacks, sawhorses incl. a log on one, beams, tool rack with
     saws / adzes / mallet, rope coils, log piles, barrels, rice bales, carts), material stacks by the tower, extra stone lanterns, potted pines,
     noren; a red runner from the street (y -70) through the gate up the steps to the stone; 22 richer banners on poles, 24 hangings on the
     south yard wall, the gate curtain (maku) and gate banners. New textures (SVG, `pagoda_tex.py`): curtain, valance, ban, nobori2, maku,
     carpet, mural, maru, cloud_band, scales.
2. **Depth**: `setup_dof(scene, focus, fstop)` / `apply_dof(cam)` / `update_dof` (API 1b). Cycles Z pass -> CoC -> one Fast-Gaussian level
   with in-focus pixels masked out (normalised convolution), so actor cards stay sharp with no halo; ~0.4 CPU s. The compositor Defocus node
   was tried first (works headless, looks right) but cost 4.6..8 CPU s per frame, so it was replaced. Verified on renders: actor in focus
   sharp, background and near foreground soft (street_eye, s01 shots 1 / 2 / 4). Defaults on for the inserts, street_eye, rubble_dawn,
   pagoda_low (a hint), off for two_buildings, town_wide, cutaway_full.
3. **Light**: still one hard key and blue-violet shade. New in-scene warm sources: flames of fire bowls, candelabra, oil lamps (emission 4..4.5
   -> bloom), 40 lanterns (1.25 by day, 2.6 at night), glowing round windows. Their light is painted into the shaders (`_extra`: warm wrap
   glow with distance falloff + a Blinn highlight of the flames, noise free, no light objects): warm interior / pillar / murals / carpet, a warm
   rim and bounce on the ground storey's front, bracket band and drapes; the ground-storey soffit stays cool on purpose (warm glow on red-brown
   rafters in violet shade read pink). Exterior gold gets a GGX lobe for the sun (real, shadowed glints). Hue tool
   (`pagoda_work/v2/hue_rows2.txt`): magenta per preset 1.5..6.6, per s01 shot 0.5..7.7 (ref a t0001 / t0007: 9.5 / 9.8); the only frames
   above 9 are SUNSET_crack_insert 19.5, SUNSET_town_wide 9.2, DAWN_crack_insert 9.5, identical to v1 (19.3 / 9.1 / 8.8: tower plaster and
   haze, untouched).
4. **The key insert**: the pillar foot is a polished bronze shoe with beaded gold rims, a cloud-scroll sleeve, gold bands, and a gold dragon
   (scaled body, dorsal spikes, claws, horned head with red eyes, fangs and open jaw) coiling down the pillar with its head right above the
   foot, turned to the insert cameras; gold highlights from the lamps; the 0.25 D gap stays open with a dark contact shade on the stone so it
   reads as a dark slot; the canopy's bead chains hang in the top of the frame (the pillar's real chain is 14 D up and cannot be in an insert
   at the foot). In s01 shot 2 the dragon head fills the upper half, foot and gap below, warm blurred murals behind (ref t0003).

## 2. Against the reference (compare2.jpg, looked at full size)

| shot | old | v2 | still different from the reference |
|---|---|---|---|
| 1 (t0001) | dark violet box, bare pillar, one lamp | drapes and pelmet framing kenta, lantern, red-gold bracket band, warm interior with murals, dragon pillar, canopy chains, carpets, soft background, kenta sharp | upper third is a cool soffit where the reference has a lit stone wall and rose window; bracket blocks are plain boxes |
| 2 (t0003) | orange cylinder, flat stone | gold dragon head over the bronze foot, highlights, dark gap, blurred red/gold room | our dragon is a simple low-poly cartoon (no scale relief in the silhouette); no fire bokeh in the frame (the lamps sit behind the pillar from this camera) |
| 3 (t0005) | sky + violet soffits | red-gold ban in the foreground, lit lanterns on every eave, gold brackets, depth hint | still mostly sky and violet soffit: the reference is an interior; this camera cannot see much ornament |
| 4 (t0007) | bare doorway, flat townspeople | lanterns, fire bowl, drapes, runner, interior detail, townspeople softly out of focus | reference background is calmer and greyer (sat 0.27 vs 0.45) |
| 5 (t0031) | bare street | red runner up the street axis, more banners, gate curtain, wall hangings | the reference's ranks of soldiers (cast, not set) and the castle wall banners at scale |

hue (red / orange / blue, sat): shot 1 old 12 / 46 / 22, 0.49 -> v2 47 / 27 / 11, 0.56 (ref 27 / 31 / 24, 0.29); shot 2 1 / 91 / 4 -> 10 / 90 / 0
(ref 9 / 77 / 0); shot 4 11 / 50 / 19 -> 32 / 41 / 10 (ref 26 / 23 / 34). v2 is warmer and more saturated than the reference interiors.

## 3. Cost (720x1280, 12 samples, 2 threads, CPU s)

All 32 set camera x preset finals 12.5..23.6 (`pagoda_work/v2/final_log2.txt`). s01 shots with cast4 actors: 23.4, 22.9, 13.8, 25.1, 15.2
(old frames 21.5, 18.0, 12.7, 22.0, 14.1); measurement noise is about +-0.6 s, shot 4 sits at the limit. Savings taken: Defocus -> layered
blur (-5), no ink hull on the interior, the bead chains and the bracket blocks (-2), no GGX lobe inside, merged glow points.

## 4. Notes / open

- shot.py must drop its `build_dressing()` (props would be doubled); `open_ground_front()` / `warm_interior()` are now no-ops. Use
  `G.setup_dof(scene, Tk.kenta.card, 3.5)` style calls per shot (s01_v2.py has the values used).
- The contact shade under the pillar is fixed to the stone; with a large pillar swing (> 2 deg) it shows beside the foot.
- `pagoda_work/stills/` and `final/` were overwritten with v2 renders (v1 contact sheet `pagoda_contact.jpg` kept).
- Determinism: digest dd713287... (after the runner fix) identical in two processes.

## 5. Fix: the red runner (director's note on s01 g 0140 / g 0167)

Defect: the stair runner was 1.4 D on the 3 D stair, its texture mapped u 0..0.7 (only the left gold border showed, so it read as half a
runner), and the treads / risers were separate flat pieces with the same shading, reading as one sheet laid diagonally over the step
edges. The courtyard and street runner had the same half-texture mapping (u 0..0.7); the interior runner was 1.6 D wide and swayed with
storey 0 across the platform; the carpet ring round the stone had its borders running across the front / back strips.

Now (`_runner`, `runner_profile`, `RUNNER_HW = 0.975`, `STAIR`): one continuous runner object `runner`, 1.95 D wide (65 % of the stair,
equal 0.525 D stone margins), centred on x = 0, from the street (y -70) through the gate and courtyard (z 0.03), over each of the three
steps as riser -> rounded nosing lip (0.03 D) -> tread, flat across the platform to the storey front (y -3); full texture width (both gold
borders), the pattern running on along its length; risers in a slightly darker carpet (gain 0.78) and the carpet's side edges have
thickness, so every step reads. Inside the storey the same width continues to the carpet ring (part of interior_v2), whose four strips now
all carry their borders along their length. Verified at 360x640 (`pagoda_work/v2/runner/`: s01 shot 4 g 140 / 167 with cast4, street_eye,
pagoda_low, two_buildings; script `pagoda_work/v2/runner_check.py`). Nothing else changed.
