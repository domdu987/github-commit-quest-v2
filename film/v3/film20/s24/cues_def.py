def CUES(add, CFG, G0, G1, H_IN, H_OUT):
    add(G0 - H_IN, G1 + H_OUT, "ambience", "first-floor restaurant of the finished tower, day 1889: murmur of many diners, cutlery and glasses, a faint string trio, a light wind through the lattice")
    for g in range(G0 - H_IN + 6, G1 + H_OUT, 15):
        add(g - 1, g + 3, "foley", "footstep on the carpet runner (alternating soft thuds of the waiter and Maupassant, the waiter's lighter)", peak_frame=g)
    add(G0, G0 + 20, "foley", "starched apron and tailcoat swish as the waiter sweeps his arm toward the window end", peak_frame=G0 + 8)
    s = CFG["events"]["snap_push"]
    add(s[0], s[1], "accent", "snap push on 'หลังหอเปิด': short airy whoosh rising", peak_frame=s[0] + 6)
    add(G1, G1, "cut", CFG["cue_note_cut_out"])
