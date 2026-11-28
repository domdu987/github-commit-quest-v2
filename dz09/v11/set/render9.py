"""render6.py -- render the current camera with the v4 pass setup, then run post6 (or re-run post6 on kept EXRs).

render(out_noext, frame=7, post_opts=None) -> dict(png, raw, z, rgb, env, idx, depth_png, cpu_render, cpu_post, ...)
repost(out_noext, info) -> re-runs post6 on <out>_rgb/_z/_idx/_env.exr (no Blender needed except EXR reading via bpy)
"""
import os, json, time, resource
import numpy as np
import bpy

import expressway as X


def _cpu():
    r = resource.getrusage(resource.RUSAGE_SELF); return r.ru_utime + r.ru_stime


def cam_info(scene=None):
    scene = scene or bpy.context.scene
    cam = scene.camera
    return dict(preset=cam.get("preset"), aspect=cam.get("aspect"), focus_z=X.focus_depth(scene, cam),
                coc_k=float(cam.get("coc_k", 3.0)), coc_max=float(cam.get("coc_max", 36.0)))


def load_passes(out, W, H):
    import cv2
    rgba = X._read_exr(out["rgb"]); z = X._read_exr(out["z"])[..., 0]; idx = X._read_exr(out["idx"])[..., 0]
    env = X._read_exr(out["env"])[..., :3]
    rgb, alpha = rgba[..., :3], rgba[..., 3]
    if rgb.shape[1] != W:
        rgb = np.maximum(cv2.resize(rgb, (W, H), interpolation=cv2.INTER_LANCZOS4), 0)
        env = np.maximum(cv2.resize(env, (W, H), interpolation=cv2.INTER_LANCZOS4), 0)
        alpha = np.clip(cv2.resize(alpha, (W, H), interpolation=cv2.INTER_LINEAR), 0, 1)
        z = cv2.resize(z, (W, H), interpolation=cv2.INTER_NEAREST); idx = cv2.resize(idx, (W, H), interpolation=cv2.INTER_NEAREST)
    return rgb, alpha, env, z, idx


def render(out_noext, frame=7, post_opts=None, scene=None):
    import post9 as post6
    scene = scene or bpy.context.scene
    c0 = _cpu()
    out = X.render_still(out_noext, frame=frame, post=False, scene=scene)
    c1 = _cpu()
    out["cpu_render_total"] = round(c1 - c0, 2)
    W, H = scene.render.resolution_x, scene.render.resolution_y
    rgb, alpha, env, z, idx = load_passes(out, W, H)
    cones = [o for o in bpy.data.objects if o.get("fx") == "cone" and not o.hide_render]
    shl = None
    if X._STATE.get("shafts", "post") == "post":
        import shafts as SH
        shl = SH.collect(scene, scene.camera, cones)
    info = dict(shafts=shl, frame=frame, **cam_info(scene))
    info.update(post_opts or {})
    post6.process(rgb, z, idx, info, out_noext + ".png", out_noext + "_depth.png", alpha=alpha, env=env, out_raw=out_noext + "_raw.png")
    c2 = _cpu()
    out["png"] = out_noext + ".png"; out["depth_png"] = out_noext + "_depth.png"
    out["cpu_post"] = round(c2 - c1, 2)
    keep = {k: v for k, v in info.items() if k != "shafts"}
    keep["n_shafts"] = len(shl or [])
    with open(out_noext + "_info.json", "w") as f: json.dump(keep, f, indent=1)
    import pickle
    with open(out_noext + "_shafts.pkl", "wb") as f: pickle.dump(shl, f)
    return out


def repost(out_noext, **over):
    """re-run post9 on the kept passes of a render9.render() call (<out>_rgb/_z/_idx/_env.exr, _info.json,
    _shafts.pkl), with optional info overrides. About 3 CPU s; needs bpy only to read the EXRs."""
    import pickle, post9
    info = json.load(open(out_noext + "_info.json"))
    sp = out_noext + "_shafts.pkl"
    info["shafts"] = pickle.load(open(sp, "rb")) if os.path.exists(sp) else None
    info.update(over)
    out = {k: f"{out_noext}_{k}.exr" for k in ("rgb", "z", "idx", "env")}
    from PIL import Image
    W, H = Image.open(out_noext + "_raw.png").size
    rgb, alpha, env, z, idx = load_passes(out, W, H)
    post9.process(rgb, z, idx, info, out_noext + ".png", out_noext + "_depth.png", alpha=alpha, env=env)
    return out_noext + ".png"
