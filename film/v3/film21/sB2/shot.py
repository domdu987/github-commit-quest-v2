#!/usr/bin/env python3
"""shot.py -- film 21 segment B2: g 295..418 (3 handle frames g 295-297 continue team 2's B1 move into P_CAMP at g 298).  D6 in at P_CAMP, CUT out at g 418.
From the knights' parade (P_CAMP = camp_wide) the camera CRANES UP over the pavilions, flies north-east across the river (glitter, the bridge on the left), and
climbs to Abbey Craig; it lands LOW looking up at the Scots spearmen on foot against the sky (P_HILL = hill_low raised 0.8 m, light shafts through the pines).
They shift their spears; one leans on his.

    python3 shot.py path <out.mp4>              10 fps 360x640 path draft (with the cast)
    python3 shot.py stills a:b[:step] <dir> [draft|final] [samples]
    python3 shot.py final a:b[:step] [samples]
"""
import math, os, sys, json, time, subprocess
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c21 as C                                          # noqa: E402
import cast21, bpy, numpy as np                          # noqa: E402,E401
from c21 import K, actors, Vector, lerp, ez              # noqa: E402

TMP = os.path.join(HERE, "work")
G0, G1, GJ = 295, 418, 298
PPD = 192
STAND = [("s1", "scot_b", "scot_b_fold_spear", "s1", 0.0), ("s2", "scot_a", "scot_a_fold_spear", "s2", 1.1),
         ("horn", "scot_horn", "scot_horn_lower", "horn", 2.0), ("w", "wallace", "wallace_fold_spear", "w", 0.6),
         ("s3", "scot_c", "scot_c_stand_still", "s3", 2.9)]


def p_hill():
    loc, look, lens = K.preset_pose("hill_low")
    return (loc[0], loc[1], loc[2] + 0.8), look, lens


def keys():
    pc = K.preset_pose("camp_wide"); ph = p_hill()
    loc = np.array(pc[0]); look = np.array(pc[1]); fwd = look - loc; fwd[2] = 0; fwd /= np.linalg.norm(fwd)
    back = loc - fwd * 5.0 + np.array([0, 0, 2.4])
    over = np.array(ph[0]) + (np.array(ph[0]) - np.array(look)) * 0.0
    end_beyond = np.array(ph[0]) + (np.array(ph[1]) - np.array(ph[0])) * 0.06
    return [(295, tuple(back), tuple(look + np.array([0, 0, 0.3])), 22.0), (298, pc[0], pc[1], 22.0),
            (322, (-50.0, -76.0, 38.0), (12.0, -38.0, 10.0), 22.0),
            (348, (6.0, -42.0, 46.0), (60.0, 22.0, 6.0), 22.0),
            (376, (64.0, 12.0, 36.0), (118.0, 90.0, 12.0), 22.0),
            (398, (104.0, 84.0, K_g(104, 84) + 14.0), (140.0, 130.0, 16.0), 22.0),
            (418, ph[0], ph[1], 22.0),
            (430, tuple(end_beyond), ph[1], 22.0)]


def K_g(x, y):
    return float(K.ground(x, y))


CTR = np.array([137.0, 137.0]); TH = math.radians(224.0)
U_R = np.array([math.cos(TH), math.sin(TH)]); T_R = np.array([-math.sin(TH), math.cos(TH)])
G_SPLIT = 369
G_ARR = 386          # v4: the landing is reached at g386, then a >1 s gentle drift to the cut (no stop, no shake)


def end_landing():
    """LOW HERO landing: the camera 3.3 m (horizontal) below the lip of the shelf, 1.3 m above the slope, looking UP 36 deg at the Scots on the lip: sky behind them."""
    rc = 16.35; p = CTR + U_R * rc
    loc = (float(p[0]), float(p[1]), float(K.ground(p[0], p[1])) + 1.3)
    q = CTR + U_R * 13.3
    look = (float(q[0]), float(q[1]), float(K.ground(q[0], q[1])) + 1.9)
    return loc, look


def _old(g):
    r = K.cam_path(None, keys(), g)
    return np.array(r["loc"]), np.array(r["look"]), r["lens"], r["vivid"]


def _herm(p0, m0, p1, m1, t):
    t2, t3 = t * t, t * t * t
    return (2 * t3 - 3 * t2 + 1) * p0 + (t3 - 2 * t2 + t) * m0 + (-2 * t3 + 3 * t2) * p1 + (t3 - t2) * m1


