#!/usr/bin/env python3
"""take3.py -- shared engine of film-3 takes s06 / s08 / s09 (render team 2).  Identical copy in each take folder.

A take module defines SHOTS = {shot_id: ShotSpec} and calls take3.main(SHOTS, ...).  Per shot:
    rng      (g_first, g_last) raw film frames rendered for that shot (handles included)
    cam(g)   -> (loc, look_at[, lens_mm])
    actors   {name: dict(cast=..., place=fn(g)->xyz, pose=fn(g)->(pose, hands_world), ppd=int)}
             hands_world: {"r"|"l": {"hand": world_xyz | "tip": world_xyz, ...arm keys}} (pinned through world_to_local)
    state(g) -> dict(paint=, seep=, bucket=(pos, fill, visible, rot))  (keyed on the shot's Blender frames)
    fg       list of names of foreground objects (made by build_fg) shown only in this shot
    drops    list of drop specs (see Drops) shown in this shot
Blender frame of (shot k, film frame g) = 1000 * k + g + 1 (shots of one take overlap inside their dissolves).
Set: v3/set3d3/harbor.py WINTER (read-only, changed at runtime only).  Cast: v3/cast3.
"""
import math, os, sys, time, json

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE))
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast3"), os.path.join(V3, "stage"), os.path.join(V3, "set3d3"), os.path.join(V3, "set3d2"),
          os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast3                                            # noqa: E402  (first: registers tommy, foreman, workers, kids)
import bpy                                              # noqa: E402
from mathutils import Vector                            # noqa: E402
import harbor as H                                      # noqa: E402
import tower as T                                       # noqa: E402
import actors, camrig, render, sprites                  # noqa: E402
from anim import ease, keys, blink, pulse, lerp, clamp  # noqa: E402


def g_of(t):
    """narration time -> film frame of an in-shot event"""
    return int(round((t + 0.10) * 30))


def W(t, n, z=0.0):
    """world point near the bucket seam: t D along the wall (+ = screen-right when facing the wall), n D out from it, height z"""
    return H.wall_pt(H.TH_B + t / H.TANK_R, H.TANK_R + n, z)


def sph(look, dist, heading, pitch):
    """camera location dist D from look, looking along compass heading (deg, atan2(x, y)) with pitch (deg, + = up)"""
    hr, pr = math.radians(heading), math.radians(pitch)
    d = Vector((math.sin(hr) * math.cos(pr), math.cos(hr) * math.cos(pr), math.sin(pr)))
    return Vector(look) - d * dist


def kcam(g, ks, lin=0.15):
    """eased camera keys [(g, (dist, heading, pitch, lx, ly, lz[, lens]), ease)] with a constant-speed share (never parks)"""
    a = keys(g, ks)
    b = keys(g, [(f, v, "lin") for f, v, e in ks])
    k = lerp(a, b, lin)
    look = Vector(k[3:6])
    loc = sph(look, k[0], k[1], k[2])
    return (loc, look, k[6]) if len(k) > 6 else (loc, look)


def shake(g, hits, amp, decay=0.35, n=10):
    """decaying jolt (dx, dz) after each hit frame"""
    dx = dz = 0.0
    for i, s in enumerate(hits):
        d = g - s
        if 0 <= d <= n:
            a = amp * math.exp(-decay * d)
            dz += a * math.cos(d * 2.1 + i)
            dx += 0.7 * a * math.sin(d * 2.7 + 2 * i)
    return dx, dz


LIP = ["talk_a", "talk_b", "talk_a", "flat", "talk_o", "talk_b", "talk_a", "talk_b", "flat", "talk_a", "talk_o", "talk_b"]


