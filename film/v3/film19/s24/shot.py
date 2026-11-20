#!/usr/bin/env python3
"""shot.py -- film 19 take s24 (MERGED, client rule §I: the camera travels instead of cutting): shots 24 + 25 + 26 in ONE continuous HALL EVENING take.
    g 1924..1932  9 f in-handle (hard cut in from s23 at g 1933)
    g 1933..2021  the approved s24 action: the King at the table compares the watch with his gold pocket watch (squint) while the candle stubs
                  pile up 0 -> 10; slide + push, snap on "สิบสัปดาห์" (66.77 s -> g 2006)           [camera: shot_a.CAM]
    g 2022..2029  WHIP-PAN across the room (7 f, motion blur) from the table to astro19 at the telescope (hall_low angle)
    g 2030..2085  astro19 jaw dropped, wig askew ("ตามที่นักดาราศาสตร์ท้าไว้เป๊ะ"); fast push-in on "เป๊ะ" (g 2081) = the ~1 s punctuation
                  close-up, face capped at ~33 %                                                        [camera: shot_b.CAM]
    g 2086..2093  WHIP back to the table (7 f, motion blur)
    g 2094..2159  the money bag falls and lands in front of old Harrison at "ต้องควักเงิน" (g 2107), the King nods, Harrison looks at the bag then
                  grins at the lens; ends centred on Harrison + bag with both men in frame, moving on the last frame (hard end, N = 2160)
                                                                                                        [camera: shot_c.CAM]
Characters: king19 (table), harrison19 old (behind the table edge), astro19 (telescope mark); cards are shown only where they are on screen.
The three camera paths and the poses are those of the approved takes (shot_a.py = old s24, ../s25/shot.py, ../s26/shot.py); this file only
joins them (whip = eased lerp of loc / look between the end of one path and the start of the next, motion blur keyed on those frames).
    python3 shot.py camreport | probe a:b[:step] | stills a:b[:step] out [scale] [spp] | final a:b[:step] [scale] [spp]
"""
import math, os, sys, json, importlib.util
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c19 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

H, K, cast19 = C.H, C.K, C.cast19
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")


def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


A = _load("shot_a", os.path.join(HERE, "shot_a.py"))
B = _load("shot_b", os.path.join(HERE, "..", "s25", "shot.py"))
Cm = _load("shot_c", os.path.join(HERE, "..", "s26", "shot.py"))

G0, G1 = A.G0, C.N_FILM                                 # 1933 .. 2159 (film end at g 2160)
H_IN = 9
G_FIRST, G_LAST = G0 - H_IN, G1 - 1
GS = list(range(G_FIRST, G_LAST + 1))
W1 = (2022, 2029)                                        # whip 1: table -> telescope (7 f)
W2 = (2086, 2093)                                        # whip 2: telescope -> table (7 f)
WHIP_SHUTTER = 0.9
PRESET, LIGHT, FINAL_SPP, PPD = "hall_table", "EVENING", 8, 256
G_SNAP = A.G_SNAP                                        # 2006 (stubs reach 10 here)
HAR_ON = (W2[0] - 3, G_LAST)


_c = Cm.CAM
CAM_C = C.CamPath(_c.loc0, _c.look0 + Vector((0.0, 0.0, -0.08)), _c.g0, _c.g1, push=_c.push, slide_px=_c.slide_px, rise_px=_c.rise_px,
                  arc_deg_s=_c.arc, decay=_c.decay, snaps=[dict(x) for x in _c.snaps])      # round 8: tilted down 0.08 D (tabletop fills the lower third)
KING_C = (Cm.KING_M[0], 4.90, 0.0)                       # round 8: 0.3 D closer to the camera
ASTRO_ON = (W1[0] - 3, W2[0] + 2)                        # round 8 (minimum fix): his card is hidden from g 2089, inside the heaviest blur


def _blend(a, b, u):
    u = u * u * (3.0 - 2.0 * u)
    return a[0].lerp(b[0], u), a[1].lerp(b[1], u)


