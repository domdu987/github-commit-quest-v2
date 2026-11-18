#!/usr/bin/env python3
"""shot.py -- film 10 take s17: shots 17 + 18 + 19 (g 1090..1427 + 6 handle frames each side), THE REVEAL ("the sea is not a
guessing game": the stripes make the captain read the ship's heading wrongly, and the torpedo runs at a ghost).
One location (sea, SEA_DAY).  NO dashed lines or arrows: the idea is told by three things in the water -- the glowing GOLD LEAD BUOY (where
the ship will be: the right aim), the translucent pale-cyan GHOST ship sailing the other way (the captain's wrong reading) and the cyan
buoy ahead of it (where he aims), and the torpedo's white wake.

    id 17  g 1084..1193  topdown_sea A: the high oblique over the sea.  The torpedo is SLOW (foam V + bubble wake creeping up from the
                         U-boat at the bottom), the dazzle ship SAILS (bow wave, smoke) toward the gold buoy that appears ahead of its
                         bow (fades in, pulsing).  Slow push + drift.
    id 18  g 1194..1295  periscope_pov: the circular lens view; the dazzle ship's stripes make its bow read as its stern; the ghost
                         ship (facing the other way) fades in over it (set_ghost, offset +30 (it sits on the real ship, reversed)), then the cyan aim buoy lights up.
                         The view sweeps slowly.
    id 19  g 1296..1433  topdown_sea C: the torpedo runs at the ghost's guessed course (cyan buoy), through the phantom, and its wake
                         passes harmlessly BEHIND the real stern while the dazzle ship sails on toward the gold buoy.

Torpedo and sea time are shared with s15 (U(g), S table): u = 0.0021 (g - 1047) until g 1090, then 0.09 + 0.002 (g - 1090); sea s runs
1.6 .. 5.0 (17), 5.0 .. 8.2 (18), 8.2 .. 12.6 (19), about real time, so the torpedo crosses the ghost's course line (u 0.607, x -41)
at s ~ 10 in the middle of shot 19.  The gold buoy is moved 23 D ahead (x 64) so the ship's bow only reaches it at the end of 19.

Blender frame of (id, g) = 1000 * (id - 1) + g + 1.

    python3 shot.py probe 17,18,19 a:b[:step]
    python3 shot.py stills 17,18,19 a:b[:step] <out_dir> [scale] [samples]
    python3 shot.py final 17|18|19 a:b[:step] [scale] [samples]
"""
import math, os, sys, json

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c10 as C                                          # noqa: E402
from mathutils import Vector                             # noqa: E402

H, camrig = C.B, C.camrig
lerp, clamp, ez, bf = C.lerp, C.clamp, C.ez, C.bf

# ----------------------------------------------------------------------------- timing
G16, G17, G18, G19, G20 = C.g_bound(34.90), C.g_bound(36.35), C.g_bound(39.80), C.g_bound(43.20), C.g_bound(47.59)   # 1047 1090 1194 1296 1428
H_IN, H_OUT = 6, 6
RANGES = {17: (G17 - H_IN, G18 - 1), 18: (G18, G19 - 1), 19: (G19, G20 + H_OUT - 1)}
S_ANCH = [(G17, 1.6), (G18, 5.0), (G19, 8.2), (G20, 12.6)]            # sea time (shared across the take; s15 ends at 1.6)
LEAD_DX = 23.0                                                       # the gold buoy is moved ahead: x 41 -> 64
GHOST_OFF = 30.0


def s_of(g):
    a = S_ANCH
    for (g0, s0), (g1, s1) in zip(a, a[1:]):
        if g <= g1:
            return lerp(s0, s1, (g - g0) / float(g1 - g0))
    return a[-1][1] + (g - a[-1][0]) * (a[-1][1] - a[-2][1]) / float(a[-1][0] - a[-2][0])


def u_of(g):
    """torpedo path parameter, continuous with s15 (0.09 at g 1090) at 0.002 / frame (9 D/s)."""
    return 0.09 + 0.002 * (g - G17)


def sm(x):
    """0.35 sine + 0.65 linear: calm, no dead ends."""
    x = clamp(x)
    return 0.35 * ez(x, "sine") + 0.65 * x


