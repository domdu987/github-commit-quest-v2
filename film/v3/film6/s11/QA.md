# s11 QA: film 6, shot 11 (quote 1: "เอ็งจะแจกขนมปังฟรีให้ข้าเจ๊งเหรอ ก้อนของข้าชั่งมาเป๊ะแล้ว"), bakery MORNING, counter

Delivered: `frames/g_0784.png .. g_0938.png` (155 frames, 720x1280, 12 samples, 2 threads, denoise FAST, no captions / audio) and
`take.mkv` (libx264rgb crf 6, 30 fps, first_g 784). g 790..932 = shot 11 ([g0, g1) = [790, 933), plan 26.32-31.09 s); g 784..789 in-handle,
g 933..938 out-handle, both rendered in 3D. Also `meta.json`, `cues.json`, `contact.jpg` (16 frames), `compare.jpg`.
Scripts: `shot.py` (probe / stills / final), `deliver.py` + `deliver_cfg.json`, `qa.py` (-> `work/qa.txt`), `sheet.py`; helpers `../common.py`.

## Framings (a change every 1.0-2.0 s)
| g | framing | action |
|---|---|---|
| 784-825 (1.4 s) | F1 two-shot over the counter from the street, slow push | kit (left, hidden stool) smirks over the basket of 13 (pale 13th on top); henry (right, by his balance) turns g 792-802, double-take (shocked g 798-805), goes furious, steam from the ears from g 800, points at the 13th loaf from g 812 |
| 826-857 (1.1 s) | F2 tighter, slightly low two-shot | henry yells (lip-sync from g 825), finger jabbing at the basket; kit shrinks g 828-838 (scale 1.0 -> 0.88, sinks 0.18 D behind the counter, worried + sweat) |
| 858-887 (1.0 s) | F3 low-angle punch-in on henry | still yelling and pointing (kit's head leaves frame left, only his basket shows) |
| 888-938 (1.7 s) | F4 cut (plan 29.5 s + 0.1 = g 888) to henry right behind his hand balance | he taps the beam with a fat finger at g 896 / 907 / 918 / 929 ("ก้อนของข้า ชั่งมาเป๊ะแล้ว"); the beam does a small damped wobble after each tap and settles level |

## Client rules
- **No depth of field**: `common.Take` (DOF off at build and before every render). Sharp throughout. In F4 the opening's hanging herb
  bundles (`opening_bundles`) came within ~1 D of the camera, where their painted texture magnifies into a soft smear that reads as blur:
  they are hidden (keyed `hide_render`) in F4 only.
- **Mouths only on the quote**: henry lip-syncs (`cast6.talk_mouth`, a new drawing every 2 frames) only g 825..935 (captions 27.41-31.06 s).
  Before g 825 the narration "ลุงเห็นก็โวยลั่นร้าน" is not a quote: henry's mouth is the static mouth of each expression (unimpressed -> shocked
  -> furious). kit never speaks.
- **Heads above the caption band**: see the table. The only head whose bottom passes y 880 is kit's in F3 (g 858-867), and that head is
  centred at x -116 (only a sliver of cap at the frame edge).
- **No magenta**: henry_yell's `anger_fill` effect was dropped: its red-violet wash read magenta on his face in the drafts; the anger is the
  furious drawing + ear steam.

## Staging (`work/qa.txt`)
| framing | actor | head width px | centre x | centre y (H) |
|---|---|---|---|---|
| F1 | kit / henry | 190-201 / 174-184 | 143-170 / 508-516 | 0.47-0.48 / 0.46 |
| F2 | kit / henry | 201-222 / 202-209 | 120-131 / 533-539 | 0.51-0.58 / 0.50 |
| F3 | henry | 237-247 | 385 | 0.54 |
| F4 | henry | 289-305 | 352 | 0.42 |
Kit stands on a hidden stool (feet z 0.80), henry on a hidden step (z 0.40) behind the counter so heads are level for the two-shot; the
customer's basket of 13 (`cast6.basket_svg(loaves=13)`) on a `common.PropCard` x1.3 on the counter between them. Henry's pointing arm is a
local "point" hand on the `top` layer (a world pin above the basket made the arm point upward; at hand targets inside his wide body the
default layer drew the arm behind the torso). The tap is a world pin of the screen-left hand onto the beam just left of the pivot.

## Pops / checks
Popcheck: one jump outside the cuts, g 805 -> 806 (7.1 levels): kit's caught reaction (smirk -> worried pose, hands up) and henry's
shocked -> furious switch on the same frame (deliberate snap). Cuts at g 826 / 858 / 888 (45-55 levels). No near-still pairs, no black /
magenta frames, no clipped sprites, no retried frames.

## Colour (`hue_report.row`, final frames)
See `work/qa.txt`. Warm interior as the set measures it (bakery_API 7): red / orange high, blue ~0.4 vs 7 in ref A, dark 0.07. Same
set look as s01; not graded per take.

## Seconds per frame
21.4 s wall / 37.3 s CPU per frame mean (two 2-thread processes on 4 cores, denoise FAST, 12 samples; kit sprite 448 px/D, henry 384 px/D).

## Differences from the plan
- The plan's "two-shot" is split into three framings (two-shot -> tighter two-shot -> low punch-in) to keep a framing change every 1-2 s.
- "points at the 13th loaf": he points at the basket of 13 (the pale 13th sits on top) from the side; the finger is ~0.3 D above / right of the
  loaf, not touching it.
- "kit shrinks": a comic squash (scale 0.88) + sinking behind the counter + the worried drawing.
- Henry's position changes at the F4 cut (from (1.80, 1.95) to (2.05, 1.45), right behind the balance).
