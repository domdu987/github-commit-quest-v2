#!/usr/bin/env python3
"""shot.py -- film 21 take s05 (nickname): shots 13 + 14, g 787..890 (g 793..884 + 6 handle frames each side; cut in).

    id 13  g 787..836  camp_wide: the English camp laughs and points across the river at the hill (screen-left); one footman mimes
                       hoeing with his spear.  Pull-out ~7 %/s + a slide of ~50 px/s (the scene slides left), bounce 3 Hz.
    id 14  g 837..890  hill_eye: punch-in cut on the Scots line.  Drift push 5 %/s + slide 40 px/s; on "พวกไอ้ชาวนา" (g 849) a snap push
                       (14 f, x1.3), 2-frame shake and 6 frames of speed lines; the Scots are unbothered; Wallace raises one eyebrow.

    python3 shot.py probe 13|14 a:b[:step]
    python3 shot.py stills 13|14 a:b[:step] <out_dir> [draft|final] [samples]
    python3 shot.py final 13|14 a:b[:step] [samples]
One location per process: run shot 13 and shot 14 as separate processes.
"""
import math, os, sys, json, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c21 as C                                          # noqa: E402
import cast21, bpy, numpy as np                          # noqa: E402,E401
from c21 import K, actors, camrig, Vector, lerp, ez      # noqa: E402
from PIL import Image, ImageDraw                          # noqa: E402

TMP = os.path.join(HERE, "work")
G_CUT = 837
RANGES = {13: (787, 836), 14: (837, 890)}
PRESET = {13: "camp_wide", 14: "hill_eye"}
G_NICK = C.g_of(28.19)       # 849: "พวกไอ้ชาวนา"
PPD = {13: 96, 14: 160}


def f_of(g):
    return int(g) + 1


# ============================================================================ cameras
CAM13 = dict(cam=(-60.0, -86.0, 8.5), look=(12.0, -52.0, -4.0), lens=22.0)     # preset camp_wide moved ~14 m forward, 3.5 m lower, tilted down


def cam13(g):
    """camp_wide (moved forward): pull-out 7 %/s from the group, scene slides left (camera dollies right) ~50 px/s at the group."""
    pr = CAM13
    c0, l0 = Vector(pr["cam"]), Vector(pr["look"])
    t = (g - RANGES[13][0]) / 30.0
    rv = C.right_vec(c0, l0)
    fwd = Vector((l0.x - c0.x, l0.y - c0.y, 0)).normalized()
    dist = (Vector(GROUP) - c0).length
    back = 0.07 * dist * t * (1.0 + 0.10 * math.sin(t * 2.2))      # a little breathing so the speed is never flat
    slide = 50.0 * dist / 782.0 * t
    loc = c0 - fwd * back + rv * slide + Vector((0, 0, 0.5 * t))
    look = l0 + rv * slide
    return loc, look


GROUP = (-22.0, -60.0, 0.0)      # centre of the laughing group (set at build time)


def cam14(g):
    """hill_eye: drift push 5 %/s toward Wallace + slide 40 px/s (camera dollies right), snap push x1.3 on the nickname, shake 2 f."""
    pr = K.PRESETS["hill_eye"]
    c0, l0 = Vector(pr["cam"]), Vector(pr["look"])
    rv = C.right_vec(c0, l0)
    d0 = Vector(pr["cam"]) ; tgt = Vector(WTGT)
    t = (g - G_CUT) / 30.0
    fwd = (tgt - c0); fwd_h = Vector((fwd.x, fwd.y, 0)).normalized(); dist = fwd.length
    push = 0.05 * dist * t
    # snap push: eased 14 frames, x1.3 about Wallace
    u = min(max((g - G_NICK) / 14.0, 0.0), 1.0)
    sn = (u * u * (3 - 2 * u)) * (1.0 - 1.0 / 1.2) * (dist - push)
    toward = (tgt - c0).normalized()
    lat = -0.26 + 0.29 * t
    loc = c0 + toward * (push + sn) + rv * lat
    look = l0 + rv * lat + toward * (push + sn)
    # 2-frame shake on the nickname
    if g == G_NICK:
        look = look + rv * 0.16 + Vector((0, 0, 0.10))
    elif g == G_NICK + 1:
        look = look - rv * 0.12 - Vector((0, 0, 0.07))
    return loc, look


WTGT = (0, 0, 0)

# ============================================================================ cast
def sway(g, ph, a=1.0):
    return a * math.sin(g * 0.11 + ph)


