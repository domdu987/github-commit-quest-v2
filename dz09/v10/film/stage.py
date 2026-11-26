"""stage.py -- the film stage: the v11 set + the v8 flat cast + props, and the helpers the shot scripts use (bpy).

    F = Stage(tier="draft", width=360, height=640)      # aspect comes from width / height
    F.begin(shot_module)                                 # reset to the neutral stage, run shot.setup(F)
    post = F.frame(shot_module, g)                       # camera, poses, lights for film frame g -> post options
    F.render(out_noext, g, post)

Nothing outside v10/film is edited: v11/set and v8/cast are imported (v8's raster cache lives in its own tmp/).
"""
import os, sys, math, json, time
import numpy as np
import common as C
from common import PROJ, HERE, FPS

sys.path.insert(0, os.path.join(PROJ, "v11", "set"))
sys.path.append(os.path.join(PROJ, "v8", "cast"))
import bpy
from mathutils import Vector, Matrix, Euler, Quaternion
import beauty as B
import presets, kit
import stage8 as S8
import draw8, phone8
import cutter as CT

TEX = os.path.join(HERE, "tex")
os.makedirs(TEX, exist_ok=True)

# tier -> (set quality name, samples, render percentage or None = the quality's own)
TIERS = {
    "draft": dict(q="preview", spp=2, pct=100, note="2 spp + OIDN at 100 % of the asked size; use at 360x640"),
    "preview": dict(q="preview", spp=4, pct=100, note="4 spp at 100 %"),
    "final": dict(q="final", spp=5, pct=None, note="5 spp at 75 % then Lanczos (the set's final tier)"),
    "final8": dict(q="final8", spp=8, pct=None, note="8 spp at 75 %: holds and inserts"),
}
PCT_FORCE = 0            # run.py --pct N: one render scale for the whole run
KONG_H, CREW_H, DRV_H, DRV_HIP_Z = 2.86, 2.80, 2.03, 1.12
WARM = (1.0, 0.72, 0.45)
COOL = (0.70, 0.82, 1.0)


# ------------------------------------------------------------------------------------ cutter drawing with moving jaws
_prop_svg0 = draw8.prop_svg


def _prop_svg(kind, P, sp=None):
    """draw8's cutter with a `jaw` key: 1 = open V (draw8's own drawing), 0 = closed bite."""
    if kind == "cutter" and P.get("two"):
        return CT.prop_svg(P, sp)                          # the two-handed tool (cutter.py)
    if kind != "cutter" or "jaw" not in P:
        return _prop_svg0(kind, P, sp)
    D = draw8; f = D.f; INK = D.INK
    bars = int(P.get("bars", 3)); wet = P.get("wet", False)
    org = "#ee7a1f" if not wet else "#d0621a"
    o = D.path("M-0.20 -0.06 C-0.32 -0.34 0.24 -0.40 0.18 -0.08", "none", INK, 0.10)
    o += D.path("M-0.20 -0.06 C-0.32 -0.34 0.24 -0.40 0.18 -0.08", "none", "#2a2a2a", 0.05)
    o += '<rect x="-0.13" y="-0.10" width="0.26" height="0.62" rx="0.07" fill="%s" stroke="%s" stroke-width="0.03"/>' % (org, INK)
    o += '<rect x="-0.11" y="-0.06" width="0.06" height="0.52" rx="0.03" fill="#fbc48d" opacity="0.55"/>'
    o += '<rect x="-0.13" y="0.10" width="0.26" height="0.07" fill="#f4f2ec" stroke="%s" stroke-width="0.016"/>' % INK
    o += '<rect x="-0.105" y="0.21" width="0.21" height="0.22" rx="0.02" fill="#151515" stroke="%s" stroke-width="0.02"/>' % INK
    colr = {3: "#3ee05a", 2: "#f2d22e", 1: "#ff3b30", 0: "#333"}[max(0, min(3, bars))]
    for k in range(3):
        on = (2 - k) < bars
        o += '<rect x="-0.075" y="%s" width="0.15" height="0.048" rx="0.008" fill="%s"/>' % (f(0.235 + k * 0.064), colr if on else "#3a3a3a")
    o += '<rect x="-0.15" y="0.50" width="0.30" height="0.11" rx="0.03" fill="#222" stroke="%s" stroke-width="0.024"/>' % INK
    o += D.ell(0, 0.66, 0.06, 0.06, "#bfc4ca", INK, 0.02)
    close = (1.0 - float(P["jaw"])) * 13.0                       # degrees each jaw swings in
    for side in (-1, 1):
        jaw = [(side * 0.02, 0.62), (side * 0.16, 0.70), (side * 0.20, 0.92), (side * 0.11, 1.10), (side * 0.05, 1.04), (side * 0.10, 0.88),
               (side * 0.04, 0.72)]
        j = D.path(D.smooth_d(jaw, True, 0.25), "#b9bfc6", INK, 0.026)
        j += D.path(D.pts_d([(side * 0.07, 0.74), (side * 0.15, 0.90), (side * 0.10, 1.02)], False), "none", "#dfe3e8", 0.016)
        o += D.g(j, "rotate(%s 0 0.66)" % f(side * close))
    o += D.ell(0, 0.66, 0.03, 0.03, "#555")
    return D.g(o, "translate(%s %s) rotate(%s)%s" % (f(P["at"][0]), f(P["at"][1]), f(P.get("angle", 0.0)),
                                                     " scale(%s)" % f(P["scale"]) if P.get("scale") else ""))


draw8.prop_svg = _prop_svg


# ------------------------------------------------------------------------------------------------ v3: faces
# "serious": the sheet's determined brows without its smile (S06 read as a smirk).
draw8.EXPR["serious"] = dict(eyes="oval", brows=(20, -0.005), mouth=("flat", 0.8))
# The wet specs put three small pale rain beads on the face.  At 360-720 px they are 1-3 px dots that the denoiser
# turns into a shimmering patch between the eyes, so the film draws the faces without them (hair beads stay).
import re as _re
_face0 = draw8._face
_BEAD = _re.compile(r'<path d="[^"]*" fill="#cfe6f5"/>')


def _face_clean(*a, **k):
    return _BEAD.sub("", _face0(*a, **k))


draw8._face = _face_clean

# Skin cards (head, face) get their own copy of the flat card shader: the even fill is nearly neutral (the sheet's
# paper-white / the driver's grey-green stay what they are, with a mild cool tint), it carries more of the level, and
# the red / blue beacon lights are light-linked away from them, so a face no longer swings pink <-> blue at 2 Hz.
SKIN = dict(TINT_MIX=0.70, AMB=1.0, DIR=1.0, BACK=1.0, no_beacon=True, layers=("head", "face"))


def skin_group():
    g = bpy.data.node_groups.get("DZ8_flat_skin")
    if g is None:
        g = S8.flat_group().copy(); g.name = "DZ8_flat_skin"
    return g


