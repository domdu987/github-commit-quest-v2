#!/usr/bin/env python3
"""shot.py -- film 17 take s04: shots 9-12 (narration 14.72-21.61 s), g0 445 .. g1 651 (exclusive) + 6 handle frames each side (439..656).
One location (measure, DAY_INT), four set-ups, all hard cuts (transition_in cut):
  id 9   g 439..492  measure_wide : inspector strides in from the door, sees Bertillon measuring an ear, bursts out laughing (467 = 15.46 s, bounce
                     3 Hz, gendarmes join).  Push-in + slide; kepi stool / crates foreground.
  id 10  g 493..539  measure_low  : "วัดหูโจรเนี่ยนะ!" lip-sync (16.32 s), inspector near, points at the calipers; Bertillon behind, unmoved.
  id 11  g 540..591  measure_chair: "ถ้าเอ็งใช้คีมนั่นจับโจรเก่าได้สักคน" inspector flicks the calipers; slide.
  id 12  g 592..656  measure_chair: snap push-in (20 f, x1.5) on the inspector tapping his own ear "ข้าจะนั่งให้เอ็งวัดหูข้าเองเลย!".
Lips move only g 493..650 (16.32-21.59 s narration + 0.10 s).  Blender frame = g.
    python3 shot.py probe a:b[:s]        python3 shot.py stills a:b[:s] out [scale] [samples]        python3 shot.py final a:b[:s] [scale] [samples]
"""
import os, sys, math, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c17 as C
from c17 import K, cast17, actors, camrig, sprites, render, puppet, Vector, lerp, clamp, sm, sine, mix3
TMP = os.path.join(HERE, "work")

G0, G1, HIN, HOUT = 445, 651, 6, 6
FIRST, LAST = G0 - HIN, G1 + HOUT - 1                       # 439 .. 656
B9, B10, B11, B12 = 445, 493, 540, 592
RANGES = {9: (FIRST, B10 - 1), 10: (B10, B11 - 1), 11: (B11, B12 - 1), 12: (B12, LAST)}
G_LAUGH = C.g_of(15.46) - 1                                # 466: the laugh bursts (15.46 s)
G_SPEAK0, G_SPEAK1 = C.g_of(16.32), C.g_of(21.59)          # lips 493 .. 650
def shot_of(g):
    for s, (a, b) in RANGES.items():
        if a <= g <= b: return s

# ---------------------------------------------------------------- cameras: waypoints (g, loc, look, kind); kind = ease of the segment that STARTS there
S = lambda *a: tuple(a)
CAMS = {
    9: [(439, S(-2.30, -3.60, 1.50), S(0.60, 1.10, 1.30), "d"), (468, S(-1.95, -3.30, 1.50), S(0.70, 1.15, 1.30), "s"),
        (480, S(-0.95, -2.05, 1.50), S(0.75, 1.30, 1.30), "d"), (492, S(-0.55, -1.65, 1.50), S(0.90, 1.30, 1.30), "d")],
    10: [(493, S(0.15, 0.30, 0.50), S(0.55, 2.4, 1.50), "d"), (512, S(0.32, 0.44, 0.50), S(0.70, 2.4, 1.50), "s"),
         (522, S(0.22, 0.74, 0.50), S(0.52, 2.4, 1.60), "d"), (539, S(0.28, 0.80, 0.50), S(0.56, 2.4, 1.62), "d")],
    11: [(540, S(2.25, 0.05, 1.50), S(0.55, 2.4, 1.30), "d"), (562, S(1.95, 0.22, 1.50), S(0.45, 2.4, 1.30), "s"),
         (574, S(1.50, 0.50, 1.50), S(0.55, 2.3, 1.30), "d"), (591, S(1.40, 0.60, 1.48), S(0.45, 2.3, 1.30), "d")],
    12: [(592, S(1.75, 0.35, 1.50), S(0.70, 1.60, 1.38), "d"), (604, S(1.72, 0.38, 1.50), S(0.72, 1.60, 1.38), "s"),
         (617, S(1.48, 0.68, 1.48), S(0.80, 1.60, 1.38), "d"), (632, S(1.50, 0.70, 1.47), S(0.84, 1.60, 1.38), "s"), (644, S(1.92, 0.76, 1.47), S(1.05, 1.60, 1.38), "d"), (656, S(1.98, 0.78, 1.47), S(1.08, 1.60, 1.38), "d")],
}
LENS = 22.0


