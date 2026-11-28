"""blockcast.py -- DEAD ZONE 09 blocky toy-figure cast (sheets_v3), modelled, textured and rigged by code (bpy, Cycles).

    import blockcast as BC
    k = BC.Figure("kong", "kong", height=None, wet=False)      # height None = true metres (Kong 1.80 m); else stage units
    k.place((x, y, z), facing_deg)                              # soles point, facing 0 = toward -Y (+90 = toward +X)
    k.pose(dict(expr="determined", arm_r="down", legs="stand", mouth=0.5), camera=cam)
    k.head_world(); k.sole_world("L"); k.objects; k.hide(True)
    BC.BlockAct(F, name, kind, height_bu, seated=False)        # drop-in for stage.Act (see API.md)

Kinds: "kong" (rescue worker, sheet kong.png), "z_office" (office-worker zombie = the hook's driver, sheet z_office.png),
"crew" (the junior rescue crew member: Kong's uniform, crew face, helmet; z_rescue.png before he turns).
Proportions: proportions.md (measured on the sheet turnarounds by measure_sheets.py).  Units: model metres; the root
carries the stage scale.  Rest frame: soles at z = 0, facing -Y, the character's LEFT = +X.
"""
import os, sys, math, json
import numpy as np
import bpy
from mathutils import Vector, Matrix, Quaternion, Euler

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path: sys.path.insert(0, HERE)
import bc_geom as G
import bc_mat as M
import bc_face as FACE

BU_M = 0.6                        # the set: 1 stage unit = 0.6 m
PUPPET_D_PER_H = 1.0 / 4.31       # the puppets' drawing unit D as a fraction of figure height (pose offsets are in D)

# ======================================================================================================= specs
# fractions of H unless noted (see proportions.md).  z = height above the soles.
BASE = dict(
    H=1.80, head=dict(w=0.205, d=0.205, h=0.190, r=0.036), chin=0.739, neck_z=0.700,
    torso=dict(w=0.370, w_top=0.372, d=0.205, z0=0.400, z1=0.694, r=0.045), waist_z=0.452,
    pelvis=dict(w=0.352, d=0.198, z0=0.258, z1=0.470, r=0.040),
    belt=dict(z=0.454, h=0.036),
    sh=dict(x=0.238, z=0.650), upper=dict(w=0.132, d=0.150, top=0.706), el_z=0.545,
    fore=dict(w=0.124, d=0.142, cuff=0.470), wr_z=0.462,
    fist=dict(w=0.118, d=0.160, h=0.147, dz=-0.074),
    hip=dict(x=0.104, z=0.300), uleg=dict(w=0.176, d=0.190, top=0.322), knee_z=0.200,
    lleg=dict(w=0.172, d=0.186, bot=0.136, flare=1.05), ankle_z=0.075,
    boot=dict(w=0.205, heel=0.115, toe=0.190, h=0.143, sole=0.030, kind="boot"),
)


def _spec(**over):
    s = json.loads(json.dumps(BASE))
    for k, v in over.items():
        if isinstance(v, dict) and k in s and isinstance(s[k], dict): s[k].update(v)
        else: s[k] = v
    return s


SPECS = {
    "kong": _spec(face="kong", hair="spiky", kit="rescue", skin=(0.80, 0.37, 0.15), gloves=True, star=True, stubble=True),
    "crew": _spec(H=1.78, head=dict(w=0.198, d=0.200, h=0.186), face="crew", hair="crest", kit="rescue", helmet=True, skin=(0.82, 0.42, 0.18),
                  gloves=True, star=True, chin=0.741),
    "z_office": _spec(H=1.75, head=dict(w=0.240, d=0.235, h=0.220, r=0.042), chin=0.722, neck_z=0.698, face="z_office", hair="wet", kit="office",
                      skin=(0.27, 0.265, 0.215), torso=dict(w=0.380, w_top=0.384, d=0.190, z0=0.400), waist_z=0.440,
                      pelvis=dict(w=0.360, d=0.186, z0=0.300, z1=0.450), belt=dict(z=0.418, h=0.026),
                      sh=dict(x=0.248), upper=dict(w=0.140, d=0.150), fore=dict(w=0.134, d=0.146, cuff=0.475), wr_z=0.456,
                      fist=dict(w=0.130, d=0.158, h=0.149, dz=-0.076),
                      hip=dict(x=0.100, z=0.340), uleg=dict(w=0.200, d=0.190, top=0.362), knee_z=0.225,
                      lleg=dict(w=0.200, d=0.188, bot=0.072, flare=1.07), ankle_z=0.050,
                      boot=dict(w=0.186, heel=0.100, toe=0.170, h=0.080, sole=0.022, kind="shoe"), zombie=True, gloves=False),
}
SPECS["z_rescue"] = SPECS["crew"]


# ======================================================================================================= helpers
def _q_axis(axis, ang):
    return Quaternion(Vector(axis).normalized(), ang)


def _frame_quat(u1, k, hinge_sign):
    """rotation whose local -Z is u1 and local X is hinge_sign * k (k = bend axis)."""
    X = Vector(k) * hinge_sign; Z = -Vector(u1); Y = Z.cross(X)
    X = Y.cross(Z)
    Mx = Matrix((X.normalized(), Y.normalized(), Z.normalized())).transposed()
    return Mx.to_quaternion()


def ik2(S, T, a, b, pole):
    S, T, pole = Vector(S), Vector(T), Vector(pole)
    d = T - S; L = d.length
    dn = d.normalized() if L > 1e-9 else Vector((0, 0, -1))
    L = max(abs(a - b) + 1e-4, min(L, (a + b) * 0.9995))
    T2 = S + dn * L
    cA = max(-1.0, min(1.0, (a * a + L * L - b * b) / (2 * a * L)))
    A = math.acos(cA)
    p = pole - dn * pole.dot(dn)
    if p.length < 1e-6:
        p = Vector((0, 1, 0)) - dn * dn.y
        if p.length < 1e-6: p = Vector((1, 0, 0))
    p.normalize()
    E = S + dn * a * cA + p * a * math.sin(A)
    return E, T2, p


def limb_quats(S, T, a, b, pole, hinge_sign):
    """2-bone chain from S toward T, elbow / knee toward the pole -> (upper quat, lower quat about the hinge, E)."""
    E, T2, p = ik2(S, T, a, b, pole)
    u1 = (E - S).normalized(); u2 = (T2 - E).normalized()
    k = u1.cross(u2)
    if k.length < 1e-5:
        k = u1.cross(-p)
    k.normalize()
    q1 = _frame_quat(u1, k, hinge_sign)
    th = math.acos(max(-1.0, min(1.0, u1.dot(u2))))
    q2 = Quaternion(Vector((hinge_sign, 0, 0)), th)
    return q1, q2, E


