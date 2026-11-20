#!/usr/bin/env python3
"""c18.py -- helper for the film-18 take scripts (team 3: s08 s09 s10 s11), adapted from film8/common.py for cast18 + set3d18/jimo.py.

Every take imports this FIRST:   HERE = dirname(abspath(__file__)); sys.path.insert(0, HERE); import c18 as C

What it does
  * puts set3d18 (jimo.py and friends) and cast18 on sys.path; the ox/person card cache goes to <take>/work/cards (the set's own cache is not touched)
  * Take(shot): one location per process; builds the set, patches the render-team items (red slab, cut beam, cloud bars) and renders frame by frame
    (resumable, raw/g_%04d.png).  Everything animated is evaluated on EVERY rendered frame (cards are rebuilt per frame, flicker(g), camera pose per g).
  * pcard(pose_name, **overrides): a person card for any cast18 STORY18 pose with pose overrides (lip-sync mouth, blink, lean ...), cached by content hash
  * place(): a card at a world mark facing the camera, with a laughing bounce (0.06 D at ~3 Hz) and a small sway
  * camera: the set's planned move (jimo_shots.pose_at) extended linearly into the handle frames, optionally blended linear/eased so no frame sits still
"""
import os, sys, math, json, hashlib, inspect, time

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.environ.get("PROJ18", "/home/user/github-commit-quest-v2/film")
SETDIR = os.path.join(PROJ, "v3", "set3d18")
CASTDIR = os.path.join(PROJ, "v3", "cast18")
for p in (SETDIR, CASTDIR):
    if p not in sys.path:
        sys.path.insert(0, p)
WORK = os.path.join(HERE, "work")
import jimo as J                                            # noqa: E402
import jimo_cards as CD                                     # noqa: E402
import jimo_shots as S                                      # noqa: E402
import jimo_r2 as R2                                        # noqa: E402
import bpy                                                  # noqa: E402
from mathutils import Vector as V                           # noqa: E402
CD.CARDS = os.path.join(WORK, "cards")
os.makedirs(CD.CARDS, exist_ok=True)
import cast18                                               # noqa: E402

NARR_T0 = 0.10


# ----------------------------------------------------------------------------- clock
def g_of(t):
    """narration time (s) of an event -> film frame (narration plays at +0.10 s)."""
    return int(round((t + NARR_T0) * 30))


QUOTE1 = (g_of(22.45), g_of(28.38))          # (676, 854): the only frames where a mouth moves in this team's takes


# ----------------------------------------------------------------------------- cards
def _add_horns(m, f):
    """paint two cream cow-horn crescents on the raised fingertips of a mock-moo card (the drawing has hands at the head but no horns): extends the canvas on top."""
    from PIL import Image, ImageDraw
    D = CD.PXD_P
    x0, y0 = f["bbox"][0], f["bbox"][1]
    pad = int(0.55 * D)
    padx = int(0.45 * D)
    im = Image.open(m["path"]).convert("RGBA")
    W, H = im.size
    big = Image.new("RGBA", (W + 2 * padx, H + pad), (0, 0, 0, 0))
    big.paste(im, (padx, pad))
    S = 4
    lay = Image.new("RGBA", ((W + 2 * padx) * S, (H + pad) * S), (0, 0, 0, 0))
    dr = ImageDraw.Draw(lay)
    for side in (-1, 1):
        hx, hy = f["anchors"]["hand_l" if side < 0 else "hand_r"]
        bx, by = ((hx - x0) * D + 4 + padx, (hy - y0) * D + 4 + pad)         # fingertip (hand centre) in px
        bx += side * 0.02 * D; by -= 0.10 * D
        # crescent: outer and inner arcs of a horn leaning outward then curling up
        pts_o, pts_i = [], []
        import math as _m
        n = 14
        for k in range(n + 1):
            t = k / n
            ang = _m.radians(10 + 95 * t)                           # sweep
            r = 0.40 * D
            ox = bx + side * (0.20 * D * _m.sin(ang) * (1 + 0.2 * t))
            oy = by - (0.36 * D * (1 - _m.cos(ang)) + 0.04 * D)
            w = 0.11 * D * (1 - 0.8 * t)
            pts_o.append((ox + side * w * 0.6, oy)); pts_i.append((ox - side * w * 0.6, oy + w))
        poly = pts_o + pts_i[::-1]
        dr.polygon([(x * S, y * S) for x, y in poly], fill=(244, 232, 200, 255), outline=(42, 26, 42, 255))
        dr.line([(x * S, y * S) for x, y in pts_o + [pts_i[-1]]], fill=(42, 26, 42, 255), width=int(0.018 * D * S))
        dr.line([(x * S, y * S) for x, y in pts_i], fill=(42, 26, 42, 255), width=int(0.014 * D * S))
    lay = lay.resize((W + 2 * padx, H + pad), Image.LANCZOS)
    big.alpha_composite(lay)
    big.save(m["path"])
    m["w"] += 2 * padx / D
    m["x0"] -= padx / D
    m["h"] += pad / D
    m["feet"] += pad / D
    return m


