#!/usr/bin/env python3
"""shot.py -- film 16 take s21 = shot 21 (44.87-46.02 s): LINE line_trench_end / RAIN.  Morse crouched at the test key on the crate
presses: nothing (the lever goes down twice, no spark, no click); Cornell holds his slouch hat over him; a worker waits, arms folded.
Rain streaks (thin), dark puddle.  Shot g 1346..1380; handles 9 each side (hard cut in, dissolve out into shot 22): first_g 1337, 53 frames.
    python3 shot.py probe|stills a:b[:step] [out scale samples]  /  python3 shot.py camreport  /  python3 shot.py final a:b[:step] [scale samples]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c16 as C
from mathutils import Vector, Matrix, Euler
TG, K, LN, actors, cast16 = C.TG, C.K, C.LN, C.actors, C.cast16
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

G0, G1 = C.g_bound(40.86), C.g_bound(42.27)       # 1226 .. 1268 (exclusive)
H = 9
GF, GL = G0 - H, G1 + H - 1
G_PLANT = C.cap_g("ลวดบนเสาไม้") + 9              # 1258: the pole reaches the vertical and is planted; the wire goes on the bare top
PRESET, LIGHT = "line_wide", "DAY"
PPD = 192
TILT0 = 40.0                                        # deg from the vertical at the first frame (leaning toward the crew, +y)
CAM_OFF = (-6.2, 6.5, -2.0)
POLE_I = 3
MIRROR = {"mor": False, "wa": False, "wb": False}
HAND_Z = {"mor": 2.7, "wa": 2.3, "wb": 2.9}         # height on the pole each person grips with the right hand (D)
OFS = {"mor": (0.0, 0.6), "wa": (-1.0, -0.9), "wb": (1.4, 0.5)}   # (dx along the line, dy behind the pole) of each person's feet from the pole axis


def tilt_deg(g):
    """pole lean (deg): eased out so it settles into the hole, 0 from G_PLANT on."""
    return TILT0 * (1.0 - C.u_of(g, GF, G_PLANT, "sine")) ** 1.0


def pole_pt(base, g, s):
    th = math.radians(tilt_deg(g))
    return base + Vector((0.0, s * math.sin(th), s * math.cos(th)))


def pose_of(key, name, g):
    p = dict(cast16.STORY16[name][1]); p["mirror"] = MIRROR[key]
    p.pop("prop_r", None); p.pop("prop_l", None)      # the real set pole is in their hands (pinned)
    p["lean"] = p.get("lean", 0) + 2.0 * math.sin(g * 0.3 + hash(key) % 5)
    p["blink"] = blink(g, [1236 + hash(key) % 7, 1252])
    p["gaze"] = (0.9, -1.0)                              # eyes up the pole to its top
    p["expr"] = "determined"
    return p


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s19")
        TG.set_ladder(False, 3); TG.set_train(None)
        for ob in C.bpy.data.objects:                     # furrow leftovers (trench 0): clipped slabs / dark holes in the ground
            if ob.name.startswith(("trench_", "pipe_")):
                ob.hide_render = True
        TG.set_poles("bare", 4)                          # poles 0..3 and the spans between them (static); span 2 (pole 2 -> pole 3) is keyed below
        P = TG.STATE["poles"][POLE_I]
        self.base = Vector(K.W((P["x"], P["y"], 0.0)))
        self.pivot = C.bpy.data.objects.new("pole3_pivot", None)
        self.scene.collection.objects.link(self.pivot)
        self.pivot.location = self.base
        C.bpy.context.view_layer.update()
        for ob in P["body"]:                             # pole 3 pivots about its foot
            ob.parent = self.pivot
            ob.matrix_parent_inverse = self.pivot.matrix_world.inverted()
        self.span2 = TG.STATE["spans_bare"][2]
        self.mk = {k: (self.base.x + OFS[k][0], self.base.y + OFS[k][1], 0.0) for k in OFS}
        d = os.path.join(WORK, "sprites")
        cv = cast16.CANVAS16_POLE
        self.mor = self.actors["mor"] = C.make_actor("mor", "morse16", d, canvas=cv["morse16"], cam=self.cam, shadow="proxy")
        self.wa = self.actors["wa"] = C.make_actor("wa", "worker16_a", d, canvas=cv["worker16_a"], cam=self.cam, shadow="proxy")
        self.wb = self.actors["wb"] = C.make_actor("wb", "worker16_b", d, canvas=cv["worker16_b"], cam=self.cam, shadow="proxy")
        look0 = Vector((self.base.x + 0.2, self.base.y + 1.0, 3.75))
        self.cam_path = C.CamPath(look0 + Vector(CAM_OFF), look0, GF, GL, push=-0.06, slide_px=-85.0, arc_deg_s=0.0, decay=0.3,
                                  snaps=[dict(g=(G_PLANT - 15, G_PLANT - 2), k=1.65, peak=2.0, shift=(1.8, 0.0))])
        self.key_cam(bf(GF), *self.cam_path.at(GF))
        self.scene.frame_set(bf(GF))

    def feet_of(self, k, g):
        """each person walks forward as the pole rises so the grip stays in reach: feet y = grip point y + offset."""
        pt = pole_pt(self.base, g, self.s_of(k, g))
        return (self.base.x + OFS[k][0], pt.y + OFS[k][1], 0.0)

    def s_of(self, k, g):
        th = math.radians(tilt_deg(g))
        return min(8.6, HAND_Z[k] / max(0.2, math.cos(th)))

    def pose(self, gs):
        for g in gs:
            f = bf(g)
            self.key_cam(f, *self.cam_path.at(g))
            self.pivot.rotation_euler = (-math.radians(tilt_deg(g)), 0.0, 0.0)
            self.pivot.keyframe_insert("rotation_euler", frame=f)
            C.key_vis(self.span2, g >= G_PLANT, f)          # the wire goes on the bare top at the plant
            for k, a in (("mor", self.mor), ("wa", self.wa), ("wb", self.wb)):
                C.place(a, f, self.feet_of(k, g))
        self.herr = {}
        for g in gs:
            f = bf(g); self.scene.frame_set(f)
            for k, a, nm in (("mor", self.mor, "morse_raise_pole"), ("wa", self.wa, "worker_a_raise_pole"), ("wb", self.wb, "worker_b_raise_pole")):
                s = self.s_of(k, g)
                hands = {"r": {"hand": tuple(pole_pt(self.base, g, s))}, "l": {"hand": tuple(pole_pt(self.base, g, s - 0.9))}}
                _, inf = a.pose(f, pose_of(k, nm, g), hands=hands, camera=self.cam)
                self.herr[(k, g)] = round(max([v.get("error", 0.0) for v in inf.values()] or [0.0]), 2)
        self.sprites_for([(self.mor, PPD), (self.wa, PPD), (self.wb, PPD)], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g); self.scene.frame_set(f)
        loc, look = self.cam_path.at(g)
        return dict(g=g, cam=[round(c, 3) for c in loc], heads=C.head_report(self, f), tilt=round(tilt_deg(g), 1),
                    herr={k: self.herr.get((k, g)) for k in ("mor", "wa", "wb")},
                    top_px=C.TG.project(tuple(self.base + Vector((0, 0, 9.25)))) if False else None)

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    gs = [g for g in C.parse(sys.argv[2]) if GF <= g <= GL]
    if cmd in ("probe", "stills"):
        Tk = Take("preview"); Tk.pose(gs)
        for g in gs:
            print(json.dumps(Tk.report(g)), flush=True)
            if cmd == "stills":
                out = sys.argv[3]; scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
                samples = int(sys.argv[5]) if len(sys.argv) > 5 else 6
                st = Tk.render([g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else TG.FINAL_SAMPLES["line"]
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take("final" if scale >= 1.0 else "preview"), gs, out, scale=scale, samples=samples)
