# Film 16 TAKE gate round 4 (re-check after fixes): QA-tech and QA-art combined
Takes: s17 and s18 from render16/team5 @05364b7; s30 from render16/team8 @0130eb5 (all three are one take.mkv, not split).
Method: I decoded every take to full-res PNG one at a time. I checked 6 fps sheets at 180x320 (the phone size is 360x640) with the y 880 line drawn, plus every cut ±3 frames. I made full-size frames and crops of the props, hands, faces and caption band. I ran film/qa_auto.py on each take and recomputed the frame-diff myself (90x160 grey, in-shot pairs).
Lip-sync window for s18: 38.46-40.80 s + 0.10 s clock = g 1157-1227 (±0.15 s).
Earlier reports: qa/TAKE_ART_r2.md (s17, s18, s30) and qa/TAKE_r3.md (s30).

| take | qa_auto | diff median / p90 (min, max) | heads y<880 | verdict |
|---|---|---|---|---|
| s17 | PASS | 8.03 / 13.88 (3.48, 19.8) | yes (bottom <= ~724) | **FIX (blocking)** |
| s18 | PASS | 6.09 / 14.38 (3.34, 20.8) | **NO**: Morse and worker b, about g 1160-1200 | **FIX (blocking)** |
| s30 | PASS | 5.56 / 14.24 (1.71, 27.5) | yes (<= 849) | **PASS (notes)** |

All three meet median >= 4 and p90 >= 12. I found no frozen run, no black, blank or magenta frames, no DOF, and no text in the picture. qa_auto's "planned cuts with no visible change" is expected, because the handles are continuous. In s30 the single in-shot diffs below 2 (g 2074, 2077, 2081) are isolated, not a parked run.

## s17: empty money bag (FIX, blocking)
Earlier issues (TAKE_ART_r2 s17):
1. A visibly EMPTY money bag, mouth down, shaken at chest height in the centre, with dust and a moth, and the side "ears" gone: **PARTLY FIXED, still BLOCKING**. The ears are gone and the bag is at chest height near the centre. Two dust puffs come out (g 1085, 1110), and a grey moth flutters down (g 1095-1122). It reads as a moth at full size and as a small grey "bow" on the phone. But the prop still does not read as a money bag:
   - The tied "bottom corner" is at the TOP, drawn as a round opening, so the sack reads as a vase or bell with its mouth UP. The real mouth at the bottom is a dark rim with a big white oval lining with a slit, which on the phone reads as an egg, coffee bean or bell clapper (see full_1080, 1098, 1112).
   - Nobody holds it. You cannot see Morse's hand on the sack in any frame, so it floats beside his right shoulder. This breaks "props held".
2. Morse's gaze INTO the bag, hopeful then slumped, with the bag fully in frame: **PARTLY FIXED**. The bag is fully in frame and his face goes from worried to sad and droopy after the g 1091 blink (reads well). His eyes, however, look at the lens or slightly screen-left, not down at the bag. The head pitch is too small to read.
3. Workers slump: **PARTLY FIXED (note)**. The squash and lean are small on the phone. Worker a (plaid) is hidden behind Morse from about g 1090 to the end. Worker b (straw hat) still has his forearms crossed over the shovel, so he still reads as arms-crossed.

Phone read: "Morse is sad next to a cream vase, and something white and a moth fall out". It does not read as "the money bag is empty".
Fix (blocking):
- (a) Put Morse's hand visibly on the tied corner, with fist and cuff touching the sack top (or two hands, one shaking).
- (b) Close the top: draw a twisted, tied neck with a string, not a round hole. Make the bottom mouth a limp, gaping, puckered opening. Make the lining a small crumpled flap, not a big flat oval. Better still, a coin-less bag with a "$"-free drawstring silhouette that matches the s12 bag's shape.
- (c) Pitch his head down 15-20 deg and turn his pupils to the bag mouth for the first shake.

Note: bring worker a out from behind Morse (slide him 0.4 D screen-left) and give worker b hands on the shovel top instead of crossed forearms.