# ======================================================================================================= figure
class Figure:
    def __init__(self, name, kind="kong", height=None, wet=False, gloves=None, collection=None, pidx=2, lod=1.0):
        self.name = name; self.kind = kind
        self.S = S = SPECS[kind]
        self.H = H = S["H"]
        self.wet = 1.0 if wet is True else float(wet or 0.0)
        self.gloves = S.get("gloves", False) if gloves is None else gloves
        self.coll = collection or G.coll("BLOCKCAST")
        self.pidx = pidx
        self.lod = lod
        self.scale = (height / H) if height else 1.0       # stage units per model metre
        self.D = PUPPET_D_PER_H * H                        # pose offsets come in the puppets' D: same fraction of the height
        self.objs = []
        self.hands = {"L": {}, "R": {}}
        self.props = {}
        self._face_state = None
        self.mats = {}
        self._build_rig()
        self._build_materials()
        self._build_body()
        self._build_head()
        self._build_kit()
        self.rest_pose()

    # ------------------------------------------------------------------------------------------------ rig
    def _build_rig(self):
        S, H = self.S, self.H
        n = self.name
        self.root = G.empty(n + "_root", collection=self.coll)
        self.root.rotation_mode = "XYZ"
        self.root.scale = (self.scale,) * 3
        self.rest = {}
        def J(name, parent, pos):
            par = self.J[parent] if parent else self.root
            ppos = self.rest[parent] if parent else Vector((0, 0, 0))
            ob = G.empty(n + "_" + name, par, tuple(Vector(pos) - ppos), self.coll)
            self.J[name] = ob; self.rest[name] = Vector(pos)
            return ob
        self.J = {}
        hz = S["hip"]["z"] * H
        J("pelvis", None, (0, 0, hz))
        J("waist", "pelvis", (0, 0, S["waist_z"] * H))
        J("neck", "waist", (0, 0, S["neck_z"] * H))
        for side, sx in (("L", 1), ("R", -1)):
            J("sh_" + side, "waist", (sx * S["sh"]["x"] * H, 0, S["sh"]["z"] * H))
            J("el_" + side, "sh_" + side, (sx * S["sh"]["x"] * H, 0, S["el_z"] * H))
            J("wr_" + side, "el_" + side, (sx * S["sh"]["x"] * H, 0, S["wr_z"] * H))
            J("hip_" + side, "pelvis", (sx * S["hip"]["x"] * H, 0, hz))
            J("kn_" + side, "hip_" + side, (sx * S["hip"]["x"] * H, 0, S["knee_z"] * H))
            J("an_" + side, "kn_" + side, (sx * S["hip"]["x"] * H, 0, S["ankle_z"] * H))
        self.len = dict(upper=(S["sh"]["z"] - S["el_z"]) * H, fore=(S["el_z"] - S["wr_z"]) * H, hand=-S["fist"]["dz"] * H,
                        thigh=(hz - S["knee_z"] * H), shin=(S["knee_z"] - S["ankle_z"]) * H)
        self.head_c = Vector((0, 0, (S["chin"] + S["head"]["h"] / 2) * H))

    def part(self, name, joint, vf, mat, smooth=True, mat_idx=None, uv=None, hidden=False):
        """geometry given in REST space (model metres) -> an object on `joint` (vertices made joint-local)."""
        v, f = vf
        o = self.rest[joint]
        ob = G.obj(self.name + "_" + name, np.asarray(v, float) - np.asarray(o), f, mat, self.J[joint], tuple(o), smooth, mat_idx, uv,
                   self.coll, self.pidx)
        ob.hide_render = hidden
        self.objs.append(ob)
        return ob

    # ------------------------------------------------------------------------------------------------ materials
    def _build_materials(self):
        S, H, w, n = self.S, self.H, self.wet, self.name
        Mt = self.mats
        z = S.get("zombie", False)
        bl = self._blood_spots() if z else {}
        Mt["skin"] = M.skin(n + "_skin", tuple(S["skin"]), H, wet=w, grime=0.8 if z else 0.0,
                            blood=dict(spots=bl.get("skin", []), specks=0.6) if z else None)
        Mt["black"] = M.solid(n + "_black", (0.016, 0.016, 0.018), 0.55, wet=w, H=H, noise_bump=0.25)
        Mt["webbing"] = M.cloth(n + "_web", (0.020, 0.020, 0.022), 0.6, H, weave=0.0022, weave_k=0.5, sheen=0.04, wet=w)
        Mt["metal"] = M.solid(n + "_metal", (0.55, 0.56, 0.58), 0.28, metal=1.0, wet=w, H=H)
        hair_col = (0.010, 0.009, 0.009) if not z else (0.014, 0.010, 0.008)
        Mt["hair"] = M.solid(n + "_hair", hair_col, 0.42 if not (z or w) else 0.22, coat=0.25 if not (z or w) else 0.7, coat_rough=0.12,
                             wet=max(w, 0.9 if z else 0.0), H=H, noise_bump=0.4, drops=260.0)
        if S["kit"] == "rescue":
            org = (0.56, 0.088, 0.011)
            Mt["jacket"] = M.cloth(n + "_jacket", org, 0.66, H, dirt=dict(low=0.22, knee=None, amount=1.0, mottle=0.85, mottle_scale=13.0),
                                   wet=w, tee=dict(z_top=S["torso"]["z1"] * H, half=0.055 * H, depth=0.10 * H, y_front=0.07 * H, col=(0.016, 0.016, 0.018)),
                                   panel_v=dict(y_front=0.08 * H, z_top=(S["torso"]["z1"] - 0.10) * H, x=-0.012 * H))
            Mt["trousers"] = M.cloth(n + "_trousers", org, 0.68, H, dirt=dict(low=0.28, knee=S["knee_z"], amount=1.0, mottle=0.85, mottle_scale=13.0), wet=w)
            Mt["tee"] = M.cloth(n + "_tee", (0.016, 0.016, 0.018), 0.7, H, sheen=0.04, wet=w)
            Mt["tape"] = M.tape(n + "_tape", wet=w)
            Mt["cuff"] = M.cloth(n + "_cuff", (0.025, 0.022, 0.022), 0.6, H, sheen=0.04, wet=w)
            Mt["boot"] = M.solid(n + "_boot", (0.022, 0.017, 0.013), 0.5, wet=w, H=H, dirt=dict(low=0.06, amount=1.0, mottle=0.40, mottle_scale=16.0),
                                 dirt_col=(0.10, 0.060, 0.030), noise_bump=0.6)
            Mt["sole"] = M.solid(n + "_sole", (0.018, 0.016, 0.015), 0.7, wet=w, H=H, dirt=dict(low=0.03, amount=0.8), dirt_col=(0.12, 0.07, 0.035))
            Mt["glove"] = M.solid(n + "_glove", (0.020, 0.020, 0.022), 0.48, wet=w, H=H, noise_bump=0.5)
            Mt["patch"] = M.image_mat(n + "_patch", star_png(), 0.45, wet=w)
            Mt["radio"] = M.solid(n + "_radio", (0.025, 0.027, 0.03), 0.35, wet=w, H=H)
            Mt["led"] = M.emit(n + "_led", (0.3, 1.0, 0.35), 6.0)
            Mt["badge"] = M.cloth(n + "_badge", (0.78, 0.55, 0.05), 0.6, H, wet=w)
            Mt["helmet"] = M.solid(n + "_helmet", (0.62, 0.61, 0.58), 0.3, coat=0.5, coat_rough=0.08, wet=w, H=H,
                                   dirt=dict(low=0.0, amount=0.0, mottle=0.35, mottle_scale=18.0), dirt_col=(0.18, 0.15, 0.12))
            Mt["red"] = M.solid(n + "_red", (0.45, 0.02, 0.02), 0.4, wet=w, H=H)
            Mt["lamp"] = M.emit(n + "_lamp", (1.0, 0.88, 0.62), 18.0)
        else:
            Mt["shirt"] = M.cloth(n + "_shirt", (0.42, 0.40, 0.36), 0.62, H, dirt=dict(low=0.45, amount=0.9, mottle=0.60, mottle_scale=7.0),
                                  dirt_col=(0.17, 0.13, 0.08), blood=dict(spots=bl["shirt"], specks=1.0), wet=max(w, 0.8), tears=bl["shirt_tears"],
                                  tear_skin=tuple(S["skin"]), panel_v=dict(y_front=0.07 * H, x=0.0, z_top=(S["torso"]["z1"] - 0.08) * H, col=(0.32, 0.30, 0.27)))
            Mt["slacks"] = M.cloth(n + "_slacks", (0.020, 0.020, 0.022), 0.6, H, sheen=0.04, dirt=dict(low=0.20, knee=S["knee_z"], amount=1.0, mottle=0.35),
                                   dirt_col=(0.065, 0.05, 0.035), blood=dict(spots=bl["slacks"], specks=0.4), wet=max(w, 0.8), tears=bl["slack_tears"],
                                   tear_skin=tuple(S["skin"]))
            Mt["tie"] = M.cloth(n + "_tie", (0.12, 0.012, 0.016), 0.42, H, weave=0.003, sheen=0.3, blood=dict(spots=bl["tie"], specks=0.3), wet=max(w, 0.8))
            Mt["shoe"] = M.solid(n + "_shoe", (0.018, 0.015, 0.013), 0.28, coat=0.5, coat_rough=0.12, wet=max(w, 0.8), H=H,
                                 dirt=dict(low=0.05, amount=0.6, mottle=0.3), dirt_col=(0.09, 0.07, 0.05))
            Mt["belt"] = M.solid(n + "_belt", (0.02, 0.016, 0.014), 0.35, wet=max(w, 0.6), H=H)
            Mt["card"] = M.image_mat(n + "_card", card_png(), 0.25, wet=max(w, 0.6))
            Mt["lanyard"] = M.cloth(n + "_lanyard", (0.02, 0.02, 0.03), 0.5, H, sheen=0.04, wet=max(w, 0.6))

    def _blood_spots(self):
        """zombie blood / tears placed by code in rest space (metres): (centre, radius, drip)."""
        H = self.H; S = self.S
        tf = -S["torso"]["d"] / 2 * H          # torso front y
        tb = S["torso"]["d"] / 2 * H
        sx = S["sh"]["x"] * H
        sh = [((0.02 * H, tf, 0.66 * H), 0.035 * H, 0.10 * H), ((-0.10 * H, tf, 0.60 * H), 0.05 * H, 0.08 * H),
              ((0.12 * H, tf, 0.52 * H), 0.04 * H, 0.06 * H), ((-0.06 * H, tf, 0.45 * H), 0.035 * H, 0.05 * H),
              ((0.15 * H, tb, 0.62 * H), 0.06 * H, 0.05 * H), ((-0.08 * H, tb, 0.50 * H), 0.05 * H, 0.07 * H),
              ((0.0, tb, 0.40 * H), 0.04 * H, 0.04 * H),
              ((sx, -0.05 * H, 0.60 * H), 0.04 * H, 0.04 * H), ((-sx, 0.0, 0.52 * H), 0.045 * H, 0.05 * H),
              ((-sx - 0.06 * H, 0.0, 0.62 * H), 0.03 * H, 0.03 * H), ((sx + 0.06 * H, 0.02 * H, 0.50 * H), 0.035 * H, 0.04 * H),
              ((-0.03 * H, tf, 0.68 * H), 0.04 * H, 0.12 * H), ((0.07 * H, tf, 0.64 * H), 0.03 * H, 0.10 * H), ((-0.15 * H, tf, 0.52 * H), 0.04 * H, 0.05 * H),
              ((0.16 * H, tf, 0.40 * H), 0.03 * H, 0.03 * H), ((-0.14 * H, tf, 0.38 * H), 0.035 * H, 0.03 * H), ((0.02 * H, tb, 0.66 * H), 0.05 * H, 0.08 * H),
              ((-0.16 * H, tb, 0.62 * H), 0.04 * H, 0.06 * H), ((0.16 * H, tb, 0.44 * H), 0.04 * H, 0.05 * H), ((sx, 0.05 * H, 0.66 * H), 0.035 * H, 0.04 * H),
              ((-sx, -0.06 * H, 0.66 * H), 0.035 * H, 0.04 * H), ((sx, 0.0, 0.47 * H), 0.03 * H, 0.03 * H), ((-sx, 0.05 * H, 0.47 * H), 0.03 * H, 0.03 * H)]
        tears = [((-0.12 * H, tf, 0.62 * H), 0.024 * H, 0), ((0.13 * H, tf, 0.44 * H), 0.020 * H, 0), ((0.10 * H, tb, 0.58 * H), 0.028 * H, 0),
                 ((-sx - 0.05 * H, -0.02 * H, 0.62 * H), 0.022 * H, 0), ((sx, -0.06 * H, 0.55 * H), 0.020 * H, 0), ((sx + 0.07 * H, 0.0, 0.62 * H), 0.02 * H, 0),
                 ((-0.05 * H, tb, 0.45 * H), 0.024 * H, 0), ((0.17 * H, tf, 0.58 * H), 0.016 * H, 0), ((-sx, 0.07 * H, 0.58 * H), 0.02 * H, 0)]
        lf = -S["uleg"]["d"] / 2 * H
        sl = [((0.10 * H, lf, 0.26 * H), 0.035 * H, 0.06 * H), ((-0.12 * H, lf, 0.30 * H), 0.03 * H, 0.04 * H),
              ((-0.10 * H, lf, 0.12 * H), 0.03 * H, 0.03 * H)]
        st = [((-0.11 * H, lf, 0.18 * H), 0.034 * H, 0), ((0.11 * H, lf - 0.0, 0.25 * H), 0.028 * H, 0), ((0.12 * H, 0.09 * H, 0.15 * H), 0.034 * H, 0),
              ((-0.13 * H, 0.09 * H, 0.24 * H), 0.03 * H, 0), ((0.08 * H, lf, 0.10 * H), 0.025 * H, 0), ((-0.19 * H, 0.0, 0.12 * H), 0.025 * H, 0)]
        skin = [((sx, -0.02 * H, 0.40 * H), 0.04 * H, 0.03 * H), ((-sx, -0.03 * H, 0.36 * H), 0.05 * H, 0.03 * H),
                ((0.0, -0.13 * H, 0.75 * H), 0.05 * H, 0.04 * H)]
        tie = [((0.0, tf, 0.58 * H), 0.04 * H, 0.06 * H)]
        return dict(shirt=sh, shirt_tears=tears, slacks=sl, slack_tears=st, skin=skin, tie=tie)

    # ------------------------------------------------------------------------------------------------ body
    def _box(self, cx, cy, cz, hx, hy, hz, r, n=(4, 4, 4), taper=None):
        v, f = G.rbox(hx, hy, hz, r, n)
        if taper is not None:                    # taper(zfrac 0 bottom .. 1 top) -> x scale
            t = (v[:, 2] + hz) / (2 * hz)
            v[:, 0] *= np.vectorize(taper)(t)
        return v + np.array([cx, cy, cz]), f

    def _build_body(self):
        S, H, Mt = self.S, self.H, self.mats
        office = S["kit"] == "office"
        T = S["torso"]
        cloth_t = Mt["shirt"] if office else Mt["jacket"]
        cloth_b = Mt["slacks"] if office else Mt["trousers"]
        # torso (the jacket / shirt is the torso block: toy figures wear their clothes as the body shell)
        hz = (T["z1"] - T["z0"]) / 2 * H
        wt, wb = T["w_top"] / T["w"], 1.0
        self.part("torso", "waist", self._box(0, 0, (T["z0"] + T["z1"]) / 2 * H, T["w"] / 2 * H, T["d"] / 2 * H, hz, T["r"] * H, (5, 4, 6),
                                              taper=lambda t: wb + (wt - wb) * t), cloth_t)
        P = S["pelvis"]
        self.part("pelvis", "pelvis", self._box(0, 0, (P["z0"] + P["z1"]) / 2 * H, P["w"] / 2 * H, P["d"] / 2 * H, (P["z1"] - P["z0"]) / 2 * H,
                                                P["r"] * H, (5, 4, 3)), cloth_b)
        # neck (mostly hidden by the collar)
        nk = G.sweep([(0, 0.004 * H, (T["z1"] - 0.02) * H), (0, 0.004 * H, (S["chin"] + 0.02) * H)], [0.055 * H, 0.055 * H], 12, cap0=False, tip=False)
        self.part("neck", "neck", nk, Mt["tee"] if "tee" in Mt else Mt["skin"])
        for side, sx in (("L", 1), ("R", -1)):
            x = sx * S["sh"]["x"] * H
            U, F_ = S["upper"], S["fore"]
            top = U["top"] * H; elz = S["el_z"] * H
            sleeve = Mt["shirt"] if office else Mt["jacket"]
            self.part("upper_" + side, "sh_" + side, self._box(x, 0, (top + elz - 0.025 * H) / 2, U["w"] / 2 * H, U["d"] / 2 * H, (top - elz + 0.025 * H) / 2,
                                                               0.052 * H, (3, 3, 4)), sleeve)
            cz = F_["cuff"] * H
            if office:
                # rolled sleeve: forearm sleeve to the roll, a thick rolled cuff, bare forearm below
                self.part("fore_" + side, "el_" + side, self._box(x, 0, (elz + 0.02 * H + cz) / 2, F_["w"] / 2 * H, F_["d"] / 2 * H,
                                                                   (elz + 0.02 * H - cz) / 2, 0.048 * H, (3, 3, 3)), sleeve)
                rv, rf = G.ring(F_["w"] / 2 * H, F_["d"] / 2 * H, 0.03 * H, cz - 0.034 * H, cz + 0.004 * H, off=0.004 * H, th=0.012 * H,
                                zfun=lambda xx, yy, z0: z0 - 0.004 * H * math.sin(7 * math.atan2(yy, xx)))
                rv[:, 0] += x
                self.part("roll_" + side, "el_" + side, (rv, rf), sleeve)
                fa = self._box(x, 0, (cz + S["wr_z"] * H) / 2 - 0.01 * H, 0.050 * H, 0.060 * H, (cz - S["wr_z"] * H) / 2 + 0.03 * H, 0.02 * H, (2, 2, 2))
                self.part("forearm_" + side, "el_" + side, fa, Mt["skin"])
            else:
                self.part("fore_" + side, "el_" + side, self._box(x, 0, (elz + 0.02 * H + cz) / 2, F_["w"] / 2 * H, F_["d"] / 2 * H,
                                                                   (elz + 0.02 * H - cz) / 2, 0.048 * H, (3, 3, 3)), sleeve)
                cv, cf = G.ring(F_["w"] / 2 * H, F_["d"] / 2 * H, 0.03 * H, cz, cz + 0.022 * H, off=0.002 * H, th=0.006 * H)
                cv[:, 0] += x
                self.part("cuff_" + side, "el_" + side, (cv, cf), Mt["cuff"])
            self._build_hand(side, x)
            # legs
            hx = sx * S["hip"]["x"] * H
            UL, LL = S["uleg"], S["lleg"]
            kz = S["knee_z"] * H
            self.part("uleg_" + side, "hip_" + side, self._box(hx, 0, (UL["top"] * H + kz - 0.02 * H) / 2, UL["w"] / 2 * H, UL["d"] / 2 * H,
                                                                (UL["top"] * H - kz + 0.02 * H) / 2, 0.035 * H, (3, 3, 4)), cloth_b)
            lo = LL["bot"] * H; topl = kz + 0.025 * H
            fl = LL["flare"]
            lv, lf = self._box(hx, 0, (topl + lo) / 2, LL["w"] / 2 * H, LL["d"] / 2 * H, (topl - lo) / 2, 0.035 * H, (3, 3, 4),
                               taper=lambda t: fl + (1.0 - fl) * t)
            if office:                                       # torn hem: jag the lowest ring of vertices
                low = lv[:, 2] < lo + 0.012 * H
                ang = np.arctan2(lv[:, 1], lv[:, 0] - hx)
                lv[low, 2] -= (0.022 * H * (np.abs(np.sin(9 * ang[low] + sx)) ** 2) + 0.010 * H * np.sin(23 * ang[low]))
            self.part("lleg_" + side, "kn_" + side, (lv, lf), cloth_b)
            self._build_foot(side, hx)

    def _build_hand(self, side, x):
        """C-shaped toy fist (a tunnel through the grip, front to back), an open hand, a claw and a pointing fist."""
        S, H, Mt = self.S, self.H, self.mats
        Fz = S["fist"]
        sx = 1 if side == "L" else -1
        fw, fd, fh = Fz["w"] * H, Fz["d"] * H, Fz["h"] * H
        cz = S["wr_z"] * H + Fz["dz"] * H
        mat = Mt["glove"] if (self.gloves and "glove" in Mt) else Mt["skin"]
        fist = self._box(x, 0, cz, fw / 2, fd / 2, fh / 2, 0.30 * min(fw, fh), (2, 2, 2))
        thumb = self._box(x - sx * fw * 0.26, -fd * 0.40, cz + fh * 0.24, fw * 0.28, fd * 0.16, fh * 0.17, 0.016 * H, (1, 1, 1))
        ob = self.part("fist_" + side, "wr_" + side, G.merge([fist]), mat)
        # the C: a tunnel along Y through the lower front of the fist
        tun = G.sweep([(x, -fd, cz - fh * 0.06), (x, fd, cz - fh * 0.06)], [fh * 0.16, fh * 0.16], 16, cap0=True, tip=False)
        try:
            G.boolean_diff(ob, (tun[0] - np.asarray(self.rest["wr_" + side]), tun[1]))
            self._set_rest(ob, self.rest["wr_" + side])
        except Exception as ex:
            print("fist boolean failed", ex)
        tb = self.part("thumb_" + side, "wr_" + side, thumb, mat)
        self.hands[side]["fist"] = [ob, tb]
        # open hand: flat slab + thumb, fingers together
        op = self._box(x, -fd * 0.05, cz - fh * 0.10, fw * 0.30, fd * 0.48, fh * 0.62, 0.02 * H, (1, 2, 2))
        opt = self._box(x - sx * fw * 0.18, -fd * 0.48, cz + fh * 0.05, fw * 0.18, fd * 0.14, fh * 0.26, 0.015 * H, (1, 1, 1))
        o = self.part("open_" + side, "wr_" + side, G.merge([op, opt]), mat, hidden=True)
        self.hands[side]["open"] = [o]
        # claw: open slab with three hooked finger blocks
        parts = [self._box(x, -fd * 0.05, cz + fh * 0.05, fw * 0.32, fd * 0.46, fh * 0.42, 0.02 * H, (1, 2, 2))]
        for k in range(3):
            yy = -fd * 0.32 + k * fd * 0.30
            parts.append(self._box(x, yy - fd * 0.06, cz - fh * 0.42, fw * 0.24, fd * 0.11, fh * 0.20, 0.012 * H, (1, 1, 1)))
        parts.append(self._box(x - sx * fw * 0.2, -fd * 0.50, cz + fh * 0.0, fw * 0.16, fd * 0.12, fh * 0.24, 0.012 * H, (1, 1, 1)))
        o = self.part("claw_" + side, "wr_" + side, G.merge(parts), mat, hidden=True)
        self.hands[side]["claw"] = [o]
        # point: the fist + an index finger forward
        pf = self._box(x, -fd * 0.85, cz + fh * 0.18, fw * 0.16, fd * 0.36, fh * 0.13, 0.014 * H, (1, 2, 1))
        o = self.part("point_" + side, "wr_" + side, G.merge([fist, thumb, pf]), mat, hidden=True)
        self.hands[side]["point"] = [o]

    def _set_rest(self, ob, origin):
        me = ob.data
        at = me.attributes.get("rest") or me.attributes.new("rest", "FLOAT_VECTOR", "POINT")
        co = np.zeros(len(me.vertices) * 3, np.float32); me.vertices.foreach_get("co", co)
        at.data.foreach_set("vector", (co.reshape(-1, 3) + np.asarray(origin, np.float32)).ravel())

    def _build_foot(self, side, hx):
        S, H, Mt = self.S, self.H, self.mats
        B = S["boot"]
        bw, h, so = B["w"] * H, B["h"] * H, B["sole"] * H
        y0, y1 = -B["toe"] * H, B["heel"] * H
        office = B["kind"] == "shoe"
        up_mat = Mt["shoe"] if office else Mt["boot"]
        sole_mat = Mt["shoe"] if office else Mt["sole"]
        cy = (y0 + y1) / 2
        # upper: a box whose front top is rounded down to the toe
        uv, uf = G.rbox(bw / 2 * 0.96, (y1 - y0) / 2 * 0.97, (h - so) / 2, min(0.030 * H, (h - so) / 2 * 0.95), (3, 5, 3))
        t = (uv[:, 1] - uv[:, 1].min()) / max(np.ptp(uv[:, 1]), 1e-6)       # 0 at the toe
        zr = (uv[:, 2] + (h - so) / 2) / (h - so)                             # 0 at the bottom
        if not office:
            drop = np.clip(0.42 - t, 0, 1) / 0.42                            # the toe box: lower and rounder in front
            uv[:, 2] -= drop ** 1.5 * zr * (h - so) * 0.42
        else:
            drop = np.clip(0.75 - t, 0, 1) / 0.75
            uv[:, 2] -= drop * zr * (h - so) * 0.40
        uv += np.array([hx, cy, so + (h - so) / 2])
        self.part("boot_" + side, "an_" + side, (uv, uf), up_mat)
        sv = self._box(hx, cy, so / 2, bw / 2 * 1.04, (y1 - y0) / 2 * 1.01, so / 2, min(so * 0.45, 0.012 * H), (3, 5, 1))
        self.part("sole_" + side, "an_" + side, sv, sole_mat)
        if not office:
            # boot collar and laces
            cv, cf = G.ring(bw / 2 * 0.90, (y1 - y0) / 2 * 0.30, 0.03 * H, h - 0.020 * H, h + 0.004 * H, off=0.0, th=0.010 * H)
            cv += np.array([hx, y1 - (y1 - y0) * 0.30, 0])
            self.part("bootcollar_" + side, "an_" + side, (cv, cf), Mt["sole"])
            laces = []
            for k in range(4):
                zz = h * (0.88 - k * 0.13); yy = y1 - (y1 - y0) * (0.62 + k * 0.06) + 0.004 * H
                laces.append(self._box(hx, yy - 0.012 * H, zz, bw * 0.22, 0.004 * H, 0.004 * H, 0.002 * H, (1, 1, 1)))
            self.part("laces_" + side, "an_" + side, G.merge(laces), Mt["black"])

    # ------------------------------------------------------------------------------------------------ head
    def _build_head(self):
        S, H, Mt = self.S, self.H, self.mats
        Hd = S["head"]
        w, d, h = Hd["w"] * H, Hd["d"] * H, Hd["h"] * H
        self.head_dims = (w, d, h)
        c = self.head_c
        v, f = G.rbox(w / 2, d / 2, h / 2, Hd["r"] * H, (6, 6, 6))
        pc, pe = FACE.face_png(S["face"], "determined" if not S.get("zombie") else "idle")
        self.mats["head"] = M.skin(self.name + "_head", tuple(S["skin"]), H, wet=self.wet, grime=0.8 if S.get("zombie") else 0.0,
                                   face=dict(w=w, h=h, img=pc, emit=pe), eyes_glow=7.0 if S.get("zombie") else 0.0)
        self.head = self.part("head", "neck", (v + np.array(c), f), self.mats["head"])
        # the head object's origin must be the head centre for the decal mapping: move it (verts stay put in rest)
        me = self.head.data
        co = np.zeros(len(me.vertices) * 3); me.vertices.foreach_get("co", co); co = co.reshape(-1, 3)
        off = np.asarray(c) - np.asarray(self.rest["neck"])
        me.vertices.foreach_set("co", (co - off).ravel()); self.head.location = tuple(off)
        self._build_hair()
        if S.get("helmet"): self._build_helmet()

    def _scalp_point(self, az, el, inflate):
        """point on the hair cap (the head box grown by the style's crown height) along direction (azimuth from the
        front -Y toward +X, elevation), pushed out by inflate."""
        w, d, h = self.head_dims
        H = self.H
        top = getattr(self, "_cap_top", 0.0)
        dv = np.array([math.sin(az) * math.cos(el), -math.cos(az) * math.cos(el), math.sin(el)])
        half = (w / 2 + 0.005 * H, d / 2 + 0.005 * H, h / 2 + top * 0.5)
        cz = top * 0.5
        p = dv * 2.0 * max(w, h) + np.array([0, 0, cz])
        q, n = G.onto_rbox(p, (0, 0, cz), half, self.S["head"]["r"] * H + 0.005 * H, inflate)
        return q, n

    HAIR = {
        # count, r (x w), L (x w), lift deg, droop, flat, fringe (count, r, L), side spikes (count, r, L, lift), hairline (front, side, back)
        "spiky": dict(n=200, r=(0.11, 0.16), L=(0.22, 0.34), lift=(18, 45), droop=0.10, flat=0.58, tip=0.86,
                      fringe=(10, (0.12, 0.15), (0.30, 0.40)), spikes=(30, (0.10, 0.13), (0.26, 0.36), (30, 55)),
                      hem=(34, (0.10, 0.13), (0.12, 0.18)), hl=(0.62, -0.10, -0.98), whorl=(0.0, 0.35), top=0.030, seed=3),
        "wet": dict(n=250, r=(0.075, 0.105), L=(0.30, 0.46), lift=(8, 22), droop=0.50, flat=0.45, tip=0.78,
                    fringe=(16, (0.07, 0.095), (0.20, 0.27)), spikes=(26, (0.06, 0.08), (0.34, 0.48), (12, 28)),
                    hem=(34, (0.07, 0.09), (0.22, 0.32)), hl=(0.80, -0.15, -0.90), whorl=(0.0, 0.25), top=0.022, seed=5),
        "crest": dict(n=90, r=(0.08, 0.11), L=(0.14, 0.22), lift=(10, 25), droop=0.15, flat=0.42, tip=0.85,
                      fringe=(7, (0.08, 0.10), (0.20, 0.28)), spikes=(10, (0.07, 0.09), (0.16, 0.22), (20, 35)),
                      hem=(16, (0.08, 0.10), (0.14, 0.20)), hl=(0.50, -0.05, -0.70), whorl=(0.0, 0.2), top=0.010, seed=7),
    }

    def _build_hair(self):
        """chunky clumped hair: leaf-shaped clumps lying on the scalp along a flow from the crown whorl (lifted at the
        tips), longer spikes on the silhouette ring, and a fringe over the forehead; a dark cap underneath."""
        S, H = self.S, self.H
        w, d, h = self.head_dims
        st = self.HAIR[S["hair"]]
        rng = np.random.RandomState(st["seed"])
        c = np.asarray(self.head_c)
        HL = st["hl"]
        def hairline(az):
            a = abs(((az + math.pi) % (2 * math.pi)) - math.pi)          # 0 front .. pi back
            if a < math.pi / 2:
                t = a / (math.pi / 2); return (HL[0] * (1 - t) + HL[1] * t) * h / 2
            t = (a - math.pi / 2) / (math.pi / 2); return (HL[1] * (1 - t) + HL[2] * t) * h / 2
        self._cap_top = st["top"] * H
        cv, cf = G.rbox(w / 2 + 0.005 * H, d / 2 + 0.005 * H, h / 2 + st["top"] * H * 0.5, S["head"]["r"] * H + 0.005 * H, (5, 5, 5))
        cv[:, 2] += st["top"] * H * 0.5
        az_ = np.arctan2(cv[:, 0], -cv[:, 1])
        zl = np.array([hairline(a) + 0.012 * H for a in az_])
        lowm = cv[:, 2] < zl
        cv[lowm, 2] = zl[lowm]
        self.part("haircap", "neck", (cv + c, cf), self.mats["hair"])
        whorl = np.array([0.0, st["whorl"][1] * d / 2, h / 2 + 0.02 * H])
        locks = []
        def clump(az, el, L, r0, lift, droop, flat, inflate=0.003 * H, flow=None):
            base, n = self._scalp_point(az, el, inflate)
            if base[2] < hairline(az) - 0.01 * H: return False
            if flow is None:
                flow = base - whorl
            t = np.asarray(flow, float) - n * np.dot(flow, n)
            if np.linalg.norm(t) < 1e-6: t = np.array([0, 1.0, 0]) - n * n[1]
            t /= np.linalg.norm(t)
            dv = t * math.cos(math.radians(lift)) + n * math.sin(math.radians(lift))
            p0 = base - n * 0.010 * H - t * 0.15 * L
            p1 = base + dv * L * 0.45
            p2 = base + dv * L + np.array([0, 0, -droop * L])
            k = 7
            pts = [(1 - s) ** 2 * p0 + 2 * (1 - s) * s * p1 + s * s * p2 for s in np.linspace(0, 1, k)]
            rad = [r0 * (1.0 - st["tip"] * s ** 1.25) * (0.75 + 0.25 * math.sin(math.pi * min(1, s * 1.6))) for s in np.linspace(0, 1, k)]
            v, f = G.sweep(pts, rad, 6, flat=flat, normals=[n] * k)
            locks.append((v + c, f))
            return True
        def rand_dir():
            zz = rng.uniform(-0.92, 1.0); a = rng.uniform(-math.pi, math.pi)
            return a, math.asin(zz)
        placed = 0; tries = 0
        while placed < st["n"] and tries < st["n"] * 8:
            tries += 1
            az, el = rand_dir()
            if clump(az, el, rng.uniform(*st["L"]) * w, rng.uniform(*st["r"]) * w, rng.uniform(*st["lift"]), st["droop"], st["flat"]):
                placed += 1
        # silhouette spikes: the ring around the crown and the temples / back, lifted out
        cnt, rr, Lr, lr = st["spikes"]
        for i in range(cnt):
            az = -math.pi + 2 * math.pi * (i + rng.uniform(0.2, 0.8)) / cnt
            if abs(az) < math.radians(40): continue                       # not over the face
            el = math.radians(rng.uniform(5, 40))
            clump(az, el, rng.uniform(*Lr) * w, rng.uniform(*rr) * w, rng.uniform(*lr), st["droop"] * 0.6, st["flat"])
        # hem: clumps along the hairline at the sides and back, hanging down past it (a jagged lower edge)
        cnt, rr, Lr = st["hem"]
        for i in range(cnt):
            az = math.radians(50 + 260 * (i + rng.uniform(0.2, 0.8)) / cnt)
            zt = hairline(az) + 0.03 * H
            el = math.asin(max(-0.95, min(0.95, zt / (h / 2 + 0.02 * H) * 0.9)))
            fl = np.array([math.sin(az) * 0.3, -math.cos(az) * 0.3, -1.0])
            clump(az, el, rng.uniform(*Lr) * w, rng.uniform(*rr) * w, rng.uniform(6, 16), st["droop"] * 0.5, st["flat"], inflate=0.006 * H, flow=fl)
        # fringe: clumps over the front edge, hanging onto the forehead
        cnt, rr, Lr = st["fringe"]
        for i in range(cnt):
            az = math.radians(-55 + 110 * (i + rng.uniform(0.25, 0.75)) / cnt)
            el = math.radians(rng.uniform(30, 48))
            fl = np.array([math.sin(az) * 0.5, -0.35, -1.0])
            clump(az, el, rng.uniform(*Lr) * w, rng.uniform(*rr) * w, rng.uniform(4, 12), 0.05, st["flat"], inflate=0.006 * H, flow=fl)
        v, f = G.merge(locks)
        self.part("hair", "neck", (v, f), self.mats["hair"])

    def _build_helmet(self):
        S, H, Mt = self.S, self.H, self.mats
        w, d, h = self.head_dims
        c = np.asarray(self.head_c)
        hv, hf = G.rbox(w / 2 * 1.20, d / 2 * 1.24, h / 2 * 0.62, w / 2 * 0.95, (5, 5, 3))
        hv = hv[:, :] ; keep = hv[:, 2] > -1
        hv[:, 2] = np.maximum(hv[:, 2], 0.0)
        hv += c + np.array([0, 0.004 * H, h * 0.14])
        self.part("helmet", "neck", (hv, hf), Mt["helmet"])
        bv, bf = G.ring(w / 2 * 1.18, d / 2 * 1.22, w / 2 * 0.8, 0, 0.022 * H, off=0.0, th=0.012 * H)
        bv += c + np.array([0, 0.004 * H, h * 0.14 - 0.004 * H])
        self.part("helmet_brim", "neck", (bv, bf), Mt["helmet"])
        cr = [self._box(c[0], c[1] - d / 2 * 1.10, c[2] + h * 0.42, 0.012 * H, 0.004 * H, 0.032 * H, 0.003 * H, (1, 1, 1)),
              self._box(c[0], c[1] - d / 2 * 1.10, c[2] + h * 0.42, 0.032 * H, 0.004 * H, 0.012 * H, 0.003 * H, (1, 1, 1))]
        self.part("helmet_cross", "neck", G.merge(cr), Mt["red"])
        lb = self._box(c[0] + w * 0.22, c[1] - d / 2 * 1.20, c[2] + h * 0.36, 0.030 * H, 0.020 * H, 0.022 * H, 0.008 * H, (1, 1, 1))
        self.part("helmet_lampbox", "neck", lb, Mt["black"])
        lv, lf = G.disc(0.017 * H, 0.004 * H, 20)
        lv += np.array([c[0] + w * 0.22, c[1] - d / 2 * 1.20 - 0.021 * H, c[2] + h * 0.36])
        self.part("helmet_lamp", "neck", (lv, lf), Mt["lamp"])

    # ------------------------------------------------------------------------------------------------ kit
    def _build_kit(self):
        if self.S["kit"] == "rescue": self._kit_rescue()
        else: self._kit_office()

    def _on_torso(self, pts, off):
        """lay rest-space points onto the torso shell (rounded box) and push them out by off -> points, normals."""
        S, H = self.S, self.H
        T = S["torso"]
        c = (0, 0, (T["z0"] + T["z1"]) / 2 * H)
        half = (T["w_top"] / 2 * H, T["d"] / 2 * H, (T["z1"] - T["z0"]) / 2 * H)
        out, nr = [], []
        for p in pts:
            q, n = G.onto_rbox(p, c, half, T["r"] * H, off)
            out.append(q); nr.append(n)
        return out, nr

    def _strap(self, name, ctrl, width, thick, mat, joint="waist", n=28, off=None):
        H = self.H
        ctrl = [np.asarray(p, float) for p in ctrl]
        # resample the control polyline
        seg = [np.linalg.norm(b - a) for a, b in zip(ctrl[:-1], ctrl[1:])]
        tot = sum(seg); pts = []
        for i in range(n):
            s = tot * i / (n - 1); k = 0
            while k < len(seg) - 1 and s > seg[k]: s -= seg[k]; k += 1
            pts.append(ctrl[k] + (ctrl[k + 1] - ctrl[k]) * min(1.0, s / max(seg[k], 1e-9)))
        pts, nr = self._on_torso(pts, off if off is not None else 0.006 * H)
        v, f = G.sweep(pts, [width / 2] * len(pts), flat=thick / width, normals=nr, rect=True, cap0=True, tip=False)
        return self.part(name, joint, (v, f), mat)

    def _tape_ring(self, name, joint, hx, hy, r, z0, z1, xc=0.0, yc=0.0, off=0.003):
        H = self.H
        v, f = G.ring(hx, hy, r, z0, z1, off=off * H, th=0.0025 * H, n=10)
        v[:, 0] += xc; v[:, 1] += yc
        ob = self.part(name, joint, (v, f), self.mats["tape"])
        me = ob.data
        at = me.attributes.new("tapev", "FLOAT", "POINT")
        co = np.zeros(len(me.vertices) * 3); me.vertices.foreach_get("co", co); co = co.reshape(-1, 3)
        zz = co[:, 2] + self.rest[joint][2]
        at.data.foreach_set("value", np.clip((zz - z0) / max(z1 - z0, 1e-6), 0, 1).astype(np.float32))
        return ob

    def _kit_rescue(self):
        S, H, Mt = self.S, self.H, self.mats
        T = S["torso"]; tw, td = T["w_top"] / 2 * H, T["d"] / 2 * H
        z1 = T["z1"] * H
        # reflective bands: chest, upper arms, shins
        self._tape_ring("tape_chest", "waist", T["w"] / 2 * H * 1.003, td, T["r"] * H, 0.528 * H, 0.566 * H)
        for side, sx in (("L", 1), ("R", -1)):
            x = sx * S["sh"]["x"] * H
            U = S["upper"]
            self._tape_ring("tape_arm_" + side, "sh_" + side, U["w"] / 2 * H, U["d"] / 2 * H, 0.035 * H, 0.556 * H, 0.594 * H, xc=x)
            hx = sx * S["hip"]["x"] * H
            LL = S["lleg"]
            self._tape_ring("tape_leg_" + side, "kn_" + side, LL["w"] / 2 * H * 1.01, LL["d"] / 2 * H * 1.01, 0.035 * H, 0.162 * H, 0.198 * H, xc=hx)
            # cargo pocket on the outer thigh + flap
            UL = S["uleg"]
            px = hx + sx * (UL["w"] / 2 * H + 0.006 * H)
            pk = self._box(px, -0.01 * H, 0.255 * H, 0.012 * H, 0.060 * H, 0.050 * H, 0.010 * H, (1, 2, 2))
            fl = self._box(px + sx * 0.004 * H, -0.01 * H, 0.300 * H, 0.012 * H, 0.064 * H, 0.012 * H, 0.006 * H, (1, 2, 1))
            self.part("pocket_" + side, "hip_" + side, G.merge([pk, fl]), Mt["trousers"])
            # front thigh pocket
            fp = self._box(hx, -UL["d"] / 2 * H - 0.006 * H, 0.262 * H, 0.050 * H, 0.008 * H, 0.040 * H, 0.008 * H, (2, 1, 2))
            self.part("fpocket_" + side, "hip_" + side, fp, Mt["trousers"])
        # star-of-life patch on the LEFT upper arm (outer face)
        pv, pf = G.disc(0.040 * H, 0.004 * H, 40)
        x = S["sh"]["x"] * H + S["upper"]["w"] / 2 * H + 0.002 * H
        pv2 = pv @ G.rotz(math.pi / 2).T                     # face +X (outward on the left arm)
        uv = np.zeros((len(pv), 2))
        uv[:, 0] = 0.5 - pv[:, 0] / (0.080 * H) * 1.0; uv[:, 1] = 0.5 + pv[:, 2] / (0.080 * H)
        pv2 += np.array([x, 0.0, 0.625 * H])
        self.part("star_L", "sh_L", (pv2, pf), Mt["patch"], uv=uv)
        # collar: two flaps on the shoulders and a band behind the neck
        for sx in (1, -1):
            cv = self._box(sx * 0.070 * H, -0.035 * H, z1 + 0.006 * H, 0.050 * H, 0.060 * H, 0.010 * H, 0.008 * H, (2, 2, 1))
            vv = cv[0] - np.array([sx * 0.070 * H, -0.035 * H, z1 + 0.006 * H])
            vv = vv @ G.rotz(sx * -0.45).T @ G.roty(sx * 0.20).T
            self.part("collar_%d" % sx, "waist", (vv + np.array([sx * 0.072 * H, -0.050 * H, z1 + 0.004 * H]), cv[1]), Mt["jacket"])
        bv, bf = G.ring(0.085 * H, 0.060 * H, 0.045 * H, z1 - 0.004 * H, z1 + 0.044 * H, off=0.0, th=0.012 * H,
                        skip=lambda xx, yy: yy < -0.03 * H and abs(xx) < 0.045 * H)
        bv[:, 1] += 0.012 * H
        self.part("collar_back", "waist", (bv, bf), Mt["jacket"])
        # chest pockets (flaps) and the name badge
        for sx in (1, -1):
            cp = self._box(sx * 0.10 * H, -td - 0.004 * H, 0.615 * H, 0.055 * H, 0.005 * H, 0.012 * H, 0.004 * H, (2, 1, 1))
            self.part("chestflap_%d" % sx, "waist", cp, Mt["jacket"])
        bd = self._box(0.105 * H, -td - 0.004 * H, 0.590 * H, 0.040 * H, 0.003 * H, 0.012 * H, 0.002 * H, (2, 1, 1))
        self.part("badge", "waist", bd, Mt["badge"])
        # harness: a cross strap from the LEFT shoulder to the right hip, front and back; a vertical strap on the right
        zt = z1
        f_ = -td; b_ = td
        cross = [(-0.15 * H, f_, 0.47 * H), (0.0, f_, 0.56 * H), (0.10 * H, f_, 0.64 * H), (0.13 * H, f_ * 0.6, zt), (0.13 * H, 0.0, zt + 0.01 * H),
                 (0.13 * H, b_ * 0.6, zt), (0.10 * H, b_, 0.64 * H), (0.0, b_, 0.56 * H), (-0.15 * H, b_, 0.47 * H)]
        self._strap("strap_cross", cross, 0.050 * H, 0.010 * H, Mt["webbing"])
        vert = [(-0.115 * H, f_, 0.47 * H), (-0.115 * H, f_, 0.60 * H), (-0.12 * H, f_ * 0.6, zt), (-0.12 * H, 0.0, zt + 0.01 * H),
                (-0.12 * H, b_ * 0.6, zt), (-0.115 * H, b_, 0.60 * H), (-0.115 * H, b_, 0.47 * H)]
        self._strap("strap_vert", vert, 0.042 * H, 0.009 * H, Mt["webbing"])
        bk = self._box(0.035 * H, f_ - 0.018 * H, 0.585 * H, 0.022 * H, 0.006 * H, 0.016 * H, 0.004 * H, (1, 1, 1))
        self.part("strap_buckle", "waist", bk, Mt["metal"])
        # radio on the vertical strap (right chest) with an antenna and a green LED
        rd = self._box(-0.115 * H, f_ - 0.030 * H, 0.600 * H, 0.030 * H, 0.020 * H, 0.050 * H, 0.008 * H, (1, 1, 2))
        an = G.sweep([(-0.132 * H, f_ - 0.030 * H, 0.645 * H), (-0.132 * H, f_ - 0.030 * H, 0.700 * H)], [0.006 * H, 0.004 * H], 8, tip=True)
        self.part("radio", "waist", G.merge([rd, an]), Mt["radio"])
        ld = self._box(-0.105 * H, f_ - 0.051 * H, 0.625 * H, 0.008 * H, 0.002 * H, 0.010 * H, 0.002 * H, (1, 1, 1))
        self.part("radio_led", "waist", ld, Mt["led"])
        # utility belt + buckle + pouches (on the pelvis: it stays with the hips when he leans)
        P = S["pelvis"]; bz = S["belt"]["z"] * H; bh = S["belt"]["h"] * H
        bv, bf = G.ring(P["w"] / 2 * H, P["d"] / 2 * H, P["r"] * H, bz - bh / 2, bz + bh / 2, off=0.004 * H, th=0.010 * H)
        self.part("belt", "pelvis", (bv, bf), Mt["webbing"])
        bu = self._box(0.0, -P["d"] / 2 * H - 0.018 * H, bz, 0.030 * H, 0.006 * H, 0.020 * H, 0.004 * H, (1, 1, 1))
        self.part("belt_buckle", "pelvis", bu, Mt["metal"])
        pouches = []
        for (px, sz) in ((-0.13 * H, 1.0), (-0.075 * H, 0.9), (0.075 * H, 0.9), (0.13 * H, 1.0)):
            pouches.append(self._box(px, -P["d"] / 2 * H - 0.028 * H, bz - 0.020 * H, 0.030 * H * sz, 0.022 * H, 0.040 * H, 0.008 * H, (1, 1, 2)))
            pouches.append(self._box(px, -P["d"] / 2 * H - 0.030 * H, bz + 0.012 * H, 0.031 * H * sz, 0.024 * H, 0.010 * H, 0.005 * H, (1, 1, 1)))
        for sx in (1, -1):
            pouches.append(self._box(sx * (P["w"] / 2 * H + 0.024 * H), 0.0, bz - 0.022 * H, 0.020 * H, 0.040 * H, 0.042 * H, 0.008 * H, (1, 1, 2)))
        self.part("pouches", "pelvis", G.merge(pouches), Mt["webbing"])
        snaps = [self._box(px, -P["d"] / 2 * H - 0.055 * H, bz + 0.004 * H, 0.005 * H, 0.003 * H, 0.005 * H, 0.002 * H, (1, 1, 1))
                 for px in (-0.13 * H, -0.075 * H, 0.075 * H, 0.13 * H)]
        self.part("pouch_snaps", "pelvis", G.merge(snaps), Mt["metal"])
        # gloves: shells over the hands (the skin hands are hidden under them)
        if self.gloves:
            pass

    def _kit_office(self):
        S, H, Mt = self.S, self.H, self.mats
        T = S["torso"]; td = T["d"] / 2 * H; z1 = T["z1"] * H
        P = S["pelvis"]
        # shirt tail: a skirt from the waist to a torn hem, open at the front centre
        rng = np.random.RandomState(9)
        ph = rng.uniform(0, 6, 4)
        def jag(xx, yy, z0):
            a = math.atan2(yy, xx)
            return z0 - (0.020 * H * abs(math.sin(5 * a + ph[0])) + 0.018 * H * abs(math.sin(13 * a + ph[1])) ** 3 + 0.010 * H * math.sin(31 * a + ph[2]))
        sv, sf = G.ring(T["w"] / 2 * H * 0.985, td, T["r"] * H, 0.345 * H, 0.445 * H, off=0.003 * H, th=0.006 * H, n=16,
                        skip=lambda xx, yy: yy < -td * 0.8 and abs(xx) < 0.030 * H, zfun=jag)
        self.part("shirt_tail", "pelvis", (sv, sf), Mt["shirt"])
        # collar (open), tie knot, tie blade swinging a little to his left
        for sx in (1, -1):
            cv = self._box(sx * 0.068 * H, -0.03 * H, z1 + 0.008 * H, 0.050 * H, 0.055 * H, 0.009 * H, 0.008 * H, (2, 2, 1))
            vv = cv[0] - np.array([sx * 0.068 * H, -0.03 * H, z1 + 0.008 * H])
            vv = vv @ G.rotz(sx * -0.55).T @ G.roty(sx * 0.30).T
            self.part("collar_%d" % sx, "waist", (vv + np.array([sx * 0.066 * H, -0.050 * H, z1 + 0.002 * H]), cv[1]), Mt["shirt"])
        bv, bf = G.ring(0.085 * H, 0.050 * H, 0.04 * H, z1 - 0.004 * H, z1 + 0.034 * H, off=0.0, th=0.010 * H, skip=lambda xx, yy: yy < -0.02 * H)
        bv[:, 1] += 0.020 * H
        self.part("collar_back", "waist", (bv, bf), Mt["shirt"])
        kn = self._box(0.0, -td - 0.012 * H, z1 - 0.022 * H, 0.020 * H, 0.012 * H, 0.020 * H, 0.008 * H, (1, 1, 1))
        self.part("tie_knot", "waist", kn, Mt["tie"])
        tie = [(0.0, -td, z1 - 0.040 * H), (0.008 * H, -td, 0.58 * H), (0.022 * H, -td, 0.47 * H), (0.030 * H, -td, 0.420 * H)]
        n = 16
        pts = [np.asarray(tie[0]) + (np.asarray(tie[-1]) - np.asarray(tie[0])) * t for t in np.linspace(0, 1, n)]
        for i, t in enumerate(np.linspace(0, 1, n)):
            pts[i][0] = 0.030 * H * t ** 1.6
        pts, nr = self._on_torso(pts, 0.010 * H)
        wid = [0.016 * H + 0.024 * H * t for t in np.linspace(0, 1, n)]
        wid[-1] = 0.004 * H
        v, f = G.sweep(pts, wid, flat=0.12, normals=nr, rect=True, cap0=True, tip=False)
        self.part("tie", "waist", (v, f), Mt["tie"])
        # lanyard and ID card on his LEFT chest
        lan = [(0.03 * H, -td * 0.5, z1 + 0.004 * H), (0.075 * H, -td, 0.64 * H), (0.10 * H, -td, 0.585 * H)]
        self._strap("lanyard", lan, 0.010 * H, 0.002 * H, Mt["lanyard"], n=12, off=0.006 * H)
        cw, ch = 0.050 * H, 0.072 * H
        cx, cz = 0.10 * H, 0.540 * H
        q, nn = self._on_torso([(cx, -td, cz)], 0.012 * H)
        q = q[0]
        card = self._box(cx, q[1] + 0.002 * H, cz, cw / 2, 0.002 * H, ch / 2, 0.003 * H, (1, 1, 1))
        self.part("card_back", "waist", card, Mt["belt"])
        fv = np.array([(-cw / 2, 0, -ch / 2), (cw / 2, 0, -ch / 2), (cw / 2, 0, ch / 2), (-cw / 2, 0, ch / 2)]) + np.array([cx, q[1] - 0.0012 * H, cz])
        self.part("card", "waist", (fv, [[0, 1, 2, 3]]), Mt["card"], uv=np.array([(0, 0), (1, 0), (1, 1), (0, 1)]), smooth=False)
        # belt (leather) + buckle, mostly under the shirt tail; a visible front
        bz = S["belt"]["z"] * H; bh = S["belt"]["h"] * H
        bv, bf = G.ring(P["w"] / 2 * H, P["d"] / 2 * H, P["r"] * H, bz - bh / 2, bz + bh / 2, off=0.002 * H, th=0.006 * H)
        self.part("belt", "pelvis", (bv, bf), Mt["belt"])
        bu = self._box(0.0, -P["d"] / 2 * H - 0.010 * H, bz, 0.020 * H, 0.004 * H, 0.014 * H, 0.003 * H, (1, 1, 1))
        self.part("belt_buckle", "pelvis", bu, Mt["metal"])

    # ------------------------------------------------------------------------------------------------ placement
    @property
    def objects(self):
        return list(self.objs) + [p for p in self.props.values()]

    def place(self, loc, facing_deg=0.0):
        self.root.location = tuple(loc)
        self.root.rotation_euler = (0, 0, math.radians(facing_deg))
        self.facing = facing_deg

    def hide(self, h=True):
        if h:
            for o in self.objects: o.hide_render = True
            return
        self._apply_visibility()
        for k, p in self.props.items(): p.hide_render = k not in getattr(self, "_props_on", ())

    def set_pass_index(self, i):
        self.pidx = i
        for o in self.objects: o.pass_index = i

    def _apply_visibility(self):
        shapes = getattr(self, "_hand_shape", {"L": "fist", "R": "fist"})
        hand_obs = set()
        for side in ("L", "R"):
            for k, obs in self.hands[side].items():
                for o in obs:
                    hand_obs.add(o.name); o.hide_render = (k != shapes[side])
        for o in self.objs:
            if o.name not in hand_obs: o.hide_render = False

    # ------------------------------------------------------------------------------------------------ pose
    def rest_pose(self):
        for j in self.J.values():
            j.rotation_quaternion = (1, 0, 0, 0); j.scale = (1, 1, 1)
        for nm in self.J:
            par = self.J[nm].parent
            pn = next((k for k, v in self.J.items() if v == par), None)
            self.J[nm].location = tuple(self.rest[nm] - (self.rest[pn] if pn else Vector((0, 0, 0))))
        self._hand_shape = {"L": "fist", "R": "fist"}
        self._apply_visibility()

    def cam_side(self, camera):
        """'L' if the camera is on the character's left (+X side), else 'R'."""
        if camera is None: return "L"
        bpy.context.view_layer.update()
        p = self.root.matrix_world.inverted() @ camera.matrix_world.translation
        return "L" if p.x >= 0 else "R"

    def pose(self, P, camera=None):
        """P: the puppets' pose dict (see API.md).  'view' and 's' are ignored: the model is 3D."""
        S, H, D = self.S, self.H, self.D
        self.rest_pose()
        near = self.cam_side(camera)
        far = "R" if near == "L" else "L"
        # ---------- pelvis / legs
        legs = P.get("legs", "stand")
        hip = P.get("hip", (0, 0)) or (0, 0)
        pel = Vector(self.rest["pelvis"]) + Vector((0, -hip[0] * D, -hip[1] * D))
        seated = isinstance(legs, dict) and legs.get("seated")
        feet = {}
        hx = S["hip"]["x"] * H; az = S["ankle_z"] * H
        if seated:
            for side, sx in (("L", 1), ("R", -1)):
                feet[side] = Vector((sx * hx * 1.15, -(self.len["thigh"] + 0.02 * H), pel.z - self.len["shin"] * 0.98))
        else:
            name = legs if isinstance(legs, str) else "stand"
            spread, fwd_n, fwd_f, drop, lunge_fwd = {"stand": (0.0, 0.0, 0.0, 0.0, 0.0), "wide": (0.040, 0.01, -0.01, 0.012, 0.0),
                                                     "step": (0.010, 0.075, -0.065, 0.020, 0.0), "lunge": (0.025, 0.14, -0.12, 0.045, 0.02),
                                                     "crouch": (0.035, 0.03, -0.02, 0.09, 0.0)}.get(name, (0, 0, 0, 0, 0))
            pel.z -= drop * H; pel.y -= lunge_fwd * H
            for side, sx in (("L", 1), ("R", -1)):
                fw = fwd_n if side == near else fwd_f
                feet[side] = Vector((sx * (hx + spread * H), -fw * H, az))
            if isinstance(legs, dict) and not legs.get("seated"):
                for key, side in (("foot_n", near), ("foot_f", far)):
                    if key in legs:
                        fx, fy = legs[key]
                        feet[side] = Vector(((1 if side == "L" else -1) * hx, -fx * D, az - fy * D))
                if "hip" in legs: pel += Vector((0, -legs["hip"][0] * D, -legs["hip"][1] * D))
        # reachability: lower the pelvis until both ankles can be reached
        Lmax = (self.len["thigh"] + self.len["shin"]) * 0.985
        if not seated:
            for side, sx in (("L", 1), ("R", -1)):
                hp = pel + Vector((sx * hx, 0, 0)); f = feet[side]
                horiz = math.hypot(f.x - hp.x, f.y - hp.y)
                if horiz < Lmax:
                    zmax = f.z + math.sqrt(Lmax * Lmax - horiz * horiz)
                    if pel.z > zmax: pel.z = zmax
        self.J["pelvis"].location = tuple(pel)
        self._legs(pel, feet, seated)
        # ---------- spine, head
        lean = float(P.get("lean", 0.0) or 0.0)
        qw = Quaternion((1, 0, 0), math.radians(lean))
        self.J["waist"].rotation_quaternion = qw
        b = P.get("breath", 0.0)
        hd = P.get("head", (0, 0, 0, 0)) or (0, 0, 0, 0)
        hd = tuple(hd) + (0,) * (4 - len(hd))
        qn = Quaternion((0, 0, 1), math.radians(hd[0])) @ Quaternion((1, 0, 0), math.radians(hd[1]))
        self.J["neck"].rotation_quaternion = qn
        self.J["neck"].location = tuple(Vector(self.rest["neck"] - self.rest["waist"]) + Vector((hd[2] * D * 0.5, 0, -hd[3] * D)))
        # ---------- arms
        shapes = {}
        prop_hand = None
        for side in ("L", "R"):
            key = None
            if side == near and "arm_n" in P: key = P["arm_n"]
            elif side == far and "arm_f" in P: key = P["arm_f"]
            for k2 in ("arm_" + side.lower(), "arm_" + side):
                if key is None and k2 in P: key = P[k2]
            mode = "q" if (("arm_n" in P or "arm_f" in P) and ("arm_" + side.lower()) not in P) else "front"
            pk = None
            for k3 in (("prop_" + side.lower()), ("prop_n" if side == near else "prop_f")):
                if P.get(k3): pk = P[k3]
            shapes[side] = self._arm(side, key if key is not None else "down", mode, pk)
            if pk: prop_hand = (side, pk)
        self._hand_shape = shapes
        self._apply_visibility()
        self._props(prop_hand)
        # ---------- face
        self.set_face(P.get("expr"), P.get("mouth"), P.get("blink", 0), P.get("gaze", (0, 0)))
        return self

    def _legs(self, pel, feet, seated):
        S, H = self.S, self.H
        hx = S["hip"]["x"] * H
        for side, sx in (("L", 1), ("R", -1)):
            hp = pel + Vector((sx * hx, 0, 0))
            T = feet[side]
            pole = Vector((sx * 0.15, -1.0, 0.25 if seated else 0.0))
            q1, q2, E = limb_quats(hp, T, self.len["thigh"], self.len["shin"], pole, +1)
            self.J["hip_" + side].rotation_quaternion = q1
            self.J["kn_" + side].rotation_quaternion = q2
            # flat foot: undo the leg rotations (the pelvis does not rotate)
            self.J["an_" + side].rotation_quaternion = (q1 @ q2).inverted()

    ARM3D = {   # named arm poses -> fist-centre target relative to the shoulder, fractions of H: (out, forward, down), elbow pole, hand shape
        "down": ((0.012, 0.010, 0.262), "back", "fist"), "hang": ((0.016, 0.020, 0.258), "back", "fist"),
        "hips": ((-0.050, 0.0, 0.180), "out", "fist"), "hold_cutter": ((-0.070, 0.110, 0.190), "back", "fist"),
        "phone_ear": (None, "out", "fist"), "phone_look": ((-0.110, 0.160, 0.080), "down", "fist"),
        "point": ((0.010, 0.250, 0.010), "down", "point"), "raise": ((0.040, 0.030, -0.255), "out", "open"),
        "wave": ((0.110, 0.040, -0.190), "down", "open"), "reach": ((-0.020, 0.245, 0.050), "down", "open"),
        "claw": ((-0.030, 0.240, 0.040), "down", "claw"), "claw_up": ((-0.020, 0.215, -0.080), "down", "claw"),
        "lap": ((-0.050, 0.120, 0.220), "back", "fist"), "wheel": ((-0.055, 0.235, 0.070), "down", "fist"),
        "cross": ((-0.200, 0.120, 0.140), "out", "fist"), "head": ((-0.120, 0.030, -0.220), "out", "open"),
        "pocket": ((0.010, 0.0, 0.200), "back", "fist"), "carry": ((-0.040, 0.060, 0.200), "back", "fist"),
        "umbrella": ((-0.050, 0.120, 0.100), "down", "fist"), "shout": ((-0.120, 0.100, -0.120), "down", "open"),
        "guard": ((-0.050, 0.170, 0.020), "down", "open"),
    }
    SHAPE = {"glove": "fist", "grip": "fist", "hand": "fist", "fist": "fist", "open": "open", "claw": "claw", "point": "point"}

    def _arm(self, side, key, mode, prop):
        S, H, D = self.S, self.H, self.D
        sx = 1 if side == "L" else -1
        Sh = Vector(self.rest["sh_" + side] - self.rest["waist"])            # shoulder in the chest frame
        shape = "fist"; pole_k = "back"; tgt = None
        if isinstance(key, str):
            off, pole_k, shape = self.ARM3D.get(key, self.ARM3D["down"])
            if self.S.get("zombie") and key in ("down", "hang"): shape = "fist"
            if off is None or (key == "phone_ear"):
                tgt = self._ear_target(side)
            else:
                tgt = Sh + Vector((sx * off[0] * H, -off[1] * H, -off[2] * H))
        else:
            hxy = key.get("hand", (0.1, 1.0)); el = key.get("elbow")
            shape = self.SHAPE.get(key.get("hand_shape", "fist"), "fist")
            dx, dy = hxy[0] * D, hxy[1] * D
            if prop and prop.get("type") == "phone" and dy < -0.25 * D:
                tgt = self._ear_target(side); pole_k = "out"
            elif mode == "front":
                fwd = 0.04 * H + (0.08 * H if dy < -0.1 * D else 0.0) + (0.10 * H if dx < -0.15 * D else 0.0)
                tgt = Sh + Vector((sx * dx, -fwd, -dy))
                pole_k = "out" if el == 1 else ("down" if el == -1 else ("down" if dy < 0.3 * D else "back"))
            else:
                inward = 0.30 * max(0.0, min(1.0, dx / (1.0 * D))) * S["sh"]["x"] * H
                tgt = Sh + Vector((-sx * inward, -dx, -dy))
                pole_k = "out" if el == 1 else ("down" if dx > 0.3 * D else "back")
        # keep the fist out of the torso block
        T = S["torso"]
        rel = tgt - Vector((0, 0, 0))
        zc = tgt.z + self.rest["waist"].z
        hw = T["w"] / 2 * H + S["fist"]["w"] / 2 * H * 0.9; hd = T["d"] / 2 * H + S["fist"]["d"] / 2 * H * 0.8
        if T["z0"] * H - 0.05 * H < zc < T["z1"] * H and abs(tgt.x) < hw and abs(tgt.y) < hd:
            tgt.y = -hd
        pole = {"back": Vector((sx * 0.35, 1.0, -0.2)), "out": Vector((sx * 1.0, 0.25, -0.3)), "down": Vector((sx * 0.45, 0.2, -1.0))}[pole_k]
        q1, q2, E = limb_quats(Sh, tgt, self.len["upper"], self.len["fore"] + self.len["hand"], pole, -1)
        self.J["sh_" + side].rotation_quaternion = q1
        self.J["el_" + side].rotation_quaternion = q2
        if shape == "claw":
            self.J["wr_" + side].rotation_quaternion = Quaternion((1, 0, 0), math.radians(-25))
        return shape

    def _ear_target(self, side):
        """fist beside the head at ear height (the phone call), in the chest frame."""
        S, H = self.S, self.H
        sx = 1 if side == "L" else -1
        w, d, h = self.head_dims
        c = self.head_c - self.rest["waist"]
        return Vector((sx * (w / 2 + S["fist"]["w"] / 2 * H + 0.030 * H), c.y + 0.01 * H, c.z - 0.03 * H))

    def _props(self, ph):
        for p in self.props.values(): p.hide_render = True
        self._props_on = ()
        if not ph: return
        side, spec = ph
        t = spec.get("type")
        if t != "phone": return
        key = "phone_" + side
        if key not in self.props:
            H = self.H
            pm = bpy.data.materials.get(self.name + "_phone") or M.solid(self.name + "_phone", (0.012, 0.012, 0.016), 0.2, coat=0.6, coat_rough=0.05, H=H)
            v, f = G.rbox(0.040 * H, 0.0045 * H, 0.080 * H, 0.008 * H, (2, 1, 3))
            sx = 1 if side == "L" else -1
            Fz = self.S["fist"]
            cz = self.S["wr_z"] * H + Fz["dz"] * H
            o = self.rest["wr_" + side]
            # held in the fist, its long side along the forearm, the screen toward the body midline
            v = v @ G.rotz(math.pi / 2).T
            v += np.array([sx * self.S["sh"]["x"] * H - sx * 0.065 * H, -0.01 * H, cz + 0.07 * H])
            ob = G.obj(self.name + "_" + key, v - np.asarray(o), f, pm, self.J["wr_" + side], tuple(o), True, None, None, self.coll, self.pidx)
            self.props[key] = ob
        self.props[key].hide_render = False
        self._props_on = (key,)

    def set_face(self, expr=None, mouth=None, blink=0, gaze=(0, 0)):
        z = self.S.get("zombie", False)
        e = expr or ("idle" if z else "determined")
        st = (e, json.dumps(mouth), int(blink or 0), tuple(gaze or (0, 0)))
        if st == self._face_state: return
        pc, pe = FACE.face_png(self.S["face"], e, mouth=mouth, blink=blink, gaze=tuple(gaze or (0, 0)))
        glow = None
        if z:
            glow = 0.0 if FACE.EXPR.get(e, {}).get("eyes") == "zshut" else 7.0
        M.set_face(self.mats["head"], pc, pe, glow)
        self._face_state = st

    # ------------------------------------------------------------------------------------------------ queries
    def head_world(self):
        bpy.context.view_layer.update()
        return self.head.matrix_world.translation.copy()

    def sole_world(self, side):
        """world point at the centre of the sole's bottom face."""
        bpy.context.view_layer.update()
        S, H = self.S, self.H
        B = S["boot"]
        o = self.rest["an_" + side]
        local = Vector((0, (B["heel"] - B["toe"]) / 2 * H, 0)) + Vector((o.x, 0, 0)) - Vector((o.x, o.y, o.z))
        return self.J["an_" + side].matrix_world @ local

    # ------------------------------------------------------------------------------------------------ gait
    def gait_pose(self, t, kind="walk", path0=(0, 0, 0), direction=(0, -1, 0), extra=None, T=None):
        """walk / run along a straight line on flat ground with planted feet.  Returns the dict of what was set."""
        G_ = GAITS[kind]
        H = self.H
        T = T or G_["T"]
        v = G_["v"]                                    # model m/s
        beta = G_["beta"]
        d = Vector(direction).normalized()
        face = math.degrees(math.atan2(d.x, -d.y))
        sc = self.scale
        root_at = lambda tt: Vector(path0) + d * (v * tt * sc)
        self.place(root_at(t), face)
        self.rest_pose()
        S = self.S; hx = S["hip"]["x"] * H; az = S["ankle_z"] * H
        feet, phase = {}, {}
        for side, off in (("L", 0.0), ("R", 0.5)):
            ph = ((t / T) + off) % 1.0
            t_land = t - ph * T
            P_land = v * t_land + v * T * beta / 2          # along the path, model metres from path0
            if ph < beta:
                s_along = P_land; lift = 0.0; pitch = 0.0
            else:
                u = (ph - beta) / (1 - beta)
                e = 0.5 - 0.5 * math.cos(math.pi * u)
                s_along = P_land + v * T * e
                lift = G_["lift"] * H * math.sin(math.pi * u)
                pitch = G_["toe"] * math.sin(2 * math.pi * u)
            root_s = v * t
            feet[side] = (Vector(((1 if side == "L" else -1) * hx * G_["track"], -(s_along - root_s), az + lift)), pitch)
            phase[side] = ph
        # pelvis: lowered so the planted legs never straighten, bob twice per cycle
        bob = G_["bob"] * H * math.cos(4 * math.pi * (t / T))
        pel = Vector(self.rest["pelvis"]) + Vector((0, -G_["fwd"] * H, -G_["drop"] * H + bob))
        Lmax = (self.len["thigh"] + self.len["shin"]) * 0.985
        for side, sx in (("L", 1), ("R", -1)):
            hp = pel + Vector((sx * hx, 0, 0)); f = feet[side][0]
            horiz = math.hypot(f.x - hp.x, f.y - hp.y)
            zmax = f.z + math.sqrt(max(Lmax * Lmax - horiz * horiz, 0.0))
            if pel.z > zmax: pel.z = zmax
        self.J["pelvis"].location = tuple(pel)
        twist = math.radians(G_["twist"]) * math.sin(2 * math.pi * t / T)
        self._legs(pel, {k: v_[0] for k, v_ in feet.items()}, False)
        for side in ("L", "R"):
            p = feet[side][1]
            if p:
                q = self.J["an_" + side].rotation_quaternion
                self.J["an_" + side].rotation_quaternion = q @ Quaternion((1, 0, 0), math.radians(p))
        self.J["waist"].rotation_quaternion = Quaternion((1, 0, 0), math.radians(G_["lean"])) @ Quaternion((0, 0, 1), -twist)
        # arms swing opposite the legs
        for side, sx in (("L", 1), ("R", -1)):
            ph = ((t / T) + (0.5 if side == "L" else 0.0)) % 1.0
            sw = math.sin(2 * math.pi * (t / T + (0.5 if side == "L" else 0.0)) + math.pi / 2)
            self.J["sh_" + side].rotation_quaternion = Quaternion((1, 0, 0), math.radians(-G_["arm"] * sw)) @ Quaternion((0, 1, 0), math.radians(sx * 6))
            self.J["el_" + side].rotation_quaternion = Quaternion((-1, 0, 0), math.radians(G_["elbow"] + 8 * max(0, sw)))
        self.J["neck"].rotation_quaternion = Quaternion((0, 0, 1), twist * 0.6)
        e = dict(expr="determined") if not self.S.get("zombie") else dict(expr="idle")
        if extra: e.update(extra)
        self.set_face(e.get("expr"), e.get("mouth"), e.get("blink", 0), e.get("gaze", (0, 0)))
        return dict(phase=phase, feet={k: tuple(v_[0]) for k, v_ in feet.items()}, beta=beta)


