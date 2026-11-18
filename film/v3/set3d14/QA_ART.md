# QA-art — film 14 "ไอ้บ้าผึ้ง" — SET gate

Reviewed: `farm_work/final/*.png` (16 finals, full size 720x1280, every key frame opened one by one), a 360x640 phone sheet of all 16
(made in scratch, not committed), `contact.jpg`, `styleboard/board.jpg`, `cast14/sheet.jpg`, the quality bar `set3d10/contact_small.jpg` +
`cast10/sheet.jpg`, `analysis/sheets/bell_0.jpg`, `farm_work/hue_rows.txt`, `final_log.txt`. Placeholder cards = puppet positions/sizes.

## Verdict: FIX-FIRST

The world is good: warm, sharp, no DOF, no text, nice Kenyan palette, true to the style board. But at phone size the story's key images do
not read yet. The low presets are about half foreground grass. The subjects are small, hidden or upstaged. Three of the six key moments
(the hook, the push wave, the ending) would not be understood by a blind viewer. Fix the blocking items below, then show the client.

## Scores (1-10)

| area | score | note |
|---|---|---|
| Set density / ornament | 7 | Village, huts, acacias, mountain, hive roofs and flowers are rich and in the series' toy-3D look. But the lower 40-55 % of fence_line x4, fence_low_night, push_side x2, trunk_close and uncle_hang is the same tall grass clump, so the dense set sits in a strip at mid-frame. set3d10 fills the frame with built ornament: bunting, crates, lamps, scaffold. |
| Lighting & colour | 7 | DAY, DUSK and MORNING are warm and pleasing, with a clear hard key and long shadows (hive_close DUSK is the best frame). NIGHT has a flat, very saturated lavender sky with no gradient or stars, and the style board had a deep blue gradient. Warm practicals are random campfires in wrong places (see 5). Shade hue is out of band on all four fence_line frames (222-232), uncle_hang (239.5), village_wide DAY (238) and yard_two_shot DAY (272). |
| Composition / framing per preset | **4** | village_wide: good vista, but the bottom 45 % is empty meadow and the people are 15 px specks. fence_line: hero card ~60 px tall at the vanishing point, and grass covers the lower half. yard_two_shot: the goat stands dead centre between the two speakers, the cards are pushed to the edges and the sacks are huge in the foreground. push_side: four yellow jerrycans are the biggest, brightest thing in frame, the goat is in front of the matriarch, and the hive row is hidden. fence_low_night / trunk_close: matriarch cut by the left edge. uncle_hang: uncle stands beside the stool, not on it, and the frame is too wide. |
| Cast appeal / acting (sheet) | 8 | cast14 matches the series (cast10): appealing faces, clear poses, a lip-sync set, nose_swell 0..1 and the elephant expressions all read. Note: nose_swell 1.0 is only ~1 head long. "Like an elephant trunk" will land better with a longer, curling 1.0 (or 1.2) key. |
| Key moments | **4** | (see below) |
| Match to style board / series | 6 | Board palette and light presets are kept (7). Against the set3d10 bar and the hit refs the frames are farther away and more grass-bound: their mediums put heads at 15-30 % of frame width, ours put them at ~8-10 % (6). |

### Key moments (phone-size read)
| moment | read | why |
|---|---|---|
| Hook: fence, village laughs | 3 | village_wide DAY fs1: the one hive and the hero are invisible at 360x640, and no laughing crowd is visible. fence_line fs1: hero is a speck and the single hive is at the far left edge. |
| Count beat (1 / 10 / all + wire) | 4 | fs1, fs2 and fs3 are almost identical at phone size. Only the wire's appearance changes. The roofs hide the hives, and the grass hides the posts. |
| ONE wire links all hives | 7 | hive_close DUSK (wire through every hive, receding) and field_night_wide (wire along the whole row) show it clearly. Keep these. |
| Push wave + bee burst | 3 | push_side: the matriarch stands in front of the hive row, so the swinging/knocking wave along the wire cannot be seen, and the wire is a faint line at the left. The bees read as gold glitter or haze, not as bees coming out of each hive. |
| Bees at eyes / trunk | 6 | trunk_close: bees around the eye and trunk tip read. The elephant is cut in half by the frame edge, most bees still cling to the hive, and a stray bright flame sits in the bottom-right corner. |
| Trampled uncle field | 3 | uncle_field_morning uf1 reads as a golden, ripe, intact crop with no flattened stalks, no footprints and no visible broken thorn fence. A campfire burns in the morning field. |
| Swollen-nose ending | 2 | No preset is close enough. In uncle_hang the uncle's head is ~35 px at phone size, so the nose gag is invisible, and the stool is not under him. |

