#!/usr/bin/env python3
"""shot.py -- film 10 take s01: shots 1 + 2 (g 0..133 + 6 out-handle frames g 134..139), the hook:
"this painter paints a warship in zebra stripes that contrast so hard they can be seen from far away".
One location (harbour, DAY), one process, two set-ups joined by the plan's cut at 2.30 s (g 69):

    id 1  g 0..68    shot 1, hull_plank: Norman on the hanging plank against the grey hull paints a bold zigzag; set_stripes
                     animates 0.30 -> 0.48 (the stripe front enters frame at ~0.36 and reaches his brush at 0.47).  Slow push.
    id 2  g 69..139  shot 2, harbour_wide: crane OUT (the camera rises and pulls back over the dockyard): the half-striped ship
                     (stage 0.48 -> 0.50) stands out among the grey ships.  Real cast10 cards replace the quay / deck placeholders.
Mouths: nobody speaks (no quote in shots 1-2): static expression mouths only.   NO depth of field.
Blender frame of (id, g) = 1000 * (id - 1) + g + 1.

    python3 shot.py probe 1,2 a:b[:step]
    python3 shot.py stills 1,2 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 1|2 a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c10 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

H, actors, camrig, cast10, bpy = C.B, C.actors, C.camrig, C.cast10, C.bpy
lerp, clamp, blink, ez, bf = C.lerp, C.clamp, C.blink, C.ez, C.bf
TMP = os.path.join(HERE, "work")

# ----------------------------------------------------------------------------- timing
G_CUT = C.g_bound(2.30)            # 69: shot 2 starts
G_END = C.g_bound(4.48)            # 134: shot 3 starts here
H_OUT = 6
RANGES = {1: (0, G_CUT - 1), 2: (G_CUT, G_END + H_OUT - 1)}
LOC = ("harbour", "hull_plank")
LIGHT = "DAY"
STAGE0, STAGE1, STAGE2 = 0.30, 0.48, 0.50      # shot 1 start / end, shot 2 end

# ----------------------------------------------------------------------------- cameras
# shot 1: the preset (-1.5,-10,3.6) -> (-2.4,1.2,4.6) 24 mm, a slow push and a drift to the right with the brush
CAM1 = [((-1.9, -10.6, 3.55), (-2.55, 1.2, 4.55), 24.0), ((-1.5, -8.7, 3.7), (-1.9, 1.2, 4.6), 26.0)]
# shot 2: crane OUT: starts low over the quay near the striped hull, rises and pulls back to the preset harbour_wide
CAM2 = [((-22.0, -16.0, 11.0), (2.0, 12.0, 4.0), 20.0), ((-46.0, -33.0, 30.0), (10.0, 24.0, 0.0), 20.0)]
PPD = {"painter": {1: 224, 2: 64}, "bg": 48}


def cam_of(shot, g):
    a, b = (CAM1 if shot == 1 else CAM2)
    x = (g - RANGES[shot][0]) / float(RANGES[shot][1] - RANGES[shot][0])
    u = 0.30 * ez(x, "sine") + 0.70 * x
    return Vector([lerp(a[0][i], b[0][i], u) for i in range(3)]), Vector([lerp(a[1][i], b[1][i], u) for i in range(3)]), lerp(a[2], b[2], u)


def stage_of(shot, g):
    if shot == 1:
        return lerp(STAGE0, STAGE1, g / float(G_CUT - 1))
    return lerp(STAGE1, STAGE2, (g - G_CUT) / float(G_END + H_OUT - 1 - G_CUT))


# ----------------------------------------------------------------------------- poses
PLANK = None   # filled from the set: painter_plank mark


def pose_painter1(g):
    """on the plank: bigbrush sweeps toward the stripe front (screen-right), bucket on the other arm."""
    base = dict(cast10.STORY10["painter_on_plank"][1])
    base["plank"] = 0                                       # the set has its own hanging stage
    ph = (g % 22) / 22.0
    s = 0.5 - 0.5 * math.cos(2 * math.pi * ph)              # 0..1..0 stroke
    base["arm_r"] = dict(hand=(lerp(0.74, 0.66, s), lerp(0.58, -0.28, s)), bend=lerp(-0.2, -0.65, s), stretch=1.3, layer="front")
    base["prop_r"] = dict(type="bigbrush", scale=0.9, angle=lerp(-20, -62, s))
    base["arm_l"] = dict(hand=(-0.4, 1.0), bend=0.3)
    base["lean"] = lerp(-1.0, -3.5, s)
    base["pitch"] = lerp(-0.1, -0.35, s)
    base["head_roll"] = -4 + 1.2 * math.sin(g * 0.21)
    base["gaze"] = (0.9, lerp(0.0, -0.45, s))
    base["blink"] = blink(g, [24, 55])
    base["t"] = g / 30.0
    return base


def pose_painter2(g):
    p = pose_painter1(g)
    p["blink"] = blink(g, [90, 120])
    return p


SAIL = ("sailor_a", "sailor_b", "sailor_c")


def pose_bg(i, g):
    """idle life for the small background figures: the stock idle poses with a slow sway; every 3rd one points and laughs."""
    k = SAIL[i % 3]
    name = "sailor_idle_" + k[-1]
    cast, p = cast10.STORY10[name]
    p = dict(p)
    p["lean"] = 1.6 * math.sin(g * 0.07 + i * 1.7)
    p["head_roll"] = 2.2 * math.sin(g * 0.05 + i)
    p["t"] = g / 30.0
    p["blink"] = blink(g, [(37 * i + 20) % 90 + 5])
    return cast, p


# ----------------------------------------------------------------------------- the take
class Take(C.Take):
    def __init__(self, quality="preview", shot=1):
        C.Take.__init__(self, LOC[0], LOC[1], quality=quality, lens=24.0, name="cam_s01", light=LIGHT)
        self.pl = Vector(self.A["marks"]["painter_plank"])
        self.pnt = self.actors["pnt"] = C.make_actor("pnt", "painter10", os.path.join(TMP, "sprites"), canvas=cast10.CANVAS10_PLANK["painter10"])
        self.bg = []
        self._swap_cards()

    def _swap_cards(self):
        """replace the visible placeholder cards (quay / scaffold / deck) with real cast10 sailors at the same spots; hide the rest."""
        from bpy_extras.object_utils import world_to_camera_view
        sc = self.scene
        keep = []
        for ob in list(H.STATE.get("cards", [])):
            bpy.context.view_layer.update()
            w = ob.matrix_world.translation.copy()
            seen = False
            for sh in (1, 2):
                for g in (RANGES[sh][0], (RANGES[sh][0] + RANGES[sh][1]) // 2, RANGES[sh][1]):
                    loc, look, lens = cam_of(sh, g)
                    # temporary camera pose for the projection
                    self.key_cam(1, loc, look, lens=lens)
                    sc.frame_set(1)
                    p = world_to_camera_view(sc, self.cam, w + Vector((0, 0, 1.5)))
                    if -0.05 < p.x < 1.05 and -0.05 < p.y < 1.05 and p.z > 0:
                        seen = True
            ob.hide_render = True
            if seen:
                keep.append((ob, w))
        # reset camera keys written by the visibility probe
        self.cam.animation_data_clear()
        for i, (ob, w) in enumerate(keep):
            c = "sailor_" + "abc"[i % 3]
            a = C.make_actor("bg%d" % i, c, os.path.join(TMP, "sprites"))
            a.base = w
            self.bg.append(a)
            self.actors[a.name] = a
        print("take: %d background cards swapped for cast10 sailors" % len(self.bg), flush=True)

    def pose(self, shot, gs):
        for g in gs:
            f = bf(shot, g)
            loc, look, lens = cam_of(shot, g)
            self.key_cam(f, loc, look, lens=lens)
            H.set_stripes(stage_of(shot, g), frame=f)
            H.set_smoke(1.0, frame=f)
            self.pnt.hide_render = False
            C.place(self.pnt, f, self.pl[:2], self.pl[2])
            for a in self.bg:
                C.place(a, f, a.base[:2], a.base[2])
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            self.pnt.pose(f, pose_painter1(g) if shot == 1 else pose_painter2(g), camera=self.cam)
            for i, a in enumerate(self.bg):
                a.pose(f, pose_bg(i, g)[1], camera=self.cam)
        frames = [bf(shot, g) for g in gs]
        self.sprites_for([(self.pnt, PPD["painter"][shot])] + ([(a, PPD["bg"]) for a in self.bg] if shot == 2 else []), frames)
        for a in self.bg:                                  # background figures show in shot 2 only
            for g in gs:
                a.card.hide_render = shot == 1
                a.card.keyframe_insert("hide_render", frame=bf(shot, g))

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look, lens = cam_of(shot, g)
        v = look - loc
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], lens=round(lens, 2), stage=round(stage_of(shot, g), 3),
                    pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1), heads=C.head_report(self, f, extra=None))

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
                    os.makedirs(out, exist_ok=True)
                    st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                    os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
                    print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q: Take(q), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
