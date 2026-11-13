# s08 QA: film 5, shot 8 (the nickname "ไอ้เด็กเลี้ยงนก"), mine set tunnel LAMP

Delivered: `take.mkv` = `frames/g_0683.png .. g_0764.png` (82 frames, 720x1280, 12 samples, 2 threads, no captions, no audio).
g 691..756 = shot 8 ([g0, g1) = [691, 757)); g 683..690 = in-handle, g 757..764 = out-handle (both rendered in 3D, the cameras keep moving).
Also `meta.json` (first_g 683, n_frames 82), `cues.json`, `contact.jpg`, `compare.jpg` (8a / 8b vs ref a t0047). Scripts: `shot.py`,
`tk.py` (take toolkit, shared by s08/s09/s11), `deliver.py` + `tk_deliver.py` (frames, meta, cues, sheets, mkv, `work/qa.txt`).

## Client rules
- No depth of field: `M.setup_dof(scene, None, None, cam=...)` at build and before every render. No motion blur. Everything is sharp.
- Alfie holds the cage, so this shot uses the cast's 2D held cage (prop `cage` + pose key `bird`, bars drawn over the bird). The set's 3D cage is hidden.
  The bird is visibly inside the bars in 8a (small, behind the miners' arms, beside alfie) and in 8b (held in front of his waistcoat, singing 3 notes).

## Timing
| seg | g | what | ref a |
|---|---|---|---|
| 8a | 683-728 (handle 683-690) | eye level looking inbye: miner2 (front right), miner1, miner3 (partly hidden) laugh and point screen-left at alfie, who stands small in the depth with the cage, sad; slow push + drift | t0047 |
| 8b | 729-764 (cut, handle 757-764) | cut on "ไอ้เด็ก" (24.25 s = g 730): the reverse, looking outbye; alfie in the foreground, hurt (sad, head lowering), the cage held in front of him, the bird singing 3 notes; the miners behind still laugh and point at him; slow push | t0047 |
Framing changes: g 691 (in), 729 (1.27 s). The camera moves in every frame (no near-still transitions).

## Staging (`work/qa.txt`)
| seg | head | width px | centre x | centre y (H) |
|---|---|---|---|---|
| 8a | miner2 / miner1 / miner3 | 218-255 / 167-188 / 122-133 | 620-724 / 396-452 / 460-510 | 0.43-0.46 / 0.38-0.41 / 0.41-0.43 |
| 8a | alfie (far) | 97-103 | 264-274 | 0.50 |
| 8b | alfie | 324-378 | 484 | 0.47-0.48 |
| 8b | miner1 / miner2 / miner3 | 131-139 / 109-114 / 180-194 | 250-274 / 177-203 / 34-84 | 0.35-0.47 |
All heads are above y 880. Mouths: the miners' laughing grins and alfie's sad wavy mouth are static drawings, so no mouth moves (this shot has no quoted line).
Laughter is animated with a body bounce, head roll, squash and the pointing hand. Nobody has their back to the camera.
Popcheck: one pop at the cut 728 -> 729. No black or magenta frames, no retried frames, no clipped sprites.

## Colour (hue_report rows)
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s08 8a (g 683-728)                             18.9   18.4    0.4    0.1    0.1   41.4   11.2    9.6  0.32 0.45 0.05
s08 8b (g 729-764)                             18.4   15.6    0.8    0.3    0.0   43.0   11.3   10.5  0.33 0.46 0.09
s08 all (g 683-764)                            18.6   17.2    0.5    0.2    0.1   42.1   11.2   10.0  0.32 0.45 0.06
ref a t0047                                    33.9   48.0    5.6    0.4    0.0    0.5    7.4    4.3  0.37 0.45 0.16
```
Blue dominates by the set's design (the LAMP night look; s01's tunnel shots read red 11 / blue 38-72). Shade reads blue-violet. Magenta is 10, which is the top of the band.

## Seconds per frame
15.2 s wall / 29.5 s CPU mean (2 threads, another render process running alongside). 8a: 31.2 CPU s (four actors + three keyed lamps), 8b: 27.4.

## Differences from the plan / known issues
- The plan has one `tunnel_eye` setup. I split it into 8a and 8b (reverse) for the 1.0-1.5 s rhythm. Both cameras are custom, at eye level.
- In 8a miner3 is mostly hidden behind miner1 and miner2. Only his cap and part of his face show.
- In 8b a coal tub frames the left edge in the foreground.
