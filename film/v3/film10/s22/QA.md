# s22 QA: film 10, shots 22-23 (g 1627-1814, handles 1621-1626 and 1815-1820)
Delivered: take.mkv.part* (`cat take.mkv.part* > take.mkv`; libx264rgb crf 6, first_g 1621, 200 frames), meta.json, cues.json, contact.jpg, QA_AUTO.md (PASS), phone_sheet.jpg.
- Shot 22 (g 1621-1709): harbour_wide DAY, hd1 st0: the grey berth ship in front, every other ship dazzle behind it. Custom camera, slow crane-down/in (z 19 -> 12). Admiral (worried, sweat) and painter (calm smile) on the quay, small (wide, heads y 740-820, chin < 880). Glossy bounces off: no mirrored-ship panels on the water.
- Shot 23 (g 1710-1820): hull_plank DAY, admiral on the set's hanging stage (`admiral_plank_sheepish`, plank=0), brush sweeping, paint_spots 0.7 -> 1, set_stripes 0 -> 0.62 keyed linear (g 1710-1800). Head y ~510-550 (0.40-0.43 H). Rendered through g 1820, past the film end (N 1815) and the hard cut on "เอง" (g ~1797-1800).
- Cut 22 -> 23 at g 1710 checked +-3 frames. No mouth moves (sheepish smirk held).
- Known: the admiral's sheepish face reads slightly stern at phone size.

## QA-art rework round
- Shot 23: stripe front is tied to the brush (set_stripes 0.38 -> 0.48; the admiral shuffles right along the stage, his last stroke lands on the front at g 1798 = the cut on "เอง"). Big navy/white paint blobs (overlay) on moustache, cap peak and cheek. Push-in ends with the head 19% of the frame width (w 139 px). Ladder kept clear of him.
- Shot 22: camera ends close (head w ~60-70 px, heads y 800-860, chin < 880); the admiral looks up at his grey ship from g 1650-1685.
- qa_auto PASS; its note 'cut 1710 not visible' is a luminance heuristic: the 22->23 cut (harbour wide -> hull plank) is obvious on g 1709/1710.
