#!/usr/bin/env python3
"""shot.py -- film 16 take s18 = shot 18 (LINE line_road / DUSK): the mocker in the open buggy (mule in the shafts) taunts Morse.
Shot g 1119..1225 (37.30-40.86 s), handles 9 f each side (g 1110..1234).  Hard cut in (continuity: shot 17 is the key crate at the furrow
end; here a different place, on the road) and hard cut out to the dissolve of shot 19.
LIP-SYNC ONLY in the quote 38.46-40.80 s (event frames 1157..1227): talk_mouth(g); before it the mouth is 'flat' (smug, leaning out),
laughing + tears from the blink at 1154; belly bounce +/-0.06 D at 3 Hz from there.  The mule is a cast16 card (harness 2, walk), the buggy
rolls along +x at 1.4 D/s (wheels turn); the camera tracks it low from the furrow side (pipe + spoil ridge in the foreground).
SNAP x1.7 with a pan on "ใต้ดินแล้ว" (40.12 s -> g 1207).
    python3 shot.py camreport | probe a:b | stills a:b out [scale] | final a:b[:step] [scale] [samples]"""
import math, os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import c16 as C
import bpy
from mathutils import Vector
TG, cast16, actors = C.TG, C.cast16, C.actors
bf, u_of, lerp, blink = C.bf, C.u_of, C.lerp, C.blink
WORK = os.path.join(HERE, "work")
G0, G1 = C.g_bound(37.30), C.g_bound(40.86)      # 1119 .. 1226 (exclusive)
H = 9
GA, GZ = G0 - H, G1 + H - 1
GS = list(range(GA, GZ + 1))
Q0, Q1 = C.g_of(38.46), C.g_of(40.80)            # lip-sync window 1157 .. 1227
G_LAUGH = Q0 - 3                                  # expression change on the closed frame of a blink
G_WORD = C.g_of(40.12)                            # 1207 "ใต้ดินแล้ว"
SNAP = (G_WORD - 3, G_WORD + 9)
V = 3.0 / 30.0                                    # buggy speed, D per frame
X0 = 62.0
bx = lambda g: X0 + V * (g - GA)

SUBJ0 = Vector((X0 - 0.15, -2.3, 3.5))             # mocker's chest / head, road
OFF = Vector((0.7, -3.75, -1.2))                   # camera: furrow side, low (z ~ 1.3), pitch ~ 16 deg
CAM = C.CamPath(SUBJ0 + OFF, SUBJ0, GA, GZ, push=0.05, slide_px=50.0, arc_deg_s=12.0, decay=0.1,
                snaps=[dict(g=SNAP, k=1.4, peak=1.9, shift=(-0.8, 0.0))])
WIDE_OFF = Vector((1.5, -10.5, -1.6))
G_ARRIVE = 1160                                    # the opening wide reframes onto the mocker by the time the lips start



def cam_pose(g):
    loc, look = CAM.at(g)
    d = Vector((1.0 * V * (g - GA), 0, 0))
    loc, look = loc + d, look + d
    w = 1.0 - u_of(g, GA + 6, G_ARRIVE, "quint")           # 1 = opening wide (mocker, buggy, mule head), 0 = the medium
    if w > 0:
        wl = Vector((X0 + 3.9, -2.3, 3.0)) + Vector((V * (g - GA) * 1.0, 0, 0))
        wloc = wl + WIDE_OFF
        loc, look = loc.lerp(wloc, w), look.lerp(wl, w)
    return loc, look


def bob(g, ph=0.0, amp=0.05):
    """the buggy jolting on the road: ~3 Hz"""
    return amp * math.sin(2 * math.pi * 3.0 * g / 30.0 + ph)


def mocker_pose(g):
    p = dict(cast16.STORY16["mocker_taunt_buggy"][1])
    if g >= Q0 - 3 and g <= Q1 + 3 and Q0 <= g <= Q1:
        p["mouth"] = cast16.talk_mouth(g, 1.0)
    else:
        p["mouth"] = "flat"
    if g < G_LAUGH:
        p["expr"] = "smug"; p.pop("fx", None)
    p["blink"] = blink(g, [G_LAUGH - 1, 1180, 1214])
    ph = math.sin(2 * math.pi * 3.0 * g / 30.0)
    laugh = u_of(g, G_LAUGH, G_LAUGH + 6)
    p["squash"] = (1.01 + 0.035 * ph * laugh, 0.99 - 0.035 * ph * laugh)
    p["head_roll"] = p.get("head_roll", 0) + 3.0 * math.sin(g * 0.2)
    p["t"] = g / 30.0
    return p, 0.09 * ph * laugh


