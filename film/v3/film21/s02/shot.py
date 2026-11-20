#!/usr/bin/env python3
"""shot.py -- film 21 take s02: shots 4-7, g 159..418 (+ 7 in-handle g 152..158, + 6 out-handle g 418..423).

  shot 4  g 152..234  valley_wide   establishing, crane down + push 6 %/s                       (in: D11 from s01, handle frames 152..158)
  shot 5  g 235..303  camp_wide     English parade past tents and banners, slide + push         (303 = last frame of the internal dissolve)
  shot 6  g 293..359  hill_low      Scots with long spears against the sky, pull-out 7 %/s     (internal D11 at g 298: frames 293..303 blend shot 5 -> 6)
  shot 7  g 360..423  valley_river  eye level over the river from the south bank, push + slide  (out handle 418..423)

The dissolve 5 -> 6 is made by blend.py from the raw frames of both shots.  One location per process: run one shot per process.

    python3 shot.py probe <shot> <g list>                       camera + heads numbers only
    python3 shot.py stills <shot> <g list> <out_dir> [scale] [samples]
    python3 shot.py final <shot> <g list> [samples]             raw/s<shot>/g_%04d.png (resumable)
"""
import math, os, sys, json, time

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import c21 as C                                            # noqa: E402
import numpy as np                                         # noqa: E402
from mathutils import Vector                               # noqa: E402

K, cast21, bpy = C.K, C.cast21, C.bpy
lerp, clamp, sine, mixu, vl, snap_u = C.lerp, C.clamp, C.sine, C.mixu, C.vl, C.snap_u
SC = C.SC
S21 = cast21.STORY21

RANGES = {4: (152, 234), 5: (235, 303), 6: (293, 359), 7: (360, 423)}
PRESET = {4: "valley_wide", 5: "camp_wide", 6: "hill_low", 7: "valley_river"}
CUTS = (235, 298, 360)


def u_of(g, a, b):
    return sine((g - a) / float(b - a)) if g > a else 0.0


# ----------------------------------------------------------------------------- cameras
def cam_of(shot, g):
    if shot == 4:
        return cam4(g)
    if shot == 5:
        return cam5(g)
    if shot == 6:
        return cam6(g)
    return cam7(g)


def sn(g, g0, g1):
    return snap_u((g - g0) / float(g1 - g0))


# shot 4: crane down + push 6 %/s toward the bridge / loop, one snap (re-frame onto the loop, 14 f) on "เจ็ดร้อยกว่าปีก่อน" (6.57 s = g 200)
G4_SNAP = (188, 200)


def cam4(g):
    x = (g - 152) / float(234 - 152)
    uc = mixu(x, 0.2)
    ul = 0.2 * uc + 0.8 * sn(g, *G4_SNAP)
    c0, c1 = (445.0, 244.0, 361.0), (366.0, 200.0, 290.0)
    l0, l1 = (160.0, 62.0, 0.0), (-84.0, 96.0, 0.0)
    return vl(c0, c1, uc), vl(l0, l1, ul)


# shot 5: camp_wide: drift slide + push, snap re-frame (pan left + 6 m push, 13 f) on "เต็มทุ่ง" (9.26 s = g 281)
G5_SNAP = (278, 290)


def cam5(g):
    x = (g - 235) / float(303 - 235)
    uc = mixu(x, 0.25)
    us = sn(g, *G5_SNAP)
    f, lf = (0.898, 0.439), (-0.439, 0.898)
    c0 = (-78.0, -96.0, 9.2)
    c1 = (c0[0] + f[0] * 9 + lf[0] * 6, c0[1] + f[1] * 9 + lf[1] * 6, 8.6)
    c = vl(c0, c1, uc)
    c = (c[0] + f[0] * 5 * us, c[1] + f[1] * 5 * us, c[2])
    l0 = (12.0 - lf[0] * 8, -52.0 - lf[1] * 8, 2.0)             # starts looking a little to the right of the preset line
    l1 = (12.0 + f[0] * 4 + lf[0] * 8, -52.0 + f[1] * 4 + lf[1] * 8, 2.0)
    lk = vl(l0, l1, 0.25 * uc + 0.75 * us)
    return c, lk


# shot 6: hill_low: pull-out 7 %/s + slide, snap re-frame / pull-out (x1.25, 13 f) on "ส่วนใหญ่เดินเท้า" (10.59 s = g 321)
G6_SNAP = (320, 332)


