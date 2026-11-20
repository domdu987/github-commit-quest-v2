#!/usr/bin/env python3
"""shot.py -- film 19 take s02 = the BIGZOOM (shots 2 + 3 merged, QA_TEAM section H).  g 57..190 (1.91-6.37 s, 134 frames) + 9 handle frames each side
(hard cut in from s01 at g 57; DISSOLVE 13 f out into s04 at g 191): g 48..199.

ONE continuous eased camera move, no cut.  SHIP ship_aerial / NOON (set_sea + set_roll keyed on every frame):
  START  extreme wide from high above and behind: the lone warship on the endless glittering sea, small in the frame; captain19 and astro19_c on the
         quarterdeck are ~6 px tall (under 5 % of the frame), findable
  MIDDLE the camera descends and pushes in toward the stern, passing the spanker sail (a fore-and-aft sail, 1.8 D from the lens) as a parallax foreground
  END    (by ~5.9 s, g 177) a MEDIUM shot on the quarterdeck: captain19 holds a blank sea chart, astro19_c squints through a quadrant at the sky and
         scratches his head (g ~150-165); 35-60 % of the frame height; the camera rides the deck (C.on_ship)
No mouth movement.  NO depth of field, NO text, NO caption_shade.

    python3 shot.py camreport | probe a:b[:step] | stills a:b[:step] out [scale] [spp] | final a:b[:step] [scale] [spp]
    python3 deliver.py [draft]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c19 as C                                          # noqa: E402
from mathutils import Vector, Matrix                     # noqa: E402

H, K, cast19 = C.H, C.K, C.cast19
lerp, clamp, blink, u_of, bf = C.lerp, C.clamp, C.blink, C.u_of, C.bf
WORK = os.path.join(HERE, "work")
TAKE = "s02"
PRESET, LIGHT = "ship_aerial", "NOON"
G0, G1 = 57, 191                                         # shot = g 57..190
H_IN, H_OUT = 9, 9
FIRST_G, G_LAST = G0 - H_IN, G1 + H_OUT - 1              # 48..199
GS = list(range(FIRST_G, G_LAST + 1))
FINAL_SPP = 10
S = 1.85
PPD = 224                                                # sprite px per D (head ~110 px at the end; the start is downsampled)
G_ARRIVE = 176                                           # the medium shot is reached (5.9 s)
G_SCRATCH = (155, 175)       # head scratch; 157-190 the whole puzzled beat                                   # astro19_c scratches his head (comic), 4.9-5.5 s
BLINKS_C, BLINKS_A = [70, 128, 171], [92, 150, 188]

# ----------------------------------------------------------------------------- staging (ship rest frame = world D at t = 0; z of the quarterdeck 14.34)
Z_QD = 14.34 + 0.22                                        # the deck plus the shoe sole (the card base sat 0.2 D low)
CAP_XY = (-0.75, -31.3)                                  # captain19, beside the wheel, camera-left
AST_XY = (1.7, -30.6)                                   # astro19_c, camera-right (short: 2.8 D)

# ----------------------------------------------------------------------------- camera: a spline through key poses in the SHIP's rest frame (D), eased in and out
KEYS = [  # (u, loc, look)
    (0.00, (30.0, -530.0, 395.0), (0.0, -14.0, 14.0)),            # truly extreme wide: ~640 D away, the ship <= 12 % of the frame height, the crew ~4 px
    (0.50, (13.0, -125.0, 96.0), (1.0, -30.0, 15.0)),             # descending
    (0.76, (6.2, -52.0, 46.0), (0.8, -30.5, 16.0)),               # high over the stern, level with the mizzen yards / sails
    (0.91, (3.1, -40.5, 31.0), (0.6, -30.3, 16.0)),               # passes the spanker sail at ~1.9 D and the rigging, then dives
    (1.00, (0.45, -36.3, 16.5), (0.5, -30.0, 15.9)),              # medium on the quarterdeck
]


def _cr(p0, p1, p2, p3, t):
    """Catmull-Rom, uniform"""
    return 0.5 * ((2 * p1) + (-p0 + p2) * t + (2 * p0 - 5 * p1 + 4 * p2 - p3) * t * t + (-p0 + 3 * p1 - 3 * p2 + p3) * t * t * t)


TM = [(48, 0.0), (66, 0.07), (90, 0.27), (112, 0.55), (125, 0.70), (140, 0.85), (153, 0.935), (164, 0.98), (176, 1.0)]    # g -> FRACTION OF THE PATH LENGTH (ease in, one speed hump, ease OUT over g 138-170)


def _slopes():
    """Fritsch-Carlson monotone cubic slopes at the knots (C1: no velocity dips at the knots; zero speed at the landing)"""
    n = len(TM)
    h = [TM[i + 1][0] - TM[i][0] for i in range(n - 1)]
    d = [(TM[i + 1][1] - TM[i][1]) / h[i] for i in range(n - 1)]
    m = [d[0]] + [0.0 if d[i - 1] * d[i] <= 0 else 2 * d[i - 1] * d[i] / (d[i - 1] + d[i]) for i in range(1, n - 1)] + [0.0]
    m[0] = 0.5 * d[0]                                                      # a gentle ease-in, never a dead start
    return m


_M = _slopes()


def _umap(g):
    if g <= TM[0][0]:
        return 0.0
    if g >= TM[-1][0]:
        return 1.0
    j = max(i for i in range(len(TM) - 1) if TM[i][0] <= g)
    (g0_, u0_), (g1_, u1_) = TM[j], TM[j + 1]
    h = g1_ - g0_
    t = (g - g0_) / float(h)
    h00, h10, h01, h11 = 2 * t ** 3 - 3 * t ** 2 + 1, t ** 3 - 2 * t ** 2 + t, -2 * t ** 3 + 3 * t ** 2, t ** 3 - t ** 2
    return h00 * u0_ + h10 * h * _M[j] + h01 * u1_ + h11 * h * _M[j + 1]


_ARC = []


def _u_of_s(sf):
    """the spline is reparametrised by LOG DISTANCE to the pair (equal steps = equal zoom rate, so the image speed has ONE hump and an ease-out): s (0..1) -> the spline parameter u"""
    if not _ARC:
        N = 1800
        C0 = Vector((0.5, -30.5, 15.9))                                    # the pair: the zoom is measured toward it
        lg = [math.log((_spline_u(i / float(N), 1) - C0).length) for i in range(N + 1)]
        cum = [lg[0] - v for v in lg]                                      # progress in LOG distance (equal steps = equal zoom rate)
        for i in range(1, len(cum)):
            cum[i] = max(cum[i], cum[i - 1] + 1e-9)
        _ARC.extend([c / cum[-1] for c in cum])
    lo, hi = 0, len(_ARC) - 1
    while hi - lo > 1:
        mid = (lo + hi) // 2
        if _ARC[mid] <= sf:
            lo = mid
        else:
            hi = mid
    f = (sf - _ARC[lo]) / max(1e-9, _ARC[hi] - _ARC[lo])
    return (lo + f) / float(len(_ARC) - 1)


def _spline(g, which):
    return _spline_u(_u_of_s(_umap(g)), which)


def _spline_u(u, which):
    """position on the key spline at the parameter u (which 1 = loc, 2 = look)"""
    P = [Vector(k[which]) for k in KEYS]
    us = [k[0] for k in KEYS]
    j = max(i for i in range(len(us) - 1) if us[i] <= u) if u < 1.0 else len(us) - 2
    tt = (u - us[j]) / (us[j + 1] - us[j])
    p0 = P[j - 1] if j > 0 else P[j] * 2 - P[j + 1]
    p3 = P[j + 2] if j + 2 < len(P) else P[j + 1] * 2 - P[j]
    return Vector([_cr(p0[i], P[j][i], P[j + 1][i], p3[i], tt) for i in range(3)])


def cam_rest(g):
    """(loc, look) in the ship's rest frame at film frame g.  After arrival: a slow push so the shot never parks."""
    loc, look = _spline(min(g, G_ARRIVE), 1), _spline(min(g, G_ARRIVE), 2)
    # settle: a slow orbit about the pair (parallax against the rigging) plus a gentle push; it STARTS during the ease-out (g 140) so the camera never parks
    d = clamp((g - 150) / 70.0)
    ang = math.radians(17.0) * d * d * (3 - 2 * d)
    c = Vector((0.5, -30.5, loc.z))
    loc = c + Matrix.Rotation(ang, 3, "Z") @ (loc - c)
    loc = loc + (look - loc) * (0.0030 * max(0.0, g - 150) * d)
    look = look + Vector((0.0, 0.0, 0.30 * clamp((g - 134) / 36.0)))      # aim a little higher so the heads sit at y 450-760 (the camera still rides the deck)
    return loc, look


