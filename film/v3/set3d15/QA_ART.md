# QA-art — film 15 (ไอ้ปลาดิ้น), SET gate

Reviewer: QA-art (opus). Date 2026-11-19.
Looked at: all 37 start framings in `work/final/*.png` at full size (720x1280), `contact.jpg`, `styleboard/board.jpg` (client-approved),
`cast15/sheet.jpg`, `sheet_phone.jpg`, `flop_strip.jpg`, references `analysis/sheets/rail_0.jpg`, approved `set3d10/contact_small.jpg`.

## Verdict: FIX-FIRST

The world is right. The board look carries over: golden 1963 school track with pines, brick gym, bunting and a sawdust pit, and a
dense, glowing 1968 stadium with torch, floodlights and flags. The cast is charming and on-model. The problem is framing. Many
shots are spoiled by huge dark standard poles and blank foreground slabs, or have no bar in frame when the action needs one. The
reveal shots (26, 27, 29) put a thin bar and a pale jumper over the busiest, mid-tone part of the picture. Fix these before the
client sees the sheet. None of this needs new assets, only camera, standard and light changes.

## Scores

| Area | Score | Notes |
|---|---|---|
| Set density / ornament | **6** | B stadium: rich crowd, flags, torch, floodlights, scoreboard (7). A school: good in 1, 2, 9, 13, 34, but 3, 35 and 5 show open grass and empty sky, and the ground is flat and bare compared with the rail reference and set3d10 (5-6). |
| Lighting & colour | **7** | One hard key with blue-violet shade, warm lit gym windows and pleasing period colour, true to the board. TENSE dims the crowd only a little, so 26/27 are still busy. In 21 and 31 the EVE track becomes a flat neon orange field. 33 (DAY) is washed out: white mat on a white-blue sky. |
| Composition / framing | **4** | Lowest score. Standards are 100-150 px dark columns with ladder-sized pegs (17, 18, 20, 26, 28, 30, 31, 32), and shot 4's diagonal pole takes ~35 % of the frame. Blank foreground slabs fill a third to half of 21, 22, 24 and 33. There is no bar or pit in 3, 21 or 35, though the action needs one. 3 and 35 are almost the same framing, with ~40 % empty sky. |
| Cast design & acting poses | **8** | Consistent with the series, with readable expressions, varied boys, rivals and crowd, and good comic poses (coach neck mime, finger wag, buried). Weak spot: the flop is a shallow diagonal with a straight torso, and the hips sit ON the bar line instead of clearly above it (flop_strip 2-3). |
| Key moments | **5** | Hook: 1 and 2 are fine. 3 has no bar, and 4 has a strong idea (bar against the sky) that the pole half-hides. Reveal: 25 is beautiful (board sb3), but 26/27/29 are side views with the bar and jumper over the noisy crowd and a pale mat, so they read poorly at phone size. Ending: 34 is good. 35 has no pit. In 36 the sawdust is a faceted grey-beige dome that looks like a boulder or a bread loaf, sitting on grass outside the pit. |
| Overall match to board / client taste | **6** | Sharp, no DOF, no text, reveal inside the 3D world: OK. The look matches the board. The board frames are calm, uncluttered and show the bar clearly, and many shots here lose that. |

## Reveal check: will the ∩ jumper over the bar read at phone size (26, 27)?

**Not reliably as framed.**
- The bar is about 12 px thick at full size (about 6 px on the 360x640 sheet). It runs at y ≈ 650, right where the mid-tone confetti crowd
  meets the pale lavender mat top (y ≈ 720). The head and legs that should hang BELOW the bar (the whole point of shot 27) fall onto that
  pale mat. Dick's costume B is a white vest, so it is pale on pale.
- The jumper is small: the placeholder is about 260 px tall, so the arch will span about 130 px on the phone sheet.
- The cast's flop pose is a shallow ∧ with the hips touching the bar, not a clear ∩ bridge with daylight between hips and bar.
- Compare shots 4 and 25: there the bar sits against clean SKY and would read immediately. Use that idea for the side view.

## Standards and poles

**Yes, they hurt.** They are square-section, dark navy or purple, roughly twice real thickness, with pegs the size of ladder rungs, and
the camera sits ~1 m from them, so they become 100-150 px walls (26 and 28 at left, 27 and 30 at right, 18, 20 and 32 at the edge). On a
phone they read as a black bar down the frame and squeeze the action into ~70 % of the width. Shot 31's "flag" FG is a bare 180 px
purple column with no flag visible. In 17 the flag reads as a dark wall. Shot 4's near-black diagonal post covers about a third of the
hook's key frame. The board's sb3 has the right standard: thin, round, silver-grey, lit, and in the picture rather than blocking it.

