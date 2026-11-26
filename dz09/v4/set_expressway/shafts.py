"""shafts.py -- light cones (sodium masts, rescue floodlight) as a depth-tested splat in post instead of transparent
lathe cards in Cycles (review fix: the 10 sodium cone cards plus the flood beam cost about 40 % of a final frame,
because every camera ray in the cones crossed two transparent surfaces).

collect(scene, cam, res)  -> list of shafts (bpy side; projects disks along each cone axis to pixels)
splat(rgb, z, shafts, s)  -> rgb + light (numpy side; called by post.process after fog)

Each cone is sampled as N cross-section disks from the lamp head (t = 0) to its end on the deck (t = 1). A disk adds
a soft radial gaussian of the cone colour wherever the scene behind it is farther than the disk (so cars, Kong and
the barriers in front of a cone hide it, and the cone stops at the road). The density profile matches the cards:
brightest near the head, fading toward the ground."""
import math
import numpy as np

N_DISK = 36


def collect(scene, cam, objects):
    """objects: the cone/beam objects (hidden from the render). Each needs custom props shaft_r0, shaft_r1,
    shaft_len, shaft_col (rgb x strength) and its local -Z... we read the lathe axis: local +Z points from the
    base (z = -len) to the apex (z = 0)."""
    import bpy
    from mathutils import Vector
    from bpy_extras.object_utils import world_to_camera_view as w2c
    W = scene.render.resolution_x; H = scene.render.resolution_y
    fpx = cam.data.lens / cam.data.sensor_width * max(W, H)
    cinv = cam.matrix_world.inverted()
    out = []
    for ob in objects:
        L = float(ob["shaft_len"]); r0 = float(ob["shaft_r0"]); r1 = float(ob["shaft_r1"])
        col = list(ob["shaft_col"])
        M = ob.matrix_world
        xs, ys, zs, rs, ws = [], [], [], [], []
        for i in range(N_DISK):
            t = (i + 0.5) / N_DISK
            p = M @ Vector((0, 0, -L * t))
            pc = cinv @ p
            d = -pc.z
            if d < 0.3: continue
            v = w2c(scene, cam, p)
            r = (r0 + (r1 - r0) * t) * fpx / d
            xs.append(v.x * W); ys.append((1 - v.y) * H); zs.append(d); rs.append(r)
            # the card adds a(t') = a_top t'^1.7 (t' = 1 - t, 1 at the head) at each of its two crossings, whatever the
            # cone's width there. Seen from the side, about 2 r / spacing disks overlap a pixel, so each disk carries
            # 2 a(t') x spacing / (2 r) to give the same sum.
            rw = r0 + (r1 - r0) * t
            ws.append(2.0 * (1 - t) ** 1.7 * (L / N_DISK) / max(rw, 0.05))
        if xs:
            out.append(dict(name=ob.name, x=xs, y=ys, z=zs, r=rs, w=ws, col=col))
    return out


def splat(rgb, z, shafts, gain=1.0):
    H, W = z.shape
    acc = np.zeros((H, W, 3), np.float32)
    for sh in shafts:
        col = np.array(sh["col"], np.float32)
        for x, y, d, r, w in zip(sh["x"], sh["y"], sh["z"], sh["r"], sh["w"]):
            R = int(math.ceil(r * 1.6)) + 1
            x0, x1 = max(0, int(x) - R), min(W, int(x) + R + 1)
            y0, y1 = max(0, int(y) - R), min(H, int(y) + R + 1)
            if x1 <= x0 or y1 <= y0: continue
            yy, xx = np.mgrid[y0:y1, x0:x1].astype(np.float32)
            q = ((xx - x) ** 2 + (yy - y) ** 2) / max(r * r, 1e-3)
            g = np.exp(-1.6 * q) * (q < 2.56)
            # a disk of radius r seen face-on: path length through it ~ 2 r (world) -> the gaussian already spreads it
            vis = (z[y0:y1, x0:x1] > d).astype(np.float32)
            acc[y0:y1, x0:x1] += (g * vis * w)[..., None] * col
    return rgb + acc * gain
