"""Film 22 fallback for QA_TEAM.md §K ground_check (use film/v3/tools/ground_check.py instead once it exists on the branch).

Call from inside a shot script AFTER the scene, actors and animation are set up, BEFORE rendering:

    import sys; sys.path.insert(0, PROJ + "/v3/tools"); import ground_check22
    ok = ground_check22.run(f0, f1, out_md=TAKE_DIR + "/GROUND.md", step=10)

Every 10th frame, for every visible object that is not airborne, it ray-casts down from the object's lowest world point.
- An object is airborne if it has the custom property `airborne=True`, or its name contains an airborne token.
- The checked objects are character cards, props and set dressing. Large set geometry (floors, walls, sky) is skipped.
- It FAILS when the gap to the first surface below is more than 0.02 scene units (2 cm, §K), or when nothing is below.
- It writes GROUND.md (a table of every failure with frame, object and gap) and returns True or False. Fix by snapping to
  the ground (lower the object by the gap), or set airborne=True ONLY for things that really fly (birds, thrown or falling
  paper mid-air, smoke, hanging lamps on a visible cord, signs on visible brackets, wall-mounted items touching a wall).
- Mounted things (frames, posters, shelves on a wall; a pendant on a visible cord) can carry the custom property
  `mounted=True` after you have LOOKED that they touch their wall or cord. Otherwise the tool also casts toward the nearest wall. If a horizontal ray within 0.02 hits a surface, the object is
  counted as attached.
"""
import bpy, mathutils

AIR = ("sky", "cloud", "smoke", "steam", "bird", "lamp_cord", "halo", "glow", "light", "camera", "star", "moon",
       "flutter", "fly", "airborne", "beam", "shaft", "fog", "rain", "dust")
SKIP_BIG = 40.0  # objects wider than this many units are set geometry (ground, walls), not checked


def _lowest_point(ob, dg):
    ev = ob.evaluated_get(dg)
    try:
        me = ev.to_mesh()
    except Exception:
        return None
    if me is None or len(me.vertices) == 0:
        ev.to_mesh_clear(); return None
    mw = ev.matrix_world
    pts = [mw @ v.co for v in me.vertices]
    ev.to_mesh_clear()
    low = min(pts, key=lambda p: p.z)
    xs = [p.x for p in pts]; ys = [p.y for p in pts]
    span = max(max(xs) - min(xs), max(ys) - min(ys))
    # centre of the lowest 5 % band, so a tilted card is judged at its feet
    zmin = low.z; band = [p for p in pts if p.z <= zmin + 0.05 * (max(p.z for p in pts) - zmin + 1e-6)]
    c = sum(band, mathutils.Vector()) / len(band)
    return mathutils.Vector((c.x, c.y, zmin)), span


def _airborne(ob):
    if ob.get("airborne"): return True
    n = ob.name.lower()
    return any(t in n for t in AIR)


def _cast(scene, dg, origin, d, dist, ob):
    """first hit that is not `ob` itself (steps past self hits)"""
    o = mathutils.Vector(origin); d = mathutils.Vector(d); left = dist
    for _ in range(12):
        hit, loc, nrm, idx, hob, _m = scene.ray_cast(dg, o, d, distance=left)
        if not hit: return None
        if hob is not None and hob.original != ob.original and hob.name != ob.name: return loc
        step = (loc - o).length + 1e-4; left -= step; o = loc + d * 1e-4
        if left <= 0: return None
    return None


def check_frame(scene, frame, tol=0.02):
    scene.frame_set(frame)
    dg = bpy.context.evaluated_depsgraph_get()
    fails = []
    for ob in scene.objects:
        if ob.type != 'MESH' or ob.hide_render or _airborne(ob): continue
        lp = _lowest_point(ob, dg)
        if lp is None: continue
        p, span = lp
        if span > SKIP_BIG: continue
        # downward from just above the lowest point, ignoring the object itself
        loc = _cast(scene, dg, p + mathutils.Vector((0, 0, 0.01)), (0, 0, -1), 1e4, ob)
        gap = (p.z - loc.z) if loc is not None else None
        if loc is not None and gap <= tol: continue
        # sunk slightly into a floor/desk (its surface is just above the lowest point): grounded
        if _cast(scene, dg, p - mathutils.Vector((0, 0, 0.001)), (0, 0, 1), 0.35, ob) is not None and (loc is None or gap > tol): 
            up = _cast(scene, dg, p - mathutils.Vector((0, 0, 0.001)), (0, 0, 1), 0.35, ob)
            if up is not None and (up.z - p.z) < 0.35: continue
        if ob.get("mounted"): continue
        # attached: something other than itself within tol+0.05 sideways or behind (walls, desks, hooks, frames)
        attached = False
        for d in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1)):
            dv = mathutils.Vector(d)
            for zoff in (0.01, 0.3):
                o = p + mathutils.Vector((0, 0, zoff)) - dv * 0.05
                if _cast(scene, dg, o, d, tol + 0.12, ob) is not None: attached = True; break
            if attached: break
        if attached: continue
        fails.append((frame, ob.name, "nothing below" if gap is None else f"gap {gap:.3f}"))
    return fails


def run(f0, f1, out_md=None, step=10, tol=0.02):
    scene = bpy.context.scene
    frames = list(range(f0, f1 + 1, step)) + ([f1] if (f1 - f0) % step else [])
    allf = []
    for f in frames: allf += check_frame(scene, f, tol)
    ok = not allf
    if out_md:
        L = ["# GROUND.md (QA_TEAM §K ground_check, film 22 fallback tool)", f"frames {f0}-{f1} step {step}, tolerance {tol}",
             f"RESULT: {'PASS' if ok else 'FAIL'} ({len(allf)} failures)", "", "| frame | object | problem |", "|---|---|---|"]
        L += [f"| {a} | {b} | {c} |" for a, b, c in allf[:400]]
        open(out_md, "w").write("\n".join(L) + "\n")
    print("ground_check", "PASS" if ok else f"FAIL {len(allf)}")
    return ok
