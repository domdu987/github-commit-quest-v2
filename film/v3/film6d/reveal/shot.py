#!/usr/bin/env python3
"""shot.py -- film 6 (ไอ้สิบสาม) "reveal": why the bread lost weight, re-made as a lit 3D scene inside the bakery set
(replaces the flat 2D infographic of the f6d cut).  Film frames g = round(t*30), 30 fps, 720x1280, 12 samples.

    shot A  g 1349..1395  "ไม่ใช่ควัน มันคือน้ำในขนมปัง"  macro of a fresh loaf torn open on the bakery table (board at the
                          near end of the work table), MORNING light, warm crumb, cool blue window rim light; glistening
                          semi-transparent water droplets of many sizes sit in the crumb and start lifting off.  Slow push in.
    shot B  g 1396..1437  "ที่ระเหยหนีไป"   closer; the droplets rise, turn to mist and dissolve into the steam wisps
                          (the set's steam materials, set_steam) above the loaf; the camera tilts up with them.
    shot C  g 1438..1478  "ยิ่งบ่าย ก็ยิ่งเบา"  the hand balance on the counter (small_scale_insert area): a loaf on the pan with
                          thin steam; the sun swings from the MORNING to the AFTERNOON preset (direction, colour, the
                          sun shafts through a shape key, the oven fire 1.0 -> 0.8) while the loaf pan slowly RISES
                          (set_scale +5 -> -4).
    Handles: g 1346..1348 (shot A, 3D) and g 1479..1481 (shot C, 3D).
No text anywhere.  NO depth of field (C.Take switches it off at build and before every render).
Blender frame = g (one timeline; each shot's keys only on its own frames).

    python3 shot.py stills a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final a:b[:step]            -> raw/g_%04d.png + .json
    python3 shot.py deliver                     -> frames/, contact.jpg, compare.jpg, meta.json
"""
import math, os, sys, json, random

HERE = os.path.dirname(os.path.abspath(__file__))
FILM6 = os.path.join(os.path.dirname(os.path.dirname(HERE)), "film6")
G_FIRST, G_LAST = 1346, 1481
A0, B0, C0, C1 = 1349, 1396, 1438, 1478      # shot starts; C1 = last content frame
PROJ = os.path.dirname(os.path.dirname(os.path.dirname(HERE)))


def shot_of(g):
    return "A" if g < B0 else ("B" if g < C0 else "C")


# =============================================================================================== blender part
def _blender():
    sys.path.insert(0, FILM6)
    import common as C                                  # noqa: E402
    return C


if __name__ == "__main__" and sys.argv[1] in ("stills", "final"):
    C = _blender()
    import bpy, bmesh
    from mathutils import Vector, Matrix, Euler, Quaternion
    B = C.B
    T = B.T
    MN = B.MN

TMP = os.path.join(HERE, "work")

# ----------------------------------------------------------------------------- staging (bakery world D)
BOARD_Z = 1.35                       # top of the first cooling board on the table (table top 1.30 + board 0.05)
LOAF_C = (4.34, 3.66)                # torn loaf on the (emptied) first board
LR = 0.30                            # loaf radius (the set's round loaves are 0.24; hero a bit bigger)
SQ = 0.84                            # dome height / radius


def ez(u, kind="sine"):
    u = max(0.0, min(1.0, u))
    return 0.5 - 0.5 * math.cos(math.pi * u) if kind == "sine" else u * u * (3 - 2 * u)


def lerp(a, b, u):
    if isinstance(a, (tuple, list)):
        return tuple(x + (y - x) * u for x, y in zip(a, b))
    return a + (b - a) * u


# cameras (loc, look, lens) at the start / end of each shot -------------------------------------------------
DV = (0.55, 0.835)                   # horizontal direction from the loaf toward the camera (looking out to the counter opening)
RV = (-0.835, 0.55)                  # camera right


def _lp(d, r, z):
    return (LOAF_C[0] + DV[0] * d + RV[0] * r, LOAF_C[1] + DV[1] * d + RV[1] * r, BOARD_Z + z)


CAM = {
    "A": [(_lp(1.85, 0.05, 0.50), _lp(-0.06, -0.02, 0.46), 45.0), (_lp(1.55, 0.04, 0.46), _lp(-0.06, -0.03, 0.42), 45.0)],
    "B": [(_lp(1.05, -0.12, 0.32), _lp(-0.04, -0.16, 0.30), 45.0), (_lp(1.05, -0.12, 0.34), _lp(-0.07, -0.16, 0.56), 45.0)],
    "C": [((2.02, 2.38, 2.16), (2.34, 0.75, 1.84), 26.0), ((1.98, 2.30, 2.14), (2.32, 0.75, 1.84), 26.0)],
}
RANGE = {"A": (G_FIRST, B0 - 1), "B": (B0, C0 - 1), "C": (C0, G_LAST)}


def cam_at(g):
    s = shot_of(g); g0, g1 = RANGE[s]
    if s == "B":                                        # hold, then tilt up with the rising droplets
        u = ez((g - (B0 + 6)) / float(C0 - 1 - (B0 + 6)))
    else:
        u = ez((g - g0) / float(g1 - g0), "sine") if s == "C" else (g - g0) / float(g1 - g0)   # A: linear slow push
    (l0, k0, f0), (l1, k1, f1) = CAM[s]
    return lerp(l0, l1, u), lerp(k0, k1, u), lerp(f0, f1, u)


