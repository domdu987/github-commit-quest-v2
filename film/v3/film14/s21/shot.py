#!/usr/bin/env python3
"""film 14, take s21 v2: shot 21 only (45.59-48.44 s, g1368-1452; take g1362-1458). NIGHT, no elephant, NO dust.
Simple design: the camera stays on unit 1 (the hero hive of shot 22), hives at TRUE scale. The swing wave runs down the row from screen-right (units 3, 2, 1 visible, set swing),
unit 1 is thrown into its posts and BANGS them on g1390 (right post), g1410 (left), g1430 (right): accelerating run-in (>=30 px over 5 frames), hard stop on the contact frame, 12 px rebound over 2 frames,
5 px shake of posts + roofs for 2 frames and a 1-frame 5 px camera bump. World / sky / moon / lamps built exactly like team 4's shot 22 (same preset camera, dimmed lamps, dress).
Bees: none before g1442, small puffs from g1442. Last frame g1452 = shot 22's first frame (camera, lens, unit 1 at true size).
  python3 shot.py <g0> <g1> [preview|final] [outdir]   (resumable)"""
import sys, os, math, json, random
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c14 as C
from c14 import F, G, lerp, sm, mv, clamp
import bpy, numpy as np
from mathutils import Vector

PS = 14.0 + 10.25                    # push point arc (x 10.25, front row) = the push of shot 19/20
WAVE = 15.0                          # m/s: 5 m hive spacing = 10 frames between hives (the wave visibly passes hive to hive)
BANG = [(1390, +1), (1410, -1), (1430, +1)]   # (contact frame, side of the post hit: +1 right post, -1 left post) of unit 1
T_U3 = 1382                          # g at which the wave front reaches unit 3 (tau 0)
SLIDE = 0.32                         # m the hive slides along the wire into its post (hive end gap to the post)
LENS_END = 24

SLIDE = 0.32                         # m between the hive centre and each post contact (the hive end meets the post)
T_U1 = 1384                          # g at which the wave front reaches unit 1 (tau 0)
def tsec(g): return (abs(PS - (14 - 6.5)) / WAVE + 0.12) + (g - T_U1) / 30.0          # wire sim seconds; unit 1's tau = 0 at T_U1

def cam22(g):                         # team 4's shot 22 camera (s20/shot.py cam_of, s == 22)
    u = mv(clamp((g - 1453) / 50.0)); mvx = u
    return (lerp(-9.0, -8.2, u), lerp(2.1, 2.7, u), lerp(1.3, 1.35, u)), (lerp(-6.4, -6.2, u), 4.9, lerp(1.45, 1.5, u)), lerp(24, 26, u)

def cam_of(g):
    """eases from a low view down the row (units 3, 2, 1 receding to the right) into shot 22's first frame exactly"""
    P0 = ((-10.3, 1.2, 1.15), (-5.2, 5.0, 1.5), 26.0); P1 = cam22(1453)
    u = mv(clamp((g - 1362) / 90.0)); A, B = P0, P1
    loc = tuple(lerp(a, b, u) for a, b in zip(A[0], B[0])); look = tuple(lerp(a, b, u) for a, b in zip(A[1], B[1]))
    return loc, look, lerp(A[2], B[2], u)

# ---- contact geometry (measured from the meshes at build time, see Driver.__init__): LIM_R / LIM_L = hive offset (m) at which its end TOUCHES the inner surface of the right / left post
LIM = {'R': 0.265, 'L': -0.265}
LIMG = {}                                         # per cue frame: offset at which the hive end meets the post silhouette (solved from the camera projection of that frame)
REB = {1390: 0.08, 1410: 0.08, 1430: 0.08}      # rebound metres (set per contact from the camera scale: 13 px) in Driver.frame via px_per_m
CONTACT = [(1390, 'R'), (1410, 'L'), (1430, 'R')]
RUN0 = 1376                                       # first run-in starts from the soft left apex (-0.15 m, 0.06 m short of the left post: no contact)
PRE0 = 1366                                       # the wave arrives: hive eases (ease-in-out) from the centre to the left apex over g1366-1376
OVERRIDE = {}
def slide(g):
    if g in OVERRIDE: return OVERRIDE[g]
    """unit 1's hive, driven by hand: accelerating run-in toward the post (last 5 frames carry ~50 % of the travel), its end TOUCHES the post on the contact frame and stops dead, rebounds over 2 frames, rests for a beat, runs to the other post.
    No other hard stops: every segment starts from rest and accelerates (ease-in), only the contact frames stop abruptly."""
    seq = [(RUN0, 0.0, CONTACT[0][0], LIM[CONTACT[0][1]], CONTACT[0][1])]
    prev_g, prev_x = None, None
    pts = []                                           # (g_start, x_start, g_contact, x_contact, side)
    x_start = -0.15; g_start = RUN0
    for (gb, side) in CONTACT:
        pts.append((g_start, x_start, gb, LIMG.get(gb, LIM[side]), side)); reb = REB[gb] * (1 if side == 'L' else -1) * -1   # rebound away from the post
        reb = -REB[gb] if side == 'R' else REB[gb]
        x_start = LIMG.get(gb, LIM[side]) + reb; g_start = gb + 2
    if g < PRE0: return 0.0
    if g < RUN0: return -0.15 * sm((g - PRE0) / float(RUN0 - PRE0))
    for (g0, x0, g1, x1, side) in pts:
        if g0 <= g <= g1:
            u = clamp((g - g0) / float(g1 - g0)); return lerp(x0, x1, u ** 2.8)           # ease-in: fastest at the contact
        if g1 < g < g1 + 2:                                                                  # rebound frame 1 (2/3 of the way) then frame 2 = full rebound
            reb = (-REB[g1] if side == 'R' else REB[g1]); return LIMG.get(g1, LIM[side]) + reb * (0.65 if g == g1 + 1 else 1.0)
    # after the last contact + rebound: drift back to where shot 22's first frame has the hive
    g0, x0 = CONTACT[-1][0] + 2, LIMG.get(CONTACT[-1][0], LIM['R']) - REB[CONTACT[-1][0]]
    return lerp(x0, -0.30, sm((g - g0) / float(1452 - g0)))