def ease(kind, u):
    if kind == "s": return sm(u)
    return 0.35 * sine(u) + 0.65 * clamp(u, -1.0, 2.0) if 0 <= u <= 1 else u


def cam_of(g):
    wps = CAMS[shot_of(g)]
    i = 0
    while i < len(wps) - 2 and g >= wps[i + 1][0]: i += 1
    a, b = wps[i], wps[i + 1]
    u = (g - a[0]) / float(b[0] - a[0])
    e = ease(a[3], u)
    loc = mix3(a[1], b[1], e); look = mix3(a[2], b[2], e)
    am = 0.07 if shot_of(g) == 9 else 0.035
    loc = (loc[0] + am * math.sin(2 * math.pi * g / 37.0), loc[1] + 0.5 * am * math.sin(2 * math.pi * g / 29.0), loc[2] + 0.4 * am * math.sin(2 * math.pi * g / 23.0))
    return loc, look


# ---------------------------------------------------------------- staging
CHAIR = (0.7, 2.3); H = K.CAST_H; HD = K.CAST_HD
INS_WALK = [(439, (2.6, -1.35)), (462, (0.55, -0.35)), (466, (0.5, -0.33))]       # in at the door, stops, laughs
INS_S10 = (0.12, 1.95); INS_S11 = (0.85, 1.45); INS_S12 = (0.85, 1.45)
BERT = {9: (-0.15, 2.15), 10: (1.55, 2.55), 11: (1.34, 2.34), 12: (1.34, 2.34)}


def lerp_path(pts, g):
    if g <= pts[0][0]: return pts[0][1]
    for (g0, p0), (g1, p1) in zip(pts, pts[1:]):
        if g <= g1:
            u = (g - g0) / float(g1 - g0); return (lerp(p0[0], p1[0], u), lerp(p0[1], p1[1], u))
    return pts[-1][1]


def bounce(g, amp=0.06 * 1.7, hz=3.0, ph=0.0):
    return amp * abs(math.sin(math.pi * hz * g / 30.0 + ph))


def rim(p, cast):
    c = K.RIM_FOR.get(cast)
    if c: p["rim"] = c; p["rim_opacity"] = 0.55; p["rim_w"] = 0.02
    return p


def speak(p, g):
    lvl = 0.85 + 0.15 * math.sin(g * 0.37)
    return cast17.speak(p, g, lvl) if G_SPEAK0 <= g <= G_SPEAK1 else cast17.silent(p)


def story(name, **kw):
    cast, p = cast17.STORY17[name]; p = dict(p); p.update(kw); return cast, p


