"""blender_card.py -- icons as EMISSION-ONLY cards inside the lit 3D world (bpy 5.3, Cycles).

    import bpy, blender_card as BC
    from anim import Cue
    cue = Cue(g_in=20, hold=40)
    seq = BC.bake(name="rings", icon="sound_rings", kw={"mode": "arcs"}, cue=cue, out_dir="/abs/tex", px=256)
    ob = BC.add_card(seq, height=1.2, location=(0, 0, 2.6), facing="camera", camera=scene.camera)
    BC.key_pop(ob, cue)                      # scale / roll / hide keyed per frame (CONSTANT), Blender frame = g + 1

`bake` writes the icon's own animation (rings growing, stopwatch sweeping...) as a PNG per Blender frame, WITHOUT the
pop (the pop is the card's object scale, so the texture keeps its full resolution through the overshoot).  A static
icon (animated=False) is one PNG.  The texture is an image SEQUENCE: Cycles reads a different file each frame, so the
stale-texture trap of v3/stage/REVIEW.md (same path rewritten while persistent data is on) cannot happen.

The card material is Emission (strength 1) mixed with Transparent by the PNG alpha, emission_sampling NONE: never lit,
never tinted, lights nothing.  By default the card is visible to camera rays only (no shadow, no bounce, no reflection
in the wet road); pass reflect=True to let the glossy road mirror it.  It still gets the camera's depth of field and
motion blur, as the reference's world-anchored labels and X marks do.

facing: "camera"  -- parallel to the image plane (Copy Rotation from the camera), a screen-facing sign in depth;
        "flat"    -- lying on the ground, +Z up, turned by `yaw` (the reference's measuring tape);
        "fixed"   -- the `rotation` you give (Euler, radians), e.g. stuck on a car door.
"""
import math, os

import bpy

import icons as I
import raster
from anim import pop_state


def _hex_lin(h):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c) + (1.0,)


class Baked(object):
    def __init__(self, name, files, first_frame, w_px, h_px, anchor_px, px):
        self.name, self.files, self.first_frame = name, files, first_frame
        self.w_px, self.h_px, self.anchor_px, self.px = w_px, h_px, anchor_px, px


def bake(name, icon, kw=None, cue=None, out_dir=".", px=256, animated=True, frame_offset=1, pad=0.25, t_static=None):
    """rasterise the icon for every frame of the cue (Blender frame = g + frame_offset).  Returns Baked."""
    kw = kw or {}
    os.makedirs(out_dir, exist_ok=True)
    frames = list(cue.frames()) if (animated and cue is not None) else [None]
    jobs, files = [], []
    for g in frames:
        t = pop_state(cue, g).t if g is not None else (t_static if t_static is not None else 1.0)
        ic = I.make(icon, max(t, 0.0), **kw)
        svg, W, H, anc = I.to_svg(ic, px, pad=pad, name=icon)
        fn = os.path.join(out_dir, "%s_%04d.png" % (name, (g + frame_offset) if g is not None else 1))
        jobs.append({"svg": svg, "w": W, "h": H, "out": fn})
        files.append(fn)
    raster.render(jobs)
    if len(files) > 1:
        # Blender asks for frame (first - 1) while the card is still hidden before its cue: give it the first drawing
        import shutil
        shutil.copyfile(files[0], os.path.join(out_dir, "%s_%04d.png" % (name, frames[0] + frame_offset - 1)))
    ic0 = I.make(icon, 0.0, **kw)
    W, H, m = I.canvas_size(ic0, px, pad)
    anc = ((m + ic0.anchor[0]) * px / 100.0, (m + ic0.anchor[1]) * px / 100.0)
    first = (frames[0] + frame_offset) if frames[0] is not None else None
    return Baked(name, files, first, W, H, anc, px)


