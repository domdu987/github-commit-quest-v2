#!/usr/bin/env python3
"""shot.py -- film 21 segment E1 (g 793-885, D6 in at P_BANK, CUT out at 885), worlds camp_bank + hill_eye.
Starts EXACTLY at P_BANK (the camp_bank camera) with 3 handle frames (790-792) that continue team 4's pull-out into it.  The laughing English on the
south bank point across, one mimes hoeing (bounce).  The camera RISES and flies across the river and up the hill; on "พวกไอ้ชาวนาบนเนิน" (27.80, g 837)
it lands with a SNAP punch-in on the Scots line (6 frames of speed lines, 2-frame shake).  The Scots are unbothered; Wallace raises an eyebrow.
    python3 shot.py stills a:b[:step] out [scale] [samples]   |   python3 shot.py final a:b[:step] [scale] [samples]
"""
import os, sys, math
import c21 as C
from c21 import np
K, cast21, bpy = C.K, C.cast21, C.bpy
from mathutils import Vector
ez, lerp, blink = C.ez, C.lerp, C.blink
HERE = C.HERE
G0, G1 = 793, 885
G_FIRST = G0 - 3
G_SNAP = C.g_of(27.80)            # 837: punch-in
EXTRAS = [("e0", 8.0, 470, "foot"), ("e1", 6.2, 335, "foot"), ("e2", 6.7, 440, "knight"), ("e3", 7.8, 390, "foot"), ("e4", 9.0, 250, "foot")]
# English are CRIMSON only (set3d21/API.md section 13): footman_a (russet gambeson), knight_a and knight_a_open (red surcoats); no blue tunics.
CAST = [("e0", "footman_a", "footman_a_mime_hoe", 0.0), ("e1", "knight_a", "knight_a_laughing", 2.1), ("e2", "knight_a_open", "knight_a_open_point_laugh", 4.2),
        ("e3", "footman_a", "footman_a_point_laugh", 1.2), ("e4", "knight_a", "knight_a_point_laugh", 3.3),
        # the close group the camera slides past in g 793-820 (just outside the P_BANK frustum): one hoeing mime, big pointing arms, bounce
        ("c0", "footman_a", "footman_a_mime_hoe", 0.7), ("c1", "knight_a", "knight_a_point_laugh", 2.6), ("c2", "knight_a_open", "knight_a_open_point_laugh", 4.8),
        ("c3", "footman_a", "footman_a_point_laugh", 5.7)]
SCOTS = [("s1", "s1", "scot_b", "scot_b_fold_spear"), ("s2", "s2", "scot_a", "scot_a_chew_grass"), ("w", "w", "wallace", "wallace_calm"),
         ("s3", "s3", "scot_c", "scot_c_scratch_nose"), ("s4", "s4", "scot_a", "scot_a_fold_spear")]


def group_geo(A):
    """world geometry of the close bank group (just outside the P_BANK frustum, the camera slides past it in g 793-820)."""
    pb = A["cams"]["camp_bank"]; cam0 = Vector(pb[0]); look0 = Vector(pb[1]); f = look0 - cam0
    fh = Vector((f.x, f.y, 0)).normalized(); rh = Vector((fh.y, -fh.x, 0))
    B = cam0 + fh * 4.4 + rh * 3.3
    return cam0, look0, fh, rh, B


def group_marks(A):
    cam0, look0, fh, rh, B = group_geo(A)
    out = {}
    for nm, lat, fw in (("c0", -0.9, 0.5), ("c1", 0.1, 0.0), ("c2", 1.1, -0.35), ("c3", 2.0, 0.45)):
        p = B + rh * lat + fh * fw
        out[nm] = (p.x, p.y, float(K.ground(p.x, p.y)))
    return out