def cam6(g):
    x = (g - 293) / float(359 - 293)
    uc = mixu(x, 0.2)
    us = sn(g, *G6_SNAP)
    fw = (22.0, 22.0); n = math.hypot(*fw); fw = (fw[0] / n, fw[1] / n); rt = (fw[1], -fw[0])
    c = (118.0 - fw[0] * (1.6 * uc + 1.6 * us) + rt[0] * 1.0 * uc, 112.0 - fw[1] * (1.6 * uc + 1.6 * us) + rt[1] * 1.0 * uc)
    la = (140.0 + rt[0] * 7.0, 134.0 + rt[1] * 7.0, 17.4)          # start: Scots pushed to the right of frame
    lb = (140.0 - rt[0] * 2.5, 134.0 - rt[1] * 2.5, 17.4)
    return (c[0], c[1], K.ground(118.0, 112.0) + 1.40), vl(la, lb, 0.25 * uc + 0.75 * us)


# shot 7: valley_river: drift right + forward along the spit, snap pan across the river to the hill (13 f) on "อีกฝั่งของแม่น้ำ" (12.73 s = g 385)
G7_SNAP = (382, 394)


def cam7(g):
    x = (g - 360) / float(423 - 360)
    uc = mixu(x, 0.2)
    us = sn(g, *G7_SNAP)
    z0 = float(K.ground(38.0, -24.0)) + 1.65
    fw, rt = (0.79, 0.613), (0.613, -0.79)
    c0 = (38.0, -24.0, z0)
    c1 = (c0[0] + rt[0] * 2.4 + fw[0] * 1.8, c0[1] + rt[1] * 2.4 + fw[1] * 1.8, z0)
    l0 = (105.0 + rt[0] * 16.0, 28.0 + rt[1] * 16.0, 4.0)
    l1 = (105.0 - rt[0] * 16.0, 28.0 - rt[1] * 16.0, 4.0)
    return vl(c0, c1, uc), vl(l0, l1, 0.25 * uc + 0.75 * us)


# ----------------------------------------------------------------------------- stage
def idle(g, k=0, lean=1.2, roll=1.5):
    return dict(lean=lean * math.sin(g * 0.071 + k * 1.7), head_roll=roll * math.sin(g * 0.053 + k * 2.3), blink=C.blink_at(g, 84 + 7 * k, 11 * k))


SPEAR_SC = 1.1


def spear_pose(p, sc=SPEAR_SC):
    for k in ("prop_r", "prop_l"):
        if isinstance(p.get(k), dict) and p[k].get("type") == "spear21":
            p[k] = dict(p[k], scale=sc)
    return p


class Member(object):
    """one cast card: stand point (fixed or walking), base pose, optional per-frame pose function."""

    def __init__(self, actor, xyz_fn, base, k, fn=None, mirror=False, riding=False):
        self.a, self.xyz_fn, self.base, self.k, self.fn, self.mirror, self.riding = actor, xyz_fn, base, k, fn, mirror, riding


def fixed(xyz):
    return lambda g: xyz


def stage_6(Tk):
    """Scots on the shelf: long spears up against the sky; three more up near the crest where the spears reach the sky."""
    A, pr = Tk.A, Tk.pr
    mk = A["marks"]
    cast = [("s1", "scot_b", "scot_b_fold_spear", 0), ("s2", "scot_a", "scot_a_fold_spear", 1), ("horn", "scot_horn", "scot_horn_fold_spear", 2),
            ("w", "wallace", "wallace_stand_spear", 3), ("s3", "scot_c", "scot_c_fold_spear", 4)]
    out = []
    for nm, c, pose, k in cast:
        x, y, z = mk[nm][:3]
        out.append(Member(Tk.add_actor(nm, c), fixed((x, y, z)), pose, k))
    # crest line: small Scots whose spears stand against the sky
    far = [("c1", "scot_a_v1", "scot_a_fold_spear", 16.5, 640), ("c2", "scot_c", "scot_c_fold_spear", 16.0, 520), ("c3", "scot_b_v2", "scot_b_fold_spear", 15.5, 400),
           ("c4", "scot_a_v2", "scot_a_fold_spear", 17.0, 690), ("c5", "scot_b", "scot_b_fold_spear", 16.0, 300), ("c6", "scot_c_v1", "scot_c_fold_spear", 15.5, 190)]
    for i, (nm, cast_, pose, d, xp) in enumerate(far):
        x, y = K.at_px(pr, d, xp)
        z = Tk.ground(x, y)
        base = pose
        out.append(Member(Tk.add_actor(nm, cast_.split("_v")[0]), fixed((x, y, z)), base, 5 + i,
                          fn=(lambda p, v=cast_: dict(p, variant21=int(v.split("_v")[1])) if "_v" in v else p)))
    return out


