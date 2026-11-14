#!/usr/bin/env python3
"""shot.py -- film 9 take s15: shots 15 + 16 (g 1153..1412, handles g 1147..1152 and g 1413..1418), THE REVEAL inside the mortar joint
(wall.py macro area, 1 D ~ 2 mm, BATTLE light).  Two set-ups, two processes (one macro kind per build):

    id 15  g 1147..1283  mortar_macro (plain lime mortar): oblique along the grey bed joint packed with white lime crystals, slow push.
                         "ปูนธรรมดา แข็งก็จริง แต่เปราะ" calm; the cannonball flies in over the camera's left shoulder (g 1180..1207)
                         and strikes on "โดนกระแทก" (40.12 s -> g 1207): flash, small camera jolt, a BLACK brittle crack with a pale
                         chipped lip races along the whole joint both ways and branches up / down into the bricks on
                         "ทีเดียวก็ร้าวทั้งแผ่น" (g 1207..1262), shards spall toward the lens, dust puff; the ball drops away.
    id 16  g 1284..1418  mortar_macro_rice: the mirrored oblique from the right (reads as "the other wall"), creamy matrix.
                         On "ส่วนแป้งข้าวเหนียว ไปพันกับผลึกปูน เป็นตาข่ายเหนียวหนึบ" (41.95-45.39 s) the glowing gold starch web
                         SPREADS out from the frame centre and wraps the crystals (runtime radial reveal on the web material,
                         g 1290..1338), then glows; on "ลูกปืนกระแทก" the ball flies in (g 1352..1381) and hits (g 1381): the face dents,
                         the web stretches, flares, flexes back in a damped spring and HOLDS; the ball bounces back out and drops away on
                         "แค่ไหนก็แค่บุบ" (46.12-47.10 s).  Out-handle g 1413..1418 continues.
Mouths: nobody on screen.  NO depth of field (C.Take).  Blender frame of (id, g) = 1000 * (id - 1) + g + 1 - 1000 * 14 (bf below).

    python3 shot.py stills 15|16 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 15|16 a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c9 as C                                           # noqa: E402
from mathutils import Vector                             # noqa: E402
import bpy                                               # noqa: E402

W = C.B
lerp, clamp, ez = C.lerp, C.clamp, C.ez

G0, G_CUT, G1, H = 1153, 1284, 1413, 6
RANGES = {15: (G0 - H, G_CUT - 1), 16: (G_CUT, G1 + H - 1)}
PRESET = {15: "mortar_macro", 16: "mortar_macro_rice"}
IMP = Vector((1.5, 0.22, 0.0))

# event frames (narration t -> g = round((t + 0.10) * 30))
G_HIT15 = C.g_of(40.12)            # 1207 "โดนกระแทก"
G_FLY15 = G_HIT15 - 27             # 1180 ball enters
G_CRACK_END = C.g_of(41.85)        # 1262 "ร้าวทั้งแผ่น" ends: the crack has reached both ends
G_WEB = (C.g_of(43.10) - 9, C.g_of(44.72) - 19)     # 1290..1337 the web spreads ("ไปพันกับผลึกปูน เป็นตาข่าย")
G_HIT16 = C.g_of(45.88)            # 1380 end of "ลูกปืนกระแทก"
G_FLY16 = G_HIT16 - 28             # 1352


def bf(shot, g):
    return 1000 * (shot - 14) + int(g) + 1


def macro_t(shot, g):
    if shot == 15:
        if g < G_FLY15:
            return 0.0
        if g < G_HIT15:
            return 0.3 * (g - G_FLY15) / float(G_HIT15 - G_FLY15)
        if g < G_CRACK_END:
            return 0.3 + 0.45 * (g - G_HIT15) / float(G_CRACK_END - G_HIT15)
        return min(1.0, 0.75 + 0.25 * (g - G_CRACK_END) / 26.0)
    if g < G_FLY16:
        return 0.0
    if g < G_HIT16:
        return 0.3 * (g - G_FLY16) / float(G_HIT16 - G_FLY16)
    return min(1.0, 0.3 + 0.7 * (g - G_HIT16) / 40.0)


# cameras: (loc, look) at the start / end of each set-up; 22 mm.  Both = the preset's oblique (from the front-left, joint receding
# right, the impact point mid-frame) so plain vs rice compare 1:1; the rice set-up starts closer and pushes further in.
# (a mirrored oblique from the front-right was tried: hot-lit brick ends, weak web -> dropped.)
CAM = {15: (((-5.6, -5.2, 1.25), (2.4, 0.2, -0.05)), ((-3.9, -3.75, 0.75), (2.55, 0.2, -0.15))),
       16: (((-4.9, -4.95, 1.05), (2.3, 0.2, -0.05)), ((-3.0, -3.05, 0.55), (2.05, 0.2, -0.12)))}
LENS = 22.0


def cam_of(shot, g):
    a, b = CAM[shot]
    lo, hi = RANGES[shot]
    x = (g - lo) / float(hi - lo)
    u = 0.35 * ez(x, "sine") + 0.65 * x
    loc, look = Vector(lerp(a[0], b[0], u)), Vector(lerp(a[1], b[1], u))
    gh = G_HIT15 if shot == 15 else G_HIT16
    if g >= gh:                                      # a small jolt on the hit, decaying over ~10 frames
        k = (g - gh)
        amp = 0.07 * math.exp(-k / 4.0)
        loc += Vector((amp * math.sin(k * 2.1), 0.0, amp * math.cos(k * 2.7)))
        look += Vector((0.5 * amp * math.sin(k * 1.7 + 1), 0.0, 0.5 * amp * math.cos(k * 2.3)))
    return loc, look


# ----------------------------------------------------------------------------- runtime: the web spreads over the face (rice only)
def web_reveal_nodes():
    """insert transparent-mix on the web material: visible where |p - c| < R (R keyed), soft edge 0.6 D, a bright front at the edge."""
    m = W.STATE['M']['web']; nt = m.node_tree
    em = nt.nodes['strength']; out = nt.nodes['Material Output']
    tc = nt.nodes.new('ShaderNodeTexCoord')
    dist = nt.nodes.new('ShaderNodeVectorMath'); dist.operation = 'DISTANCE'; dist.inputs[1].default_value = (0.9, 0.2, 0.0)
    nz = nt.nodes.new('ShaderNodeTexNoise'); nz.inputs['Scale'].default_value = 0.6
    add = nt.nodes.new('ShaderNodeMath'); add.operation = 'MULTIPLY_ADD'; add.inputs[1].default_value = 2.5
    rad = nt.nodes.new('ShaderNodeValue'); rad.name = 's15_R'; rad.outputs[0].default_value = 99.0
    mr = nt.nodes.new('ShaderNodeMapRange'); mr.name = 's15_map'
    tr = nt.nodes.new('ShaderNodeBsdfTransparent'); mx = nt.nodes.new('ShaderNodeMixShader')
    nt.links.new(tc.outputs['Object'], dist.inputs[0]); nt.links.new(tc.outputs['Object'], nz.inputs['Vector'])
    nt.links.new(nz.outputs['Fac'], add.inputs[0]); nt.links.new(dist.outputs['Value'], add.inputs[2])     # noisy distance
    nt.links.new(add.outputs[0], mr.inputs['Value'])
    sub = nt.nodes.new('ShaderNodeMath'); sub.operation = 'SUBTRACT'; sub.inputs[1].default_value = 0.8
    nt.links.new(rad.outputs[0], sub.inputs[0]); nt.links.new(sub.outputs[0], mr.inputs['From Min']); nt.links.new(rad.outputs[0], mr.inputs['From Max'])
    mr.inputs['To Min'].default_value = 1.0; mr.inputs['To Max'].default_value = 0.0
    nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(em.outputs[0], mx.inputs[2]); nt.links.new(mr.outputs[0], mx.inputs[0])
    nt.links.new(mx.outputs[0], out.inputs['Surface'])
    return rad


def key_web(rad, f, g):
    u = clamp((g - G_WEB[0]) / float(G_WEB[1] - G_WEB[0]))
    R = -1.0 + 32.0 * ez(u, "sine") ** 1.6 if g >= G_WEB[0] else -1.0
    rad.outputs[0].default_value = R
    rad.outputs[0].keyframe_insert('default_value', frame=f)
    # glow: dim while it spreads, then the web settles at the set's 1.8 (set_macro keys it each frame; we scale on top)
    sk = W.STATE['M']['web'].node_tree.nodes['strength'].inputs['Strength']
    t = macro_t(16, g)
    base = 1.8 * (1.0 + 1.4 * math.exp(-((t - 0.36) / 0.1) ** 2) + 0.25 * W._ss(0.3, 0.6, t)) if t > 0 else 1.8
    breathe = 1.0 + 0.10 * math.sin(g * 0.21) if t == 0 else 1.0
    spread = 1.0 + 0.35 * math.exp(-((u - 0.55) / 0.3) ** 2) if 0 < u < 1 else 1.0     # it glows hot while it wraps
    sk.default_value = base * breathe * spread
    sk.keyframe_insert('default_value', frame=f)


class Take(C.Take):
    def __init__(self, quality="preview", shot=15):
        C.Take.__init__(self, "wall_site", PRESET[shot], quality=quality, lens=LENS, name="cam_s15_%d" % shot, light="BATTLE")
        self.shot = shot
        self.rad = web_reveal_nodes() if shot == 16 else None

    def pose(self, shot, gs):
        for g in gs:
            f = bf(shot, g)
            loc, look = cam_of(shot, g)
            self.key_cam(f, loc, look, lens=LENS)
            self.key_set(f, macro=macro_t(shot, g))
            if self.rad is not None:
                key_web(self.rad, f, g)

    def report(self, shot, g):
        loc, look = cam_of(shot, g)
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], macro_t=round(macro_t(shot, g), 4), heads={})

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    shot = int(sys.argv[2])
    if cmd == "stills":
        Tk = Take("preview", shot)
        gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
        Tk.pose(shot, gs)
        out = sys.argv[4]; os.makedirs(out, exist_ok=True)
        scale = float(sys.argv[5]) if len(sys.argv) > 5 else 1.0
        samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
        for g in gs:
            st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
            os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
            print("shot %d g %d t %.3f  %.1f s wall %.1f cpu" % (shot, g, macro_t(shot, g), st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q, s: Take(q, s), [shot], sys.argv[3], RANGES, HERE, scale=scale, samples=samples, take_key=lambda s: s)
