#!/usr/bin/env python3
"""Film 15 conform (adapted from conform15.py): take.mkv frames -> captions -> narration + music + SFX mix -> loudness-normalised mp4.

usage: python3 film/conform15.py [options] [TAKE_DIR_OR_LISTFILE ...]     (default takes: film/v3/film15/s*)
  --test        no takes needed: renders captions over a grey placeholder video of full length + the full audio mix
  --name NAME   output basename (default film15_test)  -> film/release15/NAME.mp4 + NAME_report.json
  --n N         frame count (default 2095 = 69.83 s)
  --work DIR    scratch dir (default /tmp/conform15_work/NAME), --keep keeps it, --target LUFS (default -12)
Takes: each contributes frames g0..g1 (meta g1 inclusive), ordered by first_g, later override earlier; transition_in dissolve blends centred on g0
(string transition_in is normalised to a dict); uncovered frames fall back to a handle frame, else a grey MISSING placeholder.
SFX: film15/audio/sfx_cues.json, times on the narration clock (+0.10 s added here). Music: film15/audio/music_suno.wav else none (warning).
"""
import sys, os, re, json, glob, shutil, argparse, subprocess
import numpy as np
from PIL import Image, ImageDraw, ImageFont

P = os.path.dirname(os.path.abspath(__file__)); F15 = P + "/film15"; FPS = 30; OFF = 0.10; SR = 48000
ap = argparse.ArgumentParser(); ap.add_argument("takes", nargs="*"); ap.add_argument("--test", action="store_true"); ap.add_argument("--name", default="film15_test")
ap.add_argument("--n", type=int, default=2095); ap.add_argument("--work"); ap.add_argument("--keep", action="store_true"); ap.add_argument("--target", type=float, default=-12.0)
a = ap.parse_args(); N = a.n; T = N / FPS; name = a.name
work = a.work or f"/tmp/conform15_work/{name}"; os.makedirs(work, exist_ok=True)
rel = P + "/release15"; os.makedirs(rel, exist_ok=True)
run = lambda cmd, **k: subprocess.run(cmd, check=True, **k)

# ---------- 1. takes ----------
dirs = []
if not a.takes and not a.test: a.takes = sorted(glob.glob(P + "/v3/film15/s*"))
for t in ([] if a.test else a.takes):
    if os.path.isfile(t):
        dirs += [os.path.abspath(l.strip()) for l in open(t) if l.strip() and not l.startswith("#")]
    else: dirs.append(os.path.abspath(t))
def norm_ti(ti):
    if isinstance(ti, str):
        m = re.search(r"(\d+)", ti); return {"type": "dissolve" if "dissolve" in ti else "cut", "frames": int(m.group(1)) if m else 0}
    return ti or {"type": "cut", "frames": 0}
TK = []
for d in dirs:
    m = json.load(open(d + "/meta.json")); m["name"] = m.get("take") or os.path.basename(d); m["ti"] = norm_ti(m.get("transition_in"))
    fr = f"{work}/{m['name']}"; os.makedirs(fr, exist_ok=True)
    if not glob.glob(fr + "/g_*.png"):
        mkv = d + "/take.mkv"
        if not os.path.exists(mkv):
            parts = sorted(glob.glob(d + "/take.mkv.part*")); assert parts, f"no take.mkv or parts in {d}"
            mkv = fr + "/take.mkv"
            with open(mkv, "wb") as o:
                for p in parts: o.write(open(p, "rb").read())
        run(["ffmpeg", "-v", "error", "-y", "-i", mkv, "-start_number", str(m["first_g"]), "-compression_level", "1", fr + "/g_%04d.png"])
        if mkv.startswith(fr): os.remove(mkv)
    m["have"] = {int(f[-8:-4]): f for f in glob.glob(fr + "/g_*.png")}
    if len(m["have"]) != m["n_frames"]: print(f"WARN {m['name']}: decoded {len(m['have'])} frames, meta says {m['n_frames']}")
    TK.append(m)
