"""Test setup 2 for ground_check.py: the real film-3 set (set3d3/harbor.py, Boston waterfront) with 3 stage actors (placeholder
sprites) and the set's own props (bucket, yard_props, ...).  python3 ground_test_harbor.py [--fix]
Planted: 'clerk' stands on the cobbles (fine); 'sailor' floats 0.5 over the sidewalk; 'mill' walks from the street up onto the
sidewalk with a keyed Z that stays 0.3 too high; a loose 'cart' prop hovers 0.8 over the yard."""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
V3 = os.path.dirname(HERE)
sys.path[:0] = [os.path.join(V3, "stage"), os.path.join(V3, "set3d3"), HERE]
import bpy
import harbor, actors, sprites, ground_check as GC
from ground_test_stub import png, mesh_box
import tempfile

def build(frames=60):
    sc = bpy.context.scene
    harbor.build("WINTER")
    sc.frame_start, sc.frame_end = 1, frames
    d = tempfile.mkdtemp(prefix="gc_sprites_")
    for nm in ("clerk", "sailor", "mill"):
        for f in range(1, frames + 1):
            png(os.path.join(d, "%s_%04d.png" % (nm, f)), 16, 32, 0.0)
    cv = (-0.5, -1.0, 0.5, 0.0)       # 1 D wide, feet at the bottom edge of the sprite: sprite bottom == feet
    for nm, p0, p1 in (("clerk", (0.0, 10.0, 0.0), (0.0, 10.0, 0.0)), ("sailor", (-6.5, 10.0, 0.5), (-6.5, 10.0, 0.5)),
                       ("mill", (-3.0, 5.0, 0.0), (-8.0, 5.0, 0.3))):
        a = actors.Actor(nm, "hero"); a.build(cv, d)
        a.place(1, p0); a.place(frames, p1)
    cart = mesh_box("cart", (-0.6, -0.4, 0.0), (0.6, 0.4, 0.5), sc); cart.location = (2.0, 8.0, 0.8)
    sc.frame_set(1)
    return sc

if __name__ == "__main__":
    build()
    sys.exit(GC.run_cli(["--every", "10", "--gap", "0.02", "--out", os.path.join(HERE, "GROUND_harbor.md")] + (["--fix"] if "--fix" in sys.argv else [])))
