#!/usr/bin/env python3
"""shot.py -- film 5 take s16: shot 16, the fast replay (g 1707..1813 + 8-frame handles both sides), mine set (tunnel LAMP).

The shrinking song replayed fast, ECU of the canary inside the set's 3D cage on its nail (bird sprite on the perch, behind the front
bars), each beat a new angle and a quick push; the gas haze (my camera-facing card, as in s15) thickens each time:
    16a g 1699..1742  day 1: 5 notes, haze faint (0.10)            ("เพลงที่สั้นลงทุกวัน")      in-handle 1699..1706
    16b g 1743..1778  cut, day 5: 3 notes, haze thicker (0.22)     ("ก็คือแก๊สที่ค่อย ๆ")
    16c g 1779..1821  cut, day 10: 1 note, then the beak closes, eyes heavy (gentle), haze thick (0.36)
                      ("เพิ่มขึ้นทุกวัน นั่นเอง")                     out-handle 1814..1821
NO depth of field anywhere (client rule).  Sub-shot ids 1..3; Blender frame = 2000 * (id - 1) + (g - 1600).

    python3 shot.py stills <ids> a:b[:step] <out_dir> [scale] [samples] | final <ids> a:b [scale] [samples]
"""
import math, os, sys, time, json

HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(os.path.dirname(HERE))
PROJ = os.path.dirname(V3)
for p in (os.path.join(V3, "cast5"), os.path.join(V3, "stage"), os.path.join(V3, "set3d5"), os.path.join(PROJ, "v2", "shots")):
    if p not in sys.path:
        sys.path.insert(0, p)
import cast5                                            # noqa: E402
import bpy                                              # noqa: E402
from mathutils import Vector                            # noqa: E402
import mine as M                                        # noqa: E402
import actors, camrig, render, sprites                  # noqa: E402
from anim import ease, keys, blink, lerp, clamp         # noqa: E402

TMP = os.path.join(HERE, "work")


def g_of(t):
    return int(round((t + 0.10) * 30))


G0, G1, H = 1707, 1814, 8
B = [G0, 1743, 1779, G1]
RANGES = {1: (G0 - H, B[1] - 1), 2: (B[1], B[2] - 1), 3: (B[2], G1 + H - 1)}
NAME = {1: "16a", 2: "16b", 3: "16c"}
HAZE = {1: 0.10, 2: 0.22, 3: 0.36}
NOTES = {1: 5, 2: 3, 3: 1}
G_HUSH = 1797                                               # 16c: the one note ends, beak closes


def bf(shot, g):
    return 2000 * (shot - 1) + int(g) - 1600


def _ez(u, kind="sine"):
    return ease(clamp(u), kind)


TP = M.TP
# per beat: (azimuth deg from the across-the-roadway direction, height offset, distance start, end, mirror)
VIEW = {1: (-38.0, 0.04, 1.75, 1.20, True), 2: (8.0, 0.10, 1.65, 1.15, True), 3: (-12.0, 0.02, 1.40, 0.98, True)}


def bird_pose(g, shot):
    n = NOTES[shot]
    t = g / 30.0
    if shot < 3:
        return dict(state="perch_sing", notes=n, beak=0.75 + 0.2 * math.sin(g * 0.9), t=t, mirror=VIEW[shot][4])
    u = clamp((g - G_HUSH) / 8.0)
    if g < G_HUSH:
        return dict(state="sing_one", notes=1, beak=0.6 + 0.15 * math.sin(g * 0.8), t=t, mirror=VIEW[shot][4])
    return dict(state="droop", notes=0, beak=0.0, eyes=lerp(0.85, 0.45, u), droop=lerp(0.35, 0.6, u), ruffle=lerp(0.3, 0.6, u),
                t=t, mirror=VIEW[shot][4], breath=0.6)


