# T2 QA (film 15 v2, team 2) — g 489-862 (+6 handle frames each side: file g 483..868, 386 frames)
Location A (Medford 1963) HERO golden hour. Script `shot.py` (+ `grade.py`). `take.mkv` is split: `cat take.mkv.part* > take.mkv`.
Render: 720x1280, 12 samples, ~14 s/frame (2 processes x 2 threads, per-frame card rebuild).

## Numbers (take.mkv)
qa_auto PASS (blank-frame check fixed: flash white-out capped at 0.9). qa_stats2: sat 0.63, vivid 67.8 %, luma 101.5, warm 64 / cool 25 %, magenta 0.0 %.
motion_check (cut at 744 excluded): median 7.6, p90 18.7 (per section: g483 5.3 / g564 7.9 / g687 10.4 / g708 16.3 / g744 6.3 / g780 9.0 / g838 19.7).
Grade (grade.py): sat x1.15, shadows pulled to hue ~250 (only cool/green hues, reds keep hue), luma gain 1.05; page frames sat x1.30, gain 0.95.

## Angle types / frame ranges
- g483-564 over-the-shoulder push-in on the laughing coach (back-view Dick card in the left foreground, cast15 has no back view: his front sprite with the face painted over by hair + ears, `_back_post`); foreground Dick passes the lens (parallax).
- g564-687 side tracking along the bleacher front (coach: wag, broken-neck mime g565-621, point/jab; mouth moves only g534-706 = 17.80-23.55 s).
- g687-708 PUNCH CLOSE-UP 1 on the coach ("ดูเอง", ~22.9-23.6 s), slow creep so never static; coach head ~38 % of frame height (planned close-up).
- g708-744 whip/swing back and rise to a medium-wide of the pit from the run-up side: Dick runs the J-curve (g709-730), take-off, flop_rise/head/back, arch over the bar at g738 = 24.6 s with the photographer's FLASH (flash pose key 1->0 over 4 frames + set flash bulb).
- g738-751 push THROUGH the flash: white-out (cap 0.9) and the newspaper page arrives (hard change at g744, planned "cut" for qa_auto).
- g744-838 through-the-newspaper reveal: page fills the frame (25.0-26.0 s, slow pull + drift), pull back with an arc/crane to reveal reader on a bench, laughing coach + boys.
- g838-868 push INTO the newspaper photo (ease out to a slow creep, 0.375 m/s inward at g862).
BIGZOOM: none in T2. Close-ups: g687-708 only. Wide / medium-wide frames: g708-744 and g790-840 (about 25 %), the rest are medium (coach full body 25-35 %) and the page; page-only frames g744-790, 846-868 are short (<1.5 s each).

## SEAM to T3: exact final camera / newspaper framing at g 862 (T3 starts INSIDE this photo)
Texture: `v2_a.tex_newspaper()` (work_v2_a/tex/newspaper.png, 2400 x 3200 px, MEDFORD MAIL TRIBUNE, headline FOSBURY FLOPS OVER BAR, photo = `photo_flop` halftone).
World (set-local metres, set A, HERO): page centre (10.20, 4.20, 1.18), width 0.74 m, height 0.9867 m (texture aspect), faces -x (towards the field), roll -2 deg, bend 0.045 (bows toward the camera), mesh `world_page()` in shot.py (u runs along -y, v up).
Photo rectangle on the texture: x 110..1640, y 1450..2521 px (from the top) = UV u 0.046..0.683, v(from bottom) 0.212..0.547; photo centre u 0.365, v 0.38 = world (10.20, 4.30, 1.298).
Camera g862: loc (9.700, 4.300, 1.298) m, looks +x at (10.20, 4.30, 1.298) = photo centre, distance 0.500 m, lens 22 mm, 720x1280, no roll. At this distance the photo is ~100 % of the frame width (photo 0.472 m wide, frame 0.46 m), the headline sits at the top, the caption band just below the photo bottom.
Motion at g862: dolly in along +x, 0.0125 m/frame (0.375 m/s), no pan; handle frames g863-868 continue it (d 0.4875 ... 0.425 m). Frame files g_0862.png.. in the take (first_g 483). To reproduce exactly: `shot.py cam_for(862)` / `page_cam`.
Grade on page frames: gain 0.95, sat 1.30, no shadow shift (`grade.grade(a, 0.95, 1.30, 0.0)`); the page is emission, so the paper colour is ~ (0.93,0.84,0.62) tint of the texture.

