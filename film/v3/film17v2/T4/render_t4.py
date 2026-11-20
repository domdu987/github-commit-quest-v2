"""python3 render_t4.py <g0> <g1> <out_dir>   (resumes: skips frames > 50 kB)"""
import sys, os, time, math
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import t4lib as L
from t4lib import P, bpy, cast17, Vector, actors
import numpy as np

def build_assign(g):
    """story poses for every T4 card on frame g. returns (assign, bert_target) ; bert_target = (kind, victim anchor or None)"""
    a = {}; W = L.WALK
    # prisoner_s: walks station to station, otherwise stands
    ws = W['prisoner_s'][g]
    base_p = cast17.STORY17['prisoner_standing_a'][1]
    if ws['speed'] > 0.05:
        a['prisoner_s'] = (L.reg('p4_ps_%d' % g, 'prisoner_a', L.walker('prisoner_a', base_p, 'prisoner_s', g)), {})
    else: a['prisoner_s'] = ('prisoner_standing_a', {})
    for q, st in (('queue0', 'prisoner_standing_b'), ('queue1', 'prisoner_standing_c')):
        if not L.too_close(q, g): a[q] = (st, {})
    if not L.too_close('clerk', g):
        wc = W['clerk'][g]; a['clerk'] = ('gendarme_standing_b', {})
    wa = W['clerk_arch'][g]
    if not L.too_close('clerk_arch', g):
        a['clerk_arch'] = (L.reg('p4_ca_%d' % g, 'gendarme_a', cast17.cycle('gendarme_a', wa['phase'], 'walk', 1 if math.cos(math.radians(wa['heading'])) >= 0 else -1, base=cast17.STORY17['gendarme_standing_a'][1], speed=0.8)), {}) if wa['speed'] > 0.05 else ('gendarme_standing_a', {})
    # bertillon
    wb = W['bertillon'][g]; moving = wb['speed'] > 0.05; run = wb['speed'] > 1.9
    if g < 955: kind = 'measure'
    elif g < 971: kind = 'transit'
    elif g < 991: kind = 'write'
    elif g < 1030: kind = 'card'
    else: kind = 'insert'
    return a, kind

def bert_pose(g, kind, mirror=False, target=None):
    wb = L.WALK['bertillon'][g]; moving = wb['speed'] > 0.05 and g < 1030
    name = {'measure': 'bertillon_measuring', 'transit': 'bertillon_neutral', 'write': 'bertillon_writing', 'card': 'bertillon_holding_card', 'insert': 'bertillon_holding_card'}[kind]
    cast, pose = cast17.STORY17[name]; pose = dict(pose)
    if mirror: pose['mirror'] = True
    if kind == 'insert': pose['prop_r'] = dict(pose['prop_r'], angle=90)
    if g >= 1045 and kind == 'insert': pose.pop('prop_r', None)     # the card is fully inside the drawer: no card in the glove
    if target is not None: pose = cast17.hand_for_anchor(cast, pose, 'r', ('card' if kind == 'insert' else 'calipers') + ('_l' if mirror else '_r'), target)
    if moving:
        arms = 'l' if kind in ('measure', 'card', 'drawer') else 'both'
        cyc = cast17.cycle(cast, wb['phase'], 'run' if wb['speed'] > 1.9 else 'walk', 1, base=pose, arms=arms)
        pose['legs'] = cyc['legs']; pose['lean'] = cyc.get('lean', 0); pose['head_roll'] = cyc.get('head_roll', 0); pose['head_dy'] = cyc.get('head_dy', 0)
        pose['arm_l'] = cyc['arm_l']
        if arms == 'both': pose['arm_r'] = cyc['arm_r']
    return L.reg('p4_b_%d' % g, cast, pose)

def ramp(g, a, b): return max(0.0, min(1.0, (g - a) / float(b - a)))

