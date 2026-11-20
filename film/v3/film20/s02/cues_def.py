def CUES(add, CFG, G0, G1, H_IN, H_OUT):
    add(G0 - H_IN, G1 + H_OUT, "ambience", "first-floor restaurant of the finished tower, day 1889: room murmur of diners, cutlery and plates, a light wind through the open lattice, a faint string trio")
    for g in (G0 + 20, G0 + 60):
        add(g - 2, g + 3, "foley", "fork lifted to his mouth: small cutlery clink on the plate, a happy 'mmm' hum without words (mouth stays still)", peak_frame=g)
    add(G0 + 40, G1, "foley", "napkin rustle and a chair creak as he settles; glasses tinkle on the table", peak_frame=G0 + 45)
    s = CFG["events"]["snap_pull_out"]
    add(s[0], s[1], "accent", "snap pull-out on 'เดียวกันนั้น': fast whoosh sliding back, the room tone opens up into wind and a huge airy height (reveal: the girders and Paris below)", peak_frame=s[0] + 6)
    add(CFG["events"]["word_same"], CFG["events"]["word_same"] + 6, "accent", "reveal sting: a bright rising 'tada' glissando as the iron lattice appears", peak_frame=CFG["events"]["word_same"] + 2)
    add(G1, G1, "dissolve", CFG["cue_note_cut_out"])
