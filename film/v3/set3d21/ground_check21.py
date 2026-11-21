"""Film 21 ground check (QA_TEAM.md §K step 1), until film/v3/tools/ground_check.py lands.

Usage inside a shot script, AFTER the scene is built and BEFORE the final render:

    import ground_check21 as GC
    rep = GC.check(items, frames=range(g0, g1 + 1, 10), set_frame=my_set_frame,
                   airborne={'helmet_float': range(1575, 1600)}, out='GROUND.md')
    assert rep['fail'] == 0, 'fix the floating items listed in GROUND.md first'

items     list of things that must touch the ground: cast Actors (their .card is used), bpy objects (props, carts,
          barrels, banners on poles), or (name, obj, foot_offset) tuples. foot_offset (scene units) = transparent
          padding under the soles in the card's sprite, if any.
set_frame callable(g) that poses EVERYTHING for film frame g (call your per-frame hooks, place actors, set camera).
airborne  {name: iterable of g} where an item is legitimately in the air (a jump, a thrown helmet, a swimmer card
          floating on water counts as grounded when water is below it).
Each sampled frame ray-casts straight down from the item's lowest point. FAIL if the gap to the first surface that is
not the item itself is more than TOL (2 cm), or if nothing is below the item. A negative gap (sunk below the surface
by more than SINK) is reported as SUNK (a warning).
"""
import bpy
from mathutils import Vector

TOL = 0.02
SINK = 0.25


def _obj(it):
    if isinstance(it, tuple):
        return it[0], it[1], (it[2] if len(it) > 2 else 0.0)
    o = getattr(it, 'card', None) or getattr(it, 'root', None) or it
    return getattr(it, 'name', o.name), o, 0.0


def _own(o):
    s = {o.name}
    for c in o.children_recursive:
        s.add(c.name)
    p = o.parent
    while p is not None:
        s.add(p.name)
        for c in p.children_recursive:
            s.add(c.name)
        p = p.parent
    return s


def _lowest(o):
    dg = bpy.context.evaluated_depsgraph_get(); ev = o.evaluated_get(dg)
    pts = [ev.matrix_world @ Vector(c) for c in ev.bound_box]
    zmin = min(p.z for p in pts); low = [p for p in pts if p.z - zmin < 1e-4]
    x = sum(p.x for p in low) / len(low); y = sum(p.y for p in low) / len(low)
    return Vector((x, y, zmin))


def _gap(o, own):
    sc = bpy.context.scene; dg = bpy.context.evaluated_depsgraph_get(); p = _lowest(o); org = p + Vector((0, 0, 0.5))
    for _ in range(12):
        hit, loc, nrm, idx, ob, mtx = sc.ray_cast(dg, org, Vector((0, 0, -1)))
        if not hit:
            return None
        if ob.name in own or ob.name.startswith(('contact', 'shadow', 'proxy')) or ob.hide_render:
            org = loc + Vector((0, 0, -1e-3)); continue
        return p.z - loc.z
    return None


def check(items, frames, set_frame, airborne=None, out='GROUND.md'):
    airborne = {k: set(v) for k, v in (airborne or {}).items()}
    rows, fail, sunk = [], 0, 0
    for g in frames:
        set_frame(g); bpy.context.view_layer.update()
        for it in items:
            name, o, off = _obj(it)
            if o.hide_render or g in airborne.get(name, ()):
                continue
            gap = _gap(o, _own(o))
            if gap is not None:
                gap -= off
            if gap is None or gap > TOL:
                fail += 1; rows.append((g, name, 'FAIL', 'nothing below' if gap is None else f'{gap * 100:.1f} cm above'))
            elif gap < -SINK:
                sunk += 1; rows.append((g, name, 'SUNK', f'{-gap * 100:.1f} cm below'))
    lines = [f"# GROUND check (QA §K) — {'PASS' if fail == 0 else 'FAIL'}", '',
             f"frames sampled: {len(list(frames))}; items: {len(items)}; FAIL {fail}; SUNK (warning) {sunk}; tolerance {TOL * 100:.0f} cm", '']
    if rows:
        lines += ['| g | item | result | gap |', '|---|---|---|---|'] + [f'| {g} | {n} | {r} | {d} |' for g, n, r, d in rows]
    if out:
        open(out, 'w').write('\n'.join(lines) + '\n')
    return dict(fail=fail, sunk=sunk, rows=rows)