TK.sort(key=lambda m: m["first_g"])
owner = {}
for m in TK:
    for g in range(m["g0"], min(m["g1"] + 1, N)): owner[g] = m   # meta g1 is INCLUSIVE (s01: g1 183 + 6 handle = first_g 0 + n_frames 190)
SHOTS = [(1,0,2.1),(2,2.1,3.6),(3,3.6,4.45),(4,4.45,6.15),(5,6.15,8.2),(6,8.2,11.45),(7,11.45,13.25),(8,13.25,14.15),(9,14.15,16.3),(10,16.3,18.8),(11,18.8,20.7),(12,20.7,23.6),(13,23.6,25.4),(14,25.4,27.95),(15,27.95,28.73),(16,28.73,31.05),(17,31.05,32.5),(18,32.5,33.8),(19,33.8,35.27),(20,35.27,37.5),(21,37.5,38.35),(22,38.35,39.65),(23,39.65,42.3),(24,42.3,44.3),(25,44.3,46.4),(26,46.4,49.0),(27,49.0,50.35),(28,50.35,52.85),(29,52.85,55.08),(30,55.08,58.2),(31,58.2,60.15),(32,60.15,62.5),(33,62.5,64.62),(34,64.62,66.25),(35,66.25,68.0),(36,68.0,69.84)]
font = ImageFont.truetype(P + "/fonts/WorkSans-Black.ttf", 44)
def placeholder(g, path):
    t = g / FPS; sh = [s for s in SHOTS if s[1] <= t < s[2]] or [SHOTS[-1]]; s = sh[0]
    im = Image.new("RGB", (720, 1280), (118, 118, 118)); d = ImageDraw.Draw(im)
    for i, txt in enumerate(["MISSING TAKE", f"expected take s{s[0]:02d}", f"shot {s[0]}  {s[1]:.2f}-{s[2]:.2f} s", f"g {g}  (t {t:.2f} s)", "PLACEHOLDER"]):
        d.text((360, 470 + i * 70), txt, fill=(255, 255, 255) if i != 4 else (255, 220, 0), font=font, anchor="mm")
    d.rectangle([4, 4, 715, 1275], outline=(255, 0, 0), width=8); im.save(path)
fdir = work + "/frames"
if not a.test: shutil.rmtree(fdir, ignore_errors=True); os.makedirs(fdir)
blends = fallback = 0; missing = []
def px(path): return np.asarray(Image.open(path).convert("RGB"), float)
for g in ([] if a.test else range(N)):
    dst = f"{fdir}/f_{g:04d}.png"; m = owner.get(g); done = False
    if m is not None and m["ti"]["type"] == "dissolve" and m["ti"]["frames"] > 0:
        n = m["ti"]["frames"]; a0 = m["g0"] - n // 2
        if a0 <= g < a0 + n:
            prev = [p for p in TK if p is not m and p["first_g"] < m["first_g"] and g in p["have"]]
            if prev and g in m["have"]:
                p_ = (g - a0 + 1) / (n + 1); p_ = p_ * p_ * (3 - 2 * p_)
                Image.fromarray(np.clip(px(prev[-1]["have"][g]) * (1 - p_) + px(m["have"][g]) * p_ + 0.5, 0, 255).astype(np.uint8)).save(dst); blends += 1; done = True
    if done: continue
    if m is not None and g in m["have"]: os.symlink(m["have"][g], dst); continue
    cand = [p for p in TK if g in p["have"]]
    if cand: os.symlink(cand[0]["have"][g], dst); fallback += 1; continue
    missing.append(g); placeholder(g, dst)
def ranges(l):
    out = []
    for g in l:
        if out and g == out[-1][1] + 1: out[-1][1] = g
        else: out.append([g, g])
    return out
print("takes:", [(m["name"], m["g0"], m["g1"]) for m in TK]); print(f"dissolve blends {blends}, handle fallbacks {fallback}, placeholder frames {len(missing)} {ranges(missing)}")

