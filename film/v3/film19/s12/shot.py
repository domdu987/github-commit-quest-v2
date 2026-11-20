#!/usr/bin/env python3
"""shot.py -- film 19 take s12 = shot 12 (WORKSHOP shop_clock NIGHT, set_clock(3)): "เครื่องที่สาม สิบกว่าปี".
Harrison (harrison19 default: greying hair, apron) works on the H3 (compact brass box, two round balances) by candlelight, the bench candle
stub burning down (set_candles(level 1 -> 0.3) keyed on every frame).  Take = g 929..994: 9-frame dissolve in-handle g 929..937, shot g 938..985
(31.26-32.85 s), 9-frame out-handle g 986..994 (the next shot 13 is a CUT).
    g 938..   he taps with the chisel at the H3, head bent (a small nod each stroke); the H3 balances counter-rotate; flame flickers
    SNAP push on "สิบ" of "สิบกว่าปี" (caption 31.91 = g 960): he straightens, looks at the lens, tired
Camera: shop_clock start pose region, push + slide + arc; snap with a pan.  NO DOF, NO text, NO caption_shade.
Mouths: nobody speaks: fixed expression mouth.

    python3 shot.py probe a:b[:step]       numbers only        python3 shot.py camreport
    python3 shot.py stills a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final a:b[:step] [scale] [samples]     (resumable; two processes e.g. 853:946:2 / 854:946:2)
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c19 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

H, K, actors, cast19 = C.H, C.K, C.actors, C.cast19
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

G0, G1 = C.g_bound(31.26), C.g_bound(32.85)            # 938, 986: shot 12 = g 938..985
H_IN, H_OUT = 9, 9
G_FIRST, G_LAST = G0 - H_IN, G1 + H_OUT - 1            # 929 .. 994
GS = list(range(G_FIRST, G_LAST + 1))
G_WORD = C.cap_g("สิบกว่าปี")                          # 960: caption start; "สิบ" spoken right at it
SNAP = (G_WORD - 8, G_WORD + 12)                       # 955..969 (14 f)
G_LOOKUP = (G_WORD + 30, G_WORD + 40)                   # he straightens and looks at the lens
BLINKS = [950, 975, 990]

LIGHT, PRESET, CLOCK = "NIGHT", "shop_clock", 3
FINAL_SPP = 8
PPD = 256
CANVAS = None

MARK = "harrison_bench"
MARK_DX = float(os.environ.get("MARK_DX", -0.1))
MARK_DY = float(os.environ.get("MARK_DY", -2.8))
CAM_LOC0 = tuple(float(v) for v in os.environ.get("CAM_LOC0", "2.2,-1.6,2.4").split(","))
CAM_LOOK0 = tuple(float(v) for v in os.environ.get("CAM_LOOK0", "2.6,2.9,2.3").split(","))
CAM = C.CamPath(CAM_LOC0, CAM_LOOK0, G_FIRST, G_LAST, push=float(os.environ.get("PUSH", 0.07)), slide_px=float(os.environ.get("SLIDE", -70)),
                rise_px=float(os.environ.get("RISE", 0)), arc_deg_s=float(os.environ.get("ARC", 8)), decay=0.25,
                snaps=[dict(g=SNAP, k=float(os.environ.get("SNAPK", 1.3)), peak=float(os.environ.get("SNAPPEAK", 3.0)), shift=(float(os.environ.get("SNAPSX", 0.6)), -0.1))])

BASE = dict(cast19.STORY19["harrison_chisel"][1])


def pose_of(g):
    p = dict(BASE)
    p["mirror"] = True                                    # the H3 is at screen-left of him
    lk = u_of(g, *G_LOOKUP, kind="sine")
    ph = 2 * math.pi * g / 14.0                           # ~2 Hz tapping
    tap = (1.0 - lk) * 0.16 * max(0.0, math.sin(ph))
    p["arm_r"] = dict(hand=(0.78 + 0.5 * tap, 1.0 - tap), bend=0.2, layer="front", stretch=1.2)
    p["prop_r"] = dict(type="chisel19", angle=40 - 25 * tap * 6 * (1 - lk))
    p["lean"] = lerp(8 + 1.5 * math.sin(ph), 1.0, lk)
    p["pitch"] = lerp(0.30 + 0.05 * math.sin(ph), -0.05, lk)
    p["yaw"] = lerp(0.5, 0.2, lk)
    p["gaze"] = (lerp(0.7, 0.1, lk), lerp(0.9, 0.0, lk))
    p["expr"] = "determined" if lk < 0.5 else "worried"
    p["blink"] = blink(g, BLINKS)
    p["t"] = g / 30.0
    return p


def candle_level(g):
    """the bench candle stub burns down over the shot (1.0 -> 0.3)"""
    return lerp(1.0, 0.35, clamp((g - G0) / float(G1 - G0)))


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s12")
        self._base = {}
        assert self.final_samples() == FINAL_SPP, "set final samples changed: %s" % self.final_samples()
        # the bench candle stub moves from the far left of the bench to the bench top at his right shoulder, so it stays in frame while it burns down
        st = H.STATE["stub"]
        st["pv"].location = (1.7, 0.8, 0.56)
        st["base"] = (1.7, 0.8, 0.56)
        for o, _b in H.STATE["lampgroups"]["candle"]:
            if o.name == "p_bench":
                o.location = (1.7 * 1.85, 0.8 * 1.85, 1.6)
        self.key_cam(bf(G_FIRST), *CAM.at(G_FIRST))
        self.scene.frame_set(bf(G_FIRST))
        self.har = self.actors["har"] = C.make_actor("har", "harrison19", os.path.join(WORK, "sprites"), canvas=CANVAS, contact=True, cam=self.cam)

    def pose(self, gs):
        mark = Vector(self.A["marks"][MARK]) + Vector((MARK_DX, MARK_DY, 0))
        for g in gs:
            f = bf(g)
            self.key_cam(f, *CAM.at(g))
            C.place(self.har, f, mark)
            self.key_set(f, clock=CLOCK, balance=g / 30.0, candles=candle_level(g))
            self.dim(f, g)
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.har.pose(f, pose_of(g), camera=self.cam)
        self.sprites_for([(self.har, PPD)], [bf(g) for g in gs])

    def dim(self, f, g):
        """the room gets darker as the candle burns down: candle lights x1 -> 0.55, other lamps / fills / moon key x1 -> 0.7, the flame
        emission follows the stub; keyed on every frame.  (set_candles resets the candle lights and flame every call, so those are
        scaled after it; the other lights are scaled from their stored base.)"""
        u = clamp((g - G0) / float(G1 - G0))
        for grp, items in H.STATE["lampgroups"].items():
            for o, _b in items:
                if grp == "candle":
                    o.data.energy = o.data.energy * lerp(1.0, 0.3, u)
                else:
                    self._base.setdefault(o.name, o.data.energy)
                    o.data.energy = self._base[o.name] * lerp(1.0, 0.3, u)
                o.data.keyframe_insert("energy", frame=f)
        em = H.STATE["M"]["flame"].node_tree.nodes["Emission"].inputs["Strength"]
        em.default_value = em.default_value * lerp(1.0, 0.5, u)
        em.keyframe_insert("default_value", frame=f)
        sun = H.STATE.get("sun")
        if sun is not None:
            self._base.setdefault("sun", sun.data.energy)
            sun.data.energy = self._base["sun"] * lerp(1.0, 0.3, u)
            sun.data.keyframe_insert("energy", frame=f)

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = CAM.at(g)
        bars = C.clock_world(CLOCK, (0.0, 0.0, 0.64))
        return dict(g=g, cam=[round(c, 3) for c in loc], heads=C.head_report(self, f), h1_bars_px=H.project(tuple(bars)),
                    dof=self.cam.data.dof.use_dof, caption_shade=bool(C.bpy.data.objects.get("caption_shade")))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        rows, worst = CAM.report(GS[:-1])
        for r in rows:
            print(r)
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
                print("g %d  %.1f s wall %.1f cpu" % (g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else None
        quality = "final" if scale >= 1.0 else "preview"
        if samples is None:
            samples = FINAL_SPP
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take(quality), gs, out, scale=scale, samples=samples)
