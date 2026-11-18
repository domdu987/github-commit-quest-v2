#!/usr/bin/env python3
"""post.py -- raw Blender frames -> finished picture frames (no captions; assemble.py burns those last).

    python3 post.py <raw_dir> <out_frames_dir> [--no-streak]

What happens outside Blender, and nothing else:
  * camera streak on the fast frames (the whip pan between shots 2 and 3, the snap pull-out from the insert, the snap
    pushes): the picture is averaged along the 2D motion that the camera gives the set during an exposure of SHUTTER
    frames.  In the whip the whole frame is streaked; elsewhere the plate (the same 3D frame rendered without the
    actors, render_layers.py) is streaked and the actors of the film frame are laid over it sharp through their matte.  The motion is not guessed from pixels: reference points of the set (map corners, track, floor, the marks)
    are projected with the true camera of frames g - 1, g, g + 1 and a similarity (zoom + pan) is fitted to them.
    Frames slower than STREAK_MIN px per frame are copied untouched.
  * nothing is added to the other frames: bloom, grade and shadows are rendered in Blender.
Every frame is still a full 3D render; the streak only smears it along its own camera motion (reference: the plate
streaks when it travels more than about 40 px per frame, HOOK_STUDY 3.3).
"""
import json, math, os, shutil, sys
import numpy as np
from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
F_PX = 782.22
STREAK_MIN = 60.0          # px per frame at the frame corners: below this the frame is left sharp (a follow move keeps its subject sharp)
SHUTTER = 0.40             # exposure in frames
MAX_TAPS = 48


def project(loc, look, pts):
    loc = np.asarray(loc, float); look = np.asarray(look, float)
    f = look - loc; f /= np.linalg.norm(f)
    r = np.cross(f, [0, 0, 1.0]); r /= np.linalg.norm(r)
    u = np.cross(r, f)
    d = np.asarray(pts, float) - loc
    z = d @ f
    return np.stack([360.0 + F_PX * (d @ r) / z, 640.0 - F_PX * (d @ u) / z], 1), z


def ref_points():
    """world points of the set that carry the picture: the map wall, the wall around it, the floor in front."""
    pts = []
    for x in np.linspace(-3.4, 3.4, 9):
        for z in np.linspace(0.2, 4.6, 7):
            pts.append((x, 0.0, z))                      # map wall
    for x in np.linspace(-3.0, 3.0, 7):
        for y in np.linspace(-3.6, -0.4, 5):
            pts.append((x, y, 0.0))                      # floor
    return np.array(pts)


def similarity(p, q):
    """least-squares similarity q = s R p + t as a 2x3 matrix (complex form)."""
    pc = p[:, 0] + 1j * p[:, 1]; qc = q[:, 0] + 1j * q[:, 1]
    pm, qm = pc.mean(), qc.mean()
    a = ((qc - qm) * np.conj(pc - pm)).sum() / (np.abs(pc - pm) ** 2).sum()
    b = qm - a * pm
    return np.array([[a.real, -a.imag, b.real], [a.imag, a.real, b.imag]])


def camera_motion(cam_fn, g, g0, g1):
    """2x3 similarity that carries the picture of frame g - 0.5 to frame g + 0.5 (fitted over the visible reference
    points), and the largest displacement it gives to the four frame corners (px per frame)."""
    a, b = max(g0, g - 1), min(g1, g + 1)
    if a == b:
        return np.array([[1.0, 0, 0], [0, 1.0, 0]]), 0.0
    P = ref_points()
    pa, za = project(*cam_fn(a), P)
    pb, zb = project(*cam_fn(b), P)
    pg, zg = project(*cam_fn(g), P)
    ok = (za > 0.3) & (zb > 0.3) & (zg > 0.3) & (np.abs(pg[:, 0] - 360) < 900) & (np.abs(pg[:, 1] - 640) < 1500)
    if ok.sum() < 6:
        ok = (za > 0.3) & (zb > 0.3)
    M = similarity(pa[ok], pb[ok])
    # per-frame motion = the (b - a)-th root of M: scale and angle divided, translation about the fixed point
    n = float(b - a)
    a_c = complex(M[0, 0], M[1, 0]); t_c = complex(M[0, 2], M[1, 2])
    a1 = a_c ** (1.0 / n)
    t1 = t_c * (a1 - 1) / (a_c - 1) if abs(a_c - 1) > 1e-9 else t_c / n
    M1 = np.array([[a1.real, -a1.imag, t1.real], [a1.imag, a1.real, t1.imag]])
    corners = np.array([[0, 0], [720, 0], [0, 1280], [720, 1280]], float)
    moved = corners @ M1[:, :2].T + M1[:, 2]
    return M1, float(np.abs(moved - corners).max(axis=None) if False else np.linalg.norm(moved - corners, axis=1).max())


def frac_sim(M1, alpha):
    """the similarity M1 raised to the power alpha (alpha in frames, may be negative)."""
    a_c = complex(M1[0, 0], M1[1, 0]); t_c = complex(M1[0, 2], M1[1, 2])
    a = a_c ** alpha
    t = t_c * (a - 1) / (a_c - 1) if abs(a_c - 1) > 1e-9 else t_c * alpha
    return np.array([[a.real, -a.imag, t.real], [a.imag, a.real, t.imag]])


