#!/usr/bin/env python3
"""ground_check.py -- "nothing floats": ray-cast every character card and prop down onto the set (bpy + mathutils only).

Run it INSIDE Blender (QA_TEAM.md section K), on a .blend or after a shot script has built the scene:

    blender -b scene.blend --python film/v3/tools/ground_check.py -- --every 10 --gap 0.02 --out GROUND.md
    blender -b --python shot.py --python film/v3/tools/ground_check.py -- --every 10 --out GROUND.md     # shot script first
    blender -b --python film/v3/tools/ground_check.py -- --setup shot.py --every 10 --out GROUND.md      # same, one --python
    python3 ground_check.py --every 10 ...                                                               # pip "bpy" module: build the scene yourself, then run_cli()

Options (after the lone "--"):
    --every N        sample every Nth frame of the scene range (default 10; the first and the last frame are always sampled)
    --frames a:b     frame range instead of the scene's (inclusive)          --frame-list 1,40,77   explicit frames
    --gap G          FAIL when the gap to the first surface is more than G scene units (default 0.02); 1 unit = 1 D in v3
    --out FILE       write the report (default GROUND.md)                     --fails-only   leave the OK rows out of the table
    --fix            snap failing objects onto the surface (see below), re-check, report what changed
    --save FILE      save the .blend after --fix (nothing is saved otherwise)
    --setup FILE     python file run first (builds the scene); it may define nothing special
    --include REGEX  also check meshes whose name matches (props whose names the default rules do not know)
    --skip REGEX     never check meshes whose name matches
    --auto-props     treat every mesh that is not ground-like and not larger than --max-prop-size as a prop
    --max-prop-size  largest bbox dimension --auto-props accepts (default 8 units)
    --ground REGEX   extra names that are ground/set (never checked; hits on them are always fine)

WHAT IS CHECKED (per sampled frame, scene.frame_set(f); stage actors are re-synced if the stage package is loaded)
  card   a mesh named "*_card" (stage/actors.py), or custom property gc_role = "card": its lowest VISIBLE alpha row is read
         from the sprite of that frame (alpha > 0.1; bottom-left / middle / bottom-right of that row are the contact points); no
         readable sprite -> bounding box, marked "bbox".
  prop   a mesh with gc_role = "prop", or a name that matches PROP_NAMES (pole, flag, disc, pot, ox, cart, canopy, girder ...).
         Contact points = up to 5 spread-out vertices within 1 cm of its lowest point (so legs count, a hovering canopy does not).
  never  non-meshes, hidden objects, shadow proxies / contact decals / blobs (*_shadow, *_contact, *_gcshadow, gc_role =
         "shadow"), ground/terrain/buildings/sky (GROUND_NAMES or gc_role = "ground"), anything with gc_role = "skip".
  The ray starts 30 cm above each contact point and goes straight down (scene.ray_cast); hits on the object itself, its
  children, and card shadow/decal objects are skipped and the ray continues.  gap = contact z - hit z, the SMALLEST over the
  contact points (one foot on the floor is enough).  No hit -> "NO SURFACE" = FAIL.  gap < 0 (sunk in) is OK.

HOW TO FLAG A THING AS ALLOWED TO BE OFF THE GROUND (birds, thrown objects, flags on poles, smoke, mid-jump)
    obj["airborne"] = True                     # Object properties > Custom Properties, or in python.  Inherited from parents.
    obj["airborne_frames"] = "20:34,60:70"     # airborne only on these frames (inclusive ranges); optional
  The property may also be keyframed (right click > Insert Keyframe on the custom property): it is read on every frame.
  Other tags: obj["gc_role"] = "prop" | "card" | "ground" | "skip" | "shadow".   obj["gc_gap"] = 0.1  per-object tolerance.

--fix  a failing object is moved straight down by its gap (to the hit surface).  The thing that is moved is the object's
  "mover": the object itself or its nearest ancestor that has location animation (an Actor's "<name>_root").  A static
  mover gets a plain location change.  An ANIMATED mover keeps its keys untouched: a Z offset is added on its delta_location
  channel, keyed (LINEAR) on every sampled frame (0 on frames that were fine), so the animation itself is not edited.  Frames
  between samples interpolate the offset, so re-run the check with a smaller --every after a fix.  The report lists every change.

add_contact_shadow(obj, ...) -- a soft dark blob plane on the ground under a card or prop that follows its XY (see below).
Exit code: 1 if any checked object fails (after --fix: if any still fails), else 0.  2 on a usage error.
"""
import array
import fnmatch
import math
import os
import re
import sys

