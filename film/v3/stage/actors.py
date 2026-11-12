"""actors.py -- the v2 puppets as flat cards in the Blender scene (bpy 5.3, Cycles).

    hero = Actor("hero", "hero")
    hero.build(sprites.DEFAULT_CANVAS["hero"], "/abs/sprites")      # card + shadow proxy + (optional) contact decal
    hero.place(1, (-0.8, -0.6, 0.0))                                 # feet on the floor point, keyed
    pose, info = hero.pose(1, {...}, hands={"r": {"tip": (0.4, 0.0, 3.1), "prop": "pencil", "angle": -55}}, camera=cam)
    hero.render_sprites(256)                                         # one PNG per posed frame: <sprite_dir>/hero_0001.png

Objects made by build() (all children of one empty at the feet, "<name>_root", which carries the keyed position and scale):
    <name>_card     the visible card.  Emission only: never lit, tinted or shadowed.  Alpha from the sprite.
    <name>_shadow   shadow proxy: the same sprite on a second card that is seen by shadow rays ONLY.  Above the hips it
                    is turned toward the key light, so the cast shadow is a full figure for every light and does not move
                    when the camera does; at the ankles it lies exactly in the visible card (a twist over the legs), so
                    the shadow starts AT the drawn feet.  (shadow="card": the visible card casts the shadow itself;
                    shadow=None: no cast shadow.)
    <name>_contact  optional soft contact ellipse lying on the floor (a multiplying decal).

Card orientation (decided by test, see API.md "Card orientation"): the card is VERTICAL and only yaws; its width axis is
the camera's horizontal right axis, so it is parallel to the image plane left-to-right and upright in the world.  A low
camera therefore sees the legs nearer than the head and longer (a/t16.0), a high camera sees the head nearer and the body
foreshortened (a/t58.5), and the soles sit exactly on the floor line for every camera.  `tilt` (0 = vertical, 1 = parallel
to the image plane) and `max_slant` (the card starts to lean back only when the view axis is steeper than this, for
top-down shots) can be set per actor.

Coordinates: puppet-local = head centre (0, 0), x right, y DOWN, D units (what puppet.figure and the hand targets use);
card = puppet-local minus the feet point; world = root + scale * (card.x * X_card - card.y * Z_card).
"""
import math, os, sys
import bpy
from mathutils import Matrix, Vector

HERE = os.path.dirname(os.path.abspath(__file__))
try:                                                            # "from stage import actors" (v3 on sys.path) ...
    from . import camrig, sprites
except ImportError:                                             # ... or "import actors" (v3/stage on sys.path)
    if HERE not in sys.path:
        sys.path.insert(0, HERE)
    import camrig                                               # noqa: E402
    import sprites                                              # noqa: E402

TILT_DEFAULT = 0.0          # vertical card that only yaws (see API.md)
MAX_SLANT_DEFAULT = 50.0    # degrees between view axis and horizon above which the card leans to keep facing the lens
SHADOW_MAX_ANGLE = 40.0     # degrees: the shadow proxy turns toward the light until the light is at most this far off its normal
SHADOW_TWIST = (0.12, None)  # D above the feet: below the first height the shadow proxy lies in the visible card (the shadow
                            # is attached to the drawn feet), above the second it faces the light; None = 0.9 x the standing
                            # hip height of the cast.  Actor.shadow_twist = None gives the rigid proxy of the first version.
ALPHA_GAMMA = 1.0           # exponent on the sprite alpha (1 = linear-light blend of the silhouette edge)
DEPTH_STEP = 0.0025         # D: every actor's card sits this much farther along its depth axis than the previous actor's,
                            # so two cards are never coplanar (coplanar transparent cards hide each other in Cycles)

REGISTRY = []               # every Actor built in this process (render.render_frames syncs them)


# ----------------------------------------------------------------------------- helpers
def _clean(mat):
    nt = mat.node_tree
    for n in list(nt.nodes):
        nt.nodes.remove(n)
    return nt


def _quad(name, x0, z0, x1, z1):
    """vertical quad in the local XZ plane (normal -Y, toward a camera that looks along +Y), UV 0..1."""
    me = bpy.data.meshes.new(name)
    me.from_pydata([(x0, 0.0, z0), (x1, 0.0, z0), (x1, 0.0, z1), (x0, 0.0, z1)], [], [(0, 1, 2, 3)])
    uv = me.uv_layers.new(name="UVMap")
    for i, c in enumerate(((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0))):
        uv.data[i].uv = c
    me.update()
    return me


def _grid(name, x0, z0, x1, z1, zs, nx=4):
    """the same quad as _quad, cut into rows at the heights `zs` (ascending, from z0 to z1) and nx columns, so that the
    twist modifier of the shadow proxy has something to bend.  UV 0..1 as _quad."""
    me = bpy.data.meshes.new(name)
    xs = [x0 + (x1 - x0) * i / float(nx) for i in range(nx + 1)]
    verts = [(x, 0.0, z) for z in zs for x in xs]
    faces = []
    for j in range(len(zs) - 1):
        for i in range(nx):
            a = j * (nx + 1) + i
            faces.append((a, a + 1, a + nx + 2, a + nx + 1))
    me.from_pydata(verts, [], faces)
    uv = me.uv_layers.new(name="UVMap")
    for lp in me.loops:
        v = me.vertices[lp.vertex_index].co
        uv.data[lp.index].uv = ((v.x - x0) / (x1 - x0), (v.z - z0) / (z1 - z0))
    me.update()
    return me