# ---------- 2. captions ----------
caps = json.load(open(F15 + "/script/captions.json"))
ass = ["[Script Info]", "ScriptType: v4.00+", "PlayResX: 720", "PlayResY: 1280", "WrapStyle: 2", "", "[V4+ Styles]",
 "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
 "Style: Pop,Kanit Black,88,&H00FFFFFF,&H00FFFFFF,&H00000000,&H80000000,0,0,0,0,100,100,0,0,1,5,0,5,30,30,0,1", "", "[Events]",
 "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text"]
ts = lambda t: f"{int(t//3600)}:{int(t%3600//60):02d}:{t%60:05.2f}"
tim = json.load(open(F15 + "/audio/timing.json")); last_end = tim["sent_end"][-1]
for i, c in enumerate(caps):
    if c.get("end") is None: c["end"] = caps[i + 1]["t"] if i + 1 < len(caps) else last_end   # missing end -> next phrase / end of narration
    s0 = max(0.0, c["t"]) + OFF; e0 = min(c["end"] + OFF, T)
    if s0 >= T: continue
    ass.append(f"Dialogue: 0,{ts(s0)},{ts(e0)},Pop,,0,0,0,,{{\\pos(360,900)}}{c['text']}")
open(work + "/cap.ass", "w", encoding="utf8").write("\n".join(ass))
silent = work + "/silent.mp4"
src_in = ["-f", "lavfi", "-i", f"color=c=0x404040:s=720x1280:r={FPS}:d={T:.3f}"] if a.test else ["-framerate", str(FPS), "-i", fdir + "/f_%04d.png"]
run(["ffmpeg", "-y", "-v", "error"] + src_in + [ "-vf", f"ass={work}/cap.ass:fontsdir={P}/fonts", "-frames:v", str(N), "-c:v", "libx264", "-pix_fmt", "yuv420p", "-crf", "17", "-movflags", "+faststart", silent])

# ---------- 3. audio ----------
sys.path.insert(0, P + "/audio"); import mixer
NARR = F15 + "/audio/narration.wav"; SFXD = F15 + "/audio/sfx/"
VOICE_DB, MUSIC_DB = -14.4, -31.0
nx = mixer.load(NARR); narr_db = 20 * np.log10(np.sqrt((nx ** 2).mean()) + 1e-12); gain = 10 ** ((VOICE_DB - narr_db) / 20)
v = nx.mean(1)[::6]; env = np.sqrt(np.convolve(v ** 2, np.ones(480) / 480, "same"))[::8]   # 8 kHz -> 100 Hz envelope, as conform9
def talk(at, ln):
    i0, i1 = int((at - OFF) * 100), int((at - OFF + ln) * 100); seg = env[max(0, i0):max(0, i1)]
    return seg.size > 0 and (seg > 0.02).mean() > 0.3
cues = json.load(open(F15 + "/audio/sfx_cues.json"))["cues"]; sfx = []
for c in cues:
    c = dict(c, at=c["at"] + OFF)   # narration clock -> film clock
    if c["at"] >= T: continue
    if "until" in c: c["until"] = min(c["until"] + OFF, T)
    base = {"fade_in": c.get("fade_in", 0.005), "fade_out": c.get("fade_out", 0.03)}
    for k in ("peak_db", "rms_db", "align"):
        if k in c: base[k] = c[k]
    if c.get("until"):   # tiled bed
        step = 19.5; t0 = c["at"]
        while t0 < min(c["until"], T) - 0.5:
            e = dict(base, file=SFXD + c["file"], at=t0, len=min(20.0, min(c["until"], T) - t0), kind="bed", fade_in=0.5 if t0 > 0 else 0.3, fade_out=0.5 if t0 + step < c["until"] else 0.6); sfx.append(e); t0 += step
    else:
        ln = min(c.get("len", 3.0), T - c["at"]); sfx.append(dict(base, file=SFXD + c["file"], at=c["at"], len=ln, kind=c.get("kind", "sfx")))
