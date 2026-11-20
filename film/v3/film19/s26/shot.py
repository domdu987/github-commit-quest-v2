"""shot.py -- film 19 take s26 = shot 26 (HALL hall_table EVENING), THE LAST SHOT: "แล้วสภาก็ต้องควักเงินจ่ายให้ไอ้ช่างไม้".
A fat money bag (set_moneybag 'full', dropped from above with a bounce by keying its object) lands on the Board table in front of old
Harrison at "ต้องควักเงิน" (caption 70.12 s -> g 2107); the King (far end, king_stand) nods; Harrison grins and bounces.  The ten candle
stubs of shot 24 stay (set_stubs 10), the King's chair and the regulator on.  Push-in with a snap on "ช่างไม้" (71.46 s -> g 2147);
the film ENDS ON A HARD CUT while the camera is still moving: g 2086..2159 (the film is N = 2160 frames: the narration plus 0.10 s
ends at film 72.0 s; the plan's t1 71.90 is the narration clock).  9 f in-handle (hard cut in), no out-handle (end of film).
No DOF, no text, no caption_shade.
    python3 shot.py camreport | probe a:b[:step] | stills a:b[:step] out [scale] [spp] | final a:b[:step] [scale] [spp]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c19 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

H, K, actors, cast19 = C.H, C.K, C.actors, C.cast19
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

G0, G1 = C.g_bound(69.55), C.N_FILM                    # 2086 .. 2159 (film end at g 2160)
H_IN, H_OUT = 9, 0
G_FIRST, G_LAST = G0 - H_IN, G1 + H_OUT - 1
GS = list(range(G_FIRST, G_LAST + 1))
G_BAG = C.cap_g("ต้องควักเงิน")                          # 2107: the bag lands
G_DROP = G_BAG - 8                                       # it falls for 8 frames
G_SNAP = C.g_of(71.46)                                   # 2147: "ช่างไม้", the last word (caption 71.46)
SNAP = (G_SNAP - 4, G_SNAP + 10)
PRESET, LIGHT, FINAL_SPP, PPD = "hall_table", "EVENING", 8, 256
BLINKS_H, BLINKS_K = [2095, 2125, 2150], [2100, 2130]

HAR_M = (-0.90, 1.70, 0.0)                               # D: BEHIND the table edge (near edge y 1.1 D); the bag lands in front of him
KING_M = (0.10, 5.60, 0.0)                               # D: beside the table head, clear of Harrison
BAG_XY_M = (0.15, 0.80)                                  # metres on the tabletop: right of Harrison, near edge (lower third of the frame)
BAG_SCALE = 1.6
N_COINS = 10
CAM_LOC0 = (-1.00, -2.70, 3.60)
CAM_LOOK0 = (-0.90, 1.80, 2.30)
CAM = C.CamPath(CAM_LOC0, CAM_LOOK0, G_FIRST, G_LAST, push=0.11, slide_px=0.0, rise_px=8.0, arc_deg_s=11.0, decay=0.10,
                snaps=[dict(g=SNAP, k=1.10, peak=3.5, shift=(1.40, 0.90))])

HB = dict(cast19.STORY19["harrison_old_idle"][1])
KB = dict(cast19.STORY19["king_idle"][1])


def bag_dz(g):
    """height above the table (D): falls from 7 D in 8 frames (ease-in), then two decaying bounces."""
    if g < G_DROP:
        return 7.0
    if g < G_BAG:
        u = (g - G_DROP) / float(G_BAG - G_DROP)
        return 7.0 * (1.0 - u * u)
    t = (g - G_BAG) / 30.0
    return 0.55 * abs(math.sin(math.pi * t / 0.32)) * math.exp(-t / 0.25) if t < 0.7 else 0.0


def bag_squash(g):
    """z scale of the bag: 0.8 for 2 frames on the land, a small rebound."""
    d = g - G_BAG
    return {0: 0.78, 1: 0.82, 2: 0.95, 3: 1.06, 4: 1.0}.get(d, 1.0)


def pose_har(g):
    p = dict(HB)
    p.update(old=1, yaw=0.15, expr="grinning", mouth="smile")
    t = g / 30.0
    u = u_of(g, G_BAG, G_BAG + 8, kind="sine")                 # arms come to the bag
    up = u_of(g, G_BAG + 22, G_BAG + 30, kind="sine")          # then he looks up and grins at the lens
    bob = 0.04 * math.sin(t * 12.0)
    joy = u_of(g, G_BAG + 14, G_BAG + 24, kind="sine")         # arms rise with joy once he looks up
    p["arm_r"] = dict(hand=(lerp(lerp(0.30, 0.55, u), 0.95, joy), lerp(lerp(1.17, 0.95, u), 0.35, joy) + bob), bend=0.2, shape="open", layer="front")
    p["arm_l"] = dict(hand=(lerp(lerp(-0.30, -0.45, u), -0.80, joy), lerp(lerp(1.17, 0.85, u), 0.45, joy) + bob), bend=0.2, shape="open", layer="front")
    p["prop_l"] = dict(type="h4_watch", scale=1.4)             # the H4 in his left hand (continuity)
    p["lean"] = 5.0 + 4.0 * u * (1.0 - up) + 1.5 * math.sin(t * 9.0)
    p["pitch"] = 0.0 + 0.30 * u * (1.0 - up)                    # head bowed to the bag
    p["yaw"] = 0.15 + 0.30 * u * (1.0 - up)
    p["head_roll"] = -2.0 + 3.0 * math.sin(t * 7.0)
    if g <= G_BAG:
        p["gaze"] = (0.3, 0.6)
    else:
        p["gaze"] = (lerp(0.6, 0.15, up), lerp(-0.5, 0.05, up))   # down at the bag, then at the lens
    p["blink"] = blink(g, BLINKS_H)
    p["t"] = t
    return p


def pose_king(g):
    p = dict(KB)
    t = g / 30.0
    p.update(expr="happy", mouth="smile", yaw=0.2)
    nod = 0.0
    if g >= G_BAG + 6:                                          # bigger nods after the bag lands
        nod = 1.00 * max(0.0, math.sin(2 * math.pi * (g - G_BAG - 6) / 22.0)) * (1.0 if g < G_BAG + 6 + 66 else 0.0)
    p["pitch"] = 0.05 + nod
    p["head_roll"] = 2.0 * math.sin(t * 6.0)
    p["lean"] = 1.0 + 1.0 * math.sin(t * 8.0)
    p["blink"] = blink(g, BLINKS_K)
    return p


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s26")
        assert self.final_samples() == FINAL_SPP, "set final samples changed: %s" % self.final_samples()
        self.key_cam(bf(G_FIRST), *CAM.at(G_FIRST))
        self.scene.frame_set(bf(G_FIRST))
        sd = os.path.join(WORK, "sprites")
        self.har = self.actors["har"] = C.make_actor("har", "harrison19", sd, contact=dict(width=1.1, depth=0.5, opacity=0.8), cam=self.cam)
        self.king = self.actors["king"] = C.make_actor("king", "king19", sd, contact=True, cam=self.cam)
        self.bag = K.STATE["hooks"]["bag_full"]
        self.bag0 = Vector((BAG_XY_M[0], BAG_XY_M[1], self.bag.location.z))   # on the tabletop in front of Harrison
        self._make_coins()

    def _make_coins(self):
        """runtime set dressing: N_COINS gold coins spill out of the bag when it lands (g G_BAG..), plus a warm key light over the bag."""
        bpy = C.bpy
        mat = bpy.data.materials.new("coin_gold")
        mat.use_nodes = True
        b = mat.node_tree.nodes["Principled BSDF"]
        b.inputs["Base Color"].default_value = (0.95, 0.72, 0.18, 1.0)
        b.inputs["Metallic"].default_value = 0.9
        b.inputs["Roughness"].default_value = 0.30
        if "Emission Color" in b.inputs:
            b.inputs["Emission Color"].default_value = (1.0, 0.7, 0.15, 1.0)
            b.inputs["Emission Strength"].default_value = 0.6
        self.coins, self.coin_plan = [], []
        rnd = __import__("random").Random(19)
        base = Vector(K.W((BAG_XY_M[0], BAG_XY_M[1], 0.812)))
        for i in range(N_COINS):
            bpy.ops.mesh.primitive_cylinder_add(vertices=20, radius=0.075, depth=0.014)
            ob = bpy.context.active_object
            ob.name = "coin%d" % i
            ob.data.materials.append(mat)
            ob.parent = None
            ang = rnd.uniform(0, 2 * math.pi)
            dist = rnd.uniform(0.35, 0.95)
            self.coins.append(ob)
            self.coin_plan.append((ang, dist, rnd.uniform(0, 1.0), rnd.uniform(-60, 60), rnd.randint(0, 2)))
        self.coin_base = base
        ld = bpy.data.lights.new("bag_key", "POINT")
        ld.energy = 45.0
        ld.color = (1.0, 0.78, 0.45)
        ld.shadow_soft_size = 0.3
        self.bag_light = bpy.data.objects.new("bag_key", ld)
        bpy.context.scene.collection.objects.link(self.bag_light)
        self.bag_light.location = base + Vector((0.0, -0.6, 1.4))

    def pose(self, gs):
        hm = Vector((HAR_M[0], HAR_M[1], 0.0))
        km = Vector(KING_M)
        for g in gs:
            f = bf(g)
            self.key_cam(f, *CAM.at(g))
            C.place(self.har, f, hm + Vector((0, 0, 0.07 * abs(math.sin(2 * math.pi * g / 16.0)) * u_of(g, G_BAG + 14, G_BAG + 20))))
            C.place(self.king, f, km)
            self.key_set(f, candles=1.0, regulator=True, kings_chair=True, stubs=10, moneybag="full" if g >= G_DROP else "none", box="none")
            if g >= G_DROP:                                       # the fall + bounces: key the bag object (local metres under the scaled root)
                self.bag.location = self.bag0 + Vector((0, 0, bag_dz(g) / 1.85))
                self.bag.keyframe_insert("location", frame=f)
                sz = bag_squash(g)
                self.bag.scale = Vector((BAG_SCALE / sz ** 0.5, BAG_SCALE / sz ** 0.5, BAG_SCALE * sz))
                self.bag.keyframe_insert("scale", frame=f)
            for ob, (ang, dist, dly, tilt, _k) in zip(self.coins, self.coin_plan):     # coin spill: launched at the land, arc, settle flat on the baize
                t = (g - G_BAG - dly * 3.0) / 30.0
                vis = g >= G_BAG
                if t < 0:
                    pos = self.coin_base + Vector((0, 0, 0.1))
                    h = 0.1
                else:
                    u = min(t / 0.45, 1.0)
                    r = dist * (1.0 - (1.0 - u) ** 2) * 1.0
                    h = 0.1 + 0.9 * 4 * u * (1 - u) * 0.6 if u < 1.0 else 0.02
                    pos = self.coin_base + Vector((math.cos(ang) * r, math.sin(ang) * r * 0.7, h if u < 1.0 else 0.02))
                ob.location = pos
                ob.rotation_euler = (math.radians(tilt * (1.0 - min(t / 0.45, 1.0)) if t > 0 else 0.0), 0, 0)
                ob.keyframe_insert("location", frame=f)
                ob.keyframe_insert("rotation_euler", frame=f)
                C.key_vis([ob], vis, f)
            self.bag_light.hide_render = False
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.har.pose(f, pose_har(g), camera=self.cam)
            self.king.pose(f, pose_king(g), camera=self.cam)
        self.sprites_for([(self.har, PPD), (self.king, PPD)], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = CAM.at(g)
        return dict(g=g, cam=[round(c, 3) for c in loc], heads=C.head_report(self, f), dof=self.cam.data.dof.use_dof,
                    caption_shade=bool(C.bpy.data.objects.get("caption_shade")), bag_dz=round(bag_dz(g), 2))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        rows, worst = CAM.report(GS[:-1])
        print([r["px"] for r in rows])
        print("longest run under 0.25 px/frame: %d frames (bible max 6)" % worst)
        sys.exit(0)
    gs = [g for g in C.parse(sys.argv[2]) if G_FIRST <= g <= G_LAST]
    if cmd in ("probe", "stills"):
        Tk = Take("preview")
        Tk.pose(gs)
        for g in gs:
            print(json.dumps(Tk.report(g)), flush=True)
            if cmd == "stills":
                out = sys.argv[3]
                scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
                samples = int(sys.argv[5]) if len(sys.argv) > 5 else 6
                st = Tk.render([g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else None
        quality = "final" if scale >= 1.0 else "preview"
        samples = samples or FINAL_SPP
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take(quality), gs, out, scale=scale, samples=samples)