# ----------------------------------------------------------------------------- the sea (ONE camera-fitted grid): fit it to a virtual camera far above and behind
def widen_sea(preset, nu, nv):
    import h19_ship as SH
    P = SH.PRESETS[preset]
    look = Vector(P["cam"]["look"])
    P["cam"] = dict(P["cam"], loc=tuple(Vector((14.0, -330.0, 255.0)) * 3.0 / S))   # metres: a virtual camera 3x as far / high as the start pose
    P["sea_nu"], P["sea_nv"] = nu, nv
    P["foam_k"] = float(os.environ.get("FOAMK", "0.55"))                # a calmer wake: less white lace (it dominated the frame statistics)


# ----------------------------------------------------------------------------- the BLANK chart (QA-art: no coastline, no compass, no red mark: "nobody knows where we are")
def _blank_chart_body(k):
    """the unrolled sea chart of cast19.chart19, but BLANK (no coast, no compass, no red mark, no text): parchment, a fold, a dark header band along ONE edge and a
    hanging tie at one corner, so a 180 deg turn reads on a phone."""
    g = cast19._g3(k, "ch", cast19.PARCH, 0, 0, 0.74, 0)
    o = ['<path d="M0,-0.26 L0.74,-0.26 L0.74,0.26 L0,0.26 Z" fill="%s" stroke="%s" stroke-width="0.022" stroke-linejoin="round"/>' % (g, k.ink)]
    o.append('<path d="M0.02,-0.245 L0.72,-0.245 L0.72,-0.115 L0.02,-0.115 Z" fill="%s"/>' % k.c("#1c2a4a"))       # the header band (the top edge)
    o.append('<path d="M0.37,-0.16 L0.37,0.25" stroke="%s" stroke-width="0.006" opacity="0.18"/>' % k.ink)                          # the fold
    o.append('<path d="M0.66,0.26 Q0.69,0.34 0.64,0.40 M0.70,0.26 Q0.74,0.33 0.72,0.38" stroke="%s" stroke-width="0.020" fill="none" stroke-linecap="round"/>' % k.c("#8a5a3a"))  # the tie hanging from the bottom-right corner
    return "".join(o)


