# s01 QA: film 6b, shots 1-3 (the hook), bakery MORNING

Delivered: `take.mkv` (libx264rgb crf 6, 30 fps, 129 frames g 0..128, **first_g 0**, 45.4 MB -> also split as `take.mkv.partaa` +
`take.mkv.partab` per WORKER6B; rejoin with `cat take.mkv.part* > take.mkv`; take.mkv itself is not committed, only the parts),
`meta.json` (g0 0, g1 123, first_g 0, n_frames 129, transition_in cut), `cues.json` (13 cues), `contact.jpg`, `compare.jpg`
(g 40 beside ref a t0001; g 100 beside ref a t0046), `shot.py`, `take_cfg.py`, `deliver.py`, `qa.py` (-> work/qa.txt), `lib6b.py`
(Thai sign / steam puff / pale loaf / cool light helpers), `sheet.py`. Raw renders: raw/s1..s3 (not in git).
Shot boundaries: shot 1 g 0-47, shot 2 g 48-71, shot 3 g 72-122 (plan 0.00 / 1.60 / 2.40 / 4.10 s). Out-handle g 123..128 (3D: push + grin
continue). No in-handle (film start).

## What is on screen (word-literal)
| g | picture | caption |
|---|---|---|
| 0-47 | CU kit behind the counter, push in (head 302 -> 375 px = 42-52 % W): deadpan, sneaky glance screen-left (6-16) and right (18-28); the pale 13th loaf comes up on his palm (26-32); smirk (38) | "เด็กคนนี้แอบ" / "ยัดขนมปัง" |
| 48-71 | ECU basket of 12 on the counter, kit smirking behind it (head 342-397 px): his hand holds the pale loaf over the pile, lets go (53), it lands on the very top (56) with a squash and a white steam puff (56-71) | "ก้อนที่สิบสาม" |
| 72-122 | from the street: Thai shop sign "ร้านลุงเฮนรี่" over the counter; the customer (woman1) holds the basket of 13, walks off screen-left (84-112); camera pushes onto kit, who turns to the lens and WINKS (98-104) then grins | "ลงตะกร้า ลูกค้า ทุกครั้ง" |

## Rules
- No depth of field (camera dof off + B.setup_dof(None) before every render). Everything sharp. No motion streaks.
- Mouths: no quote in s01 -> static expression mouths only (neutral / smirk / wink / grinning).
- Heads above y 880: kit always (centre 0.29-0.44 H). **Exception: the customer's head bottom dips below 880 on g 86-94 (9 frames)** while she
  walks out of frame screen-left (head centre 0.58-0.62 H, half out of frame); the caption band touches her chin there. Not re-rendered.
- Thai sign: Kanit Black via Chromium (font embedded as data URI, proper Thai mark stacking), ink outline, card over the painted fascia.
- Cool counter-colour: one blue area light (L_cool_window, 2500 W, colour (0.12, 0.30, 1.0)) aimed at the back wall / right of the shop:
  blue-grey stone and shelves on the right against the orange oven on the left. Blue 6.9 % (set was 0.5-0.8 %).
- Popcheck: no pops outside the planned cuts (g 48, 72); no near-still frames; no black / magenta frames; no retried frames.

## Numbers (work/qa.txt)
```
shot 1: kit head w 302..375 px (42..52 % W), centre y 0.44 H
shot 2: kit head w 342..397 px (48..55 % W), centre y 0.29..0.34 H
shot 3: kit head w 127..253 px (push), woman 255..385 px
set                     red orange yellow green cyan blue violet magent  sat  val dark
s01 all                29.8  51.6   1.5   1.3  0.5  6.9   2.0    6.3  0.40 0.61 0.05
refs of compare.jpg    31.1  42.1   4.5   0.3  0.0 10.6   5.3    6.0  0.33 0.48 0.10
```
Still warmer / lighter than ref A (set look, bakery_API 7); the blue counter-colour is now present. Mean 17.8 s wall / 33.4 s CPU per frame
(2 processes x 2 threads).

## Differs from the plan
- Shot 3: the customer walks off screen-left on the street (out of frame) rather than through the half-door (the half-door is not in the
  street-side framing that also holds kit's wink).
- Shot 1: the 13th loaf in kit's hand is the cast prop loaf (normal colour); the pale loaf card is used in shot 2 where it lands.
