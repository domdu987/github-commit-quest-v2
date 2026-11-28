"""Film 25 conform: render-team takes (render25/t1..t3) -> frames (hard cuts) -> sky-hue safety clamp -> Kanit captions -> SFX + music + voice.
usage: python3 conform25.py <out_basename>    env: MUSICF (default film25/audio/music_tmp1.mp3), MUSIC_DB (-31), ONLY_FRAMES=1, WORK=<dir>
Takes are read straight from the team branches with `git show` (nothing is checked out). For each g the take whose [g0, g1) holds g
wins; when two branches deliver the same row, the most recent commit wins. Missing frames become black and are listed (never shipped).
No overlays: only the narration captions (client rule)."""
import sys, os, json, glob, subprocess, colorsys
import numpy as np
from PIL import Image
P = os.path.dirname(os.path.abspath(__file__)); R = os.path.dirname(P); out = sys.argv[1]; FPS = 30; N = 2093; T = N / FPS
WORK = os.environ.get("WORK", out + "_work"); FR = out + "_frames"; os.makedirs(FR, exist_ok=True); os.makedirs(WORK, exist_ok=True)
BRANCHES = ["render25/t1", "render25/t2", "render25/t3"]
git = lambda *a: subprocess.run(["git", "-C", R] + list(a), capture_output=True, text=True, check=True).stdout

# ---------------------------------------------------------------- 1. collect takes from the branches
takes = []
for b in BRANCHES:
    subprocess.run(["git", "-C", R, "fetch", "-q", "origin", b], check=True)
    ref = "origin/" + b
    for mp in [l for l in git("ls-tree", "-r", "--name-only", ref, "film/v3/film25").split() if l.endswith("/meta.json")]:
        td = os.path.dirname(mp); name = os.path.basename(td)
        files = git("ls-tree", "-r", "--name-only", ref, td).split()
        parts = sorted(f for f in files if os.path.basename(f).startswith("take.mkv"))
        if not parts: continue
        m = json.loads(git("show", "%s:%s" % (ref, mp)))
        when = int(git("log", "-1", "--format=%ct", ref, "--", td).strip() or 0)
        d = os.path.join(WORK, b.replace("/", "_"), name); os.makedirs(d, exist_ok=True)
        mk = d + "/take.mkv"
        if not os.path.exists(mk) or os.path.getmtime(mk) < when:
            with open(mk, "wb") as fo:
                for f in parts:
                    fo.write(subprocess.run(["git", "-C", R, "show", "%s:%s" % (ref, f)], capture_output=True, check=True).stdout)
            for f in glob.glob(d + "/g_*.png"): os.remove(f)
            subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mk, "-start_number", str(m["first_g"]), d + "/g_%04d.png"], check=True)
        m.update(name=name, branch=b, when=when, have={int(f[-8:-4]): f for f in glob.glob(d + "/g_*.png")})
        takes.append(m)
src, missing, used = {}, [], {}
for g in range(N):
    own = sorted([t for t in takes if t["g0"] <= g < t["g1"] and g in t["have"]], key=lambda t: t["when"])
    if own:
        src[g] = own[-1]["have"][g]; used.setdefault("%s:%s" % (own[-1]["branch"], own[-1]["name"]), [g, g])[1] = g
    else:
        src[g] = None; missing.append(g)
print("takes used:", len(used)); print("missing frames:", len(missing), (missing[:5], missing[-5:]) if missing else "")
json.dump({"used": used, "missing": missing}, open(out + "_conform_log.json", "w"), indent=1)

# ---------------------------------------------------------------- 2. frames + sky-hue safety clamp (blue-violet 230-330 deg -> 215 deg)
def sky_clamp(im):
    a = np.asarray(im.convert("HSV")).astype(np.int16)
    h = a[..., 0].astype(np.float32) * 360 / 255; s = a[..., 1]
    sel = (h > 228) & (h < 330) & (s > 25)            # lavender / violet drift only; reds, skins and whites untouched
    if not sel.any(): return im
    a[..., 0] = np.where(sel, int(215 * 255 / 360), a[..., 0])
    return Image.fromarray(a.astype(np.uint8), "HSV").convert("RGB")
