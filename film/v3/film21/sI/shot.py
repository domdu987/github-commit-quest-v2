#!/usr/bin/env python3
"""shot.py -- film 21 segment I (the AHA, the bridge jam).  g 1519..1639 (121 frames), narration 50.53-54.55, CUT in, no handles.
World: K.build_world(['bridge_deck','bridge_high']).  ONE continuous travelling camera (K.cam_path):
  f0-58   ride-along on the deck (outside the west rail, sliding north) on the jammed English column: it tries to turn back (ขาถอย, 52.3),
          two riders wedged nose to tail, a knight's helmet pops off (comic).
  f58-88  CRANE UP and back: straight down the bridge, two by two all along, everybody given up (nobody moving), "ก็ได้ทีละสองคน" 52.7.
  f89-    SNAP pull-out on "เหมือนกัน" (53.6 = g 1608), then a slow drift.
    python3 shot.py path_draft           10 fps 360x640 camera-path draft (no cast) -> path_draft.mp4
    python3 shot.py draft  a:b[:s]       drafts of local frames to draft/
    python3 shot.py final  a:b[:s]       finals (32 samples) to raw/
"""
import os, sys, json, math, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c21 as C
import numpy as np
bpy, K, Vector = C.bpy, C.K, C.Vector
lerp, clamp, sm, u_of = C.lerp, C.clamp, C.sm, C.u_of

G0, N = 1519, 121                       # film frame of local frame 0; 121 frames (1519..1639)
FPS = 30.0
G_SNAP = 89                             # local frame of the snap pull-out ("เหมือนกัน" 53.6 s -> g 1608)
G_TURN = (34, 60)                       # the column tries to turn back (ขาถอย 52.29 = local 52)
G_GIVEUP = 80                           # everybody gives up, faces north again
G_POP = 62                              # helmet pops
BX, DZ = K.BRIDGE_X, K.DECK_Z
LANE_W, LANE_E = BX - 0.62, BX + 0.62

# ------------------------------------------------------------------ camera
KEYS = [(-10, (-3.1, -7.2, 3.5), (0.3, -1.2, 3.3), 22.0),
        (0, (-3.6, -4.7, 3.5), (0.2, 0.0, 3.3), 22.0),          # starts 2.4 m from the set's foreground post (-2.4, -1.25) and slides away from the rail
        (16, (-5.8, -3.0, 3.6), (0.0, 1.6, 3.4), 22.0),
        (36, (-7.4, -1.8, 3.9), (0.0, 2.4, 3.4), 22.0),
        (66, (-6.8, 1.4, 4.6), (0.0, 3.0, 3.1), 22.0),
        (78, (-3.4, -14.0, 11.5), (0.0, 3.0, 2.2), 22.0),       # CRANE UP and back, fast
        (88, (-1.2, -40.0, 19.0), (0.0, 12.0, 1.8), 22.0),      # straight down the bridge
        (112, (-5.0, -66.0, 29.0), (0.0, 8.0, 1.5), 17.0),
        (121, (-6.5, -76.0, 33.0), (0.0, 8.0, 1.5), 16.0)]


def path_frame(f):
    """local frame -> path parameter: linear, then a SNAP (18 frames, about x2 speed) at G_SNAP, then a slower drift."""
    if f <= G_SNAP:
        return float(f)
    if f <= G_SNAP + 18:
        return G_SNAP + 24.0 * sm((f - G_SNAP) / 18.0)
    return G_SNAP + 24.0 + (f - G_SNAP - 18) * 0.28


def cam_at(f):
    return K.cam_path(None, KEYS, path_frame(f))


# ------------------------------------------------------------------ world and the 3D column
def build():
    t0 = time.time()
    A = K.build_world(['bridge_deck', 'bridge_high'])
    K.place_troops(A, 'bridge', 0)                                 # clear the default column; we build our own (jammed, some of it animated)
    return A


MATS = K.KNIGHT_MATS
ANIM = []                                                          # [(empty, base_yaw_deg, amp, t0, phase, wob)]