def pcard(name, horns=False, **over):
    """person card (dict path/w/h/x0/feet/height) for STORY18[name] with pose overrides; cached on disk by content hash. horns=True paints cow horns on the fingertips."""
    c, pose = cast18.STORY18[name]
    over_key_extra = "|horns" if horns else ""
    pose = dict(pose)
    pose.update(over)
    key = name + "|" + repr(sorted((k, repr(v)) for k, v in over.items())) + over_key_extra
    h = hashlib.md5(key.encode()).hexdigest()[:10]
    nm = h + "_person"
    mp = os.path.join(CD.CARDS, nm + ".json")
    if os.path.exists(mp) and os.path.exists(os.path.join(CD.CARDS, nm + ".png")):
        return json.load(open(mp))
    cast, P = CD._cast()
    f = P.figure(c, pose, "p%s" % h[:6])
    a = f["anchors"]
    m = CD._write(f["svg"], f["bbox"], f["feet_y"], CD.PXD_P, nm)
    m["kind"] = "person"
    m["height"] = f["feet_y"] - a["head_top"][1]
    m["x0"] = f["bbox"][0] - 4.0 / CD.PXD_P
    if horns:
        m = _add_horns(m, f)
    json.dump(m, open(mp, "w"))
    return m


def sway(g, ph=0.0, hz=0.5):
    return math.sin(2 * math.pi * hz * g / 30.0 + ph)


def bounce(g, ph=0.0, hz=3.0, amp=0.06):
    """laughing bounce: 0.06 D at ~3 Hz (|sin| arches, always >= 0)."""
    return amp * abs(math.sin(math.pi * hz * g / 30.0 + ph))


def place(card, pos, camloc, role_h, g, name, bounce_amp=0.0, ph=0.0, roll_deg=0.0, tint=None, k=None, sw_scale=1.0):
    """put a person card at world pos facing camloc; role_h = height in D of the full figure (head top to soles) -> scale; bounce raises it on z; roll tilts it in-plane about the feet."""
    import math as m
    p = V(pos)
    d = V(camloc) - p
    yaw = m.degrees(m.atan2(d.x, -d.y))
    sc = role_h / card["height"]
    z = bounce(g, ph, amp=bounce_amp) if bounce_amp else 0.0
    ob = R2.put_card(card, (p.x, p.y, p.z + z), yaw, sc, name=name, tint=tint, k=k, sw=0.9 * role_h / 3.0 * sw_scale)
    if roll_deg:
        ob.rotation_euler = (0.0, m.radians(roll_deg), m.radians(yaw))
    return ob


