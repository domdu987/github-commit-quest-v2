# QA-tech round 14 s01: FAIL
Checked: all 162 frames extracted, 6 fps sheet, every frame g57-100, 1:1 crops g0/60/80/97/108/155. Frame-diff re-measured (90x160 grey, in-shot g1-155): median 8.56, p90 14.86, min 2.98 (g124) = matches the director. Colour: sat 0.48-0.52, luma 78 (g0) / 95 (g60) / 111 (g108-155).

## Blockers
1. g64-g84 - the two basket carriers enter from the bottom and right edges with heads below the y 860 line and half-cut by the frame edge, and they were not in frame before (they pop in; the team admits g60).
   - Blue-robe carrier (bottom-left): head first appears at the bottom edge at g63-64 (head top y ~1240, chin ~1290, cut by the edge), g68 head y ~1130-1250, g72 ~990-1130, g76 ~910-1040, g80 chin ~950; the head clears y 860 only at ~g83. About 20 frames (0.7 s) with the head in the caption band.
   - Second carrier (right edge): head y ~1000-1050, half cut by the right edge at g72-90.
   - The ground where they stand is empty at g60 and g63 at the same screen place, so this is a pop, not a camera reveal.
   - Fix: put both carriers in the world from g0 at positions the camera reaches with head above 860 (or keep them out of frame until their chin < 860, i.e. g84+; or delete them and leave Tian Dan + ox as the only foreground characters until g85). No character may be cut by an edge.

## Checks passed
- Zoom: one continuous eased move g0-108 (3.6 s), then slow push + orbit g108-155. No stall (lowest frame-diff 2.98, never < 2.9). No pulsing, no cut.
- Tian Dan height / frame height: g0 ~25 px = 2.0 % (at x 370, y 610-635, lit patch beside the ox herd), g60 ~7 %, g80 ~17 %, g97 ~35 %, g108 ~41 % (hat y 421 to feet y 950 = 530 px = 41 %), g155 ~42 %. Start < 5 %, g108 in 35-60 %, zoom 3.6 s. OK.
- Passes through set detail: roofs/pagoda, wall walk with braziers, oxen rows, 即墨 sign, sand yard. Rich at every stage.
- 即墨 plaque readable: sharp, gold on dark red, glyphs 20-100 px from g38 to g72 (about 1.1 s clear, fully legible g45-g72). OK.
- Blades tied at g97: he holds the blade bundle at the ox horns (g90-108). OK.
- Heads (Tian Dan, oxen) above 860 throughout: chin max ~600. No mouth moves. No flames on his tail issue (brazier flames are set lamps). No placeholders.
- Ground at the end: sand mask 0.30 at g108, 0.28 at g155 (limit 0.30): on the line, note.
- Rim: pale blue edge on Tian Dan's hat and horn; warm lantern/brazier key; warm + cool in frame. OK.

## Notes
- Plaque post g62-84: a flat unlit near-black pole crosses the frame (x 0-10 % wide at g76-84, black bar at the left edge). It lasts about 0.5 s as a foreground wipe; acceptable, but a tint of warm rim would remove the "black slab" look.
- g0-20: Tian Dan is 25 px tall among 100+ oxen; findable only by the brazier next to him and his white face. Marginal; a slightly brighter pool of light on him would help.
- g0 luma 78 (night opening), sat 0.485; rest of the shot is fine.
- Fix list is only blocker 1; the move itself passes.
