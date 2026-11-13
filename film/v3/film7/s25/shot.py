#!/usr/bin/env python3
"""shot.py -- film 7 take s25: shot 25 (plan 81.48-85.77 s = g 2444..2572) + 6 handle frames each side (g 2438..2578), dissolve in.
Plan: room / under_bed_insert -> room_wide: the trunk under the bed slides out, the lid opens, the panel inside; vincenzo_peek_bed,
candlelight.  One location (the attic, under_bed_insert build, ATTIC_DUSK), three set-ups (framing change every 1.5-1.6 s):

    id 1  g 2438..2484  A  floor level under the bed by the floor candle: the trunk slides out toward us (pull 0 -> 0.75, g 2450..2482),
                           slow push.                                                     "ส่วนภาพจริง นอนอยู่ในหีบ"
    id 2  g 2485..2530  B  the attic room: vincenzo (normal clothes) crouched beside the bed, peeking; the trunk comes fully out
                           (0.75 -> 1, g 2485..2494) and the lid swings open (0 -> 100 deg, g 2494..2514); a sly smirk, a glance
                           at the window, back to the trunk.                              "ไม้ใต้เตียง ห้องเช่าของเขา"
    id 3  g 2531..2578  C  looking down into the open trunk: the panel on its red cloth, her smile in the candlelight; push in.
                                                                                          "สองปีเต็ม"
Runtime set fixes (set module untouched):
  * the trunk panel sits under the trunk's inner top face (invisible even with the lid open, louvre_API "visible only from above"):
    it is raised 0.13 D (keyed per frame) once the lid is past 35 deg, so it shows inside the open trunk.
  * the camera-only sun-shaft sheet hazes the trunk area grey: hidden (as s01 did in the corridor).
  * the panel is turned 180 deg about its centre so she reads upright from the open (+x) side.
  * a small warm candle-coloured fill (no shadow) over the trunk so her face reads in C (motivated by the floor candle beside it).
Mouths: nobody speaks.  NO depth of field (client rule).

    python3 shot.py stills 1,2 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 1,2,3 a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
sys.path.insert(0, os.path.join(os.path.dirname(HERE), "s21"))
import common as C                                       # noqa: E402
import t5lib as T5                                       # noqa: E402
import bpy                                               # noqa: E402
from mathutils import Vector                             # noqa: E402

L, actors, camrig, cast7 = C.L, C.actors, C.camrig, C.cast7
lerp, clamp, blink, pulse, ez, bf = C.lerp, C.clamp, C.blink, C.pulse, C.ez, C.bf
TMP = os.path.join(HERE, "work")

G0, G1, H = C.g_bound(81.48), C.g_bound(85.77), 6            # 2444, 2573
SETUPS = {1: (G0 - H, 2484), 2: (2485, 2530), 3: (2531, G1 + H - 1)}
RANGES = SETUPS
G_PULL = (2450, 2482)
G_PULL2 = (2485, 2494)
G_LID = (2494, 2514)
PANEL_UP = 0.13

CAMS = {
    1: (((1.55, 0.62, 0.95), (-2.0, 2.9, 0.45), 22.0), ((1.10, 0.95, 0.92), (-2.0, 2.9, 0.47), 22.0)),
    2: (((2.70, 0.45, 2.65), (-0.80, 3.55, 1.05), 20.0), ((2.45, 0.75, 2.55), (-0.85, 3.50, 1.00), 20.0)),
    3: (((0.75, 2.62, 2.55), (-0.92, 2.62, 0.30), 24.0), ((0.25, 2.62, 2.05), (-0.95, 2.62, 0.35), 24.0)),
}
VIN = (0.45, 3.65)


def cam_of(sid, g):
    a, b = SETUPS[sid]
    u = ez((g - a) / float(max(1, b - a)), "lin" if sid == 3 else "sine")
    (l0, k0, n0), (l1, k1, n1) = CAMS[sid]
    return Vector(lerp(l0, l1, u)), Vector(lerp(k0, k1, u)), lerp(n0, n1, u)


def trunk_at(g):
    if g < G_PULL2[0]:
        pull = 0.75 * ez((g - G_PULL[0]) / float(G_PULL[1] - G_PULL[0]))
    else:
        pull = lerp(0.75, 1.0, ez((g - G_PULL2[0]) / float(G_PULL2[1] - G_PULL2[0])))
    lid = 100.0 * ez((g - G_LID[0]) / float(G_LID[1] - G_LID[0]), "sine")
    return pull, lid


def vin_pose(g):
    p = dict(cast7.STORY7["vincenzo_peek_bed"][1])
    p["mirror"] = True                                       # faces screen-left: the trunk
    s = math.sin(g * 0.19)
    if 2512 <= g < 2522:                                     # a glance at the window (anyone watching?), then back
        p["gaze"] = (-0.9, -0.3)
        p["yaw"] = 0.30
    else:
        p["gaze"] = (0.9, 0.75)
    p["expr"] = "smirk" if g < G_LID[0] + 6 else "smug"
    p["head_roll"] = -10 + 2.5 * s
    p["lean"] = 34 + 2.0 * math.sin(g * 0.13)
    p["blink"] = blink(g, [2510, 2523])
    ha = p["arm_r"]["hand"]
    p["arm_r"] = dict(p["arm_r"], hand=(ha[0] + 0.03 * s, ha[1]))
    p["t"] = g / 30.0
    return p


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, "room", "under_bed_insert", quality=quality, lens=22.0, name="cam_s25")
        for o in self.scene.objects:
            if o.name.startswith("sun_shafts"):
                o.hide_render = True
        ld = bpy.data.lights.new("s25_trunk_fill", "POINT")
        ld.energy = 14.0
        ld.color = L.LANTERN if hasattr(L, "LANTERN") and len(L.LANTERN) == 3 else (1.0, 0.72, 0.42)
        ld.shadow_soft_size = 0.3
        try:
            ld.use_shadow = False
        except Exception:
            pass
        self.fill = bpy.data.objects.new("s25_trunk_fill", ld)
        self.scene.collection.objects.link(self.fill)
        self.fill.location = (-0.35, 2.15, 1.55)
        self.panel = L.STATE["trunk"]["panel"]
        # turn the panel 180 deg about its own centre so her head is at the far (hinge) end: upright from the open side (C)
        from mathutils import Matrix
        c = sum((Vector(v) for v in self.panel.bound_box), Vector()) / 8.0
        self.panel.matrix_basis = self.panel.matrix_basis @ (Matrix.Translation(c) @ Matrix.Rotation(math.pi, 4, "Z") @ Matrix.Translation(-c))
        self.panel_z0 = float(self.panel.location.z)
        self.actors["vin"] = C.make_actor("vin", "vincenzo", os.path.join(TMP, "sprites"))

    def pose(self, sid, gs):
        vin = self.actors["vin"]
        for g in gs:
            f = bf(sid, g)
            loc, look, lens = cam_of(sid, g)
            self.key_cam(f, loc, look, lens=lens)
            pull, lid = trunk_at(g)
            self.key_set(f, trunk=(pull, lid, True))
            self.panel.location.z = self.panel_z0 + (PANEL_UP if lid > 35.0 else 0.0)
            self.panel.keyframe_insert("location", frame=f)
            self.fill.data.energy = (14.0 if sid == 3 else 6.0) * (0.92 + 0.08 * math.sin(g * 1.3))
            self.fill.data.keyframe_insert("energy", frame=f)
            C.place(vin, f, VIN, 0.0)
        if sid == 2:
            fr = []
            for g in gs:
                f = bf(sid, g)
                self.scene.frame_set(f)
                vin.pose(f, vin_pose(g), camera=self.cam)
                fr.append(f)
            self.sprites_for([(vin, 288)], fr)

    def _vis(self, sid):
        self.actors["vin"].set_hidden(sid != 2)

    def report(self, sid, g):
        f = bf(sid, g)
        self._vis(sid)
        self.scene.frame_set(f)
        loc, look, lens = cam_of(sid, g)
        pull, lid = trunk_at(g)
        return dict(shot=sid, g=g, cam=[round(c, 3) for c in loc], lens=round(lens, 1), trunk=[round(pull, 3), round(lid, 1)],
                    heads=C.head_report(self, f))

    def render(self, sid, gs, out_dir, scale=1.0, samples=12, threads=2):
        self._vis(sid)
        return C.Take.render(self, [bf(sid, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    sids = [int(s) for s in sys.argv[2].split(",")]
    if cmd == "stills":
        Tk = Take("preview")
        for sid in sids:
            gs = [g for g in C.parse(sys.argv[3]) if RANGES[sid][0] <= g <= RANGES[sid][1]]
            if not gs:
                continue
            Tk.pose(sid, gs)
            for g in gs:
                print(json.dumps(Tk.report(sid, g)), flush=True)
                out = sys.argv[4]
                scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
                samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
                st = Tk.render(sid, [g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (sid, g)))
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q: Take(q), sids, sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