# ----------------------------------------------------------------------------- camera
def pose_ext(shot, t, lin=0.0):
    """camera pose of the set's planned move at t (t < 0 / > 1 extend the move linearly for handle frames).  lin blends the eased move with a straight linear one
    so the first / last frames are not near-static: u = (1 - lin) * smooth + lin * t."""
    sh = S.SHOTS[shot]
    def at(tt):
        base = S.pose_at(sh, min(1.0, max(0.0, tt)))
        if lin <= 0:
            return base
        e = S.pose_at(sh, min(1.0, max(0.0, tt)))
        # linear version of the same move: sample pose at the t whose smoothstep equals the blended u
        u = (1 - lin) * (min(1, max(0, tt)) ** 2 * (3 - 2 * min(1, max(0, tt)))) + lin * min(1, max(0, tt))
        # invert smoothstep(u) numerically
        lo, hi = 0.0, 1.0
        for _ in range(30):
            mid = 0.5 * (lo + hi)
            if mid * mid * (3 - 2 * mid) < u:
                lo = mid
            else:
                hi = mid
        return S.pose_at(sh, 0.5 * (lo + hi))
    if 0.0 <= t <= 1.0:
        return at(t)
    a, b = (at(0.0), at(0.12)) if t < 0 else (at(1.0), at(0.88))
    k = (-t if t < 0 else t - 1.0) / 0.12
    out = {}
    for key in ("loc", "look_at"):
        out[key] = tuple(a[key][i] + (a[key][i] - b[key][i]) * k for i in range(3))
    out["lens"] = a["lens"]
    return out


# ----------------------------------------------------------------------------- sky: shortened cloud base bars (QA_ART_SET_R2 instruction 13)
def make_sky(path):
    import jimo_tex as X
    src = inspect.getsource(X.dusk_sky)
    src = src.replace("cx - cw / 2, ", "cx - cw * 0.40, ").replace("cx + cw / 2, ", "cx + cw * 0.40, ")
    src = src.replace("for k in range(34):", "for k in range(0):")   # director QA-tech: the cloud sprites read as stickers -> no clouds
    src = src.replace("def dusk_sky(", "def dusk_sky_short(")
    ns = {}
    exec(src, X.__dict__, ns)
    ns["dusk_sky_short"](path)
    return path


def patch_sky():
    """swap the DUSK sky texture for one whose cloud base bars are as wide as the puffs."""
    path = os.path.join(WORK, "sky_DUSK_clear.png")
    if not os.path.exists(path):
        os.makedirs(WORK, exist_ok=True)
        make_sky(path)
    M = J.STATE["M"]
    mat = M["sky"]
    img = bpy.data.images.load(path, check_existing=True)
    for n in mat.node_tree.nodes:
        if n.bl_idname == "ShaderNodeTexImage":
            img.alpha_mode = n.image.alpha_mode if n.image else "STRAIGHT"
            n.image = img
            n.image.colorspace_settings.name = img.colorspace_settings.name


# ----------------------------------------------------------------------------- red slab -> #8a2a20
def tone_red(objs=("roof", "tower", "cityroof", "citybody", "rampart", "palisade", "props"), hexc="#8a2a20", gain=1.0):
    lin = lambda c: ((c + 0.055) / 1.055) ** 2.4 if c > 0.04045 else c / 12.92
    r, g, b = (lin(int(hexc[i:i + 2], 16) / 255.0) * gain for i in (1, 3, 5))
    ob = J.STATE["objects"]
    done = {}
    for nm in objs:
        o = ob.get(nm)
        if o is None:
            continue
        for slot in o.material_slots:
            m = slot.material
            if m is None or "b82c20" not in m.name:
                continue
            if m.name not in done:
                m2 = m.copy()
                m2.name = m.name + "_toned"
                for n in m2.node_tree.nodes:
                    if n.bl_idname == "ShaderNodeRGB":
                        n.outputs[0].default_value = (r, g, b, 1.0)
                done[m.name] = m2
            slot.material = done[m.name]
    return len(done)