def build_column():
    rs = np.random.RandomState(21)
    ys = [7.2 - 3.0 * i for i in range(14)]                        # bunched up: 3 m pitch (horses are 2.4 m long)
    anim_slots = {(1, +1), (1, -1), (2, +1), (3, +1), (3, -1), (4, +1), (4, -1), (5, +1)}   # (pair index, lane sign) that turn; hero cards own (1,-1)/(2,-1)
    hero_slots = {(1, -1), (2, -1)}
    Bs = K.Batch(85)
    for i, y in enumerate(ys):
        for sx in (-1, 1):
            slot = (i, sx)
            if slot in hero_slots:
                continue
            m = MATS[(i * 2 + (0 if sx < 0 else 1)) % len(MATS)]
            coat = ['horse', 'horse_dk', 'horse'][rs.randint(0, 3)]
            tint = 0.85 + 0.3 * rs.rand()
            x = BX + 0.62 * sx
            if slot in anim_slots or (i, -sx) in anim_slots and False:
                Bh = K.Batch(90 + i * 2 + (0 if sx < 0 else 1))
                K.horse(Bh, (0, 0, 0), 0.0, coat=coat, trap=m[0], trim=m[1], tint=tint, rider=(m[0],))
                root = bpy.data.objects.new('turn_%d_%d' % (i, sx), None)
                bpy.context.scene.collection.objects.link(root)
                Bh.finalize('turnh_%d_%d' % (i, sx), parent=root)
                root.location = (x, y, DZ)
                ANIM.append(dict(root=root, x=x, y=y, i=i, sx=sx, amp=rs.uniform(95, 150), t0=G_TURN[0] + int(rs.randint(0, 8)) + (3 if sx > 0 else 0),
                                 ph=rs.uniform(0, 6.28), toward=(1 if sx < 0 else -1) * rs.choice([-1, 1])))
            else:
                K.horse(Bs, (x, y, DZ), 90.0, coat=coat, trap=m[0], trim=m[1], tint=tint, rider=(m[0],))
    Bs.finalize('column')


def key_column(f):
    """yaw of every animated horse at local frame f.  Base 90 deg = facing north (+y).  They swing round toward the rail trying to turn back,
    jam, wobble, and give up (back to north) by G_GIVEUP."""
    for a in ANIM:
        t0 = a['t0']
        up = u_of(f, t0, t0 + 14)                                   # swing out
        down = u_of(f, G_GIVEUP - 4 + (a['i'] % 3) * 2, G_GIVEUP + 8)       # give up
        k = up * (1 - down)
        wob = 7.0 * math.sin(f * 0.55 + a['ph']) * k * (1 - 0.5 * up)
        yaw = 90.0 + a['toward'] * (a['amp'] * 0.55 * k) + wob + 1.5 * math.sin(f * 0.21 + a['ph'])
        a['root'].rotation_euler = (math.radians(2.0 * math.sin(f * 0.4 + a['ph'])), 0.0, math.radians(yaw))
        a['root'].location = (a['x'], a['y'] + 0.12 * math.sin(f * 0.3 + a['ph']) * k, DZ + 0.04 * abs(math.sin(f * 0.45 + a['ph'])) * k)



# ------------------------------------------------------------------ the cast cards (hero riders on the west lane, nearest the camera)
S_CARD = 0.62                                   # card scale: world metres per D (knight 3.26 D -> 2.0 m with hat; the set's riders are about 2.4 m)
SX = {'A': (LANE_W, 4.2), 'B': (LANE_W, 1.2)}   # lane x, y of the two hero riders
SPR = os.path.join(HERE, 'work', 'sprites')
PPD = 128