GAITS = {
    # v model m/s, T s, beta stance share, lift / drop / bob / fwd fractions of H, lean / twist / arm / elbow degrees
    "walk": dict(v=0.78, T=0.92, beta=0.60, lift=0.040, drop=0.028, bob=0.006, fwd=0.004, lean=4.0, twist=5.0, arm=22.0, elbow=14.0, toe=10.0, track=1.0),
    "run": dict(v=2.10, T=0.64, beta=0.36, lift=0.075, drop=0.050, bob=0.012, fwd=0.012, lean=13.0, twist=9.0, arm=48.0, elbow=75.0, toe=18.0, track=0.9),
}


# ======================================================================================================= textures
def star_png():
    """the star-of-life patch: white disc, blue six-armed star, white rod, orange border (PIL)."""
    from PIL import Image, ImageDraw
    p = os.path.join(HERE, "tex", "star_of_life.png")
    if os.path.exists(p): return p
    os.makedirs(os.path.dirname(p), exist_ok=True)
    N = 512; im = Image.new("RGB", (N, N), (226, 92, 30)); d = ImageDraw.Draw(im)
    d.ellipse([18, 18, N - 18, N - 18], fill=(236, 236, 232))
    d.ellipse([34, 34, N - 34, N - 34], outline=(30, 70, 160), width=10)
    c = N / 2; L = 170; w = 46
    for k in range(3):
        a = math.radians(90 + 60 * k)
        dx, dy = math.cos(a), math.sin(a); nx, ny = -dy, dx
        pts = [(c + dx * L + nx * w, c - dy * L - ny * w), (c + dx * L - nx * w, c - dy * L + ny * w),
               (c - dx * L - nx * w, c + dy * L + ny * w), (c - dx * L + nx * w, c + dy * L - ny * w)]
        d.polygon(pts, fill=(28, 80, 186))
    d.rectangle([c - 9, c - 120, c + 9, c + 120], fill=(245, 245, 245))
    for k in range(5):
        y = c - 90 + k * 40
        d.arc([c - 26, y - 14, c + 26, y + 26], 200 if k % 2 else 20, 340 if k % 2 else 160, fill=(245, 245, 245), width=9)
    im.save(p)
    return p