def tune_skin():
    """call after every S8.tune_flat(): the skin copy follows the shot's flat look with the SKIN overrides."""
    FL = S8.FLAT; n = skin_group().nodes; k = SKIN["TINT_MIX"]
    lum_t = 0.2126 * FL["TINT"][0] + 0.7152 * FL["TINT"][1] + 0.0722 * FL["TINT"][2]
    tint = tuple(c + (max(lum_t, 0.6) - c) * k for c in FL["TINT"])          # pulled toward neutral, never darker than 0.6
    n["amb"].inputs["Strength"].default_value = FL["AMB"] * SKIN["AMB"] / max(FL["EXPO"], 1e-3)
    n["amb_tint"].inputs[7].default_value = tint + (1.0,)
    n["dir_k"].inputs[7].default_value = (FL["DIR"] * SKIN["DIR"],) * 3 + (1.0,)
    n["back_k"].inputs[7].default_value = (FL["BACK"] * SKIN["BACK"],) * 3 + (1.0,)
    n["nmap"].inputs["Strength"].default_value = FL["NSTR"]
    n["ink_min"].inputs["Min"].default_value = FL["INK_MIN"]; n["ink_lum"].inputs[1].default_value = FL["INK_LUM"]


def skin_cards(a):
    """point the head / face card materials of Actor8 `a` at the skin shader and keep the beacons off them."""
    c = bpy.data.collections.get("FILM_skin") or bpy.data.collections.new("FILM_skin")
    g = skin_group(); new = False
    for nm in SKIN["layers"]:
        ob = a.cards.get(nm)
        if ob is None: continue
        for m in ob.data.materials:
            for nd in m.node_tree.nodes:
                if nd.type == "GROUP" and nd.node_tree is not g and nd.node_tree.name.startswith("DZ8_flat"): nd.node_tree = g
        if ob.name not in c.objects:
            c.objects.link(ob); new = True
    if new:
        for co in c.collection_objects: co.light_linking.link_state = "EXCLUDE"
        for L in bpy.data.objects:
            if L.type == "LIGHT" and L.name.startswith("beacon_"):
                L.light_linking.receiver_collection = c if SKIN["no_beacon"] else None


# ---------------------------------------------------------------- update-free versions of two Actor8 methods (speed)
# stage8 calls view_layer.update() inside both (80 ms each on this 2800-object scene, 50 times per frame).  The actor
# roots are unparented, so their world transform is just location + facing; lights do not move within a frame.
def _cam_rel_fast(self, camera):
    if camera is None:
        return 0.0
    p = self.root.location; c = camera.location
    dx, dy = c.x - p.x, c.y - p.y
    if dx * dx + dy * dy < 1e-12:
        return 0.0
    return (math.degrees(math.atan2(dx, -dy)) - self.facing + 180) % 360 - 180


def _place_proxy_fast(self):
    L = self.shadow_light
    try:
        if L is not None: L.name
    except ReferenceError:
        L = self.shadow_light = None
    if L is None:
        self.proxy.rotation_euler = (0, 0, self.pivot.rotation_euler[2]); self.proxy.location = (0, 0, 0)
        return
    p = Vector(self.root.location)
    if L.data.type == "SUN":
        d = L.matrix_world.to_3x3() @ Vector((0, 0, -1))
    else:
        d = p + Vector((0, 0, 1.5 * self.sc)) - L.matrix_world.translation
    dh = Vector((d.x, d.y, 0))
    if dh.length < 1e-4: dh = Vector((0, 1e-3, 0))
    dh.normalize()
    dl = Matrix.Rotation(-math.radians(self.facing), 3, "Z") @ dh
    yaw = math.degrees(math.atan2(-dl.x, dl.y))
    self.proxy.rotation_euler = (-math.radians(S8.PROXY_TILT), 0, math.radians(yaw))
    self.proxy.location = (0, 0, 0)


S8.Actor8._cam_rel = _cam_rel_fast
S8.Actor8._place_proxy = _place_proxy_fast


# ------------------------------------------------------------------------------------------------ small bpy helpers
def _mat_emit(name, col, strength=1.0):
    m = bpy.data.materials.get(name)
    if m is None:
        m = bpy.data.materials.new(name); m.use_nodes = True
        nt = m.node_tree; nt.nodes.clear()
        o = nt.nodes.new("ShaderNodeOutputMaterial"); e = nt.nodes.new("ShaderNodeEmission"); e.name = "Emission"
        nt.links.new(e.outputs[0], o.inputs[0])
    e = m.node_tree.nodes["Emission"]
    e.inputs["Color"].default_value = tuple(col) + (1.0,); e.inputs["Strength"].default_value = strength
    return m


def _mat_pbr(name, col, rough=0.5, metal=0.0):
    m = bpy.data.materials.get(name)
    if m is None:
        m = bpy.data.materials.new(name); m.use_nodes = True
        b = m.node_tree.nodes["Principled BSDF"]
        b.inputs["Base Color"].default_value = tuple(col) + (1.0,)
        b.inputs["Roughness"].default_value = rough; b.inputs["Metallic"].default_value = metal
    return m


def _mat_image_emit(name, path, strength=1.0):
    m = bpy.data.materials.get(name)
    if m is None:
        m = bpy.data.materials.new(name); m.use_nodes = True
        nt = m.node_tree; nt.nodes.clear()
        o = nt.nodes.new("ShaderNodeOutputMaterial"); e = nt.nodes.new("ShaderNodeEmission"); e.name = "Emission"
        t = nt.nodes.new("ShaderNodeTexImage"); t.name = "img"; t.extension = "EXTEND"
        nt.links.new(t.outputs["Color"], e.inputs["Color"]); nt.links.new(e.outputs[0], o.inputs[0])
    nt = m.node_tree
    nt.nodes["img"].image = bpy.data.images.load(path, check_existing=True)
    nt.nodes["Emission"].inputs["Strength"].default_value = strength
    return m


def hexrgb(h):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c)


def _box(name, size, loc, mat, parent=None, rot=(0, 0, 0), bevel=0.0, idx=4):
    bpy.ops.mesh.primitive_cube_add(size=1.0)
    ob = bpy.context.active_object
    ob.name = name; ob.scale = size; ob.location = loc; ob.rotation_euler = rot
    ob.data.materials.append(mat)
    if bevel > 0:
        md = ob.modifiers.new("bv", "BEVEL"); md.width = bevel; md.segments = 2
    ob.pass_index = idx
    if parent is not None:
        ob.parent = parent
    return ob


def _cyl(name, r, h, loc, mat, parent=None, rot=(0, 0, 0), idx=4):
    bpy.ops.mesh.primitive_cylinder_add(radius=r, depth=h, vertices=14)
    ob = bpy.context.active_object
    ob.name = name; ob.location = loc; ob.rotation_euler = rot; ob.data.materials.append(mat); ob.pass_index = idx
    if parent is not None:
        ob.parent = parent
    return ob


def _plane(name, w, h, mat, parent=None, loc=(0, 0, 0), rot=(0, 0, 0), idx=4):
    me = bpy.data.meshes.new(name)
    me.from_pydata([(-w / 2, -h / 2, 0), (w / 2, -h / 2, 0), (w / 2, h / 2, 0), (-w / 2, h / 2, 0)], [], [(0, 1, 2, 3)])
    uv = me.uv_layers.new()
    for i, c in enumerate([(0, 0), (1, 0), (1, 1), (0, 1)]):
        uv.data[i].uv = c
    me.materials.append(mat)
    ob = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(ob)
    ob.location = loc; ob.rotation_euler = rot; ob.pass_index = idx
    if parent is not None:
        ob.parent = parent
    return ob


def _empty(name, loc=(0, 0, 0)):
    ob = bpy.data.objects.new(name, None); bpy.context.scene.collection.objects.link(ob); ob.location = loc
    return ob


def tree(ob):
    return [ob] + list(ob.children_recursive)