def lipsync(g, g0, g1, gaps=()):
    """mouth drawing for frame g of a quoted line g0..g1 (a new drawing every 2 frames; 'flat' in the gaps and outside)"""
    if g < g0 or g > g1:
        return None
    for a, b in gaps:
        if a <= g <= b:
            return "flat"
    i = (g - g0) // 2
    return LIP[(i * 7 + i // 3) % len(LIP)]


# ----------------------------------------------------------------------------- light side
def head_flip_for(loc, look):
    """True when the key comes from screen-right (cast3 / stage convention)"""
    kd = Vector(H.STATE["P"]["key_dir"])
    src = Vector((-kd.x, -kd.y, 0.0))
    f = Vector((look[0] - loc[0], look[1] - loc[1], 0.0)).normalized()
    right = Vector((f.y, -f.x, 0.0))
    return src.dot(right) > 0


# ----------------------------------------------------------------------------- foreground masses in shade, drops
def _cyl(name, base, r, h, mat, coll, seg=20, bulge=0.0):
    me = bpy.data.meshes.new(name)
    vs, fs = [], []
    rings = 6
    for j in range(rings + 1):
        z = h * j / rings
        rr = r * (1 + bulge * math.sin(math.pi * j / rings))
        for i in range(seg):
            a = 2 * math.pi * i / seg
            vs.append((base[0] + rr * math.cos(a), base[1] + rr * math.sin(a), base[2] + z))
    for j in range(rings):
        for i in range(seg):
            a0 = j * seg + i; a1 = j * seg + (i + 1) % seg
            fs.append((a0, a1, a1 + seg, a0 + seg))
    fs.append(tuple(range(rings * seg, rings * seg + seg)))
    me.from_pydata(vs, [], fs); me.update()
    uv = me.uv_layers.new(name="UVMap")
    for poly in me.polygons:
        for li in poly.loop_indices:
            co = me.vertices[me.loops[li].vertex_index].co
            uv.data[li].uv = (math.atan2(co.y - base[1], co.x - base[0]) * r / 1.5, co.z / 1.5)
    me.materials.append(mat)
    ob = bpy.data.objects.new(name, me); coll.objects.link(ob); T.no_bounce(ob)
    return ob


def _box(name, lo, hi, mat, coll):
    me = bpy.data.meshes.new(name)
    x0, y0, z0 = lo; x1, y1, z1 = hi
    v = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    f = [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)]
    me.from_pydata(v, [], f); me.update()
    uv = me.uv_layers.new(name="UVMap")
    for poly in me.polygons:
        n = poly.normal
        for li in poly.loop_indices:
            co = me.vertices[me.loops[li].vertex_index].co
            uv.data[li].uv = (co.x / 2.0, co.y / 2.0) if abs(n.z) > 0.5 else ((co.y / 2.0, co.z / 2.0) if abs(n.x) > 0.5 else (co.x / 2.0, co.z / 2.0))
    me.materials.append(mat)
    ob = bpy.data.objects.new(name, me); coll.objects.link(ob); T.no_bounce(ob)
    return ob


def shade_mats():
    """shade-only materials (key gain 0: painted blue-violet shade, as s01's loggia)"""
    tex = os.path.join(V3, "set3d3", "tex_harbor")
    return dict(
        wood=T.mat_lit("T3_wood_shade", color="#7a4a2a", gain=0.0, shade_mul=0.55),
        hoop=T.mat_lit("T3_hoop_shade", color="#3c3034", gain=0.0, shade_mul=0.6),
        girder=T.mat_lit("T3_girder_shade", image=os.path.join(tex, "girder.png"), gain=0.0, shade_mul=0.5),
        column=T.mat_lit("T3_column_shade", image=os.path.join(tex, "column.png"), gain=0.0, shade_mul=0.5),
        crate=T.mat_lit("T3_crate_shade", color="#8a5a34", gain=0.0, shade_mul=0.55),
    )


def barrel(name, base, coll, M, r=0.42, h=1.15):
    obs = [_cyl(name, base, r, h, M["wood"], coll, bulge=0.08)]
    for z in (0.18, h - 0.22):
        obs.append(_cyl(name + "_hoop%d" % int(z * 100), (base[0], base[1], base[2] + z), r * 1.07 + 0.01, 0.07, M["hoop"], coll))
    for o in obs:
        o.visible_shadow = False
    return obs


class Drops(object):
    """glossy elongated molasses drops that form at the tip of a seep strip and fall (the set's own drop reads as a dot).
    spec = dict(strip=i, period=P, phase=k, floor=z_land, n_out=0.14)"""
    def __init__(self, coll):
        self.coll = coll
        m = T.mat_lit("T3_drop", color="#5c2a0e", gain=0.85, shade_mul=0.6)
        self.mat = H._add_gloss(m, 0.6, 0.08, (1.0, 0.93, 0.84))
        self.obs = {}

    def get(self, key):
        if key not in self.obs:
            me = bpy.data.meshes.new("drop_%s" % key)
            vs, fs = [], []
            seg, rings = 10, 8
            for j in range(rings + 1):                         # teardrop: round bottom, pointed top (z 0..1, radius 0.5 max)
                v = j / rings
                z = v
                r = 0.5 * math.sin(math.pi * min(1.0, v * 1.25)) ** 0.9 * (1.0 - 0.75 * max(0.0, v - 0.4) / 0.6) if j not in (0, rings) else 0.0
                for i in range(seg):
                    a = 2 * math.pi * i / seg
                    vs.append((r * math.cos(a), r * math.sin(a), z))
            for j in range(rings):
                for i in range(seg):
                    a0 = j * seg + i; a1 = j * seg + (i + 1) % seg
                    fs.append((a0, a1, a1 + seg, a0 + seg))
            me.from_pydata(vs, [], fs); me.update()
            for p in me.polygons:
                p.use_smooth = True
            me.materials.append(self.mat)
            ob = bpy.data.objects.new("drop_%s" % key, me); self.coll.objects.link(ob); T.no_bounce(ob)
            ob.visible_shadow = False
            self.obs[key] = ob
        return self.obs[key]

    def key(self, spec, g, f, seep_a, visible=True):
        ob = self.get(spec["key"])
        th, z0, L, w = H.STATE["seep_strips"][spec["strip"]]
        tip = z0 - L * max(seep_a, 0.25)
        P, form = spec.get("period", 30), spec.get("form", 18)
        u = (g + spec.get("phase", 0)) % P
        size = spec.get("size", 1.0)
        n0 = 0.02 + w * 0.15
        fall_to = spec.get("floor", 0.0)
        rad = 0.055 * size
        if u < form:                                           # swelling at the tip, hanging
            e = ease(u / float(form), "quad_out")
            sx, sz = rad * (0.35 + 0.65 * e), rad * 2.2 * (0.4 + 0.9 * e)
            z = tip - sz * 0.92
            n = n0
        else:                                                  # released: falls with gravity, stretches
            t = u - form
            dz = 0.5 * spec.get("acc", 0.016) * t * t + 0.02 * t
            sx, sz = rad * 0.85, rad * (2.6 + min(2.0, 0.35 * t))
            z = tip - rad * 2.2 * 1.3 * 0.92 - dz
            n = n0 + min(spec.get("n_out", 0.14), 0.02 * t)
        vis = visible and seep_a > 0.05 and z > fall_to
        p = H.wall_pt(th, H.TANK_R + n, z)
        ob.location = p
        ob.scale = (sx, sx, sz)
        ob.rotation_euler = (0, 0, 0)
        ob.hide_render = not vis
        for path in ("location", "scale"):
            T._key(ob, path, f, "LINEAR")
        T._key(ob, "hide_render", f)


# ----------------------------------------------------------------------------- the take
class Take(object):
    def __init__(self, shots, build_fg=None, quality="preview", verbose=True, preset="WINTER", tag="t3"):
        t0 = time.time()
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.scene = scene = bpy.context.scene
        self.shots = shots
        self.A = H.build(preset)
        H.setup_render(scene, quality)
        scene.render.use_persistent_data = False
        scene.cycles.transparent_max_bounces = 12
        scene.frame_start, scene.frame_end = 1, 9000
        d = H.STATE.get("drop")
        if d is not None:                                      # the set's static drop dot: replaced by Drops
            d.scale = (1e-4, 1e-4, 1e-4)
        self.coll = bpy.data.collections.new("T3_FG"); scene.collection.children.link(self.coll)
        self.M = shade_mats()
        self.fg = build_fg(self) if build_fg else {}
        self.drops = Drops(self.coll)
        fm = T.mat_lit("T3_bucket_molasses", color="#4a1606", gain=0.75, shade_mul=0.32)      # the set's fill reads blue in shade
        bf_ = H.STATE["bucket"]["fill"]
        bf_.data.materials.clear(); bf_.data.materials.append(fm)
        sm = T.mat_lit("T3_seep", color="#34100a", gain=0.6, shade_mul=0.45)
        so = H.STATE["seep"]                                   # seep strips: darker, with a wet highlight (sweating)
        so.data.materials.clear(); so.data.materials.append(sm)
        for sh in shots.values():
            for spec in sh.get("drops", []):
                self.drops.get(spec["key"])
        self.cam = camrig.make_camera(scene, name="cam_" + tag)
        self.cam.data.clip_start = 0.02
        self.cam.data.clip_end = 600
        sd = os.path.join(HERE, "work", "sprites")
        self.actors = {}
        for k, sh in shots.items():
            for nm, a in sh["actors"].items():
                if nm not in self.actors:
                    A = actors.Actor(nm, a["cast"])
                    A.build(sprites.DEFAULT_CANVAS[a["cast"]], sd, contact=True)
                    T.no_bounce(A.card)
                    A.head_flip = {}
                    self.actors[nm] = A
        self.info, self.anch = {}, {}
        self.keyed = set()
        if verbose:
            print("%s: built in %.1f s" % (tag, time.time() - t0), flush=True)

    def bf(self, k, g):
        return 1000 * int(k) + int(g) + 1

    def cam_at(self, k, g):
        r = self.shots[k]["cam"](g)
        return (Vector(r[0]), Vector(r[1]), (r[2] if len(r) > 2 else 22.0))

    def visible(self, k):
        sh = self.shots[k]
        for nm, A in self.actors.items():
            A.set_hidden(nm not in sh["actors"])
        for nm, obs in self.fg.items():
            for o in obs:
                o.hide_render = nm not in sh.get("fg", ())

    def pose(self, k, gs):
        sh = self.shots[k]
        self.visible(k)
        for g in gs:
            f = self.bf(k, g)
            loc, look, lens = self.cam_at(k, g)
            camrig.key_camera(f, loc, look, lens=lens, cam=self.cam, interp="LINEAR", easing="AUTO")
            st = sh["state"](g)
            if "paint" in st:
                H.set_paint(st["paint"], frame=f)
            if "seep" in st:
                H.set_seep(st["seep"], frame=f)
            if "bucket" in st:
                pos, fill, vis, rot = st["bucket"]
                H.set_bucket(pos=pos, fill=fill, visible=vis, frame=f, rot=rot or (0, 0, math.degrees(H.TH_B + math.pi / 2)), interp="LINEAR")
            dspecs = sh.get("drops", [])
            for key_, ob in list(self.drops.obs.items()):
                if key_ not in [d["key"] for d in dspecs]:
                    ob.hide_render = True; T._key(ob, "hide_render", f)
            for spec in dspecs:
                self.drops.key(spec, g, f, st.get("seep", 0.6), visible=spec.get("on", lambda g: True)(g))
            for nm, a in sh["actors"].items():
                self.actors[nm].place(f, tuple(a["place"](g)))
                self.actors[nm].head_flip[f] = head_flip_for(loc, look)
            self.keyed.add((k, g))
        cam = self.cam
        for g in gs:
            f = self.bf(k, g)
            self.scene.frame_set(f)
            for nm, a in sh["actors"].items():
                A = self.actors[nm]
                p, hw = a["pose"](g)
                hands = None
                if hw:
                    feet = sprites.feet_of(a["cast"], p)
                    hands = {}
                    for side, h in hw.items():
                        h = dict(h)
                        for kk in ("hand", "tip"):
                            if kk in h and len(h[kk]) == 3:
                                h[kk] = actors.world_to_local(A, cam, tuple(h[kk]), f, feet=feet)
                        hands[side] = h
                _, inf = A.pose(f, p, hands=hands, camera=cam)
                if hands:
                    self.info.setdefault((k, g), {})[nm] = {s: round(inf[s]["error"], 3) for s in hands}
        fr = [self.bf(k, g) for g in gs]
        for nm, a in sh["actors"].items():
            A = self.actors[nm]
            for f, r in zip(fr, A.render_sprites(a.get("ppd", 256), frames=fr)):
                self.anch[(nm, f)] = r["anchors"]
                if r.get("clipped"):
                    print("WARNING sprite of %s clipped on frame %d" % (nm, f), flush=True)

    def report(self, k, g):
        f = self.bf(k, g)
        self.scene.frame_set(f)
        loc, look, lens = self.cam_at(k, g)
        v = look - loc
        out = dict(shot=k, g=g, cam=[round(c, 3) for c in loc], lens=round(lens, 1),
                   pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1),
                   heading=round(math.degrees(math.atan2(v.x, v.y)), 1), heads={})
        for nm in self.shots[k]["actors"]:
            A = self.actors[nm]
            if f not in A.poses or (nm, f) not in self.anch:
                continue
            res = A.feet.get(f)
            hx, hy = self.anch[(nm, f)]["head"]
            c = actors.local_to_screen(A, self.cam, (hx, hy), f, res)
            l = actors.local_to_screen(A, self.cam, (hx - 0.5, hy), f, res)
            r = actors.local_to_screen(A, self.cam, (hx + 0.5, hy), f, res)
            w = math.hypot(r[0] - l[0], r[1] - l[1])
            out["heads"][nm] = dict(x=round(c[0], 1), y=round(c[1], 1), w=round(w, 1), yc=round(c[1] / 1280.0, 3),
                                    bottom=round(c[1] + w / 2, 1), flip=bool(A.head_flip.get(f)))
        out["hands_err"] = self.info.get((k, g), {})
        for nm, p in self.shots[k].get("marks", {}).items():
            out[nm] = [round(x, 1) for x in render.world_to_screen(self.cam, tuple(p), f)[:2]]
        return out

    def render(self, k, gs, out_dir, scale=1.0, samples=12, threads=2):
        self.visible(k)
        self.scene.cycles.samples = samples
        return render.render_frames([self.bf(k, g) for g in gs], out_dir, scale=scale, threads=threads, scene=self.scene,
                                    camera=self.cam, verbose=False)


