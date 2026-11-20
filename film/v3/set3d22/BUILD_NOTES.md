# BUILD_NOTES (builder A): beck.py core, beck_london.py, beck_hq.py (+ beck_tex.py painters, make_contact.py)
Built: registry/CLI/cameras/cast cards in beck.py; london DUSK+NIGHT (real window openings, 1930s skyline, grate, joins); Beck's lodgings (animated diagram geometry, 3D arm, old map, cork board, cot, chair, trunk, rug); publicity room (partition, official's desk with drawer/stamp, clerks' desks, map towers, crate); HQ corridor (doors, notice boards, lamps). Shots s01 s02 s04 s05 s06 s07 s08 s15 with contact stills in contact/, contact_sheet.jpg, contact_phone.jpg, hue_rows.txt.
## Render seconds per frame (720x1280, 14 samples + OIDN, 4 threads; whole-process wall incl. build, final-quality)
lodgings 5-9 s (render 4.5-11 s); london DUSK 9-14 s (render 7.6-12 s); london NIGHT s15 11-22 s (the end frame inside the room is the slowest, 20 s); publicity 6-9 s; corridor 8-11 s. Cycles CPU, 25-45 CPU-s per frame.
## Known issues
- s06/s07 foreground furniture (typewriters, desks) is blocky; s07 bird's-eye clerks are small and lean-back cards read thin.
- s05 uses a 3D arm (not a card) for the top-down shot; Beck's head is only in the first frames.
- Placeholder: lodging window join uses the painted night_city outside in the room vs the real 3D street in london (hidden by the push through the glass, needs a 4-frame dissolve).
- s01 end / s05 luma can exceed 110 (window card, paper); see hue_rows.txt. Lens 22-24 used in a few publicity frames because the room is shallow.
- Setters set_crowd / set_rack / set_train belong to B or were not needed; london crowd is static.
