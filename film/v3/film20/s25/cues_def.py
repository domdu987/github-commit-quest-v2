def CUES(add, CFG, G0, G1, H_IN, H_OUT):
    add(G0 - H_IN, G1 + H_OUT, "ambience", "first-floor restaurant of the finished tower, day 1889: room murmur, cutlery and plates, a faint string trio, wind through the open lattice")
    for r in (19,):
        add(G0 + r - 2, G0 + r + 3, "foley", "fork lifted to his mouth: small cutlery clink on the plate, blissful nasal hum without words (mouth stays still)", peak_frame=G0 + r)
    add(G0 + 50, G0 + 68, "foley", "wine glass raised and set down: a light crystal 'tink' and a soft swallow", peak_frame=G0 + 58)
    add(G0 + 22, G0 + 36, "foley", "napkin rustle, chair creak as he sways happily", peak_frame=G0 + 30)
    s = CFG["events"]["snap_push"]
    add(s[0], s[1], "accent", "snap push on 'ที่เดียว': short airy whoosh rising with a pleased 'tada' on the lyrical word", peak_frame=s[0] + 6)
    add(G1, G1, "cut", CFG["cue_note_cut_out"])
