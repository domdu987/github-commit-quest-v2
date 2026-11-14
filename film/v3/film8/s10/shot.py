#!/usr/bin/env python3
"""shot.py -- film 8 take s10: shots 10 + 11 + 12 (g 781..963, plan 26.03-32.12 s) + 6 handle frames each side (g 775..969).
"Night one, the water in the channels froze into a thin sheet.  Night ten, it was a finger thick.  Every morning before sunrise he cut
the ice and carried it into the dome."  One location (desert_ice plain), two lights (NIGHT for 10-11, DAWN for 12: one build each):

    id 10  g 775..839  shot 10, NIGHT, low over channel 3 (y 7.4, no sawn hole) looking east: open starlit water freezes into the thin
                       translucent sheet (set_ice 0 -> 0.25, keyed per frame, g 790..830; "แข็งเป็นแผ่นบาง ๆ" 26.98 s = g 812).  Lantern
                       glints, the dome's glowing door far down the channel.  Slow low push.
    id 11  g 840..881  shot 11, NIGHT, night ten: thick white-blue ice; farid crouches on the north bank and taps the slab with one finger
                       (taps g 850 / 858 / 866 around "หนาเท่านิ้ว" 28.62 s = g 862), then a pleased smile.  Push + slight orbit.
    id 12  g 882..969  shot 12, DAWN wide from the north-west over the channels: farid saws a block at the hole in channel 2 (g 882..911),
                       lifts it (912..921) and carries it east along the bank toward the dome (922..969), sunrise sky, the dome ahead.
Cuts at g 840 and 882 (plan).  transition_in cut (from shot 9's dome at dawn).  Mouths: no quote.  NO depth of field (C.Take).

    python3 shot.py stills 10,11,12 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 10|11|12 a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import common as C                                       # noqa: E402
from mathutils import Vector                             # noqa: E402

D, actors, camrig, cast8 = C.D, C.actors, C.camrig, C.cast8
import puppet                                            # noqa: E402
lerp, clamp, blink, ez, bf = C.lerp, C.clamp, C.blink, C.ez, C.bf
TMP = os.path.join(HERE, "work")

G0, G11, G12, G1 = C.g_bound(26.03), C.g_bound(28.00), C.g_bound(29.40), C.g_bound(32.12)   # 781, 840, 882, 964
H = 6
RANGES = {10: (G0 - H, G11 - 1), 11: (G11, G12 - 1), 12: (G12, G1 + H - 1)}
LIGHT = {10: "NIGHT", 11: "NIGHT", 12: "DAWN"}
PRESET = {10: "channel_ecu", 11: "channel_ecu", 12: "channels_wide"}
G_FREEZE = (790, 830)
TAPS = (850, 858, 866)
G_SAW, G_LIFT = (882, 911), (912, 921)


def aim(loc, az, el, d=30.0):
    a, e = math.radians(az), math.radians(el)
    return tuple(loc[i] + d * v for i, v in enumerate((math.sin(a) * math.cos(e), math.cos(a) * math.cos(e), math.sin(e))))


CH3 = D.CH_Y[2]                                          # 7.4
CAM = {10: (((-5.0, 7.15, 0.95), 80.0, -6.0), ((-3.9, 7.3, 0.82), 80.5, -5.0)),
       11: (((-2.9, 6.55, 1.45), 66.0, -4.0), ((-2.35, 6.75, 1.40), 70.0, -4.0)),
       12: (((-9.2, 7.45, 3.1), 108.5, -4.0), ((-8.4, 7.35, 2.95), 106.0, -3.0))}
LENS = {10: 22.0, 11: 22.0, 12: 20.0}
FARID11 = Vector((1.55, 8.78, 0.0))                     # north bank of channel 3 (lane y 8.8), clear of the x -9 / 2 / 12 posts
TAP_PT = (2.75, 7.75)                                    # the ice point he taps (channel 3, near its north edge)
FARID12_SAW = Vector((-2.55, 3.2, 0.0))                  # south bank lane of channel 2, just west of the sawn hole
WALK_V = 0.055                                           # D per frame while carrying


def cam_of(shot, g):
    a, b = RANGES[shot]
    x = (g - a) / float(b - a)
    (l0, az0, p0), (l1, az1, p1) = CAM[shot]
    u = 0.35 * ez(x, "sine") + 0.65 * x
    loc = Vector(lerp(l0, l1, u))
    return loc, Vector(aim(loc, lerp(az0, az1, u), lerp(p0, p1, u)))


def ice_of(shot, g):
    if shot == 10:
        return (0.25 * clamp((g - G_FREEZE[0]) / float(G_FREEZE[1] - G_FREEZE[0])), 0.0)
    return (1.0, 0.0) if shot == 11 else "thick"


# ----------------------------------------------------------------------------- poses
def tap_u(g):
    """0 = finger on the ice, 1 = lifted: three quick taps."""
    u = 1.0
    for t in TAPS:
        d = abs(g - t)
        if d < 4:
            u = min(u, d / 4.0)
    return u


def pose11(g, target=None):
    """crouched on the bank, leaning over the channel (screen-right), right index finger down to the ice; target = local hand point."""
    after = clamp((g - TAPS[-1] - 4) / 8.0)
    p = dict(yaw=0.60, pitch=lerp(0.85, 0.35, after) + 0.05 * math.sin(g * 0.2), expr="excited" if g < TAPS[-1] + 6 else "happy",
             mouth="smile", head_roll=-6 + 2 * math.sin(g * 0.15), lean=lerp(26.0, 14.0, after), gaze=(0.6, lerp(0.9, 0.2, after)),
             legs=dict(preset="crouch", crouch=0.45, stride=0.35),
             arm_l=dict(hand=(0.30, 1.15), bend=0.4, stretch=1.2, shape="open", layer="front"))
    if target is None:
        target = (0.95, 1.35)
    lift = 0.22 * tap_u(g) + 0.25 * after
    p["arm_r"] = dict(hand=(target[0] - 0.10, target[1] - 0.12 - lift), bend=-0.25, stretch=1.3, sharp=1.0, shape="point", layer="front")
    p["blink"] = blink(g, [846, 873])
    p["t"] = g / 30.0
    return p


def pose12(g):
    if g <= G_SAW[1]:
        p = dict(cast8.STORY8["farid_saw"][1])
        a = math.radians(32); s = 0.10 * math.sin(2 * math.pi * (g - G_SAW[0]) / 10.0)
        h = p["arm_r"]["hand"]
        p["arm_r"] = dict(p["arm_r"], hand=(h[0] + s * math.cos(a), h[1] + s * math.sin(a)))
        p["head_roll"] = -6 + 1.5 * math.sin(g * 0.6)
    elif g <= G_LIFT[1]:
        u = ez((g - G_LIFT[0]) / float(G_LIFT[1] - G_LIFT[0]))
        p = dict(cast8.STORY8["farid_carry_ice"][1])
        p["legs"] = dict(preset="crouch", crouch=lerp(0.42, 0.0, u), stride=lerp(0.4, 0.2, u))
        p["lean"] = lerp(24.0, -5.0, u); p["pitch"] = lerp(0.7, 0.25, u)
        for k in ("arm_r", "arm_l"):
            h = p[k]["hand"]; p[k] = dict(p[k], hand=(h[0], h[1] + 0.35 * (1 - u)))
    else:
        base = dict(cast8.STORY8["farid_carry_ice"][1])
        w = cast8.cycle("farid", (g - G_LIFT[1]) / 28.0, "walk", facing=-1, base=base, arms="none")
        p = w
        p["yaw"] = 0.55; p["lean"] = -5.0 + 1.0 * math.sin(g * 0.45)
    p["mirror"] = True                        # east (the hole, the dome) is screen-left from this camera
    p["blink"] = blink(g, [905, 948])
    p["t"] = g / 30.0
    return p


def farid12_at(g):
    if g <= G_LIFT[1]:
        return FARID12_SAW
    return FARID12_SAW + Vector((WALK_V * (g - G_LIFT[1]), 0.0, 0.0))


# ----------------------------------------------------------------------------- runtime set dressing (desert.py untouched)
def dress(shot):
    S = D.STATE; M = S['M']; SET = S['SET']; mb = D.MB()
    if shot == 12:
        for k, (x, y, z) in enumerate(((-4.6, 2.95, 0.0), (-3.75, 3.0, 0.0), (-4.2, 2.95, 0.44))):     # cut blocks waiting on the bank
            mb.box((x - 0.36, y - 0.26, z), (x + 0.36, y + 0.26, z + 0.44), M['ice_block'])
        D.beam(mb, (-6.4, 2.9, 0.08), (-5.2, 2.9, 0.08), 0.5, 0.06, M['wood_l'])                    # straw mat strip under the next blocks
        D.lumpy(mb, (-6.0, 3.1, 0.05), 0.35, M['straw'], 1201, seg=8, rings=4, rough=0.35, squash=0.35)
        D._bucket(mb, (-3.3, 3.45, 0.0), M, s=0.55)
        D._jar(mb, (-7.6, 3.15, 0.0), M, h=1.0, r=0.34, seed=12)
        D.beam(mb, (-2.0, 6.3, 0.05), (-0.6, 6.15, 0.05), 0.12, 0.08, M['wood'])                    # a spare plank on the far bank
    else:
        D._bucket(mb, (-0.8, 8.9, 0.0), M, s=0.55)                                               # his bucket on the bank
        D._jar(mb, (4.6, 9.0, 0.0), M, h=1.0, r=0.34, seed=11)
        D.lumpy(mb, (-1.6, 5.95, 0.08), 0.18, M['rock'], 1101, seg=8, rings=4, rough=0.3, squash=0.6)
    ob = D._obj(mb, 's10_dress_%d' % shot, SET, hull=0.012)
    D.no_bounce(ob)
    return ob


SUN12 = ((0.62, -0.78), 13.0)                            # as s08 shot 9: warm dawn key from the north-west (dome face, wall, farid lit)


class Take(C.Take):
    def __init__(self, quality="preview", shot=10):
        if LIGHT[shot] == "DAWN":
            D.LIGHTS["DAWN"] = dict(D.LIGHTS["DAWN"], key_dir=D.G._kd(*SUN12), sun_elev=SUN12[1])
        C.Take.__init__(self, "desert_ice", PRESET[shot], quality=quality, lens=LENS[shot], name="cam_s10", light=LIGHT[shot])
        self.far = self.actors["far"] = C.make_actor("far", "farid", os.path.join(TMP, "sprites"))
        self.dress = dress(shot)

    def pose(self, shot, gs):
        far = self.far
        for g in gs:
            f = bf(shot, g)
            loc, look = cam_of(shot, g)
            self.key_cam(f, loc, look, lens=LENS[shot])
            C.place(far, f, FARID11 if shot == 11 else (farid12_at(g) if shot == 12 else Vector((-40.0, 40.0, 0.0))))
            far.card.hide_render = shot == 10; far.card.keyframe_insert("hide_render", frame=f)
            self.key_set(f, ice=ice_of(shot, g))
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            if shot == 11:
                far.pose(f, pose11(g), camera=self.cam)
                tgt = actors.world_to_local(far, self.cam, (TAP_PT[0], TAP_PT[1], D.CH_Z['ice0'] + 0.08), f)
                if g in (846, 850, 875): print("tap target", g, tuple(round(v, 3) for v in tgt), flush=True)
                far.pose(f, pose11(g, tgt), camera=self.cam)
            elif shot == 12:
                far.pose(f, pose12(g), camera=self.cam)
            else:
                far.pose(f, dict(cast8.STORY8["farid_stand"][1]), camera=self.cam)
        self.sprites_for([(far, {10: 64, 11: 320, 12: 192}[shot])], [bf(shot, g) for g in gs])

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look = cam_of(shot, g)
        v = look - loc
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    heads=C.head_report(self, f) if shot != 10 else {}, ice=ice_of(shot, g))

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    if cmd in ("probe", "stills"):
        for shot in shots:
            gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
            if not gs:
                continue
            Tk = Take("preview", shot)
            Tk.pose(shot, gs)
            for g in gs:
                print(json.dumps(Tk.report(shot, g)), flush=True)
                if cmd == "stills":
                    out = sys.argv[4]; os.makedirs(out, exist_ok=True)
                    scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
                    samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
                    st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                    os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
                    print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q, shot: Take(q, shot), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples, take_key=lambda s: s)