def facing(v):
    """facing_deg of an actor that looks along the horizontal vector v (0 = toward -Y)."""
    return math.degrees(math.atan2(v[0], -v[1]))


# ====================================================================================================== actor wrapper
class Act:
    """one puppet: desired state per frame (loc, facing, view, pose) -> the fewest Actor8.pose() calls."""

    def __init__(self, F, name, spec, height, ppd=200, seated=False):
        self.F = F; self.name = name
        self.a = S8.Actor8(name, spec, height=height, ppd=ppd, mode="flat")
        self.a.set_pass_index(2)
        if seated:
            self.a.pitch_override = 0.0
        self.key = None
        self.visible = False
        self.posed = False
        self.loc = (0, 0, 0); self.face = 0.0
        self.pose_d = {}
        self.view = None; self.s = None
        self.breath = 0.0
        self.pidx = 2

    def set(self, loc=None, face=None, view="keep", s="keep", idx=None, **pose):
        """loc (x, y, z of the soles), face = facing degrees, view/s = force a drawing ("front" / "q" / "side" / "back",
        +1 = faces screen-right), pose keys as draw8 (expr, mouth, blink, head, lean, arm_n, legs, prop_n, ...)."""
        self.visible = True
        if loc is not None: self.loc = tuple(loc)
        if face is not None: self.face = face
        if view != "keep": self.view = view
        if s != "keep": self.s = s
        if idx is not None: self.pidx = idx
        if pose: self.pose_d = pose
        return self

    def hide(self):
        self.visible = False

    def _orient(self, cam):
        a = self.a
        rel = a._cam_rel(cam)
        yaw_p = a.walk_lock if a.walk_lock is not None else rel
        if a.pitch_override is not None:
            pitch = a.pitch_override
        else:
            fz = (cam.matrix_world.to_3x3() @ Vector((0, 0, -1))).z
            pitch = math.degrees(math.asin(max(-1.0, min(1.0, -fz)))) * S8.FLAT["PITCH"]
        pitch = max(-S8.FLAT["PITCH_MAX"], min(S8.FLAT["PITCH_MAX"], pitch))
        a.pitch = pitch
        a.pivot.rotation_euler = (-math.radians(pitch), 0, math.radians(yaw_p))
        if pitch and a.pitch_anchor:
            c = Vector((0, 0, a.pitch_anchor * a.height))
            a.pivot.location = c - (a.pivot.rotation_euler.to_matrix() @ c)
        else:
            a.pivot.location = (0, 0, 0)
        if a.contact:
            a.contact.rotation_euler = (0, 0, math.radians(yaw_p))
        a._place_proxy()

    def apply(self, cam):
        a = self.a
        if not self.visible:
            if self.posed: a.hide(True)
            return
        a.place(self.loc, self.face)
        a.view_override = self.view
        pose = dict(self.pose_d)
        if self.s is not None: pose["s"] = self.s
        rel = a._cam_rel(cam)
        v = self.view or S8.view_for(rel)
        s = pose.get("s", -1 if rel > 0.5 else 1)
        if "_hold" in pose:                                 # two-handed cutter: needs the drawing's side, so it is resolved here
            h = pose.pop("_hold")
            if v in ("q", "side"): pose.update(CT.hold(a.spec, v, s, **h))
            else: pose.update(arm_r="hold_cutter", prop_r=dict(type="cutter", bars=h.get("bars", 3), wet=True), arm_l="down")
        key = json.dumps([v, s, pose], sort_keys=True, default=str)
        if key != self.key or not self.posed:
            for attempt in range(3):
                try:
                    a.pose(pose, camera=cam); break
                except Exception as ex:                    # a half-written cache PNG from a parallel worker
                    print("pose retry", self.name, ex, flush=True); time.sleep(0.5)
            else:
                raise
            self.key = key; self.posed = True
            for o in a.objects: o.pass_index = self.pidx
        else:
            self._orient(cam)
            for o in a.objects:
                if o.pass_index != self.pidx: o.pass_index = self.pidx
        a.hide(False)
        skin_cards(a)
        for nm, ob in a.cards.items():                      # pose() hides unused layer cards; hide(False) showed them again
            if nm not in a.layers: ob.hide_render = True
        # breathing: a tiny vertical stretch about the soles (no re-raster)
        a.pivot.scale = (1.0, 1.0, 1.0 + self.breath)

    def head(self):
        return self.a.head_world()

    def pt(self, xy, z=0.0):
        return self.a.world_of(xy, z)