import puppet as _puppet
_orig_prop = _puppet._prop


def _prop_rot(k, kind, H, ang, sc=1.0):
    """cast19._prop, plus: a chart19 prop is turned by the pose's 'angle' about its centre (the captain turns the chart upside down)"""
    o, tip = _orig_prop(k, kind, H, ang, sc)
    if kind == "chart19" and abs(ang) > 1e-6:
        o = '<g transform="rotate(%.3f %.4f %.4f)">%s</g>' % (ang, H[0] + 0.37 * sc, H[1], o)
    return o, tip


_puppet._prop = _prop_rot                                    # the puppet drawer calls puppet._prop


cast19._chart_body = _blank_chart_body                        # the prop drawer looks it up at call time


# ----------------------------------------------------------------------------- poses
def _ramp(g, a, b):
    return u_of(g, a, b)


def pose_captain(g):
    """captain19: peers at the blank chart; from g 157 he lifts it, TURNS it 180 deg (upside down), brows up (shocked, then worried), looks at astro19_c and shrugs"""
    p = dict(cast19.STORY19["captain_peer_chart"][1])
    p["lean"] = 8 + 2.0 * math.sin(g * 0.13)
    p["head_roll"] = 4.0 * math.sin(g * 0.09)
    p["blink"] = blink(g, BLINKS_C)
    p["pitch"] = 0.35 + 0.08 * math.sin(g * 0.17)
    p["arm_r"] = dict(hand=(0.6, 0.96 + 0.05 * math.sin(g * 0.2)), bend=0.3, layer="front")
    p["arm_l"] = dict(hand=(1.3, 1.0 + 0.04 * math.sin(g * 0.23 + 1)), bend=0.0, stretch=1.3, layer="front")
    flip = _ramp(g, 160, 170)                     # the 180 deg turn, 160-170, held until the shrug
    lift = _ramp(g, 157, 167) * (1.0 - _ramp(g, 175, 185))
    if lift > 0.0:
        sw = math.sin((g - 159) * 0.6) * (1.0 if g < 175 else 0.3)
        p["arm_r"] = dict(hand=(lerp(0.6, 0.45, lift), lerp(0.96, 1.7, lift) + 0.12 * sw), bend=lerp(0.3, 0.9, lift), layer="front")
        p["arm_l"] = dict(hand=(lerp(1.3, 1.0, lift), lerp(1.0, 1.85, lift) - 0.12 * sw), bend=0.2, stretch=1.2, layer="front")
        p["pitch"] = lerp(0.35, -0.10, lift)
        p["head_roll"] = -10.0 * lift + 3.0 * sw
    p["prop_r"] = dict(type="chart19", scale=1.0, angle=180.0 * flip)
    if g >= 158:
        p["expr"] = "shocked" if g < 172 else "worried"                         # brows up: a clear double-take
    look = _ramp(g, 173, 179)
    if look > 0.0:
        p["gaze"] = (lerp(0.8, 1.0, look), lerp(0.9, 0.0, look))               # at astro19_c (screen-right): the shared look
        p["head_roll"] = lerp(p["head_roll"], 8.0, look)
    shrug = _ramp(g, 181, 189)
    if shrug > 0.0:
        p["arm_r"] = dict(hand=(lerp(0.45, 0.95, shrug), lerp(1.2, 0.80, shrug)), bend=lerp(0.6, 0.0, shrug), shape="open", layer="front")      # symmetric: both elbows out,
        p["arm_l"] = dict(hand=(lerp(1.0, -0.55, shrug), lerp(1.4, 0.80, shrug)), bend=lerp(0.2, 0.0, shrug), shape="open", stretch=1.0, layer="front")   # both hands up, palms open
        p["expr"] = "worried"                                                    # brows stay up through the shrug
                                                                                # the chart stays in his right hand (held low, upside down) through g 199
        p["head_roll"] = lerp(8.0, 7.0, shrug) + 2.0 * math.sin(g * 0.8)
        p["lean"] = 8 - 10.0 * shrug
        p["pitch"] = lerp(0.1, 0.15, shrug)
    p["t"] = g / 30.0
    p = {k: v for k, v in p.items() if v is not None}
    return p


