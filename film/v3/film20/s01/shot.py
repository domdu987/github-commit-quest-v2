#!/usr/bin/env python3
"""shot.py -- film 20 take s01 = shot 1, THE HOOK (g 0..79 + 4 out-handle frames g 80..83; hard cut to shot 2 at g 80).
"นักเขียนคนนี้ เกลียดหอคอย ต้นหนึ่ง ที่สุดในโลก" -- this writer hated one tower more than anything in the world.

TOWER tower_low / DAY 1889.  Maupassant stands in the foreground on the Champ de Mars (mark maupassant_low), arms crossed; the
FINISHED tower fills the sky behind him; lamp-post (left) + bench (right) foreground from the preset.
    g  0..25  he sneers up at the tower (expr sneer, gaze up-right, chin up); the camera is already moving: push + slide + tilt up
    g 25..40  SNAP push x1.45 + extra tilt-up on "เกลียดหอคอย" (event g 27); the face swaps sneer -> disgust on the CLOSED frame of a
              3-frame blink (g 26 half, g 27 closed = swap, g 28 half)
    g 45..53  "ต้นหนึ่ง" (event g 47): he turns his nose away -- yaw +0.30 -> -0.85 (faces screen-left), chin up, eyes squeezed
              shut (expr avoid; the swap rides on the head turn at g 48)
    g 61..66  "ที่สุดในโลก" (event g 61): a small "hmph" chin jerk (pitch bump), still turned away
    g 66..83  he holds the snub with an idle sway; the camera keeps tilting up to the second platform and the spire (cut at g 80)
Mouths: no quote in this shot -> expression mouths only (smirk / frown), never animated.  NO depth of field, NO text.

The camera (c20.CamPath): the preset pose lowered from 1.0 m to 0.35 m (his head rides higher in frame, so there is room to tilt
up the tower and still keep his head centre in 450-760); push 8 %/s toward his head + slide 30 px/s + arc + tilt up 4.5 deg/s,
decay 0.3 (moving on frame 0 and on the last frame), plus the snap.

    python3 shot.py probe a:b[:step]                       numbers only (camera, heads), no render
    python3 shot.py camreport                              CamPath corner speed per frame (never parked check), no scene build
    python3 shot.py stills a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final a:b[:step] [scale] [samples]     -> raw/g_%04d.png + .json (resumable; run 2 processes, e.g. 0:83:2 / 1:83:2)
    python3 shot.py final 0:83:2 0.5 4                     DRAFT (360x640, 4 spp) -> work/draft/ (same loop)
    python3 shot.py hue g [g ...]                          render final frames and measure the cast-shadow hue (hue20)
    python3 deliver.py                                     -> frames/, take.mkv, meta.json, cues.json, contact.jpg, framediff, QA_AUTO
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c20 as C                                          # noqa: E402  (paths, cast20 first, bpy, set3d20, stage)
from mathutils import Vector                             # noqa: E402

S, CO, actors, cast20 = C.S, C.CO, C.actors, C.cast20
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

# ----------------------------------------------------------------------------- timing (film frames g)
G0, G1 = C.g_bound(0.00), C.g_bound(2.67)     # 0, 80: shot 1 = g 0..79; shot 2 (hard cut, RESTO) starts at g 80
H_OUT = 4                                      # out-handle g 80..83 (cut side: 4 frames, rendered in 3D, the move continues)
G_LAST = G1 + H_OUT - 1                        # 83
GS = list(range(G0, G_LAST + 1))
G_HATE = C.cap_g("เกลียดหอคอย")                 # 27: "hates the tower" -> snap + face swap sneer -> disgust
G_ONE = C.cap_g("ต้นหนึ่ง")                     # 47: "one (tower)" -> he turns his nose away
G_MOST = C.cap_g("ที่สุดในโลก")                  # 61: "most in the world" -> hmph chin jerk
SNAP = (G_HATE - 2, G_HATE + 13)               # 25..40 (15 frames)
G_SWAP = G_HATE                                # closed frame of the blink 26..28
TURN = (G_ONE - 2, G_ONE + 6)                  # 45..53 yaw turn
G_AVOID = G_ONE + 1                            # 48: expression -> avoid (eyes squeezed) mid-turn
HMPH = (G_MOST, G_MOST + 5)                    # 61..66 chin jerk
BLINKS = [11, G_SWAP - 1]                      # blink(g, starts): half, closed, half

# ----------------------------------------------------------------------------- staging (world D; set3d20 marks / cams are already D)
LIGHT = "DAY"
PRESET = "tower_low"
MARK = "maupassant_low"
HEAD_Z = 2.6                                   # head centre above the feet (3.1 D figure, head 1 D)
PPD = 256                                      # sprite px per D (head 120 -> ~210 px on screen)
CANVAS = (-1.75, -4.25, 1.75, 0.1875)          # taller than CANVAS20['maupassant'] (top -3.5625): low-angle upper_k stretch
CAM_DROP = 1.22                                # lower the preset camera by 1.22 D (1.0 m -> 0.35 m above the ground)
CAM_BACK = -1.6                                # D further back along the view: -1.6 = 1.6 D CLOSER (5.0 D from his head instead of
                                               # the preset 6.6 D: he fills the lower frame, so the aim can pitch up into the tower)
TILT0 = -19.0                                  # aim pitched 19 deg BELOW the lens -> head line (pitch ~ +2 deg on frame 0: head y ~475)


def cam_path(A):
    """the CamPath from the preset camera: same x/y, lowered; subject = his head centre.  A function: A only exists after build."""
    m = Vector(A["marks"][MARK])
    subj = m + Vector((0.0, 0.0, HEAD_Z))
    c = Vector(A["cams"][PRESET]["loc"]) - Vector((0.0, 0.0, CAM_DROP))
    c = c + (c - subj).normalized() * CAM_BACK
    return C.CamPath(c, subj, G0, G_LAST, push=0.08, slide_px=30.0, rise_px=0.0, arc_deg_s=3.0, tilt0=TILT0, tilt_deg_s=4.5,
                     decay=0.2, snaps=[dict(g=SNAP, k=1.35, peak=1.7, shift=(-0.25, 0.0), tilt=6.0)])


def move_fg(A, cam_loc):
    """the preset FG (lamp-post + bench: objects fg_*, and the invisible shade casters over the near ground) is built relative to
    the PRESET camera (tower20._fg / _shade).  Our camera starts elsewhere, so move them by the same ground offset: the lamp-post
    stays 1.2 m (2.3 D) ahead-left of the lens and the bench 2 m ahead-right.  Objects are children of the scaled root (metres)."""
    d = Vector(cam_loc) - Vector(A["cams"][PRESET]["loc"])
    d.z = 0.0
    for ob in C.bpy.data.objects:
        if ob.name.startswith(("fg_", "shade_casters")):
            ob.location = ob.location + d / CO.SC


def cam_path_static():
    """CamPath without building the set (camreport): the preset numbers from tower20 in metres -> D."""
    import tower20
    cam = tower20.CAMS_M[PRESET]
    A = dict(marks={MARK: CO.W((-6.8, -116.5, 0.0))}, cams={PRESET: dict(loc=CO.W(cam["loc"]))})   # tower20._marks, metres -> D
    return cam_path(A)


# ----------------------------------------------------------------------------- poses (cast20 STORY20: arms folded as in maupassant_turn_away)
TURN_AWAY = cast20.STORY20["maupassant_turn_away"][1]
C.add_expression("disgust20", eyes="half", tilt=8.0, brows=("both", 0.105, 20.0, 0.050, 0.18, 0.012), mouth="frown", mouth_dy=0.02)


def pose_of(g):
    """the drawn pose of frame g (no pinned hands: arms folded the whole shot)."""
    p = dict(arm_r=TURN_AWAY["arm_r"], arm_l=TURN_AWAY["arm_l"], legs="wide", mouth=None)
    u = u_of(g, *TURN)                                                  # 0 = facing us three-quarter right, 1 = nose away left
    p["yaw"] = lerp(0.30, -0.85, u)
    hm = math.sin(math.pi * clamp((g - HMPH[0]) / float(HMPH[1] - HMPH[0])))      # 0 -> 1 -> 0 over HMPH
    if g < G_SWAP:
        p["expr"], p["head_roll"], p["pitch"] = "sneer", 6.0, -0.30
        p["gaze"] = (0.6, -0.9)                                         # up-right at the tower behind him
    elif g < G_AVOID:
        p["expr"], p["head_roll"], p["pitch"] = "disgust20", -3.0, -0.18
        p["gaze"] = (0.5, -0.7)
    else:
        p["expr"], p["head_roll"] = "avoid", lerp(-3.0, -6.0, u)
        p["pitch"] = -0.30 - 0.12 * u - 0.25 * hm                        # chin up, plus the hmph jerk
    p.pop("mouth")
    p["lean"] = lerp(0.0, -4.0, u) + 1.3 * math.sin(g * 0.19)          # leans back as he turns away + idle sway
    p["head_roll"] += 1.8 * math.sin(g * 0.15 + 0.6) + 4.0 * hm
    p["squash"] = (1.0, 1.0 + 0.008 * math.sin(g * 0.26))               # breathing
    p["blink"] = blink(g, BLINKS) if g < G_AVOID else 0
    p["t"] = g / 30.0
    return p


# ----------------------------------------------------------------------------- the take
class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s01")
        self.path = cam_path(self.A)
        move_fg(self.A, self.path.loc0)
        self.key_cam(bf(G0), *self.path.at(G0))
        self.scene.frame_set(bf(G0))
        self.mau = self.actors["mau"] = C.make_actor("mau", "maupassant", os.path.join(WORK, "sprites"), canvas=CANVAS,
                                                     contact=dict(width=1.3, depth=0.55, opacity=0.8), cam=self.cam)

    def pose(self, gs):
        mark = self.A["marks"][MARK]
        for g in gs:
            f = bf(g)
            self.key_cam(f, *self.path.at(g))
            C.place(self.mau, f, mark)
            self.key_set(f, set_year=1889, set_crowd=1)               # the preset state, keyed on every frame
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.mau.pose(f, pose_of(g), camera=self.cam)
        self.sprites_for([(self.mau, PPD)], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = self.path.at(g)
        v = look - loc
        tower = {k: CO.project(CO.W(p)) for k, p in (("platform2", (0, 0, 115.0)), ("summit", (0, 0, 300.0)))}
        return dict(g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    heads=C.head_report(self, f), upper_k=round(self.mau.upper_k.get(f, 1.0), 3), tower_px=tower)

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        P = cam_path_static()
        rows, worst = P.report(GS[:-1])
        for r in rows:
            print(r)
        print("longest run under 0.25 px/frame: %d frames (bible max 6)" % worst)
        sys.exit(0)
    if cmd == "hue":
        gs = [int(v) for v in sys.argv[2:]]
        Tk = Take("final")
        Tk.pose(gs)
        out = os.path.join(WORK, "hue")
        for g in gs:
            st = Tk.render([g], out)[0]
            print(g, json.dumps(C.hue_frame(st["path"])), flush=True)
        sys.exit(0)
    gs = [g for g in C.parse(sys.argv[2]) if G0 <= g <= G_LAST]
    if cmd in ("probe", "stills"):
        Tk = Take("preview")
        Tk.pose(gs)
        for g in gs:
            print(json.dumps(Tk.report(g)), flush=True)
            if cmd == "stills":
                out = sys.argv[3]
                scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
                samples = int(sys.argv[5]) if len(sys.argv) > 5 else 4
                st = Tk.render([g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
                print("g %d  %.1f s wall %.1f cpu" % (g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else CO.FINAL_SPP
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")       # drafts never mix with finals
        C.final_loop(lambda: Take("final" if scale >= 1.0 else "preview"), gs, out, scale=scale, samples=samples)
