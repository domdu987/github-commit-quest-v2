#!/usr/bin/env python3
"""shot.py -- film 3 take s06: shots 6 and 7, harbor set WINTER (engine: take3.py, same folder).

    shot 6  g 422..541  base_eye: tommy, smallest among the dock workers at the foot of the tank ("dek fuek ngan ... noi thi sut");
                        snap reframe g 471..483 onto tommy (lands on "tae khao dai yin" 15.8 s = g 477); he cups a hand behind the
                        ear toward the tank (tommy_listen); the tank groans (camera jolts g 492, 519), slow push in.
                        In-handle g 415..421 (10-frame dissolve in from shot 5).
    shot 7  g 542..619  seam_insert: molasses seeping out of the riveted seam (set_seep 0.35 -> 1), glossy elongated drops form and
                        fall into the bucket; 9-frame dissolve 6 -> 7 mixed g 538..546 (raw: shot 6 to g 548, shot 7 from g 536).
                        Hard cut out to shot 8 (no out-handle).

    python3 shot.py probe|stills|final <6|7> <a:b[:step]|all> [out_dir] [scale] [samples]
"""
import math, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import take3 as X                                      # noqa: E402
from take3 import W, g_of, kcam, shake, keys, ease, blink, pulse, lerp, clamp, H, Vector   # noqa: E402
import puppet                                          # noqa: E402
import cast3                                           # noqa: E402

G6, G7, G8 = 422, 542, 620
H_IN = 7
D67 = 9
M0 = G7 - D67 // 2                                     # 538: first mixed frame
RNG = {6: (G6 - H_IN, M0 + D67 + 1), 7: (M0 - 2, G8 - 1)}
REFRAME = g_of(15.8)                                   # 477
SNAP = (REFRAME - 6, REFRAME + 6)
GROANS = [g_of(16.3), g_of(17.2)]                      # 492, 519
TOMMY6 = W(-1.1, 1.5)
W2_6 = W(1.7, 2.3)                                     # worker2 (beard, wrench), right of tommy, nearer
W1_6 = W(-3.4, 2.6)                                    # worker1 (lanky), left, behind
HEAD6 = Vector((TOMMY6.x, TOMMY6.y, 1.95))


def cam6(g):
    hx, hy = TOMMY6.x, TOMMY6.y
    ks = [(RNG[6][0], (9.4, -10.0, -4.0, hx + 0.9, hy + 0.9, 2.45), "sine"),
          (448, (8.8, -13.5, -3.0, hx + 0.75, hy + 0.7, 2.35), "sine"),
          (SNAP[0], (8.6, -14.5, -3.0, hx + 0.7, hy + 0.65, 2.32), "quint"),
          (SNAP[1], (4.3, -14.0, 1.0, hx + 0.32, hy + 0.12, 2.02), "sine"),
          (505, (3.95, -12.0, 3.0, hx + 0.30, hy + 0.10, 2.05), "sine"),
          (RNG[6][1], (3.55, -9.0, 6.0, hx + 0.32, hy + 0.12, 2.15), "hold")]
    loc, look = kcam(g, ks, 0.18)
    dx, dz = shake(g, GROANS, 0.035)
    look = look + Vector((dx, 0, dz))
    return loc, look


SEAM = W(0.0, 0.0, 2.3)


def cam7(g):
    sx, sy = SEAM.x, SEAM.y
    ks = [(RNG[7][0], (3.05, 0.0, -4.0, sx, sy, 2.55), "sine"),
          (566, (2.75, 3.0, -6.0, sx, sy, 2.35), "cubic"),
          (590, (2.6, 6.0, -14.0, sx, sy, 1.55), "sine"),
          (RNG[7][1], (2.45, 8.0, -16.0, sx, sy, 1.40), "hold")]
    return kcam(g, ks, 0.18)