def pose_astro(g):
    """astro19_c: squints through the quadrant at the sky; g 155-173 an OBVIOUS head-scratch; 173-179 looks at the captain; 181-189 shrugs, palms up"""
    p = dict(cast19.STORY19["william_quadrant_sun"][1])                    # arms / prop of the quadrant pose
    p["expr"] = "squint"
    p["blink"] = blink(g, BLINKS_A)
    p["lean"] = -3 + 1.2 * math.sin(g * 0.15)
    p["head_roll"] = 3.0 * math.sin(g * 0.11 + 1.0)
    p["glint"] = 0.5 + 0.5 * math.sin(g * 0.2)
    scr = _ramp(g, 155, 161) * (1.0 - _ramp(g, 173, 177))
    if scr > 0.0:
        w = math.sin(g * 1.35)                                                 # the scratching wobble
        p["arm_r"] = dict(hand=(lerp(0.46, 0.5, scr), lerp(0.1, 0.5, scr)), bend=lerp(-0.7, 0.5, scr), stretch=1.1, layer="top")
        p["prop_r"] = dict(type="quadrant19", angle=lerp(-62, -8, scr), scale=0.95)
        p["arm_l"] = dict(hand=(lerp(-0.46, -0.10 + 0.10 * w, scr), lerp(0.96, 2.3 + 0.12 * w, scr)), bend=lerp(0.5, 1.0, scr), shape="open")
        p["pitch"] = lerp(-0.75, 0.2, scr)
        p["expr"] = "unimpressed" if scr > 0.4 else "squint"
        p["head_roll"] = 9.0 * scr * math.sin(g * 1.35 + 0.7)
        p["gaze"] = (0.2, 0.3)
        p["glint"] = 0.0
    look = _ramp(g, 173, 179)
    if look > 0.0:
        p["pitch"] = lerp(p.get("pitch", -0.75), 0.15, look)
        p["gaze"] = (lerp(0.2, -1.0, look), 0.0)                              # at the captain (screen-left; the card is mirrored)
        p["expr"] = "worried" if look > 0.5 else p["expr"]
    shrug = _ramp(g, 181, 189)
    if shrug > 0.0:
        p["arm_r"] = dict(hand=(lerp(0.5, 0.95, shrug), lerp(0.5, 0.7, shrug)), bend=lerp(0.5, -0.2, shrug), shape="open", stretch=1.0, layer="top")
        p["arm_l"] = dict(hand=(lerp(-0.1, -0.9, shrug), lerp(2.2, 0.75, shrug)), bend=lerp(1.0, 0.4, shrug), shape="open")
        p["prop_r"] = dict(type="quadrant19", angle=lerp(-8, 25, shrug), scale=0.95)   # the quadrant stays in his right hand (lowered), never pops out
        p["head_roll"] = lerp(0.0, -8.0, shrug)
        p["lean"] = lerp(-3, -8, shrug)
        p["pitch"] = 0.1
    p["t"] = g / 30.0
    p = {k: v for k, v in p.items() if v is not None}
    return p