def stage_5(Tk):
    """camp parade: caparisoned knights ride to the bridge (screen-left) past the tents; foot soldiers idle in the tent lane."""
    Tk.hide(["parade"])
    pr = Tk.pr
    out = []
    left = (-0.439, 0.898)
    riders = [("r1", "knight_a_mtd", "knight_a_mounted", 31.0, 420, "red"), ("r2", "knight_b_mtd", "knight_b_mounted", 35.0, 340, "blue"),
              ("r3", "knight_a_open_mtd", "knight_a_mounted", 39.0, 270, "gold"), ("r4", "knight_b_great_mtd", "knight_b_mounted", 43.0, 200, "red"),
              ("r5", "knight_a_mtd", "knight_a_mounted", 47.0, 130, "blue"), ("r6", "knight_b_mtd", "knight_b_mounted", 34.0, 470, "gold"),
              ("r7", "knight_a_open_mtd", "knight_a_mounted", 37.0, 560, "blue"), ("r8", "knight_b_great_mtd", "knight_b_mounted", 41.0, 600, "red"),
              ("r9", "knight_a_mtd", "knight_a_mounted", 45.0, 520, "gold"), ("r10", "knight_b_mtd", "knight_b_mounted", 50.0, 450, "blue")]
    for i, (nm, cast_, base, d, xp, cap) in enumerate(riders):
        x0, y0 = K.at_px(pr, d, xp)
        def xyz(g, x0=x0, y0=y0, i=i):
            t = (g - 235) / 30.0
            x, y = x0 + left[0] * 1.35 * t, y0 + left[1] * 1.35 * t
            return (x, y, Tk.ground(x, y))
        def fn(p, g=None, cap=cap, i=i):
            return dict(p, mode21="walk", horse21=cap, mirror=True)
        out.append(Member(Tk.add_actor(nm, cast_), xyz, base, i, fn=fn, mirror=True, riding=True))
    foot = [("f1", "footman_a", 50.0, 110, 0), ("f2", "footman_b", 53.0, 190, 1), ("f3", "footman_a", 47.0, 330, 2), ("f4", "footman_b", 55.0, 440, 3),
            ("f5", "footman_a", 51.0, 540, 1), ("f6", "footman_a", 58.0, 610, 2), ("f7", "footman_b", 36.0, 600, 0), ("f8", "footman_a", 33.0, 70, 3), ("f9", "footman_a", 41.0, 670, 2), ("f10", "footman_b", 44.0, 380, 1), ("f11", "footman_a", 39.0, 150, 2), ("f12", "footman_b", 46.0, 290, 3)]
    for i, (nm, cast_, d, xp, v) in enumerate(foot):
        x, y = K.at_px(pr, d, xp)
        z = Tk.ground(x, y)
        out.append(Member(Tk.add_actor(nm, cast_), fixed((x, y, z)), cast_ + "_stand", 10 + i,
                          fn=(lambda p, g=None, v=v, i=i: dict(p, variant21=v + 1, mirror=bool(i % 2)))))
    return out


def stage_7(Tk):
    """south bank: two footmen at the water's edge, watching the hill (right of frame, on the spit)."""
    pr = Tk.pr
    out = []
    watchers = [("w1", "footman_a", 6.6, 540, 0, False), ("w2", "footman_b", 7.0, 625, 1, False)]
    for i, (nm, cast_, d, xp, v, mir) in enumerate(watchers):
        x, y = K.at_px(pr, d, xp)
        z = Tk.ground(x, y)
        out.append(Member(Tk.add_actor(nm, cast_), fixed((x, y, z)), cast_ + "_stand_arms_down", i,
                          fn=(lambda p, g=None, v=v, mir=mir: dict(p, variant21=v + 1, mirror=True))))
    return out


