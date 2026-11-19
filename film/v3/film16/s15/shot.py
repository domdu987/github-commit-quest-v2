#!/usr/bin/env python3
"""shot.py -- film 16 take s15 = shot 15 (g 958..1006, plan 31.93-33.57 s) + handles 9 each side (g 949..1015).
"แต่พอลอง ส่งข่าว เงียบกริบ" -- LINE line_trench_end / DUSK: Morse at the test key on the crate at the furrow's end presses it; the register stays
silent; Cornell and the workers lean in, waiting.  On "เงียบกริบ" (g 988) the picture dips to x0.75 brightness for 0.4 s (bible device).
DIS in, DIS out (shot 16 is a cut-away: handles are for a dissolve or cut).  Camera: slow push 6 %/s + slide, crate + coil in the foreground.
Mouths: nobody speaks.  NO depth of field, NO text.
    python3 shot.py probe a:b | stills a:b out [scale] [spp] | final a:b[:step] [scale] [spp]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c16 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

TG, K, LN, cast16 = C.TG, C.K, C.LN, C.cast16
lerp, clamp, blink, u_of, bf = C.lerp, C.clamp, C.blink, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

G0, G1 = C.g_bound(31.93), C.g_bound(33.57)            # 958, 1007: shot = g 958..1006
H_IN, H_OUT = 9, 9
GA, GB = G0 - H_IN, G1 + H_OUT - 1                      # 949 .. 1015
GS = list(range(GA, GB + 1))
G_TRY = C.cap_g("ส่งข่าว")                              # 975: the press
G_SIL = C.cap_g("เงียบกริบ")                            # 988: silence, brightness dip
DIP = (G_SIL - 2, G_SIL + 10)                           # 0.4 s
PRESS = (G_TRY, G_TRY + 6)
PRESS2 = (G_SIL - 6, G_SIL - 1)
CAM_NEAR = 0.72
CAM_UP = 1.2
PRESET, LIGHT = "line_trench_end", "DUSK"

def dip(g):
    """brightness factor: 1 -> 0.75 -> 1 over the dip window (smooth)"""
    a, b = DIP
    if g <= a or g >= b:
        return 1.0
    u = (g - a) / float(b - a)
    return 1.0 - 0.25 * math.sin(math.pi * u)

def key_press(g):
    v = 0.0
    for a, b in (PRESS, PRESS2):
        if a <= g <= b:
            v = max(v, math.sin(math.pi * (g - a) / float(b - a)))
    return v

STORY = cast16.STORY16
def story(name):
    return dict(STORY[name][1])

ACTORS = dict(morse=("morse16", "morse_key_wait", "morse_key"), cornell=("cornell", "cornell_wait", "worker_key_c"),
              worker_a=("worker16_a", "worker_a_lean_shovel", "worker_key_a"), worker_b=("worker16_b", "worker_b_lean_shovel", "worker_key_b"))
CANVAS = dict(worker_a=(-2.6875, -4.375, 2.6875, 0.375), worker_b=(-2.6875, -4.625, 2.6875, 0.1875), cornell=(-2.6875, -4.1875, 2.6875, 0.1875),
              morse=(-2.375, -4.375, 2.375, 0.1875))

class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s15")
        A = self.A
        loc0, look0 = Vector(A["cam"]["loc"]), Vector(A["cam"]["look_at"])
        mm, mc = Vector(A["marks"]["morse_key"]), Vector(A["marks"]["worker_key_c"])
        look0 = Vector((121.0, -8.4, 2.3))
        loc0 = look0 + (loc0 - look0) * CAM_NEAR
        loc0.z += CAM_UP
        self.cp = C.CamPath(loc0, look0, GA, GB, push=0.10, slide_px=25.0, arc_deg_s=20.0, decay=0.25, snaps=[dict(g=(G_TRY - 2, G_TRY + 11), k=1.8, peak=1.7, shift=(0.5, 0.1))])
        self.key_cam(bf(GA), *self.cp.at(GA))
        self.scene.frame_set(bf(GA))
        self.base_exp = self.scene.view_settings.exposure
        sd = os.path.join(WORK, "sprites")
        self.act = {}
        for nm, (cast, pose, mark) in ACTORS.items():
            self.actors[nm] = self.act[nm] = C.make_actor(nm, cast, sd, canvas=CANVAS.get(nm), contact=True, cam=self.cam)

    def pose(self, gs):
        for g in gs:
            self.key_cam(bf(g), *self.cp.at(g))
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.scene.view_settings.exposure = self.base_exp + math.log2(dip(g))
            self.scene.view_settings.keyframe_insert("exposure", frame=f)
            for nm, (cast, pose, mark) in ACTORS.items():
                p = story(pose)
                if nm == "morse":
                    p["key_press"] = key_press(g)
                    if key_press(g) > 0.02:
                        p["expr"] = "determined"
                p["lean"] = p.get("lean", 0.0) + 1.2 * math.sin(g * 0.17 + len(nm))
                p["head_roll"] = p.get("head_roll", 0.0) + 1.5 * math.sin(g * 0.11 + 2 * len(nm))
                p["blink"] = blink(g, [960 + 29 * (len(nm) % 4), 1000 + 3 * len(nm)])
                p["mirror"] = MIRROR.get(nm, False)
                p["t"] = g / 30.0
                mk = self.A["marks"][mark]
                hands = None
                if nm == "morse":
                    mk = MORSE_AT
                    p.pop("prop_r", None)                  # the set shows the key
                    hands = {"r": {"hand": (KEY[0], KEY[1], KEY[2] - 0.35 * key_press(g) + 0.15)}}
                C.place(self.act[nm], f, mk)
                _, info = self.act[nm].pose(f, p, hands=hands, camera=self.cam)
                if hands:
                    self.herr = info["r"].get("error", 0.0)
        self.sprites_for([(a, 256) for a in self.act.values()], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = self.cp.at(g)
        return dict(g=g, dip=round(dip(g), 3), press=round(key_press(g), 2), cam=[round(c, 2) for c in loc], heads=C.head_report(self, f))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)

MIRROR = dict()
KEY = (119.21, -8.15, 2.29)                  # the set key knob (world D), found by projecting the set's mesh vertices
MORSE_AT = (120.1, -9.4, 0.0)

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        Tk = Take("preview")
        rows, worst = Tk.cp.report(GS[:-1])
        print("longest run under 0.25 px/frame:", worst)
        sys.exit(0)
    gs = [g for g in C.parse(sys.argv[2]) if GA <= g <= GB]
    if cmd in ("probe", "stills"):
        Tk = Take("preview"); Tk.pose(gs)
        for g in gs:
            print(json.dumps(Tk.report(g)), flush=True)
            if cmd == "stills":
                out = sys.argv[3]; scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
                samples = int(sys.argv[5]) if len(sys.argv) > 5 else 6
                st = Tk.render([g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "g_%04d.png" % g)); print("g %d %.1f s" % (g, st["wall"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else TG.FINAL_SAMPLES["line"]
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take("final" if scale >= 1.0 else "preview"), gs, out, scale=scale, samples=samples)
