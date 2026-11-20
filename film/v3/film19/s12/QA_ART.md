# s12 QA-art (MERGED shots 12 + 13, WORKSHOP NIGHT, H3, age swap)

## Round 7 (director QA-art): FIX, 6.5

Take checked: take.mkv 13:25 (first_g 929, g 929-1024). Frames: 3 fps plus every frame g 950-976 (whip and swap), at full size and 360x640. A shift estimate (row-mean cross-correlation) and frame-diff per frame over the whip.
Frames: /tmp/qa19_r7art/s12/all_NNN.png (NNN = g - 929 + 1), f3_*.png; sheets /tmp/qa19_r7art/s12_3fps.jpg, s12_whip.jpg, s12_swap_phone.jpg, s12_phone.jpg

| Check | Status |
|---|---|
| Opening (g 938-965) | Good. Greying Harrison in his apron taps the chisel at the bench, with the brass H3 gears behind him, a candle on the chest, a blue night window at the left and a warm wall glow. Night mood reads. |
| "Whip" pan | **Not a whip.** The measured image shift peaks at about 20-23 px per frame (g 960-965), about 3 % of the width. There is no motion blur, and every frame is sharp. On a phone it reads as a slow slide. |
| Age swap invisible? | **No.** At g 965 to g 966 the swap is a hard, fully visible pop. Harrison is in the same screen spot (head x ~300). Grey hair, apron and chisel change to white hair, spectacles, coat and hand-on-chin in one sharp frame. The chisel vanishes and the pose jumps. Nothing hides it. |
| Ageing gag reads? | Half. The old look reads at 360x640 (glasses, white hair, coat, sweat drop). But the hair is already white at g 966, on "สิบ", a full second before "จนผมหงอกทั้งหัว" (หงอก ~g 996). The punchline word arrives after the picture has already told it. The jump from grey to white hair is also small, because the "young" Harrison already has grey hair and wrinkles. |
| Funny? | Mildly. The eye-rub with the sweat drop (g 1000-1015) is the best beat. The "lean back" (g 993-1003) is barely visible: it reads as a hand moving from chin to eye, not a slump back. |
| Composition after the whip | From g 967 the camera looks into the corner. The right ~40 % of the frame is plain pink wall, and the H3 (the clock he has spent ten years on) is out of frame or reduced to gear shapes at the far left. Harrison sits left of centre behind the lantern. This is a dead frame for 1.6 s. |
| Edges / face size | OK. Head 198-255 px (well under 35 %). Nobody is cut by an edge. |
| Grounding | Weak. The legs end in thin white stubs that run down in front of the chest's left edge (g 964-1015), so he reads as hovering or poking through the chest at phone size. This is a known rig limit, but here it sits right at the centre of the frame. |
| Light & colour | Good. The candle is the motivated key, the light visibly dims (1.0 to 0.25), with a warm wall glow and a cool blue window only in the opening. After the whip it is warm-only. Brightness 66.8 is under the 85 target before the conform. |

| Criterion | Score |
|---|---|
| Set | 7 |
| Light & colour | 7.5 |
| Composition / phone | 6 |
| Acting | 6.5 |
| Key moment (age swap gag) | 5.5 |
| Match to refs (R4 candle rooms, R5 travel) | 6.5 |
| **Overall** | **6.5 - FIX** |

Fixes (shot.py / cast cues):
1. **Hide the swap for real, or make it a deliberate gag. Pick one.**
   - (a) Invisible: make it a true whip. Peak 120-180 px per frame for 4-6 frames (g 962-968), with directional motion blur (Cycles motion blur, shutter 0.5, or a post smear of 60 px or more on those frames). Swap on the peak frame. Or put a foreground occluder across the lens at g 966 as a wipe: the lantern, a roof post, or the H3 frame passing close to the lens.
   - (b) Gag (recommended, funnier): after the whip, keep him grey-haired but in the old coat and spectacles, slumped and tired. On "หงอก" (g ~994-997), pop the hair to white in 1 frame with a small puff or flash and a 3-frame squash. The narration then lands the joke on the word, and the swap no longer has to be hidden.
2. **Keep the H3 in the tired frame.** End the whip about 0.6 D earlier, or turn the look point back left about 0.5 D over g 975-1015, so the H3 (balance moving) fills the right side next to him instead of the blank wall. Ten years on this clock should be in the picture when he rubs his eyes.
3. **Bigger lean back.** Rotate the card 10-15 degrees back with a 4-6 % squash over g 993-1000, the arms dropping or flopping, then the rub. It must read as "exhausted slump" at 360x640.
4. **Chisel continuity.** Keep the chisel in his hand after the swap (resting or dangling), or let it drop on the swap, instead of vanishing.
5. **Grounding.** Hide the leg stubs behind the chest (raise the chest 0.1 D, or place Harrison 0.15 D further behind it), or give the shoes a contact shadow on the floor.
Keep the candle burn-down and the frame-diff (median 5.6 / p90 14.5) as they are.