for g in range(N):
    dst = "%s/f_%04d.png" % (FR, g)
    if src[g] is None:
        Image.new("RGB", (720, 1280)).save(dst); continue
    im = Image.open(src[g]).convert("RGB")
    if im.size != (720, 1280): im = im.resize((720, 1280), Image.LANCZOS)
    sky_clamp(im).save(dst)
if os.environ.get("ONLY_FRAMES"):
    sys.exit(0)

# ---------------------------------------------------------------- 3. captions (Kanit Black 88 at y 900), narration at 0.00
caps = json.load(open(P + "/film25/script/captions.json"))
caps = caps if isinstance(caps, list) else caps["captions"]
ass = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: 720", "PlayResY: 1280", "WrapStyle: 2", "", "[V4+ Styles]",
       "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
       "Style: Pop,Kanit Black,88,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,5,0,5,30,30,0,1", "", "[Events]",
       "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
ts = lambda t: "%d:%02d:%05.2f" % (int(t // 3600), int(t % 3600 // 60), t % 60)
for c in caps:
    a = max(0.0, c["t"]); b = min(c["end"] if c.get("end") else T, T)
    if a >= T: continue
    ass.append("Dialogue: 0,%s,%s,Pop,,0,0,0,,{\\pos(360,900)}%s" % (ts(a), ts(b), c["text"]))
open(out + ".ass", "w").write("\n".join(ass))
subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", "30", "-i", FR + "/f_%04d.png", "-vf", "ass=%s.ass:fontsdir=%s/fonts" % (out, P),
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "17", "-movflags", "+faststart", out + "_silent.mp4"], check=True)

# ---------------------------------------------------------------- 4. sound: SFX cues on the shot plan's word locks, location beds, ducking under the voice
SF = P + "/film25/audio/sfx/"
sfx = []
def add(f, t, db, ln, **k):
    if t < T: sfx.append(dict({"file": SF + f + ".mp3", "at": t, "peak_db": db, "len": min(ln, T - t), "align": "onset", "fade_out": 0.08}, **k))