# ----------------------------------------------------------------------------- take
class Take(object):
    def __init__(self, shot, quality="final", samples=None, patches=()):
        self.shot = shot
        self.sh = S.SHOTS[shot]
        self.A = J.build(None, shot)
        self.sc = bpy.context.scene
        J.MN.setup_render(self.sc, quality)
        self.sc.render.threads = int(os.environ.get("THREADS", "2"))
        if samples:
            self.sc.cycles.samples = samples
        self.sc.render.resolution_x, self.sc.render.resolution_y = (720, 1280) if quality == "final" else (360, 640)
        self.cam = J.shot_camera(shot, 0.0)                    # builds the fg prop once (parented to the camera)
        for fn in patches:
            fn(self)
        bpy.context.view_layer.update()

    def camera(self, g, lin=0.0, mod=None):
        t = (g - self.sh["f0"]) / float(self.sh["frames"])
        pose = pose_ext(self.shot, t, lin)
        if mod:
            pose = mod(g, t, dict(pose))
        cam = self.cam
        cam.location = pose["loc"]
        cam.rotation_euler = J._look_rot(pose["loc"], pose["look_at"])
        cam.data.lens = pose["lens"]
        J._sky_follow(self.sc)
        bpy.context.view_layer.update()
        return V(pose["loc"])

    def render_frames(self, gs, outdir, stage_fn, lin=0.0, mod=None, log=None):
        os.makedirs(outdir, exist_ok=True)
        t0 = time.time()
        n = 0
        for g in gs:
            png = os.path.join(outdir, "g_%04d.png" % g)
            if os.path.exists(png):
                continue
            R2.clear_placeholders()
            R2.LIT.clear()
            self.sc.frame_set(g)
            camloc = self.camera(g, lin, mod)
            J.flicker(g)
            stage_fn(g, camloc)
            bpy.context.view_layer.update()
            w, c = J.T.render(png)
            n += 1
            print("g %d: %.1f s wall, %.1f s cpu" % (g, w, c), flush=True)
            if log is not None:
                log.append((g, w, c))
        print("done %d frames in %.0f s (%.1f s/frame)" % (n, time.time() - t0, (time.time() - t0) / max(1, n)), flush=True)


# ----------------------------------------------------------------------------- QA numbers
def framediff(frames_dir, gs, scale=(90, 160)):
    """mean abs diff x255 between consecutive frames on 90x160 grey; returns (median, p90, list)."""
    import numpy as np
    from PIL import Image
    prev = None
    out = []
    for g in gs:
        im = np.asarray(Image.open(os.path.join(frames_dir, "g_%04d.png" % g)).convert("L").resize(scale, Image.BILINEAR), np.float32)
        if prev is not None:
            out.append(float(np.abs(im - prev).mean()))
        prev = im
    a = np.array(out)
    return float(np.median(a)), float(np.percentile(a, 90)), out


def cut_faces_in_rect(objname, rect, cam, mark=None):
    """delete faces of mesh `objname` having a vertex that projects (720x1280 px, current camera) inside rect=(x0,y0,x1,y1): hides a cut / floating fragment at the frame edge."""
    import numpy as np
    o = J.STATE["objects"].get(objname) or bpy.data.objects.get(objname)
    me = o.data
    n = len(me.vertices)
    co = np.empty(n * 3, np.float32); me.vertices.foreach_get("co", co); co = co.reshape(n, 3)
    mw = np.array(o.matrix_world, np.float64)
    w = np.c_[co, np.ones(n)] @ mw.T
    dg = bpy.context.evaluated_depsgraph_get()
    P = np.array(cam.calc_matrix_camera(dg, x=720, y=1280), np.float64)
    vm = np.array(cam.matrix_world.inverted(), np.float64)
    c = w @ (P @ vm).T
    ok = c[:, 3] > 0
    x = (c[:, 0] / np.where(ok, c[:, 3], 1) * 0.5 + 0.5) * 720
    y = (1 - (c[:, 1] / np.where(ok, c[:, 3], 1) * 0.5 + 0.5)) * 1280
    inside = ok & (x >= rect[0]) & (x <= rect[2]) & (y >= rect[1]) & (y <= rect[3])
    if mark is None:
        mark = np.zeros(n, bool)
    mark |= inside
    return mark


def apply_cut(objname, mark):
    import bmesh
    o = J.STATE["objects"].get(objname) or bpy.data.objects.get(objname)
    bm = bmesh.new(); bm.from_mesh(o.data); bm.verts.ensure_lookup_table()
    dl = [f for f in bm.faces if any(mark[v.index] for v in f.verts)]
    for f in dl:
        bm.faces.remove(f)
    bm.to_mesh(o.data); bm.free(); o.data.update()
    return len(dl)


