"""Film 24 conform: takes -> frames (hard cuts) -> overlays (R10-style motion graphics) -> Kanit captions -> SFX + music + voice mix.
usage: python3 conform24.py <out_basename>      env: MUSICF (default film24/audio/music_temp.mp3), MUSIC_DB (-31), ONLY_FRAMES=1
Takes: v3/film24/s*/meta.json (+ take.mkv or take.mkv.part*). Missing frames become black and are listed (never shipped)."""
import sys, os, json, glob, math, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont
P = os.path.dirname(os.path.abspath(__file__)); out = sys.argv[1]; FPS = 30; OFF = 0.10
VER = os.environ.get("VERSION", "B")   # B = R9 look (take.mkv); A = films 1-13 look (take_A.mkv, graded here with the v1.1 grade); C = LIGHT_SPEC look + build-up (take_C.mkv, 71.9 s)
SUF = {"A": "_A", "C": "_C"}.get(VER, "")
N = 2158 if VER == "C" else 1950; T = N / FPS
SH = 208 if VER == "C" else 0          # version C: everything after the build-up (old g >= 919) is 208 frames later
AUD = P + "/film24/audio/" + ("" if VER == "C" else "bk0_v1/")      # A/B keep the 65 s narration + captions
SCR = P + "/film24/" + ("script/" if VER == "C" else "audio/bk0_v1/")
FR = out + "_frames"; os.makedirs(FR, exist_ok=True)
FONT = P + "/fonts/Kanit_900Black.ttf"

# ---------------------------------------------------------------- 1. frames from takes (hard cuts at each take's g0)
takes = []
for mp in sorted(glob.glob(P + "/v3/film24/s*/meta.json") + glob.glob(P + "/v3/film24/s08C/meta_C.json")):
    td = os.path.dirname(mp)
    if os.path.exists(td + "/meta%s.json" % SUF): mp = td + "/meta%s.json" % SUF
    elif VER in ("A", "C"): continue
    m = json.load(open(mp)); fr = td + "/frames" + SUF
    if not glob.glob(fr + "/g_*.png"):
        mk = td + "/take%s.mkv" % SUF
        if not os.path.exists(mk) and glob.glob(mk + ".part*"):
            subprocess.run("cat %s.part* > %s" % (mk, mk), shell=True, check=True)
        if not os.path.exists(mk):
            continue
        os.makedirs(fr, exist_ok=True)
        subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", mk, "-start_number", str(m["first_g"]), fr + "/g_%04d.png"], check=True)
        if glob.glob(mk + ".part*"):
            os.remove(mk)                     # rebuilt from the committed parts: do not leave an untracked copy
    m["have"] = {int(f[-8:-4]): f for f in glob.glob(fr + "/g_*.png")}; m["name"] = os.path.basename(td); m["dir"] = td
    takes.append(m)
takes.sort(key=lambda m: m["g0"])
src, missing = {}, []
for g in range(N):
    own = [t for t in takes if t["g0"] <= g < t["g1"]]
    f = own[-1]["have"].get(g) if own else None
    if f is None:
        missing.append(g)
    src[g] = f
print("takes:", [t["name"] for t in takes], "missing frames:", len(missing))

# ---------------------------------------------------------------- 2. overlays (client R10 note): red X on hit ships, "47 : 0" tally
def pop(u):
    """0..1 -> scale with a small overshoot over 4 frames (u in frames since pop)."""
    if u < 0: return 0.0
    return [0.4, 1.18, 1.05, 1.0][int(u)] if u < 4 else 1.0

def draw_x(d, x, y, s, a=255):
    r = 13 * s
    for w, col in ((int(9 * s) + 4, (255, 255, 255, a)), (int(9 * s), (226, 30, 36, a))):
        d.line([(x - r, y - r), (x + r, y + r)], fill=col, width=max(w, 1))
        d.line([(x - r, y + r), (x + r, y - r)], fill=col, width=max(w, 1))

