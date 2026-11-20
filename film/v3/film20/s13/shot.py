#!/usr/bin/env python3
"""shot.py -- film 20 take s13 = shot 13, SITE site_rivet / DAY stage 1.  g 907..944 + 4-frame handles each side (g 903..948, cuts).
"หมุดสองล้านครึ่งตัว": on the rivet deck one worker tosses a glowing rivet with tongs, another catches it in a bucket, a third hammers
(sparks); close-medium, snap push on the catch.
    python3 shot.py probe a:b[:step] | camreport | stills a:b[:step] out [scale] [spp] | final a:b[:step] [scale] [spp]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c20 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

S, CO, actors, cast20 = C.S, C.CO, C.actors, C.cast20
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

G0, G1 = C.g_bound(30.23), C.g_bound(31.49)        # 907, 945
H_IN, H_OUT = 4, 4
G_FIRST, G_LAST = G0 - H_IN, G1 + H_OUT - 1        # 903 .. 948
GS = list(range(G_FIRST, G_LAST + 1))
G_TOSS = (911, 921)                                # the rivet flies (k 0 -> 1)
G_CATCH = G_TOSS[1]                                # 921: lands in the bucket -> snap push
G_HITS = [913, 922, 931, 940, 949]                 # hammer blows (period 9)
LIGHT, PRESET = "DAY", "site_rivet"
PPD = 256


def cam_path(A):
    """close-medium on the deck from the neighbouring scaffold; the deck marks are in A['marks'] (world D)."""
    m = {k: Vector(A["marks"][k]) for k in ("riveter_tongs", "riveter_catch", "riveter_hammer")}
    subj = (m["riveter_tongs"] + m["riveter_catch"]) * 0.5 + Vector((0.0, 0.0, 2.4))
    c0 = Vector(A["cams"][PRESET]["loc"])
    v = (c0 - subj)
    v.z = 0.0
    c = subj + v.normalized() * CAMDIST + Vector((0.0, 0.0, -1.0))
    return C.CamPath(c, subj, G_FIRST, G_LAST, push=0.07, slide_px=55.0, rise_px=15.0, arc_deg_s=3.0, tilt0=0.0, decay=0.2,
                     snaps=[dict(g=(G_CATCH - 1, G_CATCH + 12), k=1.5, peak=1.7, shift=(0.0, -0.3), tilt=0.0)])


CAMDIST = 11.0                                     # D from the subject point (~5.8 m): close-medium


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s13")
        self.path = cam_path(self.A)
        for ob in C.bpy.data.objects:
            if ob.name.startswith("fg_"):
                ob.hide_render = True
        self.key_cam(C.bf(G_FIRST), *self.path.at(G_FIRST))
        self.scene.frame_set(C.bf(G_FIRST))
        mk = self.A["marks"]
        self.mk = dict(t=Vector(mk["riveter_tongs"]), c=Vector(mk["riveter_catch"]), h=Vector(mk["riveter_hammer"]))
        for who, cast in (("t", "riveter_tongs"), ("c", "riveter_hammer"), ("h", "riveter_forge")):
            self.actors[who] = C.make_actor(who, cast, os.path.join(WORK, "sprites"), cam=self.cam,
                                            contact=dict(width=1.2, depth=0.5, opacity=0.8))

    def hit_phase(self, g):
        """0 -> 1 over the wind-up before the nearest blow, 1 at the blow (g in G_HITS), then back"""
        d = min(abs(g - h) for h in G_HITS)
        return clamp(1.0 - d / 4.0)

    def pose(self, gs):
        for g in gs:
            f = bf(g)
            self.key_cam(f, *self.path.at(g))
            for who, a in self.actors.items():
                C.place(a, f, tuple(self.mk[who]))
            k = clamp((g - G_TOSS[0]) / float(G_TOSS[1] - G_TOSS[0]))
            S.set_stage(1, frame=f)
            S.spark(frame=f, t0=G_HITS[0], period=9, strength=1.5)
            S.rivet_toss(k if G_TOSS[0] <= g <= G_TOSS[1] else None, frame=f)
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            t = g / 30.0
            # tongs man: holds the glowing rivet, throws at G_TOSS[0] (pose riveter_tongs_throw), then reaches for the next
            pt = dict(cast20.STORY20["riveter_tongs_work"][1])
            if g >= G_TOSS[0] - 2:
                pt = dict(cast20.STORY20["riveter_tongs_throw"][1])
            if g > G_TOSS[0] + 3:
                pt["prop_r"] = dict(type="tongs_cold", angle=-5)
            pt["glow"] = 0.75 + 0.25 * math.sin(t * 17.0)
            pt["lean"] = pt.get("lean", 0) + 2.0 * math.sin(t * 5.0)
            pt["blink"] = blink(g, [909, 936])
            pt["t"] = t
            self.actors["t"].pose(f, pt, camera=self.cam)
            # catcher: bucket low in front, flinches/cheers at the catch
            pc = dict(cast20.STORY20["riveter_hammer_cheer" if g >= G_CATCH + 2 else "riveter_hammer_work"][1])
            if g < G_CATCH + 2:
                pc["arm_r"] = dict(hand=(0.7, 0.9), bend=0.2, stretch=1.1)
                pc["arm_l"] = dict(hand=(0.5, 0.95), bend=0.2, stretch=1.1)
                pc.pop("prop_r", None)
                pc["yaw"] = -0.4
                pc["lean"] = 6 + 3 * math.sin(t * 6.0)
            pc["blink"] = blink(g, [914, 940])
            pc["t"] = t
            self.actors["c"].pose(f, pc, camera=self.cam)
            # hammer man: wind up / blow every 9 frames
            ph = self.hit_phase(g)
            lo = dict(cast20.STORY20["riveter_hammer_work"][1])
            hi = dict(cast20.STORY20["riveter_hammer_hit"][1])
            ph_ = ph
            ph_blend = {k: hi[k] for k in hi} if ph_ > 0.6 else lo
            ph_blend = dict(ph_blend)
            ph_blend["prop_r"] = dict(type="rivet_hammer", angle=lerp(-70, 5, ph_))
            ph_blend["yaw"] = -0.45
            ph_blend["blink"] = blink(g, [917, 944])
            ph_blend["t"] = t
            self.actors["h"].pose(f, ph_blend, camera=self.cam)
        self.sprites_for([(a, PPD) for a in self.actors.values()], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        return dict(g=g, heads=C.head_report(self, f))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        Tk = Take("preview")
        rows, worst = Tk.path.report(range(G_FIRST, G_LAST))
        print(min(r["px"] for r in rows), max(r["px"] for r in rows), "longest parked", worst)
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
                samples = int(sys.argv[5]) if len(sys.argv) > 5 else 4
                st = Tk.render([g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else CO.FINAL_SPP
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take("final" if scale >= 1.0 else "preview"), gs, out, scale=scale, samples=samples)
