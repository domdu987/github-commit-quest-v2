#!/usr/bin/env python3
"""shot.py -- film 10 take s12: shots 12-14 (g 782..1004 incl. 6 in / 6 out handle frames), "false" line 26.27-33.27 s.
  shot 12 g 782..863  convoy_wide SEA_DAY   the dazzle ship in the convoy of grey ships, the periscope cuts the water in the foreground
  shot 13 g 864..926  periscope_pov         the lens view sweeps the convoy and stops on the dazzle ship
  shot 14 g 927..1004 bridge_deck           the admiral with binoculars shouts "เห็นมั้ย เป้าชัดแจ๋วเลย!" (lip-sync 31.60-33.25 s only)
Sea clock: s = g/30 - 35.0 (the torpedo is fired at ~35 s), the convoy sails +x at 2.5 D/s.  One process per shot (the periscope
overlay is created lazily).  Blender frame of (id, g) = 1000*(id-1)+g+1.
    python3 shot.py stills 12 a:b[:step] out [scale] [samples]
    python3 shot.py final 12|13|14 a:b[:step] [scale] [samples]"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c10 as C                                          # noqa: E402
from mathutils import Vector, Matrix                     # noqa: E402
H, actors, cast10 = C.H, C.actors, C.cast10
lerp, clamp, blink, ez = C.lerp, C.clamp, C.blink, C.ez
TMP = os.path.join(HERE, "work")
HO = 6
G12, G13, G14, GE = C.g_bound(26.27), C.g_bound(28.80), C.g_bound(30.90), C.g_bound(33.27)   # 788 864 927 998
RANGES = {12: (G12 - HO, G13 - 1), 13: (G13, G14 - 1), 14: (G14, GE + HO - 1)}
PRESET = {12: "convoy_wide", 13: "periscope_pov", 14: "bridge_deck"}
LENS = {12: 30.0, 13: 42.0, 14: 24.0}
G_LIP0, G_LIP1 = C.g_of(31.60), C.g_of(33.25)            # 951 .. 1000: the admiral's mouth moves only here
G_SHOUT_EXPR = G_LIP0 - 3


def sea_s(g):
    return g / 30.0 - 35.0


CAM12 = ((-74.0, -146.0, 14.0), (-22.0, 20.0, 1.0), (-52.0, -143.0, 15.5), (-2.0, 22.0, 1.5))


def u_lin(g, shot):
    a, b = RANGES[shot]
    x = (g - a) / float(b - a)
    return 0.35 * ez(x, "sine") + 0.65 * x


def az_deg(frm, to):
    return math.degrees(math.atan2(to[0] - frm[0], to[1] - frm[1]))


class Take(C.Take):
    def __init__(self, quality="preview", shot=12):
        C.Take.__init__(self, PRESET[shot], quality=quality, lens=LENS[shot], name="cam_s12")
        self.sh = shot
        self.crew = C.Crew(self, os.path.join(TMP, "crew%d" % shot), ppd=96)
        self.ad = None
        if shot == 14:
            self.ad = self.actors["ad"] = C.make_actor("ad", "admiral", os.path.join(TMP, "sprites14"))
            root = H.ship_root("flag")
            bpy = C.bpy
            bpy.context.view_layer.update()
            mark = Vector(self.A["marks"]["admiral_bridge"])
            self.ad_local = root.matrix_world.inverted() @ mark
            self.root = root
            self.cam14 = self.A["cams"]["bridge_deck"]
            # the bridge camera is placed for s = 0: carry it along with the flagship (same offset as the ship)
            self.base14 = self.root.location.copy()
        if shot == 13:
            self.eye = Vector(H.periscope_eye())
            u = H.STATE["uboat"]
            for k in ("head", "tube", "feather", "wash"):          # the camera sits inside the periscope head: hide it (looking sideways showed its inside)
                if k in u:
                    u[k].hide_render = True
                    for ch in u[k].children_recursive:
                        ch.hide_render = True

    # -------------------------------------------------------------------------
    def cam_of(self, shot, g):
        s = sea_s(g)
        if shot == 12:
            u = u_lin(g, 12)
            a, b, c, d = CAM12
            return Vector([lerp(a[i], c[i], u) for i in range(3)]), Vector([lerp(b[i], d[i], u) for i in range(3)])
        if shot == 13:
            return self.cam13(g)
        # shot 14: along with the flagship, slow push toward the admiral + slight orbit
        u = u_lin(g, 14)
        d = Vector((2.5 * s, 0, 0))
        loc = Vector(self.cam14["loc"]) + d
        look = Vector(self.cam14["look_at"]) + d
        tgt = Vector(self.A["marks"]["admiral_bridge"]) + d + Vector((0, 0, 2.6))
        fwd = (look - loc).normalized()
        loc = loc + fwd * lerp(0.0, 1.4, u) + Vector((lerp(0.0, -0.5, u), lerp(0.0, 0.4, u), 0))
        look = look.lerp(tgt, 0.0)
        return loc, look

    def cam13(self, g):
        """eye fixed (the periscope head); look azimuth sweeps c1 -> right across the convoy, swings back and settles on the dazzle ship."""
        s = sea_s(g)
        sh = H.STATE["ships"]
        pos = {nm: Vector(sh[nm]["base"]) + Vector((2.5 * s, 0, 0)) for nm in sh if nm != "ghost"}
        eye = self.eye
        dz = pos["dazzle"]
        a_dz = az_deg(eye, dz)
        a_l = az_deg(eye, pos["c1"])
        t = (g - RANGES[13][0]) / 30.0                  # 0 .. 2.1 s
        T_SW = 1.0                                     # one sweep c1 -> dazzle ship (nearly linear: grey ships fly past), then it stops
        if t < T_SW:
            x = t / T_SW
            az = lerp(a_l - 8.0, a_dz, 0.2 * ez(x, "sine") + 0.8 * x)
        else:
            az = a_dz + 0.35 * math.sin((t - T_SW) * 3.0) * 0.5 + 0.25 * (t - T_SW)     # settle drift while stopped (never static)
        dist = 120.0
        ar = math.radians(az)
        look = eye + Vector((math.sin(ar) * dist, math.cos(ar) * dist, 0)) + Vector((0, 0, 4.2 - eye.z))
        return eye, look

    def ad_world(self, f, g):
        self.scene.frame_set(f)
        return self.root.matrix_world @ self.ad_local

    def pose_ad(self, g):
        t = g / 30.0
        p = dict(cast10.STORY10["admiral_shout"][1])
        lip = G_LIP0 <= g <= G_LIP1
        p["mouth"] = cast10.talk_mouth(g, 1.0) if lip else "flat"
        p["expr"] = "shouting" if g >= G_SHOUT_EXPR else "determined"
        p["head_roll"] = 6 + 1.5 * math.sin(t * 5.0)
        p["lean"] = (3.0 if lip else 0.0) + 1.2 * math.sin(t * 2.1)
        p["blink"] = blink(g, [G_SHOUT_EXPR - 2])
        p["t"] = t
        return p

    def pose(self, shot, gs):
        for g in gs:
            f = C.bf(shot, g)
            s = sea_s(g)
            H.set_convoy(s, frame=f)
            H.set_smoke(1.0, frame=f)
            H.set_uboat(1.0, frame=f, periscope=1.0)
            if shot == 13:
                u = H.STATE["uboat"]
                for k in ("head", "tube", "feather", "wash"):
                    if k in u:
                        for o in [u[k]] + list(u[k].children_recursive):
                            o.hide_render = True; o.keyframe_insert("hide_render", frame=f)
            if shot == 13:
                H.periscope_overlay(True, frame=f)
            loc, look = self.cam_of(shot, g)
            self.key_cam(f, loc, look, lens=LENS[shot])
            if shot != 13:
                self.crew.key(f)
            else:
                for _, ob, a, _ in self.crew.items:      # periscope: crew would be pixels, hide them
                    a.card.hide_render = True; a.card.keyframe_insert("hide_render", frame=f)
                    for o in (a.proxy, a.contact):
                        if o is not None:
                            o.hide_render = True; o.keyframe_insert("hide_render", frame=f)
            if shot == 14:
                p = self.ad_world(f, g)
                self.ad.place(f, (p.x, p.y, p.z))
        for g in gs:
            f = C.bf(shot, g)
            self.scene.frame_set(f)
            if shot == 14:
                self.ad.pose(f, self.pose_ad(g), camera=self.cam)
            if shot != 13:
                self.crew.pose(f, g)
        fr = [C.bf(shot, g) for g in gs]
        if shot == 14:
            self.sprites_for([(self.ad, 320)], fr)
        if shot != 13:
            self.crew.sprites(fr)

    def report(self, shot, g):
        f = C.bf(shot, g)
        self.scene.frame_set(f)
        loc, look = self.cam_of(shot, g)
        hp = {}
        if self.ad is not None and (self.ad.name, f) in self.anch:
            a = self.ad
            hx, hy = self.anch[(a.name, f)]["head"]
            c = actors.local_to_screen(a, self.cam, (hx, hy), f, a.feet.get(f))
            hp = dict(x=round(c[0], 1), y=round(c[1], 1))
        return dict(shot=shot, g=g, s=round(sea_s(g), 3), cam=[round(c, 2) for c in loc], head=hp,
                    mouth_window=[G_LIP0, G_LIP1] if shot == 14 else None)

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [C.bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    if cmd == "stills":
        Tk = Take("preview", shots[0])
        for shot in shots:
            gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
            if not gs:
                continue
            Tk.pose(shot, gs)
            out = sys.argv[4]
            scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
            samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
            for g in gs:
                print(json.dumps(Tk.report(shot, g)), flush=True)
                st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
                print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q: Take(q, shots[0]), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