def hero_base(who, f):
    """pose dict for A (red) / B (blue) at local frame f.  North = screen-left: mirror=True while facing north, False when turned back."""
    S = C.cast21.STORY21
    if who == 'A':
        calm, shock, wob = S['knight_a_mounted'][1], S['knight_a_mounted_shocked'][1], S['knight_a_mounted_wobble'][1]
        flip_f, back_f, ph = 46, 82, 0.0
    else:
        calm, shock, wob = S['knight_b_mounted'][1], S['knight_b_mounted_shocked'][1], S['knight_b_mounted_wobble'][1]
        flip_f, back_f, ph = 51, 86, 1.7
    turned = flip_f <= f < back_f
    p = dict(calm)
    t = f / 30.0
    p['mode21'] = 'idle'; p['t'] = (f / 70.0 + ph) % 1.0
    # phases: 0 stuck and worried | 1 turning (hop) | 2 wedged, shocked wobble | 3 given up (tired, facing north again)
    jam = u_of(f, G_TURN[0] + 8, G_TURN[0] + 22)
    wedge = u_of(f, 56, 62) * (1 - u_of(f, G_GIVEUP - 2, G_GIVEUP + 6))
    if f < G_TURN[0]:
        p.update(C.cast21.with_expr(p, 'worried'))
        p['head_roll'] = 3.0 * math.sin(f * 0.21 + ph)
        p['lean'] = 2.0 * math.sin(f * 0.17 + ph)
        p['pitch'] = 0.05 * math.sin(f * 0.13)
    elif wedge > 0.5:
        p = dict(wob)
        p['mode21'] = 'idle'; p['t'] = (f / 70.0 + ph) % 1.0
        p['head_roll'] = 14.0 * math.sin(f * 0.6 + ph) * (1.0 if who == 'A' else 0.7)
        p['lean'] = -10.0 + 5.0 * math.sin(f * 0.5 + ph)
    elif f >= G_GIVEUP:
        p.update(C.cast21.with_expr(p, 'tired'))
        p['head_roll'] = -4.0 + 2.0 * math.sin(f * 0.14 + ph); p['lean'] = 3.0
    else:
        p.update(C.cast21.with_expr(p, 'sweat'))
        p['head_roll'] = 8.0 * math.sin(f * 0.5 + ph); p['lean'] = 6.0 * math.sin(f * 0.4 + ph)
    p['mirror'] = not turned
    p['blink'] = C.cast21.blink_at(f, 52, 9 if who == 'A' else 31)
    p['t'] = (f / 70.0 + ph) % 1.0
    return C.K.with_rim(p)


def hop_dy(f, flip_f, back_f):
    """metres of lift: a hop of 0.45 m around each flip (the facing swaps at the apex)."""
    d = 0.0
    for c in (flip_f, back_f):
        x = (f - (c - 5)) / 10.0
        if 0.0 <= x <= 1.0:
            d = max(d, 0.45 * 4.0 * x * (1.0 - x))
    return d


def hero_xyz(who, f):
    x, y = SX[who]
    flip_f, back_f = (46, 82) if who == 'A' else (51, 86)
    wedge = u_of(f, 54, 60) * (1 - u_of(f, G_GIVEUP - 2, G_GIVEUP + 6))
    if who == 'A':
        y = y - 0.62 * wedge + 0.05 * math.sin(f * 0.5) * wedge
    else:
        y = y + 0.40 * wedge + 0.05 * math.sin(f * 0.6 + 1) * wedge
    return (x, y, DZ + hop_dy(f, flip_f, back_f)), flip_f, back_f


class Cast(object):
    def __init__(self):
        sc = bpy.context.scene
        self.a = C.actors.Actor('hA', 'knight_a_mtd'); self.a.build(C.sprites.DEFAULT_CANVAS['knight_a_mtd'], SPR, contact=True)
        self.b = C.actors.Actor('hB', 'knight_b_great_mtd'); self.b.build(C.sprites.DEFAULT_CANVAS['knight_b_great_mtd'], SPR, contact=True)
        self.c = C.actors.Actor('hC', 'knight_b_great_bare_mtd'); self.c.build(C.sprites.DEFAULT_CANVAS['knight_b_great_bare_mtd'], SPR, contact=True)
        self.h = C.actors.Actor('hH', 'helmet_air'); self.h.build(C.sprites.DEFAULT_CANVAS['helmet_air'], SPR, contact=False, shadow='card')
        for x in (self.a, self.b, self.c, self.h):
            x.head_flip = False
            x.round_head = False
        self.helm = {}                                  # f -> (x, y, z, tilt)

    def pose_all(self, frames):
        cam = bpy.context.scene.camera
        for f in frames:
            bf = f + 1
            bpy.context.scene.frame_set(bf); cam_at(f)
            for who, act in (('A', self.a), ('B', self.b), ('B', self.c)):
                xyz, _, _ = hero_xyz(who, f)
                act.place(bf, xyz, scale=S_CARD)
                act.pose(bf, hero_base(who, f), camera=cam)
            self.h.place(bf, self.helm_xyz(f), scale=S_CARD * 1.15)
            self.h.pose(bf, dict(tilt=self.helm_tilt(f)), camera=cam)

    def helm_xyz(self, f):
        # launched from B's head at G_POP: up, over, lands on the deck and bounces once (comic).  B head ~ 2.9 m above the deck at card scale .62
        x0, y0, z0 = hero_xyz('B', G_POP)[0]
        t = max(0.0, (f - G_POP) / 30.0)
        zh = z0 + 2.9
        vz, g = 4.6, 14.0
        z = zh + vz * t - 0.5 * g * t * t
        zl = DZ + 0.28
        tl = (vz + math.sqrt(vz * vz + 2 * g * (zh - zl))) / g               # time to hit the deck
        if t > tl:
            tb = t - tl
            z = zl + max(0.0, 1.8 * tb * 5.0 - 0.5 * 24.0 * tb * tb)         # one small bounce
            z = max(zl, z)
        x = x0 + 0.5 * min(t, tl + 0.4) * 1.2
        y = y0 + 0.9 * min(t, tl + 0.4) * 1.0
        return (x, y, z)

    def helm_tilt(self, f):
        return 30.0 + 640.0 * max(0.0, (f - G_POP) / 30.0) * (1.0 - 0.6 * u_of(f, G_POP + 10, G_POP + 22))

    def sprites(self, frames):
        jobs = []
        for f in frames:
            bf = f + 1
            B_on = f < G_POP
            for act, on in ((self.a, True), (self.b, B_on), (self.c, not B_on)):
                pass
        for act in (self.a, self.b, self.c, self.h):
            act.render_sprites(PPD if act is not self.h else 128, frames=[f + 1 for f in frames])

    def sync(self, f):
        bf = f + 1
        cam = bpy.context.scene.camera
        on_h = f >= G_POP
        self.a.set_hidden(False); self.b.set_hidden(f >= G_POP); self.c.set_hidden(f < G_POP); self.h.set_hidden(not on_h)
        for act in (self.a, self.b, self.c, self.h):
            act.sync(cam)