# ============================================================================================================== stage
class Stage:
    def __init__(self, tier="draft", width=360, height=640, threads=4, spp=None):
        self.tier = tier; self.W, self.H = width, height
        self.v = height >= width                              # vertical frame
        self.aspect = "9:16" if self.v else "16:9"
        T = TIERS[tier]
        t0 = time.time()
        self.A = A = B.build()
        B.setup_render(T["q"], threads=threads)
        sc = self.sc = bpy.context.scene
        sc.cycles.samples = spp or T["spp"]
        self.spp = sc.cycles.samples
        if T["pct"]: B.X._STATE["pct"] = T["pct"]
        self._pct0 = B.X._STATE.get("pct", 100)                # the tier's render scale; a shot's PCT = {tier: n} overrides it
        sc.render.use_motion_blur = False                      # puppets on twos: no motion blur, ever
        sc.cycles.adaptive_min_samples = min(sc.cycles.adaptive_min_samples, sc.cycles.samples)
        sc.cycles.transparent_max_bounces = max(sc.cycles.transparent_max_bounces, 32)
        sc.render.resolution_x, sc.render.resolution_y = width, height
        sc.render.resolution_percentage = B.X._STATE.get("pct", 100)
        sc.render.fps = FPS
        S8.set_mode("flat")
        th = A["hero_heading"]
        self.fwd = Vector((-math.sin(th), math.cos(th), 0.0)); self.right = Vector((math.cos(th), math.sin(th), 0.0))
        self.K = Vector(A["kong_mark"]); self.seat = Vector(A["driver_seat"]); self.door_mid = Vector(A["door_mid"])
        self.PM = Vector(A["kong_phone_mark"])
        self.up = Vector((0, 0, 1))
        self.cam = B.X.make_camera()
        sc.camera = self.cam
        for ob in bpy.data.objects:
            for con in ob.constraints:
                if con.type == "TRACK_TO": con.target = self.cam
        # cast
        self.kong = Act(self, "kong", "kong_wet", KONG_H, ppd=240)
        self.crew = Act(self, "crew", "crew_wet", CREW_H, ppd=240)
        self.drv = Act(self, "driver", "driver", DRV_H, ppd=240, seated=True)
        self.drv_out = Act(self, "driver_out", "driver", 2.70, ppd=240)          # the driver once he is out of the seat
        self.cast = [self.kong, self.crew, self.drv, self.drv_out]
        self.extras = []
        self._build_extras()
        self._build_props()
        self._door0 = None
        self._hid = []
        self._moved = []
        self._fills = {}
        self.shot = None
        self.glare_log = []
        self.lamp_info = None
        print("stage built in %.1f s" % (time.time() - t0), flush=True)

    # ------------------------------------------------------------------------------------------------ helpers
    def pick(self, vert, wide):
        return vert if self.v else wide

    def P(self, base, f=0.0, r=0.0, z=0.0):
        """base + f along the hero car's forward + r toward the driver's side (the action side) + z up."""
        return Vector(base) + self.fwd * f + self.right * r + Vector((0, 0, z))

    def free(self, x, y, r=0.7):
        """is the deck clear around (x, y)?  rays down from 6 D."""
        dg = bpy.context.evaluated_depsgraph_get()
        for dx, dy in ((0, 0), (r, 0), (-r, 0), (0, r), (0, -r)):
            hit, loc, n, i, ob, m = self.sc.ray_cast(dg, Vector((x + dx, y + dy, 6.0)), Vector((0, 0, -1)))
            if hit and loc.z > 0.25:
                return False
        return True

    def top(self, x, y, z0=8.0):
        dg = bpy.context.evaluated_depsgraph_get()
        hit, loc, n, i, ob, m = self.sc.ray_cast(dg, Vector((x, y, z0)), Vector((0, 0, -1)))
        return loc.z if hit else 0.0

    # ------------------------------------------------------------------------------------------------ extras
    EXTRA_SPOTS = [  # (x, y, facing vector, idle pair)   lane gaps: -6.55 (L1/L2), -12.35 (L2/L3), +: opposing side
        (-6.9, 12.0, (0.3, 1.0)), (-6.1, 4.5, (-0.4, 1.0)), (-7.0, -4.0, (0.5, 1.0)), (-5.9, -13.0, (-0.2, 1.0)),
        (-12.6, 8.0, (0.6, 1.0)), (-12.0, 47.5, (0.5, -1.0)), (-6.3, 52.0, (-0.3, -1.0)), (-12.7, 58.0, (0.4, -1.0)),
        (-6.8, 64.0, (0.2, -1.0)), (-1.2, 44.0, (-0.8, -0.6)),
    ]

    def _build_extras(self):
        specs = draw8.extras(10, seed=0)
        for i, sp in enumerate(specs):
            x, y, fv = self.EXTRA_SPOTS[i]
            ok = False
            for k in range(40):                             # nearest free patch of deck
                dx = ((k % 5) - 2) * 0.35; dy = (k // 5) * 0.8 * (1 if k % 2 else -1)
                if self.free(x + dx, y + dy, 0.55):
                    x, y, ok = x + dx, y + dy, True; break
            e = Act(self, "extra%d" % i, sp, 2.55 + 0.3 * C.hash01(i, 3), ppd=110)
            e.spec_d = sp
            e.set(loc=(x, y, 0.0), face=facing(fv))
            e.home = (x, y, 0.0); e.ok = ok; e.i = i
            self.extras.append(e)

    def extras_frame(self, t):
        """idle life for the background people: two alternating drawings each (look / gesture), blinks, own rhythm."""
        for e in self.extras:
            if not e.visible: continue
            per = 1.3 + 1.4 * C.hash01(e.i, 7)
            k = int((t + 3.1 * e.i) / per) % 2
            pose = dict(e.spec_d.get("extra_pose", {}))
            pose["expr"] = e.spec_d.get("default_expr", "neutral")
            pose["head"] = (0, (-5 if k else 5) * (1 if e.i % 2 else -1), 0, 0)
            pose["gaze"] = (0.4 if k else -0.3, 0.0)
            pose["blink"] = C.blink(e.name, t)
            e.pose_d = pose

    # ------------------------------------------------------------------------------------------------ props
    def _build_props(self):
        # --- rescue radio handset (S01): body, grille, antenna, display, LED
        r = self.radio = _empty("radio_root")
        # final: the handset and the gloved hand holding it are ONE flat drawn card in the cast's style (radio_card_png);
        # the box-built radio / hand of v3 read as a stack of blocks.  Only the display and the LED are emissive planes on it.
        cpath, npath, (cx0, cy0, cx1, cy1) = radio_card_png()
        cm = S8.card_material("f_radio_card", cpath, npath, False, mode="flat")
        self.radio_card = _plane("radio_card", cx1 - cx0, cy1 - cy0, cm, r, ((cx0 + cx1) / 2, 0.0, -(cy0 + cy1) / 2), (math.radians(90), 0, 0))
        self.radio_card.visible_shadow = False
        self.radio_disp = _mat_emit("f_radio_disp", (0.10, 0.45, 1.0), 2.0)
        _plane("radio_display", 0.19, 0.10, self.radio_disp, r, (0, -0.012, 0.50), (math.radians(90), 0, 0)).visible_shadow = False
        self.radio_led = _mat_emit("f_radio_led", (1.0, 0.07, 0.03), 2.0)
        _plane("radio_ledbox", 0.045, 0.032, self.radio_led, r, (0.10, -0.012, 0.655), (math.radians(90), 0, 0)).visible_shadow = False
        L = bpy.data.lights.new("radio_led_light", "POINT"); L.color = (1.0, 0.10, 0.05); L.shadow_soft_size = 0.05
        self.radio_light = bpy.data.objects.new("radio_led_light", L); self.sc.collection.objects.link(self.radio_light)
        self.radio_light.parent = r; self.radio_light.location = (0.10, -0.22, 0.655)
        # --- phone (S11, S16): body, emissive screen, a glove thumb and the sleeve
        p = self.phone = _empty("phone_root")
        pb = _mat_pbr("f_phone_body", hexrgb("#0d0d11"), 0.22, 0.3)
        _box("phone_body", (0.46, 0.86, 0.05), (0, 0, 0), pb, p, bevel=0.03)
        self.screens = {}
        for st in ("missed", "ended", "off", "incoming"):
            self.screens[st] = screen_png(st)
        self.phone_mat = _mat_image_emit("f_phone_screen", self.screens["missed"], 1.6)
        self.phone_scr = _plane("phone_screen", 0.42, 0.80, self.phone_mat, p, (0, 0, 0.027))
        gl = _mat_pbr("f_glove", hexrgb("#17161b"), 0.75)
        _box("phone_palm", (0.62, 0.50, 0.22), (0.04, -0.34, -0.14), gl, p, bevel=0.10)
        _box("phone_thumb", (0.16, 0.34, 0.12), (0.30, -0.16, 0.03), gl, p, rot=(0, 0, math.radians(18)), bevel=0.05)
        for i in range(3):
            _box("phone_finger%d" % i, (0.13, 0.20, 0.12), (-0.27, -0.02 + i * 0.17, 0.0), gl, p, rot=(0, 0, math.radians(-8)), bevel=0.05)
        self.phone_arm = _cyl("phone_arm", 0.085, 1.5, (0.10, -1.25, -0.30), _mat_pbr("f_skin", hexrgb("#f1efe8"), 0.6), p, rot=(math.radians(78), 0, 0))
        _cyl("phone_sleeve", 0.20, 0.7, (0.10, -2.2, -0.50), _mat_pbr("f_sleeve", hexrgb("#c8581b"), 0.6), p, rot=(math.radians(78), 0, 0))
        # --- glove + forearm on the 3D cutter (S08, S09)
        cu = bpy.data.objects.get(self.A.get("cutter3d", "cutter3d"))
        self.cutter = cu
        self.cut_hand = h = _empty("cut_hand_root")
        if cu:
            loop = bpy.data.objects.get("cutter3d_loop"); fh = bpy.data.objects.get("cutter3d_fhandle")
            bpy.context.view_layer.update()
            for i, ob in enumerate((loop, fh)):
                if ob is None: continue
                c = ob.matrix_world.translation
                g = _box("cut_glove%d" % i, (0.30, 0.26, 0.24), c + Vector((0, 0, 0.10 if i == 0 else 0.16)), gl, h, bevel=0.10)
                tgt = c + (self.K + Vector((0, 0, 2.0)) + self.right * 0.6 - c).normalized() * 1.3
                d = (tgt - c); mid = c + d * 0.5
                a = _cyl("cut_arm%d" % i, 0.075, d.length, mid, bpy.data.materials["f_skin"], h)
                a.rotation_euler = d.to_track_quat("Z", "Y").to_euler()
            self.jaws = [(o, o.rotation_euler.copy()) for o in (bpy.data.objects.get("cutter3d_jaw_l"), bpy.data.objects.get("cutter3d_jaw_r")) if o]
            self.leds = []
            for i in range(3):
                o = bpy.data.objects.get("cutter3d_led%d" % i)
                if o:
                    m = _mat_emit("f_led%d" % i, (0.12, 0.84, 0.33), 14.0)
                    o.data.materials.clear(); o.data.materials.append(m); self.leds.append(m)
        # --- sparks: small hot streaks thrown from the jaws
        self.sparks = []
        sm = _mat_emit("f_spark", (1.0, 0.62, 0.22), 60.0)
        for i in range(18):
            bpy.ops.mesh.primitive_ico_sphere_add(radius=1.0, subdivisions=1)
            o = bpy.context.active_object; o.name = "spark%d" % i; o.data.materials.append(sm); o.pass_index = 4
            o.visible_shadow = False
            self.sparks.append(o)
        L = bpy.data.lights.new("spark_light", "POINT"); L.color = (1.0, 0.6, 0.25); L.shadow_soft_size = 0.1
        self.spark_light = bpy.data.objects.new("spark_light", L); self.sc.collection.objects.link(self.spark_light)
        # --- a pry bar for the crew (the set has a crowbar on the ground; this one is in his hands as a drawing prop)
        self._props_hide()

    def _props_hide(self):
        for root in (self.radio, self.phone, self.cut_hand):
            for o in tree(root): o.hide_render = True
        if self.cutter:
            for o in tree(self.cutter): o.hide_render = True
        for o in self.sparks: o.hide_render = True
        self.spark_light.hide_render = True
        self.radio_light.hide_render = True

    def show(self, root, on=True):
        for o in tree(root): o.hide_render = not on or o.name in ('phone_arm', 'phone_sleeve')

    def put(self, root, loc, rot=None, scale=None):
        root.location = loc
        if rot is not None: root.rotation_euler = rot
        if scale is not None: root.scale = (scale,) * 3

    def phone_screen(self, state, strength=1.6):
        nt = self.phone_mat.node_tree
        nt.nodes["img"].image = bpy.data.images.load(self.screens[state], check_existing=True)
        nt.nodes["Emission"].inputs["Strength"].default_value = strength

    def cutter3d(self, on=True, jaw=1.0, bars=3, hand=True, arms=True):
        """the modelled cutter at the door seam: jaw 1 open .. 0 bitten shut; bars lit (0-3)."""
        if not self.cutter: return
        for o in tree(self.cutter): o.hide_render = not on
        for o in tree(self.cut_hand): o.hide_render = not (on and hand and (arms or 'arm' not in o.name))
        for k, (o, r0) in enumerate(self.jaws):
            o.rotation_euler = (r0[0], r0[1], r0[2] + (1 - jaw) * math.radians(9.0) * (1 if k == 0 else -1))
        for i, m in enumerate(self.leds):
            m.node_tree.nodes["Emission"].inputs["Strength"].default_value = 14.0 if i < bars else 0.15

    def sparks_at(self, p, g, amount=1.0, away=None):
        """deterministic spark burst at world point p for film frame g (amount 0 = off)."""
        p = Vector(p); away = Vector(away) if away is not None else self.right
        n = int(round(len(self.sparks) * C.clamp(amount)))
        for i, o in enumerate(self.sparks):
            if i >= n:
                o.hide_render = True; continue
            life = 5 + int(4 * C.hash01(i, 1))
            birth = g - ((g + i * 3) % life)
            age = (g - birth) / float(FPS)
            h1, h2, h3 = C.hash01(i, birth, 2), C.hash01(i, birth, 3), C.hash01(i, birth, 4)
            v = away * (1.6 + 2.6 * h1) + self.fwd * (h2 - 0.5) * 3.0 + Vector((0, 0, 0.8 + 2.4 * h3))
            pos = p + v * age + Vector((0, 0, -9.0 * age * age))
            vel = v + Vector((0, 0, -18.0 * age))
            o.hide_render = pos.z < 0.02
            o.location = pos
            o.rotation_euler = vel.to_track_quat("Z", "Y").to_euler()
            k = 1.0 - age * FPS / life
            o.scale = (0.012, 0.012, 0.03 + 0.10 * k)
        self.spark_light.hide_render = n == 0
        self.spark_light.location = p + away * 0.25 + Vector((0, 0, 0.1))
        self.spark_light.data.energy = 900.0 * amount * (0.6 + 0.8 * C.hash01(g, 9))

    # ------------------------------------------------------------------------------------------------ set dressing
    def door(self, angle_deg):
        """swing the hero car's crushed driver door about its front hinge (0 = shut, 70 = pried open)."""
        ob = bpy.data.objects.get(self.A["hero_car"] + "_door_fr")
        if ob is None: return
        if self._door0 is None:
            bpy.context.view_layer.update()
            M0 = ob.matrix_world.copy()
            pts = [M0 @ Vector(c) for c in ob.bound_box]
            f = [p.dot(self.fwd) for p in pts]; r = [p.dot(self.right) for p in pts]
            hinge = self.fwd * max(f) + self.right * (max(r) - 0.05)
            self._door0 = (M0, Vector((hinge.x, hinge.y, 0.0)), ob.parent, ob.matrix_parent_inverse.copy())
        M0, h, par, mpi = self._door0
        R = Matrix.Translation(h) @ Matrix.Rotation(math.radians(angle_deg), 4, "Z") @ Matrix.Translation(-h)
        ob.matrix_world = R @ M0
        if not _GL.get('all_clear'):
            _door_glass(self, angle_deg > 5.0, only_door=True)      # the opened door's pane read as a glowing blade edge-on
        hd = bpy.data.objects.get(self.A["hero_car"] + "_handle")
        if hd is not None:
            if "m0" not in self.__dict__.setdefault("_hd", {}): self._hd["m0"] = hd.matrix_world.copy()
            hd.matrix_world = R @ self._hd["m0"]
        mr = bpy.data.objects.get(self.A["hero_car"] + "_mirror")
        if mr is not None:
            if "m1" not in self._hd: self._hd["m1"] = mr.matrix_world.copy()
            mr.matrix_world = R @ self._hd["m1"]

    def hide_roots(self, roots):
        for r in roots:
            ob = bpy.data.objects.get(r)
            if not ob: continue
            for o in tree(ob):
                if not o.hide_render: o.hide_render = True; self._hid.append(o)

    def nudge(self, name, dloc=(0, 0, 0), scale=None):
        """move (world space) / scale (about its origin) a set object for this shot only (begin() puts it back)."""
        ob = bpy.data.objects.get(name)
        if ob is None: return None
        bpy.context.view_layer.update()
        if not any(o is ob for o, _ in self._moved): self._moved.append((ob, ob.matrix_world.copy()))
        M = ob.matrix_world.copy()
        if scale is not None:
            c = M.translation.copy(); M = Matrix.Translation(c) @ Matrix.Scale(scale, 4) @ Matrix.Translation(-c) @ M
        ob.matrix_world = Matrix.Translation(Vector(dloc)) @ M          # world space: the fallen bike's own axes are tilted
        return ob

    def fill(self, name, loc=None, power=0.0, color=(0.72, 0.82, 1.0), size=0.5):
        ob = bpy.data.objects.get(name)
        if ob is None:
            ld = bpy.data.lights.new(name, "POINT"); ob = bpy.data.objects.new(name, ld); self.sc.collection.objects.link(ob)
            ob.visible_glossy = False; ob.visible_transmission = False; ob.visible_camera = False
        ob.data.energy = power; ob.data.color = color; ob.data.shadow_soft_size = size
        ob.hide_render = power <= 0
        if loc is not None: ob.location = loc
        self._fills[name] = ob
        return ob

    def foreground(self, kind, side="left", cover=0.3, depth=1.4, seed=1):
        """a dark out-of-focus framing prop built at the current camera (world geometry: the camera then moves past it)."""
        bpy.context.view_layer.update()
        presets.foreground(self.cam, kind, side=side, cover=cover, depth=depth, seed=seed)

    def lamp(self, base, aim, energy=8000.0, heads=(), head_z=None, hide=False):
        """place the warm work lamp for the shot; it is slid sideways until it is clear of every head (no glare)."""
        if hide:
            B.place_work_lamp(self.A, hide=True); self.lamp_info = None; return
        base = tuple(base)[:2]
        kw = dict(base=base, aim=tuple(aim), energy=energy)
        if head_z: kw["head_z"] = head_z
        bpy.context.view_layer.update()
        if heads:
            hp, moved = B.place_work_lamp_safe(self.A, self.cam, [tuple(h) for h in heads], **kw)
        else:
            hp, moved = B.place_work_lamp(self.A, **kw), None
        self.lamp_info = dict(head=tuple(hp), moved=moved)

    def shadows(self, point, actors=None):
        """one cast shadow per actor from the strongest light at `point`."""
        bpy.context.view_layer.update()
        L = dominant_light(point)
        acts = [a.a for a in (actors or self.cast + self.extras) if a.posed]
        if L is not None and acts:
            try: S8.shadow_link(acts, L)
            except Exception as ex: print("shadow_link failed", ex)
        return L

    # ------------------------------------------------------------------------------------------------ camera
    def camera(self, loc, look, lens, roll=0.0, focus=None, k=7.0, kmax=22.0, clip=0.05, shake=None):
        """loc / look world points, lens mm (36 mm on the long side), roll degrees, focus point (default = look),
        k = blur at infinity in px at 1280, shake = (yaw, pitch, roll) degrees from common.shake()."""
        cam = self.cam
        loc = Vector(loc); look = Vector(look)
        q = (look - loc).to_track_quat("-Z", "Y")
        rl = roll + (shake[2] if shake else 0.0)
        q = q @ Quaternion((0, 0, 1), math.radians(rl))
        if shake:
            q = q @ Euler((math.radians(shake[1]), math.radians(shake[0]), 0), "XYZ").to_quaternion()
        cam.rotation_mode = "XYZ"
        cam.location = loc; cam.rotation_euler = q.to_euler()
        cam.data.lens = lens; cam.data.clip_start = clip
        cam["preset"] = "look"; cam["aspect"] = self.aspect
        cam["focus"] = tuple(focus if focus is not None else look); cam["coc_k"] = float(k); cam["coc_max"] = float(kmax); cam["dof_k"] = 1.0
        bpy.context.view_layer.update()
        return cam

    def screen(self, p):
        """world point -> (x, y) in frame fractions (y down), depth."""
        from bpy_extras.object_utils import world_to_camera_view as w2c
        v = w2c(self.sc, self.cam, Vector(p))
        return v.x, 1.0 - v.y, v.z

    # ------------------------------------------------------------------------------------------------ shot life cycle
    def begin(self, shot):
        """neutral stage, then the shot's own setup."""
        self.shot = shot
        for o in self._hid:
            try: o.hide_render = False
            except ReferenceError: pass
        self._hid = []
        for ob, m0 in self._moved:
            ob.matrix_world = m0
        self._moved = []
        bpy.context.view_layer.update()                    # ray casts in setup() must see the restored set
        presets.clear_foreground()
        self._props_hide()
        for nm in list(self._fills): self.fill(nm)
        for nm in ("sodium_2_1", "sodium_2_-1", "moon_key", "flood_key", "headlight_l2_b_-1", "headlight_l2_b_1"): B.practical(nm, 1.0)
        B.pov_windscreen(self.A, False)
        _door_glass(self, False); _windscreen_soft(False); crack_window(False)
        self.door(0.0)
        for a in self.cast:
            a.hide(); a.view = None; a.s = None; a.pidx = 2; a.breath = 0.0; a.a.walk_lock = None
            a.a.set_glow(None, None)
            ppd = getattr(shot, "PPD", {}).get(a.name, 240)   # close shots re-raster the puppet finer (PPD = {"kong": 480})
            if a.a.ppd != ppd: a.a.ppd = ppd; a.key = None
        self.drv.a.pitch_override = 0.0
        for e in self.extras:
            e.visible = True; e.loc = e.home
        self.post = {"exposure": 1.6}
        # v3 line quality: render scale per shot (PCT = {"final": 100} in the shot module; run.py --pct forces one for the run)
        pct = PCT_FORCE or getattr(shot, "PCT", {}).get(self.tier, self._pct0)
        B.X._STATE["pct"] = pct; self.sc.render.resolution_percentage = pct; self.pct = pct
        self._begin_n = getattr(self, '_begin_n', 0) + 1
        self.sc.cycles.samples = self.spp
        self.heads = []
        self._lamp_done = False
        S8.tune_flat(**dict(S8.FLAT_DEFAULT, EXPO=1.6))
        tune_skin()
        if hasattr(shot, "setup"):
            shot.setup(self)

    def frame(self, shot, g):
        """stage film frame g of the current shot; returns the post options for the set's post.
        The first call in a shot stages the shot's MIDDLE frame first: the one-time decisions (work-lamp slide,
        foreground props, shadow light) are taken there, so every worker and every resume takes the same ones."""
        if not self._lamp_done:
            a, b = C.shot_range(shot.ID)
            self._stage(shot, (a + b) // 2, log=False)
            self._lamp_done = True
            self._auto_ppd(shot)
        return self._stage(shot, g)

    def _auto_ppd(self, shot):
        """v3 line quality: every puppet is rastered at no less than 1.25 x the pixels its head takes on screen at the
        shot's middle frame (so the drawing is never magnified), in steps of 60, 240..780; a shot's PPD dict is a floor."""
        long_px = max(self.W, self.H)
        for a_ in self.cast:
            if not (a_.visible and a_.posed): continue
            z = self.screen(a_.head())[2]
            if z <= 0.05: continue
            d_px = a_.a.sc * self.cam.data.lens / 36.0 / z * long_px
            want = int(min(780, max(240, math.ceil(d_px * 1.25 / 60.0) * 60)))
            want = max(want, getattr(shot, "PPD", {}).get(a_.name, 240))
            if want > a_.a.ppd:
                print("ppd %s %s: %d -> %d (head %.0f px)" % (shot.ID, a_.name, a_.a.ppd, want, d_px), flush=True)
                a_.a.ppd = want; a_.key = None

    def _stage(self, shot, g, log=True):
        a, b = C.shot_range(shot.ID)
        t = g / float(FPS)
        u = (g - a) / float(max(b - a - 1, 1))
        self.g = g
        self.sc.frame_set(g + 1)
        self.heads = []
        post = dict(self.post)
        r = shot.frame(self, g, t, u)
        if r: post.update(r)
        post["sharp_idx"] = sorted(set(list(post.get("sharp_idx", ())) + [2]))     # v3: the cast (index 2) never gets lens blur
        S8.tune_flat(**dict(S8.FLAT_DEFAULT, EXPO=post["exposure"], **post.pop("flat", {})))
        tune_skin()
        self.extras_frame(t)
        cam = self.cam
        for a_ in self.cast + self.extras:
            a_.apply(cam)
        bpy.context.view_layer.update()
        if hasattr(shot, "late"):                          # things that need posed actors (lamp, shadows, glow)
            r2 = shot.late(self, g, t, u)
            if r2: post.update(r2)
        heads = [tuple(h.head()) for h in self.cast if h.visible and h.posed and h.pidx == 2]
        gl = B.glare_check(cam, heads) if heads else []
        if gl and log: self.glare_log.append((g, [(n, i, d) for n, i, d in gl]))
        post["_glare"] = gl
        return post

    def render(self, out_noext, g, post):
        post = {k: v for k, v in post.items() if not k.startswith("_")}
        return B.render6.render(out_noext, frame=g + 1, post_opts=post)


# ------------------------------------------------------------------------------------ copies of look11's small helpers
def dominant_light(point, exclude=()):
    best, bv = None, 0.0
    for ob in bpy.data.objects:
        if ob.type != "LIGHT" or ob.hide_render or ob.name in exclude or ob.name.startswith(("look_fill", "fill_", "pov_", "spark", "radio", "beacon")): continue
        d = ob.data
        if d.type == "SUN": e = d.energy * 1.0
        else:
            v = Vector(point) - ob.matrix_world.translation
            e = d.energy / (4 * math.pi * max(v.length_squared, 0.25)) * 0.05
            if d.type == "SPOT":
                ax = ob.matrix_world.to_3x3() @ Vector((0, 0, -1))
                if v.normalized().dot(ax) < math.cos(d.spot_size / 2): continue
        if e > bv: best, bv = ob, e
    return best


_GL = {}


def _door_glass(F, clear, only_door=False):
    if not only_door: _GL['all_clear'] = clear
    obs = [bpy.data.objects.get(F.A["hero_car"] + n) for n in ("_door_fr", "_body")]
    obs = [o for o in obs if o]
    if "orig" not in _GL:
        _GL["orig"] = {o.name: [m.name for m in o.data.materials] for o in obs}
        m = bpy.data.materials.new("film_no_glass"); m.use_nodes = True
        nt = m.node_tree; nt.nodes.clear()
        o = nt.nodes.new("ShaderNodeOutputMaterial"); t = nt.nodes.new("ShaderNodeBsdfTransparent")
        nt.links.new(t.outputs[0], o.inputs[0])
        _GL["none"] = m
    for door in (obs[:1] if only_door else obs):
        for i, nm in enumerate(_GL["orig"][door.name]):
            if nm.startswith("glass"):
                door.data.materials[i] = _GL["none"] if clear else bpy.data.materials[nm]


def _windscreen_soft(on):
    m = bpy.data.materials.get("glass_hero")
    if m is None: return
    for n in m.node_tree.nodes:
        if n.type == "BSDF_PRINCIPLED":
            if "s0" not in n: n["s0"] = n.inputs["Specular IOR Level"].default_value
            n.inputs["Specular IOR Level"].default_value = 0.05 if on else n["s0"]
        if n.type == "BSDF_GLOSSY":
            if "r0" not in n: n["r0"] = n.inputs["Roughness"].default_value
            n.inputs["Roughness"].default_value = 0.12 if on else n["r0"]
            if "c0" not in n: n["c0"] = list(n.inputs["Color"].default_value)
            n.inputs["Color"].default_value = [c * (0.22 if on else 1.0) for c in n["c0"][:3]] + [1.0]


def crack_window(on, center=(0.5, 0.5), r0=0.14, r1=0.30, floor=0.0, ky=1.0):
    """thin the hero windscreen's crack overlay inside a soft window of the FRAME (window coordinates, 0..1, y up):
    cracks keep `floor` of their opacity within r0 of `center` and all of it beyond r1 (ky scales the vertical
    distance).  Used by S18 so the web does not run across the driver's face.  on=False restores the full web."""
    m = bpy.data.materials.get("glass_hero")
    if m is None: return
    nt = m.node_tree
    mr = nt.nodes.get("film_crack_mask")
    if mr is None:
        mix = next((n for n in nt.nodes if n.type == "MIX_SHADER" and n.inputs[0].is_linked and n.inputs[0].links[0].from_node.type == "TEX_IMAGE"), None)
        if mix is None: return
        alpha = mix.inputs[0].links[0].from_socket
        tc = nt.nodes.new("ShaderNodeTexCoord")
        mp = nt.nodes.new("ShaderNodeMapping"); mp.name = "film_crack_map"
        nt.links.new(tc.outputs["Window"], mp.inputs["Vector"])
        ln = nt.nodes.new("ShaderNodeVectorMath"); ln.operation = "LENGTH"; nt.links.new(mp.outputs[0], ln.inputs[0])
        mr = nt.nodes.new("ShaderNodeMapRange"); mr.name = "film_crack_mask"; mr.interpolation_type = "SMOOTHSTEP"
        nt.links.new(ln.outputs["Value"], mr.inputs["Value"])
        mul = nt.nodes.new("ShaderNodeMath"); mul.operation = "MULTIPLY"
        nt.links.new(alpha, mul.inputs[0]); nt.links.new(mr.outputs["Result"], mul.inputs[1])
        nt.links.new(mul.outputs[0], mix.inputs[0])
    mp = nt.nodes["film_crack_map"]
    mp.inputs["Location"].default_value = (-center[0], -center[1] * ky, 0.0); mp.inputs["Scale"].default_value = (1.0, ky, 0.0)
    mr.inputs["From Min"].default_value = r0; mr.inputs["From Max"].default_value = r1
    mr.inputs["To Min"].default_value = floor if on else 1.0; mr.inputs["To Max"].default_value = 1.0


# ---------------------------------------------------------------------------------------------- phone screens (Thai)
CALLER = "น้ำเหนือ"
TXT = dict(missed="4 สายที่ไม่ได้รับ", sub="ลูกสาว", ended="วางสายแล้ว", incoming="สายเรียกเข้า", again="โทรกลับ")


def radio_card_png(ppd=900):
    """S01: the rescue handset in a gloved hand with an orange long sleeve, drawn like the cast (flat colours, ink
    outline).  Units = the radio root's (body 0.34 x 0.72, base at the origin), x right, y down.
    -> colour PNG, flat normal PNG, canvas (x0, y0, x1, y1)."""
    import raster8
    from PIL import Image
    D = draw8; f = D.f; INK = D.INK
    GL, GLD, BODY, BODY_HI, ORG, SLV = "#34343a", "#26262b", "#454853", "#666b7a", "#ee7a1f", "#e8731f"
    canvas = (-0.60, -1.45, 1.60, 2.45)
    o = ""
    w0, w1 = (0.10, 0.20), (1.30, 2.40)                       # forearm: wrist under the handset -> down right, out of frame
    o += D.poly_stroke([w0, w1], INK, 0.40, cap="butt") + D.poly_stroke([w0, w1], SLV, 0.355, cap="butt")
    dx, dy = D.nrm(D.sub(w1, w0))
    for k in (0.55, 1.15):                                    # two soft cloth folds
        c = D.add(w0, (dx, dy), k)
        o += D.line(D.add(c, (-dy, dx), 0.16), D.add(c, (-dy, dx), 0.03), D.shade(SLV, 0.72), 0.018)
    c0, c1 = D.add(w0, (dx, dy), -0.06), D.add(w0, (dx, dy), 0.16)   # glove cuff
    o += D.poly_stroke([c0, c1], INK, 0.44, cap="butt") + D.poly_stroke([D.add(c0, (dx, dy), 0.018), D.add(c1, (dx, dy), -0.018)], GLD, 0.40, cap="butt")
    o += D.ell(0.02, -0.17, 0.27, 0.29, GL, INK, 0.022)       # palm, behind the handset
    o += D.poly_stroke([(-0.10, -0.70), (-0.10, -1.32)], INK, 0.062) + D.poly_stroke([(-0.10, -0.70), (-0.10, -1.32)], BODY_HI, 0.026)   # antenna
    o += '<rect x="0.05" y="-0.79" width="0.085" height="0.09" rx="0.015" fill="%s" stroke="%s" stroke-width="0.016"/>' % (BODY_HI, INK)   # knob
    o += '<rect x="-0.17" y="-0.72" width="0.34" height="0.72" rx="0.045" fill="%s" stroke="%s" stroke-width="0.022"/>' % (BODY, INK)
    o += '<rect x="-0.145" y="-0.69" width="0.035" height="0.66" rx="0.017" fill="%s"/>' % BODY_HI
    o += '<rect x="-0.17" y="-0.645" width="0.34" height="0.075" fill="%s" stroke="%s" stroke-width="0.014"/>' % (ORG, INK)
    o += '<rect x="-0.105" y="-0.56" width="0.21" height="0.12" rx="0.012" fill="#0a1626" stroke="%s" stroke-width="0.012"/>' % INK
    o += D.ell(0.10, -0.655, 0.034, 0.028, "#2a0d0a", INK, 0.010)
    for i in range(3):
        y = -0.40 + i * 0.034
        o += D.line((-0.02, y), (0.12, y), "#08080a", 0.014)
    for i in range(4):                                        # four fingers round the left side, onto the front
        y = -0.335 + i * 0.086; x1 = (-0.015, 0.005, -0.005, -0.04)[i]
        o += '<rect x="-0.255" y="%s" width="%s" height="0.078" rx="0.039" fill="%s" stroke="%s" stroke-width="0.016"/>' % (f(y), f(x1 + 0.255), GL, INK)
        o += D.line((x1 - 0.075, y + 0.016), (x1 - 0.075, y + 0.062), D.shade(GL, 0.6), 0.012)
    o += D.ell(0.185, -0.30, 0.052, 0.115, GL, INK, 0.016, rot=-16)      # thumb up the right edge
    svg, W, H = D.doc(o, canvas, ppd)
    out = os.path.join(TEX, "radio_card.png")
    raster8.png(svg, W, H, out)
    npath = os.path.join(TEX, "radio_card_n.png")
    if not os.path.exists(npath): Image.new("RGB", (8, 8), (128, 128, 255)).save(npath)
    return out, npath, canvas


def screen_png(state):
    """phone screens drawn with PIL + raqm in Kanit Black: 'missed' (4 missed calls from Namnuea), 'incoming',
    'ended' (call ended), 'off'.  Every Thai string is checked glyph by glyph (phone8.verify_thai)."""
    from PIL import Image, ImageDraw, ImageFont
    out = os.path.join(TEX, "screen_%s.png" % state)
    if os.path.exists(out):
        return out
    w, h = 540, 1030
    F = lambda sz: ImageFont.truetype(C.KANIT, int(sz), layout_engine=ImageFont.Layout.RAQM)
    im = Image.new("RGB", (w, h), (6, 7, 12)); dr = ImageDraw.Draw(im)
    if state == "off":
        im.save(out); return out
    for y in range(h):
        k = y / float(h)
        dr.line([(0, y), (w, y)], fill=(int(16 + 26 * k), int(22 + 12 * k), int(50 - 8 * k)))
    dr.text((w // 2, 40), "22:47", font=F(64), fill=(235, 238, 245), anchor="mt")
    a = 230
    av = phone8._avatar(a)
    mask = Image.new("L", (a, a), 0); ImageDraw.Draw(mask).ellipse((0, 0, a - 1, a - 1), fill=255)
    ax, ay = (w - a) // 2, 170
    im.paste(av, (ax, ay), mask)
    dr.ellipse((ax - 5, ay - 5, ax + a + 5, ay + a + 5), outline=(240, 240, 245), width=6)
    dr.text((w // 2, ay + a + 22), CALLER, font=F(84), fill=(250, 250, 252), anchor="mt")
    dr.text((w // 2, ay + a + 128), TXT["sub"], font=F(40), fill=(170, 182, 214), anchor="mt")
    if state == "missed":
        cy = 640
        dr.rounded_rectangle((28, cy, w - 28, cy + 150), radius=30, fill=(226, 69, 59))
        dr.text((w // 2, cy + 75), TXT["missed"], font=F(62), fill=(255, 255, 255), anchor="mm")
        r = 44; bx, by = ax + a - 14, ay + 24
        dr.ellipse((bx - r, by - r, bx + r, by + r), fill=(226, 69, 59), outline=(255, 255, 255), width=5)
        dr.text((bx, by - 2), "4", font=F(60), fill=(255, 255, 255), anchor="mm")
        dr.rounded_rectangle((120, 840, w - 120, 930), radius=45, fill=(57, 196, 90))
        dr.text((w // 2, 885), TXT["again"], font=F(46), fill=(255, 255, 255), anchor="mm")
    elif state == "ended":
        dr.text((w // 2, 660), TXT["ended"], font=F(70), fill=(236, 92, 82), anchor="mt")
        dr.text((w // 2, 770), "00:41", font=F(54), fill=(200, 206, 224), anchor="mt")
        dr.ellipse((w // 2 - 60, 870, w // 2 + 60, 990), fill=(70, 74, 92))
        dr.line((w // 2 - 26, 930, w // 2 + 26, 930), fill=(236, 92, 82), width=14)
    else:
        dr.text((w // 2, 650), TXT["incoming"], font=F(54), fill=(200, 206, 224), anchor="mt")
        for x, col in ((0.25, (226, 69, 59)), (0.75, (57, 196, 90))):
            dr.ellipse((int(w * x) - 62, 850 - 62, int(w * x) + 62, 850 + 62), fill=col)
    im.save(out)
    rep = {k: phone8.verify_thai(v, C.KANIT) for k, v in dict(TXT, caller=CALLER).items()}
    json.dump(rep, open(os.path.join(TEX, "thai_glyph_check.json"), "w"), ensure_ascii=False, indent=1, default=str)
    bad = [k for k, v in rep.items() if not v.get("ok")]
    if bad:
        raise RuntimeError("Thai glyph check failed: %s" % bad)
    return out
