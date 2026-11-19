#!/usr/bin/env python3
"""shot.py -- film 16 take s08 = shot 8 (CHAMBER chamber_wide_high / DAY): "เขาไปขอเงินสภา" -- Morse at the front table beside his
instrument presents to the tiers of congressmen; the mocker stands at his front-row desk, smug.  Sun shafts.
Shot 8 = g 475..541 (15.84-18.07 s); in-handle 9 f (dissolve in 13-17 f), out-handle 9 f (hard cut to shot 9).

    python3 shot.py camreport | probe a:b[:s] | stills a:b[:s] out_dir [scale] [spp] | final a:b[:s] [scale] [spp]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c16 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

TG, K, actors, cast16 = C.TG, C.K, C.actors, C.cast16
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

# ------------------------------------------------------------------ timing
G0, G1 = C.g_bound(15.84), C.g_bound(18.07)              # 475, 542 (exclusive)
H_IN, H_OUT = 9, 9
GS = list(range(G0 - H_IN, G1 + H_OUT))                  # 466..550
G_LAST = GS[-1]
G_SNAP = (487, 501)                                      # 14 f snap on "เงินสภา" (money for the council)
LIGHT, PRESET = "DAY", "chamber_wide_high"
MORSE_MARK = (-5.6, 8.6, 0.0)                             # beside the left end of the front table, level with the instrument

# ------------------------------------------------------------------ camera: crane down from high + push, snap
CAM = C.CamPath(Vector((3.0, -2.0, 7.0)), Vector((-4.3, 10.5, 2.8)), GS[0], G_LAST, push=0.08, slide_px=-25.0, rise_px=-20.0,
                arc_deg_s=10.0, decay=0.3, snaps=[dict(g=G_SNAP, k=1.5, peak=1.7, shift=(0.2, 0.1))])

# ------------------------------------------------------------------ cast
SMUG_ARMS = dict(arm_r={"hand": (-0.46, 0.88), "bend": 0.9, "layer": "top"}, arm_l={"hand": (0.46, 0.94), "bend": 0.9, "layer": "top"})
AUD_POSES = [dict(expr="unimpressed", mouth="frown", **SMUG_ARMS), dict(expr="smirk", arm_r="akimbo", arm_l="hip"),
             dict(expr="worried", arm_r="hip", arm_l="down"), dict(expr="neutral", **SMUG_ARMS),
             dict(expr="smug", arm_r="akimbo", arm_l="akimbo")]
CASTS = ["congressman_a", "congressman_b", "congressman_c"]


def seat_world(d):
    ti, a, px, py, zt = d
    return tuple(K.W((px + 0.95 * math.cos(a), py + 0.95 * math.sin(a), zt)))


def visible(pt, cam, margin=40, hmin=-60, hmax=1280 + 60):
    """screen px of a world point for a (loc, look) camera pair, or None behind the lens."""
    loc, look = cam
    f, r, u = C._cam_basis(loc, look)
    d = Vector(pt) - loc
    z = d.dot(f)
    if z <= 0.5:
        return None
    return (C.W_PX / 2 + C.F_PX * d.dot(r) / z, C.H_PX / 2 - C.F_PX * d.dot(u) / z, z)


def pick_audience(cams, n, tiers=(0, 1, 2), skip=()):
    """seats of congressmen visible (head height) in every camera of `cams`, spread evenly; returns [(mark xyz, tier)]"""
    out = []
    for d in TG.STATE["desks"]:
        if d[0] not in tiers:
            continue
        p = seat_world(d)
        head = Vector(p) + Vector((0, 0, 2.7))
        ok = True
        for cm in cams:
            s = visible(head, cm)
            if s is None or not (30 < s[0] < 690 and 330 < s[1] < 800):
                ok = False
        if ok and not any((Vector(p) - Vector(q)).length < 1.5 for q in skip):
            out.append((p, d[0]))
    out.sort(key=lambda t: (round(t[0][0] / 3.0), t[0][1]))
    step = max(1, len(out) // max(1, n))
    return out[::step][:n]


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s08")
        for g in (GS[0], G_SNAP[0] + 8, G_LAST):
            pass
        self.key_cam(bf(GS[0]), *CAM.at(GS[0]))
        self.scene.frame_set(bf(GS[0]))
        sd = os.path.join(WORK, "sprites")
        A = self.A
        self.mor = self.add("mor", "morse16", MORSE_MARK, sd)
        self.mock = self.add("mock", "mocker", A["marks"]["mocker_desk"], sd)
        self.aud = []
        cams = [CAM.at(g) for g in (GS[0], 520, G_LAST)]
        for i, (p, ti) in enumerate(pick_audience(cams, 13, skip=[A["marks"]["mocker_desk"], MORSE_MARK])):
            c = CASTS[i % 3]
            a = self.add("c%d" % i, c, p, sd)
            a.sideflip = p[0] > 0.0
            a.pdef = AUD_POSES[i % len(AUD_POSES)]
            self.aud.append(a)
        self.hand_err = {}

    def add(self, name, cast, mark, sd):
        a = C.make_actor(name, cast, sd, cam=self.cam)
        a.mark = tuple(mark)
        self.actors[name] = a
        a.sideflip = False
        return a

    # ---- poses
    def morse_pose(self, g):
        p = dict(cast16.STORY16["morse_present_table"][1])
        p["arm_r"] = dict(p["arm_r"], hand=(1.0 + 0.04 * math.sin(g * 0.2), 0.5 + 0.07 * math.sin(g * 0.13)))
        p["lean"] = 1.5 * math.sin(g * 0.17)
        p["head_roll"] = p["head_roll"] + 1.5 * math.sin(g * 0.11)
        p["blink"] = blink(g, [g0 for g0 in (488, 531)])
        p["t"] = g / 30.0
        return p

    def mock_pose(self, g):
        p = dict(cast16.STORY16["mocker_idle"][1])
        p.update(expr="smug", mouth="smirk", yaw=0.3, arm_r={"hand": (-0.46, 0.88), "bend": 0.9, "layer": "top"},
                 arm_l={"hand": (0.46, 0.94), "bend": 0.9, "layer": "top"}, head_roll=4 + 2 * math.sin(g * 0.1), legs="wide")
        p["blink"] = blink(g, [479, 521])
        p["lean"] = 1.2 * math.sin(g * 0.15)
        return p

    def aud_pose(self, a, i, g):
        p = dict(a.pdef)
        p.update(yaw=0.25, legs="stand")
        p["mirror"] = a.sideflip
        p["head_roll"] = 3 * math.sin(g * 0.09 + i)
        p["lean"] = 1.5 * math.sin(g * 0.13 + i * 1.7)
        p["blink"] = blink(g, [470 + (i * 17) % 80])
        return p

    def pose(self, gs):
        for g in gs:
            f = bf(g)
            self.key_cam(f, *CAM.at(g))
            for a in self.actors.values():
                C.place(a, f, a.mark)
            self.key_set(f, flames=1.0, shafts=True)
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.mor.pose(f, self.morse_pose(g), camera=self.cam)
            self.mock.pose(f, self.mock_pose(g), camera=self.cam)
            for i, a in enumerate(self.aud):
                a.pose(f, self.aud_pose(a, i, g), camera=self.cam)
        # px per D: 1.6x the biggest head of the take, rounded to 32
        self.sprites_for([(a, self.ppd(a)) for a in self.actors.values()], [bf(g) for g in gs])

    def ppd(self, a):
        d = max((Vector(a.mark) - Vector(CAM.at(g)[0])).length for g in (GS[0], G_LAST))
        dmin = min((Vector(a.mark) - Vector(CAM.at(g)[0])).length for g in (GS[0], G_LAST))
        head = C.F_PX / max(2.0, dmin)
        return int(min(512, max(96, 32 * round(1.6 * head / 32.0))))

    def report(self, g):
        return dict(g=g, cam=[round(c, 2) for c in CAM.at(g)[0]], heads=C.head_report(self, bf(g)))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        rows, worst = CAM.report(GS[:-1])
        print(rows[0], rows[len(rows) // 2], rows[-1])
        print("longest run under 0.25 px/frame: %d frames (bible max 6); min px %.2f" % (worst, min(r["px"] for r in rows)))
        sys.exit(0)
    gs = [g for g in C.parse(sys.argv[2]) if GS[0] <= g <= G_LAST]
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
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else TG.FINAL_SAMPLES["chamber"]
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take("final" if scale >= 1.0 else "preview"), gs, out, scale=scale, samples=samples)
