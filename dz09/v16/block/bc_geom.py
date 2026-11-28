"""bc_geom.py -- mesh builders for the blocky cast (numpy -> bpy meshes).  All sizes in metres, z up, the figure
faces -Y (the stage convention: facing 0 = toward -Y), the character's LEFT is +X.

rbox()     rounded box (soft bevel) with an angle-even edge band, welded: smooth shading without creases
ring()     a rounded-rectangle band around a box (reflective tape, belt, cuffs), closed thin shell
sweep()    a tube / ribbon along a polyline with per-point radii and an optional frame (hair locks, straps, tie)
rbox_sdf() distance + normal to a rounded box (straps and the tie are laid on the torso with it)
obj()      mesh object: material slots, parent joint, the 'rest' point attribute (rest-space position, used by the
           shaders for dirt / blood / wetness placement), pass index
"""
import math
import numpy as np
import bpy
from mathutils import Vector, Matrix


# ------------------------------------------------------------------------------------------------ rounded box
def _axis_params(h, r, n_in, n_band):
    """coordinates along one axis of a face grid: an even interior and an angle-even band in the rounding."""
    r = min(r, h * 0.999)
    a = h - r
    inner = list(np.linspace(-a, a, n_in + 1)) if a > 1e-6 else [0.0]
    band = [a + r * math.tan(math.radians(45.0 * (k + 1) / n_band)) for k in range(n_band)]
    return [-b for b in band[::-1]] + inner + band


def rbox(hx, hy, hz, r, n=(4, 4, 4), band=4):
    """half extents hx, hy, hz; bevel radius r.  n = interior segments per axis.  -> verts (N,3), faces list."""
    r = min(r, hx * 0.98, hy * 0.98, hz * 0.98)          # a radius above a half extent folds the box inside out
    P = [_axis_params(hx, r, n[0], band), _axis_params(hy, r, n[1], band), _axis_params(hz, r, n[2], band)]
    H = (hx, hy, hz)
    verts, faces, index = [], [], {}

    def vid(q):
        q = np.array(q, float)
        inner = np.clip(q, [-(H[0] - r), -(H[1] - r), -(H[2] - r)], [H[0] - r, H[1] - r, H[2] - r])
        d = q - inner
        L = np.linalg.norm(d)
        p = inner + (d / L * r if L > 1e-12 else 0.0)
        k = tuple(np.round(p, 7))
        if k not in index:
            index[k] = len(verts); verts.append(p)
        return index[k]

    for ax in range(3):
        u_ax, v_ax = [(1, 2), (2, 0), (0, 1)][ax]
        for sgn in (-1, 1):
            U, V = P[u_ax], P[v_ax]
            grid = [[None] * len(V) for _ in U]
            for i, u in enumerate(U):
                for j, v in enumerate(V):
                    q = [0.0, 0.0, 0.0]; q[ax] = sgn * H[ax]; q[u_ax] = u; q[v_ax] = v
                    grid[i][j] = vid(q)
            for i in range(len(U) - 1):
                for j in range(len(V) - 1):
                    f = [grid[i][j], grid[i + 1][j], grid[i + 1][j + 1], grid[i][j + 1]]
                    if sgn < 0: f = f[::-1]
                    if len(set(f)) == 4: faces.append(f)
    return np.array(verts), faces


def rbox_sdf(p, hx, hy, hz, r):
    """signed distance and outward normal of a rounded box centred at the origin."""
    p = np.asarray(p, float)
    q = np.abs(p) - np.array([hx - r, hy - r, hz - r])
    qo = np.maximum(q, 0.0)
    d = np.linalg.norm(qo) + min(q.max(), 0.0) - r
    eps = 1e-5
    g = []
    for k in range(3):
        e = np.zeros(3); e[k] = eps
        qp = np.abs(p + e) - np.array([hx - r, hy - r, hz - r]); qm = np.abs(p - e) - np.array([hx - r, hy - r, hz - r])
        dp = np.linalg.norm(np.maximum(qp, 0)) + min(qp.max(), 0) - r
        dm = np.linalg.norm(np.maximum(qm, 0)) + min(qm.max(), 0) - r
        g.append((dp - dm) / (2 * eps))
    g = np.array(g); g /= max(np.linalg.norm(g), 1e-9)
    return d, g


def onto_rbox(p, center, half, r, off):
    """project p onto the rounded box surface (centre, half extents, radius) and push it out by off."""
    c = np.asarray(center, float)
    d, n = rbox_sdf(np.asarray(p, float) - c, *half, r)
    q = np.asarray(p, float) - d * n
    for _ in range(3):                                 # refine (the gradient of a box SDF is exact off the medial axis)
        d, n = rbox_sdf(q - c, *half, r); q = q - d * n
    return q + n * off, n