def idle(p, g, ph, amp=1.0, blink_period=95):
    p = dict(p)
    p["lean"] = p.get("lean", 0.0) + 1.3 * amp * math.sin(g * 0.09 + ph)
    p["head_roll"] = p.get("head_roll", 0.0) + 1.6 * amp * math.sin(g * 0.13 + ph * 1.7)
    p["blink"] = cast21.blink_at(g, blink_period, int(ph * 40))
    p["t"] = g / 30.0
    return p


def S(name, **kw):
    cast, pose = cast21.STORY21[name]
    p = dict(pose); p.update(kw)
    return cast, p


# ============================================================================ the take
class Take(object):
    def __init__(self, shot, quality="final"):
        global GROUP, WTGT
        t0 = time.time()
        self.shot = shot
        self.A = K.build_for_cli(PRESET[shot], placeholders=False)
        self.scene = bpy.context.scene
        self.cam = self.scene.camera
        self.cam.data.dof.use_dof = False
        self.scene.frame_start, self.scene.frame_end = 1, 2000
        self.acts = {}
        self.script = {}
        self.pr = K.PRESETS[PRESET[shot]]
        os.makedirs(TMP, exist_ok=True)
        if shot == 13:
            self.build13()
        else:
            self.build14()
        print("take: built %s in %.1f s" % (PRESET[shot], time.time() - t0), flush=True)

    # ---- shot 13 ---------------------------------------------------------------------------------------------------
    def build13(self):
        global GROUP
        pr = CAM13
        bpy.data.objects["cam"].location = pr["cam"]
        # (name, cast, pose name, d, px, flip, phase, kind)  d = metres ahead of the first-frame camera, px = screen x at that frame
        L = [("f1", "footman_a_v1", "footman_a_point_laugh", 19.0, 200, True, 0.0, "laugh"),
             ("f2", "footman_b_v2", "footman_b_point_laugh", 24.0, 290, True, 0.33, "laugh"),
             ("k1", "knight_a_open", "knight_a_open_point_laugh", 21.0, 385, True, 0.62, "laugh"),
             ("hoe", "footman_a", "footman_a_mime_hoe", 17.0, 470, False, 0.15, "hoe"),
             ("f3", "footman_b", "footman_b_point_laugh", 26.0, 540, True, 0.8, "laugh"),
             ("k2", "knight_b_great", "knight_b_great_laughing", 28.0, 235, False, 0.5, "laugh"),
             ("f4", "footman_a_v2", "footman_a_laughing", 22.0, 620, False, 0.95, "laugh"),
             ("f5", "footman_b_v1", "footman_b_point_laugh", 30.0, 440, True, 0.22, "laugh"),
             ("f6", "footman_a_v3", "footman_a_point_laugh", 25.0, 110, True, 0.45, "laugh"),
             ("f7", "knight_a", "knight_a_point_laugh", 31.0, 330, True, 0.7, "laugh")]
        self.L13 = []
        for nm, cast, pose, d, xp, flip, ph, kind in L:
            x, y = K.at_px(pr, d, xp)
            z = float(K.ground(x, y))
            a = C.make_actor(nm, cast, os.path.join(TMP, "sprites13"))
            self.acts[nm] = a
            self.L13.append(dict(nm=nm, cast=cast, pose=pose, xyz=(x, y, z), flip=flip, ph=ph, kind=kind))
        xs = [e["xyz"] for e in self.L13]
        GROUP = tuple(np.mean(np.array(xs), axis=0))
        # the preset foreground (rope, pole) belongs to the preset camera: hide it and put the same props 1.8 / 2.2 m from the moved lens
        for ob in bpy.data.objects:
            if ob.name.startswith("fg_generic"):
                ob.hide_render = True
        K.fg_generic(self.A, dict(CAM13, fg_list=[("rope", 1.8, 60), ("pole", 2.2, 650)], fg_seed=41, name="fg13"))
        # solve the look-at height so the group's heads land at screen y ~ 680 at the first frame
        K.setup_render(self.scene, "final")
        hp = Vector((GROUP[0], GROUP[1], GROUP[2] + 1.4))
        lo, hi = -40.0, 30.0
        for _ in range(30):
            mid = 0.5 * (lo + hi)
            CAM13["look"] = (CAM13["look"][0], CAM13["look"][1], mid)
            C.key_cam(self.cam, 1, CAM13["cam"], CAM13["look"]); self.scene.frame_set(1); bpy.context.view_layer.update()
            y = K.project(self.cam, hp)[1]
            if y > 690: hi = mid          # head too low on screen: aim lower (moves the head up)
            else: lo = mid
        print("look z solved", CAM13["look"], flush=True)

    # ---- shot 14 ---------------------------------------------------------------------------------------------------
    def build14(self):
        global WTGT
        pr = self.pr
        m = self.A["marks"]
        for ob in bpy.data.objects:                      # QA-art notes for hill_eye: no black bars, no pink dome
            if ob.name.startswith(("fg_generic_steel", "fg_generic_wood", "fg_generic_r_heather")):
                ob.hide_render = True
        # one spear leaning in from the right edge (d 2.6 m, xp 690)
        B = K.Batch(96); x, y = K.at_px(pr, 2.6, 690); K.spear(B, (x, y, float(K.ground(x, y))), tilt=(-0.25, 0.1), h=3.4); B.finalize('fg_team')
        WTGT = tuple(m["w"][:3])
        # compress the line (the snap push x1.2 + drift would crop s1 / s4 at the preset spacing): same depths, closer in x
        PX = dict(s1=185, s2=277, w=370, s3=466, s4=552); DD = dict(s1=5.2, s2=6.0, w=5.6, s3=6.4, s4=5.4)
        for k in PX:
            x_, y_ = K.at_px(pr, DD[k], PX[k]); m[k] = (x_, y_, float(K.ground(x_, y_)), m[k][3], m[k][4])
        spec = [("s1", "scot_c", "scot_c_fold_spear", "s1", 0.0), ("s2", "scot_b", "scot_b_chew_grass", "s2", 0.4),
                ("w", "wallace", "wallace_calm", "w", 0.8), ("s3", "scot_a", "scot_a_fold_spear", "s3", 1.3),
                ("s4", "scot_a_v1", "scot_a_stand_still", "s4", 2.1)]
        self.L14 = []
        for nm, cast, pose, mk, ph in spec:
            a = C.make_actor(nm, cast, os.path.join(TMP, "sprites14"))
            self.acts[nm] = a
            self.L14.append(dict(nm=nm, cast=cast, pose=pose, xyz=tuple(m[mk][:3]), ph=ph))

    # ---- per-frame plan ---------------------------------------------------------------------------------------------
    def plan(self, gs):
        cam = self.cam
        camf = cam13 if self.shot == 13 else cam14
        for g in gs:
            f = f_of(g)
            loc, look = camf(g)
            C.key_cam(cam, f, loc, look)
            if self.shot == 13:
                for e in self.L13:
                    p, dy = self.pose13(e, g)
                    x, y, z = e["xyz"]
                    sc = C.SCALE.get(e["cast"], C.CS)
                    self.acts[e["nm"]].place(f, (x, y, z + dy * sc), scale=sc, flip=e["flip"])
                    self.script[(e["nm"], g)] = p
            else:
                for e in self.L14:
                    p = self.pose14(e, g)
                    x, y, z = e["xyz"]
                    sc = C.SCALE.get(e["cast"].split("_v")[0], C.CS)
                    self.acts[e["nm"]].place(f, (x, y, z), scale=sc)
                    self.script[(e["nm"], g)] = p
        for g in gs:
            f = f_of(g)
            self.scene.frame_set(f)
            for e in (self.L13 if self.shot == 13 else self.L14):
                self.acts[e["nm"]].pose(f, self.script[(e["nm"], g)], camera=cam)
        for nm, a in self.acts.items():
            a.render_sprites(PPD[self.shot], frames=[f_of(g) for g in gs])

    def pose13(self, e, g):
        cast, base = S(e["pose"])
        base = dict(base)
        ph = e["ph"]
        if e["kind"] == "hoe":
            u = g * 0.42 + ph * 6.0                          # the chop: spear swings down on the beat, a swing up on the way back
            base["lean"] = 7 + 9 * max(0.0, math.sin(u)) - 3 * max(0.0, -math.sin(u))
            base["prop_r"] = dict(base["prop_r"], angle=62 + 22 * math.sin(u - 0.6))
        else:
            base["arm_r"] = dict(base["arm_r"], hand=(base["arm_r"]["hand"][0], base["arm_r"]["hand"][1] + 0.05 * math.sin(g * 0.5 + ph * 9))) if "arm_r" in base and isinstance(base["arm_r"], dict) and "hand" in base["arm_r"] else base.get("arm_r")
        p, dy = cast21.laugh(base, g, phase=ph)
        p["t"] = g / 30.0
        return p, dy

    def pose14(self, e, g):
        nm, ph = e["nm"], e["ph"]
        cast, base = S(e["pose"])
        p = idle(base, g, ph, amp=0.8, blink_period=88 + int(ph * 7))
        if nm == "w":
            # eyebrow on the nickname (g 849), reaction delay ~4 f, changes sit behind a blink
            if g >= G_NICK + 3:
                _, pe = S("wallace_eyebrow")
                p = idle(pe, g, ph, amp=0.6)
                p["blink"] = cast21.blink_at(g, 120, 0) if g > G_NICK + 12 else (1.0 if G_NICK + 3 <= g <= G_NICK + 4 else 0.0)
            else:
                p["blink"] = 1.0 if G_NICK + 1 <= g <= G_NICK + 2 else p.get("blink", 0.0)
        return p

    # ---- render ---------------------------------------------------------------------------------------------------------
    def render_one(self, g, out_png, mode="final", samples=24):
        f = f_of(g)
        self.scene.frame_set(f)
        actors.sync_all(self.scene, self.cam)
        t = g / 30.0
        K.set_flutter(t); K.set_smoke(t); K.set_flow(t)
        dt = K.render(out_png, mode, samples)
        speed_lines(out_png, g) if self.shot == 14 else None
        return dt

    def report(self, g):
        f = f_of(g); self.scene.frame_set(f); K.setup_render(self.scene, 'final'); bpy.context.view_layer.update()
        out = {}
        for e in (self.L13 if self.shot == 13 else self.L14):
            a = self.acts[e["nm"]]
            x, y, z = e["xyz"]
            sc = a.root.scale.x
            H = 1.7 * (sc / C.CS)
            px, py, dz = K.project(self.cam, (x, y, z + H * 0.9))
            out[e["nm"]] = (round(px), round(py), round(dz, 1))
        loc = self.cam.location
        return dict(g=g, cam=[round(v, 2) for v in loc], heads=out)