def pose_ins(g):
    """(pose, floor xy, z lift) of the inspector at film frame g."""
    s = shot_of(g)
    if s == 9:
        xy = lerp_path(INS_WALK, g)
        if g < 462:                                           # striding in
            ph = (g - 439) / 30.0 * 1.9
            cast, base = story("inspector_arms_crossed")
            p = cast17.cycle("inspector17", ph, "march", 1, base=dict(base, arm_r="down", arm_l="down"))
            p.update(yaw=0.55, expr="smug", pitch=-0.2)
            return speak(p, g), xy, 0.0
        cast, a = story("inspector_arms_crossed"); cast, l = story("inspector_laughing")
        if g < G_LAUGH:                                            # stops, sees the ear: shock (pointing finger) then the first snort
            cast, pm = story("inspector_pointing_mock")
            u = sm((g - 462) / 4.0) if g >= 462 else 0.0
            p = dict(pm, expr="surprised", mouth="flat", arm_r=dict(pm["arm_r"], hand=(0.9, 0.05)))
            p["lean"] = 2.0 * math.sin(g * 0.3); p["head_roll"] = 8 + 2 * math.sin(g * 0.21)
            return speak(p, g), xy, 0.0
        u = sm((g - G_LAUGH) / 5.0)
        p = dict(l); p["lean"] = -8 + 3 * math.sin(g * 0.5); p["t"] = g / 30.0
        p["squash"] = (1.0 + 0.03 * abs(math.sin(math.pi * 3.0 * g / 30.0)), 1.0 - 0.03 * abs(math.sin(math.pi * 3.0 * g / 30.0)))
        return p, xy, bounce(g) * u
    cast, p = story("inspector_pointing_mock")
    if s == 10:
        p["arm_r"] = dict(p["arm_r"], hand=(1.15 + 0.05 * math.sin(g * 0.3), 0.10 + 0.04 * math.sin(g * 0.4)))
        p["head_roll"] = 6 + 3 * math.sin(g * 0.23); p["lean"] = -3 + 2 * math.sin(g * 0.31); p["yaw"] = 0.3
        p["expr"] = "smug"
        return speak(p, g), INS_S10, 0.0
    if s == 11:
        k = math.sin((g - B11) * 0.55)                              # the flick at the calipers
        p["arm_r"] = dict(p["arm_r"], hand=(1.05 + 0.10 * k, 0.05 + 0.10 * math.cos((g - B11) * 0.55)))
        p["head_roll"] = -5 + 3 * math.sin(g * 0.2); p["lean"] = 4 + 2 * math.sin(g * 0.33); p["yaw"] = 0.35; p["expr"] = "smug"
        return speak(p, g), INS_S11, 0.0
    # shot 12: taps his own ear, chest out
    ph = (g - B12)
    tap = 0.05 * math.sin(ph * 0.9)
    p.update(yaw=0.15, expr="smug", pitch=-0.45, lean=-9 + 1.5 * math.sin(g * 0.3), head_roll=-4 + 2 * math.sin(g * 0.25),
             arm_r=dict(hand=(0.54 + tap, 0.02 + tap), bend=0.2, shape="point", stretch=1.0, layer="front"),
             arm_l="akimbo")
    return speak(p, g), INS_S12, 0.0


def pose_bert(g):
    s = shot_of(g)
    cast, p = story("bertillon_measuring")
    sway = 1.2 * math.sin(g * 0.13)
    p = dict(p, lean=p.get("lean", 4) + sway, blink=cast17.blink_at(g, 83, 11), t=g / 30.0)
    if s == 9:
        p["gaze"] = (0.8, 0.2); p["yaw"] = 0.5
        p["arm_r"] = dict(p["arm_r"], hand=(0.88 + 0.015 * math.sin(g * 0.5), 0.34))
    else:                                                          # behind, unmoved: calipers held, eyes on the inspector
        p["expr"] = "determined"; p["gaze"] = (0.7, 0.1) if s != 12 else (0.7, 0.1)
        p["arm_r"] = dict(p["arm_r"], hand=(0.88 + 0.01 * math.sin(g * 0.4), 0.45))
        if s in (11, 12): p["mirror"] = False
    return cast17.silent(p), BERT[s], 0.0