import bpy
from mathutils import Vector

# ----------------------------------------------------------------------------- name rules (override with --include / --skip / --ground)
PROP_NAMES = (r"(^|[_\-. ])(prop|pole|flag|banner|disc|disk|pot|jar|vase|ox|cart|wagon|crate|box|barrel|bucket|bundle|sack|bag|"
              r"canopy|table|chair|stool|bench|lamp|lantern|girder|beam|slab|chunk|rock|stone|statue|cannon|tent|stall|"
              r"basket|cauldron|brazier|torch|sign|ladder|crane|gear|tool|anvil|boat|barge)s?([_\-. 0-9]|$)")
GROUND_NAMES = (r"(floor|ground|terrain|land|field|plain|dune|sand|road|street|path|cobble|pavement|plank|deck|grass|snow|mud|"
                r"water|sea|river|ocean|channel|ice|sky|dome|cloud|star|moon|sun|horizon|wall|building|house|roof|tower|"
                r"hall|palace|city|town|bridge|stair|step|hill|mountain|cliff|island|shore|bank|quay|pier|dock|harb|"
                r"room|ceiling|window|door|fog|haze|backdrop|bg|background|plate|map)")
SHADOW_SUFFIXES = ("_shadow", "_contact", "_gcshadow", "_decal", "_blob")
FOOT_BAND = 0.01          # vertices within this of the lowest point count as contact points
LIFT = 0.3                # the ray starts this far above the contact point (so an object sunk up to this deep still finds its surface)
ALPHA_MIN = 0.1           # alpha above which a sprite pixel is "visible"
MAX_SKIPS = 12            # hits on own/ignored objects the ray may pass through

_img_cache = {}           # path -> (image datablock, width, height, alpha array('f')) or None


# ----------------------------------------------------------------------------- small helpers
def _role(ob):
    r = ob.get("gc_role")
    return str(r).lower() if r is not None else None


def _truthy(v):
    return bool(v) and str(v).lower() not in ("0", "false", "no", "off")


def _ranges(spec):
    out = []
    for part in str(spec).replace(";", ",").split(","):
        part = part.strip()
        if not part:
            continue
        a, _, b = part.partition(":")
        try:
            out.append((float(a), float(b) if b else float(a)))
        except ValueError:
            pass
    return out


def is_airborne(ob, frame):
    """True when `ob` (or a parent) carries airborne=True (animated values are read at the current frame), or
    airborne_frames covers `frame`."""
    o = ob
    while o is not None:
        if "airborne" in o.keys() and _truthy(o["airborne"]):
            return True
        if "airborne_frames" in o.keys():
            for a, b in _ranges(o["airborne_frames"]):
                if a <= frame <= b:
                    return True
        o = o.parent
    return False


def _is_shadowish(ob):
    n = ob.name.lower()
    return _role(ob) == "shadow" or n.endswith(SHADOW_SUFFIXES) or (ob.type == "MESH" and not ob.visible_camera)


def classify(ob, opts):
    """-> "card" | "prop" | None for an object (see the module docstring)."""
    if ob.type != "MESH" or ob.hide_render or ob.hide_viewport:
        return None
    r = _role(ob)
    if r in ("skip", "ground", "shadow"):
        return None
    if _is_shadowish(ob):
        return None
    n = ob.name
    if opts["skip_re"] is not None and opts["skip_re"].search(n):
        return None
    if r == "card":
        return "card"
    if n.lower().endswith("_card"):
        return "card"
    if r == "prop":
        return "prop"
    if opts["include_re"] is not None and opts["include_re"].search(n):
        return "prop"
    if opts["ground_re"].search(n):
        return None
    if opts["prop_re"].search(n):
        return "prop"
    if opts["auto_props"]:
        d = ob.dimensions
        if max(d.x, d.y, d.z) <= opts["max_prop_size"]:
            return "prop"
    return None


