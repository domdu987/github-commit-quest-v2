#!/usr/bin/env python3
"""shot.py -- film 13 take s01: shot 1 (g 0..62 + out-handle 63..68), the HOOK: hotel_front DAY, worm's-eye, the whole six-storey hotel
rising (h 0.55 -> 0.65), crib pier + jack in the foreground, pullman below calm and confident, workers beside.  Slow crane up.
    python3 shot.py probe a:b[:step] | stills a:b[:step] <out_dir> [scale] [samples] | final a:b[:step] [scale] [samples]
Blender frame of g = 1000 * (id-1) + g + 1 with id = 1."""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import c13 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402
D, actors, camrig, cast13 = C.D, C.actors, C.camrig, C.cast13
lerp, clamp, blink, ez, bf = C.lerp, C.clamp, C.blink, C.ez, C.bf
TMP = os.path.join(HERE, "work")
G1 = C.g_bound(2.10)                  # 63: shot 2 starts
H_OUT = 6
RANGES = {1: (0, G1 + H_OUT - 1)}
PRESET, LIGHT = "hotel_front", "DAY"
H0, H1 = 0.55, 0.65                   # lift 0.55 -> 0.65 over the shot (continues through the handle)
CAM0 = ((-4.6, -25.0, 0.45), (0.2, 0.0, 9.0))
CAM1 = ((-3.2, -24.2, 1.35), (0.0, 0.0, 12.2))
LENS = 17.0
PPD = 160
PULL_XY, WA_XY, WB_XY, WC_XY = (-1.0, -11.2), (-8.0, -10.0), (6.2, -10.5), (2.8, -9.8)


def cam_of(g):
    x = g / float(G1 - 1)
    u = 0.35 * ez(x, "sine") + 0.65 * x
    return Vector([lerp(CAM0[0][i], CAM1[0][i], u) for i in range(3)]), Vector([lerp(CAM0[1][i], CAM1[1][i], u) for i in range(3)])


def lift_of(g):
    return lerp(H0, H1, g / float(G1 - 1))


def p_pull(g):
    p = dict(cast13.STORY13["pullman_look_up_confident"][1])
    p["t"] = g / 30.0
    p["lean"] = p.get("lean", 0) + 1.2 * math.sin(g * 0.09)
    p["head_roll"] = p.get("head_roll", 0) + 1.5 * math.sin(g * 0.07)
    p["blink"] = blink(g, [22, 51])
    return p


def p_work(key, g, ph):
    p = dict(cast13.STORY13[key][1])
    p["lean"] = p.get("lean", 0) + 1.0 * math.sin(g * 0.08 + ph)
    p["head_roll"] = p.get("head_roll", 0) + 1.2 * math.sin(g * 0.06 + ph)
    p["blink"] = blink(g, [14 + int(ph * 5), 47 + int(ph * 3)])
    p["t"] = g / 30.0
    return p


def make_dust(n=46, seed=4):
    """a trickle of cream-grey dust motes falling from the hotel's base (runtime set dressing, camera-only soft discs)."""
    import bpy, random
    r = random.Random(seed); SET = D.STATE["SET"]
    mat = bpy.data.materials.new("s01_dust"); mat.use_nodes = True; nt = mat.node_tree; nt.nodes.clear()
    em = nt.nodes.new("ShaderNodeEmission"); em.inputs["Color"].default_value = (0.86, 0.74, 0.58, 1.0); em.inputs["Strength"].default_value = 0.9
    tr = nt.nodes.new("ShaderNodeBsdfTransparent"); mx = nt.nodes.new("ShaderNodeMixShader"); out = nt.nodes.new("ShaderNodeOutputMaterial")
    mx.inputs[0].default_value = 0.55
    nt.links.new(tr.outputs[0], mx.inputs[1]); nt.links.new(em.outputs[0], mx.inputs[2]); nt.links.new(mx.outputs[0], out.inputs[0])
    obs = []
    for i in range(n):
        bpy.ops.mesh.primitive_uv_sphere_add(radius=1.0, segments=8, ring_count=5)
        ob = bpy.context.active_object; ob.name = "s01_dust_%d" % i
        for c in list(ob.users_collection): c.objects.unlink(ob)
        SET.objects.link(ob); ob.data.materials.append(mat)
        ob.visible_shadow = False; ob.visible_diffuse = False; ob.visible_glossy = False
        ob.scale = (r.uniform(0.12, 0.3),) * 3
        ob["x"] = r.uniform(-17.0, 17.0); ob["y"] = r.uniform(-3.2, -0.6); ob["ph"] = r.random(); ob["sp"] = r.uniform(0.6, 1.2); ob["dr"] = r.uniform(-0.6, 0.6)
        obs.append(ob)
    return obs