class Take(object):
    def __init__(self, quality="draft"):
        import bpy
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.A = K.build(preset="measure_chair")
        self.fg_all = {}
        before = set(bpy.data.objects.keys())
        K.fg_measure_wide(self.A); self.fg_wide = [bpy.data.objects[k] for k in set(bpy.data.objects.keys()) - before]
        before = set(bpy.data.objects.keys())
        K.fg_measure_low(self.A); self.fg_low = [bpy.data.objects[k] for k in set(bpy.data.objects.keys()) - before]
        K.clear_keys()
        for o in bpy.data.objects:                              # director fix: additive light shafts wash over the cast cards -> hidden
            if any(m and m.name.startswith('beam_fx') for m in getattr(o.data, 'materials', []) or []): o.hide_render = True
        self.cam = bpy.context.scene.camera
        self.cam.data.dof.use_dof = False; self.cam.data.clip_start = 0.02
        self.scene = bpy.context.scene
        self.scene.frame_start, self.scene.frame_end = 1, 9000
        sd = os.path.join(TMP, "sprites"); os.makedirs(sd, exist_ok=True)
        self.sd = sd
        def mk(name, cast):
            a = actors.Actor(name, cast); a.build(sprites.DEFAULT_CANVAS[cast], sd, contact=True); a.head_flip = True; return a
        self.act = dict(ins=mk("ins", "inspector17"), bert=mk("bert", "bertillon"), pris=mk("pris", "prisoner_b"), pa=mk("pa", "prisoner_a"),
                        gA=mk("gA", "gendarme_a"), gB=mk("gB", "gendarme_b"))
        self.anch = {}; self.heads = {}

    def stand(self, key, cast, pose, xy, lift, f, seated=None):
        a = self.act[key]
        fx, fy = sprites.feet_of(cast, pose)
        sc = H[cast] / HD[cast]
        z = 0.0
        if seated: z = K.HEAD_Z[seated] - sc * fy
        a.place(f, (xy[0], xy[1], z + lift), scale=sc)
        return a

    def pose(self, gs):
        cam = self.cam
        for g in gs:
            f = g
            loc, look = cam_of(g)
            camrig.key_camera(f, Vector(loc), Vector(look), lens=LENS, cam=cam, interp="LINEAR", easing="AUTO")
            s = shot_of(g)
            C.key_hide(self.fg_wide, f, s != 9); C.key_hide(self.fg_low, f, s != 10)
        K.key_life(min(gs), max(gs), dust=0.5)
        plan = {}
        for g in gs:
            f = g; s = shot_of(g); vis = {}
            p, xy, lift = pose_ins(g); p = rim(dict(p), "inspector17")
            self.stand("ins", "inspector17", p, xy, lift, f); vis["ins"] = (p, "inspector17")
            p, xy, lift = pose_bert(g); p = rim(dict(p), "bertillon")
            self.stand("bert", "bertillon", p, xy, lift, f); vis["bert"] = (p, "bertillon")
            if s == 9:
                cast, p = story("prisoner_sitting_b"); p = dict(p, seat17=None, blink=cast17.blink_at(g, 97, 5), lean=1.0 * math.sin(g * 0.15), t=g / 30.0)
                self.stand("pris", "prisoner_b", p, CHAIR, 0.0, f, seated="chair"); vis["pris"] = (cast17.silent(p), "prisoner_b")
                cast, p = story("prisoner_sitting_a"); p = dict(p, seat17=None, blink=cast17.blink_at(g, 101, 40), t=g / 30.0)
                self.stand("pa", "prisoner_a", p, (-2.35, 0.85), 0.0, f, seated="bench"); vis["pa"] = (cast17.silent(p), "prisoner_a")
                lau = g >= G_LAUGH + 3
                cast, p = story("gendarme_laughing_a" if lau else "gendarme_standing_a")
                p = dict(p, blink=cast17.blink_at(g, 89, 3), t=g / 30.0)
                if lau: p["lean"] = -6 + 3 * math.sin(g * 0.45)
                self.stand("gA", "gendarme_a", p, (1.75, 1.35), bounce(g, ph=0.8) if lau else 0.0, f); vis["gA"] = (p, "gendarme_a")
                cast, p = story("gendarme_laughing_b" if g >= G_LAUGH + 7 else "gendarme_standing_b")
                p = dict(p, blink=cast17.blink_at(g, 79, 9), t=g / 30.0)
                if g >= G_LAUGH + 7: p["lean"] = -6 + 3 * math.sin(g * 0.4)
                self.stand("gB", "gendarme_b", p, (2.45, 0.9), bounce(g, ph=2.0) if g >= G_LAUGH + 7 else 0.0, f); vis["gB"] = (p, "gendarme_b")
            for k, a in self.act.items():
                C.key_hide(a.objects(), f, k not in vis)
            for k, (p, cast) in vis.items():
                self.scene.frame_set(f)
                hands = None
                if k == "bert" and s == 9:
                    cl = Vector(cam_of(g)[0]); rv = (Vector(cam_of(g)[1]) - cl); rv = Vector((rv.y, -rv.x, 0)).normalized()
                    ear = Vector((CHAIR[0], CHAIR[1], K.HEAD_Z["chair"])) - rv * 0.30 + (cl - Vector((CHAIR[0], CHAIR[1], cl.z))).normalized() * 0.05
                    hands = {"r": {"tip": tuple(ear), "prop": "calipers"}}
                self.act[k].pose(f, p, hands=hands, camera=cam)
            plan[g] = vis
        for g in gs:
            pass
        for s in sorted(set(shot_of(g) for g in gs)):
            fr = [g for g in gs if shot_of(g) == s]
            ppd = {9: 256, 10: 448, 11: 384, 12: 512}[s]
            for k, a in self.act.items():
                fk = [g for g in fr if k in plan[g]]
                if fk:
                    for g, r in zip(fk, a.render_sprites(ppd, frames=fk)):
                        self.anch[(k, g)] = r["anchors"]
                        if r.get("clipped"): print("WARNING clipped", k, g, flush=True)

    def report(self, g):
        self.scene.frame_set(g)
        out = {}
        for k, a in self.act.items():
            if a.card.hide_render or (k, g) not in self.anch: continue
            hx, hy = self.anch[(k, g)]["head"]
            fe = a.feet.get(g)
            w0 = actors.local_to_world(a, (hx, hy), g, fe, camera=self.cam); w1 = actors.local_to_world(a, (hx + 0.5, hy), g, fe, camera=self.cam)
            c = K.project(self.cam, tuple(w0)); r = K.project(self.cam, tuple(w1))
            out[k] = dict(x=round(c[0]), y=round(c[1]), r=round(math.hypot(r[0] - c[0], r[1] - c[1])))
        return dict(g=g, shot=shot_of(g), heads=out)

    def render(self, gs, out_dir, scale=1.0, samples=12, threads=2):
        K.setup_render(self.scene, "final", samples)
        K.STATE["scale"] = scale
        res = render.render_frames(list(gs), out_dir, scale=scale, threads=threads, scene=self.scene, camera=self.cam, verbose=False)
        for st in res: K.grade(st["path"], scale=scale)
        return res