def card_png():
    """office ID card: blue header band, a grey photo box with a figure silhouette, name bars, a barcode."""
    from PIL import Image, ImageDraw
    p = os.path.join(HERE, "tex", "id_card.png")
    if os.path.exists(p): return p
    os.makedirs(os.path.dirname(p), exist_ok=True)
    W, Hh = 300, 432
    im = Image.new("RGB", (W, Hh), (236, 238, 240)); d = ImageDraw.Draw(im)
    d.rectangle([0, 0, W, 60], fill=(34, 86, 160))
    d.rectangle([20, 84, 140, 230], fill=(190, 196, 204))
    d.ellipse([52, 104, 108, 160], fill=(40, 40, 46)); d.rectangle([44, 160, 116, 230], fill=(40, 40, 46))
    for k, wd in enumerate((120, 100, 130)):
        d.rectangle([156, 100 + k * 34, 156 + wd, 116 + k * 34], fill=(70, 74, 84))
    d.rectangle([20, 260, 280, 300], fill=(34, 86, 160))
    x = 24
    rnd = np.random.RandomState(4)
    while x < 276:
        wd = int(rnd.randint(2, 7)); d.rectangle([x, 330, x + wd, 400], fill=(20, 22, 26)); x += wd + int(rnd.randint(2, 6))
    d.rectangle([120, 8, 180, 26], fill=(20, 24, 30))
    im.save(p)
    return p