def cam_at(g):
    if g < W1[0]:
        return A.CAM.at(g)
    if g <= W1[1]:
        return _blend(A.CAM.at(W1[0]), B.CAM.at(W1[1]), (g - W1[0]) / float(W1[1] - W1[0]))
    if g < W2[0]:
        return B.CAM.at(g)
    if g <= W2[1]:
        return _blend(B.CAM.at(W2[0]), CAM_C.at(W2[1]), (g - W2[0]) / float(W2[1] - W2[0]))
    return CAM_C.at(g)


def whip(g):
    return W1[0] < g <= W1[1] or W2[0] < g <= W2[1]


class _Path(object):
    def at(self, g):
        return cam_at(g)

    def report(self, gs):
        return C.CamPath.report(self, gs) if False else ([], 0)


CAM = A.C.CamPath(A.CAM_LOC0, A.CAM_LOOK0, G_FIRST, G_LAST)        # only for camreport (corner speeds); the real path is cam_at
CAM.at = cam_at


def stubs_at(g):
    return 10 if g >= G_SNAP else A.stubs_at(g)


def pose_king(g):
    if g < W2[0]:
        return A.pose_of(g)
    p = Cm.pose_king(g)
    p["pitch"] = 0.05 + (p["pitch"] - 0.05) * 1.5                      # round 8: bigger nods
    return p


def pose_har(g):
    p = Cm.pose_har(g)
    if g >= Cm.G_BAG + 2:                                              # round 8: a big open grin
        p["expr"] = "laughing"
        p.pop("mouth", None)
    u = u_of(g, Cm.G_BAG + 14, Cm.G_BAG + 24, kind="sine")
    p["arm_l"] = dict(hand=(lerp(-0.45, -0.50, u), lerp(0.50, 0.15, u)), bend=0.2, shape="open", layer="front")      # the raised watch stays inside the frame
    p["arm_r"] = dict(hand=(lerp(0.55, 0.62, u), lerp(0.80, 0.05, u)), bend=0.2, shape="open", layer="front")          # round 9: arms go UP on the landing
    p["prop_l"] = dict(type="h4_watch", scale=1.25)
    return p