def _wrap(a):
    """angle wrapped to -pi .. pi"""
    return (a + math.pi) % (2.0 * math.pi) - math.pi


def _key_const(owner, struct, path, frame):
    """insert a key for struct.path (struct = the object or one of its modifiers) and make that key CONSTANT."""
    struct.keyframe_insert(path, frame=frame)
    for fc in camrig.fcurves_of(owner):
        if fc.data_path == path or fc.data_path.endswith("." + path):
            for kp in fc.keyframe_points:
                if abs(kp.co.x - frame) < 0.5:
                    kp.interpolation = "CONSTANT"


def _drop_render_cache(scene):
    """free Cycles' persistent render data of `scene` (it is rebuilt by the next render); see Actor.reload_sprites."""
    r = scene.render
    if r.use_persistent_data:
        r.use_persistent_data = False
        r.use_persistent_data = True


def card_material(name, image=None, interpolation="Cubic", alpha_gamma=ALPHA_GAMMA):
    """Emission (strength 1, colour = the sprite) mixed with Transparent by the sprite alpha.  No BSDF: the scene's
    lights, ambient and shadows cannot change it; emission_sampling NONE: it lights nothing.  Returns (material, tex node)."""
    m = bpy.data.materials.new(name)
    nt = _clean(m)
    L = nt.links.new
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    tex = nt.nodes.new("ShaderNodeTexImage")
    tex.interpolation = interpolation            # 'Cubic' or 'Linear'
    tex.extension = "CLIP"
    if image is not None:
        tex.image = image
    emi = nt.nodes.new("ShaderNodeEmission")
    emi.inputs["Strength"].default_value = 1.0
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    mix = nt.nodes.new("ShaderNodeMixShader")
    L(tex.outputs["Color"], emi.inputs["Color"])            # straight (un-premultiplied) colour: Mix Shader is the "over"
    if abs(alpha_gamma - 1.0) > 1e-6:
        pw = nt.nodes.new("ShaderNodeMath")
        pw.operation = "POWER"
        pw.inputs[1].default_value = alpha_gamma
        L(tex.outputs["Alpha"], pw.inputs[0])
        L(pw.outputs[0], mix.inputs["Fac"])
    else:
        L(tex.outputs["Alpha"], mix.inputs["Fac"])
    L(tr.outputs["BSDF"], mix.inputs[1])
    L(emi.outputs["Emission"], mix.inputs[2])
    L(mix.outputs["Shader"], out.inputs["Surface"])
    m.cycles.emission_sampling = "NONE"
    return m, tex


def contact_material(name, color="#252432", opacity=0.5):
    """multiplying decal: Transparent BSDF whose colour falls from `color` (mixed in by `opacity`) at the centre to white
    at the rim of the quad, so it darkens whatever floor is under it."""
    m = bpy.data.materials.new(name)
    nt = _clean(m)
    L = nt.links.new
    out = nt.nodes.new("ShaderNodeOutputMaterial")
    tc = nt.nodes.new("ShaderNodeTexCoord")
    sub = nt.nodes.new("ShaderNodeVectorMath")
    sub.operation = "SUBTRACT"
    sub.inputs[1].default_value = (0.5, 0.5, 0.0)
    ln = nt.nodes.new("ShaderNodeVectorMath")
    ln.operation = "LENGTH"
    mr = nt.nodes.new("ShaderNodeMapRange")
    mr.interpolation_type = "SMOOTHSTEP"
    mr.inputs["From Min"].default_value = 0.5
    mr.inputs["From Max"].default_value = 0.16
    mr.inputs["To Min"].default_value = 0.0
    mr.inputs["To Max"].default_value = float(opacity)
    mixc = nt.nodes.new("ShaderNodeMix")
    mixc.data_type = "RGBA"
    mixc.blend_type = "MIX"
    mixc.inputs[6].default_value = (1.0, 1.0, 1.0, 1.0)
    mixc.inputs[7].default_value = (*_hex_lin(color), 1.0)
    tr = nt.nodes.new("ShaderNodeBsdfTransparent")
    L(tc.outputs["UV"], sub.inputs[0])
    L(sub.outputs["Vector"], ln.inputs[0])
    L(ln.outputs["Value"], mr.inputs["Value"])
    L(mr.outputs["Result"], mixc.inputs[0])
    L(mixc.outputs[2], tr.inputs["Color"])
    L(tr.outputs["BSDF"], out.inputs["Surface"])
    m.cycles.emission_sampling = "NONE"
    return m


def _hex_lin(h):
    h = h.lstrip("#")
    c = [int(h[i:i + 2], 16) / 255.0 for i in (0, 2, 4)]
    return tuple(x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4 for x in c)


def _only_shadow(ob):
    ob.visible_camera = False
    ob.visible_diffuse = False
    ob.visible_glossy = False
    ob.visible_transmission = False
    ob.visible_volume_scatter = False
    ob.visible_shadow = True