def hooks(f):
    t = (G0 + f) / FPS
    K.set_flow(t); K.set_flutter(t); K.set_smoke(t)


def render_path_draft(step=3, out='path_draft'):
    A = build(); build_column()
    d = os.path.join(HERE, 'work', out); os.makedirs(d, exist_ok=True)
    fs = list(range(0, N, step))
    for f in fs:
        hooks(f); key_column(f); cam_at(f)
        t0 = time.time(); K.render(os.path.join(d, 'f_%04d.png' % f), 'draft'); print('draft', f, round(time.time() - t0, 1), flush=True)
    import subprocess
    subprocess.run(['ffmpeg', '-y', '-v', 'error', '-framerate', '10', '-pattern_type', 'glob', '-i', os.path.join(d, 'f_*.png'), '-vf', 'scale=360:640', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '18',
                    os.path.join(HERE, out + '.mp4')], check=False)


def parse(spec):
    out = []
    for part in spec.split(','):
        if ':' in part:
            a = [int(v) for v in part.split(':')]
            out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
        else:
            out.append(int(part))
    return out


def render_frames(frames, mode, outdir, samples=None):
    A = build(); build_column()
    cast = Cast(); cast.pose_all(frames); cast.sprites(frames)
    os.makedirs(outdir, exist_ok=True)
    rep = {}
    for f in frames:
        png = os.path.join(outdir, 'g_%04d.png' % (G0 + f))
        if os.path.exists(png) and os.path.exists(png[:-4] + '.json'):
            continue
        bpy.context.scene.frame_set(f + 1)
        hooks(f); key_column(f); r = cam_at(f); cast.sync(f)
        t0 = time.time(); K.render(png + '.tmp.png', mode, samples); os.replace(png + '.tmp.png', png)
        json.dump(dict(f=f, g=G0 + f, cam=[round(float(v), 3) for v in r['loc']], look=[round(float(v), 3) for v in r['look']], lens=r['lens'], mode=mode, samples=samples,
                       wall=round(time.time() - t0, 1)), open(png[:-4] + '.json', 'w'))
        print('frame', f, 'g', G0 + f, round(time.time() - t0, 1), 's', flush=True)


if __name__ == '__main__':
    cmd = sys.argv[1]
    if cmd in ('draft', 'final'):
        frames = parse(sys.argv[2])
        outdir = os.path.join(HERE, 'draft' if cmd == 'draft' else 'raw')
        smp = int(sys.argv[3]) if len(sys.argv) > 3 else (None if cmd == 'draft' else 32)
        render_frames(frames, cmd, outdir, smp)
    if cmd == 'path_draft':
        step = int(sys.argv[2]) if len(sys.argv) > 2 else 3
        # path_frame(f) with f = local index; draft samples every `step` frames
        render_path_draft(step)
