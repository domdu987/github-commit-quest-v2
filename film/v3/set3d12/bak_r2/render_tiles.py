#!/usr/bin/env python3
"""Renders the contact-sheet tiles (720x1280, final quality, REAL cast12 cards at the stand points) into street_work/final/ and writes final_log.txt
(wall / CPU seconds, projected head pixels of every staged card). usage: python3 render_tiles.py [tile_name ...]  (default: all).  THREADS=2 SAMPLES=24 env respected."""
import sys, os, json, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, os.path.dirname(HERE)); os.environ.setdefault('SAMPLES', '24')
import street as S, bpy
from mathutils import Vector

def _drop(name):
    o = bpy.data.objects.get(name)
    if o: bpy.data.objects.remove(o, do_unlink=True)
def _mud(A):
    r = bpy.data.objects['coach_run']; r.location = (0.2, 14.6, 0.0); _drop('actor_hanway_mud')
    sys.path.insert(0, os.path.join(S.PROJ, 'v3', 'cast12')); sys.path.insert(0, os.path.join(S.PROJ, 'v3', 'cast10')); import cast12
    c, p = cast12.STORY12['hanway_mud_splash']; S.cast_card('actor_hanway_mud', c, p, (-4.3, 11.0, 0.0), bpy.context.scene.camera.matrix_world.translation, rim='#f2b25c')
def _ending(A):
    _drop('actor_box_a'); S.stage_cards([('box_a', 'coachman_sulk', (3.55, 18.6, 4.22), None)])
def _throw(A):
    S.throw('cabbage', (-5.0, 11.4, 5.0), (-2.45, 10.5, 5.2), 10, 22, bounce=(1.6, -1.8)); bpy.context.scene.frame_set(18)
def _queue(A):
    S.stage_cards([('q_a', 'man', (0.5, 21.0, 0.0), None), ('q_b', 'man_b', (0.2, 23.4, 0.0), None), ('q_c', 'woman', (0.6, 25.8, 0.0), None)])
def _rush(k, n=16):
    return lambda A: S.stage_rush_cards(k, n)
def _roll(A):
    S.roll_rank(1, 60, -14.0); bpy.context.scene.frame_set(34)
def _sulk(A):
    import cast12
def _bare(A):
    pass
TILES = [  # name, preset, light, u, state, extra, figures, label, cards
    ('01_hook_wide', 'street_wide', 'RAIN', 0.0, dict(), None, False, 'street_wide RAIN (hook)'),
    ('02_wide_low', 'street_wide_low', 'RAIN', 0.0, dict(), None, False, 'street_wide_low RAIN (shot 9)'),
    ('03_wide_rev', 'street_wide_rev', 'RAIN', 0.0, dict(umb=0.6), None, 'umb', 'street_wide_rev umb 0.6 (shot 20)'),
    ('04_high_hunched', 'street_high', 'RAIN', 0.0, dict(umb=0.0), None, 'umb', 'street_high RAIN bare heads (shot 4)'),
    ('05_coach_low', 'coach_low', 'RAIN', 0.0, dict(busy=1.0), None, False, 'coach_low busy 1 (shot 2)'),
    ('06_coach_close', 'coach_close', 'RAIN', 0.0, dict(busy=1.0), None, False, 'coach_close two-shot (shots 7, 15)'),
    ('07_hero_track', 'hero_track', 'RAIN', 0.0, dict(), None, False, 'hero_track RAIN (shots 3, 11)'),
    ('08_queue', 'hero_track', 'RAIN', 0.0, dict(), _queue, False, 'hero_track + rank queue (shot 18)'),
    ('09_box_face', 'box_seat', 'RAIN', 1.0, dict(), None, False, 'box_seat B (shots 6, 8)'),
    ('10_box_trio', 'box_trio', 'RAIN', 0.0, dict(), None, False, 'box_trio three coachmen (shots 2, 14)'),
    ('11_market', 'market', 'RAIN', 0.0, dict(), None, False, 'market RAIN (shot 5)'),
    ('12_puddle_low', 'puddle_low', 'RAIN', 0.0, dict(), None, False, 'puddle_low RAIN (shot 12)'),
    ('13_reveal', 'rank_rush', 'RAIN', 0.0, dict(rush=1.0, busy=1.0), _rush(1.0, 14), False, 'rank_rush REVEAL rush 1 busy 1 (shot 16)'),
    ('14_rush_dusk', 'rank_rush', 'DUSK_RAIN', 0.0, dict(rush=1.0, busy=1.0), _rush(1.0, 14), False, 'rank_rush DUSK_RAIN rush 1'),
    ('15_rank_rolling', 'rank_wide', 'RAIN', 0.0, dict(busy=1.0), _roll, False, 'rank_wide coaches rolling (shot 17)'),
    ('16_rank_idle', 'rank_idle', 'RAIN', 0.0, dict(busy=0.0), None, False, 'rank_idle busy 0 bored (shot 22)'),
    ('17_box_dusk', 'box_seat', 'DUSK_RAIN', 0.6, dict(), None, False, 'box_seat DUSK_RAIN (shot 14)'),
    ('18_wide_dusk', 'street_wide', 'DUSK_RAIN', 0.0, dict(), None, False, 'street_wide DUSK_RAIN'),
    ('19_high_dusk_bare', 'street_high', 'DUSK_RAIN', 1.0, dict(umb=0.0), None, 'umb', 'high DUSK bare heads, 1 umbrella (13)'),
    ('20_umb_05', 'street_high', 'RAIN', 1.0, dict(umb=0.5), None, 'umb', 'umbrellas 0.5 (street_high B)'),
    ('21_umb_10', 'street_high', 'RAIN', 1.0, dict(umb=1.0), None, 'umb', 'umbrellas 1.0 (street_high B)'),
    ('22_ending_pink', 'box_seat', 'RAIN', 0.55, dict(pink=1.0), _ending, False, 'box_seat pink umbrella, sulking (shot 23)'),
    ('23_mud', 'puddle_low', 'RAIN', 0.0, dict(mud=0.4), _mud, False, 'puddle_low mud splash t 0.4 (shot 12)'),
    ('24_throw', 'market', 'RAIN', 1.0, dict(), _throw, False, 'market cabbage mid-arc (frame 18 of 10-22)'),
    ('25_coach_dusk', 'coach_low', 'DUSK_RAIN', 1.0, dict(busy=1.0), None, False, 'coach_low DUSK_RAIN busy 1'),
]
if __name__ == '__main__':
    want = sys.argv[1:]; os.makedirs(os.path.join(HERE, 'final'), exist_ok=True); logp = os.path.join(HERE, 'final_log.txt')
    log = json.load(open(logp + '.json')) if os.path.exists(logp + '.json') else {}
    for (name, preset, light, u, state, extra, fig, label) in TILES:
        if want and name not in want: continue
        cards = 'cast'
        if name == '22_ending_pink': cards = 'cast'
        A = S.shot(preset, light, u=u, figures=fig, cards=cards)
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
