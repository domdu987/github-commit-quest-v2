# QA-art sJ2 v4 (TAKE gate, team11 a68e0fc)
Take: gate/sJ2/film/v3/film21/sJ2/take.mkv (140 frames, 720x1280, g1709-1848, last frame g1847, hard cut). Viewed: all 140 frames pulled from the take, full size for g1714-1744, g1786-1847 (every frame in g1786-1824 for the move and the splice), a 2x crop of the bridge mouth at g1722, a ruled crop of the last frame g1847 (y lines every 50 px), per-frame white-area and frame-difference numbers for the crowns and the camera move, the team's contact and phone sheets, the team QA.md and QA_AUTO.md. Levels and saturation are left to the conform. Rim light is a film-wide open item and is not judged here.

## Verdict: FIX-FIRST

The new end camera solves the sand problem: it sits over open water, the sand is a thin strip behind the swimmers (about 2-5 % of the frame), and the last frame is four spluttering, deadpan heads in the water with a tall crown behind them. That is a much better button than v3. But the v4 re-render of g1788-1848 does not join the v3 frames before it. At g1787 to g1788 the camera jumps (a pop that reads as an unplanned cut), and then the camera tilts up into about half a second of empty sky (g1794-1808) before it swings down onto the swimmers. On top of that, the new low camera puts every face in the caption band (faces at y about 860-1040). Both problems need the same fix: a new camera path for g1786-1847.

## B3 (v3): PARTLY FIXED
| asked for | v4 |
|---|---|
| camera over the waterline | FIXED. The camera floats just over the water from about g1813. |
| sand at most 15-20 % | FIXED. Sand is about 2-5 % (a strip behind the swimmers, not between them and the lens). Water fills about 15-20 % and sky about 35-40 % of g1819-1847. |
| all heads inside the frame | FIXED at g1819-1847 (left face about x 25-200, right coif face about x 540-700 in g1847). NOT FIXED in g1810-1817: a swimmer rises out of the bottom edge (g1810), a near-lens face is cut by the left edge (g1812-1815), and the right swimmer is cut in half by the right edge (g1816). At g1825 a fifth swimmer, arms up, is cut by the right edge. |
| crowns 1.5-2x, beside the swimmers, on 1821/1830/1839 | PARTLY. The crowns are bigger (the tallest shards are about 25-30 % of the frame height). But crown 1 stands on the right frame edge and is cut by it (g1817-1832), and crown 2 stands on the left edge and is cut by it (g1823-1841). Their white areas overlap, so g1821-1840 reads as one long spray, not two hits. The 1839 "ตูม 3" cue lands on the fading second crown. Crown 3 rises at g1843, BEHIND the heads, not beside them. |
| last crown peaking at g1846-1847 | FIXED. Crown 3 is still rising at g1846-1847 (white area 9.7 %), so the cut lands on it. |

## Blur ruling (qa_auto "suspected blur" g1794-1808): NOT BLUR. It is a false alarm on sharpness, but those frames are still a problem.
At full size, g1794, g1802 and g1808 are sharp: the cloud outlines, the far tents and the hill terrain have crisp edges, and there is no smear or ghosting. The edge score drops (about 160-390, against 670-1050 elsewhere) because these frames are 60-85 % empty blue sky during a fast tilt and swing: the frame difference is 33-54 per frame, against 12-24 elsewhere. There is no motion blur and no splash spray in them. This is not a blur fail. But what the frames show, no characters for 0.5 s just before the ending, is a problem; see B4.

## Issues

**B4 (blocking), g1786-1815: the splice pop at g1787 to g1788, and the move that follows it.**
- g1787 to g1788 is a jump, not a move. The coif jumper doubles in size, the ground under him changes from grass to sand, and the two other jumpers (one in mid-air with arms up) vanish. The frame difference spikes from 12.7 to 43.3 with no ease. The v4 path (re-rendered from g1788) does not start where the v3 path ends at g1787. That is the bump the brief asked me to check.
- g1792: the coif jumper is cut in half by the right edge.
- g1794-1808: the camera tilts up into empty sky and swings around. For about 0.5 s, in the film's last 2 s, no character is in frame, and the plan's "camera DROPS to water level and pushes in" plays as "camera looks at the sky".
- g1810-1816: the camera comes down onto near-lens faces cut by the bottom, left and right edges, and the swimmer rising at g1810 has his head in the caption band.

