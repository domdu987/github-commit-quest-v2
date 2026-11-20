# BUILD_NOTES, builder B (under + mapworld)
Files: beck_under.py, beck_map.py, beck_util.py (helpers), API.md section B, contact/B_sNN_start|mid|end.png, contact_sheet_B.jpg, contact_phone_B.jpg, hue_rows_B.txt. Textures: tex_beck/u_*_v7.png (own painters, not beck_tex).
Render cost (720x1280, 14 samples + OIDN, 4 threads, while the other builder was also rendering): under/shaft+noodles 4-8 s per frame wall (about 16-32 s CPU), platform 7 s, hall 7-8 s, carriage 5-7 s, mapworld 5-6 s. Scene build 3-5 s; first run adds about 1 s per new cast22 card (cached in actors/).
Known issues: see below (honest list).
- Colour: see hue_rows_B.txt. s11 end (paper close) luma 127, s14 mid hue off (table brown), s03 end hue 270 (pink map). Mapworld is now Becks drafting table (ink bottles, set square, ruler, green lamp, night window, tiny trains, ring crowds, name tags).
- s03: the camera passes through translucent tube walls in the noodle part (by design) and flies the long straight tunnel with little light (frames 262-290 are very dark navy); needs a lamp string if the director wants more read there.
- s09: the official's pillar peek is only seen at the end; crowd is thin near the camera. s10: train doors are overlays; the official at the bench is not hidden by it from every view (card).
- Ink hulls in mapworld are sized for ~11-14 D camera distance and thin out in the s14 high view.
- Cast cards are static pose images (billboards); lip-sync and walking need the render team's real animation.