# ------------------------------------------------------------------------------------------------ ring band
def rrect_loop(hx, hy, r, n=12):
    """closed loop around a rounded rectangle, counter-clockwise from +X."""
    r = min(r, hx * 0.999, hy * 0.999)
    pts = []
    for cx, cy, a0 in ((hx - r, hy - r, 0), (-(hx - r), hy - r, 90), (-(hx - r), -(hy - r), 180), (hx - r, -(hy - r), 270)):
        for k in range(n + 1):
            a = math.radians(a0 + 90.0 * k / n)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
    return pts


def ring(hx, hy, r, z0, z1, off=0.004, th=0.004, n=10, skip=None, zfun=None):
    """a band around a rounded box of half extents (hx, hy) / radius r between heights z0..z1, standing off by
    `off`, `th` thick.  skip(x, y) -> True drops that column (an opening).  zfun(x, y, z_bottom) jags the lower edge."""
    loop = rrect_loop(hx + off + th, hy + off + th, r + off + th, n)
    loop_i = rrect_loop(hx + off, hy + off, r + off, n)
    N = len(loop)
    verts, faces = [], []
    for (x, y), (xi, yi) in zip(loop, loop_i):
        zb = zfun(x, y, z0) if zfun else z0
        verts += [(x, y, zb), (x, y, z1), (xi, yi, z1), (xi, yi, zb)]
    for k in range(N):
        a, b = k, (k + 1) % N
        x, y = loop[k]
        x2, y2 = loop[b]
        if skip and (skip(x, y) or skip(x2, y2)): continue
        A = [4 * a + i for i in range(4)]; Bq = [4 * b + i for i in range(4)]
        faces += [[A[0], Bq[0], Bq[1], A[1]], [A[1], Bq[1], Bq[2], A[2]], [A[2], Bq[2], Bq[3], A[3]], [A[3], Bq[3], Bq[0], A[0]]]
    if skip:                                             # caps at the opening
        for k in range(N):
            b = (k + 1) % N
            sk_a = skip(*loop[k]); sk_b = skip(*loop[b])
            if sk_a != sk_b:
                j = b if sk_a else k
                faces.append([4 * j, 4 * j + 1, 4 * j + 2, 4 * j + 3][::(1 if sk_a else -1)])
    return np.array(verts, float), faces


# ------------------------------------------------------------------------------------------------ sweep
def sweep(path, radii, sides=6, flat=1.0, normals=None, cap0=True, tip=True, twist=0.0, rect=False):
    """tube along `path` (list of 3D points).  radii: per point (width radius); flat = thickness / width.
    normals: optional per-point vectors for the thin axis (ribbons on a surface).  tip: close the end to a point
    when its radius is ~0.  rect: 4 corners (a ribbon with square edges)."""
    P = [np.asarray(p, float) for p in path]
    n = len(P)
    T = []
    for i in range(n):
        a = P[max(i - 1, 0)]; b = P[min(i + 1, n - 1)]
        t = b - a; T.append(t / max(np.linalg.norm(t), 1e-9))
    frames = []
    if normals is not None:
        for i in range(n):
            nn = np.asarray(normals[i], float)
            nn = nn - T[i] * np.dot(nn, T[i]); nn /= max(np.linalg.norm(nn), 1e-9)
            frames.append((np.cross(T[i], nn), nn))           # (width axis, thickness axis)
    else:
        up = np.array([0, 0, 1.0]) if abs(T[0][2]) < 0.9 else np.array([1.0, 0, 0])
        b = np.cross(T[0], up); b /= np.linalg.norm(b)
        for i in range(n):
            b = b - T[i] * np.dot(b, T[i]); b /= max(np.linalg.norm(b), 1e-9)
            nrm = np.cross(T[i], b)
            ang = twist * i / max(n - 1, 1)
            bb = b * math.cos(ang) + nrm * math.sin(ang); nn = np.cross(T[i], bb)
            frames.append((bb, nn))
    if rect:
        sect = [(1, 1), (-1, 1), (-1, -1), (1, -1)]
    else:
        sect = [(math.cos(2 * math.pi * k / sides), math.sin(2 * math.pi * k / sides)) for k in range(sides)]
    S = len(sect)
    verts, faces = [], []
    for i in range(n):
        w, nn = frames[i]
        r = radii[i]
        for cx, cy in sect:
            verts.append(P[i] + w * cx * r + nn * cy * r * flat)
    for i in range(n - 1):
        for k in range(S):
            a = i * S + k; b = i * S + (k + 1) % S
            faces.append([a, b, b + S, a + S])
    if cap0:
        verts.append(P[0]); c = len(verts) - 1
        for k in range(S): faces.append([c, (k + 1) % S, k])
    if tip:
        verts.append(P[-1] + T[-1] * radii[-1] * 0.5); c = len(verts) - 1
        base = (n - 1) * S
        for k in range(S): faces.append([base + k, base + (k + 1) % S, c])
    return np.array(verts, float), faces