g2t = lambda g: g / 30.0
CUES = [
    ("rivet_hammer", g2t(22), -14, 0.6), ("rivet_hammer", g2t(34), -15, 0.6),                  # 1+2 hammering
    ("chain_rattle", g2t(46), -20, 1.5), ("plate_clunk", g2t(55), -12, 0.9),                    # 3+4 hull lands on the weighbridge
    ("water_pour", g2t(139), -16, 1.5),                                                         # 6 watering can
    ("whoosh", g2t(154), -26, 0.5),                                                             # 7 pivot
    ("distant_boom", g2t(200), -28, 1.4),
    ("kick", g2t(240), -24, 0.6), ("kick", g2t(250), -24, 0.6),                                 # 10 digging
    ("helmet_ping", g2t(290), -13, 1.0), ("ping", g2t(296), -18, 0.6),                          # 12 helmet ping
    ("crate_creak", g2t(318), -18, 1.4),                                                        # 13 doors slam
    ("laugh_big", g2t(522), -15, 2.2),                                                          # 19 belly laugh
    ("laugh_big", g2t(604), -20, 1.5),                                                          # 21 toy tank sneer
    ("march_drums", g2t(680), -24, 1.2),                                                        # 23 imagined march
    ("crowd_laugh", g2t(760), -18, 2.4),                                                        # 25 camp
    ("tin_cup", g2t(790), -14, 0.6), ("tin_cup", g2t(800), -15, 0.6),                           # 26 ladle tap
    ("chain_rattle", g2t(884), -20, 1.0), ("plate_clunk", g2t(893), -12, 0.9),                  # 29 plate locks
    *[("rivet_hammer", g2t(g), -13, 0.5) for g in (903, 908, 913)],                            # 30 rivets
    ("chain_rattle", g2t(919), -18, 1.0), ("track_creak", g2t(933), -18, 1.2),                  # 31+32 tracks
    ("plate_clunk", g2t(976), -12, 0.9), ("plate_clunk", g2t(1004), -10, 0.9),                  # 33 sponson, 34 gun
    ("rivet_hammer", g2t(1020), -15, 0.5), ("rivet_hammer", g2t(1030), -15, 0.5),               # 35 crate
    ("brush_paint", g2t(1045), -22, 1.2),                                                       # 36 stencil
    ("tank_rumble", g2t(1135), -24, 3.5),                                                       # 39 dawn column
    ("steam_hiss", g2t(1370), -15, 1.6),                                                        # 45 leaky kettle
    ("tank_rumble", g2t(1396), -18, 3.5), ("track_creak", g2t(1424), -16, 2.0),                 # 46-49 the crossing
    ("impact", g2t(1493), -16, 1.0), ("mud_splat", g2t(1500), -20, 0.6),                        # 50 grip
    ("wire_crack", g2t(1573), -14, 1.0),                                                        # 52 wire flattened
    *[("ricochet", g2t(g), -14, 0.8) for g in (1605, 1621)],                                   # 53+54 pings
    ("gulp", g2t(1640), -18, 0.5), ("running_feet", g2t(1659), -16, 1.8),                       # 55, 56
    ("crate_creak", g2t(1801), -16, 1.0),                                                       # 60+61 lid opens
    ("tank_rumble", g2t(1961), -22, 3.0), ("crowd_cheer", g2t(2009), -18, 2.8),                 # 67, 68-70
]
BEDS = [("factory", 0, 5.12), ("field", 5.12, 10.52), ("factory", 10.52, 16.18), ("field", 16.18, 27.93), ("factory", 27.93, 35.71),
        ("harbour", 35.71, 37.84), ("field", 37.84, 56.27), ("factory", 56.27, 62.66), ("field", 62.66, T)]
for f, t, db, ln in CUES: add(f, t, db, ln)
for n, a_, b_ in BEDS:
    t = a_
    while t < b_ - 0.5:
        sfx.append({"file": SF + n + ".mp3", "at": t, "rms_db": -42, "len": min(4.0, b_ - t), "align": "start", "fade_in": 0.2, "fade_out": 0.4}); t += 3.8
V = P + "/film25/audio/narration.wav"
_v = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", V, "-ac", "1", "-ar", "8000", "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
_env = np.sqrt(np.convolve(_v ** 2, np.ones(800) / 800, "same"))[::80]
def talk(a, ln):
    seg = _env[max(0, int(a * 100)):max(0, int((a + ln) * 100))]
    return seg.size > 0 and (seg > 0.02).mean() > 0.3
for x in sfx:
    k = "peak_db" if "peak_db" in x else "rms_db"
    if talk(x["at"], x["len"]): x[k] -= 5 if x["len"] < 3 else 3
vr = 20 * np.log10(np.sqrt((_v ** 2).mean()) + 1e-9)
spec = {"duration": T, "out_wav": out + ".wav", "video_in": out + "_silent.mp4", "video_out": out + ".mp4",
        "voice": {"file": V, "at": 0.0, "gain": float(10 ** ((-17.4 - vr) / 20))},
        "music": {"file": os.environ.get("MUSICF", P + "/film25/audio/music_tmp1.mp3"), "at": 0, "rms_db": float(os.environ.get("MUSIC_DB", "-31")),
                  "fade_in": 0.3, "fade_out": 0.6},
        "sfx": sfx}
json.dump(spec, open(out + "_mix.json", "w"), indent=1)
subprocess.run([sys.executable, P + "/audio/mixer.py", out + "_mix.json"], check=True)
print("done:", out + ".mp4", "missing frames:", len(missing))
