"""post.py -- icon pops, phone-voice bubble, grade (bloom, vignette), bite flash, title card; then captions (libass,
Kanit Black) + mix.wav -> animatic_v1.mp4, and sheet.png (one frame per shot).

    python3 post.py icons      # rasterise icon frames (iconfx, import only) -> icons/
    python3 post.py frames     # composite render/ + icons -> final/
    python3 post.py video      # captions + audio -> animatic_v1.mp4
    python3 post.py sheet
"""
import json, math, os, subprocess, sys
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

HERE = os.path.dirname(os.path.abspath(__file__))
PROJ = os.path.abspath(os.path.join(HERE, "..", ".."))
FPS, W, H, NF = 24, 360, 640, 1164
NARR0 = 0.30
KANIT = os.path.join(PROJ, "fonts", "Kanit_900Black.ttf")
WORKS = os.path.join(PROJ, "fonts", "WorkSans-Black.ttf")
ICDIR = os.path.join(HERE, "icons")

# (cue id, icon, t_in, t_out, centre x, centre y, px for 100 design units, kwargs)
CUES = [
    ("rings_radio", "sound_rings", 2.17, 3.50, 196, 214, 170, {"mode": "circle"}),
    ("battery", "battery", 15.70, 16.95, 262, 180, 110, {"level": 3}),
    ("phone4", "phone", 18.36, 19.75, 272, 150, 105, {"n": 4}),
    ("heart", "heart", 26.55, 28.25, 92, 168, 115, {"crack_at": 0.35, "split_dur": 0.3}),
    ("rings_shout", "sound_rings", 30.84, 32.10, 150, 318, 160, {"mode": "arcs"}),
    ("eye", "eye", 38.01, 39.41, 182, 150, 115, {}),
    ("stopwatch", "stopwatch", 42.26, 45.80, 272, 165, 118, {}),
    ("bio_title", "biohazard", 45.90, 48.50, 180, 205, 110, {}),
]
POP_IN = [0.0, 0.62, 1.15, 1.0]        # 4-frame overshoot
POP_OUT = [1.0, 1.08, 0.55, 0.0]


def fr(t):
    return int(round(t * FPS))


def icons():
    sys.path.insert(0, os.path.join(PROJ, "v4", "iconfx"))
    import icons as IC
    import raster
    jobs, meta = [], {}
    for cid, name, t0, t1, cx, cy, px, kw in CUES:
        g0, g1 = fr(t0), fr(t1)
        d = os.path.join(ICDIR, cid)
        os.makedirs(d, exist_ok=True)
        for g in range(g0, g1):
            k = g - g0
            sc = POP_IN[k] if k < len(POP_IN) else 1.0
            ko = g1 - 1 - g
            if ko < len(POP_OUT) - 1 and cid != "bio_title":
                sc = min(sc, POP_OUT[len(POP_OUT) - 1 - ko])
            if sc <= 0.01:
                continue
            ic = IC.make(name, t=(g - g0) / FPS, **kw)
            svg, w, h, anc = IC.to_svg(ic, px=px, scale=sc)
            out = os.path.join(d, "%04d.png" % g)
            meta["%s/%d" % (cid, g)] = [w, h, anc[0], anc[1]]
            jobs.append({"svg": svg, "w": w, "h": h, "out": out})
    raster.render(jobs)
    raster.close()
    json.dump(meta, open(os.path.join(ICDIR, "meta.json"), "w"))
    print("icon frames", len(jobs))


def font(path, sz):
    return ImageFont.truetype(path, sz, layout_engine=ImageFont.Layout.RAQM)


def bubble(im, g, t_in, t_out):
    """phone-voice bubble (Namnuea speaking through the phone): avatar + pulsing arcs, top-left."""
    t = g / FPS
    if not (t_in <= t < t_out):
        return
    k = min(1.0, (t - t_in) * 8, (t_out - t) * 8)
    av = Image.open(os.path.join(HERE, "tex", "avatar.png")).convert("RGBA")
    s = int(70 * (0.6 + 0.4 * k))
    av = av.resize((s, s), Image.LANCZOS)
    x, y = 22, 66
    d = ImageDraw.Draw(im)
    d.ellipse([x - 4, y - 4, x + s + 4, y + s + 4], fill=(31, 29, 36, int(255 * k)))
    d.ellipse([x - 2, y - 2, x + s + 2, y + s + 2], fill=(244, 241, 234, int(255 * k)))
    im.alpha_composite(av, (x, y))
    # sound arcs
    ph = (t * 2.2) % 1.0
    for i in range(3):
        r = 14 + 10 * ((ph + i / 3.0) % 1.0) * 2
        a = int(255 * k * (1 - ((ph + i / 3.0) % 1.0)))
        cx, cy = x + s + 6, y + s // 2
        d.arc([cx - r, cy - r, cx + r, cy + r], -45, 45, fill=(207, 216, 238, a), width=3)
    f = font(KANIT, 15)
    d.text((x + s / 2, y + s + 14), "น้ำเหนือ", font=f, fill=(244, 241, 234, int(255 * k)), anchor="mm",
           stroke_width=2, stroke_fill=(0, 0, 0, int(255 * k)))