# ----------------------------------------------------------------------------- poses
def tommy6(g):
    small = dict(yaw=0.35, pitch=-0.5, expr="worried", head_roll=4, gaze=(0.6, -0.8), arm_r=dict(hand=(0.30, 0.98), bend=0.6),
                 arm_l=dict(hand=(-0.28, 0.98), bend=0.6), legs="narrow")
    lis = dict(cast3.STORY3["tommy_listen"][1])
    u = ease((g - (REFRAME + 1)) / 8.0, "cubic")
    p = puppet.lerp_pose("tommy", small, lis, u) if 0 < u < 1 else (lis if u >= 1 else small)
    p = dict(p)
    p["blink"] = blink(g, [431, REFRAME + 4, 530])
    if g < REFRAME + 4:
        p["expr"] = "worried"
    for s in GROANS:                                   # winces at each groan: head tilts further toward the tank
        p["head_roll"] = p.get("head_roll", 0) - 6 * pulse(g, s, s + 4, s + 16, 1.0)
    p["squash"] = (1.0 - 0.02 * sum(pulse(g, s, s + 3, s + 12, 1.0) for s in GROANS), 1.0 + 0.02 * sum(pulse(g, s, s + 3, s + 12, 1.0) for s in GROANS))
    return p, None


def worker2_6(g):
    p = dict(cast3.STORY3["worker_wrench"][1])
    p["yaw"] = -0.45
    p["head_roll"] = -4 + 2 * math.sin(g * 0.09)
    p["blink"] = blink(g, [440, 500])
    p["lean"] = 1.5 * math.sin(g * 0.07)
    return p, None


def worker1_6(g):
    p = dict(yaw=0.4, pitch=-0.1, expr="unimpressed", head_roll=5 + 2 * math.sin(g * 0.08 + 1), arm_l="akimbo",
             arm_r=dict(hand=(0.30, 0.95), bend=0.6), legs="stand", blink=blink(g, [452, 512]))
    return p, None


# ----------------------------------------------------------------------------- shot 7 state
def state6(g):
    return dict(paint=0.0, seep=0.75, bucket=(H.BUCKET_MARK, 0.5, True, None))


def state7(g):
    a = 0.35 + 0.65 * ease((g - RNG[7][0]) / float(600 - RNG[7][0]), "sine")
    return dict(paint=0.0, seep=a, bucket=(H.BUCKET_MARK, 0.5 + 0.06 * clamp((g - 560) / 60.0), True, None))


DROPS7 = [dict(key="d0", strip=0, period=24, form=15, phase=3, floor=0.62, size=1.6),
          dict(key="d1", strip=1, period=33, form=20, phase=17, floor=0.02, size=1.2),
          dict(key="d2", strip=2, period=41, form=26, phase=8, floor=0.02, size=1.1)]
DROPS6 = [dict(key="d0", strip=0, period=24, form=15, phase=3, floor=0.62, size=1.15)]


def build_fg(tk):
    """shot 6: two barrels in shade at the near-left edge; shot 7: a shaded barrel edge at the lower left"""
    M = tk.M
    loc, look = cam6(RNG[6][0])
    f = (look - loc); f.z = 0; f.normalize(); r = Vector((f.y, -f.x, 0))
    a = loc + f * 3.4 - r * 1.75; b = loc + f * 4.4 - r * 1.15
    obs6 = X.barrel("s6_barrel_a", (a.x, a.y, 0.0), tk.coll, M) + X.barrel("s6_barrel_b", (b.x, b.y, 0.0), tk.coll, M)
    loc, look = cam7(RNG[7][0])
    f = (look - loc); f.z = 0; f.normalize(); r = Vector((f.y, -f.x, 0))
    p = loc + f * 1.05 - r * 0.78
    obs7 = [X._box("s7_post", (p.x - 0.17, p.y - 0.17, 0.0), (p.x + 0.17, p.y + 0.17, 6.0), M["wood"], tk.coll)]
    q = loc + f * 1.5 - r * 0.55
    obs7 += X.barrel("s7_barrel", (q.x, q.y, 0.0), tk.coll, M)
    for o in obs7:
        o.visible_shadow = False
    return {"fg6": obs6, "fg7": obs7}


SHOTS = {
    6: dict(rng=RNG[6], cam=cam6, state=state6, fg=("fg6",), drops=DROPS6,
            actors={"tommy": dict(cast="tommy", place=lambda g: TOMMY6, pose=tommy6, ppd=384),
                    "worker2": dict(cast="worker2", place=lambda g: W2_6, pose=worker2_6, ppd=256),
                    "worker1": dict(cast="worker1", place=lambda g: W1_6, pose=worker1_6, ppd=192)},
            marks={"bucket": W(0, 0.47, 0.7)}),
    7: dict(rng=RNG[7], cam=cam7, state=state7, fg=("fg7",), drops=DROPS7, actors={}, marks={"seam": SEAM}),
}

if __name__ == "__main__":
    X.main(SHOTS, build_fg, "s06")
