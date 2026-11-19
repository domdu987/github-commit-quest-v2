# Film 18 style board (Jimo, 279 BC). Built by `python3 jimo.py board` (jimo.py, jimo_tex.py, jimo_camp.py, jimo_ox.py, board.py, jimo_hue.py)
720x1280, Cycles CPU, 12 samples, OIDN, no DOF, no text. Render time per still (4 threads): 7.9 s wall / 30.3 cpu (1), 8.2 / 31.4 (2), 9.9 / 38.3 (3).

| still | what it tests | shade hue | luma mid-band | dark V<0.25 | red/orange/blue/violet % |
|---|---|---|---|---|---|
| board_1 jimo_wall_night | palette, rammed-earth wall, gate tower, moat/bridge, moon, lantern + torch light vs blue | 245.3 | 129 | 0.00 | 17.1 / 4.6 / 56.0 / 15.4 |
| board_2 yan_camp_night | detail density (tents, 4 fires, racks, chariot, drums, jars+cups table, palisade, horses), far lit wall | 245.0 | 103 | 0.00 | 13.9 / 15.2 / 49.2 / 12.7 |
| board_3 wall_holes_oxen | fire ox (silk, blades, tail flame) lighting the earth wall orange vs blue night | 250.8 | 145 | 0.00 | 44.5 / 12.9 / 11.3 / 8.3 |

Key night preset: moon key (0.30,0.44,1.15) cool, shade (0.085,0.105,0.34) violet-blue, warm point lights (1.0,0.58..0.64,0.24) + additive pool/halo cards.
Known weaknesses: still 3 mid-band luma 145 (above 130) and wall reads salmon/pink more than ochre; stills 1-2 are blue-heavy (49-56 % blue, warm 18-29 %);
caption band (y 880-950) holds the bridge/water edge (1), the table/fire base (2) and the ox legs (3); ox is a chunky placeholder; water reflections are
painted streak cards, not true mirror; tents in 2 are only partly framed; far city is a few roofs.