def grade(im):
    a = np.asarray(im.convert("RGB")).astype(np.float32) / 255.0
    # bloom: bright pass blurred
    lum = a.max(axis=2, keepdims=True)
    bright = np.clip((lum - 0.72) / 0.28, 0, 1) * a
    bl = Image.fromarray((bright * 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(7))
    a = a + 0.55 * np.asarray(bl).astype(np.float32) / 255.0
    # cool shadows
    a = a * np.array([0.97, 0.99, 1.04], np.float32)
    # vignette
    yy, xx = np.mgrid[0:H, 0:W]
    v = ((xx - W / 2) / (W * 0.75)) ** 2 + ((yy - H / 2) / (H * 0.72)) ** 2
    a = a * (1 - 0.55 * np.clip(v, 0, 1))[..., None]
    return Image.fromarray((np.clip(a, 0, 1) * 255).astype(np.uint8)).convert("RGBA")


def title(im, g):
    t = g / FPS
    t0 = 45.9
    if t < t0:
        return im
    k = min(1.0, (t - t0) / 0.25)
    dark = Image.new("RGBA", (W, H), (6, 8, 16, int(150 * min(1.0, (t - t0) / 0.6))))
    im = Image.alpha_composite(im, dark)
    d = ImageDraw.Draw(im)
    sc = 1.0
    f = int(t * FPS) - int(t0 * FPS)
    if f < 4:
        sc = POP_IN[f] if f < len(POP_IN) else 1.0
    if sc <= 0.01:
        return im
    lay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ld = ImageDraw.Draw(lay)
    ld.text((W / 2, 300), "เขตปิดตาย 09", font=font(KANIT, 46), fill=(244, 241, 234, 255), anchor="mm",
            stroke_width=4, stroke_fill=(10, 10, 14, 255))
    ld.rounded_rectangle([70, 340, W - 70, 382], 8, fill=(226, 69, 59, 255))
    ld.text((W / 2, 361), "DEAD ZONE 09", font=font(WORKS, 26), fill=(244, 241, 234, 255), anchor="mm")
    ld.text((W / 2, 404), "EP.1  ทางด่วนนรก", font=font(KANIT, 17), fill=(207, 216, 238, 255), anchor="mm",
            stroke_width=2, stroke_fill=(10, 10, 14, 255))
    if abs(sc - 1.0) > 0.01:
        lay = lay.resize((int(W * sc), int(H * sc)), Image.LANCZOS)
        L2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        L2.alpha_composite(lay, (int((W - lay.width) / 2), int((H - lay.height) / 2)) if sc < 1 else (0, 0),
                           (0, 0) if sc < 1 else (int((lay.width - W) / 2), int((lay.height - H) / 2)))
        lay = L2
    return Image.alpha_composite(im, lay)


def frames():
    meta = json.load(open(os.path.join(ICDIR, "meta.json")))
    out = os.path.join(HERE, "final")
    os.makedirs(out, exist_ok=True)
    for g in range(NF):
        src = os.path.join(HERE, "render", "f_%04d.png" % (g + 1))
        im = grade(Image.open(src))
        t = g / FPS
        # bite: 2-frame red flash, then red tint decaying
        if fr(39.70) <= g < fr(39.70) + 2:
            im = Image.alpha_composite(im, Image.new("RGBA", (W, H), (226, 40, 30, 150)))
        elif fr(39.70) + 2 <= g < fr(41.26):
            a = int(70 * max(0.0, 1 - (t - 39.79) / 1.4))
            im = Image.alpha_composite(im, Image.new("RGBA", (W, H), (160, 10, 10, a)))
        # radio static burst on the cut (3 frames of noise)
        if fr(3.40) <= g < fr(3.525):
            n = (np.random.default_rng(g).random((H, W)) * 255).astype(np.uint8)
            im = Image.blend(im, Image.merge("RGBA", (Image.fromarray(n),) * 3 + (Image.new("L", (W, H), 255),)), 0.45)
        bubble(im, g, 21.26, 23.74)
        bubble(im, g, 26.069, 27.25)
        im = title(im, g)
        for cid, name, t0, t1, cx, cy, px, kw in CUES:
            key = "%s/%d" % (cid, g)
            if key in meta:
                w, h, ax, ay = meta[key]
                ic = Image.open(os.path.join(ICDIR, cid, "%04d.png" % g)).convert("RGBA")
                im.alpha_composite(ic, (int(round(cx - ax)), int(round(cy - ay))))
        im.convert("RGB").save(os.path.join(out, "f_%04d.png" % (g + 1)))
    print("final frames", NF)


def ts(t):
    h = int(t // 3600); m = int(t % 3600 // 60); s = t % 60
    return "%d:%02d:%05.2f" % (h, m, s)


def video():
    caps = json.load(open(os.path.join(PROJ, "audio", "narr_v1", "captions_timing.json")))
    ass = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: %d" % W, "PlayResY: %d" % H, "WrapStyle: 2",
           "ScaledBorderAndShadow: yes", "", "[V4+ Styles]",
           "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, "
           "Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, "
           "MarginR, MarginV, Encoding",
           "Style: Cap,Kanit Black,27,&H00FFFFFF,&H00FFFFFF,&H00000000,&H90000000,0,0,0,0,100,100,0,0,1,2.6,1,5,16,16,0,222",
           "", "[Events]", "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
    for c in caps:
        t0, t1 = c["t0"] + NARR0, c["t1"] + NARR0
        if t1 > 45.88:
            t1 = 45.88
        ass.append("Dialogue: 0,%s,%s,Cap,,0,0,0,,{\\pos(180,450)\\fscx85\\fscy85\\t(0,60,\\fscx100\\fscy100)}%s"
                   % (ts(t0), ts(t1), c["text"]))
    ap = os.path.join(HERE, "captions.ass")
    open(ap, "w", encoding="utf-8").write("\n".join(ass) + "\n")
    out = os.path.join(HERE, "animatic_v1.mp4")
    cmd = ["ffmpeg", "-y", "-loglevel", "error", "-framerate", str(FPS), "-i", os.path.join(HERE, "final", "f_%04d.png"),
           "-i", os.path.join(PROJ, "audio", "narr_v1", "mix.wav"),
           "-vf", "ass=%s:fontsdir=%s" % (ap, os.path.join(PROJ, "fonts")),
           "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
           "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out]
    subprocess.run(cmd, check=True)
    print("wrote", out)


def sheet():
    sys.path.insert(0, HERE)
    import ast
    src = open(os.path.join(HERE, "shots.py")).read()
    # pull SHOTS ids/times without importing bpy
    shots = []
    for line in src.splitlines():
        line = line.strip()
        if line.startswith('dict(id="S'):
            sid = line.split('id="')[1].split('"')[0]
            t0 = float(line.split("t0=")[1].split(",")[0]); t1 = float(line.split("t1=")[1].split(",")[0])
            ang = line.split('angle="')[1].split('"')[0]
            shots.append((sid, t0, t1, ang))
    tmp = os.path.join(HERE, "_sheetframes")
    os.makedirs(tmp, exist_ok=True)
    vid = os.path.join(HERE, "animatic_v1.mp4")
    tw, th = 180, 320
    cols = 6
    rows = (len(shots) + cols - 1) // cols
    S = Image.new("RGB", (cols * tw, rows * (th + 34)), (16, 18, 26))
    d = ImageDraw.Draw(S)
    f = font(WORKS, 13)
    for i, (sid, t0, t1, ang) in enumerate(shots):
        tm = t0 + (t1 - t0) * 0.6
        if sid == "S24":
            tm = 46.8
        p = os.path.join(tmp, sid + ".png")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-ss", "%.3f" % tm, "-i", vid, "-frames:v", "1", p], check=True)
        im = Image.open(p).convert("RGB").resize((tw, th), Image.LANCZOS)
        x, y = (i % cols) * tw, (i // cols) * (th + 34)
        S.paste(im, (x, y))
        d.text((x + 4, y + th + 2), "%s %.2f-%.2f" % (sid, t0, t1), font=f, fill=(240, 240, 240))
        d.text((x + 4, y + th + 17), ang[:26], font=font(WORKS, 11), fill=(170, 180, 200))
    S.save(os.path.join(HERE, "sheet.png"))
    print("wrote sheet")


if __name__ == "__main__":
    for step in sys.argv[1:]:
        {"icons": icons, "frames": frames, "video": video, "sheet": sheet}[step]()
