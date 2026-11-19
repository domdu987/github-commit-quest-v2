#!/usr/bin/env python3
"""shot.py -- film 16 take s26 = shot 26 (CHAMBER chamber_table / DAY): the register clicks twice ("ติ๊ด ติ๊ด" 57.66 / 57.97), the paper tape
spools out (dots and dashes only), Morse reads it, congressmen crowd round, amazed, the mocker's jaw drops.
Shot g 1707..1766 (56.90-58.89 s) + 9 handle frames each side (g 1698..1775).  Mouths still (jaw drop = a held expression mouth).
    g 1733  click 1 (57.66+0.10 s): SNAP push on the tape register (13 f), tape jumps out
    g 1742  click 2 (57.97): tape jumps again; the mocker's pose swaps sour -> JAW DROP on a blink; then slide to the faces
    python3 shot.py probe a:b | camreport | stills a:b[:s] out [scale] [spp] | final a:b[:s] [scale] [spp]"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c16 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402
import tg_chamber as CH                                  # noqa: E402
TG, K, actors, cast16 = C.TG, C.K, C.actors, C.cast16
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

G0, G1 = C.g_bound(56.90), C.g_bound(58.89)              # 1707, 1767 (shot = g 1707..1766)
H = 9
GS = list(range(G0 - H, G1 + H))                         # 1698..1775
G_LAST = GS[-1]
G_C1, G_C2 = C.g_of(57.66), C.g_of(57.97)                # 1733, 1742
SNAP = (G_C1 - 2, G_C1 + 11)
PPD = 256
LIGHT, PRESET = "DAY", "chamber_table"

# ---- cast: (key, STORY16 name before, after, world mark or point, mirror)
def P(name):
    return dict(cast16.STORY16[name][1])

CAST = dict(
    mor=dict(cast="morse16", at=(3.6, 10.9), pose="morse_read_tape", mirror=True),
    moc=dict(cast="mocker", at=(1.0, 11.4), pose="mocker_sour_arms", pose2="mocker_jaw_drop", swap=G_C2 + 3, mirror=False),
    ca=dict(cast="congressman_a", at=(2.4, 12.3), pose="congressman_a_amazed", mirror=True),
    cb=dict(cast="congressman_b", at=(-2.6, 11.3), pose="congressman_b_amazed", mirror=False),
    cc=dict(cast="congressman_c", at=(-0.5, 12.8), pose="congressman_c_amazed", mirror=True),
)
for k, v in CAST.items():
    v["seed"] = 3 + 7 * list(CAST).index(k)

def pose_of(k, g):
    v = CAST[k]
    name = v["pose"] if g < v.get("swap", 1 << 30) else v["pose2"]
    p = P(name)
    s = v["seed"]
    p["mirror"] = v["mirror"]
    p["blink"] = blink(g, [g0 for g0 in range(s + 3, 3000, 37 + s % 5) if abs(g0 - g) < 3] + ([v["swap"] - 1] if "swap" in v else []))
    t = g / 30.0
    p["lean"] = p.get("lean", 0) + 2.5 * math.sin(t * 5.1 + s)
    p["head_roll"] = p.get("head_roll", 0) + 2.0 * math.sin(t * 3.9 + s)
    p["squash"] = (1.0 + 0.012 * math.sin(t * 9.0 + s), 1.0 - 0.012 * math.sin(t * 9.0 + s))     # excited tremble
    if k == "mor":
        p["gaze"] = (-0.6, 0.9)       # eyes on the tape
    p["t"] = t
    return p

def foot(k, g):
    x, y = CAST[k]["at"]
    bob = 0.05 * math.sin(g * 0.55 + CAST[k]["seed"]) if k != "mor" else 0.03 * math.sin(g * 0.5)
    return (x, y, bob)

# ---- camera
class Cam(C.CamPath):
    """CamPath + eased look-point travel (shift of camera AND look point, world D) after g_shift."""
    def __init__(self, *a, travel=None, **k):
        C.CamPath.__init__(self, *a, **k)
        self.travel = travel or []
    def at(self, g):
        loc, look = C.CamPath.at(self, g)
        for (ga, gb, v) in self.travel:
            u = C.u_of(g, ga, gb, "sine")
            loc = loc + Vector(v) * u
            look = look + Vector(v) * u
        return loc, look

TAPE_PT = (1.45, 8.1, 1.9)
CAM_LOOK0 = (1.2, 8.6, 2.5)
CAM_LOC0 = (-1.4, 2.6, 4.3)
CAM = Cam(Vector(CAM_LOOK0).lerp(Vector(CAM_LOC0), 1.0), CAM_LOOK0, G0 - H, G_LAST, push=0.07, slide_px=-35.0, arc_deg_s=3.0, decay=0.2,
          snaps=[dict(g=SNAP, k=2.1, peak=1.7, shift=(0.4, -0.2))], travel=[(G_C2 + 2, G_C2 + 20, (0.9, 2.0, 1.0))])

class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s26")
        self.key_cam(bf(GS[0]), *CAM.at(GS[0]))
        self.scene.frame_set(bf(GS[0]))
        self.hp = {}
        # the register's paper drum reads as a big log in the foreground when the camera pushes in: cut it out of the table mesh (the tape still comes from the slot)
        import bmesh
        lo = Vector(K.W((CH.TG_C[0] - 0.4, CH.TG_C[1] - 0.2, 0.9625))); hi = Vector(K.W((CH.TG_C[0] + 1.45, CH.TG_C[1] + 0.9, 3.0)))
        for ob in TG.STATE["table_objs"]:
            if ob.name.endswith("brass"):                      # the brass roller beside the drum (a big gold log end to the lens)
                a_ = Vector(K.W((CH.TG_C[0] + 0.26 * CH.TG_S - 0.12, CH.TG_C[1] + 0.1 * CH.TG_S - 0.24, CH.TG_C[2] + 0.2 * CH.TG_S - 0.16)))
                b_ = Vector(K.W((CH.TG_C[0] + 0.26 * CH.TG_S + 0.12, CH.TG_C[1] + 0.1 * CH.TG_S + 0.24, CH.TG_C[2] + 0.2 * CH.TG_S + 0.16)))
                lo2 = Vector((min(a_.x, b_.x), min(a_.y, b_.y), min(a_.z, b_.z))); hi2 = Vector((max(a_.x, b_.x), max(a_.y, b_.y), max(a_.z, b_.z)))
                bm = bmesh.new(); bm.from_mesh(ob.data)
                dead = [v for v in bm.verts if lo2.x <= v.co.x <= hi2.x and lo2.y <= v.co.y <= hi2.y and lo2.z <= v.co.z <= hi2.z]
                bmesh.ops.delete(bm, geom=dead, context="VERTS")
                bm.to_mesh(ob.data); bm.free()
            if ob.name.endswith("paper"):
                bm = bmesh.new(); bm.from_mesh(ob.data)
                dead = [v for v in bm.verts if lo.x <= v.co.x <= hi.x and lo.y <= v.co.y <= hi.y and v.co.z > lo.z]
                bmesh.ops.delete(bm, geom=dead, context="VERTS")
                bm.to_mesh(ob.data); bm.free()
        for k, v in CAST.items():
            cv = cast16.CANVAS16[v["cast"]]
            self.actors[k] = C.make_actor(k, v["cast"], os.path.join(WORK, "sprites"), canvas=cv, contact=True, cam=self.cam)
    def pose(self, gs):
        for g in gs:
            f = bf(g)
            self.key_cam(f, *CAM.at(g))
            for k, a in self.actors.items():
                x, y, z = foot(k, g)
                C.place(a, f, (x, y, z))
            u1, u2 = u_of(g, G_C1, G_C1 + 5), u_of(g, G_C2, G_C2 + 5)
            ln = 0.04 + 0.26 * u1 + 0.30 * u2 + 0.34 * u_of(g, G_C2 + 4, G_C2 + 30)
            click = 1 if (G_C1 <= g < G_C1 + 3 or G_C2 <= g < G_C2 + 3) else 0
            self.key_set(f, tape=(ln, click), flames=(1.0,))
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            for k, a in self.actors.items():
                a.pose(f, pose_of(k, g), camera=self.cam)
        self.sprites_for([(a, PPD) for a in self.actors.values()], [bf(g) for g in gs])
    def report(self, g):
        f = bf(g)
        loc, look = CAM.at(g)
        return dict(g=g, cam=[round(c, 2) for c in loc], heads=C.head_report(self, f))
    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        rows, worst = CAM.report(GS[:-1])
        print(rows[::5]); print("longest run under 0.25 px/frame: %d" % worst); sys.exit(0)
    gs = [g for g in C.parse(sys.argv[2]) if GS[0] <= g <= G_LAST]
    if cmd in ("probe", "stills"):
        Tk = Take("preview"); Tk.pose(gs)
        for g in gs:
            print(json.dumps(Tk.report(g)), flush=True)
            if cmd == "stills":
                out = sys.argv[3]; scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5; spp = int(sys.argv[5]) if len(sys.argv) > 5 else 6
                st = Tk.render([g], out, scale=scale, samples=spp)[0]
                os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else TG.FINAL_SAMPLES["chamber"]
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take("final" if scale >= 1.0 else "preview"), gs, out, scale=scale, samples=samples)
