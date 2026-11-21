# REVIEW of v3/set3d5/mine.py (film 5: the coal-mine tunnel and the pithead)

Pictures: **`mine_contact.jpg`**. Row 1 has the six tunnel finals. Row 2 has the four pithead finals next to ref a t0089 and t0001. Row 3 shows the blast at u 0.2, 0.4, 0.6 and 0.8 from blast_wide, then u 0.1 and 0.5 from tunnel_run. Row 4 shows gas at 0, 1 and 3, then the insert flame at 0, 1 and 1.8. Also in `mine_work/`: `stills/` (360x640 contract stills with placeholder actors), `final/` (720x1280 at 12 samples), `tests/` and `anim/`. The reference frames a/t0001, t0067, t0077, t0089 and b/t0010 were looked at full size.

## What was built (density pass at the pagoda v2 bar)

- **Tunnel** (`build('tunnel')`): the roadway is 40 D long with a gentle bend and noise-displaced coal walls. The coal texture has strata, cleat and pick marks, plus pyrite and mica specks that glitter as painted specks. The coal face at the end has an undercut, a heap, a pick stuck in it and a shovel.
  - 16 timber sets: legs, cap bars, lid wedges, roof wedges, lagging over the bars and behind the legs.
  - Rails and sleepers on the curve, with haulage rollers and rope. Six coal tubs: a three-tub train with couplings, plus one each at the face, the pit bottom and in the cage.
  - Two catenary cables on hooks, a bell wire, and the air pipe with flanges and brackets.
  - Six hanging flame safety lamps (brass bonnet, gauze, glass, pillars, flame), each with a warm floor pool and halo cards. The foreman's lamp hangs on a chain for lamp_insert.
  - The brass canary cage on its nail: 16 wires, dome, hoops, perch, cups, door.
  - The side heading has its own sets and a ventilation-door frame with a draped canvas sheet ("KEEP THIS DOOR SHUT").
  - The pit bottom: whitewash, steel joists, electric lamps, fire buckets, a bench, the signal rapper and a "PIT BOTTOM" sign. Behind it, the brick shaft with the two-deck cage and half-open lattice gates.
  - Smaller dressing: picks and shovels (leaning, on the floor, hung on a prop), a rope coil, jackets, snap tins and water bottles, a timber stack, stone-dust sacks, a water barrel, signs, a refuge hole, a sledge, loose coal, 10 glossy puddles, hanging drops and falling drops.
- **Pithead** (`build('pithead', 'DUSK' | 'DAWN')`):
  - A steel lattice headframe with X-bracing, platform and railings, two spoked sheaves and back-legs. Ropes run to the brick winding-engine house (lit arched windows, "No. 2 PIT").
  - Boiler house and a 36 D chimney with a smoke plume.
  - The bank (deck) with steps, cage, lattice cage gate and railings. Rails go down a ramp to the yard and the heaps, with tubs on them.
  - Four coal heaps, gas lamp posts, a pit-prop stack, barrels, sacks, a wheelbarrow, tools, two railway coal wagons on a siding, a telegraph line, a fence and puddles.
  - The first-aid hut: green weatherboard, slate roof, lit window, door, "FIRST AID" board and a lamp.
  - The bench with the **brass oxygen box**: engraved "OXYGEN" plate, a dial, and a glass window in the front showing a green cylinder, valve and breathing bag inside. A lid with a handle, a rubber tube and a small mask.
  - A 3D terrace row, a painted backdrop of terraced rows with smoking chimneys, chapels and far headframes, and a smoky sky.
- **Controls**: `lamp_light` (keyed moving miner lamps), `set_gas` (faint layered haze, invisible at 0.5..1 and just readable at 3), `set_blast`, `set_flame`, `set_cage` (carried or swinging), `set_drips` and `set_lamps`.
  - `set_blast`: the fireball forms at the face and races to y 1 by u 1. Front blobs are yellow-white and the tail is orange-red, with dark smoke, 40 debris pieces (coal, splinters, embers), dust, and keyed flash lights.
  - All controls are keyed per frame and checked in `t_anim.py` (OK).

## Light: what differs from the template, and why