def draw_check(d, x, y, s):
    r = 16 * s
    for w, col in ((int(10 * s) + 4, (255, 255, 255, 255)), (int(10 * s), (40, 190, 70, 255))):
        d.line([(x - r, y), (x - r * 0.3, y + r * 0.7), (x + r, y - r * 0.8)], fill=col, width=max(w, 1), joint="curve")

def ship_icon(d, x, y, s, hull, sail):
    """a small side-view ship: hull trapezoid + mast + square sail (white outline), centred on x, y."""
    o = (255, 255, 255, 255)
    hullp = [(x - 46 * s, y), (x + 46 * s, y), (x + 32 * s, y + 20 * s), (x - 32 * s, y + 20 * s)]
    d.polygon(hullp, fill=hull, outline=o, width=max(1, int(3 * s)))
    d.line([(x, y), (x, y - 52 * s)], fill=o, width=max(1, int(4 * s)))
    d.rectangle([x - 20 * s, y - 48 * s, x + 20 * s, y - 14 * s], fill=sail, outline=o, width=max(1, int(3 * s)))

def tally(im, g, g_in):
    u = g - g_in
    if u < 0: return
    d = ImageDraw.Draw(im, "RGBA"); f = ImageFont.truetype(FONT, 78)
    s1 = pop(u); s2 = pop(u - 8)
    # panel
    d.rounded_rectangle([70, 150, 650, 336], radius=26, fill=(0, 0, 0, 120))
    if s1 > 0:   # Japanese side: red ship, "47", red X
        ship_icon(d, 165, 272, 1.25 * s1, (150, 40, 34, 255), (235, 225, 205, 255))
        n = min(47, int(round(47 * min(1.0, u / 10.0))))          # counts up 0 -> 47 over 10 frames
        d.text((300, 250), str(n), font=f, fill=(255, 255, 255, 255), anchor="rm", stroke_width=5, stroke_fill=(0, 0, 0, 255))
        draw_x(d, 165, 228, 1.4 * s1)
    if s1 > 0:
        d.text((360, 250), ":", font=f, fill=(255, 255, 255, 255), anchor="mm", stroke_width=5, stroke_fill=(0, 0, 0, 255))
    if s2 > 0:   # Korean side: green ship, "0", green check
        ship_icon(d, 555, 272, 1.25 * s2, (40, 120, 70, 255), (225, 70, 50, 255))
        d.text((420, 250), "0", font=f, fill=(255, 255, 255, 255), anchor="lm", stroke_width=5, stroke_fill=(0, 0, 0, 255))
        draw_check(d, 555, 224, 1.3 * s2)

def graded(path, g):
    """v1.1 grade (COLOUR_SPEC section 5, film_mini.py grade) for Look A frames."""
    sys.path.insert(0, P + "/skill/reference-style-shorts/pipeline/v3/film/out_v11")
    import grade as G
    if not getattr(G, "_f24", False):
        G.TAKES, G.JOINS, G.SHOT = [("f24", 0)], [], {}; G.FOG_G0, G.FOG_G1 = 10 ** 9, -1; G._f24 = True
    return G.grade_frame(Image.open(path).convert("RGB"), g)

OV = {}
for t in takes:
    oj = t["dir"] + "/overlay%s.json" % ("_C" if VER == "C" else "")
    if os.path.exists(oj):
        for e in json.load(open(oj)):        # version C: overlay_C.json is in OLD g numbering -> +208
            OV[int(e["g"]) + SH] = [dict(sh, hit_g=sh.get("hit_g", 1e9) + SH) for sh in e["ships"]]
X_FROM = 1768 if VER == "C" else int(round((51.97 + OFF) * 30))   # C: X marks only from the close hit 13c on; A/B: "ยิงปืนใหญ่ ใส่จากทุกด้าน"
TALLY_G = int(round((57.15 + OFF) * 30)) + SH   # "เรือญี่ปุ่น แตกไปกว่าครึ่ง"
TALLY_END = 1767 + SH

