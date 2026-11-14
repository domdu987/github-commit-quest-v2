"""render.py -- Cycles settings for true-3D frames with flat-card actors, and the frame loop (bpy 5.3, CPU).

    import render
    render.setup(scene, "final")                         # or "draft"
    stats = render.render_frames(range(1, 31), "/abs/out", scale=1.0, threads=None)     # f_0001.png ...
    x, y, depth = render.world_to_screen(cam, (0.4, 0.0, 3.1), frame=12)                # px from the top-left, 720x1280
    render.drop_cache(scene)                             # after overwriting a texture file that was already rendered

Persistent render data is OFF by default (setup(persistent=False)): it saved no time in any measurement and it makes
Cycles keep the pixels of texture files that were overwritten after they were rendered.

Why it is cheap: the lighting is deterministic.  Ambient is emission inside the set materials, the key is one sun with a
tiny angle (or lamps with a tiny radius), there is no diffuse bounce and the actors are emission cards, so the only thing a
sample has to resolve is the pixel filter and the thin penumbra.  A few samples without a denoiser are enough.
"""
import os, time
import bpy
from mathutils import Vector

QUALITY = {
    # samples: fixed count, no adaptive sampling, no denoiser (nothing in these frames is noisy except the penumbra)
    "draft": dict(samples=4, filter_width=1.5),      # with render_frames(scale=0.5): about 0.6 s per frame
    "final": dict(samples=8, filter_width=1.5),      # RMS difference to a 64-sample frame: 1.2 levels of 255
}


def _bloom_group(threshold=1.0, size=0.05, strength=0.5, tint=(1.0, 0.92, 0.80, 1.0)):
    """Render Layers -> Glare (Bloom on scene-linear values above `threshold` only) -> output.  Heads (#fef7f6 = 0.93 linear)
    and everything else at or below 1.0 pass through unchanged; only emitters stronger than 1 get the tight halo."""
    ng = bpy.data.node_groups.new("StageBloom", "CompositorNodeTree")
    ng.interface.new_socket("Image", in_out="OUTPUT", socket_type="NodeSocketColor")
    rl = ng.nodes.new("CompositorNodeRLayers")
    gl = ng.nodes.new("CompositorNodeGlare")
    gl.inputs["Type"].default_value = "Bloom"
    gl.inputs["Quality"].default_value = "High"
    gl.inputs["Threshold"].default_value = threshold
    gl.inputs["Smoothness"].default_value = 0.1
    gl.inputs["Size"].default_value = size
    gl.inputs["Strength"].default_value = strength
    gl.inputs["Saturation"].default_value = 1.0
    gl.inputs["Tint"].default_value = tint
    out = ng.nodes.new("NodeGroupOutput")
    ng.links.new(rl.outputs["Image"], gl.inputs["Image"])
    ng.links.new(gl.outputs["Image"], out.inputs[0])
    return ng, rl