def whitecaps_and_wake(n=int(os.environ.get("WC", "170")), seed=int(os.environ.get("WCSEED", "5")), L=300.0):
    """the aerial preset has no whitecaps and the set's wake fades by ~150 m, so the extreme wide start is smooth water (qa_auto: 'suspected blur').  The set's own
    'streaks' hook (broken foam lines, ship frame, metres) is only fed by hero / rocks / coast scenery: wrap LD.scenery so the aerial sea gets scattered whitecap lines over +-320 m (the set's own wake is already a long V seen from behind).  Runtime only, no set edit."""
    import random as _rnd
    import h19_ship_land as LD
    orig = LD.scenery

    def sc(S_, P, LT, sea_P, marks):
        orig(S_, P, LT, sea_P, marks)
        st = sea_P.setdefault("streaks", [])
        rg = _rnd.Random(seed)
        for _ in range(n):
            cx, cy = rg.uniform(-320, 320), rg.uniform(-330, 240)
            if abs(cx) < 18 + 0.40 * max(0.0, -cy - 20) and cy < 50:
                continue                                                   # not on the ship or in its wake
            a = math.radians(rg.uniform(-35, 35)); ln = rg.uniform(20, 50)
            st.append(((cx - 0.5 * ln * math.cos(a), cy - 0.5 * ln * math.sin(a)), (cx + 0.5 * ln * math.cos(a), cy + 0.5 * ln * math.sin(a)),
                       rg.uniform(2.0, 3.6), rg.uniform(0.7, 0.9)))
    LD.scenery = sc


class Take(C.Take):
    def __init__(self, quality="preview"):
        whitecaps_and_wake()
        widen_sea(PRESET, int(os.environ.get("NU", "1500")), int(os.environ.get("NV", "2000")))
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_" + TAKE)
        assert self.final_samples() == FINAL_SPP, "set final samples changed: %s" % self.final_samples()
        root = self.A["ship_root"]
        self.cap = self.actors["cap"] = C.make_actor("cap", "captain19", os.path.join(WORK, "sprites"), contact=True, cam=self.cam)
        self.ast = self.actors["ast"] = C.make_actor("ast", "astro19_c", os.path.join(WORK, "sprites"), contact=True, cam=self.cam)
        for a in (self.cap, self.ast):
            C.ride_ship(a, root)                                           # BEFORE place() and BEFORE any set_roll key: the inverse is taken at rest
        self.cam_pose(FIRST_G, root)

    def cam_pose(self, g, root):
        f = bf(g)
        self.key_set(f, sea=g / 30.0, roll=g / 30.0)                       # same t on every frame
        loc, look = cam_rest(g)
        self.key_cam(f, *C.on_ship(root, f, loc, look))                    # the camera rides the deck (rest-frame pose -> world)

    def pose(self, gs):
        root = self.A["ship_root"]
        for g in gs:
            f = bf(g)
            self.cam_pose(g, root)
            C.key_vis([o for o in (C.bpy.data.objects.get("gulls_gullt"), C.bpy.data.objects.get("gulls_gullw"), C.bpy.data.objects.get("headland")) if o], False, f)   # no gulls, and no pale 'headland' slab on the horizon
            C.place(self.cap, f, (CAP_XY[0], CAP_XY[1], Z_QD))
            C.place(self.ast, f, (AST_XY[0], AST_XY[1], Z_QD))
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.cap.pose(f, pose_captain(g), camera=self.cam)
            pa = pose_astro(g)
            pa["mirror"] = True
            self.ast.pose(f, pa, camera=self.cam)
        self.sprites_for([(self.cap, PPD), (self.ast, PPD)], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = cam_rest(g)
        return dict(g=g, cam=[round(c, 2) for c in loc], heads=C.head_report(self, f), dof=self.cam.data.dof.use_dof,
                    caption_shade=bool(C.bpy.data.objects.get("caption_shade")))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


def camreport():
    prev = None
    mx = 0
    for g in GS:
        loc, look = cam_rest(g)
        if prev is not None:
            d = (loc - prev).length
            mx = max(mx, d)
        if g % 12 == 0:
            print(g, [round(c, 1) for c in loc], [round(c, 1) for c in look])
        prev = loc


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        camreport()
        sys.exit(0)
    gs = [g for g in C.parse(sys.argv[2]) if FIRST_G <= g <= G_LAST]
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
                print("g %d  %.1f s wall" % (g, st["wall"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else FINAL_SPP
        quality = "final" if scale >= 1.0 else "preview"
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take(quality), gs, out, scale=scale, samples=samples)
