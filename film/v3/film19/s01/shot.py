#!/usr/bin/env python3
"""shot.py -- film 19 take s01 = shot 1, THE HOOK (g 0..56 + 9 out-handle frames g 57..65; hard cut to shot 2 at g 57).
"ช่างไม้ บ้านนอกคนนี้ บอกว่านาฬิกา ..." -- this country carpenter says that a clock ...

WORKSHOP shop_bench / DAY, set_clock(1) (the H1 alone on the bench), set_balance(t) on EVERY frame (the crossed dumbbell bars rock
+-24 deg, 1.3 s period, the gears turn), set_candles(1.0) on every frame (flicker).  Harrison (harrison19 default: greying hair,
apron with shavings) stands behind the bench at mark harrison_bench, to the right of the H1, and presents it with both arms.
    g  0..11  arms swing up from his sides into the presenting gesture (both open palms toward the H1), proud grin; camera
              already moving (push + slide + arc), the plane and shavings on the sawhorse in the bottom-left foreground
    g 12..35  he holds the presentation with a small proud bounce; blink at g 20; the bars rock
    g 36..49  SNAP push x1.35 with a pan on "บอกว่านาฬิกา" (caption 1.12 s = event g 37; the word นาฬิกา is spoken
              about g 44): his palms thrust out a second time ("ta-da!") and his eyes go to the clock
    g 50..65  hold the ta-da, eyes back to the lens, grin; still moving through the hard cut at g 57 and the handle
Mouths: nobody speaks (no quote): expression mouth only (grinning, fixed).  NO depth of field, NO text, NO caption_shade.

The camera (c19.CamPath): from near the preset's start pose (0.2 D left, 0.14 D back, same height), looking 2 deg up at a subject
point at HARRISON's depth between him and the H1.  Drift push 8 %/s + slide -45 px/s + crane 35 px/s + arc 15 deg/s about that
point (the nearer H1 swings across Harrison's background: parallax), decay 0.1 (still moving on the last frame: hard cut), plus
the snap x1.35 (13 f, peak 1.9) with a pan right/down that keeps his head at y 610-670.  Values tuned on drafts for the
frame-diff target (QA.md).  A lower camera puts the sawhorse plank over 40 % of the frame; a bigger arc ends on the H1 side-on.

    python3 shot.py probe a:b[:step]                       numbers only (camera, heads), no render
    python3 shot.py camreport                              CamPath corner speed per frame (never parked check), no bpy scene
    python3 shot.py stills a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final a:b[:step] [scale] [samples]     -> raw/g_%04d.png + .json (resumable; run 2 processes, e.g. 0:65:2 / 1:65:2)
    python3 shot.py final 0:65 0.5 6                       DRAFT (360x640, 6 spp) -> work/draft/ (same loop)
    python3 deliver.py                                     -> frames/, take.mkv, meta.json, cues.json, contact.jpg, framediff numbers
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c19 as C                                          # noqa: E402  (paths, cast19 first, bpy, h19, stage)
from mathutils import Vector                             # noqa: E402

H, K, actors, cast19 = C.H, C.K, C.actors, C.cast19
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

# ----------------------------------------------------------------------------- timing (film frames g)
G0, G1 = C.g_bound(0.00), C.g_bound(1.91)     # 0, 57: shot 1 = g 0..56; shot 2 (hard cut, ship_aerial) starts at g 57
H_OUT = 9                                      # out-handle g 57..65 (WORKER19: 9 handle frames; the move and the idle continue)
G_LAST = G1 + H_OUT - 1                        # 65
GS = list(range(G0, G_LAST + 1))
G_CLOCK = C.cap_g("บอกว่านาฬิกา")               # 37: "says that a clock" -> the snap
SNAP = (G_CLOCK - 2, G_CLOCK + 16)             # 36..49 (13 frames, the bible minimum: lands as the word นาฬิกา is spoken, ~g 44)
G_RISE = (0, 11)                               # arms swing up into the presentation
G_TADA = (G_CLOCK, G_CLOCK + 7)                # second, bigger presentation on the snap
BLINKS = [20, 50]

# ----------------------------------------------------------------------------- staging
LIGHT = "DAY"
PRESET = "shop_bench"
CLOCK = 1                                      # the H1 alone (shop_bench default)
FINAL_SPP = 8                                  # = H.STATE['samples'] of WORKSHOP (Take() checks it); set3d19/cost_report.txt
PPD = 256                                      # sprite px per D (head ~130 px at g 0, ~270 px after the snap)
HIDE_SHAFTS = True                             # the faint window-shaft volume runs toward this camera: it is the 'milky haze' of the
                                               # QA_ART round-2 NOTE (shop_bench DAY); hidden here, the sun patches stay
CANVAS = None                                  # cast19.CANVAS19['harrison19'] is enough here (no clipping warnings)

CAM_LOC0 = (1.90, -1.95, 2.25)                 # near the preset start (2.31, -1.11, 2.22); lower = the sawhorse plank fills the frame
CAM_LOOK0 = (2.70, 3.2, 2.05)                  # subject point at HARRISON's depth, between him and the H1: the arc keeps him put
                                               # while the nearer H1 swings across (parallax); the push keeps both in frame
CAM = C.CamPath(CAM_LOC0, CAM_LOOK0, G0, G_LAST, push=0.04, slide_px=-25.0, rise_px=60.0, arc_deg_s=18.0, decay=0.1,
                snaps=[dict(g=SNAP, k=1.18, peak=3.2, shift=(-0.05, -0.75))])


MARK_OFF = Vector((0.12, -2.9, 0.0))             # QA_ART fix: beside the H1 on the camera side (was 1.6 D behind it)

# ----------------------------------------------------------------------------- pose (cast19 harrison19 default; mirrored: faces the H1 at screen-left)
BASE = cast19.STORY19["harrison_idle"][1]
DOWN_R, DOWN_L = (0.70, 0.85), (-0.50, 0.75)          # arms down (puppet-local, unmirrored)
PRES_R, PRES_L = (0.92, 0.42), (-0.55, 0.12)           # presenting: both open palms out toward screen-right (screen-left mirrored)
TADA_R, TADA_L = (1.0, 0.22), (-0.62, -0.02)           # the ta-da on the snap: higher and further out


def _mix(a, b, u):
    return (lerp(a[0], b[0], u), lerp(a[1], b[1], u))


def pose_of(g):
    """the drawn pose of frame g.  Mirror: the H1 is screen-LEFT of him, so the screen-right-facing figure is mirrored; the arm
    keys stay arm_r / arm_l of the UNMIRRORED figure."""
    p = dict(BASE)
    u1 = u_of(g, *G_RISE, kind="sine")
    u2 = u_of(g, *G_TADA, kind="sine")
    hr = _mix(_mix(DOWN_R, PRES_R, u1), TADA_R, u2)
    hl = _mix(_mix(DOWN_L, PRES_L, u1), TADA_L, u2)
    bob = 0.05 * math.sin(2 * math.pi * g / 15.0)                     # 2 Hz proud bob of the hands
    p["arm_r"] = dict(hand=(hr[0], hr[1] + bob), bend=-0.25, shape="open", stretch=1.15, layer="top")
    p["arm_l"] = dict(hand=(hl[0], hl[1] + bob), bend=-0.15, shape="open", stretch=1.1, layer="top")
    p["mirror"] = True
    p["yaw"] = 0.30
    p["expr"] = "grinning"
    p["lean"] = -2.0 - 3.0 * u2 + 1.2 * math.sin(g * 0.21)            # chest out on the ta-da
    p["head_roll"] = -3.0 + 2.0 * math.sin(g * 0.17 + 0.6)
    p["pitch"] = -0.10
    if G_TADA[0] <= g < G_TADA[1] + 8:
        p["gaze"] = (0.8, 0.1)                                         # a proud glance at the clock (screen-left after the mirror)
    else:
        p["gaze"] = (0.15, 0.0)                                        # at the viewer
    p["blink"] = blink(g, BLINKS)
    p["t"] = g / 30.0
    return p


def bounce_z(g):
    """a small proud rise on the toes with the ta-da (D)."""
    return 0.05 * math.sin(math.pi * u_of(g, G_TADA[0], G_TADA[1] + 6)) + 0.012 * math.sin(2 * math.pi * g / 15.0)


# ----------------------------------------------------------------------------- the take
class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s01")
        assert self.final_samples() == FINAL_SPP, "set final samples changed: %s" % self.final_samples()
        self.drop_top_right_plank()
        self.lantern = [o for o in C.bpy.data.objects if o.name.startswith(("lantern_", "lanternf_"))]
        print("stool lantern objects hidden:", [o.name for o in self.lantern], flush=True)
        self.key_cam(bf(G0), *CAM.at(G0))
        self.scene.frame_set(bf(G0))
        self.har = self.actors["har"] = C.make_actor("har", "harrison19", os.path.join(WORK, "sprites"), canvas=CANVAS, contact=True,
                                                     cam=self.cam)

    def drop_top_right_plank(self):
        """QA_ART fix: the bright diagonal oak plank hanging near the ceiling at the top right (shop_oak island holding the face
        hit by a ray at x 3.2, y 2.1, z 4.7) pulled the eye: its connected island is deleted from the (scene-local) mesh."""
        import bmesh
        ob = C.bpy.data.objects["shop_oak"]
        bm = bmesh.new()
        bm.from_mesh(ob.data)
        bm.faces.ensure_lookup_table()
        seed = [bm.faces[814]]
        island, stack = set(), list(seed)
        while stack:
            f = stack.pop()
            if f in island:
                continue
            island.add(f)
            for e in f.edges:
                stack.extend(o for o in e.link_faces if o not in island)
        print("plank island faces:", len(island), flush=True)
        bmesh.ops.delete(bm, geom=list(island), context="FACES")
        bm.to_mesh(ob.data)
        bm.free()
        # round 3: a second lit plank (shop_honey face 576, z 4.72) shows at the top right with the new framing
        ob = C.bpy.data.objects["shop_honey"]
        bm = bmesh.new()
        bm.from_mesh(ob.data)
        bm.faces.ensure_lookup_table()
        island, stack = set(), [bm.faces[576]]
        while stack:
            f = stack.pop()
            if f in island:
                continue
            island.add(f)
            for e in f.edges:
                stack.extend(o for o in e.link_faces if o not in island)
        print("plank 2 island faces:", len(island), flush=True)
        bmesh.ops.delete(bm, geom=list(island), context="FACES")
        bm.to_mesh(ob.data)
        bm.free()
        # round 3: the stool lantern's iron cage is merged into shop_iron (key_vis of lanternf_iron / lantern_lampg leaves it):
        # delete its faces (x 3.45-3.95, y 1.5-2.0, z 1.10-1.9) from the scene mesh
        ob = C.bpy.data.objects["shop_iron"]
        bm = bmesh.new()
        bm.from_mesh(ob.data)
        C.bpy.context.view_layer.update()
        mw = ob.matrix_world.copy()
        cage = [f for f in bm.faces if (lambda c: 3.45 < c.x < 3.95 and 1.5 < c.y < 2.0 and 1.10 < c.z < 1.9)(mw @ f.calc_center_median())]
        print("lantern cage faces deleted:", len(cage), flush=True)
        bmesh.ops.delete(bm, geom=cage, context="FACES")
        bm.to_mesh(ob.data)
        bm.free()

    def pose(self, gs):
        mark = Vector(self.A["marks"]["harrison_bench"]) + MARK_OFF
        for g in gs:
            f = bf(g)
            self.key_cam(f, *CAM.at(g))
            C.place(self.har, f, mark + Vector((0, 0, bounce_z(g))))
            # the set state, keyed on EVERY frame: H1 alone, bars rocking (t = film seconds), candle flicker
            self.key_set(f, clock=CLOCK, balance=g / 30.0, candles=1.0)
            C.key_vis(H.STATE.get("shafts", []), not HIDE_SHAFTS, f)
            C.key_vis(self.lantern, False, f)                           # round 3: nothing in front of him below y 880   # QA_ART NOTE: shop_bench DAY milky haze = the window-shaft volume
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.har.pose(f, pose_of(g), camera=self.cam)
        self.sprites_for([(self.har, PPD)], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = CAM.at(g)
        v = look - loc
        bars = C.clock_world(CLOCK, (0.0, 0.0, 0.64))
        pts = [H.project((x, y, z)) for x in (0.74, 3.3) for y in (2.67, 4.3) for z in (1.66, 3.71)]
        h1box = [round(min(p[0] for p in pts)), round(min(p[1] for p in pts)), round(max(p[0] for p in pts)), round(max(p[1] for p in pts))]
        return dict(g=g, h1_bbox_px=h1box, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    heads=C.head_report(self, f), h1_bars_px=H.project(tuple(bars)), dof=self.cam.data.dof.use_dof,
                    caption_shade=bool(C.bpy.data.objects.get("caption_shade")))

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
    gs = [g for g in C.parse(sys.argv[2]) if G0 <= g <= G_LAST]
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
        if samples is None:                                   # the set's own final samples (H.STATE['samples'] after build)
            samples = FINAL_SPP
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")       # drafts never mix with finals
        C.final_loop(lambda: Take(quality), gs, out, scale=scale, samples=samples)