def setup(scene=None, quality="final", bloom=None, samples=None, threads=None, filter_width=None, persistent=False):
    """Cycles CPU, Standard view transform, direct light only, fixed low sample count.

    quality   "draft" (4 samples; use with render_frames(scale=0.5)) or "final" (8 samples)
    bloom     None = leave the scene's compositor as it is (the set or the integrator may own a grade);
              True / dict(threshold=1.0, size=0.05, strength=0.5, tint=...) = attach a Glare Bloom on values above 1.0;
              False = switch compositing off
    samples, filter_width, threads   overrides (threads: FIXED count; None = automatic)
    persistent  keep Cycles' BVH and textures between frames (scene.render.use_persistent_data).  Default False (review):
              measured, it saves nothing here (5.52 against 5.53 s per final frame in the stub room, 6.06 against 6.08 s
              with four 2048 px textures and 13000 extra triangles), and with it Cycles keeps the pixels of a texture file
              that was overwritten after it was rendered (a re-posed sprite, a wall map drawn on) and shows the old
              picture.  If you switch it on, the actors guard their own sprites (Actor.reload_sprites) and drop_cache()
              is there for set textures.
    Returns the scene."""
    scene = scene or bpy.context.scene
    q = dict(QUALITY[quality])
    if samples is not None:
        q["samples"] = int(samples)
    if filter_width is not None:
        q["filter_width"] = float(filter_width)
    r = scene.render
    r.engine = "CYCLES"
    c = scene.cycles
    c.device = "CPU"
    c.samples = q["samples"]
    c.use_adaptive_sampling = False
    c.use_denoising = False
    c.seed = 0
    c.use_animated_seed = False                       # the same sample pattern on every frame: penumbra noise does not boil
    c.max_bounces = 1
    c.diffuse_bounces = 0
    c.glossy_bounces = 1
    c.transmission_bounces = 0
    c.volume_bounces = 0
    c.transparent_max_bounces = 12                    # cards, shadow proxies and contact decals stacked along one ray
    c.caustics_reflective = False
    c.caustics_refractive = False
    c.sample_clamp_indirect = 3.0
    c.pixel_filter_type = "BLACKMAN_HARRIS"
    c.filter_width = q["filter_width"]
    c.use_auto_tile = False
    r.use_persistent_data = bool(persistent)          # see the docstring: off by default
    r.use_motion_blur = False
    r.film_transparent = False
    r.use_freestyle = False                           # Freestyle aborts the process without a display
    r.resolution_x, r.resolution_y = 720, 1280
    r.resolution_percentage = 100
    r.fps = 30
    r.image_settings.file_format = "PNG"
    r.image_settings.color_mode = "RGB"
    r.image_settings.color_depth = "8"
    r.image_settings.compression = 15
    r.dither_intensity = 0.0
    vs = scene.view_settings
    vs.view_transform = "Standard"
    vs.look = "None"
    vs.exposure = 0.0
    vs.gamma = 1.0
    scene.display_settings.display_device = "sRGB"
    if threads:
        r.threads_mode = "FIXED"
        r.threads = int(threads)
    else:
        r.threads_mode = "AUTO"
    if scene.world is None:
        w = bpy.data.worlds.new("StageWorld")
        scene.world = w
        nt = w.node_tree
        for n in list(nt.nodes):
            nt.nodes.remove(n)
        bg = nt.nodes.new("ShaderNodeBackground")
        out = nt.nodes.new("ShaderNodeOutputWorld")
        bg.inputs["Color"].default_value = (0.0, 0.0, 0.0, 1.0)
        bg.inputs["Strength"].default_value = 0.0
        nt.links.new(bg.outputs["Background"], out.inputs["Surface"])
    if bloom is False:
        r.use_compositing = False
    elif bloom:
        kw = bloom if isinstance(bloom, dict) else {}
        ng, rl = _bloom_group(**kw)
        rl.scene = scene
        if hasattr(scene, "compositor_effects"):
            effs = scene.compositor_effects
            eff = effs.active or effs.new(name="StageBloom")
            eff.node_group = ng
        else:
            scene.compositing_node_group = ng
        r.use_compositing = True
        r.compositor_device = "CPU"
    return scene


def drop_cache(scene=None):
    """Free Cycles' persistent render data of the scene (BVH, textures); the next render rebuilds it.

    Needed whenever a texture FILE is overwritten in place after it has been rendered: with persistent data Cycles keys a
    file texture by its path and keeps the old pixels, and Image.reload() does not reach it (measured on the sprites:
    the old drawing was shown).  The actors do this by themselves for their sprites.  For a set texture that changes
    (the wall map with the track drawn on it) either write every version to its own path, or overwrite, call
    image.reload() and then this."""
    scene = scene or bpy.context.scene
    r = scene.render
    if r.use_persistent_data:
        r.use_persistent_data = False
        r.use_persistent_data = True


def world_to_screen(camera, point, frame=None, scene=None):
    """(x, y, depth): pixel position of a world point in the full 720x1280 frame, x from the left edge, y from the TOP
    edge, continuous coordinates (the centre of the top-left pixel is (0.5, 0.5)); depth = planar distance in D.
    frame: set the scene to this frame first (None = current frame)."""
    from bpy_extras.object_utils import world_to_camera_view
    scene = scene or bpy.context.scene
    camera = camera or scene.camera
    if frame is not None and scene.frame_current != int(frame):
        scene.frame_set(int(frame))
    bpy.context.view_layer.update()
    co = world_to_camera_view(scene, camera, Vector(point))
    return (co.x * scene.render.resolution_x, (1.0 - co.y) * scene.render.resolution_y, co.z)


def _actor_modules():
    import sys
    return [m for n, m in list(sys.modules.items())
            if m is not None and (n == "actors" or n.endswith(".actors")) and hasattr(m, "sync_all")]


