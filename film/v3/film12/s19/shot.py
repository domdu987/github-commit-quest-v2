#!/usr/bin/env python3
"""s19: shots 19-21 of film 12 (the aha, t 44.66-52.64 s): one gentleman opens his umbrella, then a second and third along the pavement (reverse),
then the whole street is a sea of umbrellas (street_high crane), Hanway smiling among them.   One process = one location (street.py) with a shot() rebuild per shot.

usage: python3 shot.py draft|final SHOT[,SHOT..] [gspec]     SHOT = 19 | 20 | 21      gspec e.g. 1334:1409 or 1340,1350 (default: whole shot + handles)
       THREADS=2 SAMPLES=20 env respected (final).  draft = 360x640 / 6 samples -> draft/, final = 720x1280 -> frames/."""
import os, sys, json, math, time
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c12 as C
import bpy
from mathutils import Vector
S, cast12 = C.S, C.cast12

SHOTS = {  # id: (preset, g0, g1) planned range (cut at g1 + 1); handles added around the TAKE only
    19: ('street_wide',     C.g_bound(44.66), C.g_bound(47.00) - 1),
    20: ('street_wide_rev', C.g_bound(47.00), C.g_bound(49.00) - 1),
    21: ('street_high',     C.g_bound(49.00), C.g_bound(52.64) - 1),
}
HANDLE = 6
# closer custom moves so the acting reads (same family as the approved street_wide / street_wide_rev tiles)
S.CAMS['s19_wide'] = dict(loc=(1.0, -12.0, 3.3), look_at=(0.3, 40.0, 6.2), lens=22, loc_b=(-1.4, 3.0, 2.9), look_b=(-2.4, 14.0, 4.7), lens_b=22)
S.CAMS['s20_rev'] = dict(loc=(-3.8, 52.0, 3.4), look_at=(0.0, 10.0, 6.0), lens=22, loc_b=(-3.4, 44.0, 3.3), look_b=(-0.2, 10.0, 6.0), lens_b=22)
PRESET_CAM = {19: 's19_wide', 20: 's20_rev', 21: 'street_high'}
TAKE_G0, TAKE_G1 = SHOTS[19][1] - HANDLE, SHOTS[21][2] + HANDLE
def shot_range(sid):
    p, a, b = SHOTS[sid]
    return (a - HANDLE if sid == 19 else a), (b + HANDLE if sid == 21 else b)

# -------- narration events (film frames) --------
G_OPEN1 = C.g_of(45.50)           # umbrella pop 1 (cue 45.5)
G_OPEN2 = C.g_of(47.20)
G_OPEN3 = C.g_of(47.80)
G_OPEN4 = C.g_of(48.30)

def umb_k(g):
    """set_crowd_umbrellas value for film frame g (0 until shot 20; pops staggered one by one; all open by ~50.7 s)"""
    if g < 1412: return 0.0
    k = 0.45 * C.smooth((g - 1411) / 58.0)
    if g >= 1470: k = 0.45 + 0.55 * C.smooth((g - 1470) / 52.0)
    return k

