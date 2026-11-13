# s07 QA: film 7, shots 7-9 (hero + nickname): louvre Salon Carré

Delivered: `frames/g_0593.png .. g_0925.png` (333 frames, 720x1280, 12 samples, 2 threads, denoise FAST, no captions, no audio) and
`take.mkv` (libx264rgb crf 6, 30 fps, **first_g 593, 333 frames**). Plan range 19.96-30.66 s = g 599..919; in-handle g 593-598 and
out-handle g 920-925 rendered in 3D (the action and camera moves continue). `meta.json` (first_g, n_frames, transition_in "cut",
transition_out "dissolve", set-ups, events, frame_source), `cues.json` (sound cues, film seconds), `contact.jpg` (16 frames, cyan line = y 880),
`compare.jpg` (g 640 / ref a t0001, g 870 and g 905 / ref a t0046 "they laughed"). Scripts: `shot.py` (stills / probe / final), `deliver.py`
(frames, meta, cues, sheets, mkv, `work/qa.txt`). One location (gallery_wide build) in two 2-thread processes.

## Set-ups (a framing change every 1.4-1.9 s)
| id | g | shot | what | caption |
|---|---|---|---|---|
| 1 | 593-648 | 7 | medium, slow push: vincenzo (normal clothes) on a step-stool beside her, carries a big glass pane from in front of him toward her frame, both hands pinned on its edge | "ส่วนเขาคือ วินเชนโซ ช่างกระจกชาวอิตาลี" |
| 2 | 649-695 | 7 | ECU insert: the pane slides the last 0.5 D and seats flush on the gilt frame at g 684, the glint streaks sweep across her face | "ที่เคยมาติด" |
| 3 | 696-740 | 8 | wide across the salon: three glaziers walk screen-right carrying panes (tall coworker1 leading, small vincenzo, stout coworker2) | "กระจกกันภาพให้ลูฟวร์" |
| 4 | 741-781 | 8 | tracking two-shot: vincenzo small next to tall coworker1, glances up at him (g 745-772) | "รวมถึงภาพนี้ด้วย" |
| 5 | 782-835 | 9 | three-shot (18 mm): panes leaned by the divan, the two laugh and point at him; he looks, then shrinks (vincenzo_mocked from g 815) | "เพื่อนร่วมงานชาวฝรั่งเศส ชอบล้อเขา" |
| 6 | 836-882 | 9 | low two-shot of the coworkers: laughing, then the jeer **lip-synced g 859-880** (coworkers_point, `talk_mouth` hold 2) | "เรียกเขาว่า ไอ้มักกะโรนี" (28.53 s = g 859) |
| 7 | 883-925 | 9 | close, slow push: vincenzo mocked (head down, blush) -> the hurt side-glare at them g 890-896 (sad -> angry behind the blink at 891), fists, a tremble; handle 920-925 | "เขาเจ็บใจเงียบ ๆ มาตลอด" |

## Client rules
- **No depth of field**: Take sets `dof.use_dof = False` + `L.setup_dof(scene, None, None, cam=cam)` at build and before every render. All sharp.
- **Mouths**: only coworker1 + coworker2 move their mouths, only g 859-880 = the narration's quoted "ไอ้มักกะโรนี" (caption 28.53-29.23 s, +0.10 s).
  The laughing before it (g 782-858) is a held laughing mouth (static `talk_b`), the bodies shake. Vincenzo never speaks.
  NOTE: the worker message said "lip-sync ~26.05-28.5"; the quoted word itself is spoken 28.53-29.23 s, so the sync sits on the word.
- **Heads above y 880 / centre 0.35-0.59 H**: every set-up passes (`work/qa.txt`): main heads 0.41-0.56 H, no head bottom below 880.
  Set-up 2 is an object insert (no head in frame; vincenzo's card hidden there).
- **Dense set**: the salon hang on every wall behind every set-up; runtime additions in `shot.py` only (the set module is untouched).

## Runtime set changes (shot.py)
- Her own glass box (`mona_glass`) hidden in shot 7 (he is fitting the glass now); a new pane object (louvre glass material + thin pale
  edges + two camera-only glint streaks) is keyed per frame and lands exactly on the frame front at g 684.
- The velvet rope + the stanchions at x 0.9 / 2.6 before her (2.3 D tall) crossed his face from every usable angle: those faces are split from
  `gallery_dressing` into `s07_rope_part`, hidden in shot 7 only ("unhooked for the work"), visible again in shots 8-9.
- A step-stool, the glazier's toolbox, putty tin and rag (shot 7); three carried panes with the walkers' hands pinned to their edges (shot 8);
  three panes leaned near the divan (shot 9).

## QA numbers (`work/qa.txt`)
Popcheck: the only jumps are the six planned cuts (649, 696, 741, 782, 836, 883); small 2-3 level blips at 784 / 829 / 831 are the laughing
shake. A stand-switch pop at 889 -> 890 found on the first final was fixed (squash lerp, no stance change; g 890-925 re-rendered).
Near-still pairs: 593 (handle) and 694 (pane seated, camera drift only) -- 1 frame each. No magenta / black frames, no retries.

## Colour
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s07 shot 7 (g 599-695)                         51.6   42.2    4.5    0.1    0.0    0.4    0.7    0.5  0.42 0.65 0.02
s07 shot 8 (g 696-781)                         47.8   44.0    2.6    0.4    0.0    3.4    0.4    1.4  0.42 0.60 0.03
s07 shot 9 (g 782-919)                         48.5   39.4    3.2    0.5    0.0    5.4    0.6    2.4  0.40 0.56 0.04
s07 all (g 593-925)                            49.7   41.4    3.4    0.3    0.0    3.1    0.6    1.5  0.41 0.60 0.04
ref a t0046 (they laughed)                     34.4   50.7    5.5    0.4    0.0    0.3    5.3    3.3  0.37 0.46 0.15
```
Warm red/orange of the red-damask salon in daylight (close to the ref interior t0046), saturation 0.41 in band, magenta 1.5, violet 0.6,
no magenta shade. Red is above the film band because the damask fills the frame; not graded here.

## Seconds per frame
11.08 s wall / 21.42 s CPU mean (12 samples, 2 threads, two processes at once on 4 cores). Sprites 240-400 px/D.

## Differences from the plan / known limits
- Shot 7's fitting is staged as "carrying the pane to her frame" (medium) + "it seats flush" (insert): a 2D card cannot reach across in front
  of the painting without his head covering the frame edge, so his hands are off-frame in the insert.
- Shot 8's "small among tall": coworker1 is 3.43 D tall vs his 2.90 at true scale; the two-shot shows the difference, coworker2 is about his height.
- Coworkers' wardrobe unchanged (blue overalls / blue blouse) -- they reappear in white smocks in s10's Monday shot.
