#!/usr/bin/env python3
"""shot.py -- film 21 take s07 (FALSE PAYOFF): shots 18 + 19, preset camp_bank.
Frames: g 1044..1141 + 7 in-handle (1037..1043) + 6 out-handle (1142..1147) = 111 frames.
  shot 18  g 1037..1092  the waiting English on the south bank laugh and point across the river, bouncing out of phase (fixed laugh
                         drawing, no lip-sync).  Pull-out ~8 %/s + lateral slide, banner pole + barrel in the foreground.
  shot 19  g 1093..1147  quick push-in on Cressingham (~10 %/s), smug, thumbs in the belt, lip-sync "เห็นไหม กลัวจนขยับไม่ได้!" ONLY in narration
                         36.32-37.89 (g 1093..1140).  Surrey (cx ~570, off the banner pole) listens, unimpressed.
    python3 shot.py probe a:b[:step]
    python3 shot.py stills a:b[:step] out_dir [scale] [samples]
    python3 shot.py final a:b[:step] [scale] [samples]      -> raw/g_%04d.png (resumable)
"""
import os, sys, math, json, time
import c21 as C
K, cast21, actors, camrig, render, sprites, bpy = C.K, C.cast21, C.actors, C.camrig, C.render, C.sprites, C.bpy
from mathutils import Vector
ez, lerp, blink = C.ez, C.lerp, C.blink
HERE = C.HERE
TMP = os.path.join(HERE, "work")

G0, G1 = 1044, 1141
G_FIRST, G_LAST = G0 - 7, G1 + 6          # 1037 .. 1147
G_CUT = 1093                              # shot 19 starts (internal cut)
Q0, Q1 = C.g_of(36.32), C.g_of(37.89)     # mouth window (narration 36.32-37.89)
PRESET = "camp_bank"
SURREY_PX = 570                           # QA-art R2: Surrey off the right-edge banner pole
PPD = 256


EXTRAS = [("e0", 8.0, 470, 'foot'), ("e1", 6.2, 335, 'foot'), ("e2", 6.7, 440, 'knight'), ("e3", 7.8, 390, 'foot'), ("e4", 9.0, 250, 'foot')]


def build():
    bpy.ops.wm.read_factory_settings(use_empty=True)
    A = K.build_for_cli(PRESET, placeholders=False)
    pr = K.PRESETS[PRESET]
    cam = bpy.context.scene.camera
    cam0, look0, ln = Vector(A['cam']['loc']), Vector(A['cam']['look']), pr['lens']
    marks = dict(A['marks'])
    marks['surrey'] = K.mark_px(tuple(cam0), tuple(look0), ln, 5.8, SURREY_PX, 'surrey')
    for nm, d_, xp, typ in EXTRAS:                    # the laughing camp stands closer than the preset marks so shot 18 reads
        marks[nm] = K.mark_px(tuple(cam0), tuple(look0), ln, d_, xp, typ)
    f = look0 - cam0
    fh = Vector((f.x, f.y, 0)).normalized()
    rh = Vector((fh.y, -fh.x, 0))
    return dict(A=A, pr=pr, cam=cam, cam0=cam0, look0=look0, lens=ln, marks=marks, fh=fh, rh=rh, rlook=math.hypot(f.x, f.y))


CAST = [  # actor, mark, cast, pose name, kind, phase
    ("cre", "cress", "cressingham", "cressingham_laughing", "cress", 0.0),
    ("sur", "surrey", "surrey", "surrey_listening", "surrey", 0.0),
    ("e0", "e0", "footman_a", "footman_a_point_laugh", "laugh", 0.0),
    ("e1", "e1", "footman_b", "footman_b_laughing", "laugh", 2.1),
    ("e2", "e2", "knight_b", "knight_b_point_laugh", "laugh", 4.2),
    ("e3", "e3", "footman_a", "footman_a_laughing", "laugh", 1.2),
    ("e4", "e4", "footman_b", "footman_b_point_laugh", "laugh", 3.3),
]


def ss(t):
    t = max(0.0, min(1.0, t)); return t * t * t * (t * (6 * t - 15) + 10)


def aim(st, loc, subj, tx, tilt_from=None):
    """look-at point so that world point `subj` lands at screen x = tx (px) with the preset's pitch."""
    cam0, look0 = st['cam0'], st['look0']
    f = st['lens'] / 36.0 * 1280.0
    th = math.atan2(subj.y - loc.y, subj.x - loc.x) + math.atan((tx - 360.0) / f)
    R = st['rlook']; z = (look0.z - cam0.z) / R
    return Vector((loc.x + R * math.cos(th), loc.y + R * math.sin(th), loc.z + R * z))


def cam_of(st, g):
    """camera position + look-at for film frame g (linear in g between keys; the cut at G_CUT is the jump)."""
    cam0, fh, rh = st['cam0'], st['fh'], st['rh']
    M = st['marks']
    if g < G_CUT:                                    # shot 18: pull-out ~9 %/s + slide right ~40 px/s, the camp group centred
        t = (g - G_FIRST) / float(G_CUT - 1 - G_FIRST)
        u = 0.8 * ss(t) + 0.2 * t
        loc = cam0 + fh * lerp(0.4, -1.0, u) + rh * lerp(-0.15, 0.45, u)
        subj = Vector(M['e1'][:3]); tx = lerp(330.0, 300.0, u)
    else:                                            # shot 19: push-in ~10 %/s on Cressingham, he settles left of centre
        t = (g - G_CUT) / float(G_LAST - G_CUT)
        u = 0.85 * ss(t) + 0.15 * t
        loc = cam0 + fh * lerp(0.5, 1.5, u) + rh * lerp(0.0, 0.55, u)
        subj = Vector(M['cress'][:3]); tx = lerp(235.0, 290.0, u)
    return loc, aim(st, loc, subj, tx)


