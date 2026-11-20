#!/usr/bin/env python3
"""shot.py -- film 20 take s21 = shot 21, THE ANTENNA REVEAL (g 1431..1560 + handles g 1427..1430 in, 1561..1564 out; cuts both sides).
"หอยิ่งสูง สัญญาณยิ่งไปไกล" -- the higher the tower, the farther the signal goes.  TOWER tower_night_wide / NIGHT 1909.

    g1427..1433  start on the summit (tower_night_summit, 250 m up), already creeping (tilt/push), rings burst from the lamp
                 (the cut lands on g1431: <= 4 frames of the summit before the whip, per the director note)
    g1433..1445  WHIP PULL-OUT (12 f, ease peak 2.1): camera flies from the summit to the night wide (x0.2 framing), lens shift
                 0 -> 0.345 with it; the whole tower, Paris and the rings come into view
    g1445..1564  drift 6 %/s push + 30 px/s slide + 2 deg/s arc (c20.CamPath, moving on the last frame), snap x1.22 (g1528..1543)
                 on "เสาอากาศยักษ์" (50.90 -> g1530); wire_glow 0 -> 1 on that word (whole lattice + wires glow)
    rings        S.signal_rings looping (period 38 f), the small summit circle hidden once its first arc has left
Mouths: none.  No actors in this shot.  NO DOF, NO text.

    python3 shot.py camreport | probe a:b[:s] | stills a:b[:s] out [scale] [spp] | final a:b[:s] [scale] [spp] | python3 deliver.py
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c20 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

S, CO = C.S, C.CO
lerp, clamp, ez, u_of, bf = C.lerp, C.clamp, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

G0, G1 = C.g_bound(47.71), C.g_bound(52.02)    # 1431, 1560 -> shot = 1431..1559
H_IN, H_OUT = 4, 4
G_FIRST, G_LAST = G0 - H_IN, G1 + H_OUT - 1    # 1427 .. 1563
GS = list(range(G_FIRST, G_LAST + 1))
G_ANT = C.g_of(50.90)                          # 1530 "เสาอากาศยักษ์": snap + whole-lattice glow
WHIP = (G0 - 3, G0 + 9)                       # 1428..1440 (the whip is under way when the cut lands on 1431)
SNAP = (G_ANT - 2, G_ANT + 13)
GLOW = (G_ANT, G_ANT + 9)
RING_PERIOD, RING_SPAN, RING_OFF = 36.0, 1.17, 9.0            # frames per burst; signal_rings t runs 0..1.17 (6 rings x 0.11 stagger + 0.62)
PRESET = "tower_night_wide"


def cams(A):
    a, b = dict(A["cams"]["tower_night_summit"]), A["cams"][PRESET]
    a["loc"] = CO.W((-5.0, -40.0, 268.0))          # closer than the preset summit camera (6 m x 250 m up, 80 m away): the lamp + rings fill the frame
    a["look_at"] = CO.W((0.0, 0.0, 289.0))
    return a, b


def drift_path(A):
    """CamPath from the wide pose, starting at the end of the whip (WHIP[1])."""
    a, b = cams(A)
    bl, bk = Vector(b["loc"]), Vector(b["look_at"])
    subj = Vector((0.0, 0.0, bl.z))                         # push/pull along the ground (a pull toward a high subject would sink the lens underground)
    tilt0 = 0.0
    return C.CamPath(bl, subj, WHIP[1], G_LAST, push=-0.05, slide_px=30.0, arc_deg_s=2.0, tilt0=tilt0, tilt_deg_s=0.0,
                     decay=0.25, snaps=[dict(g=SNAP, k=1.22, peak=1.7)])


def cam_at(A, g, P):
    """(loc, look, shift_y) of the camera at film frame g."""
    a, b = cams(A)
    la, lb = Vector(a["loc"]), Vector(b["loc"])
    ka, kb = Vector(a["look_at"]), Vector(b["look_at"])
    sa, sb = a.get("shift", 0.0), b.get("shift", 0.0)
    if g >= WHIP[1]:
        loc, look = P.at(g)
        return loc, look, sb
    # hold + whip: creep on the summit (slow push + tilt) so it is never parked, then the whip
    t = (g - G_FIRST) / 30.0
    u = C.snap_u(g, WHIP[0], WHIP[1], 2.1)
    creep = Vector((0.0, 0.5, 0.0)) * t * 4.0 + Vector((0.0, 0.0, 1.0)) * t * 3.0     # a few metres of crawl up/in
    loc = (la + creep).lerp(lb, u)
    look = (ka + creep * 0.5).lerp(kb, u)
    return loc, look, lerp(sa, sb, u)


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light="NIGHT", quality=quality, name="cam_s21")
        self.P = drift_path(self.A)
        self.scene.frame_set(bf(G_FIRST))

    def rings(self, g, f):
        """6 set ring objects driven here (S.signal_rings only emits during half of its cycle, which leaves the sky empty for ~15 f
        and reads as soft to qa_auto): ring i has age ((g+off)/P + i/6) % 1, radius 30 -> 560 m, strength 5 (1-age)^1.2, hidden
        while age < 0.1 (the small summit halo) -> a ring is born every 6 f and 5 arcs are always visible."""
        for i, ob in enumerate(CO.STATE["rings"]):
            age = (((g - G_FIRST + RING_OFF) / RING_PERIOD) + i / 6.0) % 1.0
            r = 30.0 + 530.0 * age ** 0.85
            ob.scale = (r, r, r)
            CO.key(ob, "scale", f, "LINEAR")
            CO.keysock(ob.active_material.node_tree.nodes["em"].inputs["Strength"], 5.0 * (1.0 - age) ** 1.2, f)
            CO.setv(ob, age >= 0.1, f)

    def pose(self, gs):
        for g in gs:
            f = bf(g)
            loc, look, sh = cam_at(self.A, g, self.P)
            self.key_cam(f, loc, look)
            self.cam.data.shift_y = sh
            self.cam.data.keyframe_insert("shift_y", frame=f)
            for fc in (self.cam.data.animation_data.action.fcurves if hasattr(self.cam.data.animation_data.action, "fcurves") else []):
                for kp in fc.keyframe_points:
                    kp.interpolation = "LINEAR"
            self.rings(g, f)
            S.wire_glow(u_of(g, *GLOW), frame=f)
            self.key_set(f, set_year=1909)

    def report(self, g):
        loc, look, sh = cam_at(self.A, g, self.P)
        f = bf(g)
        self.scene.frame_set(f)
        pr = {k: CO.project(CO.W(p)) for k, p in (("summit", (0, 0, 300.0)), ("platform2", (0, 0, 115.0)), ("base", (0, 0, 0)))}
        return dict(g=g, cam=[round(c, 2) for c in loc], shift=round(sh, 3), tower_px=pr, heads={})

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        # whip + drift speeds from the preset cams in metres (no build)
        import tower20
        A = dict(cams={k: dict(loc=CO.W(v["loc"]), look_at=CO.W(v["look"]), shift=v.get("shift", 0.0)) for k, v in tower20.CAMS_M.items()})
        P = drift_path(A)
        prev = None
        for g in GS[:-1]:
            a, b = cam_at(A, g, P), cam_at(A, g + 1, P)
            sp = max(C._corner_shift(a[:2], b[:2], 236 * CO.SC, cx, cy) for cx in (0, 720) for cy in (0, 1280)) if g >= WHIP[1] else -1
            print(g, [round(x, 1) for x in a[0]], "px/f", round(sp, 2))
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
                print("g %d  %.1f s wall %.1f cpu" % (g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else CO.FINAL_SPP
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take("final" if scale >= 1.0 else "preview"), gs, out, scale=scale, samples=samples)
