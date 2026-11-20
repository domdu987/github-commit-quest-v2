def CUES(add, CFG, G0, G1, H_IN, H_OUT):
    add(G0 - H_IN, G1 + H_OUT, "ambience", "high above Paris, day 1889: wind, a far fairground band and crowd murmur that thins out as the camera climbs, then the warm restaurant murmur, cutlery and a faint string trio when it lands at the window")
    add(G0 - H_IN, 1800, "accent", "BIGZOOM: a long rising airy whoosh / swoosh with a gentle pitch rise as the camera dives across the city and up the lattice", peak_frame=1770)
    add(1772, 1782, "foley", "the camera passes through the lattice girders: a quick iron whoomp, close to the first platform", peak_frame=1777)
    add(1810, 1822, "accent", "landing on Maupassant: soft glass-and-room 'pop' as the window room tone arrives", peak_frame=1815)
    add(1815, 1819, "foley", "first happy bite on 'กินข้าวบนหอ': fork clinks on the plate, a blissful nasal hum without words (mouth stays still)", peak_frame=1817)
    add(1834, 1840, "foley", "second bite, napkin rustle and a glass tinkle", peak_frame=1837)
    add(G1, G1, "cut", CFG["cue_note_cut_out"])