CANVAS_BIRD = (-0.75, -1.25, 0.875, 0.125)
class Take(object):
    def __init__(self, quality="preview", verbose=True):
        t0 = time.time()
        bpy.ops.wm.read_factory_settings(use_empty=True)
        self.scene = scene = bpy.context.scene
        self.A = M.build("tunnel")
        M.setup_render(scene, quality)
        scene.cycles.denoising_prefilter = "FAST"
        scene.render.use_persistent_data = False
        scene.frame_start, scene.frame_end = 1, 8000
        self.cam = camrig.make_camera(scene, name="cam_s16")
        self.cam.data.clip_start = 0.02
        self.cam.data.clip_end = 600
        M.setup_dof(scene, None, None, cam=self.cam)
        sd = os.path.join(TMP, "sprites")
        self.actors = {}
        b = actors.Actor("bird", "canary"); b.build(CANVAS_BIRD, sd, shadow=None); self.actors["bird"] = b
        b.head_flip = False
        M.no_bounce(b.card)
        self.perch = Vector(self.A["cage"]["perch"])
        self.anch = {}
        self._haze_card()
        if verbose:
            print("s16: built in %.1f s" % (time.time() - t0), flush=True)

    # -- the gas haze: a camera-facing card, a faint green-grey veil above a wavy lower edge (world z), drifting
    def _haze_card(self):
        me = bpy.data.meshes.new("s16_haze")
        W, Hh = 14.0, 9.0
        me.from_pydata([(-W / 2, 0, -Hh / 2), (W / 2, 0, -Hh / 2), (W / 2, 0, Hh / 2), (-W / 2, 0, Hh / 2)], [], [(0, 1, 2, 3)])
        ob = bpy.data.objects.new("s16_haze", me)
        self.scene.collection.objects.link(ob)
        ob.visible_shadow = False
        try:
            ob.visible_diffuse = False; ob.visible_glossy = False; ob.visible_transmission = False
        except Exception:
            pass
        mat = bpy.data.materials.new("s16_haze_mat"); mat.use_nodes = True
        nt = mat.node_tree; N = nt.nodes; L = nt.links
        for n in list(N):
            N.remove(n)
        out = N.new("ShaderNodeOutputMaterial")
        geo = N.new("ShaderNodeNewGeometry")
        tco = N.new("ShaderNodeTexCoord")
        sep = N.new("ShaderNodeSeparateXYZ"); L.new(geo.outputs["Position"], sep.inputs[0])
        edge = N.new("ShaderNodeValue"); edge.name = "edge"; edge.outputs[0].default_value = 5.6
        amp = N.new("ShaderNodeValue"); amp.name = "amp"; amp.outputs[0].default_value = 0.0
        tim = N.new("ShaderNodeValue"); tim.name = "time"; tim.outputs[0].default_value = 0.0
        noi = N.new("ShaderNodeTexNoise"); noi.noise_dimensions = "4D"; noi.inputs["Scale"].default_value = 0.55
        noi.inputs["Detail"].default_value = 2.0
        L.new(tco.outputs["Object"], noi.inputs["Vector"]); L.new(tim.outputs[0], noi.inputs["W"])
        # wave = (noise - 0.5) * 0.7 ; zz = z + wave - edge
        w1 = N.new("ShaderNodeMath"); w1.operation = "SUBTRACT"; w1.inputs[1].default_value = 0.5; L.new(noi.outputs["Fac"], w1.inputs[0])
        w2 = N.new("ShaderNodeMath"); w2.operation = "MULTIPLY"; w2.inputs[1].default_value = 0.7; L.new(w1.outputs[0], w2.inputs[0])
        z1 = N.new("ShaderNodeMath"); z1.operation = "ADD"; L.new(sep.outputs["Z"], z1.inputs[0]); L.new(w2.outputs[0], z1.inputs[1])
        zz = N.new("ShaderNodeMath"); zz.operation = "SUBTRACT"; L.new(z1.outputs[0], zz.inputs[0]); L.new(edge.outputs[0], zz.inputs[1])
        # body: smoothstep(0, 0.6, zz) * (0.65 + 0.35 * noise2) * amp
        mr = N.new("ShaderNodeMapRange"); mr.interpolation_type = "SMOOTHSTEP"
        mr.inputs["From Min"].default_value = 0.0; mr.inputs["From Max"].default_value = 0.6
        L.new(zz.outputs[0], mr.inputs["Value"])
        n2 = N.new("ShaderNodeTexNoise"); n2.noise_dimensions = "4D"; n2.inputs["Scale"].default_value = 1.6
        L.new(tco.outputs["Object"], n2.inputs["Vector"]); L.new(tim.outputs[0], n2.inputs["W"])
        m2 = N.new("ShaderNodeMapRange"); m2.inputs["To Min"].default_value = 0.55; m2.inputs["To Max"].default_value = 1.15
        m2.inputs["From Min"].default_value = 0.3; m2.inputs["From Max"].default_value = 0.7
        L.new(n2.outputs["Fac"], m2.inputs["Value"])
        bo = N.new("ShaderNodeMath"); bo.operation = "MULTIPLY"; L.new(mr.outputs[0], bo.inputs[0]); L.new(m2.outputs[0], bo.inputs[1])
        # edge line: exp(-(zz/0.05)^2) * 0.9
        e1 = N.new("ShaderNodeMath"); e1.operation = "DIVIDE"; e1.inputs[1].default_value = 0.06; L.new(zz.outputs[0], e1.inputs[0])
        e2 = N.new("ShaderNodeMath"); e2.operation = "MULTIPLY"; L.new(e1.outputs[0], e2.inputs[0]); L.new(e1.outputs[0], e2.inputs[1])
        e3 = N.new("ShaderNodeMath"); e3.operation = "MULTIPLY"; e3.inputs[1].default_value = -1.0; L.new(e2.outputs[0], e3.inputs[0])
        e4 = N.new("ShaderNodeMath"); e4.operation = "EXPONENT"; L.new(e3.outputs[0], e4.inputs[0])
        e5 = N.new("ShaderNodeMath"); e5.operation = "MULTIPLY"; e5.inputs[1].default_value = 0.85; L.new(e4.outputs[0], e5.inputs[0])
        tot = N.new("ShaderNodeMath"); tot.operation = "ADD"; tot.use_clamp = True; L.new(bo.outputs[0], tot.inputs[0]); L.new(e5.outputs[0], tot.inputs[1])
        fac = N.new("ShaderNodeMath"); fac.operation = "MULTIPLY"; fac.use_clamp = True; L.new(tot.outputs[0], fac.inputs[0]); L.new(amp.outputs[0], fac.inputs[1])
        em = N.new("ShaderNodeEmission"); em.inputs["Color"].default_value = (0.50, 0.70, 0.46, 1); em.inputs["Strength"].default_value = 0.55
        tr = N.new("ShaderNodeBsdfTransparent")
        mix = N.new("ShaderNodeMixShader")
        L.new(fac.outputs[0], mix.inputs[0]); L.new(tr.outputs[0], mix.inputs[1]); L.new(em.outputs[0], mix.inputs[2])
        L.new(mix.outputs[0], out.inputs["Surface"])
        me.materials.append(mat)
        self.haze, self.haze_nodes = ob, nt

    def key_haze(self, f, g, center, cam_loc, edge, amp):
        d = cam_loc - center; d.z = 0; d.normalize()
        ob = self.haze
        ob.location = center + d * 0.45
        ob.rotation_euler = (0.0, 0.0, math.atan2(d.y, d.x) - math.pi / 2)        # card normal (local -y.. +y) toward the camera
        camrig.key(ob, "location", f, Vector(ob.location), "LINEAR", "AUTO")
        camrig.key(ob, "rotation_euler", f, Vector(ob.rotation_euler), "LINEAR", "AUTO")
        N = self.haze_nodes.nodes
        for nm, v in (("edge", edge), ("amp", amp), ("time", g / 30.0 * 0.35)):
            s = N[nm].outputs[0]; s.default_value = v; s.keyframe_insert("default_value", frame=f)
        ob.hide_render = amp <= 1e-4
        ob.keyframe_insert("hide_render", frame=f)

    def cam_of(self, shot, g):
        g0, g1 = RANGES[shot]
        u = _ez((g - g0) / float(g1 + 1 - g0), "cubic_out")             # quick push that settles: replay energy
        az, dz, d0, d1, _ = VIEW[shot]
        y = 16.25
        across = TP(y, 1.0, 0) - TP(y, -1.0, 0); across.z = 0; across.normalize()
        a = math.radians(az)
        up = Vector((0, 0, 1)); side = up.cross(across)
        d = across * math.cos(a) + side * math.sin(a)
        sr = Vector((-d.y, d.x, 0.0))
        loc = self.perch + d * lerp(d0, d1, u) + Vector((0, 0, dz + 0.04))
        look = self.perch + sr * (-0.13 if VIEW[shot][4] else 0.13) + Vector((0, 0, lerp(0.42, 0.36, u)))
        return loc, look

    def pose(self, shot, gs):
        for g in gs:
            f = bf(shot, g)
            loc, look = self.cam_of(shot, g)
            camrig.key_camera(f, loc, look, cam=self.cam, interp="LINEAR", easing="AUTO")
            M.set_drips(f)
            M.set_cage(None, frame=f)
            d = loc - self.perch; d.z = 0; d.normalize(); sr = Vector((-d.y, d.x, 0.0))
            self.actors["bird"].place(f, tuple(self.perch + sr * 0.09))      # bird to the right on the perch: room for the notes inside
            amp = HAZE[shot] * (1.0 + 0.15 * clamp((g - RANGES[shot][0]) / 30.0))
            self.key_haze(f, g, self.perch, loc, -2.0, amp)
            M.set_gas({1: 1.0, 2: 2.0, 3: 3.0}[shot], frame=f)
        for g in gs:
            f = bf(shot, g)
            self.scene.frame_set(f)
            self.actors["bird"].pose(f, bird_pose(g, shot), camera=self.cam)
        fr = [bf(shot, g) for g in gs]
        for f, r in zip(fr, self.actors["bird"].render_sprites(2048, frames=fr)):
            self.anch[("bird", f)] = r["anchors"]
            if r.get("clipped"):
                print("s16: WARNING sprite of bird clipped on frame %d" % f, flush=True)
        for g in gs:
            f = bf(shot, g)
            loc, _ = self.cam_of(shot, g)
            d = loc - self.perch; d.z = 0; d.normalize()
            M.lamp_light(tuple(self.perch + d * 0.9 + Vector((0.0, 0.0, 0.6))), 0.20, frame=f, name="lamp_bird")
            M.lamp_light(tuple(self.perch - d * 0.55 + Vector((0, 0, 0.30))), 0.10, frame=f, name="lamp_rim")

    def report(self, shot, g):
        f = bf(shot, g)
        self.scene.frame_set(f)
        loc, look = self.cam_of(shot, g)
        out = dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], heads={}, haze=HAZE[shot], notes=NOTES[shot])
        a = self.actors["bird"]
        if ("bird", f) in self.anch:
            res = a.feet.get(f)
            hx, hy = self.anch[("bird", f)]["head"]
            c = actors.local_to_screen(a, self.cam, (hx, hy), f, res)
            l = actors.local_to_screen(a, self.cam, (hx - 0.09, hy), f, res)
            r = actors.local_to_screen(a, self.cam, (hx + 0.09, hy), f, res)
            out["heads"]["bird"] = dict(x=round(c[0], 1), y=round(c[1], 1), w=round(math.hypot(r[0] - l[0], r[1] - l[1]), 1))
        out["pts"] = {"perch": [round(x, 1) for x in render.world_to_screen(self.cam, self.perch, f)[:2]]}
        return out

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        self.scene.camera = self.cam
        M.setup_dof(self.scene, None, None, cam=self.cam)        # client rule: no depth of field, ever
        self.scene.cycles.samples = samples
        return render.render_frames([bf(shot, g) for g in gs], out_dir, scale=scale, threads=threads, scene=self.scene,
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


if __name__ == "__main__":
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    Tk = None
    if cmd in ("probe", "stills"):
        Tk = Take("preview")
        for shot in shots:
            gs = [g for g in parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
            if not gs:
                gs = [RANGES[shot][0], (RANGES[shot][0] + RANGES[shot][1]) // 2, RANGES[shot][1]]
            Tk.pose(shot, gs)
            for g in gs:
                print(json.dumps(Tk.report(shot, g)), flush=True)
                if cmd == "stills":
                    out = sys.argv[4]; os.makedirs(out, exist_ok=True)
                    scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
                    samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
                    st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                    os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
                    print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        for shot in shots:
            gs = [g for g in parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
            out = os.path.join(HERE, "raw", "s%d" % shot)
            os.makedirs(out, exist_ok=True)
            todo = []
            for g in gs:
                png, js = os.path.join(out, "g_%04d.png" % g), os.path.join(out, "g_%04d.json" % g)
                ok = os.path.exists(png) and os.path.exists(js)
                if ok:
                    m = json.load(open(js)); ok = m.get("scale") == scale and m.get("samples") == samples
                if not ok:
                    todo.append(g)
            print("final: shot %d, %d to render, %d done" % (shot, len(todo), len(gs) - len(todo)), flush=True)
            if not todo:
                continue
            if Tk is None:
                Tk = Take("final")
            Tk.pose(shot, todo)
            for g in todo:
                st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                png = os.path.join(out, "g_%04d.png" % g)
                os.replace(st["path"], png)
                rep = Tk.report(shot, g)
                rep.update(wall=round(st["wall"], 2), cpu=round(st["cpu"], 2), scale=scale, samples=samples, retried=st.get("retried"))
                json.dump(rep, open(png[:-4] + ".json.tmp", "w")); os.replace(png[:-4] + ".json.tmp", png[:-4] + ".json")
                print("shot %d g %d  %.1f s wall  %.1f s cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