def speed_lines(path, g):
    """6 frames of speed lines on the nickname (g 849..854): tapered cream wedges + a few plum hairlines radiating from the Scots,
    new random set every frame."""
    if not (G_NICK <= g < G_NICK + 6):
        return
    im = Image.open(path).convert("RGB")
    W, H = im.size
    k = W / 720.0
    ov = Image.new("RGBA", im.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    rs = np.random.RandomState(100 + g)
    cx, cy = 360 * k, 640 * k
    n = 46
    for i in range(n):
        ang = (i + rs.uniform(-0.4, 0.4)) / n * 2 * math.pi
        r0 = rs.uniform(300, 430) * k
        r1 = rs.uniform(760, 980) * k
        w = rs.uniform(0.012, 0.05)
        c, s = math.cos(ang), math.sin(ang)
        p0 = (cx + c * r0, cy + s * r0 * 1.15)
        pa = (cx + math.cos(ang - w) * r1, cy + math.sin(ang - w) * r1 * 1.15)
        pb = (cx + math.cos(ang + w) * r1, cy + math.sin(ang + w) * r1 * 1.15)
        col = (255, 246, 222, 235) if i % 4 else (58, 40, 50, 215)
        d.polygon([p0, pa, pb], fill=col)
    im = Image.alpha_composite(im.convert("RGBA"), ov).convert("RGB")
    im.save(path)


# ============================================================================ commands
def parse(spec):
    return C.parse(spec)


if __name__ == "__main__":
    cmd, shot = sys.argv[1], int(sys.argv[2])
    gs = [g for g in parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
    Tk = Take(shot)
    Tk.plan(gs)
    if cmd == "probe":
        for g in gs:
            print(json.dumps(Tk.report(g)), flush=True)
    elif cmd == "stills":
        out = sys.argv[4]; mode = sys.argv[5] if len(sys.argv) > 5 else "draft"; samples = int(sys.argv[6]) if len(sys.argv) > 6 else 12
        os.makedirs(out, exist_ok=True)
        for g in gs:
            dt = Tk.render_one(g, os.path.join(out, "s%d_g_%04d.png" % (shot, g)), mode, samples)
            print(json.dumps(Tk.report(g)), "%.1fs" % dt, flush=True)
    elif cmd == "final":
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else 24
        out = os.path.join(HERE, "raw", "s%d" % shot); os.makedirs(out, exist_ok=True)
        for g in gs:
            png = os.path.join(out, "g_%04d.png" % g)
            if os.path.exists(png) and os.path.exists(png[:-4] + ".json"):
                continue
            dt = Tk.render_one(g, png, "final", samples)
            rep = Tk.report(g); rep.update(wall=round(dt, 1), samples=samples)
            json.dump(rep, open(png[:-4] + ".json", "w"))
            print("shot %d g %d %.1f s" % (shot, g, dt), flush=True)