CALLOUTS = os.environ.get("CALLOUTS", "0") == "1"   # client 2026-11-27: no text, no pointer lines in the build-up (kept as an option, off)
# version C build-up callouts (R10 style): label pill in the top band + leader line + dot on the part (s08C/build_anchors.json)
LABELS = {"1": "ตัวเรือไม้สนหนา", "2": "พาย ข้างละ 8-10", "3": "ช่องปืน ราวข้างละ 11", "4": "หลังคาคลุมทั้งลำ",
          "5": "เหล็กแหลม กันปีนขึ้นเรือ", "6a": "หน้าผีบนหัวเรือ ขู่ข้าศึก", "6b": "หัวมังกร", "6c": "ยิงปืนใหญ่ออกจากปากได้", "7": "ไอ้เรือเต่า"}
SUB = {"3": "ชอนจา · จีจา · ฮยอนจา", "7": "บางบันทึกเล่าว่า พ่นควันบังตา"}
BA, BSTART = {}, {}
for t in takes:
    bj = t["dir"] + "/build_anchors.json"
    if VER == "C" and os.path.exists(bj):
        for e in json.load(open(bj)):
            st = str(e["stage"]); BA[int(e["g"])] = (st, e.get("x"), e.get("y")); BSTART.setdefault(st, int(e["g"]))
def callout(im, g):
    st, x, y = BA[g]
    if st not in LABELS: return
    u = g - BSTART[st]; s = pop(u)
    if s <= 0: return
    d = ImageDraw.Draw(im, "RGBA"); big = st == "7"
    f = ImageFont.truetype(FONT, 76 if big else 50); fs = ImageFont.truetype(FONT, 36)
    txt = LABELS[st]; bx, by = 360, 170
    w = d.textlength(txt, font=f); h = 92 if big else 66
    sc = s
    box = [bx - w / 2 * sc - 24, by - h / 2 * sc, bx + w / 2 * sc + 24, by + h / 2 * sc]
    if x is not None and y is not None and not big and 0 < x < 720 and 0 < y < 1280 and u >= 2:
        a = min(1.0, (u - 2) / 4.0); ex, ey = bx + (x - bx) * a, box[3] + (y - box[3]) * a
        d.line([(bx, box[3]), (ex, ey)], fill=(255, 255, 255, 235), width=4)
        if a >= 1: d.ellipse([x - 9, y - 9, x + 9, y + 9], fill=(255, 196, 60, 255), outline=(255, 255, 255, 255), width=3)
    d.rounded_rectangle(box, radius=int(h / 2 * sc), fill=(20, 16, 12, 185), outline=(255, 196, 60, 255), width=3)
    if sc > 0.6:
        ff = ImageFont.truetype(FONT, max(10, int((76 if big else 50) * sc)))
        d.text((bx, by), txt, font=ff, fill=(255, 255, 255, 255), anchor="mm")
    if st in SUB and u >= 6:
        d.text((bx, box[3] + 30), SUB[st], font=fs, fill=(255, 255, 255, 235), anchor="mm", stroke_width=3, stroke_fill=(0, 0, 0, 200))
for g in range(N):
    dst = "%s/f_%04d.png" % (FR, g)
    if os.path.lexists(dst): os.remove(dst)
    if src[g] is None:
        Image.new("RGB", (720, 1280)).save(dst); continue
    in_ov = src[g] is not None and ("/s13/" in src[g] or "/s14/" in src[g])   # overlays only on the reveal / aftermath takes
    ships = [sh for sh in (OV.get(g, []) if in_ov else []) if g >= X_FROM and sh.get("hit_g", 1e9) <= g and 0 < sh["x"] < 720 and 60 < sh["y"] < 860]
    co = CALLOUTS and VER == "C" and g in BA and src[g] is not None and "/s08C/" in src[g]
    if not ships and not co and not (TALLY_G <= g < TALLY_END) and VER != "A":
        os.symlink(src[g], dst); continue
    im = (graded(src[g], g) if VER == "A" else Image.open(src[g])).convert("RGBA"); d = ImageDraw.Draw(im, "RGBA")
    for sh in ships[:24]:
        draw_x(d, sh["x"], sh["y"] - 14, 0.75 * pop(g - max(sh["hit_g"], X_FROM)))
    if TALLY_G <= g < TALLY_END and "/s14/" in src[g]:
        tally(im, g, TALLY_G)
    if co:
        callout(im, g)
    im.convert("RGB").save(dst)