def keys(A):
    pb = A["cams"]["camp_bank"]; he = A["cams"]["hill_eye"]
    hl, hk = np3(he[0]), np3(he[1])
    cam0, look0, fh, rh, B = group_geo(A)
    gm = group_marks(A); gc = Vector((sum(v[0] for v in gm.values()) / 4, sum(v[1] for v in gm.values()) / 4, 1.35))
    mid = gc.lerp(look0, 0.0)
    k803 = cam0 + rh * 1.1 + fh * 0.3 + Vector((0, 0, 0.25)); l803 = look0.lerp(gc, 0.3)
    k813 = cam0 + rh * 2.5 + fh * 0.9 + Vector((0, 0, 0.7)); l813 = gc
    return [(G0, "P_BANK"),
            (G0 + 10, tuple(k803), tuple(l803), 25.0),
            (G0 + 20, tuple(k813), tuple(l813), 24.0),
            (G0 + 28, (-70.0, -5.0, 12.0), (-30.0, 18.0, 3.0), 22.0),
            (G0 + 35, (-20.0, 24.0, 30.0), (40.0, 85.0, 10.0), 22.0),
            (G_SNAP - 4, (62.0, 80.0, 30.0), (120.0, 128.0, 18.0), 22.0),
            (G_SNAP - 2, (104.0, 108.0, 25.0), (136.0, 138.0, 20.0), 22.0),
            (G_SNAP + 6, "hill_eye"),
            (G1, (hl[0] + 0.35, hl[1] - 0.35, hl[2] - 0.05), (hk[0] + 0.25, hk[1] - 0.1, hk[2] + 0.05), 22.0)]


def np3(v):
    return (float(v[0]), float(v[1]), float(v[2]))


def cam_fn(A):
    ks = keys(A); pb = A["cams"]["camp_bank"]
    cam0 = Vector(pb[0]); look0 = Vector(pb[1]); f = look0 - cam0; fh = Vector((f.x, f.y, 0)).normalized()

    def fn(g):
        if g < G0:                                        # handle: team 4's pull-out continues into P_BANK (camera a little closer, backing away)
            loc = cam0 + fh * 0.012 * (G0 - g)
            return dict(loc=tuple(loc), look=tuple(look0), lens=pb[2], vivid=K.VIVID["camp_bank"])
        if g >= G_SNAP - 2:                              # the SNAP: fast punch-in onto hill_eye, easing out with no overshoot, then a slow drift
            a = next(k for k in ks if k[0] == G_SNAP - 2); he = A["cams"]["hill_eye"]; L = np3(he[0]); T = np3(he[1])
            t = min(1.0, (g - (G_SNAP - 2)) / 8.0); te = 1 - (1 - t) ** 3
            la, ta = Vector(a[1]), Vector(a[2])
            loc = la.lerp(Vector(L), te); look = ta.lerp(Vector(T), te)
            d = ez((g - (G_SNAP + 6)) / float(G1 - G_SNAP - 6)) if g > G_SNAP + 6 else 0.0
            loc = loc + Vector((0.35, -0.35, -0.05)) * d; look = look + Vector((0.25, -0.1, 0.05)) * d
            c = dict(loc=tuple(loc), look=tuple(look), lens=22.0, vivid=K.VIVID["hill_eye"])
        else:
            c = K.cam_path(None, ks, g)
        loc, look = Vector(c["loc"]), Vector(c["look"])
        if G_SNAP <= g <= G_SNAP + 1:                     # 2-frame shake
            s = 1 if g == G_SNAP else -1
            look = look + Vector((0.5 * s, -0.4 * s, 0.35 * s))
        return dict(loc=tuple(loc), look=tuple(look), lens=c["lens"], vivid=c["vivid"])
    return fn


