#!/usr/bin/env python3
"""shot.py -- film 9 take s15: shots 15 + 16 (g 1153..1412, handles g 1147..1152 and g 1413..1418), THE REVEAL inside the mortar joint
(wall.py macro area, 1 D ~ 2 mm, BATTLE light).  Two set-ups, two processes (one macro kind per build):

    id 15  g 1147..1283  mortar_macro (plain lime mortar): macro_front, near square-on to the grey joint with cyan lime crystals, slow push.
                         "ปูนธรรมดา แข็งก็จริง แต่เปราะ" calm; the cannonball flies in over the camera's left shoulder (g 1180..1207)
                         and strikes on "โดนกระแทก" (40.12 s -> g 1207): flash, small camera jolt, a BLACK brittle crack with a pale
                         chipped lip races along the whole joint both ways and branches up / down into the bricks on
                         "ทีเดียวก็ร้าวทั้งแผ่น" (g 1207..1262), shards spall toward the lens, dust puff; the ball drops away.
    id 16  g 1284..1418  mortar_macro_rice: macro_front again (push from slightly right / below), creamy matrix.
                         On "ส่วนแป้งข้าวเหนียว ไปพันกับผลึกปูน เป็นตาข่ายเหนียวหนึบ" (41.95-45.39 s) the slow push shows the glowing
                         gold starch net wrapped round the cyan lime crystals; on "ลูกปืนกระแทก" the ball flies in (g 1352..1380) and hits
                         (g 1380): the face dents, a bright gold ring pulses out over the net, the web stretches, flexes back in a damped
                         spring and HOLDS; the ball springs back a little and settles, held in its shallow dent with a glowing dent ring,
                         on "แค่ไหนก็แค่บุบ" (46.12-47.10 s) (round-3 set: the ball stays visible).  Out-handle g 1413..1418 continues.
Mouths: nobody on screen.  NO depth of field (C.Take).  Blender frame: bf() below (smoke phase).

    python3 shot.py stills 15|16 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 15|16 a:b[:step] [scale] [samples]
QA round 1 fixes: both halves use an oblique orbit camera (17-24 deg from the front-left, raking fire light); rice: the set's thin pulse
ring is hidden and replaced by a soft gold glow ring hugging the ball that fades out; a gold glow burst along the web on impact; a web
bulge shape key (damped spring); the web glow breathes before the hit while the camera pushes in; the ball stays held and visible.
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
    """Blender frame.  The set's macro smoke billows / embers take their phase from the Blender frame (rate 0.003 = one cycle per
    333.3 frames).  Shot 16 (f 3285..3420) has a clean phase (no billow in front of the impact); shot 15 is placed exactly one cycle
    earlier (f 2952..3088) so it gets the same clean phase (at f 2148.. big billows drifted across the lens)."""
    return (2000 + int(g) + 1) if shot == 16 else (int(g) + 1805)


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


# cameras (QA round 1: "flat top-down" -> oblique): orbit the impact point by yaw (deg, + = camera to the right) / elevation (deg) /
# distance d, 24 mm, a 17-24 deg oblique from the front-left so the warm raking fire key from the front-left grazes the bricks, the
# crystals and the web (a lit 3D world); same tilt family in both halves.  Plain: slow push + small orbit; rice: a longer push (QA:
# 1297-1372 read near-still) with the orbit the other way.
ORBIT = {15: ((-24.0, 10.0, 9.8), (-19.0, 7.0, 7.8)),
         16: ((-17.0, 11.0, 10.0), (-23.0, 6.5, 6.9))}
LENS = 24.0


def orbit_loc(yaw, el, d):
    a, e = math.radians(yaw), math.radians(el)
    return IMP + Vector((d * math.sin(a) * math.cos(e), -d * math.cos(a) * math.cos(e), d * math.sin(e)))


def cam_of(shot, g):
    (y0, e0, d0), (y1, e1, d1) = ORBIT[shot]
    lo, hi = RANGES[shot]
    x = (g - lo) / float(hi - lo)
    u = 0.35 * ez(x, "sine") + 0.65 * x
    loc = orbit_loc(lerp(y0, y1, u), lerp(e0, e1, u), lerp(d0, d1, u))
    look = IMP + Vector((0.15, 0.0, -0.05))
    gh = G_HIT15 if shot == 15 else G_HIT16
    if g >= gh:                                      # a small jolt on the hit, decaying over ~10 frames
        k = (g - gh)
        amp = 0.07 * math.exp(-k / 4.0)
        loc += Vector((amp * math.sin(k * 2.1), 0.0, amp * math.cos(k * 2.7)))
        look += Vector((0.5 * amp * math.sin(k * 1.7 + 1), 0.0, 0.5 * amp * math.cos(k * 2.3)))
    return loc, look


# ----------------------------------------------------------------------------- rice: runtime fixes (QA round 1)
# 1. the set's thin pulse ring (expands to the frame edge, turns olive) is hidden every frame; instead a thick soft-glow emissive gold
#    ring hugs the ball (1.3..2.5 x the ball radius) and fades to transparent with no colour change; the web flares gold on impact.
# 2. a 'bulge' shape key on the web: the strands round the ball stretch outward / into the joint on impact and spring back.
# 3. before the hit the web breathes (a gentle gold glow pulse) while the camera pushes in.
GOLD = (1.0, 0.58, 0.12)


def make_glow_ring():
    import bmesh
    Mc = W.STATE["macro"]; RB = W.MAC["ball_r"]; ix, iz = W.MAC["impact"]; fy = W.MAC["face_y"]
    m = bpy.data.materials.new("s15_glowring"); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    tc = nt.nodes.new("ShaderNodeTexCoord"); ln = nt.nodes.new("ShaderNodeVectorMath"); ln.operation = "LENGTH"
    cr = nt.nodes.new("ShaderNodeValToRGB"); el = cr.color_ramp; el.interpolation = "B_SPLINE"
    el.elements[0].position = 0.46; el.elements[0].color = (0, 0, 0, 1); el.elements[1].position = 0.98; el.elements[1].color = (0, 0, 0, 1)
    for pos, v in ((0.56, 1.0), (0.66, 0.85), (0.82, 0.35)):
        e = el.elements.new(pos); e.color = (v, v, v, 1)
    op = nt.nodes.new("ShaderNodeValue"); op.name = "op"; op.outputs[0].default_value = 0.0
    mul = nt.nodes.new("ShaderNodeMath"); mul.operation = "MULTIPLY"
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs["Color"].default_value = GOLD + (1.0,); em.inputs["Strength"].default_value = 4.2
    tr = nt.nodes.new("ShaderNodeBsdfTransparent"); mx = nt.nodes.new("ShaderNodeMixShader"); out = nt.nodes.new("ShaderNodeOutputMaterial")
    nt.links.new(tc.outputs["Object"], ln.inputs[0]); nt.links.new(ln.outputs["Value"], cr.inputs[0])
    nt.links.new(cr.outputs["Color"], mul.inputs[0]); nt.links.new(op.outputs[0], mul.inputs[1]); nt.links.new(mul.outputs[0], mx.inputs[0])
    nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(em.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], out.inputs[0])
    me = bpy.data.meshes.new("s15_glowring"); bm = bmesh.new()
    bmesh.ops.create_circle(bm, cap_ends=True, segments=96, radius=1.0); bm.to_mesh(me); bm.free()
    ob = bpy.data.objects.new("s15_glowring", me); ob.data.materials.append(m)
    ob.rotation_euler = (math.pi / 2, 0, 0)                          # disc in the x-z plane (the joint face)
    ob.location = Vector((ix, fy + 0.1 - RB - 0.05, iz))            # through the held ball's centre: the ball hides the inner half
    ob.visible_shadow = False; ob.visible_diffuse = False; ob.visible_glossy = False
    bpy.context.scene.collection.objects.link(ob); ob.hide_render = True
    # bulge shape key on the web
    wo = Mc["web"]
    def bulge(p):
        dx, dz = p.x - ix, p.z - iz; d = math.hypot(dx, dz) + 1e-6
        r = 0.42 * math.exp(-((d - 1.05) ** 2) / 0.55)
        return Vector((dx / d * r, 0.30 * math.exp(-d * d / 1.6), dz / d * r * 0.8))
    W._shape_key(wo, "s15_bulge", bulge)
    return dict(ob=ob, op=op, RB=RB)


def key_rice(R, f, g):
    Mc = W.STATE["macro"]
    pu = Mc.get("pulse")
    if pu is not None:
        pu.hide_render = True; pu.keyframe_insert("hide_render", frame=f)
    k = g - G_HIT16
    # glow ring
    ob = R["ob"]; on = 0 <= k <= 26
    u = max(0.0, min(1.0, k / 24.0))
    sc = R["RB"] * 2.6 * (0.82 + 0.28 * ez(u))
    ob.scale = (sc, sc, sc); ob.hide_render = not on
    ob.keyframe_insert("scale", frame=f); ob.keyframe_insert("hide_render", frame=f)
    R["op"].outputs[0].default_value = (min(1.0, (k + 1) / 2.0) * (1.0 - u) ** 1.4) if on else 0.0
    R["op"].outputs[0].keyframe_insert("default_value", frame=f)
    # web glow: breathing before the hit, a gold burst along the web on impact (scales the set's keyed strength of this frame)
    if g < G_FLY16:
        mul = 1.0 + 0.24 * math.sin(2 * math.pi * (g - G_CUT) / 46.0)
    else:
        mul = 1.0 + 1.9 * math.exp(-(((k - 1) / 6.0) ** 2)) if k >= -2 else 1.0
    for nm in ("web", "web_fine"):
        sk = W.STATE["M"][nm].node_tree.nodes["strength"].inputs["Strength"]
        sk.default_value = sk.default_value * mul; sk.keyframe_insert("default_value", frame=f)
    # web bulge: out and in on the hit, a damped spring, settles at a small held stretch
    kb = Mc["web"].data.shape_keys.key_blocks["s15_bulge"]
    if k < 0:
        v = 0.0
    else:
        v = math.sin(min(1.0, k / 2.0) * math.pi / 2) * math.exp(-k / 9.0) * math.cos(max(0, k - 2) * 0.5) + 0.12 * min(1.0, k / 6.0)
    kb.value = max(-0.6, v); kb.keyframe_insert("value", frame=f)


class Take(C.Take):
    def __init__(self, quality="preview", shot=15):
        C.Take.__init__(self, "wall_site", PRESET[shot], quality=quality, lens=LENS, name="cam_s15_%d" % shot, light="BATTLE")
        self.shot = shot
        self.rice = make_glow_ring() if shot == 16 else None

    def pose(self, shot, gs):
        for g in gs:
            f = bf(shot, g)
            loc, look = cam_of(shot, g)
            self.key_cam(f, loc, look, lens=LENS)
            self.key_set(f, macro=macro_t(shot, g))
            if self.rice is not None:
                key_rice(self.rice, f, g)

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
