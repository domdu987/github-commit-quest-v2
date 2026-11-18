#!/usr/bin/env python3
"""shot.py -- film 10 take s03: shots 3 + 4 (g 134..292; in-handle g 128..133, out-handle g 293..298).
One location (sea, SEA_DAY), one process, two set-ups joined by the plan's cut at 7.10 s (g 213):

    id 3  g 128..212  shot 3, convoy_wide: grey ships at sea (hero ship plain grey, set_stripes 0); the dived U-boat's periscope cuts
                      the water in the foreground; slow push.
    id 4  g 213..298  shot 4: a grey merchant (c3) far off is hit (set_hit: water column + smoke, no fire, no gore); then the
                      periscope sinks (set_uboat periscope 1 -> 0): the U-boat dives.
Nobody speaks.   NO depth of field.   Blender frame of (id, g) = 1000 * (id - 1) + g + 1.

    python3 shot.py probe 3,4 a:b[:step]
    python3 shot.py stills 3,4 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 3|4 a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c10 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

H, actors, camrig, cast10, bpy = C.B, C.actors, C.camrig, C.cast10, C.bpy
lerp, clamp, blink, ez, bf = C.lerp, C.clamp, C.blink, C.ez, C.bf
TMP = os.path.join(HERE, "work")

G_CUT = C.g_bound(7.10)            # 213
G_END = C.g_bound(9.76)            # 293
H_IN, H_OUT = 6, 6
RANGES = {3: (C.g_bound(4.48) - H_IN, G_CUT - 1), 4: (G_CUT, G_END + H_OUT - 1)}
G0 = RANGES[3][0]
LOC = ("sea", "convoy_wide")
LIGHT = "SEA_DAY"
G_HIT = 222                        # the column shoots up (t = 0)
G_DIVE = (244, 288)                # periscope sinks

CAM3 = [((-58.5, -107.5, 2.6), (-11.5, -19.0, 5.2), 23.0), ((-58.0, -104.0, 2.8), (-9.0, -15.0, 5.4), 28.0)]
# shot 4: lower and closer to the periscope, looking at the far merchant c3 (tracked in x by the convoy's speed)
CAM4 = [((-72.0, -108.0, 4.2), (6.8, -46.4, 4.6), 22.0), ((-67.0, -103.0, 4.0), (10.0, -44.0, 4.4), 28.0)]
C3_OFF = (14.0, -106.0, 0.0)           # the hit merchant is moved to a clear lane in front of the other ships so the hit reads


def s_of(g):
    return (g - G_END) / 30.0 - 4.0              # convoy time; continuous across the cut


def cam_of(shot, g):
    a, b = CAM3 if shot == 3 else CAM4
    r0, r1 = RANGES[shot]
    x = (g - r0) / float(r1 - r0)
    u = 0.30 * ez(x, "sine") + 0.70 * x
    loc = Vector([lerp(a[0][i], b[0][i], u) for i in range(3)])
    look = Vector([lerp(a[1][i], b[1][i], u) for i in range(3)])
    return loc, look, lerp(a[2], b[2], u)


def hit_t(g):
    return -1.0 if g < G_HIT else min(1.0, (g - G_HIT) / 66.0)


def peri_k(g):
    return 1.0 - ez((g - G_DIVE[0]) / float(G_DIVE[1] - G_DIVE[0]), "sine")


class Take(C.Take):
    def __init__(self, quality="preview", shot=3):
        C.Take.__init__(self, LOC[0], LOC[1], quality=quality, lens=22.0, name="cam_s03", light=LIGHT)
        self.bg = []
        self._swap_cards()

    def _swap_cards(self):
        """deck crew placeholder cards of the convoy ships -> real cast10 sailors riding the same spots (re-placed every frame)."""
        for i, ob in enumerate(list(H.STATE.get("cards", []))):
            ob.hide_render = True
            a = C.make_actor("bg%d" % i, "sailor_" + "abc"[i % 3], os.path.join(TMP, "sprites"))
            a.src = ob
            self.bg.append(a)
            self.actors[a.name] = a
        print("take: %d deck cards swapped for cast10 sailors" % len(self.bg), flush=True)

    def pose(self, shot, gs):
        for g in gs:
            f = bf(shot, g)
            loc, look, lens = cam_of(shot, g)
            H.set_convoy(s_of(g), frame=f)
            if shot == 4:
                self.scene.frame_set(f)
                rt = H.ship_root('c3'); p = rt.location.copy()
                rt.location = (p.x + C3_OFF[0], p.y + C3_OFF[1], p.z); rt.keyframe_insert('location', frame=f)
            self.key_cam(f, loc, look, lens=lens)
            H.set_stripes(0.0, frame=f)
            H.set_smoke(1.0, frame=f)
            H.set_uboat(1.0, frame=f, periscope=peri_k(g) if shot == 4 else 1.0)
            H.set_torpedo(-1, frame=f)
            H.set_hit(hit_t(g) if shot == 4 else -1.0, frame=f)
            for b in H.STATE['plume']:                    # bigger, readable plume + smoke
                b['ob'].scale = tuple(v * 1.2 for v in b['ob'].scale); b['ob'].keyframe_insert('scale', frame=f)
            rt = H.ship_root('c3'); rt.rotation_euler.x = 0.17 * ez((g - G_HIT - 4) / 60.0) if shot == 4 else 0.0
            rt.keyframe_insert('rotation_euler', frame=f)          # the hit merchant lists
            self.scene.frame_set(f)
            bpy.context.view_layer.update()
            for a in self.bg:
                w = a.src.matrix_world.translation
                C.place(a, f, (w.x, w.y), w.z)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            for i, a in enumerate(self.bg):
                p = dict(cast10.STORY10["sailor_idle_" + "abc"[i % 3]][1])
                p["lean"] = 1.5 * math.sin(g * 0.07 + i * 1.7)
                p["t"] = g / 30.0
                a.pose(f, p, camera=self.cam)
        self.sprites_for([(a, 48) for a in self.bg], [bf(shot, g) for g in gs])

    def report(self, shot, g):
        loc, look, lens = cam_of(shot, g)
        return dict(shot=shot, g=g, cam=[round(c, 2) for c in loc], look=[round(c, 2) for c in look], hit=round(hit_t(g), 2) if shot == 4 else None)

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