def cards_wrong(path, scene=None, camera=None, skip=()):
    """Names of the visible actors whose head, in the frame just written to `path`, is a hole: every sample inside the
    head disc is black (the whole card rendered black: seen once in about 5000 renders during the review, cause not
    found) or magenta (Cycles' colour for a texture it could not read).  A head that is off screen, or a frame rendered
    with a border, is not judged.  Costs one PNG decode (about 25 ms)."""
    scene = scene or bpy.context.scene
    camera = camera or scene.camera
    r = scene.render
    if r.use_border:
        return []
    img = None
    out = []
    for m in _actor_modules():
        for a in list(m.REGISTRY):
            try:
                if a.card is None or a.card.hide_render or a.root.name not in scene.objects or a.name in skip:
                    continue
            except ReferenceError:
                continue
            if scene.frame_current not in a.poses:
                continue
            pts = m.head_samples(a, camera, scene.frame_current)
            if img is None:
                import numpy as np
                from PIL import Image
                img = np.asarray(Image.open(path).convert("RGB")).astype(np.int16)
            k = img.shape[1] / float(r.resolution_x)
            px = []
            for x, y in pts:
                xi, yi = int(x * k), int(y * k)
                if 0 <= xi < img.shape[1] and 0 <= yi < img.shape[0]:
                    px.append(img[yi, xi])
            if len(px) < 5:
                continue
            black = all(int(c.max()) <= 40 for c in px)          # (the ink is #3a2832: max 58)
            magenta = all(c[0] > 200 and c[1] < 70 and c[2] > 200 for c in px)
            if black or magenta:
                out.append(a.name)
    return out


def render_frames(frames, out_dir, scale=1.0, threads=None, scene=None, camera=None, prefix="f_", sync=True,
                  on_frame=None, verbose=True, check=True):
    """Render `frames` (Blender frame numbers) to <out_dir>/f_0001.png ...; every frame is a true-3D Cycles render.

    scale    1.0 = 720x1280, 0.5 = 360x640 (drafts)
    threads  None = keep the scene setting; n = FIXED n threads (use 2 while another job shares the machine)
    sync     orient every actors.Actor toward the camera before each frame (leave on)
    on_frame optional callable(frame) run after frame_set and before the render (per-frame set changes)
    check    after each frame, look at every visible actor's head in the written PNG (cards_wrong).  If one is a black
             or magenta hole, the sprite and render caches are emptied and the frame is rendered once more; the frame's
             entry then carries "retried": [names] and, if it did not help, "still_wrong": [names] (such an actor is
             not retried again in this call: something dark really is in front of its head).
    Returns [{"frame", "path", "wall", "cpu"}], wall and CPU (user + system, all threads) seconds per frame."""
    scene = scene or bpy.context.scene
    if camera is not None:
        scene.camera = camera
    r = scene.render
    r.resolution_percentage = int(round(100 * scale))
    if threads:
        r.threads_mode = "FIXED"
        r.threads = int(threads)
    os.makedirs(out_dir, exist_ok=True)
    actor_modules = _actor_modules()
    stats = []
    given_up = set()

    def one(f, path):
        scene.frame_set(f)
        if on_frame is not None:
            on_frame(f)
        if sync:
            for m in actor_modules:
                m.sync_all(scene, scene.camera)
        r.filepath = path
        bpy.ops.render.render(write_still=True)

    for f in frames:
        f = int(f)
        path = os.path.join(out_dir, "%s%04d.png" % (prefix, f))
        t0, c0 = time.time(), os.times()
        one(f, path)
        retried = still = None
        if check and actor_modules:
            wrong = cards_wrong(path, scene, scene.camera, skip=given_up)
            if wrong:
                for m in actor_modules:
                    for a in list(m.REGISTRY):
                        if a.name in wrong:
                            a.reload_sprites()
                drop_cache(scene)
                one(f, path)
                retried = wrong
                still = cards_wrong(path, scene, scene.camera, skip=given_up)
                given_up.update(still)
                print("render: frame %d: the head of %s was a black or magenta hole; rendered again -> %s"
                      % (f, ", ".join(wrong), ("still so for " + ", ".join(still)) if still else "fine"), flush=True)
        c1 = os.times()
        st = dict(frame=f, path=path, wall=time.time() - t0, cpu=(c1.user - c0.user) + (c1.system - c0.system))
        if retried:
            st["retried"] = retried
            if still:
                st["still_wrong"] = still
        stats.append(st)
        if verbose:
            print("render: frame %d  %.2f s wall  %.2f s cpu  -> %s" % (f, st["wall"], st["cpu"], path), flush=True)
    return stats