for x in sfx:
    if talk(x["at"], x["len"]):
        x["peak_db" if "peak_db" in x else "rms_db"] += -3 if x["kind"] == "bed" or x["len"] >= 3 else -6
        if any(k in x["file"] for k in ("laugh", "crowd")): x["peak_db" if "peak_db" in x else "rms_db"] -= 4
    del x["kind"]
spec = {"duration": T, "out_wav": work + "/mix.wav", "voice": {"file": NARR, "at": OFF, "gain": gain}, "sfx": sfx}
MUSIC = F15 + "/audio/music_suno.wav"; music_used = os.path.exists(MUSIC)
if music_used: spec["music"] = {"file": MUSIC, "at": 0, "rms_db": MUSIC_DB, "fade_in": 0.3, "fade_out": 0.6}
else: print("\n" + "!" * 78 + "\nWARNING: film15/audio/music_suno.wav NOT FOUND -> SILENT MUSIC PLACEHOLDER (no music bed in this render).\nDo not release; re-run conform15.py once the Suno track is in place.\n" + "!" * 78 + "\n")
json.dump(spec, open(work + "/mix.json", "w"), indent=1)
mixer.main(spec)

def ebur(path):
    r = subprocess.run(["ffmpeg", "-nostats", "-i", path, "-af", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    s = r[r.rfind("Summary:"):]; g = lambda k: float(re.search(k + r":\s+(-?[\d.]+)", s).group(1))
    return g("I"), g("Peak")   # integrated LUFS, true peak dBTP
I0, TP0 = ebur(work + "/mix.wav"); print(f"mix before normalisation: {I0:.1f} LUFS, TP {TP0:.1f} dBTP")
# gain to target, then true-peak-safe limiter; iterate (limiter eats a little loudness)
norm = work + "/norm.wav"; tgt = a.target; I1 = TP1 = None
for it in range(6):
    g_db = tgt - I0 if it == 0 else g_db + (a.target - I1)
    run(["ffmpeg", "-y", "-v", "error", "-i", work + "/mix.wav", "-af", f"volume={g_db:.2f}dB,alimiter=limit=0.72:attack=3:release=50:level=disabled,aresample={SR}", "-ar", str(SR), "-c:a", "pcm_s16le", norm])
    I1, TP1 = ebur(norm)
    if abs(I1 - a.target) < 0.3 and TP1 <= -1.6: break
print(f"final audio: {I1:.1f} LUFS, TP {TP1:.1f} dBTP (gain {g_db:+.1f} dB, {it+1} passes)")
out = f"{rel}/{name}.mp4"
run(["ffmpeg", "-y", "-v", "error", "-i", silent, "-i", norm, "-map", "0:v:0", "-map", "1:a:0", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", "-movflags", "+faststart", out])
nfr = int(subprocess.run(["ffprobe", "-v", "error", "-count_frames", "-select_streams", "v:0", "-show_entries", "stream=nb_read_frames", "-of", "csv=p=0", out], capture_output=True, text=True).stdout.strip())
Ifin, TPfin = ebur(out)
ok = (-14 <= Ifin <= -11) and TPfin <= -1.0 and nfr == N and (a.test or not missing)
rep = {"output": out, "frames": nfr, "expected_frames": N, "duration_s": T, "lufs": Ifin, "true_peak_dbtp": TPfin, "lufs_ok": -14 <= Ifin <= -11, "tp_ok": TPfin <= -1.0,
       "music_used": music_used, "mode": "TEST (grey placeholder video)" if a.test else "release", "music_WARNING": None if music_used else "SILENT PLACEHOLDER - music_suno.wav missing", "takes": [(m["name"], m["g0"], m["g1"]) for m in TK],
       "placeholder_ranges": ranges(missing), "handle_fallback_frames": fallback, "dissolve_blend_frames": blends, "sfx_events": len(sfx), "narration_rms_db": narr_db, "pass": ok}
json.dump(rep, open(f"{rel}/{name}_report.json", "w"), indent=1)
print(json.dumps(rep, indent=1))
if not a.keep: shutil.rmtree(work, ignore_errors=True)