def run(cmd, gs, a):
    T = Take()
    T.pose(gs)
    for g in gs:
        print(json.dumps(T.report(g)), flush=True)
    if cmd == "stills":
        out = a[0]; scale = float(a[1]) if len(a) > 1 else 0.5; samples = int(a[2]) if len(a) > 2 else 6
        os.makedirs(out, exist_ok=True)
        for g in gs:
            st = T.render([g], out, scale, samples)[0]; os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
            print("g %d %.1f s wall" % (g, st["wall"]), flush=True)
    elif cmd == "final":
        scale = float(a[0]) if a else 1.0; samples = int(a[1]) if len(a) > 1 else 12
        out = os.path.join(HERE, "raw_%d" % int(scale * 720)); os.makedirs(out, exist_ok=True)
        for g in gs:
            png = os.path.join(out, "g_%04d.png" % g)
            if os.path.exists(png): continue
            st = T.render([g], out, scale, samples)[0]; os.replace(st["path"], png)
            json.dump(T.report(g), open(png[:-4] + ".json", "w"))
            print("g %d %.1f s wall %.1f cpu" % (g, st["wall"], st["cpu"]), flush=True)


if __name__ == "__main__":
    cmd = sys.argv[1]; gs = [g for g in C.parse(sys.argv[2]) if FIRST <= g <= LAST]
    run(cmd, gs, sys.argv[3:])