def parse(spec):
    out = []
    for part in spec.split(","):
        if ":" in part:
            a = [int(v) for v in part.split(":")]
            out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1))
        else:
            out.append(int(part))
    return out


def main(SHOTS, build_fg, tag, argv=None):
    argv = argv or sys.argv
    cmd = argv[1]
    k = int(argv[2])
    rng = SHOTS[k]["rng"]
    gs = [g for g in parse(argv[3]) if rng[0] <= g <= rng[1]] if len(argv) > 3 and argv[3] != "all" else list(range(rng[0], rng[1] + 1))
    if cmd == "probe":
        Tk = Take(SHOTS, build_fg, tag=tag)
        Tk.pose(k, gs)
        for g in gs:
            print(json.dumps(Tk.report(k, g)))
    elif cmd == "stills":
        out = argv[4]
        scale = float(argv[5]) if len(argv) > 5 else 0.5
        samples = int(argv[6]) if len(argv) > 6 else 6
        Tk = Take(SHOTS, build_fg, tag=tag)
        Tk.pose(k, gs)
        for g in gs:
            st = Tk.render(k, [g], out, scale=scale, samples=samples)[0]
            dst = os.path.join(out, "s%d_g_%04d.png" % (k, g))
            os.replace(st["path"], dst)
            print(json.dumps(Tk.report(k, g)), flush=True)
            print("shot %d g %d  %.1f s wall %.1f cpu" % (k, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        out = os.path.join(HERE, "raw", "s%d" % k)
        os.makedirs(out, exist_ok=True)
        scale = float(argv[4]) if len(argv) > 4 else 1.0
        samples = int(argv[5]) if len(argv) > 5 else 12
        todo = []
        for g in gs:
            png, js = os.path.join(out, "g_%04d.png" % g), os.path.join(out, "g_%04d.json" % g)
            ok = os.path.exists(png) and os.path.exists(js)
            if ok:
                m = json.load(open(js)); ok = m.get("scale") == scale and m.get("samples") == samples
            if not ok:
                todo.append(g)
        print("final: shot %d, %d to render, %d done" % (k, len(todo), len(gs) - len(todo)), flush=True)
        if todo:
            Tk = Take(SHOTS, build_fg, quality="final", tag=tag)
            Tk.pose(k, todo)
            for g in todo:
                st = Tk.render(k, [g], out, scale=scale, samples=samples)[0]
                png = os.path.join(out, "g_%04d.png" % g)
                os.replace(st["path"], png)
                rep = Tk.report(k, g)
                rep.update(wall=round(st["wall"], 2), cpu=round(st["cpu"], 2), scale=scale, samples=samples, retried=st.get("retried"))
                json.dump(rep, open(png[:-4] + ".json.tmp", "w")); os.replace(png[:-4] + ".json.tmp", png[:-4] + ".json")
                print("shot %d g %d  %.1f s wall  %.1f s cpu" % (k, g, st["wall"], st["cpu"]), flush=True)