def card_material(name, image, strength=1.0, interpolation="Cubic"):
    m = bpy.data.materials.new(name)
    nt = m.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    L = nt.links.new
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.image = image
    tex.interpolation = interpolation
    tex.extension = "CLIP"
    emi = nt.nodes.new("ShaderNodeEmission")
    emi.inputs["Strength"].default_value = strength
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader")
    L(tex.outputs["Color"], emi.inputs["Color"])
    L(tex.outputs["Alpha"], mix.inputs["Fac"])
    L(tr.outputs["BSDF"], mix.inputs[1])
    L(emi.outputs["Emission"], mix.inputs[2])
    L(mix.outputs["Shader"], out.inputs["Surface"])
    m.cycles.emission_sampling = "NONE"
    try:
        m.surface_render_method = "BLENDED"
    except Exception:
        pass
    return m, tex


def _image(baked):
    img = bpy.data.images.load(baked.files[0], check_existing=False)
    img.alpha_mode = "STRAIGHT"
    img.colorspace_settings.name = "sRGB"
    if len(baked.files) > 1:
        img.source = "SEQUENCE"
    return img


def add_card(baked, height=1.0, location=(0, 0, 0), facing="camera", camera=None, yaw=0.0, rotation=(0, 0, 0),
             reflect=False, strength=1.0, name=None):
    """a quad whose ORIGIN is the icon's anchor; `height` = world size of 100 design units."""
    name = name or ("icon_" + baked.name)
    k = height / float(baked.px)                         # world units per pixel
    ax, ay = baked.anchor_px
    x0, x1 = -ax * k, (baked.w_px - ax) * k
    y0, y1 = -(baked.h_px - ay) * k, ay * k               # image y down -> local +Y up
    me = bpy.data.meshes.new(name)
    me.from_pydata([(x0, y0, 0), (x1, y0, 0), (x1, y1, 0), (x0, y1, 0)], [], [(0, 1, 2, 3)])
    uv = me.uv_layers.new(name="UVMap")
    for li, (u, v) in enumerate([(0, 0), (1, 0), (1, 1), (0, 1)]):
        uv.data[li].uv = (u, v)
    ob = bpy.data.objects.new(name, me)
    bpy.context.scene.collection.objects.link(ob)
    ob.location = location
    img = _image(baked)
    mat, tex = card_material(name + "_mat", img, strength)
    if img.source == "SEQUENCE":
        iu = tex.image_user
        iu.frame_start = baked.first_frame
        iu.frame_offset = baked.first_frame - 1
        iu.frame_duration = len(baked.files)
        iu.use_auto_refresh = True
        iu.use_cyclic = False
    me.materials.append(mat)
    ob.visible_shadow = False
    ob.visible_diffuse = False
    ob.visible_transmission = False
    ob.visible_volume_scatter = False
    ob.visible_glossy = bool(reflect)
    if facing == "camera":
        c = ob.constraints.new("COPY_ROTATION")
        c.target = camera or bpy.context.scene.camera
        c.mix_mode = "BEFORE"                            # the object's own Z rotation (pop kick) rolls in screen space
    elif facing == "flat":
        ob.rotation_euler = (0.0, 0.0, yaw)
    else:
        ob.rotation_euler = rotation
    ob["iconfx"] = baked.name
    ob["iconfx_h100"] = height                           # world size of 100 design units (readability checks)
    return ob


def _key_const(ob, path, frame, index=-1):
    ob.keyframe_insert(path, frame=frame, index=index)


def key_pop(ob, cue, base_scale=1.0, frame_offset=1, roll=True):
    """key scale (pop profile), Z roll (rotation kick) and hide_render for every frame from g_in - 1 to g_end."""
    base_rot = ob.rotation_euler.copy()
    g_last = cue.g_end if cue.pop_out else cue.g_hold + cue.hold
    for g in range(cue.g_in - 1, g_last + 1):
        st = pop_state(cue, g)
        F = g + frame_offset
        s = max(st.scale, 1e-4) * base_scale
        ob.scale = (s, s, s)
        ob.hide_render = not st.visible
        ob.hide_viewport = not st.visible
        if roll:
            ob.rotation_euler = (base_rot[0], base_rot[1], base_rot[2] + math.radians(st.rot_deg))
            _key_const(ob, "rotation_euler", F)
        _key_const(ob, "scale", F)
        _key_const(ob, "hide_render", F)
        _key_const(ob, "hide_viewport", F)
    ad = ob.animation_data
    if ad and ad.action:
        for fc in _fcurves(ad):
            for kp in fc.keyframe_points:
                kp.interpolation = "CONSTANT"
    return ob


