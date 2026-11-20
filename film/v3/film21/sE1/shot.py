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
CAST = [("e0", "footman_a", "footman_a_mime_hoe", 0.0), ("e1", "footman_b", "footman_b_laughing", 2.1), ("e2", "knight_b", "knight_b_point_laugh", 4.2),
        ("e3", "footman_a", "footman_a_point_laugh", 1.2), ("e4", "footman_b", "footman_b_point_laugh", 3.3)]
SCOTS = [("s1", "s1", "scot_b", "scot_b_fold_spear"), ("s2", "s2", "scot_a", "scot_a_chew_grass"), ("w", "w", "wallace", "wallace_calm"),
         ("s3", "s3", "scot_c", "scot_c_scratch_nose"), ("s4", "s4", "scot_a", "scot_a_fold_spear")]


def keys(A):
    pb = A["cams"]["camp_bank"]; he = A["cams"]["hill_eye"]
    hl, hk = np3(he[0]), np3(he[1])
    return [(G0, "P_BANK"),
            (G0 + 14, (-72.0, -6.0, 13.0), (-30.0, 20.0, 4.0), 24.0),
            (G0 + 28, (-24.0, 22.0, 30.0), (40.0, 85.0, 10.0), 22.0),
            (G0 + 38, (60.0, 78.0, 30.0), (120.0, 128.0, 18.0), 22.0),
            (G_SNAP - 2, (104.0, 108.0, 25.0), (136.0, 138.0, 20.0), 22.0),
            (G_SNAP + 6, "hill_eye"),
            (G1, (hl[0] - 0.5 + 0.9, hl[1] - 0.5 - 0.9, hl[2] - 0.1), (hk[0] + 0.6, hk[1] - 0.3, hk[2] + 0.1), 22.0)]


def np3(v):
    return (float(v[0]), float(v[1]), float(v[2]))


def cam_fn(A):
    ks = keys(A); pb = A["cams"]["camp_bank"]
    cam0 = Vector(pb[0]); look0 = Vector(pb[1]); f = look0 - cam0; fh = Vector((f.x, f.y, 0)).normalized()

    def fn(g):
        if g < G0:                                        # handle: team 4's pull-out continues into P_BANK (camera a little closer, backing away)
            loc = cam0 + fh * 0.012 * (G0 - g)
            return dict(loc=tuple(loc), look=tuple(look0), lens=pb[2], vivid=K.VIVID["camp_bank"])
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
            if nm == "e0":
                p["arm_l"] = dict(p.get("arm_l") or {}, hand=(0.34, 0.31 + 0.16 * math.sin(g * 0.6)))     # the hoeing stroke
                p["lean"] = p.get("lean", 0) + 4 * math.sin(g * 0.3)
            x, y, z = bank_marks[nm][:3]
            out[nm] = ((x, y, z + dy * K.D), p)
        for nm, mk, cst, base in SCOTS:
            p = dict(cast21.STORY21[base][1]); x, y, z = hm[mk][:3]
            p["lean"] = p.get("lean", 0) + 1.5 * math.sin(g * 0.07 + len(nm)); p["head_roll"] = 1.5 * math.sin(g * 0.05 + len(nm))
            p["blink"] = blink(g, [850 + 7 * len(nm), 872])
            if nm == "w":
                p = dict(cast21.STORY21["wallace_eyebrow"][1]) if g >= 848 else dict(cast21.STORY21["wallace_calm"][1])
                p["blink"] = blink(g, [845, 872])
            out[nm] = ((x, y, z), p)
        return out
    return fn


def post(g, path):
    if G_SNAP <= g < G_SNAP + 6:
        C.speed_lines(path, strength=1.0 - 0.12 * (g - G_SNAP), seed=g)


if __name__ == "__main__":
    bpy.ops.wm.read_factory_settings(use_empty=True)
    A = K.build_world(["camp_bank", "hill_eye"], over=dict(shaft_k=0.5))
    pb = A["cams"]["camp_bank"]
    bank = {}
    for nm, d_, xp, typ in EXTRAS:
        bank[nm] = K.mark_px(tuple(pb[0]), tuple(pb[1]), pb[2], d_, xp, typ)

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