def hop(g):
    d = g - Cm.G_BAG
    return 0.16 * math.sin(math.pi * d / 10.0) if 0 <= d <= 10 else 0.0


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s24m")
        assert self.final_samples() == FINAL_SPP, "set final samples changed: %s" % self.final_samples()
        self.key_cam(bf(G_FIRST), *cam_at(G_FIRST))
        self.scene.frame_set(bf(G_FIRST))
        sd = os.path.join(WORK, "sprites")
        self.king = self.actors["king"] = C.make_actor("king", "king19", sd, contact=True, cam=self.cam)
        self.har = self.actors["har"] = C.make_actor("har", "harrison19", sd, contact=dict(width=1.1, depth=0.5, opacity=0.8), cam=self.cam)
        self.astro = self.actors["astro"] = C.make_actor("astro", "astro19", sd, contact=dict(width=1.9, depth=0.8, opacity=1.0), cam=self.cam)
        self.bag = K.STATE["hooks"]["bag_full"]
        self.bag0 = Vector((Cm.BAG_XY_M[0], Cm.BAG_XY_M[1], self.bag.location.z))
        self._make_coins()
        self._make_modesty_panel()
        for pv in K.STATE["hooks"]["stubs"]:                  # stub row in front of the King (as the approved s24)
            pv.location.y += A.STUB_DY / 1.85

    _make_coins = Cm.Take._make_coins
    _make_modesty_panel = Cm.Take._make_modesty_panel

    def pose(self, gs):
        kA = Vector(K.W(A.KING_M))
        kC = Vector(KING_C)
        hm = Vector((Cm.HAR_M[0], Cm.HAR_M[1], 0.0))
        am = Vector(self.A["marks"][B.MARK])
        for g in gs:
            f = bf(g)
            self.key_cam(f, *cam_at(g))
            u = u_of(g, W2[0], W2[1], kind="sine")             # the King moves from his table spot to his ending spot during whip 2 (off screen)
            kp = kA.lerp(kC, u)
            C.place(self.king, f, kp + Vector((0, 0, 0.012 * math.sin(2 * math.pi * g / 20.0))))
            C.place(self.har, f, hm + Vector((0, 0, hop(g) + 0.07 * abs(math.sin(2 * math.pi * g / 16.0)) * u_of(g, Cm.G_BAG + 14, Cm.G_BAG + 20))))
            C.place(self.astro, f, am + Vector((0, 0, 0.012 * math.sin(2 * math.pi * g / 20.0))))
            C.key_vis(self.har.objects(), HAR_ON[0] <= g <= HAR_ON[1], f)
            C.key_vis(self.astro.objects(), ASTRO_ON[0] <= g <= ASTRO_ON[1], f)
            C.key_vis(H.STATE.get("shafts", []), g < 2086, f)            # round 9: the pale window-shaft volume lay over the table front / carpet g 2094-2146: hidden from g 2086
            self.key_set(f, candles=1.0, regulator=True, kings_chair=True, stubs=stubs_at(g),
                         moneybag="full" if g >= Cm.G_DROP else "none", box="none")
            if g >= Cm.G_DROP:
                self.bag.location = self.bag0 + Vector((0, 0, Cm.bag_dz(g) / 1.85))
                self.bag.keyframe_insert("location", frame=f)
                sz = Cm.bag_squash(g)
                self.bag.scale = Vector((Cm.BAG_SCALE / sz ** 0.5, Cm.BAG_SCALE / sz ** 0.5, Cm.BAG_SCALE * sz))
                self.bag.keyframe_insert("scale", frame=f)
            for ob, (ang, dist, dly, tilt, _k) in zip(self.coins, self.coin_plan):
                t = (g - Cm.G_BAG - dly * 3.0) / 30.0
                if t < 0:
                    pos = self.coin_base + Vector((0, 0, 0.1))
                else:
                    uu = min(t / 0.45, 1.0)
                    r = dist * (1.0 - (1.0 - uu) ** 2)
                    hh = 0.1 + 0.9 * 4 * uu * (1 - uu) * 0.6 if uu < 1.0 else 0.02
                    pos = self.coin_base + Vector((math.cos(ang) * r, math.sin(ang) * r * 0.7, hh if uu < 1.0 else 0.02))
                ob.location = pos
                ob.rotation_euler = (math.radians(tilt * (1.0 - min(t / 0.45, 1.0)) if t > 0 else 0.0), 0, 0)
                ob.keyframe_insert("location", frame=f)
                ob.keyframe_insert("rotation_euler", frame=f)
                C.key_vis([ob], g >= Cm.G_BAG, f)
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.king.pose(f, pose_king(g), camera=self.cam)
            self.har.pose(f, pose_har(g), camera=self.cam)
            self.astro.pose(f, B.pose_of(g), camera=self.cam)
        self.sprites_for([(self.king, PPD), (self.har, PPD), (self.astro, PPD)], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        heads = C.head_report(self, f)
        vis = dict(king=not (W1[1] < g < W2[0]), har=HAR_ON[0] <= g <= HAR_ON[1], astro=ASTRO_ON[0] <= g <= ASTRO_ON[1])
        heads = {k: v for k, v in heads.items() if vis.get(k, True) and not whip(g) and -60 < v["x"] < 780}
        return dict(g=g, cam=[round(c, 3) for c in cam_at(g)[0]], heads=heads, whip=whip(g), stubs=stubs_at(g),
                    dof=self.cam.data.dof.use_dof, caption_shade=bool(C.bpy.data.objects.get("caption_shade")))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        out = []
        for g in gs:                                         # motion blur ONLY on the whip frames (camera keyed on every frame, so it smears)
            r = self.scene.render
            r.use_motion_blur = whip(g)
            if whip(g):
                r.motion_blur_shutter = WHIP_SHUTTER
            out += C.Take.render(self, [bf(g)], out_dir, scale=scale, samples=samples, threads=threads)
        return out


if __name__ == "__main__":
    cmd = sys.argv[1]
    gs = [g for g in C.parse(sys.argv[2]) if G_FIRST <= g <= G_LAST] if len(sys.argv) > 2 else GS
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
