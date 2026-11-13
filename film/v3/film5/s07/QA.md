# s07 QA: film 5, shot 7 (plan t 17.63-23.03, g 529..690), mine set (tunnel LAMP)

Delivered: `take.mkv` = frames g 522..697 (176 frames, 720x1280, 12 samples, 2 threads, denoise FAST), first_g 522.
g 522..528 in-handle, g 691..697 out-handle (rendered in 3D, cameras keep moving). Also `meta.json`, `cues.json` (9 cues), `contact.jpg`,
`compare.jpg`, `work/qa.txt`. Scripts: `shot.py`, `lib5.py`, `deliver5.py`.

## Client rules
- No depth of field anywhere, no motion streaks.
- Alfie's cage = the cast's 2D held cage (prop_r / prop_l "cage" + pose key "bird"), bird drawn on its perch behind the bars; the set's
  3D cage hidden.

## Mouths (quoted line)
The quote "เอานกมาร้องเพลงกล่อมพวกข้าเหรอ ไอ้หนู ตะเกียงข้ายังสว่างอยู่เลย" = 18.59-23.0 s = g 561..693. The gaffer's mouth moves only
inside it: a new drawing every 2 frames from the narration loudness (`lib5.lip`: quiet = held laughing grin, low = talk_a, loud = talk_b,
every third loud pair talk_o). Before g 561 he laughs with a held grin (no lip motion; "หัวหน้าหัวเราะ" is narration). The miners in 7d keep
static closed laughing grins (the quote is the gaffer's). Alfie's mouth never moves.

## Timing
| sub | g | what | ref a |
|---|---|---|---|
| 7a | 522-570 | two-shot eye level: gaffer near screen-right, alfie small and far screen-left with the cage; the gaffer bursts out laughing on "หัวเราะ" (g 541-547), the quote starts g 561; alfie's smile drops to worried; slow push | t0013 |
| 7b | 571-607 (cut) | closer, a little low on the gaffer laughing and talking (tears, lamp at his side) | t0015 |
| 7c | 608-644 (cut) | low side two-shot: the gaffer looms and leans down toward little alfie on "ไอ้หนู" (g 618-628), lifts his lamp on "ตะเกียงข้า" (g 634-642); alfie hugs the cage, worried, sweat | t0011 |
| 7d | 645-697 (cut at plan t 21.5) | miner1 / miner2 / miner3 laughing and pointing (tears), slow push | t0047 |
Framing changes g 529, 571, 608, 645, out 691: 1.40, 1.23, 1.23, 1.53 s.

## Staging (`work/qa.txt`)
| sub | head | width px | centre y (H) |
|---|---|---|---|
| 7a | gaffer / alfie | 219-256 / 107-115 | 0.38-0.41 / 0.53 |
| 7b | gaffer | 325-375 | 0.44-0.50 |
| 7c | gaffer / alfie | 244-260 / 163-168 | 0.34-0.38 / 0.61 |
| 7d | miner1 / miner2 / miner3 | 204-235 / 168-188 / 120-130 | 0.39-0.43 / 0.49-0.51 / 0.47-0.48 |
All heads above y 880. Lamps: the gaffer's held lamp (prop_tip_l), alfie's belt lamp, two miner lamps in 7d (keyed lamp_light).
Popcheck: pops only at the cuts 570/571, 607/608, 644/645. No static runs, no black / magenta frames, no retried frames.
Fixed once: the first final had a fast laugh shake (sin 1.7 rad/frame) that jerked the close-up head ~55 px per frame (pops at
g 552-640); 7a (from g 538), 7b, 7c re-rendered with a 7-frame shake cycle and smaller amplitude.

## Colour
```
set                                             red orange yellow  green   cyan   blue violet magent   sat  val dark
s07 shot 7a (g 522-570)                        13.4   17.7    0.6    0.0    0.0   44.6   16.7    6.8  0.37 0.42 0.06
s07 shot 7b (g 571-607)                        24.9   20.2    0.3    0.0    0.1   38.2    8.4    7.8  0.46 0.40 0.09
s07 shot 7c (g 608-644)                        17.4   14.8    0.0    0.0    0.0   47.5   10.2   10.1  0.40 0.40 0.07
s07 shot 7d (g 645-697)                         7.5    7.7    0.5    0.1    0.1   61.1   12.4   10.6  0.35 0.41 0.07
s07 all (g 522-697)                            15.6   15.1    0.4    0.0    0.1   47.9   12.1    8.7  0.39 0.41 0.07
```
Blue-dominant tunnel as in s01; magenta 7-11 comes from the tubs and the gaffer's ox-blood waistcoat, the shade stays blue.

## Seconds per frame
15.4 s wall / 29.7 s CPU mean (two processes x 2 threads).

## Differences from the plan
- 7c (gaffer leaning over alfie) is an extra framing to keep the 1.0-1.5 s rhythm over the 5.4 s shot; in 7c alfie holds the cage in his
  far (left) hand so the gaffer's coat never covers it.
- In 7d miner3 stands deepest and is partly behind miner2's shoulder.