def fg_rope(T, side="right", R=0.22):
    """a coiled rope in the lower `side` corner, 1.9 D in front of the lens, parented to the camera (stays 1-2 D from the lens through the move)."""
    cam = T.cam
    setup = S.pose_at(T.sh, 0.0)
    loc, f, r, u = J._cam_frame(setup)
    sg = 1 if side == "right" else -1
    o = loc + f * 1.9 + r * (0.70 * sg) + u * (-0.58)
    M = J.STATE["M"]
    n0 = set(J.STATE["SET"].objects)
    Bk2 = J.Banks()
    b = Bk2("fgrope", hull=J.T.hull(3.0))
    for k in range(3):
        c = o + u * (0.045 * k)
        rr = R * (1.0 - 0.18 * k)
        n = 14
        for i in range(n):
            a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
            p0 = c + r * (rr * math.cos(a0)) + f * (rr * 0.8 * math.sin(a0))
            p1 = c + r * (rr * math.cos(a1)) + f * (rr * 0.8 * math.sin(a1))
            J.rod(b, p0, p1, 0.04, M["straw_d"], seg=4)
    Bk2.flush(J.STATE["SET"])
    objs = [ob for ob in J.STATE["SET"].objects if ob not in n0]
    for ob in objs:
        J.no_bounce(ob)
        ob.parent = cam
        ob.matrix_parent_inverse = cam.matrix_world.inverted()
    return objs


def make_mod(sh_dur, push=0.0, slide=0.0, sway=0.0, sway_hz=1.7, yawwob=0.0, dz=0.0, dzt=0.0, vz=0.6, drift=0.0, vdrift=0.0):
    """camera modifier: extra push (fraction of the look distance per second), extra lateral slide (px/s of the 720 px frame at the look distance),
    handheld sway (D amplitude, lateral + vertical) and a small look-at wobble (D) -- all linear in time so no frame sits still."""
    def mod(g, t, pose):
        loc = V(pose["loc"]); look = V(pose["look_at"])
        d = look - loc; L = d.length; u = d.normalized()
        right = V((u.y, -u.x, 0.0)).normalized()
        tt = t * sh_dur
        sec = tt                                  # sway / wobble start at zero offset with the shot's first frame (handles run backwards)
        loc = loc + u * (push * L * tt)
        sl = slide * tt / 720.0 * 2 * L * 0.45
        loc = loc + right * sl; look = look + right * sl
        import math as m
        loc = loc + right * (sway * m.sin(2 * m.pi * sway_hz * sec)) + V((0, 0, 1)) * (vz * sway * m.sin(2 * m.pi * sway_hz * 1.3 * sec + 1.0))
        look = look + right * (yawwob * m.sin(2 * m.pi * 1.1 * sec + 0.5)) + V((0, 0, 1)) * (0.5 * yawwob * m.sin(2 * m.pi * 0.9 * sec))
        loc = loc + right * (drift * (tt - 0.5 * sh_dur)) + V((0, 0, 1)) * (vdrift * (tt - 0.5 * sh_dur))   # one-way orbit-like drift, look-at stays on the subject
        look = look + V((0, 0, dz + dzt * t))
        pose["loc"] = tuple(loc); pose["look_at"] = tuple(look)
        return pose
    return mod


def chins(T, shot):
    """max chin y (px of 720x1280) over the stand marks of the heads (general / soldier / ...) at the current camera."""
    from bpy_extras.object_utils import world_to_camera_view as w2c
    out = []
    for role, lst in S.marks_for(shot).items():
        if role not in J.HEIGHT:
            continue
        for m in lst[:12]:
            h = J.HEIGHT[role]
            c = w2c(T.sc, T.cam, V((m[0], m[1], m[2] + h - 1.0)))
            if c.z > 0:
                out.append((1 - c.y) * 1280)
    return max(out) if out else 0.0


LIP_MAP = {"flat": "dash", "talk_a": ("open", 0.5, 0.16), "talk_b": ("open", 0.9, 0.60), "talk_o": ("open", 0.5, 0.5)}


def lip(g, active):
    """quote lip-sync mouth for frame g: closed 'dash' outside the quote; inside, cast18.talk_mouth (a new drawing every 2 frames) mapped to openings that read under the huge moustache."""
    if not active:
        return "dash"
    return LIP_MAP[cast18.talk_mouth(g, 1.0)]


