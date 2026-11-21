#!/usr/bin/env python3
"""s14 (film 22) mapworld: other cities' diagrams light up; end high over the glowing London diagram (match dissolve into s15).  g 1662..1751 (+handles).
    python3 shot.py stills 1656:1758:6 <out> [scale%] [samples]      python3 shot.py final 1656:1758 <out>
"""
import os, sys, math
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c22 as C
B, U, bpy, V = C.B, C.U, C.bpy, C.V
import beck_map as M
F0, F1 = 1662, 1752
CAM = [(-8, (50.0, -9.0, 5.6), (84.0, 0.0, 1.5), 24.0), (0, (58.0, -9.0, 6.0), (92.0, 0.0, 1.5), 24.0), (18, (52.0, -20.0, 36.0), (104.0, 5.0, 4.0), 24.0),
       (44, (22.0, -72.0, 190.0), (62.0, 10.0, 0.0), 24.0), (70, (-4.0, -62.0, 360.0), (0.0, 6.0, 0.0), 24.0), (89, (0.0, -22.0, 400.0), (0.0, 3.0, 0.0), 24.0)]
PAPERS = []
def post_build():
    C.set_emission_color('BK_e_table_wood', (0.02, 0.03, 0.10), 1.0); C.tint_emission('BK_e_pp_', (1.0, 0.82, 0.58)); PAPERS.extend(C.LAST_MIX)
    C.scale_lights('lamp_sun', 0.5); C.scale_lights('key_sun', 0.85)
def animate(f, n):
    u = C.ez((f - 14) / 62.0)                                   # the paper dims to night blue as the city lights come on
    for m, em, mx in PAPERS:
        em.inputs['Strength'].default_value = 0.34 * (0.9 - 0.30 * u)
        mx.inputs[7].default_value = (1.0 + (0.12 - 1.0) * u, 0.82 + (0.26 - 0.82) * u, 0.58 + (1.0 - 0.58) * u, 1.0)
    M.place_train(M.train_s14(f), ext=True); M.place_line_trains(f)
    M.set_city_diagrams(min(1.0, max(0.0, (f - 14) / 52.0))); M.set_london_glow(min(1.0, max(0.0, (f - 40) / 45.0))); U.face_cards()
    k = min(1.0, max(0.0, (f - 36) / 48.0))
    for col in M.COL:                                           # the London lines blaze like city lights
        a, b = M.LINE_MATS[col]
        for mt, lo, hi in ((a, 0.8, 4.4), (b, 1.55, 7.0)):
            nd = mt.node_tree.nodes.get('strength')
            if nd: nd.inputs['Strength'].default_value = lo + (hi - lo) * k
    for (ci, col), (m1, m2) in M.CITY_MATS.items():
        for mt in (m1, m2):
            nd = mt.node_tree.nodes.get('strength')
            if nd: nd.inputs['Strength'].default_value *= 1.0 + 0.7 * C.ez((f - 20) / 50.0)
if __name__ == '__main__':
    C.drive('s14', CAM, 'mapworld', 'MAPWORLD', animate, post_build, sys.argv[1:], F0, F1)
