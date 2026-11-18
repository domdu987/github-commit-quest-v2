#!/usr/bin/env python3
"""s19 (v2): shots 19-21 of film 12 (the aha, t 44.66-52.64 s).  Gentleman opens his umbrella (3-stage cast12 poses blended so the umbrella is always in his hand),
three more open one by one (reverse), then a crowd of ~100 men (cast12 cards, each with his own adult-scale coloured 3D umbrella) fills the street seen from a crane.
usage: python3 shot.py draft|final SHOT[,SHOT..] [gspec]    (THREADS=2 SAMPLES=28 env; draft = 360x640 / 6 samples -> draft/, final -> frames/)"""
import os, sys, json, math, time, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c12 as C
import bpy
from mathutils import Vector
S, cast12 = C.S, C.cast12
PT = S.PT; M = None

SHOTS = {19: ('s19_wide', C.g_bound(44.66), C.g_bound(47.00) - 1),
         20: ('s20_rev',  C.g_bound(47.00), C.g_bound(49.00) - 1),
         21: ('s21_crane', C.g_bound(49.00), C.g_bound(52.64) - 1)}
HANDLE = 6
S.CAMS['s19_wide']  = dict(loc=(0.8, -4.0, 3.1), look_at=(-0.6, 18.0, 4.8), lens=22, loc_b=(-1.6, 3.6, 2.8), look_b=(-1.8, 14.0, 4.5))
S.CAMS['s20_rev']   = dict(loc=(-3.7, 40.0, 3.2), look_at=(0.9, 4.0, 5.4), lens=22, loc_b=(-3.3, 33.0, 3.1), look_b=(0.7, 4.0, 5.4))
S.CAMS['s21_crane'] = dict(loc=(-2.8, -6.0, 20.0), look_at=(0.3, 24.0, 2.0), lens=22, loc_b=(-1.8, 1.0, 12.5), look_b=(0.2, 22.0, 2.5))
def shot_range(sid):
    p, a, b = SHOTS[sid]; return (a - HANDLE if sid == 19 else a), (b + HANDLE if sid == 21 else b)

G_OPEN = dict(g0=C.g_of(45.50), g1=C.g_of(47.20), g2=C.g_of(47.80), g3=C.g_of(48.30))     # pop cues
HANWAY_X = -1.0
# the four sprite gentlemen (always there, they open one after another)
GENTS = dict(g0=('crowd_man_a', (-3.4, 10.0)), g1=('crowd_man_c', (-5.2, 21.0)), g2=('crowd_man_d', (1.2, 17.0)), g3=('crowd_man_a', (-3.3, 26.5)))

def umb_k(g):
    if g < 1412: return 0.0
    s = C.smooth((g - 1412) / 58.0); k = 0.45 * s ** 1.4
    if g >= 1470: k = 0.45 + 0.55 * C.smooth((g - 1470) / 50.0)
    return k

def lerp(a, b, t): return a + (b - a) * t
def blend_open(member, g, g_open, dur=14):
    """furled-and-staring -> umbrella half open -> open overhead, always in his right hand (arm / angle / umb_open blended), mouth shut."""
    c, p1 = C.story('%s_open_1' % member); _, p3 = C.story('%s_open_3' % member)
    u = (g - g_open) / float(dur)
    if u <= 0: p = dict(p1); p['mouth'] = 'flat'; p['expr'] = 'neutral'; return c, p
    u = min(1.0, round(u * 12) / 12.0); e = C.smooth(u)
    p = dict(p3); p['mouth'] = 'flat' if u < 0.85 else 'smile'; p['expr'] = 'surprised' if False else ('neutral' if u < 0.5 else 'happy')
    for k in ('yaw', 'pitch', 'head_roll'): p[k] = lerp(p1.get(k, 0), p3.get(k, 0), e)
    p['gaze'] = (lerp(p1['gaze'][0], 0.0, e), 0.0)
    h1, h3 = p1['arm_r']['hand'], p3['arm_r']['hand']
    p['arm_r'] = dict(hand=(lerp(h1[0], h3[0], e), lerp(h1[1], h3[1], e)), bend=lerp(p1['arm_r']['bend'], p3['arm_r']['bend'], e))
    p['prop_r'] = dict(type='umbrella_black', angle=lerp(-62, -98, e)); p['umb_open'] = round(max(0.0, (u - 0.15) / 0.7), 2) if u < 0.85 else 1.0
    p['umb_open'] = min(1.0, p['umb_open'])
    return c, p