def streak(im, M1, speed, shutter=SHUTTER):
    taps = int(min(MAX_TAPS, max(3, math.ceil(speed * shutter / 2.0))))
    acc = np.zeros((im.size[1], im.size[0], 3), np.float64)
    for i in range(taps):
        alpha = (i / (taps - 1.0) - 0.5) * shutter
        M = frac_sim(M1, alpha)                       # picture(g) -> picture(g + alpha); PIL wants the inverse map
        A = np.vstack([M, [0, 0, 1]])
        Ai = np.linalg.inv(A)
        w = im.transform(im.size, Image.AFFINE, tuple(Ai[:2].ravel()), resample=Image.BILINEAR)
        m = Image.new("L", im.size, 255).transform(im.size, Image.AFFINE, tuple(Ai[:2].ravel()), resample=Image.BILINEAR)
        wa = np.asarray(w, np.float64); ma = np.asarray(m, np.float64)[..., None] / 255.0
        acc += (wa / 255.0) ** 2.2 * ma + (np.asarray(im, np.float64) / 255.0) ** 2.2 * (1 - ma)   # outside the frame: itself
    out = (acc / taps) ** (1 / 2.2)
    return Image.fromarray(np.clip(out * 255 + 0.5, 0, 255).astype(np.uint8))


def streak_list():
    """[(g, is_whip)] for every frame whose camera is faster than STREAK_MIN.  The whip pan (the last frames of take A
    from WHIP_OFF on, the first of take B up to WHIP_ON) is streaked whole; elsewhere only the plate is streaked."""
    import film
    out = []
    for take, (g0, g1) in sorted(film.TAKES.items()):
        cam_fn = film.cam_a if take == "A" else film.cam_b
        fn = lambda g: tuple(tuple(v) for v in cam_fn(g))
        for g in range(g0, g1 + 1):
            M1, speed = camera_motion(fn, g, g0, g1)
            if speed >= STREAK_MIN:
                out.append((g, film.WHIP_OFF[0] <= g <= film.WHIP_ON[1]))
    return out


def over(bg, fg, matte):
    """fg over bg through the matte's alpha (sharp actors over the streaked plate)."""
    a = np.asarray(matte.convert("RGBA"), np.float64)[..., 3:4] / 255.0
    o = np.asarray(bg, np.float64) * (1 - a) + np.asarray(fg, np.float64) * a
    return Image.fromarray(np.clip(o + 0.5, 0, 255).astype(np.uint8))


def main(argv):
    raw, out = argv[0], argv[1]
    no_streak = "--no-streak" in argv
    import film
    os.makedirs(out, exist_ok=True)
    log = []
    for take, (g0, g1) in sorted(film.TAKES.items()):
        cam_fn = film.cam_a if take == "A" else film.cam_b
        fn = lambda g: tuple(tuple(v) for v in cam_fn(g))
        for g in range(g0, g1 + 1):
            src = os.path.join(raw, "f_%04d.png" % (g + 1))
            dst = os.path.join(out, "f_%04d.png" % (g + 1))
            if not os.path.exists(src):
                raise SystemExit("missing raw frame " + src)
            M1, speed = camera_motion(fn, g, g0, g1)
            row = dict(g=g, take=take, corner_speed_px=round(speed, 2), zoom_per_frame=round(float(np.hypot(M1[0, 0], M1[1, 0])), 5),
                       pan_px=[round(float(M1[0, 2] + 360 * (M1[0, 0] - 1) - 640 * M1[1, 0]), 2), round(float(M1[1, 2] + 360 * M1[1, 0] + 640 * (M1[1, 1] - 1)), 2)],
                       streaked=False)
            if speed >= STREAK_MIN and not no_streak:
                im = Image.open(src).convert("RGB")
                whip = film.WHIP_OFF[0] <= g <= film.WHIP_ON[1]
                pl = os.path.join(raw, "plate", "f_%04d.png" % (g + 1)); mt = os.path.join(raw, "matte", "f_%04d.png" % (g + 1))
                if (not whip) and os.path.exists(pl) and os.path.exists(mt) and os.path.getmtime(pl) >= os.path.getmtime(src) - 1:
                    # the plate (set without the actors) is streaked, the actors of the film frame stay sharp on top
                    over(streak(Image.open(pl).convert("RGB"), M1, speed), im, Image.open(mt)).save(dst)
                    row["streaked"] = "plate"
                else:
                    streak(im, M1, speed).save(dst)
                    row["streaked"] = "whole"
            else:
                shutil.copyfile(src, dst)
            log.append(row)
    json.dump(log, open(os.path.join(out, "..", "post_log.json") if os.path.basename(os.path.normpath(out)) == "frames" else os.path.join(out, "post_log.json"), "w"), indent=0)
    print("post: %d frames; plate streaked under sharp actors g %s; whole frame streaked g %s" % (
        len(log), [r["g"] for r in log if r["streaked"] == "plate"], [r["g"] for r in log if r["streaked"] == "whole"]))
    return log


if __name__ == "__main__":
    main(sys.argv[1:])
