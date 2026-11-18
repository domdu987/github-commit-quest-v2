#!/usr/bin/env python3
"""Renders the contact-sheet tiles (720x1280, final quality, placeholder cards at the stand points) into street_work/final/ and writes final_log.txt
(wall / CPU seconds, projected head pixels of every staged card). usage: python3 render_tiles.py [tile_name ...]  (default: all).  THREADS=2 SAMPLES=14 env respected."""
import sys, os, json, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE))
import street as S, bpy
from mathutils import Vector

def _mud_coach(A):
    r = bpy.data.objects['coach_run']; r.location = (0.2, 14.6, 0.0)
def _throw(A):
    S.throw('cabbage', (-5.0, 11.4, 4.6), (-2.55, 10.45, 4.35), 10, 22, bounce=(1.6, -1.8)); bpy.context.scene.frame_set(18)
TILES = [  # name, preset, light, u, state, extra, label
    ('01_street_wide', 'street_wide', 'RAIN', 0.0, dict(), None, 'street_wide RAIN'),
    ('02_street_high', 'street_high', 'RAIN', 0.0, dict(umb=0.0), None, 'street_high RAIN umb 0'),
    ('03_coach_low', 'coach_low', 'RAIN', 0.0, dict(busy=1.0), None, 'coach_low RAIN busy 1'),
    ('04_hero_track', 'hero_track', 'RAIN', 0.0, dict(), None, 'hero_track RAIN'),
    ('05_box_seat', 'box_seat', 'RAIN', 0.0, dict(), None, 'box_seat RAIN'),
    ('06_market', 'market', 'RAIN', 0.0, dict(), None, 'market RAIN'),
    ('07_puddle_low', 'puddle_low', 'RAIN', 0.0, dict(), None, 'puddle_low RAIN'),
    ('08_rank_rush', 'rank_rush', 'RAIN', 0.0, dict(rush=0.0), None, 'rank_rush RAIN rush 0'),
    ('09_wide_dusk', 'street_wide', 'DUSK_RAIN', 0.0, dict(), None, 'street_wide DUSK_RAIN'),
    ('10_high_dusk', 'street_high', 'DUSK_RAIN', 0.0, dict(umb=0.0), None, 'street_high DUSK_RAIN'),
    ('11_box_dusk', 'box_seat', 'DUSK_RAIN', 0.5, dict(), None, 'box_seat DUSK_RAIN'),
    ('12_umb_05', 'street_high', 'RAIN', 1.0, dict(umb=0.5), None, 'umbrellas 0.5 (street_high B)'),
    ('13_umb_10', 'street_high', 'RAIN', 1.0, dict(umb=1.0), None, 'umbrellas 1.0 (street_high B)'),
    ('14_busy_0', 'coach_low', 'RAIN', 0.0, dict(busy=0.0), None, 'coach_low rank empty (busy 0)'),
    ('15_pink', 'box_seat', 'RAIN', 1.0, dict(pink=1.0), None, 'box_seat pink umbrella on'),
    ('16_rush_1', 'rank_rush', 'RAIN', 0.0, dict(rush=1.0, busy=0.5), None, 'rank_rush rush 1, busy 0.5'),
    ('17_rush_wide', 'rank_rush', 'RAIN', 1.0, dict(rush=1.0, busy=1.0), None, 'rank_rush B, rush 1, busy 1'),
    ('18_mud', 'puddle_low', 'RAIN', 0.0, dict(mud=0.4), _mud_coach, 'puddle_low mud splash t 0.4'),
    ('19_throw', 'market', 'RAIN', 1.0, dict(), _throw, 'market cabbage mid-arc (f 18 of 10-22)'),
    ('20_dusk_rush', 'rank_rush', 'DUSK_RAIN', 1.0, dict(rush=0.7, busy=1.0), None, 'rank_rush DUSK_RAIN rush 0.7'),
]
if __name__ == '__main__':
    want = sys.argv[1:]; os.makedirs(os.path.join(HERE, 'final'), exist_ok=True); logp = os.path.join(HERE, 'final_log.txt')
    log = json.load(open(logp + '.json')) if os.path.exists(logp + '.json') else {}
    for (name, preset, light, u, state, extra, label) in TILES:
        if want and name not in want: continue
        fig = 'rush' if 'rush' in state else ('umb' if state.get('umb', 0) > 0 else False)
        A = S.shot(preset, light, u=u, figures=fig)
        S.apply_state(state)
        if extra: extra(A)
        bpy.context.view_layer.update()
        cam = bpy.context.scene.camera; heads = {}
        for (nm, role, umb) in S.staged(preset, u):
            x, y, z = S.STAND[nm]['pos']; px = S.project_px(cam, (x, y, z + S.PH_ROLES[role][1])); heads[nm] = [round(px[0]), round(px[1])]
        w, c = S.render(os.path.join(HERE, 'final', name + '.png'))
        log[name] = dict(label=label, wall=round(w, 1), cpu=round(c, 1), heads=heads); json.dump(log, open(logp + '.json', 'w'), indent=1)
        print('%s %.1f s wall %.1f s cpu heads %s' % (name, w, c, heads), flush=True)
    with open(logp, 'w') as f:
        for k, v in sorted(log.items()): f.write('%s | %s | wall %.1f s | cpu %.1f s | heads(px) %s\n' % (k, v['label'], v['wall'], v['cpu'], v['heads']))