def make_people(sid_unused=None):
    """deterministic crowd of walking men: dict(i, pos, member, mat, thr, r)"""
    rs = random.Random(12); mats = ['umb_green', 'umb_ochre', 'umb_red', 'umb_brown', 'umb_blue', 'umb_dark', 'umb_green', 'umb_ochre', 'umb_red', 'umb_grey']
    keep_c = [Vector((p[0], p[1], 0)) for _, p in GENTS.values()]
    pts = []
    def ok(x, y):
        if abs(x) > 8.6: return False
        if x > 1.1 and 14.0 < y < 78.0 and x < 6.2: return False          # the rank's coaches and horses
        if -2.3 < x < 0.5 and 5.0 < y < 26.0: return False                # Hanway's corridor
        if any((x - c.x) ** 2 + (y - c.y) ** 2 < 3.6 ** 2 for c in keep_c): return False
        return all((x - a) ** 2 + (y - b) ** 2 > 2.45 ** 2 for a, b in pts)
    for _ in range(4000):
        if rs.random() < 0.5: x = rs.choice([-1, 1]) * rs.uniform(6.9, 8.6)                 # pavements
        else: x = rs.uniform(-5.4, 5.2)
        y = rs.uniform(-8.0, 64.0)
        if ok(x, y): pts.append((x, y))
    ppl = []
    for i, (x, y) in enumerate(pts):
        d = math.hypot(x - HANWAY_X, y - 14.0); ppl.append(dict(i=i, pos=(x, y, 0.28 if abs(x) > 6.35 else 0.0), member=['crowd_man_a', 'crowd_man_c', 'crowd_man_d'][i % 3],
            mat=mats[rs.randrange(len(mats))], d=d + rs.uniform(-4, 4), r=rs.uniform(1.1, 1.3), mir=bool(i % 2)))
    order = sorted(range(len(ppl)), key=lambda j: ppl[j]['d'])
    for rank, j in enumerate(order): ppl[j]['thr'] = 0.03 + 0.9 * rank / len(ppl)
    return ppl