def texture_buggy():
    """the set's buggy panels are flat green: add painted plank grain + weathering (wave bands + noise) to the green / wood / red materials."""
    for o in bpy.data.objects:
        if not o.name.startswith("buggy_") or o.type != "MESH":
            continue
        for sl in o.material_slots:
            m = sl.material
            if m is None or not m.use_nodes or m.get("s18_tex"):
                continue
            nt = m.node_tree
            bsdf = next((n for n in nt.nodes if n.type == "BSDF_PRINCIPLED"), None)
            if bsdf is None:
                continue
            m["s18_tex"] = 1
            base = bsdf.inputs["Base Color"]
            src = base.links[0].from_socket if base.links else None
            tc = nt.nodes.new("ShaderNodeTexCoord")
            wv = nt.nodes.new("ShaderNodeTexWave")
            wv.wave_type, wv.bands_direction = "BANDS", "Z"
            wv.inputs["Scale"].default_value = 11.0
            wv.inputs["Distortion"].default_value = 3.0
            wv.inputs["Detail"].default_value = 3.0
            nz = nt.nodes.new("ShaderNodeTexNoise")
            nz.inputs["Scale"].default_value = 55.0
            nz.inputs["Detail"].default_value = 8.0
            mixn = nt.nodes.new("ShaderNodeMixRGB")
            mixn.blend_type, mixn.inputs[0].default_value = "MULTIPLY", 1.0
            ramp = nt.nodes.new("ShaderNodeValToRGB")
            ramp.color_ramp.elements[0].color = (0.30, 0.32, 0.30, 1)
            ramp.color_ramp.elements[1].color = (1.15, 1.15, 1.15, 1)
            nt.links.new(tc.outputs["Object"], wv.inputs["Vector"])
            nt.links.new(tc.outputs["Object"], nz.inputs["Vector"])
            mf = nt.nodes.new("ShaderNodeMath")
            mf.operation = "MULTIPLY_ADD"
            nt.links.new(wv.outputs["Fac"], mf.inputs[0])
            mf.inputs[1].default_value = 0.9
            nt.links.new(nz.outputs["Fac"], mf.inputs[2])
            nt.links.new(mf.outputs[0], ramp.inputs[0])
            if src is not None:
                nt.links.new(src, mixn.inputs[1])
            else:
                mixn.inputs[1].default_value = tuple(base.default_value)
            nt.links.new(ramp.outputs[0], mixn.inputs[2])
            nt.links.new(mixn.outputs[0], base)
            bump = nt.nodes.new("ShaderNodeBump")
            bump.inputs["Strength"].default_value = 0.35
            nt.links.new(nz.outputs["Fac"], bump.inputs["Height"])
            nt.links.new(bump.outputs["Normal"], bsdf.inputs["Normal"])


class Take(C.Take):
    def __init__(self, quality="preview"):
        C.Take.__init__(self, "line_road", light="DUSK", quality=quality, name="cam_s18")
        self.key_cam(bf(GA), *cam_pose(GA))
        self.scene.frame_set(bf(GA))
        sd = os.path.join(WORK, "sprites")
        TG.set_buggy(bx(GA), frame=bf(GA))
        texture_buggy()
        self.moc = self.actors["moc"] = C.make_actor("moc", "mocker", sd, canvas=cast16.CANVAS16["mocker"], cam=self.cam)
        self.mul = self.actors["mul"] = C.make_actor("mul", "mule", sd, canvas=cast16.CANVAS16_BUGGY["mule"], cam=self.cam, head_flip=False)
        self.mk = {}

    def pose(self, gs):
        for g in gs:
            f = bf(g)
            self.key_cam(f, *cam_pose(g))
            TG.set_buggy(bx(g), frame=f)
            rt = TG.STATE["buggy"]["root"]
            rt.location.z += bob(g)
            rt.keyframe_insert("location", frame=f)
            m = TG.STATE["marks"]
            _, bounce = mocker_pose(g)
            mm, ml = m["mocker_buggy"], m["mule_buggy"]
            C.place(self.moc, f, (mm[0], mm[1], mm[2] + bounce + bob(g)))
            C.place(self.mul, f, (ml[0] - 2.4, ml[1], ml[2] + bob(g, 1.3, 0.04)))
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            self.moc.pose(f, mocker_pose(g)[0], camera=self.cam)
            mp = cast16.cycle("mule", g / 30.0, "walk", 1, dict(harness=2))
            self.mul.pose(f, mp, camera=self.cam)
        self.sprites_for([(self.moc, 256), (self.mul, 256)], [bf(g) for g in gs])

    def report(self, g):
        f = bf(g)
        self.scene.frame_set(f)
        return dict(g=g, cam=[round(c, 3) for c in cam_pose(g)[0]], heads=C.head_report(self, f), mouth=("sync" if Q0 <= g <= Q1 else "flat"))

    def render(self, gs, out_dir, scale=1.0, samples=None, threads=2):
        return C.Take.render(self, [bf(g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "camreport":
        rows, worst = C.CamPath.report(CAM, GS[:-1])
        print(rows[0], rows[-1]); print("longest run under 0.25 px/frame: %d" % worst); sys.exit(0)
    gs = [g for g in C.parse(sys.argv[2]) if GA <= g <= GZ]
    if cmd in ("probe", "stills"):
        Tk = Take("preview"); Tk.pose(gs)
        for g in gs:
            print(json.dumps(Tk.report(g)), flush=True)
            if cmd == "stills":
                out = sys.argv[3]; scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
                st = Tk.render([g], out, scale=scale, samples=6)[0]
                os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
    elif cmd == "final":
        scale = float(sys.argv[3]) if len(sys.argv) > 3 else 1.0
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else TG.FINAL_SAMPLES["line"]
        out = os.path.join(HERE, "raw") if scale >= 1.0 else os.path.join(WORK, "draft")
        C.final_loop(lambda: Take("final" if scale >= 1.0 else "preview"), gs, out, scale=scale, samples=samples)