# droplets ------------------------------------------------------------------------------------------------
def droplet_specs():
    """[(half, s, a, radius, t_lift)] -- deterministic; no two droplets on one half overlap."""
    rr = random.Random(613)
    out = []
    for half, n in (("front", 40), ("back", 18)):
        placed = []
        tries = 0
        while len(placed) < n and tries < 5000:
            tries += 1
            s = 0.10 + 0.78 * math.sqrt(rr.random())
            a = rr.uniform(0.12, math.pi - 0.12)
            k = len(placed)
            r = 0.034 + 0.005 * k if k < 3 else 0.006 + 0.026 * rr.random() ** 2.2
            y, z = LR * s * math.cos(a), SQ * LR * s * math.sin(a)
            if any((y - y2) ** 2 + (z - z2) ** 2 < (r + r2 + 0.006) ** 2 for (y2, z2, r2) in placed):
                continue
            placed.append((y, z, r))
            tl = rr.uniform(1364, 1394) if rr.random() < 0.28 else rr.uniform(1392, 1430)
            out.append((half, s, a, r, tl))
    return out


def droplet_state(tl, g, r):
    """(rise D, fog 0..1, alpha 0..1, scale) of a droplet that lifts at frame tl."""
    dt = g - tl
    if dt <= 0:
        return 0.0, 0.0, 1.0, 1.0
    h = 0.0018 * dt + 0.00022 * dt * dt
    h0, h1 = 0.10, 0.36                                # mist from h0, gone at h1
    fog = ez((h - h0) / 0.10)
    alpha = 1.0 - ez((h - (h0 + 0.06)) / (h1 - h0 - 0.06))
    scale = 1.0 + 0.6 * fog
    return h, fog, alpha, scale