def stage_actors(Tk, shot):
    return {5: stage_5, 6: stage_6, 7: stage_7}.get(shot, lambda T: [])(Tk)


class Shot(object):
    def __init__(self, shot, quality="final", samples=24, threads=2):
        self.shot = shot
        self.Tk = C.Take(PRESET[shot], quality=quality, samples=samples, threads=threads)
        self.setup()

    def setup(self):
        Tk, shot = self.Tk, self.shot
        self.cast = stage_actors(Tk, shot)

    def pose(self, gs):
        Tk, shot = self.Tk, self.shot
        for g in gs:
            f = C.bf(g)
            loc, look = cam_of(shot, g)
            Tk.key_cam(f, loc, look)
            Tk.scene.frame_set(f)
            K.set_flutter(g / 30.0); K.set_smoke(g / 30.0); K.set_flow(g / 30.0)
        for g in gs:
            f = C.bf(g)
            Tk.scene.frame_set(f)
            for m in self.cast:
                m.a.place(f, m.xyz_fn(g), scale=SC)
                p = dict(S21[m.base][1]) if m.base in S21 else dict(S21[m.base.replace("_v1", "").replace("_v2", "")][1])
                if m.riding:
                    p.update(gait=((g + 9 * m.k) / 40.0) % 1.0, t=((g + 13 * m.k) / 70.0) % 1.0, blink=C.blink_at(g, 90 + 5 * m.k, 13 * m.k),
                             lean=0.8 * math.sin(g * 0.09 + m.k))
                else:
                    p.update(idle(g, m.k))
                if m.fn:
                    p = m.fn(p)
                m.a.pose(f, spear_pose(p, SPEAR_SC), camera=Tk.cam)
        Tk.render_sprites([C.bf(g) for g in gs])

    def heads(self, g):
        f = C.bf(g)
        return {m.a.name: Tk_head(self.Tk, m.a.name, f) for m in self.cast}


def Tk_head(Tk, name, f):
    return Tk.head_px(name, f)


def main():
    cmd, shot = sys.argv[1], int(sys.argv[2])
    gs = [g for g in C.parse(sys.argv[3]) if RANGES[shot][0] <= g <= RANGES[shot][1]]
    if cmd == "probe":
        S = Shot(shot, "draft", 6)
        S.pose(gs)
        for g in gs:
            loc, look = cam_of(shot, g)
            print(g, [round(v, 1) for v in loc], S.heads(g), flush=True)
    elif cmd == "stills":
        out = sys.argv[4]
        scale = float(sys.argv[5]) if len(sys.argv) > 5 else 0.5
        samples = int(sys.argv[6]) if len(sys.argv) > 6 else 8
        os.makedirs(out, exist_ok=True)
        S = Shot(shot, "draft" if scale < 1 else "final", samples)
        S.pose(gs)
        for g in gs:
            dt = S.Tk.render_frame(g, os.path.join(out, "s%d_g%04d.png" % (shot, g)))
            print("shot %d g %d  %.1f s  heads %s" % (shot, g, dt, S.heads(g)), flush=True)
    elif cmd == "final":
        samples = int(sys.argv[4]) if len(sys.argv) > 4 else 24
        out = os.path.join(HERE, "raw", "s%d" % shot)
        os.makedirs(out, exist_ok=True)
        todo = []
        for g in gs:
            png, js = os.path.join(out, "g_%04d.png" % g), os.path.join(out, "g_%04d.json" % g)
            if os.path.exists(png) and os.path.exists(js) and json.load(open(js)).get("samples") == samples:
                continue
            todo.append(g)
        print("final: shot %d, %d to render, %d done" % (shot, len(todo), len(gs) - len(todo)), flush=True)
        if not todo:
            return
        S = Shot(shot, "final", samples)
        S.pose(todo)
        for g in todo:
            png = os.path.join(out, "g_%04d.png" % g)
            dt = S.Tk.render_frame(g, png + ".tmp.png")
            os.replace(png + ".tmp.png", png)
            json.dump(dict(shot=shot, g=g, samples=samples, wall=round(dt, 1), heads=S.heads(g), cam=[round(v, 2) for v in cam_of(shot, g)[0]]), open(png[:-4] + ".json", "w"))
            print("shot %d g %d  %.1f s" % (shot, g, dt), flush=True)


if __name__ == "__main__":
    main()