def pose_of(name, kind, base, g, phase):
    """pose + lift (m) for actor `name` at film frame g."""
    p = dict(cast21.STORY21[base][1])
    lift = 0.0
    if kind == "laugh":                              # fixed laugh drawing + bounce, out of phase
        p, dy = cast21.laugh(p, g, phase=phase)
        lift = dy * K.D
    elif kind == "cress":
        if g < G_CUT:                                # shot 18: he laughs with the camp (no lip-sync)
            p, dy = cast21.laugh(p, g, phase=1.7)
            lift = dy * K.D
        else:                                        # shot 19: smug, thumbs in the belt; mouth moves ONLY inside the quote window
            p = dict(cast21.STORY21["cressingham_smug_belt"][1])
            p["lean"] = p.get("lean", 0.0) + 1.2 * math.sin(g * 0.11)
            p["head_roll"] = p.get("head_roll", 0.0) + 1.5 * math.sin(g * 0.07)
            if Q0 <= g <= Q1:
                p = cast21.speak(p, g)
            p["blink"] = blink(g, [1111, 1135])
    else:                                            # surrey: idle sway, blinks
        p["lean"] = p.get("lean", 0.0) + 1.0 * math.sin(g * 0.09)
        p["head_roll"] = p.get("head_roll", 0.0) + 1.2 * math.sin(g * 0.06 + 1.0)
        p["blink"] = blink(g, [1058, 1112])
    p["t"] = p.get("t", 0.0) if kind == "laugh" or (kind == "cress" and g < G_CUT) else g / 30.0
    return p, lift


class Take(object):
    def __init__(self):
        self.st = build()
        st = self.st
        K.setup_render(bpy.context.scene, "final")
        self.cam = st['cam']
        self.cam.data.dof.use_dof = False
        self.acts = {}
        for nm, mark, cast, base, kind, ph in CAST:
            a = C.make_actor(nm, cast, os.path.join(TMP, "sprites"))
            self.acts[nm] = a

    def pose(self, gs):
        st = self.st
        K.set_flutter(0.0)
        for g in gs:
            f = g - G_FIRST + 1
            loc, look = cam_of(st, g)
            camrig.key_camera(f, loc, look, lens=st['lens'], cam=self.cam, interp="LINEAR", easing="AUTO")
            K.set_flutter(g / 30.0); K.set_smoke(g / 30.0); K.set_flow(g / 30.0)
            for nm, mark, cast, base, kind, ph in CAST:
                x, y, z, _, _ = st['marks'][mark]
                p, lift = pose_of(nm, kind, base, g, ph)
                self.acts[nm].place(f, (x, y, z + lift), scale=C.unit_scale(cast))
        for g in gs:
            f = g - G_FIRST + 1
            bpy.context.scene.frame_set(f)
            for nm, mark, cast, base, kind, ph in CAST:
                p, lift = pose_of(nm, kind, base, g, ph)
                self.acts[nm].pose(f, p, camera=self.cam)
        for a in self.acts.values():
            a.render_sprites(PPD, frames=[g - G_FIRST + 1 for g in gs])

    def render(self, g, out_dir, scale=1.0, samples=24):
        f = g - G_FIRST + 1
        sc = bpy.context.scene
        K.set_flutter(g / 30.0); K.set_smoke(g / 30.0); K.set_flow(g / 30.0)
        K.setup_render(sc, "final", samples)
        st = render.render_frames([f], out_dir, scale=scale, scene=sc, camera=self.cam, verbose=False)[0]
        K.grade(st["path"], scale=scale)
        return st

    def heads(self, g):
        f = g - G_FIRST + 1
        bpy.context.scene.frame_set(f)
        out = {}
        for nm, a in self.acts.items():
            hx, hy = (0.0, 0.0)
            try:
                an = a.poses[f]
            except Exception:
                pass
        return out


def parse(spec):
    out = []
    for part in spec.split(","):
        a = [int(v) for v in part.split(":")]
        out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1)) if len(a) > 1 else a
    return out


if __name__ == "__main__":
    cmd = sys.argv[1]
    gs = [g for g in parse(sys.argv[2]) if G_FIRST <= g <= G_LAST]
    if cmd == "stills":
        out = sys.argv[3]; scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5; samples = int(sys.argv[5]) if len(sys.argv) > 5 else 8
        os.makedirs(out, exist_ok=True)
        T = Take(); T.pose(gs)
        for g in gs:
            t0 = time.time(); st = T.render(g, os.path.join(TMP, "tmp"), scale=scale, samples=samples)
            os.replace(st["path"], os.path.join(out, "g_%04d.png" % g)); print("g", g, round(time.time() - t0, 1), "s", flush=True)
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0; samples = int(sys.argv[4]) if len(sys.argv) > 4 else 24
        out = os.path.join(HERE, "raw"); os.makedirs(out, exist_ok=True)
        todo = [g for g in gs if not os.path.exists(os.path.join(out, "g_%04d.png" % g))]
        print("final: %d to render" % len(todo), flush=True)
        if todo:
            T = Take(); T.pose(todo)
            for g in todo:
                t0 = time.time(); st = T.render(g, os.path.join(TMP, "tmp"), scale=scale, samples=samples)
                os.replace(st["path"], os.path.join(out, "g_%04d.png" % g)); print("g", g, round(time.time() - t0, 1), "s", flush=True)