## Known leftovers / differences from the plan
- The plan's "pull back to reveal the boys and coach" is in (g790-840), then the push into the photo (brief override: T2 ends pushing into the photo).
- Back-view Dick is a painted-over front sprite (hair disc); at the lens pass (g495-505) his head is large (~40 % of frame) but it is the back of the head, no face.
- The reader sits on a crate/bench behind the page (legs visible below the page, hat hidden); the crate is a plain red-wood block.
- Run-up Dick is only in view for ~1 s before the flash (g720-744), because the whip back to the pit costs 0.8 s.
- Coach pose in the quote is not mouth-synced to words (talk_mouth random), only restricted to the quote window.
- God rays turned off (build rays=False) to avoid the sky smudges; clutter in the OTS area removed from midA/folk meshes (`clean_set`).

## Round 2 (director TAKE gate FIX) — changes
1. Newspaper no longer floats: the page is now one world prop at every frame (g483-868): the reader sits on a riser behind it, two 3D hands grip the side edges (thumbs in front), sleeves run back to the reader, and a fedora brim + eyes show above the top edge (card scale 1.12). Same prop in the background at g540-640 and g790-850.
2. Whip: shortened to g709-716 (CU creep knot 709, mid knot 712, pit wide from 716) with a 5-sub-frame directional blur on g710-715 (qa_auto lists these as soft = intended). It now lands on the pit wide, no empty lawn / bin.
3. Press photographer with flash camera stands at the pit edge (0.5, 2.6 m) in the wide, g716-744; the flash bulb fires from his gun at g738.
4. The MEXICO 68 poster on the Medford wall is hidden (hide_render) for the whole take.
Page framing (g856-868) is unchanged: same page, same camera path (g862 diff vs round 1: mean 2 / 255, g868 0.7; g856 differs only by the new hat/hands at the frame edge).
Numbers after round 2: qa_auto PASS, sat 0.63, vivid 66.7 %, luma 101.2, magenta 0 %; motion median 7.1, p90 19.4.

## EXACT END FRAMING at g862 in pixels (720x1280 frame, 22 mm lens = 782.2 px focal length, camera 0.500 m from the page, axis perpendicular to the page, roll -2 deg page tilt)
- Photo (halftone, black frame line) spans x about -9..729 (it just overflows both sides, 0.472 m wide = 738 px), y about 382..898 (0.330 m = 516 px), centred on (360, 640). Dick's arched figure sits at the photo centre area.
- Headline: line 1 "FOSBURY FLOPS" is cut by the top edge (y -9..165); line 2 "OVER BAR" fully in frame, y about 172..343, letters ~170 px tall, left edge x about -20 (the O is clipped slightly), the page shows the whole headline width ~1530 px at this scale (about 2x the frame width), i.e. only the left part "OVER B" is visible.
- Below the photo: caption line at y about 920-950; column text below that.
- Scale rule for T3: the frame shows 0.46 m x 0.82 m of page = 1493 x 2655 texture px (page texture 2400 x 3200), centred on texture px (876, 1985) measured from the top-left (u 0.365, v 0.38 from the bottom). 1 frame px = 2.07 texture px.
- Velocity: still dollying in at 0.0125 m/frame (0.375 m/s).

## Round 3
The reader's hands are now skin-coloured (not bunting orange) and are hidden from g852 on (they would sit inside the photo crop; T3 has no hands). Page and camera framing g856-868 unchanged (the end framing section above still holds exactly). Re-rendered g520-707 and g744-868 (g708-743 unchanged). qa_auto PASS; numbers as round 2.
