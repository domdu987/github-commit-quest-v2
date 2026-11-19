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
V = 0.12 / 30.0                                    # the buggy rolls gently past Morse's group (taunting over his shoulder)
X0 = 62.0
bx = lambda g: X0 + V * (g - GA)
MX = lambda g: bx(g) - 0.65                       # the mocker's world x (the buggy mark)

# camera on the FIELD side (+y) of the buggy looking -y: the near side panel + a wheel in the foreground, the mocker seated above them, behind
# him the road, the furrow, the pole line and Morse's group (which he points at).  +x (the buggy's heading) is screen-LEFT, so the mule is on the left.
SUBJ0 = Vector((X0 - 0.15 - 0.9, -2.3, 2.5))
OFF = Vector((0.3, 4.5, -1.7))
CAM = C.CamPath(SUBJ0 + OFF, SUBJ0, GA, GZ, push=0.05, slide_px=28.0, arc_deg_s=9.0, decay=0.1,
                snaps=[dict(g=SNAP, k=1.3, peak=1.9, shift=(0.45, 0.0))])
WIDE_OFF = Vector((0.4, 6.4, -1.4))
G_ARRIVE = 1138                                    # the (short) opening wide reframes onto the mocker well before the lips start
GROUP = dict(morse=(60.2, -7.4), wa=(59.4, -8.2), wb=(61.3, -8.4))        # world x, y at the furrow edge, behind the buggy


def cam_pose(g):
    loc, look = CAM.at(g)
    d = Vector((0.55 * V * (g - GA), 0, 0))
    loc, look = loc + d, look + d
    w = 1.0 - u_of(g, GA + 4, G_ARRIVE, "quint")           # 1 = opening wide (mocker, buggy, mule), 0 = the medium
    if w > 0:
        wl = Vector((X0 - 0.4, -2.3, 2.5)) + d
        loc, look = loc.lerp(wl + WIDE_OFF, w), look.lerp(wl, w)
    return loc, look


def bob(g, ph=0.0, amp=0.05):
    """the buggy jolting on the road: ~3 Hz"""
    return amp * math.sin(2 * math.pi * 3.0 * g / 30.0 + ph)


def hand_pt(g):
    """world target of the pointing index finger: out to screen-right (-x) at shoulder height, toward Morse's group"""
    return Vector((MX(g) - 1.25, -2.7, 3.15))


def mocker_pose(g):
    p = dict(cast16.STORY16["mocker_taunt_buggy"][1])
    if Q0 <= g <= Q1:
        p["mouth"] = cast16.talk_mouth(g, 1.0)
    else:
        p["mouth"] = "flat"
    turn = u_of(g, 1160, 1182)                                               # head turns toward the group well BEFORE the snap
    if g < G_LAUGH:
        p["expr"] = "smug"; p.pop("fx", None)
    elif g >= 1170:
        p["expr"] = "excited"                                                # eyes OPEN, on the group (the laugh squint ends on the blink at 1169)
        p["fx"] = ["tears"]
        p["gaze"] = (1.0, 0.55)
    p["blink"] = blink(g, [G_LAUGH - 1, 1169, 1196, 1214])
    ph = math.sin(2 * math.pi * 3.0 * g / 30.0)
    laugh = u_of(g, G_LAUGH, G_LAUGH + 6)
    p["squash"] = (1.01 + 0.035 * ph * laugh, 0.99 - 0.035 * ph * laugh)
    p["head_roll"] = p.get("head_roll", 0) + 3.0 * math.sin(g * 0.2)
    p["yaw"] = lerp(0.45, 0.85, turn)
    p["legs"] = dict(crouch=0.75, spread=0.05)                               # seated: knees bent, no stride
    arm = dict(p.get("arm_r", {}))
    arm.update(shape="point", bend=0.0, stretch=1.0)
    p["arm_r"] = arm
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
            tint = nt.nodes.new("ShaderNodeMixRGB")
            tint.blend_type, tint.inputs[0].default_value = "MULTIPLY", 1.0
            tint.inputs[2].default_value = (0.17, 0.29, 0.42, 1.0)
            nt.links.new(mixn.outputs[0], tint.inputs[1])
            nt.links.new(tint.outputs[0], base)
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
        for o in bpy.data.objects:
            if o.name.startswith("buggy_leather"):
                o.hide_render = True              # the red seat slab hid the seated mocker
        self.moc = self.actors["moc"] = C.make_actor("moc", "mocker", sd, canvas=cast16.CANVAS16["mocker"], cam=self.cam)
        self.mul = self.actors["mul"] = C.make_actor("mul", "mule", sd, canvas=cast16.CANVAS16_BUGGY["mule"], cam=self.cam)
        self.mk = {}
        self.hand_err = {}
        self.grp = {}
        for nm, cast_ in (("morse", "morse16"), ("wa", cast16.key16("worker_a")), ("wb", cast16.key16("worker_b"))):
            self.grp[nm] = self.actors["g_" + nm] = C.make_actor("g_" + nm, cast_, sd, cam=self.cam)

    def pose(self, gs):
        for g in gs:
            f = bf(g)
            self.key_cam(f, *cam_pose(g))
            TG.set_buggy(bx(g), frame=f)
            for o in bpy.data.objects:
                if o.name.startswith("buggy_leather"):
                    C.key_vis(o, False, f)                    # the red seat slab hid the seated mocker (visibility is keyed by set_buggy: re-key it)
            rt = TG.STATE["buggy"]["root"]
            rt.location.z += bob(g)
            rt.keyframe_insert("location", frame=f)
            m = TG.STATE["marks"]
            _, bounce = mocker_pose(g)
            mm, ml = m["mocker_buggy"], m["mule_buggy"]
            C.place(self.moc, f, (mm[0], mm[1], mm[2] + bounce + bob(g)))
            C.place(self.mul, f, (ml[0] - 2.4, ml[1], ml[2] + bob(g, 1.3, 0.04)))
            for nm, (gx, gy) in GROUP.items():
                C.place(self.grp[nm], f, (gx, gy, 0.35))
        for g in gs:
            f = bf(g)
            self.scene.frame_set(f)
            _, hi = self.moc.pose(f, mocker_pose(g)[0], hands={"r": {"hand": tuple(hand_pt(g))}}, camera=self.cam)
            self.hand_err[g] = round(max([v.get("error", 0.0) for v in hi.values()] or [0.0]), 3)
            mp = cast16.cycle("mule", g / 40.0, "walk", -1, dict(harness=2))
            self.mul.pose(f, mp, camera=self.cam)
            gp = {"morse": dict(cast16.STORY16["morse_clutch_coil"][1], mirror=True),
                  "wa": dict(cast16.STORY16["worker_a_lean_shovel"][1], mirror=True),
                  "wb": dict(cast16.STORY16["worker_b_lean_shovel"][1], mirror=True)}
            for nm, pp in gp.items():
                pp["lean"] = pp.get("lean", 0) + 2.0 * math.sin(g * 0.13 + len(nm))
                pp["blink"] = blink(g, [1125 + 7 * len(nm), 1170 + 5 * len(nm), 1210])
                pp["t"] = g / 30.0
                self.grp[nm].pose(f, pp, camera=self.cam)
        self.sprites_for([(self.moc, 256), (self.mul, 256), (self.grp['morse'], 256), (self.grp['wa'], 256), (self.grp['wb'], 256)], [bf(g) for g in gs])

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