U1S = [None]
PUSH_A = 0.10                         # the wire's own bow carried the hive's pivot through a 250 px pendulum (1.1 Hz ring-down): keep it tiny, the hive is placed by hand
YOFF = 0.27                           # unit 1's hive sits 0.22 m deeper than its rest so its front face is level with the posts' front (never in front of them)
C0 = (0.79, 0.79, 0.88); M0 = float(os.environ.get('M0', 160.0))
def _swing(s, t, s0=None):
    s = np.asarray(s, dtype=float); a, b = _ORIG(s, t, s0); a = a * 0.5; b = b * 0.5      # calmer set swing for the other hives
    if U1S[0] is not None:                                                                  # unit 1 is driven by hand (slide): no hook swing / twist
        z = np.abs(s - U1S[0]) < 0.05; a = np.where(z, 0.0, a); b = np.where(z, 0.0, b)
    return a, b
_ORIG = F.hive_swing

class Driver:
    def __init__(self, quality, threads):
        c0, l0, ln0 = cam22(1455)                                   # build with shot 22's preset camera: identical moon azimuth / key / sky
        C.register_preset('s21', c0, l0, ln0)
        F.WAVE_C = WAVE; F.hive_swing = _swing; F.PUSH_A = PUSH_A; C.SLEEP_N[0] = 0
        C.build('s21', quality, threads=threads, samples=int(os.environ.get('SAMPLES', 6 if quality == 'preview' else 24)), dense_bees=240)
        self.cam = C.Cam(); print('maize rows hidden', C.hide_maize_rows(7.0))
        pts = [cam22(g)[0] for g in range(1453, 1504, 6)]           # shot 22's own camera path points (what team 4 passed to cut_path / lamps / dress)
        pts21 = [cam_of(g)[0] for g in range(1362, 1459, 6)]
        C.cut_boxes([(-8.0, -3.0, -1.5, 5.2, 2.8), (-15, -8, -4, 6.0, 1.5)])
        keep = (lambda w: w.y > 4.2 and w.x > -13.3 and w.x < 10.4)
        C.cut_path(pts, 1.3, names=('grass', 'flowers', 'edge', 'pebbles'), keep=keep)
        C.cut_path(pts21, 1.3, names=('grass', 'flowers', 'edge', 'pebbles'), keep=keep)
        print('lamps dimmed', C.dim_lamps(pts[0], 16.0, 0.12), C.dim_lamps((-10.4, 0.5, 1.0), 9.0, 0.05))
        avoid = [(p[0], p[1], 1.2) for p in pts]
        C.dress((-12.5, -5.5), (-0.6, 3.6), 60, 6, avoid)
        self.shake = [o for o in bpy.data.objects if o.name.startswith(('posts_', 'roof'))]
        self.rest = (F.STATE['hive'][1].location.copy(), F.STATE['bar'][1].location.copy())
        U1S[0] = F.UNITS[1]['s']; self.geometry(); LIMG.update({1390: 0.30, 1410: -0.10, 1430: 0.34}); self.world_nodes()      # contact offsets calibrated on the rendered frames (hive end meets the post edge; the projection solve is kept as solve_contacts for reference)

    def geometry(self):
        """contact limits measured from the meshes: the hive end touches the INNER surface of its post (no overlap)"""
        u = F.UNITS[1]; px, py = float(u['pos'][0]), float(u['pos'][1]); hv = F.STATE['hive'][1]
        hx = 0.66; self.hx = hx            # box body half-length (the bbox 0.725 includes the landing board / bar ends)
        self.hy = max(abs(v.co.y) for v in hv.data.vertices)
        ob = bpy.data.objects['posts_wood']; mw = ob.matrix_world; vs = [mw @ v.co for v in ob.data.vertices]; self.post = {}
        for side, nm in ((1, 'R'), (-1, 'L')):
            near = [v for v in vs if abs(v.x - (px + side * 1.0)) < 0.3 and abs(v.y - py) < 0.3]
            bot = [v for v in near if v.z < 0.5]; top = [v for v in near if v.z > 2.0]
            zb, zt = bot[0].z, top[0].z; t = (1.25 - zb) / (zt - zb)
            f = (min if side == 1 else max)                                      # the face turned to the hive
            xi = f(v.x for v in bot) * (1 - t) + f(v.x for v in top) * t
            self.post[nm] = (xi, py, 1.25)
        LIM['R'] = self.post['R'][0] - (px + hx); LIM['L'] = self.post['L'][0] - (px - hx); self.px = px
        print('contact limits R %.3f L %.3f (hive half-length %.3f, posts inner x %.3f / %.3f)' % (LIM['R'], LIM['L'], hx, self.post['L'][0], self.post['R'][0]), flush=True)
        for gb, sd in CONTACT:
            l, lk, ln = cam_of(gb); self.cam.set(l, lk, ln); bpy.context.view_layer.update()
            a_ = C.screen((px, py, 1.3))[0]; b_ = C.screen((px + 0.1, py, 1.3))[0]; self.pxm_x = abs(b_ - a_) / 0.1; REB[gb] = 15.0 / max(self.pxm_x, 1.0)      # rebound = 13 px (along the wire) at that frame
        print('rebounds (m)', {k: round(v, 3) for k, v in REB.items()}, flush=True)

    def solve_contacts(self):
        """per cue frame: the hive offset at which the hive's end meets the post's SILHOUETTE edge in that frame's camera (hive sits behind the post: YOFF); bisection on the projected edges"""
        px, py = float(F.UNITS[1]['pos'][0]), float(F.UNITS[1]['pos'][1]); hr = self.rest[0]; ob = bpy.data.objects['posts_wood']; mw = ob.matrix_world; vs = [mw @ v.co for v in ob.data.vertices]
        def post_sil(side):
            near = [v for v in vs if abs(v.x - (px + side * 1.0)) < 0.3 and abs(v.y - py) < 0.3]; bot = [v for v in near if v.z < 0.5]; top = [v for v in near if v.z > 2.0]
            t = (1.25 - bot[0].z) / (top[0].z - bot[0].z); f = (min if side == 1 else max)
            xb = f(C.screen(tuple(v))[0] for v in bot); xt = f(C.screen(tuple(v))[0] for v in top); return xb * (1 - t) + xt * t
        for gb, sd in CONTACT:
            l, lk, ln = cam_of(gb); self.cam.set(l, lk, ln); bpy.context.view_layer.update(); sign = 1 if sd == 'R' else -1
            edge = post_sil(sign)
            def f(off):
                xs = [C.screen((hr.x + off + sign * self.hx, hr.y + YOFF + dy, hr.z + dz))[0] for dy in (-self.hy, self.hy) for dz in (0.0, -0.8)]
                return (max(xs) - edge) if sign == 1 else (edge - min(xs))
            lo, hi = 0.0, sign * 0.7
            for _ in range(30):
                mid = (lo + hi) / 2
                if f(mid) < 0: lo = mid
                else: hi = mid
            LIMG[gb] = (lo + hi) / 2
            if sd == 'L' and abs(LIMG[gb]) < 0.05: LIMG[gb] = -0.19             # the left post is nearer the camera: the silhouette solve degenerates; value from the rendered-frame check
            print('contact %d (%s): offset %.4f m (screen edge %d)' % (gb, sd, LIMG[gb], edge), flush=True)

    def world_nodes(self):
        nt = bpy.context.scene.world.node_tree; bg = [n for n in nt.nodes if n.type == 'BACKGROUND'][0]
        src = bg.inputs['Color'].links[0].from_socket; mx = nt.nodes.new('ShaderNodeMix'); mx.data_type = 'RGBA'; mx.blend_type = 'MULTIPLY'; mx.inputs[0].default_value = 1.0
        nt.links.new(src, mx.inputs[6]); nt.links.new(mx.outputs[2], bg.inputs['Color']); self.tint = mx
        self.starmul = [n for n in nt.nodes if n.type == 'MATH' and n.operation == 'MULTIPLY' and abs(n.inputs[1].default_value - 16.0) < 1e-6][0]
    def ramp(self, g):
        """world grade: shot 20's sky at g1368 (darker, more stars), linearly to shot 22's (= the set's plain NIGHT) by g1452"""
        u = clamp((g - 1368) / 84.0); c = [lerp(a, 1.0, u) for a in C0]
        self.tint.inputs[7].default_value = (c[0], c[1], c[2], 1.0); self.starmul.inputs[1].default_value = lerp(M0, 16.0, u)

    def frame(self, g, path, hide=()):
        loc, look, lens = cam_of(g); focal = lens / 36.0 * 1280.0
        h1 = F.STATE['hive'][1]; dep = (Vector((-6.5, 4.9, 1.2)) - Vector(loc)).length; pxm = dep / focal       # metres per pixel at the hive
        hit = [gb for gb, sd in BANG if 0 <= g - gb < 2]; bump = [gb for gb, sd in BANG if g == gb]
        if bump:                                                              # 1-frame camera bump of 5 px
            d = 5.0 * pxm; loc = (loc[0], loc[1], loc[2] - d); look = (look[0], look[1], look[2] - d)
        self.cam.set(loc, look, lens); bpy.context.view_layer.update()
        self.ramp(g); F.set_fence_stage(3); F.set_wire_push(tsec(g) / F.SEQ_T, PS); bpy.context.view_layer.update()
        off = slide(g); hr, br = self.rest; h1.location = Vector((hr.x + off, hr.y + YOFF, hr.z)); F.STATE['bar'][1].location = Vector((br.x + off, br.y + YOFF, br.z)); h1.rotation_euler = (0, 0, 0)       # world position set LAST (after set_wire_push / update)
        if hit:                                                               # posts + roofs shake 5 px for 2 frames (alternating)
            sh = 5.0 * pxm * (1 if (g - hit[0]) == 0 else -0.6)
            for o in self.shake: o.location = (sh, 0, sh * 0.4)
        else:
            for o in self.shake: o.location = (0, 0, 0)
        bpy.context.view_layer.update()
        bs = (g - 1442) / 30.0                                                # bees only from g1442: small puffs, leading into shot 22
        if bs < 0: F.set_bees(-1.0, 0.0, None, None)
        else: F.set_bees((3.3 + bs) / F.SEQ_T, 0.03 + 0.05 * clamp(bs / 0.4), None, None)
        bpy.context.view_layer.update()
        info = dict(slide=round(off, 3), hive=C.screen(h1.location), pxm=round(pxm, 4))
        hid = [o for o in bpy.data.objects if o.name in hide]
        for o in hid: o.hide_render = True
        w, cpu = F.render(path)
        for o in hid: o.hide_render = False
        return w, cpu, info