def act_fn(A, bank_marks):
    hm = A["marks"]["hill_eye"]

    def fn(g):
        out = {}
        for nm, cst, base, ph in CAST:
            p = dict(cast21.STORY21[base][1])
            p, dy = cast21.laugh(p, g, phase=ph)
            if nm == "c1" or nm == "c2" or nm == "c3":       # big pointing arm across the river
                p["arm_r"] = dict(p.get("arm_r") or {}, hand=(0.95, -0.05 + 0.05 * math.sin(g * 0.5)), bend=0.15, stretch=1.1, shape="point")
            if nm in ("e0", "c0"):
                amp = 0.3 if nm == "c0" else 0.16
                p["arm_l"] = dict(p.get("arm_l") or {}, hand=(0.34, 0.31 + amp * math.sin(g * 0.6)))     # the hoeing stroke
                p["lean"] = p.get("lean", 0) + 4 * math.sin(g * 0.3)
            x, y, z = bank_marks[nm][:3]
            out[nm] = ((x, y, z + dy * K.D), p)
        for nm, mk, cst, base in SCOTS:
            p = dict(cast21.STORY21[base][1]); x, y, z = hm[mk][:3]
            p["lean"] = p.get("lean", 0) + 1.5 * math.sin(g * 0.07 + len(nm)); p["head_roll"] = 1.5 * math.sin(g * 0.05 + len(nm))
            p["blink"] = blink(g, [850 + 7 * len(nm), 872])
            if nm == "w":
                p = dict(cast21.STORY21["wallace_eyebrow"][1]) if g >= 848 else dict(cast21.STORY21["wallace_calm"][1])
                if g >= 848:
                    p["head_roll"] = 7.0 * ez((g - 848) / 4.0) * (1.0 if g < 868 else 0.7); p["pitch"] = -0.35; p["lean"] = -3.0 * ez((g - 848) / 4.0)
                p["blink"] = blink(g, [845, 872])
            out[nm] = ((x, y, z), p)
        return out
    return fn


def post(g, path):
    if G_SNAP <= g < G_SNAP + 6:
        C.speed_lines(path, strength=1.0 - 0.12 * (g - G_SNAP), seed=g)


if __name__ == "__main__":
    bpy.ops.wm.read_factory_settings(use_empty=True)
    K.PRESETS["hill_eye"]["fg_list"] = [("spear", 2.6, 12, (0.35, 0.2)), ("gorse", 2.4, 640, 0.55)]     # QA-tech: the pole must not cross the right-most Scot's face
    A = K.build_world(["camp_bank", "hill_eye"], over=dict(shaft_k=0.5))
    import numpy as _np
    cam0_, look0_, fh_, rh_, B_ = group_geo(A); rs_ = _np.random.RandomState(31); Bp = K.Batch(91)
    for fw, lt in ((3.2, 1.6), (6.0, 5.2), (4.0, 7.0), (2.6, 4.9), (5.0, 2.3)):
        p_ = cam0_ + fh_ * fw + rh_ * lt; K.barrel(Bp, (p_.x, p_.y, float(K.ground(p_.x, p_.y))), rs=rs_)
    for fw, lt in ((2.4, 2.4), (3.4, 6.2), (5.6, 4.0)):
        p_ = cam0_ + fh_ * fw + rh_ * lt; K.spear(Bp, (p_.x, p_.y, float(K.ground(p_.x, p_.y))), tilt=(0.05, 0.12), h=3.0)
    Bp.finalize("e1_props", shadow=False)
    pb = A["cams"]["camp_bank"]
    bank = {}
    for nm, d_, xp, typ in EXTRAS:
        bank[nm] = K.mark_px(tuple(pb[0]), tuple(pb[1]), pb[2], d_, xp, typ)
    bank.update(group_marks(A))

    class W(C.Take):
        def __init__(self):
            pass
    T = W(); T.A = A; T.cam = bpy.context.scene.camera; T.cam.data.dof.use_dof = False; T.cam.data.clip_start = 0.1
    K.setup_render(bpy.context.scene, "final")
    T.cam_fn, T.act_fn, T.g0, T.work, T.post_fn = cam_fn(A), act_fn(A, bank), G_FIRST, os.path.join(HERE, "work"), post
    T.cast = {n: c for n, c, _, _ in CAST}; T.cast.update({n: c for n, _, c, _ in SCOTS}); T.acts = {}; T.vivid = {}
    for nm, cst in T.cast.items():
        a = C.actors.Actor(nm, cst); a.build(C.sprites.DEFAULT_CANVAS[cst], os.path.join(T.work, "sprites"), contact=True); a.head_flip = False; T.acts[nm] = a
    T.main(sys.argv, (G_FIRST, G1))
