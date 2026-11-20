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

## Round 8 (director QA-art): FIX, 6.9

Take: take.mkv 14:26 (first_g 929, g 929-1024, frame index = g - 929). I extracted every frame and viewed it at 3 fps, then every frame from g 984 to 1007 (the gag), at full size and at 360x640. I also cropped the right edge (x 540-720) every 2nd frame from g 994 to 1024.
Frames: /tmp/qa19_r8art/s12/all_NNN.png. Sheets: /tmp/qa19_r8art/s12_3fps.jpg, s12_gag.jpg, s12_phone.jpg, s12_key_full.jpg, s12_rightedge.jpg, s12_edge_strip.jpg.

| Check | Status |
|---|---|
| Gag on the word | **FIXED, and it is funny now.** The hair stays grey through the pan. At g 996 ("หงอก") he pops in one frame to white hair, spectacles and the brown coat, with puff clouds and a hop. At 360x640 the grey-to-white change, the glasses and the puffs all read clearly, and the picture lands on the word instead of a second early. The cartoon "aged on the spot" logic gets a laugh. |
| Slump + rub | Better. He leans and droops at g 993-1000, then the left hand rubs his eyes, with a sweat drop and a tired squint (g 1003-1024). The chisel stays in his right hand and hangs down, so continuity is good. The slump reads more as sagging sideways (toward screen right) than falling back, but it reads as tired. |
| H3 in frame | FIXED. The gold H3 wheels and gear frames fill the left ~45 % behind him during the rub. The blank-wall frame of round 7 is gone. |
| **Right edge (BLOCKER, §G "nobody cut by an edge")** | **The head is cut by the right frame edge from g 997 to about g 1012 (0.5 s), which is exactly the payoff.** In this range the right side of the white hair, the ear and bow, the ponytail and the right puff cloud run off x 720, and about 15 % of the head is missing. It is obvious on a phone (see s12_phone.jpg g 1003 and s12_rightedge.jpg). The head only closes inside the frame from about g 1014. The "head x 199-697" in QA.md is wrong: the detector misses the outline, the hair and the puffs. Check this by eye. |
| Grounding | OK. The chest with the candle and lantern hides the leg stubs. |
| Light / colour | The candle is the key and it dims; the room is warm with brass. Brightness 59.9 is dark (the conform lifts it). There is almost no cool light after the opening window. Sat 0.72. |
| Face size | OK (head <= ~250 px, about 20 % of the frame height). |

| Criterion | Score |
|---|---|
| Set | 7 |
| Light & colour | 7 |
| Composition / phone | 5.5 |
| Acting | 7.5 |
| Key moment (white-hair pop) | 7.5 |
| Match to refs (R4 candle rooms) | 7 |
| **Overall** | **6.9 - FIX (one blocker, cheap)** |

Fixes (shot.py, re-render g 990-1024 only):
1. **Keep the whole head in frame from g 994 to 1024.** Over g 990-1000, end the settle-back move about 70-90 px further left on screen: turn the look point about 0.12-0.15 D toward +x (his side), or move his mark about 0.12 D left. The hop and the slump both push him right, so do not just add slide. Target: head outline, ponytail and puff clouds at x <= 690 on every frame. Check this with a crop of x 600-720, not with the head detector.
2. (Polish) Make the puff about 1.5x bigger and hold it 2-3 frames longer (to g 1004), so the "poof" sells at phone size.
3. (Polish) For the slump, tilt the card back (top toward the wall) rather than sideways toward screen right. That also helps fix 1.
Keep the pop timing (g 996), the chisel continuity, the H3 framing and the candle burn-down as they are.

## Round 9 (director QA-art): FIX, 6.6

Take: take.mkv (first_g 929, g 929-1024). I extracted every frame and viewed them at 3 fps, every frame from g 984 to 1023, key frames at 360x640, and crops of the head (x 300-720, y 380-800) every 2nd frame from g 997 to 1015. I also measured the right-most near-white pixel per frame.
Frames: /tmp/qa19_r9art/s12/f_NNN.png (NNN = g - 928). Sheets: /tmp/qa19_r9art/s12_3fps.jpg, s12_gag.jpg, s12_key_full.jpg, s12_clip.jpg.

| Check | Status |
|---|---|
| Round 8 blocker: head off the right edge | **Fixed for the frame edge.** The right-most head/puff pixel is at x <= 600 on every frame from g 990 to 1024, with nothing in x 700-720. |
| **NEW BLOCKER: the head is sliced by the wall** | **From g 997 to about g 1013 (0.55 s, the payoff) the right side of the card is cut by a straight vertical line at about x 550-590.** That is where the card tilts back into the plaster wall. The right puff, the ponytail, the bow and about 15-20 % of the head vanish into the wall (see s12_clip.jpg and s12_key_full.jpg g 1000). On a phone this reads as a cut-off head with a hard edge, the same fault as round 8 moved 150 px left. §G "nobody cut". The head comes back whole from about g 1015. |
| Gag on "หงอก" | Works and is funny. Grey hair, apron and chisel at g 995 pop in one frame (g 996) to white hair, spectacles, the brown coat and puffs, then the tired eye-rub with a sweat drop and a wobbly mouth. The puffs are bigger and last to about g 1006, so the "poof" sells at phone size. The chisel stays in his hand. |
| Slump | The backward tilt reads as an exhausted sag, which is better than round 8. But the tilt is exactly what drives the card into the wall. |
| Set / H3 | The gold wheels are visible left and behind him; the candle, lantern and chest are in the foreground. Good. |
| Light / colour | Warm candle key. Sat 0.72, vivid 80 %. Luma falls to 56 by g 1019, which is dark (the conform lifts it). There is no cool light after the pan. |
| Face size | OK, about 20 %. |

| Criterion | Score |
|---|---|
| Set | 7 |
| Light & colour | 6.5 |
| Composition / phone | 5.5 |
| Acting | 7.5 |
| Key moment (white-hair pop) | 7 |
| Match to refs (R4 candle rooms) | 7 |
| **Overall** | **6.6 - FIX (one blocker, cheap)** |

Fixes (shot.py, re-render g 994-1016 only):
1. **Keep the card clear of the wall.** During the slump (g 996-1014), move Harrison's mark about 0.2-0.3 D away from the wall (toward the camera / screen-left), or tilt the card about its base toward the camera instead of back toward the wall. Check every frame from g 994 to 1016 with a crop of x 450-720: the puff, the ponytail and the bow must be whole, with no straight cut line.
2. (Polish) Lift the exposure about 15 % after the pop, or add a cool moon rim on his left. The ending frames are at luma 56.
Keep the pop timing (g 996), the puffs, the glasses and rub, the chisel and the H3 framing.
