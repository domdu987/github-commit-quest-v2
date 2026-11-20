#!/usr/bin/env python3
"""shot.py -- film 19 take s04 = shot 4 (g 191..261, 6.37-8.74 s) + 9 in-handle (g 182..190, dissolve in 13 f) + 9 out-handle (g 262..270,
hard cut to shot 5 in the same set).  SHIP ship_rocks / STORM_DUSK, rain on, set_sea(t) + set_roll(t) keyed on every frame.

"อังกฤษ เกือบสามร้อยปีก่อน กลางทะเล ..." -- Captain19 on the forecastle (mark captain_bow, parented to ship_root: rides the deck), holding out the
sea chart in both hands and peering into the fog over the bulwark (captain_peer_chart, facing screen-right), a small lean/peer and a
glance back at the chart; the FG lantern (the set's own mesh, re-hung on a pivot that is parented to the camera so it stays ~1.7 D
from the lens through the push) swings on its rope with the rain falling past it; its warm pool lights the deck.
Camera (c19.CamPath, on_ship so it rides the deck): push 7 %/s + slide + a little crane, one eased snap x1.45 with a pan on
"เกือบสามร้อย" (caption 7.56 s = g 230), still moving on the last frame (hard cut to shot 5).
Nobody speaks (no quote): the captain's mouth is the pose's fixed expression mouth.  NO DOF, NO text, NO caption_shade.

    python3 shot.py camreport | probe a:b[:step] | stills a:b[:step] <dir> [scale] [spp] | final a:b[:step] [scale] [spp]
    python3 shot.py final 182:270 0.5 6        DRAFT 360x640 6 spp -> work/draft/       (then deliver.py draft)
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c19 as C                                          # noqa: E402
from mathutils import Vector, Matrix                     # noqa: E402

H, K, actors, cast19, bpy = C.H, C.K, C.actors, C.cast19, C.bpy
lerp, clamp, blink, ez, u_of, bf = C.lerp, C.clamp, C.blink, C.ez, C.u_of, C.bf
WORK = os.path.join(HERE, "work")

# ----------------------------------------------------------------------------- timing
G0, G1 = C.g_bound(6.37), C.g_bound(8.74)         # 191, 262 -> shot 4 = g 191..261
H_IN, H_OUT = 9, 9
GA, GZ = G0 - H_IN, G1 + H_OUT - 1                # 182 .. 270
GS = list(range(GA, GZ + 1))
G_WORD = C.cap_g("เกือบสามร้อย")                  # 230: the strongest word -> the snap
SNAP = (G_WORD - 1, G_WORD + 14)
BLINKS = [205, 246]

PRESET, LIGHT = "ship_rocks", "STORM_DUSK"
FINAL_SPP = 12
PPD = 256
T_OFFSET = 0.0                                    # sea / roll time = g / 30 + T_OFFSET (shot 5 continues the same clock)

CAM_LOC0 = (3.60, 27.10, 16.30)                   # near the preset start (4.07, 26.27, 16.37), a touch left / back
CAM_LOOK0 = (3.0, 34.55, 14.65)                  # subject point: the captain's head / chart
CAM = C.CamPath(CAM_LOC0, CAM_LOOK0, GA, GZ, push=0.085, slide_px=35.0, rise_px=-12.0, arc_deg_s=0.0, decay=0.15,
                snaps=[dict(g=SNAP, k=1.85, peak=2.4, shift=(0.50, -0.12)), dict(g=(246, 264), k=1.0, peak=1.3, shift=(-0.42, 0.0))])

HIDE = ("deck_cannon_iron", "deck_carr_w", "deck_hatchw")           # render as black blobs in the FG (QA_TECH): kept out of frame
LANT_OFF = (1.75, 0.34, 0.30)                     # lantern centre in the camera frame: forward, right, up (D)
CHART_POSE = cast19.STORY19["captain_peer_chart"][1]


def pose_of(g):
    p = dict(CHART_POSE)
    t = g / 30.0
    u = 0.5 + 0.5 * math.sin(2 * math.pi * t / 2.2)                     # slow peer back and forth
    p["yaw"] = 0.75 + 0.08 * math.sin(2 * math.pi * t / 2.9)            # 3/4 toward the rail (screen-right), not at the lens
    p["lean"] = 6 + 2.5 * u + 3.0 * u_of(g, *SNAP) * (1 if g < SNAP[1] + 20 else 0)
    # head: up into the fog on "กลางทะเล"-ish beats, down at the chart between: eyes always OFF the lens
    look_up = 0.5 + 0.5 * math.sin(2 * math.pi * t / 2.2 + 1.6)
    p["pitch"] = lerp(0.20, -0.20, look_up)
    p["gaze"] = (lerp(0.9, 1.0, look_up), lerp(-0.7, 0.6, look_up))
    # chart in both hands in front of the chest (bent elbows, fingers on the card edge)
    bob = 0.03 * math.sin(2 * math.pi * t / 1.1)
    p["arm_r"] = dict(CHART_POSE["arm_r"], hand=(0.30 + bob, 0.80 + 0.03 * math.sin(2 * math.pi * t / 1.3 + 0.7)), bend=0.7)
    p["arm_l"] = dict(CHART_POSE["arm_l"], hand=(0.08 + bob, 0.76), bend=0.5, stretch=1.0)
    p["blink"] = blink(g, BLINKS)
    p["t"] = t
    return p


def swing(g):
    """lantern swing about its rope top, in the CAMERA's frame: (about view axis, about the camera X) radians."""
    t = g / 30.0
    return 0.09 * math.sin(2 * math.pi * t / 1.9 + 0.4) + 0.03 * math.sin(2 * math.pi * t / 0.7), 0.06 * math.sin(2 * math.pi * t / 2.7)


