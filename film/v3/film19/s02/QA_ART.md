# s02 QA-art

## Round 9 (director QA-art): FIX, 6.3

Take: take.mkv.partaa + partab, joined to /tmp/s02_a.mkv (first_g 48, g 48-199, frame index = g - 48). I extracted every frame, viewed them at 3 fps, viewed every frame from g 104 to 127 (the descent), and viewed key frames at 360x640.
Frames: /tmp/qa19_r9art/s02/f_NNN.png (NNN = index + 1). Sheets: /tmp/qa19_r9art/s02_3fps.jpg, s02_dive.jpg, s02_full1.jpg, s02_full2.jpg (360 px wide = phone), s02_astro.jpg.

| Check | Status |
|---|---|
| Start is extreme wide? | **No, it is a wide.** At g 48-57 the ship fills about 30 % of the frame height, with only a thin strip of horizon and sky at the top. The sea is a lovely vivid turquoise with a white wake, but it reads as "a ship from a drone", not "one lone ship on an endless ocean". The characters cannot be found (they are under 5 %, which is right, but nothing guides the eye to them). |
| Move shape | **Badly timed.** From g 48 to 107 (2 s) the camera only pushes slowly; the ship grows from about 30 % to 55 %. Then the whole descent happens in about 10 frames (g 108-117, 0.33 s): frame-diff jumps from about 10 to 27-40. On a phone this reads as a jump cut, not as a swoop. The medium is reached at g 118 (3.93 s) and then the shot holds for 2.4 s with only a slow orbit. |
| Detail passing on the way down? | **Hardly any.** The sails pass in 2-3 frames. For g 111-116 the main thing passing is the plain navy hull side and gunwale, which fills up to half the frame as a dark, flat wedge. The rigging, ratlines, lanterns, cannon, crew and deck life are never seen up close on the way in. |
| Landing / "nobody knows where we are" beat | **Weak.** The landing frame is good: a medium on the quarterdeck, with the wheel shadow and rigging shadows on the orange deck, the sails and shrouds behind, and the bodies about 37 % of the frame height. Nobody is cut and the faces are about 16 %. But: (1) **the chart is not blank.** It shows a coastline and a big red compass-rose/X mark, so on a phone it reads as "we know exactly where we are" (a treasure map), the opposite of the beat. (2) The captain only holds the chart with a stern frown for 2.4 s. He does not look puzzled, turn the chart or look around. (3) The astronomer squints through the quadrant, lowers it with a frown and raises it again (g 142-166). This is fine but small. The planned head-scratch does not read as a scratch. There is no shared "?" moment by 5.5 s. |
| Colour | **Good.** Sat 0.76 to 0.52, luma 106 to 88, vivid 77 % to 54 %. The noon sun gives crisp blue shadows on a warm deck. The sails are a dull grey-lilac and could be warmer or whiter. |
| Grounding / edges | OK. The feet have contact shadows and nobody is cut. |

| Criterion | Score |
|---|---|
| Set | 7.5 |
| Light & colour | 8 |
| Composition / phone | 6 |
| Acting | 5 |
| Key moment (BIGZOOM + "where are we?" beat) | 5 |
| Match to refs (R5 crane up/out over the ship) | 6.5 |
| **Overall** | **6.3 - FIX** |

Fixes (shot.py):
1. **Retime the descent so that it reads as a swoop, not a jump.** Today TM = [(48,0),(80,.26),(108,.57),(114,.84),(118,.97),(150,1)]. Use something like [(48,0),(66,.10),(90,.35),(115,.70),(135,.92),(150,1)]. This gives a clear ease-in, about 1.5 s of fast travel centred on g 100-130, and an ease-out landing at about g 150 (5.0 s). The peak frame-diff should be about 15-20, not 40.
2. **Start wider.** Push KEYS[0] loc out and up about 2x (for example (20, -330, 240)) and lift the look so the horizon sits at about 25 % from the top. Target: ship at or under 12 % of the frame height, with a big glittering sea around it. Add a few sun-glint sparkles near the ship so the eye finds it.
3. **Fly through the rigging, not past the hull.** Raise KEYS[2] and KEYS[3] about 6-8 D in z and route them between the mizzen shrouds and the spanker. Over g 110-140 the frame should pass ratlines, a sail face, a lantern, a flag or pennant, and a sailor on the yard, and the hull side should never be more than about 15 % of the frame.
4. **Make the chart blank** (an empty parchment, or just a big "?" scribble) and remove the red X or compass mark.
5. **Puzzled acting by 5.5 s.** Over g 150-170 the captain turns the chart upside down (rotate the prop 180 degrees, or flip it twice), tilts his head and raises his brows (a puzzled face, not the stern one). The astronomer lowers the quadrant and does a clear head-scratch with the free hand (3 strokes), and they shrug at each other (a 4-frame squash). If allowed, add a small "?" pop over each head on g 160.
6. (Polish) Warm or whiten the sails a little (they read as grey).
