# s18 QA: film 9, shots 18-19 (the ending): wall_site two_sections_out + wall_top_battle, BATTLE

Delivered: `frames/g_1548.png .. g_1766.png` (219 frames, 720x1280, 12 samples, 2 threads, denoise FAST; not in git) and `take.mkv`
(libx264rgb crf 6, 30 fps, first_g 1548, 219 frames; 75.7 MB, so it is split in git as `take.mkv.partaa` / `partab`:
`cat take.mkv.part* > take.mkv`). g 1548..1553 = in-handle; g 1554..1625 = shot 18; g 1626..1766 = shot 19, which ends on the last
film frame (N 1767), so there is no out-handle. Rendered on the client-approved set (commit 5d511aa). Also `meta.json`, `cues.json`
(15 cues), `contact.jpg`, `qa.txt`. Scripts: `shot.py`, `deliver.py` (+ `take.json`), helper `c9.py`.

## Set-ups (re-rendered after QA-tech round 1; cuts at g 1626 and g 1666)
1. **g 1548-1625 (shot 18), `two_sections_out`.**
   - Wide from behind the enemy cannon line: both sections (Lin's creamy one and the general's grey one), the gate, a row of bronze
     guns with fire pots, a black-red banner and smoke. The general laughs on top (small; this is the wide).
   - Shot 1 hits on "นัดแรกร้าว" at g 1592: crater + star crack. Shot 2 hits on "นัดที่สอง" at g 1613: cracks race along the whole
     row by g 1632.
   - The ball reads as it flies. Impact dust is 0.45x the set's size at 0.55x opacity, and muzzle smoke is 0.6x, so the cracks stay
     visible. Smoke billows within 9 D of the lens are hidden (one hazed g 1548-1555).
   - Small camera kick on each hit; the general shudders, hops and kicks up dust.
2. **g 1626-1665 (shot 19a), `wall_top_battle`.** The general laughs on the top. Shot 3 hits on "นัดที่สาม" at g 1653: a strong
   camera shake, and he shudders (lean + roll wobble, squash), hops 0.35 D and dust comes up round his boots.
3. **g 1666-1766 (shot 19b), `two_sections_out`, tracking camera at 28 -> 30 mm** (head 43 px at the cut, about 2x the previous take).
   - The look-at follows the general (smoothed) as the section collapses (g 1660-1715). He drops laughing, the helmet flies off
     (g 1672-1690), and he slides down the rubble (g 1692-1714).
   - Collapse billows are 0.62x size at 0.55x opacity. His own dust is light (0.3), and from g 1710 the foreground billows are
     hidden for a clean closing image.
   - He ends sitting laughing in the rubble at (9.0, -5.4): head 151 px, centre 0.39-0.51 H, body above the caption band. He has a
     contact decal plus a soft ground-shadow disc (the decal is keyed off while he is airborne) and light base dust.
   - Slow push-in to the cut at g 1766. The helmet is an opaque card on the grass at (8.5, -9.0), inside the frame, with its own
     contact shadow.

Comic only, no injury. No quote, so mouths are static (the laughing grin is held). No DOF.

## Numbers (qa.txt)
- Heads (all above 880 on every frame):
  - Set-up 1: 18-20 px, centre y 419-436.
  - Set-up 2: 68-80 px, centre y 499-573.
  - Set-up 3: 43-151 px, centre y 504-657.
- Sprite clipping: warnings on g 1684-1689. The helmet in flight reaches the CANVAS9_FALL edge; nothing visible is cut.
- Popcheck:
  - Jumps only at the two planned cuts (1625->1626, 1665->1666), plus a small one at 1575->1576: the muzzle flash of shot 1.
  - No near-still runs; no black or magenta frames.
- Render: set-ups 1-3 at 12-15 s wall (23-30 s CPU) per frame. The late shot-3 frames show 28 s wall because they shared the CPU
  with a third process.
- Hue: warm BATTLE set-ups (orange 53-55 %, violet / magenta 11 % in the wall-top sky). The report's band flags come from the set's
  BATTLE look, not re-graded.

## Differences from the plan
- Shot 19 is split into two set-ups (wall_top_battle, then a cut to the wide outer view) instead of one wall_top -> two_sections move.
- The slide path is the set's `slide_out`, bent to land at (9.0, -5.4), clear of the gabions, the stake rows and the fire pot.
- I tried enemy gunners in shot 18 and left them out: from the wide camera their heads fell below y 880.
- The wall-top general stands at x 8 in set-up 2 but at x 5.4 in set-ups 1 and 3 (from the field he is clear of the banner there):
  a small jump across the cuts.