# ----------------------------------------------------------------------------- cameras
# 17: the high oblique, widened a little so the sub's bubble track, the real ship, the ghost's lane and the gold buoy all fit;
#     it pushes in and drifts toward the real ship / buoy.  19: lower and nearer, drifting with the ship, so the wake runs under the stern.
CAM17 = ((6.0, -64.0, 125.0), (6.0, 4.0, 0.0), 14.5), ((12.0, -58.0, 122.0), (12.0, 12.0, 0.0), 15.0)
CAM19 = ((-8.0, -62.0, 125.0), (-8.0, 10.0, 0.0), 14.5), ((16.0, -58.0, 120.0), (16.0, 12.0, 0.0), 15.0)
# 18: inside the periscope (eye fixed at the head); a slow sweep over the real ship, lens 30 -> 33.
POV_LOOK = ((8.0, 0.0, 5.6), 30.0), ((22.0, 0.0, 5.0), 31.0)


def lerp_cam(c0, c1, x, raw=False):
    u = x if raw else sm(x)
    return (Vector([lerp(c0[0][i], c1[0][i], u) for i in range(3)]), Vector([lerp(c0[1][i], c1[1][i], u) for i in range(3)]), lerp(c0[2], c1[2], u))


def cam_of(shot, g, eye=None):
    if shot == 17:
        return lerp_cam(CAM17[0], CAM17[1], (g - G17) / float(G18 - G17))
    if shot == 19:
        lin = (g - G19) / float(G20 - G19)
        u = 0.25 * lin + 0.75 * ez((g - 1355) / 70.0)          # holds on the crossing (g ~1320-1375), then follows the ship on
        return lerp_cam(CAM19[0], CAM19[1], u, raw=True)
    u = sm((g - G18) / float(G19 - G18))
    pan = 40.0 * ez((g - (G19 - 26)) / 22.0)                             # last ~0.7 s: the view swings left so the aim buoy enters the circle
    look = Vector((2.5 * s_of(g) + 1.0 - pan, 0.0, lerp(5.6, 5.0, u)))   # follows the ship's centre
    return Vector(eye), look, lerp(POV_LOOK[0][1], POV_LOOK[1][1], u)


def ghost_off(g):
    """ghost x offset: 5 s puts its centre exactly on the real ship's (hull on hull, mirrored); from shot 19 it peels away to the left."""
    s = s_of(g)
    slide = 50.0 * ez((g - G19) / 66.0)
    if g < G19:                                   # shot 18: directly over the real hull, a slow drift to shot 19's first-frame offset
        return 5.0 * s - 15.0 * sm((g - G18) / float(G19 - G18))
    return 5.0 * s - 15.0 - slide


def ghost_k(g):
    """ghost opacity: fades in over shot 18 (0 -> 0.95 across 1202..1250), held through 19."""
    if g < G18:
        return 0.0
    if g < G19:
        return 0.8 * ez((g - G18) / 45.0)
    return 1.0 - 0.7 * ez((g - G19) / 36.0) - 0.2 * ez((g - (G20 - 40)) / 40.0)


def lead_k(g):
    if g < G18:
        return clamp((g - (G17 + 4)) / 22.0) * (1.0 + 0.12 * math.sin(g * 0.35))
    return 0.0 if g < G19 else (1.0 + 0.12 * math.sin(g * 0.35))


def gmark_k(g):
    """the cyan aim buoy lights up at the end of shot 18 and stays."""
    return clamp((g - (G19 - 18)) / 8.0) if g >= G18 else 0.0


# ----------------------------------------------------------------------------- the take
def bpy_obj(n):
    import bpy
    return bpy.data.objects[n]