def open_pose(member, g, g_open, dur=12, stare=None):
    """gentleman opening his umbrella: furled + staring -> half open (umb_open .15 -> .9) -> open overhead (smiling). returns (cast, pose)"""
    if g < g_open:   return C.story('%s_open_1' % member)
    u = (g - g_open) / float(dur)
    if u < 1.0:
        c, p = C.story('%s_open_2' % member); p['umb_open'] = round(0.15 + 0.75 * C.smooth(u) // 0.1 * 0.1 + 0.0, 2) if False else round(0.15 + 0.75 * round(u * 6) / 6.0, 2); return c, p
    return C.story('%s_open_3' % member)

class Shot(object):
    def __init__(self, sid, quality):
        self.sid = sid; self.preset, self.g0, self.g1 = SHOTS[sid]; self.q = quality
        a, b = shot_range(sid); self.a, self.b = a, b
        t0 = time.time()
        S.shot(self.preset, 'RAIN', u=0.5, placeholders=False, figures=False, quality=quality)
        self.A = S.STATE.get('A') if hasattr(S, 'STATE') else None
        self.sc = bpy.context.scene; self.cards = C.Cards(); self.slotcards = {}
        S.rain(1.0); S.set_rank_busy(1.0)
        self.build_static()
        print('shot %d built in %.1f s' % (sid, time.time() - t0), flush=True)

    # ---- the static crowd at the umbrella slots (bare hunched men -> same men under their 3D umbrella)
    def build_static(self):
        cl = self.sc.camera.matrix_world.translation; slots = S.STATE['umb_slots']
        ymin = {19: 3.0, 20: -9.0, 21: -9.0}[self.sid]; ymax = {19: 70.0, 20: 36.0, 21: 70.0}[self.sid]
        self.slots = [s for s in slots if ymin <= s['feet'][1] <= ymax]
        keep = set(x['i'] for x in self.slots)
        for x in slots:
            if x['i'] not in keep:
                for nm in ('umb_%02d' % x['i'],):
                    o = bpy.data.objects.get(nm)
                    if o is not None: o.hide_render = True
        mem = ['crowd_man_a', 'crowd_man_c', 'crowd_man_d', 'crowd_man_a']
        for s in self.slots:
            m = mem[s['i'] % 4]
            cb, pb = cast12.cycle_frame(m + '_walk_hat', (s['i'] * 0.137) % 1.0, facing=1)
            co, po = C.story(m + '_open_3', dict(prop_r=None))
            mark = s['feet']; mir = (s['i'] % 2 == 1)
            bare = C.S.cast_card('actor_sb%02d' % s['i'], cb, pb, mark, cl, 0.0, mirror=mir)
            opn = C.S.cast_card('actor_so%02d' % s['i'], co, po, mark, cl, 0.0, mirror=mir)
            for o in (bare, opn): o.visible_glossy = True
            self.slotcards[s['i']] = (bare, opn, s)

    def update_static(self, g, w, tilt):
        cl = self.sc.camera.matrix_world.translation; k = umb_k(g); ph = g * 0.11
        for i, (bare, opn, s) in self.slotcards.items():
            is_open = k > s['open_at'] + 0.012
            bare.hide_render = is_open; opn.hide_render = not is_open
            for o in (bare, opn):
                d = Vector(cl) - Vector(o.location); yaw = math.atan2(d.x, -d.y)
                sway = 0.025 * math.sin(ph + i * 1.7)
                o.rotation_euler = (math.radians(-tilt), sway * 0.6, yaw)
                o.location = (s['feet'][0], s['feet'][1], s['feet'][2] + 0.04 * abs(math.sin(ph * 1.3 + i)))
        S.set_crowd_umbrellas(k)

    # ---- per-shot acting
    def acting(self, g, w, tilt):
        cl = self.sc.camera.matrix_world.translation; Cd = self.cards; sid = self.sid
        rep = {}
        if sid == 19:
            hy = 17.0 - 0.1 * (g - 1334); hx = -0.9 - 0.3 * (g - 1334) / 80.0
            c, p = C.cyc('hanway_walk_umbrella', g); Cd.put('hanway', c, p, (hx, hy, 0.0), cl, rim=C.RIM)
            c, p = open_pose('crowd_man_a', g, G_OPEN1); c, p = c, C.blinkpose(p, g, 80)
            Cd.put('gent', c, p, (-3.4, 9.0, 0.0), cl, mirror=True)
            c, p = C.cyc('crowd_man_b_walk_soaked', g + 5); Cd.put('man_b', c, p, (-6.8, 24.0 - 0.085 * (g - 1334), 0.28), cl)
            c, p = C.cyc('crowd_woman_a_walk_umbrella', g + 3); Cd.put('woman', c, p, (7.5, 30.0 - 0.085 * (g - 1334), 0.28), cl)
            c, p = C.story('coachman_grin_drop'); Cd.put('coach', c, C.blinkpose(p, g, 100), (3.55, 18.6, 4.22), cl, mirror=True)
            rep['hanway'] = (hx, hy, 0.0)
        elif sid == 20:
            hy = 20.0 + 0.075 * (g - 1410)
            c, p = C.cyc('hanway_walk_umbrella', g); Cd.put('hanway', c, p, (-0.9, hy, 0.0), cl, rim=C.RIM)
            c, p = open_pose('crowd_man_c', g, G_OPEN2); Cd.put('gent_a', c, C.blinkpose(p, g, 85), (-4.0, 30.0, 0.0), cl)
            c, p = open_pose('crowd_man_d', g, G_OPEN3); Cd.put('gent_b', c, C.blinkpose(p, g, 95, 7), (1.6, 26.0, 0.0), cl, mirror=True)
            c, p = open_pose('crowd_man_a', g, G_OPEN4); Cd.put('gent_c', c, C.blinkpose(p, g, 75, 3), (-7.4, 34.0, 0.28), cl)
            rep['hanway'] = (-0.8, hy, 0.0)
        else:
            hy = 20.0 - 0.055 * (g - 1470); hx = -1.0
            c, p = C.cyc('hanway_smile_walk', g); Cd.put('hanway', c, p, (hx, hy, 0.0), cl, tilt=tilt, rim=C.RIM)
            c, p = C.story('coachman_grin_drop'); Cd.put('coach', c, p, (3.55, 18.6, 4.22), cl, tilt=tilt, mirror=True)
            rep['hanway'] = (hx, hy, 0.0)
        for nm, ob in Cd.d.items():                                         # keep every card facing the camera, tilt for the crane
            d = Vector(cl) - Vector(ob.location); ob.rotation_euler = (math.radians(-tilt if sid == 21 else 0.0), 0, math.atan2(d.x, -d.y))
        return rep

    def pose(self, g):
        w = C.mixu((g - self.a) / float(self.b - self.a))
        cam = C.set_cam(PRESET_CAM[self.sid], w); tilt = 0.0
        if self.sid == 21: tilt = 0.85 * C.cam_pitch_deg(PRESET_CAM[self.sid], w)
        self.sc.frame_set(g)
        rep = self.acting(g, w, tilt)
        self.update_static(g, w, tilt)
        bpy.context.view_layer.update()
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
