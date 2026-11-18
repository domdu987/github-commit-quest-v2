#!/usr/bin/env python3
"""shot.py -- film 10 take s15: shots 15 + 16 (g 998..1089 + 6 handle frames each side), the attack.
One location (sea, SEA_DAY), two set-ups joined by the plan's cut at 34.90 s (g 1047):

    id 15  g 992..1046  periscope_close: the U-boat captain at the conning-tower periscope, eye in the eyepiece, the other eye
                        squeezed shut, both hands on the grips turning the handles; a slow push in (with a small orbit); at the
                        end the right fist comes up ("aim").  The convoy sails on beyond (s -1.6 .. 0).
    id 16  g 1047..1095 torpedo_chase: the torpedo leaves the bow of the U-boat (the boat sinks under it) and a camera low behind it
                        races over the foam wake toward the convoy (s 0 .. 3.4, torpedo_u(s)).

Blender frame of (id, g) = 1000 * (id - 1) + g + 1.  Sea time s is shared with s17 (same S_KEYS table in both shot.py files).

    python3 shot.py probe 15,16 a:b[:step]
    python3 shot.py stills 15,16 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 15|16 a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c10 as C                                          # noqa: E402  (paths, cast10 first, bpy, harbour, stage)
from mathutils import Vector                             # noqa: E402

H, actors, camrig, cast10 = C.B, C.actors, C.camrig, C.cast10
lerp, clamp, blink, ez, bf = C.lerp, C.clamp, C.blink, C.ez, C.bf
TMP = os.path.join(HERE, "work")

# ----------------------------------------------------------------------------- timing
G15, G16, G17 = C.g_bound(33.27), C.g_bound(34.90), C.g_bound(36.35)       # 998, 1047, 1090
H_IN, H_OUT = 6, 6
RANGES = {15: (G15 - H_IN, G16 - 1), 16: (G16, G17 + H_OUT - 1)}
LOC = ("sea", "periscope_close")
G_FIST = (G15 + 26, G15 + 40)                  # the right fist comes up ("aim")

# sea time s (shared with s17): s < 0 before the shot is fired
S15 = (-1.6, 0.0)                              # across shot 15 (G15 .. G16)
S16 = (0.0, 1.6)                               # across shot 16 (G16 .. G17)
U16 = 0.09                                     # torpedo path parameter reached at the end of shot 16 (s17 continues from here)


def s_of(shot, g):
    if shot == 15:
        return lerp(S15[0], S15[1], (g - G15) / float(G16 - G15))
    return lerp(S16[0], S16[1], (g - G16) / float(G17 - G16))


def uw(v):
    return tuple(H._uboat_world(v))


# set-up 15: low by the conning tower, the captain left of centre against the convoy; push in + orbit toward his face
CAM15_0 = (uw((-6.8, -5.8, 3.7)), uw((-0.8, 0.4, 5.0)), 24.0)
CAM15_1 = (uw((-4.3, -3.4, 4.1)), uw((-1.0, 0.1, 5.35)), 26.0)


def cam15(g):
    x = (g - G15) / float(G16 - G15)
    u = 0.35 * ez(x, "sine") + 0.65 * x
    return (Vector([lerp(CAM15_0[0][i], CAM15_1[0][i], u) for i in range(3)]), Vector([lerp(CAM15_0[1][i], CAM15_1[1][i], u) for i in range(3)]),
            lerp(CAM15_0[2], CAM15_1[2], u))


def u_of16(g):
    return U16 * (g - G16) / float(G17 - G16)      # constant speed; s17 continues at 0.002 / frame


def cam16(g):
    x = (g - G16) / float(G17 - G16)
    u = u_of16(g)
    back = lerp(16.0, 12.5, clamp(x * 1.5)); up = lerp(8.0, 4.4, clamp(x * 1.5))
    c = H.torpedo_cam(u, back=back, up=up)
    loc, look = Vector(c["loc"]), Vector(c["look_at"])
    # a slow sideways drift so the chase never sits still, and a gentle roll of the look-at
    side = Vector((-math.cos(math.radians(80)), math.sin(math.radians(80)), 0))   # roughly perpendicular to the path (path ~ +y)
    sw = lerp(3.5, -1.5, x)
    return loc + Vector((sw, 0, 0)), look, 22.0


def u_of(g, a, b):
    return ez((g - a) / float(b - a)) if g > a else 0.0


# ----------------------------------------------------------------------------- the captain
P_PER = cast10.STORY10["uboat_periscope"][1]
P_AIM = cast10.STORY10["uboat_aim"][1]


def pose15(g):
    f = u_of(g, *G_FIST)
    p = dict(P_PER)
    k = (g - G15)
    # both hands turn the grips (small circular wobble), then the left fist comes up to aim
    al = dict(P_PER["arm_l"]); ar = dict(P_PER["arm_r"])
    hl = P_PER["arm_l"]["hand"]; hr = P_PER["arm_r"]["hand"]
    wob = 0.035
    ar["hand"] = (hr[0] + wob * math.sin(k * 0.31), hr[1] + wob * math.cos(k * 0.31))
    if f > 0:
        al["hand"] = (lerp(hl[0], P_AIM["arm_l"]["hand"][0], f), lerp(hl[1], P_AIM["arm_l"]["hand"][1], f))
        al["bend"] = lerp(P_PER["arm_l"]["bend"], P_AIM["arm_l"]["bend"], f)
        al["stretch"] = lerp(P_PER["arm_l"]["stretch"], P_AIM["arm_l"]["stretch"], f)
        al["layer"] = "back" if f > 0.5 else "front"
    else:
        al["hand"] = (hl[0] + wob * math.sin(k * 0.31 + 1.6), hl[1] + wob * math.cos(k * 0.31 + 1.6))
    p.update(arm_l=al, arm_r=ar)
    p["lean"] = lerp(5.0, 9.5, ez((g - G15) / 49.0)) + 0.8 * math.sin(g * 0.19)
    p["pitch"] = 0.05 + 0.04 * math.sin(g * 0.13)
    p["head_roll"] = -3.0 + 1.2 * math.sin(g * 0.17)
    p["t"] = g / 30.0
    return p


# ----------------------------------------------------------------------------- the take
class Take(C.Take):
    def __init__(self, quality="preview", shot=15):
        C.Take.__init__(self, LOC[0], LOC[1], quality=quality, lens=22.0, name="cam_s15")
        cv = cast10.CANVAS10_SCOPE["uboat_captain"]
        self.cap = self.actors["cap"] = C.make_actor("cap", "uboat_captain", os.path.join(TMP, "sprites"), canvas=cv)
        self.mark = Vector(self.A["marks"]["uboat_captain"])
        U = H.STATE["uboat"]
        self.scope3d = [U["tube"], U["head"]]               # the cast draws its own periscope in shot 15

    def pose(self, shot, gs):
        cap = self.cap
        for g in gs:
            f = bf(shot, g)
            if shot == 15:
                loc, look, lens = cam15(g)
                s = s_of(15, g)
                self.key_set(f, convoy=s, torpedo=-1.0, uboat=(0.0, 1.0), ghost=0.0, lead_marker=0.0, ghost_marker=0.0, hit=-1.0)
            else:
                loc, look, lens = cam16(g)
                s = s_of(16, g)
                x = clamp((g - G16) / float(G17 - G16 + 4))
                self.key_set(f, convoy=s, torpedo=u_of16(g), uboat=(ez(x * 1.15), 1.0 - ez(x * 1.15)), ghost=0.0, lead_marker=0.0,
                             ghost_marker=0.0, hit=-1.0)
            self.key_cam(f, loc, look, lens=lens)
            C.place(cap, f, self.mark, z=self.mark.z)
            hide = shot == 16
            cap.card.hide_render = hide
            cap.card.keyframe_insert("hide_render", frame=f)
            for ob in self.scope3d:
                ob.hide_render = shot == 15
                ob.keyframe_insert("hide_render", frame=f)
        for g in gs:                                    # (shot 16: the card is hidden, but keeps valid sprites)
            f = bf(shot, g)
            self.scene.frame_set(f)
            cap.pose(f, pose15(min(g, G16 - 1)), camera=self.cam)
        self.sprites_for([(cap, 320)], [bf(shot, g) for g in gs])

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look, lens = cam15(g) if shot == 15 else cam16(g)
        v = look - loc
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    s=round(s_of(shot, g), 3), heads=C.head_report(self, f) if shot == 15 else {})

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    if cmd in ("probe", "stills"):
        Tk = Take("preview")
        for shot in shots:
            gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
            if not gs:
                continue
            Tk.pose(shot, gs)
            for g in gs:
                print(json.dumps(Tk.report(shot, g)), flush=True)
                if cmd == "stills":
                    out = sys.argv[4]
                    scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
                    samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
                    st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                    os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
                    print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q, shot=15: Take(q), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