class Take(C.Take):
    def __init__(self, quality="preview", shot=17):
        C.Take.__init__(self, "sea", "topdown_sea", quality=quality, lens=22.0, name="cam_s17")
        H.set_uboat(1.0, periscope=1.0)                      # for periscope_eye(): the head position of the raised periscope
        self.eye = Vector(H.periscope_eye())
        mk = H.STATE["markers"]
        for ob in list(mk["buoy"]) + [mk["lamp"]]:
            ob.location.x += LEAD_DX                         # runtime set change: the lead buoy is 23 D further ahead
        H.set_ghost(0.0, offset=GHOST_OFF)
        self.strip_wires()
        self.fix_torpedo_and_buoys()
        U = H.STATE["uboat"]
        import bpy
        self.near_eye = [U["head"], bpy.data.objects["uboat_mast"]]      # the periscope camera sits inside them

    def fix_torpedo_and_buoys(self):
        """QA: torpedo 3x without its arrow-like foam V (the soft bubble wake carries it); buoys 1.5x about their own centres."""
        import bmesh
        o = H.STATE["torp"]["ob"]
        bm = bmesh.new(); bm.from_mesh(o.data)
        fm = [i for i, m in enumerate(o.data.materials) if m and "foam" in m.name]
        bmesh.ops.delete(bm, geom=[f for f in bm.faces if f.material_index in fm], context="FACES")
        bm.to_mesh(o.data); bm.free()
        o.scale = (3.0, 3.0, 3.0)
        mk = H.STATE["markers"]
        for key, c in (("buoy", (H.LEAD[0], 0.0)), ("ghost_buoy", H.GHOST_AIM)):
            for ob in mk[key]:
                ob.scale = (1.5, 1.5, 1.5)
                ob.location = (ob.location.x + c[0] * (1 - 1.5), c[1] * (1 - 1.5), 0.0)

    def strip_wires(self):
        """QA-art: drop the ghost's rigging wires (the 6-vertex loose parts of the hull mesh)."""
        import bmesh
        o = H.STATE["ghost"]["hull"]
        bm = bmesh.new(); bm.from_mesh(o.data)
        seen, kill = set(), []
        for v in bm.verts:
            if v.index in seen:
                continue
            st, comp = [v], [v]; seen.add(v.index)
            while st:
                x = st.pop()
                for e in x.link_edges:
                    w = e.other_vert(x)
                    if w.index not in seen:
                        seen.add(w.index); st.append(w); comp.append(w)
            zs = [v.co.z for v in comp]
            dims = sorted(max(v.co[i] for v in comp) - min(v.co[i] for v in comp) for i in range(3))
            thin_rod = len(comp) == 8 and dims[1] < 0.16 and dims[2] > 1.5
            if len(comp) == 6 or thin_rod or (len(comp) == 24 and max(zs) - min(zs) > 12):
                kill += comp
        bmesh.ops.delete(bm, geom=kill, context="VERTS")
        bm.to_mesh(o.data); bm.free()
        # flat clean cyan silhouette: constant alpha = gk (no fresnel falloff: the real stripes no longer show through), one cyan
        import bpy
        m = bpy.data.materials["HB_sea_SEA_DAY_ghost"]
        for n in m.node_tree.nodes:
            if n.bl_idname == "ShaderNodeMath" and n.operation == "MULTIPLY_ADD":
                n.inputs[1].default_value = 0.0; n.inputs[2].default_value = 1.0
            if n.bl_idname == "ShaderNodeMix":
                n.inputs[6].default_value = (0.48, 0.9, 1.0, 1.0); n.inputs[7].default_value = (0.62, 0.95, 1.0, 1.0)
            if n.bl_idname == "ShaderNodeEmission":
                n.inputs["Strength"].default_value = 1.15
        g = H.STATE["ghost"]
        self.ghost_smoke = [o for o in bpy.data.objects if o.name.startswith("ghost_smoke")]
        self.lamps = [bpy_obj("L_lead_buoy_lamp"), bpy_obj("L_ghost_buoy_lamp")]

    def pose(self, shot, gs):
        if shot == 18:                                    # the cyan aim buoy is shown on the line of sight, inside the left of the circle
            mk = H.STATE["markers"]
            for ob in list(mk["ghost_buoy"]) + [mk["ghost_lamp"]]:
                ob.location = (ob.location.x + 11.0, ob.location.y - 10.0, ob.location.z)
        if shot == 18:                                    # QA: the aim buoy is CYAN like the ghost (body recoloured)
            import bpy
            def _em(name, col, k):
                m = bpy.data.materials.new(name); m.use_nodes = True; nt = m.node_tree; nt.nodes.clear()
                e = nt.nodes.new("ShaderNodeEmission"); e.inputs["Color"].default_value = col; e.inputs["Strength"].default_value = k
                o = nt.nodes.new("ShaderNodeOutputMaterial"); nt.links.new(e.outputs[0], o.inputs[0]); return m
            gb = bpy.data.objects["ghost_buoy"]
            cy, pw = _em("gb_cyan", (0.30, 0.78, 0.95, 1), 0.9), _em("gb_pale", (0.78, 0.97, 1.0, 1), 1.0)
            for i, sl in enumerate(gb.material_slots):
                sl.material = cy if i % 2 == 0 else pw
        for g in gs:
            f = bf(shot, g)
            s = s_of(g)
            pov = shot == 18
            if pov:
                dive, peri = 1.0, 1.0
            else:
                dive, peri = 1.0, 0.0
            H.set_smoke(1.0, frame=f); H.set_flames(1.0, frame=f)
            H.set_uboat(dive, frame=f, periscope=peri)
            H.set_convoy(s, frame=f)
            H.set_torpedo(u_of(g), frame=f)
            H.set_ghost(ghost_k(g), frame=f, offset=ghost_off(g))
            H.set_convoy(s, frame=f)
            for ob in self.ghost_smoke:                      # QA: no cyan bubble discs over the funnels
                ob.hide_render = True
                ob.keyframe_insert("hide_render", frame=f)
            H.set_lead_marker(lead_k(g), frame=f)
            H.set_ghost_marker(gmark_k(g) if shot != 17 else 0.0, frame=f)
            H.set_hit(-1.0, frame=f)
            if shot == 18 and g >= G19 - 26:               # QA: the buoy lamp is a small steady glow, not a flare disc
                H._keyval(H.STATE["M"]["halo_cyan"], "cyan_k", 0.35 * gmark_k(g), f)
            for L in self.lamps:                              # QA-art: no glare streaks from the buoy lamps on the water
                L.data.energy = 0.0
                L.data.keyframe_insert("energy", frame=f)
            H.periscope_overlay(pov, frame=f)
            loc, look, lens = cam_of(shot, g, self.eye)
            self.key_cam(f, loc, look, lens=lens)
            for ob in self.near_eye:
                ob.hide_render = pov
                ob.keyframe_insert("hide_render", frame=f)

    def report(self, shot, g):
        loc, look, lens = cam_of(shot, g, self.eye)
        v = look - loc
        return dict(shot=shot, g=g, cam=[round(c, 3) for c in loc], lens=round(lens, 2), s=round(s_of(g), 3), u=round(u_of(g), 4),
                    ghost=round(ghost_k(g), 3), lead=round(lead_k(g), 3), pitch=round(math.degrees(math.atan2(v.z, math.hypot(v.x, v.y))), 1))

    def render(self, shot, gs, out_dir, scale=1.0, samples=12, threads=2):
        return C.Take.render(self, [bf(shot, g) for g in gs], out_dir, scale=scale, samples=samples, threads=threads)


if __name__ == "__main__":
    cmd = sys.argv[1]
    shots = [int(s) for s in sys.argv[2].split(",")]
    if cmd in ("probe", "stills"):
        Tk = Take("preview")
        for shot in shots:
            gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
            if not gs:
                continue
            Tk.pose(shot, gs)
            for g in gs:
                print(json.dumps(Tk.report(shot, g)), flush=True)
                if cmd == "stills":
                    out = sys.argv[4]
                    scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
                    samples = int(sys.argv[6]) if len(sys.argv) > 6 else 6
                    st = Tk.render(shot, [g], out, scale=scale, samples=samples)[0]
                    os.replace(st["path"], os.path.join(out, "s%d_g_%04d.png" % (shot, g)))
                    print("shot %d g %d  %.1f s wall %.1f cpu" % (shot, g, st["wall"], st["cpu"]), flush=True)
    elif cmd == "final":
        scale = float(sys.argv[4]) if len(sys.argv) > 4 else 1.0
        samples = int(sys.argv[5]) if len(sys.argv) > 5 else 12
        C.final_loop(lambda q, shot=17: Take(q), shots, sys.argv[3], RANGES, HERE, scale=scale, samples=samples)