def _camera_axes(camera):
    m = camera.matrix_world
    r = Vector((m[0][0], m[1][0], m[2][0]))
    u = Vector((m[0][1], m[1][1], m[2][1]))
    f = -Vector((m[0][2], m[1][2], m[2][2]))
    return m.to_translation(), r.normalized(), u.normalized(), f.normalized()


# ----------------------------------------------------------------------------- the actor
class Actor(object):
    """one puppet on a card.  name: unique object-name prefix and sprite file prefix; cast: "hero" | "boss"."""

    def __init__(self, name, cast, tilt=TILT_DEFAULT, max_slant=MAX_SLANT_DEFAULT):
        self.name = name
        self.cast = cast
        self.tilt = float(tilt)              # 0 = vertical card that only yaws, 1 = parallel to the image plane
        self.max_slant = float(max_slant)    # deg; steeper views tilt the card by the excess (top-down shots)
        self.yaw_fixed = None                # deg about Z: ignore the camera and keep this yaw (0 = parallel to the map wall)
        self.shadow_max_angle = SHADOW_MAX_ANGLE
        self.shadow_light = None             # light object the proxy turns toward (default: first SUN in the scene, else
                                             # the strongest other light)
        self.shadow_twist = SHADOW_TWIST     # (h0, h1) in D above the feet, see SHADOW_TWIST; None = rigid proxy
        self._twist = None                   # the proxy's twist modifier
        self._mesh_zone = "unset"            # twist zone the proxy mesh was cut for
        self._sig = {}                       # frame -> (inode, mtime, size) of the sprite file last shown on that frame
        self._baked = False                  # bake_facing() was called: sync() keeps its keys up to date
        self.canvas = None
        self.sprite_dir = None
        self.pattern = None
        self.root = self.card = self.proxy = self.contact = None
        self.material = None
        self.tex = None
        self.image = None
        self.round_head = True               # Actor.pose() stretches the upper body so that the head is round on screen
        self.head_flip = False               # True: sprites are drawn with the head disc mirrored (thick ink side and
                                             # crescent at the lower LEFT) for a key light from screen-right; or a dict /
                                             # callable frame -> bool for a per-frame choice
        self.poses = {}                      # frame -> solved pose
        self.upper_k = {}                    # frame -> upper-body stretch the sprite of that frame is drawn with
        self.feet = {}                       # frame -> (x, feet_y) of the feet point in puppet-local D
        self.flips = {}                      # frame -> bool (from place)
        self.scene = None
        self._default_feet = None
        self.depth_bias = 0.0                # set by build(): DEPTH_STEP x (number of actors built before this one)

    # ------------------------------------------------------------------ build
    def build(self, canvas, sprite_dir, scene=None, shadow="proxy", contact=None, interpolation="Cubic",
              pattern=None, alpha_gamma=ALPHA_GAMMA):
        """create the card for a sprite canvas.

        canvas      (x0, y0, x1, y1) relative to the feet, y down, D units: the "canvas" of a render_sprites result (or
                    sprites.DEFAULT_CANVAS[cast] / sprites.canvas_px(...)[2]); the card is exactly this rectangle with
                    its origin at the feet point.
        sprite_dir  directory of the PNG sequence; file of frame f = <sprite_dir>/<name>_%04d.png (`pattern` overrides,
                    it must contain one %d field).  Frame numbers are Blender frame numbers and must be >= 1.
        shadow      "proxy" (default) | "card" | None
        contact     None, True (0.9 D wide, 0.42 D deep, #252432 at 0.5) or dict(width=, depth=, color=, opacity=)
        interpolation  "Cubic" (default) or "Linear" texture filtering
        Returns the card object.  The sprite files may be rendered after build(); the image is attached on first sync."""
        scene = scene or bpy.context.scene
        self.scene = scene
        self.canvas = tuple(float(v) for v in canvas)
        self.sprite_dir = os.path.abspath(sprite_dir)
        self.pattern = pattern or (self.name + "_%04d.png")
        x0, y0, x1, y1 = self.canvas
        col = scene.collection
        root = bpy.data.objects.new(self.name + "_root", None)
        root.empty_display_size = 0.2
        col.objects.link(root)
        self.root = root
        self.material, self.tex = card_material(self.name + "_mat", None, interpolation, alpha_gamma)
        iu = self.tex.image_user
        iu.frame_start = 1
        iu.frame_offset = 0
        iu.frame_duration = 1000000
        iu.use_auto_refresh = True
        iu.use_cyclic = False
        card = bpy.data.objects.new(self.name + "_card", _quad(self.name + "_card", x0, -y1, x1, -y0))
        card.data.materials.append(self.material)
        card.parent = root
        card.rotation_mode = "XYZ"
        col.objects.link(card)
        card.visible_shadow = (shadow == "card")
        card.visible_diffuse = False          # the card never lights or bounces onto the set
        self.card = card
        if shadow == "proxy":
            px = bpy.data.objects.new(self.name + "_shadow", _quad(self.name + "_shadow", x0, -y1, x1, -y0))
            px.data.materials.append(self.material)
            px.parent = root
            px.rotation_mode = "XYZ"
            col.objects.link(px)
            _only_shadow(px)
            tw = px.modifiers.new("feet_twist", "SIMPLE_DEFORM")        # twist about the vertical through the feet point
            tw.deform_method = "TWIST"
            tw.deform_axis = "Z"
            tw.angle = 0.0
            self._twist = tw
            self.proxy = px
            self._fit_proxy_mesh(self._twist_zone())
        if contact:
            c = dict(width=0.9, depth=0.42, color="#252432", opacity=0.5)
            if isinstance(contact, dict):
                c.update(contact)
            me = bpy.data.meshes.new(self.name + "_contact")
            hw, hd = c["width"] / 2.0, c["depth"] / 2.0
            me.from_pydata([(-hw, -hd, 0.0), (hw, -hd, 0.0), (hw, hd, 0.0), (-hw, hd, 0.0)], [], [(0, 1, 2, 3)])
            uv = me.uv_layers.new(name="UVMap")
            for i, t in enumerate(((0.0, 0.0), (1.0, 0.0), (1.0, 1.0), (0.0, 1.0))):
                uv.data[i].uv = t
            dc = bpy.data.objects.new(self.name + "_contact", me)
            dc.data.materials.append(contact_material(self.name + "_contact_mat", c["color"], c["opacity"]))
            dc.parent = root
            dc.location = (0.0, 0.0, 0.004)
            dc.rotation_mode = "XYZ"
            dc.visible_shadow = False
            dc.visible_diffuse = False
            dc.visible_glossy = False
            col.objects.link(dc)
            self.contact = dc
        self._default_feet = sprites.feet_of(self.cast, {})
        if self not in REGISTRY:
            REGISTRY.append(self)
        idx = REGISTRY.index(self)
        self.depth_bias = DEPTH_STEP * idx
        if self.proxy is not None:
            self.proxy.location = (0.0, 0.0, 0.0)
        if self.contact is not None:
            self.contact.location = (0.0, 0.0, 0.004 + 0.0007 * idx)
        self._attach_image()
        return card

    def sprite_path(self, frame):
        return os.path.join(self.sprite_dir, self.pattern % int(frame))

    def _attach_image(self, frame=None):
        """load the PNG sequence as soon as one sprite file exists."""
        if self.image is not None:
            return True
        cand = []
        if frame is not None:
            cand.append(int(frame))
        cand += sorted(self.poses.keys())[:1] + [1]
        for f in cand:
            p = self.sprite_path(f)
            if os.path.exists(p):
                img = bpy.data.images.load(p, check_existing=False)
                img.source = "SEQUENCE"
                img.alpha_mode = "STRAIGHT"
                img.colorspace_settings.name = "sRGB"
                self.image = img
                self.tex.image = img
                return True
        return False

    def reload_sprites(self):
        """make Blender AND Cycles forget every sprite of this actor they hold.  Needed after a sprite file that has
        already been rendered was written again; render_sprites() and sync() notice that by themselves (they compare
        inode, time and size of the files with what was shown) and call this, so you only need it if you render through
        Blender's own animation loop after rewriting files by hand.

        Two caches are emptied: Blender's decoded frames of the image sequence (Image.reload) and Cycles' persistent
        render data.  The second one matters: with persistent data Cycles keeps the pixels of a texture FILE PATH for
        as long as the same frame is rendered again, and neither Image.reload() nor an update tag nor a new image
        datablock makes it read the file again (measured: render f, re-pose f, write the sprite, render f -> the old
        drawing).  Persistent data is therefore switched off and on once, which costs one rebuild of the set's BVH and
        textures on the next frame."""
        self._sig.clear()
        if self.image is None:
            self._attach_image()
            return
        self.image.reload()
        _drop_render_cache(self.scene or bpy.context.scene)

    def _file_sig(self, frame):
        try:
            st = os.stat(self.sprite_path(frame))
        except OSError:
            return None
        return (st.st_ino, st.st_mtime_ns, st.st_size)

    def _refresh_if_changed(self):
        """reload only if a sprite file that was already shown has changed (new frames need nothing)."""
        if self.image is None:
            self._attach_image()
            return False
        for f, old in list(self._sig.items()):
            if self._file_sig(f) != old:
                self.reload_sprites()
                return True
        return False

    def _check_sprite(self, frame):
        """the stale-image guard of sync(): if the PNG of `frame` was replaced since this actor last showed that frame,
        empty the caches (reload_sprites); then remember what is shown now."""
        sig = self._file_sig(frame)
        old = self._sig.get(frame)
        if old is not None and old != sig:
            self.reload_sprites()
        self._sig[frame] = sig

    # ------------------------------------------------------------------ placement
    def place(self, frame, floor_xyz, scale=1.0, flip=False, interp="LINEAR", easing="AUTO"):
        """key the feet point on world `floor_xyz` at `frame` with uniform `scale` (1 = head diameter 1 D).
        flip=True mirrors the figure from this frame on: it is realised by the puppet's own mirror (pose["mirror"], which
        keeps the head disc and its shadow crescent unmirrored) when the sprites are made through Actor.pose(); the card
        itself is never mirrored.  interp / easing shape the move from this key to the next (camrig.key)."""
        camrig.key(self.root, "location", frame, Vector(floor_xyz), interp, easing)
        camrig.key(self.root, "scale", frame, Vector((scale, scale, scale)), interp, easing)
        self.flips[int(frame)] = bool(flip)
        return self

    def flip_at(self, frame):
        ks = [f for f in self.flips if f <= frame]
        return self.flips[max(ks)] if ks else False

    def feet_at(self, frame):
        """(x, feet_y) of the feet point in puppet-local D for the pose stored on `frame` (standing default otherwise)."""
        return self.feet.get(int(frame), self._default_feet)

    # ------------------------------------------------------------------ orientation
    def basis(self, camera):
        """(X, Y, Z) world axes of the card for the camera's CURRENT matrix: X = width (to the right on screen),
        Y = depth (away from the camera), Z = up along the card."""
        _, r, u, f = _camera_axes(camera)
        up = Vector((0.0, 0.0, 1.0))
        if self.yaw_fixed is not None:
            a = math.radians(self.yaw_fixed)
            rh = Vector((math.cos(a), math.sin(a), 0.0))
        else:
            rh = Vector((r.x, r.y, 0.0))
            if rh.length < 1e-5:                    # camera rolled on its side: fall back to the view direction
                fh = Vector((f.x, f.y, 0.0))
                rh = fh.cross(up) if fh.length > 1e-5 else Vector((1.0, 0.0, 0.0))
            rh.normalize()
        h = up.cross(rh)                             # horizontal direction away from the camera
        p = math.asin(max(-1.0, min(1.0, f.z)))      # elevation of the view axis (+ = looking up)
        if f.dot(h) < 0.0 and self.yaw_fixed is None:
            p = math.copysign(math.pi - abs(p), p)   # looking past the vertical (does not happen with roll 0)
        tau = self.tilt * p
        lim = math.radians(self.max_slant)
        if abs(p - tau) > lim:
            tau = p - math.copysign(lim, p - tau)
        y = h * math.cos(tau) + up * math.sin(tau)
        z = up * math.cos(tau) - h * math.sin(tau)
        return rh, y, z

    def _key_light(self, scene):
        """the light the shadow proxy turns toward: shadow_light, else the first visible SUN, else the strongest other
        visible light that casts shadows."""
        if self.shadow_light is not None:
            return self.shadow_light
        best = None
        for ob in scene.objects:
            if ob.type != "LIGHT" or ob.hide_render:
                continue
            if ob.data.type == "SUN":
                return ob
            if getattr(ob.data, "use_shadow", True) and (best is None or ob.data.energy > best.data.energy):
                best = ob
        return best

    def _proxy_yaw(self, scene, card_yaw=0.0):
        """rotation about Z (radians) of the upper part of the shadow proxy: from the stage-front orientation (normal
        toward -Y; the stage-back one when the camera looks from the other side, so the shadow is never the mirror image
        of the figure the camera sees; yaw_fixed when that is set) toward the key light, until the light's horizontal
        direction is at most shadow_max_angle off the proxy normal.  Apart from that front / back choice it does not
        depend on the camera, so the body's shadow does not move in a camera move."""
        lt = self._key_light(scene)
        if self.yaw_fixed is not None:
            base = math.radians(self.yaw_fixed)
        else:
            base = 0.0 if math.cos(card_yaw) >= 0.0 else math.pi
        if lt is None:
            return base
        m = lt.matrix_world
        if lt.data.type == "SUN":
            d = -Vector((m[0][2], m[1][2], m[2][2]))                     # travel direction of the light
        else:
            d = self.root.matrix_world.to_translation() + Vector((0.0, 0.0, 1.5)) - m.to_translation()
        dh = Vector((d.x, d.y, 0.0))
        if dh.length < 1e-5:
            return base
        dh.normalize()
        n = Vector((-math.sin(base), math.cos(base), 0.0))               # proxy depth axis (+Y at yaw 0)
        if dh.dot(n) < 0.0:
            dh = -dh                                                     # the card is two-sided
        ang = math.atan2(n.x * dh.y - n.y * dh.x, n.dot(dh))             # signed angle from n to dh about +Z
        lim = math.radians(self.shadow_max_angle)
        if abs(ang) > lim:
            base += ang - math.copysign(lim, ang)
        return base

    def _fit_proxy_mesh(self, zone):
        """give the proxy the mesh its twist needs: one quad for a rigid proxy, else that quad cut into rows of about
        0.15 D across the twist zone only (every extra row costs shadow-ray time: measured +0.35 s CPU per final frame
        for this layout against +0.95 s for rows over the whole card)."""
        key = None if zone is None else (round(zone[0], 4), round(zone[1], 4))
        if key == self._mesh_zone:
            return
        x0, y0, x1, y1 = self.canvas
        zmin, zmax = -y1, -y0
        if key is None:
            me = _quad(self.name + "_shadow", x0, zmin, x1, zmax)
        else:
            h0, h1 = key
            n = max(2, int(math.ceil((h1 - h0) / 0.15)))
            zs = sorted(set([zmin, zmax] + ([0.0] if zmin < -1e-6 else []) + [h0 + (h1 - h0) * i / float(n) for i in range(n + 1)]))
            zs = [z for i, z in enumerate(zs) if i == 0 or z - zs[i - 1] > 1e-5]
            me = _grid(self.name + "_shadow", x0, zmin, x1, zmax, zs)
        me.materials.append(self.material)
        old = self.proxy.data
        self.proxy.data = me
        if old is not None and old.users == 0:
            bpy.data.meshes.remove(old)
        self._mesh_zone = key

    def _twist_zone(self):
        """(h0, h1, lower limit, upper limit) of the proxy's twist, or None for a rigid proxy.  Heights in D above the
        feet (card units, before the actor's scale); the limits are the modifier's fractions of the proxy's height."""
        if self._twist is None or not self.shadow_twist:
            return None
        h0, h1 = self.shadow_twist
        if h1 is None:
            fig = sprites.puppet.figure(self.cast, {}, "s")
            h1 = 0.9 * (float(fig["feet_y"]) - float(fig["anchors"]["hip"][1]))
        zmin, zmax = -self.canvas[3], -self.canvas[1]
        h0 = max(0.0, float(h0))
        h1 = min(max(float(h1), h0 + 0.05), zmax)
        return h0, h1, (h0 - zmin) / (zmax - zmin), (h1 - zmin) / (zmax - zmin)

    def sync(self, camera=None, scene=None):
        """orient the card (and proxy, decal) for the scene's CURRENT frame.  render.render_frames calls this for every
        actor before each frame; call it yourself after scene.frame_set() if you render another way."""
        scene = scene or self.scene or bpy.context.scene
        camera = camera or scene.camera
        if not self.card.hide_render:
            if not os.path.exists(self.sprite_path(scene.frame_current)):
                raise FileNotFoundError("%s: no sprite for frame %d (%s). Pose every rendered frame with Actor.pose() and "
                                        "call Actor.render_sprites(), or hide the actor with Actor.set_hidden(True)."
                                        % (self.name, scene.frame_current, self.sprite_path(scene.frame_current)))
            self._attach_image(scene.frame_current)
            self._check_sprite(scene.frame_current)
        x, y, z = self.basis(camera)
        self.card.rotation_euler = Matrix((x, y, z)).transposed().to_euler("XYZ")
        self.card.location = y * self.depth_bias              # (the root has no rotation: its axes are the world's)
        yaw = math.atan2(x.y, x.x)
        if self.contact is not None:
            self.contact.rotation_euler = (0.0, 0.0, yaw)
        if self.proxy is not None:
            a = self._proxy_yaw(scene, yaw)                     # orientation of the proxy above the twist zone
            zone = self._twist_zone()
            self._fit_proxy_mesh(zone)                          # (rebuilds the mesh only when shadow_twist was changed)
            if zone is None:
                if self._twist is not None and abs(self._twist.angle) > 1e-7:
                    self._twist.angle = 0.0
                self.proxy.rotation_euler = (0.0, 0.0, a)
            else:
                # twist modifier: a row at height h is turned by clamp(h, h0, h1) * angle / (h1 - h0) about Z.  With
                # this object rotation the rows below h0 lie in the visible card (yaw) and the rows above h1 face the
                # light (a): the shadow is attached to the drawn feet and its body does not follow the camera.
                h0, h1, lo, hi = zone
                d = _wrap(a - yaw)
                if abs(self._twist.limits[0] - lo) > 1e-6 or abs(self._twist.limits[1] - hi) > 1e-6:
                    self._twist.limits = (lo, hi)
                if abs(self._twist.angle - d) > 1e-7:
                    self._twist.angle = d
                self.proxy.rotation_euler = (0.0, 0.0, yaw - h0 * d / (h1 - h0))
            self.proxy.location = (-math.sin(a) * self.depth_bias, math.cos(a) * self.depth_bias, 0.0)
        if self._baked:                                       # keys from bake_facing exist: keep them equal to what was just set
            self._key_facing(scene.frame_current)

    def objects(self):
        """the Blender objects of this actor that render: card, shadow proxy, contact decal (those that exist)."""
        return [o for o in (self.card, self.proxy, self.contact) if o is not None]

    def set_hidden(self, hidden=True):
        """take the actor out of the render (and its shadow and contact decal with it) or bring it back."""
        for o in self.objects():
            o.hide_render = bool(hidden)

    def bake_facing(self, frames, camera=None, scene=None):
        """key everything sync() sets (card rotation and depth offset, shadow proxy rotation, offset and twist, contact
        decal rotation) on every frame of `frames`, CONSTANT, for renders that do not go through render.render_frames
        (e.g. bpy.ops.render.render(animation=True)).  Call it again when the camera, a placement or the light changes."""
        scene = scene or self.scene or bpy.context.scene
        self._baked = True                                    # from now on sync() rewrites the key of the frame it sets
        for f in frames:
            scene.frame_set(int(f))
            self.sync(camera, scene)

    def _key_facing(self, f):
        f = int(f)
        _key_const(self.card, self.card, "rotation_euler", f)
        _key_const(self.card, self.card, "location", f)
        if self.proxy is not None:
            _key_const(self.proxy, self.proxy, "rotation_euler", f)
            _key_const(self.proxy, self.proxy, "location", f)
            if self._twist is not None:
                _key_const(self.proxy, self._twist, "angle", f)
        if self.contact is not None:
            _key_const(self.contact, self.contact, "rotation_euler", f)

    # ------------------------------------------------------------------ poses and sprites
    def pose(self, frame, pose, hands=None, camera=None, upper_k=None):
        """store the pose of `frame`, pin hands to WORLD points and fit the drawing to the camera of that frame.

        hands = {"r": {"tip": (wx, wy, wz), "prop": "pencil", "angle": -55, "stretch": 1.1},   # tip of a held prop
                 "l": {"hand": (wx, wy, wz)}}                                                    # the hand itself
        (2-tuples are taken as puppet-local targets).  "r" / "l" are the pose keys arm_r / arm_l.  The camera and this
        actor's place() keys for `frame` must exist already: a target is where the world point APPEARS on the card from
        the camera of that frame (world_to_local).
        upper_k: upper-body stretch of the sprite (sprites.py).  None = computed from the camera so that the head is round
        on screen although the card is vertical (1.00 at eye level, about 1.08 at the low angle, 1.2 at the high angle);
        pass 1.0 (or set actor.round_head = False) to switch it off.
        Returns (solved pose, info); info[side]["error"] is the arm's miss in D (0 when the target is within reach).
        For a world target info[side] also has "world" (the point on the card that covers the target) and "clearance"
        (D along the line of sight by which that point is in FRONT of the target; negative = the card stands behind the
        target there, so a wall the target lies on hides the tip; a warning is issued)."""
        frame = int(frame)
        p = dict(pose or {})
        if self.flip_at(frame):
            p["mirror"] = True
        feet = sprites.feet_of(self.cast, p)
        self.feet[frame] = feet
        if upper_k is None:
            upper_k = upper_stretch(self, camera, frame, p) if self.round_head else 1.0
        k = round(float(upper_k), 3)
        info = {}
        if hands:
            loc_h, world_t = {}, {}
            for side, h in hands.items():
                h = dict(h)
                for key in ("tip", "hand"):
                    if h.get(key) is not None and len(h[key]) == 3:
                        world_t[side] = Vector(h[key])
                        h[key] = world_to_local(self, camera, h[key], frame, feet=feet)
                loc_h[side] = h
            p, info = sprites.solve_hands(self.cast, p, loc_h, upper_k=k)
            # where the pinned point really is: on the card, in front of (or behind) the world point it covers
            cam_ob = camera or (self.scene or bpy.context.scene).camera
            for side, wp in world_t.items():
                if side not in info:
                    continue
                c = cam_ob.matrix_world.to_translation()
                hit = local_to_world(self, info[side]["target"], frame, feet, camera)
                info[side]["world"] = tuple(hit)
                info[side]["clearance"] = (wp - c).length - (hit - c).length
                if info[side]["clearance"] < 0.0:
                    import warnings
                    warnings.warn("%s: a pinned hand target lies in front of its card (info[side]['clearance'] < 0): the surface "
                                  "the target is on will hide the hand or the prop tip. Move the actor away from that surface, "
                                  "turn the camera less, or set actor.yaw_fixed." % self.name, stacklevel=2)
        self.poses[frame] = p
        self.upper_k[frame] = k
        return p, info

    def jobs(self, px_per_D, frames=None, overlay=None):
        """sprite jobs for the stored poses (all frames, or `frames`).  overlay: SVG fragment or callable(frame, pose)."""
        out = []
        for f in (sorted(self.poses) if frames is None else frames):
            f = int(f)
            hf = self.head_flip
            hf = hf(f) if callable(hf) else (hf.get(f, False) if isinstance(hf, dict) else hf)
            j = dict(cast=self.cast, pose=self.poses[f], px_per_D=px_per_D, out=self.sprite_path(f), canvas=self.canvas,
                     upper_k=self.upper_k.get(f, 1.0), head_flip=bool(hf))
            if overlay is not None:
                j["overlay"] = overlay(f, self.poses[f]) if callable(overlay) else overlay
            out.append(j)
        return out

    def render_sprites(self, px_per_D, frames=None, overlay=None, mode="canvas", verbose=False):
        """rasterise the stored poses to <sprite_dir>/<name>_%04d.png.  If a sprite that was already rendered into a
        frame has changed, Blender's and Cycles' caches are emptied (reload_sprites).  Returns the sprite results
        (sprites.render_sprites).  px_per_D must give the card's canvas a whole number of pixels (multiples of 16 do)."""
        w, h, cv = sprites.canvas_px(self.canvas, px_per_D)
        if max(abs(a - b) for a, b in zip(cv, self.canvas)) > 1e-6:
            raise ValueError("%s: canvas %r is not a whole number of pixels at %g px per D (use sprites.canvas_px)"
                             % (self.name, self.canvas, px_per_D))
        res = sprites.render_sprites(self.jobs(px_per_D, frames, overlay), mode=mode, verbose=verbose)
        self._refresh_if_changed()
        return res