class Shot(object):
    def __init__(self, sid, quality):
        global M
        self.sid = sid; self.cam_key, self.g0, self.g1 = SHOTS[sid]; self.a, self.b = shot_range(sid)
        t0 = time.time()
        S.shot(S.PRESETS[0] if False else 'street_wide', 'RAIN', u=0.5, placeholders=False, figures=False, quality=quality)
        M = S.STATE['M']; self.sc = bpy.context.scene; self.cards = C.Cards()
        S.rain(1.0); S.set_rank_busy(1.0); S.set_crowd_umbrellas(0.0)
        for o in list(bpy.data.objects):
            if o.name.startswith(('umb_', 'crowd_')) and o.name[:4] in ('umb_', 'crow') and o.name != 'cam': o.hide_render = True      # the set's own oversized umbrellas / blocky people
        self.ppl = make_people(); self.build_people()
        print('shot %d built (%d people) in %.1f s' % (sid, len(self.ppl), time.time() - t0), flush=True)

    def build_people(self):
        cl = self.sc.camera.matrix_world.translation; self.obj = {}
        for p in self.ppl:
            m = p['member']; cb, pb = cast12.cycle_frame(m + '_walk_hat', (p['i'] * 0.137) % 1.0, facing=1); pb = dict(pb, mouth='flat', expr='unimpressed')
            co, po = C.story(m + '_open_3', dict(prop_r=None, mouth='smile'))
            bare = S.cast_card('actor_pb%03d' % p['i'], cb, pb, p['pos'], cl, 0.0, mirror=p['mir']); opn = S.cast_card('actor_po%03d' % p['i'], co, po, p['pos'], cl, 0.0, mirror=p['mir'])
            mb = PT.MB() if hasattr(PT, 'MB') else S.MB(); r = p['r']
            PT.umbrella(mb, M, Vector((0, 0, 2.15)), r=r, h=0.7, mat=p['mat'], n=10, pole_to=Vector((0, 0, 0)))
            um = S._obj(mb, 'myumb_%03d' % p['i'], S.STATE['SHOT']); um.scale = (0.001,) * 3
            for o in (bare, opn): o.visible_glossy = True
            S.no_bounce(um); um.visible_glossy = False
            self.obj[p['i']] = (bare, opn, um)

    def update_people(self, g, tilt, cam):
        cl = cam.matrix_world.translation; k = umb_k(g); ph = g * 0.2; drift = -0.008 * (g - 1334)
        for p in self.ppl:
            bare, opn, um = self.obj[p['i']]; x, y, z = p['pos']; y2 = y + drift
            bob = 0.05 * abs(math.sin(ph + p['i'] * 1.3)); sway = 0.03 * math.sin(ph * 0.5 + p['i'])
            dx, dy = cl.x - x, cl.y - y2; dist = math.hypot(dx, dy); yaw = math.atan2(dx, -dy)
            px = S.project_px(cam, (x, y2, z + 3.4)); vis = dist > 7.5 and px[2] > 0 and px[1] < 860 and -40 < px[0] < 760
            s = max(0.0, min(1.0, (k - p['thr']) / 0.045)); s = C.smooth(s); is_open = s > 0.0
            for o in (bare, opn):
                o.location = (x, y2, z + bob); o.rotation_euler = (math.radians(-tilt), sway, yaw)
            bare.hide_render = not vis or is_open; opn.hide_render = not vis or not is_open
            hz = 1.95 + bob; away = Vector((-dx, -dy, 0)).normalized() * 0.3
            um.location = (x + away.x, y2 + away.y, z + hz + 0.0); um.scale = (max(s, 0.001),) * 3; um.hide_render = not vis or not is_open; um.rotation_euler = (0, 0, p['i'])

    def hanway_pose(self, g):
        sid = self.sid
        if sid == 19: return 'hanway_walk_umbrella', (HANWAY_X - 0.3 * (g - 1334) / 80.0, 17.0 - 0.1 * (g - 1334))
        if sid == 20: return 'hanway_walk_umbrella', (HANWAY_X, 13.0 + 0.07 * (g - 1410))
        return 'hanway_smile_walk', (HANWAY_X, 18.0 - 0.055 * (g - 1470))

    def acting(self, g, tilt):
        cl = self.sc.camera.matrix_world.translation; Cd = self.cards; sid = self.sid; T = tilt if sid == 21 else 0.0
        name, (hx, hy) = self.hanway_pose(g); c, p = C.cyc(name, g); p = dict(p, mouth=p.get('mouth', 'smile') if sid == 21 else 'flat') if False else p
        Cd.put('hanway', c, p, (hx, hy, 0.0), cl, tilt=T, rim=C.RIM)
        for key, (m, (x, y)) in GENTS.items():
            if sid == 19 and key != 'g0': pass
            c, p = blend_open(m, g, G_OPEN[key]); mir = (x < HANWAY_X) if sid == 20 else (x > HANWAY_X)
            Cd.put(key, c, C.blinkpose(p, g, 85, hash(key) % 40), (x, y, 0.0), cl, tilt=T, mirror=mir)
        if sid != 20:
            c, p = C.story('coachman_grin_drop'); Cd.put('coach', c, C.blinkpose(p, g, 100), (3.55, 18.6, 4.22), cl, tilt=T, mirror=True)
        for nm, ob in Cd.d.items():
            d = Vector(cl) - Vector(ob.location); ob.rotation_euler = (math.radians(-T), 0, math.atan2(d.x, -d.y))
        return dict(hanway=(hx, hy))

    def pose(self, g):
        w = C.mixu((g - self.a) / float(self.b - self.a)); cam = C.set_cam(self.cam_key, w)
        tilt = 0.85 * C.cam_pitch_deg(self.cam_key, w) if self.sid == 21 else 0.0
        self.sc.frame_set(g); rep = self.acting(g, tilt); self.update_people(g, tilt, cam); bpy.context.view_layer.update()
        cam = self.sc.camera; heads = {}
        for nm, ob in self.cards.d.items():
            x, y, z = ob.location; px = S.project_px(cam, (x, y, z + 3.2)); heads[nm] = [round(px[0]), round(px[1])]
        return dict(g=g, w=round(w, 4), k=round(umb_k(g), 3), tilt=round(tilt, 1), heads=heads)

def parse(spec):
    out = []
    for part in spec.split(','):
        if ':' in part: a, b = part.split(':'); out += list(range(int(a), int(b) + 1))
        else: out.append(int(part))
    return out

if __name__ == '__main__':
    mode = sys.argv[1]; shots = [int(s) for s in sys.argv[2].split(',')]; spec = sys.argv[3] if len(sys.argv) > 3 else None
    quality = 'preview' if mode == 'draft' else 'final'
    out = os.path.join(HERE, 'draft' if mode == 'draft' else 'frames'); os.makedirs(out, exist_ok=True)
    for sid in shots:
        a, b = shot_range(sid); gs = [g for g in (parse(spec) if spec else range(a, b + 1)) if a <= g <= b]
        todo = [g for g in gs if not (os.path.exists(os.path.join(out, 'g_%04d.png' % g)) and os.path.exists(os.path.join(out, 'g_%04d.json' % g)))]
        print('shot %d: %d frames, %d to do' % (sid, len(gs), len(todo)), flush=True)
        if not todo: continue
        Sh = Shot(sid, quality)
        for g in todo:
            rep = Sh.pose(g); png = os.path.join(out, 'g_%04d.png' % g)
            w, c = S.render(png); rep.update(wall=round(w, 1), cpu=round(c, 1), mode=mode, samples=int(Sh.sc.cycles.samples))
            json.dump(rep, open(png[:-4] + '.json', 'w')); print('g %d  %.1f s  heads %s' % (g, w, rep['heads']), flush=True)