def cam_state(g):
    if g <= G_SPLIT:
        loc, look, lens, viv = _old(g); return tuple(loc), tuple(look), lens, viv
    l0, k0, _, v0 = _old(G_SPLIT); l0b, k0b, _, _ = _old(G_SPLIT - 1)
    el, ek = end_landing(); n = float(G_ARR - G_SPLIT)
    t = min((g - G_SPLIT) / n, 1.0)
    m_l0 = (l0 - l0b) * n; m_k0 = (k0 - k0b) * n                         # continue the old velocity (no bump)
    dirv = np.array(ek) - np.array(el); dirv /= np.linalg.norm(dirv)
    m_l1 = dirv * 0.02 * n; m_k1 = np.zeros(3)                      # still creeping up the slope at the cut
    loc = _herm(l0, m_l0, np.array(el), m_l1, t); look = _herm(k0, m_k0, np.array(ek), m_k1, t)
    if g > G_ARR:
        u = (g - G_ARR) / float(G1 - G_ARR); loc = loc + dirv * 0.30 * u + np.array([T_R[0], T_R[1], 0.0]) * 0.30 * u; look = look + np.array([T_R[0], T_R[1], 0.0]) * 0.10 * u
    gz = float(K.ground(loc[0], loc[1])) + 1.3
    if loc[2] < gz: loc[2] = gz
    viv = v0
    return tuple(loc), tuple(look), 22.0, viv


def pose_of(e, g):
    nm, cast, pname, mk, ph = e
    c, p = cast21.STORY21[pname]; p = dict(p)
    p["yaw"] = 0.3
    t = g / 30.0
    p["lean"] = p.get("lean", 0.0) + 3.5 * math.sin(g * 0.10 + ph * 2.1)             # weight shifts: big
    p["head_roll"] = p.get("head_roll", 0.0) + 3.0 * math.sin(g * 0.13 + ph)
    p["blink"] = cast21.blink_at(g, 70 + int(ph * 9), int(ph * 29))
    p["t"] = t
    sw = math.sin(g * 0.17 + ph * 1.3)
    if nm == "s1":                                   # swings his spear: shaft angle sways +-14 deg and the hand follows with a lean
        pr_ = p.get("prop_r")
        if isinstance(pr_, dict): p["prop_r"] = dict(pr_, angle=-90 + 14 * sw)
        p["lean"] += 5 * sw
    if nm == "s2":                                   # leans hard on his spear
        p["lean"] = 11.0 + 2.5 * math.sin(g * 0.06) + 1.5 * math.sin(g * 0.21)
        p["head_roll"] += 5.0
    if nm == "horn":                                 # looks around: slow head turns
        p["yaw"] = 0.3 + 0.55 * math.sin(g * 0.08 + 1.0)
    if nm == "s3" and 392 <= g <= 412:               # scratches his nose (switch hidden behind a blink)
        c2, p2 = cast21.STORY21["scot_c_scratch_nose"]; p2 = dict(p2)
        p2.update(lean=p["lean"], head_roll=p["head_roll"], t=t, blink=1.0 if g in (392, 412) else 0.0, yaw=0.45)
        p = p2
    if nm == "w":                                    # Wallace raises one eyebrow (behind a blink) and holds it
        if g >= 398:
            c2, p2 = cast21.STORY21["wallace_eyebrow"]; p2 = dict(p2); p2.update(lean=p["lean"] * 0.5, t=t, blink=1.0 if g in (398, 399) else p["blink"]); p = p2
    return K.with_rim(p)