# ----------------------------------------------------------------------------- registration
def _at_frame(scene, frame):
    if frame is not None and scene.frame_current != int(frame):
        scene.frame_set(int(frame))
    bpy.context.view_layer.update()


def card_state(actor, camera, frame=None):
    """(origin, X, Y, Z, scale) of the card on `frame` (world vectors; see Actor.basis).  origin = the feet point on the
    card (the root's position plus the actor's tiny depth bias along Y)."""
    scene = actor.scene or bpy.context.scene
    camera = camera or scene.camera
    _at_frame(scene, frame)
    mw = actor.root.matrix_world
    x, y, z = actor.basis(camera)
    s = mw.to_scale().x
    return mw.to_translation() + y * (actor.depth_bias * s), x, y, z, s


def upper_stretch(actor, camera, frame=None, pose=None, limit=1.6):
    """upper-body stretch that makes the head of `actor` round on screen on `frame`: the ratio of the card's horizontal
    to its vertical on-screen scale at the head centre (1.0 when the card is seen square on).  Clamped to 1 .. limit."""
    from bpy_extras.object_utils import world_to_camera_view
    scene = actor.scene or bpy.context.scene
    camera = camera or scene.camera
    o, x, y, z, s = card_state(actor, camera, frame)
    fig = sprites.puppet.figure(actor.cast, pose or {}, "s")
    fx, fy, yh = float(fig["anchors"]["feet"][0]), float(fig["feet_y"]), float(fig["anchors"]["hip"][1])
    W, H = scene.render.resolution_x, scene.render.resolution_y

    def px(v):
        co = world_to_camera_view(scene, camera, v)
        return Vector((co.x * W, co.y * H))
    k = 1.0
    e = 0.05 * s
    for _ in range(3):
        hy = yh * (1.0 - k)                                  # head centre of the stretched drawing (puppet-local y)
        c = o + x * ((0.0 - fx) * s) - z * ((hy - fy) * s)
        sx = (px(c + x * e) - px(c - x * e)).length
        sy = (px(c + z * e) - px(c - z * e)).length
        k = max(1.0, min(limit, sx / max(sy, 1e-9)))
    return k