## Changes, by impact

1. **[BLOCKING] Clear the foreground and bring subjects closer on every low preset** (fence_line, yard_two_shot, fence_low_night,
   push_side, trunk_close, uncle_hang):
   - Remove grass/flower scatter inside a ~3-4 m wedge in front of each preset camera (cull by camera distance), or drop the scatter
     density 80 % there. Leave low red-earth path with a few tufts.
   - Delete the jerrycan stack from push_side, and the sacks and yellow bucket from yard_two_shot (move them to frame edges, ≤ 10 % of
     the frame).
   - Tilt or raise the cameras so the subject band sits at y 450-820. Dolly in so medium-shot heads are ≥ 120 px tall at 720 wide (cast10
     / bridge_deck bar).
   - yard_two_shot: move the goat out of the centre, behind and to one side. Place hero and uncle ~1/3 and 2/3 across, facing each other,
     with the hive fence behind them.
2. **[BLOCKING] Rebuild push_side so the reveal reads inside the 3D world.**
   - Use a 3/4 side camera looking ALONG the wire, with the wire running diagonally from frame-right foreground to frame-left
     background, and 6-8 hives in a row clearly visible under their roofs.
   - Put the matriarch at the near end (frame right) with her chest on the wire, and nothing between the camera and the hive row (no
     goat, no props).
   - Check at phone size that `set_wire_push` at 0.35 and 0.7 shows a visible bow plus hives swinging at different angles (raise the
     swing amplitude if it does not read).
   - Burst: each hive entrance emits its own column (swarm_column/burst cards). Draw fewer, larger bees near the camera (≥ 8 px at
     phone size) so they read as bees, not glitter.
   - trunk_close: frame the whole head + trunk (no edge cut), move the swarm off the hive onto the eye and up the trunk (`bloc`
     target), and remove the corner flame.
3. **[BLOCKING] Ending.**
   - Add an `uncle_nose_close` preset: a medium close-up with the uncle ON the stool (feet on the seat, stool under him) and his head
     ~260-300 px wide at y 450-650. The hive he is hanging and the fence roof are above-left, and the trampled field and village are
     behind in morning light. Hard cut on "งวงช้าง" needs the nose to fill the read.
   - Make nose_swell 1.0 trunk-like (longer, drooping curl). Fix uncle_hang so the stool is under his feet.
4. **[BLOCKING] Trampled field `set_uncle_field(1)`.**
   - Lay stalks FLAT and at random angles on the ground (rotate 70-90°), and snap half of them mid-height.
   - Keep greens and browns. Do not use the uniform golden standing leaves: they read as a healthy harvest.
   - Add oval elephant footprint decals in the red earth, a broken, scattered thorn fence, dangling tin-can strings and scattered
     chewed cobs.
   - Remove the campfire from uncle_field_morning.
5. **[BLOCKING] Hook and count beat legibility.**
   - Hook: make the opening frame a lower, closer `village_wide` variant (or a `fence_line` with crowd). The hero is on the stepladder
     hanging the hive at y ~600, the hive with its tin roof is ≥ 100 px, and 3-4 laughing villagers plus the uncle stand on the path in
     the foreground mid-ground.
   - Fix crowd placement: in yard_two_shot DUSK cr1 the log puts 5 villagers in frame, but only the uncle is visible (the others are
     hidden behind the goat/sacks).
   - fence_line count: angle the camera ~25° more onto the fence so the hives (not only the roofs) show. Stage 1 = one hive centred near
     the hero; stage 2 = 10 hives clearly countable along the row; stage 3 = the white wire threaded through all of them.
6. **[Fine during shot work] Clean-up and colour.**
   - Remove stray props: the campfire under the matriarch in fence_low_night; the grey slab/tin panel by the field edge in
     village_wide/field_night_wide; the dark blue spiky plant cut by the right edge in uncle_hang; the goat in the night fence shots.
   - Night sky: add a top-to-horizon gradient (deep blue 230-245 → lighter at the horizon), the moon and a few stars as on the style
     board, and lower the sky saturation ~15 %.
   - Push day shade hue into 240-260 (fence_line, yard_two_shot DAY).
   - field_night_wide: turn the herd to walk TOWARD the fence (not parallel to it).

Blocking before the client sees it: 1-5. Fine to fix during shot work: 6.