def ship_cam(g, f):
    loc, look = CAM.at(g)
    return C.on_ship(Take.SHIP_ROOT, f, loc, look)


class Take(C.Take):
    SHIP_ROOT = None

    def __init__(self, quality="preview"):
        C.Take.__init__(self, PRESET, light=LIGHT, quality=quality, name="cam_s04")
        assert self.final_samples() == FINAL_SPP, "set final samples changed: %s" % self.final_samples()
        Take.SHIP_ROOT = self.A["ship_root"]
        self.key_cam(bf(GA), *CAM.at(GA))                   # the ship is level here (no roll keys yet): ride_ship takes the REST inverse
        self.scene.frame_set(bf(GA))
        self.cpt = self.actors["cpt"] = C.make_actor("cpt", "captain19", os.path.join(WORK, "sprites"), canvas=None, contact=True, cam=self.cam)
        C.ride_ship(self.cpt, self.A["ship_root"])
        for n in HIDE:
            ob = bpy.data.objects.get(n)
            if ob is not None:
                ob.hide_render = True
                ob.hide_viewport = True
        self._hang_lantern()

    def _hang_lantern(self):
        """re-hang the FG lantern (meshes fglantern_*, light lampfg) on a pivot at its rope top.  The pivot is keyed per frame (world) to
        a fixed offset in the CAMERA's frame, so the lantern stays ~1.7 D from the lens through the push; it swings about the rope top."""
        bpy.context.view_layer.update()
        names = [o for o in bpy.data.objects if o.name.startswith("fglantern_")]
        light = bpy.data.objects.get("lampfg")
        root = self.A["ship_root"]
        p = Vector(light.location)                                                     # lantern centre, ship_root space (D, rest = world)
        self.lant_c = p.copy()
        self.lant_top = root.matrix_world @ (p + Vector((-0.04, 0.0, 3.0)) * 0.46 * 1.85)
        self.rope_len = (self.lant_top - p).length
        piv = bpy.data.objects.new("lant_pivot", None)
        bpy.context.scene.collection.objects.link(piv)
        piv.matrix_world = Matrix.Translation(self.lant_top)
        bpy.context.view_layer.update()
        for o in names + ([light] if light is not None else []):
            mw = o.matrix_world.copy()
            o.parent = piv
            o.matrix_parent_inverse = piv.matrix_world.inverted() @ mw
        self.piv = piv
        piv.rotation_mode = "XYZ"
        piv.scale = (1.35, 1.35, 1.35)
        self.rope_len *= 1.35

    def key_lantern(self, g, f, loc, look):
        fwd = (look - loc).normalized()
        right = Vector((fwd.y, -fwd.x, 0.0)).normalized()
        up = right.cross(fwd).normalized()
        centre = loc + fwd * LANT_OFF[0] + right * LANT_OFF[1] + up * LANT_OFF[2]
        top = centre + Vector((0, 0, 1)) * self.rope_len
        fh = Vector((fwd.x, fwd.y, 0.0)).normalized()
        a, b = swing(g)
        R = Matrix.Rotation(a, 3, fh) @ Matrix.Rotation(b, 3, right)
        self.piv.location = top
        self.piv.keyframe_insert("scale", frame=f)
        self.piv.rotation_euler = R.to_euler("XYZ")
        self.piv.keyframe_insert("location", frame=f)
        self.piv.keyframe_insert("rotation_euler", frame=f)

    def pose(self, gs):
        mark = Vector(self.A["marks"]["captain_bow"])
        for g in gs:
            f = bf(g)
            t = g / 30.0 + T_OFFSET
            H.set_sea(t, frame=f)
            H.set_roll(t, frame=f)                          # BEFORE the camera (on_ship reads the keyed root)
            H.set_rain(True, frame=f)
            self.key_cam(f, *ship_cam(g, f))
            C.place(self.cpt, f, mark)
            self.key_lantern(g, f, *ship_cam(g, f))
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.cpt.pose(f, pose_of(g), camera=self.cam)
        self.sprites_for([(self.cpt, PPD)], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        loc, look = ship_cam(g, f)
        v = look - loc
        return dict(g=g, cam=[round(c, 3) for c in loc], pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                    heads=C.head_report(self, f), dof=self.cam.data.dof.use_dof, caption_shade=bool(bpy.data.objects.get("caption_shade")))

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
    gs = [g for g in C.parse(sys.argv[2]) if GA <= g <= GZ]
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
        if samples is None:
            samples = FINAL_SPP
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take(quality), gs, out, scale=scale, samples=samples)