def world_to_local(actor, camera, world_point, frame=None, feet=None):
    """Puppet-local D coordinates (head centre origin, y down) at which `world_point` APPEARS on the actor's card as seen
    from `camera` on `frame`: the ray from the lens through the world point is cut with the card plane.  Give a hand or a
    prop tip this target and it covers the world point exactly, whatever the camera does (the card may stand in front of
    the wall the point lies on).  feet: the pose's feet point (sprites.feet_of); default = the pose stored for the frame.
    Sets the scene to `frame`."""
    scene = actor.scene or bpy.context.scene
    camera = camera or scene.camera
    o, x, y, z, s = card_state(actor, camera, frame)
    c = camera.matrix_world.to_translation()
    p = Vector(world_point)
    d = p - c
    den = d.dot(y)
    if abs(den) < 1e-9:
        raise ValueError("world point lies edge-on to the card of %s" % actor.name)
    t = (o - c).dot(y) / den
    hit = c + d * t
    fx, fy = feet if feet is not None else actor.feet_at(scene.frame_current)
    u, v = (hit - o).dot(x) / s, (hit - o).dot(z) / s
    return (u + fx, -v + fy)


def local_to_world(actor, local_xy, frame=None, feet=None, camera=None):
    """world position of a puppet-local point (an anchor of the sprite result) on the card on `frame`."""
    scene = actor.scene or bpy.context.scene
    o, x, y, z, s = card_state(actor, camera or scene.camera, frame)
    fx, fy = feet if feet is not None else actor.feet_at(scene.frame_current)
    return o + x * ((local_xy[0] - fx) * s) - z * ((local_xy[1] - fy) * s)


