"""orbit_test.py -- proof renders of the 2.5D puppet.

    python3 orbit_test.py still  <out.png> <orbit_deg> [cast] [mode 25d|flat] [samples]
    python3 orbit_test.py compare               # tmp/compare/: flat vs 2.5D at -30, 0, +30 degrees -> out/compare_flat_vs_25d.png
    python3 orbit_test.py orbit [frames] [cast] # out/orbit_<cast>.mp4: camera orbits -35..+35..-35 around the cast member
"""
import math, os, sys, time, json
import bpy
from mathutils import Vector

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import stage25 as st
import testset

KONG_POSE = {"expr": "determined", "arm_l": "hold", "prop_l": {"type": "cutter", "angle": 96, "bars": 3},
             "arm_r": "down", "legs": "stand"}
RADIUS, HEIGHT, LOOK_Z = 6.0, 2.2, 1.7


def scene_new(samples=16, w=360, h=640, rain=True):
    bpy.ops.wm.read_factory_settings(use_empty=True)
    sc = bpy.context.scene
    st.setup_render(sc, w, h, samples=samples, denoise=True, threads=int(os.environ.get("THREADS", "4")))
    L = testset.build(sc, rain=rain)
    cam_d = bpy.data.cameras.new("cam")
    cam_d.lens = 28
    cam_d.sensor_width = 36
    cam_d.dof.use_dof = True
    cam_d.dof.aperture_fstop = 2.0
    cam = bpy.data.objects.new("cam", cam_d)
    sc.collection.objects.link(cam)
    sc.camera = cam
    st.sync_lights(key=L["key"], rims=[L["beacon"], L["sodium"]], shadow=L["sodium"])
    st.set_toon(exposure=0.92, rim_amt=0.6, wash_amt=0.20, glint_amt=1.6)
    return sc, cam, L


def cam_at(cam, deg, actor_loc=(0, 0, 0), r=RADIUS, hgt=HEIGHT, look=LOOK_Z):
    a = math.radians(deg)
    x = actor_loc[0] + r * math.sin(a)
    y = actor_loc[1] - r * math.cos(a)
    cam.location = (x, y, hgt)
    tgt = Vector((actor_loc[0], actor_loc[1], look))
    d = tgt - cam.location
    cam.rotation_euler = d.to_track_quat("-Z", "Y").to_euler()
    cam.data.dof.focus_distance = d.length


def still(out, deg, cast="kong", mode="25d", samples=16, pose=None, w=360, h=640):
    sc, cam, L = scene_new(samples, w, h)
    a = st.Actor25("A", cast, mode=mode)
    a.place((0, 0, 0), 0.0)
    cam_at(cam, deg)
    bpy.context.view_layer.update()
    a.pose(pose or KONG_POSE, camera=cam)
    sc.render.filepath = out
    t = time.time()
    bpy.ops.render.render(write_still=True)
    return time.time() - t, a


def compare():
    from PIL import Image, ImageDraw, ImageFont
    d = os.path.join(HERE, "tmp", "compare")
    os.makedirs(d, exist_ok=True)
    meas = {}
    for mode in ("flat", "25d"):
        sc, cam, L = scene_new(16)
        a = st.Actor25("K", "kong", mode=mode)
        for deg in (-30, 0, 30):
            a.place((0, 0, 0), 0.0)
            cam_at(cam, deg)
            bpy.context.view_layer.update()
            a.pose(KONG_POSE, camera=cam)
            sc.render.filepath = os.path.join(d, "%s_%+03d.png" % (mode, deg))
            t = time.time()
            bpy.ops.render.render(write_still=True)
            meas["%s_%+d" % (mode, deg)] = {"s": round(time.time() - t, 2), "view": a.view,
                                            "pts": a.screen_points(sc, cam, ("head", "hand_l", "hand_r", "shoulder_r", "hip"))}
    json.dump(meas, open(os.path.join(d, "measure.json"), "w"), indent=1)
    # sheet
    ims = {k: Image.open(os.path.join(d, "%s_%+03d.png" % (k.split("_")[0], int(k.split("_")[1])))) for k in meas}
    W, H = 360, 640
    sheet = Image.new("RGB", (W * 3 + 40, H * 2 + 90), (18, 18, 24))
    dr = ImageDraw.Draw(sheet)
    try:
        f = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 18)
    except Exception:
        f = ImageFont.load_default()
    for r, mode in enumerate(("flat", "25d")):
        for c, deg in enumerate((-30, 0, 30)):
            sheet.paste(ims["%s_%+d" % (mode, deg)], (20 + c * W, 50 + r * (H + 20)))
            dr.text((26 + c * W, 52 + r * (H + 20)), "%s  orbit %+d deg" % ("2D flat card" if mode == "flat" else "2.5D layers", deg),
                    fill=(255, 230, 120), font=f)
    dr.text((20, 14), "Kong under red beacon + sodium lamp: 2D-flat sticker (top) vs 2.5D layered toon (bottom)", fill=(230, 230, 230), font=f)
    out = os.path.join(HERE, "out", "compare_flat_vs_25d.png")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    sheet.save(out)
    print(json.dumps(meas, indent=1))


def orbit(frames=96, cast="kong", tag=None, samples=12):
    tag = tag or cast
    d = os.path.join(HERE, "tmp", "orbit_" + tag)
    os.makedirs(d, exist_ok=True)
    sc, cam, L = scene_new(samples)
    a = st.Actor25("K", cast, mode="25d")
    a.place((0, 0, 0), 0.0)
    times, views = [], []
    for i in range(frames):
        u = i / float(frames - 1)
        deg = -35 * math.cos(2 * math.pi * u)            # -35 -> +35 -> -35, eased at the ends
        cam_at(cam, deg)
        bpy.context.view_layer.update()
        p = dict(KONG_POSE)
        if cast.startswith("kong") and i in (40, 41, 42):
            p["blink"] = {40: 1, 41: 2, 42: 1}[i]
        if cast == "kong_wet":
            p["expr"] = "tired"
        a.pose(p, camera=cam)
        views.append(a.view)
        sc.render.filepath = os.path.join(d, "f_%04d.png" % i)
        if os.path.exists(sc.render.filepath):
            continue
        t = time.time()
        bpy.ops.render.render(write_still=True)
        times.append(time.time() - t)
    out = os.path.join(HERE, "out", "orbit_%s.mp4" % tag)
    os.makedirs(os.path.dirname(out), exist_ok=True)
    os.system("ffmpeg -y -loglevel error -framerate 30 -i %s/f_%%04d.png -c:v libx264 -pix_fmt yuv420p -crf 18 %s" % (d, out))
    json.dump({"sec_per_frame": sum(times) / max(1, len(times)), "views": views}, open(os.path.join(d, "stats.json"), "w"))
    print("orbit", out, "s/frame", sum(times) / max(1, len(times)))


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "still":
        out, deg = sys.argv[2], float(sys.argv[3])
        cast = sys.argv[4] if len(sys.argv) > 4 else "kong"
        mode = sys.argv[5] if len(sys.argv) > 5 else "25d"
        sm = int(sys.argv[6]) if len(sys.argv) > 6 else 16
        big = len(sys.argv) > 7
        t, a = still(out, deg, cast, mode, sm, w=720 if big else 360, h=1280 if big else 640)
        print("render s", round(t, 2), "view", a.view)
    elif cmd == "compare":
        compare()
    elif cmd == "orbit":
        orbit(int(sys.argv[2]) if len(sys.argv) > 2 else 96, sys.argv[3] if len(sys.argv) > 3 else "kong")