class Seg(object):
    def __init__(self):
        t0 = time.time()
        self.A = K.build_world(["camp_wide", "hill_low"], fg=["camp_wide", "hill_low"], over=dict(shaft_k=1.0))
        for o in bpy.data.objects:                         # the set's boxy 3D parade is replaced by the cast cards (as in B1, team 2)
            if o.name.startswith("parade"): o.hide_render = True; o.hide_viewport = True
        self.scene = bpy.context.scene; self.cam = self.scene.camera; self.cam.data.dof.use_dof = False
        self.scene.frame_start, self.scene.frame_end = 1, 2000
        self.acts = {}
        for ob in bpy.data.objects:                       # no fg spear shaft crossing the Scots' faces
            if ob.name.startswith(("fg_generic_steel", "fg_generic_wood")): ob.hide_render = True
        self.marks = {}
        for mk, k, dr in (("s1", -1.0, 0.8), ("s2", -0.7, 0.0), ("w", 0.0, 0.1), ("horn", 0.7, 0.0), ("s3", 1.0, 0.8)):
            p = CTR + U_R * (13.3 + dr) + T_R * k; self.marks[mk] = (float(p[0]), float(p[1]), float(K.ground(p[0], p[1])))
        for nm, cast, pname, mk, ph in STAND:
            self.acts[nm] = C.make_actor(nm, cast, os.path.join(TMP, "sprites"))
        pts = [K.cam_path(None, keys(), g)["loc"] for g in range(G0, 419, 3)]
        print("hidden banners/plumes near the path:", K.hide_near_banners(pts, 15), flush=True)
        self.stage_parade()
        print("B2: built world in %.1f s" % (time.time() - t0), flush=True)

    def stage_parade(self):
        """B1's parade (team 2 message): at g 298 the cast stands exactly where B1 left it; the knights keep walking toward the bridge at 1.35 m/s, the marchers at 1.5 m/s."""
        pr = K.PRESETS["camp_wide"]; left = (-0.439, 0.898); SC = 1.7 / 3.18
        self.SC = SC; self.par = []
        riders = [("r1", "knight_a_mtd", "knight_a_mounted", 31.0, 420, "red"), ("r2", "knight_b_mtd", "knight_b_mounted", 35.0, 340, "red"),
                  ("r3", "knight_a_open_mtd", "knight_a_mounted", 39.0, 270, "gold"), ("r4", "knight_b_great_mtd", "knight_b_mounted", 43.0, 200, "red"),
                  ("r5", "knight_a_mtd", "knight_a_mounted", 47.0, 130, "red"), ("r6", "knight_b_mtd", "knight_b_mounted", 34.0, 470, "gold"),
                  ("r7", "knight_a_open_mtd", "knight_a_mounted", 37.0, 560, "red"), ("r8", "knight_b_great_mtd", "knight_b_mounted", 41.0, 600, "red"),
                  ("r9", "knight_a_mtd", "knight_a_mounted", 45.0, 520, "gold"), ("r10", "knight_b_mtd", "knight_b_mounted", 50.0, 450, "red")]
        def mk(name, cast):
            a = actors.Actor(name, cast); a.build(C.sprites.DEFAULT_CANVAS[cast], os.path.join(TMP, "sprites_par"), contact=True, shadow="proxy"); a.head_flip = False
            return a
        for i, (nm, cast_, base, d, xp, cap) in enumerate(riders):
            x0, y0 = K.at_px(pr, d, xp)
            self.par.append(dict(a=mk(nm, cast_), x0=x0, y0=y0, v=1.35, k=i, base=base, kind="ride", cap=cap))
        foot = [("f1", "footman_a", 50.0, 110, 0), ("f2", "footman_b", 53.0, 190, 1), ("f3", "footman_a", 47.0, 330, 2), ("f4", "footman_b", 55.0, 440, 3),
                ("f5", "footman_a", 51.0, 540, 1), ("f6", "footman_a", 58.0, 610, 2), ("f7", "footman_b", 36.0, 600, 0), ("f8", "footman_a", 33.0, 70, 3),
                ("f9", "footman_a", 41.0, 670, 2), ("f10", "footman_b", 44.0, 380, 1), ("f11", "footman_a", 39.0, 150, 2), ("f12", "footman_b", 46.0, 290, 3)]
        for i, (nm, cast_, d, xp, v) in enumerate(foot):
            x0, y0 = K.at_px(pr, d, xp)
            self.par.append(dict(a=mk(nm, cast_), x0=x0, y0=y0, v=0.0, k=10 + i, base=cast_ + "_stand", kind="idle", var=v + 1, mir=bool(i % 2), cast=cast_))
        for i in range(6):
            cast_ = ("footman_a", "footman_b")[i % 2]; d = 36.0 + 3.0 * i; xp = 90 + 95 * i
            x0, y0 = K.at_px(pr, d, xp)
            self.par.append(dict(a=mk("w%d" % (i + 1), cast_), x0=x0, y0=y0, v=1.5, k=30 + i, kind="walk", var=(i % 3) + 1, cast=cast_))
        self.left = left

    def par_pose(self, m, g):
        S21 = cast21.STORY21; k = m["k"]
        if m["kind"] == "walk":
            p = dict(cast21.walk_spear(m["cast"], ((g + 7 * k) / 28.0) % 1.0, -1, "march")); pass
        elif m["kind"] == "ride":
            p = dict(S21[m["base"]][1]); p.update(gait=((g + 9 * k) / 40.0) % 1.0, t=((g + 13 * k) / 70.0) % 1.0, blink=cast21.blink_at(g, 90 + 5 * k, 13 * k), lean=0.8 * math.sin(g * 0.09 + k), mode21="walk", horse21=m["cap"], mirror=True)
        else:
            p = dict(S21[m["base"]][1]); p.update(lean=1.2 * math.sin(g * 0.071 + k * 1.7), head_roll=1.5 * math.sin(g * 0.053 + k * 2.3), blink=cast21.blink_at(g, 84 + 7 * (k % 9), 11 * k), mirror=m["mir"])
        for kk in ("prop_r", "prop_l"):
            if isinstance(p.get(kk), dict) and p[kk].get("type") == "spear21": p[kk] = dict(p[kk], scale=1.1)
        return K.with_rim(p)

    def plan(self, gs):
        cam = self.cam; self.viv = {}
        for g in gs:
            f = g + 1
            loc, look, lens, viv = cam_state(g); self.viv[g] = viv
            cam.location = loc; cam.rotation_euler = (Vector(look) - Vector(loc)).to_track_quat('-Z', 'Y').to_euler(); cam.data.lens = lens
            cam.keyframe_insert("location", frame=f); cam.keyframe_insert("rotation_euler", frame=f); cam.data.keyframe_insert("lens", frame=f)
            for nm, cast, pname, mk, ph in STAND:
                x, y, z = self.marks[mk][:3]
                self.acts[nm].place(f, (x, y, z), scale=C.SCALE.get(cast, C.CS))
            for m in self.par:
                t = (g - GJ) / 30.0; x, y = m["x0"] + self.left[0] * m["v"] * t, m["y0"] + self.left[1] * m["v"] * t
                m["a"].place(f, (x, y, float(K.ground(x, y))), scale=self.SC)
        for g in gs:
            f = g + 1; self.scene.frame_set(f)
            for e in STAND:
                self.acts[e[0]].pose(f, pose_of(e, g), camera=cam)
            for m in self.par:
                m["a"].pose(f, self.par_pose(m, g), camera=cam)
        for nm, a in self.acts.items():
            a.render_sprites(PPD, frames=[g + 1 for g in gs])
        for m in self.par:
            m["a"].render_sprites(96, frames=[g + 1 for g in gs])

    def render_one(self, g, out, mode="final", samples=32):
        self.scene.frame_set(g + 1); bpy.context.view_layer.update()
        actors.sync_all(self.scene, self.cam)
        t = g / 30.0
        K.set_flutter(t); K.set_smoke(t); K.set_flow(t)
        if self.viv.get(g): K.STATE["vivid"] = self.viv[g]
        return K.render(out, mode, samples)

    def report(self, g):
        self.scene.frame_set(g + 1); K.setup_render(self.scene, "final"); bpy.context.view_layer.update()
        out = {}
        for nm, cast, pname, mk, ph in STAND:
            x, y, z = self.marks[mk][:3]; H = 1.7 if nm != "w" else 1.92
            px, py, dz = K.project(self.cam, (x, y, z + H * 0.9)); out[nm] = (round(px), round(py), round(dz, 1))
        return dict(g=g, cam=[round(v, 1) for v in self.cam.location], heads=out)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "path":
        gs = list(range(G0, G1 + 1, 3)); out = sys.argv[2]
    else:
        gs = [g for g in C.parse(sys.argv[2]) if G0 <= g <= G1]
    Tk = Seg(); Tk.plan(gs)
    if cmd == "path":
        d = os.path.join(HERE, "work", "pathdraft"); os.makedirs(d, exist_ok=True)
        for i, g in enumerate(gs):
            Tk.render_one(g, os.path.join(d, "p_%03d.png" % i), "draft", 8); print(json.dumps(Tk.report(g)), flush=True)
        subprocess.check_call(["ffmpeg", "-y", "-v", "error", "-framerate", "10", "-i", os.path.join(d, "p_%03d.png"), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "20", out])
    elif cmd == "stills":
        out = sys.argv[3]; mode = sys.argv[4] if len(sys.argv) > 4 else "draft"; samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        os.makedirs(out, exist_ok=True)
        for g in gs:
            dt = Tk.render_one(g, os.path.join(out, "b2_g_%04d.png" % g), mode, samples); print(json.dumps(Tk.report(g)), "%.1fs" % dt, flush=True)
    elif cmd == "final":
        samples = int(sys.argv[3]) if len(sys.argv) > 3 else 32
        out = os.path.join(HERE, "raw"); os.makedirs(out, exist_ok=True)
        for g in gs:
            png = os.path.join(out, "g_%04d.png" % g)
            if os.path.exists(png) and os.path.exists(png[:-4] + ".json"): continue
            dt = Tk.render_one(g, png, "final", samples); rep = Tk.report(g); rep.update(wall=round(dt, 1), samples=samples)
            json.dump(rep, open(png[:-4] + ".json", "w")); print("B2 g %d %.1f s" % (g, dt), flush=True)