Fix: re-render g1786-1847 with one path whose first key is exactly the v3 camera at g1787 (same position, rotation and lens; ease out of it). Drop the camera DOWN and forward toward the waterline over about 20 frames (a crane-down with a slight push) and keep the jumpers or splashes in frame the whole way. Do not tilt above the horizon, so the sky stays under about 40 %. Land on the end framing by about g1808. Keep near-lens culling so no face comes closer than the end framing.

**B5 (blocking), g1813-1847, including the last frame: the faces sit in the caption band.** In g1847 the hat brims are at y about 800-860, the eyes at about 920-960 and the chins at about 1000-1040, so all four faces sit below the y 880 line, and the same is true from about g1813. The phone sheet's cyan line runs across their foreheads at g1829 and g1844. The punchline faces would sit under the captions and the platform UI. (The lower 18 % of the frame is flat cyan water, and the top 38 % is sky.)
Fix: with the same camera height, tilt down about 6-8 deg, or raise the camera 0.2-0.3 m and tilt down, so the faces sit at y about 600-820. Water then fills the lower third under them, and the sky drops to about 25-30 %. Keep all faces inside x 60-660.

**N5 (non-blocking, do it in the same re-render), g1817-1847: crown placement and timing.** Move crown 1 and crown 2 inward so neither is cut by a frame edge: crown 1 beside the right swimmer at about x 520-640, crown 2 beside the left swimmer at about x 80-200. Shorten their life so they read as two separate hits (peaks at about 1821 and 1830). Put crown 3 beside the middle swimmer, not straight behind the heads; it can overlap a shoulder. Keep its peak on g1846-1847. Then either move the "ตูม 3" sound cue from 1839 to about 1843, or bring crown 3's impact earlier so its rise starts at 1839. The sound and the third visual hit must land together. (Cues are in cues.json; the plan's 61.2 s = g1839 is the sound, and the visual may lead it slightly.)

**N1 (non-blocking, carried from v3), g1714-1745: the Scots "wall" still reads as orange and yellow crates,** with a hard yellow ground hotspot at the far left. The two lit saltire flags carry the why-they-jump read on a phone, so this is not blocking. Fix as in v3: blue tunic head-cards with spears above the shield row, and a softer or narrower point light.

**N2 (non-blocking, carried), g1714-1749: faint grey smoke wisps** (thin curved white-grey streaks behind the flags). They are thin and read as smoke trails. They are gone from the end frames (the smoke columns are hidden), which is good.

**N4 (non-blocking, carried), g1713-1745: the "look at the bridge" is mostly the eyes.** A short head-card turn toward the flags would read better on a phone.

## Regression checks (v3 fixed items)
- Lit Scots wall with saltire flags at the bridge mouth, g1714-1745: NO REGRESSION. The big flag (about 10-12 % of frame height) and the second flag are lit and clear at g1714-1732; the big flag is at the left edge by g1744 as the camera follows the group, as in v3.
- No grey crescent or horn smoke slabs: NO REGRESSION. None anywhere in the take; the end frames have no smoke at all.

## Checks
- Heads above y 880: pass g1709-1792; FAIL g1810-1847 (B5).
- Frame edges: fail g1792, g1810-1816, g1825 (B4/B3 residual); crowns cut by the edges at g1817-1841 (N5); pass g1819-1847 for faces.
- Continuity around the camera change (g1788-1812): FAIL, pop at g1787 to g1788 (B4). The swing itself is continuous, with no further jumps.
- Colour story: English all crimson with grey helmets and gold leopard badges; Scots blue as the saltire flags; the ending is blue sky and cyan water against crimson. Pass. Lower-frame water is a flat, very bright cyan; that is for the conform.
- No speech: none in the picture (no speech bubbles or text). Pass.
- Comic and bloodless: swimmers splutter (droplets, wide eyes) and float deadpan with helmets bobbing; nobody is under water or lying still. Pass.
- §G nothing floats: the jumpers are in motion with ground shadows; the swimmers have water rings; the helmets float on the water. Pass. No face over 35 % of the frame height (the largest is about 20 % at g1788-1790). Pass.

## Scores
phone legibility 6 (bank 7, end 6: faces in the caption band) / set density 6 / light 7 / colour story 8 / acting and comedy 8 / last-frame button 7 (up from 5) / camera travel 4 (pop at g1788 and 0.5 s of empty sky).