def local_to_screen(actor, camera, local_xy, frame=None, feet=None):
    """pixel (x from the left, y from the TOP, 720x1280 units) and planar depth of a puppet-local point on `frame`."""
    from bpy_extras.object_utils import world_to_camera_view
    scene = actor.scene or bpy.context.scene
    camera = camera or scene.camera
    w = local_to_world(actor, local_xy, frame, feet, camera)
    co = world_to_camera_view(scene, camera, w)
    return (co.x * scene.render.resolution_x, (1.0 - co.y) * scene.render.resolution_y, co.z)


def head_samples(actor, camera, frame=None, radius=0.1):
    """nine screen points (x, y from the top, 720x1280 units) inside the head disc of `actor` on `frame`: the head
    centre of the finished drawing and eight points `radius` D around it (render.cards_wrong looks at them)."""
    scene = actor.scene or bpy.context.scene
    f = scene.frame_current if frame is None else int(frame)
    pose = actor.poses.get(f, {})
    k = actor.upper_k.get(f, 1.0)
    hy = sprites.hip_y(actor.cast, pose) * (1.0 - k)
    sq = pose.get("squash", 1.0)
    sq = float(sq[1] if isinstance(sq, (tuple, list)) else sq) or 1.0
    out = []
    for dx in (-radius, 0.0, radius):
        for dy in (-radius, 0.0, radius):
            x, y, _ = local_to_screen(actor, camera, (dx, hy + dy * k * sq), f)
            out.append((x, y))
    return out


def sync_all(scene=None, camera=None):
    """orient every actor of the scene for the current frame (drops actors whose objects were deleted)."""
    scene = scene or bpy.context.scene
    for a in list(REGISTRY):
        try:
            if a.root is None or a.root.name not in scene.objects:
                continue
        except ReferenceError:
            REGISTRY.remove(a)
            continue
        a.sync(camera, scene)


def clear_registry():
    del REGISTRY[:]
