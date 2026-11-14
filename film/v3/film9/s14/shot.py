#!/usr/bin/env python3
"""shot.py -- film 9 take s14: shot 14 (g 1041..1152, handles g 1035..1040 and g 1153..1158), BATTLE: "แล้วทัพศัตรูก็มาถึง
ลากปืนใหญ่มาเรียงหน้ากำแพงทั้งสองช่วง".  One location (wall_site, cannon_line build, BATTLE light, army on, smoke), two set-ups:

    id 1  g 1035..1096  wide behind the enemy cannon row (cannon_line camera, slow crane-track to the right and up): six bronze guns
                        in a diagonal into depth toward BOTH wall sections (Lin's creamy one left, the general's taller grey one
                        right), fire pots, black banners, smoke columns rising.  Two gunners stand at guns 2 and 3 with smouldering
                        linstocks, then crouch toward the touch holes (from g 1080).
    id 2  g 1097..1158  medium, low, behind-right of the gunner at gun 3 (aimed at the general's section): he touches the glowing
                        match to the touch hole (g 1112), the fuse spits sparks (g 1113..1138), he ducks and covers his ears
                        (g 1128..), the gun FIRES (g 1140: muzzle flash, light, smoke; wall.set_impact('general', 0, t)); the ball
                        flies toward the wall (handle).  Cut to shot 15 (the macro: the ball hits the plain mortar).
Mouths: nobody speaks (static expression mouths only).  NO depth of field (C.Take).  Blender frame bf(id, g) = 1000 * (id - 1) + g + 1.

    python3 shot.py stills 1|2 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 1|2 a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c9 as C                                           # noqa: E402
from mathutils import Vector                             # noqa: E402
import bpy                                               # noqa: E402

W, actors, cast9 = C.B, C.actors, C.cast9
import puppet                                            # noqa: E402
lerp, clamp, ez, blink = C.lerp, C.clamp, C.ez, C.blink
TMP = os.path.join(HERE, "work")

G0, G1, H = 1041, 1153, 6
G_CUT = 1097
RANGES = {1: (G0 - H, G_CUT - 1), 2: (G_CUT, G1 + H - 1)}
G_CROUCH_A = (1078, 1094)          # set-up 1: both gunners crouch toward the touch holes
G_CROUCH_B = (1100, 1112)          # set-up 2: gunner 3 brings the match down to the touch hole
G_TOUCH = 1112
G_DUCK = (1126, 1134)              # he ducks and covers his ears
G_FIRE = 1140                      # muzzle flash (set_impact t 0.02)

CX = W.CANNON_X; CY = W.CANNON_Y
GUN_A = Vector((CX[2] + 1.3, CY - 1.6, 0.0))      # gunner_a at gun 2 (x -2.5, aims at Lin's section)
GUN_B = Vector((CX[3] - 1.3, CY - 2.3, 0.0))      # gunner_b at gun 3 (x 4.5, aims at the general's section), on the gun's left,
                                                  # in front of its bucket: from both cameras the gun is screen-right of him
TOUCH = Vector((CX[3], CY - 1.05, 1.62))          # gun 3's touch hole (top of the breech)

CAM = {1: (((-23.0, -28.5, 3.4), (5.0, -13.0, 5.4)), ((-20.6, -30.2, 4.4), (6.6, -13.6, 5.6))),
       2: (((9.6, -30.0, 2.05), (1.7, -20.2, 3.3)), ((8.8, -29.15, 1.85), (1.5, -19.9, 3.4)))}
LENS = {1: 20.0, 2: 22.0}
PPD = {1: 160, 2: 288}


def bf(shot, g):
    return 1000 * (shot - 1) + int(g) + 1


def u_of(g, a, b):
    return ez((g - a) / float(b - a)) if g > a else 0.0


def cam_of(shot, g):
    a, b = CAM[shot]; lo, hi = RANGES[shot]
    x = (g - lo) / float(hi - lo)
    u = 0.35 * ez(x, "sine") + 0.65 * x
    loc, look = Vector(lerp(a[0], b[0], u)), Vector(lerp(a[1], b[1], u))
    if shot == 2 and g >= G_FIRE:                  # the shot's concussion: a short shake
        k = g - G_FIRE; amp = 0.10 * math.exp(-k / 5.0)
        loc += Vector((amp * math.sin(k * 2.3), 0.0, amp * math.cos(k * 3.1)))
    return loc, look


def impact_t(g):
    return 0.0 if g < G_FIRE - 1 else min(0.34, 0.02 + (g - G_FIRE) / 60.0)


# ----------------------------------------------------------------------------- poses
STAND = {"gunner_a": cast9.STORY9["gunner_stand"][1], "gunner_b": cast9.STORY9["gunner_stand_b"][1]}
LIGHT = {"gunner_a": cast9.STORY9["gunner_light"][1], "gunner_b": cast9.STORY9["gunner_light_b"][1]}
EARS = {"gunner_a": cast9.STORY9["gunner_ears"][1], "gunner_b": cast9.STORY9["gunner_ears_b"][1]}


def blend(cast, a, b, u, extra):
    p = puppet.lerp_pose(cast, a, b, u)
    p.update(extra)
    return p


def pose_gunner(cast, g, crouch, duck=0.0, seed=0.0, mirror=True):
    """stand (linstock upright) -> light (crouched, match at the touch hole) -> ears (ducking).  Linstock angle tweened."""
    ang = lerp(-80.0, 32.0, crouch)
    if duck <= 0:
        p = blend(cast, STAND[cast], LIGHT[cast], crouch, dict(prop_r=dict(type="linstock", angle=ang)))
    else:
        p = blend(cast, LIGHT[cast], EARS[cast], duck, {})
        if duck < 0.5:
            p["prop_r"] = dict(type="linstock", angle=32.0)
    p["mirror"] = mirror                                   # gunner_a: gun screen-left (mirror); gunner_b: gun screen-right
    p["match_glow"] = 1.0
    p["t"] = g / 30.0
    p["head_roll"] = p.get("head_roll", 0) + 2.0 * math.sin(g * 0.17 + seed)
    p["lean"] = p.get("lean", 0) + 1.5 * math.sin(g * 0.11 + seed)
    if duck <= 0.3:
        p["blink"] = blink(g, [1050 + int(seed * 7), 1088 + int(seed * 5), 1118])
    return p


# ----------------------------------------------------------------------------- runtime dressing: fuse sparks at gun 3's touch hole
def make_sparks():
    m = bpy.data.materials.new("s14_spark"); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs["Color"].default_value = (1.0, 0.75, 0.3, 1.0); em.inputs["Strength"].default_value = 30.0
    out = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(em.outputs[0], out.inputs[0])
    obs = []
    for k in range(9):
        me = bpy.data.meshes.new("s14_spark_%d" % k)
        import bmesh
        bm = bmesh.new(); bmesh.ops.create_uvsphere(bm, u_segments=6, v_segments=4, radius=0.035); bm.to_mesh(me); bm.free()
        ob = bpy.data.objects.new("s14_spark_%d" % k, me); ob.data.materials.append(m)
        ob.visible_shadow = False; ob.visible_diffuse = False; ob.visible_glossy = False
        bpy.context.scene.collection.objects.link(ob); obs.append(ob)
    ld = bpy.data.lights.new("s14_fuse", "POINT"); ld.color = (1.0, 0.7, 0.35); ld.shadow_soft_size = 0.1; ld.energy = 0.0
    lo = bpy.data.objects.new("s14_fuse", ld); lo.location = TOUCH + Vector((0, 0, 0.2)); bpy.context.scene.collection.objects.link(lo)
    return obs, lo


def key_sparks(obs, lo, f, g):
    on = G_TOUCH <= g < G_FIRE
    for k, ob in enumerate(obs):
        ph = ((g * 0.37 + k * 0.29) % 1.0)
        a = k * 2.4 + g * 0.9
        ob.location = TOUCH + Vector((0.45 * ph * math.cos(a), 0.3 * ph * math.sin(a), 0.1 + 0.7 * ph - 0.6 * ph * ph))
        s = 1.0 - ph
        ob.scale = (s, s, s)
        ob.hide_render = not on
        ob.keyframe_insert("location", frame=f); ob.keyframe_insert("scale", frame=f); ob.keyframe_insert("hide_render", frame=f)
    lo.data.energy = (60.0 + 40.0 * math.sin(g * 2.7) ** 2) if on else 0.0
    lo.data.keyframe_insert("energy", frame=f)


class Take(C.Take):
    def __init__(self, quality="preview", shot=1):
        C.Take.__init__(self, "wall_site", "cannon_line", quality=quality, lens=LENS[1], name="cam_s14", light="BATTLE")
        self.ga = self.actors["ga"] = C.make_actor("ga", "gunner_a", os.path.join(TMP, "sprites"))
        self.gb = self.actors["gb"] = C.make_actor("gb", "gunner_b", os.path.join(TMP, "sprites"))
        self.sparks, self.fuse = make_sparks()

    def pose(self, shot, gs):
        for g in gs:
            f = bf(shot, g)
            loc, look = cam_of(shot, g)
            self.key_cam(f, loc, look, lens=LENS[shot])
            C.place(self.ga, f, GUN_A); C.place(self.gb, f, GUN_B)
            W.set_flames(1.0, frame=f)
            W.set_smoke(1.0, frame=f)
            W.set_army(True, frame=f)
            W.set_wall_height("lin", 26, frame=f); W.set_wall_height("general", 30, frame=f)
            W.set_cauldron_steam(0.4, frame=f)
            W.set_impact("general", 0, impact_t(g) if shot == 2 else 0.0, frame=f)
            key_sparks(self.sparks, self.fuse, f, g if shot == 2 else 0)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            if shot == 1:
                ca = u_of(g, *G_CROUCH_A); cb = u_of(g, G_CROUCH_A[0] + 4, G_CROUCH_A[1] + 4) * 0.55
                pa = pose_gunner("gunner_a", g, ca, seed=0.0)
                pb = pose_gunner("gunner_b", g, cb, seed=1.3, mirror=False)
            else:
                pa = pose_gunner("gunner_a", g, 1.0, duck=u_of(g, G_DUCK[0] + 3, G_DUCK[1] + 3), seed=0.0)
                pb = pose_gunner("gunner_b", g, max(0.55, u_of(g, *G_CROUCH_B)), duck=u_of(g, *G_DUCK), seed=1.3, mirror=False)
            self.ga.pose(f, pa, camera=self.cam)
            self.gb.pose(f, pb, camera=self.cam)
        self.sprites_for([(self.ga, PPD[shot]), (self.gb, PPD[shot])], [bf(shot, g) for g in gs])

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look = cam_of(shot, g)
        rep = dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], heads=C.head_report(self, f), impact_t=round(impact_t(g), 4) if shot == 2 else 0)
        an = self.anch.get(("gb", f), {})
        for k in ("match_r", "match_l"):
            if k in an:
                w = actors.local_to_world(self.gb, an[k], f, camera=self.cam)
                rep["match_world"] = [round(v, 2) for v in w]
                rep["match_to_touch"] = round((w - TOUCH).length, 2)
        return rep

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    shot = int(sys.argv[2])
    if cmd in ("probe", "stills"):
        Tk = Take("preview", shot)
        gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
        Tk.pose(shot, gs)
        for g in gs:
            print(json.dumps(Tk.report(shot, g)), flush=True)
            if cmd == "stills":
                out = sys.argv[4]; os.makedirs(out, exist_ok=True)
                scale = float(sys.argv[5]) if len(sys.argv) > 5 else 1.0
                samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
                st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
                print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q: Take(q), [shot], sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
