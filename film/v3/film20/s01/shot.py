#!/usr/bin/env python3
"""shot.py -- film 20 take s01 = shot 1, THE HOOK (g 0..79 + 4 out-handle frames g 80..83; hard cut to shot 2 at g 80).
"นักเขียนคนนี้ เกลียดหอคอย ต้นหนึ่ง ที่สุดในโลก" -- this writer hated one tower more than anything in the world.

TOWER tower_low / DAY 1889, staged 50 m further down the avenue than the preset (see STAGE_DY_M).  Maupassant stands in the
foreground on the Champ de Mars, arms crossed; the WHOLE finished tower (spire in frame from g 0) fills the sky behind him;
lamp-post (left edge) + bench (lower right) foreground, kiosks / flags / crowd cards in the lower third.
    g  0..25  he sneers up at the tower (expr sneer, gaze up-right, chin up); the camera is already moving: push + slide + arc + tilt
    g 25..40  SNAP push x1.4 + orbit 18 deg + tilt 2 deg on "เกลียดหอคอย" (event g 27): the tower whips sideways behind him; the face
              swaps sneer -> disgust on the CLOSED frame of a 3-frame blink (g 26 half, g 27 closed = swap, g 28 half)
    g 45..53  "ต้นหนึ่ง" (event g 47): he turns his nose away -- yaw +0.30 -> -0.85 (faces screen-left), chin up, eyes squeezed
              shut (expr avoid; the swap rides on the head turn at g 48)
    g 61..66  "ที่สุดในโลก" (event g 61): a small "hmph" chin jerk (pitch bump), still turned away
    g 66..83  he holds the snub with an idle sway; the camera keeps pushing, orbiting and tilting (cut at g 80)
Mouths: no quote in this shot -> expression mouths only (smirk / frown), never animated.  NO depth of field, NO text.

The camera (c20.CamPath): 0.16 m above the gravel path, 5.2 D in front of him, lens shift -0.12 (preset +0.08), pitch 32 -> 39
deg; push 8 %/s toward his head + slide 45 px/s + orbit 8 deg/s + tilt 2 deg/s, decay 0.1 (moving on frame 0 and the last
frame), plus the snap.  The numbers were solved for: summit y >= 30 from g 0, head centre 585-720, horizon ~y 970 (ground
<= 25 %), then tuned on drafts for the frame-diff target (QA.md).

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
SNAP = (G_HATE - 2, G_HATE + 13)               # 25..40 (15 frames; 13 gave FEWER high frame-diff pairs: p90 fell 12.3 -> 11.9)
G_SWAP = G_HATE                                # closed frame of the blink 26..28
TURN = (G_ONE - 2, G_ONE + 6)                  # 45..53 yaw turn
G_AVOID = G_ONE + 1                            # 48: expression -> avoid (eyes squeezed) mid-turn
HMPH = (G_MOST, G_MOST + 5)                    # 61..66 chin jerk
SELL_END = 60                                  # the F3 turn accent (head roll / chin / gaze) holds to g 60, eases out by g 64
BLINKS = [11, G_SWAP - 1]                      # blink(g, starts): half, closed, half

# ----------------------------------------------------------------------------- staging (world D; set3d20 marks / cams are already D)
LIGHT = "DAY"
PRESET = "tower_low"
MARK = "maupassant_low"
HEAD_Z = 2.6                                   # head centre above the feet (3.1 D figure, head 1 D)
PPD = 256                                      # sprite px per D (head 120 -> ~210 px on screen)
CANVAS = (-1.75, -4.25, 1.75, 0.1875)          # taller than CANVAS20['maupassant'] (top -3.5625): low-angle upper_k stretch
STAGE_DY_M = -50.0                             # the whole staging (his mark, the camera, the preset FG and crowd cards) moves 50 m
                                               # back down the avenue (y -116.5 -> -166.5 m): from 120 m the summit sits 68 deg up
                                               # and cannot share a 22 mm frame with his head in the 450-760 band; from 170 m it is
                                               # 60.5 deg up and the WHOLE tower fits above him from frame 0 (director note)
STAGE_DX_M = 2.0                               # and 2 m toward the avenue centre (x -6.8 -> -4.8 m): the shaded kiosk awnings on the
                                               # left (x -11.6 m) otherwise fill the left edge as a black slab
CAM_H = 0.30                                   # lens height above the path, D (0.16 m): low angle
CAM_DIST = 5.2                                 # horizontal distance lens -> his feet at g 0, D
CAM_X = -0.38                                  # lens x offset from his mark, D (the preset camera is 0.2 m left of the mark)
SHIFT = -0.12                                  # lens shift_y (preset +0.08): negative = optical centre ABOVE the frame centre, so
                                               # the summit and his head (40 deg apart) both fit; verticals stay as the pitch sets them
TILT0 = 8.0                                    # aim pitched 8 deg ABOVE the lens -> head line on frame 0 (pitch ~32 deg)
TILT_RATE = 2.0                                # deg/s drift tilt-up (the push raises the head line, so his head stays in band)
SNAP_TILT = 2.0                                # extra tilt in the snap
ARC0, ARC_RATE, SNAP_ARC = -13.0, 8.0, 22.0    # orbit round his head (deg, deg/s, deg in the snap): the far tower slides behind
                                               # him; it carries the frame-diff (tilt alone gave median 3.2 / p90 6.3 on the draft)
SLIDE = 45.0                                   # px/s lateral slide
SNAP_K = 1.5                                   # snap framing factor
FG_ANCHOR = G_LAST                             # the preset FG is placed relative to the lens at THIS frame.  Anchored at g 0 the
                                               # push + arc drove the lens THROUGH the bench at g 53-64 (frame-diff pop 50.9);
                                               # anchored at the end (+ LAMP_AT / BENCH_AT) both stay clear of the lens and of him


def delta():
    """the staging offset in world D (STAGE_DY_M metres along y)."""
    return Vector(CO.W((STAGE_DX_M, STAGE_DY_M, 0.0)))


def cam_path(A):
    """the CamPath: lens CAM_DIST D in front of his (moved, ground-snapped) mark, CAM_H D above the path; subject = his head
    centre.  A function: A only exists after build (or comes from cam_path_static)."""
    m = Vector(A["marks"][MARK])
    subj = m + Vector((0.0, 0.0, HEAD_Z))
    c = Vector((m.x + CAM_X, m.y - CAM_DIST, m.z + CAM_H))
    return C.CamPath(c, subj, G0, G_LAST, push=0.08, slide_px=SLIDE, rise_px=0.0, arc_deg_s=ARC_RATE, arc0=ARC0, tilt0=TILT0,
                     tilt_deg_s=TILT_RATE, decay=0.1,
                     snaps=[dict(g=SNAP, k=SNAP_K, peak=1.7, shift=(-0.25, 0.0), tilt=SNAP_TILT, arc=SNAP_ARC)])


BENCH_AT = (2.0, 2.0)                          # bench (m ahead, m right of the lens at FG_ANCHOR): lower right, only its end shows
                                               # (QA-art F2: at 1.1 m right it read as a black slab; the preset shade casters keep it
                                               # in shade, so it is pushed out until only its end shows)
LAMP_X, LAMP_BASE_Y = 40.0, 1045.0             # our own lamp-post (QA-art F1): base on the path at screen (40, 1045) on g 0 =
                                               # 4.9 D from the lens, lantern at y ~83; centre line leaves frame left by g 25-30
LAMP_H_M = 3.6                                 # pole height, metres (kit20.lamppost default)
LAMP_HIDE = 41                                 # hidden from this g on (it leaves frame left with the snap g 25-40)


def _ground_basis(loc, look):
    f, r, _u = C._cam_basis(loc, look)
    return Vector((f.x, f.y, 0.0)).normalized(), Vector((r.x, r.y, 0.0)).normalized()


def move_set_dressing(A, cam):
    """the preset FG is built relative to the PRESET camera (tower20._fg): lamp-post 1.2 m ahead / 0.46 m left, bench 2 m ahead /
    1.1 m right, merged into one mesh per material (fg_dark_sh, fg_timber_sh, fg_lamp: children of the scaled root, metres).
    We split the vertices by distance to the preset lamp spot: the preset lamp-post (an unlit near-black pole, QA-art F1) is
    sunk 200 m under the ground (build_lamp makes ours); the bench moves to BENCH_AT of our lens at FG_ANCHOR (cam = (loc, look)
    of that frame) and gets the plain lit timber instead of the shade variant (QA-art F2).  The invisible near-ground shade
    casters move with the lens.  The 8 crowd cards (crowd_*, world D) move with the staging (delta())."""
    import tower20
    pc = tower20.CAMS_M[PRESET]
    pl = Vector(pc["loc"]); pl.z = 0.0
    f0, r0 = _ground_basis(Vector(pc["loc"]), Vector(pc["look"]))
    old_lamp, old_bench = pl + f0 * 1.2 + r0 * -0.46, pl + f0 * 2.0 + r0 * 1.1          # metres (tower20.FG_ITEMS)
    cl = Vector(cam[0]) / CO.SC
    cl.z = 0.0
    f1, r1 = _ground_basis(*cam)
    d_sink = Vector((0.0, 0.0, -200.0))
    d_bench = cl + f1 * BENCH_AT[0] + r1 * BENCH_AT[1] - old_bench
    M = CO.STATE["M"]
    for ob in C.bpy.data.objects:
        if ob.name.startswith("fg_"):
            for v in ob.data.vertices:
                q = Vector((v.co.x, v.co.y, 0.0))
                v.co = v.co + (d_sink if (q - old_lamp).length < 0.8 else d_bench)
            ob.data.update()
            if ob.name.startswith("fg_timber"):                          # bench planks: lit wood, not the blue shade variant
                for slot in ob.material_slots:
                    slot.material = M["timber"]
        elif ob.name.startswith("shade_casters"):
            ob.location = ob.location + (cl - pl)
        elif ob.name.startswith("crowd_") and ob.parent is None:
            ob.location = ob.location + delta()


def lamp_geometry(cam, ground):
    """(base point, unit pole direction) of our lamp-post: base on the path where the g-0 ray through (LAMP_X, LAMP_BASE_Y) hits
    it; the pole lies in the plane of the camera and that image COLUMN, as close to world-vertical as that plane allows, so it
    stands UPRIGHT in frame (QA-art F1) instead of slanting with the 32-deg pitch (a true vertical at the frame edge leans
    ~12 deg on screen).  The lean in 3D is that same small angle, toward the lens: invisible from this camera."""
    loc, look = Vector(cam[0]), Vector(cam[1])
    f, r, u = C._cam_basis(loc, look)
    cy = 640.0 + SHIFT * 1280.0

    def ray(px, py):
        return (f + r * ((px - 360.0) / C.F_PX) + u * ((cy - py) / C.F_PX)).normalized()
    rb = ray(LAMP_X, LAMP_BASE_Y)
    base = loc + rb * ((ground - loc.z) / rb.z)
    n = rb.cross(ray(LAMP_X, 0.0)).normalized()                        # normal of the column plane
    z = Vector((0.0, 0.0, 1.0))
    d = (z - n * n.dot(z)).normalized()
    return base, d


def build_lamp(cam, ground):
    """our lamp-post (QA-art F1): dark-green iron pole + base + lit lantern head (warm emitter) + finial, built in D at the origin
    along +z and turned onto lamp_geometry().  The set palette has no green iron: 'iron_green20' is made here (runtime dressing)."""
    base, d = lamp_geometry(cam, ground)
    M = CO.STATE["M"]
    green = CO.mat("iron_green20", "#24402f", "#34583f", 3.0, rough=0.55)
    glow = CO.mat_emit("lantern20", "#ffd28a", 7.0)
    S, h = CO.SC, LAMP_H_M * CO.SC
    mb = CO.MB("s01_lamp")
    mb.rod(green, (0, 0, 0), (0, 0, h), 0.06 * S, 0.045 * S, 8)
    mb.cyl(green, (0, 0, 0.25 * S), 0.12 * S, 0.5 * S, "z", 10)
    mb.box(green, (0, 0, h + 0.04 * S), (0.30 * S, 0.30 * S, 0.06 * S))
    mb.ell(glow, (0, 0, h + 0.28 * S), (0.17 * S, 0.17 * S, 0.24 * S), (10, 8))
    mb.box(green, (0, 0, h + 0.54 * S), (0.36 * S, 0.36 * S, 0.05 * S))
    mb.rod(green, (0, 0, h + 0.56 * S), (0, 0, h + 0.78 * S), 0.07 * S, 0.01 * S, 6)
    obs = mb.finish()
    rot = Vector((0.0, 0.0, 1.0)).rotation_difference(d)
    for ob in obs:
        ob.rotation_mode = "QUATERNION"
        ob.rotation_quaternion = rot
        ob.location = base
    return obs


def cam_path_static():
    """CamPath without building the set (camreport / solve): mark in metres -> D, moved, on the gravel path (z 0.113 D)."""
    A = dict(marks={MARK: tuple(Vector(CO.W((-6.8, -116.5, 0.0))) + delta() + Vector((0, 0, 0.113)))})
    return cam_path(A)


def project(loc, look, p):
    """pure-math projection (x, y px at 720x1280) of world point p for a camera (loc, look) with lens shift SHIFT: the same
    as Blender's for sensor fit AUTO on a portrait frame (shift is in units of the larger dimension, 1280)."""
    f, r, u = C._cam_basis(loc, look)
    d = Vector(p) - Vector(loc)
    z = d.dot(f)
    return (360.0 + C.F_PX * d.dot(r) / z, 640.0 + SHIFT * 1280.0 - C.F_PX * d.dot(u) / z)


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
    # QA-art F3: sell the turn on the flat card (g 45-60): head roll -10 deg, chin up 0.15 more, gaze hard right, eased in with the
    # turn and out over g 60-64 (the hmph at g 61-66 stays on top)
    sell = u * (1.0 - u_of(g, SELL_END, SELL_END + 4))
    p["head_roll"] = p["head_roll"] - 10.0 * sell
    p["pitch"] = p["pitch"] - 0.15 * sell
    if sell > 0.0:
        p["gaze"] = (0.9 * sell, -0.3 * sell)
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
        self.A["marks"][MARK] = C.on_ground(Vector(self.A["marks"][MARK]) + delta())   # moved; the gravel path is 0.113 D up
        self.cam.data.shift_y = SHIFT
        self.path = cam_path(self.A)
        move_set_dressing(self.A, self.path.at(FG_ANCHOR))
        self.lamp = build_lamp(self.path.at(G0), self.A["marks"][MARK][2])
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
            C.key_vis(self.lamp, g < LAMP_HIDE, f)                    # our lamp-post: gone once it has left frame (no corner sliver)
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