def probe_table(d, g0, g1):
    """no render: hive bbox vs post screen-x per frame (gap in px between the hive end and the nearest post's inner surface; 0 = touching)"""
    rows = []
    for g in range(g0, g1 + 1):
        loc, look, lens = cam_of(g); d.cam.set(loc, look, lens); bpy.context.view_layer.update()
        F.set_fence_stage(3); F.set_wire_push(tsec(g) / F.SEQ_T, PS); bpy.context.view_layer.update()
        h1 = F.STATE['hive'][1]; off = slide(g); cx = d.px + off
        def sx(x, y, z): return C.screen((x, y, z))[0]
        y = float(F.UNITS[1]['pos'][1]); xr = sx(cx + d.hx, y, 1.3); xl = sx(cx - d.hx, y, 1.3); pr = sx(d.post['R'][0], y, 1.3); pl = sx(d.post['L'][0], y, 1.3)
        rows.append((g, round(off, 4), xl, xr, pl, pr, pl - xl, pr - xr))
    return rows

if __name__ == '__main__':
    a = sys.argv[1:]; g0, g1 = int(a[0]), int(a[1]); q = a[2] if len(a) > 2 else 'preview'; outdir = a[3] if len(a) > 3 else os.path.join(HERE, 'draft'); os.makedirs(outdir, exist_ok=True)
    step = int(os.environ.get('STEP', '1')); thr = int(os.environ.get('THREADS', '2'))
    d = Driver(q, thr)
    if os.environ.get('PROBE'):
        for r in probe_table(d, g0, g1): print(r)
        sys.exit(0)
    for g in range(g0, g1 + 1, step):
        p = os.path.join(outdir, 'g_%04d.png' % g)
        if os.path.exists(p) and os.environ.get('RESUME', '1') == '1': continue
        w, cpu, info = d.frame(g, p); print(g, '%.1fs' % w, json.dumps(info), flush=True)