# ======================================================================================================= stage adapter
class _Shim:
    """what stage.py / run.py / the shots read from `Act.a` (the Actor8 they used to wrap)."""

    def __init__(self, act, drop=0.0):
        self._act = act
        self.walk_lock = None
        self.pitch_override = None
        self.pitch_anchor = 0.0
        self.ppd = 240
        f = act.fig
        self.height = act.height
        self.sc = act.height * PUPPET_D_PER_H                    # stage units per puppet D (run.py logs heads with it)
        hip_h = f.rest["pelvis"].z * f.scale
        self.spec = dict(legs=(hip_h + drop) / self.sc - 0.06)   # base.driver_seated: soles = hip - (legs + 0.06) * sc
        self.layers = {}

    def set_glow(self, color=None, strength=None):
        pass                                                     # the puppets' card halo: no 3D equivalent

    def set_pass_index(self, i):
        self._act.fig.set_pass_index(i)

    @property
    def objects(self):
        return self._act.fig.objects

    def hide(self, h=True):
        self._act.fig.hide(h)

    def head_world(self):
        return self._act.fig.head_world()

    def world_of(self, pt_D, layer_z=0.0):
        f = self._act.fig
        bpy.context.view_layer.update()
        return f.root.matrix_world @ Vector((pt_D[0] * f.D, 0.0, -pt_D[1] * f.D))