def _fcurves(ad):
    act = ad.action
    if hasattr(act, "fcurves"):
        try:
            return list(act.fcurves)
        except Exception:
            pass
    out = []                                             # layered actions (Blender 4.4+)
    for layer in getattr(act, "layers", []):
        for strip in layer.strips:
            for cb in strip.channelbags:
                out += list(cb.fcurves)
    return out


def _res(scene, w, h):
    """the output size: the scene's own resolution unless w, h are given (they used to default to 720x1280, which
    put 16:9 overlays in the wrong place)."""
    if w is None or h is None:
        r = scene.render
        w, h = r.resolution_x, r.resolution_y           # full-size pixels, before resolution_percentage
    return w, h


def project(scene, cam, xyz, w=None, h=None):
    """pixel (x, y from the top) of world point xyz in a w x h frame (default: the scene's resolution_x/_y) and its
    camera depth -- for a screen overlay that follows a 3D point."""
    from bpy_extras.object_utils import world_to_camera_view
    import mathutils
    w, h = _res(scene, w, h)
    co = world_to_camera_view(scene, cam, mathutils.Vector(xyz))
    return co.x * w, (1.0 - co.y) * h, co.z


# ---- phone readability -----------------------------------------------------------------------------------------------
# At 720 px wide the frame is shown about 390 pt wide on a phone (x 0.54).  The reference's X marks are about
# 90-110 px tall on 720x1280, its check about 140 px.  Below these sizes a symbol stops reading on a phone.
MIN_PX = {"symbol": 64, "text_cap": 22}             # pixels of a 720-wide (9:16) or 720-high (16:9) frame


def _short_side(scene, w=None, h=None):
    w, h = _res(scene, w, h)
    return float(min(w, h))


def height_for_px(scene, cam, location, px, w=None, h=None):
    """the add_card `height` (world size of 100 design units) that makes 100 design units `px` pixels tall on a
    720-short-side frame when the card is at `location` (camera-facing).  Use it to size world cards for the phone."""
    import mathutils
    w, h = _res(scene, w, h)
    loc = mathutils.Vector(location)
    up = cam.matrix_world.to_3x3() @ mathutils.Vector((0, 1, 0))
    a = project(scene, cam, loc, w, h)
    b = project(scene, cam, loc + up, w, h)
    ppm = math.hypot(a[0] - b[0], a[1] - b[1]) * 720.0 / _short_side(scene, w, h)     # px per metre
    return px / max(ppm, 1e-6)


def card_px(ob, scene, cam, w=None, h=None):
    """on-screen height in pixels (on a 720-short-side frame) of 100 design units of a card at the current frame."""
    import mathutils
    w, h = _res(scene, w, h)
    k = ob.get("iconfx_h100", 1.0) * ob.matrix_world.to_scale()[1]
    loc = ob.matrix_world.translation
    up = cam.matrix_world.to_3x3() @ mathutils.Vector((0, 1, 0))
    a = project(scene, cam, loc, w, h)
    b = project(scene, cam, loc + up * k, w, h)
    return math.hypot(a[0] - b[0], a[1] - b[1]) * 720.0 / _short_side(scene, w, h)


def readability_report(scene, cam, cards, frames, min_px=None):
    """cards: [(object, kind)] with kind "symbol" or "text_cap" (for a label, pass its 100-unit height scaled to
    the cap height: see API.md).  Returns [(name, frame, px)] for every visible frame where a card is too small."""
    bad = []
    for F in frames:
        scene.frame_set(F)
        for ob, kind in cards:
            if ob.hide_render:
                continue
            lim = (min_px or MIN_PX)[kind]
            px = card_px(ob, scene, cam) * (ob.get("iconfx_cap", 1.0) if kind == "text_cap" else 1.0)
            if ob.matrix_world.to_scale()[1] < 0.99:      # mid-pop frames are meant to be small
                continue
            if px < lim:
                bad.append((ob.name, F, round(px, 1)))
    return bad