def disc(r, th, n=40):
    """flat cylinder (a patch), axis +Y (its front faces -Y), with planar UVs on the -Y face."""
    verts, faces, uvs = [], [], []
    for k in range(n):
        a = 2 * math.pi * k / n
        verts += [(r * math.cos(a), -th / 2, r * math.sin(a)), (r * math.cos(a), th / 2, r * math.sin(a))]
    verts += [(0, -th / 2, 0), (0, th / 2, 0)]
    c0, c1 = 2 * n, 2 * n + 1
    for k in range(n):
        a, b = 2 * k, 2 * ((k + 1) % n)
        faces += [[a, b, b + 1, a + 1], [c0, b, a], [c1, a + 1, b + 1]]
    return np.array(verts, float), faces


# ------------------------------------------------------------------------------------------------ objects
def coll(name="BLOCKCAST"):
    c = bpy.data.collections.get(name)
    if c is None:
        c = bpy.data.collections.new(name); bpy.context.scene.collection.children.link(c)
    return c


def empty(name, parent=None, loc=(0, 0, 0), collection=None):
    ob = bpy.data.objects.new(name, None)
    (collection or coll()).objects.link(ob)
    ob.empty_display_size = 0.05
    ob.rotation_mode = "QUATERNION"
    if parent is not None: ob.parent = parent
    ob.location = loc
    return ob


def obj(name, verts, faces, mats, parent=None, rest_origin=(0, 0, 0), smooth=True, mat_idx=None, uv=None, collection=None, pidx=2):
    """mesh object in its parent joint's frame (verts are joint-local); the 'rest' attribute = verts + rest_origin."""
    me = bpy.data.meshes.new(name)
    v = np.asarray(verts, float)
    me.from_pydata([tuple(p) for p in v], [], [list(f) for f in faces])
    me.validate(clean_customdata=False)
    if smooth:
        me.shade_smooth()
    for m in (mats if isinstance(mats, (list, tuple)) else [mats]):
        me.materials.append(m)
    if mat_idx is not None:
        me.polygons.foreach_set("material_index", list(mat_idx))
    at = me.attributes.new("rest", "FLOAT_VECTOR", "POINT")
    co = np.zeros(len(me.vertices) * 3, np.float32); me.vertices.foreach_get("co", co)
    co = co.reshape(-1, 3) + np.asarray(rest_origin, np.float32)
    at.data.foreach_set("vector", co.ravel())
    if uv is not None:
        uvl = me.uv_layers.new(name="UVMap")
        lv = np.zeros(len(me.loops), np.int32); me.loops.foreach_get("vertex_index", lv)
        uvl.data.foreach_set("uv", np.asarray(uv, np.float32)[lv].ravel())
    ob = bpy.data.objects.new(name, me)
    (collection or coll()).objects.link(ob)
    if parent is not None: ob.parent = parent
    ob.pass_index = pidx
    return ob


def merge(parts):
    """[(verts, faces), ...] -> one (verts, faces)."""
    V, Fc, o = [], [], 0
    for v, f in parts:
        V.append(np.asarray(v, float)); Fc += [[i + o for i in ff] for ff in f]; o += len(v)
    return np.concatenate(V, 0), Fc


def moved(vf, d=(0, 0, 0), R=None, S=None):
    v, f = vf
    v = np.asarray(v, float).copy()
    if S is not None: v = v * np.asarray(S, float)
    if R is not None: v = v @ np.asarray(R, float).T
    return v + np.asarray(d, float), f


def rotz(a):
    c, s = math.cos(a), math.sin(a); return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1.0]])


def rotx(a):
    c, s = math.cos(a), math.sin(a); return np.array([[1.0, 0, 0], [0, c, -s], [0, s, c]])


def roty(a):
    c, s = math.cos(a), math.sin(a); return np.array([[c, 0, s], [0, 1.0, 0], [-s, 0, c]])


def boolean_diff(ob, cutter_vf, name="cut"):
    """ob minus a temporary mesh (exact solver); applied into ob's mesh."""
    v, f = cutter_vf
    me = bpy.data.meshes.new(name); me.from_pydata([tuple(p) for p in v], [], [list(x) for x in f])
    co = bpy.data.objects.new(name, me); bpy.context.scene.collection.objects.link(co)
    co.parent = ob.parent; co.matrix_world = ob.matrix_world.copy()
    md = ob.modifiers.new("bool", "BOOLEAN"); md.operation = "DIFFERENCE"; md.object = co
    try: md.solver = "EXACT"
    except Exception: pass
    dg = bpy.context.evaluated_depsgraph_get()
    dg.update()
    new = bpy.data.meshes.new_from_object(ob.evaluated_get(dg))
    old = ob.data
    ob.modifiers.remove(md)
    ob.data = new
    bpy.data.meshes.remove(old)
    bpy.data.objects.remove(co); bpy.data.meshes.remove(me)
    new.shade_smooth()
    return ob
