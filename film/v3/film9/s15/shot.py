#!/usr/bin/env python3
"""shot.py -- film 9 take s15: shots 15 + 16 (g 1153..1412, handles g 1147..1152 and g 1413..1418), THE REVEAL inside the mortar joint
(wall.py macro area, 1 D ~ 2 mm, BATTLE light).  Two set-ups, two processes (one macro kind per build):

    id 15  g 1147..1283  mortar_macro (plain lime mortar): macro_front, near square-on to the grey joint with cyan lime crystals, slow push.
                         "ปูนธรรมดา แข็งก็จริง แต่เปราะ" calm; the cannonball flies in over the camera's left shoulder (g 1180..1207)
                         and strikes on "โดนกระแทก" (40.12 s -> g 1207): flash, small camera jolt, a BLACK brittle crack with a pale
                         chipped lip races along the whole joint both ways and branches up / down into the bricks on
                         "ทีเดียวก็ร้าวทั้งแผ่น" (g 1207..1262), shards spall toward the lens, dust puff; the ball drops away.
    id 16  g 1284..1418  mortar_macro_rice: macro_front again (push from slightly right / below), creamy matrix.
                         On "ส่วนแป้งข้าวเหนียว ไปพันกับผลึกปูน เป็นตาข่ายเหนียวหนึบ" (41.95-45.39 s) the slow push shows the glowing
                         gold starch net wrapped round the cyan lime crystals; on "ลูกปืนกระแทก" the ball flies in (g 1352..1380) and hits
                         (g 1380): the face dents, a bright gold ring pulses out over the net, the web stretches, flexes back in a damped
                         spring and HOLDS; the ball springs back a little and settles, held in its shallow dent with a glowing dent ring,
                         on "แค่ไหนก็แค่บุบ" (46.12-47.10 s) (round-3 set: the ball stays visible).  Out-handle g 1413..1418 continues.
Mouths: nobody on screen.  NO depth of field (C.Take).  Blender frame: bf() below (smoke phase).

    python3 shot.py stills 15|16 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 15|16 a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c9 as C                                           # noqa: E402
from mathutils import Vector                             # noqa: E402
import bpy                                               # noqa: E402

W = C.B
lerp, clamp, ez = C.lerp, C.clamp, C.ez

G0, G_CUT, G1, H = 1153, 1284, 1413, 6
RANGES = {15: (G0 - H, G_CUT - 1), 16: (G_CUT, G1 + H - 1)}
PRESET = {15: "mortar_macro", 16: "mortar_macro_rice"}
IMP = Vector((1.5, 0.22, 0.0))

# event frames (narration t -> g = round((t + 0.10) * 30))
G_HIT15 = C.g_of(40.12)            # 1207 "โดนกระแทก"
G_FLY15 = G_HIT15 - 27             # 1180 ball enters
G_CRACK_END = C.g_of(41.85)        # 1262 "ร้าวทั้งแผ่น" ends: the crack has reached both ends
G_WEB = (C.g_of(43.10) - 9, C.g_of(44.72) - 19)     # 1290..1337 the web spreads ("ไปพันกับผลึกปูน เป็นตาข่าย")
G_HIT16 = C.g_of(45.88)            # 1380 end of "ลูกปืนกระแทก"
G_FLY16 = G_HIT16 - 28             # 1352


def bf(shot, g):
    """Blender frame.  The set's macro smoke billows / embers take their phase from the Blender frame (rate 0.003 = one cycle per
    333.3 frames).  Shot 16 (f 3285..3420) has a clean phase (no billow in front of the impact); shot 15 is placed exactly one cycle
    earlier (f 2952..3088) so it gets the same clean phase (at f 2148.. big billows drifted across the lens)."""
    return (2000 + int(g) + 1) if shot == 16 else (int(g) + 1805)


def macro_t(shot, g):
    if shot == 15:
        if g < G_FLY15:
            return 0.0
        if g < G_HIT15:
            return 0.3 * (g - G_FLY15) / float(G_HIT15 - G_FLY15)
        if g < G_CRACK_END:
            return 0.3 + 0.45 * (g - G_HIT15) / float(G_CRACK_END - G_HIT15)
        return min(1.0, 0.75 + 0.25 * (g - G_CRACK_END) / 26.0)
    if g < G_FLY16:
        return 0.0
    if g < G_HIT16:
        return 0.3 * (g - G_FLY16) / float(G_HIT16 - G_FLY16)
    return min(1.0, 0.3 + 0.7 * (g - G_HIT16) / 40.0)


# cameras: (loc, look) at the start / end of each set-up.  Round-3 set: the default macro_front (1.4, -8.6, 0.25) -> (1.5, 0.22, 0),
# 24 mm, near square-on, impact dead centre, the joint a horizontal band.  Plain: slow push in from slightly left + above; rice: the
# same push from slightly right + below (a fresh framing at the cut, same subject placement for the 1:1 comparison).
CAM = {15: (((0.95, -9.5, 0.55), (1.45, 0.22, 0.02)), ((1.75, -7.7, 0.12), (1.5, 0.22, 0.0))),
       16: (((2.35, -9.5, -0.15), (1.55, 0.22, -0.02)), ((1.3, -7.4, 0.3), (1.5, 0.22, 0.0)))}
LENS = 24.0


def cam_of(shot, g):
    a, b = CAM[shot]
    lo, hi = RANGES[shot]
    x = (g - lo) / float(hi - lo)
    u = 0.35 * ez(x, "sine") + 0.65 * x
    loc, look = Vector(lerp(a[0], b[0], u)), Vector(lerp(a[1], b[1], u))
    gh = G_HIT15 if shot == 15 else G_HIT16
    if g >= gh:                                      # a small jolt on the hit, decaying over ~10 frames
        k = (g - gh)
        amp = 0.07 * math.exp(-k / 4.0)
        loc += Vector((amp * math.sin(k * 2.1), 0.0, amp * math.cos(k * 2.7)))
        look += Vector((0.5 * amp * math.sin(k * 1.7 + 1), 0.0, 0.5 * amp * math.cos(k * 2.3)))
    return loc, look


class Take(C.Take):
    def __init__(self, quality="preview", shot=15):
        C.Take.__init__(self, "wall_site", PRESET[shot], quality=quality, lens=LENS, name="cam_s15_%d" % shot, light="BATTLE")
        self.shot = shot

    def pose(self, shot, gs):
        for g in gs:
            f = bf(shot, g)
            loc, look = cam_of(shot, g)
            self.key_cam(f, loc, look, lens=LENS)
            self.key_set(f, macro=macro_t(shot, g))

    def report(self, shot, g):
        loc, look = cam_of(shot, g)
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], macro_t=round(macro_t(shot, g), 4), heads={})

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    shot = int(sys.argv[2])
    if cmd == "stills":
        Tk = Take("preview", shot)
        gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
        Tk.pose(shot, gs)
        out = sys.argv[4]; os.makedirs(out, exist_ok=True)
        scale = float(sys.argv[5]) if len(sys.argv) > 5 else 1.0
        samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
        for g in gs:
            st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
            os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
            print("shot %d g %d t %.3f  %.1f s wall %.1f cpu" % (shot, g, macro_t(shot, g), st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q, s: Take(q, s), [shot], sys.argv[3], RANGES, HERE, scale=scale, samples=samples, take_key=lambda s: s)