OFF_REF = {}
BOPT = {}
def stage_frame(g):
    sc = bpy.context.scene; sc.frame_set(g + 1); cam = sc.camera; bpy.context.view_layer.update(); L.clean(); camloc = Vector(cam.location)
    assign, kind = build_assign(g); mirror = kind in ('measure', 'insert')    # calipers / card go to the screen-left (prisoner on the left; drawers on the wall at x 13)
    global BOPT
    BOPT = {}
    if g >= 1018:      # director: he stops beside the cabinet (eased from g1018): 0.5 m to the right of the MOYEN mouth on screen, 0.7 m deeper than the cabinet front, re-solved every frame because the camera is still moving
        import math as _m
        c = cam.matrix_world.translation; fw = cam.matrix_world.to_quaternion() @ Vector((0, 0, -1)); f = Vector((fw.x, fw.y, 0)).normalized(); rr = Vector((f.y, -f.x, 0))
        M = Vector((L.CAB['cx'] + 0.10, L.CAB['cy'] - 0.30, 0)); a_ = (M - c).dot(f); b_ = (M - c).dot(rr); a2 = a_ - 0.20; b2 = (b_ + 0.55) * a2 / a_
        pos = Vector((c.x, c.y, 0)) + f * a2 + rr * b2
        p = P.cast_pos(L.CASTD['bertillon'], g); r = ramp(g, 1018, 1030); BOPT = {'dx': (pos.x - p[0]) * r, 'dy': (pos.y - p[1]) * r}
    L.set_mid_drawer(g)
    assign['bertillon'] = (bert_pose(g, kind, mirror), BOPT)
    acts = P.stage_cast2('T4', g, assign); ab = acts['bertillon']; ps = acts['prisoner_s']; info = {}
    if kind == 'measure':
        tip = L.L2W(ab, cam, cast17_anchor(g, kind, mirror, 'calipers'))
        ox, x, y, z, s = L._basis(ps, cam); head = L.L2W(ps, cam, (0.0, 0.0)); want = tip + x * (-0.42 * s)      # head centre 0.42 D left of the jaw tips: the jaws grip the head's near edge
        want = want - 0.0 * z; d = want - head; dy = (L.L2W(ab, cam, (0.0, 0.0)) - head).dot(Vector((0, 1, 0))) + 0.12   # same depth as Bertillon, 12 cm behind him (his arm in front)
        off = {'dx': d.x, 'dy': dy}; L.clean_actor('prisoner_s'); acts['prisoner_s'] = P.stage_cast2('T4', g, {'prisoner_s': (assign['prisoner_s'][0], off)})['prisoner_s']; info = off
        # jaw tips onto the EAR (head-centre height, the prisoner's near side edge): re-pose Bertillon's arm with the glove holding the beam
        ox, x, y, z, s = L._basis(acts['prisoner_s'], cam); head = L.L2W(acts['prisoner_s'], cam, (0.0, 0.0)); ear = head + x * (0.47 * s) - z * (0.05 * s)
        tgt = L.to_local_on_plane(ab, cam, ear, camloc); L.clean_actor('bertillon'); acts['bertillon'] = P.stage_cast2('T4', g, {'bertillon': (bert_pose(g, kind, mirror, tgt), {})})['bertillon']; info['ear_tgt'] = tgt[0]
    if kind != 'measure' and g >= 955 and g < 995:     # the measuring offset of the prisoner ramps out (director-approved), no pop at g955
        if not OFF_REF:
            sc.frame_set(954 + 1); bpy.context.view_layer.update(); _, _, i0 = stage_frame_measure(954); OFF_REF.update(i0); sc.frame_set(g + 1); bpy.context.view_layer.update(); L.clean(); acts = P.stage_cast2('T4', g, assign); ab = acts['bertillon']; ps = acts['prisoner_s']
        k = 1.0 - ramp(g, 955, 995); off = {'dx': OFF_REF['dx'] * k, 'dy': OFF_REF['dy'] * k}
        L.clean_actor('prisoner_s'); acts['prisoner_s'] = P.stage_cast2('T4', g, {'prisoner_s': (assign['prisoner_s'][0], off)})['prisoner_s']; info = off
    if kind == 'insert':
        MZ = L.CAB['MZ']; cx = L.CAB['cx']; yf = L.CAB['cy'] - 0.30; z_t = MZ + 0.15
        u = ramp(g, 1032, 1044); zc = (z_t + 0.32) * (1 - u) + (z_t - 0.12) * u      # the card centre sinks from above the drawer mouth to inside it (g1032-1044)
        W = Vector((cx + 0.10, yf - 0.20, zc)); tgt = L.to_local_on_plane(ab, cam, W, camloc)
        L.clean_actor('bertillon'); acts['bertillon'] = P.stage_cast2('T4', g, {'bertillon': (bert_pose(g, kind, mirror, tgt), BOPT)})['bertillon']; info = {'card_z': zc}
    for nm in ('queue0', 'queue1', 'clerk', 'clerk_arch'):      # background cards: gone when the head is bigger than 190 px (the card is on the lens; the origin's head-centre test missed these)
        if nm in acts:
            p0 = actors.local_to_screen(acts[nm], cam, (0.0, 0.0)); p1 = actors.local_to_screen(acts[nm], cam, (0.5, 0.0)); dpx = 2 * abs(p1[0] - p0[0])
            if dpx > 190 or p0[2] < 0.3: L.clean_actor(nm); del acts[nm]
    return acts, kind, info

def stage_frame_measure(g): return stage_frame(g)

def cast17_anchor(g, kind, mirror, which):
    c, p = cast17.STORY17['p4_b_%d' % g]; an = L.puppet.figure(c, p, 'q')['anchors']; key = which + ('_l' if mirror else '_r'); return an[key]

def render(g, out):
    acts, kind, info = stage_frame(g)
    bpy.context.scene.render.filepath = out; bpy.ops.render.render(write_still=True); P.grade2(out); return kind, info

if __name__ == '__main__':
    g0, g1, od = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]; os.makedirs(od, exist_ok=True); A = L.setup()
    step = int(sys.argv[4]) if len(sys.argv) > 4 else 1
    for g in range(g0, g1 + 1, step):
        out = os.path.join(od, 'g_%04d.png' % g)
        if os.path.exists(out) and os.path.getsize(out) > 50000: continue
        t = time.time(); k = render(g, out); print('g%d %s %s %.0fs' % (g, k[0], {a: round(b, 2) for a, b in k[1].items()}, time.time() - t), flush=True)
