TAKE, SHOTS = "s30", [30]
SHOT_RANGES = {"30": [1980, 2095]}
FIRST, LAST = 1971, 2099
G0, G1 = 1980, 2096
TRANS_IN = dict(type="dissolve", frames=17, note="DIS from shot 29, the longest dissolve of the film (17 f smoothstep, centred on g 1980); 9 handle frames rendered before g 1980")
CUTS_QA = [2096]
EV = dict(yawn_poses="candle yawn / nod alternate", snap=[2024, 2038], word_guard_the_wire=2026, hard_cut=2096)
NOTES = dict(light="NIGHT", set="v3/set3d16 CHAMBER chamber_table NIGHT (camera chamber_table_night): candles, lit side doorway, full tape piled round the stool, set_click toggled every 9 f (the register clicks)",
             cast="v3/cast16 mocker_stool_candle / mocker_stool_candle_nod (alternating, yawn + sleep Z), morse_peek_door in the lit doorway (grinning); no lip-sync",
             camera="custom 22 mm from the preset start pose pulled in 38 %, slow pull back 8 %/s + slide + arc, snap push x1.45 on 'นั่งเฝ้าลวด' (g 2026)")
CUES = [(1971, 2100, "ambience", "night: empty chamber, a faint clock, the candle flame flutters"),
        (1980, 2096, "prop", "the register clicks 'ติ๊ด ติ๊ด' steadily (every 9 frames), paper tape hisses out"),
        (1992, 2010, "foley", "the mocker's big yawn: a long sleepy groan"),
        (2024, 2038, "accent", "snap push whoosh (soft)"),
        (2090, 2096, "accent", "last click, then hard cut on 'เอง'")]