def key_dust(obs, f, g, lift_z):
    for ob in obs:
        u = (ob["ph"] + g * 0.0145 * ob["sp"]) % 1.0              # 0 at the hotel base, 1 on the ground
        z = lift_z - 0.3 - u * (lift_z + 0.2)
        ob.location = (ob["x"] + ob["dr"] * u * 2.0, ob["y"] - u * 0.6, max(0.05, z))
        ob.hide_render = u > 0.97
        ob.keyframe_insert("location", frame=f); ob.keyframe_insert("hide_render", frame=f)


class Take(C.Take):
    def __init__(self, quality="preview", shot=1):
        C.Take.__init__(self, "street", PRESET, quality=quality, lens=LENS, name="cam_s01", light=LIGHT)
        sd = os.path.join(TMP, "sprites")
        self.pul = self.actors["pul"] = C.make_actor("pul", "pullman", sd)
        self.wa = self.actors["wa"] = C.make_actor("wa", "worker13_a", sd)
        self.wb = self.actors["wb"] = C.make_actor("wb", "worker13_b", sd)
        self.wc = self.actors["wc"] = C.make_actor("wc", "worker13_c", sd)
        self.dust = make_dust()

    def pose(self, shot, gs):
        for g in gs:
            f = bf(shot, g)
            loc, look = cam_of(g)
            self.key_cam(f, loc, look, lens=LENS)
            self.key_set(f, lift=lift_of(g))
            key_dust(self.dust, f, g, lift_of(g) * D.LIFT_MAX)
            C.place(self.pul, f, PULL_XY)
            C.place(self.wa, f, WA_XY)
            C.place(self.wb, f, WB_XY)
            C.place(self.wc, f, WC_XY)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            self.pul.pose(f, p_pull(g), camera=self.cam)
            self.wa.pose(f, p_work("worker_stand_a", g, 0.0), camera=self.cam)
            self.wb.pose(f, p_work("worker_stand_b", g, 1.7), camera=self.cam)
            self.wc.pose(f, p_work("worker_stand_c", g, 3.1), camera=self.cam)
        fr = [bf(shot, g) for g in gs]
        self.sprites_for([(self.pul, PPD), (self.wa, PPD), (self.wb, PPD), (self.wc, PPD)], fr)

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look = cam_of(g)
        v = look - loc
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    lift=round(lift_of(g), 3), heads=C.head_report(self, f))

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd in ("probe", "stills"):
        Tk = Take("preview")
        gs = [g for g in C.parse(sys.argv[2]) if RANGES[1][0] <= g <= RANGES[1][1]]
        Tk.pose(1, gs)
        for g in gs:
            print(json.dumps(Tk.report(1, g)), flush=True)
            if cmd == "stills":
                out = sys.argv[3]; os.makedirs(out, exist_ok=True)
                scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
                samples = int(sys.argv[5]) if len(sys.argv) > 5 else 6
                st = Tk.render(1, [g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "s1_g_%04d.png" % g))
                print("g %d %.1f s wall" % (g, st["wall"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else 12
        C.final_loop(lambda q: Take(q), [1], sys.argv[2], RANGES, HERE, scale=scale, samples=samples)