## s18: mocker's taunt from the buggy (FIX, blocking)
Earlier issues (TAKE_ART_r2 s18):
1. The buggy should read, with the camera outside the buggy side, a wheel and textured panel in the FG, and the mocker seated: **PARTLY FIXED**. The opening (g 1119-1140) is good: a blue wagon with two big red-rimmed spoked wheels and a plank-grain side panel, and the mocker above it. It clearly reads as a cart or buggy. But from about g 1159, a large flat MINT-GREEN untextured slab enters the lower left (it is 25-30 % of the frame at g 1185-1206). His grey trouser legs are in a walking stride over the side (g 1185-1225). He does not read as seated.
2. A target for the point (the furrow, poles or Morse's group on the side he points to), and his head turned toward it on "ใต้ดินแล้ว": **PARTLY FIXED, with a new BLOCKING issue**. Morse (with the coil) and the two workers now stand on screen-right behind him, and the mocker's right hand hangs toward them (good staging). However:
   - **BLOCKING (caption band):** from about g 1160 to 1200 the group's heads sit ON the y 880 line. Morse's face (mouth and chin) and worker b's moustache are below 880 (see band_crops.jpg g 1165/1180/1195/1200, and meta g_morse head y up to 955, bottom 1058). The caption will cover the target of the taunt.
   - The "point" is a small dark fist hanging at hip height, with no index finger extended. His eyes are shut laughing and his face stays on the lens. The head turn at g 1201-1209 does not read, and the snap at g 1204-1216 pans AWAY from the group. You cannot see the furrow itself.
3. Opening wide: **FIXED**. The mocker is near the centre at about 117 px, with clear air round him. The mule is not visible in the opening on my frames (only the wagon), which is acceptable.

Lip-sync: the mouth is closed and smug until g 1153, the laugh pose starts at g 1154, and the talk shapes alternate from g 1157 to the cut at g 1226. This is inside the window. Tears and the belly bounce read. The cut at g 1226 is clean.
Phone read: "a laughing fat man on a cart, and sad Morse and workers behind him". This is close, but the taunt has no aim and the group is half under the caption.
Fix (blocking):
- (a) Raise the group so the heads sit at y <= 800 (bottom < 880). Do this by dropping the camera 0.2-0.3 D or tilting it 2-3 deg down, or by moving the group 0.5 D further back and up the bank. Keep Morse fully in frame and do not let him clip at the right edge after g 1180.
- (b) Give the point a real index finger aimed at the group on "ลวดของเอ็ง" (g 1170-1185) and turn his head and eyes toward them before the snap. Then keep the group's edge in the snap's end framing, or snap toward the group rather than away.
- (c) Texture the mint slab (plank grain like the panel) or darken it to the panel blue. Hide the walking legs: seat him, or cut the frame above the knees with the panel.

## s30: ENDING (PASS, notes)
Earlier issues:
- TAKE_r3 BLOCKING, Morse half hidden behind the jamb at the frame edge: **FIXED**. He stands in the lit opening, beside the door frame. His face measures 65-75 px wide at 720 over g 2065-2095 (about 33-37 px on the phone, head y 597-672), at x 77-158, clear of the left frame edge. Only his right cheek edge touches the jamb in the last frames. Both eyes and the toothy grin read, backlit by the warm doorway. The grin pop (blink at g 2084, laughing squint from g 2085) makes him the last motion the eye finds. The hard cut on "เอง" at g 2096 is kept and clean.
- TAKE_ART_r2 #1, register at his elbow, one ribbon and dot-dash heap: **FIXED** (it stays from r3). In g 1980-2030 the walnut instrument with post, lever and coil sits at his right elbow, and the dot-dash ribbon runs from it into the curled heap at his boots. The candle is a brass chamberstick in his hand at the table edge (g 2085-2092 crop).
- TAKE_ART_r2 #2, night contrast: **FIXED** (walls dark, windows deep blue, warm candle and door pools).
- TAKE_ART_r2 #3, Morse bigger and in the door: **FIXED**, as above.
- Yawn, Z and nods are planned (no lip-sync, mouths OK). Heads are above 880 (lowest bottom 849, in the close).

Phone read: YES. "He sits up all night by candlelight, yawning in a heap of telegraph paper, and Morse grins at him from the door." I find it funny and clear.
Notes (non-blocking):
1. In the final wide (g 2070-2095) the camera's leftward move pushes the instrument itself off the right edge. Only the table edge, the ribbon and the candle remain, so "the register at his elbow" is established only in the first 1.5 s. If anything is re-rendered, ease the final pose 0.1-0.15 D right so the lever and post stay at x <= 690. I could not see the 9-frame click in the end wide (the instrument is out of frame).
2. The ceiling is still the largest evenly lit grey-beige area (top 30-35 %) in the wide. It could go about 20 % darker.
3. The red rectangle on his vest (the cast16 sash mail bag) reads as a dark red pocket patch. It is prominent only in the close (g 2035-2060), and it does not hurt the reading. Accept it.
4. The snaps at g 2024-2038 (diff peak 27.5) and g 2056-2070 are eased, not pops.

## Summary
- s17 FIX (blocking): the bag still reads as a cream vase with an open top and an egg-like lining, it floats with no hand on it, and Morse looks at the lens, not into it. The dust and moth are good.
- s18 FIX (blocking): Morse's group is now the target, but their heads sit in the caption band from g 1160 to 1200. The point is a hanging fist, and the snap pans away from them. A mint untextured slab and walking legs remain. The buggy wheels and panel, the opening wide and the lip-sync are fixed.
- s30 PASS: Morse's face is 65-75 px, clear of the jamb and edge, with a grin pop, and the hard cut is clean. Notes: the instrument is cropped in the final wide, the ceiling is still bright, and the vest patch is accepted.
Sheets and crops: /tmp/claude-0/-home-user-github-commit-quest-v2/d013e474-c7c9-591e-b74b-eccded3d274b/scratchpad/qa16/r4/<take>/ (p6_*.jpg, cut_*.jpg, full_*.jpg, band_crops.jpg, morse_crops.jpg, reg_*.jpg, QA_AUTO.md). Frames and worktrees are deleted, and the repo is untouched (film16/main).