# =============================================================================================== scene building
if __name__ == "__main__" and sys.argv[1] in ("stills", "final"):

    def crumb_png():
        """crumb texture (cream with airy holes), drawn once with PIL."""
        from PIL import Image, ImageDraw, ImageFilter
        import numpy as np
        os.makedirs(TMP, exist_ok=True)
        p = os.path.join(TMP, "crumb_v8.png")
        if os.path.exists(p):
            return p
        W = 1024; rs = np.random.RandomState(5)

        def field(n, blur):
            f = Image.fromarray((rs.rand(n, n) * 255).astype("uint8")).resize((W, W), Image.BICUBIC).filter(ImageFilter.GaussianBlur(blur))
            f = np.asarray(f).astype(float) / 255.0
            return (f - f.mean()) / (f.std() + 1e-6)
        f = 0.65 * field(150, 2.0) + 0.35 * field(400, 1.0)
        hole = np.clip((-0.95 - f) / 0.35, 0, 1)                   # irregular pores (~15 % of the face)
        deep = np.clip((-1.6 - f) / 0.4, 0, 1)
        lip = np.clip(1 - np.abs(f + 0.8) / 0.15, 0, 1) * (np.roll(f, 3, axis=0) > f)   # lit lower lip of each pore
        tone = 0.5 * field(30, 6.0)
        base = np.stack([248 + 4 * tone, 230 + 5 * tone, 188 + 6 * tone], -1)
        col = base * (1 - hole[..., None]) + np.array([228, 204, 156]) * hole[..., None]
        col = col * (1 - deep[..., None]) + np.array([210, 176, 122]) * deep[..., None]
        col = col * (1 - 0.5 * lip[..., None]) + 0.5 * lip[..., None] * np.array([255, 248, 222])
        im = Image.fromarray(np.clip(col, 0, 255).astype("uint8")).filter(ImageFilter.GaussianBlur(0.6))
        im.save(p)
        return p

    SX, SY = 1.0, float(os.environ.get("REV_SY", "1"))

    def mat_droplet():
        """water droplet: camera-only; clear body (alpha grows to the rim), a dark refraction edge, a sharp white highlight and a
        small warm caustic; object colour R = alpha, G = mist (soft white ball as it evaporates)."""
        m = bpy.data.materials.new("REV_drop"); nt = T._tree(m); N = nt.nodes.new; L = nt.links.new
        out = N("ShaderNodeOutputMaterial")
        oi = N("ShaderNodeObjectInfo"); sp = N("ShaderNodeSeparateColor"); L(oi.outputs["Color"], sp.inputs[0])
        lw = N("ShaderNodeLayerWeight"); lw.inputs["Blend"].default_value = 0.5
        fac = lw.outputs["Facing"]

        def math_(op, a, b=None, c=None):
            n = N("ShaderNodeMath"); n.operation = op
            for k, v in enumerate((a, b, c)):
                if v is None:
                    continue
                if isinstance(v, (int, float)):
                    n.inputs[k].default_value = v
                else:
                    L(v, n.inputs[k])
            return n.outputs[0]

        def mixc(f, c0, c1):
            n = N("ShaderNodeMix"); n.data_type = "RGBA"
            if isinstance(f, (int, float)):
                n.inputs[0].default_value = f
            else:
                L(f, n.inputs[0])
            for k, c in ((6, c0), (7, c1)):
                if isinstance(c, tuple):
                    n.inputs[k].default_value = (*c, 1.0)
                else:
                    L(c, n.inputs[k])
            return n.outputs[2]

        # camera-space normal for the highlight
        geo = N("ShaderNodeNewGeometry")
        vt = N("ShaderNodeVectorTransform"); vt.vector_type = "NORMAL"; vt.convert_from = "WORLD"; vt.convert_to = "CAMERA"
        L(geo.outputs["Normal"], vt.inputs[0])

        def spot(d, lo, hi):
            # d = (right, up, toward camera) in the A / B camera frame -> a fixed world vector (the droplets only live in A / B)
            Rw = Vector((RV[0], RV[1], 0.0)); Uw = Vector((0, 0, 1)); Fw = Vector((DV[0], DV[1], 0.0))
            v = (Rw * d[0] + Uw * d[1] + Fw * d[2]).normalized()
            dp = N("ShaderNodeVectorMath"); dp.operation = "DOT_PRODUCT"; L(geo.outputs["Normal"], dp.inputs[0]); dp.inputs[1].default_value = tuple(v)
            mr = N("ShaderNodeMapRange"); mr.interpolation_type = "SMOOTHSTEP"; L(dp.outputs["Value"], mr.inputs[0])
            mr.inputs[1].default_value = lo; mr.inputs[2].default_value = hi
            return mr.outputs[0]
        # camera space: +z toward the camera, +y up, +x right (blender camera looks down -z)
        hl = spot((-0.40, 0.48, 0.78), 0.935, 0.97)              # sharp window highlight, upper left
        hl2 = spot((0.30, 0.20, 0.93), 0.975, 0.99)              # small second glint
        cau = spot((0.25, -0.78, 0.57), 0.86, 0.97)              # warm caustic crescent inside the lower edge
        upper = spot((0.0, 1.0, 0.0), -0.3, 0.55)                # the refraction band is dark on the upper side
        rim_cool = spot((-0.2, 0.75, 0.6), 0.80, 0.95)
        band = N("ShaderNodeMapRange"); band.interpolation_type = "SMOOTHSTEP"; L(fac, band.inputs[0])
        band.inputs[1].default_value = 0.40; band.inputs[2].default_value = 0.90
        dark = math_("MULTIPLY", band.outputs[0], math_("MULTIPLY_ADD", upper, 0.7, 0.3))
        col = mixc(math_("MINIMUM", math_("MULTIPLY", dark, 1.6), 1.0), (0.85, 0.93, 1.05), (0.13, 0.10, 0.11))
        col = mixc(math_("MULTIPLY", rim_cool, 0.5), col, (0.55, 0.75, 1.05))
        a_w = math_("MAXIMUM", math_("MULTIPLY_ADD", dark, 0.80, 0.08), math_("MULTIPLY", rim_cool, 0.35))
        # mist: soft white ball (opaque centre, clear rim)
        mist_a = math_("MULTIPLY", math_("POWER", math_("SUBTRACT", 1.0, fac), 2.0), 0.38)
        mist = sp.outputs["Green"]
        a = math_("MULTIPLY", N_mix_val(N, L, mist, a_w, mist_a), sp.outputs["Red"])
        colf = mixc(mist, col, (1.0, 0.98, 0.95))
        em = N("ShaderNodeEmission"); L(colf, em.inputs["Color"]); em.inputs["Strength"].default_value = 1.0
        tr = N("ShaderNodeBsdfTransparent")
        mx = N("ShaderNodeMixShader"); L(a, mx.inputs[0]); L(tr.outputs[0], mx.inputs[1]); L(em.outputs[0], mx.inputs[2])
        # highlights (additive), fade with mist and alpha
        hk = math_("MULTIPLY", math_("ADD", math_("MULTIPLY", hl, 4.0), math_("MULTIPLY", hl2, 2.0)), math_("SUBTRACT", 1.0, mist))
        hk = math_("MULTIPLY", hk, sp.outputs["Red"])
        eh = N("ShaderNodeEmission"); eh.inputs["Color"].default_value = (1.0, 1.0, 1.0, 1.0); L(hk, eh.inputs["Strength"])
        ck = math_("MULTIPLY", math_("MULTIPLY", cau, 0.8), math_("MULTIPLY", math_("SUBTRACT", 1.0, mist), sp.outputs["Red"]))
        ec = N("ShaderNodeEmission"); ec.inputs["Color"].default_value = (1.0, 0.78, 0.45, 1.0); L(ck, ec.inputs["Strength"])
        ad = N("ShaderNodeAddShader"); L(mx.outputs[0], ad.inputs[0]); L(eh.outputs[0], ad.inputs[1])
        ad2 = N("ShaderNodeAddShader"); L(ad.outputs[0], ad2.inputs[0]); L(ec.outputs[0], ad2.inputs[1])
        lp = N("ShaderNodeLightPath"); tr2 = N("ShaderNodeBsdfTransparent"); mc = N("ShaderNodeMixShader")
        L(lp.outputs["Is Camera Ray"], mc.inputs[0]); L(tr2.outputs[0], mc.inputs[1]); L(ad2.outputs[0], mc.inputs[2])
        L(mc.outputs[0], out.inputs["Surface"])
        m.cycles.emission_sampling = "NONE"

        return m

    def N_mix_val(N, L, f, a, b):
        n = N("ShaderNodeMix"); n.data_type = "FLOAT"; L(f, n.inputs[0]); L(a, n.inputs[2]); L(b, n.inputs[3])
        return n.outputs[0]

    def half_loaf(name, crumb_m, crust_m, edge_m, bottom_m, seed):
        """half a round loaf, local frame: crust on x >= 0, the torn face near the plane x = 0 facing -x, base on z = 0."""
        mb = T.MB(); r, sq = LR, SQ; rr = random.Random(seed)
        seg, rings = 24, 9
        nz = lambda y, z, k=1.0: MN.vnoise(y * 21 * k + seed, z * 21 * k, seed) - 0.5
        # crust dome
        R = []
        for k in range(rings + 1):
            th = 0.5 * math.pi * k / rings
            row = []
            for i in range(seg + 1):
                ph = -0.5 * math.pi + math.pi * i / seg
                b = 1.0 + 0.05 * (MN.vnoise(3 * math.cos(ph) + seed, 3 * math.sin(ph) + k * 0.6, seed) - 0.5) * math.cos(ph)
                row.append(Vector((r * math.cos(th) * math.cos(ph) * b, r * math.cos(th) * math.sin(ph), sq * r * math.sin(th) * (1 + 0.04 * math.cos(ph)))))
            R.append(row)
        for k in range(rings):
            for i in range(seg):
                mb.face([R[k][i], R[k][i + 1], R[k + 1][i + 1], R[k + 1][i]][::-1], crust_m,
                        [(i / seg, k / rings), ((i + 1) / seg, k / rings), ((i + 1) / seg, (k + 1) / rings), (i / seg, (k + 1) / rings)][::-1])
        # base
        mb.face([R[0][i] for i in range(seg + 1)], bottom_m, [(0.5, 0.5)] * (seg + 1))
        # torn face: polar grid (s, a) on the plane x = 0; s = 1 is the crust rim (= the dome's edge at phi = +-90)
        ns, na = 16, 28
        S_IN = 0.935

        def face_pt(s, a):
            y = r * s * math.cos(a); z = sq * r * s * math.sin(a)
            if s >= S_IN:
                x = -0.004 * (1 - s) / (1 - S_IN)
            else:
                u = s / S_IN
                x = -(0.10 * r * (1 - u * u) + 0.11 * r * nz(y, z) + 0.05 * r * nz(y, z, 2.7)) * (0.35 + 0.65 * (1 - u ** 4)) - 0.004
            return Vector((x, y, z))
        sv = [0.0] + [S_IN * k / (ns - 1) for k in range(1, ns)] + [1.0]
        G = [[face_pt(s, math.pi * j / na) for j in range(na + 1)] for s in sv]
        for k in range(len(sv) - 1):
            mat = crumb_m if sv[k + 1] <= S_IN + 1e-6 else edge_m
            for j in range(na):
                pts = [G[k][j], G[k][j + 1], G[k + 1][j + 1], G[k + 1][j]]
                uvs = [(0.5 + p.y / (2.2 * r), p.z / (2.2 * r)) for p in pts]
                mb.face(pts, mat, uvs)
        ob = mb.obj(name, B.STATE["SET"], hull=0.0035)
        for p in ob.data.polygons:
            p.use_smooth = True
        T.no_bounce(ob)
        return ob, face_pt

    class Reveal(C.Take):
        def __init__(self, quality="preview"):
            C.Take.__init__(self, "bakery", "MORNING", quality=quality, lens=38.0, name="cam_reveal")
            self.scene.frame_start, self.scene.frame_end = 1, 2000
            self.scene.cycles.transparent_max_bounces = 40
            S = B.STATE; M = S["M"]
            self.M = M
            self._clear_board()
            self._thin_hulls()
            # torn loaf ---------------------------------------------------------------------------------------
            cm = B._untoon(T.mat_lit("REV_crumb", image=crumb_png(), gain=1.05, shade_mul=(1.9, 1.35, 0.75), form=(0.0, -0.06, 0.25)))
            self._crumb_bump(cm)
            crust = M["loaf"].copy(); crust.name = "REV_crust"
            for n in crust.node_tree.nodes:
                if n.bl_idname == "ShaderNodeBsdfGlossy":
                    c = n.inputs["Color"].default_value; n.inputs["Color"].default_value = (c[0] * 0.35, c[1] * 0.35, c[2] * 0.35, 1.0)
                    n.inputs["Roughness"].default_value = 0.45
            em = S["C"]("#b47838", 1.0)
            bm = S["C"]("#6e3a1c", 1.0)
            self.back, fp_b = half_loaf("rev_half_back", cm, crust, em, bm, 11)
            self.front, fp_f = half_loaf("rev_half_front", cm, crust, em, bm, 23)
            self.face_pt = dict(back=fp_b, front=fp_f)
            lc = Vector((LOAF_C[0], LOAF_C[1], BOARD_Z))
            # back half: standing behind, its torn face turned to the camera (+y) and tipped back a little
            def face_to(yaw_off, tilt, off):
                n = Vector((DV[0], DV[1], 0.0)); n.rotate(Matrix.Rotation(math.radians(yaw_off), 3, "Z"))
                th = math.atan2(-n.y, -n.x)
                return (Matrix.Translation(Vector(_lp(*off))) @ Matrix.Rotation(th, 4, "Z") @ Matrix.Rotation(math.radians(tilt), 4, "Y"))
            # back half: standing, its torn face to the camera (a little to the left), tipped back 14 deg
            self.back.matrix_world = face_to(-78, 8, (-0.12, 0.21, 0.0))
            # front half: lying back on its crust so the crumb looks up at the camera
            self.front.matrix_world = face_to(32, 12, (0.0, -0.22, 0.0))
            bpy.context.view_layer.update()
            for o in (self.back, self.front):
                zmin = min((o.matrix_world @ v.co).z for v in o.data.vertices)
                o.matrix_world = Matrix.Translation(Vector((0, 0, BOARD_Z - zmin))) @ o.matrix_world
            bpy.context.view_layer.update()
            # a few crumbs on the board
            mbc = T.MB(); rr = random.Random(9)
            for i in range(14):
                p = Vector(_lp(rr.uniform(0.2, 0.6), rr.uniform(-0.4, 0.4), 0.0))
                MN.lumpy(mbc, p + Vector((0, 0, 0.006)), rr.uniform(0.006, 0.014), em, 400 + i, seg=6, rings=3, rough=0.4, squash=0.7)
            T.no_bounce(mbc.obj("rev_crumbs", S["SET"]))
            # droplets ----------------------------------------------------------------------------------------
            dm = mat_droplet()
            sm = T.MB(); sm.sphere((0, 0, 0), 1.0, dm, seg=20, rings=12)
            sph = sm.obj("rev_drop_mesh", S["SET"]); me = sph.data
            for p in me.polygons:
                p.use_smooth = True
            bpy.data.objects.remove(sph, do_unlink=True)
            self.drops = []
            for i, (half, s, a, r, tl) in enumerate(droplet_specs()):
                ob = bpy.data.objects.new("rev_drop_%02d" % i, me)
                S["SET"].objects.link(ob); T.no_bounce(ob); ob.visible_shadow = False
                hob = self.back if half == "back" else self.front
                p = self.face_pt[half](s, a)
                wp = hob.matrix_world @ (p + Vector((-0.55 * r, 0, 0)))
                n = (hob.matrix_world.to_3x3() @ Vector((-1, 0, 0))).normalized()
                self.drops.append(dict(ob=ob, base=wp, n=n, r=r, tl=tl, ph=random.Random(i).uniform(0, 6.28)))
            # steam above the loaf (the set's steam materials: set_steam scales + scrolls them) ----------------
            stb = T.MB(); rr = random.Random(77)
            self.rsteam = [M["steam"].copy(), M["steam2"].copy()]
            for i, m in enumerate(self.rsteam):
                m.name = "REV_steam%d" % i
            R = Vector((-0.83, 0.55, 0.0)); Dv = Vector((0.55, 0.83, 0.0))
            for k, (dx, w, h, z0) in enumerate(((-0.10, 0.22, 0.95, 0.06), (0.07, 0.26, 1.10, 0.12), (-0.01, 0.18, 0.85, 0.20), (0.15, 0.16, 0.75, 0.16))):
                c = lc + R * dx - Dv * (0.04 * k) + Vector((0, 0, 0.16 + z0))
                u = R * (w / 2); v0 = rr.uniform(0, 1)
                stb.pid += 1
                stb.face([c - u, c + u, c + u + Vector((0, 0, h)), c - u + Vector((0, 0, h))], self.rsteam[k % 2],
                         [(0, v0), (1, v0), (1, v0 + 0.6), (0, v0 + 0.6)])
            self.steam_loaf = stb.obj("rev_steam_loaf", S["SET"]); self.steam_loaf.visible_shadow = False; T.no_bounce(self.steam_loaf)
            # steam on the balance loaf (child of the loaf pan pivot) -------------------------------------------
            sml = S["small"]; pan = sml["pans"][0]
            stc = T.MB()
            x, y, z = B.SMALL_SCALE; pz = sml["pz"]; cl = Vector((x - sml["arm"], y, pz - 0.62 + 0.14))
            for k, (dx, w, h) in enumerate(((0.0, 0.20, 0.75), (0.05, 0.16, 0.6))):
                c = cl + Vector((dx, 0.02 * k, 0)); a = math.radians(25 if k else -35)
                u = Vector((math.cos(a), math.sin(a), 0)) * (w / 2)
                stc.pid += 1
                stc.face([c - u, c + u, c + u + Vector((0, 0, h)), c - u + Vector((0, 0, h))], M["steam2"] if k else M["steam"],
                         [(0, 0.2 + 0.3 * k), (1, 0.2 + 0.3 * k), (1, 0.75 + 0.3 * k), (0, 0.75 + 0.3 * k)])
            self.steam_pan = stc.obj("rev_steam_pan", S["SET"]); self.steam_pan.visible_shadow = False; T.no_bounce(self.steam_pan)
            bpy.context.view_layer.update()
            mw = self.steam_pan.matrix_world.copy(); self.steam_pan.parent = pan; self.steam_pan.matrix_parent_inverse = pan.matrix_world.inverted()
            self.steam_pan.matrix_world = mw
            # macro lights: warm key from the oven side, cool rim from the leaded window ---------------------------
            self.warm = self._area("REV_warm", (3.75, 4.9, 2.3), lc + Vector((0, 0, 0.12)), (1.0, 0.70, 0.42), 1.2)
            self.cool = self._area("REV_cool", (5.2, 0.6, 2.9), lc + Vector((0, 0, 0.18)), (0.50, 0.70, 1.0), 1.4)
            # sun sweep (shot C): shape-keyed sun shafts ---------------------------------------------------------
            self._sweep_setup()

        # -------------------------------------------------------------- set edits at runtime (set module untouched)
        def _clear_board(self):
            """empty the first cooling board (6 loaves near the table end) and drop its steam cards."""
            ob = B.STATE["objects"]["table"]; me = ob.data
            loafm = {i for i, m in enumerate(me.materials) if m and "_t_loaf" in m.name}
            bm = bmesh.new(); bm.from_mesh(me)
            kill = [f for f in bm.faces if f.material_index in loafm and f.calc_center_median().y < 5.40 and f.calc_center_median().z > 1.33]
            bmesh.ops.delete(bm, geom=kill, context="FACES"); bm.to_mesh(me); bm.free()
            st = B.STATE["steam"][0]; me = st.data
            bm = bmesh.new(); bm.from_mesh(me)
            kill = [f for f in bm.faces if 3.6 < f.calc_center_median().x < 5.8 and f.calc_center_median().y < 5.5]
            bmesh.ops.delete(bm, geom=kill, context="FACES"); bm.to_mesh(me); bm.free()
            print("reveal: board cleared", flush=True)

        def _crumb_bump(self, m):
            """fine pores: a voronoi + noise bump on the diffuse normal (the area lights rake over it)."""
            nt = m.node_tree; N = nt.nodes.new; L = nt.links.new
            dif = [n for n in nt.nodes if n.bl_idname == "ShaderNodeBsdfDiffuse"][0]
            uv = N("ShaderNodeTexCoord")
            vo = N("ShaderNodeTexVoronoi"); vo.feature = "SMOOTH_F1"; vo.inputs["Scale"].default_value = 70.0; L(uv.outputs["UV"], vo.inputs["Vector"])
            no = N("ShaderNodeTexNoise"); no.inputs["Scale"].default_value = 160.0; L(uv.outputs["UV"], no.inputs["Vector"])
            ad = N("ShaderNodeMath"); ad.operation = "MULTIPLY_ADD"; L(no.outputs["Fac"], ad.inputs[0]); ad.inputs[1].default_value = 0.5; L(vo.outputs["Distance"], ad.inputs[2])
            bp = N("ShaderNodeBump"); bp.inputs["Strength"].default_value = 0.3; bp.inputs["Distance"].default_value = 0.02
            L(ad.outputs[0], bp.inputs["Height"]); L(bp.outputs["Normal"], dif.inputs["Normal"])

        def _thin_hulls(self):
            """ink hulls of the near table are sized for normal shots: thin them for the macro (no fat outlines at 0.8 D)."""
            for nm in ("table",):
                ob = B.STATE["objects"].get(nm)
                for md in (ob.modifiers if ob else []):
                    if md.type == "SOLIDIFY":
                        md.thickness = 0.0045

        def _area(self, name, loc, target, rgb, size):
            d = bpy.data.lights.new(name, "AREA"); d.shape = "DISK"; d.size = size; d.color = rgb; d.energy = 0.0
            ob = bpy.data.objects.new(name, d); B.STATE["LIGHTS"].objects.link(ob)
            ob.location = loc; ob.rotation_euler = (Vector(target) - Vector(loc)).to_track_quat("-Z", "Y").to_euler()
            ob.visible_camera = False
            return ob

        def _sweep_setup(self):
            PM, PA = B.PRESETS["MORNING"], B.PRESETS["AFTERNOON"]
            self.kd = [Vector(PM["key_dir"]).normalized(), Vector(PA["key_dir"]).normalized()]
            self.kc = [tuple(PM["key"]), tuple(PA["key"])]
            self.sun = B.STATE["sun"]
            old = B.STATE["objects"]["sun_shafts"]
            mat = old.data.materials[0]
            old.hide_render = True

            def verts(kd):
                V = []
                for (a, b, c, d) in (B.COUNTER_OPEN, B.DOOR_OPEN, B.WIN_OPEN):
                    if (a, b, c, d) == B.DOOR_OPEN:
                        c = 2.0
                    cs = [Vector((a, 0.0, c)), Vector((b, 0.0, c)), Vector((b, 0.0, d)), Vector((a, 0.0, d))]
                    ext = lambda p: p + kd * min(p.z / max(0.05, -kd.z), 12.0)
                    fa = [ext(p) for p in cs]; mid = lambda p, q: (p + q) / 2
                    V += [mid(cs[0], cs[3]), mid(cs[1], cs[2]), mid(fa[1], fa[2]), mid(fa[0], fa[3])]
                    V += [mid(cs[0], cs[1]), mid(cs[3], cs[2]), mid(fa[3], fa[2]), mid(fa[0], fa[1])]
                return V
            v0 = verts(self.kd[0]); v1 = verts(self.kd[1])
            faces = [tuple(range(4 * k, 4 * k + 4)) for k in range(len(v0) // 4)]
            me = bpy.data.meshes.new("rev_shafts"); me.from_pydata(v0, [], faces); me.update()
            uvl = me.uv_layers.new(name="UVMap")
            for k in range(len(faces)):
                for j, uv in enumerate(((0, 0), (1, 0), (1, 1), (0, 1))):
                    uvl.data[4 * k + j].uv = uv
            me.materials.append(mat)
            ob = bpy.data.objects.new("rev_shafts", me); B.STATE["SET"].objects.link(ob); ob.visible_shadow = False; T.no_bounce(ob)
            ob.shape_key_add(name="Basis"); sk = ob.shape_key_add(name="afternoon")
            for i, v in enumerate(v1):
                sk.data[i].co = v
            self.shafts = ob; self.sk = sk

        # -------------------------------------------------------------- per-frame keys
        def pose(self, gs):
            for g in gs:
                f = g
                s = shot_of(g)
                loc, look, lens = cam_at(g)
                self.key_cam(f, loc, look, lens)
                # steam: thin wisps in A, fuller in B (the droplets feed it), thin off the balance loaf in C
                if s == "A":
                    st = 0.45 + 0.15 * (g - G_FIRST) / float(B0 - G_FIRST)
                elif s == "B":
                    st = 0.65 + 0.35 * ez((g - B0) / float(C0 - B0))
                else:
                    st = 0.55
                u = ez((g - (C0 + 2)) / float(C1 - 4 - (C0 + 2))) if s == "C" else 0.0
                self.key_set(f, steam=st, oven=1.0 - 0.2 * u)
                for i, m in enumerate(self.rsteam):
                    nt = m.node_tree; kv = nt.nodes["steam_k"].outputs[0]; mp = nt.nodes["scroll"].inputs["Location"]
                    kv.default_value = 0.85 * (0.0 if s == "C" else 0.35 + 0.45 * ez((g - 1380) / 50.0))
                    mp.default_value[1] = -0.014 * f * (1.0 if i == 0 else 0.8)
                    kv.keyframe_insert("default_value", frame=f); mp.keyframe_insert("default_value", index=1, frame=f)
                for ob, vis in ((self.steam_loaf, s != "C"), (self.steam_pan, s == "C")):
                    ob.hide_render = not vis; ob.keyframe_insert("hide_render", frame=f)
                # sun sweep
                kd = self.kd[0].slerp(self.kd[1], u) if hasattr(self.kd[0], "slerp") else (self.kd[0].lerp(self.kd[1], u)).normalized()
                kc = lerp(self.kc[0], self.kc[1], u); k = max(kc)
                self.sun.data.color = tuple(x / k for x in kc); self.sun.data.energy = math.pi * k
                self.sun.rotation_euler = (-kd).to_track_quat("Z", "Y").to_euler()
                self.sun.data.keyframe_insert("color", frame=f); self.sun.data.keyframe_insert("energy", frame=f)
                self.sun.keyframe_insert("rotation_euler", frame=f)
                self.sk.value = u; self.sk.keyframe_insert("value", frame=f)
                # balance: the loaf pan rises as the bread dries out
                ub = ez((g - (C0 + 4)) / float(C1 - 2 - (C0 + 4)))
                B.set_scale(5.0 - 9.0 * ub if s == "C" else 5.0, frame=f)
                B.set_scale_loaf(True, frame=f)
                # macro lights only in A / B
                self.warm.data.energy = 0.0 if s == "C" else 60.0
                self.cool.data.energy = 0.0 if s == "C" else 26.0
                self.warm.data.keyframe_insert("energy", frame=f); self.cool.data.keyframe_insert("energy", frame=f)
                for o in (self.back, self.front):
                    o.hide_render = s == "C"; o.keyframe_insert("hide_render", frame=f)
                # droplets
                for i, d in enumerate(self.drops):
                    ob = d["ob"]
                    h, fog, al, sc = droplet_state(d["tl"], g, d["r"])
                    vis = s != "C" and al > 0.01
                    ob.hide_render = not vis; ob.keyframe_insert("hide_render", frame=f)
                    lift_u = ez(h / 0.05)               # leaves the crumb along its normal, then goes straight up
                    wob = Vector((0.012 * math.sin(0.21 * g + d["ph"]) * min(1.0, h / 0.06), 0.0, 0.0))
                    p = d["base"] + d["n"] * (0.012 * lift_u) + Vector((0, 0, h)) + wob
                    # mist drifts toward the steam column above the loaf centre
                    cx = Vector((LOAF_C[0], LOAF_C[1] - 0.05, p.z))
                    p = p.lerp(cx, 0.35 * fog)
                    r = d["r"] * sc * (1.0 + 0.04 * math.sin(0.5 * g + d["ph"]) * (1 - fog))
                    stretch = 1.0 + 0.18 * min(1.0, h / 0.04) * (1 - fog)
                    ob.location = p; ob.scale = (r, r, r * 1.06 * stretch)
                    ob.color = (al, fog, 0.0, 1.0)
                    for path in ("location", "scale", "color"):
                        ob.keyframe_insert(path, frame=f)
            for o in [self.cam] + [d["ob"] for d in self.drops]:
                for fc in C.camrig.fcurves_of(o):
                    for kp in fc.keyframe_points:
                        kp.interpolation = "LINEAR" if fc.data_path != "hide_render" else "CONSTANT"

        def report(self, g):
            loc, look, lens = cam_at(g)
            return dict(g=g, shot=shot_of(g), cam=[round(c, 3) for c in loc], look=[round(c, 3) for c in look], lens=round(lens, 2))

        def render_g(self, gs, out, scale=1.0, samples=12, threads=2):
            return C.Take.render(self, gs, out, scale=scale, samples=samples, threads=threads)


# =============================================================================================== CLI
def parse(spec):
    out = []
    for part in spec.split(","):
        a = [int(v) for v in part.split(":")]
        out += list(range(a[0], a[1] + 1, a[2] if len(a) > 2 else 1)) if len(a) > 1 else [a[0]]
    return out


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "stills":
        gs = parse(sys.argv[2]); out = sys.argv[3]
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 0.5
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 6
        Tk = Reveal("preview"); Tk.pose(gs)
        for g in gs:
            st = Tk.render_g([g], out, scale=scale, samples=samples)[0]
            os.replace(st["path"], os.path.join(out, "g_%04d.png" % g))
            print("g %d %s  %.1f s wall %.1f cpu" % (g, shot_of(g), st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        gs = parse(sys.argv[2]); raw = os.path.join(HERE, "raw"); os.makedirs(raw, exist_ok=True)
        todo = [g for g in gs if not (os.path.exists(os.path.join(raw, "g_%04d.png" % g)) and os.path.exists(os.path.join(raw, "g_%04d.json" % g)))]
        print("final: %d to render" % len(todo), flush=True)
        if todo:
            Tk = Reveal("final"); Tk.pose(todo)
            for g in todo:
                st = Tk.render_g([g], raw)[0]
                png = os.path.join(raw, "g_%04d.png" % g); os.replace(st["path"], png)
                rep = Tk.report(g); rep.update(wall=round(st["wall"], 2), cpu=round(st["cpu"], 2), samples=12)
                json.dump(rep, open(png[:-4] + ".json", "w"))
                print("g %d %s  %.1f s wall  %.1f s cpu" % (g, shot_of(g), st["wall"], st["cpu"]), flush=True)
    elif cmd == "deliver":
        import shutil, glob
        from PIL import Image, ImageDraw
        raw = os.path.join(HERE, "raw"); fr = os.path.join(HERE, "frames"); os.makedirs(fr, exist_ok=True)
        rows = []
        for g in range(G_FIRST, G_LAST + 1):
            shutil.copyfile(os.path.join(raw, "g_%04d.png" % g), os.path.join(fr, "g_%04d.png" % g))
            rows.append(json.load(open(os.path.join(raw, "g_%04d.json" % g))))
        walls = [r["wall"] for r in rows]; cpus = [r["cpu"] for r in rows]
        meta = dict(take="reveal", film=6, first_g=G_FIRST, n_frames=G_LAST - G_FIRST + 1, content=[A0, C1], handles=[[G_FIRST, A0 - 1], [C1 + 1, G_LAST]],
                    shots=dict(A=[A0, B0 - 1], B=[B0, C0 - 1], C=[C0, C1]), transition_in="cut", samples=12, resolution=[720, 1280],
                    s_per_frame_wall_mean=round(sum(walls) / len(walls), 2), s_per_frame_cpu_mean=round(sum(cpus) / len(cpus), 2),
                    dof="none", text="none")
        json.dump(meta, open(os.path.join(HERE, "meta.json"), "w"), indent=1)
        # contact sheet: 24 frames
        gs = [G_FIRST + int(round(i * (G_LAST - G_FIRST) / 23.0)) for i in range(24)]
        w, h, lab, cols = 240, 427, 16, 8
        S = Image.new("RGB", (cols * w, 3 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
        for i, g in enumerate(gs):
            x, y = (i % cols) * w, (i // cols) * (h + lab)
            S.paste(Image.open(os.path.join(fr, "g_%04d.png" % g)).convert("RGB").resize((w, h), Image.LANCZOS), (x, y + lab))
            dr.text((x + 3, y + 2), "g %d  %s" % (g, shot_of(g)), fill=(255, 255, 255))
        S.save(os.path.join(HERE, "contact.jpg"), quality=88)
        # compare: new (top) vs old diagram (bottom)
        pairs = [(1360, 1372), (1420, 1424), (1470, 1466)]
        w, h = 360, 640
        S = Image.new("RGB", (3 * w, 2 * (h + lab)), (16, 12, 20)); dr = ImageDraw.Draw(S)
        for i, (go, gn) in enumerate(pairs):
            S.paste(Image.open(os.path.join(fr, "g_%04d.png" % gn)).convert("RGB").resize((w, h), Image.LANCZOS), (i * w, lab))
            dr.text((i * w + 3, 2), "NEW 3D  g %d (shot %s)" % (gn, shot_of(gn)), fill=(255, 255, 255))
            S.paste(Image.open(os.path.join(PROJ, "deliver", "f6d_frames", "f_%04d.png" % go)).convert("RGB").resize((w, h), Image.LANCZOS), (i * w, 2 * lab + h))
            dr.text((i * w + 3, h + lab + 2), "OLD diagram  f_%d" % go, fill=(255, 255, 255))
        S.save(os.path.join(HERE, "compare.jpg"), quality=88)
        print(json.dumps(meta))
