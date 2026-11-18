#!/usr/bin/env python3
"""shot.py -- film 11 take s15: shot 15, the false payoff turns: "แต่เช้า วันรุ่งขึ้น เด็กลุกขึ้นมาวิ่งเล่นเหมือนเดิม" g 898..982 (+6 handle frames each side).
room_morning / light A (sun across the bed).  James wakes in bed (lying card, flush gone, eyes open), sits up and leaps out of bed (standing card, jump arc
from the bed edge to the sunny floor, landing squash), then skips and runs about the floor; his mother sits relieved by the bed head, Jenner stands
proud beside the room.  Nobody speaks.  The blister card stays on James's upper_arm_l (lying overlay and standing overlay).
    python3 shot.py probe 15 a:b[:step] | stills 15 a:b[:step] <out_dir> [scale] [samples] | final 15 a:b[:step] [scale] [samples]
"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c11 as C                                          # noqa: E402
import cast11                                            # noqa: E402
from mathutils import Vector                             # noqa: E402

lerp, clamp, blink, ez, bf, u_of = C.lerp, C.clamp, C.blink, C.ez, C.bf, C.u_of
TMP = os.path.join(HERE, "work")
SHOT = 15
G0, G1 = C.g_bound(29.95), C.g_bound(32.76)              # 898, 983
H = 6
RANGES = {SHOT: (G0 - H, G1 - 1 + H)}
DISSOLVE_IN = True
CUES = [{"frame": 922, "label": "James springs out of bed, bare feet thump on the floor boards", "kind": "foley"}]
PRESET, LIGHT = "room_morning", None

G_SIT = 922                    # James sits up (lying card -> standing card)
G_LEAP = (924, 938)            # the leap: from the bed edge to the floor
G_RUN = 938                    # skipping / running about
BED = (-5.2, 7.0)
BED_Z = 1.86
BED_EDGE = (-3.5, 5.6, 1.86)
LAND = (-1.5, 4.3)
MOM = (-2.8, 6.8)
JEN = (-0.9, 7.9)

CAM0 = ((2.8, -2.2, 2.5), (-2.2, 5.6, 1.5))
CAM1 = ((1.8, -1.4, 2.35), (-1.9, 5.2, 1.45))


def cam_of(g):
    x = (g - G0) / float(G1 - G0)
    x = min(x, 1.0)
    u = 0.3 * ez(max(x, 0.0), "sine") + 0.7 * x
    return Vector([lerp(CAM0[0][i], CAM1[0][i], u) for i in range(3)]), Vector([lerp(CAM0[1][i], CAM1[1][i], u) for i in range(3)])


def quilt_svg():
    cols = ["#e9dcbc", "#d9a35a", "#9fb59a", "#8f9fb8", "#e9dcbc", "#c98a5a"]
    x0, x1, y0, y1 = -0.66, 0.14, 1.02, 1.93
    n, m = 2, 2
    w, h = (x1 - x0) / n, (y1 - y0) / m
    s = '<g stroke="#3a2832" stroke-width="0.018">'
    for i in range(n):
        for j in range(m):
            s += '<rect x="%.3f" y="%.3f" width="%.3f" height="%.3f" fill="%s"/>' % (x0 + i * w, y0 + j * h, w, h, cols[(i * 2 + j * 3) % len(cols)])
    s += '</g>'
    s += '<rect x="%.3f" y="%.3f" width="0.11" height="%.3f" rx="0.04" fill="#f3ead4" stroke="#3a2832" stroke-width="0.02"/>' % (x1 - 0.02, y0 - 0.04, y1 - y0 + 0.08)
    return s


def lie_overlay(f, pose, an):
    return quilt_svg() + C.sore_svg(an["upper_arm_l"], "blister")


def stand_overlay(f, pose, an):
    return C.sore_svg(an["upper_arm_l"], "blister")


def jump_state(g):
    """(x, y, z, mode) of the standing James: 'air' on the leap, 'floor' after."""
    u = u_of(g, *G_LEAP)
    x = lerp(BED_EDGE[0], LAND[0], u); y = lerp(BED_EDGE[1], LAND[1], u)
    z = lerp(BED_EDGE[2], 0.0, u) + 1.1 * 4 * u * (1 - u)
    return x, y, z


def run_path(g):
    """after the landing he skips round a small loop on the sunny floor."""
    t = (g - G_RUN) / 30.0
    ang = t * 2.1
    x = LAND[0] + 0.9 * math.sin(ang) + 0.35 * t
    y = LAND[1] + 0.55 * (1 - math.cos(ang)) * 0.6 - 0.2 * t
    dx = 0.9 * 2.1 * math.cos(ang) + 0.35
    return x, y, dx


def pose_lie(g):
    p = dict(cast11.STORY11["james_in_bed"][1])
    wake = u_of(g, 905, 920)
    p.update(lie=-90, head_roll=-72 + 3.0 * math.sin(g * 0.15), pitch=0.12 * math.sin(g * 0.2), flush=lerp(0.8, 0.0, u_of(g, 892, 912)), sweat=0.0,
             expr="neutral" if g < 912 else "happy", t=g / 30.0)
    p["mouth"] = "smile" if g >= 912 else None
    if p["mouth"] is None:
        del p["mouth"]
    p["arm_r"] = dict(hand=(0.18 - 0.1 * wake, 0.9 - 0.25 * wake), bend=0.6)
    p["blink"] = blink(g, [904, 916])
    return p


def pose_stand(g):
    if g < G_LEAP[0] + 2:                                    # on the bed edge: arms thrown up as he springs
        p = dict(cast11.STORY11["james_jump_up"][1])
        p.update(legs=dict(preset="wide", crouch=0.35))
    elif g < G_LEAP[1]:
        p = dict(cast11.STORY11["james_jump_up"][1])
        p["squash"] = [0.97, 1.05]
    else:
        p = dict(cast11.STORY11["james_play"][1])
        ph = (g - G_RUN) / 14.0
        run = cast11.cycle("james", (g - G_RUN) / 18.0, "run", 1)
        _, _, dx = run_path(g)
        p = dict(run)
        p["yaw"] = 0.75 if dx > 0 else -0.75
        if dx < 0:
            p["mirror"] = True
        p["expr"] = "grinning"
    p["t"] = g / 30.0
    p["flush"] = 0.0
    p["blink"] = blink(g, [930, 960])
    return p


def pose_mom(g):
    p = dict(cast11.STORY11["mother_sit_relieved"][1])
    p.update(mirror=True, head_roll=4 + 1.5 * math.sin(g * 0.07), lean=1.0 * math.sin(g * 0.05), t=g / 30.0)
    gz = 1.0 if g < G_LEAP[0] else 0.0
    p["gaze"] = [0.7, 0.2]
    p["blink"] = blink(g, [910, 944, 975])
    return p


def pose_jen(g):
    p = dict(cast11.STORY11["jenner_proud"][1])
    k = math.sin(g * 0.12)
    p.update(mirror=True, head_roll=-3 + 1.5 * k, lean=1.2 * math.sin(g * 0.06), t=g / 30.0)
    p["blink"] = blink(g, [905, 949])
    return p


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s15")
        sd = os.path.join(TMP, "sprites")
        self.jb = self.actors["jb"] = C.make_actor("jb", "james", sd, canvas=cast11.CANVAS11_LIE["james"])
        self.jm = self.actors["jm"] = C.make_actor("jm", "james", sd + "_m")
        self.mom = self.actors["mom"] = C.make_actor("mom", "mother", sd)
        self.jen = self.actors["jen"] = C.make_actor("jen", "jenner", sd)

    def pose(self, shot, gs):
        lie_f, std_f = [], []
        for g in gs:
            f = bf(shot, g)
            loc, look = cam_of(g)
            self.key_cam(f, loc, look)
            lying = g < G_SIT
            C.key_hidden(self.jb, f, not lying)
            C.key_hidden(self.jm, f, lying)
            C.place(self.jb, f, BED, z=BED_Z, scale=C.SCALE["james"])
            if lying:
                C.place(self.jm, f, BED_EDGE[:2], z=BED_EDGE[2], scale=C.SCALE["james"])
                lie_f.append(g)
            else:
                if g < G_LEAP[1]:
                    x, y, z = jump_state(g)
                else:
                    x, y, _ = run_path(g)
                    z = 0.0
                    if g < G_LEAP[1] + 4:                       # landing squash
                        pass
                C.place(self.jm, f, (x, y), z=z, scale=C.SCALE["james"])
                std_f.append(g)
            C.place(self.mom, f, MOM, scale=C.SCALE["mother"])
            C.place(self.jen, f, JEN, scale=C.SCALE["jenner"])
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            if g < G_SIT:
                self.jb.pose(f, pose_lie(g), camera=self.cam)
            else:
                self.jm.pose(f, pose_stand(g), camera=self.cam)
            self.mom.pose(f, pose_mom(g), camera=self.cam)
            self.jen.pose(f, pose_jen(g), camera=self.cam)
        fb = [bf(shot, g) for g in gs if g < G_SIT]
        fm = [bf(shot, g) for g in gs if g >= G_SIT]
        if fb:
            self.sprites_for([(self.jb, 192)], fb, overlays={"jb": lie_overlay})
        if fm:
            self.sprites_for([(self.jm, 192)], fm, overlays={"jm": stand_overlay})
        self.sprites_for([(self.mom, 192), (self.jen, 192)], [bf(shot, g) for g in gs])

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look = cam_of(g)
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], heads=C.head_report(self, f))

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    if cmd in ("probe", "stills"):
        Tk = Take("preview")
        for shot in shots:
            gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
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
        C.final_loop(lambda q: Take(q), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