if os.environ.get("ONLY_FRAMES"):
    sys.exit(0)

# ---------------------------------------------------------------- 3. captions (Kanit Black 88 at y 900)
caps = json.load(open(SCR + "captions.json"))
ass = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: 720", "PlayResY: 1280", "WrapStyle: 2", "", "[V4+ Styles]",
       "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
       "Style: Pop,Kanit Black,88,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,5,0,5,30,30,0,1", "", "[Events]",
       "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
ts = lambda t: "%d:%02d:%05.2f" % (int(t // 3600), int(t % 3600 // 60), t % 60)
for c in caps:
    a = c["t"] + OFF; b = min((c["end"] if c["end"] else T) + OFF, T)
    if a >= T: continue
    ass.append("Dialogue: 0,%s,%s,Pop,,0,0,0,,{\\pos(360,900)}%s" % (ts(a), ts(b), c["text"]))
open(out + ".ass", "w").write("\n".join(ass))
subprocess.run(["ffmpeg", "-y", "-v", "error", "-framerate", "30", "-i", FR + "/f_%04d.png", "-vf", "ass=%s.ass:fontsdir=%s/fonts" % (out, P),
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "17", "-movflags", "+faststart", out + "_silent.mp4"], check=True)

# ---------------------------------------------------------------- 4. sound: SFX cue list (narration times + 0.10), beds, ducking
SF = P + "/film24/audio/sfx/"
sfx = []
def add(f, t, db, ln, **k):
    if t < T: sfx.append(dict({"file": SF + f + ".mp3", "at": t, "peak_db": db, "len": min(ln, T - t), "align": "onset", "fade_out": 0.08}, **k))
CUES = [
    # shot 1-2: hammer clinks on the strike frames of s01 (every 12 frames from g 13), smoke hiss on the dragon puff
    *[("hammer_clink", g / 30.0, -14, 0.6) for g in range(13, 78, 12)],
    ("smoke_hiss", 2.85, -22, 1.6), ("smoke_hiss", 3.9, -24, 1.4),
    ("whoosh", 5.0, -28, 0.6), ("war_drums", 5.4, -30, 4.2),                     # shot 3: fleet
    ("laugh_big", 14.55, -16, 2.4),                                               # shot 5
    ("crowd_laugh", 21.6, -20, 2.6),                                              # shot 7
    ("hammer_clink", 26.5, -14, 0.6), ("hammer_clink", 27.7, -14, 0.6), ("hammer_clink", 28.4, -14, 0.6),   # spike rows
    ("port_thunk", 29.65, -16, 1.2),                                              # gun ports
    ("oar_splash", 30.75, -16, 0.9), ("oars_rowing", 31.8, -26, 1.6),             # shot 9a / 9
    ("war_drums", 37.2, -24, 4.5),                                                # shot 11 chase
    ("gulp", 44.6, -18, 0.6), ("ladder_clatter", 45.6, -20, 1.0),                 # shot 12
    ("whoosh", 47.1, -26, 0.6), ("cannon_boom", 52.1, -14, 1.6), ("cannon_volley", 52.6, -16, 4.0),   # shot 13 reveal
    ("wood_creak", 53.7, -24, 3.0),                                               # shot 14
    ("whoosh", 57.25, -24, 0.5),                                                  # tally pop
    ("splash_small", 59.0, -20, 1.4), ("sand_crawl", 62.2, -18, 2.0),             # shot 15
]
BEDS = [("yard_ambience", 0, 5.02), ("sea_fleet", 5.02, 9.6), ("yard_ambience", 9.6, 14.37), ("sea_fleet", 14.37, 24.45),
        ("yard_ambience", 24.45, 30.64), ("sea_fleet", 30.64, 64.9)]
if VER == "C":
    D = SH / 30.0
    CUES = [c for c in CUES if c[1] < 24.45] + [(f, t + D, db, ln) for f, t, db, ln in CUES if t >= 30.64 and not (50.0 < t < 53.0)]
    CUES += [  # build-up: one punchy hit per stage (g / 30)
        ("build_slam", 781 / 30, -13, 0.9), ("build_planks", 800 / 30, -18, 1.2), ("build_oars", 830 / 30, -14, 1.0),
        ("build_cannon", 862 / 30, -15, 1.2), ("build_plates", 898 / 30, -15, 1.1), ("build_spikes", 932 / 30, -15, 1.2),
        ("build_slam", 971 / 30, -15, 0.9), ("build_dragon", 1001 / 30, -14, 1.8), ("cannon_boom", 1052 / 30, -12, 1.6),
        ("build_hit", 1084 / 30, -12, 1.8),
        # 13b broadside (old 50.95.. +D), 13c the hit + jumpers
        *[("cannon_boom", t + D, -13, 1.4) for t in (50.98, 51.28, 51.58, 51.88)],
        ("explosion_big", 1767 / 30, -10, 2.2), ("debris_rain", 1770 / 30, -20, 1.6), ("splash_small", 1795 / 30, -18, 1.2),
        ("cannon_volley", 52.6 + D, -18, 3.5)]
    BEDS = [(n, a_ if a_ < 24.45 else a_ + (D if a_ >= 30.64 else 0), b_ if b_ < 24.45 else b_ + D) for n, a_, b_ in BEDS]
    BEDS = [b for b in BEDS if b[0] != "yard_ambience" or b[1] != 24.45] + [("yard_ambience", 24.45, 37.57)]
for f, t, db, ln in CUES:
    add(f, t, db, ln)
for n, a_, b_ in BEDS:
    t = a_
    while t < b_ - 0.5:
        sfx.append({"file": SF + n + ".mp3", "at": t, "rms_db": -40, "len": min(5.0, b_ - t), "align": "start", "fade_in": 0.2, "fade_out": 0.4}); t += 4.8
V = AUD + ("narration.wav" if VER == "C" else "narration_65s.wav")
_v = np.frombuffer(subprocess.run(["ffmpeg", "-v", "error", "-i", V, "-ac", "1", "-ar", "8000", "-f", "f32le", "-"], capture_output=True).stdout, np.float32)
_env = np.sqrt(np.convolve(_v ** 2, np.ones(800) / 800, "same"))[::80]
def talk(a, ln):
    seg = _env[max(0, int((a - OFF) * 100)):max(0, int((a - OFF + ln) * 100))]
    return seg.size > 0 and (seg > 0.02).mean() > 0.3
for x in sfx:
    k = "peak_db" if "peak_db" in x else "rms_db"
    if talk(x["at"], x["len"]):
        x[k] -= 6 if x["len"] < 3 else 3
        if any(s in x["file"] for s in ("laugh", "gulp", "drums", "volley")): x[k] -= 4
vr = 20 * np.log10(np.sqrt((_v ** 2).mean()) + 1e-9)
spec = {"duration": T, "out_wav": out + ".wav", "video_in": out + "_silent.mp4", "video_out": out + ".mp4",
        "voice": {"file": V, "at": OFF, "gain": float(10 ** ((-17.4 - vr) / 20))},
        "music": {"file": os.environ.get("MUSICF", P + "/film24/audio/music_temp.mp3"), "at": 0, "rms_db": float(os.environ.get("MUSIC_DB", "-31")),
                  "fade_in": 0.3, "fade_out": 0.6},
        "sfx": sfx}
json.dump(spec, open(out + "_mix.json", "w"), indent=1)
subprocess.run([sys.executable, P + "/audio/mixer.py", out + "_mix.json"], check=True)
print("done:", out + ".mp4", "missing frames:", len(missing))
