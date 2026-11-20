"""shot.py -- film 19 take s25 = shot 25 (HALL hall_low EVENING): "ตามที่นักดาราศาสตร์ท้าไว้เป๊ะ".
astro19 (the mocker) stands at the telescope with his JAW DROPPED (held wide-open mouth, ring eyes, sweat drop), wig askew, trembling
(no talking: the jaw drop is a held open mouth).  hall_low camera: low angle, snap push-in on "เป๊ะ" (caption 68.89 s; the word is
spoken ~69.35 s -> g ~2081).  g 2028..2086 = the shot (67.61-69.55 s), 9 f in-handle and 9 f out-handle (hard cuts both sides).
Hooks keyed every frame: set_candles flicker, set_regulator(True).  No DOF, no text, no caption_shade.
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

G0, G1 = C.g_bound(67.61), C.g_bound(69.55)            # 2028, 2086 (exclusive)
H_IN, H_OUT = 9, 9
G_FIRST, G_LAST = G0 - H_IN, G1 + H_OUT - 1
GS = list(range(G_FIRST, G_LAST + 1))
G_SNAP = C.g_of(69.35)                                  # "เป๊ะ" spoken ~69.35 s (caption phrase starts 68.89)
SNAP = (G_SNAP - 12, G_SNAP + 1)
PRESET, LIGHT, FINAL_SPP, PPD = "hall_low", "EVENING", 8, 256
BLINKS = [2050, 2074]

MARK = "mocker_telescope"                               # A['marks'] (D): (-3.24, 3.24, 0)
CAM_LOC0 = (-3.30, -1.60, 1.35)                          # near the preset hall_low start (-3.51, -2.22, 1.30): low angle
CAM_LOOK0 = (-3.20, 3.30, 2.55)
CAM = C.CamPath(CAM_LOC0, CAM_LOOK0, G_FIRST, G_LAST, push=0.10, slide_px=-110.0, rise_px=20.0, arc_deg_s=14.0, decay=0.15,
                snaps=[dict(g=SNAP, k=1.70, peak=2.3, shift=(1.40, 0.10))])

AB = dict(cast19.STORY19["astro_jaw_drop"][1])


def pose_of(g):
    p = dict(AB)
    t = (g - G_FIRST) / 30.0
    u = u_of(g, G0 - 12, G0 - 3, kind="sine")                # the jaw drops in the first frames, then is HELD open
    p["mouth"] = ("open", 0.10 + 0.16 * u, 0.04 + 0.16 * u)
    p["expr"] = "shocked"
    p["yaw"] = 0.05 + 0.04 * math.sin(t * 9.0)
    p["pitch"] = 0.10
    p["head_roll"] = 7.0 + 5.0 * math.sin(t * 17.0)         # wig askew + tremble
    p["lean"] = -3.0 + 1.5 * math.sin(t * 13.0)
    sq = 0.02 * math.sin(2 * math.pi * 3.0 * t)            # a shaky breath, never frozen
    p["squash"] = (0.98 + sq, 1.03 - sq)
    p["blink"] = blink(g, BLINKS)
    p["t"] = g / 30.0
    p["fx"] = ["sweat"]
    return p


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s24")
        assert self.final_samples() == FINAL_SPP, "set final samples changed: %s" % self.final_samples()
        self.key_cam(bf(G_FIRST), *CAM.at(G_FIRST))
        self.scene.frame_set(bf(G_FIRST))
        self.astro = self.actors["astro"] = C.make_actor("astro", "astro19", os.path.join(WORK, "sprites"), contact=dict(width=1.9, depth=0.8, opacity=1.0), cam=self.cam)

    def pose(self, gs):
        mark = Vector(self.A["marks"][MARK])
        for g in gs:
            f = bf(g)
            self.key_cam(f, *CAM.at(g))
            C.place(self.astro, f, mark + Vector((0, 0, 0.012 * math.sin(2 * math.pi * g / 20.0))))
            self.key_set(f, candles=1.0, regulator=True)
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.astro.pose(f, pose_of(g), camera=self.cam)
        self.sprites_for([(self.astro, PPD)], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = CAM.at(g)
        return dict(g=g, cam=[round(c, 3) for c in loc], heads=C.head_report(self, f), dof=self.cam.data.dof.use_dof,
                    caption_shade=bool(C.bpy.data.objects.get("caption_shade")))

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