VIEW_MODE = os.environ.get("BLOCK_VIEW", "ignore")      # "ignore": true 3D facing;  "compat": a forced view turns the figure
VIEW_REL = {"front": 0.0, "q": 38.0, "side": 90.0, "back": 180.0}


def compat_facing(cam, loc, view, s, face, tol=16.0):
    """the facing (degrees, stage convention) that shows `view` to the camera the way the puppet drawing did
    (s = +1: facing screen-right).  Keeps the shot's own facing when it already shows that view (within tol)."""
    if view not in VIEW_REL or cam is None: return face
    M3 = cam.matrix_world.to_3x3()
    rc = Vector((M3[0][0], M3[1][0], 0)); fc = -Vector((M3[0][2], M3[1][2], 0))
    if rc.length < 1e-6 or fc.length < 1e-6: return face
    rc.normalize(); fc.normalize()
    th = math.radians(VIEW_REL[view]); sg = 1.0 if (s is None or s >= 0) else -1.0
    v = -fc * math.cos(th) + rc * sg * math.sin(th)
    want = math.degrees(math.atan2(v.x, -v.y))
    d = (want - face + 180) % 360 - 180
    return face if abs(d) <= tol else want


class BlockAct:
    """drop-in for stage.Act: same set() / hide() / apply(cam) / head() / pt() and attributes."""

    SEATED_SCALE = 0.88        # the seated driver: the toy body is taller above the hips than the puppet, so he is drawn
    SEAT_DROP = 0.12           # 12 % smaller and sits 0.12 stage units deeper, or his hair goes through the sedan roof

    def __init__(self, F, name, kind, height, ppd=200, seated=False, wet=True, gloves=None):
        self.F = F; self.name = name; self.height = height
        self.view_mode = VIEW_MODE
        self.fig = Figure(name, kind, height=height * (self.SEATED_SCALE if seated else 1.0), wet=wet, gloves=gloves)
        self.a = _Shim(self, drop=self.SEAT_DROP if seated else 0.0)
        if seated: self.a.pitch_override = 0.0
        self.key = None; self.visible = False; self.posed = False
        self.loc = (0, 0, 0); self.face = 0.0; self.pose_d = {}
        self.view = None; self.s = None; self.breath = 0.0; self.pidx = 2
        self.fig.hide(True)

    def set(self, loc=None, face=None, view="keep", s="keep", idx=None, **pose):
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

    def apply(self, cam):
        f = self.fig
        if not self.visible:
            f.hide(True); return
        face = self.face
        if self.view_mode == "compat" and self.view:
            face = compat_facing(cam, self.loc, self.view, self.s, self.face)
        self.face_used = face
        f.place(self.loc, face)
        pose = dict(self.pose_d)
        if "_hold" in pose:                                     # the two-handed cutter: both fists forward at the hips
            h = pose.pop("_hold")
            pose.update(arm_n=dict(hand=(0.55, 0.70), elbow=None, hand_shape="grip"), arm_f=dict(hand=(0.70, 0.50), elbow=None, hand_shape="grip"))
        pose["breath"] = self.breath
        key = json.dumps([pose, f.cam_side(cam)], sort_keys=True, default=str)
        if key != self.key or not self.posed:
            f.pose(pose, camera=cam)
            self.key = key
        f.hide(False)
        if self.breath:
            f.J["waist"].scale = (1.0, 1.0, 1.0 + self.breath)
        f.set_pass_index(self.pidx)
        self.posed = True

    def head(self):
        return self.fig.head_world()

    def pt(self, xy, z=0.0):
        return self.a.world_of(xy, z)
