"""Test setup 1 for ground_check.py: stage/stubroom.py + real stage/actors.py cards (placeholder sprites) + props.
   python3 ground_test_stub.py [--fix]      (needs the pip `bpy` module; in Blender: blender -b --python ground_test_stub.py)
Planted defects: boss floats 0.6 up; walker's keyed path lifts 0.35 over frames 21..40; 'ox' sprite has 12% empty rows at the
bottom (alpha-bottom test); pole_flag hovers; 'canopy_top' has no legs; 'stub_box' (stubroom) and 'crate' are fine;
'bird' is airborne=True; 'thrown_pot' is airborne only on frames 30..60."""
import os, sys, tempfile
HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(HERE)
sys.path[:0] = [os.path.join(V3, "stage"), HERE]
import bpy
from mathutils import Vector
import stubroom, actors, sprites, ground_check as GC


def png(path, w, h, bottom_empty=0.0):
    img = bpy.data.images.new(os.path.basename(path), w, h, alpha=True)
    buf = [0.0] * (w * h * 4)
    r0 = int(h * bottom_empty)
    for y in range(r0, h):
        for x in range(int(w * 0.3), int(w * 0.7)):
            i = (y * w + x) * 4
            buf[i:i + 4] = [0.8, 0.3, 0.2, 1.0]
    img.pixels = buf
    img.filepath_raw = path
    img.file_format = "PNG"
    img.save()
    bpy.data.images.remove(img)


def mesh_box(name, lo, hi, scene):
    me = bpy.data.meshes.new(name)
    x0, y0, z0 = lo; x1, y1, z1 = hi
    v = [(x0, y0, z0), (x1, y0, z0), (x1, y1, z0), (x0, y1, z0), (x0, y0, z1), (x1, y0, z1), (x1, y1, z1), (x0, y1, z1)]
    me.from_pydata(v, [], [(0, 3, 2, 1), (4, 5, 6, 7), (0, 1, 5, 4), (1, 2, 6, 5), (2, 3, 7, 6), (3, 0, 4, 7)])
    ob = bpy.data.objects.new(name, me)
    scene.collection.objects.link(ob)
    return ob


def build(frames=60):
    scene = bpy.context.scene
    scene.frame_start, scene.frame_end = 1, frames
    stubroom.build(scene)
    cam = camrig_cam(scene)
    d = tempfile.mkdtemp(prefix="gc_sprites_")
    canvas = sprites.DEFAULT_CANVAS["hero"]
    for nm, empty in (("hero", 0.0), ("boss", 0.0), ("walker", 0.0), ("ox", 0.12)):
        for f in range(1, frames + 1):
            png(os.path.join(d, "%s_%04d.png" % (nm, f)), 16, 32, empty)
    hero = actors.Actor("hero", "hero"); hero.build(canvas, d, contact=True)
    hero.place(1, (-1.0, -3.0, 0.0)); hero.place(frames, (-1.0, -3.0, 0.0))                 # on the floor: OK
    boss = actors.Actor("boss", "hero"); boss.build(canvas, d)
    boss.place(1, (1.0, -4.0, 0.6)); boss.place(frames, (1.0, -4.0, 0.6))                   # floats 0.6
    walker = actors.Actor("walker", "hero"); walker.build(canvas, d)
    walker.place(1, (-3.0, -5.0, 0.0)); walker.place(20, (-2.0, -5.0, 0.0))
    walker.place(30, (-1.5, -5.0, 0.35)); walker.place(40, (-1.0, -5.0, 0.35)); walker.place(frames, (0.0, -5.0, 0.0))
    ox = actors.Actor("ox", "hero"); ox.build(canvas, d)
    ox.place(1, (4.0, -6.0, 0.0)); ox.place(frames, (4.0, -6.0, 0.0))                       # bottom 12% empty: alpha-bottom must be used
    pole = mesh_box("pole_flag", (-0.05, -0.05, 1.0), (0.05, 0.05, 3.0), scene); pole.location = (-4.0, -3.0, 0.0)
    can = mesh_box("canopy_top", (-1.0, -0.5, 1.6), (1.0, 0.5, 1.7), scene); can.location = (3.0, -8.0, 0.0)
    crate = mesh_box("crate", (-0.3, -0.3, 0.0), (0.3, 0.3, 0.6), scene); crate.location = (-2.0, -9.0, 0.0)
    onbox = mesh_box("crate_on_box", (-0.2, -0.2, 0.0), (0.2, 0.2, 0.4), scene); onbox.location = (2.7, -1.0, 1.3)   # sits on stub_box top
    bird = mesh_box("bird", (-0.1, -0.1, 0.0), (0.1, 0.1, 0.1), scene); bird.location = (0.0, -7.0, 4.0); bird["airborne"] = True
    pot = mesh_box("thrown_pot", (-0.1, -0.1, 0.0), (0.1, 0.1, 0.3), scene); pot.location = (-3.0, -7.0, 2.0); pot["airborne_frames"] = "30:60"
    scene.frame_set(1)
    return scene


def camrig_cam(scene):
    import camrig
    c = camrig.make_camera(scene)
    c.location = (0.0, -14.0, 3.0)
    c.rotation_euler = (1.4, 0.0, 0.0)
    scene.camera = c
    return c


if __name__ == "__main__":
    scene = build()
    argv = ["--every", "10", "--gap", "0.02", "--out", os.path.join(HERE, "GROUND_stub.md")] + (["--fix"] if "--fix" in sys.argv else [])
    sys.exit(GC.run_cli(argv))