## Changes, ordered by impact

1. **BLOCKING: reframe the reveal side views 26, 27, 29 (and 28 as the matching contrast)** in `set15_shots.py`.
   - Lower the camera ~0.6-0.8 m below bar height, move it 25-35 % closer and tilt up 8-12°, so the bar and arch sit against the
     upper stand, roof band or sky instead of the confetti mid-band. The jumper's arch should span ≥ 55 % of the frame width.
   - Keep both standards inside the frame: thin, near the left and right thirds.
   - TENSE preset: drop crowd albedo/emission ~40 % and add a hard floodlight pool on the bar and jumper, so a lit figure reads
     against a dark mass. The plan already asks for "crowd dimmed".
   - Darken or tint the mat top in these shots so the white vest and the hanging head and legs separate from it.
   - Check on a 360x640 downscale: the hips must be above the bar and the head and legs below it, both readable.
2. **BLOCKING: thin and relight the standards, and pull them off the lens** in `set15_props.py` and the cameras in `set15_shots.py`.
   - Round tube about 0.05 m (not a square post), lit silver-grey metal as in board sb3, pegs ~⅓ of their current size.
   - Where a standard is the FG prop (17, 18, 20, 26, 28, 30, 32), keep it ≤ 50 px wide at the frame edge, or swap the FG for a
     lower, lighter prop (crossbar end on the ground, towel, spike bag, cone).
   - Shot 31: replace the bare pole with a visible waving flag cloth, or drop it.
   - Shot 4: rotate or offset the camera so the post is a thin sliver at the left edge (≤ 10 % width, lit side toward the camera).
     Keep the bar against the sky, which is the strongest hook idea.
3. **BLOCKING: put the bar and pit in frame where the action needs them**, in `set15_shots.py`.
   - Shot 3 (curved approach, back to the bar): pan target or camera so pit, standards and bar are in the right half.
   - Shot 35 (coach runs the curve and flops): same fix, and do not repeat shot 3's framing exactly; use the opposite side or a lower
     angle.
   - Shot 21 (attempt 1, the bar falls): the bar and standards are missing, so add them. Also cut the big empty orange track area by
     tilting up and moving closer.
4. **BLOCKING: remove the blank foreground slabs** in `set15_shots.py`. These are the mat top or edge filling 35-50 % of the frame in 21, 22
   and 33, and the grey standard-top slab in 24. Lower or raise the camera so the mat edge is a narrow band at the bottom (≤ 15 %), or
   give the mat texture: seams, a cover cloth, a towel or spikes on it. In 33 also cut the DAY exposure about ⅓ stop and make the sky
   bluer so the white mat does not merge with it.
5. **BLOCKING: deepen the flop pose in cast15** (`flop`, `flop_back`, `flop_head`, `flop_flick` for dick and rival1).
   - Bend the torso into a real bridge (two-segment curve).
   - Raise the hips 0.12-0.15 D above the bar line so there is a visible gap, and hang the head lower.
   - This is the image the whole film turns on ("like a fish"), so it must be a clear ∩ in silhouette.
6. **NICE (close to blocking for the ending): rebuild the sawdust heap for 34 and 36** in `set15_props.py`.
   - Put it IN the wooden pit frame, not on the grass.
   - Use a smoother, subdivided mound in warm sawdust colour with chip and grain texture and loose chips around it.
   - Replace the FG faceted dome in 36 with scattered chips or the pit's wooden edge.
   - Make sure the coach_buried card's own 2D mound and the 3D heap line up, and do not draw two mounds.
7. **NICE: densify the A-set mid-ground and lift shot 5 into a real establishing crane.**
   - Shots 3, 5, 35: fewer metres of bare grass and sky. Add spectators on the bleachers, a coach's bench with bags, a rake, a
     wheelbarrow, hurdles stacked by the fence, and a scoreboard or flagpole without letters.
   - Shot 5 is meant to be "high wide": raise it so the pines no longer block the pit and bleachers, and the whole 1963 venue reads in
     one picture as in board sb1.
8. **NICE: tame the EVE track** in 17, 20, 21, 31 and 32. Lower saturation ~15 % toward brick red, as in board sb2, so the orange field does
   not outshine the actors. Add a few lane marks or chalk to break up the flat areas.

After fixes 1-5, re-render the start framings of 3, 4, 17, 18, 20-22, 24, 26-33, 35, 36. Rebuild the contact sheet and the 360x640
phone sheet, and send them back to QA-art before the client sees them.
