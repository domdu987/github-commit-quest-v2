# QA-art FINAL gate: film 19 v3 (harrison_v3.mp4), film-13 rules (QA_TEAM_film13.md, section D.3)

**Verdict: FIX-FIRST, overall 7.5.** The film is close. It needs one small re-render (the king at 64.5-67.5 s) and two conform-grade tweaks.

## Inputs

- Full-res frames at 2 fps: /tmp/claude-0/final_v3/f2/h000-h143.png.
- The four 360x640 phone sheets: sheet_phone_360x640_v3_p1-p4.jpg.
- The timed narration.
- Reference sheets: film/analysis/sheets/*.jpg (the oil ship short in particular).

I measured luma and saturation myself for each 0.5 s tile (mean of 0.299R+0.587G+0.114B, and (max-min)/max at 180x320). For the king shot (s24), I checked the cast spec in v3/cast19/cast19.py.

## Scores (film-13 QA-art)

| Criterion | Score | Notes |
|---|---|---|
| Set density / ornament | 8.5 | Every location is dense, lived-in and lit by practical lights: the brass-and-gear workshop, the parliament hall (red drapes, globes, telescope, chandeliers, green table), the storm deck with its lantern and rain, the noon deck, Port Royal and the Barbados beach. |
| Lighting & colour | 7.5 | There is warm against cool everywhere: the gold workshop, the red and gold hall against blue windows, the stormy blue-grey with a gold lantern, the cobalt sea. Saturation is 0.58 overall. Points are lost to two grade jumps and the dark ending (see the grade table). |
| Composition / phone legibility | 7 | Mostly wide or medium inside the set. Heads clear the caption band, and the captions are legible. Points are lost to the king's framing (below) and a few foreground crossings. |
| Character acting | 8 | Clear, readable faces: the proud Harrison; the mocking astronomer's big laugh (18-25 s); the steam-puff grey-hair gag (33.5 s); the crew's joy on the beach; the "Fluke!" shrug; the shocked, sweating astronomer and the grinning Harrison at the end. |
| Key moments | 7.25 | Hook 7.5, reveal 7.5, false payoff 7.5, ending 6.5 (details below). |
| Match to references | 7.5 | Same channel feel as the references: flat-faced cartoon cast in lit 3D sets, continuous camera travel, ship and sea spectacle. The ship design is plainer than the oil reference (navy hull, lilac sails). |
| **Overall** | **7.5** | |

## Key moments

- **Hook, 0-6 s: works.** The proud carpenter at his giant brass H1 is followed by the opening BIGZOOM (lone ship, over the stern, down to the puzzled captain and astronomer). The strange claim reads.
- **Reveal, 34-46 s: works.**
  - The tiny H4 sits beside the giant H1, and the whip lands on "เท่าจานรอง" with the dial whole.
  - The noon deck has the sun right overhead (a lovely flare at 39 s), and William holds up the watch that "still shows home time".
  - The sea shots and the heeling ship carry "15 degrees per hour".
- **False payoff, 52-55 s: works.** The beach celebration (cheering crew, flying tricornes, the watch held up) cuts to the same mocking astronomer shrugging "ฟลุ๊ค!". The turn is clear.
- **Ending, 62-72 s: weak.**
  - The old Harrison walks in, then the king times the watch (64.5-67.5 s), then a whip to the shocked, sweating astronomer, then a whip to Harrison grinning over the bag of gold. The final image reads.
  - **The king does not read as a king.** king19 is a historically correct George III: powdered wig, blue coat, a sash that is barely visible, no crown. On a phone he looks like another wigged astronomer in a blue coat.
  - He is also small at the right edge, behind the candelabra. At 66-67 s the lit candles cross his coat, and his watch hand touches the right frame edge.
  - The narration says "พระราชา", but nothing on screen confirms it. The joke ("the king himself, exactly as the astronomer dared") is carried by the audio alone.
  - This hits two of the client's own complaints at the film's punchline: someone cut weirdly by the foreground, and by the frame edge.

## Grade continuity (luma per 0.5 s tile)

| Where | Luma before → after | Judgement |
|---|---|---|
| 8.7 s, s04 → s05 (same storm deck) | 111-114 → 83-86 | **Visible jump inside one scene.** Grade fix. |
| 67.5-72 s, s24 after whip 2 (library, then the ending table) | about 110 → **66-73** | **The ending is the darkest stretch of the film.** The other hall shots sit at 74-81. Grade fix. |
| 31.0 → 31.5 s, s11 → s12 workshop | 107 → 82 | Motivated (candle-lit years passing). OK. |
| 38.5 → 39.0 s, inside s15 | 91 → 121 | In-take: the camera turns into the overhead sun on "ดวงอาทิตย์". Motivated. OK. |
| 52.7 / 55.5 / 58.5 s (beach ↔ hall) | 116 → 76, and back | A change of location; reads as intended. OK. |

## The client's own complaints

- **Floating:** none seen. Feet and contact shadows are visible in every scene with legs in frame (storm crew, hall, decks, Port Royal after the float fix, Barbados, the corridor walk). The per-take GROUND checks reported 0 FAIL.
- **Shaky:** none seen. The camera reads calm and always moving; the s02, s14 and s19 passes removed the bumps. The 20-21 s jitter flag is the laughing actor in s08, not the camera.
- **Cut weirdly by the frame or the foreground:**
  - **the king at 64.5-67.5 s (blocking, see above);**
  - minor: at 14-15.5 s the brass telescope crosses the top of the left astronomer's wig;
  - minor: at 56-58 s a dark woven basket is cut by the bottom-left edge;
  - the dissolves at 55.5, 58.5 and 62.0 s briefly ghost a large face over the next shot, which is acceptable for a dissolve.

## Fixes, ranked

### Needs a re-render (one, small)

1. **s24, the king beat (about g 1933-2021, roughly 3 s, before whip 1). Make the king read as the king and give him clean space.**
   - Give king19 an unmistakable royal signal at phone size: a small gold crown on the wig, or a red, ermine-trimmed robe over the blue coat. Also make the Garter sash and star bolder.
   - Re-block so that the candelabra does not cross him: move it about 0.4 D left on the table, or slide the camera.
   - Keep his hands and watches at least about 40 px inside the right edge.
   - Everything after whip 1 (the astronomer and the ending) can stay as it is. A frame check of that segment is enough.

### Conform grade only (no re-render)

2. **Lift the ending (s24 from about 68.0 s to the end) by about +8 to +10 luma** (a gentle lift or gamma), so the final payoff image sits with the other hall shots (75-81) and does not end the film darker than everything else. Keep the warm gold of the bag.
3. **Even out the storm cut at 8.7 s:** bring s04 down by about 8-10 and/or s05 up by about 6-8, so the two shots of the same storm deck sit within about 10 luma of each other.

### Optional polish (does not block)

4. s06: nudge the telescope or camera so the brass tube clears the left astronomer's wig at 14-15.5 s.
5. Ship design: warm the sails (cream or striped) or add a red band on the hull, toward the oil reference.

Once fix 1 is re-rendered and fixes 2-3 are applied in the conform, I expect this to SHIP: about 7.8, with the ending at about 7.5. A check of the new s24 king segment and the re-graded 1 fps sheet is enough to confirm.