# ----------------------------------------------------------------------------- lowest points
def _eval_world_verts(ob, depsgraph, cap=40000):
    ev = ob.evaluated_get(depsgraph)
    try:
        me = ev.to_mesh()
    except Exception:
        me = None
    mw = ev.matrix_world
    if me is not None and len(me.vertices):
        vs = me.vertices
        step = max(1, len(vs) // cap)
        pts = [mw @ vs[i].co for i in range(0, len(vs), step)]
        ev.to_mesh_clear()
        return pts
    if me is not None:
        ev.to_mesh_clear()
    return [mw @ Vector(c) for c in ob.bound_box]


def _spread(points, n=5):
    """up to n points far apart from each other (farthest-point sampling in XY)."""
    if len(points) <= n:
        return list(points)
    chosen = [min(points, key=lambda p: (p.x, p.y))]
    while len(chosen) < n:
        best = max(points, key=lambda p: min((p.x - c.x) ** 2 + (p.y - c.y) ** 2 for c in chosen))
        if min((best.x - c.x) ** 2 + (best.y - c.y) ** 2 for c in chosen) < 1e-10:
            break
        chosen.append(best)
    return chosen


def bbox_contacts(ob, depsgraph):
    pts = _eval_world_verts(ob, depsgraph)
    zmin = min(p.z for p in pts)
    foot = [p for p in pts if p.z <= zmin + FOOT_BAND]
    return _spread(foot), zmin


def _tex_image_node(ob):
    for slot in ob.material_slots:
        m = slot.material
        if m is not None and m.use_nodes and m.node_tree:
            for n in m.node_tree.nodes:
                if n.type == "TEX_IMAGE" and n.image is not None:
                    return n
    return None


_NUM = re.compile(r"(\d+)(?=\D*$)")


def _sprite_path(node, frame):
    img = node.image
    path = bpy.path.abspath(img.filepath)
    if img.source != "SEQUENCE":
        return path
    d, base = os.path.split(path)
    m = _NUM.search(os.path.splitext(base)[0])
    if m is None:
        return path
    iu = node.image_user
    first = int(m.group(1))
    n = first + (int(frame) - iu.frame_start) + iu.frame_offset
    s = str(max(n, 0)).zfill(len(m.group(1)))
    stem, ext = os.path.splitext(base)
    return os.path.join(d, stem[:m.start(1)] + s + stem[m.end(1):] + ext)


def _alpha_of(path):
    if path in _img_cache:
        return _img_cache[path]
    res = None
    if os.path.exists(path):
        try:
            img = bpy.data.images.load(path, check_existing=False)
            w, h = img.size
            buf = array.array("f", [0.0]) * (w * h * 4)
            img.pixels.foreach_get(buf)
            res = (img, w, h, buf[3::4])
        except Exception:
            res = None
    _img_cache[path] = res
    return res


def _uv_affine(ob):
    """world position of a (u, v) on the card's mesh: (origin, du, dv) in object space, from the first loops of the UV map."""
    me = ob.data
    if not me.uv_layers:
        return None
    uv = me.uv_layers.active.data
    pairs = []
    for lp in me.loops:
        pairs.append((Vector(uv[lp.index].uv), me.vertices[lp.vertex_index].co.copy()))
    p0 = pairs[0]
    pa = pb = None
    for p in pairs[1:]:
        if pa is None and (p[0] - p0[0]).length > 1e-6:
            pa = p
        elif pa is not None:
            e1, e2 = pa[0] - p0[0], p[0] - p0[0]
            if abs(e1.x * e2.y - e1.y * e2.x) > 1e-6:
                pb = p
                break
    if pa is None or pb is None:
        return None
    # solve co = c0 + a*(u-u0) + b*(v-v0) from the three samples
    du1, du2 = pa[0] - p0[0], pb[0] - p0[0]
    det = du1.x * du2.y - du1.y * du2.x
    if abs(det) < 1e-12:
        return None
    d1, d2 = pa[1] - p0[1], pb[1] - p0[1]
    a = (d1 * du2.y - d2 * du1.y) / det
    b = (d2 * du1.x - d1 * du2.x) / det
    return p0[0], p0[1], a, b


def card_contacts(ob, depsgraph, frame):
    """(contact points, zmin, how) for a card: the bottom edge of the visible alpha of this frame's sprite; falls back to the bbox."""
    node = _tex_image_node(ob)
    aff = _uv_affine(ob)
    if node is not None and aff is not None:
        got = _alpha_of(_sprite_path(node, frame))
        if got is not None:
            _, w, h, al = got
            row = None
            for r in range(h):
                seg = al[r * w:(r + 1) * w]
                if max(seg) > ALPHA_MIN:
                    row = r
                    break
            if row is not None:
                seg = al[row * w:(row + 1) * w]
                cols = [c for c in range(w) if seg[c] > ALPHA_MIN]
                v = row / float(h)
                us = [(cols[0] + 0.5) / w, (cols[len(cols) // 2] + 0.5) / w, (cols[-1] + 0.5) / w]
                u0, c0, a, b = aff
                mw = ob.evaluated_get(depsgraph).matrix_world
                pts = [mw @ (c0 + a * (u - u0.x) + b * (v - u0.y)) for u in us]
                return pts, min(p.z for p in pts), "alpha"
    pts, z = bbox_contacts(ob, depsgraph)
    return pts, z, "bbox"


# ----------------------------------------------------------------------------- ray casting
def _descendants(ob):
    out = set()
    stack = list(ob.children)
    while stack:
        c = stack.pop()
        if c not in out:
            out.add(c)
            stack.extend(c.children)
    return out


def _ignored_hit(hit, ob, own):
    if hit is None:
        return True
    if hit == ob or hit in own:
        return True
    if _is_shadowish(hit) or _role(hit) == "shadow":
        return True
    if hit.name.lower().endswith("_card") or _role(hit) == "card":     # other people's cards are not floors
        return True
    return False


def cast_down(scene, depsgraph, ob, point, lift=LIFT):
    """first surface below `point` (starting `lift` above it).  The object and its descendants must be hidden from the depsgraph
    by the caller (check_object does it) so a surface that is coplanar with the object's own bottom is still found; hits on
    card/shadow objects are skipped.  -> (hit_z, hit_object) or (None, None)."""
    origin = Vector((point.x, point.y, point.z + lift))
    for _ in range(MAX_SKIPS):
        ok, loc, _n, _i, hit, _m = scene.ray_cast(depsgraph, origin, Vector((0.0, 0.0, -1.0)))
        if not ok:
            return None, None
        if _ignored_hit(hit, ob, ()):
            origin = Vector((loc.x, loc.y, loc.z - 1e-4))
            continue
        return loc.z, hit
    return None, None


class _Hidden(object):
    """context manager: hide `ob` and its descendants from ray casts (hide_viewport + depsgraph update)."""
    def __init__(self, ob):
        self.obs = [ob] + sorted(_descendants(ob), key=lambda o: o.name)
        self.old = []

    def __enter__(self):
        self.old = [(o, o.hide_viewport) for o in self.obs]
        for o in self.obs:
            o.hide_viewport = True
        bpy.context.view_layer.update()
        return bpy.context.evaluated_depsgraph_get()

    def __exit__(self, *exc):
        for o, h in self.old:
            o.hide_viewport = h
        bpy.context.view_layer.update()
        return False


def check_object(scene, depsgraph, ob, kind, frame, gap_tol):
    """one result dict for `ob` on the current frame."""
    if kind == "card":
        pts, zmin, how = card_contacts(ob, depsgraph, frame)
    else:
        pts, zmin = bbox_contacts(ob, depsgraph)
        how = "bbox"
    tol = float(ob["gc_gap"]) if "gc_gap" in ob.keys() else gap_tol
    best = None
    with _Hidden(ob) as dg:
        for p in pts:
            hz, hob = cast_down(scene, dg, ob, p)
            if hz is None:
                continue
            g = p.z - hz
            if best is None or g < best[0]:
                best = (g, hz, hob, p)
    res = dict(obj=ob.name, kind=kind, frame=frame, low=zmin, how=how, tol=tol)
    if best is None:
        res.update(gap=None, hit=None, hit_z=None, point=pts[0] if pts else None, status="FAIL")
    else:
        g, hz, hob, p = best
        res.update(gap=g, hit=hob.name, hit_z=hz, point=p, status="FAIL" if g > tol else "OK")
    return res


# ----------------------------------------------------------------------------- frames, scene sweep
def _sync_stage(scene):
    """re-orient stage actors for the current frame (cards rotate with the camera), if stage/actors.py is loaded."""
    for name in ("actors", "stage.actors", "v3.stage.actors"):
        mod = sys.modules.get(name)
        if mod is not None and hasattr(mod, "sync_all") and getattr(mod, "REGISTRY", None):
            try:
                mod.sync_all(scene, scene.camera)
            except Exception:
                pass
            return


def sample_frames(scene, every=10, frames=None, frame_list=None):
    if frame_list:
        return sorted(set(int(f) for f in frame_list))
    a, b = (scene.frame_start, scene.frame_end) if frames is None else frames
    fs = list(range(int(a), int(b) + 1, max(1, int(every))))
    if fs[-1] != int(b):
        fs.append(int(b))
    return fs


def make_opts(include=None, skip=None, ground=None, auto_props=False, max_prop_size=8.0):
    return dict(
        include_re=re.compile(include, re.I) if include else None,
        skip_re=re.compile(skip, re.I) if skip else None,
        ground_re=re.compile(GROUND_NAMES + (("|" + ground) if ground else ""), re.I),
        prop_re=re.compile(PROP_NAMES, re.I),
        auto_props=bool(auto_props), max_prop_size=float(max_prop_size))


def run_check(scene=None, every=10, gap=0.02, frames=None, frame_list=None, **optkw):
    """sweep the sampled frames; -> (results, skipped_airborne) where results is a list of dicts (see check_object)."""
    scene = scene or bpy.context.scene
    opts = make_opts(**optkw)
    keep = scene.frame_current
    results, air = [], {}
    fl = sample_frames(scene, every, frames, frame_list)
    for f in fl:
        scene.frame_set(f)
        _sync_stage(scene)
        dg = bpy.context.evaluated_depsgraph_get()
        for ob in scene.objects:
            kind = classify(ob, opts)
            if kind is None:
                continue
            if is_airborne(ob, f):
                air.setdefault(ob.name, []).append(f)
                continue
            results.append(check_object(scene, dg, ob, kind, f, gap))
    scene.frame_set(keep)
    return results, air


# ----------------------------------------------------------------------------- --fix
def _anim_has(ob, paths):
    ad = ob.animation_data
    if ad is None or ad.action is None:
        return False
    try:
        fcs = ad.action.fcurves
    except AttributeError:                                   # Blender 5 layered actions
        fcs = []
        try:
            for layer in ad.action.layers:
                for strip in layer.strips:
                    for cb in strip.channelbags:
                        fcs.extend(cb.fcurves)
        except Exception:
            return False
    return any(fc.data_path in paths for fc in fcs)


def mover_of(ob):
    """the object that is moved to fix `ob`: itself or the nearest ancestor with location animation (else `ob`)."""
    o = ob
    while o is not None:
        if _anim_has(o, ("location", "delta_location")):
            return o, True
        o = o.parent
    return ob, False


def _parent_linear(ob):
    if ob.parent is None:
        from mathutils import Matrix
        return Matrix.Identity(3)
    return ob.parent.matrix_world.to_3x3() @ ob.matrix_parent_inverse.to_3x3()


def apply_fix(scene, results, fl, gap_tol=0.02, **optkw):
    """snap failing objects down (see module docstring).  `results` from run_check.  -> list of change dicts."""
    changes = []
    groups = {}
    for r in results:
        if r["status"] != "FAIL" or r["gap"] is None:
            continue
        ob = scene.objects.get(r["obj"])
        if ob is None:
            continue
        mv, animated = mover_of(ob)
        groups.setdefault(mv.name, dict(mover=mv, animated=animated, objs=set(), per_frame={}))
        g = groups[mv.name]
        g["objs"].add(r["obj"])
        dz = r["hit_z"] - r["point"].z                      # negative: down
        cur = g["per_frame"].get(r["frame"])
        g["per_frame"][r["frame"]] = dz if cur is None else max(cur, dz)     # the smallest move wins: never sink another member
    for name, g in groups.items():
        mv = g["mover"]
        if not g["animated"]:
            dz = list(g["per_frame"].values())[0]
            delta = _parent_linear(mv).inverted() @ Vector((0.0, 0.0, dz))
            before = mv.location.copy()
            mv.location += delta
            changes.append(dict(mover=mv.name, objs=sorted(g["objs"]), mode="moved", detail="location %s -> %s" % (
                tuple(round(c, 4) for c in before), tuple(round(c, 4) for c in mv.location))))
            continue
        keep = scene.frame_current
        lin_inv = _parent_linear(mv).inverted()
        cur_delta = {}
        for f in fl:
            scene.frame_set(f)
            cur_delta[f] = mv.delta_location.copy()
        for f in fl:
            dz = g["per_frame"].get(f, 0.0)
            d = cur_delta[f] + (lin_inv @ Vector((0.0, 0.0, dz)))
            mv.delta_location = d
            mv.keyframe_insert("delta_location", frame=f)
        try:
            ad = mv.animation_data
            fcs = ad.action.fcurves if hasattr(ad.action, "fcurves") else []
            for fc in fcs:
                if fc.data_path == "delta_location":
                    for kp in fc.keyframe_points:
                        kp.interpolation = "LINEAR"
        except Exception:
            pass
        scene.frame_set(keep)
        fixed = ", ".join("f%d %+.3f" % (f, dz) for f, dz in sorted(g["per_frame"].items()))
        changes.append(dict(mover=mv.name, objs=sorted(g["objs"]), mode="delta_location keys",
                            detail="Z offset (world units) on %d sampled frames: %s" % (len(g["per_frame"]), fixed)))
    return changes


# ----------------------------------------------------------------------------- contact shadow
_SHADOW_MATS = {}


def _shadow_material(color=(0.05, 0.045, 0.07), opacity=0.55, name="gc_contact_mat"):
    key = (color, round(opacity, 3))
    if key in _SHADOW_MATS and _SHADOW_MATS[key].name in bpy.data.materials:
        return _SHADOW_MATS[key]
    m = bpy.data.materials.new(name)
    m.use_nodes = True
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sub = nt.nodes.new("ShaderNodeVectorMath")
    sub.operation = "SUBTRACT"
    sub.inputs[1].default_value = (0.5, 0.5, 0.0)
    ln = nt.nodes.new("ShaderNodeVectorMath")
    ln.operation = "LENGTH"
    mr = nt.nodes.new("ShaderNodeMapRange")                  # distance 0.5 (rim) -> 0, 0.12 (core) -> opacity, smooth
    mr.interpolation_type = "SMOOTHSTEP"
    mr.inputs["From Min"].default_value = 0.5
    mr.inputs["From Max"].default_value = 0.12
    mr.inputs["To Min"].default_value = 0.0
    mr.inputs["To Max"].default_value = float(opacity)
    emi = nt.nodes.new("ShaderNodeBsdfTransparent")
    dark = nt.nodes.new("ShaderNodeEmission")
    dark.inputs["Color"].default_value = (*color, 1.0)
    dark.inputs["Strength"].default_value = 1.0
    mix = nt.nodes.new("ShaderNodeMixShader")
    nt.links.new(tc.outputs["UV"], sub.inputs[0])
    nt.links.new(sub.outputs["Vector"], ln.inputs[0])
    nt.links.new(ln.outputs["Value"], mr.inputs["Value"])
    nt.links.new(mr.outputs["Result"], mix.inputs["Fac"])
    nt.links.new(emi.outputs["BSDF"], mix.inputs[1])
    nt.links.new(dark.outputs["Emission"], mix.inputs[2])
    nt.links.new(mix.outputs["Shader"], out.inputs["Surface"])
    try:
        m.blend_method = "BLEND"
        m.surface_render_method = "BLENDED"
        m.use_backface_culling = False
    except Exception:
        pass
    try:
        m.cycles.emission_sampling = "NONE"
    except Exception:
        pass
    _SHADOW_MATS[key] = m
    return m


def add_contact_shadow(obj, scene=None, width=None, depth=None, opacity=0.55, color=(0.05, 0.045, 0.07), lift=0.004,
                       frames=None, follow_ground=False, name=None):
    """a soft dark blob plane lying on the ground under a card or prop; its XY follows `obj` (COPY_LOCATION on X and Y only,
    rotation and Z are NOT copied), so it stays under the feet while the object moves or turns.

    width / depth   blob size in units; default: footprint of the object x1.3 (a card: its width x0.9 by 0.45 of that).
    lift            height above the surface (default 4 mm: no z-fighting).
    frames          optional iterable of frames; with follow_ground=True the blob Z is keyed (CONSTANT) on each of them to the
                    surface found under the object, so a walk over steps / a slope keeps the blob on the ground.
    The blob is tagged gc_role = "shadow" (ground_check ignores it, rays pass through it) and cannot cast shadows or bounce
    light; it is a transparent/emission mix, so it darkens whatever is under it in Cycles and EEVEE.
    Returns the blob object (an existing one is returned, not duplicated)."""
    scene = scene or bpy.context.scene
    nm = name or (obj.name + "_gcshadow")
    old = bpy.data.objects.get(nm)
    if old is not None:
        return old
    dg = bpy.context.evaluated_depsgraph_get()
    kind = "card" if obj.name.lower().endswith("_card") or _role(obj) == "card" else "prop"
    pts = _eval_world_verts(obj, dg)
    xs, ys = [p.x for p in pts], [p.y for p in pts]
    cx, cy = (min(xs) + max(xs)) / 2.0, (min(ys) + max(ys)) / 2.0
    ext_x, ext_y = max(xs) - min(xs), max(ys) - min(ys)
    foot = max(ext_x, ext_y)
    if width is None:
        width = foot * 0.9 if kind == "card" else max(ext_x * 1.3, 0.1)
    if depth is None:
        depth = width * 0.45 if kind == "card" else max(ext_y * 1.3, 0.1)
    ctr, zmin = (card_contacts(obj, dg, scene.frame_current)[:2] if kind == "card" else bbox_contacts(obj, dg))
    with _Hidden(obj) as dgh:
        hz, _h = cast_down(scene, dgh, obj, ctr[0] if ctr else Vector((cx, cy, zmin)))
    z0 = (hz if hz is not None else zmin) + lift
    me = bpy.data.meshes.new(nm)
    hw, hd = width / 2.0, depth / 2.0
    me.from_pydata([(-hw, -hd, 0.0), (hw, -hd, 0.0), (hw, hd, 0.0), (-hw, hd, 0.0)], [], [(0, 1, 2, 3)])
    uv = me.uv_layers.new(name="UVMap")
    for i, c in enumerate(((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0))):
        uv.data[i].uv = c
    me.materials.append(_shadow_material(tuple(color), opacity))
    sh = bpy.data.objects.new(nm, me)
    (obj.users_collection[0] if obj.users_collection else scene.collection).objects.link(sh)
    sh["gc_role"] = "shadow"
    mw = obj.matrix_world.translation
    sh.location = (cx - mw.x, cy - mw.y, z0)                 # with use_offset the constraint adds the target's XY to this
    con = sh.constraints.new("COPY_LOCATION")
    con.target = obj
    con.use_x, con.use_y, con.use_z = True, True, False
    con.use_offset = True
    con.target_space = con.owner_space = "WORLD"
    sh.visible_shadow = False
    sh.visible_diffuse = False
    sh.visible_glossy = False
    sh.visible_transmission = False
    sh.hide_select = True
    if follow_ground and frames:
        keep = scene.frame_current
        for f in frames:
            scene.frame_set(int(f))
            _sync_stage(scene)
            dg2 = bpy.context.evaluated_depsgraph_get()
            pts2, z2 = card_contacts(obj, dg2, int(f))[:2] if kind == "card" else bbox_contacts(obj, dg2)
            with _Hidden(obj) as dgh:
                h2, _ = cast_down(scene, dgh, obj, pts2[0]) if pts2 else (None, None)
            if h2 is not None:
                sh.location.z = h2 + lift
                sh.keyframe_insert("location", index=2, frame=int(f))
        if sh.animation_data and sh.animation_data.action:
            try:
                for fc in sh.animation_data.action.fcurves:
                    for kp in fc.keyframe_points:
                        kp.interpolation = "CONSTANT"
            except Exception:
                pass
        scene.frame_set(keep)
    return sh


def add_contact_shadows(scene=None, **optkw):
    """add_contact_shadow() for every card and non-airborne prop the checker would look at; -> list of blobs."""
    scene = scene or bpy.context.scene
    opts = make_opts(**{k: v for k, v in optkw.items() if k in ("include", "skip", "ground", "auto_props", "max_prop_size")})
    out = []
    for ob in list(scene.objects):
        k = classify(ob, opts)
        if k and not is_airborne(ob, scene.frame_current):
            out.append(add_contact_shadow(ob, scene))
    return out


# ----------------------------------------------------------------------------- report
def _fmt_gap(r):
    return "NO SURFACE" if r["gap"] is None else "%+.4f" % r["gap"]


def write_report(path, results, air, args_line, scene, gap, fl, changes=None, before=None, fails_only=False):
    fails = [r for r in results if r["status"] == "FAIL"]
    objs = sorted(set(r["obj"] for r in results))
    bad = sorted(set(r["obj"] for r in fails))
    L = []
    L.append("# GROUND.md -- ground check")
    L.append("")
    L.append("- scene: `%s`   file: `%s`" % (scene.name, os.path.basename(bpy.data.filepath) or "(unsaved)"))
    L.append("- frames sampled: %d (%s%s)   tolerance: gap > %.3f units FAILS   rays: straight down from the lowest contact point(s)" % (
        len(fl), ", ".join(str(f) for f in fl[:12]), " ..." if len(fl) > 12 else "", gap))
    L.append("- checked objects: %d   rows: %d   FAIL rows: %d   **result: %s**" % (
        len(objs), len(results), len(fails), "FAIL (%d objects)" % len(bad) if fails else "PASS"))
    L.append("- command: `%s`" % args_line)
    L.append("")
    if bad:
        L.append("## Failing objects")
        L.append("")
        L.append("| object | kind | failing frames | worst gap |")
        L.append("|---|---|---|---|")
        for o in bad:
            rr = [r for r in fails if r["obj"] == o]
            worst = "NO SURFACE" if any(r["gap"] is None for r in rr) else "%.4f" % max(r["gap"] for r in rr)
            L.append("| %s | %s | %s | %s |" % (o, rr[0]["kind"], ", ".join(str(r["frame"]) for r in rr), worst))
        L.append("")
    if changes is not None:
        L.append("## --fix: changes made")
        L.append("")
        if not changes:
            L.append("nothing to fix.")
        for c in changes:
            L.append("- `%s` (%s) for %s: %s" % (c["mover"], c["mode"], ", ".join("`%s`" % o for o in c["objs"]), c["detail"]))
        if before is not None:
            L.append("")
            L.append("Before the fix: %d FAIL rows (%d objects).  After the fix (table below): %d FAIL rows." % (
                len([r for r in before if r["status"] == "FAIL"]), len(set(r["obj"] for r in before if r["status"] == "FAIL")), len(fails)))
        L.append("")
    if air:
        L.append("## Skipped as airborne")
        L.append("")
        for o, f in sorted(air.items()):
            L.append("- `%s` on frames %s" % (o, ", ".join(str(x) for x in f)))
        L.append("")
    L.append("## All rows" if not fails_only else "## Failing rows")
    L.append("")
    L.append("| object | frame | gap | status | kind/how | lowest z | surface under it |")
    L.append("|---|---|---|---|---|---|---|")
    for r in sorted(results, key=lambda r: (r["status"] != "FAIL", r["obj"], r["frame"])):
        if fails_only and r["status"] == "OK":
            continue
        L.append("| %s | %d | %s | %s | %s/%s | %.3f | %s |" % (
            r["obj"], r["frame"], _fmt_gap(r), r["status"], r["kind"], r["how"], r["low"], r["hit"] or "-"))
    L.append("")
    with open(path, "w") as fh:
        fh.write("\n".join(L))
    return len(fails)


# ----------------------------------------------------------------------------- CLI
def _parse(argv):
    import argparse
    p = argparse.ArgumentParser(prog="ground_check", description="Ray-cast cards and props down; fail when they float.")
    p.add_argument("--every", type=int, default=10)
    p.add_argument("--frames")
    p.add_argument("--frame-list")
    p.add_argument("--gap", type=float, default=0.02)
    p.add_argument("--out", default="GROUND.md")
    p.add_argument("--fails-only", action="store_true")
    p.add_argument("--fix", action="store_true")
    p.add_argument("--save")
    p.add_argument("--setup")
    p.add_argument("--include")
    p.add_argument("--skip")
    p.add_argument("--ground")
    p.add_argument("--auto-props", action="store_true")
    p.add_argument("--max-prop-size", type=float, default=8.0)
    return p.parse_args(argv)


def run_cli(argv=None):
    if argv is None:
        argv = sys.argv[sys.argv.index("--") + 1:] if "--" in sys.argv else []
    a = _parse(argv)
    if a.setup:
        import runpy
        runpy.run_path(os.path.abspath(a.setup), run_name="gc_setup")
    scene = bpy.context.scene
    fr = None
    if a.frames:
        x, _, y = a.frames.partition(":")
        fr = (int(x), int(y or x))
    fl_list = [int(x) for x in a.frame_list.split(",")] if a.frame_list else None
    kw = dict(include=a.include, skip=a.skip, ground=a.ground, auto_props=a.auto_props, max_prop_size=a.max_prop_size)
    fl = sample_frames(scene, a.every, fr, fl_list)
    results, air = run_check(scene, a.every, a.gap, fr, fl_list, **kw)
    changes = before = None
    if a.fix:
        before = results
        changes = apply_fix(scene, results, fl, a.gap)
        results, air = run_check(scene, a.every, a.gap, fr, fl_list, **kw)
        if a.save:
            bpy.ops.wm.save_as_mainfile(filepath=os.path.abspath(a.save))
    line = "blender -b ... --python ground_check.py -- " + " ".join(argv)
    n = write_report(a.out, results, air, line, scene, a.gap, fl, changes, before, a.fails_only)
    print("ground_check: %d objects, %d rows, %d FAIL -> %s" % (len(set(r["obj"] for r in results)), len(results), n, a.out))
    return 1 if n else 0


if __name__ == "__main__":
    sys.exit(run_cli())