def subject_x(T, shot, role="general"):
    """screen x (px of 720) of the role's first stand mark (head height) at the current camera."""
    from bpy_extras.object_utils import world_to_camera_view as w2c
    m = S.marks_for(shot)[role][0]
    c = w2c(T.sc, T.cam, V((m[0], m[1], m[2] + J.HEIGHT[role] - 0.5)))
    return c.x * 720 if c.z > 0 else -9999


def fg_world_props(T, specs, t=0.5, lin=0.5, mod=None):
    """static WORLD-space foreground props placed relative to the camera pose at shot time t (so a dolly / truck makes them slide across and grow slowly).
    specs: (kind, lateral D (+ right), down D, scale); kind = 'rope' | 'jar' | 'basket'.  Lit period props in the set's own materials, nothing parented to the camera."""
    sh = T.sh
    g = sh["f0"] + t * sh["frames"]
    pose = pose_ext(T.shot, t, lin)
    if mod:
        pose = mod(g, t, dict(pose))
    loc = V(pose["loc"]); look = V(pose["look_at"])
    f = (look - loc).normalized(); r = f.cross(V((0, 0, 1))).normalized(); u = r.cross(f).normalized()
    M = J.STATE["M"]
    n0 = set(J.STATE["SET"].objects)
    Bk2 = J.Banks()
    b = Bk2("fgworld", hull=J.T.hull(3.0))
    for kind, lat, down, sc in specs:
        o = loc + f * 2.8 + r * lat + u * (-down)
        base = V((o.x, o.y, max(0.0, o.z)))
        if kind == "rope":
            for k in range(3):
                c = base + V((0, 0, 0.05 + 0.08 * k))
                rr = 0.55 * sc * (1.0 - 0.18 * k)
                n = 16
                for i in range(n):
                    a0, a1 = 2 * math.pi * i / n, 2 * math.pi * (i + 1) / n
                    J.rod(b, c + V((rr * math.cos(a0), rr * math.sin(a0), 0)), c + V((rr * math.cos(a1), rr * math.sin(a1), 0)), 0.09 * sc, M["straw_d"], seg=4)
        elif kind == "jar":
            J.ellipsoid(b, base + V((0, 0, 0.55 * sc)), 0.5 * sc, 0.5 * sc, 0.6 * sc, M["clay"], seg=12, rings=8, rough=0.05, seed=3)
            J.cyl(b, base + V((0, 0, 1.05 * sc)), 0.3 * sc, 0.25 * sc, M["clay_d"], seg=10, r1=0.35 * sc)
            J.cyl(b, base + V((0, 0, 1.28 * sc)), 0.36 * sc, 0.1 * sc, M["red"], seg=10)
        elif kind == "basket":
            b.frustum(base, base + V((0, 0, 0.7 * sc)), 0.35 * sc, 0.55 * sc, M["straw_d"], seg=10)
    Bk2.flush(J.STATE["SET"])
    objs = [ob for ob in J.STATE["SET"].objects if ob not in n0]
    for ob in objs:
        J.no_bounce(ob)
    return objs


def cut_islands(objname, mark, max_faces=500):
    """delete whole connected islands (posts, poles) of mesh `objname` that contain a vertex flagged in `mark` (cut_faces_in_rect output), if the island is small."""
    import bmesh
    o = J.STATE["objects"].get(objname) or bpy.data.objects.get(objname)
    bm = bmesh.new(); bm.from_mesh(o.data); bm.verts.ensure_lookup_table(); bm.faces.ensure_lookup_table()
    seen = set(); kill = []
    for f in bm.faces:
        if f.index in seen or not any(mark[v.index] for v in f.verts):
            continue
        isl = []; stack = [f]; seen.add(f.index)
        while stack:
            c = stack.pop(); isl.append(c)
            for e in c.edges:
                for nf in e.link_faces:
                    if nf.index not in seen:
                        seen.add(nf.index); stack.append(nf)
        if len(isl) <= max_faces:
            kill.extend(isl)
    for f in kill:
        if f.is_valid:
            bm.faces.remove(f)
    bm.to_mesh(o.data); bm.free(); o.data.update()
    return len(kill)
