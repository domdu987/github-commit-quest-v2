"""runtime dressing of the cellar for my takes: cast13 worker cards (static turn-bar poses A / B) as crowd cards, keyed on / off per frame."""
import math, random
import c13 as C
import cast13
S = C.S; STATE = S.STATE

def worker_roles():
    """six placeholder roles: bar pose A / B of workers a, b, c (T.PH feeds S.crowd -> shared-mesh cards)."""
    roles = {}
    for sfx in ("a", "b", "c"):
        for ph in ("A", "B"):
            cast, pose = cast13.STORY13["worker_turn_bar_%s_%s" % (ph, sfx)]
            name = "w%s_%s" % (ph, sfx); pz = dict(pose); pz.update(expr="neutral", mouth="dash"); S.T.PH[name] = (cast, pz, 3.25 if sfx != "c" else 3.1)
            roles[(ph, sfx)] = name
    return roles

def dense_slots(n_workers, jacks_per_worker=10, x0=-8.3, dx=0.56, y0=5.0, cols=48):
    pts = []
    for k in range(n_workers):
        idx = jacks_per_worker * k + jacks_per_worker // 2; row, c = divmod(idx, cols)
        pts.append((x0 + c * dx, y0 + row * dx - 0.34))
    return pts

def make_crowd(points, seed=3, scale=(0.96, 1.04)):
    """one A card and one B card per point: [(obA, obB)]"""
    roles = worker_roles(); r = random.Random(seed); out = []
    for (x, y) in points:
        sfx = r.choice(("a", "b", "c", "a", "b")); s = r.uniform(*scale)
        a = S.crowd(1, None, points=[(x, y)], kinds=[roles[("A", sfx)]], ground=0.0, scale=(s, s))[0]
        b = S.crowd(1, None, points=[(x, y)], kinds=[roles[("B", sfx)]], ground=0.0, scale=(s, s))[0]
        out.append((a, b))
    return out

def key_crowd(crowd, f, g, on_fn, flip_fn=None, hide_fn=None):
    """on_fn(k) -> bool shown; flip_fn(k, g) -> 0/1 pose A/B; hide_fn(k) -> True hides it (e.g. chin in the caption band)."""
    for k, (a, b) in enumerate(crowd):
        on = on_fn(k) and not (hide_fn(k) if hide_fn else False); fl = flip_fn(k, g) if flip_fn else 0
        for ob, show in ((a, on and fl == 0), (b, on and fl == 1)):
            ob.hide_render = not show; ob.keyframe_insert("hide_render", frame=f)

def replace_lamps(halo=False):
    """the set's oil lamps carry a 2.6 D additive halo that washes out everything in the aisle (cards in front of / behind a lamp vanish into the glow).
    Hide that merged object and rebuild the same lamps (rod, glass, shade, emissive glass) WITHOUT the halo; the point lights stay."""
    from mathutils import Vector
    M = STATE['M']; SET = STATE['SET']; ob = __import__("bpy").data.objects.get("cellar_lamps")
    if ob is not None: ob.hide_render = True
    lamps = [(3.0, 7.35, 1.95), (3.0, 15.45, 1.95), (3.0, 23.55, 1.95), (3.0, 34.35, 1.95), (3.0, 50.55, 1.95), (9.0, 15.45, 1.95), (13.5, 40.0, 1.95)]
    fl = S.MB()
    for (xl, yl, zl) in lamps:
        c = Vector((xl, yl, zl)); S.rod(fl, c + Vector((0, 0, 0.5)), c + Vector((0, 0, 3.7 - zl)), 0.03, M['iron_d'], seg=4)
        fl.frustum(c - Vector((0, 0, 0.5)), c + Vector((0, 0, 0.5)), 0.26, 0.34, M['lamp_glass'], seg=7); fl.frustum(c + Vector((0, 0, 0.5)), c + Vector((0, 0, 0.8)), 0.38, 0.05, M['iron_d'], seg=7)
    S._obj(fl, "lamps_mine", SET, shadow=False)


def fix_cellar():
    """hide the pale light-shaft cards (one of them reads as a tan wedge over the aisle) and lay a raised plank slab over the central aisle so the
    floor undulations do not poke through the planks as flat brown blobs."""
    import bpy
    o = bpy.data.objects.get("shafts")
    if o is not None: o.hide_render = True
    mb = S.MB(); S.sbox(mb, (1.9, -6.0, 0.0), (4.1, 70.0, 0.36), STATE['M']['plank_f'], 0.2)
    S._obj(mb, "plank_aisle", STATE['SET'], shadow=False)