1. **No sun underground.** The lamps are real point lights so miners can carry them and cast shadows. The template's toon term divides by the sun's N·L, so it is removed on every tunnel material (`_untoon`). The fixed and pit-bottom lamps are shadowless: this saves 1.7 CPU s and the frame looks the same.
2. **Denoiser on.** About 12 lamps at 12 samples leave light-selection grain that the template's painted lights never had. OpenImageDenoise (albedo and normal guides, fast prefilter) costs about 2.3 CPU s and the result is clean. The light tree is off, because it cost about 4 s more. `M.setup_render` wraps the tower version: use it.
3. **Light linking.** A lamp's own light does not light its own brass and glass; without this the whole lamp blew out into one blob. Instead the lamp bodies get the painted glow of their flames (`pagoda._extra`).
4. **Shade colour.** The shade is a deep blue (hue about 230-250) with shade_mix 0.8. The lamp colour is a yellowish warm (1.0, 0.8, 0.5), and the timber is ochre. The first pass used a violet shade with an orange lamp, and timber in mixed light came out mauve (magenta up to 33 %); it is now 2-10 %.
5. **Brass and gold** use the pagoda metal rule (dark-gold shade), so the cage and lamps read golden in blue shade.

## Against the reference (looked at full size)

| shot | reads like the reference | still different |
|---|---|---|
| tunnel_eye / low / run vs a t0089, t0077 (night, lamp windows, torches) | blue night palette, warm lamp accents, depth through repeating frames, ink outlines, soft DOF | value is a little low (0.45 vs 0.54) and the walls are a darker, greyer blue than the ref's saturated lavender stone (sat 0.27-0.38 vs 0.47). The torches in the ref throw big glows; our hanging lamps are small and read as lanterns |
| cage_insert / lamp_insert vs a t0001 (golden dragon, fire bowl) | golden brass objects against a blurred, lamp-lit room, warm bokeh | the cage's brass is fairly flat (no engraved detail); the insert flame is small inside the glass, and k 1.8 is only modestly taller |
| blast_wide | a cartoon fireball filling the roadway, debris, flash on the timbers | the fire blobs read as soft clay lumps rather than billowing flame; there is no motion blur; the dust sprites are flat |
| pithead_wide DUSK / DAWN | a strong silhouette of the headframe, chimney and engine house against a smoky orange (DUSK) or pale misty (DAWN) sky; lit windows and lamps | only one sheave clearly reads (the second sits behind it from this angle); the yard foreground is fairly bare; actors are small; DAWN is low-saturation (0.18) on purpose (mist), which is below the band |
| oxygen_insert | the brass box reads clearly: the OXYGEN plate, the dial and the green cylinder behind the glass | the bench and hut wall are big flat red-orange areas at dusk; the hut window is a blown yellow block in the background |

Hue: tunnel finals have **magenta at or under 10.5** (target 10) and are blue-dominant as expected for night; the **red and orange bands are low**, by design (lamp accents only). Pithead DUSK has red 31, orange 24, blue 19, magenta 8. DAWN has magenta 2.

## Cost and determinism

All 10 finals take **19.8..24.2 CPU s** at 720x1280, 12 samples, 2 threads, including denoise, DOF and bloom (`mine_work/final_log.txt`). The heaviest are DUSK and DAWN oxygen_insert (24.2 and 23.8) and tunnel_eye (23.9).

That is tight: cast actors will add about 1-2 s, as they did on the pagoda. Measured breakdown: scene sync about 1.5, path tracing about 1.6 per sample, compositor 1.3, denoise 2.3. Shading complexity is not the cost: replacing every material with a plain one changed nothing. If shots go over, the levers are, in order:

1. Fewer actor lamps per shot.
2. `M.setup_dof(..., None)` on wides.
3. Dropping the denoiser on wides with few lamps.

Digests are identical in two processes: tunnel 9faaa55e..., pithead DUSK 2b2853a8....

## Notes for shots

- `lamp_light` creates a real light per call name. Key every frame of a moving lamp; place it at the flame of the cast's lamp prop.
- The bird is a sprite: use `A['cage']['perch']` for its feet and `set_cage` to carry the cage.
- At the pithead, `A['oxygen']['bird_spot']` is the spot on the bench beside the box.
- The blast front positions are given by `M.blast_front(u)`. The fireball engulfs anything inbye of the front, so keep runners outbye of it.
- `hue_report.py`'s "reference A interiors" row has a broken file pattern and crashes; `mine_hue.py` works around it. The tool itself (not in my folder) was not changed.
